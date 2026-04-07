# Greedy Algorithms — SDE-3 Level

Make the **locally optimal choice** at each step; prove (or argue) it leads to a **global optimum**. SDE-3 expects proof intuition, exchange arguments, and when greedy fails.

---

## 1. Concept Overview

**Problem space**: Interval scheduling, jump game, gas station, task scheduler, Huffman, MST (Prim/Kruskal), activity selection, "minimum arrows to burst balloons", candy (two passes).

**When to use**: Optimal substructure + greedy choice property. If "take best local option" can be shown never to hurt the global solution, use greedy. Otherwise consider DP.

---

## 2. Core Ideas

- **Greedy choice property**: A global optimum can be achieved by taking the local optimum at each step.
- **Optimal substructure**: Optimal solution contains optimal solutions to subproblems.
- **Proof techniques**: Exchange argument (swap greedy choice into any optimal solution); greedy stays ahead (greedy is never behind optimal at each step); structural (e.g., "earliest deadline first" maximizes count).

---

## 3. Common Patterns

- **Sort first**: Intervals by end (or start); items by ratio; then scan and take greedily.
- **Priority queue**: Always take min/max (e.g., merge K lists, Huffman, Task Scheduler — most frequent first).
- **Two passes**: Candy (left-to-right then right-to-left for constraints).
- **Jump / reachability**: Jump Game — track farthest reachable; Jump Game II — min jumps = BFS levels or greedy "jump to farthest we can each time".

---

## 4. Classic SDE-3 Greedy Problems

**Easy**: Assign Cookies, Array Partition I, Largest Perimeter Triangle.  
**Medium**: Jump Game, Jump Game II, Gas Station, Task Scheduler, Non-overlapping Intervals, Min Arrows to Burst Balloons.  
**Hard**: Min Refueling Stops, Reaching Points, Candy.

---

## 5. Pattern Recognition

- **Intervals**: Sort by end (or start); take non-overlapping greedily. "Min arrows" = sort by end, shoot at end, skip covered.
- **Scheduling**: Earliest deadline; or by frequency (Task Scheduler: slot by max freq).
- **Reachability**: Farthest index we can reach; min jumps = number of "steps" to reach end.
- **When greedy fails**: Need to try multiple choices (DP) or constraints are global (e.g., partition equal subset — DP).

---

## 6. SDE-3 Level Thinking

- **Trade-offs**: Greedy O(N log N) or O(N) vs DP O(N²); greedy when proof is clear; DP when in doubt for optimization.
- **Scalability**: Sorting and single pass; heap when "current best" changes dynamically.

---

## 7. Interview Strategy

- **Identify**: "Schedule most", "minimum cost to cover", "earliest/largest first" → try greedy. State "I'll try greedy and argue it's optimal."
- **Approach**: Define the greedy rule; give exchange or "stays ahead" intuition; then code.
- **Common mistakes**: Not sorting correctly (by end vs start); wrong heap type; forgetting to handle ties.

---

## 8. Quick Revision

- **Tricks**: Intervals → sort by end; take if start >= last_end. Jump II → while not at end: jump to farthest in current range, steps++. Task Scheduler → (max_count-1)*(n+1) + num_max (with cap at len(tasks)).
- **Edge cases**: Empty; single interval; all same; zero/n negative.
- **Pattern tip**: "Maximum number of non-overlapping" / "minimum to cover" → sort + greedy.

---

## 9. Code sketch (non-overlapping intervals)

```python
def eraseOverlapIntervals(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])  # sort by end time
    end = intervals[0][1]
    removals = 0
    for s, e in intervals[1:]:
        if s < end:       # overlap with previous chosen interval
            removals += 1
        else:
            end = e
    return removals
```

**Jump Game II** (minimum jumps): greedy “furthest in current jump range” — extend `end` of current level, when `i == reach` increment jumps and set `reach = furthest`.

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness |
|----------|------------|------------|
| **Jump Game II** | Greedy: furthest in current jump range; increment jumps at range end | Jump Game I is only reachability — different |
| **Non-overlapping Intervals** | Sort by **end**; count removal when overlap | Sort by start fails — counterexample |
| **Gas Station** | If total gas ≥ total cost, start exists; reset when tank < 0 | Proof of uniqueness |
| **Task Scheduler** | Idle slots `(max-1)*(n+1)+num_max` | Cap at `len(tasks)` |
| **Assign Cookies** | Sort both; greedily match smallest cookie that fits | Two pointers after sort |
| **Candy** | Left pass then right pass ratings | Two passes for both constraints |

---

## See also

- [Dynamic Programming](dynamic-programming/README.md) — when greedy fails  
- [Sorting](sorting.md) — sort key for intervals  
- [patterns/leetcode-patterns.md](../../patterns/leetcode-patterns.md)
