---
module: tracking
topic: Weakness Log
tags: [tracking, senior, sde3]
---

# Weakness Log

> [!IMPORTANT]
> **How to use this file:** After every mock or real attempt that isn't ✅ Clean, add one row below. Classify the failure by **taxonomy**, not by problem name — the taxonomy is what transfers to new problems. Problem-level tracking (which problems you've solved) stays out of this repo; see [`questions.md`](../questions.md).

---

## Taxonomy

Classify each miss into exactly one category:

| Code | Category | Signature |
|---|---|---|
| `PATTERN` | Pattern recognition | Didn't identify the right pattern within ~5 min of reading the problem |
| `INVARIANT` | Invariant formulation | Identified the pattern but couldn't state the loop/recursion invariant precisely |
| `EDGE` | Edge cases | Correct approach, missed empty input / single element / all-same / negative values |
| `OFFBYONE` | Off-by-one | Correct approach, wrong boundary (`<` vs `<=`, `i` vs `i+1`) |
| `DPSTATE` | DP state definition | Couldn't define `dp[i]` / `dp[i][j]` precisely before coding |
| `BTDEDUP` | Backtracking dedup | Duplicate results from unsorted input or missing `i > start` skip check |
| `HEAPLAZY` | Heap lazy delete | Didn't know/apply the "validate on pop against a stale set" trick for heaps needing deletion |
| `BSBOUND` | Binary search boundary | Wrong `lo`/`hi` init, wrong midpoint bias, infinite loop on 2-element range |
| `COMPLEXITY` | Complexity misstatement | Solved it but stated wrong Big-O, or didn't notice a hidden O(n) inside a loop |
| `COMMUNICATION` | Communication / drive | Solved it but didn't narrate trade-offs unprompted (senior-bar miss, not a correctness miss) |
| `FOLLOWUP` | Follow-up chain break | Base was clean; broke on follow-up 1/2/3 — note which follow-up type from [`SENIOR_FOLLOWUPS.md`](../03-patterns/SENIOR_FOLLOWUPS.md) |

---

## Log

| Date | Problem | Pattern | Taxonomy code | What exactly broke | Fixed on retry? |
|---|---|---|---|---|---|
| | | | | | |

*(Add rows above this line, newest last. Keep entries one line — detail goes in "what exactly broke," not a separate essay.)*

---

## Reading your own log

Every 5–10 entries, scan the taxonomy column:

- **Same code 3+ times** → that's a systemic gap, not bad luck. Drill it specifically using the relevant section of [`03-patterns/PATTERN_LADDERS.md`](../03-patterns/PATTERN_LADDERS.md) or [`03-patterns/HOW_TO_THINK.md`](../03-patterns/HOW_TO_THINK.md).
- **`FOLLOWUP` entries clustering on one type** (e.g. always breaking on concurrency discussion) → drill that section of [`SENIOR_FOLLOWUPS.md`](../03-patterns/SENIOR_FOLLOWUPS.md) specifically, not the whole file.
- **`COMMUNICATION` entries** → this is not a DSA gap, it's a rehearsal gap. Redo the same problem out loud, narrating trade-offs, before moving to a new one.

Feed recurring weak areas into [`spaced-revision.md`](spaced-revision.md) at the next 2-day checkpoint.
