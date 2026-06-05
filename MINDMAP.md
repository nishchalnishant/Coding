---
module: root
topic: Mindmap
subtopic: 
status: unread
tags: [root, mindmap]
---

← [Start here](00-start-here/README.md) · [Flowcharts (triggers)](FLOWCHARTS.md) · [coding/data-structures/](coding/data-structures/) · [coding/algorithms/](coding/algorithms/)

# Mindmap — ASCII only (`coding/`)

> [!note] L3 Reference Document
> This file is a **reference / meta document** — read it once, then use it as a lookup.
> It is NOT a coding practice file. Do not deep-study it like a topic file.

_E/M/H = difficulty · ★ = must-nail · → = one-line hint_

## coding/data-structures/


### advanced.md

```
coding/data-structures/advanced.md
└── advanced.md
    └── Segment Tree
    │   └── Number of Longest Increasing Subsequences (LC 673) `🎯 T2` [M]
    │   │   → For each nums[i] (left to right), query the tree over [0, rank[i]-1] to get the best (len, cnt) for any element smaller than nums[i]. Then new_len = len+1, new_cnt = cnt. Point-update rank[i] with (new_len, new_cnt). Merge rule: keep the entry with larger length; if tie, add counts
```


### array.md

```
coding/data-structures/array.md
└── array.md
    ├── Two Pointers
    │   ├── Two Sum (sorted variant) `⚡ T1` [E]
    │   │   → Two Pointers on sorted array: l=0, r=n-1. If numbers[l] + numbers[r] == target, done. If sum < target, l++ (we need larger). If sum > target, r-- (we need smaller). The sorted invariant guarantees we never skip valid pairs
    │   ├── 3Sum `⚡ T1` [M]
    │   │   → Fix + Two Pointers: Sort. For each i, if nums[i] > 0 break (sorted — no triplet can sum to 0). Skip duplicate i. Run two-pointer on the suffix. On match, skip duplicate left and right before advancing both. Three deduplication sites: i, left, right. Interview note: sorting is what makes the duplicate skipping and early break safe, so this pattern is usually the cleanest solution in interviews
    │   ├── 3Sum Closest `⚡ T1` [M]
    │   │   → Sort + Two Pointers with closest tracking: Sort. For each i, two-pointer on suffix. Compute s = nums[i]+nums[l]+nums[r]. Update closest if |s - target| < |closest - target|. If s < target, l++. If s > target, r--. If exact match, return immediately
    │   ├── Container with Most Water `⚡ T1` [M]
    │   │   → Two Pointers — advance the shorter line: l=0, r=n-1. Compute area. Always advance the pointer pointing to the shorter line — moving the taller line can never increase min(h[l], h[r]) while width also decreases
    │   ├── Trapping Rain Water `⚡ T1` [H]
    │   │   → Two Pointers — binding constraint side: l=0, r=n-1, l_max=r_max=0. If l_max <= r_max, the left side is the constraint, so water at l is l_max - height[l] and we advance l. Otherwise, the right side is the constraint, so water at r is r_max - height[r] and we decrement r
    │   └── Remove Duplicates from Sorted Array `⚡ T1` [M]
    │   │   → Two Pointers — slow/fast write pattern: slow=1. For fast in 1..n-1: if nums[fast] != nums[slow-1], write nums[slow] = nums[fast], slow++. Return slow
    ├── Sliding Window `⚡ T1`
    │   ├── Max Consecutive Ones III `⚡ T1` [M]
    │   │   → Variable sliding window — zero count tracking: Expand r. If nums[r] == 0, increment zero count. If zeros > k, shrink l until zeros ≤ k (moving l past a zero decrements zero count). Track r - l + 1 as window size
    │   ├── Longest Repeating Character Replacement `⚡ T1` [M]
    │   │   → Variable window with monotone max_freq trick: Expand r. Update freq map. If (r - l + 1) - max_freq > k, shrink l by one (decrement freq of s[l]). Key insight: max_freq never needs to decrease — a smaller max_freq cannot yield a larger valid window
    │   ├── Subarrays with K Different Integers `⚡ T1` [M]
    │   │   → Exactly-k = at_most(k) − at_most(k−1): at_most(k) counts subarrays with ≤ k distinct integers. Use standard sliding window: expand right, if distinct count > k shrink left, add r - l + 1 (all subarrays ending at r and starting at l..r). Answer = at_most(k) - at_most(k-1)
    │   ├── Minimum Window Substring `⚡ T1` [H]
    │   │   → Sliding window with have counter: Build need freq map for t. Expand r. For each char, if its count in window hits required count, have++. When have == len(need), try to shrink: record window, shrink l. If removing s[l] drops a count below required, have--
    │   └── Sliding Window Maximum `⚡ T1` [H]
    │       → Monotonic decreasing deque: For each r: pop rear of deque while deque is non-empty and nums[deque[-1]] <= nums[r]. Append r. Pop front if deque[0] <= r - k (out of window). Once r >= k-1, the front index gives the current window max
    ├── Prefix Sum
    │   ├── Subarray Sum Equals K `⚡ T1` [M]
    │   │   → Prefix sum + hash map complement lookup: Scan left to right, maintaining running_sum and a hash map seen of count of each prefix sum seen so far. Seed seen[0] = 1 (empty prefix). For each element, count += seen[running_sum - k]
    │   └── Product of Array Except Self `🎯 T2` [M]
    │       → Two-pass left/right product accumulation: Pass 1: output[i] = product of nums[0..i-1]. Pass 2: maintain right = 1, scan right to left, multiply output[i] *= right, then right *= nums[i]
    ├── Kadane's Algorithm
    │   ├── Maximum Subarray `🎯 T2` [E]
    │   │   → Kadane's algorithm — local reset on negative prefix: Initialize cur = best = nums[0] (handles all-negative case). For each subsequent element: cur = max(x, cur + x). Update best = max(best, cur)
    │   └── Maximum Product Subarray `🎯 T2` [M]
    │   │   → Track max and min simultaneously: At each element x: new max_prod = max(x, max_prod * x, min_prod * x), new min_prod = min(x, max_prod * x, min_prod * x). Use temps to avoid overwriting. Update global best
    ├── Dutch National Flag / Partitioning
    │   └── Sort Colors `⚡ T1` [M]
    │   │   → Dutch National Flag — three-pointer partition: lo=0, mid=0, hi=n-1. While mid <= hi: if nums[mid]==0, swap with lo, advance both; if nums[mid]==1, advance mid; if nums[mid]==2, swap with hi, decrement hi — do NOT advance mid (swapped element from hi is unexamined)
    ├── Boyer-Moore Voting
    │   ├── Majority Element `🎯 T2` [M]
    │   │   → Boyer-Moore voting — cancellation argument: This works because: imagine each "non-candidate" vote cancels one "candidate" vote. Since majority has > n/2 votes, it survives after all cancellations
    │   └── Majority Element II `🎯 T2` [M]
    │       → Boyer-Moore with two candidates: Maintain c1, c2, cnt1, cnt2. For each x: if x == c1, cnt1++; elif x == c2, cnt2++; elif cnt1 == 0, c1=x, cnt1=1; elif cnt2 == 0, c2=x, cnt2=1; else cnt1--, cnt2--. Second pass: count actual frequencies and filter > n/3
    ├── Floyd's Cycle Detection (on Arrays)
    │   └── Find the Duplicate Number `🎯 T2` [M]
    │       → Floyd's cycle detection on implicit linked list: Phase 1 — slow = nums[slow], fast = nums[nums[fast]] until they meet (inside cycle). Phase 2 — reset slow = nums[0] (the start), advance both at speed 1; they meet at the cycle entry = duplicate
    ├── Miscellaneous Array Techniques
    │   ├── Best Time to Buy and Sell Stock `🎯 T2` [M]
    │   │   → min_price = inf, max_profit = 0. For each price: min_price = min(min_price, price), max_profit = max(max_profit, price - min_price)
    │   ├── Move Zeroes `⚡ T1` [M]
    │   │   → slow = 0. For each fast: if nums[fast] != 0, set nums[slow] = nums[fast], slow++. After the loop, zero out nums[slow..n-1]
    │   ├── Two Sum (hash map variant) `⚡ T1` [E]
    │   │   → Hash map complement lookup: For each (i, x): compute complement = target - x. If in map, return [map[complement], i]. Else record x → i. Checking before recording ensures we don't use same index twice
    │   ├── Jump Game II `🎯 T2` [M]
    │   │   → Greedy BFS — level-by-level farthest reach: Advance i from 0 to n-2. Update farthest = max(farthest, i + nums[i]). When i == current_end: a new jump is needed, jumps++, current_end = farthest. Stop when current_end >= n-1
    │   ├── Longest Consecutive Sequence `⚡ T1` [M]
    │   │   → Hash set — start sequences only from minimums: Insert all values into a set. For each n, if n-1 not in set (start of sequence), count consecutive n, n+1, n+2, ... until gap. Update best length
    │   └── Median of Two Sorted Arrays `⚡ T1` [H]
    │       → Binary search on shorter array partition: Binary search on shorter array (WLOG m <= n). Partition nums1 at i, derive nums2 partition j = half - i. Check: nums1[i-1] <= nums2[j] and nums2[j-1] <= nums1[i]. Adjust binary search accordingly. For odd total, median = max(left sides). For even, median = (max(left) + min(right)) / 2
    ├── Range / Immutable Prefix Queries
    │   ├── Range Sum Query — Immutable (LC 303) `🎯 T2` [M]
    │   │   → Prefix sum array — O(1) per query: Precompute prefix[0..n] where prefix[0] = 0 and prefix[i] = prefix[i-1] + nums[i-1]. Each query: return prefix[right+1] - prefix[left]
    │   └── Contiguous Array (LC 525) `⚡ T1` [M]
    │       → Prefix sum with 0→−1 transform + first-occurrence hash map: Seed seen = {0: -1}. For each index i, update running. If running in seen, candidate length = i - seen[running]. Else store seen[running] = i. Never overwrite (want earliest occurrence for max length)
    ├── Two-pass / Greedy
    │   ├── Jump Game (LC 55) `🎯 T2` [M]
    │   │   → Greedy — track farthest reachable index: reach = 0. For each i in 0..n-1: if i > reach, return False. Update reach = max(reach, i + nums[i]). If reach >= n-1 at any point, return True
    │   └── Gas Station (LC 134) `🎯 T2` [M]
    │       → Greedy — reset start on deficit: total = 0, tank = 0, start = 0. For each i: tank += gas[i] - cost[i], total += gas[i] - cost[i]. If tank < 0, set start = i + 1, reset tank = 0. Return start if total >= 0 else -1
    ├── Matrix `⚡ T1`
    │   ├── Rotate Image (LC 48) [M]
    │   │   → Transpose then reverse each row: Transpose: for i in range(n): for j in range(i+1, n): swap matrix[i][j] and matrix[j][i]. Reverse: for row in matrix: row.reverse()
    │   └── Search a 2D Matrix (LC 74) [M]
    │       → Binary search treating the matrix as a flat sorted array: lo=0, hi=m*n-1. At each mid: val = matrix[mid//n][mid%n]. Compare with target; adjust lo/hi accordingly
    ├── Intervals `🎯 T2`
    │   ├── Merge Intervals (LC 56) `🎯 T2` [M]
    │   │   → Sort by start, linear merge scan: Sort by start. Initialize merged = [intervals[0]]. For each subsequent interval: if interval.start <= merged[-1].end, merge by updating merged[-1].end = max(merged[-1].end, interval.end). Else append
    │   ├── Insert Interval (LC 57) `🎯 T2` [M]
    │   │   → Three-phase linear scan: before, overlap, after: Phase 1: while intervals[i].end < new.start, append. Phase 2: while intervals[i].start <= new.end, extend new.start = min(new.start, ...) and new.end = max(new.end, ...). Append merged. Phase 3: append remaining
    │   └── Non-overlapping Intervals (LC 435) `🎯 T2` [M]
    │       → Greedy — sort by end, keep earliest-ending non-conflicting interval: Sort by end. prev_end = -inf, kept = 0. For each interval: if start >= prev_end, keep it (kept++, update prev_end = end). Else skip (remove it). Answer = n - kept
    └── Prefix Sum
        ├── Subarray Sum Equals K (with negative numbers) `⚡ T1` [M]
        │   → Initialize map with {0: 1} (empty prefix). Walk the array accumulating running_sum; add count_map[running_sum - k] to the answer; then increment count_map[running_sum]
        ├── Contiguous Array (Equal 0s and 1s) `⚡ T1` [M]
        │   → Initialize {0: -1}. For each index, compute prefix sum (treating 0 as -1). If seen before, update max_len = max(max_len, i - first_seen[prefix]). Otherwise, store first_seen[prefix] = i
        └── Product of Array Except Self (no division) `🎯 T2` [M]
            → output[i] after left pass = product of nums[0..i-1]. Then walk right to left with a right_product variable, multiply output[i] *= right_product, then right_product *= nums[i]
```


### graph.md

```
coding/data-structures/graph.md
└── graph.md
    ├── BFS on Graphs
    │   ├── Rotting Oranges `⚡ T1` [M]
    │   │   → Multi-source BFS — simultaneous spread from all rotten sources: Multi-source start avoids O(R × M×N) repeated BFS. Return max_time if fresh == 0, else -1
    │   ├── Number of Islands (BFS) `⚡ T1` [M]
    │   │   → Seed the queue with the trigger cell; mark visited on enqueue (not dequeue) to prevent duplicate entries. Mutating the grid avoids an extra visited array
    │   ├── Walls and Gates (LC 286) `⚡ T1` [M]
    │   │   → Only enqueue cells that are INF — this acts as the visited guard. The first time a room is reached is always via its nearest gate
    │   ├── 01 Matrix (LC 542) `⚡ T1` [M]
    │   │   → Initialize dist matrix with 0 for zeroes, INF for ones. Enqueue all zeroes at start. Only update a cell if current dist > neighbor dist + 1
    │   ├── Word Ladder `⚡ T1` [H]
    │   │   → BFS on implicit word graph — L×26 mutation enumeration: For each word dequeued, try all single-char mutations; if mutation == endWord, return. Otherwise enqueue if the word is still in the set and then delete it
    │   ├── Shortest Path in Binary Matrix `⚡ T1` [M]
    │   │   → BFS from (0,0) — 8-directional, mark on enqueue: Mark cells visited by setting to 1 as you enqueue (not after dequeue) to prevent duplicate enqueueing; return distance when (n-1, n-1) is dequeued
    │   └── Find if Path Exists in a Graph `⚡ T1` [M]
    │   │   → Union-Find — reachability in O(E α(N)): Path compression + union by rank for optimal performance
    ├── DFS on Graphs
    │   ├── Number of Islands `⚡ T1` [M]
    │   │   → DFS sinking — flood-fill each component, count triggers: Sinking avoids a separate visited array — the mutation is the visit mark. Increment count only on the initial call, not within DFS
    │   ├── Max Area of Island `⚡ T1` [M]
    │   │   → DFS returning component size — sink inline: max(dfs(r,c) for all r,c) — zero-cost for water cells
    │   ├── Surrounded Regions `⚡ T1` [M]
    │   │   → Reverse DFS — mark border-safe 'O's, then flip interior: Walk all 4 borders, DFS from each 'O' found there
    │   ├── Pacific Atlantic Water Flow `⚡ T1` [M]
    │   │   → Reverse BFS from both ocean borders — intersect reachable sets: Reverse BFS condition — expand to neighbors with height >= current height (uphill in the reverse direction)
    │   ├── All Paths From Source to Target `⚡ T1` [M]
    │   │   → DFS backtracking on DAG — no visited set needed: path.append(nei), recurse, path.pop()
    │   ├── Number of Provinces (LC 547) `⚡ T1` [M]
    │   │   → Use a visited array instead of mutating the matrix. The matrix is symmetric but you only need to follow one direction per city
    │   ├── Number of Enclaves (LC 1020) `⚡ T1` [M]
    │   │   → Walk all 4 borders; DFS from each '1' encountered, sinking to 0. After traversal, sum remaining 1-cells
    │   ├── Clone Graph `⚡ T1` [M]
    │   │   → DFS with original→clone map — register before recursing: Guard if n in visited: return visited[n] handles cycles. Register BEFORE recursing into neighbors
    │   └── Find Eventual Safe States `⚡ T1` [M]
    │       → Three-color DFS — 0=unvisited, 1=in-progress, 2=safe: Mark gray before recursing neighbors; mark black after all neighbors are confirmed safe
    ├── Topological Sort
    │   ├── Course Schedule `⚡ T1` [M]
    │   │   → Kahn's BFS topo sort — cycle detection via leftover nodes: If completed == numCourses, no cycle
    │   ├── Course Schedule II `⚡ T1` [M]
    │   │   → Kahn's topo sort — collect removal order: Append node to order as it's dequeued; return order or []
    │   ├── Alien Dictionary `⚡ T1` [H]
    │   │   → Edge extraction from adjacent word pairs + Kahn's topo sort: Invalid input detection — if word A is a prefix of word B but A appears after B (e.g., "abc" before "ab"), return "" immediately
    │   └── Minimum Number of Vertices to Reach All Nodes `⚡ T1` [M]
    │       → Nodes with in-degree 0 — the only possible starting set: Collect all destination nodes from edges — these have in-degree ≥ 1; return all nodes not in this set
    ├── Shortest Path / Weighted
    │   ├── Network Delay Time (Dijkstra's) `⚡ T1` [M]
    │   │   → Dijkstra's — min-heap SSSP with stale-entry skip: After Dijkstra, answer = max of all shortest distances; -1 if any node unreached
    │   ├── Swim in Rising Water `⚡ T1` [M]
    │   │   → Modified Dijkstra — minimize maximum edge weight (bottleneck path): The first time we reach (n-1,n-1), we have the answer
    │   ├── Cheapest Flights Within K Stops `⚡ T1` [M]
    │   │   → Bellman-Ford with k+1 rounds — copy dist array each round: Copy dist array each round to prevent using edges discovered in the same round (would allow more than 1 edge per round effectively)
    │   └── Path with Minimum Effort (LC 1631) `⚡ T1` [M]
    │   │   → First pop of (rows-1, cols-1) from the heap is the answer. Mark visited on pop to avoid reprocessing
    ├── Bipartite / Coloring
    │   └── Is Graph Bipartite? `⚡ T1` [M]
    │   │   → BFS 2-coloring — alternating colors, fail on same-color neighbor: Initialize all colors to -1 (uncolored). For each unvisited node, BFS assigning color 0; assign 1 - color[node] to unvisited neighbors; return False if neighbor has same color
    └── Advanced
    │   └── Redundant Connection `⚡ T1` [M]
    │   │   → Union-Find — first edge connecting already-connected nodes is redundant: For each edge (a, b): if union(a, b) returns False (same component), return [a, b]
```


### hashing.md

```
coding/data-structures/hashing.md
└── hashing.md
    ├── Complement Map
    │   ├── Two Sum `⚡ T1` [E]
    │   │   → Single pass. Before storing x, look up target - x. If found, return [seen[complement], i]. Store x → i after checking to avoid using the same index twice
    │   └── 3Sum (hash-based) `⚡ T1` [M]
    │   │   → Sort. Skip duplicate values of a. For the inner scan, use a seen set: if target - b in seen, record triplet; else add b to seen
    ├── Frequency Map
    │   ├── Group Anagrams `⚡ T1` [M]
    │   │   → For each string, compute tuple(sorted(s)) as key, append to defaultdict(list)
    │   ├── Find All Anagrams in a String `⚡ T1` [M]
    │   │   → Use two Counter maps (window and p). Track have = number of chars where window count equals p count. When have == len(p_count), record the start
    │   ├── Top K Frequent Elements `⚡ T1` [M]
    │   │   → Counter → buckets list of size n+1 where buckets[f] holds all numbers with frequency f. Iterate from index n down and collect until we have k elements
    │   └── Minimum Window Substring `⚡ T1` [H]
    │       → Expand right, update have when a char's count first meets requirement. Shrink left while have == need. Record minimum window during each valid state
    ├── Prefix Sum + Map
    │   ├── Subarray Sum Equals K `⚡ T1` [M]
    │   │   → Maintain running prefix sum. Before updating the map, check seen[prefix - k]. Initialize seen = {0: 1} to handle subarrays starting at index 0
    │   └── Contiguous Array (Max Equal 0/1 Subarray) `⚡ T1` [M]
    │   │   → Track running sum with 0→-1 transform. When prefix repeats, the subarray between the two occurrences has sum 0. Store first_seen = {0: -1} and compare i - first_seen[prefix]
    ├── Design
    │   ├── LRU Cache `🎯 T2` [M]
    │   │   → On get: look up node, move to front, return val. On put: if key exists update and move to front; else insert at front; if over capacity evict tail
    │   └── Insert Delete GetRandom O(1) `⚡ T1` [M]
    │   │   → Insert appends to list and stores index in map. Remove swaps target with last element, updates map for the moved element, pops the list, deletes map entry for removed value
    ├── Miscellaneous
    │   └── Longest Consecutive Sequence `⚡ T1` [M]
    │   │   → Build set. For each x, if x - 1 not in set, extend the chain x, x+1, x+2, ... while each successor is in the set
    └── Prefix Sum + Hashing
        └── Contiguous Array (LC 525) `⚡ T1` [M]
        │   → Initialize {0: -1}. For each index i, update prefix. If prefix is in the map, update max_len = max(max_len, i - first_seen[prefix]). Otherwise record first_seen[prefix] = i
```


### heap.md

```
coding/data-structures/heap.md
└── heap.md
    ├── Top-K Pattern
    │   ├── Kth Largest Element in a Stream `⚡ T1` [M]
    │   │   → On each add, push the new value. If heap size exceeds k, pop the minimum. Root is the answer in O(1); each insert is O(log k)
    │   ├── Last Stone Weight `⚡ T1` [M]
    │   │   → Pop twice, push abs(a - b) if non-zero. Repeat until one or zero stones remain
    │   ├── K Closest Points to Origin `⚡ T1` [M]
    │   │   → For each point compute x²+y². Push (-dist, x, y) onto a max-heap. If size exceeds k, pop the farthest. Remaining heap contains the k closest
    │   ├── Top K Frequent Elements `⚡ T1` [M]
    │   │   → Build Counter in O(n). Heap push (freq, num) for each unique num; pop when size > k. Alternatively, bucket sort by frequency for O(n)
    │   ├── Furthest Building You Can Reach `⚡ T1` [M]
    │   │   → For each upward jump, assign a ladder (push jump to heap). If ladders exhausted, pop the smallest ladder-jump, reclaim it as bricks. If bricks insufficient for the current jump, stop
    │   ├── Kth Largest Element in an Array `⚡ T1` [M]
    │   │   → For each number, push to heap. If heap exceeds size k, pop the minimum. Root after full pass is the answer in O(1)
    │   └── Top K Frequent Words `⚡ T1` [M]
    │       → Count with Counter, then ask for the k best items under that custom key. This is safer than hand-rolling a size-k heap because naive tuple ordering is easy to get wrong for ties
    ├── Scheduling / Reorganization
    │   ├── Task Scheduler `⚡ T1` [M]
    │   │   → Count frequencies. Compute max_freq. The formula models "frames" of size n+1 with the most frequent task anchoring each frame. Return max(formula, len(tasks))
    │   └── Reorganize String `⚡ T1` [M]
    │       → Impossible if max_freq > (len(s) + 1) // 2. Otherwise, greedily fill from the heap
    ├── Two Heaps
    │   ├── Find Median from Data Stream `⚡ T1` [M]
    │   │   → Always push to lo, then move lo's max to hi to maintain order. Rebalance sizes so lo is never smaller than hi. Median is either lo[0] or the average of both tops
    │   ├── Sliding Window Median `⚡ T1` [H]
    │   │   → Maintain lo (max-heap) and hi (min-heap). Slide window: add new element, mark removed element as "invalid". Rebalance heaps. When reading tops, skip invalid elements
    │   └── IPO (Maximize Capital) `⚡ T1` [M]
    │       → Sort zip(capital, profits) by capital. Use a pointer i advancing when projects[i][0] <= w. Max-heap holds unlocked profits (negated). Repeat k times
    ├── K-Way Merge
    │   ├── Merge K Sorted Lists `⚡ T1` [H]
    │   │   → Seed heap with head of each non-null list. Use list_id as tie-breaker to avoid comparing ListNode objects (not comparable in Python)
    │   ├── Find K Pairs with Smallest Sums `⚡ T1` [M]
    │   │   → Pop smallest (sum, i, j), record pair. Push (nums1[i] + nums2[j+1], i, j+1) if j+1 < len(nums2). Stop after k pops
    │   └── Kth Smallest Element in a Sorted Matrix `⚡ T1` [M]
    │   │   → Push (matrix[i][0], i, 0) for all i. Pop k-1 times advancing (matrix[i][j+1], i, j+1). The k-th pop is the answer
    ├── Dijkstra / Graph
    │   ├── Network Delay Time `⚡ T1` [M]
    │   │   → Build adjacency list. Push (0, k). Pop min dist node; skip if already visited. Relax neighbors. Track visited set. Answer = max(dist.values()) if len(dist) == n else -1
    │   ├── Path with Minimum Effort `⚡ T1` [M]
    │   │   → Push (0, 0, 0). For each pop, update neighbors with max(effort, abs diff). Skip if already visited at a better effort
    │   └── Swim in Rising Water `⚡ T1` [M]
    │       → Push (grid[0][0], 0, 0). Pop min elevation; if it's the destination return it. Mark visited. Push unvisited neighbors with max(current_t, grid[nr][nc])
    ├── Design
    │   └── Ugly Number II `⚡ T1` [M]
    │       → Push 1. Pop min (= current ugly). Push val*2, val*3, val*5 if not seen. Repeat n times
    └── Heap Applications
        └── Reorganize String (LC 767) `⚡ T1` [M]
        │   → Alternate approach (cleaner): pop the top character, append it, push the previous character back (if count > 0). This naturally avoids placing the same character twice in a row
```


### linked-list.md

```
coding/data-structures/linked-list.md
└── linked-list.md
    ├── In-Place Reversal
    │   ├── Reverse Linked List `🎯 T2` [E] ★
    │   │   → Three-pointer iterative reversal: Save nxt = curr.next before overwriting. Set curr.next = prev. Advance prev = curr, curr = nxt. When curr is None, prev is the new head. Watch the order carefully: save next before rewiring or you lose the rest of the list
    │   ├── Reverse Linked List II `🎯 T2` [E]
    │   │   → Find pre-node + in-place splice-reversal: Each iteration: save nxt = curr.next, detach nxt from its position, reattach it after pre. This inserts nodes one by one at the front of the reversed section. After right - left iterations, the segment is reversed. If left == right, the loop runs zero times and the list stays unchanged
    │   ├── Palindrome Linked List `🎯 T2` [M]
    │   │   → Find middle + reverse second half + compare: Slow/fast to find middle. If the list has odd length, advance slow one more step to skip the middle node. Reverse from that point onward. Walk two pointers — one from head, one from reversed head — checking values. Restore (optional): reverse second half back
    │   └── Reorder List `🎯 T2` [M] ★
    │   │   → Find middle + reverse second half + interleave: Slow/fast to find mid. Reverse second half. Merge two halves alternating: take one from first, one from second (reversed), repeat until second half is exhausted
    ├── Fast / Slow Pointers
    │   ├── Linked List Cycle `⚡ T1` [M]
    │   │   → Floyd's fast/slow pointer cycle detection: Start both at head. Loop: slow = slow.next, fast = fast.next.next. Check slow is fast (identity, not equality). If fast or fast.next is None, exit — no cycle. The identity check matters whenever node values can repeat
    │   └── Remove Nth Node From End of List `🎯 T2` [M]
    │   │   → Two pointers with N+1 gap: Dummy → head. Advance fast by n+1 steps. Then while fast: slow=slow.next, fast=fast.next. Now slow is the predecessor of the node to delete. slow.next = slow.next.next
    ├── Floyd's Cycle Detection
    │   ├── Linked List Cycle II `⚡ T1` [M]
    │   │   → Floyd's two-phase cycle entry detection: Phase 1 — slow and fast meet after slow travels distance d+c, fast travels d+c+L (one full cycle extra), where d = head-to-entry, c = entry-to-meeting, L = cycle length. This implies d = L - c = d' (distance from meeting point back to entry). Phase 2 — slow resets to head, both advance 1 step at a time → they meet at the entry
    │   └── Find the Duplicate Number (Floyd's variant) `🎯 T2` [M]
    │       → Floyd's on implicit linked list defined by array values: Identical to Linked List Cycle II but operating on array indices. slow = nums[slow], fast = nums[nums[fast]]. After meeting, reset slow = nums[0] (not 0, because the linked list starts from nums[0])
    ├── Merge / Sorting `🎯 T2`
    │   ├── Merge Two Sorted Lists `🎯 T2` [M]
    │   │   → Dummy head + two-pointer merge: dummy → result chain. curr pointer builds the result. While both l1 and l2 non-null: attach smaller, advance it. After loop, attach the non-null remainder
    │   ├── Merge K Sorted Lists `⚡ T1` [H]
    │   │   → Min-heap of size k: Initialize heap with heads of all non-null lists. While heap non-empty: pop min node, attach to result, push node.next if non-null
    │   ├── Sort List `🎯 T2` [M]
    │   │   → Bottom-up merge sort on linked list: For each sublist size size = 1, 2, 4, 8, ...: split list into pairs of size-length sublists, merge each pair, connect results. One full pass per doubling of size, log n passes total. This is the version interviewers like when they explicitly ask for O(1) extra space
    │   └── Insertion Sort List `🎯 T2` [M]
    │       → Dummy head + find-insertion-point per node: Detach each node from the original list. Walk the sorted prefix from dummy until prev.next.val > node.val or prev.next is None. Insert node between prev and prev.next. If the input is nearly sorted, this often behaves closer to linear time
    ├── Copy / Design
    │   ├── Copy List with Random Pointer `🎯 T2` [M]
    │   │   → Hash map original→clone, two-pass wiring: Pass 1: iterate and create {node: ListNode(node.val)} for all nodes. Pass 2: for each original node, set clone.next = map[node.next], clone.random = map[node.random]. Mapping None → None keeps the wiring concise
    │   └── LRU Cache `🎯 T2` [M]
    │       → Doubly linked list + hash map: Dummy head and dummy tail eliminate all edge cases in _remove and _insert_front. On get: remove from current position, insert at front, return value. On put: if key exists, remove old; create new node, insert at front, update map; if over capacity, remove LRU (tail.prev), delete from map
    └── Design
        └── LRU Cache (Doubly Linked List + Hash Map) `🎯 T2` [M] ★
            → get: if key missing return -1, else move node to front and return value. put: if key exists update value and move to front; if new key and at capacity, remove the node just before the tail (LRU), then insert new node at front
```


### queue.md

```
coding/data-structures/queue.md
└── queue.md
    ├── Monotonic Deque
    │   ├── Sliding Window Maximum `⚡ T1` [H]
    │   │   → EDGE CASES:: For each index i — (1) evict from the back any index whose value ≤ nums[i] (they are dominated and can never be future maxima; using <= also drops older duplicates); (2) evict from the front if it has fallen outside the window; (3) append i; (4) once i >= k-1, the front of the deque is the answer. Each index is enqueued and dequeued at most once → O(n) total. - EDGE CASES: k = 1 returns the original array; k = len(nums) returns a single maximum
    │   └── Jump Game VI (DP + Sliding Window Max) `🎯 T2` [M]
    │   │   → dp[i] = nums[i] + max(dp[j] for j in range(max(0, i-k), i)). Use a deque of indices in decreasing dp value order. Before computing dp[i], evict indices outside the window [i-k, i-1] from the front. The front of the deque is argmax dp in the window
    ├── BFS / Level-order
    │   ├── Binary Tree Level Order Traversal `🎯 T2` [M]
    │   │   → Enqueue root. At the start of each BFS iteration snapshot size = len(queue). Dequeue exactly size nodes, collect their values, enqueue their children. Append the level list to results
    │   ├── Binary Tree Zigzag Level Order Traversal `🎯 T2` [M]
    │   │   → Toggle left_to_right after each level. When False, reverse the collected level list. Children are always enqueued left-to-right; only the output list is reversed
    │   └── Binary Tree Right Side View `🎯 T2` [M]
    │       → Standard level-size snapshotting. After processing all nodes in a level, the most recently processed node value is the rightmost — append it to results
    ├── BFS Multi-Source
    │   ├── Rotting Oranges `⚡ T1` [M]
    │   │   → Count fresh oranges. Run BFS — each time a fresh orange is infected, decrement fresh count and enqueue the new cell with time + 1. After BFS, if fresh > 0, return -1 (blocked cells remain). Otherwise return the last timestamp used
    │   ├── 01 Matrix `⚡ T1` [M]
    │   │   → Initialize all 0 cells with distance 0 in the queue. Initialize all 1 cells with inf. BFS outward — first time a 1 cell is reached sets its distance. BFS guarantees minimum distance
    │   ├── Walls and Gates `⚡ T1` [M]
    │   │   → Enqueue all cells with value 0 (gates). BFS outward — each INF cell reached gets distance = parent's distance + 1. Walls (-1) are never enqueued or updated
    │   └── Shortest Path in Binary Matrix `⚡ T1` [M]
    │   │   → If start or end is 1, return -1 immediately. BFS with 8 directions. The first time (n-1, n-1) is dequeued, return the current distance + 1
    ├── BFS Single-Source
    │   ├── Word Ladder `⚡ T1` [H]
    │   │   → Enqueue (beginWord, 1). For each dequeued word, generate all one-letter variants; if a variant is in the word set, enqueue it with distance + 1 and remove from the set. Return the distance when endWord is reached
    │   ├── Cheapest Flights Within K Stops `⚡ T1` [M]
    │   │   → Use Bellman-Ford with exactly k+1 relaxation rounds. Maintain prices[node] = cheapest price to reach node using at most current_round hops. Use a copy of prices per round to avoid using within-round updates
    │   └── Jump Game III `🎯 T2` [M]
    │       → Enqueue start. For each index, compute both jump targets. If in bounds and unvisited, enqueue. Return True immediately if a target index has value 0
    ├── Topological Sort (Kahn's BFS)
    │   ├── Course Schedule `⚡ T1` [M]
    │   │   → Build adjacency list and in-degree array. Enqueue all nodes with in-degree 0. For each dequeued node, decrement neighbors' in-degrees; enqueue any that reach 0. Count processed nodes — if count equals numCourses, return True
    │   ├── Course Schedule II `⚡ T1` [M]
    │   │   → Append each dequeued node to order. If len(order) == numCourses, the graph is a DAG and order is a valid schedule. Otherwise return []
    │   └── Alien Dictionary `⚡ T1` [H]
    │       → For each adjacent word pair, find the first differing character — that gives an edge. If word A is a prefix of word B but appears after B, return "" (invalid). Run Kahn's BFS. If all characters are processed, the BFS output is the alien alphabet order
    ├── Priority Queue / Heap
    │   ├── Task Scheduler `⚡ T1` [M]
    │   │   → Build frequency map; push all (-count,) entries to the heap. At each time tick: if the cooldown queue front is ready (available_at <= time), push it back onto the heap. If the heap is non-empty, pop and execute the most frequent task, push it to the cooldown queue with updated count. Otherwise, idle. Increment time
    │   └── Find Median from Data Stream `⚡ T1` [M]
    │       → addNum: push to lo (negate for max-heap), then balance by moving lo's max to hi if lo[0] > hi[0] or sizes diverge. Rebalance so lo is never smaller than hi
    ├── Sliding Window with Queue
    │   └── Sliding Window Median (LC 480) `⚡ T1` [M]
    │       → Lazy deletion: track counts of "dead" elements in each heap. When computing the median, first pop any dead elements from the heap tops. Balance rule: len(lo) == len(hi) or len(lo) == len(hi) + 1
    └── Scheduling
        └── Task Scheduler with Cooldown (LC 621) `⚡ T1` [M]
            → Count frequencies with a Counter. max_freq = highest frequency. max_count = number of tasks that share that frequency. Formula accounts for max_freq - 1 complete cycles, each of length n+1, plus the final partial cycle of max_count tasks
```


### segment-tree.md

```
coding/data-structures/segment-tree.md
└── segment-tree.md
    └── Segment Tree Applications
    │   └── Number of Longest Increasing Subsequence `🎯 T2` [M]
    │   │   → O(n²) DP is simple. Segment tree on values (coordinate compressed) can reduce to O(n log n): tree node stores (max_length, total_count) for values processed so far; query [0, nums[i]-1] for best, then update at nums[i]
```


### stack.md

```
coding/data-structures/stack.md
└── stack.md
    ├── Monotonic Stack — Next Greater/Smaller
    │   ├── Daily Temperatures `🎯 T2` [M]
    │   │   → Push index i onto the stack. When temps[i] > temps[stack[-1]], pop and record result[popped] = i - popped. Stack holds indices of temperatures that haven't yet seen a warmer day
    │   └── Next Greater Element II `🎯 T2` [M]
    │   │   → Initialize result = [-1] * n. Iterate 2n times. Use i % n to access elements. Only push i % n when i < n
    ├── Monotonic Stack — Histogram / Rectangle
    │   ├── Largest Rectangle in Histogram `🎯 T2` [M]
    │   │   → Append sentinel 0 to flush the stack. On pop, height = heights[popped]. Width = i - stack[-1] - 1 if stack is non-empty, else i (the bar is the global minimum so far)
    │   └── Trapping Rain Water (stack approach) `⚡ T1` [H]
    │       → Push indices onto a decreasing stack. On pop (taller bar arrived), compute bounded water above the popped bar
    ├── Valid Parentheses / Nesting `🎯 T2`
    │   ├── Valid Parentheses `🎯 T2` [M]
    │   │   → Map ')' → '(', etc. If stack is empty when closing bracket arrives, or top doesn't match, return False. Valid iff stack is empty at end
    │   ├── Decode String `🎯 T2` [M]
    │   │   → Parse digits to get k. On [: push (current_string, k), reset both. On ]: pop (prev_str, k), set current = prev_str + current * k. Characters append to current
    │   ├── Remove All Adjacent Duplicates in String [M]
    │   │   → Linear scan. Maintain stack. At each character, cancel with top if equal. Analogous to bracket matching
    │   └── Remove K Digits `🎯 T2` [M]
    │       → Build the stack left to right. Pop larger elements while k > 0. If k still > 0 after the loop, trim last k digits from the stack (which is already sorted ascending). Strip leading zeros
    ├── Stack Design
    │   └── Min Stack `🎯 T2` [M]
    │   │   → On push, min_stack pushes min(val, min_stack[-1]). On pop, both stacks pop. get_min returns min_stack[-1]
    ├── Simulation / Other
    │   └── Asteroid Collision `🎯 T2` [M]
    │       → While collision conditions hold: if top is smaller, pop (top destroyed, current continues); if equal, pop and break (both destroyed); if top is larger, break (current destroyed, don't append). Use while...else to append only if current survived
    ├── Monotonic Stack — Arrays and Sequences
    │   └── Car Fleet (LC 853) `🎯 T2` [M]
    │   │   → Iterate sorted arrival times. Push if > stack[-1] (or stack empty). Stack size = number of fleets
    └── Iterative Tree Traversal
    │   ├── Flatten Binary Tree to Linked List (LC 114 — iter... `🎯 T2` [M]
    │   │   → Push root. While stack: pop node, if node.right exists push it, if node.left exists push it. Set node.right = stack[-1] if stack else None, node.left = None
    │   └── Path Sum II (LC 113 — iterative DFS) `🎯 T2` [M]
    │       → Push (root, target, []). On each pop: if leaf and remaining == 0, add copy of path to results. Push right child, then left child (left processed first) with updated remaining and path
```


### string.md

```
coding/data-structures/string.md
└── string.md
    ├── Frequency Map / Anagram
    │   ├── Group Anagrams `⚡ T1` [M]
    │   │   → For each word, compute key = tuple(freq_array) or key = "".join(sorted(word)). Append word to groups[key]. Return list(groups.values())
    │   └── Find All Anagrams in a String `⚡ T1` [M]
    │       → Build p_freq. Maintain w_freq for the window. Add the incoming character on the right; evict the outgoing character on the left when the window exceeds len(p). If arrays match, record the left index. Use a matches counter to avoid O(26) comparison: track how many of the 26 buckets currently match between w_freq and p_freq
    ├── Two Pointers — Palindrome
    │   └── Longest Palindromic Substring `🎯 T2` [M]
    │   │   → expand(l, r) expands while s[l] == s[r] and indices are in bounds, returning the palindrome substring. For each index i, try both expand(i, i) (odd length) and expand(i, i+1) (even length). Track the longest result
    ├── Sliding Window `⚡ T1`
    │   ├── Longest Substring Without Repeating Characters `⚡ T1` [M]
    │   │   → For each right: if s[right] is in the set, remove s[left] and advance left until the duplicate is gone. Then add s[right] and update max
    │   ├── Minimum Window Substring `⚡ T1` [H]
    │   │   → Expand right: add s[right] to have; if have[c] == need[c], increment formed. When formed == len(need) (window valid): record min window, shrink from left — decrement have[s[left]]; if it drops below need[s[left]], decrement formed. Repeat shrinking until no longer valid
    │   └── Longest Repeating Character Replacement `⚡ T1` [M]
    │       → Expand right: update count[s[right]] and max_freq. If (window_size - max_freq) > k, slide left by 1 — don't shrink, just slide. The window grows when a valid longer window is found
    ├── Prefix Sum on Characters
    │   └── Subarray Sum Equals K (character version) `⚡ T1` [M]
    │       → For each character ch: running += (1 if ch == target else 0). count += prefix_count[running - k]. prefix_count[running] += 1
    ├── Encoding / Hashing
    │   └── Encode and Decode Strings `🎯 T2` [M]
    │   │   → Encode: for each string, emit str(len(s)) + '#' + s. Decode: read digits up to # to get length L; read exactly L characters as the next string; advance pointer past them; repeat
    └── Parsing / Simulation (Extended)
    │   └── Decode String `🎯 T2` [M]
    │   │   → Two stacks (count_stack, string_stack) or a single character stack. On digit: accumulate k. On [: push current string and k onto stacks, reset. On ]: pop string and k, append k * current_string to the popped prefix
```


### tree.md

```
coding/data-structures/tree.md
└── tree.md
    ├── DFS Traversal
    │   ├── Invert Binary Tree `🎯 T2` [M]
    │   │   → Post-order recursive swap: Base case not root → None. Recurse left and right, then swap: root.left, root.right = invertTree(root.right), invertTree(root.left). Pre-order also works since swapping is an O(1) local operation
    │   ├── Symmetric Tree `🎯 T2` [M]
    │   │   → Recursive mirror(l, r) — outer and inner pair matching: Base cases: both None → True (symmetric absence), exactly one None → False. Otherwise: l.val == r.val and mirror(l.left, r.right) and mirror(l.right, r.left)
    │   ├── Maximum Depth of Binary Tree `🎯 T2` [M]
    │   │   → Post-order recursive max height: Base case not root → 0; otherwise 1 + max(maxDepth(left), maxDepth(right))
    │   ├── Path Sum `🎯 T2` [M]
    │   │   → DFS subtracting current value — check at leaf: The leaf check is critical — only return True at nodes where not left and not right (both children null), not at any node where partial sum matches
    │   ├── Path Sum II `🎯 T2` [M]
    │   │   → At leaf (not left and not right) and remaining == 0: result.append(list(path)) (copy! not reference). Then path.pop() on return regardless of whether this was a leaf
    │   ├── Count Good Nodes in Binary Tree `🎯 T2` [M]
    │   │   → DFS with propagated path_max: Update path_max = max(path_max, node.val) before recursing; root is always good
    │   └── Flatten Binary Tree to Linked List `🎯 T2` [M]
    │   │   → Morris-style in-place threading — find inorder predecessor: For each curr with a left child: find rightmost node in left subtree (prev), wire prev.right = curr.right, move curr.right = curr.left, null curr.left. Advance curr = curr.right
    ├── Level Order BFS
    │   ├── Binary Tree Level Order Traversal `🎯 T2` [M]
    │   │   → BFS with level-size snapshot: Inner loop runs exactly level_size times; enqueue children during inner loop; append collected level after inner loop
    │   ├── Binary Tree Zigzag Level Order Traversal `🎯 T2` [M]
    │   │   → left_to_right = True initially; after collecting each level: if not left_to_right, level.reverse(); then left_to_right = not left_to_right
    │   ├── Binary Tree Right Side View `🎯 T2` [M]
    │   │   → BFS — capture last node per level: Snapshot level size; run inner loop; append value only when i == level_size - 1
    │   ├── Populating Next Right Pointers in Each Node `🎯 T2` [M]
    │   │   → O(1) space — walk current level to connect next level: Start with leftmost = root; inner loop walks the current level using head.next; outer loop descends via leftmost = leftmost.left
    │   ├── Vertical Order Traversal of a Binary Tree `🎯 T2` [M]
    │   │   → DFS collect (col, row, val) tuples, sort, group: DFS assigning (row, col) to each node, collect all tuples, sort, then group by column
    │   └── All Nodes Distance K in Binary Tree `🎯 T2` [M]
    │       → Build undirected graph, BFS k steps from target: Build graph first, BFS second, collect nodes at distance == k
    ├── Lowest Common Ancestor `🎯 T2`
    │   ├── Lowest Common Ancestor of a Binary Tree `🎯 T2` [M]
    │   │   → Post-order recursion — converge at split node: if left and right: return root; return left or right
    │   └── Lowest Common Ancestor of a BST [M]
    │       → Iterative BST-guided descent — O(h) instead of O(n): If both p, q < root, go left. If both > root, go right. Otherwise return root
    ├── Tree DP
    │   ├── Diameter of Binary Tree `🎯 T2` [M]
    │   │   → Post-order height DFS with global diameter update: Return 1 + max(left, right) upward; update best[0] with l + r at each node
    │   ├── Binary Tree Maximum Path Sum `🎯 T2` [H]
    │   │   → Post-order gain DFS — clamp negatives to 0: gain(node) = node.val + max(l, r) returned upward; global update = node.val + l + r (where l and r already have negatives clamped to 0)
    │   ├── House Robber III `🎯 T2` [M]
    │   │   → Post-order DP returning (rob, skip) pair: rob = node.val + l_skip + r_skip; skip = max(l_rob, l_skip) + max(r_rob, r_skip). Post-order: compute children first
    │   └── Path Sum III `🎯 T2` [M]
    │       → DFS with prefix sum hash map + backtracking: DFS — add node.val to running sum, query map for running_sum - targetSum, increment map, recurse children, then decrement map on backtrack (critical: prevents prefix sum from leaking into sibling branches)
    ├── BST Operations
    │   ├── Validate Binary Search Tree `🎯 T2` [M]
    │   │   → Recursive range validation — propagate (lo, hi) bounds: validate(node, lo, hi) — fail if not lo < node.val < hi, else recurse with tightened bounds
    │   └── Kth Smallest Element in a BST `🎯 T2` [M]
    │   │   → Iterative inorder with early exit at k: while stack or root: push all left children, pop, decrement k, if k == 0 return val, else advance to right child
    └── Construction / Serialization
    │   ├── Serialize and Deserialize Binary Tree `🎯 T2` [H]
    │   │   → Preorder DFS with null markers — iterator-based deserialization: Serialize: DFS pre-order appending values or #. Deserialize: iterate tokens; # → return None; otherwise create node, recurse left, recurse right. Use an iterator to advance position across recursive calls
    │   └── Construct Binary Tree from Preorder and Inorder T... `🎯 T2` [M]
    │   │   → Preorder index advance + inorder hash map for O(1) root lookup: build(in_left, in_right) — take preorder[pre_idx] as root, find its inorder position mid, build left subtree with in_left..mid-1, right subtree with mid+1..in_right
```


### trie.md

```
coding/data-structures/trie.md
└── trie.md
    ├── Core Trie Implementation
    │   └── Implement Trie (Prefix Tree) `⚡ T1` [M]
    │       → EDGE CASES:: - insert: walk the tree character by character, creating nodes as needed, set is_end = True at the last character. - search: walk the tree; return False if any character is missing; return node.is_end at the end — this distinguishes "apple" (exact) from "app" (only prefix). - startsWith: same walk as search but return True after the walk completes regardless of is_end. - EDGE CASES: The empty string is valid only if you explicitly mark the root as terminal; duplicate inserts are idempotent with a boolean trie; deletes must prune only dead branches so shared prefixes stay intact
    ├── Autocomplete / Prefix Search
    │   └── Replace Words `⚡ T1` [M]
    │       → Insert all roots into the trie. For each word in the sentence, walk the trie; if is_end is reached at depth d, replace the word with word[:d]. If the walk exits without finding a root, keep the original word
    ├── Trie + Backtracking
    │   └── Word Search II `⚡ T1` [H]
    │   │   → Build trie, storing the actual word string at is_end nodes. DFS: if ch not in node.children, return immediately. If node.word is set, record and clear it (deduplication). Mark cell as '#' during DFS; restore on backtrack. After DFS, prune dead trie nodes (del node.children[ch] when subtree is empty) to avoid re-exploring exhausted branches
    ├── Core Trie Operations (Extended)
    │   └── Add and Search Word `⚡ T1` [M]
    │       → addWord: standard trie insert. search(word, node, i): if i == len(word) return node.is_end. If word[i] == '.', recurse into every child and return True if any succeeds. Otherwise follow the exact child as usual
    ├── Prefix Problems
    │   └── Search Suggestions System `⚡ T1` [M]
    │   │   → Sort products. Insert each: at every node on the path, append the word to node.suggestions if len < 3. Query: walk the search word prefix character by character; at each step return node.suggestions (or [] if the branch doesn't exist, and stay dead for subsequent characters)
    ├── Suffix Trie / Advanced
    │   └── Implement Trie II (Count Operations) `⚡ T1` [M]
    │   │   → insert: walk, incrementing node.pass_count at every node, node.end_count at terminal. countWordsStartingWith(prefix): walk to prefix node, return node.pass_count. countWordsEqualTo(word): walk to terminal, return node.end_count. erase(word): walk, decrementing node.pass_count; decrement node.end_count at terminal. Optionally prune nodes where pass_count == 0
    └── Trie Applications
        └── Replace Words (LC 648) `⚡ T1` [M]
        │   → Insert all roots. For each sentence word, traverse the trie; if a node has is_end = True, return the prefix built so far. If traversal ends without a match, keep the original word
```


## coding/algorithms/


### backtracking.md

```
coding/algorithms/backtracking.md
└── backtracking.md
    ├── Subsets / Combinations `🎯 T2`
    │   ├── Subsets (Power Set) `🎯 T2` [M]
    │   │   → Record subset at every node (not just leaves) — each partial path is itself a valid subset
    │   ├── Subsets II (with duplicates) `🎯 T2` [M]
    │   │   → Same structure as Subsets but with if i > start and nums[i] == nums[i-1]: continue
    │   ├── Combination Sum (unbounded) `🎯 T2` [M]
    │   │   → Recurse with bt(i, remaining - candidates[i]) — same i, not i+1
    │   ├── Combination Sum II (0/1 — no reuse) `🎯 T2` [M]
    │   │   → if i > start and candidates[i] == candidates[i-1]: continue
    │   ├── Combinations `🎯 T2` [M]
    │   │   → Pruning: if n - i + 1 < k - len(path): break — not enough numbers remain
    │   └── Letter Combinations of a Phone Number `🎯 T2` [M]
    │       → Base case: d == len(digits) → record. No pruning needed — every path is valid
    ├── Permutations `🎯 T2`
    │   ├── Permutations `🎯 T2` [M]
    │   │   → Base case: len(path) == n. No pruning — every branch leads to a valid permutation
    │   ├── Permutations II (with duplicates) `🎯 T2` [M]
    │   │   → if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue
    │   ├── Next Permutation (iterative approach) [M]
    │   │   → If no pivot found (fully descending), entire array is reversed
    │   └── Letter Case Permutation [M]
    │       → String building via list (mutable); convert at leaf
    ├── String Backtracking
    │   ├── Generate Parentheses `🎯 T2` [M]
    │   │   → Leaf count = Catalan number C(n). The invariant close < open ensures every partial string is a valid prefix
    │   ├── Palindrome Partitioning `🎯 T2` [M]
    │   │   → Precompute is_pal[i][j] via DP in O(n²). Then backtracking is O(2^n) calls × O(1) palindrome check
    │   ├── Remove Invalid Parentheses `🎯 T2` [H]
    │   │   → Compute open_rem, close_rem first; backtrack with those exact budgets
    │   └── Word Search `🎯 T2` [M]
    │   │   → Early return True on complete match. Board is restored on each backtrack
    ├── Board / Matrix Backtracking
    │   ├── N-Queens `🎯 T2` [M]
    │   │   → Add to sets before recursing; remove after. Leaf (row==n) records the board
    │   ├── Sudoku Solver `🎯 T2` [H]
    │   │   → box_id = (r//3)*3 + c//3. Linear scan for next empty cell at each recursion level
    │   └── Unique Paths III `🎯 T2` [M]
    │       → Track remaining count of unvisited non-obstacle cells. Prune when stuck (all 4 neighbors blocked and remaining > 1)
    ├── Trie + Backtracking
    │   └── Word Search II `⚡ T1` [H]
    │       → Key optimizations: (1) Delete found words from Trie (node.word = None) to avoid duplicates. (2) Prune empty Trie nodes (del node[ch] after DFS) — reduces future DFS calls significantly
    ├── Constraint Satisfaction / Pruning-Heavy
    │   ├── Combination Sum III `🎯 T2` [M]
    │   │   → Because the domain is tiny (1-9), no sorting needed — it's inherently sorted. Upper bound prune: if remaining > sum(range(start, 10))[:k-len(path)], stop
    │   ├── Target Sum `🎯 T2` [M]
    │   │   → Backtracking here: O(2^n). DP reduction: let P = sum of positives, N = sum of negatives. P - N = target, P + N = total → P = (target + total) / 2. Count subsets summing to P
    │   └── Restore IP Addresses `🎯 T2` [M]
    │       → After choosing 4 segments, the entire string must be consumed. Feasibility check: remaining_digits must be between remaining_segments and 3 * remaining_segments
    ├── String Backtracking (continued)
    │   ├── Word Break II `🎯 T2` [M]
    │   │   → Memoization key is start index. Value is list of sentence suffixes from that position. Build full sentences by prepending current word
    │   └── Palindrome Partitioning II (Minimum Cuts) `🎯 T2` [M]
    │       → WHAT (DP):: dp[0] = 0 (empty prefix needs 0 cuts). Final answer: dp[n] - 1 (subtracting the artificial initial cut). Equivalently, dp[i] = min cuts for first i chars → dp[n]
    ├── Grid Traversal
    │   └── Word Search (All Occurrences) `🎯 T2` [M]
    │       → Each DFS is independent — board restored fully between starting cells. Use in-place '#' marking within a single DFS call
    ├── Advanced Backtracking
    │   └── Word Break (Decision — Backtracking + Memo) `🎯 T2` [M]
    │   │   → Check only words in the dictionary (not all prefixes). Short-circuit on first True. BFS or DP are preferred in interviews
    └── Backtracking — Hard Problems
        └── Remove Invalid Parentheses (LC 301) `🎯 T2` [H]
            → is_valid(s): count open brackets, decrement on ), return false if count < 0, return count == 0 at end
```


### binary-search.md

```
coding/algorithms/binary-search.md
└── binary-search.md
    ├── Lower Bound / Upper Bound
    │   ├── Search Insert Position (LC 35) `⚡ T1` [M]
    │   │   → If nums[mid] < target → lo = mid + 1; else hi = mid. Loop terminates at lo == hi
    │   └── First Bad Version (LC 278) `⚡ T1` [M]
    │   │   → if isBadVersion(mid): hi = mid (don't discard mid); else lo = mid + 1. Terminates at lo == hi
    ├── Binary Search on Answer (Predicate Pattern)
    │   ├── Koko Eating Bananas (LC 875) `⚡ T1` [M]
    │   │   → ceil(p/k) without math.ceil → -(-p // k). If feasible → hi = mid (try slower); else lo = mid + 1
    │   ├── Capacity To Ship Packages Within D Days (LC 1011) `⚡ T1` [H]
    │   │   → Greedy feasibility: greedily fill each day; when adding next weight exceeds capacity, start a new day
    │   ├── Split Array Largest Sum (LC 410) `⚡ T1` [H]
    │   │   → Greedily extend current subarray; when adding next element would exceed max_sum, start new part. If parts ≤ k → feasible
    │   └── Minimum Speed to Arrive on Time (LC 1870) `⚡ T1` [M]
    │       → Early exit: if hour <= n - 1, impossible (each of n-1 waits costs at least 1 hour)
    ├── Rotated Sorted Array `⚡ T1`
    │   ├── Search in Rotated Sorted Array (LC 33) `⚡ T1` [M]
    │   │   → If nums[lo] <= nums[mid], left half [lo, mid] is sorted. If target in [nums[lo], nums[mid]) → go left; else go right
    │   ├── Find Minimum in Rotated Sorted Array (LC 153) `⚡ T1` [M]
    │   │   → if nums[mid] > nums[hi]: lo = mid + 1 else hi = mid. Do NOT compare with nums[lo]
    │   ├── Search in Rotated Sorted Array II (LC 81) `⚡ T1` [M]
    │   │   → On ambiguity → lo += 1; hi -= 1. Worst case O(n) for all-same arrays
    │   └── Find Minimum in Rotated Sorted Array II (LC 154) `⚡ T1` [M]
    │       → Three-way branch on nums[mid] vs nums[hi]
    ├── Peak Element `⚡ T1`
    │   ├── Find Peak Element (LC 162) `⚡ T1` [M]
    │   │   → if nums[mid] < nums[mid+1]: lo = mid + 1 else hi = mid. Terminates at lo == hi which is a peak
    │   ├── Peak Index in a Mountain Array (LC 852) [M]
    │   │   → Same code as LC 162; mountain guarantee makes the result unique
    │   └── Find a Peak Element in a 2D Grid (LC 1901) [M]
    │       → If mat[max_row][mid_col] < mat[max_row][mid_col+1] → a peak exists to the right; else left or at mid
    ├── Median / Order Statistics
    │   ├── Median of Two Sorted Arrays (LC 4) `⚡ T1` [H]
    │   │   → If max_left1 > min_right2 → partition too far right in nums1 → hi = i - 1; else lo = i + 1
    │   └── Kth Smallest Element in a Sorted Matrix (LC 378) `⚡ T1` [M]
    │   │   → Start top-right. If matrix[row][col] <= d → all col+1 elements in this row qualify → row += 1; else col -= 1. If count ≥ k → hi = mid; else lo = mid + 1. Answer is always an actual matrix element
    ├── Classic / Miscellaneous
    │   ├── Minimum Number of Days to Make m Bouquets (LC 1482) `⚡ T1` [M]
    │   │   → Count bouquets formed; if >= m → feasible. Early exit: if m * k > len(bloomDay) → impossible
    │   └── Find K Closest Elements (LC 658) `⚡ T1` [M]
    │   │   → If x - arr[mid] > arr[mid+k] - x → window is too far left → lo = mid + 1; else hi = mid. Answer is arr[lo : lo + k]
    └── Second Occurrence / Exact Match Variants
        ├── Find the Duplicate Number (LC 287) — BS on Value `🎯 T2` [M]
        │   → if count > mid: hi = mid else lo = mid + 1. Not a standard in-place BS — it's BS on the value space, not the index space
        └── Longest Increasing Subsequence — Length via BS (L... `🎯 T2` [M]
            → If num > tails[-1] → append (extend LIS). Else → replace tails[pos] = num (maintain smallest tails for future options)
```


### bit-manipulation.md

```
coding/algorithms/bit-manipulation.md
└── bit-manipulation.md
    ├── Bitmask State Space Search
    │   └── Shortest Path with Keys and Locks [M]
    │       → Preprocess grid for start position, key count. BFS with state space O(R · C `⚡ T1`· 2^K). Goal: keys_mask == (1 << num_keys) - 1
    └── Encoding / Decoding with Bits
        └── Find the Duplicate Number (Bit Approach) `🎯 T2` [M]
            → Outer loop over 32 bit positions; inner loop counts set bits in nums and in range(1, n+1). If count_nums > count_range, set that bit in the answer
```


### divide-and-conquer.md

```
coding/algorithms/divide-and-conquer.md
└── divide-and-conquer.md
    ├── Classic D&C
    │   ├── Merge Two Sorted Lists `🎯 T2` [M]
    │   │   → Base: if either list is None, return the other. Compare l1.val vs l2.val; attach smaller, recurse
    │   ├── Merge K Sorted Lists `⚡ T1` [H]
    │   │   → While len(lists) > 1: pop two, merge them, push result back. Or recurse: merge(lists[:mid]) + merge(lists[mid:]) as left/right
    │   └── Median of Two Sorted Arrays `⚡ T1` [H]
    │   │   → Ensure A is shorter. Binary search lo to hi (size of A). At midpoint i, compute j. If A[i-1] > B[j], go left; if B[j-1] > A[i], go right; else compute median from boundary values
    ├── QuickSelect
    │   ├── Kth Largest Element in an Array `⚡ T1` [M]
    │   │   → Randomize pivot to avoid O(n²) worst case on sorted input. kth largest = (n-k)th index in 0-indexed sorted array
    │   ├── K Closest Points to Origin `⚡ T1` [M]
    │   │   → 2 + p[1]: Same partition logic; compare by dist(p) = p[0]2 + p[1]2. After QuickSelect, points[:k] are the answer
    │   └── Top K Frequent Elements `⚡ T1` [M]
    │       → freq = Counter(nums). Run QuickSelect on list(freq.keys()) comparing by freq[key]. Target index = n - k
    ├── Merge Sort Variants (D&C with Counting) `🎯 T2`
    │   ├── Count of Smaller Numbers After Self [M]
    │   │   → Track right_picked count during merge. Each time a right element is chosen over remaining left[i:] elements, increment counts[left[i].index]
    │   ├── Reverse Pairs [M]
    │   │   → Two-pointer count: for each left[i], advance j while left[i] > 2 * right[j]; add j to total. Then perform standard merge
    │   ├── Count of Range Sum [M]
    │   │   → For each element in left half L[i], find window [lo, hi) in right half where lower ≤ R[k] - L[i] ≤ upper. Two pointers maintain this window as i advances
    │   ├── Majority Element (D&C Approach) `🎯 T2` [M]
    │   │   → Base: single element is its own majority. Count occurrences of left and right candidates in the full subarray; return whichever exceeds half
    │   └── Majority Element II `🎯 T2` [M]
    │       → Maintain two (candidate, count) pairs. On each element: if matches candidate, increment; else decrement both; if count reaches 0, replace. Final verification pass confirms actual frequency
    ├── Binary Search D&C
    │   ├── Search in Rotated Sorted Array `⚡ T1` [M]
    │   │   → If nums[lo] <= nums[mid], left half is sorted. If nums[lo] <= target < nums[mid], go left; else go right. Mirror logic when right half is sorted
    │   └── Find Minimum in Rotated Sorted Array `⚡ T1` [M]
    │       → Compare nums[mid] with nums[hi]. If nums[mid] > nums[hi], lo = mid + 1. Else hi = mid. Converges when lo == hi
    ├── Tree Construction D&C
    │   └── Construct Binary Tree from Preorder and Inorder `🎯 T2` [M]
    │       → Precompute an index map of {value: inorder_index} for O(1) lookup. Track preorder start offset instead of slicing to stay O(n) total
    ├── Maximum Subarray D&C `🎯 T2`
    │   └── Maximum Subarray (Divide and Conquer) `🎯 T2` [E]
    │       → Cross sum: scan left from mid accumulating suffix max; scan right from mid+1 accumulating prefix max; sum them
    └── QuickSelect Variants
    │   └── Kth Smallest Element in a Sorted Matrix `⚡ T1` [M]
    │       → Staircase count: start at top-right corner; if matrix[r][c] <= mid, add r+1 (all rows above in column c are ≤ mid), move right; else move up. O(n) per count step
```


### dynamic-programming.md

```
coding/algorithms/dynamic-programming.md
└── dynamic-programming.md
    ├── Linear DP (1-D)
    │   ├── Climbing Stairs `🎯 T2` [E]
    │   │   → dp[i] = dp[i-1] + dp[i-2]; base dp[0]=1, dp[1]=1. This is Fibonacci. Space collapses to two variables
    │   ├── Min Cost Climbing Stairs `🎯 T2` [E]
    │   │   → dp[i] = cost[i] + min(dp[i-1], dp[i-2]); answer = min(dp[n-1], dp[n-2])
    │   ├── House Robber `🎯 T2` [M]
    │   │   → dp[i] = max(dp[i-1], dp[i-2] + nums[i]); base dp[0]=nums[0], dp[1]=max(nums[0],nums[1])
    │   ├── House Robber II (Circular) `🎯 T2` [M]
    │   │   → max(rob(0..n-2), rob(1..n-1)) — run linear House Robber twice
    │   ├── Maximum Subarray (Kadane's — DP view) `🎯 T2` [E]
    │   │   → dp[i] = max(nums[i], dp[i-1] + nums[i]); answer = max(dp). Collapses to one variable
    │   ├── Word Break `🎯 T2` [M]
    │   │   → dp[i] = any(dp[j] and s[j:i] in word_set) for j in [i-max_len, i). Base: dp[0]=True
    │   └── Decode Ways `🎯 T2` [M]
    │       → add dp[i-1] if s[i-1] != '0'; add dp[i-2] if 10 ≤ s[i-2:i] ≤ 26. Base: dp[0]=1
    ├── 0/1 Knapsack
    │   ├── Partition Equal Subset Sum `🎯 T2` [M]
    │   │   → Odd total → return False immediately. Then run 0/1 knapsack DP
    │   ├── Target Sum `🎯 T2` [M]
    │   │   → dp[j] += dp[j - x] in reverse order (0/1 knapsack). Base: dp[0]=1
    │   └── Last Stone Weight II `⚡ T1` [M]
    │       → Standard 0/1 knapsack boolean DP; answer = total - 2 × max_j_where_dp[j]
    ├── Unbounded Knapsack
    │   ├── Coin Change (Min Coins) `🎯 T2` [M]
    │   │   → dp[i] = min(dp[i-c] + 1) for each coin c ≤ i; forward sweep (reuse allowed). Base: dp[0]=0, rest inf
    │   └── Coin Change II (Total Ways) `🎯 T2` [M]
    │   │   → Outer loop over coins; inner forward sweep: dp[i] += dp[i-c]. This ensures [1,2] and [2,1] are the same combination
    ├── LCS Family
    │   ├── Longest Common Subsequence `🎯 T2` [M]
    │   │   → If s1[i-1]==s2[j-1]: dp[i][j] = dp[i-1][j-1]+1; else max(dp[i-1][j], dp[i][j-1]). Space: roll to one row
    │   ├── Edit Distance `🎯 T2` [M]
    │   │   → If chars match: dp[i-1][j-1]; else 1 + min(replace=dp[i-1][j-1], delete=dp[i-1][j], insert=dp[i][j-1]). Base: dp[i][0]=i, dp[0][j]=j
    │   └── Longest Palindromic Subsequence `🎯 T2` [M]
    │   │   → If s[i]==s[j]: dp[i][j] = dp[i+1][j-1]+2; else max(dp[i+1][j], dp[i][j-1]). Fill diagonals outward (length 1→2→…→n)
    ├── Grid DP
    │   ├── Unique Paths `🎯 T2` [M]
    │   │   → dp[j] += dp[j-1] for each row. Base: all 1s initially (single path along edges)
    │   ├── Unique Paths II (With Obstacles) `🎯 T2` [M]
    │   │   → Same recurrence; set dp[j]=0 when obstacleGrid[i][j]==1. Careful with first row/col initialization
    │   ├── Minimum Path Sum `🎯 T2` [M]
    │   │   → dp[j] = grid[i][j] + min(dp[j], dp[j-1]). Initialize first row as prefix sums
    │   └── Maximal Square `🎯 T2` [M]
    │       → If matrix[i][j]=='1': dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1. Roll to two rows or 1D
    ├── Interval DP
    │   └── Palindrome Partitioning II (Minimum Cuts) `🎯 T2` [M]
    │   │   → dp[i] = min(dp[j-1]+1) for all j ≤ i where s[j..i] is palindrome; dp[j-1]=-1 when j=0
    ├── Tree DP
    │   ├── Diameter of Binary Tree `🎯 T2` [M]
    │   │   → DFS returns depth; at each node diameter = max(diameter, left_depth + right_depth). Return max(left, right) + 1
    │   ├── Binary Tree Maximum Path Sum `🎯 T2` [H]
    │   │   → left_gain = max(0, dfs(left)), right_gain = max(0, dfs(right)). ans = max(ans, node.val + left_gain + right_gain). Return node.val + max(left_gain, right_gain)
    │   └── House Robber III `🎯 T2` [M]
    │       → rob = node.val + left_skip + right_skip; skip = max(left_rob, left_skip) + max(right_rob, right_skip)
    ├── State Machine DP
    │   └── Best Time to Buy and Sell Stock (All Variants) `🎯 T2` [M]
    │   │   → I: track min price; II: sum uphill diffs; III/IV: buy/sell state machine for k txns
    ├── Longest Increasing Subsequence (LIS) Family `🎯 T2`
    │   ├── Longest Increasing Subsequence `🎯 T2` [M]
    │   │   → For each x in nums, binary search tails for the first element >= x. If found, replace it with x; otherwise append x. Answer = len(tails)
    │   ├── Number of LIS [M]
    │   │   → For each i, scan j < i. If nums[j] < nums[i]: if length[j]+1 > length[i], update both; if equal, add count[j] to count[i]. Answer = sum of count[i] where length[i] == max_length
    │   └── Longest Bitonic Subsequence [M]
    │       → Compute lis left-to-right O(n²), lds right-to-left O(n²). Answer = max(lis[i] + lds[i] - 1)
    ├── String DP
    │   ├── Distinct Subsequences `🎯 T2` [M]
    │   │   → If s[i-1] == t[j-1]: dp[i][j] = dp[i-1][j-1] + dp[i-1][j] (use or skip). Else: dp[i][j] = dp[i-1][j]. Base: dp[i][0] = 1 for all i
    │   └── Interleaving String `🎯 T2` [M]
    │   │   → dp[i][j] = (dp[i-1][j] and s1[i-1]==s3[i+j-1]) or (dp[i][j-1] and s2[j-1]==s3[i+j-1]). Base: dp[0][0] = True
    ├── Bitmask DP
    │   └── Partition to K Equal Subset Sums `🎯 T2` [M]
    │       → target = total / k. Iterate all masks in order. For each set mask, compute current_sum = sum of selected elements % target. Try adding each unselected element; if it fits, dp[mask | (1<<i)] = True. Answer = dp[(1<<n)-1]
    └── DP on Sequences
    │   ├── Jump Game II `🎯 T2` [M]
    │   │   → Iterate; update farthest = max(farthest, i + nums[i]). When i == current_end and not at last index: increment jumps, set current_end = farthest
    │   └── Maximum Product Subarray `🎯 T2` [M]
    │   │   → At each element x: max_prod, min_prod = max(x, max_prod*x, min_prod*x), min(x, max_prod*x, min_prod*x). Update global answer with max_prod
```


### graph-algorithms.md

```
coding/algorithms/graph-algorithms.md
└── graph-algorithms.md
    ├── Dijkstra's Algorithm
    │   ├── Network Delay Time `⚡ T1` [M]
    │   │   → Min-heap of (dist, node). Lazy deletion guard if d > dist[u]: continue discards stale heap entries. Answer = max(dist.values()); if any node has inf distance, return -1
    │   ├── Swim in Rising Water `⚡ T1` [M]
    │   │   → Heap entry (max_elevation_on_path, r, c). At each step, cost(u→v) = max(current_max, grid[v]). The first time we pop (N-1,N-1) is the answer
    │   └── Cheapest Flights Within K Stops (Dijkstra variant) `⚡ T1` [M]
    │       → Heap (cost, node, stops). Mark visited as (node, stops) pair. Bellman-Ford is simpler for this problem; Dijkstra works but requires careful pruning
    ├── Bellman-Ford
    │   └── Cheapest Flights Within K Stops `⚡ T1` [M]
    │   │   → Critical — use a copy of prices each round (temp = prices[:]). Without the copy, a single round might chain multiple hops, violating the hop bound
    ├── Topological Sort (BFS — Kahn's)
    │   ├── Course Schedule `⚡ T1` [M]
    │   │   → Build adjacency list and in-degree array. BFS from zero-in-degree nodes; decrement neighbors. If processed == numCourses → no cycle
    │   ├── Course Schedule II `⚡ T1` [M]
    │   │   → Collect dequeued nodes into order. If len(order) == numCourses → valid. Otherwise cycle exists
    │   └── Alien Dictionary `⚡ T1` [H]
    │   │   → For each pair (words[i], words[i+1]), find first differing character — adds directed edge. Invalid: if word A is a proper prefix of word B but A appears after B. Cycle in graph → ""
    ├── Strongly Connected Components / Bridges
    │   └── Find Eventual Safe States (Reverse Graph / Kahn's) `⚡ T1` [M]
    │       → outdegree[u] = original out-degree. Initialize queue with outdegree[u] == 0. When a node is processed safe, decrement predecessors' outdegree; add them if 0
    ├── Multi-source BFS / Special BFS
    │   ├── Word Ladder (BFS on Implicit Graph) `⚡ T1` [H]
    │   │   → Remove visited words from word_set immediately (not just a visited set) to prevent revisits efficiently
    │   └── Shortest Path in Binary Matrix `⚡ T1` [M]
    │       → Check both endpoints are 0 before starting. Distance = BFS level when target is first reached
    ├── Bipartite `⚡ T1`
    │   ├── Is Graph Bipartite? `⚡ T1` [M]
    │   │   → Must handle disconnected components — start BFS from every unvisited node
    │   └── Possible Bipartition [M]
    │       → Identical to isBipartite — just build the graph first from dislikes
    └── Graph Algorithms — More Problems
        └── Word Ladder II (LC 126) `⚡ T1` [M]
        │   → Remove words from word_set only after the full layer is processed — prevents cutting off valid same-layer paths
```


### greedy.md

```
coding/algorithms/greedy.md
└── greedy.md
    ├── Interval Greedy
    │   ├── Merge Intervals `🎯 T2` [M]
    │   │   → merged[-1][1] = max(merged[-1][1], end) when start ≤ merged[-1][1]
    │   ├── Non-overlapping Intervals (Minimum number to remove) `🎯 T2` [M]
    │   │   → Track last_end; if start >= last_end, keep (update last_end = end); else remove (increment count)
    │   └── Meeting Rooms II `🎯 T2` [M]
    │   │   → Heap size at the end = rooms needed
    ├── Jump / Coverage Greedy
    │   ├── Jump Game (can reach?) `🎯 T2` [M]
    │   │   → Single pass; early exit the moment current index exceeds max_reach
    │   ├── Jump Game II (minimum jumps) `🎯 T2` [M]
    │   │   → Loop only to n-2 (last index doesn't need a jump from it)
    │   ├── Jump Game III `🎯 T2` [M]
    │   │   → visited set prevents cycles. Return False if queue exhausts without finding 0
    │   └── Jump Game VI (DP + Deque) `🎯 T2` [M]
    │   │   → Deque stores indices in decreasing dp-value order; pop front when out of window, pop back when dp[i-1] ≥ dp[deque.back()]
    ├── Scheduling
    │   ├── Task Scheduler `⚡ T1` [M]
    │   │   → Pure math; no simulation needed
    │   └── Reorganize String `⚡ T1` [M]
    │   │   → Track prev (last placed char) — if top of heap == prev, temporarily swap with second-most-frequent
    ├── String / Array Greedy
    │   ├── Gas Station `🎯 T2` [M]
    │   │   → Single pass. Feasibility check built into the same pass via total sum
    │   └── Trapping Rain Water (greedy view) `⚡ T1` [H]
    │   │   → Advance the pointer with the smaller current boundary; maintain running max for each side
    └── Sorting-Based Greedy
    │   └── IPO (Maximize Capital, LC 502) `⚡ T1` [M]
    │   │   → Sort projects by capital. For each of k steps: push all projects with capital[i] ≤ W into max-heap; pop the most profitable; add to W. If max-heap empty, can't proceed
```


### maths.md

```
coding/algorithms/maths.md
└── maths.md
    └── Combinatorics / nCr
    │   └── Unique Paths (Combinatorics Approach) `🎯 T2` [M]
    │       → Python's math.comb computes this exactly in O(min(m,n)) time without overflow using integer arithmetic
```


### recursion.md

```
coding/algorithms/recursion.md
└── recursion.md
    ├── Foundation — Include/Exclude
    │   ├── Subsets (Power Set) `🎯 T2` [M]
    │   │   → At index i, add current path to results, then recurse with i+1 after optionally appending nums[i]. Or equivalently: iterate from i to n, choose nums[j], recurse from j+1
    │   └── Permutations `🎯 T2` [M]
    │   │   → Swap nums[i] with nums[start], recurse with start+1, swap back (in-place backtracking preserves O(1) space overhead per level)
    ├── Divide and Conquer (via Recursion)
    │   └── Merge Sort `🎯 T2` [M]
    │   │   → Base case = length ≤ 1. Split, conquer left, conquer right, merge in O(n) with two-pointer technique
    ├── Pruning & Constraints
    │   ├── Combination Sum (Unbounded) `🎯 T2` [M]
    │   │   → Recurse with (start=i, remaining-candidates[i]). Backtrack by popping. Sort candidates for early termination
    │   ├── Combination Sum II (No Reuse) `🎯 T2` [M]
    │   │   → if j > start and candidates[j] == candidates[j-1]: continue — only skip siblings, not the first occurrence at a level
    │   ├── Generate Parentheses `🎯 T2` [M]
    │   │   → Add ( if open < n; add ) if close < open. Leaf = string of length 2n
    │   ├── Word Search (Grid Backtracking) `🎯 T2` [M]
    │   │   → Mark board[r][c] with a sentinel (e.g., '#') before recursing, restore after. Check bounds and match before recursing
    │   └── Palindrome Partitioning `🎯 T2` [M]
    │   │   → Precompute is_pal in O(n²). DFS: for each end ≥ start, if is_pal[start][end], add substring and recurse from end+1
    ├── Constraint Satisfaction
    │   ├── N-Queens `🎯 T2` [M]
    │   │   → Track sets cols, diag1 (r-c), diag2 (r+c). For each row, try each column not in any set; add to sets, recurse, remove
    │   ├── Sudoku Solver `🎯 T2` [H]
    │   │   → Precompute sets for each row, column, and 3×3 box. At each empty cell, try only valid digits; backtrack immediately on failure
    │   └── Word Search II (Trie + Backtracking) `⚡ T1` [H]
    │   │   → At each cell, check trie_node.children[char]. If present, descend. If trie_node.word, add to results. Mark visited, recurse 4 directions, unmark. Prune exhausted Trie subtrees
    ├── Foundation — Recursion Fundamentals
    │   └── Binary Search (Recursive) `🎯 T2` [M]
    │   │   → Pass lo, hi as parameters. Base case: lo > hi → return -1. No extra space beyond call stack
    ├── Graph — Recursive Traversal
    │   └── All Paths from Source to Target `⚡ T1` [M]
    │       → Backtrack by appending node, recursing through neighbors, then popping
    ├── String Recursion
    │   └── Decode String (Recursive) `🎯 T2` [M]
    │   │   → Pass a mutable index (via list). Accumulate digits for k, accumulate chars for the current segment, recurse on [, multiply result on ]
    ├── Dynamic Programming Foundations (Recursive + Memo)
    │   └── Climbing Stairs (Memoized Recursion) `🎯 T2` [E]
    │   │   → memo dict on n. k steps: ways(n) = sum(ways(n-i) for i in 1..k if n-i >= 0)
    ├── Structural Tree Recursion
    │   ├── Flatten Binary Tree to Linked List (LC 114) `🎯 T2` [M]
    │   │   → Recursively flatten root.left and root.right. Find the rightmost node of the flattened left subtree. Attach root.right to it, move the left chain to root.right, set root.left = None
    │   ├── Construct Binary Tree from Preorder and Inorder T... `🎯 T2` [M]
    │   │   → Root = preorder[0]. Find mid = inorder.index(root.val). Left subtree uses preorder[1:mid+1] and inorder[:mid]. Right uses the remainder
    │   └── Serialize and Deserialize Binary Tree (LC 297) `🎯 T2` [M]
    │   │   → Serialize: root.val, serialize(left), serialize(right) joined by a delimiter. Deserialize: pop from deque; if "#" return None; else create node and recurse for left then right
    ├── Combinatorial Generation
    │   ├── Permutations II (LC 47) `🎯 T2` [M]
    │   │   → Sort nums. At each level, skip nums[i] if nums[i] == nums[i-1] and not used[i-1] (sibling was already explored — ensures we always use the left duplicate before the right at any level)
    │   ├── Subsets II (LC 90) `🎯 T2` [M]
    │   │   → Sort nums. In the loop for i in range(start, n): if i > start and nums[i] == nums[i-1], skip. Append path snapshot, continue
    │   └── Combinations (LC 77) `🎯 T2` [M]
    │       → Prune early: if remaining elements n - i + 1 < k - len(path), no valid completion possible — skip
    ├── Divide and Conquer — Advanced
    │   └── Maximum Subarray — D&C (O(n log n)) `🎯 T2` [E]
    │   │   → max_cross = max suffix of left + max prefix of right. Return max(max_left, max_right, max_cross)
    └── Recursion on Graphs
    │   ├── Clone Graph (LC 133) `⚡ T1` [M]
    │   │   → If node already in visited, return its clone. Otherwise create a new node, record it in visited, then recursively clone each neighbor and append to the new node's neighbors list
    │   └── Number of Islands (LC 200) `⚡ T1` [M]
    │       → DFS marks grid[r][c] = '0' then recurses into all 4 directions if in-bounds and == '1'
```


### sliding-window.md

```
coding/algorithms/sliding-window.md
└── sliding-window.md
    ├── Fixed-Size Window
    │   ├── Find All Anagrams in a String (LC 438) `⚡ T1` [M]
    │   │   → On adding s[right]: if freq reaches exactly need[c] → matches += 1. On removing s[left]: if freq drops below need[c] → matches -= 1. When matches == len(need) → anagram found
    │   └── Permutation in String (LC 567) `⚡ T1` [M]
    │       → When matches == required at any valid window position → return True
    ├── Variable Window — At Most K
    │   ├── Longest Substring Without Repeating Characters (L... `⚡ T1` [M]
    │   │   → Only jump left if last_seen[c] >= left (character might be outside current window — stale)
    │   ├── Longest Repeating Character Replacement (LC 424) `⚡ T1` [M]
    │   │   → Key insight: max_count never needs to decrease (we only care about the *best* window seen so far). When we shrink, max_count stays the same, and the window stays the same size or shrinks — we're looking for a *longer* window
    │   └── Fruits Into Baskets (At Most 2 Distinct) (LC 904) `⚡ T1` [M]
    │   │   → Window length right - left + 1 after shrinking is the candidate answer
    ├── Variable Window — Exactly K
    │   └── Subarrays with K Different Integers (LC 992) `⚡ T1` [M]
    │   │   → count(exactly k) = at_most(k) - at_most(k-1)
    ├── Variable Window — Minimum Length
    │   └── Minimum Window Substring (LC 76) `⚡ T1` [H]
    │       → need can go negative (excess characters) — only decrement missing when need[c] was positive (character was still required)
    ├── Sliding Window + Monotonic Deque
    │   └── Sliding Window Maximum (LC 239) `⚡ T1` [H]
    │   │   → Before adding i: (1) pop front if it's outside window [i-k+1, i]; (2) pop back while nums[deque[-1]] <= nums[i] (smaller elements can never be max while i is in window). Append i. Record nums[deque[0]] once i >= k-1
    ├── Variable Window — Max Length (Flip / Delete)
    │   ├── Max Consecutive Ones III (LC 1004) `⚡ T1` [M]
    │   │   → Answer is right - left + 1 after each valid step — window never shrinks below the best size seen (LC 424 trick not needed here since we do want exact max)
    │   └── Minimum Operations to Reduce X to Zero (LC 1658) `⚡ T1` [M]
    │   │   → Use a variable window (shrink when sum exceeds target, track max length when sum == target). Requires all non-negative integers for monotone shrink property — guaranteed by constraints
    └── Sliding Window + Monotonic Deque — Variable Window
    │   └── Jump Game VI (LC 1696) `🎯 T2` [M]
    │       → Before computing dp[i]: evict stale front (dq[0] < i - k). After computing dp[i]: evict back while dp[dq[-1]] <= dp[i]; append i. Space-optimise by storing dp in original array
```


### sorting.md

```
coding/algorithms/sorting.md
└── sorting.md
    ├── Merge Sort Variants `🎯 T2`
    │   ├── Merge Intervals `🎯 T2` [M]
    │   │   → For each interval after sort, either extend merged[-1][1] = max(merged[-1][1], end) or append a new interval
    │   ├── Sort List `🎯 T2` [M]
    │   │   → get_mid severs the list at the middle. Merge uses dummy head and two pointers
    │   ├── Count of Smaller Numbers After Self [M]
    │   │   → Sort (original_index, value) pairs; accumulate into result[original_index] during merge
    │   ├── Count of Range Sum [M]
    │   │   → For each right-half prefix r, maintain two pointers lo, hi on sorted left half: lo = first index where r - left[lo] ≤ upper, hi = first where r - left[hi] < lower. Count = hi - lo
    │   ├── Reverse Pairs [M]
    │   │   → Inner loop: for each left[i], advance j while left[i] > 2 * right[j]. Count += j per left element
    │   └── Count Inversions (Merge Sort) [M]
    │       → Recursive merge sort returning (sorted_array, inversion_count). Standard merge with count accumulation
    ├── QuickSort / QuickSelect
    │   ├── Kth Largest Element in an Array `⚡ T1` [M]
    │   │   → Target rank = k-1 (0-indexed from largest). Stop when pivot index == target
    │   ├── K Closest Points to Origin `⚡ T1` [M]
    │   │   → Partition by dist² ascending; recurse until pivot == k
    │   └── Top K Frequent Elements `⚡ T1` [M]
    │       → len(nums)+1 buckets (freq ranges 1..n); linear scan backward
    ├── Counting / Radix Sort
    │   └── Sort Colors `⚡ T1` [M]
    │   │   → nums[mid]==0: swap(lo,mid), lo++, mid++. nums[mid]==1: mid++. nums[mid]==2: swap(mid,hi), hi-- (don't advance mid — swapped value is unexplored)
    ├── Interview Classics
    │   └── Meeting Rooms II (LC 253) `🎯 T2` [M]
    │       → Sort intervals by start. For each interval: if heap and heap[0] <= start, heappop (reuse). heappush(end). Return heap size
    ├── Classic Merge Variants
    │   ├── Merge Two Sorted Lists `🎯 T2` [M]
    │   │   → Dummy head avoids null-checking the result head. After loop, cur.next = l1 or l2
    │   ├── Merge K Sorted Lists `⚡ T1` [H]
    │   │   → Heap entries are (val, tie_break_id, node) — tie-break prevents comparing ListNode objects on equal values
    │   └── Median of Two Sorted Arrays `⚡ T1` [H]
    │       → Always binary search on the shorter array. Handle edge cases with ±inf
    ├── Majority / Frequency
    │   ├── Majority Element (Boyer-Moore) `🎯 T2` [M]
    │   │   → The surviving candidate after one pass is the majority. (If majority not guaranteed, do a second pass to verify.)
    │   └── Majority Element II `🎯 T2` [M]
    │       → After the voting pass, verify both candidates have true count > n/3 (the vote may admit false positives for the second candidate)
    ├── Interval / Sweep Line
    │   ├── Insert Interval (LC 57) `🎯 T2` [M]
    │   │   → Overlap condition: existing.end >= new.start AND existing.start <= new.end
    │   └── Non-overlapping Intervals (LC 435) `🎯 T2` [M]
    │   │   → Removals = total − number kept. Ties in end time: keep the one with the earlier end (already handled by sort)
    ├── Topological Sort
    │   ├── Course Schedule II (LC 210) `⚡ T1` [M]
    │   │   → If len(order) < n, a cycle exists → return []
    │   └── Alien Dictionary (LC 269) `⚡ T1` [M]
    │       → Kahn's BFS topological sort on the character graph. Cycle → return "". Unconnected characters can appear anywhere
    ├── External Sort / K-way Merge
    │   ├── Find K Pairs with Smallest Sums (LC 373) `⚡ T1` [M]
    │   │   → At most k pops → O(k log k) after O(min(k, m) log min(k, m)) initial heapify
    │   └── Kth Smallest Element in a Sorted Matrix (LC 378) `⚡ T1` [M]
    │       → Count function: start at top-right; if matrix[r][c] <= mid → add r+1 to count, move right; else move up. O(n) per count call
    └── Partial Sort / Order Statistics
    │   ├── Kth Largest Element in a Stream (LC 703) `⚡ T1` [M]
    │   │   → Heap size invariant: always ≤ k. After each add, heap[0] = k-th largest among all seen elements
    │   ├── Find Median from Data Stream (LC 295) `⚡ T1` [M]
    │   │   → On add: push to lo (negate), rebalance by moving top of lo to hi, then if len(hi) > len(lo) move top of hi back to lo
    │   └── Sliding Window Median (LC 480) `⚡ T1` [M]
    │       → Rebalance: after each add/remove, ensure len(lo) == len(hi) or len(lo) == len(hi) + 1. Lazy removal: pop from heap top while heap[0] is in to_remove
```


### string-algorithms.md

```
coding/algorithms/string-algorithms.md
└── string-algorithms.md
    ├── Rabin-Karp (Rolling Hash)
    │   └── Implement Rabin-Karp [M]
    │   │   → Pre-compute BASE^(m-1) mod MOD. On hash match, verify character-by-character to rule out collisions. Double hashing (two independent mod values) reduces false positive probability to ~1/(p₁·p₂) `⚡ T1`
    ├── Palindrome Algorithms
    │   └── Palindrome Partitioning II — Minimum Cuts `🎯 T2` [M]
    │   │   → Pre-compute is_pal[i][j] using expand-around-center in O(n²). Then linear scan for dp[i]. Base: dp[i] = i (cut every character). If s[0..i] is itself a palindrome, dp[i] = 0
    ├── Sliding Window on Strings
    │   ├── Permutation in String `⚡ T1` [M]
    │   │   → Track matches = number of characters (out of 26) where window frequency equals s1 frequency. Slide window: add right char, remove left char, update matches accordingly. Avoids O(26) comparison per step
    │   └── Minimum Window Substring `⚡ T1` [H]
    │       → formed increments only when have[c] == need[c] (exact threshold), not on every increment. This makes the condition O(1) to check per step
    ├── Classic String Problems
    │   ├── Group Anagrams `⚡ T1` [M]
    │   │   → Sorting each string: O(k log k) per string where k = max length. Total: O(nk log k). Alternatively, use a tuple of 26 counts as key: O(nk) total
    │   ├── Longest Substring Without Repeating Characters `⚡ T1` [M]
    │   │   → Direct index tracking is more efficient than a frequency-decrement approach for this problem
    │   └── Find All Anagrams in a String `⚡ T1` [M]
    │       → Identical to Permutation in String but collect all starting indices where matches == 26 instead of returning True on first match
    └── DP on Strings
    │   └── Distinct Subsequences (LC 115) `🎯 T2` [M]
    │       → - Base: dp[i][0] = 1 for all i (empty t matched by any prefix of s). dp[0][j] = 0 for j > 0. - Transition: if s[i-1] == t[j-1]: dp[i][j] = dp[i-1][j-1] + dp[i-1][j] (use this char OR skip it). - Else: dp[i][j] = dp[i-1][j] (must skip s[i-1])
```


### two-pointers.md

```
coding/algorithms/two-pointers.md
└── two-pointers.md
    ├── Opposite Ends (Sorted Array)
    │   ├── 3Sum (LC 15) `⚡ T1` [M]
    │   │   → Skip duplicate anchors (nums[i] == nums[i-1]). On finding a triplet, skip duplicate inner pointers before advancing
    │   ├── Container With Most Water (LC 11) `⚡ T1` [M]
    │   │   → if height[lo] <= height[hi]: lo += 1 else hi -= 1. Record max at each step
    │   └── Trapping Rain Water (LC 42) `⚡ T1` [H]
    │       → if left_max <= right_max: water += left_max - height[lo]; lo += 1 else process right side
    ├── Same Direction (Fast/Slow)
    │   ├── Remove Duplicates from Sorted Array (LC 26) `⚡ T1` [M]
    │   │   → Each non-duplicate advances write. Duplicates are simply skipped
    │   └── Move Zeroes (LC 283) `⚡ T1` [M]
    │   │   → Avoids unnecessary writes for zeros — write pointer skips over zero positions and fills at the end
    ├── Partition / Dutch National Flag
    │   └── Sort Colors (LC 75) `⚡ T1` [M]
    │       → Process nums[mid]: if 0 → swap with lo, advance both lo and mid; if 1 → advance mid only; if 2 → swap with hi, decrement hi but do NOT advance mid (swapped element is unseen)
    ├── Linked List Two Pointers
    │   ├── Linked List Cycle (LC 141) `⚡ T1` [E]
    │   │   → Check fast and fast.next before each step to avoid null pointer dereference
    │   └── Remove Nth Node From End of List (LC 19) `🎯 T2` [M]
    │       → Use a dummy head to handle edge case of deleting the first node. slow.next = slow.next.next removes the target
    ├── Palindrome Two Pointers
    │   └── 3Sum Closest (LC 16) `⚡ T1` [M]
    │       → If s < target → lo += 1 (need larger sum); if s > target → hi -= 1; if equal → return immediately
    └── Two Pointers — More Problems
        └── Minimum Operations to Reduce X to Zero (LC 1658) `⚡ T1` [M]
            → Two-pointer (sliding window): expand right to grow the window, shrink left when the window sum exceeds target. Track the maximum window length where sum equals target
```


### union-find.md

```
coding/algorithms/union-find.md
└── union-find.md
    ├── Basic Union-Find
    │   ├── Number of Provinces (Matrix Form) `⚡ T1` [M]
    │   │   → Only process upper triangle (j > i) to avoid redundant unions and double-decrementing
    │   ├── Graph Valid Tree `⚡ T1` [M]
    │   │   → Short-circuit if len(edges) != n-1. Process edges; if any union returns False (cycle) → not a tree
    │   ├── Redundant Connection `⚡ T1` [M]
    │   │   → union returns False when already connected → that's the answer
    │   └── Satisfiability of Equality Equations `⚡ T1` [M]
    │       → 26 lowercase letters → DSU of size 26. If find(x) == find(y) for a != constraint → contradiction
    ├── Weighted / Ranked Union-Find
    │   └── Accounts Merge (Email Graph) `⚡ T1` [M]
    │   │   → Map email → index. For each account, union the first email with all subsequent ones. After all unions, group indices by root
    ├── Dynamic / Offline Union-Find
    │   └── Number of Islands II `⚡ T1` [M]
    │   │   → Track which cells are land (set). Skip duplicate additions. DSU's union automatically decrements component count on merge
    ├── DSU for Other Problems
    │   └── Longest Consecutive Sequence (DSU Approach) `⚡ T1` [M]
    │   │   → Build val → index map. For each value, if val+1 exists, union their indices
    ├── Directed Graph Union-Find
    │   └── Redundant Connection II `⚡ T1` [M]
    │       → Pass 1: record in-degree-2 candidates. Pass 2: DSU union excluding cand2. If no cycle detected with cand2 excluded → return cand2. If cycle detected and cand1 exists → return cand1. If cycle and no candidate → return the cycle edge
    ├── Grid / Coordinate Union-Find
    │   └── Swim in Rising Water `⚡ T1` [M]
    │   │   → Create list of (elevation, r, c), sort it. Maintain visited set. For each cell in order, mark visited, union with adjacent visited cells, check connectivity
    ├── Connectivity With Constraints
    │   └── Making a Large Island `⚡ T1` [M]
    │   │   → Label each cell's DSU root. For each 0-cell, collect unique roots of neighboring 1-cells (avoid double-counting same component), sum their sizes
    └── Union-Find — More Problems
        └── Redundant Connection II (LC 685, Directed Graph) `⚡ T1` [M]
        │   → 1. Scan edges; track parent for each node. If a node already has a parent, record cand1 = prev_edge, cand2 = current_edge and skip cand2. 2. Run Union-Find on remaining edges. If a cycle forms and cand1 exists, return cand1; else return the cycle edge. If no cycle and cand2 exists, return cand2
```

