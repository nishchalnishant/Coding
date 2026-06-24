---
tags: [coding, amazon-interview, system-design, architecture]
topic: System Design — Amazon SDE-2
difficulty: sde2
---

# System Design Guide — Amazon SDE-2

> SDE-2 system design scope: URL Shortener, Rate Limiter, Distributed Cache, News Feed (simplified). Know the 5-step framework cold. You are expected to make reasonable tradeoff decisions and explain them, but you are NOT expected to handle petabyte-scale distributed consensus or ML pipeline design.




> [!important] The Framework First
> Every system design answer follows the same skeleton. Internalize this framework before studying individual designs. An imperfect answer with strong structure beats a brilliant answer with no structure.

---

## The Universal System Design Framework

```
Total time: 45 minutes

Step 1 — Requirements (5 min)
Step 2 — Capacity Estimation (3 min)  
Step 3 — High-Level Architecture (5 min)
Step 4 — Deep Dive (20 min)
Step 5 — Scale & Failure Handling (7 min)
Step 6 — Wrap-up & Tradeoffs (5 min)
```

### Step 1: Requirements Clarification

Never assume. Always clarify:

**Functional requirements (what the system does):**
- What are the core features? (Limit to 3 for 45 min)
- What does a user request look like?
- What does the response look like?

**Non-functional requirements (how well it does it):**
- Scale: How many users? Daily Active Users (DAU)?
- Read/Write ratio: read-heavy (Twitter timeline) vs write-heavy (logging)?
- Latency: real-time (<100ms) vs eventual (minutes)?
- Consistency: strong (banking) vs eventual (social feed)?
- Availability: 99.9% (3 nines) vs 99.99% (4 nines)?
- Durability: can data be lost? (logs = ok, payments = never)

### Step 2: Capacity Estimation

```
Key numbers to memorize:
  1 million  = 10^6
  1 billion  = 10^9
  1 day      = 86,400 sec ≈ 10^5 sec
  1 year     = 3 × 10^7 sec

Rule of thumb: 10M DAU → ~100 req/sec (100 requests per user per day / 86400)

Storage:
  1 tweet (280 chars)     = ~300 bytes
  1 photo (compressed)    = ~300 KB
  1 video (1 min, 720p)   = ~50 MB
  1 user record           = ~1 KB

Bandwidth:
  QPS × avg_response_size = bandwidth

Example (Twitter):
  300M DAU, 50% active daily = 150M active
  Each user reads 100 tweets/day → 150M × 100 / 86400 = ~170,000 reads/sec
  Each user writes 1 tweet/day  → 150M / 86400 = ~1,700 writes/sec
  Read:Write ≈ 100:1 (heavily read-dominant)
```

### Step 3: High-Level Architecture

Start with this template for every system:

```
[Client]
   │
[Load Balancer / API Gateway]
   │
[Application Servers / Microservices]
   │              │
[Cache (Redis)]  [Message Queue (Kafka)]
   │
[Primary DB]  →  [Read Replicas]
   │
[CDN (for static assets)]
[Object Store (S3 for media)]
[Search (Elasticsearch)]
```

---

## Core Building Blocks (Memorize These)

### Databases

| Need | Choice | Why |
|------|--------|-----|
| Structured data, ACID transactions | PostgreSQL / MySQL | Relational, joins, strong consistency |
| Document storage, flexible schema | MongoDB | JSON-like, easy to scale horizontally |
| Key-value, ultra-low latency | Redis, DynamoDB | O(1) lookup, in-memory option |
| Time-series data | InfluxDB, Cassandra | Optimized for append-heavy time-ordered data |
| Full-text search | Elasticsearch | Inverted index, ranking, fuzzy matching |
| Graph relationships | Neo4j | Efficient traversal of highly connected data |

**Rule**: Default to PostgreSQL unless you have a specific reason not to. Explain the reason.

### Caching

```
Cache Hierarchy:
  L1: In-process (application memory) — fastest, limited size
  L2: Distributed cache (Redis/Memcached) — fast, shared across servers
  L3: CDN — static assets, geographic distribution

Cache Strategies:
  Cache-Aside (Lazy Loading): App reads cache → miss → reads DB → writes cache
    + Cache only what's needed
    - Cold start penalty; stale data possible

  Write-Through: Write to cache and DB simultaneously
    + Cache always fresh
    - Write latency higher; cache filled with unread data

  Write-Behind (Write-Back): Write to cache → async write to DB
    + Lowest write latency
    - Data loss risk if cache crashes before DB write

Cache Eviction Policies:
  LRU (Least Recently Used)  — default choice
  LFU (Least Frequently Used) — for access-pattern-stable data
  TTL (Time To Live)          — for time-sensitive data (sessions, OTPs)

Cache Invalidation Strategies:
  TTL-based: simple, may serve stale data briefly
  Event-driven: DB change triggers cache invalidation (pub/sub)
  Write-through: always consistent but higher write cost
```

### Message Queues

```
When to use: decouple producers from consumers, async processing, fan-out

Kafka:
  - Durable, ordered, replayable log
  - Use for: event sourcing, audit logs, high-throughput streaming
  - Topics → Partitions (ordered within partition)
  - Consumer groups: each group gets all messages; each partition → one consumer

RabbitMQ:
  - Traditional message broker, ack-based delivery
  - Use for: task queues, work distribution, fan-out with routing

SQS (AWS):
  - Managed queue, at-least-once delivery
  - Use for: simple decoupling in AWS environments

Fan-out pattern (Twitter notifications):
  Tweet created → Kafka topic → multiple consumers
    Consumer 1: Write to follower feeds
    Consumer 2: Send push notifications  
    Consumer 3: Update search index
```

### Load Balancing

```
Algorithms:
  Round Robin: requests distributed evenly — stateless services
  Least Connections: route to server with fewest active connections
  IP Hash: same client → same server (sticky sessions)
  Consistent Hashing: same key → same server even as cluster scales

Layer 4 (Transport) vs Layer 7 (Application):
  L4: Routes by IP/port — fast, no content inspection
  L7: Routes by URL, headers, cookies — can do smart routing, SSL termination
```

### Sharding (Horizontal Partitioning)

```
Why: Single DB can't handle scale → split data across multiple DBs (shards)

Strategies:
  Range-based: shard by value range (user_id 1-1M → shard1)
    + Simple, range queries efficient
    - Hotspots if data not uniformly distributed

  Hash-based: shard = hash(key) % num_shards
    + Uniform distribution
    - Range queries hit all shards; resharding is painful

  Directory-based: lookup table maps key → shard
    + Flexible
    - Lookup table becomes a bottleneck/SPOF

Consistent Hashing (best for dynamic cluster):
  + Minimal data movement when nodes added/removed
  + Virtual nodes handle uneven load
```

---

## Design 1: URL Shortener (bit.ly)

**Functional**: Shorten URL, redirect to original, (optional) analytics

**Capacity**: 500M URLs/month, 10:1 read:write → ~2000 writes/sec, 20,000 reads/sec

**Key Design Decisions:**

```
Short code generation:
  Option A: hash(long_url) → take first 7 chars
    Problem: collisions, not unique per user
  Option B: Base62 encode a counter (0-9, a-z, A-Z)
    62^7 = 3.5 trillion unique URLs — sufficient
    Problem: predictable sequential IDs (security concern)
  Option C: Random 7-char Base62 + uniqueness check in DB
    Best: unpredictable, unique

Storage:
  1 URL record ≈ 500 bytes
  500M × 500 bytes = 250 GB/month → 3 TB/year
  → Use NoSQL (DynamoDB or Cassandra) for KV lookup (short_code → long_url)

Redirect:
  301 (permanent): client caches → reduces server load, breaks analytics
  302 (temporary): client always asks server → accurate analytics
  → Use 302 if you need click analytics

Caching:
  80/20 rule: 20% of URLs = 80% of traffic
  Cache hot short_codes in Redis with LRU eviction
  TTL = 24 hours for most URLs

Schema:
  urls: {short_code (PK), long_url, created_at, user_id, expiry_at}
  analytics: {short_code, timestamp, ip, country, device} → write to Kafka
```

**Architecture:**
```
Client → Load Balancer → URL Service (stateless, horizontally scalable)
         → Redis Cache (cache-aside, 300ms TTL hits)
         → Cassandra (short_code → long_url, single-region write, multi-region read)
         → Kafka (click events) → Analytics Service → ClickHouse
```

---

## Design 2: Rate Limiter

**Functional**: Limit each user to N requests per time window

**Algorithms:**

```
Token Bucket (best for burst traffic):
  - Bucket holds max N tokens
  - Tokens refill at rate R per second
  - Request consumes 1 token; if empty → reject (429)
  + Allows bursts up to bucket size
  Implementation: Redis key per user; Lua script for atomic decrement + refill

Sliding Window Counter (most accurate):
  - Divide time into small sub-windows (e.g., 1-min window → 60 1-sec buckets)
  - Count requests in current window + weighted count from previous window
  + No burst artifacts at window boundary
  Implementation: Redis sorted set; score = timestamp; zcount by range

Fixed Window Counter (simplest):
  - Count requests in current 1-min window
  - Reset at window boundary
  - Problem: 2x burst at window boundary (end of min1 + start of min2)
```

**Distributed Rate Limiter:**
```
Problem: multiple app servers share rate limit state
Solution: Redis as centralized counter (atomic INCR + EXPIRE)

Race condition: 
  Thread 1 reads count=99 (limit=100) 
  Thread 2 reads count=99 simultaneously
  Both increment → count=101 (over limit)
Fix: Lua script (atomic read-check-increment) or Redis MULTI/EXEC

At scale (10M req/sec):
  Shard Redis by user_id hash
  Accept ~0.1% over-limit due to race conditions (tolerable for most APIs)
```

---

## Design 3: Twitter/News Feed

**Functional**: Post tweets, follow users, see personalized feed

**The Core Challenge**: Fan-out on write (push model) vs fan-out on read (pull model)

```
Fan-out on Write (Push):
  When user tweets → immediately write to all followers' feed tables
  + Fast reads (feed is pre-computed)
  - Write amplification: Katy Perry (100M followers) → 100M writes per tweet
  - Celebrities make this infeasible at scale

Fan-out on Read (Pull):
  When user opens feed → query tweets from all followed users
  + No write amplification
  - Slow reads: must query N followed users → merge sort → paginate

Twitter's Actual Solution: Hybrid
  Regular users (< 1M followers): fan-out on write → feed stored in Redis
  Celebrities (> 1M followers): fan-out on read → fetched at read time
  Reader merges: pre-computed feed + celebrity tweets → final timeline
```

**Schema:**
```sql
users:  {user_id, username, created_at, follower_count}
tweets: {tweet_id, user_id, content, created_at, like_count, retweet_count}
follows: {follower_id, followee_id, created_at}  -- partitioned by follower_id
feed:   {user_id, tweet_id, created_at}  -- Redis sorted set, score=timestamp
```

**Architecture:**
```
Write path:
  POST /tweet → Tweet Service → Cassandra (tweets)
                              → Kafka (tweet_created event)
                              → Fan-out Service (reads follower list)
                                → Redis (write to follower feeds)
                                → [skip if celebrity]

Read path:
  GET /feed → Feed Service → Redis (user feed) 
                           → for each celebrity followed: fetch recent tweets
                           → merge + sort + paginate
```

---

## Design 4: File Storage (Dropbox) — Awareness

**Not a core SDE-2 design. Know the key ideas:**

- **File chunking**: split files into 4 MB chunks; each chunk hashed (SHA-256); upload only changed chunks (delta sync).
- **Storage split**: metadata DB (Postgres) for folders/files/permissions; Object Storage (S3) for actual chunks.
- **Upload flow**: client uploads chunks directly to S3 via presigned URLs (bypasses app server); app records metadata after S3 upload completes.
- **Sync**: server sends diff of changed chunk IDs; client downloads only those.
- **Conflict resolution**: simplest approach is keep-both-versions with conflict marker (Dropbox style).

---

## Design 5: Video Streaming (YouTube) — Awareness

**Not a core SDE-2 design. Know the key ideas:**

- **Upload pipeline**: raw video → Object Storage → async transcoding service (Kafka trigger) → multiple resolutions (360p, 720p, 1080p) stored back in S3 → CDN.
- **Adaptive bitrate streaming (HLS/DASH)**: video split into 2-sec segments at each resolution; client downloads a manifest file; player switches resolution based on bandwidth.
- **CDN**: push popular videos to edge nodes; pull-on-first-request for the long tail.
- **Scale signal**: 500 hours uploaded/minute → ~300 TB/day of transcoded video; tiered storage (SSD for hot, cold storage for archive).

---

## Design 6: Distributed Cache (Redis at Scale)

**The Core Challenge**: When cache itself needs to scale beyond one node

```
Replication:
  Primary-Replica: writes go to primary, reads distributed to replicas
  Async replication → replicas may lag by milliseconds (eventual consistency)
  Use case: read-heavy workloads where slight staleness is OK

Cluster (Sharding):
  Redis Cluster: 16,384 hash slots distributed across nodes
  Client computes slot = CRC16(key) % 16384 → connects to correct node
  Resharding: move slots between nodes with zero downtime

Sentinel (High Availability):
  Monitors primary; if primary fails → promotes a replica to primary
  Automatic failover in ~30 seconds
  
Eviction under Memory Pressure:
  allkeys-lru: evict least recently used keys (default recommendation)
  volatile-lru: only evict keys with TTL set
  allkeys-random: random eviction (rarely the right choice)

Cache Stampede (Thundering Herd):
  Problem: cache key expires → 10,000 requests hit DB simultaneously
  Fix 1: Probabilistic early expiry (re-cache before TTL expires)
  Fix 2: Mutex lock on cache miss (only one request fetches from DB)
  Fix 3: Background refresh (always serve from cache; refresh async)
```

---

## Design 7: Chat System — Awareness

**Know the key ideas:**

- **Transport**: WebSocket (persistent TCP) for real-time; stateful chat servers; consistent hashing so same user → same server.
- **Message flow**: online → WebSocket push; offline → Message Queue → DB + push notification (APNS/FCM).
- **Storage**: Cassandra (append-heavy, time-ordered); partition by chat_id; sort by Snowflake ID.
- **Group chat**: fan-out on write for small groups (< 100 members); fan-out on read for large groups.
- **Presence**: heartbeat every 30s → Redis TTL key; "last seen" on disconnect.

---

## Design 8: Search Autocomplete — Awareness

**Know the key ideas:**

- **Data collection**: search events → Kafka → batch aggregation (hourly) → (query, score) pairs.
- **Trie storage**: in-memory trie on suggestion servers; each node caches top-5 suggestions; rebuilt from batch job every few hours (blue-green swap).
- **Latency**: client debounce 100ms; CDN for common prefixes; in-memory trie lookup < 1ms.
- **API**: `GET /autocomplete?q=ap` → top 5 completions.

---

## Numbers Every Candidate Should Know

```
Latency reference (L1 cache → disk → network):
  L1 cache hit:          0.5 ns
  L2 cache hit:          7 ns
  Main memory (RAM):     100 ns   (0.1 μs)
  SSD random read:       150 μs
  HDD seek:              10 ms
  Network: same datacenter: 0.5 ms
  Network: cross-region:    50–150 ms

Throughput reference:
  Single MySQL:          ~5,000 writes/sec
  Single Redis:          ~100,000 ops/sec
  Single Kafka partition: ~100 MB/sec write

Availability:
  99%   uptime = 87.6 hours/year downtime  (2 nines)
  99.9% uptime = 8.7 hours/year downtime   (3 nines)
  99.99% uptime = 52 min/year downtime     (4 nines)

Storage reference:
  1 char = 1 byte
  1 KB = 10^3 bytes
  1 MB = 10^6 bytes
  1 GB = 10^9 bytes
  1 TB = 10^12 bytes
  1 PB = 10^15 bytes
```

---

## CAP Theorem (Must Know Cold)

```
CAP: In a distributed system, you can only guarantee 2 of 3:
  C = Consistency (all nodes see the same data at the same time)
  A = Availability (every request gets a response, even if stale)
  P = Partition Tolerance (system works even when nodes can't communicate)

Network partitions WILL happen → P is always required → choose C or A:
  CP systems: consistent under partition → may reject requests
    Examples: HBase, Zookeeper, etcd, Redis (strong consistency mode)
    Use when: financial transactions, distributed locks
    
  AP systems: available under partition → may return stale data
    Examples: DynamoDB, Cassandra, CouchDB
    Use when: social feeds, product catalog, user sessions

PACELC (more practical than CAP):
  If Partition: choose Availability or Consistency
  Else (no partition): choose Latency or Consistency
```

---

## Common System Design Mistakes

1. **Jumping to components before requirements** — Always clarify scale and constraints first
2. **Over-engineering** — Don't design for 1 billion users if the question says 1 million
3. **No capacity estimation** — Amazon expects you to quantify; it shows engineering rigor
4. **Ignoring failure modes** — "What happens when the DB goes down?" is always asked
5. **Single point of failure (SPOF)** — Everything needs redundancy: DB replication, multi-AZ
6. **Not explaining tradeoffs** — "I chose Cassandra because [tradeoffs]" > "I chose Cassandra"
7. **Perfect consistency everywhere** — Most systems can tolerate eventual consistency; say why
8. **Forgetting the cache** — Almost every read-heavy system at scale needs caching
9. **Not mentioning monitoring/alerting** — Briefly mention: "I'd add Prometheus metrics and PagerDuty alerts"
10. **One-size-fits-all DB** — Use the right DB for the access pattern

---

## See Also

- [System Design Algorithms](../02-algorithms/system-design-algorithms.md)
- [Amazon Interview Strategy](./google-interview-strategy.md)
- [Behavioral Interview](./behavioral-interview.md)
