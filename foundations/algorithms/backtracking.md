# Backtracking — SDE-3 Level

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

- **Permutations**: Choices = unused elements; path length = n.
- **Combinations/Subsets**: Choices = include or not; or "next start index" to avoid duplicate sets.
- **Constraint satisfaction**: N-Queens (place row by row, check column/diagonals); Sudoku (try 1-9, check row/col/box).
- **String/path**: Word Search — 4 directions, visited set; undo visited on backtrack.

---

## 6. SDE-3 Level Thinking

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
