---
tags: [coding, algorithms, backtracking]
topic: Backtracking
difficulty: mixed
---

# Backtracking — Amazon SDE-2

Backtracking is DFS over choices: pick something, go deeper, undo if it doesn't work. The easy bug is forgetting to undo — always pop/unmark after the recursive call.

**Prune when:** the partial answer is already invalid, not enough room left to finish, or you'd repeat the same choice at the same depth (sort + skip duplicates).

---

## Subsets / Combinations

### Subsets (Power Set)

> [!example] Problem
> Given an integer array nums of unique elements, return all possible subsets (the power set).
>
> ```
> Input: nums = [1,2,3]
> Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
> ```

> [!info] Approach
> Every element has a binary choice — include or exclude. The `start` parameter enforces non-decreasing index selection, eliminating permutation variants. Record the path at every node (not just leaves) — each partial path is itself a valid subset.

> [!note]- Python Solution
> ```python
> def subsets(nums):
>     result = []
>     path = []
>
>     def backtrack(start):
>         result.append(path[:])
>         for i in range(start, len(nums)):
>             path.append(nums[i])
>             backtrack(i + 1)
>             path.pop()
>
>     backtrack(0)
>     return result
> ```

> [!success] Complexity
> O(n · 2^n) time, O(n) recursion depth.

> [!tip] Alternatives
> Bitmask: for k in range(2^n), bits indicate inclusion. Iterative cascade: start with `[[]]`, extend by each new element.

---

### Subsets II (with duplicates)

> [!example] Problem
> Given an integer array nums that may contain duplicates, return all possible subsets without duplicate subsets.
>
> ```
> Input: nums = [1,2,2]
> Output: [[],[1],[1,2],[1,2,2],[2],[2,2]]
> ```

> [!info] Approach
> Sort to group duplicates; skip `nums[i]` if `i > start and nums[i] == nums[i-1]`. The `i > start` (not `i > 0`) condition is critical: it only skips duplicates at the current level, not when the first copy was used at a parent level.

> [!note]- Python Solution
> ```python
> def subsets_with_dup(nums):
>     nums.sort()
>     result = []
>     path = []
>
>     def backtrack(start):
>         result.append(path[:])
>         for i in range(start, len(nums)):
>             if i > start and nums[i] == nums[i - 1]:
>                 continue
>             path.append(nums[i])
>             backtrack(i + 1)
>             path.pop()
>
>     backtrack(0)
>     return result
> ```

> [!success] Complexity
> O(n · 2^n) worst case, O(n) space.

---

### Combination Sum (unbounded)

> [!example] Problem
> Given distinct integers candidates and a target, return all unique combinations that sum to target. The same number may be chosen unlimited times.
>
> ```
> Input: candidates = [2,3,6,7], target = 7
> Output: [[2,2,3],[7]]
> ```

> [!info] Approach
> Using `start = i` (not `i+1`) allows re-selecting the same element. Prune when `candidate > remaining`. Recurse with `backtrack(i, remaining - candidates[i])` — same `i`, not `i+1`.

> [!note]- Python Solution
> ```python
> def combination_sum(candidates, target):
>     result = []
>     path = []
>
>     def backtrack(start, remaining):
>         if remaining == 0:
>             result.append(path[:])
>             return
>         for i in range(start, len(candidates)):
>             if candidates[i] > remaining:
>                 continue
>             path.append(candidates[i])
>             backtrack(i, remaining - candidates[i])
>             path.pop()
>
>     backtrack(0, target)
>     return result
> ```

> [!success] Complexity
> O(n^(T/M)) where T = target, M = min candidate; O(T/M) recursion depth.

---

### Combination Sum II (0/1 — no reuse)

> [!example] Problem
> Each number may only be used once. Return unique combinations summing to target.
>
> ```
> Input: candidates = [10,1,2,7,6,1,5], target = 8
> Output: [[1,1,6],[1,2,5],[1,7],[2,6]]
> ```

> [!info] Approach
> No reuse → recurse with `i+1`. Duplicates need the same skip pattern as Subsets II: `i > start and candidates[i] == candidates[i-1]`. Sort enables both early termination (`break` when candidate > remaining) and deduplication.

> [!note]- Python Solution
> ```python
> def combination_sum2(candidates, target):
>     candidates.sort()
>     result = []
>     path = []
>
>     def backtrack(start, remaining):
>         if remaining == 0:
>             result.append(path[:])
>             return
>         for i in range(start, len(candidates)):
>             if candidates[i] > remaining:
>                 break
>             if i > start and candidates[i] == candidates[i - 1]:
>                 continue
>             path.append(candidates[i])
>             backtrack(i + 1, remaining - candidates[i])
>             path.pop()
>
>     backtrack(0, target)
>     return result
> ```

> [!success] Complexity
> O(2^n) worst case; O(n) space.

---

### Combinations

> [!example] Problem
> Given two integers n and k, return all possible combinations of k numbers from [1, n].
>
> ```
> Input: n = 4, k = 2
> Output: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
> ```

> [!info] Approach
> Fixed-size subset. Prune when remaining slots can't be filled: `n - i + 1 < k - len(path)`.

> [!note]- Python Solution
> ```python
> def combine(n, k):
>     result = []
>     path = []
>
>     def backtrack(start):
>         if len(path) == k:
>             result.append(path[:])
>             return
>         for i in range(start, n + 1):
>             if n - i + 1 < k - len(path):
>                 break
>             path.append(i)
>             backtrack(i + 1)
>             path.pop()
>
>     backtrack(1)
>     return result
> ```

> [!success] Complexity
> O(C(n,k) · k) time; O(k) recursion depth.

---

### Letter Combinations of a Phone Number

> [!example] Problem
> Given a digit string (2-9), return all possible letter combinations.
>
> ```
> Input: digits = "23"
> Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
> ```

> [!info] Approach
> Pure Cartesian product — at depth d, choose one letter for `digits[d]`. No pruning needed.

> [!note]- Python Solution
> ```python
> def letter_combinations(digits):
>     if not digits:
>         return []
>     phone = {
>         '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
>         '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
>     }
>     result = []
>     path = []
>
>     def backtrack(d):
>         if d == len(digits):
>             result.append("".join(path))
>             return
>         for ch in phone[digits[d]]:
>             path.append(ch)
>             backtrack(d + 1)
>             path.pop()
>
>     backtrack(0)
>     return result
> ```

> [!success] Complexity
> O(4^n · n) where n = len(digits); O(n) recursion depth.

---

## Permutations

### Permutations

> [!example] Problem
> Given an array of distinct integers, return all permutations.
>
> ```
> Input: nums = [1,2,3]
> Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
> ```

> [!info] Approach
> At each level, try all unused elements. A `used` boolean array gives O(1) per check. No pruning — every branch leads to a valid permutation.

> [!note]- Python Solution
> ```python
> def permute(nums):
>     result = []
>     path = []
>     used = [False] * len(nums)
>
>     def backtrack():
>         if len(path) == len(nums):
>             result.append(path[:])
>             return
>         for i, num in enumerate(nums):
>             if used[i]:
>                 continue
>             used[i] = True
>             path.append(num)
>             backtrack()
>             path.pop()
>             used[i] = False
>
>     backtrack()
>     return result
> ```

> [!success] Complexity
> O(n · n!) time, O(n) recursion depth.

---

### Permutations II (with duplicates)

> [!example] Problem
> Given nums that might contain duplicates, return all unique permutations.
>
> ```
> Input: nums = [1,1,2]
> Output: [[1,1,2],[1,2,1],[2,1,1]]
> ```

> [!info] Approach
> Sort + skip: `if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue`. This enforces canonical ordering — among duplicates, always use the leftmost first.

> [!note]- Python Solution
> ```python
> def permute_unique(nums):
>     nums.sort()
>     result = []
>     path = []
>     used = [False] * len(nums)
>
>     def backtrack():
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
>             backtrack()
>             path.pop()
>             used[i] = False
>
>     backtrack()
>     return result
> ```

> [!success] Complexity
> O(n · n!) worst case; O(n) space.

---

## String Backtracking

### Generate Parentheses

> [!example] Problem
> Given n pairs of parentheses, generate all combinations of well-formed parentheses.
>
> ```
> Input: n = 3
> Output: ["((()))","(()())","(())()","()(())","()()()"]
> ```

> [!info] Approach
> Add `(` only if `open < n`; add `)` only if `close < open`. Constraint-driven pruning eliminates all invalid paths before they're fully built.

> [!note]- Python Solution
> ```python
> def generate_parenthesis(n):
>     result = []
>
>     def backtrack(path, open_cnt, close_cnt):
>         if len(path) == 2 * n:
>             result.append(path)
>             return
>         if open_cnt < n:
>             backtrack(path + '(', open_cnt + 1, close_cnt)
>         if close_cnt < open_cnt:
>             backtrack(path + ')', open_cnt, close_cnt + 1)
>
>     backtrack('', 0, 0)
>     return result
> ```

> [!success] Complexity
> O(4^n / sqrt(n)) — Catalan number; O(n) recursion depth.

---

### Palindrome Partitioning

> [!example] Problem
> Partition s such that every substring is a palindrome. Return all such partitions.
>
> ```
> Input: s = "aab"
> Output: [["a","a","b"],["aa","b"]]
> ```

> [!info] Approach
> Precompute `is_pal[i][j]` via DP in O(n²) to avoid O(n) palindrome checks during backtracking. At each start, try substrings that are palindromes and recurse on the rest.

> [!note]- Python Solution
> ```python
> def partition(s):
>     n = len(s)
>     is_pal = [[False] * n for _ in range(n)]
>     for i in range(n - 1, -1, -1):
>         for j in range(i, n):
>             if s[i] == s[j] and (j - i <= 2 or is_pal[i + 1][j - 1]):
>                 is_pal[i][j] = True
>
>     result = []
>     path = []
>
>     def backtrack(start):
>         if start == n:
>             result.append(path[:])
>             return
>         for end in range(start, n):
>             if is_pal[start][end]:
>                 path.append(s[start:end + 1])
>                 backtrack(end + 1)
>                 path.pop()
>
>     backtrack(0)
>     return result
> ```

> [!success] Complexity
> O(n · 2^n) time; O(n²) space for palindrome table.

---

### Word Search

> [!example] Problem
> Given a board and a word, return true if the word exists in the grid using adjacent cells (no reuse).
>
> ```
> Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
> Output: true
> ```

> [!info] Approach
> DFS from each cell matching `word[0]`. Mark cell visited with `'#'` in-place, recurse on 4 neighbors for next character, then restore. Pruning: mismatch at any character immediately abandons that branch.

> [!note]- Python Solution
> ```python
> def exist(board, word):
>     m, n = len(board), len(board[0])
>     directions = ((0, 1), (0, -1), (1, 0), (-1, 0))
>
>     def dfs(r, c, i):
>         if i == len(word):
>             return True
>         if not (0 <= r < m and 0 <= c < n):
>             return False
>         if board[r][c] != word[i]:
>             return False
>         tmp = board[r][c]
>         board[r][c] = '#'
>         found = any(dfs(r + dr, c + dc, i + 1) for dr, dc in directions)
>         board[r][c] = tmp
>         return found
>
>     for r in range(m):
>         for c in range(n):
>             if dfs(r, c, 0):
>                 return True
>     return False
> ```

> [!success] Complexity
> O(m · n · 4^L) where L = len(word); O(L) recursion depth.

---

## Board / Matrix Backtracking

### N-Queens

> [!example] Problem
> Place n queens on an n×n board so no two attack each other. Return all solutions.
>
> ```
> Input: n = 4
> Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
> ```

> [!info] Approach
> One queen per row. O(1) conflict check via three sets: `cols`, `diags` (row-col), `anti_diags` (row+col). Backtrack row by row; skip if any constraint set contains the column/diagonal.

> [!note]- Python Solution
> ```python
> def solve_n_queens(n):
>     result = []
>     cols = set()
>     diags = set()
>     anti_diags = set()
>     board = [['.' ] * n for _ in range(n)]
>
>     def backtrack(row):
>         if row == n:
>             result.append([''.join(r) for r in board])
>             return
>         for col in range(n):
>             d, ad = row - col, row + col
>             if col in cols or d in diags or ad in anti_diags:
>                 continue
>             cols.add(col); diags.add(d); anti_diags.add(ad)
>             board[row][col] = 'Q'
>             backtrack(row + 1)
>             board[row][col] = '.'
>             cols.remove(col); diags.remove(d); anti_diags.remove(ad)
>
>     backtrack(0)
>     return result
> ```

> [!success] Complexity
> O(n!) upper bound; O(n²) board space.

---

### Sudoku Solver (awareness)

> Constraint satisfaction — each empty cell has a small set of valid digits. Backtrack on the first empty cell, try all valid digits in O(1) using pre-populated boolean arrays for rows/cols/boxes. Practically near-constant for valid puzzles.
>
> Key insight: `box_id = (r//3)*3 + c//3`. Precompute `rows[r][d]`, `cols[c][d]`, `boxes[b][d]` before backtracking. Try digits 1-9; recurse; undo if stuck.

---

## Additional Core Problems

### Word Break II

> [!example] Problem
> Given string s and wordDict, return all sentences that segment s into dictionary words.
>
> ```
> Input: s = "catsanddog", wordDict = ["cat","cats","and","sand","dog"]
> Output: ["cats and dog","cat sand dog"]
> ```

> [!info] Approach
> Try every possible first word; recurse on suffix. Memoize by `start` index — cache the list of sentences producible from each suffix. Without memoization: O(2^n). With: each suffix solved once.

> [!note]- Python Solution
> ```python
> def word_break(s, wordDict):
>     word_set = set(wordDict)
>     memo = {}
>
>     def backtrack(start):
>         if start in memo:
>             return memo[start]
>         if start == len(s):
>             return ['']
>         sentences = []
>         for end in range(start + 1, len(s) + 1):
>             word = s[start:end]
>             if word in word_set:
>                 for rest in backtrack(end):
>                     sentences.append(word + (' ' + rest if rest else ''))
>         memo[start] = sentences
>         return sentences
>
>     return backtrack(0)
> ```

> [!success] Complexity
> O(n²) time ignoring output; space O(n · output_size).

---

### Target Sum

> [!example] Problem
> Assign + or - to each element in nums. Count expressions that evaluate to target.
>
> ```
> Input: nums = [1,1,1,1,1], target = 3
> Output: 5
> ```

> [!info] Approach
> Binary choice per element → 2^n branches. Backtracking with pruning (suffix-sum bounds). Better: DP subset-sum reduction — let P = sum of positives. P - N = target, P + N = total → P = (target + total) / 2. Count subsets summing to P in O(n · S).

> [!note]- Python Solution
> ```python
> def find_target_sum_ways(nums, target):
>     count = 0
>     n = len(nums)
>     suffix_sum = [0] * (n + 1)
>     for i in range(n - 1, -1, -1):
>         suffix_sum[i] = suffix_sum[i + 1] + nums[i]
>
>     def backtrack(i, current):
>         nonlocal count
>         if i == n:
>             if current == target:
>                 count += 1
>             return
>         if current + suffix_sum[i] < target:
>             return
>         if current - suffix_sum[i] > target:
>             return
>         backtrack(i + 1, current + nums[i])
>         backtrack(i + 1, current - nums[i])
>
>     backtrack(0, 0)
>     return count
> ```

> [!success] Complexity
> O(2^n) backtracking with pruning; O(n · S) DP alternative.

---

### Restore IP Addresses

> [!example] Problem
> Given a digit string, return all valid IP addresses that can be formed by inserting dots.
>
> ```
> Input: s = "25525511135"
> Output: ["255.255.11.135","255.255.111.35"]
> ```

> [!info] Approach
> Exactly 4 segments, each 1-3 digits. Pruning: (1) value > 255; (2) leading zeros; (3) feasibility — `remaining_chars` must be in `[remaining_segs, 3*remaining_segs]`.

> [!note]- Python Solution
> ```python
> def restore_ip_addresses(s):
>     result = []
>     path = []
>
>     def backtrack(start):
>         if len(path) == 4:
>             if start == len(s):
>                 result.append('.'.join(path))
>             return
>         segs_left = 4 - len(path)
>         chars_left = len(s) - start
>         if chars_left < segs_left or chars_left > 3 * segs_left:
>             return
>         for length in range(1, 4):
>             if start + length > len(s):
>                 break
>             segment = s[start:start + length]
>             if len(segment) > 1 and segment[0] == '0':
>                 break
>             if int(segment) > 255:
>                 break
>             path.append(segment)
>             backtrack(start + length)
>             path.pop()
>
>     backtrack(0)
>     return result
> ```

> [!success] Complexity
> O(1) — at most 3^4 = 81 combinations; path depth fixed at 4.

---

## See Also

[[dynamic-programming]] | [[graph-algorithms]] | [[greedy]]
