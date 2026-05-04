# Recursion Questions Bank — Tiered Drill Sheet

60 questions organized by difficulty. Each entry: pattern tag, LC #, hint, key gotcha. For theory see [README.md](README.md) and the pattern files.

---

## How to Use

1. **Before coding:** Name the pattern. State the base case. Write the recurrence.
2. **Time yourself:** Easy: 15 min, Medium: 25 min, Hard: 40 min.
3. **After solving:** Can you convert recursion → memo → tabulation?
4. **Missed one?** Go back to the specific pattern file, not just random LeetCode.

---

## Easy (15 Questions)

| # | Problem | LC # | Pattern | Hint | Key Gotcha |
| :--- | :--- | :--- | :--- | :--- | :--- |
| E1 | **Fibonacci Number** | 509 | Mathematical | `f(n) = f(n-1) + f(n-2)` | `@lru_cache` → O(N); iterative → O(1) space |
| E2 | **Pow(x, n)** | 50 | Mathematical | `half = pow(x, n//2)`; `half*half` or `half*half*x` | Handle `n < 0`: invert x, negate n |
| E3 | **Factorial** | — | Mathematical | `f(n) = n * f(n-1)`; base `f(0)=1` | Python `math.factorial` exists; write from scratch in interview |
| E4 | **Maximum Depth of Binary Tree** | 104 | Tree structural | `1 + max(depth(L), depth(R))`; `None → 0` | Skewed tree hits recursion limit; mention BFS alternative |
| E5 | **Same Tree** | 100 | Tree structural | Both null → True; one null → False; vals match + recurse | Handle null BEFORE comparing values |
| E6 | **Symmetric Tree** | 101 | Tree structural | `mirror(left, right)`: check `left.left ↔ right.right` | Don't compare left with left (that's same subtree check) |
| E7 | **Invert Binary Tree** | 226 | Tree structural | Swap left and right at each node; recurse into children | Works in any order (pre/post); return root |
| E8 | **Merge Two Sorted Lists** | 21 | Structural recursion | Compare heads; recurse on the larger-head side | Base: either list null → return the other |
| E9 | **Reverse Linked List** | 206 | Structural recursion | `head.next.next = head; head.next = None`; return new_head | Stack depth = O(N); iterative is O(1) stack |
| E10 | **Sum of Nested List** | 339 | Structural (nested) | If int: return; if list: recurse into elements | `NestedInteger.getList()` vs `.getInteger()` API |
| E11 | **Tower of Hanoi** | — | Mathematical | Move n-1 to aux, disk n to dst, n-1 to dst | Exactly `2^N - 1` moves; cannot improve |
| E12 | **Binary Search (recursive)** | 704 | D&C | `mid = (lo+hi)//2`; recurse on left or right half | Base: `lo > hi → -1`; avoid integer overflow |
| E13 | **Path Sum I** | 112 | Tree structural | Reduce `target - node.val` each level; True at leaf if 0 | Leaf: `not left AND not right` |
| E14 | **Count Nodes in BST** | 222 | Tree structural | Perfect subtree shortcut: `2^h - 1` | Check lh==rh first for O(log² N) |
| E15 | **GCD (Euclidean)** | — | Mathematical | `gcd(a, b) = gcd(b, a % b)`; base `gcd(a, 0) = a` | `gcd(0, b) = b` — don't swap args carelessly |

---

## Medium (30 Questions)

| # | Problem | LC # | Pattern | Hint | Key Gotcha |
| :--- | :--- | :--- | :--- | :--- | :--- |
| M1 | **Subsets** | 78 | Include/Exclude | Record `current[:]` at every node | Snapshot `[:]` not reference |
| M2 | **Subsets II** | 90 | Include/Exclude | Sort + `if j>start and nums[j]==nums[j-1]: continue` | `j > start` (not `j > 0`) |
| M3 | **Permutations** | 46 | Permutations | `used[]` array; depth = n when all placed | Swap-based: restore swap on return |
| M4 | **Permutations II** | 47 | Permutations | Sort + `not used[i-1]` guard | `not used[i-1]` prevents same-level duplicates |
| M5 | **Combinations** | 77 | Combinations | `start` index; prune loop end | `n - (k-len(cur)) + 2` as loop bound |
| M6 | **Combination Sum I** | 39 | Combinations | Recurse with same `i` (reuse); sort + break | `break` (not `continue`) when too large |
| M7 | **Combination Sum II** | 40 | Combinations | Recurse `i+1`; skip `candidates[i]==candidates[i-1]` when `i>start` | `i > start` distinguishes same-level vs different-level |
| M8 | **Combination Sum III** | 216 | Combinations | Both `len==k` AND `remaining==0` at base | Range is 1..9 only |
| M9 | **Generate Parentheses** | 22 | IP/OP | `open < n → add '('`; `close < open → add ')'` | Count = Catalan(n); no need to filter invalid strings |
| M10 | **Letter Combinations Phone** | 17 | IP/OP | Map digit → chars; branch on each char | Empty input → `[]` not `['']` |
| M11 | **Palindrome Partitioning** | 131 | IP/OP | Try all end positions; add if palindrome | Precompute `is_pal[i][j]` for O(1) check |
| M12 | **Letter Case Permutation** | 784 | IP/OP | Branch: lower always; upper only if alpha | Join list at base; use char list not string |
| M13 | **Word Break** | 139 | Memoized | `solve(i)` = can segment `s[i:]`; try all prefix lengths | Pass `frozenset` to `@lru_cache` |
| M14 | **Decode Ways** | 91 | Memoized | 1-digit + 2-digit branches | `'0'` alone invalid; `'06'` invalid |
| M15 | **Coin Change (min)** | 322 | Memoized → DP | `solve(rem) = 1 + min(solve(rem-c) for c in coins)` | Init `inf`; return `-1` if still `inf` |
| M16 | **House Robber III** | 337 | Tree DP | `dfs → (rob, skip)` tuple | Return pair; don't prematurely take max |
| M17 | **Validate BST** | 98 | BST structural | Pass `(lo, hi)` range down | Don't just check immediate parent — check ancestry |
| M18 | **LCA General Tree** | 236 | Tree structural | Both non-null returns → current node is LCA | `root==p or root==q → return root` immediately |
| M19 | **LCA BST** | 235 | BST structural | Both < root → go left; both > root → go right | Divergence point = LCA |
| M20 | **Path Sum II** | 113 | Tree backtrack | Backtrack: `path.pop()` after each recursive call | Snapshot `path[:]` before appending |
| M21 | **Flatten Binary Tree** | 114 | Tree structural | Connect left tail to right; move left → right | Return rightmost tail of flattened subtree |
| M22 | **Unique BSTs II** | 95 | D&C | For each root, left = solve(lo,root-1), right = solve(root+1,hi) | Empty range returns `[None]` not `[]` |
| M23 | **Different Ways to Parenthesize** | 241 | D&C + memo | Split at each operator; cartesian product | `@lru_cache` on string slice |
| M24 | **Kth Smallest in BST** | 230 | BST inorder | Inorder = sorted; count steps | Short-circuit once k reached |
| M25 | **Number of Islands** | 200 | Graph DFS | Sink visited cells to `'#'`; count DFS starts | 4-directional; restore if needed |
| M26 | **Clone Graph** | 133 | Graph DFS | Register clone before recursing into neighbors | Use original node as dict key |
| M27 | **Course Schedule** | 207 | Graph cycle detect | 3-color: 0=white, 1=gray, 2=black | Gray neighbor = back edge = cycle |
| M28 | **Josephus Problem** | — | Mathematical | `f(n,k) = (f(n-1,k) + k) % n`; base `f(1,k)=0` | Answer is 0-based; add 1 for 1-based |
| M29 | **Pow(x, n) full** | 50 | Mathematical | `half = pow(x, n//2)^2`; odd n → multiply once more | `n < 0`: invert x and negate n |
| M30 | **Merge Sort** | — | D&C | Split at mid; merge two sorted halves | Python slice `arr[:mid]` creates new list — O(N) space |

---

## Hard (15 Questions)

| # | Problem | LC # | Pattern | Hint | Key Gotcha |
| :--- | :--- | :--- | :--- | :--- | :--- |
| H1 | **N-Queens** | 51 | Constraint backtrack | `cols, diag1(r-c), diag2(r+c)` sets | Anti-diagonal key is `r+c`, not `r-c` |
| H2 | **N-Queens II (count)** | 52 | Constraint backtrack | Bitmask version: `avail = ~(cols|diag1|diag2)` | Bitmask ~3x faster; iterate with `bit = avail & -avail` |
| H3 | **Sudoku Solver** | 37 | Constraint backtrack | Try 1–9 at each empty cell; backtrack on conflict | Box index = `(r//3)*3 + c//3` |
| H4 | **Word Search II** | 212 | Trie + DFS backtrack | Build Trie from words; DFS from each cell | Prune by removing words found (set `end_of_word=False`) |
| H5 | **Regular Expression Matching** | 10 | Memoized recursion | `*` = zero-or-more of PRECEDING; `dp(i, j+2)` for zero-occur | Base: `j==len(p) → i==len(s)` |
| H6 | **Wildcard Matching** | 44 | Memoized recursion | `*` standalone: `dp(i+1,j)` or `dp(i,j+1)` | Base: remaining pattern must all be `*` |
| H7 | **Serialize/Deserialize Binary Tree** | 297 | Tree structural | Preorder + `'#'` sentinel; `iter()` for stateful consumption | Each recursive `build()` consumes exactly one token |
| H8 | **Expression Add Operators** | 282 | String backtrack | Track `prev` for multiplication undo | Leading zeros: `break` not `continue` |
| H9 | **Remove Invalid Parentheses** | 301 | String backtrack | Count min removals first; use set to deduplicate | Track both open and close removals separately |
| H10 | **Decode String** | 394 | Recursive descent | `[` = recurse; `]` = return; return `(result, new_index)` | Handle multi-digit k; skip `[` and `]` |
| H11 | **Scramble String** | 87 | D&C + memo | Try all split sizes; swap and no-swap variants | `sorted(a)!=sorted(b)` prunes most branches |
| H12 | **Max Path Sum (Binary Tree)** | 124 | Tree DP | `gain(node)` returns best single arm; clip negatives | Path through node = `node.val + left + right` |
| H13 | **Course Schedule II (order)** | 210 | Graph topo sort | Add to order AFTER all descendants (postorder) | Reverse at end; empty if cycle detected |
| H14 | **Largest BST Subtree** | 333 | Tree DP (tuple) | Return `(is_bst, size, min, max)` from each node | Empty subtree: `is_bst=True, size=0, min=inf, max=-inf` |
| H15 | **Combination Sum IV (order matters)** | 377 | Memoized → DP | `dp(rem) = sum(dp(rem-n) for n in nums)` | Amount outer loop → counts permutations (ordered combos) |

---

## Pattern Quick-Reference Index

| Pattern | Easy | Medium | Hard |
| :--- | :--- | :--- | :--- |
| **Mathematical recursion** | E1, E2, E3, E11, E15 | M28, M29 | — |
| **Tree structural** | E4, E5, E6, E7, E8, E9, E13, E14 | M16, M17, M18, M19, M20, M21, M22, M24 | H7, H12, H14 |
| **Graph DFS** | — | M25, M26, M27 | H13 |
| **Include/Exclude (Subsets)** | — | M1, M2 | — |
| **Permutations** | — | M3, M4 | — |
| **Combinations** | — | M5, M6, M7, M8 | H15 |
| **IP/OP string** | — | M9, M10, M11, M12 | — |
| **Memoized recursion** | — | M13, M14, M15 | H5, H6 |
| **D&C** | E12 | M23, M30 | H11 |
| **Constraint backtracking** | — | — | H1, H2, H3, H4 |
| **String recursion** | — | — | H8, H9, H10 |
| **Recursion → DP** | E1 | M13, M14, M15 | H15 |

---

## Drill Schedules

### 1-Week Blitz (Interview in 7 days)

| Day | Focus | Questions |
| :--- | :--- | :--- |
| 1 | Tree structural | E4–E9, E13, M16, M17, M18 |
| 2 | Subsets + Permutations | M1–M4, E11 |
| 3 | Combinations + IP/OP | M5–M12 |
| 4 | Memoized + Recursion→DP | M13, M14, M15, E1, M29 |
| 5 | Graph recursion | M25, M26, M27, H13 |
| 6 | Hard constraint backtrack | H1, H2, H3, H4 |
| 7 | Hard review | H5, H6, H7, H8, H12 |

### 2-Day Emergency Revision

| Session | Questions | Time |
| :--- | :--- | :--- |
| AM | E4, E5, M1, M3, M6, M9, M13, M17 | 90 min |
| PM | M25, M27, H1, H5, H7, H12 | 90 min |

---

## See also

- [README.md](README.md) — Theory and mental models
- [aditya-verma.md](aditya-verma.md) — Full pattern playbook with code
- [recursion-to-dp.md](recursion-to-dp.md) — Recursion → DP bridge (8 problems)
- [tree-recursion.md](tree-recursion.md) | [graph-recursion.md](graph-recursion.md) | [combination-problems.md](combination-problems.md) | [string-recursion.md](string-recursion.md)
- [tips-and-gotchas.md](tips-and-gotchas.md) — Master cheatsheet
