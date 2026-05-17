# Canonical Questions — Logic + Trickiness Index

One-line insight per problem. Use this to check your mental model before opening the solution. If you can state the key insight cold, you know the problem.

---

## Arrays

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Two Sum | Easy | Hash Map | Store complement; check-before-store avoids self-match |
| Best Time to Buy/Sell Stock | Easy | Kadane variant | Track running min; profit = price - min_so_far |
| Maximum Subarray | Easy | Kadane's | Reset to 0 when prefix goes negative |
| Product Except Self | Medium | Prefix × Suffix | Left pass then right pass; no division needed |
| Maximum Product Subarray | Medium | DP | Track both max and min (negatives flip sign) |
| Container With Most Water | Medium | Two Pointers | Move the shorter side — taller side can never improve by moving |
| Trapping Rain Water | Hard | Monotonic Stack / Two Pointers | Water at i = min(left_max, right_max) - height[i] |
| Sliding Window Maximum | Hard | Monotonic Deque | Deque stores indices; pop front when out of window |
| Merge Intervals | Medium | Sorting | Sort by start; extend end when overlap detected |
| Non-overlapping Intervals | Medium | Greedy | Sort by end; greedily keep intervals with earliest end |
| Jump Game | Medium | Greedy | Track max reachable index; fail if current > max_reach |
| Jump Game II | Medium | Greedy | BFS layers — count jumps when you cross current layer end |
| Find Minimum in Rotated Array | Medium | Binary Search | Pivot is where arr[mid] > arr[right] |
| Search in Rotated Array | Medium | Binary Search | Identify sorted half first; then standard binary search |

---

## Strings

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Valid Palindrome | Easy | Two Pointers | Skip non-alphanumeric; compare lowercased |
| Valid Anagram | Easy | Frequency Map | Counter(s) == Counter(t) |
| Longest Substring Without Repeat | Medium | Sliding Window | Shrink left when duplicate enters window |
| Longest Repeating Character Replacement | Medium | Sliding Window | Window valid if len - max_freq ≤ k |
| Minimum Window Substring | Hard | Sliding Window | Two counters; shrink when all chars satisfied |
| Group Anagrams | Medium | Grouping | sorted(word) as hash key |
| Find All Anagrams | Medium | Sliding Window (fixed) | Fixed window; compare freq maps |
| Longest Palindromic Substring | Medium | Expand Around Center | Try both odd and even expansions at each index |
| Palindromic Substrings (count) | Medium | Expand Around Center | Count each successful expansion |
| Encode and Decode Strings | Medium | Delimiter | Length-prefix format: "4#word" handles all delimiters |

---

## Linked Lists

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Reverse Linked List | Easy | Iterative / Recursive | Three-pointer: prev, curr, next |
| Merge Two Sorted Lists | Easy | Dummy Node | Dummy head eliminates edge cases |
| Reorder List | Medium | Fast/Slow + Reverse | Find mid, reverse second half, interleave |
| Remove Nth from End | Medium | Two Pointers | Advance fast n steps; then move both |
| Linked List Cycle | Easy | Fast/Slow Pointers | Cycle if fast == slow |
| Cycle Start | Medium | Fast/Slow Pointers | After meeting, reset one to head; both move 1 step |
| Merge K Sorted Lists | Hard | Heap | Min-heap of (val, list_idx); extract min repeatedly |
| LRU Cache | Medium | HashMap + Doubly Linked List | O(1) get and put; move to head on access |

---

## Stacks

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Valid Parentheses | Easy | Stack | Push open; pop and match on close |
| Min Stack | Easy | Two Stacks | Track running min alongside main stack |
| Daily Temperatures | Medium | Monotonic Stack (decreasing) | Pop when warmer found; answer = current_idx - stack_idx |
| Next Greater Element | Medium | Monotonic Stack | Same pattern; map result by value |
| Largest Rectangle in Histogram | Hard | Monotonic Stack | Pop when shorter bar found; width = current - stack_top - 1 |
| Trapping Rain Water | Hard | Monotonic Stack | Water above each bar bounded by walls |
| Car Fleet | Medium | Monotonic Stack | Sort by position; car merges fleet if it arrives before or same time |

---

## Trees

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Invert Binary Tree | Easy | DFS | Swap left/right at each node recursively |
| Maximum Depth | Easy | DFS | 1 + max(left_depth, right_depth) |
| Same Tree | Easy | DFS | Recurse both trees simultaneously |
| Subtree of Another Tree | Easy | DFS | At each node, check if trees match |
| Lowest Common Ancestor (BST) | Easy | BST property | If both < root go left; if both > root go right |
| Lowest Common Ancestor (any) | Medium | DFS Post-order | Return node when found; LCA = where both sides return non-null |
| Validate BST | Medium | DFS with bounds | Pass min/max bounds; tighten at each step |
| Kth Smallest in BST | Medium | In-order DFS | In-order gives sorted; count down to k |
| Path Sum II | Medium | DFS backtrack | Add to path, recurse, remove from path |
| Binary Tree Maximum Path Sum | Hard | DFS Post-order | At each node: gain = node.val + max(0, left) + max(0, right) |
| Serialize/Deserialize | Hard | Pre-order DFS | Encode null as "#"; reconstruct with queue |
| Level Order Traversal | Medium | BFS | Deque; record len at start of each level |
| Right Side View | Medium | BFS | Last node at each BFS level |
| Count Good Nodes | Medium | DFS | Pass max_so_far down; count if node >= max |
| Construct from Pre+Inorder | Medium | DFS + Index Map | Preorder[0] = root; find in inorder to split |

---

## Graphs

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Number of Islands | Medium | DFS/BFS | Flood fill from each unvisited '1'; count floods |
| Clone Graph | Medium | BFS + HashMap | Map original→clone; BFS to copy edges |
| Pacific Atlantic Water Flow | Medium | Reverse BFS | BFS from both coasts; answer = intersection |
| Course Schedule | Medium | Topological Sort | Cycle in directed graph = no valid ordering |
| Course Schedule II | Medium | Topo Sort (Kahn's) | Return topo order; empty if cycle exists |
| Number of Connected Components | Medium | Union-Find / DFS | Count distinct roots |
| Graph Valid Tree | Medium | Union-Find | n nodes, n-1 edges, no cycle = valid tree |
| Word Ladder | Hard | BFS | Each word = node; edge if 1 char diff; BFS = shortest path |
| Alien Dictionary | Hard | Topological Sort | Build graph from adjacent word pairs; topo sort |
| Network Delay Time | Medium | Dijkstra | Single-source shortest path; return max dist |
| Swim in Rising Water | Hard | Binary Search + BFS / Dijkstra | Min time = min max-height path from (0,0) to (n-1,n-1) |

---

## Dynamic Programming

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Climbing Stairs | Easy | 1D DP | dp[i] = dp[i-1] + dp[i-2]; Fibonacci |
| House Robber | Medium | 1D DP | dp[i] = max(dp[i-1], dp[i-2] + nums[i]) |
| House Robber II (circular) | Medium | 1D DP | Run twice: [0..n-2] and [1..n-1]; take max |
| Longest Palindromic Subsequence | Medium | 2D DP (interval) | dp[i][j] = 2+dp[i+1][j-1] if match else max(dp[i+1][j], dp[i][j-1]) |
| Longest Common Subsequence | Medium | 2D DP | dp[i][j] = 1+dp[i-1][j-1] if match else max(dp[i-1][j], dp[i][j-1]) |
| Edit Distance | Hard | 2D DP | dp[i][j] = min(insert, delete, replace) |
| Coin Change | Medium | Unbounded Knapsack | dp[i] = min(dp[i], 1 + dp[i-coin]) for each coin |
| Coin Change II (ways) | Medium | Unbounded Knapsack | dp[i] += dp[i-coin]; order: coin outer, amount inner |
| 0-1 Knapsack | Medium | 2D DP | dp[i][w] = max(skip, take if weight fits) |
| Partition Equal Subset Sum | Medium | 0-1 Knapsack | Can we reach sum/2? Subset sum DP |
| Word Break | Medium | DP + Set | dp[i] = True if any dp[j] and s[j:i] in word_set |
| Unique Paths | Medium | Grid DP | dp[i][j] = dp[i-1][j] + dp[i][j-1] |
| Longest Increasing Subsequence | Medium | DP / Binary Search | O(n log n): patience sort with bisect_left |
| Burst Balloons | Hard | Interval DP | dp[i][j] = max coins if last balloon in (i,j) is k |
| Regular Expression Matching | Hard | 2D DP | Handle '*': match 0 times (dp[i][j-2]) or 1+ times (dp[i-1][j]) |

---

## Binary Search

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Binary Search | Easy | Standard | lo=0, hi=n-1; mid=(lo+hi)//2 |
| Search a 2D Matrix | Medium | BS on 1D index | Treat as 1D: row=mid//cols, col=mid%cols |
| Koko Eating Bananas | Medium | BS on Answer | Binary search speed; validate: can finish in h hours? |
| Minimum in Rotated Array | Medium | BS | Left-biased: if arr[mid] > arr[hi], pivot in right half |
| Time-Based Key-Value Store | Medium | BS on timestamps | bisect_right on sorted timestamps per key |
| Split Array Largest Sum | Hard | BS on Answer | Binary search max subarray sum; validate with greedy |
| Median of Two Sorted Arrays | Hard | BS on partition | Partition both arrays; check cross conditions |

---

## Heaps

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Kth Largest Element | Medium | Min-Heap size K | Push all; pop until size K; heap[0] is answer |
| Top K Frequent Elements | Medium | Heap / Bucket Sort | Bucket sort by frequency is O(n) |
| Find Median from Data Stream | Hard | Two Heaps | Max-heap left, min-heap right; balance sizes |
| Task Scheduler | Medium | Greedy + Heap | Max-frequency task drives idle time: max(n+1, total_tasks) trick |
| Merge K Sorted Lists | Hard | Min-Heap | Push (val, list_idx, elem_idx); extract min |

---

## Backtracking

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Subsets | Medium | Choose/Skip | For each element: include or exclude |
| Subsets II (duplicates) | Medium | Sorted + Skip | Skip element if same as previous at same depth |
| Permutations | Medium | Swap / Used[] | Mark used; recurse; unmark |
| Permutations II (duplicates) | Medium | Sorted + Skip | Skip if used[i] or (same as prev and prev not used) |
| Combination Sum | Medium | BS start index | Can reuse; recurse with same index |
| Combination Sum II | Medium | Sorted + Skip | Cannot reuse; skip duplicates at same depth |
| Word Search | Medium | DFS + Backtrack | Mark visited; recurse 4 dirs; unmark on return |
| N-Queens | Hard | Row-by-row | Track col, diag1, diag2 as sets |
| Palindrome Partitioning | Medium | Backtrack + precompute | Precompute is_palindrome[i][j]; then backtrack |
