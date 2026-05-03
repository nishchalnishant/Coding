# Recursion — SDE-3 Gold Standard

A function that calls itself on a reduced subproblem. SDE-3 focus: recognizing which recursion type applies, converting to iterative for stack safety, the memoization path to top-down DP, and parallel fork-join recursion.

---

## Theory & Mental Models

**What it is.** Recursion is a function that calls itself on a strictly smaller instance of the same problem. Core invariant: (1) a base case handles the smallest solvable instance directly, (2) each recursive call makes progress toward the base case, (3) the result combines the base value with recursive sub-results.

**Why it exists.** Many problems have self-similar structure — trees, nested subproblems, combinatorial generation. Recursion directly expresses this structure. Every recursive solution has an equivalent iterative one (using an explicit stack), but the recursive form is often far more readable and derivable.

**The mental model.** Trust the recursive call: assume `f(subproblem)` correctly solves the subproblem, then write only the logic that combines it with the current node/choice. Your job is not to trace the recursion — it's to define the base case, ensure progress, and combine correctly.

**Complexity at a glance.**

| Recurrence | Expanded Form | Result |
| :--- | :--- | :--- |
| T(n) = T(n-1) + O(1) | Linear chain | O(N) |
| T(n) = 2T(n-1) + O(1) | Binary branching without pruning | O(2^N) |
| T(n) = T(n/2) + O(1) | Halving each level | O(log N) |
| T(n) = 2T(n/2) + O(N) | Merge sort | O(N log N) |
| T(n) = T(n-1) + T(n-2) + O(1) | Fibonacci (naive) | O(2^N); O(N) with memo |

**When to reach for it.**
- Tree or graph traversal — the recursive structure matches the data structure.
- Divide-and-conquer — independent halves.
- Generating all combinations / permutations — backtracking with choose/unchoose.
- Problems with self-similar structure: nested lists, fractal patterns, expression parsing.

**When NOT to use it.**
- Depth > 10^4 in Python — default recursion limit is 1000 (`sys.setrecursionlimit`); convert to iterative + explicit stack.
- Overlapping subproblems without memoization — exponential blowup; add `@lru_cache` or rewrite as DP.
- Tail recursion for performance — Python does not optimize tail calls; unroll to a loop.

**Common mistakes.**
- Missing base case — infinite recursion and stack overflow.
- Not making progress toward the base case — each call must reduce the problem size.
- Python's default recursion limit is 1000 — mention `sys.setrecursionlimit` and the iterative alternative in interviews.
- Mutable default arguments persist across calls — never use `def f(path=[])`, use `def f(path=None)` and initialize inside.

---

## 1. Recursion Types & Click Moments

> [!IMPORTANT]
> **The Click Moment**: "**Process a tree / list** node" → structural recursion (base: null/empty). "**Generate all** combinations/permutations" → backtracking (make choice, recurse, undo). "**Overlapping subproblems**" → add `@lru_cache` → top-down DP. "**Divide** into independent halves" → divide-and-conquer. Match the type first; write the base case before the recursive step.

| Type | Pattern | Key Signature |
| :--- | :--- | :--- |
| **Structural** | Tree/list traversal | `f(node) = combine(node.val, f(node.left), f(node.right))` |
| **Backtracking** | Generate all valid paths | `f(state) → add, recurse, undo` |
| **Memoized** | Overlapping subproblems | `cache.get(key) or (compute; cache[key] = result; return)` |
| **D&C** | Independent halves | `f(lo, hi) = merge(f(lo, mid), f(mid+1, hi))` |
| **Tail** | Accumulator pattern | `f(n, acc) = f(n-1, acc + n)` → unrollable to iterative loop |

---

## 2. Core Patterns & Click Moments

### Structural Recursion — Trees and Lists

> [!IMPORTANT]
> **The Click Moment**: "Process a **tree** node in terms of its children" — OR — "process a **linked list** node in terms of the rest". Result at node N depends only on N's value and the recursive results from its children. Base case: null/empty node returns a neutral value (0, None, True, False, etc.).

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class TreeNode:
    val: int
    left: Optional['TreeNode'] = None
    right: Optional['TreeNode'] = None

def max_depth(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

def reverse_list(head):
    if head is None or head.next is None:
        return head
    new_head = reverse_list(head.next)
    head.next.next = head  # reverse pointer
    head.next = None       # cut old forward link
    return new_head
```

> [!CAUTION]
> **Python recursion limit**: Default is 1000 frames. A skewed tree with 10,000 nodes will crash with `RecursionError`. Use `sys.setrecursionlimit(50000)` as a stopgap, or — better — convert to **iterative with an explicit stack**. Always mention this trade-off in interviews when the input can be large.

---

### Memoized Recursion — Path to Top-Down DP

> [!IMPORTANT]
> **The Click Moment**: "The recursive call tree has **repeated subproblems**" — same arguments appear in multiple branches. Add `@lru_cache` or a manual `cache` dict. This converts exponential recursion to polynomial. Memoized recursion and top-down DP are the same pattern — interviewers may ask you to convert one to the other.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

@lru_cache(maxsize=None)
def word_break(s: str, word_set: frozenset) -> bool:
    if not s:
        return True
    return any(
        s[:i] in word_set and word_break(s[i:], word_set)
        for i in range(1, len(s) + 1)
    )
```

> [!TIP]
> **`frozenset` as a cache key**: `@lru_cache` requires hashable arguments. Convert `list → tuple`, `set → frozenset`, `dict → tuple(sorted(d.items()))` before passing to a memoized function. Alternatively, use a manual `dict` cache with string or tuple keys and manage it explicitly.

---

### Iterative Recursion — Explicit Stack Conversion

> [!IMPORTANT]
> **The Click Moment**: "Tree DFS with potentially large depth (skewed tree)" — OR — "Python recursion depth limit will be hit". Replace the call stack with an explicit Python list used as a stack. For postorder (need both children before processing parent): push `(node, visited)` flag pairs; process the node on the second visit.

```python
from typing import Optional

def inorder_iterative(root: Optional[TreeNode]) -> list[int]:
    result = []
    stack = []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result

def postorder_iterative(root: Optional[TreeNode]) -> list[int]:
    if not root:
        return []
    result = []
    stack = [(root, False)]
    while stack:
        node, processed = stack.pop()
        if processed:
            result.append(node.val)
        else:
            stack.append((node, True))      # revisit after both children done
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))
    return result
```

---

### Constrained Generation — Generate Parentheses

```python
def generate_parentheses(n: int) -> list[str]:
    result = []

    def backtrack(s: str, open_count: int, close_count: int) -> None:
        if len(s) == 2 * n:
            result.append(s)
            return
        if open_count < n:
            backtrack(s + '(', open_count + 1, close_count)
        if close_count < open_count:
            backtrack(s + ')', open_count, close_count + 1)

    backtrack('', 0, 0)
    return result
```

> [!TIP]
> **Invariant**: `close_count ≤ open_count` always. This single constraint prunes all invalid prefixes without validating the full string. Recognizing this invariant is the difference between O(2^(2N)) brute force and the Catalan-bounded O(4^N / √N) solution.

---

## 3. SDE-3 Deep Dives

### Scalability: Tail Call Optimization (TCO)

> [!TIP]
> A **tail-recursive** function's last operation is the recursive call — the current stack frame is immediately reusable. Languages with TCO (Scheme, Scala, Haskell, some C++ compilers with `-O2`) optimize this to O(1) stack space. **Python and Java do not perform TCO** — tail-recursive Python still uses O(N) stack. To get O(1) space in Python, manually unroll to an iterative loop. Mention this when an interviewer asks why you prefer iterative over recursive for list/tree problems.

### Scalability: Parallel Recursion — Fork-Join

> [!TIP]
> When recursive subproblems are independent (divide-and-conquer), they can run in parallel. Java's `ForkJoinPool` + `RecursiveTask` implements this with **work stealing** — idle threads steal tasks from busy threads' queues. Switch to sequential when problem size drops below a threshold (typically 1,000–10,000 elements) to amortize thread overhead. Python: use `concurrent.futures.ProcessPoolExecutor` (bypasses GIL for CPU-bound work); `ThreadPoolExecutor` is GIL-limited for pure Python recursion.

### Concurrency: Thread-Safe Memoization

> [!TIP]
> `functools.lru_cache` is **not thread-safe** in Python — concurrent cache writes to the same key can cause data races. For multithreaded memoization: protect the cache dict with a `threading.Lock`, or use a `concurrent.futures.Future` per unique key (double-checked locking: if key exists, return cached Future; else create and store the Future before computing, so other threads can wait on it). Java: `ConcurrentHashMap.computeIfAbsent()` is atomic and handles this natively.

### Trade-offs: Recursion vs Iteration

| Dimension | Recursion | Iteration |
| :--- | :--- | :--- |
| Readability | High — matches problem structure | Lower — explicit stack management |
| Stack space | O(depth) — can overflow | O(1) with pointer/index |
| Function call overhead | Higher (frame allocation) | Better cache locality |
| TCO support | Language-dependent | Always O(1) stack |
| Backtracking | Natural — undo on function return | Requires explicit state push/pop |

---

## 4. Common Interview Problems

### Easy
- **Fibonacci** — Memoized: `@lru_cache`; iterative O(1) space: `prev, curr = curr, prev+curr`.
- **Same Tree** — Structural: `p.val == q.val and same(p.left, q.left) and same(p.right, q.right)`.
- **Maximum Depth of Binary Tree** — `1 + max(depth(left), depth(right))`; `None → 0`.

### Medium
- **Generate Parentheses** — Constrained backtracking; `close < open` invariant.
- **Word Break** — Memoized on suffix index; `@lru_cache` with `frozenset` for hashable key.
- **Decode Ways** — Memoized on suffix; 1-digit or 2-digit decode choices; handle `'0'` specially.
- **Flatten Multilevel Doubly Linked List** — Recursive: process child, rewire child's tail to next.

### Hard
- **Regular Expression Matching** — Memoized on `(i, j)` indices; `'*'` = zero or more of preceding.
- **Serialize/Deserialize Binary Tree** — Preorder recursion; sentinel `#` for null nodes.
- **Word Search II** — Trie + DFS backtracking; prune with `end_of_word` flag removal.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **Reverse Linked List** | "Structural recursion; rewire on return" | `reverse(head.next)` returns new head; `head.next.next = head; head.next = None` | O(N) stack space — mention iterative O(1) space alternative. New head is always the original tail. |
| **Same Tree** | "Structural equality of two trees" | `p.val == q.val and same(left) and same(right)`; both null → True | One null + one non-null → False — handle **before** val comparison to avoid NullPointerException. |
| **Maximum Depth** | "Height via postorder return value" | `1 + max(depth(left), depth(right))`; `None → 0` | Skewed tree → O(N) depth. Iterative BFS (count levels) avoids stack overflow for large trees. |
| **Fibonacci** | "Overlapping subproblems in tree recursion" | `@lru_cache` reduces O(2^N) to O(N); iterative reduces space to O(1) | Matrix exponentiation gives O(log N) for huge N. Mod 10^9+7 variant: apply mod at each step. |
| **Generate Parentheses** | "Constrained recursive generation" | `open < n → add '('`; `close < open → add ')'`; full string → collect | Invariant `close ≤ open` prunes all invalid prefixes. Total count = Catalan number C(n). |
| **Word Break** | "Memoized recursion on suffix" | `any(s[:i] in word_set and word_break(s[i:], frozenset))` | Pass `frozenset` (hashable) not `set` (unhashable) to `@lru_cache`. Avoid recomputing suffix slices. |
| **Decode Ways** | "1-digit or 2-digit decode choice per step" | `dp(i) = dp(i+1)` if valid 1-digit `+ dp(i+2)` if valid 2-digit | `'0'` cannot stand alone; `'06'` is not `'6'`. Empty suffix returns 1 (one valid decoding). |
| **Regular Expression Matching** | "Pattern match with `'*'` and `'.'`" | `'*'` = zero or more of preceding char; `match(i,j)` branches on `p[j+1] == '*'` | Handle `'.*'` as greedy match-all. Two base cases: `i` exhausted (check remaining pattern), `j` exhausted (True only if `i` also exhausted). |

---

## Quick Revision Triggers

- "Process a tree or linked list node in terms of its children / rest" → structural recursion; base case is null/empty.
- "Generate all combinations / permutations / valid strings" → backtracking recursion; undo state after each recursive call.
- "Recursive call tree has repeated arguments" → memoize with `@lru_cache`; this is top-down DP.
- "Divide into two independent halves and merge results" → divide and conquer; apply Master Theorem for complexity.
- "Recursion depth > ~1000 in Python" → convert to iterative with explicit stack; mention `sys.setrecursionlimit` as stopgap.
- "Last operation is the recursive call (tail recursion)" → Python does not optimize tail calls; unroll to a loop for O(1) stack.
- "Default argument `def f(path=[])` persists across calls" → use `def f(path=None)` and initialize inside the function.

---

## See also

- [Aditya Verma recursion patterns](aditya-verma.md) — IP/OP and decision-tree style for subset/permutation problems
- [Backtracking](../backtracking.md) — recursion with undo; choose / recurse / unchoose template
- [Dynamic Programming](../dynamic-programming/README.md) — memoized recursion → tabulation conversion
- [Tree](../../data-structures/tree.md) — structural recursion on binary trees
- [Divide and Conquer](../divide-and-conquer.md) — independent subproblems; parallel fork-join
