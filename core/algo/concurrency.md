# Concurrency Patterns for Coding Interviews

SDE-3 / Senior roles often test your ability to handle multi-threading, synchronization, and race conditions.

## 1. Core Concepts

| Concept | Use it for | Python/Java Keywords |
| :--- | :--- | :--- |
| **Lock / Mutex** | Mutual exclusion; only one thread can access a resource. | `Lock`, `synchronized` |
| **Semaphore** | Limit number of concurrent threads (e.g., connection pool). | `Semaphore` |
| **Condition Variable** | Signal/Wait between threads (e.g., consumer waits for producer). | `Condition`, `wait/notify` |
| **Atomic Variables** | Lock-free thread-safe updates to simple values. | `AtomicInteger`, `AtomicReference` |
| **Thread Safety** | Ensuring code works correctly when executed by multiple threads. | Immutable objects, thread-local storage |

---

## 2. Classic Patterns

### Producer-Consumer
- **Problem**: One thread produces data, another consumes it. Handled via a bounded buffer.
- **Solution**: Use two semaphores (`empty`, `full`) and a mutex for the buffer.
- **Click Moment**: "Buffer size K", "Threads waiting for data".

### Readers-Writers Lock
- **Problem**: Multiple readers can read simultaneously, but writers need exclusive access.
- **Solution**: Track `reader_count`. First reader locks the writer mutex; last reader unlocks it.
- **Click Moment**: "Read-heavy load", "Consistency required for writes".

### Dining Philosophers
- **Problem**: Circular dependency leading to deadlock.
- **Solution**: Break the cycle by ordering resource acquisition (e.g., always pick lower ID chopstick first).
- **Click Moment**: "Circular wait", "Deadlock prevention".

---

## 3. Concurrency Problems (LeetCode style)

| Problem | Key Trick |
| :--- | :--- |
| **Print FooBar Alternately** | Use two semaphores; `foo` signals `bar`, `bar` signals `foo`. |
| **Print in Order** | Use two latches or semaphores for sequential execution. |
| **Building H2O** | Use semaphores for H and O; use a barrier or count to release H2O. |
| **FizzBuzz Multithreaded** | Use condition variables to signal based on the current number. |

---

## 4. Implementation Checklist

- [ ] **Deadlock**: Check for circular dependencies in lock acquisition.
- [ ] **Starvation**: Ensure every thread eventually makes progress.
- [ ] **Livelock**: Avoid threads infinitely responding to each other without progress.
- [ ] **Efficiency**: Minimize the size of critical sections (the code inside a lock).
