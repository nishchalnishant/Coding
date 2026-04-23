# Backtracking — SDE-2+ Level

Build solutions incrementally; **backtrack** when constraints fail. DFS over the decision tree. SDE-3 expects pruning, complexity analysis, and when to add memoization (overlap with DP).

---

## 1. Concept Overview

**Problem space**: Permutations, combinations, subsets, N-Queens, Sudoku, Word Search, combination sum, palindrome partitioning, invalid parentheses removal.

**When to use**: "Generate all" or "find one" with constraints; choices at each step; no obvious greedy. If overlapping subproblems appear, add memo → DP.

---

## 2. Core Template

- **State**: path (or current partial solution); optional index/start.
- **Choices**: at each step, which option to try (e.g., which number to place, which letter).
- **Constraints**: prune when invalid (e.g., queen under attack, sum > target).
- **Goal**: path complete → add to result (or return true for "find one").
- **Backtrack**: undo last choice (path.pop(); restore state) after recursive call.

```python
def backtrack(path, start, ...):
    if is_goal(path):
        results.append(path[:])
        return
    for choice in choices(start, ...):
        if not valid(choice): continue
        path.append(choice)
        backtrack(path, new_start, ...)
        path.pop()
```

---

## 3. Advanced Variations

- **Pruning**: Combination sum — stop when remaining < 0; N-Queens — skip column/diagonal attack; Subset sum — sort and prune if remaining sum too small.
- **Memoization**: When same (state, start) can repeat (e.g., combination sum with duplicates but "use each once") — state = (index, target); memo avoids recomputation → becomes DP.
- **Complexity**: Permutations O(N!); subsets O(2^N); combinations C(n,k). Word Search: 4^L per cell without memo; with visited O(cells * 4^L) worst case.

### Edge Cases
- Empty input; single element; duplicates (skip same choice in same level); large N (stack depth).

---

## 4. Common Interview Problems

**Easy**: Binary Tree Paths, Subsets.  
**Medium**: Permutations, Combinations, Combination Sum, Word Search, Letter Combinations.  
**Hard**: N-Queens, Sudoku Solver, Word Search II (Trie + backtrack), Remove Invalid Parentheses.

---

## 5. Pattern Recognition

- **[Problem Details](../../google-sde2/PROBLEM_DETAILS.md#permutations)**: Choices = unused elements; path length = n.
- **Combinations/Subsets**: Choices = include or not; or "next start index" to avoid duplicate sets.
- **Constraint satisfaction**: N-Queens (place row by row, check column/diagonals); Sudoku (try 1-9, check row/col/box).
- **String/path**: Word Search — 4 directions, visited set; undo visited on backtrack.

---

## 6. Trade-offs & Scaling (optional)

- **Trade-offs**: Backtracking explores all valid paths; DP when subproblems overlap (then state + memo). Pruning reduces tree size significantly.
- **Memory**: Recursion depth = length of path; visited set O(path length) or reuse array. Word Search II: Trie reduces branches (only follow existing prefixes).

---

## 7. Interview Strategy

- **Identify**: "All solutions", "place/assign with constraints" → backtrack. "Count" or "min/max" with overlap → DP.
- **Approach**: Define state, choices, constraints, goal; code template; add pruning. Mention complexity.
- **Common mistakes**: Forgetting to undo (path.pop(), visited.remove); duplicate results (use start index or sort and skip same value at same level).

---

## 8. Quick Revision

- **Template**: path, choices, valid, goal, path.pop() after recurse.
- **Tricks**: Use start index to avoid duplicate combinations; for permutations swap and recurse or use "remaining" set. N-Queens: cols, diag1 (r+c), diag2 (r-c) sets.
- **Edge cases**: Duplicates; empty; one element.
- **Pattern tip**: "Generate all" / "find one valid" with constraints → backtrack; overlap → memo → DP.

---

## 9. Code sketch (permutations)

More SDE-2 reference implementations (Python): `../../google-sde2/snippets/python/backtracking.py`.

```python
def permute(nums):
    res = []
    def backtrack(path, remaining):
        if not remaining:
            res.append(path[:])
            return
        for i, x in enumerate(remaining):
            backtrack(path + [x], remaining[:i] + remaining[i+1:])
    backtrack([], nums)
    return res
```

*(Production-style: swap in-place or use a `used` boolean array to avoid O(n) slice cost.)*

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness & details |
|----------|------------|----------------------|
| **[Problem Details](../../google-sde2/PROBLEM_DETAILS.md#permutations)** | DFS: choose next unused element; **swap** method: fix position `i` with each `j≥i`. | **Duplicates:** **sort** first; skip `nums[j]==nums[j-1]` when `j>start` not to repeat same level choice. |
| **Permutations II** | Same as permutations with **duplicate skip**; or use **Counter** multiset. | **Time:** O(n! × n); **space** recursion depth. |
| **Combinations** | `dfs(start, path)` pick `i` from `start..n-1` until `len(path)==k`. | **Prune:** if `remaining elements < k - len(path)` return. |
| **[Problem Details](../../google-sde2/PROBLEM_DETAILS.md#combination-sum)** | Reuse index `i` (unbounded same element); target decreases by `nums[i]`. | **Combination Sum II:** **next index `i+1`**, no reuse; **duplicate** values skip same as subset II. |
| **[Problem Details](../../google-sde2/PROBLEM_DETAILS.md#subsets)** | Include/exclude each index; or iterative cascade. | **[Problem Details](../../google-sde2/PROBLEM_DETAILS.md#subsets-ii)** with duplicate skip. |
| **N-Queens** | Place row `r` in column `c` if `col` and two diagonals `r+c`, `r-c` free. | **Diag** keys: `r+c` and `r-c`; **bitmask** for speed. |
| **[Problem Details](../../google-sde2/PROBLEM_DETAILS.md#word-search)** | DFS from each cell; mark visited **or** mutate board to `#`; **4-direction** backtrack. | **Word Search II:** **Trie** of words to prune; **O(sum of words)** vs repeated scans. |
| **Sudoku Solver** | Find empty; try 1–9; check row/col/box; recurse; **undo** on failure. | **Heuristic:** pick cell with **fewest** candidates (MRV). |
| **Palindrome Partitioning** | DFS: partition prefix if palindrome; recurse on suffix. | **DP** precompute `isPal[i][j]` to avoid O(n) palindrome check each step. |
| **Restore IP Addresses** | DFS insert dots after 1–3 digits; validate octet 0–255 and no leading `0` unless single `0`. | **Prune** invalid length early; **4 parts** exactly. |
| **Letter Combinations Phone** | Cartesian product via DFS or iterative queue. | **Empty** digits edge case. |

---

## See also

- [Dynamic Programming](dynamic-programming/README.md) — overlapping subproblems → memo  
- [Recursion](recursion/README.md) — base case and stack depth  
- [Trie + backtrack](../../advanced-dsa/trie-segment-trees.md) — Word Search II
