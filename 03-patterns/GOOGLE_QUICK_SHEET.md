---
module: 03-patterns
topic: Google Quick Sheet
subtopic: 
status: unread
tags: [patterns, google-quick-sheet]
---
# First-Principles Map — Google Interview Quick Sheet

> [!note] L3 Reference Document
> This file is a **reference / meta document** — read it once, then use it as a lookup.
> It is NOT a coding practice file. Do not deep-study it like a topic file.


```
WHY a Google-specific Quick Sheet exists
├── Google's bar is calibrated to L3+ — pattern recognition alone is insufficient
├── Interviewers look for structured reasoning + clean abstraction, not just a working solution
└── Google rounds have specific failure modes not present at other companies

WHAT it is
├── A one-page compressed map of: Google-specific patterns, L3 bar signals, interviewer heuristics
├── Covers: what gets hired, what gets a "no hire," and why
└── Examples:
    ├── L3 signal: correct O(n log n) solution with clean code + edge case handling
    ├── L3 stretch signal: proactively finds the optimal, discusses tradeoffs unprompted
    └── No-hire signal: correct answer but silent, messy, or no complexity analysis

HOW it works
├── Google-specific patterns (appear more often than elsewhere):
│   ├── Graph problems disguised as matrix traversal (BFS/DFS on grid)
│   ├── Interval scheduling / meeting rooms (greedy + sort)
│   ├── Prefix sum + hash → subarray sum equals K
│   └── Two-phase preprocess → query (prefix sum; skip sparse table at L3)
├── L3 bar signals:
│   ├── Arrives at correct approach within 10 min
│   ├── Code is readable without explanation
│   ├── States time/space complexity unprompted
│   └── Tests at least 2 edge cases voluntarily
├── What interviewers score:
│   ├── Problem Solving: correct approach, optimality awareness
│   ├── Coding: clean, no major bugs, good naming
│   ├── Communication: structured, proactive, non-defensive to hints
│   └── Testing: catches own bugs, handles edge cases
└── Complexity:
    ├── Google expects optimal or near-optimal — brute force is a no-hire at L3
    └── "Almost correct" with wrong complexity = no hire

WHEN to use
├── Night before the interview (last-minute anchor)
├── During mock — use as scoring rubric
└── Decision:
    ├── Multiple approaches → state tradeoffs, pick optimal, justify
    ├── Hint received → say "good catch, let me adjust" then fix cleanly
    └── Not sure of complexity → derive it out loud, don't guess

WHAT can go wrong
├── Treating Google like LeetCode — passing test cases ≠ hired
├── Solving correctly but communicating poorly → "brilliant jerk" signal → no hire
├── Skipping complexity analysis → automatic downgrade
└── Over-engineering the solution → wrong signal (clever but unreadable code)
```

## First-Principles Breakdown

- **Root problem:** Google's hiring bar is calibrated to predict on-the-job performance at scale — the interview is a proxy for real engineering judgment, not puzzle solving.
- **Core insight:** L3 bar = correct medium solution + clean code + communicated; near-optimal with tradeoffs stated is a strong hire signal.
- **Invariant:** Every Google round scores four axes (problem solving, coding, testing, communication) — a zero on any axis is a no-hire regardless of other axes.
- **Why it works:** The quick sheet surfaces the meta-game (what the interviewer is scoring) so you optimize for the actual signal, not just the answer.
- **Where it breaks:** If the quick sheet is read but not internalized under pressure — knowing the rubric cold is necessary but not sufficient without practice reps.

---

# Google Interview — One-Page Quick Sheet

Print or keep on a second screen during **last-minute** review (not during the interview). For full context see [GOOGLE_INTERVIEW_REVISION.md](GOOGLE_INTERVIEW_REVISION.md).

---

## Patterns → action

| Pattern | When | Core idea | Time |
|---------|------|-----------|------|
| Hash map | Two sum, frequency, grouping | Key → count or index | O(n) avg |
| Prefix + map | Subarray sum = K | Count of `prefix - K` | O(n) |
| Sliding window | Longest/shortest substring/subarray with constraint | Expand j, shrink i while invalid | O(n) |
| Two pointers | Sorted array, pair/triplet | left/right or slow/fast | O(n) or O(n²) |
| Kadane | Max subarray sum | `cur = max(x, cur+x)` | O(n) |
| BFS | Shortest path unweighted, level order | Queue + visited | O(V+E) |
| DFS | Components, cycle, topo | Stack/recursion + visited | O(V+E) |
| Topo sort | Dependencies, DAG | Kahn (in-degree) or DFS post | O(V+E) |
| Dijkstra | Weighted, non-negative | Min-heap of (dist, node) | O((V+E)log V) |
| Union-Find | Connectivity, Kruskal | find + union | ~O(1) amortized |
| Heap | Top K, merge K lists | Size-K min-heap or push all heads | O(n log k) |
| Binary search on answer | Minimize max, feasibility | `valid(mid)` + search range | O(n log range) |
| Monotonic stack | Next greater, histogram | Pop while smaller | O(n) |
| Tree DP | Max path through node | Postorder, return up value | O(n) |
| 2D DP | LCS, edit distance | `dp[i][j]` from three neighbors | O(nm) |

---

## Must-state edge cases

- Empty / null; length 1; duplicates; negative numbers; integer overflow.
- Graph: disconnected; single node; repeated edges (if relevant).

---

## Complexity sound bites

- “We visit each node/edge at most once → O(V+E).”
- “Sorting dominates → O(n log n).”
- “Hash map gives O(1) average lookup, so overall O(n).”
- “Binary search on answer: O(n) check per mid × O(log range) mids.”

---

## Open with

1. Repeat problem in your words.  
2. Ask: size limits? duplicates? can we modify input?

---

## Close with

1. Time and space.  
2. Two test cases (normal + edge).  
3. Possible follow-up (e.g. stream, huge n).

---

## Full notes

For explanations and practice lists, use [GOOGLE_INTERVIEW_REVISION.md](GOOGLE_INTERVIEW_REVISION.md), [01-data-structures/README.md](../01-data-structures/README.md), and [02-algorithms/README.md](../02-algorithms/README.md). Problem walkthroughs: [`coding/`](../coding/) and [MINDMAP.md](../MINDMAP.md).
