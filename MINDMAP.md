---
module: root
topic: Mindmap
subtopic:
status: unread
tags: [root, mindmap, l3]
---

← [L3 Roadmap](coding/l3-google-roadmap.md) · [Flowcharts](FLOWCHARTS.md) · [DS index](01-data-structures/README.md) · [Algorithms index](02-algorithms/README.md)

# Mindmap — ASCII only (`coding/`, L3 scope)

> [!note] L3 Reference Document
> Lookup index for **T1/T2 problems only** in the L3 study path. Skips `💤 T3` entries. Not a substitute for topic deep-dives.

_→ = one-line hint from each problem's Approach block_

## coding/data-structures/

### 01-array.md

```
coding/data-structures/01-array.md
└── 01-array.md
    ├── Two Pointers
    │   ├── Two Sum (sorted variant) `⚡ T1`
    │   │   → Two Pointers on sorted array.
    │   ├── 3Sum `⚡ T1`
    │   │   → Fix + Two Pointers.
    │   ├── 3Sum Closest `⚡ T1`
    │   │   → Sort + Two Pointers with closest tracking.
    │   ├── 4Sum `⚡ T1`
    │   │   → Two nested loops + Two Pointers.
    │   ├── Container with Most Water `⚡ T1`
    │   │   → Two Pointers — advance the shorter line.
    │   ├── Trapping Rain Water `⚡ T1`
    │   │   → Two Pointers — binding constraint side.
    │   ├── Remove Duplicates from Sorted Array `⚡ T1`
    │   └── Next Permutation `🎯 T2`
    │       → Three-step: find rightmost descent, swap, reverse suffix.
    ├── Sliding Window
    │   ├── Max Consecutive Ones III `⚡ T1`
    │   │   → Variable sliding window — zero count tracking.
    │   ├── Subarrays with K Different Integers `⚡ T1`
    │   │   → Exactly-k = at_most(k) − at_most(k−1).
    │   ├── Continuous Subarray Sum
    │   │   → Prefix modulo — first-occurrence index map.
    │   └── Product of Array Except Self `🎯 T2`
    │       → Two-pass left/right product accumulation.
    ├── Kadane's Algorithm
    │   ├── Maximum Subarray `🎯 T2`
    │   │   → Kadane's algorithm — local reset on negative prefix.
    │   └── Maximum Circular Subarray Sum (Maximum Sum Circular Subarray)
    │       → Kadane's max + Kadane's min on total sum.
    ├── Dutch National Flag / Partitioning
    │   ├── Sort Colors `⚡ T1`
    │   │   → Dutch National Flag — three-pointer partition.
    │   └── Find All Numbers Disappeared in an Array
    │       → Sign-flip in-place visited marking.
    ├── Boyer-Moore Voting
    │   ├── Majority Element `🎯 T2`
    │   │   → Boyer-Moore voting — cancellation argument.
    │   └── Find the Duplicate Number `🎯 T2`
    │       → Floyd's cycle detection on implicit linked list.
    ├── Difference Array
    │   ├── Difference Array Pattern
    │   ├── Car Pooling
    │   │   → Each trip is a range update — passengers board at from and alight at to.
    │   ├── Corporate Flight Bookings
    │   │   → Each booking is a range update over flight indices.
    │   └── Range Addition
    ├── Miscellaneous Array Techniques
    │   ├── Best Time to Buy and Sell Stock `🎯 T2`
    │   │   → Track the minimum price seen so far.
    │   ├── Move Zeroes `⚡ T1`
    │   │   → We need to compact non-zero elements to the front, preserving order, without allocating extra space.
    │   ├── Two Sum (hash map variant) `⚡ T1`
    │   │   → Hash map complement lookup.
    │   ├── Spiral Matrix
    │   │   → Boundary shrinking — four-direction cycling.
    │   ├── Set Matrix Zeroes
    │   │   → Use first row/col as markers — O(1) space.
    │   ├── Rotate Array
    │   │   → Triple reversal trick.
    │   ├── Range Sum Query — Immutable (LC 303) `🎯 T2`
    │   │   → Prefix sum array — O(1) per query.
    │   ├── Jump Game (LC 55) `🎯 T2`
    │   │   → Greedy — track farthest reachable index.
    │   └── Gas Station (LC 134) `🎯 T2`
    ├── Matrix / Intervals
    │   ├── Rotate Image (LC 48)
    │   │   → Transpose then reverse each row.
    │   ├── Merge Intervals (LC 56) `🎯 T2`
    │   │   → Sort by start, linear merge scan.
    │   ├── Insert Interval (LC 57) `🎯 T2`
    │   │   → Three-phase linear scan: before, overlap, after.
    │   └── Non-overlapping Intervals (LC 435) `🎯 T2`
    │       → Greedy — sort by end, keep earliest-ending non-conflicting interval.
    ├── Miscellaneous (Continued)
    │   └── First Missing Positive (LC 41)
    │       → Index-as-hash — cyclic placement of values in range [1, n].
    └── Prefix Sum
        ├── Subarray Sum Equals K (with negative numbers) `⚡ T1`
        │   → Two-pointer/sliding-window breaks with negatives.
        ├── Contiguous Array (Equal 0s and 1s) `⚡ T1`
        │   → Replace 0 with -1.
        └── Product of Array Except Self (no division)
            → Division breaks on zeros.
```

### 02-hashing.md

```
coding/data-structures/02-hashing.md
└── 02-hashing.md
    ├── Complement Map
    │   ├── Two Sum `⚡ T1`
    │   │   → Brute force checks every pair — O(n²).
    │   ├── 3Sum (hash-based) `⚡ T1`
    │   │   → Reduce to two-sum: fix element a, find pair (b, c) with b + c = -a in the remaining array.
    │   ├── 4Sum (hash-based) `⚡ T1`
    │   │   → Reduce to 3Sum by fixing one element.
    │   └── Max Number of K-Sum Pairs
    │       → Each number can only pair once — we need to greedily match available complements, consuming them.
    ├── Frequency Map
    │   ├── First Unique Character in a String
    │   │   → Need both frequency (to identify unique) and order (to find the first).
    │   ├── Ransom Note
    │   │   → This is a frequency matching problem; each character in the note must be available at least as many times as needed.
    │   ├── Top K Frequent Elements `⚡ T1`
    │   │   → Sorting by frequency is O(n log n).
    │   ├── Subdomain Visit Count
    │   │   → Each domain contributes its count to itself and all suffix domains.
    │   ├── Sort Characters by Frequency
    │   │   → Need characters ordered by count descending.
    │   ├── Longest Subarray with Sum K
    │   │   → Sliding window fails with negatives.
    │   ├── Count Number of Nice Subarrays
    │   │   → Map odd/even to 1/0.
    │   ├── Subarray Sum Equals K `⚡ T1`
    │   │   → Sliding window fails with negatives (sum can decrease when adding elements).
    │   ├── Contiguous Array (Max Equal 0/1 Subarray) `⚡ T1`
    │   │   → "Equal 0s and 1s" means the difference between 0-count and 1-count is 0 over the subarray.
    │   ├── Make the Array Sum Divisible by P
    │   │   → We want (total - subarray_sum) % P == 0, i.e., subarray_sum % P == total % P.
    │   └── Subarray Sums Divisible by K `⚡ T1`
    │       → (prefix[j] - prefix[i]) % K == 0 iff prefix[j] % K == prefix[i] % K.
    ├── Design
    │   ├── Insert Delete GetRandom O(1) `⚡ T1`
    │   │   → Hash map gives O(1) insert/delete/lookup.
    │   └── Design HashMap `⚡ T1`
    │       → Understand collision resolution.
    ├── Set Operations
    │   ├── Contains Duplicate
    │   │   → Membership check in O(1) is exactly what a hash set provides.
    │   ├── Intersection of Two Arrays
    │   │   → Set intersection directly models the problem.
    │   └── Two Sum Less Than K `⚡ T1`
    │       → We want the largest valid pair sum — greedy with two pointers after sorting is cleanest.
    ├── Miscellaneous
    │   ├── Longest Consecutive Sequence `⚡ T1`
    │   │   → Sorting is O(n log n).
    │   ├── Substring with Concatenation of All Words
    │   │   → Words are fixed length.
    │   └── Max Points on a Line
    │       → For each pair of points, their line is defined by slope.
    └── Rolling Hash / Dedup
        ├── Longest Duplicate Substring (Rabin-Karp) `⚡ T1`
        │   → Binary search on length L: if a duplicate of length L exists, so does one of length L-1.
        ├── Find Duplicate File in System
        │   → Files with the same content are duplicates.
        └── 4Sum II `⚡ T1`
            → Brute force O(n⁴).
```

### 03-string.md

```
coding/data-structures/03-string.md
└── 03-string.md
    ├── Frequency Map / Anagram
    │   ├── Valid Anagram `🎯 T2`
    │   │   → Two strings are anagrams iff they are identical after sorting.
    │   ├── Group Anagrams `⚡ T1`
    │   │   → All anagrams share the same canonical form — their sorted version.
    │   └── Find All Anagrams in a String `⚡ T1`
    │       → We need a fixed-size sliding window of length len(p).
    ├── Two Pointers — Palindrome
    │   ├── Valid Palindrome `🎯 T2`
    │   │   → After filtering to alphanumeric + lowercase, a palindrome reads the same forwards and backwards.
    │   ├── Longest Palindromic Substring `🎯 T2`
    │   │   → A palindrome is symmetric around its center.
    │   └── Palindromic Substrings (Count All Palindromic Substrings)
    │       → Same expand-around-center logic as Longest Palindromic Substring, but instead of tracking the longest, count every expansion that succeeds.
    ├── Sliding Window
    │   ├── Longest Substring Without Repeating Characters `⚡ T1`
    │   │   → A valid window has all unique characters.
    │   ├── Minimum Window Substring `⚡ T1`
    │   │   → We need the smallest window satisfying all character demands from t.
    │   └── Longest Repeating Character Replacement `⚡ T1`
    │       → A window is valid iff window_length - max_frequency_in_window <= k.
    ├── Prefix Sum on Characters
    │   ├── Prefix Sum on Characters Pattern
    │   ├── Number of Substrings Containing All Three Characters
    │   │   → For any right endpoint r, the valid left endpoints form a contiguous suffix — as soon as all three chars appear, every further-left start also works.
    │   ├── Count Vowel Substrings of a Word
    │   │   → Direct sliding window with "exactly 5 distinct vowels" is non-monotone.
    │   ├── Binary Subarrays With Sum
    │   │   → Binary array can have negative-like complications if solved with sliding window (zero elements don't shrink the sum).
    │   └── Subarray Sum Equals K (character version) `⚡ T1`
    │       → Map target character to 1, all others to 0 — identical to the numeric subarray sum equals k problem.
    ├── Encoding / Hashing
    │   ├── Encode and Decode Strings `🎯 T2`
    │   └── String Hashing (Duplicate Substring Detection)
    │       → Comparing every pair of substrings of length L is O(n × L) per comparison and O(n²L) total.
    ├── Parsing / Simulation
    │   ├── String to Integer (atoi)
    │   └── Longest Common Prefix
    │       → The longest common prefix is bounded by the shortest string.
    ├── Two Pointers — Reverse / Subsequence
    │   ├── Reverse String
    │   │   → Classic two-pointer swap.
    │   └── Is Subsequence
    │       → Greedy two-pointer: advance through t trying to match characters of s in order.
    ├── Parsing / Simulation (Extended)
    │   ├── Decode String
    │   │   → Nested brackets suggest a stack.
    │   ├── Compare Version Numbers
    │   │   → Split on .
    │   └── Integer to English Words
    │       → Numbers follow a recursive pattern: every 3-digit group is described the same way, then suffixed with Billion/Million/Thousand.
    ├── Pattern Matching
    │   ├── Implement strStr (KMP)
    │   │   → Naive search is O(n×m) in the worst case (e.g., haystack = "aaa…a", needle = "aaa…ab").
    │   ├── Repeated Substring Pattern
    │   │   → If s is a repetition of some pattern p, then s + s contains s starting at a position other than 0 or len(s).
    │   └── Longest Happy Prefix
    │       → This is exactly the KMP failure function / LPS (Longest Proper Prefix which is also Suffix) for the entire string.
    └── String Manipulation
        ├── String Compression
        │   → We need to write compressed output back into the same array, so one pointer reads runs and another pointer writes results.
        ├── Zigzag Conversion (LC 6)
        ├── Valid Palindrome II (LC 680) `🎯 T2`
        │   → A standard two-pointer palindrome check stops at the first mismatch.
        └── Reverse Words in a String (LC 151)
            → Python's split() without arguments handles multiple spaces and strips leading/trailing whitespace.
```

### 04-matrix.md

```
coding/data-structures/04-matrix.md
└── 04-matrix.md
    ├── Grid BFS / DFS
    │   ├── Number of Islands `⚡ T1`
    │   ├── Walls and Gates `⚡ T1`
    │   ├── Shortest Path in Binary Matrix `⚡ T1`
    │   └── Rotting Oranges `⚡ T1`
    ├── Traversal / In-Place Transformation
    │   ├── Spiral Matrix `🎯 T2`
    │   ├── Rotate Image `🎯 T2`
    │   └── Set Matrix Zeroes `🎯 T2`
    ├── Grid DP
    │   ├── Unique Paths `⚡ T1`
    │   ├── Minimum Path Sum `⚡ T1`
    │   ├── Maximal Square `🎯 T2`
    │   └── Longest Increasing Path in a Matrix `⚡ T1` (L4)
    └── Prefix Sums on Grids
        └── 2D Prefix Sum `🎯 T2`
```

### 05-stack.md

```
coding/data-structures/05-stack.md
└── 05-stack.md
    ├── Monotonic Stack — Next Greater/Smaller
    │   ├── Daily Temperatures `🎯 T2`
    │   │   → Brute force checks every future day for each index — O(n²).
    │   ├── Next Greater Element II `🎯 T2`
    │   │   → Circular array means element 0 might be the next greater for element n-1.
    │   ├── Online Stock Span
    │   │   → Naively scan backwards each day — O(n) per call, O(n²) total.
    │   └── Sum of Subarray Minimums
    │       → Enumerate all subarrays — O(n²) or O(n³).
    ├── Monotonic Stack — Histogram / Rectangle
    │   ├── Largest Rectangle in Histogram `🎯 T2`
    │   │   → For each bar as the height of the rectangle, the width extends left and right until a shorter bar is hit.
    │   ├── Maximal Rectangle `🎯 T2`
    │   │   → Reduce to Largest Rectangle in Histogram.
    │   └── Trapping Rain Water (stack approach) `⚡ T1`
    │       → Water fills valleys.
    ├── Valid Parentheses / Nesting
    │   ├── Valid Parentheses `🎯 T2`
    │   ├── Remove All Adjacent Duplicates in String
    │   │   → Removing one pair can create new adjacent duplicates — process must cascade.
    │   └── Remove K Digits `🎯 T2`
    │       → Greedy — to minimize, remove a digit when the next digit is smaller (it would be more beneficial at that position).
    ├── Stack Design
    │   ├── Min Stack `🎯 T2`
    │   │   → A regular stack loses track of the minimum after pops.
    │   └── Maximum Frequency Stack
    │       → Standard stack gives LIFO; we want frequency-priority with LIFO for ties.
    ├── Queue from Stacks
    │   ├── Implement Queue using Stacks
    │   │   → Stack is LIFO; reversing the stack gives FIFO order.
    │   └── Validate Stack Sequences
    │       → Simulate the push sequence and greedily pop when the top matches the next expected pop.
    ├── Expression Evaluation
    │   ├── Evaluate Reverse Polish Notation `🎯 T2`
    │   │   → RPN eliminates parentheses — operators apply to the two most recently seen operands.
    │   ├── Basic Calculator I
    │   │   → Parentheses introduce nested scope.
    │   ├── Basic Calculator II
    │   │   → * and / have higher precedence than + and -.
    │   └── Basic Calculator III
    │       → Combination of I (parentheses) and II (precedence).
    ├── Simulation / Other
    │   ├── Exclusive Time of Functions
    │   ├── Simplify Path
    │   ├── Baseball Game
    │   └── Asteroid Collision `🎯 T2`
    │       → Collisions only happen between a positive (right-moving) on the stack and a new negative (left-moving).
    ├── Parentheses — Score and Repair
    │   ├── Score of Parentheses (LC 856)
    │   │   → Depth determines the multiplier — each level of nesting doubles the score of inner ().
    │   ├── Minimum Add to Make Parentheses Valid (LC 921)
    │   │   → An unmatched ) cannot be fixed by future characters — it needs an immediate ( inserted to its left.
    │   └── Check if Word is Valid After Substitutions (LC 1003)
    │       → Every c must be preceded by ab immediately below it — a nesting structure.
    ├── Monotonic Stack — Arrays and Sequences
    │   ├── Car Fleet (LC 853) `🎯 T2`
    │   │   → Cars closer to the target are ahead.
    │   ├── Maximum Width Ramp (LC 962)
    │   │   → We want the leftmost possible i and rightmost possible j.
    │   ├── Number of Visible People in a Queue (LC 1944)
    │   │   → A taller person blocks all shorter ones behind them.
    │   ├── Flatten Binary Tree to Linked List (LC 114 — iterative) `🎯 T2`
    │   │   → Recursive flatten risks call-stack overflow on skewed trees.
    │   └── Path Sum II (LC 113 — iterative DFS) `🎯 T2`
    │       → Recursive DFS is natural but risks stack overflow.
    ├── See Also
    │   └── Next Greater Element I `🎯 T2`
    │       → We need the next greater element for many values, so we preprocess nums2 with a monotonic stack to avoid repeated scans.
    └── Monotonic Stack — Advanced
        ├── 132 Pattern (LC 456)
        │   → Brute force is O(n³).
        └── Buildings With an Ocean View (LC 1762)
```

### 06-queue.md

```
coding/data-structures/06-queue.md
└── 06-queue.md
    ├── Monotonic Deque
    │   ├── Sliding Window Maximum `⚡ T1`
    │   │   → Naive O(nk) rescans the window on every step; we need O(n).
    │   ├── Sliding Window Minimum
    │   │   → Same argument — need O(n), not O(nk).
    │   ├── Shortest Subarray with Sum at Least K
    │   │   → Negative values break the simple two-pointer sliding window — shrinking from the left doesn't always decrease the sum.
    │   ├── Jump Game VI (DP + Sliding Window Max) `🎯 T2`
    │   │   → Naive DP dp[i] = nums[i] + max(dp[i-k..i-1]) is O(nk) — the inner max over a window of size k is expensive.
    │   └── Maximum of Minimums of Every Window Size
    │       → Brute force is O(n³).
    ├── BFS / Level-order
    │   ├── Binary Tree Level Order Traversal `🎯 T2`
    │   │   → DFS mixes levels; BFS processes nodes level-by-level naturally.
    │   └── Binary Tree Right Side View `🎯 T2`
    │       → The rightmost node at each level is exactly the last node dequeued in a level-order BFS.
    ├── BFS Multi-Source
    │   ├── 01 Matrix `⚡ T1`
    │   │   → Running BFS from each 1 independently is O((m×n)²) — too slow.
    │   ├── Walls and Gates `⚡ T1`
    │   ├── Farthest Building from Land (As Far from Land as Possible)
    │   │   → The cell farthest from all land is the last cell reached when BFS expands outward from all land cells simultaneously.
    │   ├── Shortest Path in Binary Matrix `⚡ T1`
    │   │   → All edges have equal weight (each step costs 1), so BFS gives the shortest path.
    │   └── Minimum Knight Moves `⚡ T1`
    ├── BFS Single-Source
    │   ├── Open the Lock `⚡ T1`
    │   │   → Each lock state is a node; each valid turn is an edge with weight 1.
    │   ├── Bus Routes
    │   │   → BFS over stops would revisit stops on the same route repeatedly.
    │   ├── Shortest Path in Grid with Obstacles Elimination
    │   │   → Standard BFS doesn't capture how many eliminations have been used — two paths to the same cell may have different remaining k.
    │   ├── Cheapest Flights Within K Stops
    │   └── Jump Game III `🎯 T2`
    │       → We need to determine reachability — BFS from start explores all reachable indices.
    ├── Topological Sort (Kahn's BFS)
    │   ├── Course Schedule `⚡ T1`
    │   │   → The prerequisites form a directed graph; a cycle makes it impossible to finish all courses.
    │   └── Alien Dictionary `⚡ T1`
    ├── Design
    │   ├── Design Hit Counter
    │   ├── Design Circular Queue
    │   │   → A plain list wastes space as the front pointer drifts forward.
    │   ├── Moving Average from Data Stream
    │   ├── Number of Recent Calls
    │   │   → Old timestamps outside the window are never useful again.
    │   └── Implement Stack Using Queues
    │       → A queue is FIFO; to make the most recently pushed element accessible first, we must rotate older elements behind the new one after each push.
    ├── Priority Queue / Heap
    │   ├── Task Scheduler `⚡ T1`
    │   │   → We always want to execute the most frequent remaining task next (greedy).
    │   └── Find Median from Data Stream `⚡ T1`
    │       → Sorting on every query is O(n log n).
    ├── See Also
    │   └── Design Circular Deque
    │       → A circular buffer lets us use O(1) index arithmetic without shifting elements.
    └── Sliding Window with Queue
        └── Sliding Window Median (LC 480) `⚡ T1`
            → Recalculating the median from scratch for each window is O(k log k) per step — too slow.
```

### 07-linked-list.md

```
coding/data-structures/07-linked-list.md
└── 07-linked-list.md
    ├── In-Place Reversal
    │   ├── Reverse Linked List `🎯 T2`
    │   │   → Three-pointer iterative reversal.
    │   ├── Reverse Linked List II `🎯 T2`
    │   │   → Find pre-node + in-place splice-reversal.
    │   ├── Palindrome Linked List `🎯 T2`
    │   │   → Find middle + reverse second half + compare.
    │   ├── Reorder List `🎯 T2`
    │   │   → Find middle + reverse second half + interleave.
    │   └── Reverse Nodes in K-Group `🎯 T2`
    │       → Count-verify + in-place reversal per group.
    ├── Fast / Slow Pointers
    │   ├── Linked List Cycle `🎯 T2`
    │   │   → Floyd's fast/slow pointer cycle detection.
    │   ├── Middle of the Linked List
    │   │   → Fast/slow one-pass middle finder.
    │   ├── Remove Nth Node From End of List `🎯 T2`
    │   │   → Two pointers with N+1 gap.
    │   ├── Delete the Middle Node of a Linked List
    │   │   → Slow/fast with prev pointer — land before middle.
    │   └── Happy Number
    │       → Floyd's cycle detection on the implicit sequence.
    ├── Floyd's Cycle Detection
    │   ├── Linked List Cycle II `🎯 T2`
    │   │   → Floyd's two-phase cycle entry detection.
    │   └── Find the Duplicate Number (Floyd's variant) `🎯 T2`
    │       → Floyd's on implicit linked list defined by array values.
    ├── Merge / Sorting
    │   ├── Merge Two Sorted Lists `🎯 T2`
    │   │   → Dummy head + two-pointer merge.
    │   ├── Sort List `🎯 T2`
    │   │   → Bottom-up merge sort on linked list.
    │   └── Insertion Sort List
    │       → Dummy head + find-insertion-point per node.
    ├── Copy / Design
    │   ├── Copy List with Random Pointer `🎯 T2`
    │   │   → Hash map original→clone, two-pass wiring.
    │   └── LRU Cache `🎯 T2`
    │       → Doubly linked list + hash map.
    └── Other Manipulation
        ├── Add Two Numbers
        │   → Digit-by-digit addition with carry.
        ├── Swap Nodes in Pairs
        │   → Dummy head + iterative pair swapping.
        ├── Intersection of Two Linked Lists
        ├── Rotate List (Circular List Trick)
        │   → Make circular, find new tail, break circle.
        ├── Remove Duplicates from Sorted List
        │   → Single pass: skip consecutive equal nodes.
        ├── Remove Duplicates from Sorted List II
        │   → Dummy head + prev pointer skipping duplicate runs.
        ├── Partition List
        │   → Two dummy heads — collect two sublists, then join.
        └── Flatten a Multilevel Doubly Linked List
```

### 08-tree.md

```
coding/data-structures/08-tree.md
└── 08-tree.md
    ├── DFS Traversal
    │   ├── Binary Tree Inorder Traversal `🎯 T2`
    │   │   → Recursive inorder is trivial; the iterative version uses an explicit stack to simulate the call stack.
    │   ├── Invert Binary Tree `🎯 T2`
    │   │   → Post-order recursive swap.
    │   ├── Symmetric Tree `🎯 T2`
    │   │   → Recursive mirror(l, r) — outer and inner pair matching.
    │   ├── Maximum Depth of Binary Tree `🎯 T2`
    │   │   → Post-order recursive max height.
    │   ├── Minimum Depth of Binary Tree
    │   │   → Critical trap: a node with only one child is NOT a leaf.
    │   ├── Path Sum `🎯 T2`
    │   │   → DFS subtracting current value — check at leaf.
    │   ├── Path Sum II `🎯 T2`
    │   │   → Collecting all paths requires backtracking — extend the path on entry, collect at leaves, pop on exit.
    │   ├── Sum Root to Leaf Numbers
    │   │   → As we descend, the current number is parent_number * 10 + node.val.
    │   ├── Count Complete Tree Nodes
    │   │   → A naive O(n) traversal ignores the complete tree property.
    │   ├── Count Good Nodes in Binary Tree `🎯 T2`
    │   │   → DFS with propagated path_max.
    │   ├── Same Tree
    │   │   → Two trees are the same iff their roots match and both subtrees are recursively the same.
    │   ├── Subtree of Another Tree
    │   │   → For each node in root, check if the subtree rooted there matches subRoot.
    │   ├── Flatten Binary Tree to Linked List `🎯 T2`
    │   │   → Morris-style in-place threading — find inorder predecessor.
    │   └── Step-By-Step Directions From a Binary Tree Node to Another
    │       → DFS to root→start and root→dest paths, strip common prefix.
    ├── Level Order BFS
    │   ├── Binary Tree Zigzag Level Order Traversal `🎯 T2`
    │   │   → Same as level-order BFS but every other level needs reversal.
    │   ├── Populating Next Right Pointers in Each Node `🎯 T2`
    │   │   → O(1) space — walk current level to connect next level.
    │   ├── Vertical Order Traversal of a Binary Tree `🎯 T2`
    │   └── All Nodes Distance K in Binary Tree `🎯 T2`
    │       → Build undirected graph, BFS k steps from target.
    ├── Lowest Common Ancestor
    │   ├── Lowest Common Ancestor of a Binary Tree `🎯 T2`
    │   │   → Post-order recursion — converge at split node.
    │   └── Lowest Common Ancestor of a BST `🎯 T2`
    │       → Iterative BST-guided descent — O(h) instead of O(n).
    ├── Tree DP
    │   ├── Diameter of Binary Tree `🎯 T2`
    │   │   → Post-order height DFS with global diameter update.
    │   ├── Binary Tree Maximum Path Sum `🎯 T2`
    │   │   → Post-order gain DFS — clamp negatives to 0.
    │   ├── House Robber III `🎯 T2`
    │   │   → Post-order DP returning (rob, skip) pair.
    │   ├── Binary Tree Cameras `🎯 T2`
    │   │   → Greedy post-order — delay cameras upward.
    │   └── Path Sum III `🎯 T2`
    │       → DFS with prefix sum hash map + backtracking.
    ├── BST Operations
    │   ├── Validate Binary Search Tree `🎯 T2`
    │   │   → Recursive range validation — propagate (lo, hi) bounds.
    │   ├── Kth Smallest Element in a BST `🎯 T2`
    │   │   → Iterative inorder with early exit at k.
    │   ├── Insert and Delete in BST
    │   │   → Insert follows BST search path to find the null slot.
    │   ├── Range Sum of BST
    │   │   → DFS with BST pruning — skip entire subtrees.
    │   └── Recover Binary Search Tree
    │       → Inorder DFS — detect inversion pair(s), swap values.
    ├── Construction / Serialization
    │   ├── Serialize and Deserialize Binary Tree `🎯 T2`
    │   │   → Preorder DFS with null markers — iterator-based deserialization.
    │   ├── Construct Binary Tree from Preorder and Inorder Traversal `🎯 T2`
    │   │   → Preorder index advance + inorder hash map for O(1) root lookup.
    │   └── Construct Binary Tree from Inorder and Postorder Traversal
    │       → Postorder's last element is always the root.
    ├── Morris Traversal / Iterative Postorder
    │   ├── Morris Inorder Traversal (Technique)
    │   ├── Morris Preorder Traversal (Technique)
    │   └── Iterative Postorder Traversal (Technique)
    └── See Also
        └── Binary Tree Boundary Traversal
            → The boundary is not a standard traversal; it is a combination of three ordered pieces with non-overlapping responsibilities.
```

### 09-trie.md

```
coding/data-structures/09-trie.md
└── 09-trie.md
    ├── Core Trie Implementation
    │   └── Implement Trie (Prefix Tree) `⚡ T1`
    │       → A hash set gives O(L) exact match but cannot answer "does any word start with prefix X?" without scanning all keys — O(N × L).
    ├── Autocomplete / Prefix Search
    │   ├── Design Search Autocomplete System `⚡ T1`
    │   ├── Map Sum Pairs
    │   │   → A trie propagates prefix sums naturally — each node on the insertion path of a key can accumulate that key's value.
    │   ├── Longest Word in Dictionary
    │   │   → "Each prefix must also be in the dictionary" maps exactly to "each ancestor in the trie must have is_end = True".
    │   └── Replace Words `⚡ T1`
    │       → For each word in the sentence, we need to find the shortest dictionary root that is a prefix of that word.
    ├── Trie + Backtracking
    │   ├── Word Search II `⚡ T1`
    │   │   → Searching the board independently for each word is O(W × M × 4 × 3^(L-1)) where W = words, M = board cells, L = max word length.
    │   └── Word Squares
    ├── XOR Trie
    │   └── Maximum XOR of Two Numbers in an Array `⚡ T1`
    │       → Brute force is O(n²).
    ├── Miscellaneous
    │   ├── Number of Distinct Substrings in a String
    │   │   → KMP handles one pattern in O(n+m).
    │   └── Multi String Search (AlgoExpert / similar)
    │       → Naive approach: for each small string, run Python's in operator — O(b × s × len(small)) total.
    ├── Core Trie Operations (Extended)
    │   └── Add and Search Word `⚡ T1`
    │       → Exact-match trie search is O(L).
    ├── Prefix Problems
    │   ├── Search Suggestions System `⚡ T1`
    │   │   → After inserting and sorting, a trie lets us walk to the prefix node once and collect the first 3 words in lexicographic order via a bounded DFS — O(prefix_length + output) per query.
    │   ├── Prefix and Suffix Search
    │   │   → Checking all words for every query is O(N × L).
    │   ├── Count Words With Given Prefix
    │   │   → A trie answers prefix-count queries in O(L) after O(N × L) build — count of words in the subtree rooted at the prefix node.
    │   └── Implement Magic Dictionary
    │       → We need "exactly one substitution" match, not exact or prefix match.
    ├── XOR Trie (Extended)
    │   ├── Maximum XOR With an Element From Array
    │   │   → If we could insert all nums freely, a standard XOR trie answers each query in O(32).
    │   └── Count Pairs With XOR in a Range
    │       → Brute force O(n²).
    ├── Bitwise Trie / Other
    │   ├── Design File System
    │   ├── Stream of Characters
    │   │   → Checking all words against the current stream suffix by suffix is O(W × L) per query.
    │   └── Palindrome Pairs `⚡ T1`
    │       → Brute force O(N² × L).
    └── Suffix Trie / Advanced
        ├── Implement Trie II (Count Operations) `⚡ T1`
        │   → The basic trie only tracks is_end (bool).
        ├── Shortest Unique Prefix for Every Word
        │   → "Unique prefix" means the trie node at the end of the prefix has pass_count == 1 — only one word passes through it.
        └── Maximum XOR of Two Numbers — Prefix Hash Approach `⚡ T1`
            → Demonstrates the equivalence of "XOR trie greedy" and "prefix hash greedy" for this problem.
```

### 10-heap.md

```
coding/data-structures/10-heap.md
└── 10-heap.md
    ├── Top-K Pattern
    │   ├── Kth Largest Element in a Stream `⚡ T1`
    │   │   → We need the kth largest at all times without sorting after every insert.
    │   ├── Last Stone Weight `⚡ T1`
    │   │   → We always need the two current maximums — repeated maximum extraction is a max-heap problem.
    │   ├── K Closest Points to Origin `⚡ T1`
    │   │   → Want the k smallest by distance without fully sorting n points.
    │   ├── Furthest Building You Can Reach `⚡ T1`
    │   │   → We want to save ladders for the largest jumps but can't see the future — greedy with reconsideration.
    │   ├── Kth Largest Element in an Array `⚡ T1`
    │   │   → Sorting is O(n log n) but we only need one order-statistic.
    │   └── Top K Frequent Words `⚡ T1`
    │       → We need two ordering rules: higher frequency first, then lexicographically smaller word first on ties.
    ├── Scheduling / Reorganization
    │   ├── Sliding Window Median `⚡ T1`
    │   │   → Naively recomputing the median per window is O(nk).
    │   └── IPO (Maximize Capital) `⚡ T1`
    │       → Greedy — always take the most profitable project currently affordable.
    ├── K-Way Merge
    │   ├── Merge K Sorted Lists `⚡ T1`
    │   ├── Find K Pairs with Smallest Sums `⚡ T1`
    │   │   → There are m*n possible pairs — we need the k smallest without enumerating all.
    │   ├── Kth Smallest Element in a Sorted Matrix `⚡ T1`
    │   │   → Each row is a sorted list — this is K-way merge of n sorted arrays.
    │   ├── Smallest Range Covering Elements from K Lists (Heap Variant) `⚡ T1`
    │   │   → We need a window containing one element per list.
    │   ├── K-th Smallest in M Sorted Arrays `⚡ T1`
    │   │   → This is the general form of "Kth Smallest in a Sorted Matrix" — M sorted sequences, find the k-th minimum globally.
    │   └── Maximum CPU Load `⚡ T1`
    │       → Classic interval overlap problem — need to track which jobs are active at each moment.
    ├── Dijkstra / Design / Ordered Generation
    │   ├── Path with Minimum Effort `⚡ T1`
    │   │   → Minimizing the maximum edge weight along a path — modified Dijkstra where "dist" is the bottleneck edge.
    │   ├── Design Twitter `⚡ T1`
    │   │   → News feed merges multiple sorted tweet streams (one per followee) — this is K-way merge on recency.
    │   └── Ugly Number II `⚡ T1`
    │       → We need to generate ugly numbers in order without iterating all integers.
    └── Heap Applications
        ├── Reorganize String (LC 767) `⚡ T1`
        │   → Greedy: always place the most frequent remaining character, as long as it is not the same as the last placed character.
        └── Minimum Refueling Stops (LC 871) `⚡ T1`
```

### 13-graph.md

```
coding/data-structures/13-graph.md
└── 13-graph.md
    ├── BFS on Graphs
    │   ├── Rotting Oranges `⚡ T1`
    │   │   → Multi-source BFS — simultaneous spread from all rotten sources.
    │   ├── Number of Islands (BFS) `⚡ T1`
    │   │   → Each island is a connected component.
    │   ├── Walls and Gates (LC 286) `⚡ T1`
    │   ├── 01 Matrix (LC 542) `⚡ T1`
    │   │   → Multi-source BFS from all 0-cells simultaneously propagates shortest distances outward in O(M×N).
    │   ├── Word Ladder `⚡ T1`
    │   │   → BFS on implicit word graph — L×26 mutation enumeration.
    │   ├── Employee Importance
    │   │   → Hash map + BFS over subordinate ids.
    │   ├── Find if Path Exists in a Graph `⚡ T1`
    │   │   → Union-Find — reachability in O(E α(N)).
    │   └── Find Center of Star Graph
    │       → O(1) — center appears in both the first and second edges.
    ├── DFS on Graphs
    │   ├── Number of Islands `⚡ T1`
    │   │   → DFS sinking — flood-fill each component, count triggers.
    │   ├── Flood Fill `⚡ T1`
    │   │   → DFS recolor — guard against same-color infinite loop.
    │   ├── Max Area of Island `⚡ T1`
    │   │   → DFS returning component size — sink inline.
    │   ├── Surrounded Regions `⚡ T1`
    │   │   → Reverse DFS — mark border-safe 'O's, then flip interior.
    │   ├── Pacific Atlantic Water Flow `⚡ T1`
    │   ├── All Paths From Source to Target `⚡ T1`
    │   │   → DFS backtracking on DAG — no visited set needed.
    │   ├── Number of Provinces (LC 547) `⚡ T1`
    │   │   → Each province is a connected component of an undirected graph.
    │   ├── Number of Enclaves (LC 1020) `⚡ T1`
    │   │   → Any land cell connected to the border can reach the sea — it is NOT an enclave.
    │   ├── Clone Graph `⚡ T1`
    │   └── Find Eventual Safe States `⚡ T1`
    │       → Three-color DFS — 0=unvisited, 1=in-progress, 2=safe.
    ├── Topological Sort
    │   ├── Course Schedule II `⚡ T1`
    │   │   → Kahn's topo sort — collect removal order.
    │   └── Minimum Number of Vertices to Reach All Nodes `⚡ T1`
    │       → Nodes with in-degree 0 — the only possible starting set.
    ├── Shortest Path / Weighted
    │   ├── Network Delay Time (Dijkstra's)
    │   │   → Dijkstra's — min-heap SSSP with stale-entry skip.
    │   ├── Swim in Rising Water `⚡ T1`
    │   │   → Modified Dijkstra — minimize maximum edge weight (bottleneck path).
    │   ├── Path with Minimum Effort (LC 1631) `⚡ T1`
    │   │   → Minimize the maximum edge weight on a path = bottleneck shortest path.
    │   └── Shortest Path in a DAG
    │       → In a DAG, a topological order guarantees that when a node is processed, all incoming dependencies are already finalized.
    ├── Bipartite / Coloring
    │   ├── Is Graph Bipartite? `⚡ T1`
    │   │   → BFS 2-coloring — alternating colors, fail on same-color neighbor.
    │   └── Possible Bipartition (LC 886)
    │       → Equivalent to bipartite checking on an undirected graph where edges represent dislikes.
    ├── Advanced
    │   ├── Redundant Connection `⚡ T1`
    │   │   → Union-Find — first edge connecting already-connected nodes is redundant.
    │   ├── Minimum Spanning Tree (Kruskal's)
    │   │   → Kruskal's — sort edges by weight, greedily add if no cycle.
    │   ├── Longest Path in a DAG `⚡ T1`
    │   │   → Kahn's topo sort + DP — relax dp[v] = max(dp[u] + 1).
    │   ├── Reconstruct Itinerary (LC 332)
    │   └── Minimum Height Trees (LC 310)
    │       → The roots of minimum height trees are the "center" nodes of the tree — at most 2 nodes lying on the longest path (diameter).
    └── Advanced Graph Algorithms
        ├── Minimum Spanning Tree — Prim's Algorithm
        │   → Prim's grows the MST greedily from any starting node, always adding the cheapest edge that connects the current MST to an unvisited node.
        └── All-Pairs Shortest Path — Floyd-Warshall
            → Dijkstra's is per-source (O(V * E log V) total for all-pairs).
```

### 14-design.md

```
coding/data-structures/14-design.md
└── 14-design.md
    ├── Sliding-Window State
    │   └── Design Hit Counter `⚡ T1`
    │       → Deque of timestamps; pop expired (<= t - 300) from the left — each hit enters and leaves once, amortized O(1).
    ├── Composed Data Structures
    │   ├── Insert Delete GetRandom O(1) `⚡ T1`
    │   │   → Array + map val→index; remove = swap with last, pop — order is destroyed, but nothing required order.
    │   └── LFU Cache `⚡ T1`
    │       → key→(val, freq) + freq→LRU bucket + min_freq; it's LRU plus one more dimension — derive it from LRU, don't recall it.
    ├── Randomness / Versioning
    │   ├── Random Pick with Weight `⚡ T1`
    │   │   → Prefix sums + binary search: each index owns a segment of the number line proportional to its weight.
    │   ├── Snapshot Array `🎯 T2`
    │   │   → Copying per snapshot is the trap; per-index history [(snap_id, val)] + bisect on read.
    │   └── Stock Price Fluctuation `🎯 T2`
    │       → Map timestamp→price is the truth; heaps for max/min with lazy deletion — pop while the heap top disagrees with the map.
    └── Iterators
        └── Peeking Iterator / Flatten Nested List Iterator `🎯 T2`
            → Peek = cache one element ahead; nested = stack holding reversed contents, flatten lazily on hasNext.
```


## coding/algorithms/

### 03-two-pointers.md

```
coding/algorithms/03-two-pointers.md
└── 03-two-pointers.md
    ├── Opposite Ends (Sorted Array)
    │   ├── Two Sum II — Input Array is Sorted (LC 167) `⚡ T1`
    │   │   → Array is sorted — sum is monotonically controlled by which endpoints we choose.
    │   ├── 3Sum (LC 15) `⚡ T1`
    │   │   → O(n³) brute force is too slow.
    │   ├── 4Sum (LC 18) `⚡ T1`
    │   │   → Fix two anchors, run two-pointer for the remaining pair.
    │   ├── Container With Most Water (LC 11) `⚡ T1`
    │   │   → Volume = min(height[lo], height[hi]) * (hi - lo).
    │   └── Trapping Rain Water (LC 42) `⚡ T1`
    │       → Water at position i = min(max_left, max_right) - height[i].
    ├── Same Direction (Fast/Slow)
    │   ├── Remove Duplicates from Sorted Array (LC 26) `⚡ T1`
    │   ├── Remove Element (LC 27)
    │   ├── Move Zeroes (LC 283) `⚡ T1`
    │   │   → Two-step: compact non-zeros forward (remove-element pattern), then fill tail with zeros.
    │   └── Squares of a Sorted Array (LC 977)
    │       → Squares of negatives can be large.
    ├── Partition / Dutch National Flag
    │   └── Sort Colors (LC 75) `⚡ T1`
    │       → Standard sort is O(n log n).
    ├── Linked List Two Pointers
    │   ├── Linked List Cycle (LC 141) `🎯 T2`
    │   │   → No random access → can't track visited nodes without O(n) space.
    │   ├── Find Duplicate Number — Floyd's (LC 287)
    │   │   → Treat the array as a function f(i) = nums[i] — following indices creates a linked list with a cycle (since one value appears twice, two indices map to the same "next").
    │   ├── Middle of the Linked List (LC 876)
    │   │   → Length unknown without full traversal.
    │   └── Remove Nth Node From End of List (LC 19) `🎯 T2`
    │       → To reach the nth-from-end, the fast pointer must be exactly n steps ahead of slow.
    ├── 3Sum Family (Anchor + Two Pointers)
    │   └── 3Sum Closest (LC 16) `⚡ T1`
    │       → Same scaffold as 3Sum — fix anchor, converging two-pointer on remainder.
    ├── Partition / Sort-Based
    │   ├── Partition Array According to Given Pivot (LC 2161)
    │   │   → Relative order must be preserved, so an in-place swap (DNF-style) would break ordering.
    │   └── Minimum Difference Between Highest and Lowest of K Scores (LC 1984)
    │       → After sorting, the k elements with minimum spread must be contiguous (any non-contiguous selection can be improved by replacing the outlier with a neighbor).
    ├── Sorted Array / Two-Pointer Greedy
    │   ├── Number of Subsequences That Satisfy the Given Sum Condition (LC 1498)
    │   │   → After sorting, for a fixed minimum at index lo, find the furthest hi where nums[lo] + nums[hi] <= target.
    │   ├── Max Number of K-Sum Pairs (LC 1679)
    │   │   → Each operation removes a pair summing to k.
    │   └── Bag of Tokens (LC 948)
    │       → To maximize points, spend power on the cheapest token (face-up) and spend points on the most expensive token to regain power (face-down).
    ├── Two-Pointer on Strings
    │   ├── Reverse String (LC 344)
    │   │   → Swapping from both ends converges in n/2 steps — the simplest two-pointer pattern.
    │   └── Long Pressed Name (LC 925)
    │       → Both strings share a subsequence structure — name characters must appear in typed in order, with possible repetitions in typed.
    ├── See Also
    │   └── Reverse Vowels of a String
    │       → The vowels to swap form a sparse subset, so moving two pointers inward and skipping non-vowels is optimal.
    └── Two Pointers — More Problems
        ├── Minimum Operations to Reduce X to Zero (LC 1658) `⚡ T1`
        │   → Removing from both ends to sum to x is equivalent to finding the longest subarray in the middle with sum = total - x.
        └── Boats to Save People (LC 881)
            → Greedy: pair the heaviest person with the lightest person if their combined weight fits.
```

### 04-sliding-window.md

```
coding/algorithms/04-sliding-window.md
└── 04-sliding-window.md
    ├── Fixed-Size Window
    │   ├── Find All Anagrams in a String (LC 438) `⚡ T1`
    │   │   → An anagram is a permutation — same character frequencies, different order.
    │   ├── Maximum Average Subarray I (LC 643)
    │   │   → Maximizing average is equivalent to maximizing sum (k is fixed).
    │   └── Permutation in String (LC 567) `⚡ T1`
    │       → A permutation has the same character frequencies.
    ├── Variable Window — At Most K
    │   ├── Longest Substring Without Repeating Characters (LC 3) `⚡ T1`
    │   │   → At most 0 duplicate characters per window.
    │   ├── Longest Repeating Character Replacement (LC 424) `⚡ T1`
    │   │   → In a window of length L, we need L - max_count <= k (replace all non-max-frequency characters).
    │   ├── Fruits Into Baskets (At Most 2 Distinct) (LC 904) `⚡ T1`
    │   │   → Longest subarray with at most 2 distinct values.
    │   └── Longest Substring with At Most K Distinct Characters (LC 340)
    │       → General form of the "at most K distinct" pattern.
    ├── Variable Window — Exactly K
    │   ├── Subarrays with K Different Integers (LC 992) `⚡ T1`
    │   │   → The "exactly k" constraint is not monotone for a window — adding elements can go over or under.
    │   └── Count Number of Nice Subarrays (LC 1248)
    │       → Remap: odd → 1, even → 0.
    ├── Variable Window — Minimum Length
    │   ├── Minimum Size Subarray Sum (LC 209)
    │   │   → Positive integers mean adding elements always increases sum, removing always decreases.
    │   └── Minimum Window Substring (LC 76) `⚡ T1`
    │       → Need to cover all characters of t.
    ├── Sliding Window + Monotonic Deque
    │   ├── Sliding Window Maximum (LC 239) `⚡ T1`
    │   │   → Recomputing max per window is O(nk).
    │   └── Sliding Window Minimum (LC variant)
    │       → Symmetric to sliding window maximum.
    ├── Fixed Window — Threshold & Uniqueness
    │   ├── Number of Sub-arrays of Size K and Average ≥ Threshold (LC 1343)
    │   │   → Fixed window of size k; average ≥ threshold ↔ sum ≥ k * threshold.
    │   ├── Maximum Sum of Almost Unique Subarray (LC 2841)
    │   │   → Fixed window of size k; track distinct count in the window alongside the running sum.
    │   └── Sliding Window Average from Data Stream (LC 346)
    ├── Variable Window — Max Length (Flip / Delete)
    │   ├── Max Consecutive Ones III (LC 1004) `⚡ T1`
    │   │   → Window contains at most k zeros.
    │   ├── Longest Subarray of 1s After Deleting One Element (LC 1493)
    │   │   → Deleting one element = flipping one 0 to nothing, or dropping one 1.
    │   └── Binary Subarrays with Sum (LC 930)
    │       → Exactly-k trick: binary values make at_most well-defined.
    ├── Variable Window — Minimum Length (All Characters / Distinct)
    │   ├── Minimum Window with All Characters Including Duplicates
    │   │   → This IS LC 76 — the standard minimum window already handles duplicates via missing counter.
    │   └── Smallest Subarray with Distinct Element Count K
    │       → Minimum-length window with an exact distinct count.
    ├── Sliding Window + Monotonic Deque — Variable Window
    │   ├── Longest Continuous Subarray with Absolute Diff ≤ Limit (LC 1438)
    │   │   → max(window) - min(window) <= limit.
    │   └── Jump Game VI (LC 1696) `🎯 T2`
    │       → DP recurrence: dp[i] = nums[i] + max(dp[i-k], ..., dp[i-1]).
    ├── More Variable Window Problems
    │   ├── Subarray Product Less Than K (LC 713)
    │   │   → All elements are positive → product is monotonically non-decreasing as window expands.
    │   ├── Longest Subarray with Sum ≤ K (Nonnegative)
    │   │   → Non-negative elements ensure monotone sum — expanding can only increase sum, so shrink-when-violated is valid.
    │   ├── Diet Plan Performance (LC 1176)
    │   └── Count Vowel Substrings of a Word (LC 2062)
    ├── See Also
    │   └── Maximum Number of Vowels in a Substring of Given Length
    │       → The window size is fixed, so every move only removes one character and adds one character.
    └── Sliding Window — More Problems
        ├── Grumpy Bookstore Owner (LC 1052) `⚡ T1`
        │   → Customers at non-grumpy minutes are always satisfied.
        └── Minimum Number of Flips to Make Binary String Alternating (LC 1888)
            → There are only two valid alternating patterns: "0101..." and "1010...".
```

### 11-binary-search.md

```
coding/algorithms/11-binary-search.md
└── 11-binary-search.md
    ├── Lower Bound / Upper Bound
    │   ├── Search Insert Position (LC 35) `⚡ T1`
    │   │   → Need the leftmost index where arr[i] >= target — classic lower bound problem.
    │   ├── First Bad Version (LC 278) `⚡ T1`
    │   │   → The version sequence has a monotone predicate: False…False, True…True.
    │   ├── Find Smallest Letter Greater Than Target (LC 744) `⚡ T1`
    │   │   → Upper bound variant — find first index where letters[i] > target.
    │   └── H-Index II (LC 275) `⚡ T1`
    │       → Array is sorted.
    ├── Binary Search on Answer (Predicate Pattern)
    │   ├── Koko Eating Bananas (LC 875) `⚡ T1`
    │   │   → Larger k → fewer hours needed.
    │   ├── Capacity To Ship Packages Within D Days (LC 1011) `⚡ T1`
    │   ├── Split Array Largest Sum (LC 410) `⚡ T1`
    │   │   → Larger allowed max-sum → easier to fit into k parts.
    │   ├── Minimize Max Distance to Gas Station (LC 774) `⚡ T1`
    │   └── Minimum Speed to Arrive on Time (LC 1870) `⚡ T1`
    ├── Rotated Sorted Array
    │   ├── Search in Rotated Sorted Array (LC 33) `⚡ T1`
    │   │   → Not fully sorted, but one half around any mid is always sorted.
    │   ├── Find Minimum in Rotated Sorted Array (LC 153) `⚡ T1`
    │   │   → Minimum is the rotation boundary.
    │   ├── Search in Rotated Sorted Array II (LC 81) `⚡ T1`
    │   │   → Duplicates create ambiguity: when nums[lo] == nums[mid] == nums[hi], we cannot determine which half is sorted.
    │   └── Find Minimum in Rotated Sorted Array II (LC 154) `⚡ T1`
    │       → Same as LC 153 but nums[mid] == nums[hi] is now possible — can't determine which half contains the minimum.
    ├── Peak Element
    │   ├── Find Peak Element (LC 162) `⚡ T1`
    │   │   → If nums[mid] < nums[mid+1], the slope is ascending to the right — a peak must exist in [mid+1, hi].
    │   ├── Peak Index in a Mountain Array (LC 852) `⚡ T1`
    │   │   → Strictly unimodal — same ascending/descending slope argument as LC 162.
    │   └── Find a Peak Element in a 2D Grid (LC 1901) `⚡ T1`
    │       → Binary search on columns.
    ├── Median / Order Statistics
    │   ├── Median of Two Sorted Arrays (LC 4) `⚡ T1`
    │   │   → Merging is O(m+n).
    │   ├── Kth Smallest Element in a Sorted Matrix (LC 378) `⚡ T1`
    │   │   → "How many elements ≤ x?" is a monotone function of x.
    │   └── Search a 2D Matrix II (LC 240)
    │       → Rows AND columns are sorted but rows don't have total order (first of row i+1 may be less than last of row i).
    ├── Classic / Miscellaneous
    │   ├── Guess Number Higher or Lower (LC 374) `⚡ T1`
    │   │   → Search space [1, n] is totally ordered and the API gives three-way comparison — textbook binary search.
    │   ├── Find First and Last Position (LC 34) `⚡ T1`
    │   │   → Need leftmost and rightmost occurrence — two separate lower/upper bound searches.
    │   ├── Minimum Number of Days to Make m Bouquets (LC 1482) `⚡ T1`
    │   ├── Find K Closest Elements (LC 658) `⚡ T1`
    │   │   → The answer is always a contiguous subarray of length k.
    │   ├── Search a 2D Matrix — Row + Column BS (LC 74 variant note)
    │   │   → Useful when the single-index trick is not obvious in an interview.
    │   └── Longest Increasing Subsequence — Length via BS (LC 300) `⚡ T1`
    │       → Patience sorting uses a tails array where tails[i] is the smallest tail of all LIS of length i+1.
    ├── See Also
    │   └── Aggressive Cows / Maximize Minimum Distance
    │       → If a distance d works, any smaller distance also works.
    └── Binary Search on Answer — More Problems
        ├── Find K-th Smallest Pair Distance (LC 719) `⚡ T1`
        │   → The distance range is [0, max(nums) - min(nums)].
        └── Sqrt(x) — Integer Square Root (LC 69) `⚡ T1`
            → Binary search on the answer: the answer lies in [0, x].
```

### 00-sorting.md

```
coding/algorithms/00-sorting.md
└── 00-sorting.md
    ├── Bucket Sort
    │   └── Maximum Gap (Bucket Sort)
    │       → Comparison sort O(n log n) is too slow.
    ├── Custom Ordering / Comparator
    │   ├── Pancake Sorting
    │   │   → Standard swaps aren't available; only prefix reversals.
    │   ├── Custom Sort String
    │   │   → Standard sort knows nothing about the custom ordering.
    │   ├── Largest Number (custom comparator)
    │   │   → Numeric sort fails (e.g., 9 vs 91: "991" > "919" so 9 should precede 91).
    │   └── Wiggle Sort II (LC 324)
    │       → Find median, then place larger-than-median elements at odd indices and smaller-than-median elements at even indices, both in reverse order to avoid equal adjacent elements.
    ├── Interview Classics
    │   ├── H-Index (LC 274) `⚡ T1`
    │   │   → After sorting descending, at position i (0-indexed), if citations[i] >= i+1 then at least i+1 papers have >= i+1 citations.
    │   └── Meeting Rooms II (LC 253)
    │       → Sort by start time.
    ├── Classic Merge Variants
    │   ├── Majority Element (Boyer-Moore) `🎯 T2`
    │   │   → The majority element has count > n/2, so it outnumbers all others combined.
    │   ├── Sort an Array (Counting Sort Variant)
    │   │   → Comparison-based sorts bottom out at O(n log n); counting sort exploits a bounded integer domain to achieve O(n + k).
    │   ├── Radix Sort Implementation
    │   │   → Achieves O(d · (n + b)) where d = number of digits, b = base (10).
    │   └── Maximum Number After Digit Swaps (LC 2231)
    │       → Digits at even positions can only be rearranged among themselves; same for odd positions.
    ├── Interval / Sweep Line
    │   └── Minimum Number of Arrows to Burst Balloons (LC 452)
    │       → Same greedy activity-selection structure as LC 435.
    ├── Offline Sorting Tricks
    │   ├── Sort Array by Parity (LC 905)
    │   │   → Classic two-pointer Dutch-flag-style partition.
    │   └── Advantages Shuffle (LC 870)
    │       → Greedy: for each element of nums2 (sorted descending), try to "beat" it with the smallest element of nums1 that is still larger.
    ├── Topological Sort
    │   ├── Course Schedule II (LC 210) `⚡ T1`
    │   │   → Topological sort detects cycles and produces a valid linear ordering of a DAG.
    │   └── Alien Dictionary (LC 269) `⚡ T1`
    ├── External Sort / K-way Merge
    │   ├── Find K Pairs with Smallest Sums (LC 373) `⚡ T1`
    │   │   → K-way merge pattern: each row i of the implicit (nums1 × nums2) matrix is sorted.
    │   ├── Kth Largest Element in a Stream (LC 703) `⚡ T1`
    │   │   → A min-heap of size k maintains exactly the k largest elements seen so far.
    │   ├── Find Median from Data Stream (LC 295) `⚡ T1`
    │   │   → Two heaps maintain a balanced partition: a max-heap for the lower half and a min-heap for the upper half.
    │   └── Wiggle Sort II (Median Split)
    │       → The median separates smaller and larger elements.
    └── Sorting Applications
        └── Relative Sort Array (LC 1122)
            → Standard sorting can't directly encode a custom ordering defined by another array.
```

### 13-graph-algorithms.md

```
coding/algorithms/13-graph-algorithms.md
└── 13-graph-algorithms.md
    ├── Dijkstra's Algorithm
    │   ├── Network Delay Time
    │   │   → Shortest paths from a single source with non-negative weights.
    │   ├── Path with Maximum Probability
    │   │   → Maximize a product along a path — same structure as shortest path but with max-product instead of min-sum.
    │   ├── Evaluate Division (LC 399)
    │   └── Cheapest Flights Within K Stops (Dijkstra variant)
    │       → Bellman-Ford (next section) is the usual answer.
    ├── Bellman-Ford
    │   └── Find the City with the Smallest Number of Neighbors at a Threshold Distance (Floyd-Warshall)
    ├── Topological Sort (BFS — Kahn's)
    │   ├── Sequence Reconstruction (Check Unique Topo Order)
    │   └── Find All Possible Recipes from Given Supplies
    ├── Strongly Connected Components / Bridges
    │   └── Find Eventual Safe States (Reverse Graph / Kahn's) `⚡ T1`
    │       → Unsafe nodes are those on or leading to cycles.
    ├── Cycle Detection in Directed Graph
    │   └── Detect Cycle in Directed Graph (DFS 3-Color)
    │       → Kahn's BFS detects cycles implicitly via count, but DFS 3-color is the canonical O(V+E) approach that also identifies the cycle.
    ├── 0-1 BFS
    │   └── Open the Lock (Unweighted BFS Variant) `⚡ T1`
    │       → Each combination is a node; 8 neighbors (each of 4 digits ±1 mod 10).
    ├── Multi-source BFS / Special BFS
    │   ├── Word Ladder (BFS on Implicit Graph) `⚡ T1`
    │   │   → Nodes = words, edges = one-letter-apart pairs.
    │   ├── Word Ladder II (All Shortest Transformation Sequences) `⚡ T1`
    │   │   → Finding all shortest paths requires BFS to establish the level structure (shortest distance to each node), then backtracking to reconstruct paths — DFS alone is exponential without the level constraint.
    │   └── Possible Bipartition
    │       → "Split into two groups with no conflicts" = 2-color the conflict graph = bipartite check.
    ├── Minimum Spanning Tree — Prim's Algorithm
    │   └── Min Cost to Connect All Points (LC 1584)
    │       → MST problem on a dense graph (n² edges).
    ├── Graph Coloring
    │   └── M-Coloring Problem (Backtracking)
    │       → Graph coloring is NP-complete in general; backtracking with pruning is the standard approach for exact solutions on small graphs.
    └── See Also
        └── Bellman-Ford (Negative Weights)
            → Dijkstra does not work with negative edges.
```

### 14-union-find.md

```
coding/algorithms/14-union-find.md
└── 14-union-find.md
    ├── Basic Union-Find
    │   ├── Number of Connected Components in an Undirected Graph
    │   ├── Number of Provinces (Matrix Form) `⚡ T1`
    │   │   → Adjacency matrix encodes undirected edges.
    │   ├── Graph Valid Tree `⚡ T1`
    │   └── Satisfiability of Equality Equations `⚡ T1`
    │       → == is transitive.
    ├── Weighted / Ranked Union-Find
    │   ├── Accounts Merge (Email Graph) `⚡ T1`
    │   │   → Emails are the identity key, not names.
    │   ├── Smallest String With Swaps
    │   └── Evaluate Division (Weighted DSU)
    ├── MST (Kruskal's)
    │   ├── Min Cost to Connect All Points
    │   │   → Complete graph MST.
    │   └── Critical Connections / Pseudo-Critical Edges in MST
    │       → An edge is critical if excluding it raises MST cost.
    ├── Dynamic / Offline Union-Find
    │   ├── Number of Islands II `⚡ T1`
    │   │   → Islands are connected components growing dynamically.
    │   └── Minimize Malware Spread
    │       → Malware spreads to the entire connected component.
    ├── DSU for Other Problems
    │   ├── Longest Consecutive Sequence (DSU Approach) `⚡ T1`
    │   │   → x and x+1 belong to the same consecutive run — union them.
    │   └── Path with Maximum Probability (Weighted DSU)
    │       → For general graphs Dijkstra (max-heap variant) is canonical and handles multiple alternate paths.
    ├── Directed Graph Union-Find
    │   └── Redundant Connection II `⚡ T1`
    │       → In a directed tree (rooted), every non-root has in-degree 1.
    ├── Grid / Coordinate Union-Find
    │   └── Most Stones Removed with Same Row or Column
    ├── Weighted / Partial Swap Union-Find
    │   └── Minimize Hamming Distance After Swap Operations
    └── Connectivity With Constraints
        ├── Minimum Cost to Make at Least One Valid Path in a Grid
        │   → Edge weights are 0 (follow direction) or 1 (change direction).
        ├── Remove Max Number of Edges to Keep Graph Fully Traversable
        │   → We want minimal spanning forest for Alice and Bob independently.
        ├── Making a Large Island `⚡ T1`
        │   → After flipping a 0, the new cell connects up to 4 adjacent islands.
        ├── Number of Good Paths
        └── Largest Component Size by Common Factor
            → Shared prime factors link numbers together transitively.
```

### 16-greedy.md

```
coding/algorithms/16-greedy.md
└── 16-greedy.md
    ├── Interval Greedy
    │   ├── Merge Intervals `🎯 T2`
    │   │   → In arbitrary order, overlaps can't be detected without O(n²) pair checks.
    │   ├── Non-overlapping Intervals (Minimum number to remove) `🎯 T2`
    │   │   → Equivalent to maximizing the number of non-overlapping intervals kept (classic Activity Selection).
    │   ├── Meeting Rooms II
    │   │   → Each new meeting either reuses an ended room or opens a new one.
    │   ├── Minimum Number of Arrows to Burst Balloons
    │   │   → Same as activity selection but we want to maximize simultaneous coverage (one arrow covers all overlapping intervals at a point).
    │   ├── Video Stitching
    │   │   → Coverage problem — must reach position time from 0.
    │   ├── Minimum Taps to Open to Water a Garden
    │   │   → Same as Video Stitching — interval covering problem.
    │   └── Minimum Number of Groups for Non-Overlapping Intervals
    │       → This is exactly Meeting Rooms II — minimum rooms = minimum groups.
    ├── Simple Greedy
    │   ├── Assign Cookies (LC 455)
    │   │   → Sort both.
    │   └── Largest Perimeter Triangle (LC 976)
    │       → Triangle inequality: a+b > c where a≤b≤c.
    ├── Jump / Coverage Greedy
    │   ├── Jump Game (can reach?) `🎯 T2`
    │   │   → At any reachable index i, all indices up to i + nums[i] are also reachable — the reachable set is always a contiguous prefix [0, max_reach].
    │   ├── Jump Game II (minimum jumps) `🎯 T2`
    │   │   → At each "jump boundary," we must take a new jump.
    │   ├── Jump Game VI (DP + Deque) `🎯 T2`
    │   │   → dp[i] = max(dp[i-1..i-k]) + nums[i].
    │   ├── Candy (LC 135) `🎯 T2`
    │   │   → Two constraints (left and right neighbors) conflict if solved simultaneously.
    │   ├── Reorganize String `⚡ T1`
    │   │   → Impossible if any character appears more than ⌈n/2⌉ times.
    │   └── Rearrange String k Distance Apart (Rearrange Barcodes)
    ├── String / Array Greedy
    │   ├── Gas Station `🎯 T2`
    │   ├── Trapping Rain Water (greedy view) `⚡ T1`
    │   │   → Water at position i is bounded by min(max_left[i], max_right[i]) - height[i].
    │   ├── GCD of Strings
    │   │   → A GCD string must divide both strings.
    │   ├── Connect Sticks (Huffman / Min Cost)
    │   │   → Each stick's length contributes to the total cost once per merge it participates in.
    │   ├── Minimum Difference After Operations
    │   │   → After removing k elements, we keep n-k elements.
    │   └── Partition Labels (LC 763)
    │       → Each character must stay in one partition — it determines the right boundary of the partition containing its first occurrence.
    ├── Sorting-Based Greedy
    │   ├── Queue Reconstruction by Height (LC 406)
    │   │   → Taller people are invisible to shorter ones for the k-count.
    │   ├── IPO (Maximize Capital, LC 502) `⚡ T1`
    │   │   → At each step, among all affordable projects, the greedy optimal is to pick the highest-profit one — taking less profit now can't help unlock better future projects than taking more profit.
    │   └── Activity Selection (Maximum Non-Overlapping Intervals)
    │       → Greedy by earliest finishing time leaves the most room for future intervals.
    └── See Also (Extended)
        └── Hand of Straights `🎯 T2`
```

### 12-backtracking.md

```
coding/algorithms/12-backtracking.md
└── 12-backtracking.md
    ├── Subsets / Combinations
    │   ├── Subsets (Power Set) `🎯 T2`
    │   │   → Every element has a binary choice — include or exclude.
    │   ├── Subsets II (with duplicates) `🎯 T2`
    │   │   → Duplicates produce identical subsets when same-valued elements are included at the same decision level.
    │   ├── Combination Sum (unbounded) `🎯 T2`
    │   │   → Elements can be reused, but combinations (not permutations) are needed.
    │   ├── Combination Sum II (0/1 — no reuse) `🎯 T2`
    │   │   → No reuse → recurse with i+1.
    │   ├── Combinations `🎯 T2`
    │   │   → Fixed-size subset problem.
    │   └── Letter Combinations of a Phone Number `🎯 T2`
    │       → Each digit maps to 3-4 letters — pure Cartesian product.
    ├── Permutations
    │   ├── Permutations `🎯 T2`
    │   │   → Each permutation chooses from all remaining unused elements at each depth.
    │   ├── Permutations II (with duplicates) `🎯 T2`
    │   │   → Duplicate values can appear at the same position in the permutation tree, generating identical permutations.
    │   ├── Next Permutation (iterative approach) `🎯 T2`
    │   │   → Not backtracking per se, but generates the next item in the permutation enumeration order.
    │   └── Letter Case Permutation `🎯 T2`
    │       → Each letter has two choices (upper/lower); digits have one choice.
    ├── String Backtracking
    │   ├── Generate Parentheses `🎯 T2`
    │   │   → At each position, two choices: ( or ).
    │   ├── Palindrome Partitioning `🎯 T2`
    │   │   → At each position, try all possible next partition points.
    │   ├── Remove Invalid Parentheses
    │   │   → First compute minimum removals (one scan: track unmatched ( as open_rem, unmatched ) as close_rem).
    │   ├── Word Search `⚡ T1`
    │   │   → Need to find a specific path through a grid — DFS with backtracking is the natural approach.
    │   └── Expression Add Operators (LC 282)
    │       → Brute force tries all 3^(n-1) operator placements.
    ├── Board / Matrix Backtracking
    │   ├── N-Queens `🎯 T2`
    │   │   → One queen per row (DFS depth = row).
    │   ├── Sudoku Solver `🎯 T2`
    │   │   → Constraint satisfaction: each empty cell has a small set of valid digits.
    │   └── Unique Paths III `🎯 T2`
    ├── Trie + Backtracking
    │   ├── Combination Sum III `🎯 T2`
    │   │   → Fixed-size (exactly k elements), fixed-sum, fixed universe (1-9).
    │   ├── Target Sum `🎯 T2`
    │   │   → Binary choice per element (+ or -) → 2^n branches.
    │   ├── Beautiful Arrangement `🎯 T2`
    │   │   → Permutation backtracking where each position has a constraint.
    │   └── Restore IP Addresses `🎯 T2`
    │       → Exactly 4 segments, each 1-3 digits.
    ├── String Backtracking (continued)
    │   ├── Word Break II `🎯 T2`
    │   │   → Try every possible first word; recurse on the suffix.
    │   └── Palindrome Partitioning II (Minimum Cuts) `🎯 T2`
    │       → Pure backtracking (enumerate all partitions) is O(n · 2^n).
    ├── Grid Traversal
    │   ├── Rat in a Maze `🎯 T2`
    │   │   → Enumerate all valid root-to-destination paths in a grid graph.
    │   └── Word Search (All Occurrences) `⚡ T1`
    │       → Extension of Word Search I: instead of stopping at the first match, collect all starting (r,c) positions.
    └── Advanced Backtracking
        ├── N-Queens II (Count Only) `🎯 T2`
        │   → Same algorithm as N-Queens but without board construction or path copying — just increment a counter at the leaf.
        ├── Word Break (Decision — Backtracking + Memo) `🎯 T2`
        │   → At each position, try every dictionary word as the next segment.
        └── Generate All Valid IP Addresses (Generalized Segmentation)
            → Generalizes Restore IP Addresses: given a digit string, split into exactly k segments each in range [lo, hi] with no leading zeros.
```

### 02-string-algorithms.md

```
coding/algorithms/02-string-algorithms.md
└── 02-string-algorithms.md
    ├── KMP (Knuth-Morris-Pratt)
    │   ├── Implement KMP — Failure Function + Search
    │   │   → Naive search rescans characters already matched; O(nm) is unacceptable for large text.
    │   ├── Find All Occurrences of Pattern in Text
    │   │   → Standard substring search is O(nm); we need every occurrence, not just the first.
    │   └── Add Minimum Characters to Make String a Palindrome
    │       → We need the longest prefix of s that is already a palindrome; characters after that prefix must be reflected at the front.
    ├── Rabin-Karp (Rolling Hash)
    │   ├── Implement Rabin-Karp
    │   │   → Direct character-by-character comparison at each position is O(nm).
    │   ├── Longest Duplicate Substring `⚡ T1`
    │   │   → Checking all substrings for duplicates is O(n³).
    │   └── Count Distinct Doubled Substrings
    │       → We need to find all substrings of even length where both halves are identical — checking naively is O(n³).
    ├── Z-Function / Z-Algorithm
    │   ├── Pattern Matching Using Z-Array
    │   │   → Same goal as KMP — O(n+m) pattern matching.
    │   └── Repeated String Match
    │       → B can span at most ceil(len(B)/len(A)) + 1 copies of A.
    ├── Palindrome Algorithms
    │   ├── Longest Palindromic Substring — Expand Around Center `🎯 T2`
    │   │   → A palindrome reads the same forwards and backwards; the structural invariant is symmetry around a center.
    │   ├── Palindromic Substrings — Count
    │   │   → Each center expansion contributes one palindrome per step.
    │   └── Manacher's Algorithm — O(n) All Palindromes
    │       → Naive expand-around-center is O(n²) because each center expands independently.
    ├── Sliding Window on Strings
    │   ├── Longest Substring with K Distinct Characters
    │   │   → We want the longest window satisfying a constraint on character diversity — a classic sliding window.
    │   ├── Permutation in String `⚡ T1`
    │   │   → A permutation of s1 is any arrangement of its characters; we need a window in s2 with the same character frequencies.
    │   ├── Regular Expression Matching (LC 10)
    │   │   → '*' creates a choice — use the preceding element 0 times (skip pattern[i-1] and '*') or 1+ times (consume s[j] if it matches).
    │   ├── Wildcard Matching (LC 44)
    │   │   → '*' can match any sequence — creates branching over all possible lengths.
    │   └── Distinct Subsequences (LC 115) `🎯 T2`
    │       → At each character of s, we choose to include it (matching t[j]) or skip it.
    └── See Also
        └── Shortest Palindrome
            → We need the longest palindromic prefix.
```

### 15-dynamic-programming.md

```
coding/algorithms/15-dynamic-programming.md
└── 15-dynamic-programming.md
    ├── Linear DP (1-D)
    │   ├── Climbing Stairs `🎯 T2`
    │   │   → reaching step i from step i-1 or i-2 creates overlapping recursive calls.
    │   ├── Min Cost Climbing Stairs `🎯 T2`
    │   │   → cost to reach step i depends on minimum of two prior steps.
    │   ├── House Robber `🎯 T2`
    │   │   → robbing house i forbids i-1; the optimal decision at each house depends on the optimal result two positions back.
    │   ├── House Robber II (Circular) `🎯 T2`
    │   │   → Circular constraint means house 0 and house n-1 can't both be robbed.
    │   ├── Maximum Subarray (Kadane's — DP view) `🎯 T2`
    │   │   → max subarray ending at i depends on whether extending the previous subarray or restarting gives a larger value.
    │   ├── Word Break `🎯 T2`
    │   │   → s[0..i] is breakable if any split s[0..j] is breakable and s[j+1..i] is in the dictionary.
    │   └── Decode Ways `🎯 T2`
    ├── 0/1 Knapsack
    │   ├── Subset Sum Problem `🎯 T2`
    │   │   → each item has two choices (include/exclude); overlap arises because the same remaining capacity is reachable via multiple item sequences.
    │   ├── Partition Equal Subset Sum `🎯 T2`
    │   │   → Equal partition iff one subset sums to total/2.
    │   └── Last Stone Weight II `⚡ T1`
    │       → Each stone ultimately gets a sign +1 or -1; minimize |P - N| = |total - 2N|.
    ├── Unbounded Knapsack
    │   ├── Coin Change (Min Coins) `🎯 T2`
    │   │   → Coins are reusable → unbounded knapsack.
    │   ├── Coin Change II (Total Ways) `🎯 T2`
    │   │   → Combinations require each denomination to be processed once, not per position.
    │   └── Perfect Squares `🎯 T2`
    │       → Perfect squares are unlimited "coins"; this is unbounded knapsack / coin change with coins = {1,4,9,16,...}.
    ├── LCS Family
    │   ├── Longest Common Subsequence `🎯 T2`
    │   │   → Matching characters at positions i,j yields a subproblem on the remaining suffixes; these sub-results are reused.
    │   ├── Edit Distance `🎯 T2`
    │   │   → Three operations at each mismatch create overlapping subproblems on shorter string pairs.
    │   ├── Longest Palindromic Subsequence `🎯 T2`
    │   │   → A palindrome is its own reverse; LPS(s) = LCS(s, reverse(s)).
    │   ├── Minimum ASCII Delete Sum for Two Strings `🎯 T2`
    │   │   → Deleting characters to equalize is equivalent to keeping the maximum-weight common subsequence (measured in ASCII values).
    │   └── Minimum Window Subsequence (LC 727) `🎯 T2`
    ├── Grid DP
    │   ├── Unique Paths `🎯 T2`
    │   │   → Each cell is reachable from exactly above or left; paths to any cell = sum of paths to two neighbors — overlapping.
    │   ├── Unique Paths II (With Obstacles) `🎯 T2`
    │   │   → Same grid DP but obstacle cells have zero paths and block propagation downstream.
    │   ├── Minimum Path Sum `🎯 T2`
    │   │   → Min-cost path to (i,j) = grid value + min of cost from above or left — overlapping.
    │   └── Maximal Square `🎯 T2`
    │       → A square of side k at (i,j) requires squares of side k-1 at three adjacent neighbors — optimal substructure with overlapping sub-rectangles.
    ├── Interval DP
    │   ├── Matrix Chain Multiplication (Concept)
    │   │   → Splitting the chain at any point k yields independent subproblems for left and right chains; optimal split depends on results of all sub-chains — overlapping.
    │   └── Strange Printer
    │       → Printing s[i..j] can leverage if s[i]==s[k] for some k in (i,j) — we can extend the first turn to cover s[k].
    ├── State Machine DP (Stocks)
    │   ├── Best Time to Buy and Sell Stock (All Variants) `🎯 T2`
    │   ├── Stock with Cooldown
    │   │   → Three states model the constraint: holding, just sold (cooldown), resting.
    │   └── Stock with Transaction Fee
    │       → Two states: hold (best profit holding), cash (best profit not holding).
    ├── Digit DP
    │   ├── Numbers At Most N Given Digit Set
    │   └── Count Numbers with Unique Digits
    │       → At each digit position, choices depend only on how many distinct digits have been used — classic digit DP structure.
    ├── Longest Increasing Subsequence (LIS) Family
    │   ├── Longest Increasing Subsequence `⚡ T1`
    │   │   → Naïve O(n²) DP checks all prior elements; patience sort uses a maintained tails array to binary-search the right position, achieving O(n log n).
    │   ├── Number of LIS
    │   │   → Length alone isn't enough; need to count paths.
    │   └── Longest Bitonic Subsequence
    │       → Decompose into LIS from the left and LIS from the right (longest decreasing = LIS reversed).
    ├── String DP
    │   ├── Distinct Subsequences `🎯 T2`
    │   │   → At each position we either use s[i] to match t[j] or we skip it; both branches must be counted.
    │   ├── Interleaving String `🎯 T2`
    │   │   → At each position in s3 we choose whether the next character comes from s1 or s2; overlapping subproblems arise.
    │   └── Regular Expression Matching
    │       → * introduces branching — match zero occurrences (skip pattern pair) or one-or-more — creating overlapping sub-problems.
    ├── Probability / Expected Value DP
    │   ├── Knight Probability in Chessboard
    │   │   → After each move, probability distributes over up to 8 neighbours; cells off-board contribute 0.
    │   └── New 21 Game
    │       → dp[x] = probability of reaching exactly x before stopping.
    ├── Bitmask DP
    │   └── Partition to K Equal Subset Sums `🎯 T2`
    │       → Subset assignment is NP-hard in general but n ≤ 16 makes 2^n bitmask DP feasible.
    ├── Game Theory DP
    │   ├── Stone Game
    │   │   → Each player maximises their own score minus the opponent's; the decision at each subarray depends on what the opponent will optimally do.
    │   ├── Stone Game II
    │   │   → The value of M changes each turn, so state must encode both position and current M.
    │   └── Predict the Winner
    │       → Identical structure to Stone Game.
    ├── DP on Sequences
    │   ├── Jump Game II `🎯 T2`
    │   │   → Greedy DP: at each jump, greedily extend to the farthest reachable index.
    │   ├── Maximum Product Subarray `🎯 T2`
    │   │   → A negative number flips max↔min, so both must be tracked at each position.
    │   └── Arithmetic Slices II — Subsequence
    │       → Unlike subarrays, subsequences can skip elements; tracking every possible common difference per ending index is necessary.
    ├── See Also
    │   └── Longest Common Substring
    │       → Unlike LCS, contiguity matters.
    └── Dynamic Programming — Hard Problems
        └── Russian Doll Envelopes (LC 354)
            → If we sort by width, this becomes LIS on heights.
```

### 09-recursion.md

```
coding/algorithms/09-recursion.md
└── 09-recursion.md
    ├── Foundation — Include/Exclude
    │   └── Binary Tree Paths
    │       → Tree structure is inherently recursive; each subtree is a smaller instance of the same problem.
    ├── Divide and Conquer (via Recursion)
    │   ├── Merge Sort `🎯 T2`
    │   │   → Sorting n items can be decomposed into sorting two halves independently (no overlap between halves) and merging in O(n).
    │   └── Fibonacci (Memoized Recursion vs DP)
    │       → Naive recursion f(n) = f(n-1) + f(n-2) recomputes the same k over and over.
    ├── Pruning & Constraints
    │   ├── Combination Sum II (No Reuse) `🎯 T2`
    │   │   → Elements can repeat in input but not in output combinations.
    │   ├── Word Search (Grid Backtracking) `⚡ T1`
    │   │   → Exponential state space of paths; backtracking explores all starting positions and directions, pruning when the current character doesn't match.
    │   ├── Word Search II (Trie + Backtracking) `⚡ T1`
    │   │   → Running Word Search separately for each word is O(W · m·n · 4^L).
    │   ├── Unique Binary Search Trees II
    │   │   → Each integer k in [1..n] can be the root; values 1..k-1 form the left subtree and k+1..n form the right subtree.
    │   ├── Expression Add Operators
    │   │   → Exponential operator assignments require backtracking.
    │   └── Robot Room Cleaner
    ├── Foundation — Recursion Fundamentals
    │   ├── Binary Search (Recursive)
    │   │   → The array is sorted — at each step the search space halves by comparing the midpoint.
    │   ├── Tower of Hanoi
    │   │   → The recurrence is T(n) = 2T(n-1) + 1.
    │   ├── Print All Subsequences
    │   │   → Each element has exactly two choices — include or exclude.
    │   └── Josephus Problem
    │       → After each elimination the circle shrinks by 1 and the indices shift.
    ├── Graph — Recursive Traversal
    │   ├── Decode String (Recursive)
    │   │   → Nested brackets are naturally recursive — decoding the inner bracket is a subproblem of the same type.
    │   ├── Flatten Nested List Iterator
    │   │   → Nested structure is recursively defined — a list element is either an integer (base case) or another list (recursive case).
    │   └── Nested List Weight Sum
    ├── Dynamic Programming Foundations (Recursive + Memo)
    │   ├── Climbing Stairs (Memoized Recursion) `🎯 T2`
    │   │   → Memoize ways(n) in a dict — same recurrence as Fibonacci.
    │   ├── Construct Binary Tree from Preorder and Inorder Traversal (LC 105) `🎯 T2`
    │   │   → preorder[0] is always the root.
    │   ├── Serialize and Deserialize Binary Tree (LC 297) `🎯 T2`
    │   │   → Preorder traversal with explicit null markers uniquely encodes any binary tree, enabling recursive reconstruction without an inorder array.
    │   ├── Permutations II (LC 47) `🎯 T2`
    │   │   → Duplicates at the same recursion level produce identical branches.
    │   ├── Subsets II (LC 90) `🎯 T2`
    │   │   → Same duplicate-skip strategy as Permutations II but applied to the combination/subset template.
    │   └── Combinations (LC 77) `🎯 T2`
    │       → Classic choose-k-from-n combinatorial generation.
    ├── Divide and Conquer — Advanced
    │   ├── Maximum Subarray — D&C (O(n log n)) `🎯 T2`
    │   │   → Illustrates D&C: split at mid; max subarray is entirely in left half, entirely in right half, or crosses the midpoint.
    │   ├── Pow(x, n) — Fast Exponentiation
    │   │   → Naive O(n) multiplication is too slow for large n.
    │   └── Count of Inversions (Merge-Sort Based)
    │       → During merge sort, when a right-half element is placed before left-half elements, all remaining left-half elements form inversions with it.
    ├── Recursion on Graphs
    │   ├── Clone Graph (LC 133) `⚡ T1`
    │   └── Number of Islands (LC 200) `⚡ T1`
    │       → DFS flood-fill: when a '1' is found, recursively sink the entire connected land mass (mark as '0') so it is never counted again.
    ├── Recursive Parsing / Evaluation
    │   ├── Basic Calculator II (LC 227)
    │   │   → Operator precedence makes this a parsing problem.
    │   └── Fast Doubling Fibonacci
    │       → The recurrence can be reduced by halving n, which turns linear recursion into logarithmic recursion depth.
    └── Recursion — More Problems
        └── Predict the Winner (LC 486)
            → dp(i, j) = score advantage for the current player on subarray [i, j].
```


---

_Maintained by hand — update alongside `coding/` problem files._
