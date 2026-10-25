---
module: striver-a2z/33-sde2-interview-prep
topic: Object-oriented and low-level design
tags: [interview, lld, oop, api-design]
---
# 03. Object-Oriented and Low-Level Design

← [Part 33](README.md)

Low-level design (LLD) interviews assess how you model behavior and change. Start with requirements and use cases; avoid inventing abstractions before their value is clear.

## Design sequence

1. Clarify actors, core use cases, constraints, and what is explicitly out of scope.
2. Identify important domain entities and the operations each supports.
3. Define APIs and invariants before implementation details.
4. Assign responsibilities; favor composition and small interfaces where they improve changeability.
5. Walk through one end-to-end use case and one failure or extension case.
6. Discuss persistence, concurrency, validation, errors, and test seams as relevant.

## Fundamentals to explain with examples

- Encapsulation protects invariants; abstraction exposes useful behavior without leaking implementation.
- Prefer composition when behavior varies independently or inheritance creates fragile coupling.
- SOLID as design questions, not a checklist: does a change force unrelated edits? Can implementations substitute safely? Is an interface too broad? Are high-level policies tied to low-level details?
- Patterns are tools: Strategy (swap algorithms), Factory (centralize construction), Observer (notify subscribers), Decorator (add behavior), Adapter (bridge interfaces). Explain the concrete problem each solves.
- Separate domain logic from I/O where it improves testing and replacement; do not create layers with no clear responsibility.

## Common exercises

- Parking lot: vehicle types, spot assignment, ticket lifecycle, pricing policy, concurrent allocation.
- LRU cache: hash map plus doubly linked list; O(1) get/put; capacity and thread-safety policy.
- Rate limiter: token bucket or sliding window; keying, clock choice, distributed coordination.
- Elevator or task scheduler: state transitions, prioritization policy, fairness, cancellation.
- Notification service: channel abstractions, retries, deduplication, templates, user preferences.

For each, prepare a small class/API sketch, key invariants, one extensibility point, and tests. Be explicit when a single-process assumption is being made.

## Quality checklist

- Requirements and assumptions are written down.
- Public methods have clear contracts and error behavior.
- State transitions preserve invariants.
- Dependencies can be substituted in tests.
- Concurrency behavior is defined where simultaneous calls are possible.
- The design is no more complex than current requirements demand.
