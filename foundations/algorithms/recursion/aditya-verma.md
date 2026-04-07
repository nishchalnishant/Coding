# Recursion — Aditya Verma Style (Supplement)

Structured way to think about **recursion as decisions + smaller input**. Use alongside [recursion/README.md](README.md) and [backtracking.md](../backtracking.md).

---

## Core idea

1. **Make the input smaller** — Each recursive call should move toward a **base case** by a valid decision (include/exclude, move to next index, split left/right).
2. **Recursion = choices + decisions** — At each step you have options; the **recursive tree** (decision tree) shows all paths.
3. **Draw the tree first** — For subsets, permutations, knapsack-style choices, sketching the tree often reveals the recurrence.

---

## IP / OP method (input–output)

- **Input:** What you have left to process (e.g. remaining string, index `i`, remaining budget).
- **Output:** What you are building (current path, current sum, current string).
- Each branch: choose an action → new IP (smaller) → recurse → optionally **undo** (backtracking).

---

## Base case and induction

- **Base case:** Smallest valid input where the answer is trivial (empty string, `i == n`, weight 0).
- **Hypothesis:** Assume recursive calls return the correct answer for smaller inputs.
- **Induction:** Combine children results to build the answer for the current node.

---

## From recursion to DP

When the same **(state)** is reached on different paths → **overlapping subproblems** → add **memoization** (top-down) or **tabulation** (bottom-up). See [dynamic-programming/README.md](../dynamic-programming/README.md).

---

## Interview Questions — Logic & Trickiness (recursive style)

| Question | Core logic | Trickiness |
|----------|------------|------------|
| **All Subsets** | Include/exclude each index; recurse | Bitmask vs recursion depth |
| **Permutations** | Swap or used[] | Duplicate elements — skip same branch |
| **Tower of Hanoi** | Move n-1, move base, move n-1 | Classic induction |
| **N-Queens** | Row recursion + validity | Diagonal encoding |
| **Generate Parentheses** | Open/close count | Prune when `close > open` |

---

## See also

- [recursion/README.md](README.md) — formal template and complexity  
- [dp-aditya-verma.md](../dynamic-programming/dp-aditya-verma.md) — knapsack and choice diagram  
- [patterns/dp-advanced.md](../../../patterns/dp-advanced.md)
