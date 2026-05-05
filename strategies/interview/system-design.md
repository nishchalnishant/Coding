# Google SDE-2 (L4) System Design — What to Cover + Templates

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
