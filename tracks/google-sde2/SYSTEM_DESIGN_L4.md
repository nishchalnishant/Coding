# Google SDE-2 (L4) System Design — What to Cover + Templates

This is **not** an L5/L6 deep-dive. For L4, you’re usually evaluated on clear thinking, fundamentals, and tradeoffs.

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
- Design a “news feed” / timeline (high-level)
- Design a file/photo upload service (metadata + storage)
- Design a chat messaging service (1:1 or group)
- Design a notification system (email/push) with retries
- Design a parking availability service (location + updates)
- Design a “top K trending” service (streaming aggregation)

Algorithm building blocks (if asked to reason/implement): `../advanced-dsa/system-design-algorithms.md`.

---

## Minimal “back-of-envelope” numbers (good enough for L4)

- QPS = requests/sec, peak vs average (assume 10× peak if unclear)
- Storage/day = (events/day) × (bytes/event)
- Cache hit rate impacts DB load directly

Keep it rough; the goal is to guide design choices, not to be perfectly accurate.

