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

| Question | Core logic | Trickiness & details |
|----------|------------|----------------------|
| **All Subsets** | At index `i`: branch **include** `nums[Problem Details](../../../google-sde2/PROBLEM_DETAILS.md#subsets-ii)** needs sort + skip duplicates on exclude branch. |
| **[Problem Details](../../../google-sde2/PROBLEM_DETAILS.md#permutations)** | Swap-based or `used[]` boolean; **depth** = n. | **Duplicate** array: sort + `if (i>0 && nums[i]==nums[i-1] && !used[i-1])` skip. |
| **Tower of Hanoi** | `move(n, src, aux, dst)` = move `n-1` src→aux, move disk n src→dst, move `n-1` aux→dst. | **Induction** proof; **2^n-1** moves optimal. |
| **Josephus / elimination games** | Recursive `f(n,k) = (f(n-1,k)+k) % n` with base; iterative from 0. | **0-based** vs **1-based** index; **k** step size. |
| **N-Queens** | Place one queen per row; recurse column choice; check `col` and diagonals. | **Bitmasks** `cols | diag1 | diag2` for speed; **count** vs **print** one solution. |
| **Generate Parentheses** | Only add `)` when `close < open`; stop when `open==close==n`. | **IP/OP style:** `open` count = output so far, `close` count; **invalid** if `close` exceeds `open`. |
| **Binary Tree Paths** | DFS: path string + `->`; on leaf append to result. | **Leaf** = node with no children; **value** to string. |
| **Expression evaluation** | Operators + recursion on **subexpr**; or two-stack **Shunting-yard** (iterative). | **Recursion** matches nested parentheses naturally. |

---

## See also

- [recursion/README.md](README.md) — formal template and complexity  
- [dp-aditya-verma.md](../dynamic-programming/dp-aditya-verma.md) — knapsack and choice diagram  
- [Patterns Master](../../../../reference/patterns/patterns-master.md)
