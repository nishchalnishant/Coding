---
module: root
topic: Flowcharts
subtopic: 
status: unread
tags: [root, flowcharts]
---
# Google SDE-2 Prep — Flowcharts
_Last updated: 2026-05-17 (gap audit pass)_

How to use: each block = one file. Follow arrows for key decision points, trigger conditions, complexities, and canonical problems. Use this for quick revision before a session or on interview day.

---

## 00 — Start Here

```
00-start-here/README.md
└── Entry point
    ├── Have 28+ days? → Follow 4-week plan (Week 1: Arrays/Strings, Week 2: Trees/Graphs, Week 3: DP, Week 4: Heaps/Tries)
    ├── Have 14 days? → Must-nail only: Arrays · Trees · Graphs · DP · Binary Search
    ├── Have 7 days?  → patterns-master.md → top-K problems per pattern → behavioral
    ├── Have 48 hrs?  → Hour 0-8: patterns-master end-to-end + drill 1E/1M per pattern
    │                   Hour 8-16: 05-revision/README.md + GOOGLE_QUICK_SHEET
    │                   Hour 16-24: 3 timed mocks (DP + Graph + free) + 3 STAR stories aloud
    │                   Hour 24-48: Sleep 8h → light review only → no new topics
    └── Interview day 30 min → interview-cheatsheet → complexity table → Python gotchas → STAR titles
```

---

## 01 — Data Structures

```
01-data-structures/array.md
└── Arrays [O(1) access · O(n) insert/delete]
    ├── Two Pointers → sorted array / linked list → target sum · remove duplicates · container with most water
    ├── Sliding Window → subarray/substring → max sum subarray · longest substring without repeat
    ├── Prefix Sum → range sum queries → subarray sum equals K · product except self
    ├── Kadane's → max subarray → O(n) time O(1) space
    └── Sorting-based → merge intervals · meeting rooms · 3Sum

01-data-structures/hashing.md
└── Hash Maps [O(1) avg insert/search/delete]
    ├── Frequency Map → anagram groups · top-K elements · first unique char
    ├── Two Sum pattern → one-pass O(n) · complement lookup
    ├── Grouping → group anagrams · isomorphic strings
    └── Rolling Hash → Rabin-Karp substring search · repeated DNA sequences

01-data-structures/string.md
└── Strings [immutable char array · O(k) substring · O(n²) concat in loop]
    ├── Frequency Map → anagram check · group anagrams · find all anagrams in string
    ├── Two Pointers → palindrome check · longest palindromic substring (expand around center)
    ├── Sliding Window (variable) → longest substring without repeat · min window substring · at-most-K distinct
    ├── Sliding Window (fixed) → find all anagrams · permutation in string
    ├── Prefix Sum on chars → count substrings with exactly K vowels / specific char counts
    └── String Hashing → detect duplicate substrings · repeated DNA sequences

01-data-structures/linked-list.md
└── Linked Lists [O(n) access · O(1) insert at pointer]
    ├── Fast/Slow Pointers → cycle detect · middle of list · cycle entry point
    ├── Dummy Node → merge sorted lists · remove Nth from end
    ├── Reverse In-Place → reverse linked list · reverse groups of K
    └── Two-list merge → merge K sorted lists (use heap)

01-data-structures/stack.md
└── Stacks [O(1) push/pop]
    ├── Monotonic Stack (decreasing) → Next Greater Element · Daily Temperatures · Largest Rectangle in Histogram
    ├── Monotonic Stack (increasing) → Next Smaller Element · Trapping Rain Water
    ├── Bracket Matching → valid parentheses · min removes · score of brackets
    └── Expression evaluation → basic calculator · reverse Polish notation

01-data-structures/queue.md
└── Queues / Deques [O(1) enqueue/dequeue]
    ├── BFS → shortest path unweighted · level-order tree · rotting oranges · word ladder
    ├── Monotonic Deque (max) → sliding window maximum · O(n) time
    └── Priority Queue (heap) → Dijkstra · top-K · median maintenance

01-data-structures/tree.md
└── Trees / BST [O(log n) avg BST ops]
    ├── DFS Pre-order  → serialize/deserialize · construct from preorder
    ├── DFS In-order   → BST sorted output · kth smallest · validate BST
    ├── DFS Post-order → subtree problems · diameter · balanced check
    ├── BFS (level)    → level-order · right side view · zigzag traversal
    ├── LCA            → binary lifting / recursive O(n)
    ├── Path Sum       → root-to-leaf · any path · max path sum
    └── Morris Traversal → O(1) space inorder

01-data-structures/graphs.md
└── Graphs [V vertices · E edges]
    ├── BFS → O(V+E) · shortest path (unweighted) · bipartite check · walls and gates
    ├── DFS → O(V+E) · cycle detection · connected components · number of islands
    ├── Topological Sort (Kahn's) → O(V+E) · course schedule · build order
    ├── Union-Find → O(α·n) ≈ O(1) · dynamic connectivity · redundant connection
    ├── Dijkstra (min-heap) → O((V+E)logV) · network delay · cheapest flights
    └── Bellman-Ford → O(VE) · negative weights · detect negative cycle

01-data-structures/heap.md
└── Heaps [O(log n) push/pop · O(n) heapify]
    ├── Top-K largest → min-heap size K → O(n log k)
    ├── Top-K smallest → max-heap size K → negate values in Python
    ├── Merge K sorted lists → min-heap of (val, list_idx, elem_idx)
    ├── Two-Heap Median → max-heap left | min-heap right → balance on insert
    └── Dijkstra → (dist, node) in min-heap → relax neighbors

01-data-structures/trie.md
└── Tries [O(m) insert/search — m = word length]
    ├── Prefix search → autocomplete · starts-with check · implement Trie
    ├── Word Break → DP + Trie to find valid splits
    ├── Word Search II → Trie + DFS backtrack on grid
    └── XOR Maximum → binary Trie for max XOR of two numbers

01-data-structures/segment-tree.md
└── Segment Trees [O(log n) query/update · O(n) build]
    ├── Range Sum Query → build once · point update · range query
    ├── Range Min/Max Query → same structure · different merge function
    └── Lazy Propagation → range update in O(log n) → range sum with add

01-data-structures/advanced-structures.md
└── Advanced [Know use-case; unlikely to implement from scratch at L4]
    ├── Fenwick Tree (BIT) → prefix sums with O(log n) update · simpler than seg tree
    ├── Bloom Filter → probabilistic set membership · false positives OK · no false negatives
    └── Skip List → sorted structure with O(log n) avg · alternative to balanced BST
```

---

## 02 — Algorithms (Flat Files)

```
02-algorithms/two-pointers.md
└── Two Pointers
    ├── Converging (left+right) → sorted array · two sum II · 3Sum · container with most water
    ├── Fast/Slow → linked list cycle · middle of list · remove duplicates
    └── Same-direction → sliding window base · partition · Dutch flag

02-algorithms/sliding-window.md
└── Sliding Window
    ├── Fixed size → max sum of size-K subarray · contains duplicate within K distance
    ├── Variable size (shrink when invalid) → longest substring without repeat · min window substring
    ├── Frequency map → permutation in string · anagram in string
    └── Monotonic deque → sliding window maximum · O(n)

02-algorithms/binary-search.md
└── Binary Search
    ├── Standard → O(log n) · sorted array · search insert position
    ├── Lower bound → first position ≥ target → bisect_left
    ├── Upper bound → first position > target → bisect_right
    ├── Rotated array → find pivot first · then binary search half
    ├── BS on answer → minimize max / maximize min → guess + validate in O(n)
    └── 2D matrix → treat as 1D with idx // cols, idx % cols

02-algorithms/sorting.md
└── Sorting
    ├── Merge Sort  → O(n log n) stable · count inversions · external sort
    ├── Quick Sort  → O(n log n) avg O(n²) worst · in-place · quick select for k-th
    ├── Heap Sort   → O(n log n) · O(1) space · not stable
    ├── Counting Sort → O(n+k) · bounded integers · frequency array
    └── Custom sort → sort by multiple keys · Schwartzian transform in Python

02-algorithms/greedy.md
└── Greedy
    ├── Interval scheduling → sort by end time · activity selection
    ├── Interval merging → sort by start · merge overlapping
    ├── Jump Game → track max reach · O(n)
    └── Huffman / Task Scheduler → frequency-based greedy + heap

02-algorithms/divide-and-conquer.md
└── Divide & Conquer
    ├── Merge Sort → inversion count as side-effect
    ├── Quick Select → O(n) avg k-th largest without full sort
    └── Closest Pair of Points → O(n log n) · split + merge strip

02-algorithms/backtracking.md
└── Backtracking [O(2^n) subsets · O(n!) permutations]
    ├── Subsets → choose/skip at each index · power set
    ├── Permutations → swap in-place or used[] array
    ├── Combinations → start index to avoid duplicates · k-of-n
    ├── N-Queens → row-by-row · col+diag sets for O(1) conflict check
    └── Sudoku Solver → try 1-9 · recurse · undo on failure

02-algorithms/union-find.md
└── Union-Find [O(α·n) ≈ O(1) with path compress + rank]
    ├── Connected components → find() with path compression
    ├── Cycle detection in undirected graph → union returns False if same component
    ├── Kruskal's MST → sort edges by weight · union if different components
    └── Dynamic connectivity → accounts merge · friend circles

02-algorithms/bit-manipulation.md
└── Bit Manipulation
    ├── XOR tricks → single number · missing number · find two non-repeating
    ├── Bit masking → subset enumeration · bitmask DP
    ├── Power of 2 → n & (n-1) == 0
    └── Brian Kernighan → count set bits: n &= (n-1) until 0

02-algorithms/graph.md
└── Graph Algorithms
    ├── BFS → deque · visited set · layer-by-layer
    ├── DFS → recursive or explicit stack · pre/post hooks
    ├── Topological Sort (Kahn's) → in-degree array · queue of 0-in-degree nodes
    ├── Dijkstra → min-heap · relax if dist[nbr] > dist[u] + w
    └── Bellman-Ford → V-1 rounds of all-edge relaxation · detect neg cycle on round V

02-algorithms/advanced-graphs.md
└── Advanced Graphs
    ├── Floyd-Warshall → O(V³) all-pairs · dp[i][j] = min(dp[i][j], dp[i][k]+dp[k][j])
    ├── Prim's MST → min-heap of (weight, node) · visited set
    ├── Bridges & Articulation Points → Tarjan's DFS · low[] and disc[] arrays
    └── A* → heuristic-guided BFS · f = g + h

02-algorithms/string.md
└── String Algorithms
    ├── KMP → O(n+m) · failure function (LPS array) · no backtrack on text
    ├── Rabin-Karp → O(n+m) avg · rolling hash · substring search
    ├── Z-algorithm → O(n) · Z[i] = length of longest prefix match at i
    └── Manacher's → O(n) longest palindromic substring

02-algorithms/maths.md
└── Math
    ├── GCD / LCM → Euclidean: gcd(a,b) = gcd(b, a%b) · lcm = a*b // gcd
    ├── Sieve of Eratosthenes → O(n log log n) · all primes ≤ n
    ├── Modular arithmetic → (a*b) % m = ((a%m) * (b%m)) % m
    └── Combinatorics → nCr with Pascal's / modular inverse

02-algorithms/searching.md
└── Searching
    ├── Linear scan → O(n) · unsorted / small n
    ├── Binary search → O(log n) · sorted
    └── Exhaustive / BFS/DFS → O(2^n or V+E) · state space problems

02-algorithms/concurrency.md
└── Concurrency [SDE-3 depth; SDE-2: know the patterns]
    ├── Visibility vs Atomicity → volatile fixes visibility; AtomicInteger fixes atomicity
    ├── Deadlock (4 conditions) → Mutual Exclusion · Hold+Wait · No Preemption · Circular Wait
    │   └── Fix → break any one; most common: resource ordering (break circular wait)
    ├── Bounded Blocking Queue → Condition + deque; enqueue waits when full, dequeue waits when empty
    ├── Dining Philosophers → circular deadlock example; fix: philosopher N reverses fork pick-up order
    └── Semaphore vs Mutex → semaphore counts (N permits); mutex is binary ownership lock

02-algorithms/system-design-algorithms.md
└── System Design Algorithms [distributed systems building blocks]
    ├── Bloom Filter → probabilistic set membership · false positives OK · no false negatives
    │   └── Use case: check username taken without DB hit · malicious URL filter · Cassandra/BigTable
    ├── HyperLogLog → estimate unique elements · 1.5 KB for 1B users · 2% error
    │   └── Use case: DAU counting · cardinality estimation in analytics pipelines
    ├── Consistent Hashing → map nodes+keys to circular ring · only 1/N keys reshuffle on node change
    │   └── Use case: distributed cache · Dynamo/Cassandra · add virtual nodes for uniform distribution
    ├── Rate Limiting → token bucket (smooth bursts) vs leaky bucket (strict rate) vs sliding window log
    └── Count-Min Sketch → frequency estimation in stream · O(1) update · sublinear space

02-algorithms/miscellaneous.md
└── Miscellaneous Advanced Structures [SDE-3 level; SDE-2: know use-cases]
    ├── Fenwick Tree (BIT) → dynamic prefix sums · O(log n) update+query · 1-indexed · ~5x less code than seg tree
    │   └── Use case: count inversions · range sum with point updates · coordinate compression problems
    ├── Sparse Table → O(n log n) build · O(1) range min/max · static only (no updates) · idempotent ops
    ├── Sweep Line → sort events by x · process with active set · O(n log n) total
    │   └── Use case: skyline problem · rectangle area union · interval overlap counting
    ├── LRU Cache → HashMap + doubly linked list · O(1) get and put · move to head on access
    └── LFU Cache → 3 maps (key→val, key→freq, freq→OrderedDict) + min_freq tracker · O(1) all ops

02-algorithms/problem-deep-dives.md
└── Problem Deep-Dives [100+ canonical problems: description + pseudocode]
    ├── Arrays / Prefix Sums / Hashing section → Two Sum · Group Anagrams · Product Except Self · ...
    ├── Trees section → LCA · Serialize/Deserialize · Max Path Sum · ...
    ├── Graphs section → Word Ladder · Clone Graph · Pacific Atlantic · ...
    ├── DP section → Edit Distance · Burst Balloons · Word Break · ...
    └── Use: before a session to refresh pseudocode; after seeing a problem to check your approach

02-algorithms/algorithm_tree.md
└── Algorithm Decision Tree [problem type → algorithm → template]
    ├── Sorting & Partitioning → Merge/Quick/QuickSelect/Dutch Flag/Counting/Custom comparator
    ├── Searching → Binary Search variants · BS on answer · Rotated array · Median finding
    ├── Graph traversal → BFS (shortest) · DFS (paths/cycles) · Topo sort (dependencies)
    ├── Optimization → Greedy (local optimal) · DP (overlapping subproblems) · Divide & Conquer
    └── Design patterns → Monotonic Stack/Deque · Two Pointers · Sliding Window · Union-Find
```

---

## 02 — Dynamic Programming

```
02-algorithms/dynamic-programming/README.md
└── DP Framework
    ├── State design → what changes between subproblems?
    ├── Recurrence → dp[i] = f(dp[i-1], dp[i-2], ...)
    ├── Base case → smallest valid input
    └── Top-down (memoize) vs Bottom-up (tabulate)

02-algorithms/dynamic-programming/dp-aditya-verma.md
└── Pattern-based DP
    ├── 0-1 Knapsack → include/exclude · dp[i][w]
    ├── Unbounded Knapsack → coin change · rod cutting
    ├── Subset Sum → target reachability · dp[i][s] bool
    ├── LCS → dp[i][j] = 1 + dp[i-1][j-1] if match else max
    └── MCM (Matrix Chain) → interval DP · dp[i][j] = min cost to multiply

02-algorithms/dynamic-programming/grid-dp.md
└── Grid DP
    ├── Unique paths → dp[i][j] = dp[i-1][j] + dp[i][j-1]
    ├── Min path sum → dp[i][j] = grid[i][j] + min(up, left)
    └── Obstacles → skip blocked cells

02-algorithms/dynamic-programming/string-palindrome-dp.md
└── String/Palindrome DP
    ├── LCS → classic 2D DP O(n*m)
    ├── LIS → O(n log n) with patience sort / binary search
    ├── Edit Distance → replace/insert/delete transitions
    └── Palindrome → expand-around-center O(n²) · Manacher O(n)

02-algorithms/dynamic-programming/stock-trading-dp.md
└── Stock Trading DP [State machine]
    ├── Buy once → Kadane variant · max(price[j] - min_so_far)
    ├── Unlimited trades → sum of all positive diffs
    ├── K transactions → dp[k][i] = max profit with k trades up to day i
    └── Cooldown / fee → extend state: hold · sold · rest

02-algorithms/dynamic-programming/advanced-dp-optimizations.md
└── DP Optimizations [for Hard / CP problems]
    ├── Divide & Conquer optimization → O(n² → n log n) when opt(i) ≤ opt(i+1)
    ├── Knuth's optimization → O(n³ → n²) for quadrangle inequality DP
    └── Convex Hull Trick → O(n) amortized when transitions are linear in previous dp
```

---

## 02 — Recursion

```
02-algorithms/recursion/README.md
└── Recursion Model
    ├── Base case → simplest input, return directly
    ├── Hypothesis → assume recursion works for smaller input
    └── Induction → use smaller result to build current answer

02-algorithms/recursion/aditya-verma.md
└── IBH Method [Induction-Base-Hypothesis]
    └── Pattern: trust the recursion, build on it

02-algorithms/recursion/tree-recursion.md
└── Tree Recursion
    ├── Return value from subtree → accumulate up
    └── Path tracking → carry path as argument, undo on return

02-algorithms/recursion/recursion-to-dp.md
└── Recursion → DP Pipeline
    ├── Step 1: Write recursive solution
    ├── Step 2: Add memoization (top-down DP)
    └── Step 3: Convert to bottom-up tabulation

02-algorithms/recursion/combination-problems.md
└── Combination Recursion
    ├── Choose/skip → power set
    └── Choose k from n → prune when remaining < k needed
```

---

## 03 — Patterns

```
03-patterns/patterns-master.md
└── Pattern Recognition Master [READ FIRST — before drilling problems]
    ├── Trigger: sorted + target sum → Two Pointers
    ├── Trigger: subarray/substring + constraint → Sliding Window
    ├── Trigger: sorted search + O(log n) → Binary Search
    ├── Trigger: shortest path → BFS
    ├── Trigger: all paths / combinations → DFS / Backtrack
    ├── Trigger: optimal substructure → DP
    └── Trigger: K largest/smallest → Heap

03-patterns/interview-cheatsheet.md
└── One-page interview cheatsheet [Read on interview day — 10 min max]
    └── All patterns + complexity + Python snippet

03-patterns/GOOGLE_QUICK_SHEET.md
└── Google-specific [What they reward / red flags]
    ├── Reward: clean code · optimal complexity · edge cases stated upfront
    └── Red flag: brute force without improvement · silent coding · no test cases

03-patterns/GOOGLE_INTERVIEW_REVISION.md
└── Deep revision guide [topic-by-topic Google lens]
    └── Use in Week 4 and 48-hr sprint

03-patterns/TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md
└── 100+ canonical problems [logic + trickiness per problem]
    └── Use to identify why a problem is tricky, not just what the solution is

03-patterns/canonical-questions.md
└── Canonical Questions — Key Insight Index [one-line insight per problem]
    ├── Arrays: Two Sum → check-before-store · Kadane → reset when prefix negative · Trapping Rain → min(left_max,right_max)-h[i]
    ├── Strings: Min Window → two counters (need/have) · Longest Palindrome → expand odd+even at each index
    ├── Trees: LCA any tree → return node when found; LCA = where both sides non-null
    ├── Graphs: Word Ladder → BFS on graph where edge = 1-char difference
    ├── DP: Coin Change → unbounded knapsack · Burst Balloons → last balloon in interval = dp[i][j]
    └── Use: check if you know the key insight cold before opening solution

03-patterns/leetcode-variants.md
└── LC variants by pattern [grouped for drilling]
    └── Use after reading patterns-master — drill 2-3 variants per pattern

03-patterns/system-design.md
└── System design stubs [SDE-2 scope]
    └── Use for hybrid DS+SD interview rounds
```

---

## 04 — Behavioral

```
04-behavioral/README.md
└── Google 4 Attributes
    ├── General Cognitive Ability → structured thinking · how you solve unknowns
    ├── Leadership → influence without authority · step up or step back
    ├── Role-related Knowledge → depth in your craft
    └── Googliness → honest · scrappy · team-first

04-behavioral/behavioral.md
└── STAR Story Index
    ├── Structure: Situation → Task → Action → Result (quantify)
    ├── Story types: conflict · failure · ambiguity · leadership · cross-team
    └── Rehearse: 3 stories minimum · titles + outcomes cold

04-behavioral/BEHAVIORAL_GOOGLINESS.md
└── Four Google Attributes — Deep Dive
    ├── GCA → decompose before diving · handle new info mid-conversation · justify tradeoffs
    │   └── Signal: "Before I start coding, let me think about edge cases..."
    ├── Leadership → emergent not positional · influence without authority · own the outcome
    │   └── Signal: "No one was owning X, so I set up a sync and drove it to completion..."
    ├── Role-Related Knowledge → know WHY you made decisions · failure modes not just happy paths
    │   └── Signal: "We chose eventual consistency because strong consistency added 3x latency..."
    ├── Googliness → scrappy · intellectually humble · credit others · bias for action
    │   └── Signal: "I didn't know X, so I read the source code and ran an experiment..."
    ├── Red Flags → sole hero stories · no quantified results · always "we" never "I" · badmouthing
    └── Pre-interview checklist → 7 story types ready: impact · conflict · failure · ambiguity · tech deep-dive · influence · fast learning
```

---

## 05 — Revision

```
05-revision/README.md
└── Complexity Quick-Reference
    ├── Sorting     → Merge O(n log n) stable · Quick O(n log n) avg · Heap O(n log n) O(1) space
    ├── DS          → Array O(1) access · HashMap O(1) avg · BST O(log n) avg · Heap O(log n) push
    ├── Graphs      → BFS/DFS O(V+E) · Dijkstra O((V+E)logV) · Floyd O(V³) · Union-Find O(α·n)
    └── Techniques  → Binary Search O(log n) · DP O(states×transition) · Backtrack O(2^n or n!)
    
└── Python Gotchas
    ├── -7 // 2 == -4 (floors toward -∞) → use -((-a)//b) for ceiling
    ├── list.pop(0) is O(n) → use deque.popleft() for queues
    ├── heapq is min-heap → negate for max-heap
    ├── dict.get(k, 0) → no KeyError on missing key
    ├── arr[:] → shallow copy (arr = arr2 is a reference, not copy)
    └── "".join(chars) → O(n) string build (s += c is O(n²))

05-revision/coding-rubric.md
└── Google Coding Rubric
    ├── Problem understanding → restate + clarify constraints + examples
    ├── Approach → brute → optimal → justify complexity
    ├── Code quality → clean · named vars · no magic numbers
    ├── Testing → trace examples · edge cases (empty · single · overflow)
    └── Communication → narrate decisions · don't go silent
```

---

## Books

```
books/the-algorithm-design-manual.md
└── Algorithm Design Manual [Skiena]
    └── Use for: algorithm intuition · war stories · when to use which algo

books/dynamic-programming-for-coding-interviews.md
└── DP for Coding Interviews
    └── Use for: pattern-based DP drilling · before dp-aditya-verma.md

books/elements-of-programming-interviews-in-python.md
└── EPI in Python
    └── Use for: problem + solution walkthroughs · harder variants of LC problems

books/data-structures-and-algorithms-using-python.md
└── DS & Algo using Python
    └── Use for: Python-specific implementation details

books/cp3.md
└── Competitive Programming 3
    └── Use for: advanced techniques · contest-style problem patterns
```
