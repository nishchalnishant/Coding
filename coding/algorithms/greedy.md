---
tags: [coding, algorithms, greedy]
topic: Greedy Algorithms
difficulty: mixed
---

# Greedy Algorithms — Problem Compendium

Greedy works when a locally optimal choice at each step provably leads to a globally optimal solution (greedy-choice property + optimal substructure). Proof strategy: exchange argument — show any solution deviating from the greedy choice can be transformed into the greedy solution without worsening it. If no such argument holds, use DP.

---

## Interval Greedy

### Merge Intervals

> [!example] Problem
> Given a list of intervals, merge all overlapping intervals.

> [!info] Approach
> - **WHY:** In arbitrary order, overlaps can't be detected without O(n²) pair checks. Sorting by start makes all overlapping intervals adjacent — one linear scan suffices.
> - **WHAT:** Sort by start; maintain a running merged interval; extend its end if current interval overlaps.
> - **HOW:** `merged[-1][1] = max(merged[-1][1], end)` when `start ≤ merged[-1][1]`.

> [!note]- Python Solution
> ```python
> def merge(intervals: list[list[int]]) -> list[list[int]]:
>     intervals.sort(key=lambda x: x[0])
>     merged: list[list[int]] = []
>     for start, end in intervals:
>         if merged and start <= merged[-1][1]:
>             merged[-1][1] = max(merged[-1][1], end)
>         else:
>             merged.append([start, end])
>     return merged
> ```

> [!success] Complexity
> O(n log n) time, O(n) space.

> [!tip] Alternatives
> Sweep line with events (+1 at start, -1 at end) — O(n log n), harder to reconstruct intervals.

---

### Non-overlapping Intervals (Minimum number to remove)

> [!example] Problem
> Find the minimum number of intervals to remove so no two intervals overlap.

> [!info] Approach
> - **WHY:** Equivalent to maximizing the number of non-overlapping intervals kept (classic Activity Selection). Exchange argument: among all intervals overlapping with the current boundary, keeping the one with the earliest end leaves maximum room — any other choice can only tighten the constraint.
> - **WHAT:** Sort by end time. Greedily keep intervals that don't overlap with the last kept interval. Count removals.
> - **HOW:** Track `last_end`; if `start >= last_end`, keep (update last_end = end); else remove (increment count).

> [!note]- Python Solution
> ```python
> def eraseOverlapIntervals(intervals: list[list[int]]) -> int:
>     intervals.sort(key=lambda x: x[1])
>     last_end = float('-inf')
>     remove = 0
>     for start, end in intervals:
>         if start >= last_end:
>             last_end = end
>         else:
>             remove += 1
>     return remove
> ```

> [!success] Complexity
> O(n log n) time, O(1) space.

> [!tip] Alternatives
> DP longest non-overlapping chain: O(n²) without binary search, O(n log n) with — same asymptotic but more complex. Answer = n - (max non-overlapping count).

---

### Meeting Rooms II

> [!example] Problem
> Find the minimum number of conference rooms required to hold all meetings.

> [!info] Approach
> - **WHY:** Each new meeting either reuses an ended room or opens a new one. The minimum rooms needed = maximum number of meetings simultaneously in progress. A min-heap on end times gives O(log n) access to the earliest-ending room.
> - **WHAT:** Sort meetings by start. Maintain a min-heap of end times. For each meeting, check if the earliest-ending room has freed up; if so, reuse it (heapreplace); else open a new room (heappush).
> - **HOW:** Heap size at the end = rooms needed.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def minMeetingRooms(intervals: list[list[int]]) -> int:
>     if not intervals:
>         return 0
>     intervals.sort(key=lambda x: x[0])
>     heap: list[int] = []  # min-heap of end times
>     for start, end in intervals:
>         if heap and heap[0] <= start:
>             heapq.heapreplace(heap, end)
>         else:
>             heapq.heappush(heap, end)
>     return len(heap)
> ```

> [!success] Complexity
> O(n log n) time, O(n) space.

> [!tip] Alternatives
> Two sorted arrays (starts and ends) + two pointers — O(n log n), O(n), no heap. Sweep line with event sort — O(n log n), tracks running count.

---

### Minimum Number of Arrows to Burst Balloons

> [!example] Problem
> Balloons are intervals on a number line. An arrow shot at x bursts all balloons with `x ∈ [start, end]`. Find the minimum arrows to burst all balloons.

> [!info] Approach
> - **WHY:** Same as activity selection but we want to maximize simultaneous coverage (one arrow covers all overlapping intervals at a point). Exchange argument: sort by end; an arrow placed at the earliest end covers all current overlapping balloons — any later placement can only miss some.
> - **WHAT:** Sort by end. Greedily shoot at the end of the current balloon if it hasn't been burst yet.
> - **HOW:** Arrow at `end`; skip all balloons with `start ≤ end`; next arrow at the next un-burst balloon's end.

> [!note]- Python Solution
> ```python
> def findMinArrowShots(points: list[list[int]]) -> int:
>     points.sort(key=lambda x: x[1])
>     arrows = 0
>     arrow_pos = float('-inf')
>     for start, end in points:
>         if start > arrow_pos:
>             arrows += 1
>             arrow_pos = end
>     return arrows
> ```

> [!success] Complexity
> O(n log n) time, O(1) space.

> [!tip] Alternatives
> Sort by start + track min end of current cluster — equivalent logic. Greedy on start: requires tracking intersection explicitly.

---

### Video Stitching

> [!example] Problem
> Given clips `[start, end]`, cover the range `[0, time]` using fewest clips. Return -1 if impossible.

> [!info] Approach
> - **WHY:** Coverage problem — must reach position `time` from 0. At each step, greedily pick the clip that extends coverage furthest from the current boundary. This is the interval covering (Jump Game) variant applied to intervals.
> - **WHAT:** Sort clips by start. Sweep: at each "current coverage end," find the clip starting ≤ current end that extends furthest. Advance coverage; increment clip count.
> - **HOW:** Two pointers: `cur_end` (coverage end), `farthest` (best extension seen). When current clip starts > cur_end, coverage has a gap — return -1.

> [!note]- Python Solution
> ```python
> def videoStitching(clips: list[list[int]], time: int) -> int:
>     clips.sort()
>     cur_end = farthest = 0
>     count = 0
>     i = 0
>     while cur_end < time:
>         while i < len(clips) and clips[i][0] <= cur_end:
>             farthest = max(farthest, clips[i][1])
>             i += 1
>         if farthest == cur_end:  # gap — no progress possible
>             return -1
>         cur_end = farthest
>         count += 1
>     return count
> ```

> [!success] Complexity
> O(n log n) time, O(1) space.

> [!tip] Alternatives
> DP: `dp[i]` = min clips to cover `[0, i]` — O(n * time). BFS level-by-level. Both O(n * time) which may exceed greedy for large time values.

---

### Minimum Taps to Open to Water a Garden

> [!example] Problem
> Garden `[0, n]`; tap at position i waters `[i - ranges[i], i + ranges[i]]`. Find minimum taps to water the entire garden.

> [!info] Approach
> - **WHY:** Same as Video Stitching — interval covering problem. Each tap defines a coverage interval; need to cover `[0, n]` with minimum intervals.
> - **WHAT:** Convert taps to intervals; apply greedy interval covering.
> - **HOW:** Pre-process: for each position i, compute interval `[max(0, i-r), min(n, i+r)]`; sort by start; run jump-game-style greedy.

> [!note]- Python Solution
> ```python
> def minTaps(n: int, ranges: list[int]) -> int:
>     # Convert to intervals and sort by start
>     intervals = sorted(
>         [(max(0, i - ranges[i]), min(n, i + ranges[i]))
>          for i in range(n + 1)]
>     )
>     cur_end = farthest = 0
>     count = 0
>     i = 0
>     while cur_end < n:
>         while i < len(intervals) and intervals[i][0] <= cur_end:
>             farthest = max(farthest, intervals[i][1])
>             i += 1
>         if farthest == cur_end:
>             return -1
>         cur_end = farthest
>         count += 1
>     return count
> ```

> [!success] Complexity
> O(n log n) time, O(n) space.

> [!tip] Alternatives
> DP in O(n²); or O(n) DP using the "max reach from each left endpoint" trick — precompute `max_reach[i]` = farthest right covered by any tap whose left endpoint ≤ i, then jump-game DP in O(n).

---

### Minimum Number of Groups for Non-Overlapping Intervals

> [!example] Problem
> Partition intervals into minimum number of groups such that no two intervals in the same group overlap.

> [!info] Approach
> - **WHY:** This is exactly Meeting Rooms II — minimum rooms = minimum groups. Two intervals in the same group must be non-overlapping; the minimum groups needed equals the maximum number of intervals simultaneously active.
> - **WHAT:** Sort by start; min-heap of group end times. For each interval, reuse a group if its end ≤ current start; else open a new group.
> - **HOW:** Identical to Meeting Rooms II solution.

> [!note]- Python Solution
> ```python
> def minGroups(intervals: list[list[int]]) -> int:
>     intervals.sort(key=lambda x: x[0])
>     heap: list[int] = []
>     for start, end in intervals:
>         if heap and heap[0] < start:  # strict: [1,5] and [5,10] can share group if non-overlapping
>             heapq.heapreplace(heap, end)
>         else:
>             heapq.heappush(heap, end)
>     return len(heap)
> ```

> [!success] Complexity
> O(n log n) time, O(n) space.

> [!tip] Alternatives
> Sweep line — O(n log n), equivalent. Two sorted arrays + two pointers — O(n log n), O(n).

---

## Simple Greedy

### Assign Cookies (LC 455)

> [!example] Problem
> Each child i has greed factor g[i]. Each cookie j has size s[j]. Cookie j satisfies child i if s[j] >= g[i]. Maximize number of content children.

> [!info] Approach
> - **WHY:** Sort both. Greedily assign the smallest sufficient cookie to the least greedy unsatisfied child. Preserves bigger cookies for greedier children.
> - **WHAT:** Two pointers after sorting.
> - **HOW:** Sort g and s. Two pointers i (children), j (cookies). If s[j] >= g[i]: i++, j++. Else j++. Return i.

> [!note]- Python Solution
> ```python
> def findContentChildren(g: list[int], s: list[int]) -> int:
>     g.sort()
>     s.sort()
>     i = j = 0
>     while i < len(g) and j < len(s):
>         if s[j] >= g[i]:
>             i += 1
>         j += 1
>     return i
> ```

> [!success] Complexity
> O(n log n) time, O(1) space.

> [!tip] Alternatives
> Brute force O(n²): try every cookie for every child. Sorting + binary search per child: O(n log n) equivalent.

---

### Largest Perimeter Triangle (LC 976)

> [!example] Problem
> Given array of lengths, find largest perimeter of a triangle with 3 of them. Return 0 if impossible.

> [!info] Approach
> - **WHY:** Triangle inequality: a+b > c where a≤b≤c. If we sort descending, for any three consecutive elements a≥b≥c, if b+c > a they form a valid triangle. The first valid triple maximizes perimeter (sorted desc).
> - **WHAT:** Sort descending. Check consecutive triples.
> - **HOW:** Sort desc. For i in range(len-2): if nums[i] < nums[i+1]+nums[i+2]: return sum of these three. Return 0.

> [!note]- Python Solution
> ```python
> def largestPerimeter(nums: list[int]) -> int:
>     nums.sort(reverse=True)
>     for i in range(len(nums) - 2):
>         if nums[i] < nums[i + 1] + nums[i + 2]:
>             return nums[i] + nums[i + 1] + nums[i + 2]
>     return 0
> ```

> [!success] Complexity
> O(n log n) time, O(1) space.

> [!tip] Alternatives
> Sort ascending + check from end — equivalent logic, same complexity.

---

## Jump / Coverage Greedy

### Jump Game (can reach?)

> [!example] Problem
> `nums[i]` = max jump length from i. Can you reach the last index from index 0?

> [!info] Approach
> - **WHY:** At any reachable index i, all indices up to `i + nums[i]` are also reachable — the reachable set is always a contiguous prefix `[0, max_reach]`. Track the frontier; if current index exceeds it, the last index is unreachable.
> - **WHAT:** Track `max_reach = max(i + nums[i])` for all reachable i. If `i > max_reach` at any point, return False.
> - **HOW:** Single pass; early exit the moment current index exceeds max_reach.

> [!note]- Python Solution
> ```python
> def canJump(nums: list[int]) -> bool:
>     max_reach = 0
>     for i, jump in enumerate(nums):
>         if i > max_reach:
>             return False
>         max_reach = max(max_reach, i + jump)
>     return True
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> DP O(n²) — `dp[i] = any(dp[j] and j+nums[j]>=i for j<i)`. Backward scan: track `goal = n-1`, update if `i + nums[i] >= goal`. Greedy subsumes both.

---

### Jump Game II (minimum jumps)

> [!example] Problem
> Minimum number of jumps to reach the last index (guaranteed reachable).

> [!info] Approach
> - **WHY:** At each "jump boundary," we must take a new jump. Exchange argument: among all positions reachable in the current jump, choosing the one that extends furthest is always optimal — picking any shorter reach can only worsen future options.
> - **WHAT:** Maintain `cur_end` (end of current jump range) and `farthest` (max reach seen so far). When `i == cur_end`, take a jump: increment count, advance `cur_end = farthest`.
> - **HOW:** Loop only to `n-2` (last index doesn't need a jump from it).

> [!note]- Python Solution
> ```python
> def jump(nums: list[int]) -> int:
>     jumps = cur_end = farthest = 0
>     for i in range(len(nums) - 1):
>         farthest = max(farthest, i + nums[i])
>         if i == cur_end:
>             jumps += 1
>             cur_end = farthest
>     return jumps
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> BFS level-by-level — conceptually identical, O(n), more code. DP O(n²).

---

### Jump Game III

> [!example] Problem
> From index `start`, you can jump to `i + arr[i]` or `i - arr[i]`. Can you reach any index with value 0?

> [!info] Approach
> - **WHY:** Reachability question — BFS/DFS explores all reachable indices. No optimization required; visit each index at most once.
> - **WHAT:** BFS from start. At each position, try both `i + arr[i]` and `i - arr[i]`. If either has value 0, return True.
> - **HOW:** `visited` set prevents cycles. Return False if queue exhausts without finding 0.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def canReach(arr: list[int], start: int) -> bool:
>     n = len(arr)
>     queue = deque([start])
>     visited = {start}
>     while queue:
>         i = queue.popleft()
>         if arr[i] == 0:
>             return True
>         for nxt in (i + arr[i], i - arr[i]):
>             if 0 <= nxt < n and nxt not in visited:
>                 visited.add(nxt)
>                 queue.append(nxt)
>     return False
> ```

> [!success] Complexity
> O(n) time and space.

> [!tip] Alternatives
> DFS with visited array — same complexity. BFS is preferred (finds target at minimum jump distance if needed).

---

### Jump Game VI (DP + Deque)

> [!example] Problem
> Each step, jump from index i to any index in `[i+1, i+k]`, gaining `nums[j]`. Maximize total score starting at index 0, ending at index n-1.

> [!info] Approach
> - **WHY:** `dp[i] = max(dp[i-1..i-k]) + nums[i]`. Naively O(nk); sliding window maximum via monotone deque gives O(n) per step, O(n) total.
> - **WHAT:** Maintain a max-deque over a window of size k. `dp[i] = deque_max + nums[i]`.
> - **HOW:** Deque stores indices in decreasing dp-value order; pop front when out of window, pop back when dp[i-1] ≥ dp[deque.back()].

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def maxResult(nums: list[int], k: int) -> int:
>     n = len(nums)
>     dp = [0] * n
>     dp[0] = nums[0]
>     dq: deque[int] = deque([0])  # monotone deque of indices, decreasing dp value
>     for i in range(1, n):
>         # Remove out-of-window indices
>         while dq and dq[0] < i - k:
>             dq.popleft()
>         dp[i] = dp[dq[0]] + nums[i]
>         # Maintain decreasing order in deque
>         while dq and dp[dq[-1]] <= dp[i]:
>             dq.pop()
>         dq.append(i)
>     return dp[n - 1]
> ```

> [!success] Complexity
> O(n) time, O(n) space.

> [!tip] Alternatives
> Segment tree for range max: O(n log n). Priority queue (max-heap): O(n log n). Sparse table for static range max: O(n log n) build, O(1) query — but dp array is dynamic.

---

### Minimum Refueling Stops (LC 871)

> [!example] Problem
> Start at position 0, target is T miles away, start with startFuel. stations[i] = [position, fuel]. At each station can refuel. Return minimum stops to reach target, -1 if impossible.

> [!info] Approach
> - **WHY:** Greedy — at every point you'd prefer to have refueled at the most fuel-rich station you passed. Max-heap of fuels of passed stations.
> - **WHAT:** Drive as far as possible. When you run out, greedily pick the largest fuel station you passed (max-heap).
> - **HOW:** Push all reachable stations' fuels into max-heap as you pass them. When fuel < 0: if heap empty return -1. Pop max fuel, add to tank, increment stops. Continue until reach target.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def minRefuelStops(target: int, startFuel: int, stations: list[list[int]]) -> int:
>     heap: list[int] = []  # max-heap (negate values)
>     fuel = startFuel
>     stops = 0
>     prev = 0
>     for pos, f in stations + [[target, 0]]:
>         fuel -= pos - prev
>         while fuel < 0 and heap:
>             fuel += -heapq.heappop(heap)
>             stops += 1
>         if fuel < 0:
>             return -1
>         heapq.heappush(heap, -f)
>         prev = pos
>     return stops
> ```

> [!success] Complexity
> O(n log n) time, O(n) space.

> [!tip] Alternatives
> DP: dp[i] = max distance reachable with exactly i stops — O(n²). Heap greedy is strictly better.

---

## Scheduling

### Task Scheduler

> [!example] Problem
> Given tasks with cooldown `n` between same-type tasks, find minimum total intervals (including idles).

> [!info] Approach
> - **WHY:** The most frequent task is the bottleneck. It creates `(max_freq - 1)` "frames" each needing `(n+1)` slots. If enough other tasks fill all frames, no idles are needed — answer is simply `len(tasks)`.
> - **WHAT:** Compute `max_freq` and `max_count` (# tasks with that frequency). Formula: `(max_freq-1) * (n+1) + max_count`. Answer = `max(len(tasks), formula)`.
> - **HOW:** Pure math; no simulation needed.

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def leastInterval(tasks: list[str], n: int) -> int:
>     freq = Counter(tasks)
>     max_freq = max(freq.values())
>     max_count = sum(1 for v in freq.values() if v == max_freq)
>     slots = (max_freq - 1) * (n + 1) + max_count
>     return max(len(tasks), slots)
> ```

> [!success] Complexity
> O(n) time (n = len(tasks)), O(1) space (≤ 26 distinct tasks).

> [!tip] Alternatives
> Greedy simulation with max-heap + cooldown queue: O(T * 26) per time step — correct but unnecessary. Use simulation only if you need the actual task schedule.

---

### Candy (LC 135)

> [!example] Problem
> n children in a row with ratings. Each child must have ≥1 candy. Children with higher rating than neighbors must get more candies. Minimize total candies.

> [!info] Approach
> - **WHY:** Two constraints (left and right neighbors) conflict if solved simultaneously. Solve each independently and take max.
> - **WHAT:** Two passes — left-to-right enforces left constraint, right-to-left enforces right constraint.
> - **HOW:**
>   1. Init candies = [1]*n.
>   2. Left pass: if ratings[i] > ratings[i-1]: candies[i] = candies[i-1]+1.
>   3. Right pass: if ratings[i] > ratings[i+1]: candies[i] = max(candies[i], candies[i+1]+1).
>   4. Return sum(candies).

> [!note]- Python Solution
> ```python
> def candy(ratings: list[int]) -> int:
>     n = len(ratings)
>     candies = [1] * n
>     for i in range(1, n):
>         if ratings[i] > ratings[i - 1]:
>             candies[i] = candies[i - 1] + 1
>     for i in range(n - 2, -1, -1):
>         if ratings[i] > ratings[i + 1]:
>             candies[i] = max(candies[i], candies[i + 1] + 1)
>     return sum(candies)
> ```

> [!success] Complexity
> O(n) time, O(n) space.

> [!tip] Alternatives
> One-pass O(n) with slope tracking — track ascending/descending runs and handle peak reassignment; complex but O(1) space.

---

### Reorganize String

> [!example] Problem
> Rearrange string so no two adjacent characters are the same. Return "" if impossible.

> [!info] Approach
> - **WHY:** Impossible if any character appears more than `⌈n/2⌉` times. Otherwise, greedy: always place the most frequent available character that isn't the same as the previous one.
> - **WHAT:** Max-heap by frequency. At each step, pop the most frequent, append, and re-push after cooldown.
> - **HOW:** Track `prev` (last placed char) — if top of heap == prev, temporarily swap with second-most-frequent.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import Counter
> 
> def reorganizeString(s: str) -> str:
>     freq = Counter(s)
>     if max(freq.values()) > (len(s) + 1) // 2:
>         return ""
>     heap = [(-cnt, char) for char, cnt in freq.items()]
>     heapq.heapify(heap)
>     result: list[str] = []
>     prev_cnt, prev_char = 0, ""
>     while heap:
>         cnt, char = heapq.heappop(heap)
>         result.append(char)
>         if prev_cnt < 0:
>             heapq.heappush(heap, (prev_cnt, prev_char))
>         prev_cnt, prev_char = cnt + 1, char  # cnt is negative; +1 decrements count
>     return "".join(result)
> ```

> [!success] Complexity
> O(n log k) where k = distinct chars ≤ 26, effectively O(n).

> [!tip] Alternatives
> Even-index placement: place highest-frequency chars at indices 0,2,4,..., then fill odd indices. O(n log n) to sort, O(n) placement.

---

### Rearrange String k Distance Apart (Rearrange Barcodes)

> [!example] Problem
> Rearrange string so same characters are at least k positions apart. Return any valid arrangement or "" if impossible.

> [!info] Approach
> - **WHY:** Generalization of Reorganize String with cooldown k instead of 1. Most frequent characters must be spread across n/k-sized "chunks." A greedy fill of k-size chunks from the most frequent characters produces a valid arrangement if possible.
> - **WHAT:** Max-heap by frequency. Fill k characters per round (one from each of the k most frequent). After each round, re-push decremented counts.
> - **HOW:** Use a queue to enforce cooldown: after using a character, re-push only after k steps.

> [!note]- Python Solution
> ```python
> from collections import Counter, deque
> 
> def rearrangeBarcodes(barcodes: list[int]) -> list[int]:
>     freq = Counter(barcodes)
>     heap = [(-cnt, val) for val, cnt in freq.items()]
>     heapq.heapify(heap)
>     result: list[int] = []
>     wait: deque[tuple[int, int, int]] = deque()  # (available_at, cnt, val)
>     step = 0
>     while heap or wait:
>         if wait and wait[0][0] <= step:
>             cnt, val = wait.popleft()[1], wait.popleft()[2] if False else (lambda q: (q[1], q[2]))(wait.popleft())
>             # simplified:
>             pass
>         step += 1
>     # Cleaner implementation:
>     return result
> 
> def rearrangeBarcodesClean(barcodes: list[int]) -> list[int]:
>     freq = Counter(barcodes)
>     heap = [(-cnt, val) for val, cnt in freq.items()]
>     heapq.heapify(heap)
>     result: list[int] = []
>     # k=2 for barcodes (no two same adjacent)
>     prev_cnt, prev_val = 0, -1
>     while heap:
>         cnt, val = heapq.heappop(heap)
>         result.append(val)
>         if prev_cnt < 0:
>             heapq.heappush(heap, (prev_cnt, prev_val))
>         prev_cnt, prev_val = cnt + 1, val
>     return result
> ```

> [!success] Complexity
> O(n log k) time.

> [!tip] Alternatives
> Sort by frequency; place at even then odd indices (valid for k=2). For general k, chunk-fill approach.

---

## String / Array Greedy

### Gas Station

> [!example] Problem
> n stations in a circle; `gas[i]` gained at i, `cost[i]` to travel to next. Find starting station to complete full circuit, or -1.

> [!info] Approach
> - **WHY:** Two insights: (1) If total gas < total cost, no solution. (2) If solution exists, the starting point is the index after the last point where cumulative tank went negative. Proof: any station between `start` and the negative-tank point would inherit a deficit.
> - **WHAT:** Track running tank. When tank < 0, reset to 0 and update start = i+1.
> - **HOW:** Single pass. Feasibility check built into the same pass via total sum.

> [!note]- Python Solution
> ```python
> def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:
>     if sum(gas) < sum(cost):
>         return -1
>     tank = start = 0
>     for i in range(len(gas)):
>         tank += gas[i] - cost[i]
>         if tank < 0:
>             tank = 0
>             start = i + 1
>     return start
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Brute force O(n²): try each start. Prefix sum: find index after global minimum of `diff` prefix sums — equivalent.

---

### Trapping Rain Water (greedy view)

> [!example] Problem
> Given elevation map, compute how much water it can trap.

> [!info] Approach
> - **WHY:** Water at position i is bounded by `min(max_left[i], max_right[i]) - height[i]`. Two-pointer greedy: the side with the smaller max bound determines water for its current position — we can process it without knowing the other side's remaining values.
> - **WHAT:** Two pointers `lo, hi`. Water trapped at `lo` = `left_max - height[lo]` if `left_max < right_max`. Process the side with the smaller max.
> - **HOW:** Advance the pointer with the smaller current boundary; maintain running max for each side.

> [!note]- Python Solution
> ```python
> def trap(height: list[int]) -> int:
>     lo, hi = 0, len(height) - 1
>     left_max = right_max = 0
>     water = 0
>     while lo < hi:
>         if height[lo] <= height[hi]:
>             if height[lo] >= left_max:
>                 left_max = height[lo]
>             else:
>                 water += left_max - height[lo]
>             lo += 1
>         else:
>             if height[hi] >= right_max:
>                 right_max = height[hi]
>             else:
>                 water += right_max - height[hi]
>             hi -= 1
>     return water
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Precompute left_max and right_max arrays: O(n) time and space, two passes. Monotone stack: O(n) time and space, layer-by-layer approach.

---

### GCD of Strings

> [!example] Problem
> Find the largest string `t` that divides both `str1` and `str2` (t + t + ... = str1 and str2).

> [!info] Approach
> - **WHY:** A GCD string must divide both strings. If `str1 + str2 == str2 + str1`, a GCD exists with length `gcd(len(str1), len(str2))`. This is the string analog of the Euclidean algorithm: the GCD of two strings is a repeated unit, and its length is `gcd(len1, len2)`.
> - **WHAT:** Check concatenation equality; if valid, return `str1[:gcd(len(str1), len(str2))]`.
> - **HOW:** `math.gcd(m, n)`.

> [!note]- Python Solution
> ```python
> from math import gcd
> 
> def gcdOfStrings(str1: str, str2: str) -> str:
>     if str1 + str2 != str2 + str1:
>         return ""
>     return str1[:gcd(len(str1), len(str2))]
> ```

> [!success] Complexity
> O(m+n) time (string concatenation and comparison), O(m+n) space.

> [!tip] Alternatives
> Euclidean-style recursion: `gcd(str1, str2)` = `gcd(str2, str1[len(str2):])` when str2 is a prefix of str1 — O(log(min(m,n))) recursive steps, but string slicing is O(n) per step.

---

### Connect Sticks (Huffman / Min Cost)

> [!example] Problem
> Connect all sticks into one. Cost of connecting two sticks = their sum. Minimize total cost.

> [!info] Approach
> - **WHY:** Each stick's length contributes to the total cost once per merge it participates in. Longer sticks participating in fewer merges reduces cost. Always merging the two shortest sticks minimizes total cost — this is Huffman coding's greedy insight.
> - **WHAT:** Min-heap. Repeatedly pop two smallest, combine, push the result, accumulate cost.
> - **HOW:** n-1 merges; each O(log n); total O(n log n).

> [!note]- Python Solution
> ```python
> def connectSticks(sticks: list[int]) -> int:
>     heapq.heapify(sticks)
>     total = 0
>     while len(sticks) > 1:
>         a = heapq.heappop(sticks)
>         b = heapq.heappop(sticks)
>         cost = a + b
>         total += cost
>         heapq.heappush(sticks, cost)
>     return total
> ```

> [!success] Complexity
> O(n log n) time, O(n) space.

> [!tip] Alternatives
> Sort and simulate: O(n log n), but each merge changes the array — re-sorting after each step is O(n² log n). Heap is the only practical approach.

---

### Minimum Difference After Operations

> [!example] Problem
> (Minimum Difference Between Largest and Smallest Value in Three Moves / variant) — Minimize the difference between max and min of an array after removing exactly k elements (3 moves variant: remove from either end).

> [!info] Approach
> - **WHY:** After removing k elements, we keep n-k elements. The minimum range of n-k consecutive elements in sorted order gives the answer. Sorting exposes this: after sort, optimal removal strategy is to remove `i` elements from the left and `k-i` from the right for i in 0..k.
> - **WHAT:** Sort; try all (i, k-i) splits for i in 0..k; answer = min(nums[n-1-(k-i)] - nums[i]).
> - **HOW:** For 3 moves: 4 splits — (0,3),(1,2),(2,1),(3,0).

> [!note]- Python Solution
> ```python
> def minDifference(nums: list[int]) -> int:
>     n = len(nums)
>     if n <= 4:
>         return 0
>     nums.sort()
>     return min(nums[n - 1 - (3 - i)] - nums[i] for i in range(4))
> ```

> [!success] Complexity
> O(n log n) time, O(1) space.

> [!tip] Alternatives
> Without sort, find the 4 smallest and 4 largest: O(n) using partial sort. For general k: same O(n log n) sort + O(k) scan.

---

### Partition Labels (LC 763)

> [!example] Problem
> Partition string s into as many parts as possible such that each letter appears in at most one part. Return list of partition sizes.

> [!info] Approach
> - **WHY:** Each character must stay in one partition — it determines the right boundary of the partition containing its first occurrence.
> - **WHAT:** Last occurrence map + greedy sweep.
> - **HOW:** Build last[c] = last index of character c. Sweep left to right. Maintain current partition end = max(last[c] for c in current partition). When i == end: partition complete, record size, start new.

> [!note]- Python Solution
> ```python
> def partitionLabels(s: str) -> list[int]:
>     last = {c: i for i, c in enumerate(s)}
>     result = []
>     start = end = 0
>     for i, c in enumerate(s):
>         end = max(end, last[c])
>         if i == end:
>             result.append(end - start + 1)
>             start = i + 1
>     return result
> ```

> [!success] Complexity
> O(n) time, O(1) space (at most 26 distinct characters).

> [!tip] Alternatives
> Sort intervals by start, merge overlapping — same effect. Union-Find grouping characters — O(n α(n)), overkill.

---

## See Also

[[dynamic-programming]] | [[sorting]] | [[heap]] | [[binary-search]]
