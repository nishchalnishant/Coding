---
module: tracking
topic: Mock Interview Scoring
tags: [tracking, senior, sde3, mock-interview]
---

# Mock Interview Scoring — Senior Rubric

> [!IMPORTANT]
> **How to use this file:** This extends the simple ✅/⚠️/❌ scoring in [`MOCK_INTERVIEW_SET.md`](../03-patterns/MOCK_INTERVIEW_SET.md) with a 10-dimension rubric for senior-level self-assessment. Use the simple scoring day-to-day; use this rubric weekly, or whenever running a full follow-up chain from [`SENIOR_FOLLOWUPS.md`](../03-patterns/SENIOR_FOLLOWUPS.md).

---

## The 8-step mock flow

Run every senior mock through all 8 steps, timed. Skipping steps under time pressure is itself a signal to log.

| Step | Target time | What's being tested |
|---|---|---|
| 1. Clarify | 2–3 min | Do you ask about constraints/scale/edge behavior before coding, unprompted? |
| 2. Brute force | 2–3 min | Can you state a correct-but-slow approach fast, to anchor complexity discussion? |
| 3. Optimal approach | 5–8 min | Do you name the pattern, state the invariant, and justify why it's better than brute force? |
| 4. Code | 15–20 min | Clean, correct, good names, no silent gaps |
| 5. Dry run | 3–5 min | Self-directed — do you trace a real example without being asked? |
| 6. Complexity | 1–2 min | Correct time/space, stated precisely (not just "O(n)" when it's O(n log n)) |
| 7. Follow-up | remaining time | Do you propose the next escalation yourself, per [`SENIOR_FOLLOWUPS.md`](../03-patterns/SENIOR_FOLLOWUPS.md)? |
| 8. Postmortem | 2 min after | Fill in one row of [`weakness-log.md`](weakness-log.md) immediately, while it's fresh |

---

## 10-dimension scoring rubric

Score each 0–2 (0 = missed, 1 = partial, 2 = clean) immediately after the round.

| # | Dimension | 0 | 1 | 2 |
|---|---|---|---|---|
| 1 | Clarification | Didn't ask | Asked but missed a key constraint | Surfaced constraints unprompted |
| 2 | Pattern ID speed | >5 min or wrong pattern | 2–5 min | <2 min, correct |
| 3 | Invariant articulation | Couldn't state it | Stated but imprecise | Precise, one sentence |
| 4 | Code correctness | Didn't finish / broke | Ran with bugs fixed via hint | Ran clean or self-fixed |
| 5 | Code structure | Monolithic, poor names | Some structure | Clear helpers, good names, testable seams named |
| 6 | Dry run | Skipped or needed prompting | Did it but shallow | Self-directed, caught own bug if any |
| 7 | Complexity statement | Wrong or skipped | Right answer, weak justification | Right + justified |
| 8 | Follow-up handling | Couldn't progress | Progressed with hints | Self-proposed the escalation |
| 9 | Trade-off communication | Silent | Explained when asked | Volunteered trade-offs unprompted |
| 10 | Recovery from own bugs | Needed hint to find bug | Found bug, slow | Found and fixed fast, named the bug class |

**Total: /20.** Senior bar: **≥16/20**, with no single dimension at 0.

---

## Score log

| Date | Base problem | Chain depth (base/F1/F2/F3) | Total /20 | Weakest dimension | Logged in weakness-log? |
|---|---|---|---|---|---|
| | | | | | |

*(Add rows above this line, newest last.)*

---

## Relationship to existing scoring

- Day-to-day single-problem practice: use the simple ✅/⚠️/❌ scale in [`MOCK_INTERVIEW_SET.md`](../03-patterns/MOCK_INTERVIEW_SET.md).
- Full L4 chain rounds (base + F1 + F2): use the pass bar already defined in [`MOCK_INTERVIEW_SET.md`](../03-patterns/MOCK_INTERVIEW_SET.md#l4-sde-2-mock-rounds--follow-up-chains).
- Full senior chain rounds (base + F1 + F2 + senior F3 from [`SENIOR_FOLLOWUPS.md`](../03-patterns/SENIOR_FOLLOWUPS.md)): use this file's 10-dimension rubric.
