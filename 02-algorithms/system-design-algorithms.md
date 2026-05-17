# System Design Algorithms — SDE-3 Gold Standard

These are the "Big Tech" algorithms that power distributed systems. While standard DSA (DP, Graphs) tests logic, these test your ability to build scalable, resilient infrastructure.

---

## 1. Membership & Cardinality (The "Is it there?" Problems)

### Bloom Filters
- **What**: A space-efficient probabilistic data structure used to test if an element is in a set.
- **Why**: Standard `Set` is too large to fit in memory for billions of URLs.
- **Click Moment**: "Check if a username is taken without hitting the DB", "Filtering malicious URLs", "Avoiding expensive disk lookups for non-existent keys (BigTable/Cassandra)".
- **Trade-off**: **False Positives** are possible; **False Negatives** are impossible. You cannot delete from a standard Bloom Filter (use a Cuckoo Filter instead).

### HyperLogLog (HLL)
- **What**: Estimates the number of *unique* elements in a multiset.
- **Why**: Counting unique visitors (DAU) for 1 billion users would require gigabytes of memory; HLL does it in **1.5 KB** with 2% error.
- **Logic**: Observe the maximum number of leading zeros in the hash of elements. More leading zeros = statistically more unique elements seen.

---

## 2. Load Balancing & Distribution

### Consistent Hashing
- **What**: Maps both "Nodes" and "Keys" to a circular 360° hash ring.
- **Why**: Traditional `hash(key) % N` causes a massive reshuffle if one node dies (N changes). Consistent hashing only reshuffles `1/N` keys.
- **Click Moment**: "Scaling a cache layer", "Distributed KV store (Dynamo/Cassandra)".
- **Deep Dive**: Use **Virtual Nodes** to ensure uniform distribution and handle heterogeneous hardware.

### Rendezvous Hashing (Highest Random Weight)
- **What**: For each key, calculate a hash with every node ID. Assign the key to the node that produces the highest weight.
- **Why**: Better than Consistent Hashing when the set of nodes is small and changes frequently. No ring to maintain.

---

## 3. Rate Limiting & Flow Control

### Token Bucket
- **What**: A bucket holds tokens, refilled at a constant rate. Each request consumes a token.
- **Why**: Allows for **bursts** (up to bucket size) while maintaining a long-term average rate.
- **Use case**: API rate limiting at the gateway level.

### Leaky Bucket
- **What**: Requests enter a queue; they are processed at a constant output rate.
- **Why**: Smooths out traffic. No bursts allowed.
- **Use case**: Traffic shaping in networking.

---

## 4. Distributed Consensus & Coordination

### Paxos / Raft
- **What**: Algorithms to reach consensus across multiple unreliable nodes.
- **Why**: Essential for "Leader Election" and "Distributed Locking". If 3/5 nodes agree, the value is committed.
- **Interview Soundbite**: "Raft is preferred for its readability; Paxos is the original proof. Both ensure safety (no two leaders) and liveness (eventual progress)."

### Vector Clocks / Lamport Timestamps
- **What**: Tracking logical time in a distributed system.
- **Why**: Physical clocks drift (skew). Logical clocks track "happened-before" relationships.
- **Use case**: Conflict resolution in multi-master databases (Dynamo).

---

## 5. Sketching & Frequency

### Count-Min Sketch
- **What**: A 2D array of counters. Like a Bloom Filter but stores frequencies instead of membership.
- **Why**: "Top K trending hashtags" or "Identify heavy hitters" in a stream of millions of events.
- **Logic**: Use multiple hash functions; the estimated frequency is `min(counters[hash_i])`. This overestimates due to collisions but never underestimates.

### Quadtrees / Geohash
- **What**: Spatial indexing.
- **Why**: "Find nearest restaurants", "Uber driver matching".
- **Logic**: Recursively divide 2D space into 4 quadrants. Geohash encodes a 2D point into a 1D string where longer prefixes = closer proximity.

---

## Quick Revision Triggers
- "Count unique visitors at scale" → HyperLogLog.
- "Is this key in the database?" → Bloom Filter.
- "Add/Remove servers without reshuffling data" → Consistent Hashing.
- "Find top-K in a stream" → Count-Min Sketch.
- "Proximity search / Uber" → Quadtree / Geohash.
- "Leader election" → Raft / Paxos.
