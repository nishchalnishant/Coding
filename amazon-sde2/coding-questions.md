# Amazon SDE-2 — High-Probability Coding Questions

Questions sourced from Amazon interview reports (Glassdoor, Leetcode discuss, Blind). Marked with frequency tier: 🔴 Very High / 🟠 High / 🟡 Medium.

---

## Arrays, Two Pointers, Sliding Window

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Two Sum / Three Sum | HashMap / Two Pointer | Easy/Med | Hash for O(n); sort+2ptr for 3sum |
| 🔴 Subarray Sum Equals K | Prefix Sum + HashMap | Medium | `prefix[i] - k` in map |
| 🔴 Max Sliding Window (239) | Monotonic Deque | Hard | Deque stores indices, front = max |
| 🔴 Trapping Rain Water (42) | Two Pointer / Stack | Hard | Left/right max arrays or two-ptr |
| 🟠 Container With Most Water (11) | Two Pointer | Medium | Move smaller side inward |
| 🟠 Longest Subarray with At Most K Distinct | Sliding Window | Medium | Shrink when map size > k |
| 🟠 Minimum Size Subarray Sum (209) | Sliding Window | Medium | Expand right, shrink left |
| 🟡 Product of Array Except Self (238) | Prefix/Suffix Product | Medium | Left pass then right pass, O(1) space |
| 🟡 Find All Anagrams in String (438) | Fixed Sliding Window | Medium | Char frequency window |
| 🟡 Spiral Matrix (54) | Simulation | Medium | Track 4 boundaries |

---

## Strings

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Longest Substring Without Repeating (3) | Sliding Window + Set | Medium | Move left ptr past duplicate |
| 🔴 Valid Parentheses (20) | Stack | Easy | Push open, pop/match on close |
| 🟠 Minimum Window Substring (76) | Sliding Window + HashMap | Hard | Contract when all chars covered |
| 🟠 Group Anagrams (49) | HashMap + Sort | Medium | Sorted string as key |
| 🟠 Longest Palindromic Substring (5) | Expand Around Center | Medium | Try each center (odd+even) |
| 🟠 String to Integer / atoi (8) | Parsing | Medium | Handle sign, overflow, non-digit |
| 🟡 Word Break (139) | DP / BFS | Medium | dp[i] = any dp[j] + word[j..i] in dict |
| 🟡 Decode Ways (91) | DP | Medium | dp[i] depends on 1-digit and 2-digit decode |

---

## Linked Lists

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Reverse Linked List (206) | Iterative / Recursive | Easy | Prev/curr/next triple swap |
| 🔴 Merge Two Sorted Lists (21) | Merge | Easy | Dummy head pattern |
| 🟠 Linked List Cycle II (142) | Floyd's Algorithm | Medium | Meet point + reset one ptr to head |
| 🟠 LRU Cache (146) | HashMap + DLL | Medium | O(1) get/put; dummy head/tail |
| 🟠 Reverse Nodes in k-Group (25) | In-place Reversal | Hard | Count k, reverse group, reconnect |
| 🟡 Add Two Numbers (2) | List traversal | Medium | Carry through; handle different lengths |
| 🟡 Merge K Sorted Lists (23) | Min-Heap | Hard | Push heads to heap, extract min |

---

## Trees

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Binary Tree Level Order Traversal (102) | BFS | Medium | Queue, process level by level |
| 🔴 Lowest Common Ancestor of BST (235) | BST property | Easy | val < p and val < q → go right, else left |
| 🔴 Lowest Common Ancestor of BT (236) | DFS post-order | Medium | Return node when found; LCA when both sides non-null |
| 🔴 Serialize/Deserialize Binary Tree (297) | BFS / preorder | Hard | BFS with null markers |
| 🔴 Validate BST (98) | DFS with bounds | Medium | Pass min/max bounds recursively |
| 🟠 Binary Tree Maximum Path Sum (124) | DFS post-order | Hard | At each node: max gain = node + max(left,0) + max(right,0) |
| 🟠 Diameter of Binary Tree (543) | DFS | Easy | At each node: left_depth + right_depth |
| 🟠 Construct BT from Preorder+Inorder (105) | Recursion | Medium | Root = preorder[0]; split inorder |
| 🟠 Flatten Binary Tree to Linked List (114) | Morris / DFS | Medium | Post-order: right = flatten(left), then flatten(old_right) |
| 🟠 Kth Smallest in BST (230) | Inorder | Medium | Inorder = sorted; count to k |
| 🟡 Path Sum II (113) | DFS + backtrack | Medium | Track current path; add copy on leaf match |
| 🟡 Word Search (79) / Trie insert-search | DFS / Trie | Medium | Mark visited; restore on backtrack |

---

## Graphs

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Number of Islands (200) | DFS/BFS flood fill | Medium | Mark visited by sinking ('1'→'0') |
| 🔴 Course Schedule I & II (207, 210) | Topological Sort / Cycle detect | Medium | Kahn's BFS or DFS 3-color |
| 🔴 Clone Graph (133) | BFS + HashMap | Medium | Map old→new, BFS to copy edges |
| 🟠 Pacific Atlantic Water Flow (417) | Multi-source BFS | Medium | BFS from both oceans inward |
| 🟠 Rotting Oranges (994) | Multi-source BFS | Medium | Start BFS from all rotten; count minutes |
| 🟠 Word Ladder (127) | BFS + pattern hashing | Hard | Replace each char with '*', build adjacency |
| 🟠 Number of Connected Components (323) | Union-Find / BFS | Medium | Union-Find with path compression |
| 🟠 Redundant Connection (684) | Union-Find | Medium | Add edge that creates cycle |
| 🟡 Alien Dictionary (269) | Topological Sort | Hard | Build graph from adjacent word pairs |
| 🟡 Minimum Spanning Tree / Prim's | Heap + greedy | Medium | Used in network design questions |

---

## Dynamic Programming

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Coin Change (322) | Unbounded Knapsack | Medium | dp[i] = min(dp[i], dp[i-coin]+1) |
| 🔴 Longest Common Subsequence (1143) | 2D DP | Medium | dp[i][j]: match→dp[i-1][j-1]+1, else max |
| 🔴 0/1 Knapsack | Classic DP | Medium | dp[i][w]: take or skip item i |
| 🔴 Word Break (139) | DP + HashSet | Medium | dp[i] = true if any dp[j] + s[j:i] in set |
| 🟠 Longest Increasing Subsequence (300) | DP / Binary Search | Medium | patience sort O(n log n) |
| 🟠 Edit Distance (72) | 2D DP | Hard | dp[i][j] = min(insert, delete, replace) |
| 🟠 Unique Paths (62) / with obstacles | Grid DP | Medium | dp[i][j] = dp[i-1][j] + dp[i][j-1] |
| 🟠 Jump Game II (45) | Greedy / DP | Medium | Track farthest reachable per level |
| 🟠 Partition Equal Subset Sum (416) | 0/1 Knapsack | Medium | Subset sum = total/2 |
| 🟠 House Robber I & II (198, 213) | Linear DP | Medium | Rob II = max(rob[0..n-2], rob[1..n-1]) |
| 🟡 Burst Balloons (312) | Interval DP | Hard | dp[i][j] = last balloon to burst in range |
| 🟡 Regular Expression Matching (10) | 2D DP | Hard | Handle `*` = 0 or more of preceding |

---

## Heaps / Priority Queues

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Top K Frequent Elements (347) | Min-Heap size k | Medium | Push (freq, elem); evict when size > k |
| 🔴 Kth Largest Element (215) | Min-Heap / Quickselect | Medium | Heap size k; root = kth largest |
| 🟠 Merge K Sorted Lists (23) | Min-Heap | Hard | Heap on (val, list_index, node) |
| 🟠 Find Median from Data Stream (295) | Two Heaps | Hard | Max-heap (lower half) + min-heap (upper half) |
| 🟠 Task Scheduler (621) | Greedy + Heap | Medium | Always pick most-frequent available task |
| 🟡 K Closest Points to Origin (973) | Max-Heap size k | Medium | Euclidean dist; evict farthest |

---

## Stack / Monotonic Stack

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Daily Temperatures (739) | Monotonic Decreasing Stack | Medium | Stack of indices; pop when warmer |
| 🔴 Largest Rectangle in Histogram (84) | Monotonic Increasing Stack | Hard | Pop when bar shorter; width = right - left - 1 |
| 🟠 Next Greater Element (496, 503) | Monotonic Stack | Medium | Process right-to-left or use circular trick |
| 🟠 Min Stack (155) | Auxiliary stack | Easy | Pair (val, current_min) |
| 🟡 Decode String (394) | Stack | Medium | Push (count, built_str) on '[' |

---

## Binary Search

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Search in Rotated Sorted Array (33) | Modified Binary Search | Medium | One half always sorted; check which |
| 🟠 Find Minimum in Rotated Array (153) | Binary Search | Medium | mid > right → min in right half |
| 🟠 Binary Search on Answer | Parametric Search | Medium | "Is X achievable?" as predicate |
| 🟠 Koko Eating Bananas (875) | Search on answer space | Medium | Binary search on speed k |
| 🟡 Median of Two Sorted Arrays (4) | Binary Search on partition | Hard | Partition smaller array |

---

## Backtracking

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🟠 Subsets I & II (78, 90) | Backtracking | Medium | Include/exclude; skip dup on same level |
| 🟠 Permutations (46, 47) | Backtracking + used[] | Medium | Swap or visited array |
| 🟠 Combination Sum I & II (39, 40) | Backtracking | Medium | Sort + skip dup; reuse only in I |
| 🟠 Letter Combinations of Phone (17) | Backtracking | Medium | Map digits to chars; recurse |
| 🟡 N-Queens (51) | Backtracking | Hard | Track col, diag1, diag2 sets |
| 🟡 Palindrome Partitioning (131) | Backtracking + DP | Medium | Precompute isPalin[i][j] |

---

## Amazon-Specific / OA Common

| Problem | Notes |
|---|---|
| LRU Cache (146) | Classic Amazon OA question |
| Design Hit Counter | Sliding window or queue |
| Maximum Units on Truck (1710) | Greedy — sort by units/box desc |
| Minimum Number of Refueling Stops (871) | Max-heap greedy |
| Reorder Log Files (937) | Custom sort — letter logs before digit logs |
| Most Common Word (819) | String parsing + frequency map |
| Brick Wall (554) | HashMap on gaps |
| Prison Cells After N Days (957) | Cycle detection |
| Expressive Words (809) | Two-pointer + run-length |
| Advantage Shuffle (870) | Greedy — sorted + two-pointer |
