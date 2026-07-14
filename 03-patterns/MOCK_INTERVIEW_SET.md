---
module: 03-patterns
topic: Mock Interview Problem Set
subtopic:
status: unread
tags: [patterns, mock-interview, google-l3]
---

# Google L3 — 25-Problem Mock Interview Set

> [!IMPORTANT]
> **How to use this file**: Do these 25 problems **cold** (no notes, 35–45 min per problem). They are ranked by Google L3 frequency. If you can solve all 25 cleanly, you are ready. Do them in order — early problems unlock the patterns you need for later ones.

---

## Tier 1: Must Solve Cleanly (No Hints)

These cover the patterns that appear in **every** Google L3 loop. Inability to solve any of these is a direct reject signal.

| # | Problem | Pattern | Expected Time | Notes |
|---|---------|---------|---------------|-------|
| 1 | **Two Sum** | Hash map | 5 min | Warm-up. Should be reflex. |
| 2 | **Longest Substring Without Repeating Characters** | Sliding window | 10 min | Canonical variable window |
| 3 | **Number of Islands** | DFS/BFS flood fill | 15 min | Grid graph — must be clean |
| 4 | **Binary Tree Level Order Traversal** | BFS | 10 min | Layered BFS template |
| 5 | **Course Schedule** (Cycle detection) | Kahn's topo sort | 20 min | Edge direction gotcha |
| 6 | **Coin Change** | DP (unbounded knapsack) | 20 min | `dp[0]=0`; build bottom-up |
| 7 | **Merge Intervals** | Sorting + greedy | 15 min | Sort by start; check overlap |
| 8 | **Binary Search in Rotated Sorted Array** | Binary search | 15 min | Identify sorted half first |
| 9 | **Valid Parentheses** | Stack | 10 min | Map close→open; stack match |
| 10 | **Group Anagrams** | Hash map + sorted key | 15 min | Key = sorted string |

---

## Tier 2: Build Fluency (Aim for Clean First Attempt)

These are the problems that separate L3 hires from strong L3 rejects. You should need no hints.

| # | Problem | Pattern | Expected Time | Notes |
|---|---------|---------|---------------|-------|
| 11 | **Minimum Window Substring** | Sliding window + freq | 30 min | `have` vs `need`; two counters |
| 12 | **Longest Common Subsequence** | 2D DP | 25 min | `dp[i][j]` from scratch |
| 13 | **Word Search** | Backtracking + DFS | 25 min | Mark visited in-place; restore |
| 14 | **Find Median from Data Stream** | Two heaps | 25 min | Max-heap left, min-heap right |
| 15 | **Lowest Common Ancestor (Binary Tree)** | Tree DFS postorder | 20 min | Return node if found; if both sides non-null → LCA |
| 16 | **Pacific Atlantic Water Flow** | Reverse BFS from borders | 30 min | Two BFS sets; intersect |
| 17 | **Jump Game** | Greedy | 15 min | Track furthest reachable |
| 18 | **Kth Largest Element in an Array** | Heap or quickselect | 15 min | Min-heap of size K |
| 19 | **Clone Graph** | BFS + hash map | 20 min | Create clone before recursing |
| 20 | **Combination Sum** | Backtracking | 20 min | `start` index; no skip needed |

---

## Tier 3: Stretch Problems (Common at Google, Separates Offers)

If you can solve all of these, you are overperforming L3 and will likely get a strong hire.

| # | Problem | Pattern | Expected Time | Notes |
|---|---------|---------|---------------|-------|
| 21 | **Word Ladder** | BFS on implicit graph | 35 min | One-letter edits = neighbors; remove from set when visited |
| 22 | **Serialize and Deserialize Binary Tree** | DFS preorder | 35 min | Use `None` markers; split on `,` |
| 23 | **Trapping Rain Water** | Two pointers or monotonic stack | 25 min | Two-pointer: `min(max_l, max_r) - height[i]` |
| 24 | **Maximum Profit in Job Scheduling** | DP + binary search | 40 min | Sort by end time; BS to find non-overlapping previous job |
| 25 | **Alien Dictionary** | Topo sort + edge extraction | 35 min | Compare adjacent words → first diff = edge; cycle → return `""` |

---

## Mock Interview Scoring Guide

For each attempt, score yourself:

| Score | Criteria |
|-------|----------|
| ✅ **Clean** | Solved within time, correct on first run (or found own bug in dry-run), stated complexity correctly |
| ⚠️ **Partial** | Solved but needed 5+ min extra, OR found bug only after interviewer hinted |
| ❌ **Fail** | Did not solve, or solved with major hint, or couldn't state complexity |

**Target before the interview:** ≥ 17/20 on Tier 1+2 at ✅ Clean.

---

## Quick Pattern Recall (For Warm-Up Before Each Session)

Before starting a mock session, spend 2 minutes saying these out loud:

```
Two Sum             → hash map, complement lookup
Sliding Window      → expand right, shrink left while invalid
BFS shortest path   → mark visited BEFORE enqueue
DFS flood fill      → mark in-place (sink), or visited set
Topo sort           → Kahn's: in-degree queue; cycle if len < n
Knapsack DP         → dp[w] inner loop; iterate w BACKWARD for 0/1
Backtracking        → choose → recurse → undo
Two heaps           → max-heap left (smaller), min-heap right (larger)
Binary search       → find sorted half first (rotated), BS on answer
Greedy intervals    → sort by end time; pick earliest non-overlapping
```

---

## Weak Area Drill List

Use this when a mock attempt reveals a gap:

| Weak Area | Drill These |
|-----------|-------------|
| Sliding window | Minimum Window Substring → Find All Anagrams → Longest Repeating Char Replacement |
| Graph BFS | Rotting Oranges → Walls and Gates → Shortest Path in Binary Matrix |
| Topo sort | Course Schedule II → Alien Dictionary → Sequence Reconstruction |
| Tree DP | Max Path Sum → Diameter → House Robber III |
| 2D DP | Unique Paths → LCS → Edit Distance → Interleaving Strings |
| Backtracking | Subsets → Permutations → N-Queens → Sudoku Solver |
| Heap | Merge K Sorted → Task Scheduler → Ugly Number II |
| Binary search | Koko Eating Bananas → Find Minimum in Rotated Array → Split Array Largest Sum |

---

## L4 (SDE-2) Mock Rounds — follow-up chains

> [!IMPORTANT]
> An L4 round is not one problem — it's a **chain**. Budget 45 min per round: base problem solved cleanly in ~20–25 min, then the interviewer escalates. Simulate that: solve the base, then *without a break* attempt each follow-up. A round "passes" only if you get through follow-up 1. Full L4 bar: [`coding/l4-sde2-delta.md`](../coding/l4-sde2-delta.md).

| Round | Base (20–25 min) | Follow-up 1 | Follow-up 2 (stretch) |
|---|---|---|---|
| A | Insert Delete GetRandom O(1) | allow duplicates | weighted `getRandom` (→ Random Pick with Weight) |
| B | Merge Intervals | bookings arrive online (→ My Calendar I) | reject only triple bookings (→ My Calendar II) |
| C | Network Delay Time (Dijkstra cold) | grid version, minimize max edge (→ Path With Minimum Effort) | at most k stops — why Dijkstra breaks (→ Cheapest Flights) |
| D | LRU Cache | evict by frequency (→ LFU) | thread safety — discuss locking, don't code |
| E | Word Search | many words to find (→ Word Search II, Trie) | prune trie nodes after matches |
| F | Kth Largest in a Stream | median of a stream (→ two heaps) | values can be *corrected* later (→ lazy deletion, Stock Price Fluctuation) |
| G | Longest Increasing Subsequence | O(n log n) version | 2-D: Longest Increasing Path in a Matrix |
| H | Rotting Oranges | BFS from all targets (→ 01 Matrix) | answer counts *routes* not cells (→ Bus Routes) |

Scoring per round: base unsolved = not ready; base + F1 = on the bar; base + F1 + F2 = strong hire territory. Log which *invariant* failed, per the [Pattern Ladders](PATTERN_LADDERS.md) protocol.

---

## See Also

- [patterns-master.md](./patterns-master.md) — Full pattern reference
- [GOOGLE_INTERVIEW_REVISION.md](./GOOGLE_INTERVIEW_REVISION.md) — 7-day and 48-hour schedules
- [TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md](./TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md) — Per-topic problem breakdowns
