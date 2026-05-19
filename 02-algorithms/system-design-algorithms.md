# System Design Algorithms — SDE-3 Gold Standard

These are the "Big Tech" algorithms that power distributed systems. While standard DSA (DP, Graphs) tests logic, these test your ability to build scalable, resilient infrastructure.

---

## Complexity & Properties at a Glance

| Algorithm | Space | Time per op | Error / Accuracy | Deletions |
|-----------|-------|------------|-----------------|-----------|
| Bloom Filter | O(m bits) | O(k) hash ops | FP rate ~(1-e^(-kn/m))^k | No (use Cuckoo Filter) |
| HyperLogLog | O(log log n) | O(1) | ~2% with m=2^14 registers | No |
| Consistent Hashing | O(n + vn) | O(log n) lookup | — | Yes (remove node) |
| Count-Min Sketch | O(w·d) | O(d) | Over-estimates by ε | No |
| Token Bucket | O(1) | O(1) | — | N/A |

---

## 1. Membership & Cardinality (The "Is it there?" Problems)

### Bloom Filters
- **What**: A space-efficient probabilistic data structure used to test if an element is in a set.
- **Why**: Standard `Set` is too large to fit in memory for billions of URLs.
- **Click Moment**: "Check if a username is taken without hitting the DB", "Filtering malicious URLs", "Avoiding expensive disk lookups for non-existent keys (BigTable/Cassandra)".
- **Trade-off**: **False Positives** are possible; **False Negatives** are impossible. You cannot delete from a standard Bloom Filter (use a Cuckoo Filter instead).
- **Tuning**: `m` = bit array size; `k` = hash functions. Optimal `k = (m/n) * ln(2)`. FP rate falls as `m` grows and `k` is tuned.

```python
import mmh3
from bitarray import bitarray

class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        self.size = size
        self.num_hashes = num_hashes
        self.bits = bitarray(size)
        self.bits.setall(0)

    def add(self, item: str):
        for seed in range(self.num_hashes):
            idx = mmh3.hash(item, seed) % self.size
            self.bits[idx] = 1

    def __contains__(self, item: str) -> bool:
        return all(self.bits[mmh3.hash(item, s) % self.size]
                   for s in range(self.num_hashes))
```

**Interview follow-ups:**
- "What if we need deletions?" → Counting Bloom Filter (each bit → counter) or Cuckoo Filter.
- "How do you choose m and k?" → FP rate formula; typically 10 bits/element and k=7 gives ~1% FP rate.

### HyperLogLog (HLL)
- **What**: Estimates the number of *unique* elements in a multiset.
- **Why**: Counting unique visitors (DAU) for 1 billion users would require gigabytes of memory; HLL does it in **1.5 KB** with 2% error.
- **Logic**: Hash each element; observe the maximum number of leading zeros across m register buckets. `estimate = α * m² * harmonic_mean(2^(-M_j))`.
- **Real-world**: Redis `PFADD` / `PFCOUNT` uses HLL. Google Analytics, Cassandra cardinality estimation.
- **Interview soundbite**: "HLL trades perfect accuracy for 99%+ accuracy at ~1000× memory reduction. Error is predictable (~2%) and configurable by m."

---

## 2. Load Balancing & Distribution

### Consistent Hashing
- **What**: Maps both "Nodes" and "Keys" to a circular 360° hash ring.
- **Why**: Traditional `hash(key) % N` causes a massive reshuffle if one node dies (N changes). Consistent hashing only reshuffles `1/N` keys.
- **Click Moment**: "Scaling a cache layer", "Distributed KV store (Dynamo/Cassandra)".
- **Deep Dive**: Use **Virtual Nodes** (each physical node → V positions on ring) to ensure uniform distribution and handle heterogeneous hardware.

```python
import hashlib
import bisect

class ConsistentHashRing:
    def __init__(self, virtual_nodes=100):
        self.ring = {}        # hash_position → node
        self.sorted_keys = [] # sorted list of hash positions
        self.virtual_nodes = virtual_nodes

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node: str):
        for i in range(self.virtual_nodes):
            vkey = self._hash(f"{node}#{i}")
            self.ring[vkey] = node
            bisect.insort(self.sorted_keys, vkey)

    def remove_node(self, node: str):
        for i in range(self.virtual_nodes):
            vkey = self._hash(f"{node}#{i}")
            del self.ring[vkey]
            self.sorted_keys.remove(vkey)

    def get_node(self, key: str) -> str:
        if not self.ring:
            return None
        h = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, h) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]
```

**Interview follow-ups:**
- "Why virtual nodes?" → Without them, one node failure causes uneven load. 100–200 vnodes per physical node is typical.
- "What moves when a node is added?" → Only keys between the new node and its predecessor on the ring (~1/N of total keys).

### Rendezvous Hashing (Highest Random Weight)
- **What**: For each key, calculate a hash with every node ID. Assign the key to the node that produces the highest weight.
- **Why**: Better than Consistent Hashing when the set of nodes is small and changes frequently. No ring to maintain.
- **Trade-off**: O(n) per lookup (must score all nodes) vs O(log n) for consistent hashing ring lookup. Preferred for CDN node selection, small cluster proxies.

---

## 3. Rate Limiting & Flow Control

### Token Bucket
- **What**: A bucket holds tokens, refilled at a constant rate. Each request consumes a token.
- **Why**: Allows for **bursts** (up to bucket size) while maintaining a long-term average rate.
- **Use case**: API rate limiting at the gateway level.

```python
import time

class TokenBucket:
    def __init__(self, rate: float, capacity: int):
        self.rate = rate          # tokens per second
        self.capacity = capacity  # max burst size
        self.tokens = capacity
        self.last_refill = time.time()

    def allow(self) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_refill = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

### Leaky Bucket
- **What**: Requests enter a queue; they are processed at a constant output rate.
- **Why**: Smooths out traffic. No bursts allowed.
- **Use case**: Traffic shaping in networking.

### Sliding Window Counter (most interview-relevant)
- **What**: Track request count in a rolling time window using a circular log of timestamps or a Redis sorted set.
- **Why**: More accurate than fixed window (avoids boundary burst), cheaper than token bucket for per-user rate limiting.
- **Implementation**: `ZADD user:requests <now> <request_id>` + `ZREMRANGEBYSCORE` to evict old entries + `ZCARD` to count.

### Comparison

| Algorithm | Burst allowed | Accuracy | Distributed? | Complexity |
|-----------|-------------|----------|-------------|-----------|
| Token bucket | Yes (up to capacity) | Eventual avg rate | Yes (atomic counter) | O(1) |
| Leaky bucket | No | Exact output rate | Yes (queue-based) | O(1) |
| Fixed window | Boundary burst | Simple | Yes | O(1) |
| Sliding window | No | Most accurate | Yes (Redis sorted set) | O(log n) |

---

## 4. Distributed Consensus & Coordination

### Paxos / Raft
- **What**: Algorithms to reach consensus across multiple unreliable nodes.
- **Why**: Essential for "Leader Election" and "Distributed Locking". If 3/5 nodes agree, the value is committed.
- **Interview Soundbite**: "Raft is preferred for its readability; Paxos is the original proof. Both ensure safety (no two leaders) and liveness (eventual progress)."

**Raft phases:**
1. **Leader Election**: Nodes start as Followers. On timeout, become Candidate → broadcast `RequestVote`. Majority wins → becomes Leader.
2. **Log Replication**: Leader sends `AppendEntries` to all followers. Committed once majority acknowledges.
3. **Safety**: A leader can only be elected if it has the most up-to-date log (prevents overwriting committed entries).

**Key properties:**
- Quorum = ⌊N/2⌋ + 1. With 5 nodes, tolerate 2 failures.
- Split-brain: prevented by requiring quorum for any decision.
- Leader lease: leader sends heartbeats every 150ms; follower timeout = 300–500ms.

### Vector Clocks / Lamport Timestamps
- **What**: Tracking logical time in a distributed system.
- **Why**: Physical clocks drift (skew). Logical clocks track "happened-before" relationships.
- **Use case**: Conflict resolution in multi-master databases (Dynamo).

**Lamport**: Single counter. Increment on send; `max(local, received) + 1` on receive. Establishes partial order but can't detect concurrent events.

**Vector Clocks**: Array of counters, one per node. `V[i]` = events node i has seen. Two events are concurrent if neither vector dominates the other. Used by Dynamo, Riak for conflict detection.

### CAP Theorem (interview must-know)
- **C**onsistency: every read returns the most recent write.
- **A**vailability: every request gets a (possibly stale) response.
- **P**artition tolerance: system continues despite network splits.
- Cannot have all three. Real choice: **CP** (Zookeeper, HBase, Spanner) or **AP** (Cassandra, DynamoDB, CouchDB).
- Modern framing: **PACELC** — during normal ops, trade-off between latency (L) and consistency (C).

---

## 5. Sketching & Frequency

### Count-Min Sketch
- **What**: A 2D array of counters (width w × depth d). Like a Bloom Filter but stores frequencies instead of membership.
- **Why**: "Top K trending hashtags" or "Identify heavy hitters" in a stream of millions of events.
- **Logic**: Use `d` independent hash functions; for `add(x)`, increment `table[i][h_i(x)]` for each row. Estimated frequency = `min(table[i][h_i(x)])`. Over-estimates (due to collisions) but **never underestimates**.
- **Error bounds**: With `w = e/ε` and `d = ln(1/δ)`, estimate is within `ε * N` of true count with probability ≥ 1−δ.

```python
import mmh3

class CountMinSketch:
    def __init__(self, width: int, depth: int):
        self.w = width
        self.d = depth
        self.table = [[0] * width for _ in range(depth)]

    def add(self, item: str, count: int = 1):
        for i in range(self.d):
            j = mmh3.hash(item, i) % self.w
            self.table[i][j] += count

    def estimate(self, item: str) -> int:
        return min(self.table[i][mmh3.hash(item, i) % self.w]
                   for i in range(self.d))
```

### Quadtrees / Geohash
- **What**: Spatial indexing.
- **Why**: "Find nearest restaurants", "Uber driver matching".
- **Quadtree**: Recursively divide 2D space into 4 quadrants until each cell has ≤ threshold points. Supports O(log n) range and nearest-neighbor queries.
- **Geohash**: Encodes a 2D point into a 1D Base32 string by interleaving bits of lat/lng. Longer prefix = tighter bounding box. Adjacent cells share prefix (mostly) — enables fast neighbor lookup via prefix search.
- **Trade-off**: Geohash is simpler (string ops) but has boundary anomalies — points near a cell boundary have different hashes. Quadtrees handle this naturally but need more infra.

---

## 6. Storage & Indexing

### LSM Trees (Log-Structured Merge)
- **Used in**: Cassandra, RocksDB, LevelDB, HBase.
- **Write path**: Write to in-memory memtable → flush to immutable SSTable on disk → periodic compaction merges SSTables.
- **Read path**: Check memtable → bloom filter to skip SSTables → binary search within SSTable.
- **Trade-off**: Write-optimized (O(1) amortized writes). Reads slower than B-Trees (multiple SSTables). Bloom filters reduce unnecessary disk reads.

### B-Trees
- **Used in**: PostgreSQL, MySQL InnoDB, SQLite.
- **Structure**: Balanced tree with n keys and n+1 pointers per node; node size = disk page (4-16KB).
- **Trade-off**: Read-optimized. O(log n) reads AND writes. Updates in-place (vs LSM's append-only).
- **When to mention**: "Traditional RDBMS indexes", "range scans on primary key", "OLTP workloads".

### Comparison: LSM vs B-Tree

| Property | LSM Tree | B-Tree |
|----------|----------|--------|
| Write performance | Excellent (sequential) | Good (random I/O) |
| Read performance | Good (with bloom filters) | Excellent |
| Space amplification | High (before compaction) | Low |
| Write amplification | Low initially, higher during compaction | Moderate |
| Best for | Write-heavy (time-series, logs) | Read-heavy (OLTP) |

---

## Quick Revision Triggers
- "Count unique visitors at scale" → HyperLogLog.
- "Is this key in the database?" → Bloom Filter.
- "Add/Remove servers without reshuffling data" → Consistent Hashing.
- "Find top-K in a stream" → Count-Min Sketch.
- "Proximity search / Uber" → Quadtree / Geohash.
- "Leader election" → Raft / Paxos.
