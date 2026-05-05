# LeetCode Patterns, Solutions, and Variants

This document categorizes canonical LeetCode questions by topic. For each foundational problem, we provide the **Core Solution Logic** and a list of **Common Variants** that test the same underlying pattern with slight twists. Mastering the base problem allows you to solve all its variants.

---

## 1. Dynamic Programming (DP)

### 1.1 Longest Increasing Subsequence (LIS)
* **What (The Problem & Goal):** Given an unsorted integer array, find the length of the longest strictly increasing subsequence. A subsequence means elements don't need to be contiguous, but they must maintain their original relative order.
* **How (Intuition & Mental Model):**
  - **O(N²) DP Approach:** Ask "what is the longest sequence *ending at* the current element?" For each element, look back at all previous elements that are strictly smaller. The longest sequence you can form is the longest valid previous sequence + 1.
  - **O(N log N) Patience Sorting Approach:** Imagine building piles of cards where you can only place a smaller card on top of a larger one. If no such pile exists, start a new pile to the right. The number of piles equals the LIS length. In code, maintain an array of the "smallest tail element" for each possible length. Because this array naturally stays sorted, you can use Binary Search to find the exact placement for each new element.
* **Variants:**
  1. **Number of Longest Increasing Subsequence:** 
     - *What:* Return the total *count* of longest increasing subsequences, not just the length.
     - *How:* Maintain a parallel `counts[i]` array alongside `dp[i]`. If you find a new max length, inherit the count. If you tie an existing max length, add the count.
  2. **Russian Doll Envelopes:** 
     - *What:* Fit envelopes inside each other (both width and height must be strictly greater).
     - *How:* Sort by width ascending, then height descending. The problem reduces to finding the 1D LIS on the heights. The descending height sort prevents envelopes of the same width from fitting into each other.
  3. **Maximum Length of Pair Chain:**
     - *What:* Chain pairs `(a,b)` and `(c,d)` where `b < c`.
     - *How:* Similar to LIS, but sort pairs by their second coordinate and greedily pick non-overlapping pairs.
  4. **Longest Bitonic Subsequence:**
     - *What:* Find the longest sequence that strictly increases, then strictly decreases.
     - *How:* Compute LIS from left to right, and LIS from right to left, then find the `max(left[i] + right[i] - 1)` at every index.
  5. **Largest Divisible Subset:**
     - *What:* Find the largest subset where every pair `(i, j)` satisfies `i % j == 0` or `j % i == 0`.
     - *How:* Sort the array first. The condition becomes `nums[i] % nums[j] == 0`. Maintain a `parent` array to reconstruct the actual subset, transitioning if modulo is zero.
  6. **Minimum Number of Removals to Make Mountain Array:**
     - *What:* Remove the minimum elements so the array strictly increases then strictly decreases.
     - *How:* Exactly the same logic as Longest Bitonic Subsequence; just subtract the bitonic length from the total length.

### 1.2 Coin Change (Unbounded Knapsack)
* **What (The Problem & Goal):** Find the minimum number of coins needed to make up a target amount. You have an infinite supply of each coin denomination.
* **How (Intuition & Mental Model):** To find the minimum coins for `amount`, look at `amount - coin_value`. The answer is `1 + minimum_coins(amount - coin_value)`. We build a DP array of size `amount + 1` initialized to infinity. `dp[0] = 0`. For each coin, we update all reachable amounts.
* **Variants:**
  1. **Coin Change II:** 
     - *What:* Find the *number of combinations* that make up that amount, rather than the minimum coins.
     - *How:* `dp[x] += dp[x - coin]`. You are accumulating paths, not finding a minimum.
  2. **Perfect Squares:**
     - *What:* Least number of perfect square numbers (`1, 4, 9...`) that sum to `n`.
     - *How:* The "coins" are just pre-calculated perfect squares `1, 4, 9, 16...`. The DP logic is exactly the same as Coin Change.
  3. **Combination Sum IV:**
     - *What:* Same as Coin Change II but permutations matter (`(1,2)` is different from `(2,1)`).
     - *How:* The loop order is inverted: loop over `amount` first, then `coins`. This allows different coin sequences to be counted as unique permutations.
  4. **Minimum Cost For Tickets:**
     - *What:* Find the minimum cost to travel on specific days given 1-day, 7-day, and 30-day passes.
     - *How:* Similar state transition `dp[day] = min(cost + dp[day - pass_duration])`, but the "coins" (passes) have different coverages instead of simple values. If you don't travel on a day, `dp[day] = dp[day-1]`.
  5. **Integer Break:**
     - *What:* Maximize the product of an array of integers that sum to `n`.
     - *How:* This is an unbounded knapsack where both the "weights" and "values" are the integers `1` to `n-1`. Try breaking `n` into `i` and `n-i`.

### 1.3 House Robber (1D DP / State Machine)
* **What (The Problem & Goal):** Maximize the money robbed from an array of houses, with the constraint that you cannot rob two adjacent houses.
* **How (Intuition & Mental Model):** At any house `i`, you have two choices: Rob it (which means you add its value to the max profit from house `i-2`) OR Skip it (which means you keep the max profit from house `i-1`). The transition is `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`. This can be optimized to O(1) space by only tracking `rob1` (i-2) and `rob2` (i-1).
* **Variants:**
  1. **House Robber II:**
     - *What:* Houses are arranged in a circle, so the first and last houses are adjacent.
     - *How:* Run the core algorithm twice: once from `0` to `n-2` (skipping the last house) and once from `1` to `n-1` (skipping the first). Return the maximum of the two runs.
  2. **House Robber III:**
     - *What:* Houses form a binary tree. You cannot rob directly linked parent and child nodes.
     - *How:* Tree DP. Use a postorder DFS returning a tuple `(rob_this_node, skip_this_node)` at every node.
  3. **Delete and Earn:**
     - *What:* If you take `x`, you must delete all `x-1` and `x+1`. Maximize your score.
     - *How:* Convert the array to a frequency map or buckets where `buckets[x] = x * count`. The problem reduces *exactly* to standard House Robber on the buckets array.
  4. **Paint House:**
     - *What:* Choose 1 of 3 colors per house, adjacent houses can't have the same color. Minimize cost.
     - *How:* Keep 3 states per step `(cost_red, cost_blue, cost_green)`. `new_red = cost_red + min(prev_blue, prev_green)`.
  5. **Maximum Alternating Subsequence Sum:**
     - *What:* Maximize `nums[i0] - nums[i1] + nums[i2] - nums[i3]...`
     - *How:* Keep two states `even_sum` and `odd_sum` at each step. Transition between them based on whether adding or subtracting the current element yields a higher sum.

---

## 2. Recursion & Backtracking

### 2.1 Permutations
* **What (The Problem & Goal):** Return all possible permutations of an array of distinct integers. A permutation is a specific arrangement of all elements.
* **How (Intuition & Mental Model):** Use DFS backtracking to build permutations incrementally. Keep a `path` array (current arrangement) and a `used` boolean array or set (to track which elements are already in the `path`). Loop through all numbers; if a number is not `used`, mark it as `used`, add it to `path`, recurse, then unmark it and pop it from `path` (the "backtrack" step).
* **Variants:**
  1. **Permutations II:** 
     - *What:* The array contains duplicates. Return all *unique* permutations.
     - *How:* Sort the array first. In the loop, skip the current number if `nums[i] == nums[i-1]` AND the previous identical number was NOT used in the current path (`used[i-1] == false`). This ensures duplicates are processed in a fixed order.
  2. **Next Permutation:**
     - *What:* Find the lexicographically next permutation in-place, rather than generating all of them.
     - *How:* Iterative approach. Find the rightmost descent (`nums[i] < nums[i+1]`). Swap `nums[i]` with the next larger element to its right, then reverse the entire suffix after `i`.
  3. **Letter Combinations of a Phone Number:**
     - *What:* Given a string of digits, return all possible letter combinations (like a T9 phone keypad).
     - *How:* Permutations across different sets of characters. At index `i` of the digits string, loop through the letters mapped to that digit, add to path, and recurse for `i+1`.
  4. **Combinations:**
     - *What:* Choose `k` numbers out of `n`. Order doesn't matter (`(1,2)` is the same as `(2,1)`).
     - *How:* Instead of a `used` array (which generates permutations), pass a `start_index` to the recursive function and loop from `start_index` to `n`. This prevents selecting elements in reverse order.
  5. **Permutation Sequence:**
     - *What:* Find the exactly $K^{th}$ permutation mathematically without generating them all.
     - *How:* A math-based approach using factorials is faster (e.g., the first digit is determined by `K / (n-1)!`). DFS with a global counter also works but is slower.

### 2.2 Combination Sum / Subsets
* **What (The Problem & Goal):** Find all unique combinations of numbers that sum to a target. Numbers can be reused infinitely.
* **How (Intuition & Mental Model):** DFS backtracking. Pass an `index` to the recursive function. To allow infinite reuse of the current number, recurse with the *same* index. To prevent duplicate combinations like `[2,3]` and `[3,2]`, the loop in the recursive call only goes from the current `index` forward, never backward.
* **Variants:**
  1. **Combination Sum II:**
     - *What:* Each number in the input array can only be used once, and the input may contain duplicates.
     - *How:* Sort the input first. Skip duplicates at the same tree level using: `if i > start_index and nums[i] == nums[i-1]: continue`. Because elements can't be reused, recurse with `index + 1`.
  2. **Combination Sum III:**
     - *What:* Find combinations of exactly `k` numbers that sum to `n` using only digits `1-9`.
     - *How:* Exactly like Combination Sum II, but the input array is implicitly `[1, 2, 3, 4, 5, 6, 7, 8, 9]`. Stop recursion if the path length exceeds `k`.
  3. **Subsets:**
     - *What:* Generate all possible subsets (the power set) of an array of unique integers.
     - *How:* There is no target sum. Just add `path.copy()` to the result at *every single* recursive call. Recurse with `index + 1`.
  4. **Subsets II:**
     - *What:* Generate all unique subsets, but the input has duplicates.
     - *How:* Sort first. Use the same duplicate-skipping logic as Combination Sum II (`if i > start and nums[i] == nums[i-1]`). Add `path.copy()` at every step.
  5. **Palindrome Partitioning:**
     - *What:* Cut a string into substrings such that every substring is a palindrome.
     - *How:* The `start_index` represents the start of the next substring. Loop `i` from `start_index` to the end. If `s[start_index:i+1]` is a palindrome, add it to the path and recurse on `i+1`.
  6. **Restore IP Addresses:**
     - *What:* Cut a string of digits into 4 valid IP address parts.
     - *How:* Backtrack while tracking the number of dots used. A segment is valid if it's between `0-255` and doesn't have leading zeros. Stop when 4 valid segments are formed.

### 2.3 Word Search
* **What (The Problem & Goal):** Find if a specific word exists in a 2D grid by connecting adjacent cells sequentially.
* **How (Intuition & Mental Model):** DFS from every cell in the grid that matches the first character. During the DFS, mark the current cell as visited (e.g., by changing it to `#`) so you don't use it twice. Recurse in 4 directions. If any recursive call returns `true`, propagate it up. If all 4 directions fail, restore the cell's original character (this is the backtracking step) and return `false`.
* **Variants:**
  1. **Word Search II:**
     - *What:* Find *multiple* words from a dictionary simultaneously.
     - *How:* Brute force Word Search for each word will Time Out. Instead, build a **Trie** out of all the dictionary words. Run DFS on the board. Prune the DFS early if the current path's prefix doesn't exist in the Trie.
  2. **Number of Islands:**
     - *What:* Count connected components of `1`s.
     - *How:* Similar grid DFS, but there is *no backtracking* to restore the state. Once a cell is visited and "sunk" (turned to `0`), it stays sunk forever.
  3. **Path with Maximum Gold:**
     - *What:* Start at any cell, collect gold, never visit the same cell twice. Find the maximum total gold.
     - *How:* Grid DFS returning the maximum sum. You *must* backtrack (unmark visited cells) because you want to explore all possible valid paths from a cell, not just find a single path.
  4. **Unique Paths III:**
     - *What:* Walk over every single empty square exactly once to reach the destination.
     - *How:* First pass: count total empty squares and find the start cell. Second pass: DFS from start, keeping track of steps taken. Backtrack as usual. Return 1 (a valid path) only when `steps == total_empty` and `current_cell == END`.

---

## 3. Sliding Window & Two Pointers

### 3.1 Longest Substring Without Repeating Characters
* **What (The Problem & Goal):** Find the length of the longest continuous substring that contains no duplicate characters.
* **How (Intuition & Mental Model):** Use a sliding window `[left, right]`. Expand `right` character by character. Track the most recent index of every character using a Hash Map. If you encounter a character you've already seen, you must shrink the window. Instead of moving `left` one step at a time, instantly jump `left` to `max(left, map[char] + 1)`. Update the max length as `right - left + 1` at each step.
* **Variants:**
  1. **Longest Repeating Character Replacement:**
     - *What:* You can change any character to another up to `k` times. Find the longest substring of a single repeating character.
     - *How:* The valid condition is `window_len - max_freq_char <= k`. Keep a frequency map. If the condition is violated, shrink `left` by 1.
  2. **Max Consecutive Ones III:**
     - *What:* Given a binary array, flip at most `k` `0`s to `1`s to get the longest contiguous array of `1`s.
     - *How:* The condition is just `zero_count <= k`. Shrink `left` whenever the count exceeds `k`.
  3. **Subarrays with K Different Integers:**
     - *What:* Count the number of subarrays with exactly `K` different integers.
     - *How:* Finding *exactly* `K` with a sliding window is hard because shrinking the window might not change the distinct count immediately. Instead, compute `atMost(K) - atMost(K-1)`.
  4. **Maximum Erasure Value:**
     - *What:* Same as longest unique substring, but return the maximum *sum* of the valid window instead of the length.
     - *How:* Maintain a `window_sum` variable alongside the sliding window. Update the max sum whenever the window is valid.
  5. **Fruit Into Baskets:**
     - *What:* Find the longest contiguous subarray with at most 2 distinct elements (fruit types).
     - *How:* Exact same logic as "Longest Substring with At Most K Distinct Characters" where `k=2`. Use a frequency map and shrink `left` when the map size exceeds 2.

### 3.2 Minimum Window Substring
* **What (The Problem & Goal):** Find the smallest substring in a string `s` that contains all the characters (including duplicates) of a target string `t`.
* **How (Intuition & Mental Model):** Sliding window. Maintain a `need` frequency map of the target string, and a `have` count of characters currently fulfilling those needs. Expand `right` until `have == total_unique_needs`. Once the window is valid, record its size, then aggressively shrink `left` to make it smaller. Stop shrinking when the window becomes invalid, then resume expanding `right`.
* **Variants:**
  1. **Permutation in String:**
     - *What:* Check if any permutation of `t` exists as a substring in `s`.
     - *How:* Instead of a variable-length minimum window, the window size is strictly fixed to `len(t)`. Slide a fixed-size window across `s` and compare frequency maps (or just check if `have == need`).
  2. **Find All Anagrams in a String:**
     - *What:* Find all start indices of anagrams (permutations) of `t` in `s`.
     - *How:* Exactly the same as Permutation in String, but instead of returning `true`, you append the `left` index to an array every time the window is valid.
  3. **Substring with Concatenation of All Words:**
     - *What:* Find all substrings that are a concatenation of all words in a given dictionary.
     - *How:* Slide a window of fixed size `total_words * word_length`. Jump by `word_length` chunks instead of single characters.
  4. **Minimum Size Subarray Sum:**
     - *What:* Find the minimum length of a contiguous subarray whose sum is `>= target`.
     - *How:* Expand `right` until `window_sum >= target`. Once valid, record the length, then shrink `left` to minimize it. No frequency maps needed, just a running sum.

### 3.3 Trapping Rain Water
* **What (The Problem & Goal):** Given an array representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.
* **How (Intuition & Mental Model):** The water above any bar is determined by `min(max_height_left, max_height_right) - current_height`. Use two pointers (`left=0, right=n-1`). Maintain `left_max` and `right_max`. Since the water is bottlenecked by the *shorter* of the two maximums, if `left_max < right_max`, we know the water at `left` is bounded by `left_max` safely, so we calculate it and advance `left`. Otherwise, we do the same for `right`.
* **Variants:**
  1. **Container With Most Water:**
     - *What:* Find two vertical lines that, together with the x-axis, form a container that holds the most water.
     - *How:* Two pointers (`left`, `right`). The area is `min(height[left], height[right]) * width`. Always advance the pointer pointing to the *shorter* line because the height is bottlenecked by it, and moving the taller line can never increase the area.
  2. **Trapping Rain Water II:**
     - *What:* 3D version on a 2D grid. Compute trapped water volume.
     - *How:* A simple two-pointer approach fails. Use a Min-Heap starting with all perimeter cells. Pop the lowest cell (the "spill point"), process its neighbors, add trapped water if applicable, and push them to the heap with `max(current_height, neighbor_height)`.
  3. **Largest Rectangle in Histogram:**
     - *What:* Find the area of the largest rectangle in a histogram.
     - *How:* While two pointers expanding outwards from every bar works in O(N²), an O(N) solution requires a Monotonic Stack to track bars that are strictly increasing, computing area when a drop in height occurs.
  4. **Shortest Unsorted Continuous Subarray:**
     - *What:* Find the shortest subarray that, if sorted, makes the whole array sorted.
     - *How:* Find the bounds `left` and `right`. `left` is the first element out of order from the left, `right` is the first out of order from the right. Then find the min/max within that subarray and expand boundaries if elements outside are greater than the min or smaller than the max.

---

## 4. Graphs (BFS / DFS / Topo Sort)

### 4.1 Course Schedule (Topological Sort)
* **What (The Problem & Goal):** Given `n` courses and a list of prerequisites, can you finish all courses? This is essentially detecting if there is a cycle in a Directed Graph.
* **How (Intuition & Mental Model):** Use Kahn’s Algorithm (BFS). First, compute the `in-degree` (number of incoming prerequisite edges) for all nodes. Push all nodes with `in-degree == 0` (courses with no prerequisites) to a queue. Pop a node, append it to your completed list, and conceptually "remove" it by decrementing the in-degree of all its neighbors. If a neighbor's in-degree hits 0, push it to the queue. If the final completed list length `== n`, you successfully took all courses (no cycle).
* **Variants:**
  1. **Course Schedule II:**
     - *What:* Return the actual ordering of courses instead of just a boolean feasibility check.
     - *How:* Kahn's algorithm naturally builds this exact ordering in the completed list as it pops elements from the queue. Just return the list.
  2. **Alien Dictionary:**
     - *What:* Given a list of alien words sorted lexicographically, derive the alphabet order.
     - *How:* Compare adjacent words to find the *first* differing character. This mismatch dictates a directed edge (`word1[i] -> word2[i]`). Build the graph with these edges, then run Topological Sort.
  3. **Find Eventual Safe States:**
     - *What:* Find any node that eventually leads to a terminal node and cannot possibly enter a cycle.
     - *How:* Reverse all graph edges. A terminal node now has an in-degree of 0. Run Kahn's algorithm. The nodes in the result list are the safe states.
  4. **Sequence Reconstruction:**
     - *What:* Check if a given sequence is the ONLY valid topological sort for the graph.
     - *How:* This is true if and only if the Kahn's algorithm queue size *never exceeds 1* at any point. If it's `> 1`, there are multiple valid choices for the next node, meaning multiple valid topological sorts.
  5. **Parallel Courses:**
     - *What:* Find the minimum number of semesters to finish courses if you can take independent courses in parallel.
     - *How:* Topological sort, but instead of just checking feasibility, process the queue layer-by-layer (BFS style). Each layer represents one semester.

### 4.2 Rotting Oranges (Multi-source BFS)
* **What (The Problem & Goal):** Find the minimum time for all oranges on a grid to rot. A rotten orange spreads to 4-directional adjacent fresh oranges every minute.
* **How (Intuition & Mental Model):** This is a Multi-source BFS. Instead of starting BFS from one node, push ALL initially rotten oranges into the queue at distance (time) 0. Count the total number of fresh oranges. Run BFS layer by layer (minute by minute). For every fresh orange infected, decrement the fresh count. Return the total levels (minutes) if the fresh count hits 0, else return -1.
* **Variants:**
  1. **01 Matrix:**
     - *What:* Find the distance of the nearest 0 for every cell in a matrix.
     - *How:* Push all 0s to the queue initially with distance 0. Run BFS outwards to fill in distances for the 1s.
  2. **Walls and Gates:**
     - *What:* Fill each empty room with the distance to its nearest gate.
     - *How:* Push all gates to the queue initially. BFS outwards to fill the empty rooms.
  3. **Shortest Path in Binary Matrix:**
     - *What:* Find the shortest clear path from top-left to bottom-right.
     - *How:* Single-source BFS, but the trick is that movement is 8-directional instead of 4-directional.
  4. **As Far from Land as Possible:**
     - *What:* Find a water cell (0) that is furthest from any land cell (1).
     - *How:* Push all land cells (1s) to the queue initially. BFS outwards. The water cell that is reached *last* in the BFS is the answer.
  5. **Pacific Atlantic Water Flow:**
     - *What:* Find all grid coordinates where water can flow to both the Pacific (top/left) and Atlantic (bottom/right) oceans.
     - *How:* Water flows *downhill*, so to find where it comes from, run BFS *uphill* from the ocean borders. Run one multi-source BFS starting from all Pacific border cells, and another from all Atlantic border cells. The answer is the intersection of the two reachable sets.

---

## 5. Trees

### 5.1 Lowest Common Ancestor (LCA)
* **What (The Problem & Goal):** Find the lowest (deepest) node in a binary tree that is an ancestor to both node `p` and node `q`.
* **How (Intuition & Mental Model):** Postorder DFS. If the `root` is `p`, or `q`, or `None`, return `root`. Recurse on the left and right children. A node's left/right children will return either the target node they found, or `None`. If *both* left and right return a non-null value, it means `p` is on one side and `q` is on the other, making the current node the LCA! If only one returns non-null, pass that non-null value up the chain.
* **Variants:**
  1. **LCA of a Binary Search Tree (BST):**
     - *What:* Same problem, but you can leverage the BST property.
     - *How:* If `p` and `q` are both `< root`, the LCA must be in the left subtree. If both are `> root`, it's in the right subtree. Otherwise (they split, or one equals the root), the current `root` is the LCA. This is O(H) without needing to traverse the whole tree.
  2. **LCA of a Binary Tree III:**
     - *What:* The tree nodes have `parent` pointers. You are given `p` and `q`, but *not* the `root`.
     - *How:* Trace both nodes up to the root. This problem is perfectly identical to finding the "Intersection of Two Linked Lists".
  3. **Lowest Common Ancestor of a Binary Tree II:**
     - *What:* `p` and `q` are not guaranteed to exist in the tree.
     - *How:* The standard LCA algorithm assumes both exist. To handle missing nodes, you must traverse the *entire* tree and track two boolean flags (`found_p` and `found_q`) during the DFS, only returning the LCA if both flags become true.
  4. **Lowest Common Ancestor of Deepest Leaves:**
     - *What:* Find the LCA of the deepest leaves in the tree.
     - *How:* DFS returning `(depth, node)`. Compare the left and right children. If `left_depth == right_depth`, the current node is the LCA of the deepest leaves. If `left_depth > right_depth`, the LCA is the left child's LCA, etc.

### 5.2 Binary Tree Maximum Path Sum
* **What (The Problem & Goal):** Find the maximum path sum between *any* two nodes in a binary tree. The path does not need to go through the root.
* **How (Intuition & Mental Model):** This is classic Tree DP. A path between two nodes resembles an "arch". The highest point of this arch is some node `V`. For any node `V`, the max path sum where `V` is the highest point is `V.val + max(left_straight_path, 0) + max(right_straight_path, 0)`. We use a Postorder DFS. The recursive function computes and returns the max *straight* path downwards to its parent. At the same time, it updates a global `max_sum` variable with the full "arch" path sum at the current node.
* **Variants:**
  1. **Diameter of Binary Tree:**
     - *What:* Find the length of the longest path between any two nodes (counting edges, not node values).
     - *How:* Exact same logic, but instead of adding node values, you are adding edges (1 per branch). The recursive function returns `1 + max(left, right)`. Update global max with `left + right`.
  2. **Longest Univalue Path:**
     - *What:* Find the longest path where all nodes have the same value.
     - *How:* Same logic, but you only include the left/right child's straight path if `child.val == root.val`. Otherwise, that side's straight path is reset to 0.
  3. **Binary Tree Cameras:**
     - *What:* Place minimum cameras to monitor all nodes (a camera monitors itself, parent, and children).
     - *How:* Postorder traversal returning a state for each node (0: needs camera, 1: has camera, 2: covered). Greedy placement: if any child returns 0 (needs camera), place a camera at the current parent.
  4. **Path Sum II:**
     - *What:* Find all root-to-leaf paths that sum to a target.
     - *How:* This uses Backtracking + Tree DFS rather than Postorder DP. Pass a `path` list down the tree, append the current node, check the sum at a leaf, and `pop()` before returning.

---

## 6. Arrays & Prefix Sums

### 6.1 Subarray Sum Equals K
* **What (The Problem & Goal):** Count the total number of continuous subarrays whose sum equals exactly `K`. The array can contain negative numbers.
* **How (Intuition & Mental Model):** Because of negative numbers, you *cannot* use a Sliding Window (the sum doesn't monotonically increase as the window expands). Instead, use Prefix Sums and a Hash Map. Keep a `running_sum`. If `running_sum - K` exists in the map, it means there is some prefix earlier in the array that we can "chop off" to leave a subarray of exactly sum `K`. Add the frequency of `running_sum - K` to your total count. Then increment `map[running_sum]`. **Crucial Initialization:** Always initialize `map[0] = 1` to account for subarrays that start from index 0.
* **Variants:**
  1. **Subarray Sums Divisible by K:**
     - *What:* Find the number of subarrays whose sum is divisible by `K`.
     - *How:* Instead of storing the raw sum, store `running_sum % K` in the map. If you've seen the same modulo before, the subarray between the two points has a sum that is a multiple of `K`.
  2. **Contiguous Array:**
     - *What:* Find the maximum length of a contiguous subarray with an equal number of `0`s and `1`s.
     - *How:* Treat `0` as `-1` and `1` as `+1`. The problem reduces to finding the longest subarray with a sum of exactly `0`. Map `running_sum` to its `first_index_seen` to maximize length (`current_index - first_index_seen`).
  3. **Path Sum III:**
     - *What:* Find all paths in a binary tree (going downwards) that sum to `K`.
     - *How:* Apply the exact same prefix sum + map logic, but dynamically maintain the map during a DFS down the binary tree. Remember to backtrack (decrement map count) when returning from a recursive call.
  4. **Continuous Subarray Sum:**
     - *What:* Check if there's a multiple of `K` subarray of size `>= 2`.
     - *How:* Map `running_sum % k -> first_index_seen`. It is valid if `current_index - map[modulo] >= 2`.
  5. **Maximum Size Subarray Sum Equals k:**
     - *What:* Find the maximum length of a subarray summing to exactly `k`.
     - *How:* Map `running_sum -> first_index_seen`. If `running_sum - k` is in the map, update `max_len = max(max_len, current_index - map[running_sum - k])`.
  6. **Number of Submatrices That Sum to Target:**
     - *What:* The 2D version. Count submatrices summing to a target.
     - *How:* 2D Prefix Sum. Fix two rows (or cols) as top and bottom boundaries. Compress the columns between them into a 1D array. Then, apply exactly the 1D Subarray Sum Equals K hash map logic.

## Strategy for Interview Preparation
When studying, **group variants together**. Do not memorize solutions. Instead, memorize the **"Click Moment"** (e.g., "Any time I need to find subarrays with an exact sum and negatives exist, I cannot use sliding window; I must use Prefix Sum + Hash Map").
