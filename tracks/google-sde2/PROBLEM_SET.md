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

- [E] [Two Sum](PROBLEM_DETAILS.md#two-sum)
- [M] [Subarray Sum Equals K](PROBLEM_DETAILS.md#subarray-sum-equals-k)
- [M] [Product of Array Except Self](PROBLEM_DETAILS.md#product-of-array-except-self)
- [M] [Maximum Subarray (Kadane)](PROBLEM_DETAILS.md#maximum-subarray-kadane)
- [M] [Merge Intervals](PROBLEM_DETAILS.md#merge-intervals)
- [M] [Majority Element](PROBLEM_DETAILS.md#majority-element) — Boyer-Moore voting
- [H] [Insert Interval](PROBLEM_DETAILS.md#insert-interval) (Stretch)
- [H] [Next Permutation](PROBLEM_DETAILS.md#next-permutation) (Stretch)

## Two pointers

- [M] [3Sum](PROBLEM_DETAILS.md#3sum)
- [M] [Container With Most Water](PROBLEM_DETAILS.md#container-with-most-water)
- [E] [Remove Duplicates from Sorted Array](PROBLEM_DETAILS.md#remove-duplicates-from-sorted-array)
- [M] [Sort Colors (Dutch Flag)](PROBLEM_DETAILS.md#sort-colors-dutch-flag)
- [H] [Trapping Rain Water](PROBLEM_DETAILS.md#trapping-rain-water) (Hard / Stretch)

## Sliding window

- [M] [Longest Substring Without Repeating Characters](PROBLEM_DETAILS.md#longest-substring-without-repeating-characters)
- [M] [Longest Repeating Character Replacement](PROBLEM_DETAILS.md#longest-repeating-character-replacement)
- [M] [Find All Anagrams in a String](PROBLEM_DETAILS.md#find-all-anagrams-in-a-string)
- [H] [Minimum Window Substring](PROBLEM_DETAILS.md#minimum-window-substring) (Hard / Stretch)
- [H] [Sliding Window Maximum](PROBLEM_DETAILS.md#sliding-window-maximum) (Hard / Stretch)

## Binary search (index + “search on answer”)

- [M] [Find First and Last Position of Element](PROBLEM_DETAILS.md#find-first-and-last-position-of-element)
- [M] [Search in Rotated Sorted Array](PROBLEM_DETAILS.md#search-in-rotated-sorted-array)
- [M] [Find Minimum in Rotated Sorted Array](PROBLEM_DETAILS.md#find-minimum-in-rotated-sorted-array)
- [M] [Koko Eating Bananas](PROBLEM_DETAILS.md#koko-eating-bananas) (BS on answer)
- [H] [Median of Two Sorted Arrays](PROBLEM_DETAILS.md#median-of-two-sorted-arrays) (Hard / Stretch)

## Stack / queue (monotonic patterns)

- [E] [Valid Parentheses](PROBLEM_DETAILS.md#valid-parentheses)
- [M] [Daily Temperatures](PROBLEM_DETAILS.md#daily-temperatures)
- [M] [Evaluate Reverse Polish Notation](PROBLEM_DETAILS.md#evaluate-reverse-polish-notation)
- [H] [Largest Rectangle in Histogram](PROBLEM_DETAILS.md#largest-rectangle-in-histogram) (Hard / Stretch)

## Linked list

- [E] [Reverse Linked List](PROBLEM_DETAILS.md#reverse-linked-list)
- [E] [Merge Two Sorted Lists](PROBLEM_DETAILS.md#merge-two-sorted-lists)
- [M] [Linked List Cycle II](PROBLEM_DETAILS.md#linked-list-cycle-ii)
- [M] [Remove Nth Node From End](PROBLEM_DETAILS.md#remove-nth-from-end)
- [H] [LRU Cache](PROBLEM_DETAILS.md#lru-cache) (Hard / Stretch; doubly linked list + hash map)

## Trees / BST

- [E] [Maximum Depth of Binary Tree](PROBLEM_DETAILS.md#maximum-depth-of-binary-tree)
- [M] [Binary Tree Level Order Traversal](PROBLEM_DETAILS.md#binary-tree-level-order-traversal)
- [M] [Validate BST](PROBLEM_DETAILS.md#validate-bst)
- [M] [Lowest Common Ancestor (BST + general)](PROBLEM_DETAILS.md#lowest-common-ancestor-bst-general)
- [M] [Kth Smallest in BST](PROBLEM_DETAILS.md#kth-smallest-in-bst)
- [H] [Binary Tree Maximum Path Sum](PROBLEM_DETAILS.md#binary-tree-maximum-path-sum) (Hard / Stretch)
- [H] [Serialize and Deserialize Binary Tree](PROBLEM_DETAILS.md#serialize-and-deserialize-binary-tree) (Hard / Stretch)

## Graphs (BFS/DFS/topo)

- [M] [Number of Islands](PROBLEM_DETAILS.md#number-of-islands)
- [M] [Clone Graph](PROBLEM_DETAILS.md#clone-graph)
- [M] [Course Schedule](PROBLEM_DETAILS.md#course-schedule) (topo + cycle)
- [M] [Rotting Oranges](PROBLEM_DETAILS.md#rotting-oranges) (multi-source BFS)
- [H] [Word Ladder](PROBLEM_DETAILS.md#word-ladder) (Hard / Stretch)
- [M] [Network Delay Time](PROBLEM_DETAILS.md#network-delay-time) (Dijkstra; Stretch)

## Dynamic programming (core)

- [M] [House Robber](PROBLEM_DETAILS.md#house-robber)
- [M] [Coin Change](PROBLEM_DETAILS.md#coin-change)
- [M] [Word Break](PROBLEM_DETAILS.md#word-break)
- [M] [Longest Increasing Subsequence](PROBLEM_DETAILS.md#longest-increasing-subsequence)
- [M] [Longest Common Subsequence](PROBLEM_DETAILS.md#longest-common-subsequence)
- [H] [Edit Distance](PROBLEM_DETAILS.md#edit-distance) (Hard / Stretch)

## Backtracking

- [M] [Subsets](PROBLEM_DETAILS.md#subsets)
- [M] [Permutations](PROBLEM_DETAILS.md#permutations)
- [M] [Combination Sum](PROBLEM_DETAILS.md#combination-sum)
- [M] [Word Search](PROBLEM_DETAILS.md#word-search) (Stretch)

## Heaps

- [M] [Top K Frequent Elements](PROBLEM_DETAILS.md#top-k-frequent-elements)
- [H] [Merge K Sorted Lists](PROBLEM_DETAILS.md#merge-k-sorted-lists)
- [H] [Find Median from Data Stream](PROBLEM_DETAILS.md#find-median-from-data-stream) (Hard / Stretch — two heaps)

---

## How to use this set effectively

- For each problem, write down:
  - Pattern name + invariant
  - Two edge cases
  - Complexity
- If you fail a problem in a mock, it goes into your mistake log in `PRACTICE_TRACKER.md` and you redo it 3 times (same day, +2 days, +7 days).

