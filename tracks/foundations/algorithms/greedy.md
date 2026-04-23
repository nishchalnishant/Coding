# Greedy Algorithms — SDE-3 Gold Standard

Make the **locally optimal choice** at each step; prove it leads to a **global optimum**. SDE-3 expects: proof intuition (exchange argument or "stays ahead"), knowing when greedy fails, and choosing between greedy and DP under pressure.

---

## 1. Concept Overview

**When to use**: Optimal substructure + **greedy choice property** (the globally optimal solution can always be extended by taking the locally best choice). If "take best local option" can be shown never to hurt the global solution, use greedy. Otherwise, reach for DP.

**Proof techniques**:
- **Exchange argument**: Take any optimal solution; swap the greedy choice into it; show the solution doesn't get worse.
- **Greedy stays ahead**: At each step, the greedy solution is at least as good as any other partial solution (e.g., "most tasks completed by time T").
- **Structural argument**: The problem's structure guarantees greedy works (e.g., earliest-deadline-first maximizes task count).

---

## 2. Core Patterns & Click Moments

### Interval Scheduling — Sort by End Time

> [!IMPORTANT]
> **The Click Moment**: "**Maximum non-overlapping** intervals" — OR — "**minimum arrows** to pop balloons" — OR — "schedule **maximum meetings**". Sort by **end time** and greedily pick intervals that don't overlap. Sorting by start time is wrong — construct a counterexample instantly to prove it.

```python
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])  # sort by END time
    removals = 0
    last_end = intervals[0][1]
    for s, e in intervals[1:]:
        if s < last_end:  # overlap
            removals += 1  # remove current (keep the one with earlier end)
        else:
            last_end = e
    return removals

def min_arrows_to_burst_balloons(points: list[list[int]]) -> int:
    if not points:
        return 0
    points.sort(key=lambda x: x[1])
    arrows = 1
    arrow_pos = points[0][1]
    for start, end in points[1:]:
        if start > arrow_pos:  # this balloon starts after the current arrow — new arrow needed
            arrows += 1
            arrow_pos = end
    return arrows
```

> [!CAUTION]
> **Overlap boundary condition**: "Minimum Arrows" uses `start > arrow_pos` (strict) — touching at a point counts as one shot. "Non-overlapping Intervals" uses `s < last_end` (strict) — intervals touching at a point are **not** overlapping. Get the `>` vs `>=` wrong and fail on boundary cases.

---

### Jump Game — Reachability

> [!IMPORTANT]
> **The Click Moment**: "**Can you reach the end?**" (Jump Game I) — OR — "**minimum jumps** to reach end" (Jump Game II). Both use a single greedy pass. Jump Game I: track `farthest` reachable index. Jump Game II: treat as BFS levels — when you exhaust the current "jump range", count a new jump.

```python
def can_jump(nums: list[int]) -> bool:
    farthest = 0
    for i, jump in enumerate(nums):
        if i > farthest:
            return False  # this position is unreachable
        farthest = max(farthest, i + jump)
    return True

def jump_game_ii_min_jumps(nums: list[int]) -> int:
    jumps = 0
    current_end = 0  # end of current jump range
    farthest = 0     # farthest we can reach in the next jump
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == current_end:  # exhausted current range — must jump
            jumps += 1
            current_end = farthest
    return jumps
```

> [!TIP]
> Jump Game II does **not** need DP. The greedy argument: at every position `i`, you know the farthest you can reach (`farthest`). When you must jump (at `i == current_end`), jumping to `farthest` is always optimal — any choice within `[current_end+1, farthest]` that improves reach is already captured by `farthest`.

---

### Gas Station — Circular Feasibility

> [!IMPORTANT]
> **The Click Moment**: "Can you complete a **circular route**?" — OR — "is there a **starting point** where a circular process completes?" Two key facts: (1) If `sum(gas) >= sum(cost)`, a valid start always exists. (2) The valid start is the position immediately after the longest prefix where the running sum goes negative.

```python
def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    if sum(gas) < sum(cost):
        return -1  # total deficit — no valid start
    tank = 0
    start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:  # can't reach i+1 from current start
            start = i + 1  # reset start to next position
            tank = 0
    return start
```

> [!CAUTION]
> The problem guarantees a **unique** valid start when `sum(gas) >= sum(cost)`. This uniqueness is key to the greedy correctness — if there were two valid starts, one would be contained within the other, contradicting the structure of the circular traversal.

---

### Task Scheduler — Frequency-Based Scheduling

> [!IMPORTANT]
> **The Click Moment**: "**Schedule tasks** with a cooldown of **n** between same tasks" — OR — "minimum time to finish all tasks with CPU cooling". The formula `(max_freq - 1) * (n + 1) + count_with_max_freq` counts the slots needed. The final answer is `max(formula, len(tasks))` — when variety fills all idle slots, no idle time is needed.

```python
from collections import Counter

def least_interval(tasks: list[str], n: int) -> int:
    if n == 0:
        return len(tasks)
    freq = Counter(tasks)
    max_freq = max(freq.values())
    count_max = sum(1 for f in freq.values() if f == max_freq)
    min_slots = (max_freq - 1) * (n + 1) + count_max
    return max(min_slots, len(tasks))
```

---

### Candy Distribution — Two-Pass Greedy

> [!IMPORTANT]
> **The Click Moment**: "Distribute **minimum candy** satisfying local constraints from both directions". No single-pass greedy works here — left-to-right constraints and right-to-left constraints are independent and must be merged with `max`.

```python
def candy(ratings: list[int]) -> int:
    n = len(ratings)
    candy = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i-1]:
            candy[i] = candy[i-1] + 1
    for i in range(n-2, -1, -1):
        if ratings[i] > ratings[i+1]:
            candy[i] = max(candy[i], candy[i+1] + 1)
    return sum(candy)
```

---

### Partition Labels — Greedy Range Extension

> [!IMPORTANT]
> **The Click Moment**: "Partition string into parts so each **letter appears in exactly one part**". Record the last occurrence of each character. Sweep and extend the current partition's end to `max(end, last[ch])`. When `i == end`, cut.

```python
def partition_labels(s: str) -> list[int]:
    last = {ch: i for i, ch in enumerate(s)}
    partitions = []
    start = end = 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])
        if i == end:
            partitions.append(end - start + 1)
            start = i + 1
    return partitions
```

---

## 3. SDE-3 Deep Dives

### When Greedy Fails: DP is Needed

> [!CAUTION]
> Greedy fails when a locally optimal choice precludes a globally better one that requires "sacrificing" now for gain later. Classic greedy failures:
> - **0/1 Knapsack**: Taking the highest value-density item can block a combination of smaller items with higher total value.
> - **Coin Change (general denominations)**: US coins work greedily (25, 10, 5, 1); `[1, 3, 4]` with target 6 does not (`4+1+1` = 3 coins vs `3+3` = 2 coins).
> - **Edit Distance**: Local character matches don't minimize global operations.
>
> Rule of thumb: if you can construct a counterexample, it's not greedy — reach for DP.

### Scalability: Online / Streaming Greedy

> [!TIP]
> Many greedy algorithms are **online** (process one element at a time without future knowledge):
> - **Interval scheduling**: Sort offline is required. For online scheduling, use a priority queue of active intervals by end time.
> - **Task Scheduler in production**: At Google scale, task scheduling is a distributed bin-packing problem — use the **Longest Processing Time (LPT)** greedy for makespan minimization on K machines.
> - **Online ads**: Greedy matching of ads to slots using priority queue of bids — approximation ratio of `1 - 1/e` for online bipartite matching.

### Concurrency: Parallel Greedy

> [!TIP]
> Some greedy algorithms parallelize naturally:
> - **Huffman coding**: Build the priority queue in parallel; merge step is sequential but small.
> - **Prim's MST**: Each machine explores its local graph shard; coordinator merges minimum edges. Approximated in distributed settings via Borůvka's algorithm — inherently parallel (each component finds its lightest outgoing edge simultaneously).

### Trade-offs: Greedy vs DP vs Backtracking

| Approach | Time | Space | When Correct |
| :--- | :--- | :--- | :--- |
| Greedy | O(N log N) or O(N) | O(1) or O(N) | Greedy choice property provable |
| DP (bottom-up) | O(N²) typical | O(N) or O(N²) | Overlapping subproblems + optimal substructure |
| Backtracking | Exponential | O(depth) | All solutions needed; no greedy/DP structure |
| Approximation greedy | Polynomial | O(N) | NP-hard problems; acceptable approximation ratio |

---

## 4. Common Interview Problems

### Easy
- **Assign Cookies** — Sort kids and cookies; two-pointer greedy matching.
- **Largest Perimeter Triangle** — Sort descending; first triple where `a < b + c`.

### Medium
- **Jump Game I** — Track `farthest`; O(N) single pass.
- [Jump Game II](../../google-sde2/PROBLEM_DETAILS.md#jump-game-ii) — Greedy BFS levels; O(N).
- [Non-overlapping Intervals](../../google-sde2/PROBLEM_DETAILS.md#non-overlapping-intervals) — Sort by end; keep non-overlapping.
- **Meeting Rooms II** — Min-heap of end times; active room count = heap size.
- [Gas Station](../../google-sde2/PROBLEM_DETAILS.md#gas-station) — Running tank; reset start on deficit.
- [Task Scheduler](../../google-sde2/PROBLEM_DETAILS.md#task-scheduler) — Formula or heap simulation.
- **Partition Labels** — Last occurrence map; sweep and cut.
- **Candy** — Two-pass: left-right then right-left.
- **Minimum Arrows to Burst Balloons** — Sort by end; shoot at end of each new balloon.

### Hard
- **Minimum Refueling Stops** — Max-heap of reachable fuel; refuel largest when tank runs dry.
- **IPO (Maximize Capital)** — Sort by capital; max-heap of available profits.
- **Smallest Range Covering K Lists** — K-way merge + greedy window shrink.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **Jump Game I** | "Can you reach the end?" | Track `farthest`; if `i > farthest` → False | O(N) — not DP. Greedy works because reaching farther never hurts. |
| **[Jump Game II](../../google-sde2/PROBLEM_DETAILS.md#jump-game-ii)** | "Minimum jumps to end" | Greedy BFS: jump to `farthest` when `i == current_end` | Increment jumps at `current_end`, not when pushing `farthest`. Off-by-one on final step. |
| **[Non-overlapping Intervals](../../google-sde2/PROBLEM_DETAILS.md#non-overlapping-intervals)** | "Remove minimum to make non-overlapping" | Sort by end; keep non-overlapping; count removed | Sort by **end** (not start). Max non-overlapping = n - removed. |
| **Min Arrows to Burst Balloons** | "Minimum shots to pop all balloons" | Sort by end; new arrow only if `start > arrow_pos` | `>` not `>=` — touching boundary is one shot. |
| **[Gas Station](../../google-sde2/PROBLEM_DETAILS.md#gas-station)** | "Starting point for circular traversal" | Reset `start` when tank goes negative | Uniqueness: valid start exists iff `sum(gas) >= sum(cost)`. |
| **[Task Scheduler](../../google-sde2/PROBLEM_DETAILS.md#task-scheduler)** | "Minimum time with cooldown n" | `(max_f-1)*(n+1) + count_max`, cap at `len(tasks)` | The cap handles "enough variety to fill idle slots" — don't forget `max(formula, len(tasks))`. |
| **Assign Cookies** | "Satisfy max children greedily" | Sort both; smallest sufficient cookie per smallest unsatisfied child | Two-pointer: greedily match smallest satisfied first. |
| **Candy** | "Minimum candy with neighbor constraints" | Two-pass: L→R then R→L; `candy[i] = max(both passes)` | One pass fails — left and right constraints are independent. |
| **Fractional Knapsack** | "Max value with fractional items" | Sort by value/weight; take greedily | 0/1 Knapsack is **not** greedy — needs DP. Verify items are divisible. |
| **Minimum Refueling Stops** | "Fewest stops to reach destination" | Max-heap of reachable stations; refuel when tank < 0 | Greedily take the largest available fuel when you must stop — not the nearest. |
| **Partition Labels** | "Partition so each letter in one part" | `last[ch]` map; extend `end`; cut at `i == end` | Each letter's last occurrence defines the minimum partition end. |

---

## See also

- [Dynamic Programming](dynamic-programming/README.md) — when greedy choice property fails
- [Sorting](sorting.md) — sorting is prerequisite for interval and scheduling greedy
- [Heap](../data-structures/heap.md) — priority queue for dynamic "current best" selection
- [Patterns Master](../../../reference/patterns/patterns-master.md) — greedy pattern triggers
