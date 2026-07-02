---
tags: [l3-google, meta, edge-cases]
topic: Edge Case Taxonomy
---

# Edge Case Taxonomy — Google L3

A systematic catalogue of edge cases by data type. Verbalize these during the *Clarify* phase (first 3–5 min of the interview). Missing an edge case costs you more than a sub-optimal complexity.

---

## Universal Edge Cases (check for every problem)

| Edge case | Why it matters |
|-----------|---------------|
| Empty input (`[]`, `""`, `None`) | Base case usually returns 0, `""`, or `False` — easy to forget |
| Single element | Often collapses the algorithm; two-pointer, sliding window, binary search all need this |
| All elements identical | Hash collision, dedup logic, monotonic stack triviality |
| Maximum constraints (n = 10⁵, values = 10⁹) | Overflow in Python? No. C++/Java? Yes. |
| Negative numbers | Breaks sliding window (can't shrink freely), Dijkstra, modular arithmetic |
| Zero | Division by zero, prefix product exception, BFS source |

---

## By Data Type

### Arrays

| Edge case | Example | Common bug |
|-----------|---------|-----------|
| Length-1 array | `[5]` | Two-pointer: `left == right`, don't enter loop |
| All same value | `[3,3,3]` | Dedup logic skips everything |
| Already sorted / reverse sorted | `[1,2,3]`, `[3,2,1]` | Quicksort worst case; binary search trivial |
| Contains duplicates | `[1,2,2,3]` | Hash set vs multiset; dedup in backtracking |
| Negative + positive mix | `[-1, 0, 1]` | Three-sum, product sign, sliding window |
| Subarray spanning full array | `[1..n]` | Prefix sum `seen={0:1}` — the zero anchor |
| Subarray of length 0 | Empty prefix | Sliding window: window size can shrink to 0 |

### Strings

| Edge case | Example | Common bug |
|-----------|---------|-----------|
| Empty string | `""` | Return 0 or `""` |
| Single character | `"a"` | Palindrome = True; no window to slide |
| All same character | `"aaaa"` | KMP/Z-array all 1s; longest substring = full |
| Unicode / non-ASCII | `"héllo"` | Python handles it; clarify in interview |
| Case sensitivity | `"Abc"` vs `"abc"` | Clarify; usually `.lower()` |
| Whitespace in string | `"hello world"` | Split, strip, or treat space as character? |
| String with only delimiters | `"   "` | After split → empty list |

### Linked Lists

| Edge case | Example | Common bug |
|-----------|---------|-----------|
| `None` head | Empty list | Check `if not head` before accessing `.next` |
| Single node | `1 → None` | Reverse = same; remove = None |
| Two nodes | `1 → 2 → None` | Slow/fast pointer: fast reaches None in 1 step |
| Cycle present | List loops back | Need `slow/fast` cycle detection before traversal |
| k ≥ length (remove kth from end) | k = 5, length = 3 | dummy head + offset trick handles gracefully |
| Palindrome check | `1→2→2→1` | Reverse second half, compare, restore |

### Trees

| Edge case | Example | Common bug |
|-----------|---------|-----------|
| `None` root | Empty tree | Return 0, `[]`, `False` |
| Single node | Just root | Height = 0 or 1 (clarify definition) |
| Left-skewed / right-skewed | All left children | O(n) height; DFS stack overflow for n=10⁵ |
| All same values | `[1,1,1,1]` | BST validation fails (equal values: clarify <, ≤) |
| Path going through root | LCA, max path sum | Don't restrict to root-to-leaf |
| Root = answer | Max depth = 0 if root is `None`, 1 if single node | Off-by-one on height definition |

### Graphs

| Edge case | Example | Common bug |
|-----------|---------|-----------|
| No edges | n nodes, 0 edges | Each node is its own component |
| Disconnected graph | Islands not reachable | BFS/DFS from all unvisited nodes |
| Self-loop | Edge `(u, u)` | Cycle detection: don't traverse back to same node |
| Duplicate edges | `(1,2)` appears twice | Deduplicate adjacency list, or it skews degree counts |
| Node 0 vs node 1 indexed | Input is 1-indexed | Adjust `n+1` array size or subtract 1 |
| Grid as implicit graph | Walls block traversal | Check bounds AND `grid[r][c] != '#'` before enqueue |

### Binary Search

| Edge case | Example | Common bug |
|-----------|---------|-----------|
| Empty array | `[]` | Return -1 or left bound |
| Single element | `[5]`, target = 5 | Works; target ≠ 5 → -1 |
| Target not in array | `[1,3,5]`, target = 2 | Return -1 or lower_bound |
| All elements satisfy predicate | Feasibility search | `lo` ends up at 0 or `hi+1` |
| Integer overflow in mid | `lo + hi` in C++ | Use `lo + (hi - lo) // 2`; Python is safe |
| Off-by-one in boundary | `while lo < hi` vs `<= hi` | Know your invariant before coding |

### Dynamic Programming

| Edge case | Example | Common bug |
|-----------|---------|-----------|
| `n = 0` | Coin change, climb stairs | `dp[0] = 1` (empty set = 1 way) |
| Target = 0 | Coin change with amount 0 | Return 0 (no coins needed) |
| No valid solution | Coin change impossible | Return -1, not 0; initialize `dp` to `inf` |
| Single row/column in 2D DP | Shortest path in 1-row grid | Only one direction to go |
| Palindrome length 1 | LPS, palindrome partition | Every single char is a palindrome |
| Identical subsequences | LCS with duplicates | Still count all occurrences |

---

## Off-by-One Patterns

These are the most common source of wrong answers even when the algorithm is correct.

| Pattern | Correct | Common mistake |
|---------|---------|----------------|
| Binary search `mid` | `lo + (hi - lo) // 2` | `(lo + hi) // 2` (overflow in some languages) |
| Binary search boundary | `while lo <= hi` (exact search) | Using `<` causes missing the target |
| Sliding window size | `r - l + 1 == k` | `r - l == k` (off by one) |
| Prefix sum index | `prefix[i+1] = prefix[i] + arr[i]` | Starting prefix at index 0 and miscounting |
| Kth element | `k-1` index in sorted array | 1-indexed k → need `k-1` for 0-indexed |
| Tree height | Leaf node height = 0 or 1? | Clarify: depth (root=0) vs height (leaf=0) |
| DFS visited marking | Mark before enqueue (BFS) | Marking after dequeue causes duplicates in BFS |

---

## Interview Communication Template

When you spot an edge case during clarification:

> "Before I start coding, I want to confirm a few edge cases:
> - Can the input be empty? I'll return X.
> - Can there be duplicates? Should the output also deduplicate?
> - Any constraint on values — can they be negative?
> - For this problem, I'll assume [your assumption] — is that correct?"

During coding, call out edge case handling verbally:
> "Here I'm checking `if not head` first because the empty list would otherwise crash `.next` access."

---

## See Also

- Constraint → complexity mapping: [`02-constraint-analysis-heuristic.md`](02-constraint-analysis-heuristic.md)
- Complexity analysis: [`05-complexity-analysis.md`](05-complexity-analysis.md)
- 45-min execution plan: [`01-45-minute-execution-plan.md`](01-45-minute-execution-plan.md)
