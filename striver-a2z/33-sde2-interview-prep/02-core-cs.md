---
module: striver-a2z/33-sde2-interview-prep
topic: Core computer science refresh
tags: [interview, operating-systems, networking, databases, concurrency]
---
# 02. Core CS Refresh

← [Part 33](README.md)

Depth should match the role. Be prepared to explain concepts plainly, relate them to production behavior, and identify trade-offs rather than recite definitions.

## Operating systems and concurrency

- **Processes and threads:** address-space isolation versus shared process memory; context switching and when parallelism helps.
- **Synchronization:** mutex, read/write lock, semaphore, condition variable, atomic operation; protect shared state and avoid holding locks across slow I/O.
- **Failure modes:** race condition, deadlock (mutual exclusion, hold-and-wait, no preemption, circular wait), starvation, priority inversion. Discuss prevention and detection.
- **Memory:** stack versus heap, allocation lifetime, garbage collection basics, memory leaks and backpressure from unbounded queues.
- **Async I/O:** distinguish concurrency from parallel execution; explain how blocking work can exhaust a worker pool.

Practice: implement a thread-safe bounded queue conceptually; diagnose a deadlock from a lock-order diagram; explain why a shared mutable cache needs a consistency policy.

## Networking and web services

- DNS lookup, TCP connection setup, TLS, HTTP request/response, connection reuse, and timeouts at a useful high level.
- TCP reliability and ordered delivery versus UDP's lower overhead and lack of delivery guarantees.
- HTTP methods, status classes, headers, idempotency, pagination, and API versioning.
- Latency components: client, network, load balancer, service, storage, and downstream dependencies.
- Retries need deadlines, bounded attempts, backoff, jitter, and idempotency to avoid retry storms or duplicate effects.

Practice: trace a request from client to database; explain what happens when a dependency is slow; design safe retry semantics for a payment-like operation.

## Databases and storage

- Relational tables, keys, joins, constraints, normalization, and when denormalization helps reads.
- Indexes speed selected reads while consuming space and adding write cost; reason about composite-index column order and query shape.
- Transactions and ACID; isolation anomalies such as dirty reads, non-repeatable reads, and write skew at a conceptual level.
- SQL versus key-value/document/wide-column stores: access patterns, consistency, query flexibility, and operational trade-offs.
- Replication, partitioning/sharding, hot keys, backups, and migration safety.
- Cache-aside, TTL, invalidation, stale reads, stampedes, and cache-aside write ordering.

Practice: choose an index for a query; explain a lost update; outline a schema migration with old and new application versions running together.

## Reliability and operations

- Availability, latency percentiles, throughput, error rate, saturation, and service-level objectives.
- Logs, metrics, traces, dashboards, alerts, and actionable on-call signals.
- Graceful degradation, timeouts, circuit breakers, bulkheads, queues, and load shedding.
- Capacity estimates should expose assumptions and order of magnitude, not false precision.

Practice: investigate rising p99 latency; distinguish a service bug from downstream saturation; pick an SLO and explain its user impact.
