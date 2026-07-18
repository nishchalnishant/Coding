---
module: root
topic: Questions
subtopic: 
status: unread
tags: [root, questions]
---
# Data Structures and Algorithms Questions

> [!note] L3 Reference Document
> This file is a **reference / meta document** — read it once, then use it as a lookup.
> It is NOT a coding practice file. Do not deep-study it like a topic file.


This file contains a comprehensive list of all questions covered in the `01-data-structures` and `02-algorithms` sections, grouped by topic.

## Data Structures

### Array

- [x] [Two Sum `⚡ T1`](coding/data-structures/02-hashing.md#two-sum) — Given an integer array `nums` and target, return indices of two numbers that sum to `target`. Exactly one solution exists [E]
- [x] [3Sum `⚡ T1`](coding/data-structures/01-array.md#3sum) — Find all unique triplets `[a, b, c]` in `nums` with `a + b + c = 0`. No duplicate triplets [M]
- [ ] [Trapping Rain Water `⚡ T1`](coding/algorithms/03-two-pointers.md#trapping-rain-water-lc-42) — Given an elevation map, compute how much water it can trap after raining [H]
- [ ] [Container with Most Water `⚡ T1`](coding/data-structures/01-array.md#container-with-most-water) — Given heights of vertical lines, find the two lines that form a container holding the maximum water [M]
- [ ] [Jump Game II `🎯 T2`](coding/data-structures/01-array.md#jump-game-ii) — Given an array where `nums[i]` is the max jump from index `i`, return the minimum number of jumps to reach the last index. Always reachable [M]
- [ ] [Sliding Window Maximum `⚡ T1`](coding/data-structures/06-queue.md#sliding-window-maximum) — Return the maximum in each sliding window of size `k` [H]
- [ ] [Jump Game `🎯 T2`](coding/data-structures/01-array.md#jump-game-lc-55) — Given an array where `nums[i]` is the max jump length from index `i`, determine if you can reach the last index [M]
- [ ] [Best Time to Buy and Sell Stock `⚡ T1`](coding/data-structures/01-array.md#best-time-to-buy-and-sell-stock) — Given an array `prices` where `prices[i]` is the price of a stock on day `i`, find the maximum profit from a single buy-sell transaction. You cannot sell before buying [E]
- [ ] [Maximum Subarray `⚡ T1`](coding/data-structures/01-array.md#maximum-subarray) — Find the contiguous subarray with the largest sum. Return the sum [M]
- [ ] [Find the Duplicate Number `🎯 T2`](coding/data-structures/01-array.md#find-the-duplicate-number) — Given an array of n+1 integers where each integer is in [1, n], find the one duplicate without modifying the array and using O(1) extra space [M]
- [ ] [Spiral Matrix `🎯 T2`](coding/data-structures/01-array.md#spiral-matrix) — Return all elements of an m×n matrix in spiral order [M]
- [ ] [Set Matrix Zeroes `🎯 T2`](coding/data-structures/01-array.md#set-matrix-zeroes) — If a cell is zero, set its entire row and column to zero. Do it in-place [M]
- [ ] [Longest Consecutive Sequence `🎯 T2`](coding/data-structures/01-array.md#longest-consecutive-sequence) — Find the length of the longest consecutive elements sequence in an unsorted array. O(n) required [H]
- [ ] [Minimum Window Substring `⚡ T1`](coding/data-structures/01-array.md#minimum-window-substring) — Find the smallest substring of `s` containing all characters of `t` (with multiplicity) [H]
- [ ] [Two Sum II (sorted) `⚡ T1`](coding/data-structures/02-hashing.md#two-sum) — Find two numbers that add to a target and return their indices. [M]
- [ ] [Permutation in String `🎯 T2`](coding/algorithms/04-sliding-window.md#permutation-in-string-lc-567) — Given strings `s1` and `s2`, return True if any permutation of `s1` is a substring of `s2`. LeetCode 567 [M]

### Graphs

- [ ] [Number of Islands `⚡ T1`](coding/data-structures/13-graph.md#number-of-islands) — Given a 2D grid of '1' (land) and '0' (water), count the number of islands (connected components of land, 4-directional) [M]
- [ ] [Rotting Oranges `🎯 T2`](coding/data-structures/13-graph.md#rotting-oranges) — Grid of `0` (empty), `1` (fresh), `2` (rotten). Each minute every rotten orange infects its 4-directional fresh neighbors. Return time until no fresh orange remains, or -1 if impossible [M]
- [ ] [Course Schedule `⚡ T1`](coding/data-structures/13-graph.md#course-schedule) — Given `numCourses` and a list of `prerequisites [a, b]` meaning "to take course `a`, you must first take course `b`", return `true` if it is possible to finish all courses (LC 207) [M]
- [ ] [Clone Graph `⚡ T1`](coding/data-structures/13-graph.md#clone-graph) — Given a reference to a node in an undirected connected graph, return a deep copy [M]
- [ ] [Surrounded Regions `🎯 T2`](coding/data-structures/13-graph.md#surrounded-regions) — Given an m×n board of 'X' and 'O', flip all 'O' regions completely surrounded by 'X' to 'X'. 'O's connected to the border are never flipped [M]
- [ ] [Word Ladder `⚡ T1`](coding/data-structures/13-graph.md#word-ladder) — Given `beginWord`, `endWord`, and a word list, return the length of the shortest transformation sequence from `beginWord` to `endWord` where each step changes exactly one letter and each intermediate word must exist in the word list. Return 0 if no sequence exists [H]
- [ ] [Alien Dictionary `⚡ T1`](coding/data-structures/13-graph.md#alien-dictionary) — Given a list of words from an alien dictionary sorted in alien lexicographic order, derive the order of letters in the alien alphabet. Return any valid order, or `""` if the ordering is invalid (contains a cycle or a word is a prefix-violated neighbor) [H]
- [ ] [Max Area of Island `🎯 T2`](coding/data-structures/13-graph.md#max-area-of-island) — Given a binary 2D grid (0=water, 1=land), return the maximum area of any island (connected 1s, 4-directional). Return 0 if no island [M]
- [ ] [Redundant Connection `⚡ T1`](coding/data-structures/13-graph.md#redundant-connection) — Given a tree of n nodes with one extra edge added (creating exactly one cycle), find the redundant edge. If multiple valid answers, return the last one in the input [M]

### Hashing

- [ ] [Group Anagrams `🎯 T2`](coding/data-structures/03-string.md#group-anagrams) — Group strings that are anagrams of each other [M]
- [ ] [Longest Consecutive `🎯 T2`](coding/data-structures/01-array.md#longest-consecutive-sequence) — Solve the standard interview variant of Longest Consecutive. [H]
- [ ] [LRU Cache `⚡ T1`](coding/data-structures/07-linked-list.md#lru-cache) — Design a cache with O(1) `get` and `put` operations, evicting the Least Recently Used item when capacity is exceeded [M]
- [ ] [Minimum Window `⚡ T1`](coding/data-structures/01-array.md#minimum-window-substring) — Solve the standard interview variant of Minimum Window. [H]
- [ ] [Insert Delete GetRandom `⚡ T1`](coding/data-structures/02-hashing.md#insert-delete-getrandom-o1) — Solve the standard interview variant of Insert Delete GetRandom. [M]
- [ ] [Two Sum `⚡ T1`](coding/data-structures/02-hashing.md#two-sum) — Given an integer array `nums` and target, return indices of two numbers that sum to `target`. Exactly one solution exists [E]
- [ ] [Valid Anagram `🎯 T2`](coding/data-structures/03-string.md#valid-anagram) — Return true if `t` is an anagram of `s` (same characters, same counts) [E]
- [ ] [Subarray Sum Equals K `⚡ T1`](coding/data-structures/01-array.md#subarray-sum-equals-k) — Count the number of contiguous subarrays with sum equal to `k`. Array may contain negatives [M]
- [ ] [Longest Increasing Subsequence (via hash) `🎯 T2`](coding/algorithms/15-dynamic-programming.md#longest-increasing-subsequence) — Given an integer array `nums`, return the length of the longest strictly increasing subsequence [M]

### Heap

- [ ] [Merge K Sorted Lists `⚡ T1`](coding/data-structures/07-linked-list.md#merge-k-sorted-lists) — Merge `k` sorted linked lists into one sorted linked list [H]
- [ ] Kth Largest Element `🎯 T2` — Find kth largest element in array [M]
- [ ] [Top K Frequent `⚡ T1`](coding/data-structures/10-heap.md#top-k-frequent-elements) — Return the k most frequent elements or words. [M]
- [ ] [K Closest Points `⚡ T1`](coding/data-structures/10-heap.md#k-closest-points-to-origin) — Return the points closest to the origin. [M]
- [ ] [Task Scheduler `⚡ T1`](coding/data-structures/06-queue.md#task-scheduler) — Given tasks (letters) and a cooldown `n`, find the minimum time to finish all tasks. Same task must have at least `n` intervals gap [M]
- [ ] [Last Stone Weight `🎯 T2`](coding/data-structures/10-heap.md#last-stone-weight) — Each turn smash the two heaviest stones. If equal, both destroyed; otherwise the difference survives. Return the weight of the last stone (or 0) [E]
- [ ] [K Closest Points to Origin `⚡ T1`](coding/data-structures/10-heap.md#k-closest-points-to-origin) — Given `n` points, return the `k` closest to the origin `(0, 0)` (Euclidean distance) [M]
- [ ] [Meeting Rooms II `⚡ T1`](coding/algorithms/16-greedy.md#meeting-rooms-ii) — Given intervals [start, end], find the minimum number of conference rooms required [M]
- [ ] [Trapping Rain Water II `⚡ T1`](coding/algorithms/03-two-pointers.md#trapping-rain-water-lc-42) — Compute how much water is trapped between bars. [H]

### Linked List

- [ ] [LRU Cache `⚡ T1`](coding/data-structures/07-linked-list.md#lru-cache) — Design a cache with O(1) `get` and `put` operations, evicting the Least Recently Used item when capacity is exceeded [M]
- [ ] [Copy List with Random Pointer `🎯 T2`](coding/data-structures/07-linked-list.md#copy-list-with-random-pointer) — Deep copy a linked list where each node has `next` and `random` pointers. `random` may point to any node or null [M]
- [ ] [Add Two Numbers `🎯 T2`](coding/data-structures/07-linked-list.md#add-two-numbers) — Two non-empty linked lists represent non-negative integers in reverse order (each node = one digit). Return the sum as a linked list in reverse order [M]
- [ ] [Linked List Cycle `🎯 T2`](coding/data-structures/07-linked-list.md#linked-list-cycle) — Detect if a linked list has a cycle [E]
- [ ] [Merge Two Sorted Lists `🎯 T2`](coding/data-structures/07-linked-list.md#merge-two-sorted-lists) — Merge two sorted linked lists into one sorted list. Return the head of the merged list [E]
- [ ] Reorder List `🎯 T2` — Reorder list in-place: `L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → ...` [M]
- [ ] [Merge K Sorted Lists `⚡ T1`](coding/data-structures/07-linked-list.md#merge-k-sorted-lists) — Merge `k` sorted linked lists into one sorted linked list [H]

### Queue

- [ ] [Word Ladder `⚡ T1`](coding/data-structures/13-graph.md#word-ladder) — Given `beginWord`, `endWord`, and a word list, return the length of the shortest transformation sequence from `beginWord` to `endWord` where each step changes exactly one letter and each intermediate word must exist in the word list. Return 0 if no sequence exists [H]
- [ ] [Sliding Window Maximum `⚡ T1`](coding/data-structures/06-queue.md#sliding-window-maximum) — Return the maximum in each sliding window of size `k` [H]
- [ ] [Jump Game III `🎯 T2`](coding/data-structures/06-queue.md#jump-game-iii) — Given array `arr` and start index `start`, at each index `i` you can jump to `i + arr[i]` or `i - arr[i]`. Return true if you can reach any index with value 0 [M]
- [ ] [Walls and Gates `🎯 T2`](coding/data-structures/13-graph.md#walls-and-gates-lc-286) — Grid with `-1` (wall), `0` (gate), `INF` (empty room). Fill each empty room with its distance to the nearest gate. Modify in place [M]



### Stack

- [ ] [Daily Temperatures `🎯 T2`](coding/data-structures/05-stack.md#daily-temperatures) — Given a list of daily temperatures, return an array where `result[i]` is the number of days until a warmer temperature. If no warmer day exists, `result[i] = 0` [M]
- [ ] [Largest Rectangle `🎯 T2`](coding/data-structures/05-stack.md#largest-rectangle-in-histogram) — Find the maximum rectangle area formed by histogram bars. [H]
- [ ] [Valid Parentheses `⚡ T1`](coding/data-structures/05-stack.md#valid-parentheses) — Given a string of `()[]{}`, determine if the brackets are valid (properly nested and matched) [E]
- [ ] [Min Stack `🎯 T2`](coding/data-structures/05-stack.md#min-stack) — Design a stack with O(1) `push`, `pop`, `top`, and `get_min` [M]
- [ ] [Trapping Rain Water `⚡ T1`](coding/algorithms/03-two-pointers.md#trapping-rain-water-lc-42) — Given an elevation map, compute how much water it can trap after raining [H]
- [ ] [Largest Rectangle in Histogram `🎯 T2`](coding/data-structures/05-stack.md#largest-rectangle-in-histogram) — Given heights of bars in a histogram, find the area of the largest rectangle that fits within the histogram [H]

### Tree

- [ ] Validate BST `🎯 T2` — Check if a binary tree satisfies BST ordering [M]
- [ ] [LCA `⚡ T1`](coding/data-structures/08-tree.md#lowest-common-ancestor) — Find LCA in a general binary tree (alias) [M]
- [ ] [Kth Smallest `🎯 T2`](01-data-structures/08-tree.md#bst-operations-validate-kth-smallest-range-sum) — Return the kth smallest value in a BST. [M]
- [ ] Diameter `⚡ T1` — Solve the standard interview variant of Diameter. [E]
- [ ] [House Robber III `🎯 T2`](coding/data-structures/08-tree.md#house-robber-iii) — Houses are arranged in a binary tree. Adjacent nodes (parent-child) cannot both be robbed. Maximize total money robbed [M]
- [ ] [Invert Binary Tree `🎯 T2`](coding/data-structures/08-tree.md#invert-binary-tree) — Given a binary tree root, mirror it — every left child becomes right and vice versa at every level [E]
- [ ] [Count Good Nodes `🎯 T2`](coding/data-structures/08-tree.md#count-good-nodes-in-binary-tree) — A node X is "good" if no node on the root-to-X path has a value greater than X.val. Count good nodes [M]
- [ ] [Construct Binary Tree from Preorder and Inorder `🎯 T2`](coding/data-structures/08-tree.md) — Given preorder and inorder traversal arrays, reconstruct the binary tree [M]
- [ ] [Binary Tree Maximum Path Sum `⚡ T1`](coding/data-structures/08-tree.md#binary-tree-maximum-path-sum) — Find the maximum path sum between any two nodes. Values can be negative; a path can start and end anywhere [H]
- [ ] [LCA BST `⚡ T1`](01-data-structures/08-tree.md#lca-bst) — Solve the standard interview variant of LCA BST. [M]

### Trie

- [ ] ----------
- [ ] [Implement Trie `⚡ T1`](coding/data-structures/09-trie.md#implement-trie-prefix-tree) — Implement a Trie with `insert(word)`, `search(word)` (returns true only if the exact word was inserted), and `startsWith(prefix)` (returns true if any inserted word begins with `prefix`) [E]
- [ ] [Word Search II `⚡ T1`](coding/data-structures/09-trie.md#word-search-ii) — Given a board of characters and a list of words, return all words that appear on the board. A word is valid if it can be traced through adjacent (4-directional) cells without reusing any cell within the same word [H]

## Algorithms

### Graph (additional)

- [ ] [Alien Dictionary `⚡ T1`](coding/data-structures/13-graph.md#alien-dictionary) — Given a list of words from an alien dictionary sorted in alien lexicographic order, derive the order of letters in the alien alphabet. Return any valid order, or `""` if the ordering is invalid (contains a cycle or a word is a prefix-violated neighbor) [H]
- [ ] [Course Schedule II `⚡ T1`](coding/data-structures/13-graph.md#course-schedule-ii) — Same setup as Course Schedule, but return one valid ordering of courses to take. Return an empty list if impossible (LC 210) [M]
- [ ] [Word Ladder II `⚡ T1`](coding/algorithms/13-graph-algorithms.md#word-ladder-ii-lc-126) — Same as Word Ladder, but return **all** shortest transformation sequences from `beginWord` to `endWord` [H]

### Backtracking

- [ ] Subsets `🎯 T2` — Given distinct integers, return all subsets (the power set) [M]
- [ ] [Permutations `🎯 T2`](coding/algorithms/09-recursion.md#permutations) — Given distinct integers, return all permutations [M]
- [ ] Combination Sum `🎯 T2` — Given distinct candidates and a target, return all unique combinations (with repetition) summing to target [M]
- [ ] [N-Queens `🎯 T2`](coding/algorithms/09-recursion.md#n-queens) — Place n queens on an n×n board so no two queens attack each other. Return all valid configurations [H]
- [ ] [Word Search `⚡ T1`](coding/algorithms/12-backtracking.md#word-search) — Given a 2D board and a word, determine if the word exists as a path of adjacent non-revisiting cells [M]
- [ ] [Palindrome Partitioning `🎯 T2`](coding/algorithms/09-recursion.md#palindrome-partitioning) — Partition string s such that every substring is a palindrome. Return all valid partitioning schemes [M]
- [ ] [Generate Parentheses `🎯 T2`](coding/algorithms/09-recursion.md#generate-parentheses) — Generate all combinations of n pairs of well-formed parentheses [M]
- [ ] Letter Combinations `🎯 T2` — Solve the standard interview variant of Letter Combinations. [M]
- [ ] [Combinations `🎯 T2`](coding/algorithms/09-recursion.md#combinations-lc-77) — Return all combinations of k numbers from the range [1, n] [M]
- [ ] [Target Sum `🎯 T2`](coding/algorithms/15-dynamic-programming.md#target-sum) — Given an integer array and a target, assign `+` or `-` to each element and count the number of ways to reach target [M]
- [ ] [Word Break II `🎯 T2`](coding/algorithms/12-backtracking.md#word-break-ii) — Given a string `s` and a dictionary, return all ways to segment `s` into space-separated dictionary words [M]
- [ ] [Unique Paths III `🎯 T2`](coding/algorithms/12-backtracking.md#unique-paths-iii) — Start at cell with value 1, reach cell with value 2, visiting every non-obstacle cell exactly once. Return count of such paths [H]
- [ ] [Combination Sum III `🎯 T2`](coding/algorithms/12-backtracking.md#combination-sum-iii) — Find all combinations of exactly k numbers from 1-9 that sum to target n. Each number used at most once, no duplicates in output [M]



### Graph

- [ ] [Course Schedule `⚡ T1`](coding/data-structures/13-graph.md#course-schedule) — Given `numCourses` and a list of `prerequisites [a, b]` meaning "to take course `a`, you must first take course `b`", return `true` if it is possible to finish all courses (LC 207) [M]
- [ ] [Word Ladder `⚡ T1`](coding/data-structures/13-graph.md#word-ladder) — Given `beginWord`, `endWord`, and a word list, return the length of the shortest transformation sequence from `beginWord` to `endWord` where each step changes exactly one letter and each intermediate word must exist in the word list. Return 0 if no sequence exists [H]
- [ ] [Alien Dictionary `⚡ T1`](coding/data-structures/13-graph.md#alien-dictionary) — Given a list of words from an alien dictionary sorted in alien lexicographic order, derive the order of letters in the alien alphabet. Return any valid order, or `""` if the ordering is invalid (contains a cycle or a word is a prefix-violated neighbor) [H]
- [ ] [Number of Islands `⚡ T1`](coding/data-structures/13-graph.md#number-of-islands) — Given a 2D grid of '1' (land) and '0' (water), count the number of islands (connected components of land, 4-directional) [M]
- [ ] [Clone Graph `⚡ T1`](coding/data-structures/13-graph.md#clone-graph) — Given a reference to a node in an undirected connected graph, return a deep copy [M]
- [ ] [Pacific Atlantic Water Flow `⚡ T1`](coding/data-structures/13-graph.md#pacific-atlantic-water-flow) — Given an m×n height matrix, water flows to 4-adjacent cells of equal or lesser height. Find all cells from which water can reach both the Pacific (top/left border) and Atlantic (bottom/right border) oceans [M]
- [ ] [Course Schedule II `⚡ T1`](coding/data-structures/13-graph.md#course-schedule-ii) — Same setup as Course Schedule, but return one valid ordering of courses to take. Return an empty list if impossible (LC 210) [M]

### Greedy

- [ ] [Jump Game I `🎯 T2`](coding/data-structures/01-array.md#jump-game-ii) — Determine whether the end of the array is reachable. [M]
- [ ] [Jump Game II `🎯 T2`](coding/data-structures/01-array.md#jump-game-ii) — Given an array where `nums[i]` is the max jump from index `i`, return the minimum number of jumps to reach the last index. Always reachable [M]
- [ ] [Gas Station `🎯 T2`](coding/data-structures/01-array.md#gas-station-lc-134) — There are `n` gas stations in a circle. `gas[i]` is the gas available at station `i`; `cost[i]` is the cost to travel from `i` to `i+1`. Find the starting station index from which you can complete the full circle, or return −1 if impossible [M]
- [ ] [Task Scheduler `⚡ T1`](coding/data-structures/06-queue.md#task-scheduler) — Given tasks (letters) and a cooldown `n`, find the minimum time to finish all tasks. Same task must have at least `n` intervals gap [M]
- [ ] [Partition Labels `🎯 T2`](coding/algorithms/16-greedy.md#partition-labels-lc-763) — Partition string s into as many parts as possible such that each letter appears in at most one part. Return list of partition sizes [M]

### Greedy

- [ ] [Merge Intervals `⚡ T1`](coding/data-structures/01-array.md#merge-intervals-lc-56) — Given a list of intervals, merge all overlapping intervals and return the result [M]
- [ ] [Meeting Rooms II `⚡ T1`](coding/algorithms/16-greedy.md#meeting-rooms-ii) — Given intervals [start, end], find the minimum number of conference rooms required [M]
- [ ] [LRU Cache `⚡ T1`](coding/data-structures/07-linked-list.md#lru-cache) — Design a cache with O(1) `get` and `put` operations, evicting the Least Recently Used item when capacity is exceeded [M]
- [ ] [Design Twitter `🎯 T2`](coding/data-structures/10-heap.md#design-twitter) — Design a simplified Twitter: `post_tweet(userId, tweetId)`, `get_news_feed(userId)` (10 most recent tweets from self + followees), `follow(followerId, followeeId)`, `unfollow` [M]
- [ ] [Find Median from Data Stream `⚡ T1`](coding/data-structures/06-queue.md#find-median-from-data-stream) — Design a data structure supporting `add_num(num)` and `find_median()` on a dynamic stream [H]

### Searching

- [ ] [Koko Eating Bananas `⚡ T1`](coding/algorithms/11-binary-search.md#koko-eating-bananas-lc-875) — `piles` of bananas. Eat at constant speed `k` bananas/hour, one pile at a time. Must finish all piles in `h` hours. Minimize `k` [M]
- [ ] [Search in Rotated Sorted Array II `⚡ T1`](coding/algorithms/11-binary-search.md#search-in-rotated-sorted-array-ii-lc-81) — Rotated sorted array *with duplicates*. Return True if target exists [M]
- [ ] [Find Minimum in Rotated Sorted Array II `⚡ T1`](coding/algorithms/11-binary-search.md#find-minimum-in-rotated-sorted-array-ii-lc-154) — Rotated sorted array with duplicates. Find the minimum [M]
- [ ] [Time Based Key-Value Store `🎯 T2`](02-algorithms/11-binary-search.md#time-based-key-value-store) — Solve the standard interview variant of Time Based Key-Value Store. [M]
- [ ] [Koko Eating Bananas `⚡ T1`](coding/algorithms/11-binary-search.md#koko-eating-bananas-lc-875) — `piles` of bananas. Eat at constant speed `k` bananas/hour, one pile at a time. Must finish all piles in `h` hours. Minimize `k` [M]
- [ ] [Capacity to Ship Packages Within D Days `⚡ T1`](coding/algorithms/11-binary-search.md#capacity-to-ship-packages-within-d-days-lc-1011) — Ship packages in order. Ship has fixed capacity per day. Minimize capacity to ship all within `days` days [M]
- [ ] [Search a 2D Matrix `🎯 T2`](coding/data-structures/01-array.md#search-a-2d-matrix-lc-74) — Given an m×n matrix where each row is sorted and the first element of each row is greater than the last element of the previous row, search for a target value in O(log(m×n)) [M]

### Sorting

- [ ] [Merge Intervals `⚡ T1`](coding/data-structures/01-array.md#merge-intervals-lc-56) — Given a list of intervals, merge all overlapping intervals and return the result [M]
- [ ] [Meeting Rooms II `⚡ T1`](coding/algorithms/16-greedy.md#meeting-rooms-ii) — Given intervals [start, end], find the minimum number of conference rooms required [M]
- [ ] [3Sum Closest `⚡ T1`](coding/data-structures/01-array.md#3sum-closest) — Find the triplet whose sum is closest to a given target. Return the sum [M]

### String

- [ ] [Longest Palindromic Substring `⚡ T1`](coding/data-structures/03-string.md#longest-palindromic-substring) — Given string `s`, return the longest substring that is a palindrome [M]
- [ ] [Group Anagrams `🎯 T2`](coding/data-structures/03-string.md#group-anagrams) — Group strings that are anagrams of each other [M]
- [ ] [Valid Parenthesis String `🎯 T2`](01-data-structures/03-string.md#valid-parenthesis-string) — Solve the standard interview variant of Valid Parenthesis String. [M]
- [ ] [Edit Distance `🎯 T2`](coding/algorithms/15-dynamic-programming.md#edit-distance) — Minimum insert/delete/replace operations to convert `word1` to `word2` [H]
- [ ] [Valid Palindrome `🎯 T2`](coding/data-structures/03-string.md#valid-palindrome) — Given string `s`, return true if it is a palindrome considering only alphanumeric characters and ignoring case [E]
- [ ] [Longest Repeating Character Replacement `🎯 T2`](coding/data-structures/01-array.md#longest-repeating-character-replacement) — Given string `s` and integer `k`, find the length of the longest substring where you can replace at most `k` characters to make all characters in the window the same [M]
- [ ] [Longest Substring Without Repeating Characters `⚡ T1`](coding/data-structures/03-string.md#longest-substring-without-repeating-characters) — Given string `s`, return the length of the longest substring with all unique characters [M]
- [ ] Palindromic Substrings `🎯 T2` — Given string `s`, return the total count of substrings that are palindromes (single characters count too) [M]
- [ ] [Word Search `⚡ T1`](coding/algorithms/12-backtracking.md#word-search) — Given a 2D board and a word, determine if the word exists as a path of adjacent non-revisiting cells [M]
- [ ] [Regular Expression Matching `🎯 T2`](coding/algorithms/15-dynamic-programming.md#regular-expression-matching) — Given string `s` and pattern `p` with `'.'` (any single char) and `'*'` (zero or more of preceding element), implement full regex matching. Must match the entire string [H]
- [ ] [Valid Palindrome II `🎯 T2`](coding/data-structures/03-string.md#valid-palindrome-ii-lc-680) — Given string `s`, return true if the string can become a palindrome by removing **at most one** character [E]
- [ ] [Encode and Decode Strings `🎯 T2`](coding/data-structures/03-string.md#encode-and-decode-strings) — Design functions `encode(strs)` and `decode(s)` to encode a list of strings into a single string and decode it back. The encoding must handle strings that contain any character including `#` and `/` [M]
- [ ] [Permutation in String `🎯 T2`](coding/algorithms/04-sliding-window.md#permutation-in-string-lc-567) — Given strings `s1` and `s2`, return True if any permutation of `s1` is a substring of `s2`. LeetCode 567 [M]

### Union Find

- [ ] [Redundant Connection `⚡ T1`](coding/data-structures/13-graph.md#redundant-connection) — Given a tree of n nodes with one extra edge added (creating exactly one cycle), find the redundant edge. If multiple valid answers, return the last one in the input [M]
- [ ] [Number of Islands II `⚡ T1`](coding/algorithms/14-union-find.md#number-of-islands-ii) — Initially empty `m×n` grid. Receive `addLand(r, c)` operations. After each, return island count [H]
- [ ] [Accounts Merge `⚡ T1`](coding/algorithms/14-union-find.md#accounts-merge) — List of accounts `[name, email1, email2, ...]`. Merge accounts sharing at least one email. Return sorted merged accounts [M]
- [ ] [Graph Valid Tree `🎯 T2`](coding/algorithms/14-union-find.md#graph-valid-tree) — `n` nodes, list of undirected edges. Determine if the graph forms a valid tree [M]
- [ ] [Number of Provinces `⚡ T1`](coding/data-structures/13-graph.md#number-of-provinces-lc-547) — Given an n×n adjacency matrix `isConnected`, return the number of provinces (connected components of cities) [E]

### Aditya Verma

- [ ] ----------
- [ ] Subsets `🎯 T2` — Given distinct integers, return all subsets (the power set) [E]
- [ ] [Subsets II `🎯 T2`](coding/algorithms/09-recursion.md#subsets-ii-lc-90) — Input may contain duplicates; return only unique subsets [M]
- [ ] [Permutations `🎯 T2`](coding/algorithms/09-recursion.md#permutations) — Given distinct integers, return all permutations [M]
- [ ] [Permutations II `🎯 T2`](coding/algorithms/09-recursion.md#permutations-ii-lc-47) — Input may contain duplicates; return only unique permutations [M]
- [ ] [Combinations `🎯 T2`](coding/algorithms/09-recursion.md#combinations-lc-77) — Return all combinations of k numbers from the range [1, n] [M]
- [ ] Combination Sum `🎯 T2` — Given distinct candidates and a target, return all unique combinations (with repetition) summing to target [M]
- [ ] Combination Sum II `🎯 T2` — Candidates may contain duplicates; each used at most once. Return unique combinations summing to target [M]
- [ ] [Generate Parentheses `🎯 T2`](coding/algorithms/09-recursion.md#generate-parentheses) — Generate all combinations of n pairs of well-formed parentheses [M]
- [ ] [Palindrome Partitioning `🎯 T2`](coding/algorithms/09-recursion.md#palindrome-partitioning) — Partition string s such that every substring is a palindrome. Return all valid partitioning schemes [M]
- [ ] [Word Search `⚡ T1`](coding/algorithms/12-backtracking.md#word-search) — Given a 2D board and a word, determine if the word exists as a path of adjacent non-revisiting cells [M]
- [ ] [N-Queens `🎯 T2`](coding/algorithms/09-recursion.md#n-queens) — Place n queens on an n×n board so no two queens attack each other. Return all valid configurations [H]
- [ ] Pow(x, n) `🎯 T2` — Compute `x^n` efficiently; handle negative exponents [M]
- [ ] [Decode Ways `🎯 T2`](coding/algorithms/15-dynamic-programming.md#decode-ways) — String of digits where A=1..Z=26. Count distinct decodings [M]
- [ ] [Word Break `🎯 T2`](coding/algorithms/15-dynamic-programming.md#word-break) — Given string s and a word dictionary, return true if s can be segmented into dictionary words [M]
- [ ] [Diameter of Binary Tree `⚡ T1`](coding/data-structures/08-tree.md#diameter-of-binary-tree) — Return the length of the longest path between any two nodes (measured in edges). The path need not pass through the root [M]
- [ ] [Lowest Common Ancestor `⚡ T1`](coding/data-structures/08-tree.md#lowest-common-ancestor) — Find LCA of two nodes in a BST and in a general binary tree [M]

### Dp Aditya Verma

- [ ] Subset Sum `🎯 T2` — Solve the standard interview variant of Subset Sum. [M]
- [ ] [Partition Equal Subset Sum `🎯 T2`](coding/algorithms/15-dynamic-programming.md#partition-equal-subset-sum) — Can `nums` be split into two subsets with equal sum? [M]
- [ ] [Target Sum (±) `🎯 T2`](coding/algorithms/15-dynamic-programming.md#target-sum) — Given an integer array and a target, assign `+` or `-` to each element and count the number of ways to reach target [M]
- [ ] Coin Change I `🎯 T2` — Optimize coin usage or count combinations for an amount. [M]
- [ ] Coin Change II `🎯 T2` — Count combinations (not permutations) of coins summing to `amount` [M]
- [ ] [Climbing Stairs `🎯 T2`](coding/algorithms/15-dynamic-programming.md#climbing-stairs) — Count distinct ways to climb n stairs, taking 1 or 2 steps at a time [E]
- [ ] [House Robber `🎯 T2`](coding/algorithms/15-dynamic-programming.md#house-robber) — Rob houses along a street; no two adjacent houses. Maximize money [M]
- [ ] [House Robber II `🎯 T2`](coding/algorithms/15-dynamic-programming.md#house-robber) — Houses in a circle — first and last are adjacent [M]
- [ ] [Decode Ways `🎯 T2`](coding/algorithms/15-dynamic-programming.md#decode-ways) — String of digits where A=1..Z=26. Count distinct decodings [M]
- [ ] [Edit Distance `🎯 T2`](coding/algorithms/15-dynamic-programming.md#edit-distance) — Minimum insert/delete/replace operations to convert `word1` to `word2` [H]
- [ ] [Burst Balloons `🎯 T2`](coding/algorithms/15-dynamic-programming.md#burst-balloons) — `n` balloons with values. Bursting balloon `i` scores `nums[i-1]*nums[i]*nums[i+1]`. Maximize total coins [H]
- [ ] [Palindrome Partitioning II `🎯 T2`](coding/algorithms/09-recursion.md#palindrome-partitioning) — Return the minimum number of cuts to partition a string so every substring is a palindrome [H]
- [ ] [House Robber III `🎯 T2`](coding/data-structures/08-tree.md#house-robber-iii) — Houses are arranged in a binary tree. Adjacent nodes (parent-child) cannot both be robbed. Maximize total money robbed [M]
- [ ] [Unique Paths `🎯 T2`](coding/algorithms/15-dynamic-programming.md#unique-paths) — Count distinct paths from top-left to bottom-right of m×n grid, moving only right or down [M]
- [ ] Unique Paths II `🎯 T2` — Unique paths but some cells are blocked (obstacle=1) [M]
- [ ] [Last Stone Weight II `🎯 T2`](coding/algorithms/15-dynamic-programming.md#last-stone-weight-ii) — Smash pairs of stones (losing the difference); minimize the last remaining stone weight [M]
- [ ] [Interleaving String `🎯 T2`](coding/algorithms/15-dynamic-programming.md#interleaving-string) — Given `s1`, `s2`, `s3`, return true if `s3` is formed by an interleaving of `s1` and `s2` (LC 97) [M]
- [ ] [Min Cost Climbing Stairs `🎯 T2`](coding/algorithms/15-dynamic-programming.md#min-cost-climbing-stairs) — Each step has a cost. You can start from step 0 or 1. Pay cost to leave a step (+1 or +2). Minimize total cost to reach beyond the last step [E]
- [ ] [Best Time to Buy and Sell Stock II `⚡ T1`](02-algorithms/15-dynamic-programming.md#best-time-to-buy-and-sell-stock-ii-unlimited-transactions) — Solve the standard interview variant of Best Time to Buy and Sell Stock II. [M]
- [ ] Best Time to Buy and Sell Stock with Cooldown `⚡ T1` — Solve the standard interview variant of Best Time to Buy and Sell Stock with Cooldown. [M]
