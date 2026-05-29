---
module: 02-algorithms
topic: Recursion
subtopic: Questions Bank
status: unread
tags: [algorithms, recursion]
---
## First-Principles Map

```text
WHY recursion & backtracking exist
├── Problems with exponential state spaces can't be enumerated iteratively without explicit stacks
│   ├── Combinatorial search: subsets, permutations, combinations — O(2^n) or O(n!) states
│   └── Constraint satisfaction: N-Queens, Sudoku — pruning makes brute-force tractable
WHAT it is
├── Recursion: reduce problem to smaller subproblem of identical structure; call stack manages state
│   ├── Base case: smallest valid input handled directly
│   └── Recursive case: split, delegate, recombine
├── Backtracking: DFS over a decision tree; undo choice (restore state) on return from branch
│   ├── "Make choice → recurse → undo choice" is the universal template
│   └── Pruning: reject a branch early when a constraint is already violated
HOW it works
├── Decision tree model
│   ├── Each node = a partial solution; each edge = one choice
│   ├── Leaf = complete solution or dead end
│   └── Backtrack = pop the last choice and try the next sibling
├── State management
│   ├── Immutable state: pass modified copies down (safe, higher memory)
│   └── Mutable state: modify in-place before recurse, restore after (O(1) overhead, error-prone)
├── Complexity
│   ├── Subsets: O(2^n · n); Permutations: O(n! · n); Combinations: O(C(n,k) · k)
│   └── Pruning can reduce by orders of magnitude but worst case remains exponential
WHEN to use
├── "generate all X" (subsets, permutations, combinations) → backtracking template
├── "find any valid assignment" (Sudoku, N-Queens) → backtracking + constraint pruning
├── "tree/graph path exists" → DFS recursion with visited set
└── Problem has overlapping subproblems → memoize recursion → DP
WHAT can go wrong
├── Missing base case → infinite recursion / stack overflow
├── Forgetting to undo mutation → corrupted state in sibling branches
└── Duplicate results → need sorted input + skip-same-value guard at each recursion level
DECISION
└── If all solutions needed → backtracking; if only optimal value needed + overlapping subproblems → DP over recursion
```

## First-Principles Breakdown

- **Root problem**: Combinatorial search requires exploring an exponentially large state space in a structured, prunable way.
- **Core insight**: The call stack IS the explicit state machine — each frame holds one level of the decision tree; returning from a frame undoes that decision for free.
- **Invariant**: At every recursive call, the partial solution is valid with respect to all constraints imposed so far.
- **Why it works**: Pruning eliminates entire subtrees early; in practice this reduces average-case from O(n!) to manageable depth-limited DFS.
- **Where it breaks**: Forgetting to restore mutable state after recursion contaminates sibling branches and produces wrong or duplicate results.

---

# Recursion & Backtracking Question Bank — Tiered Drill

Master the art of the "multiverse search". Every problem here follows the [Universal Recursion Recipe](aditya-verma.md).

---

## 🟢 Level 1: Foundation (Branching & Choice)

| Problem | Pattern | Key Insight |
| :--- | :--- | :--- |
| **Subsets (Power Set)** | Include/Exclude | 2 choices per element: `2^N` |
| **Permutations** | Choice-based | Pick any unused element; `N!` |
| **Binary Tree Paths** | Structural DFS | Leaf is base case; pass path string |
| **Merge Sort** | Divide & Conquer | Split until size 1; merge results |
| **Fibonacci** | Mathematical | `f(n) = f(n-1) + f(n-2)` |

---

## 🟡 Level 2: SDE-2 Standard (Pruning & Constraints)

| Problem | Pattern | The Twist |
| :--- | :--- | :--- |
| **Combination Sum** | Unbounded Choice | Can reuse same element: `recurse(i)` not `i+1` |
| **Combination Sum II** | Duplicate Input | Sort + skip sibling duplicates: `if j>i and nums[j]==nums[j-1]` |
| **Generate Parentheses** | Validity Guard | Add `(` if `open < n`, `)` if `close < open` |
| **Word Search** | Grid Backtracking | Mark `board[r][c]` visited; restore on undo |
| **Palindrome Partitioning** | String Splitting | Only recurse if prefix is a palindrome |
| **Letter Case Permutation** | IP/OP | Branch on alpha; skip digits |

---

## 🔴 Level 3: SDE-3 / Staff Level (Constraint Satisfaction)

| Problem | Pattern | Complexity / Optimization |
| :--- | :--- | :--- |
| **N-Queens** | Board Backtracking | Column and diagonal clash sets |
| **Sudoku Solver** | Matrix Search | Fill empty cells; 9 branches each; early exit on first valid |
| **Word Search II** | Trie + Backtracking | Use Trie to prune multiple word searches into one DFS |
| **Unique Binary Search Trees II** | Structural D&C | Build all left/right combos for each root `k` |
| **Expression Add Operators** | Mathematical Search | Handle `*` precedence by tracking `prev_added` |
| **Robot Room Cleaner** | State-Space Search | Track `(r, c)` in set; move + rotate; spiral-out |

---

## 🛠️ Drill Instructions

1.  **State your IP/OP.** What are you passing down (Input) and what are you building (Output)?
2.  **Draw the Decision Tree.** For a small example (e.g., `n=3`), can you trace the branches?
3.  **Identify the Base Case.** What is the smallest version of the problem you can solve instantly?
4.  **The "Undo" (Backtracking).** If you modified global state (visited set, board), did you restore it before returning?

---

## See also

- [Aditya Verma Patterns](aditya-verma.md) — Step-by-step build for these patterns.
- [Recursion README](README.md) — Theoretical foundations and complexity map.
