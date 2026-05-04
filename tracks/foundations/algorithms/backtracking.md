# Backtracking — SDE-3 Gold Standard

Build solutions incrementally; **backtrack** when constraints fail. DFS over the implicit decision tree. SDE-3 expects: pruning strategies, complexity derivation, and knowing when to add memoization to convert to DP.

---

## Theory & Mental Models

**What it is.** Systematic trial-and-error over a decision tree: explore depth-first, and when a partial solution violates a constraint, undo the last choice and try the next alternative. Core invariant: state is fully restored after each recursive call — the **choose → explore → unchoose** cycle.

**Why it exists.** Many problems require generating all valid configurations (permutations, placements, partitions) where constraints eliminate most candidates early. Backtracking formalizes "try everything, but prune dead ends immediately" — far faster in practice than enumerating all leaves naively.

**The mental model.** A maze solver who marks dead ends and backtracks to the last fork. At each fork, pick a direction; if you hit a wall, erase your mark and return to the fork to try the next direction.

**Complexity at a glance.**

| Operation | Time | Space |
| :--- | :--- | :--- |
| Worst-case enumeration | O(branching_factor^depth) | O(depth) — recursion stack |
| With effective pruning | Much less in practice | O(depth) |
| Copy path on collect | +O(path length) per result | — |

**When to reach for it.**
- Generate all subsets, permutations, or combinations.
- Constraint satisfaction: N-Queens, Sudoku, crossword fill.
- Word search in a grid (DFS with visited marking).
- Partition a sequence into valid groups (palindrome partition, combination sum).
- "Find one valid configuration" problems.

**When NOT to use it.**
- You need a single optimal answer — use greedy or DP (backtracking revisits too much).
- N > 20 with subset-tracking — use bitmask DP instead.
- Subproblems repeat — add memoization to convert to top-down DP.

**Common mistakes.**
- Not undoing state after the recursive call — mutations leak across branches (the #1 bug).
- Forgetting to copy the current path before appending to results (`path[:]` not `path`).
- Starting index confusion: combinations use a `start` index to avoid going backwards; permutations do not.
- Wrong base case — returning too early (missing valid paths) or too late (infinite recursion).

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

#### Sudoku Solver (LC 37)

```python
def solve_sudoku(board: list[list[str]]) -> None:
    # 1. Precompute constraints for O(1) lookup
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empty = []
    
    for r in range(9):
        for c in range(9):
            if board[r][c] == '.':
                empty.append((r, c))
            else:
                val = board[r][c]
                rows[r].add(val)
                cols[c].add(val)
                boxes[(r // 3) * 3 + c // 3].add(val)
                
    def backtrack(index: int) -> bool:
        if index == len(empty): return True
        r, c = empty[index]
        box_idx = (r // 3) * 3 + c // 3
        
        for val in map(str, range(1, 10)):
            if val not in rows[r] and val not in cols[c] and val not in boxes[box_idx]:
                # Apply choice
                board[r][c] = val
                rows[r].add(val); cols[c].add(val); boxes[box_idx].add(val)
                
                if backtrack(index + 1): return True
                
                # Undo choice
                board[r][c] = '.'
                rows[r].remove(val); cols[c].remove(val); boxes[box_idx].remove(val)
        return False
        
    backtrack(0)
```

> [!TIP]
> **MRV Optimization**: Instead of passing `empty` as a fixed list, dynamically pick the empty cell with the fewest valid options remaining (Minimum Remaining Values heuristic). This radically prunes the search space.

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

## 4. Advanced Pruning Strategies

> [!IMPORTANT]
> SDE-3 interviews aren't just about writing the backtracking template — they are about **pruning the search space** aggressively. Without pruning, backtracking is just O(N!) brute force.

### 4.1 Minimum Remaining Values (MRV) Heuristic
Instead of picking the "next" item sequentially, always pick the item with the **fewest valid options**. If an item has 0 options, the branch dies immediately.
- **Example**: In Sudoku, don't fill cells row-by-row. Count valid digits for each empty cell, and pick the cell with the fewest candidates.

### 4.2 Look-ahead / Feasibility Checks
Before recursing, check if the goal is even mathematically reachable.
- **Example**: In Subset Sum, if `remaining_target` > sum of all remaining elements, return immediately.
- **Example**: In Grid Pathfinding, if the Manhattan distance to the goal is greater than the remaining allowed steps, prune.

### 4.3 Symmetry Breaking
If the problem space is symmetric, force an arbitrary order to avoid exploring identical mirror-image branches.
- **Example**: In Combinations, the `start` index is a symmetry breaker (prevents `[1,2]` and `[2,1]`).
- **Example**: If assigning tasks to identical workers, enforce that Worker A's first task ID must be < Worker B's first task ID.

---

## 5. Complexity Reference

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

```

### Backtracking to DP: All Paths (Word Break II)

Sometimes you need *all* paths, but subproblems overlap wildly. Memoize the **list of valid suffixes** to avoid exponential re-expansion.

```python
def word_break_ii(s: str, word_dict: list[str]) -> list[str]:
    words = set(word_dict)
    
    @lru_cache(maxsize=None)
    def backtrack(start: int) -> list[str]:
        if start == len(s): return [""]
        results = []
        for end in range(start + 1, len(s) + 1):
            if s[start:end] in words:
                suffixes = backtrack(end)
                for suffix in suffixes:
                    results.append(s[start:end] + (" " + suffix if suffix else ""))
        return results
        
    return backtrack(0)
```

### State Management: Mutable vs. Immutable

> [!TIP]
> How you pass state down the recursion tree dramatically impacts performance and bug likelihood.

| Approach | Code Example | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **Mutable (In-place)** | `path.append(x); dfs(); path.pop()` | O(1) space allocation per node; extremely fast | High risk of bugs if `pop()` missed or path not copied at base case. |
| **Immutable (Copy)** | `dfs(path + [x])` | Safe; no undo needed; easy to convert to DP | O(N) allocation per call; very slow for deep trees. |

**SDE-3 Rule**: Use mutable state for large collections (lists, grids, sets) to avoid O(N) allocation overhead per node. Use immutable state (strings, integers) where Python handles the immutability natively.

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

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **Subsets** | Include/Exclude | "All possible subsets" | Include/exclude; `start` index | Deep copy path: `results.append(path[:])`, not `path`. |
| **Permutations** | Swap / Used-array | "All orderings of N elements" | Swap-in-place or unused set | Permutations II: sort first; skip `nums[i]==nums[i-1] and not used[i-1]`. |
| **Combination Sum** | Include/Exclude + Target | "Target sum, reuse allowed" | Advance same `i` (unbounded) | Sum II: advance `i+1`; skip duplicate values at same level. |
| **N-Queens** | Constraint Satisfaction | "Place N non-attacking queens" | `cols`, `diag r+c`, `diag r-c` sets | Diagonals use `r+c` and `r-c` as keys — derive from first principles. |
| **Word Search** | Grid DFS + Backtrack | "Path spelling word in grid" | Mark `#` in-place; restore after | Word Search II: Trie prunes branches with no matching prefix. |
| **Sudoku Solver** | Constraint Satisfaction | "Fill grid satisfying constraints" | Try 1-9; check row/col/box | MRV heuristic: pick cell with fewest valid candidates first. |
| **Palindrome Partitioning** | Include/Exclude + Validity Guard | "All palindrome splits" | Precompute `is_pal[i][j]` | Without precompute: O(N³); with: O(N²) — always precompute. |
| **Generate Parentheses** | IP/OP Validity Guard | "All valid bracket sequences of N pairs" | Track open/close count | Prune: `open < n` to add `(`; `close < open` to add `)`. |
| **Remove Invalid Parentheses** | BFS by Level | "Remove min to make valid" | BFS by removal count | Generate all possible removals of length `k`; check validity. |
| **Letter Combinations** | Cartesian Product DFS | "Phone keypad, all combos" | Cartesian product via DFS | Empty `digits` input → return `[]`, not `[""]`. |
| **Expression Add Operators** | Backtrack + Running State | "Insert +,-,* to reach target" | Backtrack with `last_operand` | `*` needs to undo `last_operand` from running sum before re-multiplying. |
| **Binary Watch** [E] | Include/Exclude + Pruning | "Generate all times readable on binary watch" | Backtrack placing lit LEDs; check hours < 12, minutes < 60 | Enumerate bit counts, not time values — easier to prune invalid combos. |
| **Find All Anagrams in a String** [E] | Sliding Window (not backtracking) | "All start indices of anagrams of p in s" | Sliding window with frequency map — not backtracking | Click moment: fixed window size = backtracking becomes sliding window here. |
| **Restore IP Addresses** [M] | Backtrack + Validity Guard | "Generate all valid IP addresses from digit string" | Backtrack with 4 parts; each part 0-255, no leading zeros | Leading zero check: `part[0] == '0' and len(part) > 1` is invalid. Exactly 4 parts required. |
| **Combinations** [M] | Include/Exclude + Start Index | "All K-element subsets of [1,N]" | Backtrack with `start` index; stop when path length == K | Prune: if `n - start + 1 < k - len(path)`, not enough elements left — prune early. |
| **Target Sum** [M] | Include/Exclude → 0/1 Knapsack | "Assign + or - to reach target" | Backtrack each element; or reframe as subset sum (partition into two groups) | `(sum + target) % 2 != 0` or `sum + target < 0` → impossible; converts to count-subsets problem. |
| **Partition to K Equal Subsets** [M] | Backtrack + Bucket Pruning | "Can array be split into K equal-sum subsets?" | Backtrack assigning elements to buckets; prune if bucket overflows | Sort descending first — places large elements first and prunes faster. Skip identical-value buckets at same depth. |
| **Word Break II** [M] | DFS + Memoization | "All sentences from word dictionary covering s" | DFS with memoization; memo maps `start_index → [sentences]` | Memoize the list of valid sentences from each index — avoids exponential re-expansion. |
| **Unique Paths III** [H] | Grid Backtrack + Bitmask | "Count paths visiting all non-obstacle squares exactly once" | Backtrack on grid; mark visited; only count path reaching end when all squares visited | Track remaining empty squares counter to know when path is complete — no need to re-scan. |
| **Zuma Game** [H] | Interval DP / Memoized Backtrack | "Min insertions to clear all groups" | Interval DP or memoized backtracking on remaining groups | Group consecutive same-color balls; state = current group string. Handle groups merging after removal. |
| **Stickers to Spell Word** [H] | Bitmask DP / BFS | "Min stickers to spell target (unlimited reuse)" | Bitmask BFS/DP on covered chars; each state = bitmask of covered target chars | Always fill leftmost uncovered char first to reduce duplicate states. |

---

## Quick Revision Triggers

- "Generate all valid combinations / permutations / subsets" → backtracking with choose / recurse / unchoose.
- "Constraint says order matters, use each element once" → permutation backtracking with `visited[]` array.
- "Constraint says order doesn't matter, no reuse" → combination backtracking with `start` index advancing.
- "Find paths in a grid with obstacles" → DFS backtracking marking cell visited, unmark on return.
- "Decision tree branches explode but many share the same failure condition" → prune before recursing.
- "Duplicate elements in input; distinct results required" → sort first, skip `nums[i] == nums[i-1]` at the same depth level.
- "State is mutable (list, grid) and must be restored after recursing" → explicit undo; immutable state (string, int) needs no undo.

---

## See also

- [Dynamic Programming](dynamic-programming/README.md) — memoize overlapping backtracking → DP
- [Bit Manipulation](bit-manipulation.md) — bitmask as backtracking state for N≤20
- [Recursion (Full Playbook)](recursion/README.md) — core recursion types and iterative conversion
- [Combination Problems](recursion/combination-problems.md) — full combinatorial family (Sum I-IV)
- [String Recursion](recursion/string-recursion.md) — Regex, wildcard, decode string
- [Trie](../data-structures/trie.md) — Word Search II (pruning via Trie prefix)
