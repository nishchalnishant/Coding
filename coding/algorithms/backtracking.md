---
tags: [coding, algorithms, backtracking]
topic: Backtracking
difficulty: mixed
---

# Backtracking — Problem Compendium

Backtracking = DFS on a decision tree where each node is a partial solution and each branch is a choice. Correctness comes from exhaustive exploration; efficiency from pruning branches that cannot lead to valid solutions. The `choose → explore → unchoose` invariant must be airtight — any missing undo corrupts state across branches.

Key pruning sources: (1) constraint violation (invalid partial state), (2) structural bounds (remaining slots can't fit remaining elements), (3) deduplication (skip duplicate choices at the same decision level after sorting).

---

## Subsets / Combinations

### Subsets (Power Set)

> [!example] Problem
> Given distinct integers, return all subsets (the power set).

> [!info] Approach
> - **WHY:** Every element has a binary choice — include or exclude. Tree depth = n, branching factor = 2, total leaves = 2^n. No pruning needed — every branch is valid. The `start` parameter enforces non-decreasing index selection, eliminating permutation variants of the same subset.
> - **WHAT:** At each recursive call, record the current path. Try adding each element from `start` onward; recurse with `start = i+1`; undo.
> - **HOW:** Record subset at every node (not just leaves) — each partial path is itself a valid subset.

> [!note]- Python Solution
> ```python
> def subsets(nums: list[int]) -> list[list[int]]:
>     res: list[list[int]] = []
>     path: list[int] = []
> 
>     def bt(start: int) -> None:
>         res.append(path[:])  # record at every node
>         for i in range(start, len(nums)):
>             path.append(nums[i])
>             bt(i + 1)
>             path.pop()
> 
>     bt(0)
>     return res
> ```

> [!success] Complexity
> O(n · 2^n) time (copy at each of 2^n nodes), O(n) recursion depth.

> [!tip] Alternatives
> Bitmask: for k in range(2^n), bits indicate inclusion — O(n · 2^n), no recursion. Iterative cascade: start with `[[]]`, extend by each new element — O(n · 2^n), simple.

---

### Subsets II (with duplicates)

> [!example] Problem
> Input may contain duplicates; return only unique subsets.

> [!info] Approach
> - **WHY:** Duplicates produce identical subsets when same-valued elements are included at the same decision level. Sort to group duplicates together; skip `nums[i]` if `i > start and nums[i] == nums[i-1]`. The `i > start` (not `i > 0`) condition is critical: it only skips duplicates at the current level, not when the first copy was used at a parent level.
> - **WHAT:** Sort array; apply deduplication skip in backtracking loop.
> - **HOW:** Same structure as Subsets but with `if i > start and nums[i] == nums[i-1]: continue`.

> [!note]- Python Solution
> ```python
> def subsetsWithDup(nums: list[int]) -> list[list[int]]:
>     nums.sort()
>     res: list[list[int]] = []
>     path: list[int] = []
> 
>     def bt(start: int) -> None:
>         res.append(path[:])
>         for i in range(start, len(nums)):
>             if i > start and nums[i] == nums[i - 1]:
>                 continue  # skip duplicate at same level
>             path.append(nums[i])
>             bt(i + 1)
>             path.pop()
> 
>     bt(0)
>     return res
> ```

> [!success] Complexity
> O(n · 2^n) worst case (all distinct), O(n) space.

> [!tip] Alternatives
> Set deduplication post-hoc — generates duplicates then discards; wasteful. Counter-based: iterate over how many copies of each unique value to include.

---

### Combination Sum (unbounded)

> [!example] Problem
> Given distinct candidates and a target, return all unique combinations (with repetition) summing to target.

> [!info] Approach
> - **WHY:** Elements can be reused, but combinations (not permutations) are needed. Using `start = i` (not `i+1`) in the recursive call allows re-selecting the same element. The `start` parameter enforces non-decreasing order, so `[2,3]` and `[3,2]` are treated as the same combination.
> - **WHAT:** At each step, try candidates from `start` onward. Prune when `candidate > remaining`. Record when `remaining == 0`.
> - **HOW:** Recurse with `bt(i, remaining - candidates[i])` — same `i`, not `i+1`.

> [!note]- Python Solution
> ```python
> def combinationSum(candidates: list[int], target: int) -> list[list[int]]:
>     res: list[list[int]] = []
>     path: list[int] = []
> 
>     def bt(start: int, remaining: int) -> None:
>         if remaining == 0:
>             res.append(path[:])
>             return
>         for i in range(start, len(candidates)):
>             if candidates[i] > remaining:
>                 continue
>             path.append(candidates[i])
>             bt(i, remaining - candidates[i])  # i, not i+1: allow reuse
>             path.pop()
> 
>     bt(0, target)
>     return res
> ```

> [!success] Complexity
> O(n^(T/M)) where T = target, M = min candidate; O(T/M) recursion depth.

> [!tip] Alternatives
> Sort candidates + replace `continue` with `break` (early exit). DP for count only: O(n · target). BFS: memory-intensive.

---

### Combination Sum II (0/1 — no reuse)

> [!example] Problem
> Candidates may contain duplicates; each used at most once. Return unique combinations summing to target.

> [!info] Approach
> - **WHY:** No reuse → recurse with `i+1`. Duplicates need the same skip pattern as Subsets II: `i > start and candidates[i] == candidates[i-1]`. Sort enables both early termination (break when candidate > remaining) and deduplication.
> - **WHAT:** Sort; backtrack with `i+1`; skip duplicates at same level; break early.
> - **HOW:** `if i > start and candidates[i] == candidates[i-1]: continue`.

> [!note]- Python Solution
> ```python
> def combinationSum2(candidates: list[int], target: int) -> list[list[int]]:
>     candidates.sort()
>     res: list[list[int]] = []
>     path: list[int] = []
> 
>     def bt(start: int, remaining: int) -> None:
>         if remaining == 0:
>             res.append(path[:])
>             return
>         for i in range(start, len(candidates)):
>             if candidates[i] > remaining:
>                 break  # sorted: no later candidate can work
>             if i > start and candidates[i] == candidates[i - 1]:
>                 continue
>             path.append(candidates[i])
>             bt(i + 1, remaining - candidates[i])
>             path.pop()
> 
>     bt(0, target)
>     return res
> ```

> [!success] Complexity
> O(2^n) worst case; O(n) space.

> [!tip] Alternatives
> Counter-based deduplication: group by unique value, try 0..count copies. Avoids sort-based skip logic.

---

### Combinations

> [!example] Problem
> Return all combinations of k numbers from the range [1, n].

> [!info] Approach
> - **WHY:** Fixed-size subset problem. At each level, choose one number from `start` to `n`; recurse with `start+1`. Prune when remaining slots can't be filled: `n - i + 1 < k - len(path)`.
> - **WHAT:** Standard subset backtracking with fixed depth k and pruning on remaining elements.
> - **HOW:** Pruning: `if n - i + 1 < k - len(path): break` — not enough numbers remain.

> [!note]- Python Solution
> ```python
> def combine(n: int, k: int) -> list[list[int]]:
>     res: list[list[int]] = []
>     path: list[int] = []
> 
>     def bt(start: int) -> None:
>         if len(path) == k:
>             res.append(path[:])
>             return
>         for i in range(start, n + 1):
>             if n - i + 1 < k - len(path):
>                 break  # not enough numbers left
>             path.append(i)
>             bt(i + 1)
>             path.pop()
> 
>     bt(1)
>     return res
> ```

> [!success] Complexity
> O(C(n,k) · k) time; O(k) recursion depth.

> [!tip] Alternatives
> Bitmask over n bits: try all subsets of size k — O(2^n), impractical for large n. Itertools.combinations in production code.

---

### Letter Combinations of a Phone Number

> [!example] Problem
> Given a string of digits (2-9), return all possible letter combinations a phone keypad would produce.

> [!info] Approach
> - **WHY:** Each digit maps to 3-4 letters — pure Cartesian product. Backtracking is the natural enumeration: at depth d, choose one letter for digit[d]; total combinations = product of group sizes.
> - **WHAT:** At each depth d, iterate over letters for `digits[d]`; append, recurse, pop.
> - **HOW:** Base case: `d == len(digits)` → record. No pruning needed — every path is valid.

> [!note]- Python Solution
> ```python
> def letterCombinations(digits: str) -> list[str]:
>     if not digits:
>         return []
>     phone = {
>         '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
>         '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
>     }
>     res: list[str] = []
>     path: list[str] = []
> 
>     def bt(d: int) -> None:
>         if d == len(digits):
>             res.append("".join(path))
>             return
>         for ch in phone[digits[d]]:
>             path.append(ch)
>             bt(d + 1)
>             path.pop()
> 
>     bt(0)
>     return res
> ```

> [!success] Complexity
> O(4^n · n) where n = len(digits); O(n) recursion depth.

> [!tip] Alternatives
> Iterative BFS: queue of partial strings, extend by one character per level — O(4^n · n). Equivalent, more memory.

---

## Permutations

### Permutations

> [!example] Problem
> Given distinct integers, return all permutations.

> [!info] Approach
> - **WHY:** Each permutation chooses from all remaining unused elements at each depth. Tree: depth n, branching factor decreasing from n to 1, total leaves = n!. A `used` boolean array gives O(1) per check without removing elements from the array.
> - **WHAT:** At each level, try all unused elements; mark used → recurse → mark unused.
> - **HOW:** Base case: `len(path) == n`. No pruning — every branch leads to a valid permutation.

> [!note]- Python Solution
> ```python
> def permute(nums: list[int]) -> list[list[int]]:
>     res: list[list[int]] = []
>     path: list[int] = []
>     used = [False] * len(nums)
> 
>     def bt() -> None:
>         if len(path) == len(nums):
>             res.append(path[:])
>             return
>         for i, num in enumerate(nums):
>             if used[i]:
>                 continue
>             used[i] = True
>             path.append(num)
>             bt()
>             path.pop()
>             used[i] = False
> 
>     bt()
>     return res
> ```

> [!success] Complexity
> O(n · n!) time, O(n) recursion depth.

> [!tip] Alternatives
> Swap-based in-place: swap `nums[start]` with `nums[i]`, recurse on `start+1`, swap back — O(n!) space-efficient. Itertools.permutations.

---

### Permutations II (with duplicates)

> [!example] Problem
> Input may contain duplicates; return only unique permutations.

> [!info] Approach
> - **WHY:** Duplicate values can appear at the same position in the permutation tree, generating identical permutations. Sort the array; skip element i if `nums[i] == nums[i-1]` and `used[i-1] == False` — this enforces canonical ordering: among duplicates, always use the leftmost first (so its predecessor is always used before it).
> - **WHAT:** Same structure as Permutations; sort + the `not used[i-1]` deduplication condition.
> - **HOW:** `if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue`.

> [!note]- Python Solution
> ```python
> def permuteUnique(nums: list[int]) -> list[list[int]]:
>     nums.sort()
>     res: list[list[int]] = []
>     path: list[int] = []
>     used = [False] * len(nums)
> 
>     def bt() -> None:
>         if len(path) == len(nums):
>             res.append(path[:])
>             return
>         for i in range(len(nums)):
>             if used[i]:
>                 continue
>             if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
>                 continue  # canonical ordering: use first copy before second
>             used[i] = True
>             path.append(nums[i])
>             bt()
>             path.pop()
>             used[i] = False
> 
>     bt()
>     return res
> ```

> [!success] Complexity
> O(n · n!) worst case (all distinct), fewer with duplicates; O(n) space.

> [!tip] Alternatives
> Set deduplication: add results to set — generates duplicates then discards, wasteful. Counter-based: track remaining count per value, try each value up to its remaining count.

---

### Next Permutation (iterative approach)

> [!example] Problem
> Find the next lexicographically greater permutation in-place. If none exists (descending order), rotate to the smallest (ascending).

> [!info] Approach
> - **WHY:** Not backtracking per se, but generates the next item in the permutation enumeration order. Algorithm: find the rightmost "ascent" — the pivot where the sequence stops being descending from right. Swap pivot with the smallest element to its right that is larger, then reverse the suffix.
> - **WHAT:** (1) Find pivot: rightmost i where nums[i] < nums[i+1]. (2) Find rightmost j > i where nums[j] > nums[i]. (3) Swap i and j. (4) Reverse suffix from i+1.
> - **HOW:** If no pivot found (fully descending), entire array is reversed.

> [!note]- Python Solution
> ```python
> def nextPermutation(nums: list[int]) -> None:
>     n = len(nums)
>     # Step 1: Find pivot (rightmost ascent)
>     i = n - 2
>     while i >= 0 and nums[i] >= nums[i + 1]:
>         i -= 1
>     if i >= 0:
>         # Step 2: Find rightmost element larger than pivot
>         j = n - 1
>         while nums[j] <= nums[i]:
>             j -= 1
>         nums[i], nums[j] = nums[j], nums[i]
>     # Step 3: Reverse suffix (whether or not pivot found)
>     nums[i + 1:] = nums[i + 1:][::-1]
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> No practical alternatives for in-place O(n) O(1). Generating all permutations then finding next is O(n! · n) — infeasible.

---

### Letter Case Permutation

> [!example] Problem
> Given a string with digits and letters, return all possible strings by changing letter case (upper/lower).

> [!info] Approach
> - **WHY:** Each letter has two choices (upper/lower); digits have one choice. Binary tree of depth = number of letters. Total leaves = 2^(# letters). No pruning needed.
> - **WHAT:** At each index, if digit: recurse on next index directly. If letter: try lowercase and uppercase, recurse each.
> - **HOW:** String building via list (mutable); convert at leaf.

> [!note]- Python Solution
> ```python
> def letterCasePermutation(s: str) -> list[str]:
>     res: list[str] = []
>     path = list(s)
> 
>     def bt(i: int) -> None:
>         if i == len(path):
>             res.append("".join(path))
>             return
>         bt(i + 1)  # keep as-is (or digit)
>         if path[i].isalpha():
>             path[i] = path[i].swapcase()
>             bt(i + 1)
>             path[i] = path[i].swapcase()  # restore
> 
>     bt(0)
>     return res
> ```

> [!success] Complexity
> O(2^L · n) where L = # letters, n = len(s); O(n) recursion depth.

> [!tip] Alternatives
> BFS: queue of partial strings — O(2^L · n), more memory. Bitmask: iterate over 2^L masks, assign upper/lower based on bits.

---

## String Backtracking

### Generate Parentheses

> [!example] Problem
> Generate all combinations of n pairs of well-formed parentheses.

> [!info] Approach
> - **WHY:** At each position, two choices: `(` or `)`. Constraint-driven pruning eliminates all invalid paths: add `(` only if `open < n`; add `)` only if `close < open`. This prunes invalid sequences before they're fully built — no validity check needed at the leaf.
> - **WHAT:** Track `open_cnt` and `close_cnt`. Branch into `(` or `)` based on constraints.
> - **HOW:** Leaf count = Catalan number C(n). The invariant `close < open` ensures every partial string is a valid prefix.

> [!note]- Python Solution
> ```python
> def generateParenthesis(n: int) -> list[str]:
>     res: list[str] = []
> 
>     def bt(path: str, open_cnt: int, close_cnt: int) -> None:
>         if len(path) == 2 * n:
>             res.append(path)
>             return
>         if open_cnt < n:
>             bt(path + '(', open_cnt + 1, close_cnt)
>         if close_cnt < open_cnt:
>             bt(path + ')', open_cnt, close_cnt + 1)
> 
>     bt('', 0, 0)
>     return res
> ```

> [!success] Complexity
> O(4^n / sqrt(n)) — Catalan number C(n); O(n) recursion depth.

> [!tip] Alternatives
> DP: `dp[i]` = all valid strings of i pairs, built from sub-problems — same time complexity. Closure number decomposition: `'(' + dp[c] + ')' + dp[n-1-c]` for c in 0..n-1.

---

### Palindrome Partitioning

> [!example] Problem
> Partition string s such that every substring is a palindrome. Return all valid partitioning schemes.

> [!info] Approach
> - **WHY:** At each position, try all possible next partition points. Pruning: skip substrings that aren't palindromes. Precomputing palindrome-ness for all substrings (O(n²)) avoids O(n) palindrome checks during backtracking.
> - **WHAT:** At each start, try substrings `s[start..end]` for end from start to n-1. If it's a palindrome, add and recurse on rest.
> - **HOW:** Precompute `is_pal[i][j]` via DP in O(n²). Then backtracking is O(2^n) calls × O(1) palindrome check.

> [!note]- Python Solution
> ```python
> def partition(s: str) -> list[list[str]]:
>     n = len(s)
>     # Precompute palindrome table
>     is_pal = [[False] * n for _ in range(n)]
>     for i in range(n - 1, -1, -1):
>         for j in range(i, n):
>             if s[i] == s[j] and (j - i <= 2 or is_pal[i + 1][j - 1]):
>                 is_pal[i][j] = True
> 
>     res: list[list[str]] = []
>     path: list[str] = []
> 
>     def bt(start: int) -> None:
>         if start == n:
>             res.append(path[:])
>             return
>         for end in range(start, n):
>             if is_pal[start][end]:
>                 path.append(s[start:end + 1])
>                 bt(end + 1)
>                 path.pop()
> 
>     bt(0)
>     return res
> ```

> [!success] Complexity
> O(n · 2^n) time (2^n partitions, each O(n) to copy); O(n²) space for palindrome table.

> [!tip] Alternatives
> Without precomputation: O(n) palindrome check per substring — O(n² · 2^n) total. Manacher's algorithm for O(n) palindrome precomputation.

---

### Remove Invalid Parentheses

> [!example] Problem
> Remove the minimum number of invalid parentheses to make the input valid. Return all unique results.

> [!info] Approach
> - **WHY:** First compute minimum removals (one scan: track unmatched `(` as `open_rem`, unmatched `)` as `close_rem`). Then backtrack: at each character, keep or remove it. Pruning: (1) removal budget exhausted; (2) `close_cnt > open_cnt` in current path (invalid prefix); (3) consecutive same brackets — only remove the first of a run (deduplication without a set).
> - **WHAT:** Backtrack with state `(index, path, open_cnt, close_cnt, open_rem, close_rem)`.
> - **HOW:** Compute open_rem, close_rem first; backtrack with those exact budgets.

> [!note]- Python Solution
> ```python
> def removeInvalidParentheses(s: str) -> list[str]:
>     open_rem = close_rem = 0
>     for c in s:
>         if c == '(':
>             open_rem += 1
>         elif c == ')':
>             if open_rem > 0:
>                 open_rem -= 1
>             else:
>                 close_rem += 1
> 
>     res: set[str] = set()
> 
>     def bt(i: int, path: str, open_cnt: int, close_cnt: int,
>            open_r: int, close_r: int) -> None:
>         if i == len(s):
>             if open_r == 0 and close_r == 0:
>                 res.add(path)
>             return
>         c = s[i]
>         # Option 1: Remove current bracket (if budget allows and it's a bracket)
>         if c == '(' and open_r > 0:
>             bt(i + 1, path, open_cnt, close_cnt, open_r - 1, close_r)
>         if c == ')' and close_r > 0:
>             bt(i + 1, path, open_cnt, close_cnt, open_r, close_r - 1)
>         # Option 2: Keep current character
>         if c == '(':
>             bt(i + 1, path + c, open_cnt + 1, close_cnt, open_r, close_r)
>         elif c == ')':
>             if close_cnt < open_cnt:  # valid to add: won't go negative
>                 bt(i + 1, path + c, open_cnt, close_cnt + 1, open_r, close_r)
>         else:
>             bt(i + 1, path + c, open_cnt, close_cnt, open_r, close_r)
> 
>     bt(0, '', 0, 0, open_rem, close_rem)
>     return list(res)
> ```

> [!success] Complexity
> O(2^n) worst case; O(n) recursion depth.

> [!tip] Alternatives
> BFS level-by-level removing one bracket per level — O(n · 2^n), simpler correctness argument (BFS guarantees minimum removals), but higher memory. DFS with explicit consecutive-duplicate pruning can eliminate the set.

---

### Word Search

> [!example] Problem
> Given a 2D board and a word, determine if the word exists as a path of adjacent non-revisiting cells.

> [!info] Approach
> - **WHY:** Need to find a specific path through a grid — DFS with backtracking is the natural approach. Pruning: mismatch at any character immediately abandons that branch. Temporary in-place marking avoids extra visited array.
> - **WHAT:** DFS from each cell matching `word[0]`. At each step, mark cell visited (`'#'`), recurse on 4 neighbors for next character, then restore.
> - **HOW:** Early return True on complete match. Board is restored on each backtrack.

> [!note]- Python Solution
> ```python
> def exist(board: list[list[str]], word: str) -> bool:
>     m, n = len(board), len(board[0])
> 
>     def dfs(r: int, c: int, i: int) -> bool:
>         if i == len(word):
>             return True
>         if not (0 <= r < m and 0 <= c < n) or board[r][c] != word[i]:
>             return False
>         tmp, board[r][c] = board[r][c], '#'  # mark visited
>         found = any(
>             dfs(r + dr, c + dc, i + 1)
>             for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0))
>         )
>         board[r][c] = tmp  # restore
>         return found
> 
>     return any(dfs(r, c, 0) for r in range(m) for c in range(n))
> ```

> [!success] Complexity
> O(m · n · 4^L) where L = len(word); O(L) recursion depth.

> [!tip] Alternatives
> BFS per starting cell: exponential memory — infeasible. Pruning with character frequency check before DFS: O(mn) precheck can prune early.

---

### Expression Add Operators (LC 282)

> [!example] Problem
> Given a string `num` of digits and a target integer, add operators `+`, `-`, `*` between digits to form expressions that evaluate to `target`. Return all valid expressions. Leading zeros in multi-digit operands are not allowed (except `"0"` itself).

> [!info] Approach
> - **WHY:** Brute force tries all 3^(n-1) operator placements. Backtracking prunes early (e.g. skip leading-zero operands immediately). The key challenge: `*` has higher precedence — multiplying undoes the previous addition/subtraction, so we track `prev_operand` to "undo" it.
> - **WHAT:** Backtracking with state `(index, current_expression, current_value, prev_operand)`.
> - **HOW:**
>   - At each position, try all possible next numbers (no leading zeros except `"0"` itself).
>   - For each number as next operand:
>     - First operand: recurse with `value = num_val`, `prev = num_val`.
>     - `+`: `new_val = value + num_val`, `new_prev = +num_val`.
>     - `-`: `new_val = value - num_val`, `new_prev = -num_val`.
>     - `*`: `new_val = value - prev + prev * num_val`, `new_prev = prev * num_val`. *(Undo prev add/sub, redo as product.)*
>   - Base: if `index == len(num)` and `value == target`: add expression to result.

> [!note]- Python Solution
> ```python
> def addOperators(num: str, target: int) -> list[str]:
>     res: list[str] = []
>     n = len(num)
> 
>     def bt(index: int, expr: str, value: int, prev: int) -> None:
>         if index == n:
>             if value == target:
>                 res.append(expr)
>             return
>         for end in range(index + 1, n + 1):
>             token = num[index:end]
>             # No leading zeros for multi-digit operands
>             if len(token) > 1 and token[0] == '0':
>                 break
>             num_val = int(token)
>             if index == 0:
>                 # First operand: no operator prefix
>                 bt(end, token, num_val, num_val)
>             else:
>                 # Try +
>                 bt(end, expr + '+' + token, value + num_val, num_val)
>                 # Try -
>                 bt(end, expr + '-' + token, value - num_val, -num_val)
>                 # Try *: undo previous op, apply multiplication
>                 bt(end, expr + '*' + token, value - prev + prev * num_val, prev * num_val)
> 
>     bt(0, '', 0, 0)
>     return res
> ```

> [!success] Complexity
> O(4^n × n) — at each of n digit positions, up to 4 choices (3 operators + extend operand); O(n) for string slicing/building at each node. Space O(n) recursion depth.

> [!tip] Alternatives
> - Build expression string then evaluate: simpler code (avoid tracking `prev`), but evaluation is O(n) per leaf — same overall complexity, harder to prove correctness for `*` precedence.
> - Pure brute force without backtracking: generate all 3^(n-1) operator strings, evaluate each — no early pruning on leading zeros, same worst-case O(4^n × n).

---

## Board / Matrix Backtracking

### N-Queens

> [!example] Problem
> Place n queens on an n×n board so no two queens attack each other. Return all valid configurations.

> [!info] Approach
> - **WHY:** One queen per row (DFS depth = row). At each row, try all columns; conflict check in O(1) using three constraint sets: `cols`, `diags` (row-col=const), `anti_diags` (row+col=const). Pruning eliminates all attacking positions immediately.
> - **WHAT:** Backtrack row by row. At each row, iterate columns; skip if any constraint set contains the column/diagonal.
> - **HOW:** Add to sets before recursing; remove after. Leaf (row==n) records the board.

> [!note]- Python Solution
> ```python
> def solveNQueens(n: int) -> list[list[str]]:
>     res: list[list[str]] = []
>     cols: set[int] = set()
>     diags: set[int] = set()
>     anti_diags: set[int] = set()
>     board = [['.' ] * n for _ in range(n)]
> 
>     def bt(row: int) -> None:
>         if row == n:
>             res.append([''.join(r) for r in board])
>             return
>         for col in range(n):
>             d, ad = row - col, row + col
>             if col in cols or d in diags or ad in anti_diags:
>                 continue
>             cols.add(col); diags.add(d); anti_diags.add(ad)
>             board[row][col] = 'Q'
>             bt(row + 1)
>             board[row][col] = '.'
>             cols.remove(col); diags.remove(d); anti_diags.remove(ad)
> 
>     bt(0)
>     return res
> ```

> [!success] Complexity
> O(n!) upper bound; actual solutions grow roughly as n!/e^n; O(n²) board space.

> [!tip] Alternatives
> Bitmask N-Queens: represent cols/diags/anti-diags as integers, use bit ops to find valid positions per row — lower constant, cache-friendly. Symmetry reduction: halve work for row 0.

---

### Sudoku Solver

> [!example] Problem
> Fill a 9×9 board (`.` for empties) satisfying Sudoku constraints.

> [!info] Approach
> - **WHY:** Constraint satisfaction: each empty cell has a small set of valid digits. Backtrack on the first empty cell, try all valid digits, recurse. Pruning is per-digit in O(1) via pre-populated boolean arrays. The search space is theoretically 9^81 but practically near-constant for valid puzzles due to constraint propagation via elimination.
> - **WHAT:** Precompute `rows[r][d]`, `cols[c][d]`, `boxes[b][d]` tracking used digits. Iterate empty cells; try 1-9; recurse; undo if stuck.
> - **HOW:** box_id = `(r//3)*3 + c//3`. Linear scan for next empty cell at each recursion level.

> [!note]- Python Solution
> ```python
> def solveSudoku(board: list[list[str]]) -> None:
>     rows = [[False] * 10 for _ in range(9)]
>     cols = [[False] * 10 for _ in range(9)]
>     boxes = [[False] * 10 for _ in range(9)]
> 
>     def box_id(r: int, c: int) -> int:
>         return (r // 3) * 3 + c // 3
> 
>     for r in range(9):
>         for c in range(9):
>             if board[r][c] != '.':
>                 d = int(board[r][c])
>                 rows[r][d] = cols[c][d] = boxes[box_id(r, c)][d] = True
> 
>     def bt(pos: int) -> bool:
>         while pos < 81 and board[pos // 9][pos % 9] != '.':
>             pos += 1
>         if pos == 81:
>             return True
>         r, c = pos // 9, pos % 9
>         for d in range(1, 10):
>             if rows[r][d] or cols[c][d] or boxes[box_id(r, c)][d]:
>                 continue
>             rows[r][d] = cols[c][d] = boxes[box_id(r, c)][d] = True
>             board[r][c] = str(d)
>             if bt(pos + 1):
>                 return True
>             board[r][c] = '.'
>             rows[r][d] = cols[c][d] = boxes[box_id(r, c)][d] = False
>         return False
> 
>     bt(0)
> ```

> [!success] Complexity
> O(9^m) where m = empty cells; practically O(1) for valid puzzles.

> [!tip] Alternatives
> MRV heuristic (most-constrained variable): always fill cell with fewest valid digits first — dramatically reduces backtracking. Dancing Links (Algorithm X): optimal exact cover solver, overkill for interviews.

---

### Unique Paths III

> [!example] Problem
> Start at cell with value 1, reach cell with value 2, visiting every non-obstacle cell exactly once. Return count of such paths.

> [!info] Approach
> - **WHY:** Hamiltonian path problem on a grid — no polynomial algorithm exists. DFS with backtracking, pruning when all non-obstacle cells must be visited exactly once.
> - **WHAT:** Count all non-obstacle cells (including start and end). DFS from start; at each step, mark visited; if at end and all cells visited, count +1.
> - **HOW:** Track `remaining` count of unvisited non-obstacle cells. Prune when stuck (all 4 neighbors blocked and remaining > 1).

> [!note]- Python Solution
> ```python
> def uniquePathsIII(grid: list[list[int]]) -> int:
>     m, n = len(grid), len(grid[0])
>     start_r = start_c = 0
>     total = 0  # total non-obstacle cells to visit
>     for r in range(m):
>         for c in range(n):
>             if grid[r][c] != -1:
>                 total += 1
>             if grid[r][c] == 1:
>                 start_r, start_c = r, c
> 
>     count = 0
> 
>     def dfs(r: int, c: int, visited: int) -> None:
>         nonlocal count
>         if grid[r][c] == 2:
>             if visited == total:
>                 count += 1
>             return
>         for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] != -1:
>                 grid[nr][nc], orig = -2, grid[nr][nc]  # mark
>                 dfs(nr, nc, visited + 1)
>                 grid[nr][nc] = orig  # restore
> 
>     grid[start_r][start_c] = -2  # mark start visited
>     dfs(start_r, start_c, 1)
>     grid[start_r][start_c] = 1
>     return count
> ```

> [!success] Complexity
> O(4^(m·n)) worst case; O(m·n) recursion depth.

> [!tip] Alternatives
> Bitmask DP: `dp[r][c][mask]` = number of paths visiting cells in `mask` ending at (r,c) — O(m·n·2^(mn)) space, infeasible for large grids. Backtracking with in-place marking is the standard approach.

---

## Trie + Backtracking

### Word Search II

> [!example] Problem
> Given a 2D board and a list of words, return all words found as paths on the board (adjacent, non-revisiting cells).

> [!info] Approach
> - **WHY:** Running Word Search I for each word is O(W · m · n · 4^L) — repeats identical board traversals. A Trie encodes all words simultaneously; DFS on the board drives the Trie traversal, sharing prefix exploration across all words.
> - **WHAT:** Build Trie of all words. DFS from each cell; at each step, advance in Trie if character exists. When reaching a word-end node, record the word.
> - **HOW:** Key optimizations: (1) Delete found words from Trie (`node.word = None`) to avoid duplicates. (2) Prune empty Trie nodes (`del node[ch]` after DFS) — reduces future DFS calls significantly.

> [!note]- Python Solution
> ```python
> def findWords(board: list[list[str]], words: list[str]) -> list[str]:
>     # Build Trie
>     trie: dict = {}
>     for word in words:
>         node = trie
>         for c in word:
>             node = node.setdefault(c, {})
>         node['$'] = word  # mark word end with the word itself
> 
>     m, n = len(board), len(board[0])
>     res: list[str] = []
> 
>     def dfs(r: int, c: int, node: dict) -> None:
>         ch = board[r][c]
>         if ch not in node:
>             return
>         nxt = node[ch]
>         if '$' in nxt:
>             res.append(nxt.pop('$'))  # found; remove to avoid duplicates
>         board[r][c] = '#'  # mark visited
>         for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < m and 0 <= nc < n and board[nr][nc] != '#':
>                 dfs(nr, nc, nxt)
>         board[r][c] = ch  # restore
>         if not nxt:  # prune empty trie node
>             del node[ch]
> 
>     for r in range(m):
>         for c in range(n):
>             dfs(r, c, trie)
> 
>     return res
> ```

> [!success] Complexity
> O(m · n · 4^L) DFS calls amortized across all words (Trie pruning dramatically reduces this in practice); O(W · L) Trie space.

> [!tip] Alternatives
> Per-word DFS — O(W · m · n · 4^L), degrades badly for large W. Aho-Corasick automaton: adds failure links for more aggressive pruning — overkill, not expected in interviews.

---

## See Also

[[recursion]] | [[dynamic-programming]] | [[trie]] | [[graph]]
