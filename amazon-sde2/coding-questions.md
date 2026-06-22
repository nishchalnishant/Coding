# Amazon SDE-2 — High-Probability Coding Questions

Questions ordered by priority tier. Study top-down — don't move to the next tier until you can solve Tier 1 problems cold.

Frequency: 🔴 Very High / 🟠 High / 🟡 Medium

---

## PRIORITY TIER 1 — Master These First
> These appear in nearly every Amazon loop. You will almost certainly see at least one from each section.

---

### 1. Trees (BFS + DFS)
_Amazon's single most common topic. Expect 1 tree problem in every loop._

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Binary Tree Level Order Traversal (102) | BFS | Medium | Queue, process level by level |
| 🔴 Lowest Common Ancestor of BST (235) | BST property | Easy | val < p and q → go right, else left |
| 🔴 Lowest Common Ancestor of BT (236) | DFS post-order | Medium | LCA when both left+right non-null |
| 🔴 Validate BST (98) | DFS with bounds | Medium | Pass min/max bounds recursively |
| 🔴 Serialize/Deserialize Binary Tree (297) | BFS / preorder | Hard | BFS with null markers |
| 🟠 Binary Tree Maximum Path Sum (124) | DFS post-order | Hard | max gain = node + max(left,0) + max(right,0) |
| 🟠 Diameter of Binary Tree (543) | DFS | Easy | left_depth + right_depth at each node |
| 🟠 Construct BT from Preorder+Inorder (105) | Recursion | Medium | Root = preorder[0]; split inorder |
| 🟠 Kth Smallest in BST (230) | Inorder | Medium | Inorder = sorted; count to k |
| 🟠 Flatten Binary Tree to Linked List (114) | DFS post-order | Medium | right = flatten(left), then append old right |
| 🟡 Path Sum II (113) | DFS + backtrack | Medium | Track path; copy on leaf match |

---

### 2. Dynamic Programming
_At least 1 DP problem per loop. Coin Change and LCS are classics._

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Coin Change (322) | Unbounded Knapsack | Medium | dp[i] = min(dp[i], dp[i-coin]+1) |
| 🔴 Longest Common Subsequence (1143) | 2D DP | Medium | match→dp[i-1][j-1]+1, else max(dp[i-1][j], dp[i][j-1]) |
| 🔴 0/1 Knapsack | Classic DP | Medium | dp[i][w]: take or skip item i |
| 🔴 Word Break (139) | DP + HashSet | Medium | dp[i] = true if any dp[j] + s[j:i] in dict |
| 🟠 House Robber I & II (198, 213) | Linear DP | Medium | Rob II = max(rob[0..n-2], rob[1..n-1]) |
| 🟠 Longest Increasing Subsequence (300) | DP / Binary Search | Medium | Patience sort → O(n log n) |
| 🟠 Unique Paths (62) / with obstacles | Grid DP | Medium | dp[i][j] = dp[i-1][j] + dp[i][j-1] |
| 🟠 Partition Equal Subset Sum (416) | 0/1 Knapsack | Medium | Subset sum = total/2 |
| 🟠 Jump Game II (45) | Greedy / DP | Medium | Track farthest reachable per BFS level |
| 🟠 Edit Distance (72) | 2D DP | Hard | dp[i][j] = min(insert, delete, replace) |
| 🟡 Burst Balloons (312) | Interval DP | Hard | dp[i][j] = last balloon to burst in range |
| 🟡 Regular Expression Matching (10) | 2D DP | Hard | Handle `*` = 0 or more of preceding |

---

### 3. Arrays / Sliding Window / Two Pointers
_Embedded in almost every problem. Pattern recognition here is table stakes._

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Two Sum / Three Sum | HashMap / Two Pointer | Easy/Med | Hash for O(n); sort+2ptr for 3sum |
| 🔴 Subarray Sum Equals K (560) | Prefix Sum + HashMap | Medium | `prefix[i] - k` in map |
| 🔴 Trapping Rain Water (42) | Two Pointer | Hard | Left/right max arrays or two-ptr |
| 🔴 Max Sliding Window (239) | Monotonic Deque | Hard | Deque stores indices, front = max |
| 🟠 Longest Subarray with At Most K Distinct | Sliding Window | Medium | Shrink when map size > k |
| 🟠 Container With Most Water (11) | Two Pointer | Medium | Move smaller side inward |
| 🟠 Minimum Size Subarray Sum (209) | Sliding Window | Medium | Expand right, shrink left |
| 🟡 Product of Array Except Self (238) | Prefix/Suffix Product | Medium | Left pass then right pass, O(1) space |
| 🟡 Find All Anagrams in String (438) | Fixed Sliding Window | Medium | Char frequency window |
| 🟡 Spiral Matrix (54) | Simulation | Medium | Track 4 boundaries |

---

### 4. Graphs (BFS / DFS / Topo Sort)
_Number of Islands variants and Course Schedule are near-guaranteed._

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Number of Islands (200) | BFS/DFS flood fill | Medium | Sink visited cells ('1'→'0') |
| 🔴 Course Schedule I & II (207, 210) | Topological Sort | Medium | Kahn's BFS or DFS 3-color; cycle if order incomplete |
| 🔴 Clone Graph (133) | BFS + HashMap | Medium | Map old→new, BFS to copy edges |
| 🟠 Rotting Oranges (994) | Multi-source BFS | Medium | Start BFS from all rotten; count minutes |
| 🟠 Pacific Atlantic Water Flow (417) | Multi-source BFS | Medium | BFS inward from both oceans; find intersection |
| 🟠 Number of Connected Components (323) | Union-Find / BFS | Medium | Union-Find with path compression |
| 🟠 Redundant Connection (684) | Union-Find | Medium | Add edge that creates cycle |
| 🟠 Word Ladder (127) | BFS + pattern hashing | Hard | Replace each char with '*'; build adjacency |
| 🟡 Alien Dictionary (269) | Topological Sort | Hard | Build graph from adjacent word pair diffs |

---

### 5. Heaps / Priority Queues
_Top-K and Median from stream are frequently asked._

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Top K Frequent Elements (347) | Min-Heap size k | Medium | Push (freq, elem); evict when size > k |
| 🔴 Kth Largest Element (215) | Min-Heap / Quickselect | Medium | Heap size k; root = kth largest |
| 🟠 Find Median from Data Stream (295) | Two Heaps | Hard | Max-heap (lower) + min-heap (upper); balance sizes |
| 🟠 Merge K Sorted Lists (23) | Min-Heap | Hard | Heap on (val, list_idx, node) |
| 🟠 Task Scheduler (621) | Greedy + Heap | Medium | Always pick most-frequent available task |
| 🟡 K Closest Points to Origin (973) | Max-Heap size k | Medium | Euclidean dist; evict farthest |

---

## PRIORITY TIER 2 — High Probability
> Very likely to appear. Know the template cold + solve 2–3 problems per section.

---

### 6. Strings
_Often combined with HashMap or sliding window. Rarely standalone._

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Longest Substring Without Repeating (3) | Sliding Window + Set | Medium | Move left ptr past duplicate |
| 🔴 Valid Parentheses (20) | Stack | Easy | Push open, pop/match on close |
| 🟠 Minimum Window Substring (76) | Sliding Window + HashMap | Hard | Contract when all chars covered |
| 🟠 Group Anagrams (49) | HashMap + Sort | Medium | Sorted string as key |
| 🟠 Longest Palindromic Substring (5) | Expand Around Center | Medium | Try each center (odd+even) |
| 🟠 String to Integer / atoi (8) | Parsing | Medium | Handle sign, overflow, non-digit |
| 🟡 Decode Ways (91) | DP | Medium | dp[i] depends on 1-digit and 2-digit decode |

---

### 7. Intervals
_Merge Intervals and Insert Interval appear repeatedly in Amazon OA and onsite._

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Merge Intervals (56) | Sort + Scan | Medium | Sort by start; merge if curr.start ≤ prev.end |
| 🔴 Insert Interval (57) | Scan + Merge | Medium | Three phases: before overlap, overlap, after overlap |
| 🟠 Meeting Rooms II (253) | Min-Heap / Sweep | Medium | Heap of end times; pop if end ≤ curr.start |
| 🟠 Non-overlapping Intervals (435) | Greedy | Medium | Sort by end; greedily keep earliest-ending |
| 🟡 Employee Free Time (759) | Merge Intervals | Hard | Flatten all intervals, sort, find gaps |

---

### 8. Binary Search
_Search in Rotated Array is near-certain. Parametric search is a follow-up trick._

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Search in Rotated Sorted Array (33) | Modified Binary Search | Medium | One half always sorted; check which |
| 🟠 Find Minimum in Rotated Array (153) | Binary Search | Medium | mid > right → min in right half |
| 🟠 Koko Eating Bananas (875) | Search on answer space | Medium | Binary search on speed k |
| 🟠 Binary Search on Answer (generic) | Parametric Search | Medium | "Is X achievable?" as predicate |
| 🟡 Median of Two Sorted Arrays (4) | Binary Search on partition | Hard | Partition smaller array |

---

### 9. Linked Lists
_Reverse and Merge are easy — don't drop points here. LRU is a design-coding crossover._

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Reverse Linked List (206) | Iterative / Recursive | Easy | Prev/curr/next triple swap |
| 🔴 Merge Two Sorted Lists (21) | Merge | Easy | Dummy head pattern |
| 🟠 LRU Cache (146) | HashMap + DLL | Medium | O(1) get/put; dummy head/tail |
| 🟠 Linked List Cycle II (142) | Floyd's Algorithm | Medium | Meet point + reset one ptr to head |
| 🟠 Reverse Nodes in k-Group (25) | In-place Reversal | Hard | Count k, reverse group, reconnect |
| 🟡 Add Two Numbers (2) | List traversal | Medium | Carry through; handle different lengths |

---

## PRIORITY TIER 3 — Know the Template, Drill Lightly
> 1 problem max per loop. Know the template and 2 canonical problems. Don't over-invest.

---

### 10. Stack / Monotonic Stack

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🔴 Daily Temperatures (739) | Monotonic Decreasing Stack | Medium | Stack of indices; pop when warmer |
| 🔴 Largest Rectangle in Histogram (84) | Monotonic Increasing Stack | Hard | Pop when bar shorter; width = right - left - 1 |
| 🟠 Min Stack (155) | Auxiliary stack | Easy | Pair (val, current_min) |
| 🟠 Next Greater Element (496, 503) | Monotonic Stack | Medium | Process right-to-left or circular trick |
| 🟡 Decode String (394) | Stack | Medium | Push (count, built_str) on '[' |

---

### 11. Backtracking

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🟠 Subsets I & II (78, 90) | Backtracking | Medium | Include/exclude; skip dup on same level |
| 🟠 Combination Sum I & II (39, 40) | Backtracking | Medium | Sort + skip dup; reuse only in I |
| 🟠 Permutations (46, 47) | Backtracking + used[] | Medium | Swap or visited array |
| 🟠 Letter Combinations of Phone (17) | Backtracking | Medium | Map digits to chars; recurse |
| 🟡 Palindrome Partitioning (131) | Backtracking + DP | Medium | Precompute isPalin[i][j] |
| 🟡 N-Queens (51) | Backtracking | Hard | Track col, diag1, diag2 sets |

---

## PRIORITY TIER 4 — Skim Only
> Skip unless interviewing for a specific team (Maps, Systems, Search). Know they exist.

---

### 12. Graphs — Weighted / Shortest Path

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🟠 Network Delay Time (743) | Dijkstra | Medium | Min-heap on (dist, node); relax neighbors |
| 🟠 Cheapest Flights Within K Stops (787) | Bellman-Ford / BFS | Medium | Bellman-Ford k+1 rounds |
| 🟡 Path with Minimum Effort (1631) | Dijkstra variant | Medium | Minimize max edge weight on path |

**Dijkstra template:**
```python
import heapq
dist = {node: float('inf') for node in graph}
dist[src] = 0
heap = [(0, src)]
while heap:
    d, u = heapq.heappop(heap)
    if d > dist[u]: continue
    for v, w in graph[u]:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            heapq.heappush(heap, (dist[v], v))
```

---

### 13. Trie

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| 🟡 Implement Trie (208) | Trie | Medium | children dict + is_end flag |
| 🟡 Word Search II (212) | Trie + DFS | Hard | Build trie from words; DFS on board |

---

## BONUS — LLD / Class Design (coding round variant)
_Amazon asks this especially for SDE-2+ in platform/infrastructure teams._

| System | Key Classes / Patterns |
|---|---|
| **Parking Lot** | ParkingLot, Floor, Spot(type), Ticket, Fee strategy |
| **Library Management** | Book, Member, Loan, Search(by title/author), Fine |
| **Elevator System** | Elevator, Request(up/down), Scheduler (SCAN/SSTF) |
| **Vending Machine** | Item, Slot, Inventory, Payment(strategy), Dispense |
| **Amazon Locker** | Locker, Package, Code, Assignment(size-fit), Expiry |

**LLD approach (10-min structure):**
1. Clarify actors, core operations, edge cases
2. List entities (nouns) → classes; operations (verbs) → methods
3. Identify patterns: Strategy, Factory, Singleton, Observer
4. Write skeleton: class names, key fields, method signatures

---

## BONUS — Amazon OA / Online Assessment Common

| Problem | Pattern | Difficulty | Key Insight |
|---|---|---|---|
| LRU Cache (146) | HashMap + DLL | Medium | Classic OA; O(1) get/put |
| Design Hit Counter | Sliding window / deque | Medium | Evict timestamps > 300s old |
| Maximum Units on Truck (1710) | Greedy | Easy | Sort by units/box desc; fill until capacity |
| Reorder Log Files (937) | Custom sort | Easy | Letter logs first (lex by content then id) |
| Most Common Word (819) | HashMap + parsing | Easy | Lowercase, strip punct, skip banned |
| Minimum Refueling Stops (871) | Max-heap greedy | Hard | At each stop push fuel; pop max when tank empty |
| Brick Wall (554) | HashMap on gaps | Medium | Count edge positions; answer = n - max(gap_counts) |
| Prison Cells After N Days (957) | Cycle detection | Medium | State repeats in ≤256 cycles |
| Advantage Shuffle (870) | Greedy | Medium | Sort both; assign smallest winning num or smallest losing |
| Number of Visible People in Queue (1944) | Monotonic Stack | Hard | Decreasing stack; count pops + 1 if stack non-empty |
