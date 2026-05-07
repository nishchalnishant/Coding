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
