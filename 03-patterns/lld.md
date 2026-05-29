---
module: 03-patterns
topic: Low-Level Design
subtopic: LLD
status: unread
tags: [lld, design-patterns, oop, solid]
---
# Low-Level Design (LLD) — Interview Guide

```
WHY LLD rounds exist
├── Distributed system design tests "what to build"; LLD tests "how to build it"
├── SDE-3 must show OOP fluency: encapsulation, extensibility, testability
└── Common at Google, Meta, Amazon backend/infra roles — skip if pure frontend/ML

WHAT it tests
├── Class design: entities, responsibilities, interfaces
├── Design pattern selection: which pattern fits and why
├── SOLID adherence: single responsibility, open/closed, etc.
└── Thread safety: when and how to add concurrency controls

HOW to approach
├── Step 1: Identify entities and their relationships (nouns → classes)
├── Step 2: Define interfaces before implementations
├── Step 3: Name the design pattern that fits
├── Step 4: Show thread safety if multi-threaded context
└── Step 5: Discuss extensibility (what would change if requirements grow)
```

---

## SOLID Principles — Quick Reference

| Principle | One-liner | Interview trigger |
|-----------|-----------|-------------------|
| **S** — Single Responsibility | A class should have one reason to change | "This class does too much — split auth from storage" |
| **O** — Open/Closed | Open for extension, closed for modification | Adding a new payment method without editing existing code |
| **L** — Liskov Substitution | Subtypes must be substitutable for their base type | `Square extends Rectangle` breaks LSP if it overrides setWidth |
| **I** — Interface Segregation | Clients shouldn't depend on methods they don't use | Fat interface → split into `Readable`, `Writable`, `Seekable` |
| **D** — Dependency Inversion | Depend on abstractions, not concretions | Inject `IDatabase` not `MySQLDatabase`; enables testing |

---

## Core Design Patterns for Interviews

| Pattern | What it does | Classic use case |
|---------|-------------|-----------------|
| **Strategy** | Swap algorithms at runtime via interface | Sorting strategy, pricing algorithm, payment method |
| **Observer** | Notify many subscribers when state changes | Event system, pub/sub, UI data binding |
| **Factory** | Centralize object creation, hide concrete types | `ShapeFactory.create("circle")`, DB connection pool |
| **Decorator** | Wrap object to add behavior without subclassing | Logging wrapper, caching wrapper, auth middleware |
| **Command** | Encapsulate request as object for undo/queue | Text editor undo, job queue, macro recording |
| **Singleton** | One instance per process, global access point | Config manager, thread pool, logger |
| **Builder** | Construct complex object step by step | `QueryBuilder`, HTTP request builder |
| **Adapter** | Make incompatible interfaces work together | Wrapping a legacy API to fit a new interface |

---

## Classic LLD Problems

| Problem | Core Data Structures | Key Design Decision | Pattern(s) |
|---------|---------------------|---------------------|------------|
| **LRU Cache** | HashMap + Doubly Linked List | O(1) get and put; DLL maintains recency | — |
| **LFU Cache** | HashMap + HashMap of freq→OrderedDict | Track min_freq; O(1) all ops | — |
| **Parking Lot** | Map of floor→spots, SpotType enum | Strategy for pricing; Observer for availability | Strategy, Observer |
| **Elevator System** | State machine per elevator, request queue | Scheduling algorithm (SCAN/LOOK vs FCFS) | State Machine |
| **Pub/Sub System** | Topic→List[Subscriber] map, thread-safe queue | Sync vs async delivery; fanout model | Observer |
| **Rate Limiter** | Token bucket or sliding window counter | Fixed window vs sliding window vs token bucket | Strategy |
| **Snake Game** | Deque for body, set for O(1) collision check | Deque front = head, append/popleft for movement | — |
| **Design Twitter** | HashMap of user→tweets (list), follow sets | Min-heap merge for top-K; merge across followees | — |
| **Trie (with wildcard)** | TrieNode with children dict + is_end flag | DFS for `.` wildcard; iterate all children | — |
| **Task Scheduler** | Priority queue, cooldown map | Greedy: always schedule most frequent available | Strategy |

---

## LRU Cache — Full Design

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)
```

**Interview notes:**
- `OrderedDict` = HashMap + DLL; `move_to_end` is O(1)
- Raw DLL implementation: sentinel head/tail nodes avoid null checks
- Thread-safe version: add `threading.Lock()` around get/put

---

## LFU Cache — Design Notes

```
Data structures needed:
  key_to_val: {key: val}
  key_to_freq: {key: freq}
  freq_to_keys: {freq: OrderedDict}  # preserves insertion order = LRU within same freq
  min_freq: int

get(key):
  - Increment freq, move key from freq_to_keys[f] to freq_to_keys[f+1]
  - Update min_freq if freq_to_keys[min_freq] is now empty

put(key, val):
  - If key exists: update val + call get logic (freq increment)
  - If new key + at capacity: evict first item from freq_to_keys[min_freq]
  - Insert new key with freq=1, set min_freq=1
```

---

## Parking Lot — Class Design

```python
from enum import Enum
from abc import ABC, abstractmethod

class SpotType(Enum):
    COMPACT = "compact"
    LARGE = "large"
    HANDICAPPED = "handicapped"

class ParkingSpot:
    def __init__(self, spot_id: str, spot_type: SpotType):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.is_occupied = False

class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, hours: float) -> float: ...

class FlatRatePricing(PricingStrategy):
    def __init__(self, rate: float):
        self.rate = rate
    def calculate(self, hours: float) -> float:
        return self.rate

class HourlyPricing(PricingStrategy):
    def __init__(self, rate_per_hour: float):
        self.rate = rate_per_hour
    def calculate(self, hours: float) -> float:
        return hours * self.rate

class ParkingLot:
    def __init__(self, spots: list[ParkingSpot], pricing: PricingStrategy):
        self.spots = spots
        self.pricing = pricing
        self._available = {s.spot_id for s in spots}

    def park(self, spot_type: SpotType) -> ParkingSpot | None:
        for spot in self.spots:
            if spot.spot_type == spot_type and not spot.is_occupied:
                spot.is_occupied = True
                self._available.discard(spot.spot_id)
                return spot
        return None

    def leave(self, spot: ParkingSpot, hours: float) -> float:
        spot.is_occupied = False
        self._available.add(spot.spot_id)
        return self.pricing.calculate(hours)
```

---

## Observer Pattern — Pub/Sub

```python
from abc import ABC, abstractmethod

class Subscriber(ABC):
    @abstractmethod
    def update(self, event: dict) -> None: ...

class EventBus:
    def __init__(self):
        self._subscribers: dict[str, list[Subscriber]] = {}

    def subscribe(self, topic: str, subscriber: Subscriber) -> None:
        self._subscribers.setdefault(topic, []).append(subscriber)

    def unsubscribe(self, topic: str, subscriber: Subscriber) -> None:
        self._subscribers.get(topic, []).remove(subscriber)

    def publish(self, topic: str, event: dict) -> None:
        for sub in self._subscribers.get(topic, []):
            sub.update(event)
```

**Thread safety extension:** wrap `publish` with `threading.Lock()` or use `queue.Queue` for async fanout.

---

## Class Design Template (whiteboard flow)

1. **Identify entities** — nouns in the problem become classes (`User`, `Spot`, `Ticket`)
2. **Assign responsibilities** — one responsibility per class (SRP)
3. **Define interfaces** — what operations does each entity support? Define `ABC` or protocol first
4. **Choose pattern** — does behavior need to be swappable? → Strategy. Notifications? → Observer. Creation? → Factory
5. **Show data structures** — what's inside each class? Why that structure?
6. **Address thread safety** — if concurrent access, name the lock granularity
7. **Discuss extensibility** — "if we add X requirement, only class Y changes" = good design signal

---

## Interview Phrases

- "I'll define an interface first so we can swap implementations without changing callers."
- "This is a Strategy pattern — I'm separating the algorithm from the context that uses it."
- "I'm using an Observer here so new subscribers don't require changes to the publisher."
- "Thread safety: I'll add a lock around the get/put methods since both modify shared state."
- "If requirements grew to support [X], we'd only need to add a new class, not modify existing ones — that's the Open/Closed principle."
