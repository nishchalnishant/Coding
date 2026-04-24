# Recursion — Aditya Verma Style (Supplement)

Structured way to think about **recursion as decisions + smaller input**. Use alongside [recursion/README.md](README.md) and [backtracking.md](../backtracking.md).

---

## 1. Core Principles

### The Click Moment
> [!IMPORTANT]
> **The Click Moment**: "Input-Output (IP/OP) thinking" — OR — "Smaller subproblems" — OR — "Decision Tree visualization".
- **Smaller input**: Each call reduces the problem space (n-1, i+1, s[1:]).
- **Decision Tree**: Every recursive branch is a path in a tree. Sketching this is 90% of the solution.

---

## 2. IP / OP Method (Input–Output)

- **Input:** What you have left to process (e.g. remaining string, index `i`, remaining budget).
- **Output:** What you are building (current path, current sum, current string).
- Each branch: choose an action → new IP (smaller) → recurse → optionally **undo** (backtracking).

---

## 3. Base Case and Induction

- **Base case:** Smallest valid input where the answer is trivial (empty string, `i == n`, weight 0).
- **Hypothesis:** Assume recursive calls return the correct answer for smaller inputs.
- **Induction:** Combine children results to build the answer for the current node.

---

## 4. From Recursion to DP

When the same **(state)** is reached on different paths → **overlapping subproblems** → add **memoization** (top-down) or **tabulation** (bottom-up). See [dynamic-programming/README.md](../dynamic-programming/README.md).

---

## 5. Interview Questions — Logic & Trickiness (recursive style)

| Question | Core logic | Trickiness & details |
|----------|------------|----------------------|
| **All Subsets** | At index `i`: branch **include** `nums[i]` or **exclude**. | **[Subsets II](../../../google-sde2/PROBLEM_DETAILS.md#subsets-ii)** needs sort + skip duplicates on exclude branch. |
| **[Permutations](../../../google-sde2/PROBLEM_DETAILS.md#permutations)** | Swap-based or `used[]` boolean; **depth** = n. | **Duplicate** array: sort + `if (i>0 && nums[i]==nums[i-1] && !used[i-1])` skip. |
| **Tower of Hanoi** | `move(n, src, aux, dst)` = move `n-1` src→aux, move disk n src→dst, move `n-1` aux→dst. | **Induction** proof; **2^n-1** moves optimal. |
| **Josephus Game** | Recursive `f(n,k) = (f(n-1,k)+k) % n` with base; iterative from 0. | **0-based** vs **1-based** index; **k** step size. |
| **N-Queens** | Place one queen per row; recurse column choice; check `col` and diagonals. | **Bitmasks** `cols | diag1 | diag2` for speed; **count** vs **print** one solution. |
| **Generate Parentheses** | Only add `)` when `close < open`; stop when `open==close==n`. | **IP/OP style:** `open` count = output so far, `close` count; **invalid** if `close` exceeds `open`. |
| **Binary Tree Paths** | DFS: path string + `->`; on leaf append to result. | **Leaf** = node with no children; **value** to string. |
| **Expression evaluation** | Operators + recursion on **subexpr**; or two-stack **Shunting-yard** (iterative). | **Recursion** matches nested parentheses naturally. |

---

## See also

- [recursion/README.md](README.md) — formal template and complexity  
- [dp-aditya-verma.md](../dynamic-programming/dp-aditya-verma.md) — knapsack and choice diagram  
- [Patterns Master](../../../../reference/patterns/patterns-master.md)
