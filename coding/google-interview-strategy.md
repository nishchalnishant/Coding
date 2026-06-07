---
tags: [l3-google, meta, interview-strategy]
topic: Google L3 Interview Strategy
---

# Google L3 Interview Strategy

> [!important] What L3 tests
> **4–5 coding rounds** (35–45 min each) + **Googliness/behavioral**. One LeetCode-style problem per round. No system design, LLD, SQL, or concurrency.

## Round structure (typical 45 min)

| Phase | Time | What to do |
| :--- | :--- | :--- |
| Clarify | 3–5 min | Restate problem, ask about input size, duplicates, edge cases, expected output |
| Examples | 2–3 min | Walk through 1–2 examples; call out tricky case |
| Brute force | 3–5 min | Naive approach + complexity; shows you can solve it |
| Optimize | 5–8 min | Name pattern, justify complexity, get verbal buy-in |
| Code | 15–20 min | Clean Python; narrate non-obvious lines |
| Test & wrap | 5 min | Dry-run custom case; state time/space Big-O |

Full pacing: [`00-L3-EXECUTION-META/01-45-minute-execution-plan.md`](../00-L3-EXECUTION-META/01-45-minute-execution-plan.md)

## What Google rewards at L3

- **Structured thinking** — brute force → optimize, not silent coding
- **Correct medium solutions** — optimal on easy/medium; near-optimal acceptable if communicated
- **Clean code** — meaningful names, no dead code, handle empty/single-element inputs
- **Proactive testing** — you catch your own off-by-one before the interviewer does
- **Collaboration** — treat hints as pair-programming, not failure

## What gets a no-hire

- Cannot reach a workable approach in ~15 min on a medium
- Code with major logic bugs and no self-correction
- Silent coding or defensive when given hints
- Wrong complexity with no attempt to derive it
- Ignoring stated constraints (mutating input when forbidden, etc.)

## Pattern priority (study order)

Follow [`l3-google-roadmap.md`](./l3-google-roadmap.md):

1. Graphs (BFS/DFS, topo, union-find)
2. Sliding window + two pointers
3. Binary search (including search on answer)
4. Heaps + tries
5. Core DP + backtracking

## Day-of checklist

- [ ] Read [`03-patterns/interview-cheatsheet.md`](../03-patterns/interview-cheatsheet.md) (10 min max)
- [ ] Skim [`03-patterns/GOOGLE_QUICK_SHEET.md`](../03-patterns/GOOGLE_QUICK_SHEET.md)
- [ ] Review 2 STAR stories from [`04-behavioral/behavioral.md`](../04-behavioral/behavioral.md)
- [ ] Python syntax refresh: [`00-L3-EXECUTION-META/03-python-whiteboarding-cheatsheet.md`](../00-L3-EXECUTION-META/03-python-whiteboarding-cheatsheet.md)

## Related

| Resource | Link |
| :--- | :--- |
| 4-week schedule | [`l3-google-roadmap.md`](./l3-google-roadmap.md) |
| Pattern triggers | [`FLOWCHARTS.md`](../FLOWCHARTS.md) |
| Problem index + hints | [`MINDMAP.md`](../MINDMAP.md) |
| Progress tracker | [`questions.md`](../questions.md) |
