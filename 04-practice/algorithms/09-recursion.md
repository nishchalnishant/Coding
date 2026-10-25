---
tags: [coding, algorithms, recursion]
topic: Recursion & Backtracking
difficulty: mixed
---
# Recursion & Backtracking — Problem Reference by Pattern

## What this covers

> [!abstract] In this file
> **Covers:** Worked recursion problems by pattern: include/exclude, divide & conquer, pruning, graph recursion, memoized recursion, recursive parsing.
> **You'll be able to:** Write recursive solutions from the contract, not by tracing.
> **Prereqs:** Recursion lecture · **Pair with:** [Recursion lecture](../../02-algorithms/09-recursion.md) · **Time:** 3 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/l3-google-roadmap.md#tier-legend))

**Sections:** [Foundation — Include/Exclude](#foundation--includeexclude) · [Divide and Conquer (via Recursion)](#divide-and-conquer-via-recursion) · [Pruning & Constraints](#pruning--constraints) · [Foundation — Recursion Fundamentals](#foundation--recursion-fundamentals) · [Recursive Parsing / Evaluation](#recursive-parsing--evaluation) · [Graph — Recursive Traversal](#graph--recursive-traversal) · [Dynamic Programming Foundations (Recursive + Memo)](#dynamic-programming-foundations-recursive--memo)

> [!tip] If you only have 20 minutes
> **Do these first:** [Merge Sort](#merge-sort--t2) · [Pow(x, n) — Fast Exponentiation](#powx-n--fast-exponentiation) · [Construct Binary Tree from Preorder and Inorder Traversal](#construct-binary-tree-from-preorder-and-inorder-traversal-lc-105--t2) · [Serialize and Deserialize Binary Tree](#serialize-and-deserialize-binary-tree-lc-297--t2) · [Subsets II](#subsets-ii-lc-90--t2) · [Permutations II](#permutations-ii-lc-47--t2) · [Word Search (Grid Backtracking)](#word-search-grid-backtracking--t1) · [Number of Islands](#number-of-islands-lc-200--t1) · [Decode String (Recursive)](#decode-string-recursive)
> **Template:** Trust the call: define `f(x)` in one sentence, handle the base case, assume `f(smaller)` works, combine.
> **Template:** Fast power: `half = pow(x, n // 2); return half * half * (x if n % 2 else 1)`; negative `n` → `1 / pow(x, -n)`.
> **Gotchas:** Missing/incorrect base case is the #1 bug · Python recursion limit ~1000 — mention `sys.setrecursionlimit` or iterative · recompute overlap ⇒ memoize (→ DP) · pass indices, not slices, to keep O(n) not O(n²).

---

> [!info] First Principles
> Recursion reduces a problem to a smaller identical subproblem; the call stack manages state across levels. Backtracking = DFS over a decision tree — "make choice → recurse → undo choice". The invariant at every recursive call: the partial solution satisfies all constraints imposed so far. Complexity: subsets O(2^n · n), permutations O(n! · n), combinations O(C(n,k) · k).

---

## Foundation — Include/Exclude

---

### Binary Tree Paths

> [!example] Problem
> Given the root of a binary tree, return all root-to-leaf paths in any order.
> A leaf is a node with no children.
> 
> **Example 1:**
> ```
> Input: root = [1,2,3,null,5]
> Output: ["1->2->5","1->3"]
> ```
> 
> **Example 2:**
> ```
> Input: root = [1]
> Output: ["1"]
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [1, 100].
> - -100 <= Node.val <= 100

> [!tip] Recognize · Gotcha
> **Signal:** "all root-to-leaf paths" · **Gotcha:** Leaf = no left AND no right

> [!info] Approach
> Tree structure is inherently recursive; each subtree is a smaller instance of the same problem. No backtracking needed since strings are immutable (pass by value). DFS from root; accumulate path string; record when leaf is reached. Base case = leaf node → append path to result. Recursive case = recurse left and right with extended path string.

> [!note]- Python Solution
> ```python
> def binary_tree_paths(root):
>     result = []
> 
>     def dfs(node, path):
>         if not node:
>             return
>         path = path + ('->' if path else '') + str(node.val)
>         if not node.left and not node.right:
>             result.append(path)
>         else:
>             dfs(node.left, path)
>             dfs(node.right, path)
> 
>     dfs(root, '')
>     return result
> ```

> [!success] Complexity
> Time O(n · h) where h is height (string concatenation cost per level). Space O(h) call stack.

> [!tip] Alternatives
> Use a list as path and join at leaf — amortizes string cost. Iterative BFS with (node, path) tuples.

---

## Divide and Conquer (via Recursion)

---

### Merge Sort `🎯 T2`

> [!example] Problem
> Sort an array in O(n log n) using divide and conquer.

> [!info] Approach
> Sorting n items can be decomposed into sorting two halves independently (no overlap between halves) and merging in O(n). Recursion handles the split; the merge step is the key. Split array at midpoint, sort each half recursively, merge the two sorted halves. Base case = length ≤ 1. Split, conquer left, conquer right, merge in O(n) with two-pointer technique.

> [!note]- Python Solution
> ```python
> def merge_sort(nums):
>     if len(nums) <= 1:
>         return nums
>     mid = len(nums) // 2
>     left = mergeSort(nums[:mid])
>     right = mergeSort(nums[mid:])
>     return merge(left, right)
> 
> def merge(left, right):
>     result = []
>     i = j = 0
>     while i < len(left) and j < len(right):
>         if left[i] <= right[j]:
>             result.append(left[i])
>             i += 1
>         else:
>             result.append(right[j])
>             j += 1
>     result.extend(left[i:])
>     result.extend(right[j:])
>     return result
> ```

> [!success] Complexity
> Time O(n log n) — Master Theorem T(n) = 2T(n/2) + O(n), Case 2. Space O(n) merge buffer + O(log n) stack.

> [!tip] Alternatives
> Bottom-up iterative merge sort avoids O(log n) stack. TimSort (Python's sort) adds galloping for real-world speedups.

---

### Fibonacci (Memoized Recursion vs DP)

> [!example] Problem
> Compute the nth Fibonacci number.

> [!info] Approach
> Naive recursion `f(n) = f(n-1) + f(n-2)` recomputes the same `k` over and over. Cache each `n` in a dict once → O(n). Same idea as bottom-up DP; iterative version can use O(1) space with two variables.

> [!note]- Python Solution
> ```python
> # Top-down — memo dict
> def fib_memo(n):
>     memo = {}
>
>     def f(n):
>         if n in memo:
>             return memo[n]
>         if n <= 1:
>             return n
>         memo[n] = f(n - 1) + f(n - 2)
>         return memo[n]
>
>     return f(n)
>
> # Bottom-up — O(1) space
> def fib_dp(n):
>     if n <= 1:
>         return n
>     two_back, one_back = 0, 1
>     for _ in range(2, n + 1):
>         two_back, one_back = one_back, two_back + one_back
>     return one_back
> ```

> [!success] Complexity
> Time O(n), Space O(n) for memoization / O(1) for iterative.

> [!tip] Alternatives
> Matrix exponentiation for O(log n). Naive recursion is O(2^n) — never use without memoization.

---

### Construct Binary Tree from Preorder and Inorder Traversal (LC 105) `🎯 T2`

> Full walkthrough: [Construct Binary Tree from Preorder and Inorder Traversal](../data-structures/08-tree.md#construct-binary-tree-from-preorder-and-inorder-traversal--t2).

---

### Serialize and Deserialize Binary Tree (LC 297) `🎯 T2`

> Full walkthrough: [Serialize and Deserialize Binary Tree](../data-structures/08-tree.md#serialize-and-deserialize-binary-tree--t2).

---

### Maximum Subarray — D&C (O(n log n)) `🎯 T2`

> [!example] Problem
> Same problem as [Maximum Subarray](../data-structures/01-array.md#maximum-subarray--t2) — this section covers the alternative approach only.

> [!info] Approach
> Illustrates D&C: split at mid; max subarray is entirely in left half, entirely in right half, or crosses the midpoint. Crossing case is O(n) per level; depth is O(log n). Recurse on left and right halves; compute max crossing sum by linear scan outward from `mid`. `max_cross` = max suffix of left + max prefix of right. Return `max(max_left, max_right, max_cross)`.

> [!note]- Python Solution
> ```python
> def max_sub_array(nums):
>     def helper(l, r):
>         if l == r:
>             return nums[l]
>         mid = (l + r) // 2
>         left_max = helper(l, mid)
>         right_max = helper(mid + 1, r)
>         # crossing sum
>         left_cross = cur = 0
>         for i in range(mid, l - 1, -1):
>             cur += nums[i]
>             left_cross = max(left_cross, cur)
>         right_cross = cur = 0
>         for i in range(mid + 1, r + 1):
>             cur += nums[i]
>             right_cross = max(right_cross, cur)
>         return max(left_max, right_max, left_cross + right_cross)
>     return helper(0, len(nums) - 1)
> ```

> [!success] Complexity
> Time O(n log n), Space O(log n) call stack.

> [!tip] Alternatives
> Kadane's algorithm is O(n) O(1) and preferred in production. D&C version is only asked to demonstrate the paradigm.

---

### Pow(x, n) — Fast Exponentiation

> [!example] Problem
> Implement `pow(x, n)` for real `x` and integer `n` (including negative `n`).

> [!info] Approach
> Naive O(n) multiplication is too slow for large `n`. Halving the exponent each call gives O(log n) multiplications. Recursive fast exponentiation (exponentiation by squaring). If `n == 0` return 1. If `n < 0`, compute `1 / pow(x, -n)`. If `n` is even, `half = pow(x, n//2); return half * half`. If odd, `return x * pow(x, n-1)`.

> [!note]- Python Solution
> ```python
> def my_pow(x, n):
>     if n == 0:
>         return 1.0
>     if n < 0:
>         return 1.0 / myPow(x, -n)
>     half = myPow(x, n // 2)
>     if n % 2 == 0:
>         return half * half
>     return x * half * half
> ```

> [!success] Complexity
> Time O(log n), Space O(log n) call stack.

> [!tip] Alternatives
> Iterative bit-manipulation version: accumulate result while right-shifting `n`, squaring `x` each iteration — O(log n) time, O(1) space.

---

### Count of Inversions (Merge-Sort Based)

> [!example] Problem
> Count the number of inversions in an array: pairs `(i, j)` where `i < j` but `nums[i] > nums[j]`.

> [!info] Approach
> During merge sort, when a right-half element is placed before left-half elements, all remaining left-half elements form inversions with it. Counting this during merge is O(n log n) total. Modified merge sort that accumulates an inversion count. In the merge step, when `right[j] < left[i]`, add `len(left) - i` to the count (all remaining left elements are greater than `right[j]`).

> [!note]- Python Solution
> ```python
> def count_inversions(nums):
>     def merge_sort(arr):
>         if len(arr) <= 1:
>             return arr, 0
>         mid = len(arr) // 2
>         left, lc = merge_sort(arr[:mid])
>         right, rc = merge_sort(arr[mid:])
>         merged, mc = [], 0
>         i = j = 0
>         while i < len(left) and j < len(right):
>             if left[i] <= right[j]:
>                 merged.append(left[i])
>                 i += 1
>             else:
>                 merged.append(right[j])
>                 j += 1
>                 mc += len(left) - i  # inversions with all remaining left elements
>         merged.extend(left[i:])
>         merged.extend(right[j:])
>         return merged, lc + rc + mc
>     _, count = merge_sort(nums)
>     return count
> ```

> [!success] Complexity
> Time O(n log n), Space O(n) merge buffer + O(log n) call stack.

> [!tip] Alternatives
> BIT (Binary Indexed Tree) / Fenwick Tree approach: coordinate compress then count using prefix sums — O(n log n), O(n) space.

---

### Fast Doubling Fibonacci

> [!example] Problem
> Compute the `n`th Fibonacci number faster than linear recursion or simple DP.

> [!info] Approach
> The recurrence can be reduced by halving `n`, which turns linear recursion into logarithmic recursion depth. Use the fast-doubling identities: `F(2k) = F(k) * (2*F(k+1) - F(k))` and `F(2k+1) = F(k)^2 + F(k+1)^2`. A helper returns `(F(n), F(n+1))`, allowing each recursive step to reuse the same subproblem results.

> [!note]- Python Solution
> ```python
> def fib(n):
>     def helper(k):
>         if k == 0:
>             return 0, 1
>         a, b = helper(k // 2)
>         c = a * (2 * b - a)
>         d = a * a + b * b
>         if k % 2 == 0:
>             return c, d
>         return d, c + d
> 
>     return helper(n)[0]
> ```

> [!success] Complexity
> O(log n) time, O(log n) recursion depth.

> [!tip] Alternatives
> Memoized recursion and iterative DP are simpler, but fast doubling is the classic optimization question.

---

## Pruning & Constraints

---

### Combination Sum II (No Reuse) `🎯 T2`

> Full walkthrough: [Combination Sum II (0/1 — no reuse)](12-backtracking.md#combination-sum-ii-01--no-reuse--t2).

---

### Word Search (Grid Backtracking) `⚡ T1`

> Full walkthrough: [Word Search (All Occurrences)](12-backtracking.md#word-search-all-occurrences--t1).

---

### Word Search II (Trie + Backtracking) `⚡ T1`

> Full walkthrough: [Word Search II](../data-structures/09-trie.md#word-search-ii--t1).

---

### Unique Binary Search Trees II

> [!example] Problem
> Given an integer n, return all the structurally unique BST's (binary search trees), which has exactly n nodes of unique values from 1 to n. Return the answer in any order.
> 
> **Example 1:**
> ```
> Input: n = 3
> Output: [[1,null,2,null,3],[1,null,3,2],[2,1,3],[3,1,null,null,2],[3,2,null,1]]
> ```
> 
> **Example 2:**
> ```
> Input: n = 1
> Output: [[1]]
> ```
> 
> **Constraints:**
> - 1 <= n <= 8

> [!tip] Recognize · Gotcha
> **Signal:** "all structurally unique BSTs" · **Gotcha:** `[None]` for empty range, not `[]`

> [!info] Approach
> Each integer `k` in `[1..n]` can be the root; values `1..k-1` form the left subtree and `k+1..n` form the right subtree. Recursive structure — memoize on `(lo, hi)`. Return all possible root nodes for the BST using values `lo` to `hi`. For each root `k` in `[lo, hi]`, generate all left subtrees (using `lo..k-1`) and all right subtrees (using `k+1..hi`), combine every pair.

> [!note]- Python Solution
> ```python
> class TreeNode:
>     def __init__(self, val=0, left=None, right=None):
>         self.val = val
>         self.left = left
>         self.right = right
> 
> def generate_trees(n):
>     memo = {}
>
>     def build(lo, hi):
>         if (lo, hi) in memo:
>             return memo[(lo, hi)]
>         if lo > hi:
>             return [None]
>         trees = []
>         for k in range(lo, hi + 1):
>             for left in build(lo, k - 1):
>                 for right in build(k + 1, hi):
>                     root = TreeNode(k, left, right)
>                     trees.append(root)
>         memo[(lo, hi)] = trees
>         return trees
>
>     return build(1, n)
> ```

> [!success] Complexity
> Time O(C_n · n) where C_n is the nth Catalan number (~4^n / n^(3/2)). Space O(C_n · n) for all tree nodes.

> [!tip] Alternatives
> Iterative DP building from smaller ranges — more complex. Count-only version (LC 96) uses DP in O(n²).

---

### Expression Add Operators

> Full walkthrough: [Expression Add Operators (LC 282)](12-backtracking.md#expression-add-operators-lc-282).

---

### Robot Room Cleaner

> [!example] Problem
> You are controlling a robot that is located somewhere in a room. The room is modeled as an `m x n` binary grid where `0` represents a wall and `1` represents an empty slot.
> 
> The robot starts at an unknown location in the room that is guaranteed to be empty, and you do not have access to the grid, but you can move the robot using the given API `Robot`.
> 
> You are tasked to use the robot to clean the entire room (i.e., clean every empty cell in the room). The robot with the four given APIs can move forward, turn left, or turn right. Each turn is `90` degrees.
> 
> When the robot tries to move into a wall cell, its bumper sensor detects the obstacle, and it stays on the current cell.
> 
> Design an algorithm to clean the entire room using the following APIs:
> 
> ```
> 
> interface Robot {
>   // returns true if next cell is open and robot moves into the cell.
>   // returns false if next cell is obstacle and robot stays on the current cell.
>   boolean move();
> 
>   // Robot will stay on the same cell after calling turnLeft/turnRight.
>   // Each turn will be 90 degrees.
>   void turnLeft();
>   void turnRight();
> 
>   // Clean the current cell.
>   void clean();
> }
> 
> ```
> 
> **Note** that the initial direction of the robot will be facing up. You can assume all four edges of the grid are all surrounded by a wall.
> 
>  
> 
> **Custom testing:**
> 
> The input is only given to initialize the room and the robot's position internally. You must solve this problem "blindfolded". In other words, you must control the robot using only the four mentioned APIs without knowing the room layout and the initial robot's position.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** room = [[1,1,1,1,1,0,1,1],[1,1,1,1,1,0,1,1],[1,0,1,1,1,1,1,1],[0,0,0,1,0,0,0,0],[1,1,1,1,1,1,1,1]], row = 1, col = 3
> **Output:** Robot cleaned all rooms.
> **Explanation:** All grids in the room are marked by either 0 or 1.
> 0 means the cell is blocked, while 1 means the cell is accessible.
> The robot initially starts at the position of row=1, col=3.
> From the top left corner, its position is one row below and three columns right.
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** room = [[1]], row = 0, col = 0
> **Output:** Robot cleaned all rooms.
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `m == room.length`
> 	
> - `n == room[i].length`
> 	
> - `1 <= m <= 100`
> 	
> - `1 <= n <= 200`
> 	
> - `room[i][j]` is either `0` or `1`.
> 	
> - `0 <= row < m`
> 	
> - `0 <= col < n`
> 	
> - `room[row][col] == 1`
> 	
> - All the empty cells can be visited from the starting position.

> [!tip] Recognize · Gotcha
> **Signal:** Unknown grid, robot API · **Gotcha:** Must physically back out after each branch

> [!info] Approach
> Unknown grid topology — must explore via state-space DFS. Track visited coordinates; after each branch, return the robot to the previous position and heading (backtracking). DFS in four directions; track `(row, col)` in visited set; after exploring a subtree, reverse the robot back. Try each of 4 directions (relative to current heading using direction vectors). On return: turn 180°, move forward, turn 180° to restore position+heading.

> [!note]- Python Solution
> ```python
> def clean_room(robot):
>     # Directions: up, right, down, left (relative to heading 0)
>     dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
>     visited = set()
> 
>     def go_back():
>         robot.turnRight()
>         robot.turnRight()
>         robot.move()
>         robot.turnRight()
>         robot.turnRight()
> 
>     def dfs(r, c, direction):
>         robot.clean()
>         visited.add((r, c))
>         for i in range(4):
>             new_dir = (direction + i) % 4
>             nr, nc = r + dirs[new_dir][0], c + dirs[new_dir][1]
>             if (nr, nc) not in visited and robot.move():
>                 dfs(nr, nc, new_dir)
>                 go_back()
>             robot.turnRight()
> 
>     dfs(0, 0, 0)
> ```

> [!success] Complexity
> Time O(n - m) where n = grid cells, m = obstacles. Space O(n - m) visited set + O(n - m) call depth.

> [!tip] Alternatives
> BFS with a queue — requires the same backtracking mechanism; DFS is more natural here.

---

### Permutations II (LC 47) `🎯 T2`

> Full walkthrough: [Permutations II (with duplicates)](12-backtracking.md#permutations-ii-with-duplicates--t2).

---

### Subsets II (LC 90) `🎯 T2`

> Full walkthrough: [Subsets II (with duplicates)](12-backtracking.md#subsets-ii-with-duplicates--t2).

---

### Combinations (LC 77) `🎯 T2`

> Full walkthrough: [Combinations](12-backtracking.md#combinations--t2).

---

## Foundation — Recursion Fundamentals

---

### Binary Search (Recursive)

> [!example] Problem
> Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.
> You must write an algorithm with O(log n) runtime complexity.
> 
> **Example 1:**
> ```
> Input: nums = [-1,0,3,5,9,12], target = 9
> Output: 4
> Explanation: 9 exists in nums and its index is 4
> ```
> 
> **Example 2:**
> ```
> Input: nums = [-1,0,3,5,9,12], target = 2
> Output: -1
> Explanation: 2 does not exist in nums so return -1
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^4
> - -10^4 < nums[i], target < 10^4
> - All the integers in nums are unique.
> - nums is sorted in ascending order.

> [!tip] Recognize · Gotcha
> **Signal:** Sorted + find index · **Gotcha:** Return `-1` after loop, not `lo`

> [!info] Approach
> The array is sorted — at each step the search space halves by comparing the midpoint. Recursion mirrors the decision tree: go left or go right. Compute mid; if `nums[mid] == target` return mid; recurse on left or right half. Pass `lo`, `hi` as parameters. Base case: `lo > hi` → return -1. No extra space beyond call stack.

> [!note]- Python Solution
> ```python
> def binary_search(nums, target, lo=0, hi=-1):
>     if hi == -1:
>         hi = len(nums) - 1
>     if lo > hi:
>         return -1
>     mid = (lo + hi) // 2
>     if nums[mid] == target:
>         return mid
>     elif nums[mid] < target:
>         return binarySearch(nums, target, mid + 1, hi)
>     else:
>         return binarySearch(nums, target, lo, mid - 1)
> ```

> [!success] Complexity
> Time O(log n). Space O(log n) call stack — iterative version reduces this to O(1).

> [!tip] Alternatives
> Always prefer the iterative `while lo <= hi` loop in production — avoids stack overflow on very large arrays.

---

### Tower of Hanoi

> [!example] Problem
> Move `n` disks from peg A to peg C using peg B as auxiliary. Never place a larger disk on a smaller one.

> [!info] Approach
> The recurrence is T(n) = 2T(n-1) + 1. Moving `n` disks = move top `n-1` to B (using C), move largest to C, move `n-1` from B to C (using A). Classic divide-and-conquer recursion with no overlapping subproblems. Recursion with three named pegs; base case is 1 disk. `hanoi(n-1, src, aux, dst)` → move disk n → `hanoi(n-1, aux, src, dst)`.

> [!note]- Python Solution
> ```python
> def hanoi(n, src, aux, dst):
>     moves = []
> 
>     def solve(k, s, a, d):
>         if k == 1:
>             moves.append((s, d))
>             return
>         solve(k - 1, s, d, a)
>         moves.append((s, d))
>         solve(k - 1, a, s, d)
> 
>     solve(n, src, aux, dst)
>     return moves
> ```

> [!success] Complexity
> Time O(2^n) — exactly 2^n − 1 moves required (provably optimal). Space O(n) call depth.

> [!tip] Alternatives
> Iterative using a stack is possible but significantly more complex. The recursive form is the canonical exposition.

---

### Print All Subsequences

> [!example] Problem
> Print all 2^n subsequences of an array (order of elements preserved, not necessarily contiguous).

> [!info] Approach
> Each element has exactly two choices — include or exclude. The include/exclude recursion tree has 2^n leaves, each representing one subsequence. DFS from index 0; branch into "include `arr[i]`" and "exclude `arr[i]`"; print at leaf. Carry a running `path`. At index == n, print path. Recurse both branches at each step.

> [!note]- Python Solution
> ```python
> def print_subsequences(arr):
>     result = []
> 
>     def dfs(index, path):
>         if index == len(arr):
>             result.append(path[:])  # include empty subsequence too
>             return
>         # Include arr[index]
>         path.append(arr[index])
>         dfs(index + 1, path)
>         path.pop()
>         # Exclude arr[index]
>         dfs(index + 1, path)
> 
>     dfs(0, [])
>     return result
> ```

> [!success] Complexity
> Time O(2^n · n) — 2^n subsequences, O(n) to record each. Space O(n) call depth.

> [!tip] Alternatives
> Bitmask: for each integer 0 to 2^n-1, bits mark included elements. Equivalent to Subsets; naming distinction is problem-context only.

---

### Josephus Problem

> [!example] Problem
> `n` people stand in a circle; every `k`th person is eliminated. Find the position of the last survivor (0-indexed).

> [!info] Approach
> After each elimination the circle shrinks by 1 and the indices shift. The recurrence `J(n,k) = (J(n-1,k) + k) % n` computes the survivor's position in the reduced circle and maps it back to the original numbering. Recursive formula: `J(1,k) = 0`; `J(n,k) = (J(n-1,k) + k) % n`. Memoize or convert to iteration to avoid O(n) stack depth.

> [!note]- Python Solution
> ```python
> # Recursive (clean but O(n) stack)
> def josephus_recursive(n, k):
>     if n == 1:
>         return 0
>     return (josephus_recursive(n - 1, k) + k) % n
> 
> # Iterative (O(1) space)
> def josephus(n, k):
>     pos = 0
>     for size in range(2, n + 1):
>         pos = (pos + k) % size
>     return pos
> ```

> [!success] Complexity
> Time O(n). Space O(n) recursive / O(1) iterative.

> [!tip] Alternatives
> Simulation with a list or circular linked list gives O(n·k) — fine for small k. The recurrence is O(n) regardless of k.

---

## Recursive Parsing / Evaluation

---

### Decode String (Recursive)

> [!example] Problem
> Same problem as [Decode String](../data-structures/03-string.md#decode-string) — this section covers the alternative approach only.

> [!info] Approach
> Nested brackets are naturally recursive — decoding the inner bracket is a subproblem of the same type. Recursion with an index pointer consumes the string in one pass. Recursive descent parser; when `[` is encountered, recurse; when `]` is encountered, return current decoded string. Pass a mutable index (via list). Accumulate digits for `k`, accumulate chars for the current segment, recurse on `[`, multiply result on `]`.

> [!note]- Python Solution
> ```python
> def decode_string(s):
>     idx = [0]  # mutable index shared across frames
> 
>     def decode():
>         result = []
>         while idx[0] < len(s) and s[idx[0]] != ']':
>             if s[idx[0]].isdigit():
>                 k = 0
>                 while idx[0] < len(s) and s[idx[0]].isdigit():
>                     k = k * 10 + int(s[idx[0]])
>                     idx[0] += 1
>                 idx[0] += 1  # consume '['
>                 inner = decode()
>                 idx[0] += 1  # consume ']'
>                 result.append(inner * k)
>             else:
>                 result.append(s[idx[0]])
>                 idx[0] += 1
>         return ''.join(result)
> 
>     return decode()
> ```

> [!success] Complexity
> Time O(max_k^depth · n) — worst case exponential output size; O(n) for the parse pass itself. Space O(n) call depth.

> [!tip] Alternatives
> Iterative stack: push current string and k when encountering `[`; pop and multiply on `]`. Both are O(output_size) time.

---

### Basic Calculator II (LC 227)

> [!example] Problem
> Same problem as [Basic Calculator II](../data-structures/05-stack.md#basic-calculator-ii) — this section covers the alternative approach only.

> [!info] Approach
> Operator precedence makes this a parsing problem. A recursive descent parser separates addition/subtraction (low precedence) from multiplication/division (high precedence) using mutual recursion between grammar levels. Recursive descent: `expr → term (('+' | '-') term)*`, `term → factor (('*' | '/') factor)*`. Use an index pointer (wrapped in a list for mutability) advanced through the string. `parse_expr` calls `parse_term` repeatedly; `parse_term` calls `parse_factor` (a number).

> [!note]- Python Solution
> ```python
> def calculate(s):
>     s = s.replace(' ', '')
>     idx = [0]
> 
>     def parse_number():
>         start = idx[0]
>         while idx[0] < len(s) and s[idx[0]].isdigit():
>             idx[0] += 1
>         return int(s[start:idx[0]])
> 
>     def parse_term():
>         val = parse_number()
>         while idx[0] < len(s) and s[idx[0]] in '*/':
>             op = s[idx[0]]
>             idx[0] += 1
>             right = parse_number()
>             val = val * right if op == '*' else int(val / right)
>         return val
> 
>     def parse_expr():
>         val = parse_term()
>         while idx[0] < len(s) and s[idx[0]] in '+-':
>             op = s[idx[0]]
>             idx[0] += 1
>             right = parse_term()
>             val = val + right if op == '+' else val - right
>         return val
> 
>     return parse_expr()
> ```

> [!success] Complexity
> Time O(n), Space O(1) excluding call frames (O(n/digit_length) call depth in worst case).

> [!tip] Alternatives
> Stack-based simulation (classic interview answer): process tokens left to right, push onto stack applying `*`/`/` immediately, sum the stack at the end.

---

## Graph — Recursive Traversal

---

### Flatten Nested List Iterator

> [!example] Problem
> You are given a nested list of integers nestedList. Each element is either an integer or a list whose elements may also be integers or other lists. Implement an iterator to flatten it.
> Implement the NestedIterator class:
> Your code will be tested with the following pseudocode:
> If res matches the expected flattened list, then your code will be judged as correct.
> 
> **Example 1:**
> ```
> initialize iterator with nestedList
> res = []
> while iterator.hasNext()
>     append iterator.next() to the end of res
> return res
> ```
> 
> **Example 2:**
> ```
> Input: nestedList = [[1,1],2,[1,1]]
> Output: [1,1,2,1,1]
> Explanation: By calling next repeatedly until hasNext returns false, the order of elements returned by next should be: [1,1,2,1,1].
> ```
> 
> **Example 3:**
> ```
> Input: nestedList = [1,[4,[6]]]
> Output: [1,4,6]
> Explanation: By calling next repeatedly until hasNext returns false, the order of elements returned by next should be: [1,4,6].
> ```
> 
> **Constraints:**
> - 1 <= nestedList.length <= 500
> - The values of the integers in the nested list is in the range [-10^6, 10^6].

> [!info] Approach
> Nested structure is recursively defined — a list element is either an integer (base case) or another list (recursive case). DFS through the nested list; at each element, if integer → add to result; if list → recurse. Single recursive function that iterates over the current list and dispatches based on element type.

> [!note]- Python Solution
> ```python
> from typing import Union
> 
> NestedList = list[Union[int, list]]  # simplified type alias
> 
> def flatten(nested):
>     result = []
> 
>     def dfs(item):
>         if isinstance(item, int):
>             result.append(item)
>         else:
>             for element in item:
>                 dfs(element)
> >
>     dfs(nested)
>     return result
> >
> # LeetCode NestedInteger API version
> def flatten_nested_list(nestedList):
>     result = []
> >
>     def dfs(nl):
>         for item in nl:
>             if item.isInteger():
>                 result.append(item.getInteger())
>             else:
>                 dfs(item.getList())
> >
>     dfs(nestedList)
>     return result
> ```

> [!success] Complexity
> Time O(n) where n = total number of integers across all nesting levels. Space O(d) where d = max nesting depth.

> [!tip] Alternatives
> Iterative using a stack: push elements in reverse; pop and check type; push sub-list elements if needed. `yield`-based generator avoids materializing the full list.

---

### Nested List Weight Sum

> [!example] Problem
> You are given a nested list of integers `nestedList`. Each element is either an integer or a list whose elements may also be integers or other lists.
> 
> The **depth** of an integer is the number of lists that it is inside of. For example, the nested list `[1,[2,2],[[3],2],1]` has each integer's value set to its **depth**.
> 
> Return *the sum of each integer in *`nestedList`* multiplied by its **depth***.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** nestedList = [[1,1],2,[1,1]]
> **Output:** 10
> **Explanation:** Four 1's at depth 2, one 2 at depth 1. 1*2 + 1*2 + 2*1 + 1*2 + 1*2 = 10.
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** nestedList = [1,[4,[6]]]
> **Output:** 27
> **Explanation:** One 1 at depth 1, one 4 at depth 2, and one 6 at depth 3. 1*1 + 4*2 + 6*3 = 27.
> ```
> 
> Example 3:
> 
> ```
> 
> **Input:** nestedList = [0]
> **Output:** 0
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= nestedList.length <= 50`
> 	
> - The values of the integers in the nested list is in the range `[-100, 100]`.
> 	
> - The maximum **depth** of any integer is less than or equal to `50`.

> [!info] Approach
> Each nesting level increments the depth multiplier — a natural recursion where the depth parameter is passed down. Recursive DFS; carry `depth` parameter; add `value * depth` for integers; recurse with `depth + 1` for nested lists. Start with `depth=1`. At each integer, accumulate `val * depth`. At each list, recurse with `depth + 1`.

> [!note]- Python Solution
> ```python
> def depth_sum(nestedList, depth=1):
>     total = 0
>     for item in nestedList:
>         if item.isInteger():
>             total += item.getInteger() * depth
>         else:
>             total += depthSum(item.getList(), depth + 1)
>     return total
> >
> # Pure Python version (no NestedInteger API)
> def depth_sum_pure(nested, depth=1):
>     total = 0
>     for item in nested:
>         if isinstance(item, int):
>             total += item * depth
>         else:
>             total += depthSumPure(item, depth + 1)
>     return total
> ```

> [!success] Complexity
> Time O(n) — visits each integer and list node once. Space O(d) call stack where d = max depth.

> [!tip] Alternatives
> Inverse weight sum (deeper = less weight): precompute max depth first, then DFS with `(max_depth + 1 - depth)` as multiplier.

---

### Clone Graph (LC 133) `⚡ T1`

> Full walkthrough: [Clone Graph](../data-structures/13-graph.md#clone-graph--t1).

---

### Number of Islands (LC 200) `⚡ T1`

> Full walkthrough: [Number of Islands (BFS)](../data-structures/13-graph.md#number-of-islands-bfs--t1).

---

## Dynamic Programming Foundations (Recursive + Memo)

---

### Climbing Stairs (Memoized Recursion) `🎯 T2`

> [!example] Problem
> Same problem as [Climbing Stairs](15-dynamic-programming.md#climbing-stairs--t2) — this section covers the alternative approach only.

> [!info] Approach
> Memoize `ways(n)` in a dict — same recurrence as Fibonacci. For k step sizes, sum over `ways(n - s)` for each valid step `s`.

> [!note]- Python Solution
> ```python
> def climb_stairs(n):
>     memo = {}
>
>     def ways(n):
>         if n in memo:
>             return memo[n]
>         if n <= 1:
>             return 1
>         memo[n] = ways(n - 1) + ways(n - 2)
>         return memo[n]
>
>     return ways(n)
>
> # Generalised: k distinct step sizes
> def climb_stairs_k(n, steps):
>     memo = {}
>
>     def dp(remaining):
>         if remaining in memo:
>             return memo[remaining]
>         if remaining == 0:
>             return 1
>         if remaining < 0:
>             return 0
>         memo[remaining] = sum(dp(remaining - s) for s in steps)
>         return memo[remaining]
>
>     return dp(n)
> ```

> [!success] Complexity
> Time O(n) with memoization (O(2^n) without). Space O(n) cache + O(n) call depth. Iterative reduces space to O(1).

> [!tip] Alternatives
> Iterative DP with two variables is O(1) space. Matrix exponentiation achieves O(log n) for Fibonacci-variant recurrences.

---

### Predict the Winner (LC 486)

> [!example] Problem
> You are given an integer array nums. Two players are playing a game with this array: player 1 and player 2.
> Player 1 and player 2 take turns, with player 1 starting first. Both players start the game with a score of 0. At each turn, the player takes one of the numbers from either end of the array (i.e., nums[0] or nums[nums.length - 1]) which reduces the size of the array by 1. The player adds the chosen number to their score. The game ends when there are no more elements in the array.
> Return true if Player 1 can win the game. If the scores of both players are equal, then player 1 is still the winner, and you should also return true. You may assume that both players are playing optimally.
> 
> **Example 1:**
> ```
> Input: nums = [1,5,2]
> Output: false
> Explanation: Initially, player 1 can choose between 1 and 2. 
> If he chooses 2 (or 1), then player 2 can choose from 1 (or 2) and 5. If player 2 chooses 5, then player 1 will be left with 1 (or 2). 
> So, final score of player 1 is 1 + 2 = 3, and player 2 is 5. 
> Hence, player 1 will never be the winner and you need to return false.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,5,233,7]
> Output: true
> Explanation: Player 1 first chooses 1. Then player 2 has to choose between 5 and 7. No matter which number player 2 choose, player 1 can choose 233.
> Finally, player 1 has more score (234) than player 2 (12), so you need to return True representing player1 can win.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 20
> - 0 <= nums[i] <= 10^7

> [!info] Approach
> `dp(i, j)` = score advantage for the current player on subarray `[i, j]`. Base: `dp(i, i) = nums[i]`. Recurrence: `max(nums[i] - dp(i+1, j), nums[j] - dp(i, j-1))`. Cache `(i, j)` in a dict. First player wins if `dp(0, n-1) >= 0`.

> [!note]- Python Solution
> ```python
> def predict_the_winner(nums):
>     n = len(nums)
>     memo = {}
>
>     def dp(i, j):
>         if (i, j) in memo:
>             return memo[(i, j)]
>         if i == j:
>             return nums[i]
>         pick_left = nums[i] - dp(i + 1, j)
>         pick_right = nums[j] - dp(i, j - 1)
>         memo[(i, j)] = max(pick_left, pick_right)
>         return memo[(i, j)]
>
>     return dp(0, n - 1) >= 0
> ```

> [!success] Complexity
> Time O(n²), Space O(n²).

> [!tip] Alternatives
> - Bottom-up DP: fill a 2D table by diagonal (subarray length). Same asymptotic complexity, avoids recursion stack.
> - Key insight: `dp(i, j)` represents the *net advantage* (current player's gain minus opponent's gain) — not the absolute score. This collapses the two-player tracking into one value.

---

## See Also

[[dynamic-programming]] | [[backtracking]] | [[tree]] | [[stack]]
