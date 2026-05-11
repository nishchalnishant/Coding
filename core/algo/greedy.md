# Greedy Algorithms — SDE-3 Gold Standard

Make the **locally optimal choice** at each step; prove it leads to a **global optimum**. SDE-3 expects: proof intuition (exchange argument or "stays ahead"), knowing when greedy fails, and choosing between greedy and DP under pressure.

---

## Theory & Mental Models

**What it is.** Make the locally optimal choice at each step, trusting that this leads to a globally optimal solution. Core invariant: the **greedy choice property** must hold — taking the best available option now never prevents a better global outcome.

**Why it exists.** For problems with the greedy choice property, a single sorted pass or priority queue replaces exponential search. Greedy is correct when "best now" never conflicts with "best overall" — this must be provable, not assumed.

**The mental model.** A miser who always takes the best deal available right now. This works perfectly when the deals are independent (interval scheduling) and catastrophically when future deals depend on current choices (0/1 knapsack).

**Complexity at a glance.**

| Pattern | Time | Space |
| :--- | :--- | :--- |
| Sort-based greedy (interval scheduling, task scheduling) | O(N log N) | O(1) or O(N) |
| Single-pass greedy (jump game, gas station) | O(N) | O(1) |
| Priority-queue greedy (Prim's MST, Huffman) | O(N log N) | O(N) |

**When to reach for it.**
- Interval scheduling: maximize non-overlapping intervals (sort by end time).
- Jump reachability: track the farthest index reachable.
- Gas station circuit: reset start after any deficit prefix.
- Task scheduling with cooldown: arrange by frequency.
- Partition / labeling: extend a partition greedily to the last occurrence of any character in it.

**When NOT to use it.**
- Taking the best local choice can block a globally better combination — use DP (classic failure: coin change with non-standard denominations like [1, 3, 4]).
- 0/1 knapsack — greedy on value-density fails; fractional knapsack works.
- If you cannot articulate an exchange argument or "greedy stays ahead" proof — try DP first.

**Common mistakes.**
- Sorting by the wrong key — intervals need end-time sort for maximum non-overlapping, start-time for merging.
- Assuming greedy works without a proof — always construct a potential counterexample first.
- Applying greedy to 0/1 knapsack (fractional knapsack is greedy; 0/1 is not).
- Missing the `max(formula, len(tasks))` cap in task scheduler — when task variety fills all idle slots.

---

## 1. Concept Overview: The SDE-3 Bar

**When to use**: Optimal substructure + **greedy choice property** (the globally optimal solution can always be extended by taking the locally best choice). If "take best local option" can be shown never to hurt the global solution, use greedy. Otherwise, reach for DP.

### Proof Techniques (The SDE-3 Requirement)
Interviewers for Staff/Senior roles often ask: "How do you *know* greedy works here?"

1. **Exchange Argument (The Gold Standard)**:
   - **Method**: Take an arbitrary optimal solution $O$. Suppose $O$ does *not* make the greedy choice at step 1. Show that you can swap the greedy choice into $O$ without making the solution worse.
   - **Example (Interval Scheduling)**: If $O$ picks an interval $x$ that doesn't end first, swap it for the earliest-ending interval $g$. Since $g$ ends earlier than $x$, it cannot possibly overlap with any future intervals in $O$. Thus, $O$ remains valid and optimal.

2. **Greedy Stays Ahead**:
   - **Method**: Define a measure of progress. Show that at every step $k$, the greedy solution is at least as "far along" as any other partial solution.
   - **Example (Jump Game)**: At step $i$, the greedy "farthest reachable" is always $\ge$ any other choice's reach.

3. **Matroids (Formal Logic)**:
   - If a problem's constraints form a Matroid structure (like Kruskal's for MST), greedy is mathematically guaranteed to find the global optimum.

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

#### Common Variants & Twists
1. **Video Stitching**:
   - **What (The Problem & Goal):** Given a set of clips and a time `T`, find the minimum number of clips to cover the entire range `[0, T]`.
   - **How (Intuition & Mental Model):** Sort clips by start time. At each step, choose the clip that starts within the current covered range but extends the `farthest`. This is a greedy extension approach similar to Jump Game.
2. **Minimum Number of Taps to Open to Water a Garden**:
   - **What (The Problem & Goal):** Each tap waters a range `[i - ranges[i], i + ranges[i]]`. Find the minimum taps to water the garden `[0, n]`.
   - **How (Intuition & Mental Model):** Convert each tap into an interval `[start, end]`. Then the problem is identical to Video Stitching: find the minimum intervals to cover the range `[0, n]`.
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

#### Common Variants & Twists
1. **Jump Game III**:
   - **What (The Problem & Goal):** You can jump to `i + arr[i]` or `i - arr[i]`. Can you reach any index with value 0?
   - **How (Intuition & Mental Model):** This is actually a reachability problem on a graph. Use BFS or DFS starting from the given index.
2. **Jump Game VII**:
   - **What (The Problem & Goal):** You can jump from `i` to `j` if `i + minJump <= j <= min(i + maxJump, s.length - 1)` and `s[j] == '0'`.
   - **How (Intuition & Mental Model):** Use a sliding window + DP approach. Keep track of how many indices in the current reachable window `[i - maxJump, i - minJump]` are themselves reachable. If the count > 0 and `s[i] == '0'`, then `i` is reachable.
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

#### Common Variants & Twists
1. **Gas Station II (Multiple valid starts)**:
   - **What (The Problem & Goal):** If there are multiple valid starting points, find the one with the minimum index.
   - **How (Intuition & Mental Model):** The standard algorithm already finds the first possible start point after the "last" deficit. Because of the circular nature and the `sum(gas) >= sum(cost)` condition, the greedy logic naturally points to the start of the first sequence that can complete the loop.
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

#### Common Variants & Twists
1. **Reorganize String**:
   - **What (The Problem & Goal):** Rearrange characters in a string so that no two identical characters are adjacent.
   - **How (Intuition & Mental Model):** Greedily place the most frequent characters first. Use a Max-Heap to always pick the character with the highest remaining frequency. To avoid placing the same character twice, "wait" for one step before pushing the used character back into the heap.
2. **Distant Barcodes**:
   - **What (The Problem & Goal):** Rearrange barcodes so that no two adjacent barcodes are the same.
   - **How (Intuition & Mental Model):** Identical to Reorganize String. Max-Heap + "wait" one step.
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

#### Common Variants & Twists
1. **Trapping Rain Water**:
   - **What (The Problem & Goal):** Calculate how much water a terrain can trap after rain.
   - **How (Intuition & Mental Model):** Similar to the two-pass greedy in Candy. For each bar, the water level is `min(max_left, max_right) - height`. Precompute `max_left` and `max_right` using two passes.
2. **Greatest Common Divisor of Strings**:
   - **What (The Problem & Goal):** Find the largest string `x` such that `x` divides both `str1` and `str2`.
   - **How (Intuition & Mental Model):** Use the Euclidean algorithm logic. If `str1 + str2 == str2 + str1`, then a GCD string exists and its length is `gcd(len(str1), len(str2))`.
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

#### Common Variants & Twists
1. **Merge Intervals**:
   - **What (The Problem & Goal):** Merge all overlapping intervals.
   - **How (Intuition & Mental Model):** Sort by start time. Iterate and maintain a `current_interval`. If the next interval starts before `current_interval.end`, extend `current_interval.end` to `max(current_end, next_end)`. Otherwise, push the current interval and start a new one.
2. **Minimum Number of Groups to Create Non-overlapping Intervals**:
   - **What (The Problem & Goal):** Divide intervals into the minimum number of groups such that intervals in each group don't overlap.
   - **How (Intuition & Mental Model):** This is equivalent to finding the maximum number of overlapping intervals at any point in time (the "width" of the intervals). Use a min-priority queue of end times. For each interval, if it starts after the earliest end time in the heap, reuse that "group". Otherwise, start a new group.
```

---

### Priority Queue Greedy — Maximize Capital (IPO)

> [!IMPORTANT]
> **The Click Moment**: "Maximize profit by choosing K items, where items **unlock** based on current capacity" — OR — "dynamically changing pool of valid choices". Use two data structures: a sorted array (or min-heap) for locked items sorted by cost, and a max-heap for the profits of currently unlocked items.

```python
import heapq

def find_maximized_capital(k: int, w: int, profits: list[int], capital: list[int]) -> int:
    # Min-heap of projects by capital required
    projects = list(zip(capital, profits))
    projects.sort()  # Sort by capital ascending
    
    max_heap = []
    i = 0
    n = len(projects)
    
    for _ in range(k):
        # Unlock all projects we can afford with current capital 'w'
        while i < n and projects[i][0] <= w:
            heapq.heappush(max_heap, -projects[i][1])  # Max-heap for profits
            i += 1
            
        if not max_heap:
            break  # Can't afford any more projects
            
        # Greedily pick the most profitable unlocked project
        w += -heapq.heappop(max_heap)
        
    return w

#### Common Variants & Twists
1. **Minimum Cost to Connect Sticks**:
   - **What (The Problem & Goal):** You have sticks of different lengths. You can connect two sticks of lengths `x` and `y` with cost `x + y`. Find the minimum total cost to connect all sticks.
   - **How (Intuition & Mental Model):** This is Huffman Coding. To minimize cost, you always want to merge the two smallest sticks available. Use a min-heap to always pop the two smallest, merge them, and push the result back until only one stick remains.
2. **Minimize Deviation in Array**:
   - **What (The Problem & Goal):** Perform operations (multiply odd by 2, divide even by 2) to minimize the difference between max and min elements in an array.
   - **How (Intuition & Mental Model):** First, make all numbers as large as possible (multiply odd by 2). Put all numbers into a max-heap. Track the current minimum. Repeatedly pop the max, update the result (`max - min`), divide the max by 2 (if even), and update the minimum. Stop when the max is odd.
```

> [!TIP]
> This "Two-Heap/Sorted + Heap" pattern is the gold standard for dynamic greedy algorithms. Sorting handles the unlocking condition (cost), and the max-heap handles the greedy selection (profit).

---

## 3. SDE-3 Deep Dives

### When Greedy Fails: DP is Needed

> [!TIP]
> Imagine cutting a cake into slices to maximize the number of pieces. Greedily taking the largest slice first can leave you with awkward remainders that cannot be divided further — you would have gotten more pieces by taking medium slices in a specific order. This is the coin change failure: `[1, 3, 4]` to make 6 — greedily taking 4 leaves `1+1` (3 coins total), but `3+3` (2 coins) is better. The greedy choice blocked the optimal combination.

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
- [Jump Game II](problem-deep-dives.md#jump-game-ii) — Greedy BFS levels; O(N).
- [Non-overlapping Intervals](problem-deep-dives.md#non-overlapping-intervals) — Sort by end; keep non-overlapping.
- **Meeting Rooms II** — Min-heap of end times; active room count = heap size.
- [Gas Station](problem-deep-dives.md#gas-station) — Running tank; reset start on deficit.
- [Task Scheduler](problem-deep-dives.md#task-scheduler) — Formula or heap simulation.
- **Partition Labels** — Last occurrence map; sweep and cut.
- **Candy** — Two-pass: left-right then right-left.
- **Minimum Arrows to Burst Balloons** — Sort by end; shoot at end of each new balloon.

### Hard
- **Minimum Refueling Stops** — Max-heap of reachable fuel; refuel largest when tank runs dry.
- **IPO (Maximize Capital)** — Sort by capital; max-heap of available profits.
- **Smallest Range Covering K Lists** — K-way merge + greedy window shrink.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **Jump Game I** | Greedy Reach Tracking | "Can you reach the end?" | Track `farthest`; if `i > farthest` → False | O(N) — not DP. Greedy works because reaching farther never hurts. |
| **[Jump Game II](problem-deep-dives.md#jump-game-ii)** | "Minimum jumps to end" | Greedy BFS: jump to `farthest` when `i == current_end` | Increment jumps at `current_end`, not when pushing `farthest`. Off-by-one on final step. |
| **[Non-overlapping Intervals](problem-deep-dives.md#non-overlapping-intervals)** | "Remove minimum to make non-overlapping" | Sort by end; keep non-overlapping; count removed | Sort by **end** (not start). Max non-overlapping = n - removed. |
| **Min Arrows to Burst Balloons** | "Minimum shots to pop all balloons" | Sort by end; new arrow only if `start > arrow_pos` | `>` not `>=` — touching boundary is one shot. |
| **[Gas Station](problem-deep-dives.md#gas-station)** | "Starting point for circular traversal" | Reset `start` when tank goes negative | Uniqueness: valid start exists iff `sum(gas) >= sum(cost)`. |
| **[Task Scheduler](problem-deep-dives.md#task-scheduler)** | "Minimum time with cooldown n" | `(max_f-1)*(n+1) + count_max`, cap at `len(tasks)` | The cap handles "enough variety to fill idle slots" — don't forget `max(formula, len(tasks))`. |
| **Assign Cookies** | "Satisfy max children greedily" | Sort both; smallest sufficient cookie per smallest unsatisfied child | Two-pointer: greedily match smallest satisfied first. |
| **Candy** | "Minimum candy with neighbor constraints" | Two-pass: L→R then R→L; `candy[i] = max(both passes)` | One pass fails — left and right constraints are independent. |
| **Fractional Knapsack** | "Max value with fractional items" | Sort by value/weight; take greedily | 0/1 Knapsack is **not** greedy — needs DP. Verify items are divisible. |
| **Minimum Refueling Stops** | "Fewest stops to reach destination" | Max-heap of reachable stations; refuel when tank < 0 | Greedily take the largest available fuel when you must stop — not the nearest. |
| **Partition Labels** | "Partition so each letter in one part" | `last[ch]` map; extend `end`; cut at `i == end` | Each letter's last occurrence defines the minimum partition end. |
| **Lemonade Change** [E] | "Can you give correct change for each customer?" | Greedy: prefer using $10 over $5 when making $15 change | Use $10 before $5 to preserve smaller bills for future $5 change needs. |
| **Score After Flipping Matrix** [M] | "Maximize sum of rows as binary numbers" | First: toggle row if first bit is 0 (MSB dominates); then: toggle column if zeros > ones | MSB of each row must be 1 first; then maximize each column independently. |
| **Two City Scheduling** [M] | "Send N people to each of 2 cities at min cost" | Sort by `cost_A - cost_B`; first N go to A, rest to B | Sorting by cost difference selects people with greatest relative saving for each city. |
| **Boats to Save People** [M] | "Min boats where each holds ≤ 2 people, total ≤ limit" | Sort; two pointers (lightest + heaviest); if sum ≤ limit pair them | Greedy: always try to pair the heaviest with the lightest; if impossible, heaviest goes alone. |
| **Minimum Number of Arrows** [M] | "Min arrows to burst all balloons" | Sort by end; arrow at `end`; advance to next balloon not reached | Identical to "non-overlapping intervals" — one arrow can burst multiple overlapping balloons. |
| **Queue Reconstruction by Height** [M] | "Reconstruct queue from (h, k) pairs" | Sort by height desc (ties: k asc); insert each person at index k | Taller people are placed first; inserting at `k` is valid since all remaining are shorter or equal. |
| **Car Pooling** [M] | "Can car with capacity C handle all trips?" | Difference array on stops; scan prefix sums | Or: sort events by position; track running passenger count. |
| **Wiggle Subsequence** [M] | "Longest alternating up-down subsequence" | Greedy: count peaks and valleys; every direction change is a peak/valley | No need to track indices — just count alternating slopes. DP O(N²) exists but greedy is O(N). |
| **Maximum Units on a Truck** [E] | "Greedy: load boxes with most units first" | Sort by units per box desc; load until capacity | Straightforward greedy; just don't forget to clamp last batch to remaining capacity. |
| **Minimum Cost to Connect Sticks** [M] | "Merge sticks: cost = sum of two merged; minimize total" | Min-heap; always merge two smallest; push result back | Equivalent to Huffman encoding — merging smallest first minimizes total cost. |
| **IPO (Maximize Capital)** [H] | "Pick K projects to maximize capital; project unlocks at capital threshold" | Sort by capital; max-heap of profits of unlocked projects | Unlock projects incrementally as capital grows; always pick highest-profit unlocked project. |

---

## Quick Revision Triggers

- "Always pick the locally best option (largest profit, earliest deadline, minimum cost)" → greedy; verify exchange argument before coding.
- "Interval scheduling: maximize non-overlapping intervals" → sort by end time; greedily pick earliest-ending.
- "Interval merging / covering" → sort by start time; merge overlapping or count gaps.
- "Coin change with standard denominations" → greedy works; arbitrary denominations → DP.
- "Problem asks for minimum number of 'things' to cover / jump / satisfy all constraints" → greedy scan left to right, extend reach.
- "Sort by ratio or combined key (profit/weight, deadline−duration)" → greedy on sorted order.
- "Greedy fails on a small counterexample" → switch to DP immediately.

---

## See also

- [Patterns Master](../../../reference/patterns/patterns-master.md) — greedy pattern triggers

---

## 🎙️ The Coach's Dialogue: Mastering the "Greedy" Mindset

**Student:** "Coach, I'm always scared to use Greedy. I feel like I'm taking a gamble that might fail on a weird edge case. How do I *know* it's greedy?"

**Coach:** "That fear is healthy. Most 'Greedy' problems are actually DP problems in disguise if you get the sorting or the choice wrong. The secret isn't in the code—it's in the **Sorting Key**. If I ask you to schedule the most meetings, and you sort by *start time*, you'll fail. Why?"

**Student:** "Because a meeting starting at 8 AM might last until 5 PM and block everything else?"

**Coach:** "Exactly! So you sort by *end time* to stay as 'available' as possible. That's the **Aha! Moment**. In an interview, if you're thinking Greedy, ask yourself: 'Does taking the absolute best option right now ever prevent me from taking an even better combination later?' If the answer is 'maybe,' it’s probably DP."

**Student:** "What about the 'Jump Game'? It feels like I should check every path."

**Coach:** "You could, but that's O(2^N) or O(N²) with DP. The Greedy insight is: if you can reach index 10, you can *definitely* reach everything before 10. So you don't care *how* you got to 10, you only care about the farthest point you can see from there. It’s like driving at night with high beams—you only care about the farthest point the light hits."

**Student:** "What's the one 'Gotcha' that trips up SDE-3 candidates?"

**Coach:** "The **Overlap Boundary**. In 'Minimum Arrows to Burst Balloons,' if two balloons touch at `x=5`, one arrow pops both. In 'Non-overlapping Intervals,' if they touch at `x=5`, they *don't* overlap. Interviewers will watch your `>` vs `>=` like a hawk. One character difference is the gap between a Senior and a Junior hire."
