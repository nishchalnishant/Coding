# Recursion

A problem-solving technique where a function calls itself to solve smaller instances of the same problem.

## Key Concepts
- **Base Case**: The simplest version of the problem where the function stops calling itself. Essential to prevent infinite loops / Stack Overflow.
- **Recursive Step**: The part of the function where it calls itself with a smaller/simpler input, moving towards the base case.
- **Call Stack**: Every recursive call pushes the current state onto the memory stack. Limits maximum depth (usually ~1000 in Python, varies by language).

## Types of Recursion
- **Head/Pre Recursion**: Operations are performed *before* the recursive call.
- **Tail/Post Recursion**: The recursive call is the very last operation. Many compilers can optimize this to use $O(1)$ stack space (Tail Call Optimization).
- **Tree Recursion**: The function makes multiple recursive calls (e.g., Fibonacci, Tree DFS). Time complexity is typically exponential unless memoized.

## Optimizations & Variations
- **Memoization**: Cache results of expensive recursive calls to avoid redundant work (Top-Down Dynamic Programming).
- **Backtracking**: A form of recursion that builds a solution incrementally and abandons a path ("backtracks") as soon as it determines the path cannot lead to a valid solution.

## Common SDE-2 Recursion Problems
- *Easy*: Fibonacci Number, Factorial, Reverse Linked List, Same Tree.
- *Medium*: Subsets, Permutations, Combinations, Validate Binary Search Tree.
- *Hard*: Serialize and Deserialize Binary Tree, Word Search II, Regular Expression Matching.

---

## Pattern Recognition

- **Tree / list structure** → Natural recursion (process node, recurse on children or next). Base case: null/empty.
- **Choices at each step** → Backtracking (make choice, recurse, undo). See [backtracking.md](../backtracking.md).
- **Overlapping subproblems** → Add memoization → top-down DP. See [dynamic-programming/README.md](../dynamic-programming/README.md).
- **Tail recursion** → Can be converted to iterative loop (same O(1) space if TCO; otherwise iterative is safer for depth).

## Interview Strategy

- **Identify**: "Process tree/list" → recursion. "Generate all" / "find one valid" → backtracking. "Optimal + overlapping" → memo/DP.
- **Approach**: Define base case first, then recursive step (smaller input). State time/space; mention stack depth limit. If converting to iterative, use explicit stack for tree.
- **Common mistakes**: Missing base case; not making input strictly smaller (infinite recursion); forgetting to undo in backtracking.

## Quick Revision

- **Base case**: Must be reached; typically empty list, null node, or n=0/1. **Recursive step**: Call with smaller n or child/next.
- **Memoization**: Cache by (state) before returning; check cache at start. **Backtracking**: path.append(x); recurse; path.pop().
- **Space**: O(depth) for call stack. Tree DFS: O(h). List: O(n). Consider iterative + explicit stack if depth large.

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness & details |
|----------|------------|----------------------|
| **Reverse Linked List** | `reverse(head)` = `reverse(head.next)` then `head.next.next = head; head.next = null`. | **O(n)** stack space; **cycle** breaks; **tail** becomes new head. |
| **Same Tree** | Match `p.val == q.val` and recurse `left`, `right`; both null → true; one null → false. | **Structure** and **value**; **iterative** queue alternative. |
| **Maximum Depth of Binary Tree** | `1 + max(depth(left), depth(right))`; empty → 0. | **Stack depth** on skewed tree O(n). |
| **Fibonacci** | Naive `fib(n)=fib(n-1)+fib(n-2)` is **O(2^n)**; **memo** or **iterative** O(n). | **Mod** 10^9+7; **matrix** exp log n for huge n. |
| **Pow(x, n)** | `n%2==0` → `pow(x*x, n//2)` else `x * pow(x, n-1)`; handle negative `n`. | **INT_MIN** negation; **double** vs int. |
| **Generate Parentheses** | Recurse `open` used, `close` used; add `(` if `open<n`; add `)` if `close<open`. | **Valid** prefix: `close ≤ open` always; **count** only vs **list all**. |
| **Merge Two Sorted Lists** | Recursive: smaller head = `merge(head.next, other)`; **iterative** often preferred. | **O(n)** stack vs O(1) iterative. |
| **Flatten Multilevel Doubly Linked List** | DFS: next then child; **rewire** child’s tail to next. | **Null** child; **in-place** pointer surgery. |

---

## See also

- [aditya-verma.md](aditya-verma.md) — IP/OP and decision-tree style  
- [Backtracking](../backtracking.md) — template with undo; recursion with choices  
- [Dynamic Programming](../dynamic-programming/README.md) — memoization from recursion  
- [Tree](../../data-structures/tree.md) — recursive structure
