## First-Principles Map

```
WHY system design → WHAT it tests → HOW to approach → WHEN each concept → WHAT can go wrong
       │                  │                  │               applies               │
  [Real systems          [ability to         [requirements  [caching: read-       [over-engineering
   involve tradeoffs      reason about        (5 min) →      heavy, static data;   for scale that
   no single algorithm    scale, failure,     estimation     sharding: write       isn't needed;
   handles; interviews    consistency,        (5 min) →      heavy, large data;    ignoring failure
   test whether you       and component       high-level      queues: async,        modes; no
   can decompose          selection at        design (10) →   decoupling;           monitoring plan;
   ambiguous problems     scale]              deep dive (10)  replication:          premature
   into buildable                             → tradeoffs(5)] fault tolerance]      consistency
   components]                                                                      decisions]
       │                  │                  │
  [real-world:           [CAP theorem:       [scale heuristics:
   design URL shortener   pick 2 of 3:        10M DAU → ~100 QPS read;
   = hashing + storage    Consistency,        1KB per user → 10GB/day;
   + redirect;            Availability,       cache 20% of data → 80%
   design Twitter =       Partition-tolerance; hit rate; 3× replication
   fanout + storage +     most choose AP      = 3× storage cost;
   feed + CDN]            (eventual consistency) read replicas for reads]
       ↓
[Decision: Key system design tradeoffs]
  ├── SQL vs NoSQL      → ACID needs → SQL; scale/schema-flexibility → NoSQL
  ├── Cache aside vs    → cache aside for read-heavy; write-through for consistency
      write-through
  ├── Sync vs Async     → sync for consistency (payment); async for throughput (notifications)
  └── Strong vs Eventual → bank: strong; social feed: eventual
```

## First-Principles Breakdown
- **Root problem**: Large-scale systems can't use single-machine solutions — need to reason about distribution, failure, and consistency simultaneously.
- **Core insight**: Every system design decision is a tradeoff (CAP, latency vs consistency, cost vs reliability) — the right answer is "it depends on requirements" backed by explicit tradeoffs.
- **Invariant**: Requirements drive design; never propose a solution before clarifying scale, consistency, and availability needs.
- **Why it's fast**: A structured framework (requirements → estimation → high-level → deep dive → tradeoffs) prevents going in circles and ensures all dimensions are covered.
- **Where it breaks**: Skipping estimation leads to under/over-designed systems; ignoring failure modes produces fragile designs; choosing strong consistency everywhere sacrifices availability unnecessarily.

# Google SDE-2 (L4) System Design — What to Cover + Templates

```
System Design — First Principles
│
├── WHY it exists
│   ├── Single machines have hard limits (CPU, RAM, disk, network)
│   ├── Users demand low latency + high availability globally
│   └── Failures are inevitable — systems must degrade gracefully
│
├── WHAT it is
│   ├── The discipline of decomposing a problem into components
│   │   each with well-defined responsibilities and failure modes
│   ├── Core primitives
│   │   ├── Compute   — stateless services, replicas, load balancers
│   │   ├── Storage   — relational, NoSQL, blob, cache, queue
│   │   ├── Network   — CDN, DNS, gateways, service mesh
│   │   └── Async     — queues, streams, event buses
│   └── Cross-cutting concerns
│       ├── Consistency vs Availability (CAP / PACELC)
│       ├── Latency vs Throughput
│       └── Observability — metrics, logs, traces
│
├── HOW it works (design process)
│   ├── 1. Requirements → scope, SLOs, scale estimates
│   ├── 2. API contract → inputs, outputs, auth, pagination
│   ├── 3. Data model → entities, indexes, query patterns
│   ├── 4. High-level design → services + storage + async
│   ├── 5. Deep dive → critical path (write or read)
│   └── 6. Scale + reliability → sharding, caching, failures
│
└── WHERE to apply (decision triggers)
    ├── Read-heavy   → cache aggressively, CDN, read replicas
    ├── Write-heavy  → async queues, sharding, LSM storage
    ├── Strong consistency needed → leader-follower replication, 2PC / Saga
    ├── Eventual consistency ok → CRDT, leaderless replication
    ├── Low latency  → co-locate data + compute, in-memory, edge
    └── High availability → multi-region, circuit breakers, bulkheads
```

This is **not** an L5/L6 deep-dive. For L4, you're usually evaluated on clear thinking, fundamentals, and tradeoffs.

**When to use this file:** you have a **general** system design round (e.g. URL shortener, feed, chat). If your schedule has an **AI / ML** interview instead, that round may focus on **model lifecycle, data, training, serving, and monitoring** — use the **AI / ML** section in [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md) and treat this file as **supplementary** for scalable serving and storage. Some candidates get **both**; confirm with your recruiter.

---

## What interviewers expect at L4

- Clarify requirements (functional + non-functional)
- Propose a sensible high-level architecture
- Pick reasonable storage + caching + async boundaries
- Talk about scaling (hot keys, partitioning, read/write patterns)
- Discuss reliability (timeouts, retries, idempotency, backpressure)
- Make tradeoffs explicit (consistency vs availability, cost vs latency)

---

## 35–45 minute structure (safe default)

1. **Requirements (5 min)**: scope + out-of-scope + SLOs
2. **APIs (5 min)**: request/response, auth, pagination
3. **Data model (5 min)**: entities + indexes + key queries
4. **High-level design (10 min)**: services + DB + cache + queue
5. **Deep dive (10 min)**: one critical path (write path or read path)
6. **Scale + reliability (5–10 min)**: bottlenecks, sharding, rate limits, failures

---

## Reusable checklist (ask yourself every time)

- What are the **read/write** ratios?
- What is the **hot key / hot partition** risk?
- What needs **strong consistency** vs eventual consistency?
- What should be cached (and where)?
- Where do we need **async** (queues, streams)?
- What happens on **retries** (idempotency keys)?
- How do we observe it (metrics, logs, tracing)?

---

## Common L4 practice prompts (pick 6–10)

- Design a URL shortener
- Design a rate limiter / API throttling service
- Design a "news feed" / timeline (high-level)
- Design a file/photo upload service (metadata + storage)
- Design a chat messaging service (1:1 or group)
- Design a notification system (email/push) with retries
- Design a parking availability service (location + updates)
- Design a "top K trending" service (streaming aggregation)

Algorithm building blocks (if asked to reason/implement): `../advanced-dsa/system-design-algorithms.md`.

---

## Minimal "back-of-envelope" numbers (good enough for L4)

- QPS = requests/sec, peak vs average (assume 10× peak if unclear)
- Storage/day = (events/day) × (bytes/event)
- Cache hit rate impacts DB load directly

Keep it rough; the goal is to guide design choices, not to be perfectly accurate.

---

## Worked Example 1: URL Shortener

### Requirements (clarify first)

**Functional:**
- Given a long URL, return a short code (e.g. `sho.rt/abc123`)
- Redirect short URL → original URL
- Optional: custom alias, expiry, analytics (confirm scope)

**Non-functional:**
- Read-heavy (100:1 read/write ratio — redirects >> creates)
- Latency: redirect < 50ms p99
- Availability: 99.9% (lose a redirect → bad UX)
- Scale: 100M URLs stored, 10K redirects/sec peak

**Out of scope:** auth, billing, abuse prevention (mention but park)

---

### APIs

```
POST /shorten
  body: { long_url, custom_alias?, ttl_days? }
  returns: { short_code, short_url }

GET /{short_code}
  returns: HTTP 301/302 redirect to long_url
  (301 = permanent, cached by browser; 302 = temporary, analytics possible)
```

**Tradeoff:** 301 reduces server hits (good for scale); 302 lets you count each redirect. Choose 302 if analytics matter.

---

### Data model

```
urls table (PostgreSQL or DynamoDB)
  short_code   VARCHAR(8)  PK
  long_url     TEXT        NOT NULL
  created_at   TIMESTAMP
  expires_at   TIMESTAMP   NULLABLE
  user_id      VARCHAR     NULLABLE
  click_count  BIGINT      DEFAULT 0  ← eventually-consistent counter
```

**Key query:** lookup by `short_code` — single-row fetch. No complex joins needed → NoSQL (DynamoDB, Bigtable) works well. Use SQL if you need user dashboards.

**Short code generation:**
- Option A: Base62 encode an auto-increment ID (7 chars → 62^7 ≈ 3.5T codes). Simple, sequential (predictable).
- Option B: MD5/SHA hash of URL → take first 7 chars → collision risk ~0.01% at 100M URLs. Recheck on collision.
- Option C: Pre-generate random codes in a "codes pool" table; claim one atomically. Eliminates hotspot on sequence generator.

**L4 answer:** explain A + B, mention collision handling for B, pick whichever you can justify.

---

### High-level design

```
Client → CDN (cache redirects) → Load Balancer
              ↓
        Redirect Service (stateless, many replicas)
              ↓
        Redis cache (short_code → long_url, TTL matches expiry)
              ↓
        URL DB (DynamoDB or Postgres)

Write path:
Client → API Gateway → Shorten Service → DB (write) → Cache (write-through or lazy)
```

**Cache strategy:** Read-through on miss; TTL = URL expiry. Hot codes stay in RAM.

---

### Deep dive: redirect path

1. Client hits `GET /abc123`
2. Redirect Service checks Redis: **hit** → return 302 immediately (~5ms)
3. **Miss** → query DB → write back to Redis → return 302
4. If `expires_at` is set and passed → return 410 Gone

**Hot short code problem:** a viral URL creates thundering herd on DB.
Fix: "dog-pile lock" (only one goroutine/thread fetches DB, others wait) or stale-while-revalidate in cache.

---

### Scale + reliability

| Concern | Solution |
|---------|----------|
| DB write bottleneck (100K creates/day) | Not a real bottleneck; write QPS is low |
| Read hot spots (10K redir/sec) | CDN caches 301s; Redis handles the rest |
| Analytics (click counts) | Write to Kafka → async aggregator → analytics DB; don't increment in hot path |
| Code collisions | Retry with different hash suffix or use pre-generated pool |
| Expiry cleanup | Background job scans expired rows; lazy delete on read also works |

**What to say when asked "how do you scale to 10×?":** Shard the URL table by `short_code` prefix; add Redis cluster; CDN absorbs >80% of reads.

---

### Monitoring

| Signal | What to watch | Alert threshold |
|--------|--------------|----------------|
| Redirect p99 latency | Redis hit rate + DB query time | > 50ms p99 |
| Cache hit rate | Redis hits / total lookups | < 90% → investigate cold cache or TTL misconfiguration |
| Error rate | 4xx (expired/bad code) vs 5xx (service errors) | 5xx > 0.1% |
| Short code creation rate | Writes/sec to DB | Sudden spike → abuse/spam |
| Kafka consumer lag | Click-count events processed vs queued | > 10K unprocessed |

**Detection before users notice:** alert on Redis hit rate dropping (cache eviction pressure) before latency rises. A hit rate drop from 98% → 90% can 5× your DB load.

---

## Worked Example 2: Rate Limiter

### Requirements

**Functional:**
- Allow/deny requests per user (or IP) based on a configured limit (e.g. 1000 req/min)
- Return `429 Too Many Requests` when exceeded
- Config per API key or user tier

**Non-functional:**
- Decision latency: < 5ms (in hot path of every request)
- High availability: fail-open (allow requests if rate limiter is down) or fail-closed (deny) — **must decide**
- Distributed: multiple app servers share state

**Out of scope:** billing tiers, admin UI

---

### Algorithms (explain tradeoffs)

**L4 recommendation:** Start with **fixed window counter** — it's O(1), one Redis INCR per request, easy to reason about. Upgrade to **sliding window counter** only if the interviewer raises boundary-burst gaming. Say: "I'd pick fixed window for simplicity; if clients batch requests at window edges I'd switch to sliding window counter."

| Algorithm | How | Pro | Con |
|-----------|-----|-----|-----|
| **Fixed window counter** | Count per minute bucket in Redis `INCR` | Simple, O(1) | Burst at window boundary (double limit) |
| **Sliding window log** | Store each request timestamp in sorted set; count last 60s | Accurate | Memory: O(requests), expensive at high QPS |
| **Sliding window counter** | Weighted blend of current + previous window | Good accuracy, O(1) | Slightly approximate |
| **Token bucket** | Tokens refill at rate R; consume 1 per request | Allows controlled bursts | State per user |
| **Leaky bucket** | Queue drains at fixed rate | Smooth output | Adds latency; queue is a bottleneck |

---

### Data model (Redis)

```
Key:   rate:{user_id}:{window_start_minute}
Value: integer count
TTL:   2 minutes (covers current + prev window)

INCR  rate:u123:1700000060     → returns new count
EXPIRE rate:u123:1700000060 120
```

Use a Lua script for atomicity: INCR + check + EXPIRE in one round trip.

---

### High-level design

```
Client → Load Balancer → App Server
                              ↓
                    Rate Limiter Middleware
                              ↓
                    Redis Cluster (shared counter)
                              ↓
                    Allow: forward to upstream
                    Deny:  return 429 + Retry-After header
```

**Distributed consistency:** Each app server writes to the same Redis. Risk: Redis goes down.
- **Fail-open:** skip rate check if Redis unreachable → less protection
- **Fail-closed:** deny all → safe but bad UX during outage
- **Hybrid:** local in-memory fallback counter (less accurate but better than down)

---

### Deep dive: headers + client guidance

Always return:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 237
X-RateLimit-Reset: 1700000120   ← epoch of next window
Retry-After: 47                 ← seconds until retry safe
```

---

### Scale + reliability

| Concern | Solution |
|---------|----------|
| Redis hot key (one user, massive QPS) | Shard Redis by user_id hash; local cache for top users |
| Redis latency spike | Async / fire-and-forget INCR (accept slight over-limit) |
| Multi-region | Regional Redis; accept ~10% over-limit on cross-region lag |
| Sliding log memory | Cap sorted set size; evict oldest entries |

---

### Monitoring

| Signal | What to watch | Alert threshold |
|--------|--------------|----------------|
| Rate limiter decision latency | Redis INCR round-trip time | > 5ms p99 |
| 429 rate per API key | Count of denied requests per user/tier | Sudden spike → possible abuse or misconfigured limit |
| Redis availability | Connection errors from middleware | Any failure → fail-open/closed decision activates |
| False-positive rate | Legitimate users hitting 429 | Any reports → check limit config or clock skew between nodes |
| Local fallback activation | How often in-memory counter substitutes Redis | > 0 → Redis health issue |

**Detection before users notice:** monitor Redis p99 latency independently from app latency. If Redis slows from 1ms → 4ms, you're still under threshold but trending toward the 5ms SLO; page before it breaks.

---

## Worked Example 3: News Feed (High-Level)

### Requirements

**Functional:**
- User follows other users
- Post content (text, images)
- Get chronological or ranked feed of followed users' posts

**Non-functional:**
- Read-heavy (50:1 read/write)
- Feed latency < 200ms
- Scale: 100M users, 1M DAU, celebrity accounts with 10M followers

**Out of scope:** ads ranking, video upload pipeline, notifications

---

### Core design decision: push vs pull vs hybrid

| | Push (fan-out on write) | Pull (fan-out on read) | Hybrid |
|-|------------------------|------------------------|--------|
| **How** | On post, write to every follower's feed list | On read, fetch posts from all followees and merge | Push for normal users; pull for celebrities |
| **Feed read** | O(1) — pre-built | O(followees) — merge at read time | O(1) for most |
| **Write cost** | O(followers) — expensive for celebrities | O(1) | O(normal-user followers) |
| **Staleness** | Fresh (real-time) | Fresh (real-time) | Celebrities slightly stale until merged |
| **Use when** | Most users; followees < 10K | Celebrity accounts | Default L4 answer |

**L4 answer:** Start with fan-out on write; introduce hybrid when asked about celebrities.

---

### Data model

```
posts table
  post_id     UUID PK
  author_id   UUID
  content     TEXT
  media_url   TEXT
  created_at  TIMESTAMP
  (index on author_id + created_at for pull path)

follows table
  follower_id  UUID
  followee_id  UUID
  PRIMARY KEY (follower_id, followee_id)

feed_cache (Redis sorted set, per user)
  Key:   feed:{user_id}
  Score: created_at epoch
  Value: post_id
  Max:   500 entries (trim older)
```

---

### High-level design

```
Write path:
Client → Post Service → posts DB
                     → Feed Service (async via Kafka)
                           → Fan-out Worker → Redis (feed:{follower_id} ZADD)

Read path:
Client → Feed Service → Redis feed:{user_id} ZREVRANGE 0 19 (top 20)
                     → Post Service (hydrate post details by IDs)
                     → Return sorted feed
```

---

### Deep dive: celebrity problem

A user with 10M followers: fan-out on write means 10M Redis writes per post.

**Fix:** Flag accounts as "celebrities" (>100K followers). On write, skip fan-out. On read, merge:
1. Fetch pre-built feed from Redis (normal followees)
2. Fetch latest N posts from each celebrity followee (post DB, by author_id index)
3. Merge + sort in Feed Service

This adds latency (~50ms) but only for users following celebrities. Acceptable tradeoff.

---

### Scale + reliability

| Concern | Solution |
|---------|----------|
| Fan-out latency | Async Kafka queue; user sees post with ~1–2s delay |
| Redis memory per user | Cap feed at 500 entries; TTL 7 days for inactive users |
| Feed consistency | Eventual — acceptable; strong consistency not required for feeds |
| Post delete | Soft delete in DB; feed readers skip deleted post_ids on hydrate |
| Hot posts | CDN for media; post metadata cached in Redis by post_id |

---

### Monitoring

| Signal | What to watch | Alert threshold |
|--------|--------------|----------------|
| Feed read p99 latency | Redis ZREVRANGE + hydration time | > 200ms p99 |
| Kafka consumer lag | Fan-out worker queue depth | > 50K events → fan-out workers falling behind |
| Redis memory usage | Feed cache size across cluster | > 70% capacity → expand or evict inactive feeds sooner |
| Feed freshness | Time from post creation to feed appearance | > 5s for non-celebrity posts → fan-out worker issue |
| Celebrity merge latency | Extra time added for users following celebrities | > 100ms → DB index degraded or celebrity post volume spike |

**Detection before users notice:** fan-out lag shows up in Kafka consumer lag before users report stale feeds. Alert at 50K events in queue — at typical throughput that's ~30s of lag, still within tolerance but trending wrong.

---

## Key vocabulary to use in any design

| Term | When to say it |
|------|---------------|
| **Idempotency key** | Any write API that might retry |
| **Back-pressure** | Queue consumer can't keep up with producer |
| **Hot partition** | One shard gets disproportionate load |
| **Fan-out** | Distributing one event to many recipients |
| **Write-through cache** | Write to cache and DB together |
| **Read-through cache** | Cache fetches from DB on miss |
| **Thundering herd** | Many requests simultaneously miss cache and hit DB |
| **Eventual consistency** | Replicas may lag; ok for feeds, not ok for payments |
| **SLO / SLA** | Service Level Objective vs Agreement — know the difference |

---

## Database Sharding Strategies

**When:** Single DB node can't handle write throughput or storage volume.

### Range-based sharding
- Partition by ordered key range (e.g. user_id 0–1M → shard 1, 1M–2M → shard 2)
- **Pro:** Range scans efficient; shard boundaries are predictable
- **Con:** Hot partitions if data is skewed (new users all land on latest shard); rebalancing requires moving contiguous ranges
- **Use when:** Time-series data (partition by timestamp range), ordered scans are frequent

### Hash-based sharding
- `shard = hash(key) % N`
- **Pro:** Uniform distribution; simple
- **Con:** Range scans require scatter-gather across all shards; adding/removing shards reshuffles ~all keys (use consistent hashing to reduce this)
- **Use when:** Random reads/writes dominate; user data, session data

### Directory-based sharding
- A lookup service maps key → shard (separate metadata store)
- **Pro:** Flexible — arbitrary mapping, easy rebalancing (just update directory), supports heterogeneous shards
- **Con:** Directory is a single point of failure and a hot path; adds one extra hop per request
- **Use when:** Need maximum flexibility; shard topology changes frequently (live migrations)

### Sharding tradeoff matrix

| Strategy | Hotspot risk | Range scan | Rebalance cost | Ops complexity |
|----------|-------------|-----------|---------------|---------------|
| Range | High (skewed data) | Efficient | Low | Low |
| Hash | Low | Scatter-gather | High (without consistent hash) | Medium |
| Directory | Low | Flexible | Low | High (directory infra) |

**L4 answer:** Default to hash sharding with consistent hashing. Mention directory-based if asked how you'd handle live migrations or heterogeneous nodes.

---

## CDN Architecture and Edge Caching

**Why:** Origin servers can't serve global users at < 20ms. CDN nodes are co-located with ISPs.

### How CDN works
```
User (Tokyo) → CDN PoP (Tokyo) → [cache hit] → serve directly
                                → [cache miss] → origin (US) → cache → serve
```

### Cache control headers (what you must know)
- `Cache-Control: max-age=86400` — browser + CDN cache for 24h
- `Cache-Control: s-maxage=3600` — CDN-only TTL (overrides max-age for shared caches)
- `Vary: Accept-Encoding` — separate cache entries per encoding
- `Surrogate-Key` / `Cache-Tag` — tag-based purge (invalidate all objects tagged `product:123`)

### Pull vs Push CDN
| | Pull | Push |
|-|------|------|
| **How** | CDN fetches from origin on first cache miss | You upload content to CDN proactively |
| **Good for** | Dynamic content, unpredictable access patterns | Large static assets (video, software releases) |
| **Con** | First user after cache miss hits origin | You manage invalidation and storage |

### Edge caching decision tree
- Static assets (JS/CSS/images): long TTL (1 year) + content-hash in filename → cache-bust by renaming
- API responses (read-heavy, infrequently changing): short TTL (30–60s) + surrogate key purge on write
- Personalized/auth content: **do not cache at CDN** (or cache with `Vary: Cookie` carefully)
- Real-time: bypass CDN entirely

### Interview trigger phrases
- "Reduce origin load" → CDN + aggressive TTL
- "Invalidate on update" → purge API (Cloudflare, Fastly, CloudFront) or use surrogate keys
- "Multi-region with low latency" → CDN PoPs + anycast DNS

---

## Message Queue Deep Dive

### Kafka
- **Model:** Distributed commit log. Topics → partitions → ordered, immutable append-only segments.
- **Consumer model:** Consumer groups — each partition consumed by exactly one consumer in a group. Multiple groups = fan-out for free.
- **Retention:** Data kept by time/size (default 7 days), not by consumer ack. Consumers track their own offset → replay possible.
- **Throughput:** Millions of events/sec. Sequential disk I/O. Zero-copy sendfile.
- **Ordering guarantee:** Per-partition only.
- **Use when:** Event streaming, audit log, fan-out to multiple consumers, replay, time-series pipelines, exactly-once with transactions (Kafka 0.11+).
- **Not great for:** Task queues with per-message routing, sub-100ms job dispatch, small scale (ops overhead).

### RabbitMQ
- **Model:** Message broker. Exchanges route messages to queues via bindings (direct, fanout, topic, headers).
- **Consumer model:** Push-based. Broker delivers to consumer; consumer ACKs → message deleted.
- **Routing power:** Rich routing (topic exchange with wildcards, header matching) that Kafka can't do natively.
- **Throughput:** ~50K–100K msg/sec. Lower than Kafka but more flexible per-message routing.
- **Use when:** Task queues (job dispatch), RPC patterns, priority queues, complex routing logic, per-message TTL.
- **Not great for:** Replay (messages deleted after ack), millions of events/sec, multi-consumer fan-out at scale.

### SQS (AWS)
- **Model:** Managed queue service. Standard (at-least-once, unordered) or FIFO (exactly-once, ordered, 3K msg/sec).
- **Consumer model:** Pull-based (long polling). Message invisible during processing (visibility timeout); re-queued if not deleted.
- **Dead Letter Queue (DLQ):** Automatic routing of failed messages after N retries.
- **Use when:** AWS-native workloads, decoupling microservices with minimal ops, simple task queues, auto-scaling consumers (with Lambda).
- **Not great for:** Fan-out to many consumers (use SNS → SQS), replay, high-throughput streaming.

### Decision matrix

| Need | Choose |
|------|--------|
| Event streaming, replay, audit log | Kafka |
| Complex routing (topic wildcards, priority) | RabbitMQ |
| AWS native, managed, simple task queue | SQS |
| Fan-out to many services | Kafka (consumer groups) or SNS→SQS |
| Exactly-once delivery | Kafka transactions or SQS FIFO |
| Sub-ms latency job dispatch | RabbitMQ |

---

## Service Mesh / Sidecar Pattern

**Problem:** Cross-cutting concerns (mTLS, retries, timeouts, tracing, load balancing) duplicated in every service's code.

**Solution:** Extract network concerns into a **sidecar proxy** (e.g. Envoy) co-deployed with each service instance.

```
[Service A Pod]                    [Service B Pod]
  App Container                      App Container
  Sidecar (Envoy) ─── mTLS ───────── Sidecar (Envoy)
        ↑                                   ↑
        └──────── Control Plane ────────────┘
                 (Istio / Linkerd)
            (manages config, certs, policy)
```

### What the sidecar handles (so app code doesn't have to)
- **mTLS:** Automatic certificate rotation; service-to-service encryption
- **Retries + timeouts:** Configurable per route without code changes
- **Circuit breaking:** Detect failing upstream; stop sending traffic
- **Load balancing:** L7-aware (round robin, least conn, zone-aware)
- **Observability:** Automatic span injection (Jaeger/Zipkin), metrics (Prometheus)
- **Traffic shifting:** Canary deploys — route 5% traffic to v2 via config

### Tradeoffs
- **Pro:** Decouples infra concerns from business logic; uniform policy enforcement; language-agnostic
- **Con:** Sidecar adds ~1–3ms latency per hop; doubles the container count; control plane is complexity
- **Use when:** Polyglot microservices; strict zero-trust security; need A/B or canary without code deploys

---

## Database Replication

**Why:** Single write node is a SPOF; read replicas scale read throughput; geo-replication reduces latency.

### Leader-Follower (Single-Leader)
```
Write → Leader → replication log → Follower 1
                                  → Follower 2
Read  → Follower (eventual) or Leader (strong)
```
- **Sync replication:** Leader waits for follower ack before confirming write → strong consistency, lower availability
- **Async replication:** Leader acks immediately → higher availability, replication lag risk
- **Failover:** Promote follower to leader; risk of data loss if async and leader fails between write and replication
- **Use when:** OLTP (Postgres, MySQL), most relational setups

### Multi-Leader
- Multiple nodes accept writes; each replicates to others
- **Conflict resolution required:** Last-Write-Wins (LWW), CRDTs, application-level merge
- **Use when:** Multi-datacenter active-active; offline-first apps (CouchDB, Google Docs)
- **Problem:** Write conflicts are hard; avoid unless you need multi-region writes

### Leaderless (Dynamo-style)
- Client writes to N nodes simultaneously; read from R nodes; write to W nodes
- **Quorum:** W + R > N → strong consistency. Typical: N=3, W=2, R=2
- **Read repair:** On read, stale values updated in background
- **Anti-entropy:** Background process compares replicas (Merkle trees)
- **Use when:** Cassandra, DynamoDB, Riak — high availability, eventual consistency tolerated

### Replication lag problems
| Problem | Cause | Fix |
|---------|-------|-----|
| Read-your-writes violation | User reads from stale replica right after write | Route user's reads to leader for 1 min after write |
| Monotonic read violation | Different replicas at different lag, user sees older data after newer | Sticky sessions — user always reads same replica |
| Phantom reads | Different replicas disagree on which rows exist | Use serializable isolation or read from leader |

---

## SAGA Pattern for Distributed Transactions

**Problem:** 2PC (Two-Phase Commit) requires all participants to lock resources until coordinator confirms — blocking, fragile across service boundaries.

**SAGA:** Break a long-running transaction into a sequence of local transactions. Each step publishes an event. On failure, execute **compensating transactions** in reverse.

### Choreography-based Saga
```
Order Service → [OrderCreated event]
  → Payment Service → [PaymentCharged event]
    → Inventory Service → [StockReserved event]
      → Shipping Service → [ShipmentCreated event]
```
On failure (e.g. stock unavailable):
```
Inventory fails → [StockFailed event]
  → Payment Service compensates → [PaymentRefunded event]
    → Order Service compensates → [OrderCancelled event]
```
- **Pro:** No central coordinator; loosely coupled
- **Con:** Hard to reason about; distributed debugging; risk of cyclic events

### Orchestration-based Saga
```
Saga Orchestrator → calls Order Service (local txn)
                  → calls Payment Service
                  → calls Inventory Service
                  → on any failure: calls compensating endpoints in reverse
```
- **Pro:** Central visibility; easier to reason, debug, and add steps
- **Con:** Orchestrator can become a bottleneck; slightly more coupled

### When to use SAGA vs 2PC

| | SAGA | 2PC |
|-|------|-----|
| Spanning services | Yes (designed for it) | Painful (network locks) |
| Failure semantics | Eventual consistency + compensation | Atomic |
| Performance | High (no global locks) | Low (lock contention) |
| Use when | Microservices, long-running workflows | Single DB or tightly-coupled systems |

**L4 soundbite:** "I'd use SAGA over 2PC across microservices — 2PC holds locks across network boundaries which kills availability. SAGA gives eventual consistency with compensating transactions for rollback."

---

## Circuit Breaker Pattern

**Problem:** A failing downstream service causes cascading failures — callers keep retrying, exhausting thread pools and propagating latency.

### States
```
         calls succeed                    threshold exceeded
CLOSED ──────────────── (normal) ──────────────────────► OPEN
  ↑                                                         │
  │  half-open calls succeed                                │ timeout elapsed
  │                                                         ▼
  └──────────────────────────────── HALF-OPEN ◄────────────┘
                                   (probe with 1 request)
```

| State | Behavior |
|-------|----------|
| **Closed** | All requests pass through. Count failures. |
| **Open** | All requests fail fast (no call made). Return error/fallback immediately. |
| **Half-Open** | Allow N probe requests. If they succeed → Closed. If they fail → back to Open. |

### Configuration knobs
- `failure_threshold` — e.g. 5 failures in 10s → Open
- `timeout` — how long to stay Open before probing (e.g. 30s)
- `success_threshold` in Half-Open — e.g. 3 consecutive successes → Closed

### Why it matters
- Protects thread pools from being exhausted by slow downstreams
- Gives failing service time to recover without being hammered
- Enables fallback: serve cached/degraded response while Open

**Libraries:** Resilience4j (Java), Hystrix (deprecated), Polly (.NET), `circuitbreaker` (Go)

**Interview trigger:** "What happens when Payment Service goes down?" → circuit breaker + fallback (queue the payment, retry later)

---

## Observability Triad

**Metrics, Logs, and Traces** — each answers a different question.

### Metrics — "Is something wrong?"
- Aggregated numeric time series (counters, gauges, histograms)
- **What to monitor:** RED (Rate, Errors, Duration) for services; USE (Utilization, Saturation, Errors) for resources
- **Tools:** Prometheus + Grafana, Datadog, CloudWatch
- **Key interview point:** Alert on metrics; metrics are cheap per data point (unlike logs)

```
RED:
  Rate      = requests/sec
  Errors    = error rate (4xx/5xx %)
  Duration  = p50 / p99 / p999 latency

USE (for infra):
  Utilization = CPU/memory % used
  Saturation  = queue depth, wait time
  Errors      = disk errors, packet drops
```

### Logs — "What happened?"
- Structured (JSON) preferred over unstructured — enables fast querying
- **Sampling:** Log 100% of errors; sample 1–5% of successful requests at high QPS
- **Tools:** ELK stack (Elasticsearch + Logstash + Kibana), Loki + Grafana, Cloud Logging
- **Key interview point:** Logs are expensive at scale — index only necessary fields; use log levels (ERROR/WARN/INFO/DEBUG)

### Traces — "Where did the time go?"
- Distributed trace follows a request through multiple services
- Each service adds a **span** (start time, duration, metadata); spans linked by `trace_id`
- **Tools:** Jaeger, Zipkin, AWS X-Ray, Datadog APM
- **Key interview point:** Sampling rate matters — 100% tracing at 10K rps is expensive; use head-based or tail-based sampling

### How they fit together
```
Alert fires (metric: p99 > 500ms)
  → Check dashboards → which service? (metrics)
    → Look at logs for that service → error message (logs)
      → Find trace_id in log → view full trace → slow DB query (traces)
```

**L4 soundbite:** "I instrument every service with RED metrics for alerting, structured logs for debugging, and distributed tracing for latency attribution. Logs and traces use the same trace_id for correlation."

---

## Worked Example 4: Design a Chat System

### Requirements

**Functional:**
- 1:1 messaging; optional group chat (≤ 500 members)
- Message delivery: sent → delivered → read receipts
- Online/offline presence
- Message history (persistent)

**Non-functional:**
- Latency: message delivery < 100ms when both online
- Scale: 50M DAU, 100M messages/day
- Availability: 99.99% (chat is critical UX)

**Out of scope:** voice/video, E2E encryption (mention, park), message search

---

### Core protocol decision: polling vs long-polling vs WebSocket vs SSE

| | Short Poll | Long Poll | WebSocket | SSE |
|-|-----------|-----------|-----------|-----|
| **How** | Client polls every N sec | Server holds request until data or timeout | Full-duplex TCP connection | Server→client stream (HTTP) |
| **Latency** | N sec | Near-real-time | Real-time | Real-time |
| **Server load** | High (many empty responses) | Medium | Low per connection | Low per connection |
| **Bidirectional** | Yes (2 requests) | Yes (2 requests) | Yes (1 connection) | No (client uses HTTP for sends) |
| **Use when** | Simple, low frequency | Fallback | Chat, gaming, collaborative apps | Notifications, live feeds |

**L4 answer:** WebSocket for chat. Clients maintain persistent WS connection to a Chat Server.

---

### High-level design

```
Client A ──WS──► Chat Server 1 ──► Message Service ──► DB (messages)
                                        │
                                    Kafka topic
                                        │
                 Chat Server 2 ◄── Fan-out Service ──► Push Notification (offline)
                      │
Client B ──WS──► Chat Server 2
```

**Key insight:** Chat Server 1 and Chat Server 2 are different servers. They don't share WS state. Kafka decouples message delivery from receipt.

---

### Data model

```
messages table (Cassandra — write-heavy, time-ordered reads)
  message_id   UUID (time-based, e.g. ULID)
  chat_id      UUID   ← partition key
  sender_id    UUID
  content      TEXT
  created_at   TIMESTAMP  ← clustering key (desc)
  status       ENUM(sent, delivered, read)

chat_members table
  chat_id      UUID  PK
  user_id      UUID

presence table (Redis — TTL-based)
  Key: presence:{user_id}
  Value: {server_id, last_seen}
  TTL: 30s (refreshed by heartbeat)
```

**Why Cassandra?** Messages are append-only, queried by `chat_id` + time range. Cassandra excels at this pattern.

---

### Deep dive: message delivery flow

1. Client A sends message over WS to Chat Server 1
2. Chat Server 1 writes to `messages` table (synchronous for durability)
3. Chat Server 1 publishes to Kafka `chat.{chat_id}` topic
4. Fan-out service consumes → checks presence for each recipient
   - Online: route to their Chat Server via internal pub/sub (Redis pub/sub or internal bus)
   - Offline: enqueue to Push Notification Service (APNs/FCM)
5. Chat Server 2 delivers over WS to Client B
6. Client B sends ACK → `delivered` status written

**Group chat fan-out:** for 500-member group, fan-out service writes to 500 recipients. Async via Kafka. Accept 1–2s delay for large groups.

---

### Scale + reliability

| Concern | Solution |
|---------|----------|
| WS connection state | Stateful — use sticky load balancing (consistent hash on user_id → Chat Server) |
| Chat Server crash | Client reconnects; Kafka cursor ensures no messages lost |
| Message ordering | ULID/Snowflake IDs (time-sortable); Cassandra clustering key |
| Message dedup on retry | Idempotency key = `(sender_id, client_msg_id)` |
| Hot group chat | Shard by chat_id; fan-out workers scale independently |
| Read history (pagination) | `SELECT WHERE chat_id=X AND created_at < cursor LIMIT 50` |

---

## Worked Example 5: Design a Search Autocomplete

### Requirements

**Functional:**
- User types prefix → return top 10 completions ranked by popularity
- Results update as user types (each keystroke)
- Support ~1B searches/day as training signal

**Non-functional:**
- Latency: < 100ms p99 per prefix query
- Scale: 10M DAU, 10K QPS peak on autocomplete
- Freshness: trending terms appear within ~1 hour

**Out of scope:** spell correction, personalization (mention, park)

---

### Core data structure: Trie + Top-K per node

```
         root
          │
     ┌────┴────┐
    [a]       [b]
     │
   [ap]
     │
   [app] ← stores top-10: ["apple", "app store", "appify", ...]
     │
  [appl]
     │
  [apple] ← leaf
```

**Optimization:** Pre-compute and store top-K completions at each trie node. Query = traverse to prefix node, return stored list. O(prefix_length) lookup — no subtree scan at query time.

**Problem at scale:** Trie doesn't fit in memory for all prefixes in one node.

---

### High-level design

```
Offline (batch, hourly):
Search Logs → Kafka → Spark aggregation → top-K per prefix → Trie Builder → Trie snapshot → S3

Online (query path):
Client (debounced 300ms) → API Gateway → Autocomplete Service
                                              ↓
                                         Redis (prefix → top10, TTL 1h)
                                              ↓ (miss)
                                         Trie Service (loads from S3 snapshot)
                                              ↓ (miss)
                                         Return empty / stale
```

---

### Data model

```
Redis (primary serving layer)
  Key:   ac:{prefix}          (e.g. "ac:app")
  Value: ["apple","app store","appify",...] (JSON list, top 10)
  TTL:   1 hour

Trie (in-memory, Trie Service)
  Serialized trie loaded from S3 snapshot (rebuilt hourly)
  ~10–50 GB depending on vocabulary size

search_frequency table (offline)
  query       TEXT
  count       BIGINT
  window_end  TIMESTAMP
```

---

### Deep dive: debouncing + caching

**Client-side:** debounce keystrokes by 200–300ms → reduces QPS from 10 keys/word to ~2–3 requests/word.

**Cache strategy:**
- Short prefixes (≤ 3 chars) are queried by millions → cache with long TTL (1h) in Redis
- Long prefixes are rare → allow cache miss, fetch from Trie Service
- Prefix "t", "th", "the" are super hot → pre-warm cache on Trie rebuild

**Trie sharding:** Shard by first character of prefix (26 shards). Each shard owns a subset of the trie. Route requests via `hash(prefix[0])`.

---

### Freshness: incorporating trending queries

- Kafka streams search logs in real time
- Streaming aggregator (Flink/Spark Streaming) computes rolling 1-hour frequency
- If query frequency crosses threshold → trigger incremental trie update + Redis invalidation
- **Tradeoff:** More frequent updates = fresher results + more Trie rebuild cost

---

### Scale + reliability

| Concern | Solution |
|---------|----------|
| 10K QPS on autocomplete | Redis handles easily; Trie Service is fallback |
| Trie rebuild downtime | Blue-green: build new trie while old serves; atomic pointer swap |
| Cache invalidation | TTL-based (1h) + explicit purge on trending term threshold |
| Offensive / misspelled completions | Blocklist filter applied at Trie build time |
| Personalization (future) | Blend global top-10 with user's recent searches (client-side merge) |

---

## Advanced Patterns Reference

### Database Replication — quick reference
See **Database Replication** section above for leader-follower, multi-leader, leaderless.

### Sharding — quick reference
See **Database Sharding Strategies** section above.

### Queue — quick reference
See **Message Queue Deep Dive** section above.

---

## Key vocabulary to use in any design

| Term | When to say it |
|------|---------------|
| **Idempotency key** | Any write API that might retry |
| **Back-pressure** | Queue consumer can't keep up with producer |
| **Hot partition** | One shard gets disproportionate load |
| **Fan-out** | Distributing one event to many recipients |
| **Write-through cache** | Write to cache and DB together |
| **Read-through cache** | Cache fetches from DB on miss |
| **Thundering herd** | Many requests simultaneously miss cache and hit DB |
| **Eventual consistency** | Replicas may lag; ok for feeds, not ok for payments |
| **SLO / SLA** | Service Level Objective vs Agreement — know the difference |
| **Circuit breaker** | Stop calling a failing downstream; fail fast with fallback |
| **SAGA** | Compensating transactions for distributed workflows |
| **Sidecar proxy** | Network concerns (mTLS, retries, tracing) extracted to co-deployed proxy |
| **Replication lag** | Follower is behind leader; reads may be stale |
| **Read-your-writes** | Route user's reads to leader immediately after their write |

---

## Event Sourcing & CQRS

**Event Sourcing**: store every state change as an immutable event in an append-only log. Current state = replay of all events. The log is the source of truth, not a snapshot table.

**CQRS (Command Query Responsibility Segregation)**: separate the write model (commands that mutate state via events) from the read model (optimized projections rebuilt from the event log).

**When to use:**
- Audit trail required (financial transactions, medical records, compliance)
- Temporal queries: "what was the state at time T?"
- Complex domain with many event types (DDD contexts)
- Read and write load patterns differ significantly

**Tradeoffs:**
| Benefit | Cost |
|---------|------|
| Full audit history | Event log grows unboundedly (snapshot + truncate) |
| Rebuild any projection | Read side is eventually consistent |
| Time-travel queries | Event schema evolution is hard (v1 vs v2 events) |
| Decouple read/write scale | Operational complexity — two models to maintain |

**Interview trigger phrases:** "audit log", "replay transactions", "GDPR right to erasure" (tombstone events), "how did we get to this state?"

---

## API Design Patterns

### REST vs GraphQL vs gRPC — Decision Matrix

| Dimension | REST | GraphQL | gRPC |
|-----------|------|---------|------|
| Protocol | HTTP/1.1 | HTTP/1.1 | HTTP/2 |
| Payload | JSON | JSON | Protobuf (binary) |
| Latency | Medium | Medium | Low |
| Over-fetching | Common | Avoided (client specifies fields) | N/A |
| Type safety | No (OpenAPI optional) | Schema enforced | Strong (proto IDL) |
| Browser support | Native | Native | Needs grpc-web |
| Best for | Public APIs | Complex client queries | Internal microservices |

### Pagination Patterns

**Offset-based:** `GET /items?offset=100&limit=20`
- Simple but broken at scale: offset 1M requires DB to scan 1M rows then skip
- Inconsistent if rows inserted/deleted between pages

**Cursor-based:** `GET /items?cursor=eyJpZCI6MTAwfQ&limit=20`
- Cursor = opaque token encoding last-seen position (e.g., base64 of `{id: 100}`)
- DB query: `WHERE id > 100 LIMIT 20` — uses index, O(log n) not O(offset)
- Consistent under concurrent inserts
- Cannot jump to arbitrary page (sequential only)

**Use cursor-based for all production APIs at scale.**

### Idempotency Keys
- Client generates unique key per logical operation (UUID)
- Server stores `(idempotency_key → response)` for TTL period
- On retry, return stored response without re-executing
- Critical for POST/PUT that mutate state (payments, order creation)

### Rate Limiting Headers
```
X-RateLimit-Limit: 1000        # requests per window
X-RateLimit-Remaining: 950     # remaining in current window
X-RateLimit-Reset: 1716998400  # Unix timestamp when window resets
Retry-After: 30                # seconds to wait if 429 returned
```

### Versioning Strategies
| Strategy | Example | Tradeoff |
|----------|---------|----------|
| URL path | `/v1/users` | Clear, cache-friendly; proliferates routes |
| Accept header | `Accept: application/vnd.api+json;version=2` | RESTful; harder to test in browser |
| Query param | `/users?api_version=2` | Easy to add; pollutes query string |

**Recommendation**: URL path versioning for public APIs (simple, explicit); header versioning for internal APIs.

---

## Storage Engine Internals

### LSM Tree (Log-Structured Merge Tree)
**Write path:** write → in-memory memtable (sorted) → when full, flush to immutable SSTable on disk → background compaction merges SSTables → Bloom filter per SSTable for read optimization.

- **Write amplification**: low (sequential writes only)
- **Read amplification**: high (check Bloom filter per level, then SSTable)
- **Space amplification**: medium (stale values in uncompacted SSTables)
- **Used by**: Cassandra, RocksDB, LevelDB, HBase

### B-Tree
**Structure**: balanced tree of fixed-size pages (4KB); internal nodes hold separator keys; leaf nodes hold data or pointers; page splits on overflow.

- **Read amplification**: low (tree height ≈ 3-4 for billions of rows)
- **Write amplification**: high (random writes, page splits can cascade)
- **Space amplification**: low (compact, no stale versions)
- **Used by**: PostgreSQL, MySQL InnoDB, SQLite

### WAL (Write-Ahead Log)
Every write appended to WAL before modifying data pages. On crash: replay WAL from last checkpoint to restore consistency. Enables durability (`fsync` WAL entry = durable write).

### Decision
| Workload | Choose |
|----------|--------|
| Write-heavy, high throughput | LSM (Cassandra, RocksDB) |
| Read-heavy, complex queries | B-Tree (Postgres, MySQL) |
| Mixed with strong ACID | B-Tree + WAL |
| Time-series, append-only | LSM |

---

## Geo-Distributed Systems

### Multi-Region Architecture

**Active-Passive:** one region serves all writes (leader); other regions replicate asynchronously and serve reads. Failover: promote a follower to leader (RPO = replication lag, RTO = minutes).

**Active-Active:** all regions accept writes; conflict resolution required. Higher availability, lower write latency globally. Harder to implement correctly.

### Geo-Routing
- **Latency-based DNS**: Route53/CloudFlare routes user to nearest healthy region by measured latency
- **Anycast**: single IP announced from multiple PoPs; BGP routes to topologically nearest; used for CDN, DNS (1.1.1.1, 8.8.8.8)

### Cross-Region Consistency
Replication lag = typically 50-200ms cross-region. Options:
1. **Tolerate stale reads**: social feeds, product catalog
2. **Read from leader**: payments, profile (latency penalty)
3. **Synchronous replication**: strong consistency, write latency = worst-region RTT

### Conflict Resolution in Active-Active
| Strategy | Mechanism | When |
|----------|-----------|------|
| LWW (Last Write Wins) | Highest timestamp wins | Tolerate data loss, simple |
| CRDT | Mathematically convergent data types (counters, sets) | Counters, shopping cart |
| Application merge | Custom business logic | Complex domain objects |
| Version vectors | Track causality; surface conflict to user | User-owned data (Google Docs) |

### Google Spanner — TrueTime
Spanner uses GPS + atomic clocks to bound clock uncertainty to ε (typically 1-7ms). Before a transaction commits, wait ε to guarantee external consistency: if T1 commits before T2 starts in real time, T1.commit_timestamp < T2.commit_timestamp always. Enables globally consistent snapshots without coordination.

---

## Data Pipeline Architecture

### Lambda Architecture
Three layers running in parallel:
- **Batch layer**: recomputes correct views over all historical data (MapReduce, Spark); high latency, high accuracy
- **Speed layer**: processes recent data in real time (Kafka Streams, Flink); low latency, approximate or recent-only
- **Serving layer**: merges batch + speed layer results to answer queries

**Problem**: two codepaths = double maintenance burden.

### Kappa Architecture
Eliminate batch layer. Kafka as durable, replayable log (source of truth). Stream processor handles both real-time and historical reprocessing by replaying from beginning of log. Simpler operationally when stream processing can handle reprocessing load.

### ETL vs ELT
| | ETL | ELT |
|-|-----|-----|
| Transform where | Before loading | After loading (in DW) |
| Tooling | Informatica, Glue | dbt, Dataform |
| Flexibility | Schema must be defined upfront | Raw data preserved; schema-on-read |
| Best for | Traditional DW (Redshift) | Modern cloud DW (BigQuery, Snowflake) |

### Stream Processing Concepts
- **Watermark**: declares "all events with timestamp ≤ T have arrived"; enables windows to close without waiting forever for late data
- **Tumbling window**: fixed, non-overlapping intervals (e.g., 1-min buckets); each event in exactly one window
- **Sliding window**: overlapping intervals (e.g., last 60 min, updated every 1 min); each event in multiple windows
- **Session window**: gap-based; window closes after inactivity gap (e.g., user session analytics)
- **Backpressure**: consumer signals producer to slow down when buffer full; prevents OOM; Kafka: consumer group lag; Flink: credit-based flow control

---

## Worked Example 6: Design a Distributed Key-Value Store (DynamoDB-style)

### Requirements
- **Functional**: get(key), put(key, value), delete(key)
- **Scale**: 10M writes/s, 50M reads/s; values up to 400KB; 100TB total data
- **Non-functional**: 99.9% availability; p99 latency < 10ms; eventual consistency (tunable)

### API
```
GET  /items/{key}                          → 200 {value, version} | 404
PUT  /items/{key}  body:{value}            → 200 {version}
DELETE /items/{key}                        → 204
```
Optional header: `Consistency: strong | eventual`

### Data Model — Consistent Hashing + Virtual Nodes
- Hash key to 0..2³² ring position
- Each physical node owns M virtual nodes (vnodes) spread across ring
- vnodes → even load distribution; on add/remove node, only vnodes reassigned
- Lookup: consistent hash → owning node (O(log N) binary search on sorted ring)

### Replication (N/W/R Quorum)
- N = replication factor (e.g., 3); replicate to N consecutive nodes on ring
- W = write quorum (e.g., 2); PUT returns success when W nodes acknowledge
- R = read quorum (e.g., 2); GET reads from R nodes, returns latest version
- Tuning: W+R > N → strong consistency; W=1,R=1 → high throughput eventual consistency

### Conflict Resolution — Vector Clocks
Each write tagged with vector clock `{nodeId: counter}`. On conflict (concurrent writes), return both versions to client; client or application merges. DynamoDB uses this approach; shopping cart example: union of both carts.

### Read Repair + Anti-Entropy
- **Read repair**: on read, if R replicas return different versions, coordinator writes latest back to stale replicas in background
- **Anti-entropy (Merkle Tree)**: each node maintains Merkle tree over its key space; gossip Merkle root hashes; on mismatch, exchange only differing subtrees (O(differences) not O(all keys))

### Gossip Protocol — Membership
- Each node maintains membership list with heartbeat counters
- Every T seconds, node picks random peer and exchanges membership lists
- A node is suspected dead if heartbeat hasn't incremented in k rounds
- Epidemic dissemination: info propagates in O(log N) rounds

### Write Path (Deep Dive)
```
Client → Coordinator (consistent hash) → write to W replicas in parallel
         │
         ├── Each replica: append to WAL → write to in-memory store → ACK
         │
         └── Return success to client when W ACKs received
             Background: hinted handoff if replica down (store hint, replay when node returns)
```

### Scale + Reliability

| Dimension | Target | Mechanism |
|-----------|--------|-----------|
| Throughput | 10M writes/s | Consistent hashing, horizontal sharding |
| Availability | 99.9% | N=3 replication, hinted handoff |
| Latency p99 | <10ms | In-memory store, parallel replication |
| Durability | 99.999% | WAL + cross-AZ replication |
| Fault tolerance | Single node failure | Quorum writes, read repair |

### Monitoring

| Metric | Alert threshold |
|--------|----------------|
| Replication lag | > 100ms |
| Write success rate | < 99.9% |
| p99 read latency | > 10ms |
| Gossip convergence time | > 5s |
| Hinted handoff queue depth | > 1000 |

---

## Capacity Planning Template

### QPS Estimation
```
DAU × actions_per_user_per_day / 86400 = average QPS
Peak QPS = average × peak_multiplier (2-5×)
```
Example: 10M DAU, 10 reads/day → 10M × 10 / 86400 ≈ 1,160 avg QPS → ~5,000 peak QPS

### Storage Estimation
```
users × data_per_user × replication_factor × (1 + overhead_factor)
```
Example: 10M users × 1KB profile × 3 replicas × 1.3 overhead = ~39GB

For time-series: `events_per_second × bytes_per_event × seconds_per_day × retention_days`

### Bandwidth
```
Ingress = write_QPS × avg_payload_size
Egress  = read_QPS  × avg_response_size
```
Example: 1000 writes/s × 1KB = 1 MB/s ingress; 5000 reads/s × 2KB = 10 MB/s egress

### Cache Sizing
- Cache the hot 20% of data that serves 80% of reads (Pareto principle)
- `cache_size = working_set_size × 0.2`
- Memory per cache node: 8-256GB; estimate nodes needed
- TTL: balance freshness vs hit rate; longer TTL = higher hit rate = more stale data

### Memory Requirements for In-Memory State
```
records_in_memory × bytes_per_record × overhead_factor (1.5-3×)
```
Redis overhead: ~70 bytes per key + value size. Example: 10M sessions × (32B key + 200B value) × 2× overhead = ~4.6GB

---

## PACELC Theorem (extends CAP)

**CAP** says: during a **P**artition, choose **C**onsistency or **A**vailability.
**PACELC** says: even when there's **E**lse (no partition), choose **L**atency or **C**onsistency.

```
                 Network Partition?
                  /              \
                YES               NO (normal operation)
               /                     \
    Choose: C or A              Choose: L or C
    (CAP tradeoff)              (latency vs consistency)
```

| System | Partition (C/A) | Normal (L/C) | Example |
|--------|----------------|--------------|---------|
| Cassandra | AP | EL | Eventual consistency, low latency |
| HBase | CP | EC | Strong consistency, higher latency |
| DynamoDB | AP | EL (configurable) | Default eventual, optional strong |
| Spanner | CP | EC | Globally consistent, higher latency |
| MySQL (sync replica) | CP | EC | ACID, read from leader |

**Interview soundbite:** "CAP only covers partition scenarios. For normal operation, I use PACELC: Cassandra optimizes for low latency (EL), Spanner for consistency (EC). My choice depends on whether users can tolerate stale reads."

---

## Distributed Locking

**Problem:** Multiple service instances must not execute a critical section simultaneously (e.g., only one worker deducts inventory, one leader schedules jobs).

### Redis-based Lock (Redlock)

```python
# SET key value NX PX ttl_ms — atomic: set only if not exists, with expiry
SET lock:order_123 {client_id} NX PX 5000   # acquire
# Critical section here
DEL lock:order_123                           # release (only if still your lock — use Lua script)
```

**Single Redis node:**
- Works for most use cases (Redis rarely fails)
- Risk: if Redis crashes between acquire and release, lock is lost; TTL limits damage

**Redlock (N=5 independent Redis nodes):**
1. Record start time `t1`
2. Try to acquire lock on all 5 nodes with short timeout
3. Lock acquired if: ≥3 nodes succeed AND total elapsed < TTL
4. Lock validity = TTL - (elapsed + clock_drift)
5. Release on all 5 nodes regardless of success

**Controversy (Martin Kleppmann):** Redlock doesn't protect against GC pauses — a client can hold a "valid" lock while paused, then act after TTL expires while another client acquired it.

**Fix — Fencing Tokens:**
```
Client1 acquires lock → gets token=33
Client1 paused (GC)
Token 33 expires → Client2 acquires lock → gets token=34, writes to DB
Client1 resumes → tries to write with token=33 → DB rejects (33 < 34)
```
Storage layer must reject writes with stale tokens. ZooKeeper's monotonically increasing `zxid` implements this naturally.

### ZooKeeper-based Lock

- Create ephemeral sequential node: `/locks/order_123/lock-0000000001`
- List children; acquire if your node has lowest sequence number
- Watch the node with the next-lower sequence (not all nodes — avoids herd effect)
- ZooKeeper deletes ephemeral node on client disconnect → automatic lock release on crash

**Pro:** No TTL expiry needed (session-based); fencing tokens via zxid  
**Con:** ZooKeeper adds operational complexity; requires ZK cluster

**Decision:**
- Simple use case, Redis already in stack → Redis single-node lock with TTL
- Need strong safety guarantees → ZooKeeper + fencing tokens
- Cross-region → don't use distributed locks; redesign with idempotency keys + optimistic locking

---

## Database Indexing — First Principles

**Root problem:** Full table scan is O(n). An index trades write overhead for O(log n) or O(1) read lookup.

### B-Tree Index (default in Postgres, MySQL)

```
Query: WHERE user_id = 42
Without index: scan all rows O(n)
With index on user_id: traverse B-tree → leaf page → row pointer O(log n)

B-tree structure (height ≈ 3-4 for 100M rows):
         [50 | 100]
        /      |     \
  [10|20]   [60|80]  [110|150]
    ↓↓↓        ↓↓↓       ↓↓↓
  data pages  data pages  data pages
```

**Types of queries and index support:**
| Query type | Index helps? | Notes |
|-----------|-------------|-------|
| `WHERE a = ?` | Yes (equality) | Single column index on `a` |
| `WHERE a = ? AND b = ?` | Yes | Composite `(a, b)` index |
| `WHERE a > ? AND a < ?` | Yes | Range scan on B-tree leaf level |
| `WHERE a = ? OR b = ?` | Partial | Two separate indexes, merged by DB |
| `WHERE LOWER(email) = ?` | No (on plain index) | Need expression/functional index |
| `ORDER BY a LIMIT 10` | Yes | Index scan in order, no filesort |

### Composite Index — Column Order Matters

**Rule:** Index `(a, b, c)` is useful for: `WHERE a=?`, `WHERE a=? AND b=?`, `WHERE a=? AND b=? AND c=?`. NOT useful for: `WHERE b=?` (skips leading column).

**Selectivity principle:** Put the most selective (highest cardinality) column first in a composite index when doing equality filters. Exception: if you need range on one column, range column goes last.

### Covering Index

An index that contains all columns a query needs — the query can be answered from the index alone without touching the table (index-only scan).

```sql
-- Query:
SELECT user_id, email FROM users WHERE user_id > 1000 LIMIT 100;

-- Covering index:
CREATE INDEX idx_covering ON users(user_id, email);
-- DB never reads the main table rows — reads only the index pages
```

### Partial Index

Index only a subset of rows where a condition is true — smaller index, less write overhead.

```sql
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';
-- Only indexes active users; queries filtering active users use this; others do full scan
```

**Use when:** Most queries filter on a low-selectivity column (status=active for 10% of rows). Partial index is 10% the size of full index.

### Index Write Overhead

- Every INSERT/UPDATE/DELETE must update all indexes on the table
- Wide tables with many indexes → writes become slow
- Rule of thumb: 3-5 indexes per table for OLTP; more for read-only analytical tables
- Avoid indexing columns with very low cardinality (boolean, status with 2 values) unless partial index

**Interview trigger:** "Query is slow" → check EXPLAIN plan, look for Seq Scan → add index. "Writes are slow" → too many indexes; audit and drop unused ones.

---

## Security Fundamentals in System Design

**Root problem:** Systems expose endpoints; authentication (who are you?) and authorization (what can you do?) must be built in, not bolted on.

### Authentication: OAuth2 + JWT

```
OAuth2 Authorization Code Flow (for user-facing apps):
1. User clicks "Login with Google"
2. App redirects → Google auth server with client_id + redirect_uri + scope
3. User consents → Google returns authorization code to redirect_uri
4. App exchanges code → Google token endpoint → access_token + refresh_token
5. App uses access_token in API calls; refresh_token to get new access_token when expired

JWT (JSON Web Token) structure:
HEADER.PAYLOAD.SIGNATURE
{"alg":"RS256"} . {"sub":"user123","exp":1700000000,"roles":["admin"]} . [RS256 signature]

Verification: recipient verifies signature with public key → no DB lookup needed
```

**Stateless vs Stateful tokens:**
| | JWT (stateless) | Session token (stateful) |
|-|----------------|------------------------|
| Validation | Verify signature only (fast, no DB) | DB lookup required (slower) |
| Revocation | Hard: JWT valid until expiry | Instant: delete session from DB |
| Use when | Microservices (no shared session store) | Monolith, need instant logout |

**JWT security rules:**
- Short expiry (15 min–1 hour); long-lived refresh tokens stored httpOnly cookie
- Validate `exp`, `iss`, `aud` claims — don't just verify signature
- Use RS256 (asymmetric) for public key distribution; HS256 only for single-service use
- Never put sensitive data in JWT payload (it's base64-encoded, not encrypted)

### API Security

**Rate limiting:** per-IP and per-user-token to prevent brute force + DDoS (see Rate Limiter section)

**Input validation:**
- Validate at API boundary: type, length, format, allowed values
- Parameterized queries / ORMs to prevent SQL injection — never concatenate user input into SQL
- Escape output in templates to prevent XSS — Content-Security-Policy header

**HTTPS/TLS everywhere:**
- TLS 1.2 minimum; TLS 1.3 preferred (1-RTT handshake)
- HSTS header: forces browser to use HTTPS for 1 year
- Certificate pinning for mobile apps

**Secrets management:**
- Never hardcode API keys/credentials in code or config files
- Use secret managers: AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault
- Rotate credentials automatically; audit access

**mTLS (mutual TLS) for service-to-service:**
- Both sides present certificates → authenticates client to server AND server to client
- Eliminates need for API keys in inter-service calls
- Typically handled by service mesh (Istio/Envoy) — app code doesn't change

**Interview soundbite:** "I secure at multiple layers: TLS in transit, JWT for user auth (short expiry), mTLS for service-to-service, parameterized queries to prevent injection, rate limiting to prevent abuse, secrets in a vault not in code."

---

## Task Scheduling at Scale

**Problem:** Thousands of jobs need to run at specific times (cron jobs, delayed notifications, retries) — a single-machine cron doesn't scale and is a SPOF.

### Architecture

```
Scheduler Service (stateless)
       │
       ├── Job Store (DB/Redis): stores job + next_run_at + status
       │
       ├── Leader Election (ZooKeeper/etcd): only one scheduler instance
       │   fires jobs to avoid duplicate execution
       │
       └── Message Queue (Kafka/SQS): scheduler publishes job → workers consume
                 │
           Worker Pool (stateless): execute job, mark complete, handle retry
```

### Key design decisions

**Exactly-once execution:**
- Scheduler acquires distributed lock per job before enqueueing
- Idempotency key per job run → worker deduplicates on re-delivery
- DB `status` column: pending → in_progress → completed/failed; use optimistic lock (CAS on status)

**Delayed jobs:**
- Redis Sorted Set: `ZADD jobs:pending <timestamp> <job_id>`; scheduler polls `ZRANGEBYSCORE 0 <now> LIMIT 100`; atomic claim with Lua script
- Alternative: SQS visibility delay (up to 15 min); Step Functions for multi-step workflows

**Retries with backoff:**
```
retry_at = now + base_delay × 2^attempt + jitter
Attempt 1: 30s; Attempt 2: 60s+jitter; Attempt 3: 120s+jitter
Max retries = 5; then → Dead Letter Queue for manual inspection
```

**High-frequency cron (every second):**
- Partition by hash(job_id) across multiple scheduler instances (each owns a shard)
- Clock skew: use DB `NOW()` not application clock to determine due jobs

**Interview trigger phrases:**
- "Send daily digest emails" → delayed job queue
- "Retry failed payments" → retry queue with exponential backoff + DLQ
- "Scheduled reports" → distributed cron with leader election
- "Rate-limited third-party API calls" → token bucket in worker + Redis

---

## Search System Design (Inverted Index)

**Problem:** Full-text search requires finding all documents containing a term across millions/billions of documents in < 100ms — sequential scan is impossible.

### Inverted Index — First Principles

```
Forward index: doc_id → list of words in that doc (natural storage)
Inverted index: term → list of (doc_id, position, frequency) — optimized for search

Example:
doc1: "distributed systems are complex"
doc2: "complex systems require careful design"

Inverted index:
  "complex"     → [(doc1, pos=3, freq=1), (doc2, pos=0, freq=1)]
  "systems"     → [(doc1, pos=1, freq=1), (doc2, pos=1, freq=1)]
  "distributed" → [(doc1, pos=0, freq=1)]
  "design"      → [(doc2, pos=3, freq=1)]

Query "distributed systems": intersect posting lists for both terms → doc1
```

### Ranking (TF-IDF + BM25)

- **TF (Term Frequency):** how often term appears in doc → more occurrences = more relevant
- **IDF (Inverse Document Frequency):** `log(N / df)` where N=total docs, df=docs containing term → rare terms = higher IDF score → more discriminating
- **BM25:** improved TF-IDF with document length normalization; standard in Elasticsearch/Lucene

### Elasticsearch Architecture

```
Index → N Shards (primary + replicas)
Shard = Lucene instance with its own inverted index

Write: client → coordinator → route to shard (hash(doc_id)) → primary writes → replicas
Read:  client → coordinator → broadcast to all shards → merge + rank → return top-K

Refresh interval (1s default): new docs not searchable until segment refresh
Flush (fsync): segments durably written to disk every 30s or after buffer fills
```

### Scale decisions

| Concern | Solution |
|---------|----------|
| Index too large for one node | Shard by doc_id hash; 30-50GB per shard is healthy |
| Query latency | Cache hot queries in Redis; use filter cache for repeated filters |
| Indexing throughput | Bulk API (1000 docs/batch); async indexing via Kafka |
| Schema changes | Add new fields without downtime; changing field types requires reindex |
| Near-real-time | Reduce refresh interval to 100ms (higher CPU) or use search-after pagination |

**Interview trigger:** "Build a search feature" → inverted index + BM25 ranking. "Search across user-generated content" → Elasticsearch. "Autocomplete" → trie or prefix index (see Autocomplete section). "Fuzzy search / typo tolerance" → Levenshtein distance or n-gram tokenization.

---

## File Storage System (S3-style)

**Problem:** Store billions of files (photos, videos, documents) — no single disk, must survive node failures, serve globally.

### Architecture — First Principles

```
WHY chunks: large files (10GB video) can't fit in memory, fail mid-transfer,
            need deduplication across users uploading same file.

Client → Metadata Service → DB (file_id, user_id, chunks[], size, content_type)
       → Chunk Store    → Object Storage (each chunk is content-addressed: SHA256(chunk) = key)
       → CDN            → serve reads with geographic caching
```

### Chunked Upload

```
1. Client calls POST /files/initiate → server returns upload_id + presigned chunk URLs
2. Client splits file into 5MB chunks; uploads each in parallel via presigned URLs
3. Each chunk stored as content-addressed blob: key = SHA256(chunk_bytes)
4. Client calls POST /files/complete with upload_id + [chunk_hash, ...] → server assembles metadata
5. Download: fetch chunk list from metadata DB → fetch each chunk in parallel → stream to client
```

**Content-addressing benefits:**
- Deduplication: if two users upload same file, chunks are shared (only one storage copy)
- Integrity: verify download by hashing chunks; any corruption detected
- Immutability: chunks never updated, only new chunks written → simpler caching

### Metadata vs Chunk Separation

| Service | Storage | Pattern |
|---------|---------|---------|
| Metadata | Relational DB (Postgres) or DynamoDB | User permissions, file hierarchy, version history |
| Chunks | Object storage (S3, GCS) or distributed blob store | Immutable, content-addressed, replicated |
| CDN | Edge caching | Read-heavy; cache by content hash → infinite TTL (content never changes) |

### Reliability

- **Replication:** 3 copies across AZs; erasure coding (6+3) for cold storage (saves space vs 3× replication)
- **Versioning:** each upload creates new version; metadata tracks version history; deletes are soft (mark deleted)
- **Access control:** signed URLs with TTL (S3 presigned URL pattern) — client calls metadata service, gets temporary download URL directly to object store; metadata service never proxies bytes

**Interview trigger:** "Design Google Drive / Dropbox / photo storage" → chunked upload + metadata service + content-addressed chunks + CDN + presigned URLs.

---

## Notification System — Deep Dive

**Problem:** Send millions of transactional notifications (push, email, SMS) reliably with deduplication, user preferences, and rate limiting.

### Architecture

```
Trigger Source (payment_service, order_service, etc.)
       │ publishes event
       ▼
Notification Service
  ├── Preference Check → user opted out? channel enabled? → skip or proceed
  ├── Template Engine → populate message with user-specific data
  ├── Deduplication  → idempotency key = (event_id, user_id, channel)
  │                     → check Redis SET (TTL 24h) → skip if already sent
  └── Channel Router
        ├── Push  → APNs (iOS) / FCM (Android) → handle token expiry
        ├── Email → SES / SendGrid → bounce/complaint handling
        └── SMS   → Twilio / SNS

Retry Queue (per channel):
  → Failed sends → DLQ after 3 attempts
  → DLQ → alert ops team for investigation
```

### Key design decisions

**Deduplication:** Store `(event_id, user_id, channel)` in Redis with TTL = delivery window (24h). Before sending, SETNX → 1 means proceed; 0 means already sent.

**APNs / FCM token management:**
- Tokens expire or change when user reinstalls app or device OS refreshes token
- On 410 Gone (APNs) or `NotRegistered` (FCM) → mark token invalid in DB immediately
- Token refresh: device calls your server on new token → update DB

**Rate limiting per user:** Max N notifications per user per hour per channel. Enforce in Notification Service before routing to providers.

**Ordering guarantees:** Notifications within a session should be ordered — use Kafka partitioned by user_id to maintain per-user ordering.

**Priority tiers:**
| Priority | Examples | SLA | Queue |
|----------|---------|-----|-------|
| Critical | Auth OTP, payment receipt | < 1s | Dedicated high-priority queue |
| High | Order confirmation | < 5s | Standard queue |
| Low | Marketing, digest | < 5 min | Batched queue, off-peak |

**Interview soundbite:** "Notification system is a fan-out problem. I decouple trigger sources from delivery via Kafka. Deduplication via idempotency key in Redis prevents duplicate sends on retry. Per-channel worker pools scale independently. DLQ catches undeliverable notifications for ops triage."
