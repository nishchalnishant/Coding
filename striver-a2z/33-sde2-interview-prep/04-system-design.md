---
module: striver-a2z/33-sde2-interview-prep
topic: System design interview foundations
tags: [interview, system-design, distributed-systems]
---
# 04. System Design Interview Foundations

← [Part 33](README.md) · [Beyond the sheet](../32-beyond-the-sheet/README.md)

System design is a discussion of requirements, architecture, bottlenecks, and trade-offs. The interviewer is evaluating the reasoning process as well as the final diagram. Practice high-level design and product/API architecture if those are relevant to the target role.

## A 45-minute structure

| Phase | What to do |
|---|---|
| Requirements (5 min) | Identify users, core actions, scale assumptions, latency/availability needs, and exclusions |
| API and data model (5–8 min) | Define key operations, identifiers, entities, and access patterns |
| High-level design (8–10 min) | Draw clients, edge/load balancing, services, storage, cache, queues, and external dependencies |
| Deep dive (15–18 min) | Pick the highest-risk path; trace reads/writes, partitioning, consistency, failure handling, and capacity |
| Wrap-up (3–5 min) | Summarize bottlenecks, trade-offs, observability, security, and next improvements |

Adapt timing to the interviewer and prompt. Ask targeted questions and state assumptions when answers are unavailable.

## Concepts to know

- **Traffic and storage estimates:** requests per second, read/write ratio, payload size, retention, replication overhead, peak-to-average factor.
- **Load distribution:** load balancers, stateless services, horizontal scaling, partition keys, hot partitions, consistent hashing at a conceptual level.
- **Data choices:** relational transactions versus key-value/document access; indexes, replication lag, partitioning, and consistency needs.
- **Caching:** cache key, TTL, invalidation, eviction, stampede protection, and acceptable staleness.
- **Async processing:** queues for buffering and decoupling; delivery semantics, retries, idempotent consumers, dead-letter handling, ordering.
- **Reliability:** timeouts, bounded retries, circuit breakers, redundancy, graceful degradation, backpressure, recovery and disaster planning.
- **Observability and security:** user-impacting SLOs, logs/metrics/traces, access control, encryption, abuse prevention, sensitive-data minimization.

## Design prompts to work through

For each prompt, write functional and non-functional requirements, APIs, a data model, the main diagram, one deep dive, and likely failure modes.

- URL shortener with redirects and analytics
- News feed or activity timeline
- Chat/messaging service with presence and offline delivery
- File storage and sharing
- Notification delivery platform
- Ride matching or nearby search
- Distributed rate limiter
- Metrics ingestion and query service

Do not memorize a single architecture for each. Requirements should drive choices.

## Common design trade-offs

- Strong consistency versus availability/latency for a specific operation
- Synchronous request versus asynchronous job
- Fan-out-on-write versus fan-out-on-read
- SQL transaction versus denormalized read model
- Cache freshness versus database load
- Single region versus multi-region complexity

Explain who experiences each downside and how you would detect the failure. Connect this module's advanced tools, such as consistent hashing, range indexes, tries, and graph algorithms, only when the design actually needs them.
