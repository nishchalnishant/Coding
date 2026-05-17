# Concurrency & Multithreading — SDE-3 Gold Standard

Mastery of synchronization, memory models, and lock-free primitives. SDE-3 candidates are expected to go beyond "just using a lock" and discuss cache-line contention, memory barriers, and the ABA problem.

---

## 1. The Concurrency Hierarchy

| Level | Mechanism | Trade-off |
| :--- | :--- | :--- |
| **High** | Futures, Promises, Actors | Easy to reason about, potential overhead. |
| **Mid** | Semaphores, Mutexes, Latches | Standard, risk of deadlocks/contention. |
| **Low** | Atomic Variables (CAS), Volatile | Performance, extremely difficult to get right. |
| **Hardware** | Memory Barriers, Load-Link/Store-Conditional | Raw performance, architecture-specific. |

---

## 2. Core Concepts & Mental Models

### Visibility vs. Atomicity
- **Atomicity**: An operation happens all at once or not at all (e.g., `AtomicInteger.incrementAndGet()`).
- **Visibility**: When one thread modifies a value, when do other threads see it? (Use `volatile` in Java or `std::atomic` in C++).
- **The Click Moment**: "Value updated by Thread A but Thread B still sees the old value" → **Visibility** issue. "Two threads increment `x=5` and result is `6` instead of `7`" → **Atomicity** issue.

### The "Deadlock" Four Horsemen (Coffman Conditions)
For a deadlock to exist, all four MUST be true:
1. **Mutual Exclusion**: Resource cannot be shared.
2. **Hold and Wait**: Thread holds a resource while waiting for another.
3. **No Preemption**: Resource cannot be forcibly taken.
4. **Circular Wait**: T1 waits for T2, T2 waits for T1.
> [!TIP]
> **To fix deadlock**: Break any one of these. Most common: **Resource Ordering** (break Circular Wait) — always acquire locks in the same lexicographical order.

---

## 3. Classic SDE-3 Patterns

### 3.1 Bounded Blocking Queue (Producer-Consumer)
The foundation of most asynchronous systems.

```python
import threading
import collections

class BoundedBlockingQueue:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue = collections.deque()
        self.cond = threading.Condition()

    def enqueue(self, element: int) -> None:
        with self.cond:
            while len(self.queue) == self.capacity:
                self.cond.wait()
            self.queue.append(element)
            self.cond.notify_all()

    def dequeue(self) -> int:
        with self.cond:
            while len(self.queue) == 0:
                self.cond.wait()
            val = self.queue.popleft()
            self.cond.notify_all()
            return val
```

### 3.2 Dining Philosophers (Deadlock Avoidance)

> [!IMPORTANT]
> **The Click Moment**: "N threads share N resources in a circular dependency" — the textbook deadlock scenario. Every philosopher picks up left fork, then right fork → circular wait → deadlock. Fix by breaking circular wait: philosopher N picks up right fork first (resource ordering).

Classic setup: 5 philosophers, 5 forks. Each needs both adjacent forks to eat.

**Fix 1 — Resource Ordering** (simplest):
- Philosophers 0–3: pick up left fork first, then right.
- Philosopher 4 (the last): picks up right fork first, then left.
- Breaks the circular wait condition — deadlock impossible.

**Fix 2 — Arbitrator / Waiter**:
- A waiter semaphore allows at most N-1 philosophers to attempt simultaneously.
- Guarantees at least one can eat; others wait. Simple but introduces a bottleneck.

**Fix 3 — Chandy/Misra (message-passing)**:
- Forks are "dirty" or "clean". A philosopher with a dirty fork must hand it to a requester before eating again.
- Starvation-free. Used in distributed systems where shared memory isn't available.

> [!TIP]
> For interviews: state the problem (circular wait → deadlock), name resource ordering as the fix, and explain why it breaks the Coffman condition. You don't need to implement Chandy/Misra unless asked.

### 3.3 Read-Write Lock (Readers-Writers Problem)

> [!IMPORTANT]
> **The Click Moment**: "Many readers can read simultaneously, but a writer needs exclusive access." This is the exact access pattern of a database, config file, or shared cache. A plain mutex serializes all readers — wasteful. A read-write lock allows concurrent reads, exclusive writes.

**Rules:**
- Multiple readers can hold the lock simultaneously.
- A writer must wait for all readers to finish.
- No reader can acquire while a writer is waiting or writing.

```python
import threading

class ReadWriteLock:
    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0

    def acquire_read(self):
        with self._read_ready:
            self._readers += 1

    def release_read(self):
        with self._read_ready:
            self._readers -= 1
            if self._readers == 0:
                self._read_ready.notify_all()

    def acquire_write(self):
        self._read_ready.acquire()
        while self._readers > 0:
            self._read_ready.wait()

    def release_write(self):
        self._read_ready.release()
```

> [!CAUTION]
> Writer starvation: if readers arrive continuously, a writer may never get access. Fix: once a writer is waiting, new readers must queue behind it (use a second mutex for writer priority). Python's `threading.RLock` does not implement this — you must build it explicitly.

### 3.4 Barrier / Phaser
- **Problem**: N threads must all finish Phase 1 before any can start Phase 2.
- **Solution**: Use a counter and a condition variable. The N-th thread to arrive calls `notify_all()`.

---

## 4. Advanced: Lock-Free & Scalability

### Compare-And-Swap (CAS)
Instead of locking, "optimistically" try to update. If the value changed while you were working, retry.
```python
# Conceptual CAS
def atomic_increment(ref):
    while True:
        old_val = ref.get()
        new_val = old_val + 1
        if ref.compare_and_set(old_val, new_val): # Atomic CPU instruction
            return
```

### The ABA Problem
- **What**: Thread 1 reads value `A`. Thread 2 changes it to `B` and then back to `A`. Thread 1 does a CAS and succeeds, unaware that the state actually changed.
- **Solution**: **Versioned pointers** or **Stamped references**. Add a version number that increments every time the value changes.

### Cache-Line Contention (False Sharing)
- **What**: Two threads update unrelated variables that happen to live on the same 64-byte CPU cache line. The CPU must synchronize the whole line, killing performance.
- **Solution**: **Padding**. Add dummy bytes between hot variables to push them onto different cache lines.

---

## 5. High-Impact Interview Problems

| Problem | Pattern | Trick / Gotcha |
| :--- | :--- | :--- |
| **Dining Philosophers** | Deadlock Prevention | Order the forks: always pick up `min(id1, id2)` first. |
| **Building H2O** | Counting / Barrier | Two semaphores + one barrier. 2H + 1O = 1 Release. |
| **Web Crawler** | Thread Pool + Visited Set | Use a thread-safe `Set` and a `BlockingQueue` for URLs. |
| **Traffic Light** | State Machine | Use a `Condition` variable to signal state changes. |
| **Zero Even Odd** | Hand-off | 3 Semaphores. Zero signals (Even or Odd); Even/Odd signal Zero. |

---

## 6. SDE-3 Design Questions
1. **How would you design a thread-safe HashMap?**
   - **Baseline**: `synchronized` whole map (slow).
   - **Better**: Segmented Locking (Java 7 `ConcurrentHashMap`) — lock only the bucket.
   - **SDE-3**: CAS-based updates for empty buckets, synchronized nodes only during resize (Java 8+).
2. **How do you implement a Rate Limiter for 10,000 threads?**
   - **Lock-based**: High contention.
   - **Lock-free**: Use `AtomicLong` for the token count and `AtomicLong` for the last-refill timestamp.
3. **When would you use a Spinlock vs. a Mutex?**
   - **Spinlock**: Good for very short critical sections (just a few CPU cycles) to avoid the cost of a context switch.
   - **Mutex**: Better for long-running operations where you want the thread to go to sleep and free up the CPU.

---

## 5. SDE-3 Interview Questions — Concurrency

| Question | Core Concept | What They're Testing |
|----------|-------------|----------------------|
| Implement a thread-safe LRU cache | Mutex on DLL + HashMap | Lock granularity, deadlock-free design |
| Design a rate limiter shared across threads | Atomic counter or mutex on sliding window | Atomicity vs locking tradeoff |
| Implement a countdown latch | Semaphore with count | Understanding of signaling primitives |
| Fix this deadlocked code [given snippet] | Coffman conditions | Ability to identify and break circular wait |
| How does a read-write lock differ from a mutex? | Concurrency primitives | Understanding of access patterns |
| What is the ABA problem? | CAS-based lock-free code | Advanced lock-free knowledge |

> [!TIP]
> **ABA problem in one sentence**: Thread 1 reads value A, Thread 2 changes A→B→A, Thread 1's CAS succeeds (still sees A) but the world has changed. Fix: version stamps (tagged pointers) or hazard pointers.

---

## Quick Revision Triggers
- "Buffer size K" → Bounded Blocking Queue (Condition variables).
- "Read-heavy" → ReadWriteLock.
- "Circular dependency" → Resource ordering to break deadlock.
- "Performance bottleneck in high-thread-count" → Check for False Sharing or Lock Contention.
- "Wait for N events" → CountDownLatch / Barrier.
