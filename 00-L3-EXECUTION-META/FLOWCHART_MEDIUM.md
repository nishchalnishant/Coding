# Medium-Level Problem Flowchart — Google L3

> **How to use:** Read the problem → scan for signals → follow the arrow.
> Each node is a decision. Leaf nodes (→ boxes) are the algorithm to code.

---

## 🗺 MASTER ROUTER — Start Here

```mermaid
flowchart TD
    START(["📋 Read the Problem"])
    START --> Q1{"What is the\ninput shape?"}

    Q1 -->|"Array / String"| ARR["🔢 Go to:\nArray & String"]
    Q1 -->|"Grid / Matrix"| GRID["🔲 Go to:\nGrid"]
    Q1 -->|"Linked List"| LL["🔗 Go to:\nLinked List"]
    Q1 -->|"Tree / BST"| TREE["🌲 Go to:\nTree"]
    Q1 -->|"Graph / nodes+edges"| GRAPH["🕸 Go to:\nGraph"]
    Q1 -->|"Numbers / counting"| MATH["🔢 Go to:\nDP & Math"]

    ARR --> Q2{"What are you\noptimizing?"}
    Q2 -->|"Subarray / Substring"| SUBARR["🔵 Array Detail"]
    Q2 -->|"Finding target in sorted"| BS["⬛ Binary Search"]
    Q2 -->|"Count / enumerate all"| BT["🔴 Backtracking"]

    click ARR "#array--string-flowchart"
    click GRID "#grid-flowchart"
    click LL "#linked-list-flowchart"
    click TREE "#tree-flowchart"
    click GRAPH "#graph-flowchart"
```

---

## 🔵 Array & String Flowchart

```mermaid
flowchart TD
    A(["Array / String Problem"])

    A --> S1{"Is the array\nSORTED?"}

    S1 -->|YES| S2{"Need to find\na PAIR or TRIPLET?"}
    S1 -->|NO| U1{"Key operation?"}

    S2 -->|YES| TP["✅ TWO POINTERS\nConverging lo/hi\n─────────────────\n• 3Sum\n• Container With Most Water\n• Two Sum II"]
    S2 -->|"Find target value"| BSEARCH["✅ BINARY SEARCH\nlo ≤ hi template\n─────────────────\n• Search Rotated Array\n• Find Minimum Rotated\n• Search 2D Matrix"]
    S2 -->|"Find min K where feasible"| BSANS["✅ BINARY SEARCH\nON ANSWER\nfeasible(mid) predicate\n─────────────────\n• Koko Eating Bananas\n• Capacity to Ship Packages"]

    U1 -->|"Subarray sum = K"| PS["✅ PREFIX SUM\n+ HashMap\n─────────────────\n• Subarray Sum = K\n• Continuous Subarray Sum"]
    U1 -->|"Longest substring\nwith constraint"| SW1["✅ VARIABLE\nSLIDING WINDOW\nshrink when invalid\n─────────────────\n• Longest Substr No Repeat\n• Min Window Substring\n• Longest Char Replacement"]
    U1 -->|"Fixed window\nof size K"| SW2["✅ FIXED\nSLIDING WINDOW\nmatch-count trick\n─────────────────\n• Find All Anagrams\n• Permutation in String"]
    U1 -->|"Max in window K"| MQ["✅ MONOTONIC DEQUE\nstore indices, not values\n─────────────────\n• Sliding Window Maximum"]
    U1 -->|"Next greater element\nfor each index"| MS["✅ MONOTONIC STACK\ndecreasing, pop on larger\n─────────────────\n• Daily Temperatures\n• Largest Rect in Histogram"]
    U1 -->|"Count / ways\nto reach target"| DP1["✅ 1D DP\ndefine dp[i]\n─────────────────\n• Climbing Stairs\n• House Robber\n• Coin Change"]
    U1 -->|"Frequency / grouping"| HM["✅ HASHMAP\nCounter / defaultdict\n─────────────────\n• Group Anagrams\n• Top K Frequent\n• Longest Consecutive"]
```

---

## 🔲 Grid / Matrix Flowchart

```mermaid
flowchart TD
    G(["Grid / Matrix Problem"])

    G --> G1{"What are\nyou asked?"}

    G1 -->|"Count connected\nregions / islands"| G2["✅ DFS / BFS FLOOD FILL\nmark visited in-place\n─────────────────\n• Number of Islands\n• Max Area of Island\n• Surrounded Regions"]

    G1 -->|"Shortest path\nin 0/1 grid"| G3{"Weights?"}
    G3 -->|"All cells = cost 1"| G4["✅ BFS\nfirst reach = shortest\n─────────────────\n• Shortest Path Binary Matrix\n• 01 Matrix\n• Walls and Gates"]
    G3 -->|"Different weights"| G5["✅ DIJKSTRA\nor 0-1 BFS\n─────────────────\n• Swim in Rising Water\n• Minimum Effort Path"]

    G1 -->|"Spread simultaneously\nfrom multiple sources"| G6["✅ MULTI-SOURCE BFS\nseed all sources at t=0\n─────────────────\n• Rotting Oranges\n• Pacific Atlantic Water Flow"]

    G1 -->|"Count paths\nfrom top-left to bottom-right"| G7["✅ GRID DP\ndp[r][c] = dp[r-1][c] + dp[r][c-1]\n─────────────────\n• Unique Paths\n• Unique Paths II\n• Maximal Square"]

    G1 -->|"Find word in grid"| G8["✅ BACKTRACKING\nDFS + in-place mark\n─────────────────\n• Word Search\n• Word Search II (+ Trie)"]
```

---

## 🔗 Linked List Flowchart

```mermaid
flowchart TD
    L(["Linked List Problem"])

    L --> L1{"Core operation?"}

    L1 -->|"Reverse the list\nor a segment"| L2["✅ THREE-POINTER\nprev / curr / nxt\nSave nxt FIRST\n─────────────────\n• Reverse Linked List\n• Reverse K-Group"]

    L1 -->|"Find cycle\nor cycle entry"| L3["✅ FAST & SLOW\nFLOYD'S ALGO\n─────────────────\n• Linked List Cycle\n• Linked List Cycle II\n• Find Middle of List"]

    L1 -->|"Remove N-th\nfrom end"| L4["✅ TWO-POINTER\nOFFSET BY N\nadvance fast N steps first\n─────────────────\n• Remove Nth From End"]

    L1 -->|"Merge / Sort"| L5{"How many lists?"}
    L5 -->|"Two sorted lists"| L6["✅ DUMMY HEAD\n+ two pointers\n─────────────────\n• Merge Two Sorted Lists"]
    L5 -->|"K sorted lists"| L7["✅ K-WAY MERGE\nmin-heap (val, idx, node)\n─────────────────\n• Merge K Sorted Lists"]

    L1 -->|"Reorder list\nL0→Ln→L1→Ln-1"| L8["✅ 3 STEPS\n1. Find middle\n2. Reverse second half\n3. Weave together\n─────────────────\n• Reorder List"]

    L1 -->|"Palindrome check"| L9["✅ FIND MID\n+ REVERSE HALF\n+ compare\n─────────────────\n• Palindrome Linked List"]

    L1 -->|"O(1) get/put\nwith eviction"| L10["✅ HASHMAP\n+ DOUBLY LINKED LIST\n─────────────────\n• LRU Cache"]
```

---

## 🌲 Tree Flowchart

```mermaid
flowchart TD
    T(["Tree Problem"])

    T --> T1{"What do you\nneed to compute?"}

    T1 -->|"Level-by-level\nresult"| T2["✅ BFS\nlevel-size snapshot\n─────────────────\n• Level Order Traversal\n• Zigzag Level Order\n• Right Side View"]

    T1 -->|"Path / distance\nbetween nodes"| T3{"Path goes\nthrough root?"}
    T3 -->|"Can cross root\n(any → any)"| T4["✅ TREE DP\npostorder, global closure\nreturn SINGLE ARM up\n─────────────────\n• Binary Tree Max Path Sum\n• Diameter of Binary Tree"]
    T3 -->|"Root to leaf only"| T5["✅ DFS\npass running sum down\n─────────────────\n• Path Sum I & II\n• Path Sum III (prefix sum)"]

    T1 -->|"Validate / search\nin BST"| T6["✅ BST PROPERTY\npass (lo, hi) bounds\nOR use inorder (sorted)\n─────────────────\n• Validate BST\n• Kth Smallest in BST\n• LCA of BST"]

    T1 -->|"Lowest Common\nAncestor (general tree)"| T7["✅ POSTORDER DFS\nboth sides non-null → node is LCA\n─────────────────\n• LCA of Binary Tree"]

    T1 -->|"Build tree from\ntraversals"| T8["✅ PREORDER + INORDER\nHashMap inorder for O(1) split\n─────────────────\n• Construct from Pre+Inorder"]

    T1 -->|"Serialize / deserialize"| T9["✅ PREORDER\n+ null markers\n─────────────────\n• Serialize Binary Tree"]

    T1 -->|"Rob / select nodes\nno two adjacent"| T10["✅ TREE DP\ndfs returns (rob, skip) tuple\n─────────────────\n• House Robber III\n• Binary Tree Cameras"]
```

---

## 🕸 Graph Flowchart

```mermaid
flowchart TD
    GR(["Graph Problem"])

    GR --> GR1{"Directed or\nUndirected?"}

    GR1 -->|"UNDIRECTED"| GR2{"What is asked?"}
    GR1 -->|"DIRECTED"| GR5{"What is asked?"}

    GR2 -->|"Count / detect\nconnected components"| GR3["✅ DFS / BFS\nor UNION-FIND\n─────────────────\n• Number of Islands\n• Number of Provinces\n• Graph Valid Tree"]

    GR2 -->|"Find extra edge\ncreating cycle"| GR4["✅ UNION-FIND\nfind(u)==find(v) → cycle\n─────────────────\n• Redundant Connection"]

    GR2 -->|"Merge groups\nby shared property"| GR4B["✅ UNION-FIND\nemail → root mapping\n─────────────────\n• Accounts Merge"]

    GR2 -->|"Shortest path\n(unweighted)"| GR4C["✅ BFS\nmark visited BEFORE enqueue\n─────────────────\n• Word Ladder\n• Open the Lock"]

    GR5 -->|"Prerequisite ordering\n/ can finish?"| GR6["✅ KAHN'S TOPO SORT\ncycle ↔ len(order) < n\nedge: prereq → course\n─────────────────\n• Course Schedule I & II\n• Alien Dictionary"]

    GR5 -->|"All paths\nsource → target"| GR7["✅ DFS BACKTRACK\nno visited set (DAG)\n─────────────────\n• All Paths Source to Target"]

    GR5 -->|"Bipartite check\n2-coloring"| GR8["✅ BFS/DFS\n2-color on conflict → false\n─────────────────\n• Is Graph Bipartite?"]

    GR5 -->|"Weighted shortest\npath (no negatives)"| GR9["✅ DIJKSTRA\nmin-heap (dist, node)\nskip stale: if d > dist[u]: continue\n─────────────────\n• Network Delay Time\n• Cheapest Flights K Stops\n  (use Bellman-Ford for K stops)"]

    GR5 -->|"Reverse flow /\nfind upstream"| GR10["✅ REVERSE BFS\nfrom destination border\n─────────────────\n• Pacific Atlantic Water Flow"]
```

---

## 🧩 DP / Backtracking Flowchart

```mermaid
flowchart TD
    D(["Optimization /\nCounting / Enumeration"])

    D --> D1{"Do you need\nALL solutions?"}

    D1 -->|"YES — enumerate all"| D2{"Input\nhas duplicates?"}
    D2 -->|NO| D3["✅ BACKTRACKING\n+ start index\ncopy path at base case\n─────────────────\n• Subsets\n• Combination Sum\n• Permutations\n• Generate Parentheses"]
    D2 -->|YES| D4["✅ BACKTRACKING\n+ DEDUP\nsort first;\nskip if nums[i]==nums[i-1]\n─────────────────\n• Subsets II\n• Permutations II\n• Combination Sum II"]

    D1 -->|"NO — find optimal\nor count"| D5{"Overlapping\nsubproblems?"}

    D5 -->|YES| D6{"State space\nshape?"}

    D6 -->|"1D sequence"| D7["✅ 1D DP\ndp[i] from dp[i-1] or dp[i-2]\n─────────────────\n• Climbing Stairs\n• House Robber\n• Decode Ways\n• Word Break"]

    D6 -->|"Two sequences\nor 2D"| D8["✅ 2D DP\ndp[i][j] = match or skip\n─────────────────\n• LCS\n• Edit Distance\n• Interleaving String\n• Unique Paths"]

    D6 -->|"Pick items with\nweight / budget"| D9{"Items reusable?"}
    D9 -->|NO| D10["✅ 0/1 KNAPSACK\niterate W BACKWARD\n─────────────────\n• Partition Equal Subset\n• Target Sum\n• Last Stone Weight II"]
    D9 -->|YES| D11["✅ UNBOUNDED KNAPSACK\niterate W FORWARD\n─────────────────\n• Coin Change I\n• Coin Change II\n• Combination Sum IV"]

    D6 -->|"Grid movement\n(right/down)"| D12["✅ GRID DP\ndp[r][c] = dp[r-1][c] + dp[r][c-1]\n─────────────────\n• Unique Paths\n• Maximal Square"]

    D6 -->|"Stock buy/sell\nwith states"| D13["✅ STATE MACHINE DP\ntrack held/cash/cooldown\n─────────────────\n• Stock with Cooldown\n• Stock with Fee"]

    D5 -->|NO — greedy\nworks"| D14{"Problem type?"}

    D14 -->|"Interval / scheduling"| D15["✅ GREEDY\nsort by END time\n─────────────────\n• Merge Intervals\n• Non-overlapping Intervals\n• Meeting Rooms II"]

    D14 -->|"Jump / reach end"| D16["✅ GREEDY\ntrack farthest reachable\n─────────────────\n• Jump Game I & II"]

    D14 -->|"Task scheduling\nwith cooldown"| D17["✅ GREEDY / MATH\nmax_f formula\n─────────────────\n• Task Scheduler"]
```

---

## 🟡 Heap / Priority Queue Flowchart

```mermaid
flowchart TD
    H(["Need to repeatedly\nextract min or max"])

    H --> H1{"How many\nstreams?"}

    H1 -->|"Single stream\nK largest"| H2["✅ MIN-HEAP SIZE K\nroot = K-th largest\nO(N log K)\n─────────────────\n• Kth Largest Element\n• K Closest Points\n• Top K Frequent Elements"]

    H1 -->|"K sorted\nstreams/lists"| H3["✅ K-WAY MERGE\nmin-heap (val, list_idx, elem)\nO(N log K)\n─────────────────\n• Merge K Sorted Lists\n• Find K Pairs Smallest Sums\n• Kth Smallest in Matrix"]

    H1 -->|"Dynamic median\n(stream of numbers)"| H4["✅ TWO HEAPS\nmax-heap lower half\nmin-heap upper half\nrebalance: |lo|-|hi| ≤ 1\n─────────────────\n• Find Median from Stream\n• Sliding Window Median"]

    H1 -->|"Schedule tasks\nalways pick best"| H5{"Pick max profit\nor min cost?"}
    H5 -->|"Max profit"| H6["✅ MAX-HEAP\n(negate in Python)\n─────────────────\n• IPO / Maximize Capital\n• Task Scheduler\n• Reorganize String"]
    H5 -->|"Min cost"| H7["✅ MIN-HEAP\n─────────────────\n• Minimum Cost to\n  Connect Ropes\n• Single-Threaded CPU"]

    H1 -->|"Meeting rooms\n/ interval overlap"| H8["✅ MIN-HEAP\nof end times\nsort by start first\n─────────────────\n• Meeting Rooms II\n• Car Pooling"]
```

---

## ⚡ One-Line Signal Map (Quick Scan)

> Scan this in 30 seconds. Find your keyword. Jump to the right flowchart.

```
SIGNAL                              → PATTERN               → FLOWCHART
─────────────────────────────────────────────────────────────────────────
sorted + find pair/triplet          → Two Pointers           → Array
unsorted + find sum pair            → HashMap complement     → Array
subarray sum = K                    → Prefix Sum + Map       → Array
longest / shortest substring        → Sliding Window         → Array
max in window of K                  → Monotonic Deque        → Array
next greater element                → Monotonic Stack        → Array
find target in sorted               → Binary Search          → Array
minimize K where feasible           → BS on Answer           → Array
count connected regions             → DFS/BFS Flood Fill     → Grid
shortest path in 0/1 grid           → BFS                    → Grid
shortest path with weights          → Dijkstra               → Grid
spread from multiple sources        → Multi-source BFS       → Grid
count paths top-left→bottom-right   → Grid DP                → Grid
find word in grid                   → Backtracking + mark    → Grid
reverse / reorder list              → Three Pointers         → Linked List
cycle / midpoint detection          → Fast & Slow Pointers   → Linked List
merge K sorted                      → K-way Heap             → Linked List
level-by-level output               → BFS + snapshot         → Tree
max path / diameter                 → Tree DP postorder      → Tree
validate BST / search BST           → Bounds DFS or Inorder  → Tree
lowest common ancestor              → Postorder DFS          → Tree
prerequisite / dependency           → Kahn's Topo Sort       → Graph
cycle in directed graph             → Kahn's or 3-color DFS  → Graph
connectivity in undirected          → Union-Find / DFS       → Graph
weighted shortest path              → Dijkstra               → Graph
all combinations / subsets          → Backtracking           → DP
minimize / maximize (overlapping)   → DP                     → DP
interval scheduling / merge         → Greedy (sort by end)   → DP
K-th largest / dynamic extremum     → Heap                   → Heap
dynamic median                      → Two Heaps              → Heap
merge K sorted streams              → K-way Heap             → Heap
```

---

← [DECISION_GUIDE.md](./DECISION_GUIDE.md) · ← [ds_tree.md](../01-data-structures/ds_tree.md) · ← [algorithm_tree.md](../02-algorithms/algorithm_tree.md)
