# Google Coding Rounds (SDE-2) — Rubric + Checklist

Use this as a “runbook” for every timed practice and mock.

---

## What “strong” looks like

- **Correctness**: handles edge cases, doesn’t crash, passes examples.
- **Algorithm choice**: avoids brute force when a standard pattern fits.
- **Code quality**: readable names, clean control flow, no over-engineering.
- **Communication**: constraints → approach → invariants → tests → complexity.

---

## The 7-step flow (practice until automatic)

1. **Restate** the problem and confirm constraints.
2. **Examples**: run 1 normal + 1 edge case verbally.
3. **Brute force** quickly (time/space), then explain why it’s too slow (if needed).
4. **Optimal approach**: name the pattern (e.g., “prefix sum + hash map”) and the invariant.
5. **Code**: implement in small, testable chunks.
6. **Test**: run through 2–3 cases by hand (incl. edge case).
7. **Close**: time + space; mention one follow-up direction.

---

## Must-say edge cases (default set)

- Empty input, length 1, all duplicates, negative numbers, overflow (if sums).
- Graph/tree: empty, single node, disconnected components.
- Strings: unicode/case sensitivity (ask), repeated chars.

---

## Debugging checklist (when you get stuck)

- Off-by-one (`<` vs `<=`, window length, bounds in binary search)
- Wrong invariant (what exactly is “valid” in sliding window?)
- Visited/state bugs (graph BFS/DFS)
- Mutation hazards (in-place edits, shared lists in recursion)
- Forgot base case / return value meaning (tree DP)

---

## “Google-style” communication lines (copy/paste into your brain)

- “Let me confirm constraints: can input be empty? duplicates? size limits?”
- “Brute force is O(n²) by checking all pairs; we can do O(n) using a hash map…”
- “The invariant is: the window `[i..j]` always contains at most K distinct…”
- “Time is O(n) because each pointer moves at most n times.”

---

## Virtual (video) vs in-person DSA (same bar, different logistics)

| Setting | What to practice |
|--------|-------------------|
| **Virtual** (e.g. Google Meet, screen share, shared doc) | **Audio first**: think out loud even when not typing. **Test once**: camera, mic, **screen share**, and the **IDE / language** you will use. One monitor is fine; know how to **split** problem statement and editor. **Time zone** and **link** in calendar. Minimize **keyboard noise**; have water nearby. If you have **two** DSA rounds in different formats, do at least one full mock in **video** before the virtual round — see [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md). |
| **In person** | Confirm whether you will **type on a laptop** or use a **whiteboard** (varies by site). Practice that medium: if whiteboard, **bigger** print, leave space for corrections; if laptop, same hygiene as home. Arrive with **buffer** for check-in. |

Both settings: the rubric in **What “strong” looks like** is unchanged. Weak communication hurts more on video when the interviewer cannot read your full scratch work.

---

## Where to revise inside this repo

- Full revision guide: [../foundations/GOOGLE_INTERVIEW_REVISION.md](../foundations/GOOGLE_INTERVIEW_REVISION.md)
- One-page sheet: [../foundations/GOOGLE_QUICK_SHEET.md](../foundations/GOOGLE_QUICK_SHEET.md)
- Canonical question index: [../foundations/TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md](../foundations/TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md)
- Two-week + AI-ML + EET / on-site plan: [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md)

