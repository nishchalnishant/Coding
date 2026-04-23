# Backtracking — SDE-3 Gold Standard

Build solutions incrementally; **backtrack** when constraints fail. DFS over the implicit decision tree. SDE-3 expects: pruning strategies, complexity derivation, and knowing when to add memoization to convert to DP.

---

## 1. Concept Overview

**Problem space**: Permutations, combinations, subsets, N-Queens, Sudoku, Word Search, Palindrome Partitioning, Remove Invalid Parentheses, Letter Combinations.

**When to use**: "Generate all valid solutions" — OR — "find one valid configuration" — AND — the search space is a tree of choices with constraints. If you see overlapping subproblems in the recursion, memoize → DP.

---

## 2. The Universal Template

> [!IMPORTANT]
> **The Click Moment**: "Generate **all** X" — OR — "find **one** valid assignment" — OR — "place N items with constraints". Any problem where you try choices, undo them, and try the next one maps to this template. The shape of the decision tree determines complexity before you write a line.

```python
def backtrack(path: list, state, choices) -> None:
    if is_goal(path, state):
        results.append(path[:])  # copy — path is mutated in-place
        return
    for choice in get_choices(state, choices):
        if not is_valid(choice, state):
            continue
        apply(path, state, choice)      # make choice
        backtrack(path, state, choices) # recurse
        undo(path, state, choice)       # undo choice (backtrack)
```

> [!CAUTION]
> **The #1 backtracking bug**: Forgetting to undo the choice after the recursive call. If you push to `path` before recursing, you must `path.pop()` after. If you mutate a `visited` set, you must `visited.remove()` after. Missing the undo step causes state corruption across branches.

---

## 3. Core Patterns & Click Moments

### Subsets / Combinations — Choose or Skip

> [!IMPORTANT]
> **The Click Moment**: "All subsets", "power set", "all combinations of size K", "number of ways to pick K from N". Use a `start` index to avoid duplicate sets (no going back to previous elements).

```python
def subsets(nums: list[int]) -> list[list[int]]:
    results = []
    def backtrack(start: int, path: list[int]) -> None:
        results.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return results

def combine(n: int, k: int) -> list[list[int]]:
    results = []
    def backtrack(start: int, path: list[int]) -> None:
        if len(path) == k:
            results.append(path[:])
            return
        # Pruning: not enough elements remaining
        for i in range(start, n - (k - len(path)) + 2):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    backtrack(1, [])
    return results
```

> [!TIP]
> **Key pruning for combinations**: In `combine`, the loop upper bound is `n - (k - len(path)) + 2`, not `n + 1`. This prunes branches where there aren't enough remaining elements to reach size K — reduces constant factor significantly.

---

### Permutations — Use All Elements in Different Orders

> [!IMPORTANT]
> **The Click Moment**: "All orderings", "all arrangements", "assign N tasks to N workers". Each level of the tree picks from the **remaining unused** elements. O(N!) leaves.

```python
def permute(nums: list[int]) -> list[list[int]]:
    results = []
    def backtrack(path: list[int], remaining: list[int]) -> None:
        if not remaining:
            results.append(path[:])
            return
        for i in range(len(remaining)):
            path.append(remaining[i])
            backtrack(path, remaining[:i] + remaining[i+1:])
            path.pop()
    backtrack([], nums)
    return results

def permute_unique(nums: list[int]) -> list[list[int]]:
    results = []
    nums.sort()
    def backtrack(path: list[int], used: list[bool]) -> None:
        if len(path) == len(nums):
            results.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            # Skip duplicate: same value as prev, and prev not used in this branch
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False
    backtrack([], [False] * len(nums))
    return results
```

> [!CAUTION]
> **Duplicate permutations trap**: For `[1,1,2]`, naive permutation generates duplicate results. The fix: sort first, then skip `nums[i] == nums[i-1] and not used[i-1]`. The `not used[i-1]` condition ensures we only skip when the identical previous element was skipped at this recursion level.

---

### Constraint Satisfaction — N-Queens, Sudoku

> [!IMPORTANT]
> **The Click Moment**: "Place N items on a board with mutual exclusion constraints", "fill a grid satisfying rules". The key is encoding which choices remain valid as you go deeper — sets tracking used columns/diagonals are O(1) per check vs O(N) scanning.

```python
def solve_n_queens(n: int) -> list[list[str]]:
    results = []
    cols = set()
    diag1 = set()  # row + col (left diagonal)
    diag2 = set()  # row - col (right diagonal)

    def backtrack(row: int, board: list[int]) -> None:
        if row == n:
            results.append(["." * c + "Q" + "." * (n - c - 1) for c in board])
            return
        for col in range(n):
            if col in cols or (row + col) in diag1 or (row - col) in diag2:
                continue
            cols.add(col); diag1.add(row + col); diag2.add(row - col)
            board.append(col)
            backtrack(row + 1, board)
            board.pop()
            cols.remove(col); diag1.remove(row + col); diag2.remove(row - col)

    backtrack(0, [])
    return results
```

> [!TIP]
> **Bitmask N-Queens (SDE-3 follow-up)**: Encode `cols`, `diag1`, `diag2` as integers. Available columns = `((1 << n) - 1) & ~(cols | diag1 | diag2)`. Extract lowest set bit with `pos = avail & (-avail)`. This runs 3-5× faster than set-based due to cache efficiency — mention this as the optimized version.

---

### Word Search — Grid DFS with Backtracking

> [!IMPORTANT]
> **The Click Moment**: "Find a word in a 2D grid moving to adjacent cells", "path exists through a matrix". Mark visited in-place (swap to `#`) and restore after — avoids a separate `visited` set.

```python
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(cols := board[0]) if board else (0, 0)

    def dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[idx]:
            return False
        tmp, board[r][c] = board[r][c], '#'  # mark visited in-place
        found = any(dfs(r + dr, c + dc, idx + 1) for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)])
        board[r][c] = tmp  # restore
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
```

---

### Palindrome Partitioning

> [!IMPORTANT]
> **The Click Moment**: "Partition string into palindromic substrings", "minimum cuts for palindrome partition". The key insight: precompute a 2D palindrome table in O(N²) so each validity check is O(1) during backtracking.

```python
def partition(s: str) -> list[list[str]]:
    n = len(s)
    # Precompute: is_pal[i][j] = True if s[i:j+1] is a palindrome
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            is_pal[i][j] = (s[i] == s[j]) and (j - i <= 2 or is_pal[i+1][j-1])

    results = []
    def backtrack(start: int, path: list[str]) -> None:
        if start == n:
            results.append(path[:])
            return
        for end in range(start, n):
            if is_pal[start][end]:
                path.append(s[start:end+1])
                backtrack(end + 1, path)
                path.pop()
    backtrack(0, [])
    return results
```

---

## 4. Complexity Reference

| Problem | Time | Space | Pruning Available? |
| :--- | :--- | :--- | :--- |
| Subsets | O(2^N × N) | O(N) stack | Pruning by sum or size |
| Permutations | O(N! × N) | O(N) stack | Skip duplicates |
| Combinations C(n,k) | O(C(n,k) × k) | O(k) stack | Prune when remaining < needed |
| N-Queens | O(N!) | O(N) | Column/diagonal sets |
| Word Search | O(4^L × R×C) | O(L) | Mark visited, prune early mismatch |
| Sudoku | O(9^81) worst | O(81) | Constraint propagation (MRV) |

---

## 5. SDE-3 Deep Dives

### Backtracking vs DP: The Conversion Rule

> [!TIP]
> **When to add memoization**: If the same `(start_index, current_state)` is reached by multiple distinct paths through the tree, the subproblems overlap and memoization converts the exponential backtracking to polynomial DP. Classic example: Word Break — `dp[i]` = can segment `s[:i]` — the same suffix is tried from multiple starting positions.

```python
# Backtracking → DP conversion example: Word Break
from functools import lru_cache

def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)
    n = len(s)
    @lru_cache(maxsize=None)
    def can_break(start: int) -> bool:
        if start == n:
            return True
        return any(s[start:end] in words and can_break(end)
                   for end in range(start + 1, n + 1))
    return can_break(0)
```

### Scalability: Iterative Backtracking for Deep Trees

> [!CAUTION]
> Python's default recursion limit is 1000. For grids with up to 200×200 = 40,000 cells, recursive DFS will stack-overflow. Convert to **explicit stack** for production:

```python
def dfs_iterative(start, choices):
    stack = [(start, [])]  # (state, path)
    results = []
    while stack:
        state, path = stack.pop()
        if is_goal(state):
            results.append(path)
            continue
        for choice in get_choices(state):
            if is_valid(choice, state):
                stack.append((next_state(state, choice), path + [choice]))
    return results
```

### Concurrency: Parallel Backtracking

> [!TIP]
> Backtracking trees are **embarrassingly parallelizable at the root's children**. For N-Queens(N=20+), split across the N choices for row 0 and assign each subtree to a different process (`multiprocessing.Pool`). Each subtree is fully independent — no shared state between branches. Combine results after all subtrees complete. This scales linearly with available cores.

### Trade-offs

| Approach | Time | Space | When to Prefer |
| :--- | :--- | :--- | :--- |
| Pure backtracking | Exponential | O(depth) stack | All valid solutions needed; constraints prune heavily |
| Backtracking + memo | Polynomial (if overlapping) | O(states) | Count/exists queries with repeated states |
| DP (tabulation) | Polynomial | O(states) | Overlapping subproblems confirmed; single answer |
| Bitmask DP (N≤20) | O(2^N × N) | O(2^N × N) | Subset tracking with small N |

---

## 6. Common Interview Problems

### Easy
- **Subsets** — Include/exclude each index; `start` index prevents duplicates.
- **Letter Combinations of Phone Number** — Cartesian product via DFS.

### Medium
- **Permutations / Permutations II** — Unused set; sort + skip for duplicates.
- **Combination Sum / II** — Unbounded (reuse `i`) vs 0/1 (advance `i+1`).
- **Word Search** — Grid DFS with in-place marking.
- **Palindrome Partitioning** — Precompute palindrome table; O(1) check per partition.
- **Generate Parentheses** — Track open/close counts; prune when `close > open`.

### Hard
- **N-Queens** — Column + diagonal sets; bitmask variant for speed.
- **Sudoku Solver** — MRV heuristic (cell with fewest valid digits first).
- **Word Search II** — Trie of all words + backtracking; prune when no trie prefix matches.
- **Remove Invalid Parentheses** — BFS by removal count; or backtracking with min-removal pruning.
- **Expression Add Operators** — Backtrack with last-operand tracking for `*` precedence.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **Subsets** | "All possible subsets" | Include/exclude; `start` index | Deep copy path: `results.append(path[:])`, not `path`. |
| **Permutations** | "All orderings of N elements" | Swap-in-place or unused set | Permutations II: sort first; skip `nums[i]==nums[i-1] and not used[i-1]`. |
| **Combination Sum** | "Target sum, reuse allowed" | Advance same `i` (unbounded) | Sum II: advance `i+1`; skip duplicate values at same level. |
| **N-Queens** | "Place N non-attacking queens" | `cols`, `diag r+c`, `diag r-c` sets | Diagonals use `r+c` and `r-c` as keys — derive from first principles. |
| **Word Search** | "Path spelling word in grid" | Mark `#` in-place; restore after | Word Search II: Trie prunes branches with no matching prefix. |
| **Sudoku Solver** | "Fill grid satisfying constraints" | Try 1-9; check row/col/box | MRV heuristic: pick cell with fewest valid candidates first. |
| **Palindrome Partitioning** | "All palindrome splits" | Precompute `is_pal[i][j]` | Without precompute: O(N³); with: O(N²) — always precompute. |
| **Generate Parentheses** | "All valid bracket sequences of N pairs" | Track open/close count | Prune: `open < n` to add `(`; `close < open` to add `)`. |
| **Remove Invalid Parentheses** | "Remove min to make valid" | BFS by removal count | Generate all possible removals of length `k`; check validity. |
| **Letter Combinations** | "Phone keypad, all combos" | Cartesian product via DFS | Empty `digits` input → return `[]`, not `[""]`. |
| **Expression Add Operators** | "Insert +,-,* to reach target" | Backtrack with `last_operand` | `*` needs to undo `last_operand` from running sum before re-multiplying. |

---

## See also

- [Dynamic Programming](dynamic-programming/README.md) — memoize overlapping backtracking → DP
- [Bit Manipulation](bit-manipulation.md) — bitmask as backtracking state for N≤20
- [Recursion](recursion/README.md) — base cases and stack depth
- [Trie](../data-structures/trie.md) — Word Search II (pruning via Trie prefix)
