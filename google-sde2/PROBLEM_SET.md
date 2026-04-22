# Google SDE-2 (L4) Coding Problem Set (Curated)

This is a **pattern-first** list of canonical problems that cover what Google commonly asks at **SDE-2 (L4)**.

**Fit this into a plan:** [README.md](README.md) → [ROADMAP.md](ROADMAP.md) (4–6 weeks) or [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md) (14 days, including **2 DSA + optional AI-ML**). Pair every block of practice with [CODING_ROUNDS.md](CODING_ROUNDS.md) for communication and [PRACTICE_TRACKER.md](PRACTICE_TRACKER.md) for redos.

Notes:
- Prefer **depth over volume**: redo missed problems until you can derive them quickly.
- Don’t memorize solutions; memorize **patterns + invariants**.
- Use your platform of choice (LeetCode/EPI/etc.). Titles are intentionally generic/canonical.

---

## Leveling (suggested)

- **Must-do (core L4)**: aim to complete ~70% of the list.
- **Strong**: complete ~90% and redo your failures cold.
- **Stretch**: include the harder items (marked “Hard / Stretch”).

---

## Arrays, prefix sums, hashing

- [Two Sum](PROBLEM_DETAILS.md#two-sum)
- [Subarray Sum Equals K](PROBLEM_DETAILS.md#subarray-sum-equals-k)
- [Product of Array Except Self](PROBLEM_DETAILS.md#product-of-array-except-self)
- [Maximum Subarray (Kadane)](PROBLEM_DETAILS.md#maximum-subarray-kadane)
- [Merge Intervals](PROBLEM_DETAILS.md#merge-intervals)
- [Insert Interval](PROBLEM_DETAILS.md#insert-interval) (Stretch)
- [Next Permutation](PROBLEM_DETAILS.md#next-permutation) (Stretch)
- [Majority Element](PROBLEM_DETAILS.md#majority-element)

## Two pointers

- [3Sum](PROBLEM_DETAILS.md#3sum)
- [Container With Most Water](PROBLEM_DETAILS.md#container-with-most-water)
- [Trapping Rain Water](PROBLEM_DETAILS.md#trapping-rain-water) (Hard / Stretch)
- [Remove Duplicates from Sorted Array](PROBLEM_DETAILS.md#remove-duplicates-from-sorted-array)
- [Sort Colors (Dutch Flag)](PROBLEM_DETAILS.md#sort-colors-dutch-flag)

## Sliding window

- [Longest Substring Without Repeating Characters](PROBLEM_DETAILS.md#longest-substring-without-repeating-characters)
- [Longest Repeating Character Replacement](PROBLEM_DETAILS.md#longest-repeating-character-replacement)
- [Minimum Window Substring](PROBLEM_DETAILS.md#minimum-window-substring) (Hard / Stretch)
- [Find All Anagrams in a String](PROBLEM_DETAILS.md#find-all-anagrams-in-a-string)
- [Sliding Window Maximum](PROBLEM_DETAILS.md#sliding-window-maximum) (Hard / Stretch)

## Binary search (index + “search on answer”)

- [Find First and Last Position of Element](PROBLEM_DETAILS.md#find-first-and-last-position-of-element)
- [Search in Rotated Sorted Array](PROBLEM_DETAILS.md#search-in-rotated-sorted-array)
- [Find Minimum in Rotated Sorted Array](PROBLEM_DETAILS.md#find-minimum-in-rotated-sorted-array)
- [Koko Eating Bananas](PROBLEM_DETAILS.md#koko-eating-bananas) (BS on answer)
- [Median of Two Sorted Arrays](PROBLEM_DETAILS.md#median-of-two-sorted-arrays) (Hard / Stretch)

## Stack / queue (monotonic patterns)

- [Valid Parentheses](PROBLEM_DETAILS.md#valid-parentheses)
- [Daily Temperatures](PROBLEM_DETAILS.md#daily-temperatures)
- [Largest Rectangle in Histogram](PROBLEM_DETAILS.md#largest-rectangle-in-histogram) (Hard / Stretch)
- [Evaluate Reverse Polish Notation](PROBLEM_DETAILS.md#evaluate-reverse-polish-notation)

## Linked list

- [Reverse Linked List](PROBLEM_DETAILS.md#reverse-linked-list)
- [Linked List Cycle II](PROBLEM_DETAILS.md#linked-list-cycle-ii)
- [Merge Two Sorted Lists](PROBLEM_DETAILS.md#merge-two-sorted-lists)
- [LRU Cache](PROBLEM_DETAILS.md#lru-cache) (Hard / Stretch; also design-heavy)

## Trees / BST

- [Maximum Depth of Binary Tree](PROBLEM_DETAILS.md#maximum-depth-of-binary-tree)
- [Validate BST](PROBLEM_DETAILS.md#validate-bst)
- [Lowest Common Ancestor (BST + general)](PROBLEM_DETAILS.md#lowest-common-ancestor-bst-general)
- [Binary Tree Level Order Traversal](PROBLEM_DETAILS.md#binary-tree-level-order-traversal)
- [Kth Smallest in BST](PROBLEM_DETAILS.md#kth-smallest-in-bst)
- [Binary Tree Maximum Path Sum](PROBLEM_DETAILS.md#binary-tree-maximum-path-sum) (Hard / Stretch)
- [Serialize and Deserialize Binary Tree](PROBLEM_DETAILS.md#serialize-and-deserialize-binary-tree) (Hard / Stretch)

## Graphs (BFS/DFS/topo)

- [Number of Islands](PROBLEM_DETAILS.md#number-of-islands)
- [Clone Graph](PROBLEM_DETAILS.md#clone-graph)
- [Course Schedule](PROBLEM_DETAILS.md#course-schedule) (topo + cycle)
- [Rotting Oranges](PROBLEM_DETAILS.md#rotting-oranges) (multi-source BFS)
- [Word Ladder](PROBLEM_DETAILS.md#word-ladder) (Hard / Stretch)
- [Network Delay Time](PROBLEM_DETAILS.md#network-delay-time) (Dijkstra; Stretch)

## Dynamic programming (core)

- [House Robber](PROBLEM_DETAILS.md#house-robber)
- [Coin Change](PROBLEM_DETAILS.md#coin-change)
- [Longest Increasing Subsequence](PROBLEM_DETAILS.md#longest-increasing-subsequence)
- [Longest Common Subsequence](PROBLEM_DETAILS.md#longest-common-subsequence)
- [Edit Distance](PROBLEM_DETAILS.md#edit-distance) (Hard / Stretch)
- [Word Break](PROBLEM_DETAILS.md#word-break)

## Backtracking

- [Permutations](PROBLEM_DETAILS.md#permutations)
- [Subsets](PROBLEM_DETAILS.md#subsets)
- [Combination Sum](PROBLEM_DETAILS.md#combination-sum)
- [Word Search](PROBLEM_DETAILS.md#word-search) (Stretch)

## Heaps

- [Top K Frequent Elements](PROBLEM_DETAILS.md#top-k-frequent-elements)
- [Merge K Sorted Lists](PROBLEM_DETAILS.md#merge-k-sorted-lists)
- [Find Median from Data Stream](PROBLEM_DETAILS.md#find-median-from-data-stream) (Hard / Stretch)

---

## How to use this set effectively

- For each problem, write down:
  - Pattern name + invariant
  - Two edge cases
  - Complexity
- If you fail a problem in a mock, it goes into your mistake log in `PRACTICE_TRACKER.md` and you redo it 3 times (same day, +2 days, +7 days).

