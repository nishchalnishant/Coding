---
module: tracking
topic: Spaced Revision Protocol
tags: [tracking, senior, sde3, spaced-repetition]
---

# Spaced Revision Protocol

> [!IMPORTANT]
> **How to use this file:** This is not "reread the solution." Every revision pass is **active recall of five specific things**, in order. If you can't produce all five from memory in under 2 minutes, it's not internalized yet — it stays in rotation.

---

## The five things to recall per problem

For any problem you're revisiting, recall — out loud or on paper, not by rereading the writeup:

1. **Trigger** — what in the problem statement should have made you think of this pattern within 30 seconds?
2. **Invariant** — the one sentence that's true at every step of your loop/recursion.
3. **Waste** — what does the brute force redundantly recompute or check, that this approach avoids? (Ties to [`HOW_TO_THINK.md`](../03-patterns/HOW_TO_THINK.md)'s four levers.)
4. **Edge case that would break a careless version** — the specific input that trips up a naive implementation.
5. **One follow-up** — from [`SENIOR_FOLLOWUPS.md`](../03-patterns/SENIOR_FOLLOWUPS.md), what's the standard next escalation for this base?

If any of the five stalls, that's a weakness-log entry (see [`weakness-log.md`](weakness-log.md)), not just "review again."

---

## Schedule: 2 / 7 / 21 days

| Checkpoint | When | What to do |
|---|---|---|
| **Day 2** | 2 days after first clean solve | Recall the 5 things cold, no code. If any stall, redo the problem from scratch (timed). |
| **Day 7** | 7 days after first clean solve | Recall the 5 things cold. If clean, move to day-21 rotation. If any stall, redo from scratch and reset to day-2. |
| **Day 21** | 21 days after first clean solve | Recall the 5 things cold. If clean, the problem is internalized — drop it from active rotation, keep it only in the day-of warm-up list ([`MOCK_INTERVIEW_SET.md`](../03-patterns/MOCK_INTERVIEW_SET.md) "Quick Pattern Recall"). If any stall, reset to day-2. |

A problem "graduates" only after passing day-2 → day-7 → day-21 without a reset.

---

## What to put in rotation

Not every problem you've ever solved — that's passive hoarding. Put in rotation:

- Any Tier 1 problem from [`MOCK_INTERVIEW_SET.md`](../03-patterns/MOCK_INTERVIEW_SET.md) the first time you solve it cleanly.
- Any problem logged in [`weakness-log.md`](weakness-log.md) with `PATTERN` or `INVARIANT` codes — these are the ones most likely to be forgotten, not just mis-executed.
- Any senior follow-up chain from [`SENIOR_FOLLOWUPS.md`](../03-patterns/SENIOR_FOLLOWUPS.md) once you've completed it end-to-end once.

Do **not** put in rotation: problems you solved cleanly on first attempt with no hesitation on any of the 5 recall items — those don't need spaced repetition, only the day-of quick-recall list.

---

## Weekly cadence suggestion

Run checkpoints in a single 20–30 min block, 3–4x/week, batching whatever's due that day rather than reviewing continuously. Batch active recall beats daily passive rereading.
