# Concurrency and Multithreading Patterns

Concurrency questions are standard in SDE 3/Senior Software Engineer interviews to test your understanding of thread safety, synchronization, locks, and condition variables.

## 1. Producer-Consumer Pattern
The classic bounded-buffer problem. Tests your ability to handle thread starvation, race conditions, and signaling.

### Using Python `Condition`
```python
import threading

class BoundedBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = []
        self.condition = threading.Condition()

    def produce(self, item):
        with self.condition:
            while len(self.buffer) == self.capacity:
                self.condition.wait() # Wait until buffer is not full
            self.buffer.append(item)
            self.condition.notify() # Notify consumer

    def consume(self):
        with self.condition:
            while len(self.buffer) == 0:
                self.condition.wait() # Wait until buffer is not empty
            item = self.buffer.pop(0)
            self.condition.notify() # Notify producer
            return item
```

## 2. Print FooBar Alternately
Common LeetCode concurrency question where threads must execute in a strict alternating order.

### Using Python `Event` (or Semaphore)
```python
from threading import Semaphore

class FooBar:
    def __init__(self, n):
        self.n = n
        self.foo_sem = Semaphore(1) # Foo starts first
        self.bar_sem = Semaphore(0)

    def foo(self, printFoo: 'Callable[[], None]') -> None:
        for i in range(self.n):
            self.foo_sem.acquire()
            printFoo()
            self.bar_sem.release() # Allow bar to print

    def bar(self, printBar: 'Callable[[], None]') -> None:
        for i in range(self.n):
            self.bar_sem.acquire()
            printBar()
            self.foo_sem.release() # Allow foo to print again
```

## 3. Reader-Writer Lock
Multiple readers can read simultaneously, but a writer requires exclusive access.

```python
import threading

class ReadWriteLock:
    def __init__(self):
        self.readers = 0
        self.read_lock = threading.Lock()
        self.write_lock = threading.Lock()

    def acquire_read(self):
        with self.read_lock:
            self.readers += 1
            if self.readers == 1:
                self.write_lock.acquire() # Block writers

    def release_read(self):
        with self.read_lock:
            self.readers -= 1
            if self.readers == 0:
                self.write_lock.release() # Allow writers

    def acquire_write(self):
        self.write_lock.acquire()

    def release_write(self):
        self.write_lock.release()
```

## Concepts Checklist for SDE 3:
- **Deadlock**: Conditions (Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait) and prevention.
- **Starvation and Livelock**: Causes and mitigation strategies.
- **Mutex vs Semaphore**: A Mutex provides mutual exclusion (locking mechanism), while a Semaphore is a signaling mechanism (permits).
- **Condition Variables**: Used to block a thread until a particular condition evaluates to true.
- **Concurrent Data Structures**: Knowledge of structures like `ConcurrentHashMap` in Java or Python's `queue.Queue` which is thread-safe.
