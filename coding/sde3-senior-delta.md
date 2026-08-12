---
tags: [sde3, senior, roadmap, delta]
topic: SDE-3 / Senior Delta — what changes on top of the L4 base
---

# SDE-3 / Senior FAANG Delta — Upgrade Layer

> **How to use this file:** Everything in the L3 base ([`l3-google-roadmap.md`](l3-google-roadmap.md)) and the L4 delta ([`l4-sde2-delta.md`](l4-sde2-delta.md)) is still the foundation — senior loops draw from the *same* topic pool. This file lists only what **changes again**: the senior bar, `T3` tier promotions, and the problems/variants neither prior track covers. Study L3 → L4 first; layer this on top last.

---

## 1. What actually changes at senior level

The topic list barely changes again. What changes is **what you're graded on**:

| Dimension | L4 bar | Senior (SDE-3) bar |
| :--- | :--- | :--- |
| Follow-up depth | One escalation (constraint or scale change) | **Full chain, self-driven** — you propose the next follow-up before being asked ("this also needs to handle X") |
| Ambiguity | Clarification is graded | You should **surface trade-offs the interviewer didn't ask about** (e.g. "if writes are rare I'd batch here instead") |
| Correctness under pressure | Optimal + clean code | Optimal **and** you catch your own bugs during dry run, unprompted |
| System-adjacent reasoning | Not expected | Expected in a bounded way: concurrency/consistency/memory trade-offs **discussed**, never full system design |
| Code structure | Helper functions, good names | + testable seams — you narrate what you'd unit test and why, without writing a test harness live |
| Communication | Explain your approach | **Drive the room** — narrate reasoning as a senior would review someone else's approach, including naming why alternatives are worse |
| Recovery | Fix bugs when pointed at | Catch your own bugs via **self-directed dry run**, and explain the class of bug (off-by-one vs. state-definition vs. invariant violation) |

**Still out of scope** (unchanged from L3/L4): full system design, LLD, formal concurrency primitives implementation, segment trees/BIT implementation, Tarjan SCC, bitmask/digit DP, Manacher, suffix automata. Senior *coding* rounds stay DSA + follow-up chains + bounded systems discussion — not a design round.

---

## 2. Tier promotions (L4 → Senior)

Introduces `T3` — **senior follow-up tier**: not asked as a base problem, but expected as the *second or third* link in a chain.

| Topic | L4 tier | Senior tier | Why |
| :--- | :--- | :--- | :--- |
| Follow-up chains (any T1 base) | bonus | `T3` mandatory | The chain itself is graded, not just the base solve — see [`03-patterns/SENIOR_FOLLOWUPS.md`](../03-patterns/SENIOR_FOLLOWUPS.md) |
| Design-a-data-structure | `⚡ T1` (single structure) | `T3` add: **composed / layered** designs (e.g. LFU + TTL eviction, rate limiter + sliding window) | Senior loops chain two design patterns together, not one |
| Concurrency discussion (no implementation) | not present | `T3` | Expected for any shared-state design problem (cache, rate limiter, counter) — narrate lock granularity, not code it |
| Streaming / online variants | occasional follow-up | `T3` systematic | Any T1 offline problem should have a ready streaming answer — see follow-up file §2 |
| Scale-change reasoning (100x constraints) | rare | `T3` | "What if n is 10^9?" should trigger an immediate approach swap, not a stall |
| Bounded system reasoning (sharding, partial failure) | absent | `T3`, narrow scope | Only in the context of a data-structure design problem — never a standalone system design prompt |

---

## 3. Senior-only problems / variants (not in L3 or L4 tracks)

Tiers below are **senior tiers**. These are almost always reached as follow-ups to an existing T1/T2 problem, not asked cold — treat them as the second half of a chain.

### 3.1 Composed / layered design `T3`

Full base-structure walkthroughs: [`coding/data-structures/14-design.md`](data-structures/14-design.md). These extend that file's structures by stacking a second requirement on top.

- **LFU Cache + TTL eviction** `T3` · Hard
  - Key insight: base LFU (freq→DLL map) + a min-heap or sorted structure on expiry time; evict on read (lazy) rather than a background sweep — narrate the trade-off between the two.
- **Rate Limiter (sliding window log → sliding window counter)** `T3` · Medium
  - Key insight: exact sliding window log is O(requests) memory; the follow-up is always "reduce memory" → bucketed counter with weighted overlap. State the accuracy/memory trade-off explicitly.
- **Distributed-flavored Hit Counter** `T3` · Medium (discussion, not implementation)
  - Base: Design Hit Counter (L4 §3.1). Follow-up: "now it's sharded across machines" — narrate approximate counting (e.g. count-min sketch) vs. exact aggregation trade-off. Do not implement a sketch; name it and explain why.

### 3.2 Streaming / online escalations `T3`

These are the standard "now make it a stream" answer for common T1 bases — see the full chain table in [`03-patterns/SENIOR_FOLLOWUPS.md` §2](../03-patterns/SENIOR_FOLLOWUPS.md#2-streaming--online).

- **Kth Largest in a Stream → Sliding Window Median with corrections** `T3` · Hard
  - Key insight: two heaps with lazy deletion (validate top against a hashmap of "pending removals" on pop) — same trick as Stock Price Fluctuation (L4 §3.1).
- **Top K Frequent, streaming** `T3` · Hard
  - Key insight: exact top-k over an unbounded stream needs bounded memory → discuss count-min sketch + a small heap of candidates; know this is approximate and say so.

### 3.3 Concurrency discussion (narrate, don't implement) `T3`

No code — this is a talking-points drill. Full framework: [`03-patterns/SENIOR_FOLLOWUPS.md` §5](../03-patterns/SENIOR_FOLLOWUPS.md#5-concurrency-discussion).

- **LRU/LFU Cache — thread safety** `T3`
  - Talking points: coarse lock vs. per-bucket lock, read/write lock split, why a naive global lock kills throughput under high read/write ratio.
- **Rate limiter — concurrent counters** `T3`
  - Talking points: atomic increment vs. lock, race window between check-and-increment, why a distributed rate limiter needs a shared store (Redis-style) with atomic ops.

### 3.4 Scale-change drills `T3`

Not new problems — a mandatory reflex check on **every** T1 problem: "what if n is 100x larger?" Full drill table: [`03-patterns/SENIOR_FOLLOWUPS.md` §7](../03-patterns/SENIOR_FOLLOWUPS.md#7-scale-change-100x).

- If your approach is O(n log n) and n grows 100x: still fine, say so and move on — don't over-engineer.
- If your approach is O(n²) and n grows 100x: this must trigger an immediate redesign proposal, unprompted. This reflex — not the redesign itself — is what's being graded.

---

## 4. Senior-relevant behavioral delta

Same STAR bank ([`04-behavioral/`](../04-behavioral/BEHAVIORAL_GOOGLINESS.md)), same 3 focus areas as the L4 delta (drove a decision, owned a failure end-to-end, influenced without authority) — at senior level, the bar is **scope**: stories should span teams or systems, not just a single project, and show judgment calls made under ambiguity, not just execution.

---

## 5. How this plugs into the existing tracks

1. Finish the L3 base ([`l3-google-roadmap.md`](l3-google-roadmap.md)) and L4 delta ([`l4-sde2-delta.md`](l4-sde2-delta.md)) first — this file assumes T1 fluency across both.
2. Run the L4 mock rounds ([`03-patterns/MOCK_INTERVIEW_SET.md` §"L4 Mock Rounds"](../03-patterns/MOCK_INTERVIEW_SET.md#l4-sde-2-mock-rounds--follow-up-chains)) until base + follow-up 1 + follow-up 2 are clean.
3. Then drill this file's `T3` items as **follow-up 3** on top of those same rounds, plus the senior follow-up chains in [`SENIOR_FOLLOWUPS.md`](../03-patterns/SENIOR_FOLLOWUPS.md).
4. Track weak spots in [`tracking/weakness-log.md`](../tracking/weakness-log.md) and revisit on the schedule in [`tracking/spaced-revision.md`](../tracking/spaced-revision.md).
