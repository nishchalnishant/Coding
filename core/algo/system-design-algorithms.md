# System Design Related Algorithms — SDE-3 Level

Algorithms commonly used in system design and LLD: rate limiting, consistent hashing, leader election, and quorum. SDE-3 may be asked to implement or reason about these in coding rounds.

---

## 1. Rate Limiting

> [!IMPORTANT]
> **The Click Moment**: "Protect service from **abuse**" — OR — "handle **bursty traffic** gracefully" — OR — "**throttling** per user/API key".

**Token bucket**: Bucket holds at most N tokens; refill at R tokens/sec. Request consumes 1 token; if no token, reject. Implementation: store `tokens` and `last_refill_time`; on request, refill by `(now - last_refill_time) * R`, cap at N; if tokens >= 1, deduct and allow.

**Leaky bucket**: Requests enter queue; processed at fixed rate (leak). Enforce rate by queue size or drop when full.

**Sliding window log**: Store timestamps of requests; count in last window; reject if count >= limit. Memory O(requests). **Sliding window counter**: Approximate with prev_count * (window - elapsed) / window + current_count. O(1) memory.

**When to use**: API throttling, per-user limits. Token bucket allows bursts up to N; leaky bucket smooths traffic.

---

## 2. Consistent Hashing

> [!IMPORTANT]
> **The Click Moment**: "**Scale** out cache/database nodes" — OR — "minimize **rehashing** when nodes join/leave" — OR — "**repartitioning** at scale".

**Problem**: Distribute keys across N servers; when adding/removing a server, minimize key movement.

**Idea**: Hash servers and keys to a ring (e.g., 0..2^32-1). Key goes to first server clockwise. On add/remove, only keys between old and new positions move.

**Implementation**: Sorted list or tree of server positions; binary search for key's position; handle wraparound. Virtual nodes (replicate each server many times on ring) for balance.

**Use**: Distributed caches (Memcached, Redis cluster), load balancing.

---

## 3. Leader Election

> [!IMPORTANT]
> **The Click Moment**: "**Single point of coordination**" — OR — "**High Availability (HA)**" — OR — "who is the **master** in this cluster?".

**In-memory (single process)**: One leader; on failure, next in order or highest ID wins. Use consensus (Raft, Paxos) in distributed setting.

**Ring**: Process passes token; whoever has token is leader. Failure detection and bypass.

**Bully**: Highest ID wins; on failure, higher IDs start election. O(N²) messages in worst case.

**Interview**: Often "design" rather than code; know trade-offs (availability vs consistency, single leader vs multi-leader).

---

## 4. Quorum

> [!IMPORTANT]
> **The Click Moment**: "**Eventual vs Strong Consistency**" — OR — "handle **node failures** in distributed storage" — OR — "**Replication Factor** configuration".

**Read/write quorum**: N replicas; write succeeds if W replicas ack; read succeeds if R replicas ack; W + R > N and W > N/2 for consistency (overlap with latest write).

**Use**: Distributed databases, durable writes. Trade-off: higher W/R = stronger consistency, lower availability.

---

## 5. Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **Rate Limiter** | "Throttling" | Token Bucket / Sliding Window | Handling concurrency (locks) and distributed state (Redis). |
| **Consistent Hashing** | "Minimal re-mapping" | Hash Ring + Virtual Nodes | **Virtual Nodes** are critical for load balance; mention "hot spots". |
| **Leader Election** | "Coordination" | Raft / Bully | Split-brain scenario; term/epoch numbers to resolve conflicts. |
| **Quorum** | "Consistency" | W + R > N | Trade-off between write latency (higher W) and read latency (higher R). |

---

## See also

- [Distributed Systems Foundations](../../reference/distributed/README.md) — Paxos, Raft, and CAP theorem
- [LLD Patterns](../../reference/lld/README.md) — Singleton and Proxy patterns in system design
- [Patterns Master](../../reference/patterns/patterns-master.md)
