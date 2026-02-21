# Backtracking

An algorithmic technique for solving problems incrementally by trying to build a solution piece by piece, dropping (backtracking) solutions that fail to satisfy the constraints.

## Key Concepts
- **State/Path**: The current combination being explored.
- **Choices**: The possible options at a given step.
- **Constraints**: Rules that must be satisfied to continue down a path. If violated, prune the branch.
- **Base Case (Goal)**: When the `Path` satisfies the total problem requirements, add it to the result set.

## Backtracking Template
```python
def backtrack(path, options):
    if is_goal(path):
        results.append(path.copy())
        return
    for option in options:
        if is_valid(option):
            path.append(option)      # Make a choice
            backtrack(path, new_opts) # Explore
            path.pop()               # Undo choice (Backtrack)
```

## Depth-First Search (DFS) Similarity
Backtracking is essentially a DFS traversal of the decision/state tree. The `pop()` operation reverses the state changes as the recursion unwinds.

## Common SDE-3 Backtracking Problems
- *Easy*: Binary Tree Paths, Subsets.
- *Medium*: Permutations, Combinations, Combination Sum, Word Search, Letter Combinations of a Phone Number.
- *Hard*: N-Queens, Sudoku Solver, Word Search II, Remove Invalid Parentheses.
