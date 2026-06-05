---
tags: [coding, algorithms, greedy]
topic: Greedy Algorithms
difficulty: mixed
---

# Greedy Algorithms — Problem Compendium

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: This file is core Tier 2 material. Know patterns cold; skip niche edge cases.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Conceptual awareness only.


Greedy works when a locally optimal choice at each step provably leads to a globally optimal solution (greedy-choice property + optimal substructure). Proof strategy: exchange argument — show any solution deviating from the greedy choice can be transformed into the greedy solution without worsening it. If no such argument holds, use DP.




---

## Interval Greedy

### Merge Intervals `🎯 T2`

> [!example] Problem
> Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.
> 
> **Example 1:**
> ```
> Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
> Output: [[1,6],[8,10],[15,18]]
> Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
> ```
> 
> **Example 2:**
> ```
> Input: intervals = [[1,4],[4,5]]
> Output: [[1,5]]
> Explanation: Intervals [1,4] and [4,5] are considered overlapping.
> ```
> 
> **Constraints:**
> - 1 <= intervals.length <= 10^4
> - intervals[i].length == 2
> - 0 <= starti <= endi <= 10^4

> [!info] Approach
> In arbitrary order, overlaps can't be detected without O(n²) pair checks. Sorting by start makes all overlapping intervals adjacent — one linear scan suffices. Sort by start; maintain a running merged interval; extend its end if current interval overlaps. `merged[-1][1] = max(merged[-1][1], end)` when `start ≤ merged[-1][1]`.

> [!note]- Python Solution
> ```python
> def merge(intervals):
>     intervals.sort(key=lambda x: x[0])
>     merged = []
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

### Non-overlapping Intervals (Minimum number to remove) `🎯 T2`

> [!example] Problem
> Given an array of intervals intervals where intervals[i] = [starti, endi], return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.
> Note that intervals which only touch at a point are non-overlapping. For example, [1, 2] and [2, 3] are non-overlapping.
> 
> **Example 1:**
> ```
> Input: intervals = [[1,2],[2,3],[3,4],[1,3]]
> Output: 1
> Explanation: [1,3] can be removed and the rest of the intervals are non-overlapping.
> ```
> 
> **Example 2:**
> ```
> Input: intervals = [[1,2],[1,2],[1,2]]
> Output: 2
> Explanation: You need to remove two [1,2] to make the rest of the intervals non-overlapping.
> ```
> 
> **Example 3:**
> ```
> Input: intervals = [[1,2],[2,3]]
> Output: 0
> Explanation: You don't need to remove any of the intervals since they're already non-overlapping.
> ```
> 
> **Constraints:**
> - 1 <= intervals.length <= 10^5
> - intervals[i].length == 2
> - -5 * 10^4 <= starti < endi <= 5 * 10^4

> [!info] Approach
> Equivalent to maximizing the number of non-overlapping intervals kept (classic Activity Selection). Exchange argument: among all intervals overlapping with the current boundary, keeping the one with the earliest end leaves maximum room — any other choice can only tighten the constraint. Sort by end time. Greedily keep intervals that don't overlap with the last kept interval. Count removals. Track `last_end`; if `start >= last_end`, keep (update last_end = end); else remove (increment count).

> [!note]- Python Solution
> ```python
> def erase_overlap_intervals(intervals):
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
> Given an array of meeting time intervals `intervals` where `intervals[i] = [start_i, end_i]`, return *the minimum number of conference rooms required*.
> 
>  
> 
> Example 1:
> 
> ```
> **Input:** intervals = [[0,30],[5,10],[15,20]]
> **Output:** 2
> 
> ```
> 
> Example 2:
> 
> ```
> **Input:** intervals = [[7,10],[2,4]]
> **Output:** 1
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= intervals.length <= 10^4`
> 	
> - `0 <= start_i < end_i <= 10^6`

> [!info] Approach
> Each new meeting either reuses an ended room or opens a new one. The minimum rooms needed = maximum number of meetings simultaneously in progress. A min-heap on end times gives O(log n) access to the earliest-ending room. Sort meetings by start. Maintain a min-heap of end times. For each meeting, check if the earliest-ending room has freed up; if so, reuse it (heapreplace); else open a new room (heappush). Heap size at the end = rooms needed.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def min_meeting_rooms(intervals):
>     if not intervals:
>         return 0
>     intervals.sort(key=lambda x: x[0])
>     heap = []  # min-heap of end times
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
> There are some spherical balloons taped onto a flat wall that represents the XY-plane. The balloons are represented as a 2D integer array points where points[i] = [xstart, xend] denotes a balloon whose horizontal diameter stretches between xstart and xend. You do not know the exact y-coordinates of the balloons.
> Arrows can be shot up directly vertically (in the positive y-direction) from different points along the x-axis. A balloon with xstart and xend is burst by an arrow shot at x if xstart <= x <= xend. There is no limit to the number of arrows that can be shot. A shot arrow keeps traveling up infinitely, bursting any balloons in its path.
> Given the array points, return the minimum number of arrows that must be shot to burst all balloons.
> 
> **Example 1:**
> ```
> Input: points = [[10,16],[2,8],[1,6],[7,12]]
> Output: 2
> Explanation: The balloons can be burst by 2 arrows:
> - Shoot an arrow at x = 6, bursting the balloons [2,8] and [1,6].
> - Shoot an arrow at x = 11, bursting the balloons [10,16] and [7,12].
> ```
> 
> **Example 2:**
> ```
> Input: points = [[1,2],[3,4],[5,6],[7,8]]
> Output: 4
> Explanation: One arrow needs to be shot for each balloon for a total of 4 arrows.
> ```
> 
> **Example 3:**
> ```
> Input: points = [[1,2],[2,3],[3,4],[4,5]]
> Output: 2
> Explanation: The balloons can be burst by 2 arrows:
> - Shoot an arrow at x = 2, bursting the balloons [1,2] and [2,3].
> - Shoot an arrow at x = 4, bursting the balloons [3,4] and [4,5].
> ```
> 
> **Constraints:**
> - 1 <= points.length <= 10^5
> - points[i].length == 2
> - -2^{31} <= xstart < xend <= 2^{31} - 1

> [!info] Approach
> Same as activity selection but we want to maximize simultaneous coverage (one arrow covers all overlapping intervals at a point). Exchange argument: sort by end; an arrow placed at the earliest end covers all current overlapping balloons — any later placement can only miss some. Sort by end. Greedily shoot at the end of the current balloon if it hasn't been burst yet. Arrow at `end`; skip all balloons with `start ≤ end`; next arrow at the next un-burst balloon's end.

> [!note]- Python Solution
> ```python
> def find_min_arrow_shots(points):
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
> You are given a series of video clips from a sporting event that lasted time seconds. These video clips can be overlapping with each other and have varying lengths.
> Each video clip is described by an array clips where clips[i] = [starti, endi] indicates that the ith clip started at starti and ended at endi.
> We can cut these clips into segments freely.
> Return the minimum number of clips needed so that we can cut the clips into segments that cover the entire sporting event [0, time]. If the task is impossible, return -1.
> 
> **Example 1:**
> ```
> Input: clips = [[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]], time = 10
> Output: 3
> Explanation: We take the clips [0,2], [8,10], [1,9]; a total of 3 clips.
> Then, we can reconstruct the sporting event as follows:
> We cut [1,9] into segments [1,2] + [2,8] + [8,9].
> Now we have segments [0,2] + [2,8] + [8,10] which cover the sporting event [0, 10].
> ```
> 
> **Example 2:**
> ```
> Input: clips = [[0,1],[1,2]], time = 5
> Output: -1
> Explanation: We cannot cover [0,5] with only [0,1] and [1,2].
> ```
> 
> **Example 3:**
> ```
> Input: clips = [[0,1],[6,8],[0,2],[5,6],[0,4],[0,3],[6,7],[1,3],[4,7],[1,4],[2,5],[2,6],[3,4],[4,5],[5,7],[6,9]], time = 9
> Output: 3
> Explanation: We can take clips [0,4], [4,7], and [6,9].
> ```
> 
> **Constraints:**
> - 1 <= clips.length <= 100
> - 0 <= starti <= endi <= 100
> - 1 <= time <= 100

> [!info] Approach
> Coverage problem — must reach position `time` from 0. At each step, greedily pick the clip that extends coverage furthest from the current boundary. This is the interval covering (Jump Game) variant applied to intervals. Sort clips by start. Sweep: at each "current coverage end," find the clip starting ≤ current end that extends furthest. Advance coverage; increment clip count. Two pointers: `cur_end` (coverage end), `farthest` (best extension seen). When current clip starts > cur_end, coverage has a gap — return -1.

> [!note]- Python Solution
> ```python
> def video_stitching(clips, time):
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
> Same as Video Stitching — interval covering problem. Each tap defines a coverage interval; need to cover `[0, n]` with minimum intervals. Convert taps to intervals; apply greedy interval covering. Pre-process: for each position i, compute interval `[max(0, i-r), min(n, i+r)]`; sort by start; run jump-game-style greedy.

> [!note]- Python Solution
> ```python
> def min_taps(n, ranges):
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
> This is exactly Meeting Rooms II — minimum rooms = minimum groups. Two intervals in the same group must be non-overlapping; the minimum groups needed equals the maximum number of intervals simultaneously active. Sort by start; min-heap of group end times. For each interval, reuse a group if its end ≤ current start; else open a new group. Identical to Meeting Rooms II solution.

> [!note]- Python Solution
> ```python
> def min_groups(intervals):
>     intervals.sort(key=lambda x: x[0])
>     heap = []
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
> Assume you are an awesome parent and want to give your children some cookies. But, you should give each child at most one cookie.
> Each child i has a greed factor g[i], which is the minimum size of a cookie that the child will be content with; and each cookie j has a size s[j]. If s[j] >= g[i], we can assign the cookie j to the child i, and the child i will be content. Your goal is to maximize the number of your content children and output the maximum number.
> 
> **Example 1:**
> ```
> Input: g = [1,2,3], s = [1,1]
> Output: 1
> Explanation: You have 3 children and 2 cookies. The greed factors of 3 children are 1, 2, 3. 
> And even though you have 2 cookies, since their size is both 1, you could only make the child whose greed factor is 1 content.
> You need to output 1.
> ```
> 
> **Example 2:**
> ```
> Input: g = [1,2], s = [1,2,3]
> Output: 2
> Explanation: You have 2 children and 3 cookies. The greed factors of 2 children are 1, 2. 
> You have 3 cookies and their sizes are big enough to gratify all of the children, 
> You need to output 2.
> ```
> 
> **Constraints:**
> - 1 <= g.length <= 3 * 10^4
> - 0 <= s.length <= 3 * 10^4
> - 1 <= g[i], s[j] <= 2^{31} - 1

> [!info] Approach
> Sort both. Greedily assign the smallest sufficient cookie to the least greedy unsatisfied child. Preserves bigger cookies for greedier children. Two pointers after sorting. Sort g and s. Two pointers i (children), j (cookies). If s[j] >= g[i]: i++, j++. Else j++. Return i.

> [!note]- Python Solution
> ```python
> def find_content_children(g, s):
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
> Given an integer array nums, return the largest perimeter of a triangle with a non-zero area, formed from three of these lengths. If it is impossible to form any triangle of a non-zero area, return 0.
> 
> **Example 1:**
> ```
> Input: nums = [2,1,2]
> Output: 5
> Explanation: You can form a triangle with three side lengths: 1, 2, and 2.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,1,10]
> Output: 0
> Explanation: 
> You cannot use the side lengths 1, 1, and 2 to form a triangle.
> You cannot use the side lengths 1, 1, and 10 to form a triangle.
> You cannot use the side lengths 1, 2, and 10 to form a triangle.
> As we cannot use any three side lengths to form a triangle of non-zero area, we return 0.
> ```
> 
> **Constraints:**
> - 3 <= nums.length <= 10^4
> - 1 <= nums[i] <= 10^6

> [!info] Approach
> Triangle inequality: a+b > c where a≤b≤c. If we sort descending, for any three consecutive elements a≥b≥c, if b+c > a they form a valid triangle. The first valid triple maximizes perimeter (sorted desc). Sort descending. Check consecutive triples. Sort desc. For i in range(len-2): if nums[i] < nums[i+1]+nums[i+2]: return sum of these three. Return 0.

> [!note]- Python Solution
> ```python
> def largest_perimeter(nums):
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

### Jump Game (can reach?) `🎯 T2`

> [!example] Problem
> You are given an integer array nums. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.
> Return true if you can reach the last index, or false otherwise.
> 
> **Example 1:**
> ```
> Input: nums = [2,3,1,1,4]
> Output: true
> Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,2,1,0,4]
> Output: false
> Explanation: You will always arrive at index 3 no matter what. Its maximum jump length is 0, which makes it impossible to reach the last index.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^4
> - 0 <= nums[i] <= 10^5

> [!info] Approach
> At any reachable index i, all indices up to `i + nums[i]` are also reachable — the reachable set is always a contiguous prefix `[0, max_reach]`. Track the frontier; if current index exceeds it, the last index is unreachable. Track `max_reach = max(i + nums[i])` for all reachable i. If `i > max_reach` at any point, return False. Single pass; early exit the moment current index exceeds max_reach.

> [!note]- Python Solution
> ```python
> def can_jump(nums):
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

### Jump Game II (minimum jumps) `🎯 T2`

> [!example] Problem
> You are given a 0-indexed array of integers nums of length n. You are initially positioned at nums[0].
> Each element nums[i] represents the maximum length of a forward jump from index i. In other words, if you are at nums[i], you can jump to any nums[i + j] where:
> Return the minimum number of jumps to reach nums[n - 1]. The test cases are generated such that you can reach nums[n - 1].
> 
> **Example 1:**
> ```
> Input: nums = [2,3,1,1,4]
> Output: 2
> Explanation: The minimum number of jumps to reach the last index is 2. Jump 1 step from index 0 to 1, then 3 steps to the last index.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,3,0,1,4]
> Output: 2
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^4
> - 0 <= nums[i] <= 1000
> - It's guaranteed that you can reach nums[n - 1].

> [!info] Approach
> At each "jump boundary," we must take a new jump. Exchange argument: among all positions reachable in the current jump, choosing the one that extends furthest is always optimal — picking any shorter reach can only worsen future options. Maintain `cur_end` (end of current jump range) and `farthest` (max reach seen so far). When `i == cur_end`, take a jump: increment count, advance `cur_end = farthest`. Loop only to `n-2` (last index doesn't need a jump from it).

> [!note]- Python Solution
> ```python
> def jump(nums):
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

### Jump Game VI (DP + Deque) `🎯 T2`

> [!example] Problem
> You are given a 0-indexed integer array nums and an integer k.
> You are initially standing at index 0. In one move, you can jump at most k steps forward without going outside the boundaries of the array. That is, you can jump from index i to any index in the range [i + 1, min(n - 1, i + k)] inclusive.
> You want to reach the last index of the array (index n - 1). Your score is the sum of all nums[j] for each index j you visited in the array.
> Return the maximum score you can get.
> 
> **Example 1:**
> ```
> Input: nums = [1,-1,-2,4,-7,3], k = 2
> Output: 7
> Explanation: You can choose your jumps forming the subsequence [1,-1,4,3] (underlined above). The sum is 7.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [10,-5,-2,4,0,3], k = 3
> Output: 17
> Explanation: You can choose your jumps forming the subsequence [10,4,3] (underlined above). The sum is 17.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,-5,-20,4,-1,3,-6,-3], k = 2
> Output: 0
> ```
> 
> **Constraints:**
> - 1 <= nums.length, k <= 10^5
> - -10^4 <= nums[i] <= 10^4

> [!info] Approach
> `dp[i] = max(dp[i-1..i-k]) + nums[i]`. Naively O(nk); sliding window maximum via monotone deque gives O(n) per step, O(n) total. Maintain a max-deque over a window of size k. `dp[i] = deque_max + nums[i]`. Deque stores indices in decreasing dp-value order; pop front when out of window, pop back when dp[i-1] ≥ dp[deque.back()].

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def max_result(nums, k):
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

### Candy (LC 135) `🎯 T2`

> [!example] Problem
> There are n children standing in a line. Each child is assigned a rating value given in the integer array ratings.
> You are giving candies to these children subjected to the following requirements:
> Return the minimum number of candies you need to have to distribute the candies to the children.
> 
> **Example 1:**
> ```
> Input: ratings = [1,0,2]
> Output: 5
> Explanation: You can allocate to the first, second and third child with 2, 1, 2 candies respectively.
> ```
> 
> **Example 2:**
> ```
> Input: ratings = [1,2,2]
> Output: 4
> Explanation: You can allocate to the first, second and third child with 1, 2, 1 candies respectively.
> The third child gets 1 candy because it satisfies the above two conditions.
> ```
> 
> **Constraints:**
> - n == ratings.length
> - 1 <= n <= 2 * 10^4
> - 0 <= ratings[i] <= 2 * 10^4

> [!info] Approach
> Two constraints (left and right neighbors) conflict if solved simultaneously. Solve each independently and take max. Two passes — left-to-right enforces left constraint, right-to-left enforces right constraint.

>   1. Init candies = [1]*n.
>   2. Left pass: if ratings[i] > ratings[i-1]: candies[i] = candies[i-1]+1.
>   3. Right pass: if ratings[i] > ratings[i+1]: candies[i] = max(candies[i], candies[i+1]+1).
>   4. Return sum(candies).

> [!note]- Python Solution
> ```python
> def candy(ratings):
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

### Reorganize String `⚡ T1`

> [!example] Problem
> Given a string s, rearrange the characters of s so that any two adjacent characters are not the same.
> Return any possible rearrangement of s or return "" if not possible.
> 
> **Example 1:**
> ```
> Input: s = "aab"
> Output: "aba"
> ```
> 
> **Example 2:**
> ```
> Input: s = "aaab"
> Output: ""
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 500
> - s consists of lowercase English letters.

> [!info] Approach
> Impossible if any character appears more than `⌈n/2⌉` times. Otherwise, greedy: always place the most frequent available character that isn't the same as the previous one. Max-heap by frequency. At each step, pop the most frequent, append, and re-push after cooldown. Track `prev` (last placed char) — if top of heap == prev, temporarily swap with second-most-frequent.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import Counter
> 
> def reorganize_string(s):
>     freq = Counter(s)
>     if max(freq.values()) > (len(s) + 1) // 2:
>         return ""
>     heap = [(-cnt, char) for char, cnt in freq.items()]
>     heapq.heapify(heap)
>     result = []
>     prev_cnt, prev_char = 0, ""
>     while heap:
>         cnt, char = heapq.heappop(heap)
>         result.append(char)
>         if prev_cnt < 0:
>             heapq.heappush(heap, (prev_cnt, prev_char))
>         prev_cnt, prev_char = cnt + 1, char  # cnt is negative
>         +1 decrements count
>     return "".join(result)
> ```

> [!success] Complexity
> O(n log k) where k = distinct chars ≤ 26, effectively O(n).

> [!tip] Alternatives
> Even-index placement: place highest-frequency chars at indices 0,2,4,..., then fill odd indices. O(n log n) to sort, O(n) placement.

---

### Rearrange String k Distance Apart (Rearrange Barcodes)

> [!example] Problem
> Given a string `s` and an integer `k`, rearrange `s` such that the same characters are **at least** distance `k` from each other. If it is not possible to rearrange the string, return an empty string `""`.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** s = "aabbcc", k = 3
> **Output:** "abcabc"
> **Explanation:** The same letters are at least a distance of 3 from each other.
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** s = "aaabc", k = 3
> **Output:** ""
> **Explanation:** It is not possible to rearrange the string.
> 
> ```
> 
> Example 3:
> 
> ```
> 
> **Input:** s = "aaadbbcc", k = 2
> **Output:** "abacabcd"
> **Explanation:** The same letters are at least a distance of 2 from each other.
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= s.length <= 3 * 10^5`
> 	
> - `s` consists of only lowercase English letters.
> 	
> - `0 <= k <= s.length`

> [!info] Approach
> Generalization of Reorganize String with cooldown k instead of 1. Most frequent characters must be spread across n/k-sized "chunks." A greedy fill of k-size chunks from the most frequent characters produces a valid arrangement if possible. Max-heap by frequency. Fill k characters per round (one from each of the k most frequent). After each round, re-push decremented counts. Use a queue to enforce cooldown: after using a character, re-push only after k steps.

> [!note]- Python Solution
> ```python
> from collections import Counter, deque
> 
> def rearrange_barcodes(barcodes):
>     freq = Counter(barcodes)
>     heap = [(-cnt, val) for val, cnt in freq.items()]
>     heapq.heapify(heap)
>     result = []
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
> def rearrange_barcodes_clean(barcodes):
>     freq = Counter(barcodes)
>     heap = [(-cnt, val) for val, cnt in freq.items()]
>     heapq.heapify(heap)
>     result = []
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

### Gas Station `🎯 T2`

> [!example] Problem
> There are n gas stations along a circular route, where the amount of gas at the ith station is gas[i].
> You have a car with an unlimited gas tank and it costs cost[i] of gas to travel from the ith station to its next (i + 1)th station. You begin the journey with an empty tank at one of the gas stations.
> Given two integer arrays gas and cost, return the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise return -1. If there exists a solution, it is guaranteed to be unique.
> 
> **Example 1:**
> ```
> Input: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
> Output: 3
> Explanation:
> Start at station 3 (index 3) and fill up with 4 unit of gas. Your tank = 0 + 4 = 4
> Travel to station 4. Your tank = 4 - 1 + 5 = 8
> Travel to station 0. Your tank = 8 - 2 + 1 = 7
> Travel to station 1. Your tank = 7 - 3 + 2 = 6
> Travel to station 2. Your tank = 6 - 4 + 3 = 5
> Travel to station 3. The cost is 5. Your gas is just enough to travel back to station 3.
> Therefore, return 3 as the starting index.
> ```
> 
> **Example 2:**
> ```
> Input: gas = [2,3,4], cost = [3,4,3]
> Output: -1
> Explanation:
> You can't start at station 0 or 1, as there is not enough gas to travel to the next station.
> Let's start at station 2 and fill up with 4 unit of gas. Your tank = 0 + 4 = 4
> Travel to station 0. Your tank = 4 - 3 + 2 = 3
> Travel to station 1. Your tank = 3 - 3 + 3 = 3
> You cannot travel back to station 2, as it requires 4 unit of gas but you only have 3.
> Therefore, you can't travel around the circuit once no matter where you start.
> ```
> 
> **Constraints:**
> - n == gas.length == cost.length
> - 1 <= n <= 10^5
> - 0 <= gas[i], cost[i] <= 10^4
> - The input is generated such that the answer is unique.

> [!info] Approach
> Two insights: (1) If total gas < total cost, no solution. (2) If solution exists, the starting point is the index after the last point where cumulative tank went negative. Proof: any station between `start` and the negative-tank point would inherit a deficit. Track running tank. When tank < 0, reset to 0 and update start = i+1. Single pass. Feasibility check built into the same pass via total sum.

> [!note]- Python Solution
> ```python
> def can_complete_circuit(gas, cost):
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

### Trapping Rain Water (greedy view) `⚡ T1`

> [!example] Problem
> Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.
> 
> **Example 1:**
> ```
> Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
> Output: 6
> Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.
> ```
> 
> **Example 2:**
> ```
> Input: height = [4,2,0,3,2,5]
> Output: 9
> ```
> 
> **Constraints:**
> - n == height.length
> - 1 <= n <= 2 * 10^4
> - 0 <= height[i] <= 10^5

> [!info] Approach
> Water at position i is bounded by `min(max_left[i], max_right[i]) - height[i]`. Two-pointer greedy: the side with the smaller max bound determines water for its current position — we can process it without knowing the other side's remaining values. Two pointers `lo, hi`. Water trapped at `lo` = `left_max - height[lo]` if `left_max < right_max`. Process the side with the smaller max. Advance the pointer with the smaller current boundary; maintain running max for each side.

> [!note]- Python Solution
> ```python
> def trap(height):
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
> A GCD string must divide both strings. If `str1 + str2 == str2 + str1`, a GCD exists with length `gcd(len(str1), len(str2))`. This is the string analog of the Euclidean algorithm: the GCD of two strings is a repeated unit, and its length is `gcd(len1, len2)`. Check concatenation equality; if valid, return `str1[:gcd(len(str1), len(str2))]`. `math.gcd(m, n)`.

> [!note]- Python Solution
> ```python
> from math import gcd
> 
> def gcd_of_strings(str1, str2):
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
> Each stick's length contributes to the total cost once per merge it participates in. Longer sticks participating in fewer merges reduces cost. Always merging the two shortest sticks minimizes total cost — this is Huffman coding's greedy insight. Min-heap. Repeatedly pop two smallest, combine, push the result, accumulate cost. n-1 merges; each O(log n); total O(n log n).

> [!note]- Python Solution
> ```python
> def connect_sticks(sticks):
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
> After removing k elements, we keep n-k elements. The minimum range of n-k consecutive elements in sorted order gives the answer. Sorting exposes this: after sort, optimal removal strategy is to remove `i` elements from the left and `k-i` from the right for i in 0..k. Sort; try all (i, k-i) splits for i in 0..k; answer = min(nums[n-1-(k-i)] - nums[i]). For 3 moves: 4 splits — (0,3),(1,2),(2,1),(3,0).

> [!note]- Python Solution
> ```python
> def min_difference(nums):
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
> You are given a string s. We want to partition the string into as many parts as possible so that each letter appears in at most one part. For example, the string "ababcc" can be partitioned into ["abab", "cc"], but partitions such as ["aba", "bcc"] or ["ab", "ab", "cc"] are invalid.
> Note that the partition is done so that after concatenating all the parts in order, the resultant string should be s.
> Return a list of integers representing the size of these parts.
> 
> **Example 1:**
> ```
> Input: s = "ababcbacadefegdehijhklij"
> Output: [9,7,8]
> Explanation:
> The partition is "ababcbaca", "defegde", "hijhklij".
> This is a partition so that each letter appears in at most one part.
> A partition like "ababcbacadefegde", "hijhklij" is incorrect, because it splits s into less parts.
> ```
> 
> **Example 2:**
> ```
> Input: s = "eccbbbbdec"
> Output: [10]
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 500
> - s consists of lowercase English letters.

> [!info] Approach
> Each character must stay in one partition — it determines the right boundary of the partition containing its first occurrence. Last occurrence map + greedy sweep. Build last[c] = last index of character c. Sweep left to right. Maintain current partition end = max(last[c] for c in current partition). When i == end: partition complete, record size, start new.

> [!note]- Python Solution
> ```python
> def partition_labels(s):
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

## Sorting-Based Greedy

### Queue Reconstruction by Height (LC 406)

> [!example] Problem
> You are given an array of people, people, which are the attributes of some people in a queue (not necessarily in order). Each people[i] = [hi, ki] represents the ith person of height hi with exactly ki other people in front who have a height greater than or equal to hi.
> Reconstruct and return the queue that is represented by the input array people. The returned queue should be formatted as an array queue, where queue[j] = [hj, kj] is the attributes of the jth person in the queue (queue[0] is the person at the front of the queue).
> 
> **Example 1:**
> ```
> Input: people = [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]
> Output: [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]
> Explanation:
> Person 0 has height 5 with no other people taller or the same height in front.
> Person 1 has height 7 with no other people taller or the same height in front.
> Person 2 has height 5 with two persons taller or the same height in front, which is person 0 and 1.
> Person 3 has height 6 with one person taller or the same height in front, which is person 1.
> Person 4 has height 4 with four people taller or the same height in front, which are people 0, 1, 2, and 3.
> Person 5 has height 7 with one person taller or the same height in front, which is person 1.
> Hence [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]] is the reconstructed queue.
> ```
> 
> **Example 2:**
> ```
> Input: people = [[6,0],[5,0],[4,0],[3,2],[2,2],[1,4]]
> Output: [[4,0],[5,0],[2,2],[3,2],[1,4],[6,0]]
> ```
> 
> **Constraints:**
> - 1 <= people.length <= 2000
> - 0 <= hi <= 10^6
> - 0 <= ki < people.length
> - It is guaranteed that the queue can be reconstructed.

> [!info] Approach
> Taller people are invisible to shorter ones for the k-count. So place taller people first — their relative order is determined by k alone. Inserting shorter people later doesn't affect any already-placed taller person's k value. Sort by height descending (ties: k ascending). Insert each person at index k into the result list. `result.insert(k, person)` — O(n) per insert, but n is small enough; taller people already placed are unaffected by later insertions.

> [!note]- Python Solution
> ```python
> def reconstruct_queue(people):
>     # Sort: tallest first; among same height, smallest k first
>     people.sort(key=lambda x: (-x[0], x[1]))
>     result = []
>     for person in people:
>         result.insert(person[1], person)
>     return result
> ```

> [!success] Complexity
> O(n² ) time (n insertions each O(n)), O(n) space. For n ≤ 2000 (LC constraint) this is fine.

> [!tip] Alternatives
> BIT/segment tree to find the k-th empty slot: O(n log n). Linked list for O(1) insert at position after O(n) traversal.

---

### IPO (Maximize Capital, LC 502) `⚡ T1`

> [!example] Problem
> Suppose LeetCode will start its IPO soon. In order to sell a good price of its shares to Venture Capital, LeetCode would like to work on some projects to increase its capital before the IPO. Since it has limited resources, it can only finish at most k distinct projects before the IPO. Help LeetCode design the best way to maximize its total capital after finishing at most k distinct projects.
> You are given n projects where the ith project has a pure profit profits[i] and a minimum capital of capital[i] is needed to start it.
> Initially, you have w capital. When you finish a project, you will obtain its pure profit and the profit will be added to your total capital.
> Pick a list of at most k distinct projects from given projects to maximize your final capital, and return the final maximized capital.
> The answer is guaranteed to fit in a 32-bit signed integer.
> 
> **Example 1:**
> ```
> Input: k = 2, w = 0, profits = [1,2,3], capital = [0,1,1]
> Output: 4
> Explanation: Since your initial capital is 0, you can only start the project indexed 0.
> After finishing it you will obtain profit 1 and your capital becomes 1.
> With capital 1, you can either start the project indexed 1 or the project indexed 2.
> Since you can choose at most 2 projects, you need to finish the project indexed 2 to get the maximum capital.
> Therefore, output the final maximized capital, which is 0 + 1 + 3 = 4.
> ```
> 
> **Example 2:**
> ```
> Input: k = 3, w = 0, profits = [1,2,3], capital = [0,1,2]
> Output: 6
> ```
> 
> **Constraints:**
> - 1 <= k <= 10^5
> - 0 <= w <= 10^9
> - n == profits.length
> - n == capital.length
> - 1 <= n <= 10^5
> - 0 <= profits[i] <= 10^4
> - 0 <= capital[i] <= 10^9

> [!info] Approach
> At each step, among all affordable projects, the greedy optimal is to pick the highest-profit one — taking less profit now can't help unlock better future projects than taking more profit. This is provable by exchange argument. Min-heap sorted by capital requirement (to find newly affordable projects efficiently). Max-heap of profits of all currently affordable projects. Sort projects by capital. For each of k steps: push all projects with `capital[i] ≤ W` into max-heap; pop the most profitable; add to W. If max-heap empty, can't proceed.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def find_maximized_capital(k, w, profits, capital):
>     # Min-heap by capital requirement
>     projects = sorted(zip(capital, profits))
>     available = []  # max-heap (negate profits)
>     i = 0
>     for _ in range(k):
>         # Unlock all projects affordable with current capital w
>         while i < len(projects) and projects[i][0] <= w:
>             heapq.heappush(available, -projects[i][1])
>             i += 1
>         if not available:
>             break  # no affordable project
>         w += -heapq.heappop(available)
>     return w
> ```

> [!success] Complexity
> O(n log n) time (sorting + heap ops), O(n) space.

> [!tip] Alternatives
> Brute force O(k * n): scan all projects each step. Sorting + binary search to find boundary: already implicit in the two-heap approach.

### Activity Selection (Maximum Non-Overlapping Intervals)

> [!example] Problem
> Given intervals, select the maximum number of non-overlapping intervals you can keep.

> [!info] Approach
> Greedy by earliest finishing time leaves the most room for future intervals. Sort by end time and always keep the next interval whose start is at least the end of the last kept interval. Track `last_end`; when `start >= last_end`, keep the interval and update `last_end = end`.

> [!note]- Python Solution
> ```python
> def activity_selection(intervals):
>     intervals.sort(key=lambda x: x[1])
>     count = 0
>     last_end = float("-inf")
>     for start, end in intervals:
>         if start >= last_end:
>             count += 1
>             last_end = end
>     return count
> ```

> [!success] Complexity
> O(n log n) time, O(1) extra space.

> [!tip] Alternatives
> Sorting by start does not maximize the count; earliest end is the greedy key.

---

## See Also

[[dynamic-programming]] | [[sorting]] | [[heap]] | [[binary-search]]

---

## Greedy — Interval and Coverage Problems

### Video Stitching (LC 1024)

> [!example] Problem
> You are given a series of video clips from a sporting event that lasted time seconds. These video clips can be overlapping with each other and have varying lengths.
> Each video clip is described by an array clips where clips[i] = [starti, endi] indicates that the ith clip started at starti and ended at endi.
> We can cut these clips into segments freely.
> Return the minimum number of clips needed so that we can cut the clips into segments that cover the entire sporting event [0, time]. If the task is impossible, return -1.
> 
> **Example 1:**
> ```
> Input: clips = [[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]], time = 10
> Output: 3
> Explanation: We take the clips [0,2], [8,10], [1,9]; a total of 3 clips.
> Then, we can reconstruct the sporting event as follows:
> We cut [1,9] into segments [1,2] + [2,8] + [8,9].
> Now we have segments [0,2] + [2,8] + [8,10] which cover the sporting event [0, 10].
> ```
> 
> **Example 2:**
> ```
> Input: clips = [[0,1],[1,2]], time = 5
> Output: -1
> Explanation: We cannot cover [0,5] with only [0,1] and [1,2].
> ```
> 
> **Example 3:**
> ```
> Input: clips = [[0,1],[6,8],[0,2],[5,6],[0,4],[0,3],[6,7],[1,3],[4,7],[1,4],[2,5],[2,6],[3,4],[4,5],[5,7],[6,9]], time = 9
> Output: 3
> Explanation: We can take clips [0,4], [4,7], and [6,9].
> ```
> 
> **Constraints:**
> - 1 <= clips.length <= 100
> - 0 <= starti <= endi <= 100
> - 1 <= time <= 100

> [!info] Approach
> This is the classic "minimum jumps to cover a range" greedy problem. Sort clips by start time. At each step, among all clips that start at or before the current position, pick the one that extends the furthest. Sort by start. Maintain `cur_end` (current covered end) and `farthest` (furthest reach among clips starting ≤ `cur_end`). When we've processed all clips starting ≤ `cur_end`, we must extend using the farthest clip found, incrementing the count. Iterate through sorted clips. If `clip_start > cur_end`, return -1 (gap). Update `farthest`. When we've exhausted clips for this jump, set `cur_end = farthest`, increment count.

> [!note]- Python Solution
> ```python
> def video_stitching(clips, time):
>     clips.sort()
>     count = 0
>     cur_end = 0
>     farthest = 0
>     i = 0
>     n = len(clips)
>     while cur_end < time:
>         while i < n and clips[i][0] <= cur_end:
>             farthest = max(farthest, clips[i][1])
>             i += 1
>         if farthest == cur_end:
>             return -1
>         cur_end = farthest
>         count += 1
>     return count
> ```

> [!success] Complexity
> Time O(n log n) for sort, O(n) for scan. Space O(1).

> [!tip] Alternatives
> - DP: `dp[i]` = minimum clips to reach time `i`. Fill left to right from clip endpoints. O(n * T) — correct but slower.
> - Key insight: greedy "jump to maximum reach" from each coverage window mirrors the Jump Game II pattern exactly.

---

### Minimum Taps to Water a Garden (LC 1326)

> [!example] Problem
> There is a one-dimensional garden on the x-axis. The garden starts at the point 0 and ends at the point n. (i.e., the length of the garden is n).
> There are n + 1 taps located at points [0, 1, ..., n] in the garden.
> Given an integer n and an integer array ranges of length n + 1 where ranges[i] (0-indexed) means the i-th tap can water the area [i - ranges[i], i + ranges[i]] if it was open.
> Return the minimum number of taps that should be open to water the whole garden, If the garden cannot be watered return -1.
> 
> **Example 1:**
> ```
> Input: n = 5, ranges = [3,4,1,1,0,0]
> Output: 1
> Explanation: The tap at point 0 can cover the interval [-3,3]
> The tap at point 1 can cover the interval [-3,5]
> The tap at point 2 can cover the interval [1,3]
> The tap at point 3 can cover the interval [2,4]
> The tap at point 4 can cover the interval [4,4]
> The tap at point 5 can cover the interval [5,5]
> Opening Only the second tap will water the whole garden [0,5]
> ```
> 
> **Example 2:**
> ```
> Input: n = 3, ranges = [0,0,0,0]
> Output: -1
> Explanation: Even if you activate all the four taps you cannot water the whole garden.
> ```
> 
> **Constraints:**
> - 1 <= n <= 10^4
> - ranges.length == n + 1
> - 0 <= ranges[i] <= 100

> [!info] Approach
> This reduces directly to the Jump Game II / interval cover problem. Each tap covers an interval. We want to cover `[0, n]` with the fewest intervals. Convert each tap to its interval. Then apply the same greedy: sort by left endpoint, for each coverage window pick the interval that extends farthest right. Build intervals `(max(0, i - ranges[i]), min(n, i + ranges[i]))` for each tap. Sort. Apply the Video Stitching greedy.

> [!note]- Python Solution
> ```python
> def min_taps(n, ranges):
>     intervals = []
>     for i in range(n + 1):
>         left = max(0, i - ranges[i])
>         right = min(n, i + ranges[i])
>         intervals.append((left, right))
>     intervals.sort()
>     count = 0
>     cur_end = 0
>     farthest = 0
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
> Time O(n log n), Space O(n).

> [!tip] Alternatives
> - A cleaner O(n) approach: use an array `max_reach[i]` = farthest right endpoint of any interval starting at `i`. Then one pass with the Jump Game II logic. O(n) after the O(n) preprocessing — no sort needed.

---

## See Also (Extended)

[[dynamic-programming]] | [[sorting]] | [[heap]] | [[binary-search]] | [[sliding-window]]


### Hand of Straights `🎯 T2`

**Problem**: Given a hand of cards and a groupSize, check if you can rearrange them into groups of `groupSize` consecutive cards.

**Key Insight**: Use an ordered map (sorted Counter). Always start from the smallest card — if you can't form a group starting from smallest, it's impossible.

```python
from collections import Counter
def isNStraightHand(hand, groupSize):
    if len(hand) % groupSize: return False
    count = Counter(hand)
    for card in sorted(count):
        if count[card]:
            freq = count[card]
            for i in range(groupSize):
                count[card + i] -= freq
                if count[card + i] < 0: return False
    return True
```

**TC**: O(n log n) | **SC**: O(n) | Related: Task Scheduler (same greedy idea)

