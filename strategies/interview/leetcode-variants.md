# LeetCode Patterns, Solutions, and Variants

This document categorizes canonical LeetCode questions by topic. For each foundational problem, we provide the **Core Solution Logic** and a list of **Common Variants** that test the same underlying pattern with slight twists. Mastering the base problem allows you to solve all its variants.

---

## 1. Dynamic Programming (DP)

### 1.1 Longest Increasing Subsequence (LIS)

- **What (The Problem & Goal):** Given an unsorted integer array, find the length of the longest strictly increasing subsequence. A subsequence means elements don't need to be contiguous, but they must maintain their original relative order.
- **How (Intuition & Mental Model):**
  - **O(N²) DP Approach:** Ask "what is the longest sequence _ending at_ the current element?" For each element, look back at all previous elements that are strictly smaller. The longest sequence you can form is the longest valid previous sequence + 1.
  - **O(N log N) Patience Sorting Approach:** Imagine building piles of cards where you can only place a smaller card on top of a larger one. If no such pile exists, start a new pile to the right. The number of piles equals the LIS length. In code, maintain an array of the "smallest tail element" for each possible length. Because this array naturally stays sorted, you can use Binary Search to find the exact placement for each new element.
- **Variants:**
  1. **Number of Longest Increasing Subsequence:**
     - _What:_ Return the total _count_ of longest increasing subsequences, not just the length.
     - _How:_ Maintain a parallel `counts[i]` array alongside `dp[i]`. If you find a new max length, inherit the count. If you tie an existing max length, add the count.
  2. **Russian Doll Envelopes:**
     - _What:_ Fit envelopes inside each other (both width and height must be strictly greater).
     - _How:_ Sort by width ascending, then height descending. The problem reduces to finding the 1D LIS on the heights. The descending height sort prevents envelopes of the same width from fitting into each other.
  3. **Maximum Length of Pair Chain:**
     - _What:_ Chain pairs `(a,b)` and `(c,d)` where `b < c`.
     - _How:_ Similar to LIS, but sort pairs by their second coordinate and greedily pick non-overlapping pairs.
  4. **Longest Bitonic Subsequence:**
     - _What:_ Find the longest sequence that strictly increases, then strictly decreases.
     - _How:_ Compute LIS from left to right, and LIS from right to left, then find the `max(left[i] + right[i] - 1)` at every index.
  5. **Largest Divisible Subset:**
     - _What:_ Find the largest subset where every pair `(i, j)` satisfies `i % j == 0` or `j % i == 0`.
     - _How:_ Sort the array first. The condition becomes `nums[i] % nums[j] == 0`. Maintain a `parent` array to reconstruct the actual subset, transitioning if modulo is zero.
  6. **Minimum Number of Removals to Make Mountain Array:**
     - _What:_ Remove the minimum elements so the array strictly increases then strictly decreases.
     - _How:_ Exactly the same logic as Longest Bitonic Subsequence; just subtract the bitonic length from the total length.

### 1.2 Coin Change (Unbounded Knapsack)

- **What (The Problem & Goal):** Find the minimum number of coins needed to make up a target amount. You have an infinite supply of each coin denomination.
- **How (Intuition & Mental Model):** To find the minimum coins for `amount`, look at `amount - coin_value`. The answer is `1 + minimum_coins(amount - coin_value)`. We build a DP array of size `amount + 1` initialized to infinity. `dp[0] = 0`. For each coin, we update all reachable amounts.
- **Variants:**
  1. **Coin Change II:**
     - _What:_ Find the _number of combinations_ that make up that amount, rather than the minimum coins.
     - _How:_ `dp[x] += dp[x - coin]`. You are accumulating paths, not finding a minimum.
  2. **Perfect Squares:**
     - _What:_ Least number of perfect square numbers (`1, 4, 9...`) that sum to `n`.
     - _How:_ The "coins" are just pre-calculated perfect squares `1, 4, 9, 16...`. The DP logic is exactly the same as Coin Change.
  3. **Combination Sum IV:**
     - _What:_ Same as Coin Change II but permutations matter (`(1,2)` is different from `(2,1)`).
     - _How:_ The loop order is inverted: loop over `amount` first, then `coins`. This allows different coin sequences to be counted as unique permutations.
  4. **Minimum Cost For Tickets:**
     - _What:_ Find the minimum cost to travel on specific days given 1-day, 7-day, and 30-day passes.
     - _How:_ Similar state transition `dp[day] = min(cost + dp[day - pass_duration])`, but the "coins" (passes) have different coverages instead of simple values. If you don't travel on a day, `dp[day] = dp[day-1]`.
  5. **Integer Break:**
     - _What:_ Maximize the product of an array of integers that sum to `n`.
     - _How:_ This is an unbounded knapsack where both the "weights" and "values" are the integers `1` to `n-1`. Try breaking `n` into `i` and `n-i`.

### 1.3 House Robber (1D DP / State Machine)

- **What (The Problem & Goal):** Maximize the money robbed from an array of houses, with the constraint that you cannot rob two adjacent houses.
- **How (Intuition & Mental Model):** At any house `i`, you have two choices: Rob it (which means you add its value to the max profit from house `i-2`) OR Skip it (which means you keep the max profit from house `i-1`). The transition is `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`. This can be optimized to O(1) space by only tracking `rob1` (i-2) and `rob2` (i-1).
- **Variants:**
  1. **House Robber II:**
     - _What:_ Houses are arranged in a circle, so the first and last houses are adjacent.
     - _How:_ Run the core algorithm twice: once from `0` to `n-2` (skipping the last house) and once from `1` to `n-1` (skipping the first). Return the maximum of the two runs.
  2. **House Robber III:**
     - _What:_ Houses form a binary tree. You cannot rob directly linked parent and child nodes.
     - _How:_ Tree DP. Use a postorder DFS returning a tuple `(rob_this_node, skip_this_node)` at every node.
  3. **Delete and Earn:**
     - _What:_ If you take `x`, you must delete all `x-1` and `x+1`. Maximize your score.
     - _How:_ Convert the array to a frequency map or buckets where `buckets[x] = x * count`. The problem reduces _exactly_ to standard House Robber on the buckets array.
  4. **Paint House:**
     - _What:_ Choose 1 of 3 colors per house, adjacent houses can't have the same color. Minimize cost.
     - _How:_ Keep 3 states per step `(cost_red, cost_blue, cost_green)`. `new_red = cost_red + min(prev_blue, prev_green)`.
  5. **Maximum Alternating Subsequence Sum:**
     - _What:_ Maximize `nums[i0] - nums[i1] + nums[i2] - nums[i3]...`
     - _How:_ Keep two states `even_sum` and `odd_sum` at each step. Transition between them based on whether adding or subtracting the current element yields a higher sum.

---

## 2. Recursion & Backtracking

### 2.1 Permutations

- **What (The Problem & Goal):** Return all possible permutations of an array of distinct integers. A permutation is a specific arrangement of all elements.
- **How (Intuition & Mental Model):** Use DFS backtracking to build permutations incrementally. Keep a `path` array (current arrangement) and a `used` boolean array or set (to track which elements are already in the `path`). Loop through all numbers; if a number is not `used`, mark it as `used`, add it to `path`, recurse, then unmark it and pop it from `path` (the "backtrack" step).
- **Variants:**
  1. **Permutations II:**
     - _What:_ The array contains duplicates. Return all _unique_ permutations.
     - _How:_ Sort the array first. In the loop, skip the current number if `nums[i] == nums[i-1]` AND the previous identical number was NOT used in the current path (`used[i-1] == false`). This ensures duplicates are processed in a fixed order.
  2. **Next Permutation:**
     - _What:_ Find the lexicographically next permutation in-place, rather than generating all of them.
     - _How:_ Iterative approach. Find the rightmost descent (`nums[i] < nums[i+1]`). Swap `nums[i]` with the next larger element to its right, then reverse the entire suffix after `i`.
  3. **Letter Combinations of a Phone Number:**
     - _What:_ Given a string of digits, return all possible letter combinations (like a T9 phone keypad).
     - _How:_ Permutations across different sets of characters. At index `i` of the digits string, loop through the letters mapped to that digit, add to path, and recurse for `i+1`.
  4. **Combinations:**
     - _What:_ Choose `k` numbers out of `n`. Order doesn't matter (`(1,2)` is the same as `(2,1)`).
     - _How:_ Instead of a `used` array (which generates permutations), pass a `start_index` to the recursive function and loop from `start_index` to `n`. This prevents selecting elements in reverse order.
  5. **Permutation Sequence:**
     - _What:_ Find the exactly $K^{th}$ permutation mathematically without generating them all.
     - _How:_ A math-based approach using factorials is faster (e.g., the first digit is determined by `K / (n-1)!`). DFS with a global counter also works but is slower.

### 2.2 Combination Sum / Subsets

- **What (The Problem & Goal):** Find all unique combinations of numbers that sum to a target. Numbers can be reused infinitely.
- **How (Intuition & Mental Model):** DFS backtracking. Pass an `index` to the recursive function. To allow infinite reuse of the current number, recurse with the _same_ index. To prevent duplicate combinations like `[2,3]` and `[3,2]`, the loop in the recursive call only goes from the current `index` forward, never backward.
- **Variants:**
  1. **Combination Sum II:**
     - _What:_ Each number in the input array can only be used once, and the input may contain duplicates.
     - _How:_ Sort the input first. Skip duplicates at the same tree level using: `if i > start_index and nums[i] == nums[i-1]: continue`. Because elements can't be reused, recurse with `index + 1`.
  2. **Combination Sum III:**
     - _What:_ Find combinations of exactly `k` numbers that sum to `n` using only digits `1-9`.
     - _How:_ Exactly like Combination Sum II, but the input array is implicitly `[1, 2, 3, 4, 5, 6, 7, 8, 9]`. Stop recursion if the path length exceeds `k`.
  3. **Subsets:**
     - _What:_ Generate all possible subsets (the power set) of an array of unique integers.
     - _How:_ There is no target sum. Just add `path.copy()` to the result at _every single_ recursive call. Recurse with `index + 1`.
  4. **Subsets II:**
     - _What:_ Generate all unique subsets, but the input has duplicates.
     - _How:_ Sort first. Use the same duplicate-skipping logic as Combination Sum II (`if i > start and nums[i] == nums[i-1]`). Add `path.copy()` at every step.
  5. **Palindrome Partitioning:**
     - _What:_ Cut a string into substrings such that every substring is a palindrome.
     - _How:_ The `start_index` represents the start of the next substring. Loop `i` from `start_index` to the end. If `s[start_index:i+1]` is a palindrome, add it to the path and recurse on `i+1`.
  6. **Restore IP Addresses:**
     - _What:_ Cut a string of digits into 4 valid IP address parts.
     - _How:_ Backtrack while tracking the number of dots used. A segment is valid if it's between `0-255` and doesn't have leading zeros. Stop when 4 valid segments are formed.

### 2.3 Word Search

- **What (The Problem & Goal):** Find if a specific word exists in a 2D grid by connecting adjacent cells sequentially.
- **How (Intuition & Mental Model):** DFS from every cell in the grid that matches the first character. During the DFS, mark the current cell as visited (e.g., by changing it to `#`) so you don't use it twice. Recurse in 4 directions. If any recursive call returns `true`, propagate it up. If all 4 directions fail, restore the cell's original character (this is the backtracking step) and return `false`.
- **Variants:**
  1. **Word Search II:**
     - _What:_ Find _multiple_ words from a dictionary simultaneously.
     - _How:_ Brute force Word Search for each word will Time Out. Instead, build a **Trie** out of all the dictionary words. Run DFS on the board. Prune the DFS early if the current path's prefix doesn't exist in the Trie.
  2. **Number of Islands:**
     - _What:_ Count connected components of `1`s.
     - _How:_ Similar grid DFS, but there is _no backtracking_ to restore the state. Once a cell is visited and "sunk" (turned to `0`), it stays sunk forever.
  3. **Path with Maximum Gold:**
     - _What:_ Start at any cell, collect gold, never visit the same cell twice. Find the maximum total gold.
     - _How:_ Grid DFS returning the maximum sum. You _must_ backtrack (unmark visited cells) because you want to explore all possible valid paths from a cell, not just find a single path.
  4. **Unique Paths III:**
     - _What:_ Walk over every single empty square exactly once to reach the destination.
     - _How:_ First pass: count total empty squares and find the start cell. Second pass: DFS from start, keeping track of steps taken. Backtrack as usual. Return 1 (a valid path) only when `steps == total_empty` and `current_cell == END`.

---

## 3. Sliding Window & Two Pointers

### 3.1 Longest Substring Without Repeating Characters

- **What (The Problem & Goal):** Find the length of the longest continuous substring that contains no duplicate characters.
- **How (Intuition & Mental Model):** Use a sliding window `[left, right]`. Expand `right` character by character. Track the most recent index of every character using a Hash Map. If you encounter a character you've already seen, you must shrink the window. Instead of moving `left` one step at a time, instantly jump `left` to `max(left, map[char] + 1)`. Update the max length as `right - left + 1` at each step.
- **Variants:**
  1. **Longest Repeating Character Replacement:**
     - _What:_ You can change any character to another up to `k` times. Find the longest substring of a single repeating character.
     - _How:_ The valid condition is `window_len - max_freq_char <= k`. Keep a frequency map. If the condition is violated, shrink `left` by 1.
  2. **Max Consecutive Ones III:**
     - _What:_ Given a binary array, flip at most `k` `0`s to `1`s to get the longest contiguous array of `1`s.
     - _How:_ The condition is just `zero_count <= k`. Shrink `left` whenever the count exceeds `k`.
  3. **Subarrays with K Different Integers:**
     - _What:_ Count the number of subarrays with exactly `K` different integers.
     - _How:_ Finding _exactly_ `K` with a sliding window is hard because shrinking the window might not change the distinct count immediately. Instead, compute `atMost(K) - atMost(K-1)`.
  4. **Maximum Erasure Value:**
     - _What:_ Same as longest unique substring, but return the maximum _sum_ of the valid window instead of the length.
     - _How:_ Maintain a `window_sum` variable alongside the sliding window. Update the max sum whenever the window is valid.
  5. **Fruit Into Baskets:**
     - _What:_ Find the longest contiguous subarray with at most 2 distinct elements (fruit types).
     - _How:_ Exact same logic as "Longest Substring with At Most K Distinct Characters" where `k=2`. Use a frequency map and shrink `left` when the map size exceeds 2.

### 3.2 Minimum Window Substring

- **What (The Problem & Goal):** Find the smallest substring in a string `s` that contains all the characters (including duplicates) of a target string `t`.
- **How (Intuition & Mental Model):** Sliding window. Maintain a `need` frequency map of the target string, and a `have` count of characters currently fulfilling those needs. Expand `right` until `have == total_unique_needs`. Once the window is valid, record its size, then aggressively shrink `left` to make it smaller. Stop shrinking when the window becomes invalid, then resume expanding `right`.
- **Variants:**
  1. **Permutation in String:**
     - _What:_ Check if any permutation of `t` exists as a substring in `s`.
     - _How:_ Instead of a variable-length minimum window, the window size is strictly fixed to `len(t)`. Slide a fixed-size window across `s` and compare frequency maps (or just check if `have == need`).
  2. **Find All Anagrams in a String:**
     - _What:_ Find all start indices of anagrams (permutations) of `t` in `s`.
     - _How:_ Exactly the same as Permutation in String, but instead of returning `true`, you append the `left` index to an array every time the window is valid.
  3. **Substring with Concatenation of All Words:**
     - _What:_ Find all substrings that are a concatenation of all words in a given dictionary.
     - _How:_ Slide a window of fixed size `total_words * word_length`. Jump by `word_length` chunks instead of single characters.
  4. **Minimum Size Subarray Sum:**
     - _What:_ Find the minimum length of a contiguous subarray whose sum is `>= target`.
     - _How:_ Expand `right` until `window_sum >= target`. Once valid, record the length, then shrink `left` to minimize it. No frequency maps needed, just a running sum.

### 3.3 Trapping Rain Water

- **What (The Problem & Goal):** Given an array representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.
- **How (Intuition & Mental Model):** The water above any bar is determined by `min(max_height_left, max_height_right) - current_height`. Use two pointers (`left=0, right=n-1`). Maintain `left_max` and `right_max`. Since the water is bottlenecked by the _shorter_ of the two maximums, if `left_max < right_max`, we know the water at `left` is bounded by `left_max` safely, so we calculate it and advance `left`. Otherwise, we do the same for `right`.
- **Variants:**
  1. **Container With Most Water:**
     - _What:_ Find two vertical lines that, together with the x-axis, form a container that holds the most water.
     - _How:_ Two pointers (`left`, `right`). The area is `min(height[left], height[right]) * width`. Always advance the pointer pointing to the _shorter_ line because the height is bottlenecked by it, and moving the taller line can never increase the area.
  2. **Trapping Rain Water II:**
     - _What:_ 3D version on a 2D grid. Compute trapped water volume.
     - _How:_ A simple two-pointer approach fails. Use a Min-Heap starting with all perimeter cells. Pop the lowest cell (the "spill point"), process its neighbors, add trapped water if applicable, and push them to the heap with `max(current_height, neighbor_height)`.
  3. **Largest Rectangle in Histogram:**
     - _What:_ Find the area of the largest rectangle in a histogram.
     - _How:_ While two pointers expanding outwards from every bar works in O(N²), an O(N) solution requires a Monotonic Stack to track bars that are strictly increasing, computing area when a drop in height occurs.
  4. **Shortest Unsorted Continuous Subarray:**
     - _What:_ Find the shortest subarray that, if sorted, makes the whole array sorted.
     - _How:_ Find the bounds `left` and `right`. `left` is the first element out of order from the left, `right` is the first out of order from the right. Then find the min/max within that subarray and expand boundaries if elements outside are greater than the min or smaller than the max.

---

## 4. Graphs (BFS / DFS / Topo Sort)

### 4.1 Course Schedule (Topological Sort)

- **What (The Problem & Goal):** Given `n` courses and a list of prerequisites, can you finish all courses? This is essentially detecting if there is a cycle in a Directed Graph.
- **How (Intuition & Mental Model):** Use Kahn’s Algorithm (BFS). First, compute the `in-degree` (number of incoming prerequisite edges) for all nodes. Push all nodes with `in-degree == 0` (courses with no prerequisites) to a queue. Pop a node, append it to your completed list, and conceptually "remove" it by decrementing the in-degree of all its neighbors. If a neighbor's in-degree hits 0, push it to the queue. If the final completed list length `== n`, you successfully took all courses (no cycle).
- **Variants:**
  1. **Course Schedule II:**
     - _What:_ Return the actual ordering of courses instead of just a boolean feasibility check.
     - _How:_ Kahn's algorithm naturally builds this exact ordering in the completed list as it pops elements from the queue. Just return the list.
  2. **Alien Dictionary:**
     - _What:_ Given a list of alien words sorted lexicographically, derive the alphabet order.
     - _How:_ Compare adjacent words to find the _first_ differing character. This mismatch dictates a directed edge (`word1[i] -> word2[i]`). Build the graph with these edges, then run Topological Sort.
  3. **Find Eventual Safe States:**
     - _What:_ Find any node that eventually leads to a terminal node and cannot possibly enter a cycle.
     - _How:_ Reverse all graph edges. A terminal node now has an in-degree of 0. Run Kahn's algorithm. The nodes in the result list are the safe states.
  4. **Sequence Reconstruction:**
     - _What:_ Check if a given sequence is the ONLY valid topological sort for the graph.
     - _How:_ This is true if and only if the Kahn's algorithm queue size _never exceeds 1_ at any point. If it's `> 1`, there are multiple valid choices for the next node, meaning multiple valid topological sorts.
  5. **Parallel Courses:**
     - _What:_ Find the minimum number of semesters to finish courses if you can take independent courses in parallel.
     - _How:_ Topological sort, but instead of just checking feasibility, process the queue layer-by-layer (BFS style). Each layer represents one semester.

### 4.2 Rotting Oranges (Multi-source BFS)

- **What (The Problem & Goal):** Find the minimum time for all oranges on a grid to rot. A rotten orange spreads to 4-directional adjacent fresh oranges every minute.
- **How (Intuition & Mental Model):** This is a Multi-source BFS. Instead of starting BFS from one node, push ALL initially rotten oranges into the queue at distance (time) 0. Count the total number of fresh oranges. Run BFS layer by layer (minute by minute). For every fresh orange infected, decrement the fresh count. Return the total levels (minutes) if the fresh count hits 0, else return -1.
- **Variants:**
  1. **01 Matrix:**
     - _What:_ Find the distance of the nearest 0 for every cell in a matrix.
     - _How:_ Push all 0s to the queue initially with distance 0. Run BFS outwards to fill in distances for the 1s.
  2. **Walls and Gates:**
     - _What:_ Fill each empty room with the distance to its nearest gate.
     - _How:_ Push all gates to the queue initially. BFS outwards to fill the empty rooms.
  3. **Shortest Path in Binary Matrix:**
     - _What:_ Find the shortest clear path from top-left to bottom-right.
     - _How:_ Single-source BFS, but the trick is that movement is 8-directional instead of 4-directional.
  4. **As Far from Land as Possible:**
     - _What:_ Find a water cell (0) that is furthest from any land cell (1).
     - _How:_ Push all land cells (1s) to the queue initially. BFS outwards. The water cell that is reached _last_ in the BFS is the answer.
  5. **Pacific Atlantic Water Flow:**
     - _What:_ Find all grid coordinates where water can flow to both the Pacific (top/left) and Atlantic (bottom/right) oceans.
     - _How:_ Water flows _downhill_, so to find where it comes from, run BFS _uphill_ from the ocean borders. Run one multi-source BFS starting from all Pacific border cells, and another from all Atlantic border cells. The answer is the intersection of the two reachable sets.

---

## 5. Trees

### 5.1 Lowest Common Ancestor (LCA)

- **What (The Problem & Goal):** Find the lowest (deepest) node in a binary tree that is an ancestor to both node `p` and node `q`.
- **How (Intuition & Mental Model):** Postorder DFS. If the `root` is `p`, or `q`, or `None`, return `root`. Recurse on the left and right children. A node's left/right children will return either the target node they found, or `None`. If _both_ left and right return a non-null value, it means `p` is on one side and `q` is on the other, making the current node the LCA! If only one returns non-null, pass that non-null value up the chain.
- **Variants:**
  1. **LCA of a Binary Search Tree (BST):**
     - _What:_ Same problem, but you can leverage the BST property.
     - _How:_ If `p` and `q` are both `< root`, the LCA must be in the left subtree. If both are `> root`, it's in the right subtree. Otherwise (they split, or one equals the root), the current `root` is the LCA. This is O(H) without needing to traverse the whole tree.
  2. **LCA of a Binary Tree III:**
     - _What:_ The tree nodes have `parent` pointers. You are given `p` and `q`, but _not_ the `root`.
     - _How:_ Trace both nodes up to the root. This problem is perfectly identical to finding the "Intersection of Two Linked Lists".
  3. **Lowest Common Ancestor of a Binary Tree II:**
     - _What:_ `p` and `q` are not guaranteed to exist in the tree.
     - _How:_ The standard LCA algorithm assumes both exist. To handle missing nodes, you must traverse the _entire_ tree and track two boolean flags (`found_p` and `found_q`) during the DFS, only returning the LCA if both flags become true.
  4. **Lowest Common Ancestor of Deepest Leaves:**
     - _What:_ Find the LCA of the deepest leaves in the tree.
     - _How:_ DFS returning `(depth, node)`. Compare the left and right children. If `left_depth == right_depth`, the current node is the LCA of the deepest leaves. If `left_depth > right_depth`, the LCA is the left child's LCA, etc.

### 5.2 Binary Tree Maximum Path Sum

- **What (The Problem & Goal):** Find the maximum path sum between _any_ two nodes in a binary tree. The path does not need to go through the root.
- **How (Intuition & Mental Model):** This is classic Tree DP. A path between two nodes resembles an "arch". The highest point of this arch is some node `V`. For any node `V`, the max path sum where `V` is the highest point is `V.val + max(left_straight_path, 0) + max(right_straight_path, 0)`. We use a Postorder DFS. The recursive function computes and returns the max _straight_ path downwards to its parent. At the same time, it updates a global `max_sum` variable with the full "arch" path sum at the current node.
- **Variants:**
  1. **Diameter of Binary Tree:**
     - _What:_ Find the length of the longest path between any two nodes (counting edges, not node values).
     - _How:_ Exact same logic, but instead of adding node values, you are adding edges (1 per branch). The recursive function returns `1 + max(left, right)`. Update global max with `left + right`.
  2. **Longest Univalue Path:**
     - _What:_ Find the longest path where all nodes have the same value.
     - _How:_ Same logic, but you only include the left/right child's straight path if `child.val == root.val`. Otherwise, that side's straight path is reset to 0.
  3. **Binary Tree Cameras:**
     - _What:_ Place minimum cameras to monitor all nodes (a camera monitors itself, parent, and children).
     - _How:_ Postorder traversal returning a state for each node (0: needs camera, 1: has camera, 2: covered). Greedy placement: if any child returns 0 (needs camera), place a camera at the current parent.
  4. **Path Sum II:**
     - _What:_ Find all root-to-leaf paths that sum to a target.
     - _How:_ This uses Backtracking + Tree DFS rather than Postorder DP. Pass a `path` list down the tree, append the current node, check the sum at a leaf, and `pop()` before returning.

---

## 6. Arrays & Prefix Sums

### 6.1 Subarray Sum Equals K

- **What (The Problem & Goal):** Count the total number of continuous subarrays whose sum equals exactly `K`. The array can contain negative numbers.
- **How (Intuition & Mental Model):** Because of negative numbers, you _cannot_ use a Sliding Window (the sum doesn't monotonically increase as the window expands). Instead, use Prefix Sums and a Hash Map. Keep a `running_sum`. If `running_sum - K` exists in the map, it means there is some prefix earlier in the array that we can "chop off" to leave a subarray of exactly sum `K`. Add the frequency of `running_sum - K` to your total count. Then increment `map[running_sum]`. **Crucial Initialization:** Always initialize `map[0] = 1` to account for subarrays that start from index 0.
- **Variants:**
  1. **Subarray Sums Divisible by K:**
     - _What:_ Find the number of subarrays whose sum is divisible by `K`.
     - _How:_ Instead of storing the raw sum, store `running_sum % K` in the map. If you've seen the same modulo before, the subarray between the two points has a sum that is a multiple of `K`.
  2. **Contiguous Array:**
     - _What:_ Find the maximum length of a contiguous subarray with an equal number of `0`s and `1`s.
     - _How:_ Treat `0` as `-1` and `1` as `+1`. The problem reduces to finding the longest subarray with a sum of exactly `0`. Map `running_sum` to its `first_index_seen` to maximize length (`current_index - first_index_seen`).
  3. **Path Sum III:**
     - _What:_ Find all paths in a binary tree (going downwards) that sum to `K`.
     - _How:_ Apply the exact same prefix sum + map logic, but dynamically maintain the map during a DFS down the binary tree. Remember to backtrack (decrement map count) when returning from a recursive call.
  4. **Continuous Subarray Sum:**
     - _What:_ Check if there's a multiple of `K` subarray of size `>= 2`.
     - _How:_ Map `running_sum % k -> first_index_seen`. It is valid if `current_index - map[modulo] >= 2`.
  5. **Maximum Size Subarray Sum Equals k:**
     - _What:_ Find the maximum length of a subarray summing to exactly `k`.
     - _How:_ Map `running_sum -> first_index_seen`. If `running_sum - k` is in the map, update `max_len = max(max_len, current_index - map[running_sum - k])`.
  6. **Number of Submatrices That Sum to Target:**
     - _What:_ The 2D version. Count submatrices summing to a target.
     - _How:_ 2D Prefix Sum. Fix two rows (or cols) as top and bottom boundaries. Compress the columns between them into a 1D array. Then, apply exactly the 1D Subarray Sum Equals K hash map logic.

## Strategy for Interview Preparation

When studying, **group variants together**. Do not memorize solutions. Instead, memorize the **"Click Moment"** (e.g., "Any time I need to find subarrays with an exact sum and negatives exist, I cannot use sliding window; I must use Prefix Sum + Hash Map").
