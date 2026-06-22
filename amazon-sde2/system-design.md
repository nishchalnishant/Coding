# Amazon SDE-2 — System Design (HLD)

## What Amazon expects at SDE-2
- End-to-end design in 45 min
- Functional + non-functional requirements scoping
- API design, data model, component diagram
- Scale reasoning (QPS, storage, bandwidth)
- Trade-offs — not just "what" but "why"

---

## Most Probable HLD Topics at Amazon SDE-2

### Tier 1 — Very High Probability
1. **Design URL Shortener** (TinyURL / bit.ly)
2. **Design Rate Limiter**
3. **Design LRU Cache / Distributed Cache**
4. **Design Notification System** (push/email/SMS)
5. **Design Amazon-like Product Search**
6. **Design a Feed / News Feed** (Twitter/Instagram timeline)

### Tier 2 — High Probability
7. **Design Distributed Message Queue** (Kafka-like or SQS-like)
8. **Design Key-Value Store** (DynamoDB-like)
9. **Design Typeahead / Autocomplete**
10. **Design Amazon S3 / Object Storage**
11. **Design Order Management System** (very Amazon-specific)
12. **Design Ride Sharing / Location Service**

### Tier 3 — Medium (comes up in specialized teams)
13. Design Video Streaming (Prime Video)
14. Design Recommendation System
15. Design Distributed ID Generator (Snowflake)
16. Design Web Crawler

---

## Design Template (use every time)

**Time budget for 45 min:**
| Phase | Time |
|---|---|
| Clarify requirements | 3–4 min |
| Capacity estimation | 2–3 min |
| API design | 3–4 min |
| Data model | 3–4 min |
| High-level diagram | 5–7 min |
| Deep dive (1–2 components) | 10–15 min |
| Trade-offs + Q&A | 5–7 min |

### 1. Clarify Requirements (3–4 min)
- Functional: what does the system DO?
- Non-functional: scale, latency, availability, consistency
- Out of scope: what NOT to design

### 2. Capacity Estimation (2–3 min)
```
DAU: 100M users
Read:Write ratio: 100:1
QPS (read) = 100M * 10 reads/day / 86400 ≈ 12,000 QPS
Storage = writes_per_day * avg_size * retention
Bandwidth = QPS * response_size
```

### 3. API Design
```
POST /shorten   body: {long_url}  → {short_url}
GET  /{code}                      → 301/302 redirect
```

### 4. Data Model
- Entities, relationships
- SQL vs NoSQL choice + reason
- Key access patterns → choose DB accordingly

### 5. High-Level Components
- Client → Load Balancer → App Servers → Cache → DB
- CDN for static assets
- Message Queue for async tasks

### 6. Deep Dive (pick 1–2 hard parts)
- Caching strategy (write-through / write-back / write-around)
- Sharding strategy (by user_id, geo, consistent hashing)
- Replication (primary-replica, eventual vs strong consistency)
- Failure handling / fallback

### 7. Trade-offs Discussion
- Consistency vs Availability (CAP)
- SQL vs NoSQL
- Push vs Pull for feed
- Strong vs Eventual consistency for your use case

---

## URL Shortener — Deep Dive

**Core challenge:** generate unique 7-char code for each URL, globally unique, fast redirect

**Encoding:** base62 (a-z, A-Z, 0-9) → 62^7 = 3.5 trillion combinations
**ID generation:** auto-increment DB ID → base62 encode (avoid hash collision)
**Redirect:** 301 (permanent, browser caches) vs 302 (temporary, always hits server — use 302 to track analytics)
**Cache:** most reads for top ~20% URLs → LRU cache with TTL

```
Write: Client → API → ID Generator → encode → store(code, long_url) → return short_url
Read:  Client → API → Cache(code) → if miss → DB → return long_url → redirect
```

---

## Rate Limiter — Deep Dive

**Algorithms:**
| Algorithm | Pro | Con |
|---|---|---|
| Fixed Window Counter | Simple | Burst at window boundary |
| Sliding Window Log | Exact | High memory (store timestamps) |
| Sliding Window Counter | Good accuracy, low memory | Approximate |
| Token Bucket | Allows bursts, smooth | Harder to implement distributed |
| Leaky Bucket | Very smooth | No burst handling |

**Distributed:** Use Redis + Lua script for atomic increment
```
key = "rate:{user_id}:{window}"
INCR key
EXPIRE key window_size
if count > limit: reject
```

---

## Notification System — Deep Dive

**Channels:** push (APNs/FCM), SMS (Twilio), email (SendGrid)
**Components:**
```
API Server → Notification Service → Channel Workers → 3rd Party
                    ↕
              Message Queue (dedup, retry)
                    ↕
              User Preference DB (opt-out, channel)
```
**Key decisions:**
- Queue per channel for independent scaling
- Dedup by notification_id to avoid duplicates on retry
- Priority queue: OTP/transactional > marketing

---

## LRU Cache / Distributed Cache — Deep Dive

**Single node:** HashMap + Doubly Linked List → O(1) get/put
**Distributed (Redis cluster):**
- Consistent hashing to assign keys to nodes
- Replication factor = 3
- Eviction policy: LRU / LFU / TTL
- Cache aside pattern: app reads cache first, on miss reads DB + populates cache
- Write strategies: Write-through (sync), Write-back (async, risk of loss), Write-around (skip cache on write)

---

## Key-Value Store (DynamoDB-like) — Deep Dive

**Consistent hashing:** ring with virtual nodes, each server owns a range
**Replication:** W + R > N for strong consistency (e.g., N=3, W=2, R=2)
**Conflict resolution:** vector clocks or last-write-wins
**Compaction:** SSTable + LSM tree for write-heavy workloads

---

## Order Management System — Deep Dive (Amazon-specific, very likely)

**Entities:** Order, OrderItem, Customer, Product, Payment, Shipment, Inventory

**Core flows:**
```
Place Order:  Customer → Cart → Checkout → Payment → OrderService → InventoryService → ShipmentService
              → Notification (async via SQS)

Cancel Order: Check status (only if not shipped) → Refund → Restock inventory → Notify
```

**State machine for Order:**
```
CREATED → PAYMENT_PENDING → PAYMENT_CONFIRMED → PROCESSING → SHIPPED → DELIVERED
                                                           ↘ CANCELLED (before SHIPPED)
```

**Key design decisions:**
- Saga pattern for distributed transactions (payment + inventory + shipment are separate services)
- Outbox pattern: write event to DB atomically with state change, then publish to SQS — avoids dual-write problem
- Idempotency key on payment to prevent double-charge on retry
- Eventual consistency between inventory and order service (accept oversell risk for high availability, or use reserved inventory)

**Data model:**
```
orders: order_id PK, customer_id, status, created_at, updated_at
order_items: item_id PK, order_id FK, product_id, qty, unit_price
payments: payment_id PK, order_id FK, amount, status, idempotency_key
shipments: shipment_id PK, order_id FK, address, carrier, tracking_no, status
```

---

## News Feed (Twitter/Instagram-like) — Deep Dive

**Fan-out on write (push):** on post, push to all followers' feed cache
- Pro: fast read (O(1) from cache)
- Con: write amplification for celebrities (10M followers = 10M writes)

**Fan-out on read (pull):** on read, fetch posts from all followed users
- Pro: no write amplification
- Con: slow read for users who follow many people

**Hybrid:** push for normal users (<1K followers), pull for celebrities; merge at read time

**Feed generation:**
```
Write: Post → PostService → MQ → FanoutWorker → push to Redis sorted set (score=timestamp)
Read:  GET /feed → FeedService → Redis ZRANGE → fill missing (pull celebs) → return merged
```

---

## Product Search — Deep Dive

**Core challenge:** full-text search + filters (category, price, rating, availability) at scale

**Search stack:**
- Elasticsearch / OpenSearch as search index (inverted index for text)
- DynamoDB / Aurora as source of truth for product catalog
- Change Data Capture (CDC) pipeline: DB → Kafka → Indexer → Elasticsearch

**Relevance ranking signals:** TF-IDF + BM25 (text match), click-through rate, purchase rate, recency, seller rating, Prime eligibility

**Query flow:**
```
Search API → Query Parser (tokenize, expand synonyms) → ES Query → Ranker → Result Cache → Response
```

**Pagination:** cursor-based (not offset) at scale to avoid deep offset scans

---

## Amazon-Specific Design Considerations

- **SQS:** at-least-once delivery, visibility timeout, DLQ
- **DynamoDB:** partition key design, hot partition problem, GSI/LSI
- **S3:** eventual consistency (now strong since 2020), multipart upload
- **ElastiCache:** cluster mode on/off, Redis vs Memcached
- **CloudFront:** CDN, TTL, cache invalidation

---

## Numbers to Know

| Metric | Value |
|---|---|
| L1 cache | 0.5 ns |
| L2 cache | 7 ns |
| RAM access | 100 ns |
| SSD random read | 150 μs |
| HDD seek | 10 ms |
| Network round trip (same DC) | 0.5 ms |
| Network round trip (cross-region) | 150 ms |
| 1 Gbps bandwidth | 125 MB/s |
| 1 million QPS on single server | not feasible; shard at ~10–50K |
