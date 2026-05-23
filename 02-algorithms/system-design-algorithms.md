---
module: 02-algorithms
topic: System Design Algorithms
subtopic: 
status: unread
tags: [algorithms, upsc, system-design-algorithms]
---
## First-Principles Map

```
WHY system design algos → WHAT they are → HOW they work → WHEN to use → WHAT can go wrong
       │                        │                │               │               │
  [Distributed systems         [probabilistic    [HLL: count     [unique visitor  [HLL: hash
   can't afford exact           and approximation distinct with   count; membership collisions cause
   counting at scale;           structures that   O(log log n)    testing (Bloom); overcount; Bloom
   single-server structures     trade accuracy    space; Bloom:   load balancing   false positives
   don't survive node           for speed and     bit array +     (consistent      grow with load
   failures; naive hashing      scale; consensus  k hashes; CMS:  hash); top-K     factor; CMS
   creates hotspots]            protocols for     count sketch     (Count-Min);    overestimates,
                                distributed       matrix; CH:     leader election  never under;
                                agreement]        sorted ring]    (Raft/Paxos)]   Raft log gaps]
       │                        │                │
  [real-world:                 [invariant:       [Consistent Hashing: sort servers
   Cassandra ring (CH);         HLL estimates     + keys on ring; O(log n) lookup
   Redis HLL for uniques;       within 2% error   via binary search; vnodes spread
   Kafka leader election         for >1M items;    load; key migrates to next server
   (Raft); CDN routing           Bloom never       on add/remove — only k/n keys
   (consistent hash)]           false negatives]  remapped instead of all]
       ↓
[Decision: Which system design algorithm]
  ├── Count distinct at scale → HyperLogLog (2% error, O(log log n) space)
  ├── Membership test         → Bloom Filter (no false negatives, tunable FPR)
  ├── Frequency in stream     → Count-Min Sketch (overestimate, not underestimate)
  ├── Distribute load         → Consistent Hashing + virtual nodes
  └── Distributed consensus   → Raft (understandable) or Paxos (proven)
```

## First-Principles Breakdown
- **Root problem**: Exact data structures don't scale to billions of events per second or across hundreds of nodes — approximation and distribution are required.
- **Core insight**: Probabilistic structures (HLL, Bloom, CMS) trade bounded, tunable error for orders-of-magnitude less memory; consistent hashing trades perfect balance for minimal disruption on topology changes.
- **Invariant**: HLL: estimates are unbiased with relative error ε = 1.04/√m; Bloom: zero false negatives (no false misses); Count-Min: always overestimates, never underestimates.
- **Why it's fast**: HLL uses O(log log n) bits (not O(n)); Bloom tests membership in O(k) hash evaluations regardless of set size; consistent hash lookup is O(log n) binary search on the ring.
- **Where it breaks**: Bloom filters can't delete (use Counting Bloom Filter); HLL merges across shards only if same hash seed; Raft requires a stable leader — network partitions halt writes.

# System Design Algorithms — SDE-3 Gold Standard

```
System Design Algorithms — First Principles
│
├── WHY they exist
│   ├── Distributed systems can't use simple data structures
│   │   (no shared memory, nodes fail, network partitions happen)
│   ├── Scale demands: billions of events, petabytes of data, millions of nodes
│   └── Classical algorithms break down: hash(key)%N fails when N changes
│
├── WHAT they are (problem → algorithm mapping)
│   │
│   ├── Membership / cardinality ("is it there?" / "how many unique?")
│   │   ├── Bloom Filter        — probabilistic set membership, no false negatives
│   │   ├── Cuckoo Filter       — Bloom + deletions
│   │   └── HyperLogLog         — cardinality estimation in O(log log n) space
│   │
│   ├── Distribution / routing ("which node handles this key?")
│   │   ├── Consistent Hashing  — minimal reshuffling when nodes added/removed
│   │   ├── Rendezvous Hashing  — better for small, dynamic node sets
│   │   └── Chord DHT           — structured P2P overlay, O(log n) routing
│   │
│   ├── Rate limiting ("how many requests allowed?")
│   │   ├── Token Bucket        — burst-tolerant average rate
│   │   ├── Leaky Bucket        — smooth fixed-rate output
│   │   └── Sliding Window      — accurate rolling window count
│   │
│   ├── Consensus / coordination ("who is the leader?")
│   │   ├── Raft / Paxos        — leader election, log replication
│   │   ├── Vector Clocks       — happened-before, conflict detection
│   │   ├── Two-Phase Commit    — atomic cross-node transaction (blocking)
│   │   └── SAGA                — compensating transactions (non-blocking)
│   │
│   ├── Frequency / sketching ("top-K in a stream?")
│   │   ├── Count-Min Sketch    — frequency estimation, over-estimates only
│   │   └── Quadtree / Geohash  — spatial indexing for proximity queries
│   │
│   ├── Storage / indexing ("how is data stored on disk?")
│   │   ├── LSM Tree            — write-optimized; Cassandra, RocksDB
│   │   └── B-Tree              — read-optimized; PostgreSQL, MySQL
│   │
│   └── Integrity / sync ("is this replica consistent?")
│       ├── Merkle Tree         — efficient diff between replicas
│       └── Gossip Protocol     — decentralized membership propagation
│
├── HOW to pick (decision triggers)
│   ├── "Is X in set?" → Bloom Filter
│   ├── "Count unique" → HyperLogLog
│   ├── "Add/remove servers without reshuffling" → Consistent Hashing
│   ├── "Top-K in stream" → Count-Min Sketch + heap
│   ├── "Leader election" → Raft
│   ├── "Distributed transaction (across services)" → SAGA over 2PC
│   ├── "Are two replicas in sync?" → Merkle Tree
│   ├── "How do nodes discover each other?" → Gossip Protocol
│   └── "P2P routing (academic)" → Chord DHT
│
└── WHERE they appear (real systems)
    ├── Bloom Filter      → Cassandra, BigTable, Akamai CDN, Chrome Safe Browsing
    ├── HLL               → Redis PFCOUNT, Google Analytics, Cassandra
    ├── Consistent Hash   → DynamoDB, Cassandra, Memcached, CDN routing
    ├── Count-Min Sketch  → Twitter trending, Flink heavy hitters
    ├── Raft              → etcd, CockroachDB, TiKV, Consul
    ├── Merkle Tree       → DynamoDB anti-entropy, Git, Bitcoin
    ├── Gossip            → Cassandra, DynamoDB, SWIM protocol
    ├── 2PC               → XA transactions, Spanner (2PL + Paxos)
    └── SAGA              → Uber, Netflix, e-commerce order flows
```

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

## 7. Replica Integrity & Sync

### Merkle Trees

**What:** A binary tree where every leaf node = hash(data block) and every internal node = hash(left_child || right_child). The root hash summarizes the entire dataset.

**Why:** Comparing two large datasets (e.g. two database replicas) naively requires transferring all data. Merkle trees reduce this to O(log n) hashes — only exchange sub-trees that differ.

**How sync works:**
```
Replica A root hash ≠ Replica B root hash
  → Compare left subtree hashes → match
  → Compare right subtree hashes → mismatch
    → Go deeper → find the 3 leaf blocks that differ
    → Transfer only those 3 blocks
```

**Complexity:** O(log n) to identify differing blocks out of n total blocks. Network cost proportional to differences, not dataset size.

**Where used:**
- **DynamoDB / Riak:** Anti-entropy background sync. Each node builds Merkle tree per key range; exchange root hashes with neighbors; reconcile differences.
- **Git:** Every commit object hashes its tree of files. `git diff` finds divergence in O(changed files), not O(all files).
- **Bitcoin:** Merkle tree of transactions per block. Light clients verify a transaction without downloading the full block — just the Merkle proof path (O(log n) hashes).
- **Cassandra:** Anti-entropy repair (`nodetool repair`) uses Merkle trees to identify and sync out-of-sync SSTables.

**Interview trigger:** "How does DynamoDB detect inconsistency between replicas without comparing every row?" → Merkle trees for anti-entropy.

**Gotcha:** Merkle tree is built over a snapshot. It detects divergence as of tree construction time; you need periodic rebuilds (Cassandra) or event-driven updates (Git) to stay current.

---

## 8. Membership Propagation

### Gossip Protocol

**What:** A decentralized, epidemic-style communication protocol. Each node periodically picks k random peers and exchanges state. State converges across the cluster in O(log n) rounds.

**Why:** Centralized membership tracking (e.g. a ZooKeeper ensemble) is a bottleneck and SPOF at thousands of nodes. Gossip is O(log n) convergence with no coordinator.

**How it works:**
```
Every T seconds (e.g. 1s):
  Node A picks 3 random peers → sends its membership list + heartbeat counters
  Peers merge: for each node, keep the entry with the highest heartbeat
  Dead detection: if heartbeat for node X hasn't incremented in Φ * T seconds → mark suspect → dead
```

**Failure detection:** Each node maintains a heartbeat counter that it increments and gossips. If node X's counter is stale (hasn't increased beyond threshold `φ`), declare X dead. `φ` controls false-positive rate vs detection latency — tunable.

**Convergence:** With N nodes, gossip reaches all nodes in O(log N) rounds. Each round takes T seconds. At N=1000, T=1s: ~10 rounds → ~10s for full propagation.

**Where used:**
- **Cassandra:** SWIM-based gossip for node membership. Each node knows the entire ring state within seconds of a join/leave/failure.
- **DynamoDB:** Gossip for membership; combined with Merkle anti-entropy for data sync.
- **Consul / Serf:** SWIM protocol for cluster membership and health.
- **Redis Cluster:** Gossip for slot → node mapping propagation.

**SWIM protocol (Cassandra's variant):**
- Nodes send periodic `PING` to random peer
- If no `ACK`, send indirect `PING` via k other nodes
- If still no `ACK` → declare suspect → after timeout → dead
- Eliminates false positives from transient network hiccups

**Interview trigger:** "How does Cassandra know when a node goes down?" → Gossip + SWIM failure detection.

---

## 9. Distributed Transactions

### Two-Phase Commit (2PC)

**What:** A distributed atomic commit protocol with a coordinator and N participants.

**Phases:**
```
Phase 1 — Prepare:
  Coordinator → "Can you commit?" → all participants
  Participants → lock resources, write to redo log → "Yes" / "No"

Phase 2 — Commit (if all said Yes):
  Coordinator → "Commit" → all participants
  Participants → apply, release locks, ack

Phase 2 — Abort (if any said No):
  Coordinator → "Abort" → all participants
  Participants → rollback, release locks
```

**Guarantees:** Atomic — either all commit or all abort.

**Problems:**
- **Blocking:** If coordinator crashes after Phase 1 but before Phase 2, participants are stuck holding locks indefinitely (blocking protocol).
- **Single point of failure:** Coordinator crash = deadlock until coordinator recovers.
- **Latency:** 2 network round trips × number of participants. At high QPS, lock contention kills throughput.
- **Not partition-tolerant:** Network partition between coordinator and a participant → coordinator can't commit or abort → blocking.

**When to use 2PC:**
- Within a single database (Postgres distributed transactions use 2PC internally)
- Tight coupling tolerable: small number of participants, short transactions, same datacenter
- Google Spanner uses 2PC + Paxos — Paxos makes the coordinator itself fault-tolerant, partially mitigating the blocking problem

### SAGA — the microservices alternative

See SAGA section in `03-patterns/system-design.md`. Summary:
- Sequence of local transactions + compensating transactions for rollback
- No global locks → higher availability, eventual consistency
- Two variants: choreography (events) and orchestration (central coordinator)

### 2PC vs SAGA decision

| | 2PC | SAGA |
|-|-----|------|
| Atomicity | True atomic | Eventual (compensation) |
| Locks | Global, blocking | None (local only) |
| Partition tolerance | Low (blocking on partition) | High |
| Cross-service | Painful | Designed for it |
| Use when | Same DB / tight coupling | Microservices, long workflows |

**L4 soundbite:** "For cross-service transactions I'd use SAGA — 2PC across microservices holds distributed locks which can block indefinitely on coordinator failure. SAGA trades true atomicity for availability, with compensating transactions as rollback."

---

## 10. Primality & ID Generation Context

### Sieve of Eratosthenes

**What:** O(n log log n) algorithm to find all primes up to n. Cross off multiples of each prime iteratively.

```python
def sieve(n: int) -> list[int]:
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    return [i for i, v in enumerate(is_prime) if v]
```

**Why it matters for distributed ID generation:** Large prime numbers are used as hash table sizes (minimizes clustering) and in modular arithmetic for consistent hashing and fingerprinting. Snowflake IDs, UUID v4, and ULID are not prime-based, but hash-ring slot counts (e.g. Cassandra's 2^127 − 1 virtual tokens, Redis Cluster's 16383) are chosen to be prime or near-power-of-2 for distribution properties.

**Interview context:** If asked to design a distributed ID generator, know that:
- Twitter Snowflake: `timestamp(41b) | datacenter_id(5b) | machine_id(5b) | sequence(12b)` → 64-bit, time-sortable
- UUID v4: random 128-bit, not sortable — bad for DB index locality
- ULID: timestamp(48b) + random(80b), Base32 encoded, sortable — better for indexes

The sieve itself rarely appears in system design; it's more relevant if asked "how would you generate unique IDs at scale?" and you need to discuss prime-modulus hash tables.

---

## 11. Chord DHT (Distributed Hash Table)

**What:** A structured peer-to-peer overlay network that efficiently locates which node stores a given key. O(log n) lookup hops, O(log n) routing table size per node.

**Why:** In a naive P2P system, finding which node holds a key requires O(n) broadcast. Chord brings this to O(log n) with a structured ring and finger table.

**How it works:**
```
Nodes and keys are assigned IDs in [0, 2^m) (m-bit identifier space, e.g. 160-bit SHA-1).
Each node n is responsible for keys in (predecessor(n), n].

Finger table: node n stores shortcuts to nodes at positions
  n + 2^0, n + 2^1, n + 2^2, ..., n + 2^(m-1)  (mod 2^m)

Lookup(key k):
  If k is in (n, successor(n)] → found
  Else → forward to the largest finger ≤ k → repeat
  Converges in O(log n) hops
```

**Join/Leave:** When a node joins, it updates O(log n) finger tables. When a node leaves, its successor inherits its keys. Both operations are O(log^2 n).

**Replication:** Each key is replicated to the next r successors on the ring (r = replication factor).

**Where used:**
- Academic origin: MIT 2001 paper (Stoica et al.) — foundational for DynamoDB and Cassandra ring design
- BitTorrent DHT (Kademlia, a Chord variant) for tracker-less torrent discovery
- Early Skype peer discovery
- Cassandra's ring is Chord-inspired, though Cassandra uses virtual nodes and gossip rather than strict Chord finger tables

**Tradeoffs vs Consistent Hashing:**

| | Chord DHT | Consistent Hashing |
|-|-----------|-------------------|
| Lookup | O(log n) hops across nodes | O(log n) local (sorted ring) |
| State per node | O(log n) finger table | O(n × vnodes) ring |
| Join/leave cost | O(log^2 n) table updates | Update vnodes only |
| Practical use | P2P networks | CDN, cache clusters, DB sharding |

**Interview context:** "Chord is the academic foundation for DynamoDB's ring. In practice, DynamoDB uses consistent hashing with virtual nodes + gossip rather than strict Chord routing — simpler and more operationally predictable."

---

## Quick Revision Triggers
- "Count unique visitors at scale" → HyperLogLog.
- "Is this key in the database?" → Bloom Filter.
- "Add/Remove servers without reshuffling data" → Consistent Hashing.
- "Find top-K in a stream" → Count-Min Sketch.
- "Proximity search / Uber" → Quadtree / Geohash.
- "Leader election" → Raft / Paxos.
- "Are two replicas in sync?" → Merkle Tree.
- "How does Cassandra detect node failures?" → Gossip + SWIM.
- "Distributed transaction across microservices?" → SAGA (not 2PC).
- "P2P key lookup / DHT?" → Chord (academic), Kademlia (practical).
- "Generate unique sortable IDs at scale?" → Snowflake / ULID; prime modulus for hash tables.

---

## Geospatial Indexing

### Quadtree
**Mechanism**: recursively subdivide 2D space into four quadrants. A node splits when it contains more than a threshold T of points (e.g., T=4). Leaf nodes store the actual points.

- **Lookup**: navigate from root, choose quadrant that contains query point, recurse → O(log n) avg depth
- **Range query**: prune subtrees whose bounding box doesn't intersect query range → O(k + log n) where k = results
- **Dynamic**: insert/delete with local splits/merges
- **Used by**: Uber/Lyft driver location indexing, gaming (spatial collision)

```
Root [whole map]
├── NW [quadrant]
│   ├── NW [sub-quadrant — leaf if ≤ T points]
│   └── ...
├── NE
├── SW
└── SE
```

### Geohash
**Mechanism**: interleave bits of latitude and longitude binary representations → single base-32 string. Each additional character = more precision (smaller cell).

| Precision (chars) | Cell size |
|-------------------|-----------|
| 1 | 5000 km × 5000 km |
| 4 | 40 km × 20 km |
| 6 | 1.2 km × 0.6 km |
| 8 | 38m × 19m |

**Proximity**: cells sharing a common prefix are geographically nearby. Query "all points within 5km": find the 8-cell neighborhood of query geohash (center + 8 neighbors), query DB with `WHERE geohash LIKE 'prefix%'` — uses B-tree index.

**Edge case**: cells at geohash boundary may be close in space but have different prefixes → always check 9 cells (center + 8 neighbors).

### R-Tree
Hierarchical bounding-box tree. Each node stores MBR (minimum bounding rectangle) of its children. Used in spatial databases (PostGIS, SpatiaLite). Supports arbitrary polygon/line geometry, not just points. O(log n) insert/search for balanced tree.

### S2 Library (Google)
Divides the sphere (Earth) into a hierarchy of cells using a space-filling Hilbert curve. Cell IDs are 64-bit integers — cells with numerically close IDs are geographically close. Used by Google Maps, Foursquare, Lyft. Handles poles and antimeridian correctly (unlike geohash).

### Decision
| Use case | Choose |
|----------|--------|
| Dynamic point sets, memory | Quadtree |
| DB prefix queries, simplicity | Geohash |
| Arbitrary geometry (polygons) | R-Tree (PostGIS) |
| Global scale, precision | S2 Library |

---

## Time-Series Storage

### Core Challenge
Time-series data is high-cardinality (many metrics × labels), high-ingest (millions of data points/sec), and read with aggregations over time ranges — not by primary key lookup.

### Downsampling and Rollups
Keep raw data for recent period (e.g., 7 days), then downsample to progressively coarser granularity:
```
Raw (1s)  → 7 days
1-min avg → 90 days
1-hr avg  → 2 years
1-day avg → forever
```
Tiered retention dramatically reduces storage without losing analytical value.

### Columnar Storage for Compression
Store all timestamps in one column, all values in another. Same-type data compresses far better than row-oriented storage:
- Timestamp deltas: small integers (1s, 1s, 1s, ...) → delta encoding
- Values: often smooth (temperature, CPU%) → XOR encoding eliminates redundancy

### Gorilla Compression (Facebook)
Used in in-memory TSDB. Two tricks:
1. **Timestamps**: store delta-of-delta (typically 0 for fixed-interval metrics). Delta-of-delta = 0 → 1 bit. Exceptional values: zigzag encode the difference.
2. **Values (float64)**: XOR consecutive values. Smooth metrics produce XOR with leading/trailing zeros → store only meaningful bits. 90% of XORs are 0 for smooth data → 1 bit per sample.

Result: compress 16 bytes/sample (timestamp + double) to ~1.37 bytes/sample on average.

### Tooling
| Tool | Architecture | Best for |
|------|-------------|---------|
| InfluxDB | TSM engine (LSM variant) | General TSDB, IoT |
| Prometheus | Local TSDB + remote write | Monitoring, alerting |
| TimescaleDB | PostgreSQL extension (hypertables) | SQL + time-series |
| Druid | Columnar, real-time + batch | Analytics at scale |

---

## Distributed Tracing Internals

### What Distributed Tracing Solves
In microservices, a single user request fans out to 10-100 services. Logs are per-service. Without tracing, latency attribution and error root-cause are guesswork. Distributed tracing reconstructs the full request tree with timing at each hop.

### Trace Context Propagation (W3C TraceContext)
Every request carries HTTP headers:
```
traceparent: 00-{trace-id-128bit}-{span-id-64bit}-{flags}
tracestate:  vendor-specific key-value pairs
```
- **Trace ID**: unique per root request; same across all service hops
- **Span ID**: unique per service call; parent span ID links child to parent
- Each service extracts headers, records its own span (start time, end time, metadata), passes updated headers downstream

### Sampling Strategies
Tracing every request is too expensive (storage, CPU). Two strategies:

**Head-based sampling**: decision made at trace entry point (e.g., sample 1%). Simple, low overhead. Problem: cannot preferentially keep error traces (error rate may be 0.01% — almost never sampled).

**Tail-based sampling**: collect all spans, buffer them, make sampling decision at trace completion based on outcome (error? slow? interesting?). Keep 100% of error traces, 1% of success traces. Requires a sampling proxy (e.g., OpenTelemetry Collector with tail sampling processor). Problem: buffer memory, complexity.

### Jaeger/Zipkin Architecture
```
Instrumented services
       │ (spans via gRPC/HTTP)
       ↓
Collector (validate, transform, write)
       │
       ↓
Storage (Cassandra or Elasticsearch for span data)
       │
       ↓
Query Service + UI (trace reconstruction, search by trace-id, service, duration)
```

**Span storage**: each span is a JSON/Protobuf record with trace-id, span-id, parent-span-id, service name, operation name, start time, duration, tags, logs. Query by trace-id = look up all spans sharing that trace-id → reconstruct tree by parent-span-id.

**Interview context:** "We'd add distributed tracing by instrumenting each service with OpenTelemetry SDK, propagating W3C TraceContext headers, and sending spans to a central Jaeger/Zipkin collector. We'd use tail-based sampling to ensure 100% capture of error traces while keeping storage costs bounded."

## Flashcards

**"Count unique visitors at scale" → HyperLogLog.?** #flashcard
"Count unique visitors at scale" → HyperLogLog.

**"Is this key in the database?" → Bloom Filter.?** #flashcard
"Is this key in the database?" → Bloom Filter.

**"Add/Remove servers without reshuffling data" → Consistent Hashing.?** #flashcard
"Add/Remove servers without reshuffling data" → Consistent Hashing.

**"Find top-K in a stream" → Count-Min Sketch.?** #flashcard
"Find top-K in a stream" → Count-Min Sketch.

**"Proximity search / Uber" → Quadtree / Geohash.?** #flashcard
"Proximity search / Uber" → Quadtree / Geohash.

**"Leader election" → Raft / Paxos.?** #flashcard
"Leader election" → Raft / Paxos.

**"Are two replicas in sync?" → Merkle Tree.?** #flashcard
"Are two replicas in sync?" → Merkle Tree.

**"How does Cassandra detect node failures?" → Gossip + SWIM.?** #flashcard
"How does Cassandra detect node failures?" → Gossip + SWIM.

**"Distributed transaction across microservices?" → SAGA (not 2PC).?** #flashcard
"Distributed transaction across microservices?" → SAGA (not 2PC).

**"P2P key lookup / DHT?" → Chord (academic), Kademlia (practical).?** #flashcard
"P2P key lookup / DHT?" → Chord (academic), Kademlia (practical).

**"Generate unique sortable IDs at scale?" → Snowflake / ULID; prime modulus for hash tables.?** #flashcard
"Generate unique sortable IDs at scale?" → Snowflake / ULID; prime modulus for hash tables.
