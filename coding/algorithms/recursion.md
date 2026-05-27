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

## See Also

[[dynamic-programming]] | [[backtracking]] | [[tree]] | [[divide-and-conquer]]
