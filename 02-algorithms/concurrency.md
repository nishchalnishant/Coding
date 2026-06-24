---
module: 02-algorithms
topic: Concurrency
subtopic: 
status: awareness-only
tags: [algorithms, concurrency]
---

← [Algorithms index](./README.md) · [Algorithm decision tree](./algorithm_tree.md)

> [!warning] **Amazon SDE-2 scope: LLD / system design only.**
> Concurrency does not appear in coding-round algorithm questions at SDE-2. Study if targeting LLD/OO design rounds.

## Quick Reference

- **Deadlock (Coffman conditions)**: Mutual exclusion + Hold & Wait + No preemption + Circular wait. Break any one to prevent.
- **Race condition**: Two threads read-modify-write shared state without synchronization. Fix: mutex / synchronized block.
- **Mutex vs Semaphore**: mutex = binary ownership (same thread locks/unlocks); semaphore = signaling between threads (can release from different thread).
- **Producer-Consumer**: bounded buffer; producer waits when full, consumer waits when empty. Classic `wait/notifyAll` or `BlockingQueue`.
- **Read-Write Lock**: multiple concurrent readers OR one exclusive writer. Use when reads >> writes.
- **CAS (Compare-And-Swap)**: atomic hardware instruction; basis of lock-free structures. `AtomicInteger.compareAndSet(expect, update)`.
- **ABA problem**: CAS succeeds incorrectly if value changes A→B→A. Fix: stamped reference / version counter.
- **Thread pool sizing**: CPU-bound → N cores; I/O-bound → N * (1 + wait_time/compute_time).

**LLD patterns that use concurrency**: Singleton (double-checked locking), BlockingQueue implementation, Rate Limiter with token bucket.
