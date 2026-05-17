# The SDE-3 Pattern Playbook: A Guided Conversation

Welcome to the heart of this repository. If you've ever felt like you're "memorizing" LeetCode instead of "learning" it, this document is for you. We’ve organized these problems not just as static code blocks, but as a series of **conversations**. 

Imagine we're sitting down together, and I'm showing you the "Matrix of Coding Patterns." For every foundational problem, we’ll talk about why it exists, how to spot it under pressure, and how to handle the "twists" an interviewer will throw at you when they realize you know the base solution.

---

## 1. Dynamic Programming: Beyond the Recurrence

Let's start with the big one. DP isn't about math; it's about **memoized decision trees**.

### 1.1 The LIS Family: Sorting the Chaos
*Foundational Problem: [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/)*

**The Conversation:**
If an interviewer asks you to find the longest "something" in an unsorted array where order matters, your brain should immediately scream "LIS." 

"So," the interviewer asks, "how do we find the longest strictly increasing subsequence?"
You start with the **O(N²) approach**: At every element, you look back and say, "If I'm the end of a sequence, which previous sequence can I join?" You're basically building a chain.
But then they push: "Can we do it in O(N log N)?"
This is where you bring up **Patience Sorting**. Imagine you're playing cards. You have a row of piles. You place a card on the first pile it's smaller than. If it's larger than all of them, you start a new pile. The number of piles at the end is your answer. In code, those piles are just a sorted array where you perform binary search.

**The Interviewer's Twist:**
Once you solve LIS, they won't stop there. They’ll ask:
*   "What if I want the **Number of LIS**?" (Inherit counts like paths in a graph).
*   "What if I have **Envelopes** (Russian Doll)?" (Sort by width, then the problem is just LIS on height. But wait—sort height *descending* for the same width so you don't fit an envelope into one of the same width!)
*   "What if it's a **Mountain Array**?" (Run LIS from left, LIS from right, and find the peak).

---

### 1.2 The Knapsack Logic: Making Change
*Foundational Problem: [Coin Change](https://leetcode.com/problems/coin-change/)*

**The Conversation:**
"You have infinite coins and a target. What's the minimum coins?"
This is the classic **Unbounded Knapsack**. The "Click Moment" here is realizing that to solve for `$11`, you just need to know the answer for `$11 - coin_value` for all your coins. 

**The Interviewer's Twist:**
They’ll pivot the question slightly to see if you actually understand the state transition:
*   "Don't give me the minimum, give me the **Total Combinations**." (Switch from `min()` to `+=`).
*   "What if **Order Matters** (Permutations)?" (Flip the loops! Loop over the amount first, then the coins).
*   "What if the 'coins' are **Tickets** for 1, 7, or 30 days?" (The logic is identical—you're just subtracting the pass duration instead of a coin value).

---

### 1.3 House Robber: The Binary Choice
*Foundational Problem: [House Robber](https://leetcode.com/problems/house-robber/)*

**The Conversation:**
This is the simplest form of **State Machine DP**. At every house, you have a binary choice: *Rob* (which locks you out of the neighbor) or *Skip*.
`dp[i] = max(rob_this + dp[i-2], skip_this + dp[i-1])`

**The Interviewer's Twist:**
They love to change the "shape" of the neighborhood:
*   "The street is a **Circle**." (Run it twice: once without the first house, once without the last).
*   "The neighborhood is a **Tree**." (This is where people panic. Don't. It’s just recursion returning `(rob_me, skip_me)`).
*   "Instead of houses, you have numbers. If you take `x`, you lose `x-1` and `x+1` (**Delete and Earn**)." (Plot twist: convert the numbers to an array of sums, and it’s just House Robber again!)

---

## 2. Recursion & Backtracking: The Art of Undoing

Backtracking is just DFS with a **cleanup crew**.

### 2.1 Permutations: Every Possible Order
*Foundational Problem: [Permutations](https://leetcode.com/problems/permutations/)*

**The Conversation:**
"Give me every way to arrange these numbers."
The mental model is a **Decision Tree**. At each step, you pick a number you haven't used yet, go deep, and then—critically—"undo" your choice so you can try the next one. 

**The Interviewer's Twist:**
*   "What if there are **Duplicates**?" (The "Gold Standard" fix: Sort the array and only use a duplicate if its predecessor was already used in this branch).
*   "What if I just want the **Next Permutation**?" (Don't use recursion. Find the 'pivot' where things stop increasing from the right, swap, and reverse).

---

### 2.2 Word Search: Exploring the Grid
*Foundational Problem: [Word Search](https://leetcode.com/problems/word-search/)*

**The Conversation:**
"Find this word in a 2D grid."
This is a pathfinding problem. You start at a cell, mark it as "visited" (usually by changing the character to a `#`), look in 4 directions, and if they all fail, you *must* change the `#` back to the original letter.

**The Interviewer's Twist:**
"Now find **1,000 words** at once."
Running Word Search 1,000 times is too slow. This is where you combine patterns. You put all words into a **Trie**. Now, as you move on the grid, you move in the Trie simultaneously. If the Trie branch ends, your grid path ends too. It’s a beautiful marriage of two data structures.

---

## 3. Sliding Window: The Moving Frame

This pattern is for **continuous subarrays**. If the problem says "contiguous," look for the window.

### 3.1 The Dynamic Window: Unique Substrings
*Foundational Problem: [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)*

**The Conversation:**
You have a `left` and `right` pointer. You move `right` to grow the window. If you hit a duplicate, you shrink `left`. 
The "SDE-3 move" is not moving `left` by 1. It's using a Hash Map to store the last index of each character and **jumping** `left` directly to `map[char] + 1`.

**The Interviewer's Twist:**
*   "What if I can **Replace K characters**?" (The window is valid as long as `window_size - max_char_frequency <= k`).
*   "Find the **Minimum Window** that contains all chars of `T`." (Expand until you have everything, then shrink `left` as much as possible until it breaks).

---

## 4. Graphs: The Connectivity Web

### 4.1 Topological Sort: Prerequisites & Order
*Foundational Problem: [Course Schedule](https://leetcode.com/problems/course-schedule/)*

**The Conversation:**
"Can you finish these courses?"
This is really asking: "Is there a cycle?"
We use **Kahn’s Algorithm**. Find the courses with zero prerequisites (in-degree 0), take them, and "remove" them from the graph. This reduces the prerequisite count for the next set of courses. If you can't take all courses, you’ve hit a cycle.

**The Interviewer's Twist:**
"What if the 'courses' are letters in an **Alien Dictionary**?"
The problem is the same, but the graph is implicit. You compare adjacent words, find the first different character, and that’s your edge (`a -> b`). Build the graph, then run the same Topo Sort.

---

## 5. Prefix Sums: The "Chop Off" Strategy
*Foundational Problem: [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/)*

**The Conversation:**
"Find how many subarrays sum to K. Oh, and there are **negative numbers**."
Sliding window fails here. Why? Because adding an element might make the sum smaller! 
The secret is **Prefix Sums**. At any point, if your current total is `15` and you're looking for `K=5`, you check: "Have I seen a total of `10` before?" If yes, the gap between that `10` and this `15` is a subarray that sums to `5`. 

**The Interviewer's Twist:**
*   "Find the **Longest Subarray with sum 0** (Contiguous Array)." (Treat `0`s as `-1` and `1`s as `1`. Find the longest gap between identical prefix sums).
*   "Find paths in a **Binary Tree** that sum to K." (Same logic! Use the hash map during a DFS and remember to remove the prefix from the map when you backtrack).

---

## 6. Two Pointers: The Converging Search

### 6.1 3Sum / 4Sum
*Foundational Problem: [3Sum](https://leetcode.com/problems/3sum/)*

**The Conversation:**
"Find all triplets that sum to zero."
Sort the array first. Fix one element, then use two pointers on the rest. The key is **deduplication**: skip duplicates at the outer loop AND skip duplicates in the inner two-pointer pass, otherwise you count the same triplet twice.

**The Interviewer's Twist:**
- "What if it's **4Sum**?" (Fix two elements with nested loops, then two-pointer on the rest. Same deduplication logic.)
- "What about **3Sum Closest**?" (Track the closest sum seen. Same structure, update min-delta instead of collecting results.)
- "What if I just want to **count** pairs that sum to target in a sorted array?" (Two pointers converge from both ends; O(N) time.)

---

### 6.2 Container With Most Water
*Foundational Problem: [Container With Most Water](https://leetcode.com/problems/container-with-most-water/)*

**The Conversation:**
"Two pointers start at the ends. Move the **shorter** side inward — moving the taller side can only make things worse, since the area is bottlenecked by the shorter wall."
This is the exchange argument: if the left wall is shorter, moving left inward is the only hope of finding a taller wall.

**The Interviewer's Twist:**
- "What if the bars are **Trapping Rain Water** instead?" (Per-cell water = min(left_max, right_max) - height[i]. Two-pointer does this in O(1) space.)

---

## 7. Binary Search: Beyond the Sorted Array

### 7.1 Find Peak Element
*Foundational Problem: [Find Peak Element](https://leetcode.com/problems/find-peak-element/)*

**The Conversation:**
"A peak is an element greater than its neighbors. The array can have multiple peaks."
The trick: if `arr[mid] < arr[mid+1]`, there's a peak to the right (the array is going up). Otherwise it's to the left or at mid. This works even on unsorted arrays — you're binary-searching on the **slope**, not the value.

**The Interviewer's Twist:**
- "What about **Find Peak in 2D Matrix**?" (Binary search on columns; for each mid column, find the row with the max value. Check if it's a 2D peak.)
- "What about **Koko Eating Bananas** / **Minimum Capacity to Ship Packages**?" (Binary search on answer: guess a value, write a `can_finish(speed)` check. These are the same problem family.)

---

### 7.2 Search in Rotated Sorted Array
*Foundational Problem: [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/)*

**The Conversation:**
"At every mid, one half is always sorted. Check which half — then check if target falls inside the sorted half."
`if arr[left] <= arr[mid]` → left half is sorted → `if arr[left] <= target < arr[mid]` → go left, else go right.

**The Interviewer's Twist:**
- "What if there are **duplicates**?" (You can't determine which half is sorted when `arr[left] == arr[mid]`. Do `left++` to skip. Worst case degrades to O(N).)
- "What if I want the **rotation point** (minimum)?" (Separate problem: binary search for where the sorted order breaks.)

---

## 8. Linked Lists: Pointers in Space

### 8.1 Linked List Cycle + Floyd's
*Foundational Problem: [Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/)*

**The Conversation:**
"Floyd's algorithm: slow moves 1 step, fast moves 2. If they meet, there's a cycle."
To find the **entry point**: once they meet inside the cycle, reset slow to head. Now move both one step at a time — they'll meet exactly at the cycle's start. (The math: the distance from head to entry = distance from meeting point to entry, due to the cycle structure.)

**The Interviewer's Twist:**
- "Find the **middle of the linked list**." (Fast/slow pointers. When fast reaches the end, slow is at the middle.)
- "Find the **Kth node from the end**." (Two pointers, offset by K. Move the lead pointer K steps first, then move both together.)

---

### 8.2 Merge K Sorted Lists
*Foundational Problem: [Merge K Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)*

**The Conversation:**
"Push the head of each list into a min-heap. Pop the smallest, push its `next`. Repeat."
Min-heap always gives you the current global minimum in O(log K).

**The Interviewer's Twist:**
- "What if K is very large but the lists are **very short**?" (Merge in pairs, like merge sort. Avoids the heap overhead.)
- "What if you get nodes from a **stream** one at a time?" (Maintain a sorted structure as you go — back to the heap approach.)

---

## 9. Trees: More Than Traversal

### 9.1 Lowest Common Ancestor (LCA)
*Foundational Problem: [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/)*

**The Conversation:**
"Recurse down. If you find p or q, return it. At any node, if left and right both return non-null, this node is the LCA."
The base cases: return null (not found), return p or q (found one). The merge: if both children returned something, the current node is the answer.

**The Interviewer's Twist:**
- "What if it's a **BST**?" (Use the BST property: if both p and q are less than root, go left. If both greater, go right. Otherwise current node is LCA — O(log N) for balanced.)
- "What if you need LCA for **many queries** efficiently?" (Binary Lifting or Euler Tour + sparse table — O(N log N) preprocess, O(log N) per query.)

---

### 9.2 Binary Tree Maximum Path Sum
*Foundational Problem: [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/)*

**The Conversation:**
"A path can go through any node and doesn't have to pass through the root."
Postorder traversal. At each node, compute the max gain from left child and right child (clamped to 0 — never take a negative branch). Update the global max with `node.val + left_gain + right_gain`. Return `node.val + max(left_gain, right_gain)` upward (can only extend one branch).

**The Interviewer's Twist:**
- "What if it's a **path in a general graph** (not a tree)?" (Fundamentally different — becomes longest path which is NP-hard for general graphs. But on a DAG, use topo sort + DP.)
- "What about **diameter of a binary tree**?" (Same structure: at each node, diameter through it = left_depth + right_depth.)

---

### 9.3 Serialize and Deserialize Binary Tree
*Foundational Problem: [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)*

**The Conversation:**
"Preorder traversal, represent null as `'#'`. Deserialize by consuming tokens from a queue."
The key: preorder guarantees you can reconstruct the tree uniquely because you know the root first, then left subtree, then right subtree.

**The Interviewer's Twist:**
- "What if it's a **BST**?" (Inorder gives a sorted sequence, but preorder alone is enough to reconstruct. Inorder of BST + preorder of BST together uniquely reconstruct — but for serialization, preorder is sufficient.)
- "What about **N-ary tree** serialization?" (Use a delimiter to mark how many children each node has.)

---

## 10. Intervals: Merging and Scheduling

### 10.1 Merge Intervals
*Foundational Problem: [Merge Intervals](https://leetcode.com/problems/merge-intervals/)*

**The Conversation:**
"Sort by start. If the next interval's start ≤ current end, merge (extend the end). Otherwise push current and start fresh."
The sort is the key move — it ensures overlapping intervals are adjacent.

**The Interviewer's Twist:**
- "**Insert Interval** into a sorted list." (Find the position, merge with all overlapping intervals — same condition.)
- "**Minimum Meeting Rooms**." (Sort by start time. Use a min-heap of end times. If next meeting's start ≥ heap top, a room is free — reuse it.)
- "**Non-overlapping Intervals** (minimum removals)." (Flip: count max non-overlapping, sort by end, greedy. Answer = total - max non-overlapping.)

---

## 11. Matrix / Grid Problems

### 11.1 Number of Islands / Connected Components
*Foundational Problem: [Number of Islands](https://leetcode.com/problems/number-of-islands/)*

**The Conversation:**
"BFS or DFS from every unvisited '1'. Mark cells visited as you go (set to '0' or a visited marker). Each launch is one island."
Union-Find is an alternative — merge adjacent '1's, count distinct roots.

**The Interviewer's Twist:**
- "**Max Area of Island**." (Same DFS/BFS — track size during traversal.)
- "**Pacific Atlantic Water Flow**." (Multi-source BFS from Pacific edges and Atlantic edges separately. Answer is the intersection.)
- "**01 Matrix** (distance to nearest 0)." (Multi-source BFS from all 0-cells simultaneously.)

---

### 11.2 Word Search / Unique Paths
*Foundational Problem: [Unique Paths](https://leetcode.com/problems/unique-paths/)*

**The Conversation:**
"`dp[i][j] = dp[i-1][j] + dp[i][j-1]`. You can only come from above or from the left."

**The Interviewer's Twist:**
- "What if there are **obstacles**?" (Set dp = 0 at obstacle cells. Same recurrence everywhere else.)
- "**Minimum Path Sum**." (Replace + with min, seed with the actual values.)
- "**Dungeon Game**." (Reverse DP from bottom-right to top-left — forward DP doesn't capture the constraint that HP must stay positive.)

---

## 12. Stack Problems

### 12.1 Daily Temperatures / Next Greater Element
*Foundational Problem: [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/)*

**The Conversation:**
"Monotonic stack stores indices of elements waiting for their 'next greater'. When a larger element arrives, pop all smaller ones and record the distance."

**The Interviewer's Twist:**
- "**Largest Rectangle in Histogram**." (Monotonic stack tracks left boundaries. When a bar pops because the current bar is shorter, compute the rectangle using the popped bar's height.)
- "**Trapping Rain Water** (stack version)." (Track left walls on the stack. When current bar is taller than stack top, compute trapped water between stack top and current bar.)
- "**Remove K Digits** to make smallest number." (Greedy + monotonic stack: pop larger digits when a smaller digit comes in, until K removals done.)

---

## 13. Heap / Priority Queue

### 13.1 Top K Frequent Elements
*Foundational Problem: [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)*

**The Conversation:**
"Count frequencies with a hash map. Use a min-heap of size K — push each element; if heap exceeds K, pop the minimum. What remains is the top K."

**The Interviewer's Twist:**
- "If K is close to N, use **bucket sort** instead — O(N)." (Bucket by frequency, collect from highest bucket.)
- "**Kth Largest in a Stream**." (Maintain a min-heap of size K. The top of the heap is always the Kth largest.)
- "**Find Median from Data Stream**." (Two heaps: max-heap for lower half, min-heap for upper half. Rebalance after each insert so sizes differ by at most 1.)

---

## 14. Trie Problems

### 14.1 Implement Trie / Word Dictionary
*Foundational Problem: [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/)*

**The Conversation:**
"Each node is a dict (or array of 26) plus an `is_end` flag. Insert walks/creates nodes. Search walks and checks `is_end`. StartsWith just walks."

**The Interviewer's Twist:**
- "**Design Add and Search Words** (with `.` wildcard)." (DFS at `.` — try all 26 children.)
- "**Word Search II** (find all words from a list in a grid)." (Build a Trie from the word list. DFS on the grid, move in the Trie simultaneously. Prune when the Trie branch ends.)
- "**Longest Word in Dictionary**." (Build Trie, BFS/DFS: only extend from nodes that are word ends.)

---

## 15. Bit Manipulation

### 15.1 Single Number / Missing Number
*Foundational Problem: [Single Number](https://leetcode.com/problems/single-number/)*

**The Conversation:**
"XOR all numbers. Pairs cancel out (x ^ x = 0). What remains is the lonely number."

**The Interviewer's Twist:**
- "**Single Number II** (every other appears 3 times)." (Count bits modulo 3. Or use two bitmasks `ones, twos` with state machine logic.)
- "**Missing Number in [0..N]**." (XOR all array values with XOR of 0..N. The missing number is what doesn't cancel.)
- "**Counting Bits** (for 0..N)." (DP: `dp[i] = dp[i >> 1] + (i & 1)`. Each number has the same bits as its right-shift, plus its LSB.)

---

## 16. Math / Number Theory

### 16.1 Happy Number / Fast-Slow Cycle
*Foundational Problem: [Happy Number](https://leetcode.com/problems/happy-number/)*

**The Conversation:**
"Digit-square-sum process either reaches 1 (happy) or enters a cycle. Use Floyd's fast-slow pointer on the number sequence to detect the cycle — same algorithm as linked list cycle detection, just on a virtual sequence."

**The Interviewer's Twist:**
- "**Pow(x, n)**." (Binary exponentiation: `O(log N)`. If n < 0, return `1 / pow(x, -n)`. Handle n = INT_MIN carefully.)
- "**Excel Sheet Column Number**." (Base-26 arithmetic. 'A'=1, 'Z'=26 — it's NOT zero-indexed, which is the gotcha.)
- "**Integer to Roman / Roman to Integer**." (Greedy for int → roman. Map lookup + handle subtractive notation for roman → int.)

---

## Final Strategy for the Interview

Don't just solve problems; solve **patterns**. When you see a new question, ask yourself:
1. "Is this a **Binary Choice** at each step? (State Machine DP)"
2. "Am I **Exploring All Paths** and need to undo? (Backtracking)"
3. "Is this a **Continuous Window** or contiguous range? (Sliding Window / Prefix Sum)"
4. "Is there a **Dependency Order**? (Topo Sort)"
5. "Am I looking for **min/max of a range**? (Heap / Segment Tree / Monotonic)"
6. "Can I binary search on the **answer** instead of the input? (Binary Search on Answer)"
7. "Is this a **connectivity** problem? (Union-Find / BFS/DFS)"

> [!TIP]
> The most common "aha" upgrades: O(N²) → O(N) via hash map; O(N²) → O(N log N) via sort + greedy; brute backtracking → DP when you only need count/max, not the actual path. When stuck, ask: "Am I recomputing something?" (hash/DP) or "Does sorting unlock a linear pass?" (sort + greedy/two-pointer).

If you can map a problem to a conversation, you've already won half the battle. Now go through the `core/` folder and see these patterns in action!
