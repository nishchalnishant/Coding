---
module: striver-a2z
topic: Study plan — 16-week order through all 33 parts with revision checkpoints
tags: [striver, plan, revision]
---
# Study Plan

← [Striver course map](README.md) · [Problem index](PROBLEM_INDEX.md) · [Pattern triggers](../03-patterns/patterns-master.md)

> [!abstract] How to use this
> The plan runs 16 weeks at about 2 hours a day, covering 506 notes. Each week is **theory first, then problems, then a checkpoint**.
> - **Compressed (8 weeks):** merge each pair of weeks and skip Parts 3–4. Add Part 33 as a parallel interview-readiness track during the final 4 weeks.
> - **Already fluent in a language:** skim Parts 1–7 in 2 days.
> - **Rule:** don't move on until you pass the checkpoint, meaning you can solve two random problems from the block in time without notes.

**Sections:** [1. Daily loop](#1-daily-loop) · [2. Revision protocol](#2-revision-protocol) · [3. Week-by-week](#3-week-by-week) · [4. Checkpoints](#4-checkpoints) · [5. Final two weeks](#5-final-two-weeks)

---

## 1. Daily loop

| Step | Time | What |
|---|---|---|
| Warm-up | 10 min | Re-solve one problem that is due for revision (§2) from a blank editor |
| Theory | 20–30 min | The block's theory note: read the sections, then answer the Practice questions without looking |
| Problems | 60–75 min | 3–5 problems. Give each 20–25 minutes before you open the note. Then read the optimal approach and re-code it |
| Log | 5 min | Record the problem, the pattern, what blocked you and the next revision date |

**Per-problem protocol:**
1. Restate the problem, then write the brute force with its complexity.
2. Find the repeated work, then pick a pattern from [Pattern triggers](../03-patterns/patterns-master.md).
3. Code it, then dry-run the note's edge cases.
4. Compare with the note's **Optimal** column. If yours differs, re-code theirs.

---

## 2. Revision protocol

| When | What |
|---|---|
| Day +2 | Re-solve from scratch. Fail → back to +2 |
| Day +7 | Re-solve from scratch, explaining aloud as in an interview |
| Day +21 | Solve a different problem from the same pattern |
| Weekly | Flashcards (`#flashcard`) from that week's theory notes plus the part's cheat sheet in [Master cheat sheet](MASTER_CHEATSHEET.md) |

Mark a problem **mastered** after you pass it at +21. Keep the log in one table: problem, pattern, date, +2, +7, +21 and notes.

---

## 3. Week-by-week

| Week | Parts | Notes | Focus | Start with |
|---|---|---|---|---|
| 1 | [1](01-fundamentals-of-programming/README.md)–[7](07-concept-basics/README.md) | 43 | Language, I/O, loops, patterns, Big-O, STL / collections | [Time complexity](05-time-complexity/01-theory-with-examples.md) |
| 2 | [8](08-basic-maths/README.md)–[12](12-basic-recursion/README.md) | 40 | Digit maths, basic arrays, hashing, strings, recursion | [Recursion theory](12-basic-recursion/01-recursion-theory.md) |
| 3 | [13](13-sorting/README.md), [14](14-arrays/README.md) (easy + medium) | ~28 | Sorting algorithms, array techniques | [Sorting theory](13-sorting/00-sorting-theory.md), [Array techniques](14-arrays/00-array-techniques-theory.md) |
| 4 | [14](14-arrays/README.md) (hard), [15](15-hashing/README.md), [17](17-strings-basic-medium/README.md) | ~28 | Prefix sums, Kadane, voting, merge-sort counting, strings | [String basics](17-strings-basic-medium/00-string-basics-theory.md) |
| 5 | [16](16-binary-search/README.md) | 33 | Bounds, rotated arrays, binary search on the answer, 2D | [Binary search templates](16-binary-search/01-binary-search-templates.md) |
| 6 | [18](18-recursion/README.md), [20](20-bit-manipulation/README.md) | 37 | Backtracking, subsets, bit tricks | [Subsequence patterns](18-recursion/01-subsequence-patterns.md), [Bit tricks](20-bit-manipulation/01-bits-and-tricks.md) |
| 7 | [19](19-linked-list/README.md) | 45 | Pointer manipulation, fast/slow, reversal, DLL | Part README |
| 8 | [21](21-greedy-algorithms/README.md), [22](22-sliding-window-and-2-pointer/README.md) | 29 | Greedy proofs, intervals, sliding window | [Greedy fundamentals](21-greedy-algorithms/01-greedy-fundamentals.md), [Sliding window](22-sliding-window-and-2-pointer/01-sliding-window-theory.md) |
| 9 | [23](23-stack-and-queues/README.md) | 31 | Monotonic stack/deque, expressions, LRU/LFU | [Stack/queue theory](23-stack-and-queues/01-stack-queue-implementation-theory.md) |
| 10 | [24](24-binary-trees/README.md) | 32 | Traversals, views, DFS returning values, construction | [Binary tree theory](24-binary-trees/01-binary-tree-theory.md) |
| 11 | [25](25-binary-search-trees/README.md), [26](26-heaps/README.md) | 35 | BST ordering, heaps, top-k, two heaps | [BST theory](25-binary-search-trees/01-bst-theory.md), [Heap theory](26-heaps/01-heap-theory.md) |
| 12 | [27](27-graphs/README.md) (1–24) | 24 | BFS/DFS, components, cycles, bipartite, topological sort | [Graph theory](27-graphs/01-graph-theory.md) |
| 13 | [27](27-graphs/README.md) (25–46) | 22 | Dijkstra, Bellman–Ford, Floyd, DSU, MST, SCC, bridges | [MST and DSU](27-graphs/02-mst-and-dsu-theory.md) |
| 14 | [28](28-dynamic-programming/README.md) (1D, grid, subsequences) | ~27 | Recursion → memo → table → space | [DP theory](28-dynamic-programming/01-dp-theory.md) |
| 15 | [28](28-dynamic-programming/README.md) (strings, stocks, LIS, MCM, squares) | ~27 | DP on strings, state machines, interval DP | Part README |
| 16 | [29](29-tries/README.md)–[32](32-beyond-the-sheet/README.md) | 25 | Tries, KMP/Z/hashing, sieve, modular arithmetic, advanced add-ons | [Trie theory](29-tries/01-trie-theory.md), [String matching](30-strings-advanced/01-string-hashing-and-matching-theory.md) |
| 17 (parallel) | [33](33-sde2-interview-prep/README.md) | 6 lessons | Coding execution, core CS, LLD, system design, behavioral stories, mock interviews | [Practice plan](33-sde2-interview-prep/06-practice-plan.md) |

**Priority order if time is short:** 14 → 16 → 22 → 23 → 24 → 27 → 28 → 19 → 26 → 18 → 21 → 25. Part 32 is for hard rounds and senior follow-ups only.

---

## 4. Checkpoints

| After week | Check (timed, no notes) | Pass bar |
|---|---|---|
| 2 | Reverse a number, check a palindrome, frequency of elements, recursion sum of n | 10 minutes each, all edge cases |
| 4 | 2 random medium problems from Part 14 | 25 minutes each |
| 5 | 1 "binary search on the answer" problem + 1 rotated array | Correct predicate, no off-by-one |
| 6 | Combination Sum II + Subsets II | Duplicates handled by skipping at the same level |
| 8 | 1 sliding window + 1 interval greedy | Window invariant stated aloud |
| 9 | Largest rectangle in a histogram | Under 25 minutes |
| 11 | 1 tree DFS-value problem + 1 heap top-k | State the return value before coding |
| 13 | 1 Dijkstra variant + 1 DSU problem | Correct graph modelling in 5 minutes |
| 15 | 3 random DP problems from Part 28 | State, recurrence and base case before coding |
| 16 | 2 mixed-topic mocks ([mock set](../03-patterns/INTERVIEW_JUDGMENT.md#part-d--mock-rounds)) | 45 minutes each, with explanation |

If you fail a checkpoint, spend one extra day on that block's weakest pattern before moving on.

---

## 5. Final two weeks

Run these after week 16, or in the last 2 weeks before interviews.

| Day | What |
|---|---|
| 1–5 | One mock a day (two problems, 45 minutes). Log weaknesses by pattern |
| 6–8 | Drill the three weakest patterns from the log, using [Pattern triggers](../03-patterns/patterns-master.md) to find more problems |
| 9–11 | Re-solve every problem that failed a revision |
| 12–13 | [Master cheat sheet](MASTER_CHEATSHEET.md) plus all flashcards |
| 14 | Light: read [L3 cheatsheet](../00-start-here/L3_CHEATSHEET.md) edge cases and the complexity table. No new problems |

---

**Interview track →** [Interview revision](../03-patterns/INTERVIEW_JUDGMENT.md#part-c--round-execution--revision) · [Mock set](../03-patterns/INTERVIEW_JUDGMENT.md#part-d--mock-rounds) · [Interview judgment](../03-patterns/INTERVIEW_JUDGMENT.md)
