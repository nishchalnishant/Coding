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

## Final Strategy for the Interview

Don't just solve problems; solve **patterns**. When you see a new question, ask yourself:
1.  "Is this a **Binary Choice**? (House Robber / DP)"
2.  "Am I **Exploring All Paths** and need to undo? (Backtracking)"
3.  "Is this a **Continuous Window**? (Sliding Window)"
4.  "Is there a **Dependency Order**? (Topo Sort)"

If you can map a problem to a conversation, you've already won half the battle. Now go through the `core/` folder and see these patterns in action!
