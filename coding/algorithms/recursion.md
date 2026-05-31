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
> Return all subsets (including empty set) of a list of unique integers.

> [!info] Approach
> - **WHY:** Every element has exactly two choices — include or exclude. The 2^n subsets map to all binary strings of length n. Overlapping structure: subsets of `nums[0..i-1]` are extended by the decision on `nums[i]`.
> - **WHAT:** DFS/backtracking over the array; at each index, branch into "include" and "exclude".
> - **HOW:** At index `i`, add current path to results, then recurse with `i+1` after optionally appending `nums[i]`. Or equivalently: iterate from `i` to `n`, choose `nums[j]`, recurse from `j+1`.

> [!note]- Python Solution
> ```python
> def subsets(nums: list[int]) -> list[list[int]]:
>     result: list[list[int]] = []
> 
>     def dfs(start: int, path: list[int]) -> None:
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
> Return all permutations of a list of distinct integers.

> [!info] Approach
> - **WHY:** n! orderings; at each position, any unused element can be placed. Backtracking explores all placements, undoing each choice before trying the next.
> - **WHAT:** At each recursion level, pick one unused element, add it, recurse with remaining.
> - **HOW:** Swap `nums[i]` with `nums[start]`, recurse with `start+1`, swap back (in-place backtracking preserves O(1) space overhead per level).

> [!note]- Python Solution
> ```python
> def permute(nums: list[int]) -> list[list[int]]:
>     result: list[list[int]] = []
> 
>     def dfs(start: int) -> None:
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
> Find all root-to-leaf paths in a binary tree.

> [!info] Approach
> - **WHY:** Tree structure is inherently recursive; each subtree is a smaller instance of the same problem. No backtracking needed since strings are immutable (pass by value).
> - **WHAT:** DFS from root; accumulate path string; record when leaf is reached.
> - **HOW:** Base case = leaf node → append path to result. Recursive case = recurse left and right with extended path string.

> [!note]- Python Solution
> ```python
> def binaryTreePaths(root) -> list[str]:
>     result: list[str] = []
> 
>     def dfs(node, path: str) -> None:
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
> - **WHY:** Sorting n items can be decomposed into sorting two halves independently (no overlap between halves) and merging in O(n). Recursion handles the split; the merge step is the key.
> - **WHAT:** Split array at midpoint, sort each half recursively, merge the two sorted halves.
> - **HOW:** Base case = length ≤ 1. Split, conquer left, conquer right, merge in O(n) with two-pointer technique.

> [!note]- Python Solution
> ```python
> def mergeSort(nums: list[int]) -> list[int]:
>     if len(nums) <= 1:
>         return nums
>     mid = len(nums) // 2
>     left = mergeSort(nums[:mid])
>     right = mergeSort(nums[mid:])
>     return merge(left, right)
> 
> def merge(left: list[int], right: list[int]) -> list[int]:
>     result: list[int] = []
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
> - **WHY:** Naive recursion `f(n) = f(n-1) + f(n-2)` calls `f(k)` exponentially many times for overlapping `k`. Memoization caches each call once → O(n).
> - **WHAT:** Memoized recursion (top-down DP) vs iterative DP (bottom-up). Both O(n) time O(n) space; iterative reduces to O(1) space.
> - **HOW:** Memoize using a dict or `@lru_cache`. For O(1) space, use two variables.

> [!note]- Python Solution
> ```python
> from functools import lru_cache
> 
> # Top-down memoized recursion
> @lru_cache(maxsize=None)
> def fib_memo(n: int) -> int:
>     if n <= 1:
>         return n
>     return fib_memo(n - 1) + fib_memo(n - 2)
> 
> # Bottom-up DP — O(1) space
> def fib_dp(n: int) -> int:
>     if n <= 1:
>         return n
>     prev2, prev1 = 0, 1
>     for _ in range(2, n + 1):
>         prev2, prev1 = prev1, prev2 + prev1
>     return prev1
> ```

> [!success] Complexity
> Time O(n), Space O(n) for memoization / O(1) for iterative.

> [!tip] Alternatives
> Matrix exponentiation for O(log n). Naive recursion is O(2^n) — never use without memoization.

---

## Pruning & Constraints

### Combination Sum (Unbounded)

> [!example] Problem
> Find all combinations from `candidates` that sum to `target`. Same element reusable.

> [!info] Approach
> - **WHY:** Unbounded choices — reuse is allowed. Backtracking explores all paths; pruning on `remaining < 0` cuts branches.
> - **WHAT:** DFS from index `start`; at each step include `candidates[i]` and stay at `i` (reuse) or move to `i+1`.
> - **HOW:** Recurse with `(start=i, remaining-candidates[i])`. Backtrack by popping. Sort candidates for early termination.

> [!note]- Python Solution
> ```python
> def combinationSum(candidates: list[int], target: int) -> list[list[int]]:
>     candidates.sort()
>     result: list[list[int]] = []
> 
>     def dfs(start: int, path: list[int], remaining: int) -> None:
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
> Find all unique combinations from `candidates` (may have duplicates) summing to `target`. Each element used at most once.

> [!info] Approach
> - **WHY:** Elements can repeat in input but not in output combinations. Key: sort + skip-duplicate guard prevents generating `[1a, 2]` and `[1b, 2]` separately when two `1`s exist.
> - **WHAT:** Same DFS but recurse with `i+1` and skip `candidates[j] == candidates[j-1]` when `j > start`.
> - **HOW:** `if j > start and candidates[j] == candidates[j-1]: continue` — only skip siblings, not the first occurrence at a level.

> [!note]- Python Solution
> ```python
> def combinationSum2(candidates: list[int], target: int) -> list[list[int]]:
>     candidates.sort()
>     result: list[list[int]] = []
> 
>     def dfs(start: int, path: list[int], remaining: int) -> None:
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
> Generate all valid combinations of `n` pairs of parentheses.

> [!info] Approach
> - **WHY:** Validity constraints are locally checkable at each position — prune invalid branches without generating full strings.
> - **WHAT:** DFS building the string character by character. State = `(open_count, close_count)`.
> - **HOW:** Add `(` if `open < n`; add `)` if `close < open`. Leaf = string of length `2n`.

> [!note]- Python Solution
> ```python
> def generateParenthesis(n: int) -> list[str]:
>     result: list[str] = []
> 
>     def dfs(path: list[str], open_c: int, close_c: int) -> None:
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
> Given a 2D board and a word, check if the word exists as a connected path in the grid (4-directional, no revisiting).

> [!info] Approach
> - **WHY:** Exponential state space of paths; backtracking explores all starting positions and directions, pruning when the current character doesn't match.
> - **WHAT:** DFS from each cell; mark visited in-place (avoid extra space); restore on backtrack.
> - **HOW:** Mark `board[r][c]` with a sentinel (e.g., `'#'`) before recursing, restore after. Check bounds and match before recursing.

> [!note]- Python Solution
> ```python
> def exist(board: list[list[str]], word: str) -> bool:
>     rows, cols = len(board), len(board[0])
> 
>     def dfs(r: int, c: int, idx: int) -> bool:
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
> Return all ways to partition string `s` such that every substring is a palindrome.

> [!info] Approach
> - **WHY:** Exponential number of partitions; prune by only recursing on palindromic prefixes. Precomputing `is_pal[i][j]` eliminates repeated palindrome checks.
> - **WHAT:** DFS from `start`; at each position try all palindromic prefixes starting at `start`.
> - **HOW:** Precompute `is_pal` in O(n²). DFS: for each `end ≥ start`, if `is_pal[start][end]`, add substring and recurse from `end+1`.

> [!note]- Python Solution
> ```python
> def partition(s: str) -> list[list[str]]:
>     n = len(s)
>     is_pal = [[False] * n for _ in range(n)]
>     for i in range(n - 1, -1, -1):
>         for j in range(i, n):
>             is_pal[i][j] = s[i] == s[j] and (j - i < 2 or is_pal[i+1][j-1])
> 
>     result: list[list[str]] = []
> 
>     def dfs(start: int, path: list[str]) -> None:
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
> Given string `s`, for each letter, toggle between upper and lower case. Return all possible strings.

> [!info] Approach
> - **WHY:** Each letter creates a binary branch (upper/lower); digits have no branch. Backtracking with character-level mutation.
> - **WHAT:** DFS character by character; digits pass through; letters branch into two calls.
> - **HOW:** At index `i`, if digit: recurse with `i+1`. If letter: set lowercase, recurse, set uppercase, recurse.

> [!note]- Python Solution
> ```python
> def letterCasePermutation(s: str) -> list[str]:
>     result: list[str] = []
>     chars = list(s)
> 
>     def dfs(i: int) -> None:
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
> Place N queens on an N×N board so no two queens attack each other.

> [!info] Approach
> - **WHY:** 8^8 brute force positions; backtracking with clash sets prunes immediately when a queen attacks another. At most N! leaves to visit (one queen per row).
> - **WHAT:** Place one queen per row; track occupied columns and diagonals.
> - **HOW:** Track sets `cols`, `diag1` (r-c), `diag2` (r+c). For each row, try each column not in any set; add to sets, recurse, remove.

> [!note]- Python Solution
> ```python
> def solveNQueens(n: int) -> list[list[str]]:
>     result: list[list[str]] = []
>     queens: list[int] = []  # queens[r] = column of queen in row r
>     cols: set[int] = set()
>     diag1: set[int] = set()  # r - c
>     diag2: set[int] = set()  # r + c
> 
>     def dfs(row: int) -> None:
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
> Fill empty cells in a 9×9 Sudoku board to satisfy all constraints.

> [!info] Approach
> - **WHY:** Constraint satisfaction; 9 choices per empty cell but constraints prune rapidly. Backtracking with early exit on first valid solution.
> - **WHAT:** Find next empty cell, try digits 1-9, check validity, recurse.
> - **HOW:** Precompute sets for each row, column, and 3×3 box. At each empty cell, try only valid digits; backtrack immediately on failure.

> [!note]- Python Solution
> ```python
> def solveSudoku(board: list[list[str]]) -> None:
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
>     def solve() -> bool:
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
> Given a board and a list of words, find all words present in the board.

> [!info] Approach
> - **WHY:** Running Word Search separately for each word is O(W · m·n · 4^L). A Trie lets one DFS pass check all words simultaneously — prune when the current path isn't a prefix of any word.
> - **WHAT:** Build Trie from word list. DFS from each cell; follow Trie nodes; when a terminal node is reached, record the word.
> - **HOW:** At each cell, check `trie_node.children[char]`. If present, descend. If `trie_node.word`, add to results. Mark visited, recurse 4 directions, unmark. Prune exhausted Trie subtrees.

> [!note]- Python Solution
> ```python
> def findWords(board: list[list[str]], words: list[str]) -> list[str]:
>     # Build Trie
>     trie: dict = {}
>     for w in words:
>         node = trie
>         for ch in w:
>             node = node.setdefault(ch, {})
>         node['#'] = w  # terminal marker stores the word
> 
>     rows, cols = len(board), len(board[0])
>     result: list[str] = []
> 
>     def dfs(r: int, c: int, node: dict) -> None:
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
> Generate all structurally unique BSTs with values 1 to n.

> [!info] Approach
> - **WHY:** Each integer `k` in `[1..n]` can be the root; values `1..k-1` form the left subtree and `k+1..n` form the right subtree. Recursive structure — memoize on `(lo, hi)`.
> - **WHAT:** Return all possible root nodes for the BST using values `lo` to `hi`.
> - **HOW:** For each root `k` in `[lo, hi]`, generate all left subtrees (using `lo..k-1`) and all right subtrees (using `k+1..hi`), combine every pair.

> [!note]- Python Solution
> ```python
> from functools import lru_cache
> 
> class TreeNode:
>     def __init__(self, val=0, left=None, right=None):
>         self.val = val; self.left = left; self.right = right
> 
> def generateTrees(n: int) -> list:
>     @lru_cache(maxsize=None)
>     def build(lo: int, hi: int) -> list:
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
> Given a string of digits and a target, insert `+`, `-`, `*` between digits to reach target. Return all valid expressions.

> [!info] Approach
> - **WHY:** Exponential operator assignments require backtracking. Multiplication's precedence requires tracking the previously added operand to undo and reapply multiplication.
> - **WHAT:** DFS building expression string; carry `curr_val` (running value) and `prev_operand` (last added term, for `*` precedence).
> - **HOW:** For each position, try each multi-digit number (avoid leading zeros). On `*`: `curr_val = curr_val - prev_operand + prev_operand * num`; on `+/-`: standard addition.

> [!note]- Python Solution
> ```python
> def addOperators(num: str, target: int) -> list[str]:
>     result: list[str] = []
>     n = len(num)
> 
>     def dfs(index: int, path: str, curr_val: int, prev_operand: int) -> None:
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
> Given an API-based robot in an unknown grid (can move forward, turn right/left, clean), clean every reachable cell.

> [!info] Approach
> - **WHY:** Unknown grid topology — must explore via state-space DFS. Track visited coordinates; after each branch, return the robot to the previous position and heading (backtracking).
> - **WHAT:** DFS in four directions; track `(row, col)` in visited set; after exploring a subtree, reverse the robot back.
> - **HOW:** Try each of 4 directions (relative to current heading using direction vectors). On return: turn 180°, move forward, turn 180° to restore position+heading.

> [!note]- Python Solution
> ```python
> def cleanRoom(robot) -> None:
>     # Directions: up, right, down, left (relative to heading 0)
>     dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
>     visited: set = set()
> 
>     def go_back() -> None:
>         robot.turnRight(); robot.turnRight()
>         robot.move()
>         robot.turnRight(); robot.turnRight()
> 
>     def dfs(r: int, c: int, direction: int) -> None:
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
> Search for a target in a sorted array. Return its index or -1.

> [!info] Approach
> - **WHY:** The array is sorted — at each step the search space halves by comparing the midpoint. Recursion mirrors the decision tree: go left or go right.
> - **WHAT:** Compute mid; if `nums[mid] == target` return mid; recurse on left or right half.
> - **HOW:** Pass `lo`, `hi` as parameters. Base case: `lo > hi` → return -1. No extra space beyond call stack.

> [!note]- Python Solution
> ```python
> def binarySearch(nums: list[int], target: int, lo: int = 0, hi: int = -1) -> int:
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
> - **WHY:** The recurrence is T(n) = 2T(n-1) + 1. Moving `n` disks = move top `n-1` to B (using C), move largest to C, move `n-1` from B to C (using A). Classic divide-and-conquer recursion with no overlapping subproblems.
> - **WHAT:** Recursion with three named pegs; base case is 1 disk.
> - **HOW:** `hanoi(n-1, src, aux, dst)` → move disk n → `hanoi(n-1, aux, src, dst)`.

> [!note]- Python Solution
> ```python
> def hanoi(n: int, src: str, aux: str, dst: str) -> list[tuple[str, str]]:
>     moves: list[tuple[str, str]] = []
> 
>     def solve(k: int, s: str, a: str, d: str) -> None:
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
> - **WHY:** Each element has exactly two choices — include or exclude. The include/exclude recursion tree has 2^n leaves, each representing one subsequence.
> - **WHAT:** DFS from index 0; branch into "include `arr[i]`" and "exclude `arr[i]`"; print at leaf.
> - **HOW:** Carry a running `path`. At index == n, print path. Recurse both branches at each step.

> [!note]- Python Solution
> ```python
> def print_subsequences(arr: list[int]) -> list[list[int]]:
>     result: list[list[int]] = []
> 
>     def dfs(index: int, path: list[int]) -> None:
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
> - **WHY:** After each elimination the circle shrinks by 1 and the indices shift. The recurrence `J(n,k) = (J(n-1,k) + k) % n` computes the survivor's position in the reduced circle and maps it back to the original numbering.
> - **WHAT:** Recursive formula: `J(1,k) = 0`; `J(n,k) = (J(n-1,k) + k) % n`.
> - **HOW:** Memoize or convert to iteration to avoid O(n) stack depth.

> [!note]- Python Solution
> ```python
> # Recursive (clean but O(n) stack)
> def josephus_recursive(n: int, k: int) -> int:
>     if n == 1:
>         return 0
>     return (josephus_recursive(n - 1, k) + k) % n
> 
> # Iterative (O(1) space)
> def josephus(n: int, k: int) -> int:
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
> Given a DAG with nodes 0 to n-1, find all paths from node 0 to node n-1.

> [!info] Approach
> - **WHY:** DAG has no cycles so recursion terminates naturally. Backtracking explores all paths without needing an explicit visited set (DAG guarantees no revisit loops).
> - **WHAT:** DFS from 0; at each node extend path along all neighbors; record when node n-1 is reached.
> - **HOW:** Backtrack by appending node, recursing through neighbors, then popping.

> [!note]- Python Solution
> ```python
> def allPathsSourceTarget(graph: list[list[int]]) -> list[list[int]]:
>     target = len(graph) - 1
>     result: list[list[int]] = []
> 
>     def dfs(node: int, path: list[int]) -> None:
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
> Decode an encoded string where `k[encoded_string]` means repeat `encoded_string` k times. E.g., `"3[a2[c]]"` → `"accaccacc"`.

> [!info] Approach
> - **WHY:** Nested brackets are naturally recursive — decoding the inner bracket is a subproblem of the same type. Recursion with an index pointer consumes the string in one pass.
> - **WHAT:** Recursive descent parser; when `[` is encountered, recurse; when `]` is encountered, return current decoded string.
> - **HOW:** Pass a mutable index (via list). Accumulate digits for `k`, accumulate chars for the current segment, recurse on `[`, multiply result on `]`.

> [!note]- Python Solution
> ```python
> def decodeString(s: str) -> str:
>     idx = [0]  # mutable index shared across frames
> 
>     def decode() -> str:
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
> Given a nested list of integers (each element is an integer or a list of integers, arbitrarily nested), flatten it into a single list of integers.

> [!info] Approach
> - **WHY:** Nested structure is recursively defined — a list element is either an integer (base case) or another list (recursive case).
> - **WHAT:** DFS through the nested list; at each element, if integer → add to result; if list → recurse.
> - **HOW:** Single recursive function that iterates over the current list and dispatches based on element type.

> [!note]- Python Solution
> ```python
> from typing import Union
> 
> NestedList = list[Union[int, list]]  # simplified type alias
> 
> def flatten(nested: NestedList) -> list[int]:
>     result: list[int] = []
> 
>     def dfs(item) -> None:
>         if isinstance(item, int):
>             result.append(item)
>         else:
>             for element in item:
>                 dfs(element)
>
>     dfs(nested)
>     return result
>
> # LeetCode NestedInteger API version
> def flattenNestedList(nestedList) -> list[int]:
>     result: list[int] = []
>
>     def dfs(nl) -> None:
>         for item in nl:
>             if item.isInteger():
>                 result.append(item.getInteger())
>             else:
>                 dfs(item.getList())
>
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
> Given a nested list of integers, return the sum of all integers weighted by their depth. E.g., `[1,[4,[6]]]` → `1*1 + 4*2 + 6*3 = 27`.

> [!info] Approach
> - **WHY:** Each nesting level increments the depth multiplier — a natural recursion where the depth parameter is passed down.
> - **WHAT:** Recursive DFS; carry `depth` parameter; add `value * depth` for integers; recurse with `depth + 1` for nested lists.
> - **HOW:** Start with `depth=1`. At each integer, accumulate `val * depth`. At each list, recurse with `depth + 1`.

> [!note]- Python Solution
> ```python
> def depthSum(nestedList, depth: int = 1) -> int:
>     total = 0
>     for item in nestedList:
>         if item.isInteger():
>             total += item.getInteger() * depth
>         else:
>             total += depthSum(item.getList(), depth + 1)
>     return total
>
> # Pure Python version (no NestedInteger API)
> def depthSumPure(nested, depth: int = 1) -> int:
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
> Count distinct ways to climb n stairs, taking 1 or 2 steps at a time.

> [!info] Approach
> - **WHY:** At each stair, you can arrive from stair `n-1` (one step) or stair `n-2` (two steps). The problem has optimal substructure and overlapping subproblems — identical to Fibonacci.
> - **WHAT:** `ways(n) = ways(n-1) + ways(n-2)` with `ways(0) = 1`, `ways(1) = 1`. Memoize to avoid recomputation.
> - **HOW:** `@lru_cache` or manual dict. Can extend to k steps: `ways(n) = sum(ways(n-i) for i in 1..k if n-i >= 0)`.

> [!note]- Python Solution
> ```python
> from functools import lru_cache
> 
> @lru_cache(maxsize=None)
> def climbStairs(n: int) -> int:
>     if n <= 1:
>         return 1
>     return climbStairs(n - 1) + climbStairs(n - 2)
> 
> # Generalised: k distinct step sizes
> def climbStairsK(n: int, steps: list[int]) -> int:
>     from functools import lru_cache
> 
>     @lru_cache(maxsize=None)
>     def dp(remaining: int) -> int:
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
> A digit string of length `n` is "good" if digits at even indices are even (0,2,4,6,8) and digits at odd indices are prime (2,3,5,7). Count good strings of length `n` modulo 10^9+7. (LeetCode 1922)

> [!info] Approach
> - **WHY:** The count factorises: `5^(ceil(n/2)) * 4^(floor(n/2))`. Computing large powers requires fast exponentiation (recursive divide-and-conquer).
> - **WHAT:** `countGoodNumbers(n) = pow(5, even_positions) * pow(4, odd_positions) % MOD`.
> - **HOW:** Even positions = `ceil(n/2)` = `(n+1)//2`. Odd positions = `floor(n/2)` = `n//2`. Use recursive fast-power.

> [!note]- Python Solution
> ```python
> def countGoodNumbers(n: int) -> int:
>     MOD = 10 ** 9 + 7
> 
>     def fast_pow(base: int, exp: int) -> int:
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
> Given a string `s` and a pattern `p` containing `?` (matches any single character) and `*` (matches any sequence including empty), return `True` if `p` matches `s` entirely.

> [!info] Approach
> - **WHY:** At each position the decision branches: `?` forces a single-char match, `*` can consume 0 or more chars — mutual choices that require exploring both sub-cases. Memoisation collapses exponential branching to O(m·n).
> - **WHAT:** Recursive function `dp(i, j)` on indices into `s` and `p`, memoised.
> - **HOW:** Base cases: both exhausted → `True`; pattern exhausted → `False`; string exhausted → remaining pattern must be all `*`. Recursive: if `p[j] == '*'`, try skip-star (`dp(i, j+1)`) or consume-one (`dp(i+1, j)`). Else if `p[j] == '?'` or `p[j] == s[i]`, advance both.

> [!note]- Python Solution
> ```python
> from functools import lru_cache
> 
> def isMatch(s: str, p: str) -> bool:
>     @lru_cache(maxsize=None)
>     def dp(i: int, j: int) -> bool:
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
> Given string `s` and pattern `p` with `.` (any single char) and `*` (zero or more of preceding element), return `True` if `p` matches `s` entirely.

> [!info] Approach
> - **WHY:** `*` introduces a cross-recursion: either the preceding element matches and we try consuming one more char, or we skip the `x*` unit entirely — two recursive branches with shared subproblems.
> - **WHAT:** Memoised recursion `dp(i, j)` on string index `i` and pattern index `j`.
> - **HOW:** If `j+1 < len(p)` and `p[j+1] == '*'`: either skip the `x*` pair (`dp(i, j+2)`) or, if current chars match, consume one from `s` (`dp(i+1, j)`). Otherwise if chars match (`.` or exact), advance both.

> [!note]- Python Solution
> ```python
> from functools import lru_cache
> 
> def isMatch(s: str, p: str) -> bool:
>     @lru_cache(maxsize=None)
>     def dp(i: int, j: int) -> bool:
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
> Flatten a binary tree in-place into a linked list following preorder traversal, using `node.right` as the next pointer and `node.left = None`.

> [!info] Approach
> - **WHY:** Preorder visits root → left subtree → right subtree. If we recursively flatten both subtrees, we can stitch: root → flattened-left → flattened-right by connecting root.right to the left chain's tail, then moving the left chain to the right.
> - **WHAT:** Post-order style recursion — flatten left and right children first, then rewire.
> - **HOW:** Recursively flatten `root.left` and `root.right`. Find the rightmost node of the flattened left subtree. Attach `root.right` to it, move the left chain to `root.right`, set `root.left = None`.

> [!note]- Python Solution
> ```python
> def flatten(root) -> None:
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
> Given `preorder` and `inorder` traversal arrays of a binary tree with unique values, reconstruct and return the root.

> [!info] Approach
> - **WHY:** `preorder[0]` is always the root. Its index in `inorder` splits the array into left and right subtrees. Recursion mirrors the structural decomposition.
> - **WHAT:** Recurse with shrinking subarrays (or index bounds + hash map for O(1) lookup).
> - **HOW:** Root = `preorder[0]`. Find `mid = inorder.index(root.val)`. Left subtree uses `preorder[1:mid+1]` and `inorder[:mid]`. Right uses the remainder.

> [!note]- Python Solution
> ```python
> def buildTree(preorder: list[int], inorder: list[int]):
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
> Design `serialize(root)` → string and `deserialize(data)` → root such that the tree survives a round-trip.

> [!info] Approach
> - **WHY:** Preorder traversal with explicit null markers uniquely encodes any binary tree, enabling recursive reconstruction without an inorder array.
> - **WHAT:** Serialize via DFS preorder, emit `"#"` for nulls. Deserialize by consuming tokens from a queue.
> - **HOW:** Serialize: `root.val, serialize(left), serialize(right)` joined by a delimiter. Deserialize: pop from `deque`; if `"#"` return `None`; else create node and recurse for left then right.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> class Codec:
>     def serialize(self, root) -> str:
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
>     def deserialize(self, data: str):
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
> Count nodes in a complete binary tree in less than O(n) time.

> [!info] Approach
> - **WHY:** In a complete binary tree, the height of the leftmost path equals the height of the rightmost path iff the left subtree is a perfect binary tree. This lets us skip half the tree per recursion level.
> - **WHAT:** Compute left-height and right-height at each node. If equal, left subtree is perfect → count = `2^left_h - 1 + 1` (include root) + recurse right. Else recurse left.
> - **HOW:** `left_h = right_h` → left is full, so `(1 << left_h) + count(root.right)`. Otherwise `(1 << right_h) + count(root.left)`.

> [!note]- Python Solution
> ```python
> def countNodes(root) -> int:
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
> Return all unique permutations of a list that may contain duplicates.

> [!info] Approach
> - **WHY:** Duplicates at the same recursion level produce identical branches. Sorting + skipping duplicate elements at each level prunes these branches exactly.
> - **WHAT:** Backtracking with a `used` boolean array; sort first.
> - **HOW:** Sort `nums`. At each level, skip `nums[i]` if `nums[i] == nums[i-1]` and `not used[i-1]` (sibling was already explored — ensures we always use the left duplicate before the right at any level).

> [!note]- Python Solution
> ```python
> def permuteUnique(nums: list[int]) -> list[list[int]]:
>     nums.sort()
>     result, used = [], [False] * len(nums)
> 
>     def dfs(path: list[int]) -> None:
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
> Return all unique subsets of a list that may contain duplicates.

> [!info] Approach
> - **WHY:** Same duplicate-skip strategy as Permutations II but applied to the combination/subset template. At each index in a sorted array, skip if current equals previous and previous was not part of the current path extension.
> - **WHAT:** Sort + backtracking; record path at every node, skip duplicate siblings.
> - **HOW:** Sort `nums`. In the loop `for i in range(start, n)`: if `i > start and nums[i] == nums[i-1]`, skip. Append path snapshot, continue.

> [!note]- Python Solution
> ```python
> def subsetsWithDup(nums: list[int]) -> list[list[int]]:
>     nums.sort()
>     result = []
> 
>     def dfs(start: int, path: list[int]) -> None:
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
> Return all combinations of `k` numbers chosen from `1` to `n`.

> [!info] Approach
> - **WHY:** Classic choose-k-from-n combinatorial generation. At each level choose one number ≥ current start, recurse with start+1 until path length equals k.
> - **WHAT:** Backtracking with a start index and path length guard.
> - **HOW:** Prune early: if remaining elements `n - i + 1 < k - len(path)`, no valid completion possible — skip.

> [!note]- Python Solution
> ```python
> def combine(n: int, k: int) -> list[list[int]]:
>     result = []
> 
>     def dfs(start: int, path: list[int]) -> None:
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
> Find the contiguous subarray with the largest sum (Kadane's is O(n); this is the D&C version asked specifically in interviews for the divide-and-conquer pattern).

> [!info] Approach
> - **WHY:** Illustrates D&C: split at mid; max subarray is entirely in left half, entirely in right half, or crosses the midpoint. Crossing case is O(n) per level; depth is O(log n).
> - **WHAT:** Recurse on left and right halves; compute max crossing sum by linear scan outward from `mid`.
> - **HOW:** `max_cross` = max suffix of left + max prefix of right. Return `max(max_left, max_right, max_cross)`.

> [!note]- Python Solution
> ```python
> def maxSubArray(nums: list[int]) -> int:
>     def helper(l: int, r: int) -> int:
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
> - **WHY:** Naive O(n) multiplication is too slow for large `n`. Halving the exponent each call gives O(log n) multiplications.
> - **WHAT:** Recursive fast exponentiation (exponentiation by squaring).
> - **HOW:** If `n == 0` return 1. If `n < 0`, compute `1 / pow(x, -n)`. If `n` is even, `half = pow(x, n//2); return half * half`. If odd, `return x * pow(x, n-1)`.

> [!note]- Python Solution
> ```python
> def myPow(x: float, n: int) -> float:
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
> - **WHY:** During merge sort, when a right-half element is placed before left-half elements, all remaining left-half elements form inversions with it. Counting this during merge is O(n log n) total.
> - **WHAT:** Modified merge sort that accumulates an inversion count.
> - **HOW:** In the merge step, when `right[j] < left[i]`, add `len(left) - i` to the count (all remaining left elements are greater than `right[j]`).

> [!note]- Python Solution
> ```python
> def countInversions(nums: list[int]) -> int:
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
> Given a reference to a node in a connected undirected graph, return a deep copy of the graph.

> [!info] Approach
> - **WHY:** DFS naturally visits each node once; a hash map from original → clone prevents revisiting and handles cycles.
> - **WHAT:** DFS with a `visited` dict mapping original nodes to their clones.
> - **HOW:** If node already in `visited`, return its clone. Otherwise create a new node, record it in `visited`, then recursively clone each neighbor and append to the new node's neighbors list.

> [!note]- Python Solution
> ```python
> def cloneGraph(node):
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
> Given a 2D grid of `'1'` (land) and `'0'` (water), count the number of islands.

> [!info] Approach
> - **WHY:** DFS flood-fill: when a `'1'` is found, recursively sink the entire connected land mass (mark as `'0'`) so it is never counted again. Each DFS call corresponds to one island.
> - **WHAT:** Iterate over all cells; on encountering `'1'`, increment count and launch DFS to mark the island.
> - **HOW:** DFS marks `grid[r][c] = '0'` then recurses into all 4 directions if in-bounds and `== '1'`.

> [!note]- Python Solution
> ```python
> def numIslands(grid: list[list[str]]) -> int:
>     if not grid:
>         return 0
>     rows, cols = len(grid), len(grid[0])
>     count = 0
> 
>     def dfs(r: int, c: int) -> None:
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
> Evaluate a string expression containing non-negative integers, `+`, `-`, `*`, `/` (integer division toward zero), and spaces.

> [!info] Approach
> - **WHY:** Operator precedence makes this a parsing problem. A recursive descent parser separates addition/subtraction (low precedence) from multiplication/division (high precedence) using mutual recursion between grammar levels.
> - **WHAT:** Recursive descent: `expr → term (('+' | '-') term)*`, `term → factor (('*' | '/') factor)*`.
> - **HOW:** Use an index pointer (wrapped in a list for mutability) advanced through the string. `parse_expr` calls `parse_term` repeatedly; `parse_term` calls `parse_factor` (a number).

> [!note]- Python Solution
> ```python
> def calculate(s: str) -> int:
>     s = s.replace(' ', '')
>     idx = [0]
> 
>     def parse_number() -> int:
>         start = idx[0]
>         while idx[0] < len(s) and s[idx[0]].isdigit():
>             idx[0] += 1
>         return int(s[start:idx[0]])
> 
>     def parse_term() -> int:
>         val = parse_number()
>         while idx[0] < len(s) and s[idx[0]] in '*/':
>             op = s[idx[0]]; idx[0] += 1
>             right = parse_number()
>             val = val * right if op == '*' else int(val / right)
>         return val
> 
>     def parse_expr() -> int:
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
> Given equations like `["a/b", "b/c"]` with values `[2.0, 3.0]`, answer queries like `"a/c"`. Return `-1.0` for unknown variables or self-division of unknowns.

> [!info] Approach
> - **WHY:** Model as a weighted directed graph: edge `a → b` has weight `val`, edge `b → a` has weight `1/val`. A query `x/y` is a path product from `x` to `y` — DFS with running product.
> - **WHAT:** Build adjacency list, then DFS for each query.
> - **HOW:** DFS from `src` to `dst`, multiplying edge weights along the path, using a `visited` set to avoid cycles. Return accumulated product or `-1.0` if destination unreachable.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def calcEquation(equations, values, queries):
>     graph = defaultdict(dict)
>     for (a, b), val in zip(equations, values):
>         graph[a][b] = val
>         graph[b][a] = 1.0 / val
> 
>     def dfs(src: str, dst: str, visited: set) -> float:
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
> - **WHY:** The recurrence can be reduced by halving `n`, which turns linear recursion into logarithmic recursion depth.
> - **WHAT:** Use the fast-doubling identities: `F(2k) = F(k) * (2*F(k+1) - F(k))` and `F(2k+1) = F(k)^2 + F(k+1)^2`.
> - **HOW:** A helper returns `(F(n), F(n+1))`, allowing each recursive step to reuse the same subproblem results.

> [!note]- Python Solution
> ```python
> def fib(n: int) -> int:
>     def helper(k: int) -> tuple[int, int]:
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
> Two players take turns picking from either end of an array. Each picks optimally to maximize their own score. Return true if player 1 can win (score ≥ player 2's score).

> [!info] Approach
> - **WHY:** This is a minimax recursion. From any subarray `[i, j]`, the current player picks the end that maximises their net advantage (their score minus the opponent's future score). If the first player's net advantage from the full array is ≥ 0, they win.
> - **WHAT:** `dp(i, j)` = maximum score advantage the current player can achieve over the opponent from subarray `[i, j]`. Base: `dp(i, i) = nums[i]`. Recurrence: `max(nums[i] - dp(i+1, j), nums[j] - dp(i, j-1))`.
> - **HOW:** Memoize with `@lru_cache`. Return `dp(0, n-1) >= 0`.

> [!note]- Python Solution
> ```python
> from functools import lru_cache
>
> def predict_the_winner(nums: list[int]) -> bool:
>     n = len(nums)
>
>     @lru_cache(maxsize=None)
>     def dp(i: int, j: int) -> int:
>         if i == j:
>             return nums[i]
>         pick_left = nums[i] - dp(i + 1, j)
>         pick_right = nums[j] - dp(i, j - 1)
>         return max(pick_left, pick_right)
>
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
> Implement an iterator to flatten a nested list (each element is either an integer or a list of nested integers). Must support `hasNext()` and `next()`.

> [!info] Approach
> - **WHY:** Lazy flattening with a stack: push the full list onto the stack. When `hasNext()` is called, peel the top until an integer is at the top. `next()` then pops and returns it.
> - **WHAT:** Stack holds iterators (via index pointers or list iterators). When the top element is a list, push the new list's iterator. When it's an integer, it's ready to be returned.
> - **HOW:** Use a stack of `(nested_list, index)` pairs. `_advance()` is called by `hasNext()` to ensure the top is an integer.

> [!note]- Python Solution
> ```python
> class NestedIterator:
>     def __init__(self, nestedList):
>         self.stack = [(nestedList, 0)]
>
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
>
>     def next(self) -> int:
>         self._advance()
>         lst, idx = self.stack[-1]
>         self.stack[-1] = (lst, idx + 1)
>         return lst[idx].getInteger()
>
>     def hasNext(self) -> bool:
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
