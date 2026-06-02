---
module: 03-patterns
topic: Questions
subtopic: 
status: unread
tags: [patterns, questions]
---
# Repository Interview Questions Tracker

This file serves as a centralized, interactive checklist for all the canonical interview questions covered in this repository. Use it to track your progress. Each question links directly to the detailed walkthrough, logic, and gotchas inside the deep-dive files.

---

## Progress Summary
*   [ ] **Arrays, Two Pointers & Sliding Window** (`0 / 20`)
*   [ ] **Strings** (`0 / 12`)
*   [ ] **Linked Lists** (`0 / 9`)
*   [ ] **Stacks & Queues** (`0 / 8`)
*   [ ] **Trees & BST** (`0 / 18`)
*   [ ] **Graphs** (`0 / 16`)
*   [ ] **Disjoint Set Union (DSU)** (`0 / 5`)
*   [ ] **Segment Tree & Fenwick Tree** (`0 / 3`)
*   [ ] **Heaps & Priority Queues** (`0 / 6`)
*   [ ] **Backtracking** (`0 / 12`)
*   [ ] **Dynamic Programming** (`0 / 18`)
*   [ ] **Greedy** (`0 / 4`)
*   [ ] **Intervals** (`0 / 5`)
*   [ ] **Tries** (`0 / 3`)
*   [ ] **Matrix / Grid BFS** (`0 / 5`)
*   [ ] **Binary Search** (`0 / 7`)
*   [ ] **Bit Manipulation** (`0 / 7`)
*   [ ] **Math & Number Theory** (`0 / 4`)

---

## 1. Arrays, Two Pointers & Sliding Window

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Two Sum — Given an integer array `nums` and target, return indices of two numbers that sum to `target`. Exactly one solution exists | Easy | Hash Map / Two Pointers | [array.md](../01-data-structures/array.md#interview-questions--logic--trickiness) |
| [ ] | Best Time to Buy/Sell Stock — Given an array `prices` where `prices[i]` is the price of a stock on day `i`, find the maximum profit from a single buy-sell transaction. You cannot sell before buying | Easy | Kadane's Variant | [array.md](../01-data-structures/array.md#interview-questions--logic--trickiness) |
| [ ] | Maximum Subarray — Find the contiguous subarray with the largest sum. Return the sum | Easy | Kadane's Algorithm | [array.md](../01-data-structures/array.md#interview-questions--logic--trickiness) |
| [ ] | Product of Array Except Self — Return an array where `output[i]` is the product of all elements except `nums[i]`. No division. O(n) time, O(1) extra space | Medium | Prefix/Suffix Products | [array.md](../01-data-structures/array.md#interview-questions--logic--trickiness) |
| [ ] | Maximum Product Subarray — Find the contiguous subarray with the largest product. Return the product | Medium | Dynamic Programming | [array.md](../01-data-structures/array.md#interview-questions--logic--trickiness) |
| [ ] | Container With Most Water — Given heights of vertical lines, find the two lines that form a container holding the maximum water | Medium | Two Pointers | [array.md](../01-data-structures/array.md#interview-questions--logic--trickiness) |
| [ ] | Trapping Rain Water — Given an elevation map, compute how much water it can trap after raining | Hard | Two Pointers / Stack | [array.md](../01-data-structures/array.md#interview-questions--logic--trickiness) |
| [ ] | Sliding Window Maximum — Return the maximum in each sliding window of size `k` | Hard | Monotonic Deque | [queue.md](../01-data-structures/queue.md#interview-questions--logic--trickiness) |
| [ ] | Merge Intervals — Given a list of intervals, merge all overlapping intervals and return the result | Medium | Sorting / Sweep Line | [array.md](../01-data-structures/array.md#interview-questions--logic--trickiness) |
| [ ] | Non-overlapping Intervals — Find the minimum number of intervals to remove so that the rest are non-overlapping | Medium | Greedy End-Time Sort | [greedy.md](../02-algorithms/greedy.md#interview-questions--logic--trickiness) |
| [ ] | Jump Game — Given an array where `nums[i]` is the max jump length from index `i`, determine if you can reach the last index | Medium | Greedy Reachability | [greedy.md](../02-algorithms/greedy.md#interview-questions--logic--trickiness) |
| [ ] | Jump Game II — Given an array where `nums[i]` is the max jump from index `i`, return the minimum number of jumps to reach the last index. Always reachable | Medium | Greedy BFS Layers | [greedy.md](../02-algorithms/greedy.md#interview-questions--logic--trickiness) |
| [ ] | Find Minimum in Rotated Array — Find the minimum element in a rotated sorted array with no duplicates | Medium | Binary Search | [searching.md](../02-algorithms/searching.md#interview-questions--logic--trickiness) |
| [ ] | Search in Rotated Array — Given a sorted array rotated at some pivot, search for a target. Return its index, or -1 if not found | Medium | Binary Search | [searching.md](../02-algorithms/searching.md#interview-questions--logic--trickiness) |
| [ ] | Subarray Sum Equals K — Count the number of contiguous subarrays with sum equal to `k`. Array may contain negatives | Medium | Prefix Sum + Hash Map | [array.md](../01-data-structures/array.md#interview-questions--logic--trickiness) |
| [ ] | Subarray Sums Divisible by K — Count the number of subarrays whose sum is divisible by `K` | Medium | Prefix Sum Modulo | [array.md](../01-data-structures/array.md#interview-questions--logic--trickiness) |
| [ ] | Subarrays with K Different Integers — Count subarrays with exactly `k` distinct integers | Hard | Sliding Window Subtraction | [array.md](../01-data-structures/array.md#interview-questions--logic--trickiness) |
| [ ] | 3Sum — Find all unique triplets `[a, b, c]` in `nums` with `a + b + c = 0`. No duplicate triplets | Medium | Sort + Two Pointers | [two-pointers.md](../02-algorithms/two-pointers.md#interview-questions--logic--trickiness) |
| [ ] | 4Sum — Find all unique quadruplets summing to `target` | Medium | Sort + Two Pointers (outer 2 loops) | [two-pointers.md](../02-algorithms/two-pointers.md#interview-questions--logic--trickiness) |
| [ ] | Longest Consecutive Sequence — Find the length of the longest consecutive elements sequence in an unsorted array. O(n) required | Medium | Hash Set Chain Start | [hashing.md](../01-data-structures/hashing.md#interview-questions--logic--trickiness) |

---

## 2. Strings

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Valid Palindrome — Given string `s`, return true if it is a palindrome considering only alphanumeric characters and ignoring case | Easy | Two Pointers | [string.md](../02-algorithms/string.md#interview-questions--logic--trickiness) |
| [ ] | Valid Anagram — Return true if `t` is an anagram of `s` (same characters, same counts) | Easy | Frequency Counter | [string.md](../02-algorithms/string.md#interview-questions--logic--trickiness) |
| [ ] | Longest Substring Without Repeating — Same as “Longest Substring Without Repeating Characters” (alias name) | Medium | Sliding Window | [string.md](../02-algorithms/string.md#interview-questions--logic--trickiness) |
| [ ] | Longest Repeating Char Replacement — Given string `s` and integer `k`, find the length of the longest substring where you can replace at most `k` characters to make all characters in the window the same | Medium | Sliding Window | [string.md](../02-algorithms/string.md#interview-questions--logic--trickiness) |
| [ ] | Minimum Window Substring — Find the smallest substring of `s` containing all characters of `t` (with multiplicity) | Hard | Sliding Window | [string.md](../02-algorithms/string.md#interview-questions--logic--trickiness) |
| [ ] | Group Anagrams — Group strings that are anagrams of each other | Medium | String Key Encoding | [string.md](../02-algorithms/string.md#interview-questions--logic--trickiness) |
| [ ] | Find All Anagrams — Find all starting indices where a substring of `s` is an anagram of `p` | Medium | Fixed Sliding Window | [string.md](../02-algorithms/string.md#interview-questions--logic--trickiness) |
| [ ] | Longest Palindromic Substring — Given string `s`, return the longest substring that is a palindrome | Medium | Expand from Center | [string.md](../02-algorithms/string.md#interview-questions--logic--trickiness) |
| [ ] | Palindromic Substrings (count) — Given string `s`, return the total count of substrings that are palindromes (single characters count too) | Medium | Expand from Center | [string.md](../02-algorithms/string.md#interview-questions--logic--trickiness) |
| [ ] | Encode and Decode Strings — Design functions `encode(strs)` and `decode(s)` to encode a list of strings into a single string and decode it back. The encoding must handle strings that contain any character including `#` and `/` | Medium | Length Delimiter | [string.md](../02-algorithms/string.md#interview-questions--logic--trickiness) |
| [ ] | Implement strStr (KMP) — Return the index of the first occurrence of `needle` in `haystack`. Return -1 if not present. (LC 28 — implement using KMP for O(n+m) worst case.) | Hard | LPS State Matching | [string.md](../02-algorithms/string.md#interview-questions--logic--trickiness) |
| [ ] | Word Search II — Given a board of characters and a list of words, return all words that appear on the board. A word is valid if it can be traced through adjacent (4-directional) cells without reusing any cell within the same word | Hard | Trie + Grid DFS | [trie.md](../01-data-structures/trie.md#interview-questions--logic--trickiness) |

---

## 3. Linked Lists

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Reverse Linked List — Given the head of a singly linked list, reverse it in place and return the new head | Easy | Three Pointers | [linked-list.md](../01-data-structures/linked-list.md#interview-questions--logic--trickiness) |
| [ ] | Merge Two Sorted Lists — Merge two sorted linked lists into one sorted list. Return the head of the merged list | Easy | Dummy Node | [linked-list.md](../01-data-structures/linked-list.md#interview-questions--logic--trickiness) |
| [ ] | Reorder List — Reorder list in-place: `L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → ...` | Medium | Fast/Slow + Reverse | [linked-list.md](../01-data-structures/linked-list.md#interview-questions--logic--trickiness) |
| [ ] | Remove Nth Node From End — Remove the n-th node from end in one pass | Medium | Two Pointers Offset | [linked-list.md](../01-data-structures/linked-list.md#interview-questions--logic--trickiness) |
| [ ] | Linked List Cycle — Detect if a linked list has a cycle | Easy | Fast/Slow meeting | [linked-list.md](../01-data-structures/linked-list.md#interview-questions--logic--trickiness) |
| [ ] | Linked List Cycle II (Entry) — Find the node where the cycle begins. Return None if no cycle | Medium | Fast/Slow + Math | [linked-list.md](../01-data-structures/linked-list.md#interview-questions--logic--trickiness) |
| [ ] | Merge K Sorted Lists — Merge `k` sorted linked lists into one sorted linked list | Hard | Min-Heap K-way Merge | [linked-list.md](../01-data-structures/linked-list.md#interview-questions--logic--trickiness) |
| [ ] | LRU Cache — Design a cache with O(1) `get` and `put` operations, evicting the Least Recently Used item when capacity is exceeded | Medium | Hash Map + DLL | [linked-list.md](../01-data-structures/linked-list.md#interview-questions--logic--trickiness) |
| [ ] | Copy List with Random Pointer — Deep copy a linked list where each node has `next` and `random` pointers. `random` may point to any node or null | Medium | Map Clones / Interleave | [linked-list.md](../01-data-structures/linked-list.md#interview-questions--logic--trickiness) |

---

## 4. Stacks & Queues

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Valid Parentheses — Given a string of `()[]{}`, determine if the brackets are valid (properly nested and matched) | Easy | LIFO Matching | [stack.md](../01-data-structures/stack.md#interview-questions--logic--trickiness) |
| [ ] | Min Stack — Design a stack with O(1) `push`, `pop`, `top`, and `get_min` | Easy | Auxiliary LIFO | [stack.md](../01-data-structures/stack.md#interview-questions--logic--trickiness) |
| [ ] | Daily Temperatures — Given a list of daily temperatures, return an array where `result[i]` is the number of days until a warmer temperature. If no warmer day exists, `result[i] = 0` | Medium | Monotonic Stack | [stack.md](../01-data-structures/stack.md#interview-questions--logic--trickiness) |
| [ ] | Next Greater Element — Solve the standard interview variant of Next Greater Element. | Medium | Monotonic Stack | [stack.md](../01-data-structures/stack.md#interview-questions--logic--trickiness) |
| [ ] | Largest Rectangle in Histogram — Given heights of bars in a histogram, find the area of the largest rectangle that fits within the histogram | Hard | Monotonic Stack | [stack.md](../01-data-structures/stack.md#interview-questions--logic--trickiness) |
| [ ] | Car Fleet — N cars head to the same destination `target`. Each car has a position and speed. A faster car that catches a slower one forms a fleet and travels at the slower car's speed. Return the number of fleets that arrive | Medium | Sorting + Stack | [stack.md](../01-data-structures/stack.md#interview-questions--logic--trickiness) |
| [ ] | Sliding Window Maximum — Return the maximum in each sliding window of size `k` | Hard | Monotonic Deque | [queue.md](../01-data-structures/queue.md#interview-questions--logic--trickiness) |
| [ ] | Decode String — Decode a string encoded as `k[encoded_string]`. E.g., `3[a2[c]]` → `accaccacc` | Medium | Nested LIFO Parsing | [stack.md](../01-data-structures/stack.md#interview-questions--logic--trickiness) |

---

## 5. Trees & BST

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Invert Binary Tree — Given a binary tree root, mirror it — every left child becomes right and vice versa at every level | Easy | DFS / BFS Swap | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | Maximum Depth — Return the maximum depth (number of nodes on the longest root-to-leaf path) | Easy | Post-order DFS | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | Same Tree — Given two binary trees, return true if they are structurally identical with the same node values at every position. LC 100 | Easy | DFS Simultaneous | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | Subtree of Another Tree — Given trees `root` and `subRoot`, return true if `subRoot` is a subtree of `root` (subRoot exists as an exact match rooted at some node in root). LC 572 | Easy | DFS Matching | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | Lowest Common Ancestor (BST) — Find LCA of two nodes in a BST and in a general binary tree | Easy | BST Node Bounds | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | Lowest Common Ancestor (any) — Find LCA of two nodes in a BST and in a general binary tree | Medium | Post-order DFS | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | Validate BST — Check if a binary tree satisfies BST ordering | Medium | Min/Max DFS Bounds | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | Kth Smallest in BST — Return kth smallest value in BST | Medium | In-order DFS | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | Path Sum II — Find all root-to-leaf paths in a binary tree where the sum of node values equals `target`. Return all such paths | Medium | DFS Backtracking | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | Binary Tree Max Path Sum — Find the maximum path sum between any two nodes. Values can be negative; a path can start and end anywhere | Hard | Post-order DFS Gain | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | Serialize/Deserialize — Alias name used for “Serialize and Deserialize Binary Tree” | Hard | Pre-order Traversal | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | Level Order Traversal — Given the root of a binary tree, return its level-order traversal as a list of lists, where each inner list contains node values at that depth (LC 102) | Medium | BFS with Deque | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | Right Side View — Given the root of a binary tree, return the values of nodes visible when looking at the tree from the right side — i.e., the last node at each level (LC 199) | Medium | BFS Level Extremity | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | Count Good Nodes — A node X is "good" if no node on the root-to-X path has a value greater than X.val. Count good nodes | Medium | Path Max DFS | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | Construct from Pre+Inorder — Given `preorder` and `inorder` arrays of a binary tree's traversal, reconstruct the tree | Medium | Divide & Conquer DFS | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | Step-By-Step Directions — Given root, `startValue`, and `destValue`, return the shortest path as a string of `'L'`, `'R'`, `'U'` characters | Medium | LCA Path Generation | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | Path Sum III — Count paths that sum to `targetSum`. Paths must go downward (ancestor to descendant) but need not start at root or end at leaf | Medium | DFS Prefix Sum Map | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |
| [ ] | House Robber III — Houses are arranged in a binary tree. Adjacent nodes (parent-child) cannot both be robbed. Maximize total money robbed | Medium | Tree DP (rob/skip state) | [tree.md](../01-data-structures/tree.md#interview-questions--logic--trickiness) |

---

## 6. Graphs

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Number of Islands — Given a 2D grid of '1' (land) and '0' (water), count the number of islands (connected components of land, 4-directional) | Medium | BFS/DFS Grid Flood | [graphs.md](../01-data-structures/graphs.md#interview-questions--logic--trickiness) |
| [ ] | Clone Graph — Given a reference to a node in an undirected connected graph, return a deep copy | Medium | BFS/DFS Hash Clones | [graphs.md](../01-data-structures/graphs.md#interview-questions--logic--trickiness) |
| [ ] | Pacific Atlantic Water Flow — Given an m×n height matrix, water flows to 4-adjacent cells of equal or lesser height. Find all cells from which water can reach both the Pacific (top/left border) and Atlantic (bottom/right border) oceans | Medium | Multi-source Reverse BFS | [graphs.md](../01-data-structures/graphs.md#interview-questions--logic--trickiness) |
| [ ] | Course Schedule (Cycle) — Given `numCourses` and a list of `prerequisites [a, b]` meaning "to take course `a`, you must first take course `b`", return `true` if it is possible to finish all courses (LC 207) | Medium | DFS 3-Color / Kahn's | [graphs.md](../01-data-structures/graphs.md#interview-questions--logic--trickiness) |
| [ ] | Course Schedule II — Same setup as Course Schedule, but return one valid ordering of courses to take. Return an empty list if impossible (LC 210) | Medium | Topological Sort | [graphs.md](../01-data-structures/graphs.md#interview-questions--logic--trickiness) |
| [ ] | Word Ladder — Given `beginWord`, `endWord`, and a word list, return the length of the shortest transformation sequence from `beginWord` to `endWord` where each step changes exactly one letter and each intermediate word must exist in the word list. Return 0 if no sequence exists | Hard | BFS Word Mutations | [graphs.md](../01-data-structures/graphs.md#interview-questions--logic--trickiness) |
| [ ] | Alien Dictionary — Given a list of words from an alien dictionary sorted in alien lexicographic order, derive the order of letters in the alien alphabet. Return any valid order, or `""` if the ordering is invalid (contains a cycle or a word is a prefix-violated neighbor) | Hard | Topological Sort | [graphs.md](../01-data-structures/graphs.md#interview-questions--logic--trickiness) |
| [ ] | Network Delay Time — A directed weighted graph of `n` nodes; given signal source `k`, find the time for all nodes to receive the signal. Return `-1` if unreachable | Medium | Dijkstra algorithm | [graph.md](../02-algorithms/graph.md#interview-questions--logic--trickiness) |
| [ ] | Swim in Rising Water — Grid where `grid[i][j]` is the elevation. Rain rises uniformly — at time `t` you can swim from any cell with elevation ≤ `t` to an adjacent one. Find minimum `t` to reach bottom-right from top-left | Hard | Dijkstra / BS + BFS | [graph.md](../02-algorithms/graph.md#interview-questions--logic--trickiness) |
| [ ] | Is Graph Bipartite? — Given an undirected graph, determine if it can be split into two sets such that every edge connects nodes from different sets (2-colorable) | Medium | 2-Coloring DFS/BFS | [graphs.md](../01-data-structures/graphs.md#interview-questions--logic--trickiness) |
| [ ] | Cheapest Flights within K Stops — Given `n` cities, a list of flights `[from, to, price]`, and integers `src`, `dst`, `k`, return the cheapest price from `src` to `dst` with at most `k` stops. Return -1 if impossible | Medium | Bellman-Ford / Dijkstra | [graph.md](../02-algorithms/graph.md#interview-questions--logic--trickiness) |
| [ ] | Critical Connections (Bridges) — Find all bridges in an undirected graph | Hard | Tarjan's Bridge DFS | [graph.md](../02-algorithms/graph.md#interview-questions--logic--trickiness) |
| [ ] | Reconstruct Itinerary — Given a list of airline tickets `[from, to]`, reconstruct the itinerary starting from "JFK" using all tickets exactly once. If multiple valid itineraries exist, return the lexicographically smallest one | Hard | Hierholzer's Eulerian Path | [graph.md](../02-algorithms/graph.md#interview-questions--logic--trickiness) |
| [ ] | Min Cost to Connect All Points — 2D points. Connect all with minimum total Manhattan distance (any pair can be connected directly) | Medium | Kruskal's / Prim's MST | [graph.md](../02-algorithms/graph.md#interview-questions--logic--trickiness) |
| [ ] | Find Eventual Safe States — In a directed graph, a node is "safe" if every path from it eventually terminates (no cycle reachable). Return all safe nodes sorted | Medium | Reverse DFS / Topological | [graph.md](../02-algorithms/graph.md#interview-questions--logic--trickiness) |
| [ ] | Minimum Number of Vertices to Reach All Nodes — Given a DAG with n nodes, find the minimum set of vertices from which all nodes are reachable | Medium | Zero in-degree nodes | [graph.md](../02-algorithms/graph.md#interview-questions--logic--trickiness) |

---

## 7. Disjoint Set Union (DSU)

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Number of Connected Components — `n` nodes, list of undirected edges. Return number of connected components | Medium | DSU Component count | [union-find.md](../02-algorithms/union-find.md#interview-questions--logic--trickiness) |
| [ ] | Graph Valid Tree — `n` nodes, list of undirected edges. Determine if the graph forms a valid tree | Medium | DSU Cycle checking | [union-find.md](../02-algorithms/union-find.md#interview-questions--logic--trickiness) |
| [ ] | Redundant Connection — Given a tree of n nodes with one extra edge added (creating exactly one cycle), find the redundant edge. If multiple valid answers, return the last one in the input | Medium | Union-Find Cycles | [union-find.md](../02-algorithms/union-find.md#interview-questions--logic--trickiness) |
| [ ] | Redundant Connection II — Directed graph built from a tree by adding exactly one extra directed edge. Return the redundant edge. Each node has in-degree ≤ 2. If multiple answers, return the one appearing last | Hard | Directed DSU Parents | [union-find.md](../02-algorithms/union-find.md#interview-questions--logic--trickiness) |
| [ ] | Accounts Merge — List of accounts `[name, email1, email2, ...]`. Merge accounts sharing at least one email. Return sorted merged accounts | Medium | Union email components | [union-find.md](../02-algorithms/union-find.md#interview-questions--logic--trickiness) |

---

## 8. Segment Tree & Fenwick Tree

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Range Sum Query - Mutable — Given an array of integers, support two operations: (1) update a single element, (2) query the sum over a range `[l, r]`. LeetCode 307 | Medium | Segment / Fenwick Tree | [segment-tree.md](../01-data-structures/segment-tree.md#interview-questions--logic--trickiness) |
| [ ] | Range Sum Query 2D - Mutable — Design a data structure for a 2D matrix that supports point updates and rectangular range sum queries | Hard | 2D Segment / Fenwick | [segment-tree.md](../01-data-structures/segment-tree.md#interview-questions--logic--trickiness) |
| [ ] | Count of Smaller Numbers After Self — For each element `nums[i]`, count how many elements to its right are strictly smaller. LeetCode 315 | Hard | Fenwick Inversion Sums | [segment-tree.md](../01-data-structures/segment-tree.md#interview-questions--logic--trickiness) |

---

## 9. Heaps & Priority Queues

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Kth Largest Element — Find kth largest element in array | Medium | Min-Heap size K | [heap.md](../01-data-structures/heap.md#interview-questions--logic--trickiness) |
| [ ] | Top K Frequent Elements — Given an integer array `nums` and integer `k`, return the `k` most frequent elements. Order of output does not matter | Medium | Heap / Bucket Sort | [heap.md](../01-data-structures/heap.md#interview-questions--logic--trickiness) |
| [ ] | Find Median from Data Stream — Design a data structure supporting `add_num(num)` and `find_median()` on a dynamic stream | Hard | Min & Max Heaps | [heap.md](../01-data-structures/heap.md#interview-questions--logic--trickiness) |
| [ ] | Task Scheduler — Given tasks (letters) and a cooldown `n`, find the minimum time to finish all tasks. Same task must have at least `n` intervals gap | Medium | Greedy Max frequency | [heap.md](../01-data-structures/heap.md#interview-questions--logic--trickiness) |
| [ ] | Merge K Sorted Lists — Merge `k` sorted linked lists into one sorted linked list | Hard | Heap K-way traversal | [heap.md](../01-data-structures/heap.md#interview-questions--logic--trickiness) |
| [ ] | K Closest Points to Origin — Given `n` points, return the `k` closest to the origin `(0, 0)` (Euclidean distance) | Medium | Max-Heap size K | [heap.md](../01-data-structures/heap.md#interview-questions--logic--trickiness) |

---

## 10. Backtracking

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Subsets — Given distinct integers, return all subsets (the power set) | Medium | Power Set Choose/Skip | [backtracking.md](../02-algorithms/backtracking.md#interview-questions--logic--trickiness) |
| [ ] | Subsets II — Input may contain duplicates; return only unique subsets | Medium | Sorted deduplication DFS | [backtracking.md](../02-algorithms/backtracking.md#interview-questions--logic--trickiness) |
| [ ] | Permutations — Given distinct integers, return all permutations | Medium | In-place element swap | [backtracking.md](../02-algorithms/backtracking.md#interview-questions--logic--trickiness) |
| [ ] | Permutations II — Input may contain duplicates; return only unique permutations | Medium | Sorted sibling dedupe | [backtracking.md](../02-algorithms/backtracking.md#interview-questions--logic--trickiness) |
| [ ] | Combination Sum — Given distinct candidates and a target, return all unique combinations (with repetition) summing to target | Medium | Node Reuse Backtracking | [backtracking.md](../02-algorithms/backtracking.md#interview-questions--logic--trickiness) |
| [ ] | Combination Sum II — Candidates may contain duplicates; each used at most once. Return unique combinations summing to target | Medium | Sorted Single-use DFS | [backtracking.md](../02-algorithms/backtracking.md#interview-questions--logic--trickiness) |
| [ ] | Word Search — Given a 2D board and a word, determine if the word exists as a path of adjacent non-revisiting cells | Medium | Grid Backtracking | [backtracking.md](../02-algorithms/backtracking.md#interview-questions--logic--trickiness) |
| [ ] | N-Queens — Place n queens on an n×n board so no two queens attack each other. Return all valid configurations | Hard | Diagonals tracking | [backtracking.md](../02-algorithms/backtracking.md#interview-questions--logic--trickiness) |
| [ ] | Palindrome Partitioning — Partition string s such that every substring is a palindrome. Return all valid partitioning schemes | Medium | Precomputed string splits | [backtracking.md](../02-algorithms/backtracking.md#interview-questions--logic--trickiness) |
| [ ] | Word Search II — Given a board of characters and a list of words, return all words that appear on the board. A word is valid if it can be traced through adjacent (4-directional) cells without reusing any cell within the same word | Hard | Trie-based Grid DFS | [trie.md](../01-data-structures/trie.md#interview-questions--logic--trickiness) |
| [ ] | Letter Combinations of a Phone Number — Given a string of digits (2-9), return all possible letter combinations a phone keypad would produce | Medium | DFS with digit-to-char map | [backtracking.md](../02-algorithms/backtracking.md#interview-questions--logic--trickiness) |
| [ ] | Generate Parentheses — Generate all combinations of n pairs of well-formed parentheses | Medium | DFS open/close balance | [backtracking.md](../02-algorithms/backtracking.md#interview-questions--logic--trickiness) |

---

## 11. Dynamic Programming

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Climbing Stairs — Count distinct ways to climb n stairs, taking 1 or 2 steps at a time | Easy | 1D DP / Fibonacci | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |
| [ ] | House Robber — Rob houses along a street; no two adjacent houses. Maximize money | Medium | Binary State Machine | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |
| [ ] | House Robber II — Houses in a circle — first and last are adjacent | Medium | Circular State Splitting | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |
| [ ] | Longest Palindromic Subsequence — Length of longest palindromic subsequence in string `s` | Medium | 2D Interval DP | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |
| [ ] | Longest Common Subsequence — Length of longest common subsequence (non-contiguous) of two strings | Medium | 2D Grid DP | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |
| [ ] | Edit Distance — Minimum insert/delete/replace operations to convert `word1` to `word2` | Hard | 2D Transformation DP | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |
| [ ] | Coin Change — Minimum coins from unlimited denominations to make amount `A`. Return -1 if impossible | Medium | Unbounded Knapsack | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |
| [ ] | Coin Change II — Count combinations (not permutations) of coins summing to `amount` | Medium | Combinations Knapsack | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |
| [ ] | 0-1 Knapsack — Solve the standard interview variant of 0-1 Knapsack. | Medium | 2D Capacity DP | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |
| [ ] | Partition Equal Subset Sum — Can `nums` be split into two subsets with equal sum? | Medium | 0-1 Capacity Match | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |
| [ ] | Word Break — Given string s and a word dictionary, return true if s can be segmented into dictionary words | Medium | Splitting DP | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |
| [ ] | Unique Paths — Count distinct paths from top-left to bottom-right of m×n grid, moving only right or down | Medium | Grid movement DP | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |
| [ ] | Longest Increasing Subsequence — Given an integer array `nums`, return the length of the longest strictly increasing subsequence | Medium | DP / Patience Sort | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |
| [ ] | Burst Balloons — `n` balloons with values. Bursting balloon `i` scores `nums[i-1]*nums[i]*nums[i+1]`. Maximize total coins | Hard | Interval split DP | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |
| [ ] | Regular Expression Matching — Given string `s` and pattern `p` with `'.'` (any single char) and `'*'` (zero or more of preceding element), implement full regex matching. Must match the entire string | Hard | 2D regex State transitions | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |
| [ ] | Wildcard Matching — Given string `s` and pattern `p` with `'?'` (any single char) and `'*'` (any sequence including empty), return True if `p` matches `s` entirely | Hard | 2D wildcard State match | [string.md](../02-algorithms/string.md#interview-questions--logic--trickiness) |
| [ ] | Word Break II — Given a string `s` and a dictionary, return all ways to segment `s` into space-separated dictionary words | Hard | DP memoization + backtrack all paths | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |
| [ ] | Interleaving String — Given `s1`, `s2`, `s3`, return true if `s3` is formed by an interleaving of `s1` and `s2` (LC 97) | Medium | 2D DP take-from-either | [dynamic-programming/README.md](../02-algorithms/dynamic-programming/README.md#interview-questions--logic--trickiness) |

---

## 12. Greedy

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Gas Station — There are `n` gas stations in a circle. `gas[i]` is the gas available at station `i`; `cost[i]` is the cost to travel from `i` to `i+1`. Find the starting station index from which you can complete the full circle, or return −1 if impossible | Medium | Tank tracking circular | [greedy.md](../02-algorithms/greedy.md#interview-questions--logic--trickiness) |
| [ ] | Task Scheduler — Given tasks (letters) and a cooldown `n`, find the minimum time to finish all tasks. Same task must have at least `n` intervals gap | Medium | Maximum frequency math | [greedy.md](../02-algorithms/greedy.md#interview-questions--logic--trickiness) |
| [ ] | Candy — `n` children stand in a line. Each child has a rating. Each child must receive at least one candy. Children with a higher rating than their immediate neighbor must receive more candies. Return the minimum total candies | Hard | Two-pass distribution | [greedy.md](../02-algorithms/greedy.md#interview-questions--logic--trickiness) |
| [ ] | Non-overlapping Intervals — Find the minimum number of intervals to remove so that the rest are non-overlapping | Medium | End-time Sorting | [greedy.md](../02-algorithms/greedy.md#interview-questions--logic--trickiness) |

---

## 13. Intervals

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Merge Intervals — Given a list of intervals, merge all overlapping intervals and return the result | Medium | Sort by start, merge overlapping | [array.md](../01-data-structures/array.md#interview-questions--logic--trickiness) |
| [ ] | Insert Interval — Given a list of non-overlapping intervals sorted by start, insert a new interval (merging as needed) and return the result | Medium | Find overlap range, merge, reconstruct | [array.md](../01-data-structures/array.md#interview-questions--logic--trickiness) |
| [ ] | Meeting Rooms I — Solve the standard interview variant of Meeting Rooms I. | Easy | Sort + check adjacent overlap | [greedy.md](../02-algorithms/greedy.md#interview-questions--logic--trickiness) |
| [ ] | Meeting Rooms II — Given intervals [start, end], find the minimum number of conference rooms required | Medium | Min-Heap end times / sweep line | [heap.md](../01-data-structures/heap.md#interview-questions--logic--trickiness) |
| [ ] | Minimum Interval to Include Each Query — Solve the standard interview variant of Minimum Interval to Include Each Query. | Hard | Sort + min-heap by length | [heap.md](../01-data-structures/heap.md#interview-questions--logic--trickiness) |

---

## 14. Tries

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Implement Trie — Implement a Trie with `insert(word)`, `search(word)` (returns true only if the exact word was inserted), and `startsWith(prefix)` (returns true if any inserted word begins with `prefix`) | Medium | Insert/search/startsWith node walk | [trie.md](../01-data-structures/trie.md#interview-questions--logic--trickiness) |
| [ ] | Design Add and Search Words — Solve the standard interview variant of Design Add and Search Words. | Medium | Trie + DFS wildcard '.' | [trie.md](../01-data-structures/trie.md#interview-questions--logic--trickiness) |
| [ ] | Replace Words — Given a dictionary of root words and a sentence, replace each word in the sentence with its shortest matching root. If a word has multiple roots, use the shortest one | Medium | Trie prefix replacement | [trie.md](../01-data-structures/trie.md#interview-questions--logic--trickiness) |

---

## 15. Matrix / Grid BFS

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Rotten Oranges — Grid of `0` (empty), `1` (fresh), `2` (rotten). Each minute every rotten orange infects its 4-directional fresh neighbors. Return time until no fresh orange remains, or -1 if impossible | Medium | Multi-source BFS with time tracking | [graphs.md](../01-data-structures/graphs.md#interview-questions--logic--trickiness) |
| [ ] | 01 Matrix (Distance to Nearest 0) — Given a binary matrix, for each cell return its distance to the nearest `0`. Distance is the count of steps (4-directional) | Medium | Multi-source BFS from all 0s | [graphs.md](../01-data-structures/graphs.md#interview-questions--logic--trickiness) |
| [ ] | Surrounded Regions — Given an m×n board of 'X' and 'O', flip all 'O' regions completely surrounded by 'X' to 'X'. 'O's connected to the border are never flipped | Medium | BFS/DFS from border, flip interior | [graphs.md](../01-data-structures/graphs.md#interview-questions--logic--trickiness) |
| [ ] | Set Matrix Zeroes — If a cell is zero, set its entire row and column to zero. Do it in-place | Medium | In-place sentinel / row+col flags | [array.md](../01-data-structures/array.md#interview-questions--logic--trickiness) |
| [ ] | Spiral Matrix — Return all elements of an m×n matrix in spiral order | Medium | Layer-by-layer boundary shrink | [array.md](../01-data-structures/array.md#interview-questions--logic--trickiness) |

---

## 16. Binary Search

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Search in Rotated Sorted Array — Given a sorted array rotated at some pivot, search for a target. Return its index, or -1 if not found | Medium | Rotated interval matching | [searching.md](../02-algorithms/searching.md#interview-questions--logic--trickiness) |
| [ ] | Koko Eating Bananas — `piles` of bananas. Eat at constant speed `k` bananas/hour, one pile at a time. Must finish all piles in `h` hours. Minimize `k` | Medium | Binary search on Answer | [searching.md](../02-algorithms/searching.md#interview-questions--logic--trickiness) |
| [ ] | Split Array Largest Sum — Split `nums` into exactly `k` non-empty contiguous subarrays. Minimize the largest subarray sum | Hard | BS on Subarray Capacity | [searching.md](../02-algorithms/searching.md#interview-questions--logic--trickiness) |
| [ ] | Time-Based Key-Value Store — Solve the standard interview variant of Time-Based Key-Value Store. | Medium | BS on sorted timestamps | [searching.md](../02-algorithms/searching.md#interview-questions--logic--trickiness) |
| [ ] | Median of Two Sorted Arrays — Find the median of two sorted arrays in O(log(m+n)) time | Hard | BS on partition sizes | [searching.md](../02-algorithms/searching.md#interview-questions--logic--trickiness) |
| [ ] | Search a 2D Matrix — Given an m×n matrix where each row is sorted and the first element of each row is greater than the last element of the previous row, search for a target value in O(log(m×n)) | Medium | Matrix coordinate map BS | [searching.md](../02-algorithms/searching.md#interview-questions--logic--trickiness) |
| [ ] | Find Minimum in Rotated Array — Find the minimum element in a rotated sorted array with no duplicates | Medium | BS bound checking | [searching.md](../02-algorithms/searching.md#interview-questions--logic--trickiness) |

---

## 17. Bit Manipulation

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Single Number — Every element in `nums` appears exactly twice except one. Find that one element. O(N) time, O(1) space | Easy | XOR Properties | [bit-manipulation.md](../02-algorithms/bit-manipulation.md#interview-questions--logic--trickiness) |
| [ ] | Single Number II — Every element appears exactly three times except one (appears once). Find it. O(N) time, O(1) space | Medium | Modulo Bit Counting | [bit-manipulation.md](../02-algorithms/bit-manipulation.md#interview-questions--logic--trickiness) |
| [ ] | Counting Bits — For every number `i` in `[0, n]`, return `dp[i]` = number of 1-bits in `i`. O(N) time, O(N) space | Easy | Bitwise shift DP | [bit-manipulation.md](../02-algorithms/bit-manipulation.md#interview-questions--logic--trickiness) |
| [ ] | Sum of Two Integers — Solve the standard interview variant of Sum of Two Integers. | Medium | Bit adder emulation | [bit-manipulation.md](../02-algorithms/bit-manipulation.md#interview-questions--logic--trickiness) |
| [ ] | Number of 1 Bits (Hamming Weight) — Return the number of set bits (1-bits) in a 32-bit unsigned integer | Easy | n & (n-1) loop | [bit-manipulation.md](../02-algorithms/bit-manipulation.md#interview-questions--logic--trickiness) |
| [ ] | Reverse Bits — Reverse the bits of a 32-bit unsigned integer | Easy | Bit-by-bit shift and OR | [bit-manipulation.md](../02-algorithms/bit-manipulation.md#interview-questions--logic--trickiness) |
| [ ] | Missing Number — Array `nums` contains `n` distinct numbers in range `[0, n]`. Find the missing number | Easy | XOR or Gauss sum | [bit-manipulation.md](../02-algorithms/bit-manipulation.md#interview-questions--logic--trickiness) |

---

## 18. Math & Number Theory

| Status | Question | Difficulty | Pattern | Link to Explanation |
| :---: | :--- | :---: | :--- | :--- |
| [ ] | Happy Number — Determine if a number `n` is "happy": repeatedly replace it with the sum of the squares of its digits. If the process eventually reaches 1, it is happy. Otherwise it loops forever | Easy | Floyd's cycle checking | [maths.md](../02-algorithms/maths.md#interview-questions--logic--trickiness) |
| [ ] | Pow(x, n) — Compute `x^n` efficiently; handle negative exponents | Medium | Binary exponentiation | [maths.md](../02-algorithms/maths.md#interview-questions--logic--trickiness) |
| [ ] | Sieve of Eratosthenes — Count the number of prime numbers strictly less than n | Easy | Composite prime marking | [maths.md](../02-algorithms/maths.md#interview-questions--logic--trickiness) |
| [ ] | Greatest Common Divisor of Strings — Largest string `t` that divides both strings `s1` and `s2` (i.e., concatenating copies of `t` produces each string) | Easy | Euclidean GCD reduction | [maths.md](../02-algorithms/maths.md#interview-questions--logic--trickiness) |
