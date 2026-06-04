---
tags: [coding, algorithms, recursion]
topic: Recursion & Backtracking
difficulty: mixed
---

# Recursion & Backtracking — Problem Reference by Pattern

> [!info] First Principles
> Recursion reduces a problem to a smaller identical subproblem; the call stack manages state across levels. Backtracking = DFS over a decision tree — "make choice → recurse → undo choice". The invariant at every recursive call: the partial solution satisfies all constraints imposed so far. Complexity: subsets O(2^n · n), permutations O(n! · n), combinations O(C(n,k) · k).

---

## Foundation — Include/Exclude

### Subsets (Power Set)

> [!example] Problem
> Given an integer array nums of unique elements, return all possible subsets (the power set).
> The solution set must not contain duplicate subsets. Return the solution in any order.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3]
> Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0]
> Output: [[],[0]]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10
> - -10 <= nums[i] <= 10
> - All the numbers of nums are unique.

> [!info] Approach
> Every element has exactly two choices — include or exclude. The 2^n subsets map to all binary strings of length n. Overlapping structure: subsets of `nums[0..i-1]` are extended by the decision on `nums[i]`. DFS/backtracking over the array; at each index, branch into "include" and "exclude". At index `i`, add current path to results, then recurse with `i+1` after optionally appending `nums[i]`. Or equivalently: iterate from `i` to `n`, choose `nums[j]`, recurse from `j+1`.


> [!note]- Python Solution
> ```python
> def subsets(nums):
>     result = []
> 
>     def dfs(start, path):
>         result.append(path[:])  # snapshot at every node (not just leaves)
>         for i in range(start, len(nums)):
>             path.append(nums[i])
>             dfs(i + 1, path)
>             path.pop()
> 
>     dfs(0, [])
>     return result
> ```

> [!success] Complexity
> Time O(2^n · n) — 2^n subsets, O(n) to copy each. Space O(n) call stack + O(2^n · n) output.

> [!tip] Alternatives
> Iterative: for each new number, extend all existing subsets. Bitmask: for each integer 0 to 2^n - 1, bits represent included elements.

---

### Permutations

> [!example] Problem
> Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3]
> Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,1]
> Output: [[0,1],[1,0]]
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1]
> Output: [[1]]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 6
> - -10 <= nums[i] <= 10
> - All the integers of nums are unique.

> [!info] Approach
> n! orderings; at each position, any unused element can be placed. Backtracking explores all placements, undoing each choice before trying the next. At each recursion level, pick one unused element, add it, recurse with remaining. Swap `nums[i]` with `nums[start]`, recurse with `start+1`, swap back (in-place backtracking preserves O(1) space overhead per level).


> [!note]- Python Solution
> ```python
> def permute(nums):
>     result = []
> 
>     def dfs(start):
>         if start == len(nums):
>             result.append(nums[:])
>             return
>         for i in range(start, len(nums)):
>             nums[start], nums[i] = nums[i], nums[start]
>             dfs(start + 1)
>             nums[start], nums[i] = nums[i], nums[start]
> 
>     dfs(0)
>     return result
> ```

> [!success] Complexity
> Time O(n! · n). Space O(n) call stack depth.

> [!tip] Alternatives
> Use a `visited` boolean array and build path list separately — cleaner but O(n) extra space per level. `itertools.permutations` in production.

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

### Merge Sort

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
>             result.append(left[i]); i += 1
>         else:
>             result.append(right[j]); j += 1
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
> Naive recursion `f(n) = f(n-1) + f(n-2)` calls `f(k)` exponentially many times for overlapping `k`. Memoization caches each call once → O(n). Memoized recursion (top-down DP) vs iterative DP (bottom-up). Both O(n) time O(n) space; iterative reduces to O(1) space. Memoize using a dict or `@lru_cache`. For O(1) space, use two variables.


> [!note]- Python Solution
> ```python
> from functools import lru_cache
> 
> # Top-down memoized recursion
> @lru_cache(maxsize=None)
> def fib_memo(n):
>     if n <= 1:
>         return n
>     return fib_memo(n - 1) + fib_memo(n - 2)
> 
> # Bottom-up DP — O(1) space
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

## Pruning & Constraints

### Combination Sum (Unbounded)

> [!example] Problem
> Given an array of distinct integers candidates and a target integer target, return a list of all unique combinations of candidates where the chosen numbers sum to target. You may return the combinations in any order.
> The same number may be chosen from candidates an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.
> The test cases are generated such that the number of unique combinations that sum up to target is less than 150 combinations for the given input.
> 
> **Example 1:**
> ```
> Input: candidates = [2,3,6,7], target = 7
> Output: [[2,2,3],[7]]
> Explanation:
> 2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times.
> 7 is a candidate, and 7 = 7.
> These are the only two combinations.
> ```
> 
> **Example 2:**
> ```
> Input: candidates = [2,3,5], target = 8
> Output: [[2,2,2,2],[2,3,3],[3,5]]
> ```
> 
> **Example 3:**
> ```
> Input: candidates = [2], target = 1
> Output: []
> ```
> 
> **Constraints:**
> - 1 <= candidates.length <= 30
> - 2 <= candidates[i] <= 40
> - All elements of candidates are distinct.
> - 1 <= target <= 40

> [!info] Approach
> Unbounded choices — reuse is allowed. Backtracking explores all paths; pruning on `remaining < 0` cuts branches. DFS from index `start`; at each step include `candidates[i]` and stay at `i` (reuse) or move to `i+1`. Recurse with `(start=i, remaining-candidates[i])`. Backtrack by popping. Sort candidates for early termination.


> [!note]- Python Solution
> ```python
> def combination_sum(candidates, target):
>     candidates.sort()
>     result = []
> 
>     def dfs(start, path, remaining):
>         if remaining == 0:
>             result.append(path[:])
>             return
>         for i in range(start, len(candidates)):
>             if candidates[i] > remaining:
>                 break  # sorted → no point continuing
>             path.append(candidates[i])
>             dfs(i, path, remaining - candidates[i])  # i not i+1: reuse allowed
>             path.pop()
> 
>     dfs(0, [], target)
>     return result
> ```

> [!success] Complexity
> Time O(target/min_c) branches in worst case, output-sensitive. Space O(target/min_c) call depth.

> [!tip] Alternatives
> BFS level by level (sum increases by one candidate per level). DP for counting ways only.

---

### Combination Sum II (No Reuse)

> [!example] Problem
> Given a collection of candidate numbers (candidates) and a target number (target), find all unique combinations in candidates where the candidate numbers sum to target.
> Each number in candidates may only be used once in the combination.
> Note: The solution set must not contain duplicate combinations.
> 
> **Example 1:**
> ```
> Input: candidates = [10,1,2,7,6,1,5], target = 8
> Output: 
> [
> [1,1,6],
> [1,2,5],
> [1,7],
> [2,6]
> ]
> ```
> 
> **Example 2:**
> ```
> Input: candidates = [2,5,2,1,2], target = 5
> Output: 
> [
> [1,2,2],
> [5]
> ]
> ```
> 
> **Constraints:**
> - 1 <= candidates.length <= 100
> - 1 <= candidates[i] <= 50
> - 1 <= target <= 30

> [!info] Approach
> Elements can repeat in input but not in output combinations. Key: sort + skip-duplicate guard prevents generating `[1a, 2]` and `[1b, 2]` separately when two `1`s exist. Same DFS but recurse with `i+1` and skip `candidates[j] == candidates[j-1]` when `j > start`. `if j > start and candidates[j] == candidates[j-1]: continue` — only skip siblings, not the first occurrence at a level.


> [!note]- Python Solution
> ```python
> def combination_sum2(candidates, target):
>     candidates.sort()
>     result = []
> 
>     def dfs(start, path, remaining):
>         if remaining == 0:
>             result.append(path[:])
>             return
>         for i in range(start, len(candidates)):
>             if candidates[i] > remaining:
>                 break
>             if i > start and candidates[i] == candidates[i-1]:
>                 continue  # skip duplicate siblings
>             path.append(candidates[i])
>             dfs(i + 1, path, remaining - candidates[i])
>             path.pop()
> 
>     dfs(0, [], target)
>     return result
> ```

> [!success] Complexity
> Time O(2^n · k) where k = avg combination length. Space O(n) depth.

> [!tip] Alternatives
> Use a frequency map and iterate over unique values with a count limit — avoids sorting but same complexity.

---

### Generate Parentheses

> [!example] Problem
> Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.
> 
> **Example 1:**
> ```
> Input: n = 3
> Output: ["((()))","(()())","(())()","()(())","()()()"]
> ```
> 
> **Example 2:**
> ```
> Input: n = 1
> Output: ["()"]
> ```
> 
> **Constraints:**
> - 1 <= n <= 8

> [!info] Approach
> Validity constraints are locally checkable at each position — prune invalid branches without generating full strings. DFS building the string character by character. State = `(open_count, close_count)`. Add `(` if `open < n`; add `)` if `close < open`. Leaf = string of length `2n`.


> [!note]- Python Solution
> ```python
> def generate_parenthesis(n):
>     result = []
> 
>     def dfs(path, open_c, close_c):
>         if len(path) == 2 * n:
>             result.append(''.join(path))
>             return
>         if open_c < n:
>             path.append('(')
>             dfs(path, open_c + 1, close_c)
>             path.pop()
>         if close_c < open_c:
>             path.append(')')
>             dfs(path, open_c, close_c + 1)
>             path.pop()
> 
>     dfs([], 0, 0)
>     return result
> ```

> [!success] Complexity
> Time O(4^n / √n) — Catalan number C_n counts valid strings. Space O(n) depth.

> [!tip] Alternatives
> Iterative BFS building strings level by level. DP building from smaller valid sequences.

---

### Word Search (Grid Backtracking)

> [!example] Problem
> Given an m x n grid of characters board and a string word, return true if word exists in the grid.
> The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.
> 
> **Example 1:**
> ```
> Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
> Output: true
> ```
> 
> **Example 3:**
> ```
> Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
> Output: false
> ```
> 
> **Constraints:**
> - m == board.length
> - n = board[i].length
> - 1 <= m, n <= 6
> - 1 <= word.length <= 15
> - board and word consists of only lowercase and uppercase English letters.

> [!info] Approach
> Exponential state space of paths; backtracking explores all starting positions and directions, pruning when the current character doesn't match. DFS from each cell; mark visited in-place (avoid extra space); restore on backtrack. Mark `board[r][c]` with a sentinel (e.g., `'#'`) before recursing, restore after. Check bounds and match before recursing.


> [!note]- Python Solution
> ```python
> def exist(board, word):
>     rows, cols = len(board), len(board[0])
> 
>     def dfs(r, c, idx):
>         if idx == len(word):
>             return True
>         if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[idx]:
>             return False
>         tmp, board[r][c] = board[r][c], '#'
>         found = any(dfs(r+dr, c+dc, idx+1) for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)])
>         board[r][c] = tmp
>         return found
> 
>     return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
> ```

> [!success] Complexity
> Time O(m·n · 4^L) where L = word length. Space O(L) call depth.

> [!tip] Alternatives
> BFS is possible but backtracking with in-place marking is canonical. Trie extension handles Word Search II (multiple words).

---

### Palindrome Partitioning

> [!example] Problem
> Given a string s, partition s such that every substring of the partition is a palindrome. Return all possible palindrome partitioning of s.
> 
> **Example 1:**
> ```
> Input: s = "aab"
> Output: [["a","a","b"],["aa","b"]]
> ```
> 
> **Example 2:**
> ```
> Input: s = "a"
> Output: [["a"]]
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 16
> - s contains only lowercase English letters.

> [!info] Approach
> Exponential number of partitions; prune by only recursing on palindromic prefixes. Precomputing `is_pal[i][j]` eliminates repeated palindrome checks. DFS from `start`; at each position try all palindromic prefixes starting at `start`. Precompute `is_pal` in O(n²). DFS: for each `end ≥ start`, if `is_pal[start][end]`, add substring and recurse from `end+1`.


> [!note]- Python Solution
> ```python
> def partition(s):
>     n = len(s)
>     is_pal = [[False] * n for _ in range(n)]
>     for i in range(n - 1, -1, -1):
>         for j in range(i, n):
>             is_pal[i][j] = s[i] == s[j] and (j - i < 2 or is_pal[i+1][j-1])
> 
>     result = []
> 
>     def dfs(start, path):
>         if start == n:
>             result.append(path[:])
>             return
>         for end in range(start, n):
>             if is_pal[start][end]:
>                 path.append(s[start:end+1])
>                 dfs(end + 1, path)
>                 path.pop()
> 
>     dfs(0, [])
>     return result
> ```

> [!success] Complexity
> Time O(n² + 2^n) — O(n²) precompute, O(2^n) worst-case partitions. Space O(n²) table.

> [!tip] Alternatives
> Check palindrome inline (O(n) per check) if not precomputing — O(n · 2^n) total.

---

### Letter Case Permutation

> [!example] Problem
> Given a string s, you can transform every letter individually to be lowercase or uppercase to create another string.
> Return a list of all possible strings we could create. Return the output in any order.
> 
> **Example 1:**
> ```
> Input: s = "a1b2"
> Output: ["a1b2","a1B2","A1b2","A1B2"]
> ```
> 
> **Example 2:**
> ```
> Input: s = "3z4"
> Output: ["3z4","3Z4"]
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 12
> - s consists of lowercase English letters, uppercase English letters, and digits.

> [!info] Approach
> Each letter creates a binary branch (upper/lower); digits have no branch. Backtracking with character-level mutation. DFS character by character; digits pass through; letters branch into two calls. At index `i`, if digit: recurse with `i+1`. If letter: set lowercase, recurse, set uppercase, recurse.


> [!note]- Python Solution
> ```python
> def letter_case_permutation(s):
>     result = []
>     chars = list(s)
> 
>     def dfs(i):
>         if i == len(chars):
>             result.append(''.join(chars))
>             return
>         dfs(i + 1)  # keep as-is (handles digits and one letter branch)
>         if chars[i].isalpha():
>             chars[i] = chars[i].upper() if chars[i].islower() else chars[i].lower()
>             dfs(i + 1)
>             chars[i] = chars[i].upper() if chars[i].islower() else chars[i].lower()
> 
>     dfs(0)
>     return result
> ```

> [!success] Complexity
> Time O(2^L · n) where L = number of letters. Space O(n) depth.

> [!tip] Alternatives
> BFS: start with `[s]`, for each letter position expand all current strings into two versions.

---

## Constraint Satisfaction

### N-Queens

> [!example] Problem
> The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other.
> Given an integer n, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.
> Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.
> 
> **Example 1:**
> ```
> Input: n = 4
> Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
> Explanation: There exist two distinct solutions to the 4-queens puzzle as shown above
> ```
> 
> **Example 2:**
> ```
> Input: n = 1
> Output: [["Q"]]
> ```
> 
> **Constraints:**
> - 1 <= n <= 9

> [!info] Approach
> 8^8 brute force positions; backtracking with clash sets prunes immediately when a queen attacks another. At most N! leaves to visit (one queen per row). Place one queen per row; track occupied columns and diagonals. Track sets `cols`, `diag1` (r-c), `diag2` (r+c). For each row, try each column not in any set; add to sets, recurse, remove.


> [!note]- Python Solution
> ```python
> def solve_n_queens(n):
>     result = []
>     queens = []  # queens[r] = column of queen in row r
>     cols = set()
>     diag1 = set()  # r - c
>     diag2 = set()  # r + c
> 
>     def dfs(row):
>         if row == n:
>             board = ['.' * c + 'Q' + '.' * (n - c - 1) for c in queens]
>             result.append(board)
>             return
>         for col in range(n):
>             if col in cols or (row - col) in diag1 or (row + col) in diag2:
>                 continue
>             cols.add(col); diag1.add(row - col); diag2.add(row + col)
>             queens.append(col)
>             dfs(row + 1)
>             queens.pop()
>             cols.remove(col); diag1.remove(row - col); diag2.remove(row + col)
> 
>     dfs(0)
>     return result
> ```

> [!success] Complexity
> Time O(n!) upper bound — pruning makes it much faster in practice. Space O(n) depth + O(n) tracking sets.

> [!tip] Alternatives
> Bitmask for columns and diagonals — constant-factor speedup. DLX (Dancing Links) for very large n.

---

### Sudoku Solver

> [!example] Problem
> Write a program to solve a Sudoku puzzle by filling the empty cells.
> A sudoku solution must satisfy all of the following rules:
> The '.' character indicates empty cells.
> 
> **Example 1:**
> ```
> Input: board = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
> Output: [["5","3","4","6","7","8","9","1","2"],["6","7","2","1","9","5","3","4","8"],["1","9","8","3","4","2","5","6","7"],["8","5","9","7","6","1","4","2","3"],["4","2","6","8","5","3","7","9","1"],["7","1","3","9","2","4","8","5","6"],["9","6","1","5","3","7","2","8","4"],["2","8","7","4","1","9","6","3","5"],["3","4","5","2","8","6","1","7","9"]]
> Explanation: The input board is shown above and the only valid solution is shown below:
> ```
> 
> **Constraints:**
> - board.length == 9
> - board[i].length == 9
> - board[i][j] is a digit or '.'.
> - It is guaranteed that the input board has only one solution.

> [!info] Approach
> Constraint satisfaction; 9 choices per empty cell but constraints prune rapidly. Backtracking with early exit on first valid solution. Find next empty cell, try digits 1-9, check validity, recurse. Precompute sets for each row, column, and 3×3 box. At each empty cell, try only valid digits; backtrack immediately on failure.


> [!note]- Python Solution
> ```python
> def solve_sudoku(board):
>     rows = [set() for _ in range(9)]
>     cols = [set() for _ in range(9)]
>     boxes = [set() for _ in range(9)]
> 
>     for r in range(9):
>         for c in range(9):
>             if board[r][c] != '.':
>                 d = board[r][c]
>                 rows[r].add(d); cols[c].add(d); boxes[(r//3)*3+c//3].add(d)
> 
>     def solve():
>         for r in range(9):
>             for c in range(9):
>                 if board[r][c] == '.':
>                     box_id = (r // 3) * 3 + c // 3
>                     for d in '123456789':
>                         if d not in rows[r] and d not in cols[c] and d not in boxes[box_id]:
>                             board[r][c] = d
>                             rows[r].add(d); cols[c].add(d); boxes[box_id].add(d)
>                             if solve():
>                                 return True
>                             board[r][c] = '.'
>                             rows[r].discard(d); cols[c].discard(d); boxes[box_id].discard(d)
>                     return False
>         return True
> 
>     solve()
> ```

> [!success] Complexity
> Time O(9^(empty_cells)) worst case; in practice much faster with constraint propagation. Space O(81) board + O(81) recursion depth.

> [!tip] Alternatives
> Arc consistency / constraint propagation (AC-3) reduces candidates before backtracking. DLX for competitive solving.

---

### Word Search II (Trie + Backtracking)

> [!example] Problem
> Given an m x n board of characters and a list of strings words, return all words on the board.
> Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.
> 
> **Example 1:**
> ```
> Input: board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]
> Output: ["eat","oath"]
> ```
> 
> **Example 2:**
> ```
> Input: board = [["a","b"],["c","d"]], words = ["abcb"]
> Output: []
> ```
> 
> **Constraints:**
> - m == board.length
> - n == board[i].length
> - 1 <= m, n <= 12
> - board[i][j] is a lowercase English letter.
> - 1 <= words.length <= 3 * 10^4
> - 1 <= words[i].length <= 10
> - words[i] consists of lowercase English letters.
> - All the strings of words are unique.

> [!info] Approach
> Running Word Search separately for each word is O(W · m·n · 4^L). A Trie lets one DFS pass check all words simultaneously — prune when the current path isn't a prefix of any word. Build Trie from word list. DFS from each cell; follow Trie nodes; when a terminal node is reached, record the word. At each cell, check `trie_node.children[char]`. If present, descend. If `trie_node.word`, add to results. Mark visited, recurse 4 directions, unmark. Prune exhausted Trie subtrees.


> [!note]- Python Solution
> ```python
> def find_words(board, words):
>     # Build Trie
>     trie = {}
>     for w in words:
>         node = trie
>         for ch in w:
>             node = node.setdefault(ch, {})
>         node['#'] = w  # terminal marker stores the word
> 
>     rows, cols = len(board), len(board[0])
>     result = []
> 
>     def dfs(r, c, node):
>         ch = board[r][c]
>         if ch not in node:
>             return
>         next_node = node[ch]
>         if '#' in next_node:
>             result.append(next_node['#'])
>             del next_node['#']  # dedup: don't find same word twice
>         board[r][c] = '#'
>         for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
>                 dfs(nr, nc, next_node)
>         board[r][c] = ch
>         if not next_node:  # prune empty Trie nodes
>             del node[ch]
> 
>     for r in range(rows):
>         for c in range(cols):
>             dfs(r, c, trie)
> 
>     return result
> ```

> [!success] Complexity
> Time O(m·n · 4^L) where L = max word length — same as Word Search but one pass for all words. Space O(total_chars_in_words) for Trie.

> [!tip] Alternatives
> Per-word DFS without Trie — O(W · m·n · 4^L) total, feasible only for small W.

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

> [!info] Approach
> Each integer `k` in `[1..n]` can be the root; values `1..k-1` form the left subtree and `k+1..n` form the right subtree. Recursive structure — memoize on `(lo, hi)`. Return all possible root nodes for the BST using values `lo` to `hi`. For each root `k` in `[lo, hi]`, generate all left subtrees (using `lo..k-1`) and all right subtrees (using `k+1..hi`), combine every pair.


> [!note]- Python Solution
> ```python
> from functools import lru_cache
> 
> class TreeNode:
>     def __init__(self, val=0, left=None, right=None):
>         self.val = val; self.left = left; self.right = right
> 
> def generate_trees(n):
>     @lru_cache(maxsize=None)
>     def build(lo, hi):
>         if lo > hi:
>             return [None]
>         trees = []
>         for k in range(lo, hi + 1):
>             for left in build(lo, k - 1):
>                 for right in build(k + 1, hi):
>                     root = TreeNode(k, left, right)
>                     trees.append(root)
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

> [!example] Problem
> Given a string num that contains only digits and an integer target, return all possibilities to insert the binary operators '+', '-', and/or '*' between the digits of num so that the resultant expression evaluates to the target value.
> Note that operands in the returned expressions should not contain leading zeros.
> Note that a number can contain multiple digits.
> 
> **Example 1:**
> ```
> Input: num = "123", target = 6
> Output: ["1*2*3","1+2+3"]
> Explanation: Both "1*2*3" and "1+2+3" evaluate to 6.
> ```
> 
> **Example 2:**
> ```
> Input: num = "232", target = 8
> Output: ["2*3+2","2+3*2"]
> Explanation: Both "2*3+2" and "2+3*2" evaluate to 8.
> ```
> 
> **Example 3:**
> ```
> Input: num = "3456237490", target = 9191
> Output: []
> Explanation: There are no expressions that can be created from "3456237490" to evaluate to 9191.
> ```
> 
> **Constraints:**
> - 1 <= num.length <= 10
> - num consists of only digits.
> - -2^{31} <= target <= 2^{31} - 1

> [!info] Approach
> Exponential operator assignments require backtracking. Multiplication's precedence requires tracking the previously added operand to undo and reapply multiplication. DFS building expression string; carry `curr_val` (running value) and `prev_operand` (last added term, for `*` precedence). For each position, try each multi-digit number (avoid leading zeros). On `*`: `curr_val = curr_val - prev_operand + prev_operand * num`; on `+/-`: standard addition.


> [!note]- Python Solution
> ```python
> def add_operators(num, target):
>     result = []
>     n = len(num)
> 
>     def dfs(index, path, curr_val, prev_operand):
>         if index == n:
>             if curr_val == target:
>                 result.append(path)
>             return
>         for end in range(index + 1, n + 1):
>             token = num[index:end]
>             if len(token) > 1 and token[0] == '0':
>                 break  # no leading zeros
>             val = int(token)
>             if index == 0:
>                 dfs(end, token, val, val)
>             else:
>                 dfs(end, path + '+' + token, curr_val + val, val)
>                 dfs(end, path + '-' + token, curr_val - val, -val)
>                 dfs(end, path + '*' + token, curr_val - prev_operand + prev_operand * val, prev_operand * val)
> 
>     dfs(0, '', 0, 0)
>     return result
> ```

> [!success] Complexity
> Time O(4^n · n) — 4 choices (no op, +, -, *) per gap, O(n) string ops. Space O(n) depth.

> [!tip] Alternatives
> Evaluate expression with a stack — avoids tracking `prev_operand` but more code. Iterative is significantly harder.

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
>         robot.turnRight(); robot.turnRight()
>         robot.move()
>         robot.turnRight(); robot.turnRight()
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

## Foundation — Recursion Fundamentals

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

## Graph — Recursive Traversal

### All Paths from Source to Target

> [!example] Problem
> Given a directed acyclic graph (DAG) of n nodes labeled from 0 to n - 1, find all possible paths from node 0 to node n - 1 and return them in any order.
> The graph is given as follows: graph[i] is a list of all nodes you can visit from node i (i.e., there is a directed edge from node i to node graph[i][j]).
> 
> **Example 1:**
> ```
> Input: graph = [[1,2],[3],[3],[]]
> Output: [[0,1,3],[0,2,3]]
> Explanation: There are two paths: 0 -> 1 -> 3 and 0 -> 2 -> 3.
> ```
> 
> **Example 2:**
> ```
> Input: graph = [[4,3,1],[3,2,4],[3],[4],[]]
> Output: [[0,4],[0,3,4],[0,1,3,4],[0,1,2,3,4],[0,1,4]]
> ```
> 
> **Constraints:**
> - n == graph.length
> - 2 <= n <= 15
> - 0 <= graph[i][j] < n
> - graph[i][j] != i (i.e., there will be no self-loops).
> - All the elements of graph[i] are unique.
> - The input graph is guaranteed to be a DAG.

> [!info] Approach
> DAG has no cycles so recursion terminates naturally. Backtracking explores all paths without needing an explicit visited set (DAG guarantees no revisit loops). DFS from 0; at each node extend path along all neighbors; record when node n-1 is reached. Backtrack by appending node, recursing through neighbors, then popping.


> [!note]- Python Solution
> ```python
> def all_paths_source_target(graph):
>     target = len(graph) - 1
>     result = []
> 
>     def dfs(node, path):
>         if node == target:
>             result.append(path[:])
>             return
>         for neighbor in graph[node]:
>             path.append(neighbor)
>             dfs(neighbor, path)
>             path.pop()
> 
>     dfs(0, [0])
>     return result
> ```

> [!success] Complexity
> Time O(2^n · n) — up to 2^n paths in a complete DAG, O(n) to copy each. Space O(n) call depth.

> [!tip] Alternatives
> BFS with path accumulation — uses O(2^n · n) memory for all partial paths simultaneously; DFS is memory-friendlier.

---

## String Recursion

### Decode String (Recursive)

> [!example] Problem
> Given an encoded string, return its decoded string.
> The encoding rule is: k[encoded_string], where the encoded_string inside the square brackets is being repeated exactly k times. Note that k is guaranteed to be a positive integer.
> You may assume that the input string is always valid; there are no extra white spaces, square brackets are well-formed, etc. Furthermore, you may assume that the original data does not contain any digits and that digits are only for those repeat numbers, k. For example, there will not be input like 3a or 2[4].
> The test cases are generated so that the length of the output will never exceed 105.
> 
> **Example 1:**
> ```
> Input: s = "3[a]2[bc]"
> Output: "aaabcbc"
> ```
> 
> **Example 2:**
> ```
> Input: s = "3[a2[c]]"
> Output: "accaccacc"
> ```
> 
> **Example 3:**
> ```
> Input: s = "2[abc]3[cd]ef"
> Output: "abcabccdcdcdef"
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 30
> - s consists of lowercase English letters, digits, and square brackets '[]'.
> - s is guaranteed to be a valid input.
> - All the integers in s are in the range [1, 300].

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

## Dynamic Programming Foundations (Recursive + Memo)

### Climbing Stairs (Memoized Recursion)

> [!example] Problem
> You are climbing a staircase. It takes n steps to reach the top.
> Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?
> 
> **Example 1:**
> ```
> Input: n = 2
> Output: 2
> Explanation: There are two ways to climb to the top.
> 1. 1 step + 1 step
> 2. 2 steps
> ```
> 
> **Example 2:**
> ```
> Input: n = 3
> Output: 3
> Explanation: There are three ways to climb to the top.
> 1. 1 step + 1 step + 1 step
> 2. 1 step + 2 steps
> 3. 2 steps + 1 step
> ```
> 
> **Constraints:**
> - 1 <= n <= 45

> [!info] Approach
> At each stair, you can arrive from stair `n-1` (one step) or stair `n-2` (two steps). The problem has optimal substructure and overlapping subproblems — identical to Fibonacci. `ways(n) = ways(n-1) + ways(n-2)` with `ways(0) = 1`, `ways(1) = 1`. Memoize to avoid recomputation. `@lru_cache` or manual dict. Can extend to k steps: `ways(n) = sum(ways(n-i) for i in 1..k if n-i >= 0)`.


> [!note]- Python Solution
> ```python
> from functools import lru_cache
> 
> @lru_cache(maxsize=None)
> def climb_stairs(n):
>     if n <= 1:
>         return 1
>     return climbStairs(n - 1) + climbStairs(n - 2)
> 
> # Generalised: k distinct step sizes
> def climb_stairs_k(n, steps):
>     from functools import lru_cache
> 
>     @lru_cache(maxsize=None)
>     def dp(remaining):
>         if remaining == 0:
>             return 1
>         if remaining < 0:
>             return 0
>         return sum(dp(remaining - s) for s in steps)
> 
>     return dp(n)
> ```

> [!success] Complexity
> Time O(n) with memoization (O(2^n) without). Space O(n) cache + O(n) call depth. Iterative reduces space to O(1).

> [!tip] Alternatives
> Iterative DP with two variables is O(1) space. Matrix exponentiation achieves O(log n) for Fibonacci-variant recurrences.

---

### Count Good Numbers

> [!example] Problem
> A digit string is good if the digits (0-indexed) at even indices are even and the digits at odd indices are prime (2, 3, 5, or 7).
> Given an integer n, return the total number of good digit strings of length n. Since the answer may be large, return it modulo 109 + 7.
> A digit string is a string consisting of digits 0 through 9 that may contain leading zeros.
> 
> **Example 1:**
> ```
> Input: n = 1
> Output: 5
> Explanation: The good numbers of length 1 are "0", "2", "4", "6", "8".
> ```
> 
> **Example 2:**
> ```
> Input: n = 4
> Output: 400
> ```
> 
> **Example 3:**
> ```
> Input: n = 50
> Output: 564908303
> ```
> 
> **Constraints:**
> - 1 <= n <= 1015

> [!info] Approach
> The count factorises: `5^(ceil(n/2)) * 4^(floor(n/2))`. Computing large powers requires fast exponentiation (recursive divide-and-conquer). `countGoodNumbers(n) = pow(5, even_positions) * pow(4, odd_positions) % MOD`. Even positions = `ceil(n/2)` = `(n+1)//2`. Odd positions = `floor(n/2)` = `n//2`. Use recursive fast-power.


> [!note]- Python Solution
> ```python
> def count_good_numbers(n):
>     MOD = 10 ** 9 + 7
> 
>     def fast_pow(base, exp):
>         if exp == 0:
>             return 1
>         half = fast_pow(base, exp // 2)
>         if exp % 2 == 0:
>             return half * half % MOD
>         return half * half % MOD * base % MOD
> 
>     even_positions = (n + 1) // 2  # indices 0, 2, 4, ...
>     odd_positions = n // 2         # indices 1, 3, 5, ...
>     return fast_pow(5, even_positions) * fast_pow(4, odd_positions) % MOD
> ```

> [!success] Complexity
> Time O(log n) for fast exponentiation. Space O(log n) call depth.

> [!tip] Alternatives
> Python's built-in `pow(base, exp, mod)` performs modular fast exponentiation in one call — use in actual interviews.

---

## Mutual / Cross-Recursion

### Wildcard Matching (LC 44)

> [!example] Problem
> Given an input string (s) and a pattern (p), implement wildcard pattern matching with support for '?' and '*' where:
> The matching should cover the entire input string (not partial).
> 
> **Example 1:**
> ```
> Input: s = "aa", p = "a"
> Output: false
> Explanation: "a" does not match the entire string "aa".
> ```
> 
> **Example 2:**
> ```
> Input: s = "aa", p = "*"
> Output: true
> Explanation: '*' matches any sequence.
> ```
> 
> **Example 3:**
> ```
> Input: s = "cb", p = "?a"
> Output: false
> Explanation: '?' matches 'c', but the second letter is 'a', which does not match 'b'.
> ```
> 
> **Constraints:**
> - 0 <= s.length, p.length <= 2000
> - s contains only lowercase English letters.
> - p contains only lowercase English letters, '?' or '*'.

> [!info] Approach
> At each position the decision branches: `?` forces a single-char match, `*` can consume 0 or more chars — mutual choices that require exploring both sub-cases. Memoisation collapses exponential branching to O(m·n). Recursive function `dp(i, j)` on indices into `s` and `p`, memoised. Base cases: both exhausted → `True`; pattern exhausted → `False`; string exhausted → remaining pattern must be all `*`. Recursive: if `p[j] == '*'`, try skip-star (`dp(i, j+1)`) or consume-one (`dp(i+1, j)`). Else if `p[j] == '?'` or `p[j] == s[i]`, advance both.


> [!note]- Python Solution
> ```python
> from functools import lru_cache
> 
> def is_match(s, p):
>     @lru_cache(maxsize=None)
>     def dp(i, j):
>         if i == len(s) and j == len(p):
>             return True
>         if j == len(p):
>             return False
>         if i == len(s):
>             return all(c == '*' for c in p[j:])
>         if p[j] == '*':
>             return dp(i, j + 1) or dp(i + 1, j)
>         if p[j] == '?' or p[j] == s[i]:
>             return dp(i + 1, j + 1)
>         return False
>     return dp(0, 0)
> ```

> [!success] Complexity
> Time O(m·n), Space O(m·n) memo table.

> [!tip] Alternatives
> Greedy: track last `*` position and last matched index — O(m+n) time, O(1) space. Bottom-up DP table also common.

---

### Regular Expression Matching (LC 10)

> [!example] Problem
> Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:
> The matching should cover the entire input string (not partial).
> 
> **Example 1:**
> ```
> Input: s = "aa", p = "a"
> Output: false
> Explanation: "a" does not match the entire string "aa".
> ```
> 
> **Example 2:**
> ```
> Input: s = "aa", p = "a*"
> Output: true
> Explanation: '*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".
> ```
> 
> **Example 3:**
> ```
> Input: s = "ab", p = ".*"
> Output: true
> Explanation: ".*" means "zero or more (*) of any character (.)".
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 20
> - 1 <= p.length <= 20
> - s contains only lowercase English letters.
> - p contains only lowercase English letters, '.', and '*'.
> - It is guaranteed for each appearance of the character '*', there will be a previous valid character to match.

> [!info] Approach
> `*` introduces a cross-recursion: either the preceding element matches and we try consuming one more char, or we skip the `x*` unit entirely — two recursive branches with shared subproblems. Memoised recursion `dp(i, j)` on string index `i` and pattern index `j`. If `j+1 < len(p)` and `p[j+1] == '*'`: either skip the `x*` pair (`dp(i, j+2)`) or, if current chars match, consume one from `s` (`dp(i+1, j)`). Otherwise if chars match (`.` or exact), advance both.


> [!note]- Python Solution
> ```python
> from functools import lru_cache
> 
> def is_match(s, p):
>     @lru_cache(maxsize=None)
>     def dp(i, j):
>         if j == len(p):
>             return i == len(s)
>         first_match = i < len(s) and p[j] in {s[i], '.'}
>         if j + 1 < len(p) and p[j + 1] == '*':
>             return dp(i, j + 2) or (first_match and dp(i + 1, j))
>         return first_match and dp(i + 1, j + 1)
>     return dp(0, 0)
> ```

> [!success] Complexity
> Time O(m·n), Space O(m·n) memo table.

> [!tip] Alternatives
> Bottom-up DP (classic interview approach). NFA simulation (Thompson's construction) gives O(m·n) without recursion.

---

## Structural Tree Recursion

### Flatten Binary Tree to Linked List (LC 114)

> [!example] Problem
> Given the root of a binary tree, flatten the tree into a "linked list"
> 
> **Example 1:**
> ```
> Input: root = [1,2,5,3,4,null,6]
> Output: [1,null,2,null,3,null,4,null,5,null,6]
> ```
> 
> **Example 2:**
> ```
> Input: root = []
> Output: []
> ```
> 
> **Example 3:**
> ```
> Input: root = [0]
> Output: [0]
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 2000].
> - -100 <= Node.val <= 100

> [!info] Approach
> Preorder visits root → left subtree → right subtree. If we recursively flatten both subtrees, we can stitch: root → flattened-left → flattened-right by connecting root.right to the left chain's tail, then moving the left chain to the right. Post-order style recursion — flatten left and right children first, then rewire. Recursively flatten `root.left` and `root.right`. Find the rightmost node of the flattened left subtree. Attach `root.right` to it, move the left chain to `root.right`, set `root.left = None`.


> [!note]- Python Solution
> ```python
> def flatten(root):
>     if not root:
>         return
>     flatten(root.left)
>     flatten(root.right)
>     if root.left:
>         tail = root.left
>         while tail.right:
>             tail = tail.right
>         tail.right = root.right
>         root.right = root.left
>         root.left = None
> ```

> [!success] Complexity
> Time O(n), Space O(h) call stack (h = tree height).

> [!tip] Alternatives
> Morris traversal: O(1) space, O(n) time — find inorder predecessor to rewire without a stack.

---

### Construct Binary Tree from Preorder and Inorder Traversal (LC 105)

> [!example] Problem
> Given two integer arrays preorder and inorder where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.
> 
> **Example 1:**
> ```
> Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
> Output: [3,9,20,null,null,15,7]
> ```
> 
> **Example 2:**
> ```
> Input: preorder = [-1], inorder = [-1]
> Output: [-1]
> ```
> 
> **Constraints:**
> - 1 <= preorder.length <= 3000
> - inorder.length == preorder.length
> - -3000 <= preorder[i], inorder[i] <= 3000
> - preorder and inorder consist of unique values.
> - Each value of inorder also appears in preorder.
> - preorder is guaranteed to be the preorder traversal of the tree.
> - inorder is guaranteed to be the inorder traversal of the tree.

> [!info] Approach
> `preorder[0]` is always the root. Its index in `inorder` splits the array into left and right subtrees. Recursion mirrors the structural decomposition. Recurse with shrinking subarrays (or index bounds + hash map for O(1) lookup). Root = `preorder[0]`. Find `mid = inorder.index(root.val)`. Left subtree uses `preorder[1:mid+1]` and `inorder[:mid]`. Right uses the remainder.


> [!note]- Python Solution
> ```python
> def build_tree(preorder, inorder):
>     if not preorder:
>         return None
>     idx = {v: i for i, v in enumerate(inorder)}
> 
>     def helper(pre_l, pre_r, in_l, in_r):
>         if pre_l > pre_r:
>             return None
>         root_val = preorder[pre_l]
>         root = TreeNode(root_val)
>         mid = idx[root_val]
>         left_size = mid - in_l
>         root.left = helper(pre_l + 1, pre_l + left_size, in_l, mid - 1)
>         root.right = helper(pre_l + left_size + 1, pre_r, mid + 1, in_r)
>         return root
> 
>     return helper(0, len(preorder) - 1, 0, len(inorder) - 1)
> ```

> [!success] Complexity
> Time O(n), Space O(n) for the index map + O(h) call stack.

> [!tip] Alternatives
> LC 106 (Postorder + Inorder): same idea, root = `postorder[-1]`.

---

### Serialize and Deserialize Binary Tree (LC 297)

> [!example] Problem
> Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.
> Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.
> Clarification: The input/output format is the same as how LeetCode serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.
> 
> **Example 1:**
> ```
> Input: root = [1,2,3,null,null,4,5]
> Output: [1,2,3,null,null,4,5]
> ```
> 
> **Example 2:**
> ```
> Input: root = []
> Output: []
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 10^4].
> - -1000 <= Node.val <= 1000

> [!info] Approach
> Preorder traversal with explicit null markers uniquely encodes any binary tree, enabling recursive reconstruction without an inorder array. Serialize via DFS preorder, emit `"#"` for nulls. Deserialize by consuming tokens from a queue. Serialize: `root.val, serialize(left), serialize(right)` joined by a delimiter. Deserialize: pop from `deque`; if `"#"` return `None`; else create node and recurse for left then right.


> [!note]- Python Solution
> ```python
> from collections import deque
> 
> class Codec:
>     def serialize(self, root):
>         parts = []
>         def dfs(node):
>             if not node:
>                 parts.append('#')
>                 return
>             parts.append(str(node.val))
>             dfs(node.left)
>             dfs(node.right)
>         dfs(root)
>         return ','.join(parts)
> 
>     def deserialize(self, data):
>         tokens = deque(data.split(','))
>         def dfs():
>             val = tokens.popleft()
>             if val == '#':
>                 return None
>             node = TreeNode(int(val))
>             node.left = dfs()
>             node.right = dfs()
>             return node
>         return dfs()
> ```

> [!success] Complexity
> Time O(n) serialize and deserialize. Space O(n) for the string and O(h) call stack.

> [!tip] Alternatives
> Level-order (BFS) serialization is also accepted and produces more compact output for wide trees.

---

### Count Complete Tree Nodes (LC 222)

> [!example] Problem
> Given the root of a complete binary tree, return the number of the nodes in the tree.
> According to Wikipedia, every level, except possibly the last, is completely filled in a complete binary tree, and all nodes in the last level are as far left as possible. It can have between 1 and 2h nodes inclusive at the last level h.
> Design an algorithm that runs in less than O(n) time complexity.
> 
> **Example 1:**
> ```
> Input: root = [1,2,3,4,5,6]
> Output: 6
> ```
> 
> **Example 2:**
> ```
> Input: root = []
> Output: 0
> ```
> 
> **Example 3:**
> ```
> Input: root = [1]
> Output: 1
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 5 * 10^4].
> - 0 <= Node.val <= 5 * 10^4
> - The tree is guaranteed to be complete.

> [!info] Approach
> In a complete binary tree, the height of the leftmost path equals the height of the rightmost path iff the left subtree is a perfect binary tree. This lets us skip half the tree per recursion level. Compute left-height and right-height at each node. If equal, left subtree is perfect → count = `2^left_h - 1 + 1` (include root) + recurse right. Else recurse left. `left_h = right_h` → left is full, so `(1 << left_h) + count(root.right)`. Otherwise `(1 << right_h) + count(root.left)`.


> [!note]- Python Solution
> ```python
> def count_nodes(root):
>     if not root:
>         return 0
>     left_h = right_h = 0
>     l, r = root, root
>     while l:
>         left_h += 1
>         l = l.left
>     while r:
>         right_h += 1
>         r = r.right
>     if left_h == right_h:
>         return (1 << left_h) - 1
>     return 1 + countNodes(root.left) + countNodes(root.right)
> ```

> [!success] Complexity
> Time O(log^2 n) — O(log n) levels, O(log n) height check each. Space O(log n) call stack.

> [!tip] Alternatives
> Binary search on node index at the last level: O(log^2 n) iterative.

---

## Combinatorial Generation

### Permutations II (LC 47)

> [!example] Problem
> Given a collection of numbers, nums, that might contain duplicates, return all possible unique permutations in any order.
> 
> **Example 1:**
> ```
> Input: nums = [1,1,2]
> Output:
> [[1,1,2],
>  [1,2,1],
>  [2,1,1]]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3]
> Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 8
> - -10 <= nums[i] <= 10

> [!info] Approach
> Duplicates at the same recursion level produce identical branches. Sorting + skipping duplicate elements at each level prunes these branches exactly. Backtracking with a `used` boolean array; sort first. Sort `nums`. At each level, skip `nums[i]` if `nums[i] == nums[i-1]` and `not used[i-1]` (sibling was already explored — ensures we always use the left duplicate before the right at any level).


> [!note]- Python Solution
> ```python
> def permute_unique(nums):
>     nums.sort()
>     result, used = [], [False] * len(nums)
> 
>     def dfs(path):
>         if len(path) == len(nums):
>             result.append(path[:])
>             return
>         for i in range(len(nums)):
>             if used[i]:
>                 continue
>             if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
>                 continue
>             used[i] = True
>             path.append(nums[i])
>             dfs(path)
>             path.pop()
>             used[i] = False
> 
>     dfs([])
>     return result
> ```

> [!success] Complexity
> Time O(n! · n) worst case (fewer unique permutations with duplicates). Space O(n) stack + O(n) used array.

> [!tip] Alternatives
> Counter-based approach: at each level iterate over unique remaining values, decrement counter, recurse, restore — avoids sort.

---

### Subsets II (LC 90)

> [!example] Problem
> Given an integer array nums that may contain duplicates, return all possible subsets (the power set).
> The solution set must not contain duplicate subsets. Return the solution in any order.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,2]
> Output: [[],[1],[1,2],[1,2,2],[2],[2,2]]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0]
> Output: [[],[0]]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10
> - -10 <= nums[i] <= 10

> [!info] Approach
> Same duplicate-skip strategy as Permutations II but applied to the combination/subset template. At each index in a sorted array, skip if current equals previous and previous was not part of the current path extension. Sort + backtracking; record path at every node, skip duplicate siblings. Sort `nums`. In the loop `for i in range(start, n)`: if `i > start and nums[i] == nums[i-1]`, skip. Append path snapshot, continue.


> [!note]- Python Solution
> ```python
> def subsets_with_dup(nums):
>     nums.sort()
>     result = []
> 
>     def dfs(start, path):
>         result.append(path[:])
>         for i in range(start, len(nums)):
>             if i > start and nums[i] == nums[i - 1]:
>                 continue
>             path.append(nums[i])
>             dfs(i + 1, path)
>             path.pop()
> 
>     dfs(0, [])
>     return result
> ```

> [!success] Complexity
> Time O(2^n · n), Space O(n) call stack.

> [!tip] Alternatives
> Iterative: maintain result list, for each new number only extend subsets added in the previous round (when it is a duplicate run).

---

### Combinations (LC 77)

> [!example] Problem
> Given two integers n and k, return all possible combinations of k numbers chosen from the range [1, n].
> You may return the answer in any order.
> 
> **Example 1:**
> ```
> Input: n = 4, k = 2
> Output: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
> Explanation: There are 4 choose 2 = 6 total combinations.
> Note that combinations are unordered, i.e., [1,2] and [2,1] are considered to be the same combination.
> ```
> 
> **Example 2:**
> ```
> Input: n = 1, k = 1
> Output: [[1]]
> Explanation: There is 1 choose 1 = 1 total combination.
> ```
> 
> **Constraints:**
> - 1 <= n <= 20
> - 1 <= k <= n

> [!info] Approach
> Classic choose-k-from-n combinatorial generation. At each level choose one number ≥ current start, recurse with start+1 until path length equals k. Backtracking with a start index and path length guard. Prune early: if remaining elements `n - i + 1 < k - len(path)`, no valid completion possible — skip.


> [!note]- Python Solution
> ```python
> def combine(n, k):
>     result = []
> 
>     def dfs(start, path):
>         if len(path) == k:
>             result.append(path[:])
>             return
>         for i in range(start, n + 1):
>             if n - i + 1 < k - len(path):
>                 break  # pruning: not enough elements left
>             path.append(i)
>             dfs(i + 1, path)
>             path.pop()
> 
>     dfs(1, [])
>     return result
> ```

> [!success] Complexity
> Time O(C(n,k) · k), Space O(k) call stack.

> [!tip] Alternatives
> Iterative using `itertools.combinations`. For large n/k, the pruning bound `n - i + 1 >= k - len(path)` halves the search space significantly.

---

## Divide and Conquer — Advanced

### Maximum Subarray — D&C (O(n log n))

> [!example] Problem
> Given an integer array nums, find the subarray with the largest sum, and return its sum.
> 
> **Example 1:**
> ```
> Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
> Output: 6
> Explanation: The subarray [4,-1,2,1] has the largest sum 6.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1]
> Output: 1
> Explanation: The subarray [1] has the largest sum 1.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [5,4,-1,7,8]
> Output: 23
> Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - -10^4 <= nums[i] <= 10^4

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
>                 merged.append(left[i]); i += 1
>             else:
>                 merged.append(right[j]); j += 1
>                 mc += len(left) - i  # inversions with all remaining left elements
>         merged.extend(left[i:]); merged.extend(right[j:])
>         return merged, lc + rc + mc
>     _, count = merge_sort(nums)
>     return count
> ```

> [!success] Complexity
> Time O(n log n), Space O(n) merge buffer + O(log n) call stack.

> [!tip] Alternatives
> BIT (Binary Indexed Tree) / Fenwick Tree approach: coordinate compress then count using prefix sums — O(n log n), O(n) space.

---

## Recursion on Graphs

### Clone Graph (LC 133)

> [!example] Problem
> Given a reference of a node in a connected undirected graph.
> Return a deep copy (clone) of the graph.
> Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.
> Test case format:
> For simplicity, each node's value is the same as the node's index (1-indexed). For example, the first node with val == 1, the second node with val == 2, and so on. The graph is represented in the test case using an adjacency list.
> An adjacency list is a collection of unordered lists used to represent a finite graph. Each list describes the set of neighbors of a node in the graph.
> The given node will always be the first node with val = 1. You must return the copy of the given node as a reference to the cloned graph.
> 
> **Example 1:**
> ```
> class Node {
>     public int val;
>     public List neighbors;
> }
> ```
> 
> **Example 2:**
> ```
> Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
> Output: [[2,4],[1,3],[2,4],[1,3]]
> Explanation: There are 4 nodes in the graph.
> 1st node (val = 1)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
> 2nd node (val = 2)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).
> 3rd node (val = 3)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
> 4th node (val = 4)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).
> ```
> 
> **Example 3:**
> ```
> Input: adjList = [[]]
> Output: [[]]
> Explanation: Note that the input contains one empty list. The graph consists of only one node with val = 1 and it does not have any neighbors.
> ```
> 
> **Example 4:**
> ```
> Input: adjList = []
> Output: []
> Explanation: This an empty graph, it does not have any nodes.
> ```
> 
> **Constraints:**
> - The number of nodes in the graph is in the range [0, 100].
> - 1 <= Node.val <= 100
> - Node.val is unique for each node.
> - There are no repeated edges and no self-loops in the graph.
> - The Graph is connected and all nodes can be visited starting from the given node.

> [!info] Approach
> DFS naturally visits each node once; a hash map from original → clone prevents revisiting and handles cycles. DFS with a `visited` dict mapping original nodes to their clones. If node already in `visited`, return its clone. Otherwise create a new node, record it in `visited`, then recursively clone each neighbor and append to the new node's neighbors list.


> [!note]- Python Solution
> ```python
> def clone_graph(node):
>     if not node:
>         return None
>     visited = {}
> 
>     def dfs(n):
>         if n in visited:
>             return visited[n]
>         clone = Node(n.val)
>         visited[n] = clone
>         for neighbor in n.neighbors:
>             clone.neighbors.append(dfs(neighbor))
>         return clone
> 
>     return dfs(node)
> ```

> [!success] Complexity
> Time O(V + E), Space O(V) for the visited map + O(V) call stack in worst case (linear graph).

> [!tip] Alternatives
> BFS version: use a deque, same visited map. Useful when stack depth is a concern for large graphs.

---

### Number of Islands (LC 200)

> [!example] Problem
> Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.
> An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.
> 
> **Example 1:**
> ```
> Input: grid = [
>   ["1","1","1","1","0"],
>   ["1","1","0","1","0"],
>   ["1","1","0","0","0"],
>   ["0","0","0","0","0"]
> ]
> Output: 1
> ```
> 
> **Example 2:**
> ```
> Input: grid = [
>   ["1","1","0","0","0"],
>   ["1","1","0","0","0"],
>   ["0","0","1","0","0"],
>   ["0","0","0","1","1"]
> ]
> Output: 3
> ```
> 
> **Constraints:**
> - m == grid.length
> - n == grid[i].length
> - 1 <= m, n <= 300
> - grid[i][j] is '0' or '1'.

> [!info] Approach
> DFS flood-fill: when a `'1'` is found, recursively sink the entire connected land mass (mark as `'0'`) so it is never counted again. Each DFS call corresponds to one island. Iterate over all cells; on encountering `'1'`, increment count and launch DFS to mark the island. DFS marks `grid[r][c] = '0'` then recurses into all 4 directions if in-bounds and `== '1'`.


> [!note]- Python Solution
> ```python
> def num_islands(grid):
>     if not grid:
>         return 0
>     rows, cols = len(grid), len(grid[0])
>     count = 0
> 
>     def dfs(r, c):
>         if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
>             return
>         grid[r][c] = '0'
>         dfs(r + 1, c); dfs(r - 1, c)
>         dfs(r, c + 1); dfs(r, c - 1)
> 
>     for r in range(rows):
>         for c in range(cols):
>             if grid[r][c] == '1':
>                 count += 1
>                 dfs(r, c)
>     return count
> ```

> [!success] Complexity
> Time O(m·n), Space O(m·n) call stack worst case (all land).

> [!tip] Alternatives
> BFS (deque) avoids deep recursion. Union-Find gives O(m·n · α(m·n)) — preferred when merging is incremental.

---

## Recursive Parsing / Evaluation

### Basic Calculator II (LC 227)

> [!example] Problem
> Given a string s which represents an expression, evaluate this expression and return its value.
> The integer division should truncate toward zero.
> You may assume that the given expression is always valid. All intermediate results will be in the range of [-231, 231 - 1].
> Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().
> 
> **Example 1:**
> ```
> Input: s = "3+2*2"
> Output: 7
> ```
> 
> **Example 2:**
> ```
> Input: s = " 3/2 "
> Output: 1
> ```
> 
> **Example 3:**
> ```
> Input: s = " 3+5 / 2 "
> Output: 5
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 3 * 10^5
> - s consists of integers and operators ('+', '-', '*', '/') separated by some number of spaces.
> - s represents a valid expression.
> - All the integers in the expression are non-negative integers in the range [0, 2^{31} - 1].
> - The answer is guaranteed to fit in a 32-bit integer.

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
>             op = s[idx[0]]; idx[0] += 1
>             right = parse_number()
>             val = val * right if op == '*' else int(val / right)
>         return val
> 
>     def parse_expr():
>         val = parse_term()
>         while idx[0] < len(s) and s[idx[0]] in '+-':
>             op = s[idx[0]]; idx[0] += 1
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

### Evaluate Division (LC 399)

> [!example] Problem
> You are given an array of variable pairs equations and an array of real numbers values, where equations[i] = [Ai, Bi] and values[i] represent the equation Ai / Bi = values[i]. Each Ai or Bi is a string that represents a single variable.
> You are also given some queries, where queries[j] = [Cj, Dj] represents the jth query where you must find the answer for Cj / Dj = ?.
> Return the answers to all queries. If a single answer cannot be determined, return -1.0.
> Note: The input is always valid. You may assume that evaluating the queries will not result in division by zero and that there is no contradiction.
> Note: The variables that do not occur in the list of equations are undefined, so the answer cannot be determined for them.
> 
> **Example 1:**
> ```
> Input: equations = [["a","b"],["b","c"]], values = [2.0,3.0], queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
> Output: [6.00000,0.50000,-1.00000,1.00000,-1.00000]
> Explanation: 
> Given: a / b = 2.0, b / c = 3.0
> queries are: a / c = ?, b / a = ?, a / e = ?, a / a = ?, x / x = ? 
> return: [6.0, 0.5, -1.0, 1.0, -1.0 ]
> note: x is undefined => -1.0
> ```
> 
> **Example 2:**
> ```
> Input: equations = [["a","b"],["b","c"],["bc","cd"]], values = [1.5,2.5,5.0], queries = [["a","c"],["c","b"],["bc","cd"],["cd","bc"]]
> Output: [3.75000,0.40000,5.00000,0.20000]
> ```
> 
> **Example 3:**
> ```
> Input: equations = [["a","b"]], values = [0.5], queries = [["a","b"],["b","a"],["a","c"],["x","y"]]
> Output: [0.50000,2.00000,-1.00000,-1.00000]
> ```
> 
> **Constraints:**
> - 1 <= equations.length <= 20
> - equations[i].length == 2
> - 1 <= Ai.length, Bi.length <= 5
> - values.length == equations.length
> - 0.0 < values[i] <= 20.0
> - 1 <= queries.length <= 20
> - queries[i].length == 2
> - 1 <= Cj.length, Dj.length <= 5
> - Ai, Bi, Cj, Dj consist of lower case English letters and digits.

> [!info] Approach
> Model as a weighted directed graph: edge `a → b` has weight `val`, edge `b → a` has weight `1/val`. A query `x/y` is a path product from `x` to `y` — DFS with running product. Build adjacency list, then DFS for each query. DFS from `src` to `dst`, multiplying edge weights along the path, using a `visited` set to avoid cycles. Return accumulated product or `-1.0` if destination unreachable.


> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def calc_equation(equations, values, queries):
>     graph = defaultdict(dict)
>     for (a, b), val in zip(equations, values):
>         graph[a][b] = val
>         graph[b][a] = 1.0 / val
> 
>     def dfs(src, dst, visited):
>         if src not in graph or dst not in graph:
>             return -1.0
>         if src == dst:
>             return 1.0
>         visited.add(src)
>         for neighbor, weight in graph[src].items():
>             if neighbor in visited:
>                 continue
>             result = dfs(neighbor, dst, visited)
>             if result != -1.0:
>                 return weight * result
>         return -1.0
> 
>     return [dfs(a, b, set()) for a, b in queries]
> ```

> [!success] Complexity
> Time O(Q · (V + E)) where Q = number of queries. Space O(V + E) for the graph.

> [!tip] Alternatives
> Union-Find with weighted edges (O(α(V)) per query after build). Floyd-Warshall O(V^3) preprocessing for O(1) queries — viable when V is small.

---

## See Also

[[dynamic-programming]] | [[backtracking]] | [[tree]] | [[divide-and-conquer]]
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

## Recursion — More Problems

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
> This is a minimax recursion. From any subarray `[i, j]`, the current player picks the end that maximises their net advantage (their score minus the opponent's future score). If the first player's net advantage from the full array is ≥ 0, they win. `dp(i, j)` = maximum score advantage the current player can achieve over the opponent from subarray `[i, j]`. Base: `dp(i, i) = nums[i]`. Recurrence: `max(nums[i] - dp(i+1, j), nums[j] - dp(i, j-1))`. Memoize with `@lru_cache`. Return `dp(0, n-1) >= 0`.


> [!note]- Python Solution
> ```python
> from functools import lru_cache
> >
> def predict_the_winner(nums):
>     n = len(nums)
> >
>     @lru_cache(maxsize=None)
>     def dp(i, j):
>         if i == j:
>             return nums[i]
>         pick_left = nums[i] - dp(i + 1, j)
>         pick_right = nums[j] - dp(i, j - 1)
>         return max(pick_left, pick_right)
> >
>     return dp(0, n - 1) >= 0
> ```

> [!success] Complexity
> Time O(n²), Space O(n²).

> [!tip] Alternatives
> - Bottom-up DP: fill a 2D table by diagonal (subarray length). Same asymptotic complexity, avoids recursion stack.
> - Key insight: `dp(i, j)` represents the *net advantage* (current player's gain minus opponent's gain) — not the absolute score. This collapses the two-player tracking into one value.

---

### Flatten Nested List Iterator (LC 341)

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
> Lazy flattening with a stack: push the full list onto the stack. When `hasNext()` is called, peel the top until an integer is at the top. `next()` then pops and returns it. Stack holds iterators (via index pointers or list iterators). When the top element is a list, push the new list's iterator. When it's an integer, it's ready to be returned. Use a stack of `(nested_list, index)` pairs. `_advance()` is called by `hasNext()` to ensure the top is an integer.


> [!note]- Python Solution
> ```python
> class NestedIterator:
>     def __init__(self, nestedList):
>         self.stack = [(nestedList, 0)]
> >
>     def _advance(self):
>         while self.stack:
>             lst, idx = self.stack[-1]
>             if idx == len(lst):
>                 self.stack.pop()
>             elif lst[idx].isInteger():
>                 return
>             else:
>                 self.stack[-1] = (lst, idx + 1)
>                 self.stack.append((lst[idx].getList(), 0))
> >
>     def next(self):
>         self._advance()
>         lst, idx = self.stack[-1]
>         self.stack[-1] = (lst, idx + 1)
>         return lst[idx].getInteger()
> >
>     def has_next(self):
>         self._advance()
>         return bool(self.stack)
> ```

> [!success] Complexity
> Time O(1) amortized per `next()` / `hasNext()`. Space O(d) where d = nesting depth.

> [!tip] Alternatives
> - Pre-flatten in `__init__`: collect all integers into a deque. Simplest to code but not lazy — could be slow if only a few values are ever consumed.
> - Recursive generator with `yield from`: elegant but interviewers often want the explicit stack version.

---

## See Also

[[dynamic-programming]] | [[backtracking]] | [[tree]] | [[stack]]
