# Concurrency

Concurrency and multithreading patterns for **SDE-3 / Senior** interviews. Many companies expect backend or distributed-systems candidates to discuss thread safety, locks, and classic concurrency problems.

## Contents

| File | Description |
|------|-------------|
| [Concurrency Patterns](concurrency-patterns.md) | **Producer-Consumer** (bounded buffer with `Condition`), **Print FooBar Alternately** (semaphores), **Reader-Writer Lock**. Also: deadlock, starvation, mutex vs semaphore, condition variables. Code in Python. |

## How this fits SDE-3

- [SDE-3 Guide](../sde-3-guide/sde-3-guide.md) lists concurrency as a pillar and calls out problems like **Print FooBar Alternately** and **Dining Philosophers**.
- Use this folder with [advanced-dsa/system-design-algorithms.md](../advanced-dsa/system-design-algorithms.md) (e.g. rate limiting with threads) when design rounds touch concurrency.

## Quick checklist

- Producer-Consumer with bounded buffer and signaling.
- Alternating execution (FooBar) with semaphores or events.
- Reader-Writer lock (multiple readers, exclusive writer).
- Deadlock conditions and prevention.
- Mutex vs semaphore; when to use condition variables.
