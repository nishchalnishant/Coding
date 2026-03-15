# System Design Related Algorithms — SDE-3 Level

Algorithms commonly used in system design and LLD: rate limiting, consistent hashing, leader election, and quorum. SDE-3 may be asked to implement or reason about these in coding rounds.

---

## 1. Rate Limiting

**Token bucket**: Bucket holds at most N tokens; refill at R tokens/sec. Request consumes 1 token; if no token, reject. Implementation: store `tokens` and `last_refill_time`; on request, refill by `(now - last_refill_time) * R`, cap at N; if tokens >= 1, deduct and allow.

**Leaky bucket**: Requests enter queue; processed at fixed rate (leak). Enforce rate by queue size or drop when full.

**Sliding window log**: Store timestamps of requests; count in last window; reject if count >= limit. Memory O(requests). **Sliding window counter**: Approximate with prev_count * (window - elapsed) / window + current_count. O(1) memory.

**When to use**: API throttling, per-user limits. Token bucket allows bursts up to N; leaky bucket smooths traffic.

---

## 2. Consistent Hashing

**Problem**: Distribute keys across N servers; when adding/removing a server, minimize key movement.

**Idea**: Hash servers and keys to a ring (e.g., 0..2^32-1). Key goes to first server clockwise. On add/remove, only keys between old and new positions move.

**Implementation**: Sorted list or tree of server positions; binary search for key's position; handle wraparound. Virtual nodes (replicate each server many times on ring) for balance.

**Use**: Distributed caches (Memcached, Redis cluster), load balancing.

---

## 3. Leader Election

**In-memory (single process)**: One leader; on failure, next in order or highest ID wins. Use consensus (Raft, Paxos) in distributed setting.

**Ring**: Process passes token; whoever has token is leader. Failure detection and bypass.

**Bully**: Highest ID wins; on failure, higher IDs start election. O(N²) messages in worst case.

**Interview**: Often "design" rather than code; know trade-offs (availability vs consistency, single leader vs multi-leader).

---

## 4. Quorum

**Read/write quorum**: N replicas; write succeeds if W replicas ack; read succeeds if R replicas ack; W + R > N and W > N/2 for consistency (overlap with latest write).

**Use**: Distributed databases, durable writes. Trade-off: higher W/R = stronger consistency, lower availability.

---

## Quick Revision

- **Rate limit**: Token bucket (refill rate, capacity); sliding window counter O(1).
- **Consistent hashing**: Ring; virtual nodes; minimal reassignment.
- **Leader**: Raft/Paxos for distributed; bully/ring for concepts.
- **Quorum**: W + R > N; W > N/2 for strong consistency.
