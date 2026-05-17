# Recursion Tips & Gotchas — Master Cheatsheet

Quick-reference for the 15 most common recursion bugs, pattern recognition, and the SDE-3 interview communication framework. For full pattern details see [README.md](README.md).

---

## Part 1 — Pattern Recognition (30-Second Decision)

### Signal → Pattern Map

| Problem Says... | Pattern | Key Code Shape |
| :--- | :--- | :--- |
| "All subsets / power set" | Include/Exclude | `f(i+1, cur+[x])` AND `f(i+1, cur)` |
| "All unique subsets" (duplicates in input) | Include/Exclude + dedup | Sort + `if j > start and nums[j]==nums[j-1]: continue` |
| "All permutations" | Permutations | `used[]` array; loop all unused; `depth==n` base |
| "All unique permutations" | Permutations + dedup | Sort + `not used[i-1]` guard |
| "Choose K of N (order doesn't matter)" | Combinations | `start` index; recurse `i+1` |
| "Sum to target, unlimited reuse" | Combination Sum I | Recurse with same `i`; sort + break |
| "Sum to target, each once, duplicates in input" | Combination Sum II | Recurse `i+1`; `i>start` dedup guard |
| "Build valid string (parens, palindrome)" | IP/OP with validity guard | Guard condition prunes branches |
| "Process tree node via children" | Tree structural | `f(node) = combine(node.val, f(left), f(right))` |
| "Same subproblem called multiple times" | Memoized recursion | `@lru_cache` → top-down DP |
| "Divide into two independent halves, merge" | Divide & Conquer | `f(lo, hi) = merge(f(lo,mid), f(mid+1,hi))` |
| "Traverse graph, mark visited" | Graph DFS | `visited.add(node)` before recursing |
| "Cycle in directed graph" | 3-color DFS | 0=white, 1=gray (in-stack), 2=black |
| "Topological order" | DFS + postorder stack | Add to stack AFTER all descendants |
| "Pattern match with * and ." | Memoized 2D | `dp(i, j)` on string indices |
| "Recursion depth > 1000" | Convert to iterative | Explicit stack; or `sys.setrecursionlimit` |

---

## Part 2 — The 15 Most Common Recursion Bugs

### Bug 1: Missing Snapshot — Reference Instead of Copy

```python
# WRONG: appending reference — all results will be the final (empty) state
result.append(current)        # ❌

# CORRECT: snapshot the current state
result.append(current[:])     # ✅ for lists
result.append(''.join(current))  # ✅ for char lists → string
```

**Affects:** Subsets, Permutations, Path Sum II, any backtracking that builds a list.

---

### Bug 2: Mutable Default Argument

```python
# WRONG: list persists across function calls!
def subsets(nums, current=[]):  # ❌ default [] shared across all calls

# CORRECT: use None and initialize inside
def subsets(nums, current=None):  # ✅
    if current is None:
        current = []
```

---

### Bug 3: Not Snapshotting — Wrong `current` in `@lru_cache`

```python
# WRONG: lists are not hashable — @lru_cache will crash
@lru_cache(maxsize=None)
def solve(i, current):       # ❌ current is a list

# CORRECT: use only hashable args in cached function; pass immutable state
@lru_cache(maxsize=None)
def solve(i, remaining):     # ✅ int is hashable
```

---

### Bug 4: Wrong Duplicate Guard Condition

```python
# WRONG: skips too much — prevents using same value across different levels
if i > 0 and nums[i] == nums[i-1]:
    continue   # ❌ skips even when i-1 was used at a different level

# CORRECT: only skip at the SAME recursive level
if i > start and nums[i] == nums[i-1]:
    continue   # ✅ i > start (not i > 0)
```

**Affects:** Subsets II, Combination Sum II.

---

### Bug 5: Wrong Permutation Duplicate Guard Direction

```python
# WRONG: skipping when previous IS used — allows duplicates
if i > 0 and nums[i] == nums[i-1] and used[i-1]:
    continue   # ❌ keeps duplicate branches

# CORRECT: skip when previous is NOT used (same-level duplicate)
if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
    continue   # ✅ prevents same-level duplicate branches
```

**Affects:** Permutations II.

---

### Bug 6: Forgetting to Restore State (Backtracking)

```python
# WRONG: not undoing state after recursion
def backtrack(node, r, c):
    board[r][c] = '#'
    for dr, dc in dirs:
        backtrack(node.children.get(board[r+dr][c+dc]), r+dr, c+dc)
    # ❌ board[r][c] never restored — permanent mutation

# CORRECT: restore after recursion
def backtrack(r, c, k):
    temp, board[r][c] = board[r][c], '#'
    # ... recurse ...
    board[r][c] = temp   # ✅ restore
```

---

### Bug 7: Combination Sum — Reuse vs No-Reuse

```python
# WRONG for "unlimited reuse": advances to i+1 — no reuse
backtrack(i + 1, remaining - candidates[i], ...)   # ❌

# CORRECT for "unlimited reuse":
backtrack(i, remaining - candidates[i], ...)        # ✅ same i

# CORRECT for "each used once":
backtrack(i + 1, remaining - candidates[i], ...)   # ✅ i+1
```

---

### Bug 8: Python Recursion Depth Limit

```python
# Python default limit is 1000 frames
# SYMPTOM: RecursionError on large inputs (skewed trees, long strings)

# QUICK FIX (risky — can crash interpreter on very deep stacks):
import sys
sys.setrecursionlimit(10**6)

# PROPER FIX: convert to iterative with explicit stack
stack = [root]
while stack:
    node = stack.pop()
    if node.right: stack.append(node.right)
    if node.left:  stack.append(node.left)
    process(node)
```

---

### Bug 9: Regex `*` Zero-Occurrence Case

```python
# WRONG: forgetting that * can mean zero occurrences
if p[j+1] == '*':
    if first_match:
        return dp(i+1, j)    # ❌ only handles one+ occurrences

# CORRECT: handle both cases
if j+1 < len(p) and p[j+1] == '*':
    return (dp(i, j+2)                          # ✅ zero occurrences: skip p[j] and *
            or (first_match and dp(i+1, j)))    # ✅ one+ occurrences
```

---

### Bug 10: BST Validation — Only Checking Immediate Parent

```python
# WRONG: only checks parent-child relationship
def is_valid(node):
    if node.left and node.left.val >= node.val: return False
    if node.right and node.right.val <= node.val: return False
    return is_valid(node.left) and is_valid(node.right)
    # ❌ misses: right subtree element smaller than grandparent

# CORRECT: pass valid range (lo, hi) down
def validate(node, lo, hi):
    if not node: return True
    if not (lo < node.val < hi): return False
    return (validate(node.left, lo, node.val) and
            validate(node.right, node.val, hi))   # ✅
```

---

### Bug 11: Graph DFS — Not Marking Visited Before Recursing

```python
# WRONG: marks visited after recursing — can revisit on cycles
def dfs(node):
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor)
    visited.add(node)   # ❌ too late

# CORRECT: mark before recursing
def dfs(node):
    visited.add(node)   # ✅ mark immediately
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor)
```

---

### Bug 12: Directed Graph Cycle — Wrong Coloring

```python
# WRONG for directed graph: single visited set misses same-node-different-path
visited = set()
def dfs(node):
    visited.add(node)
    for n in graph[node]:
        if n in visited: return True   # ❌ may be false positive

# CORRECT: 3-color scheme
color = [0] * n    # 0=unvisited, 1=in-stack, 2=done
def dfs(node):
    color[node] = 1
    for n in graph[node]:
        if color[n] == 1: return True    # ✅ back edge = cycle
        if color[n] == 0 and dfs(n): return True
    color[node] = 2
    return False
```

---

### Bug 13: Tree LCA — Null Check Order

```python
# WRONG: accessing .val before null check
def lca(root, p, q):
    if root.val == p.val or root.val == q.val:   # ❌ crashes if root is None
        return root
    ...

# CORRECT: null check first
def lca(root, p, q):
    if not root or root == p or root == q:   # ✅ short-circuit on None
        return root
    ...
```

---

### Bug 14: Forgetting to Reset Used[] on Backtrack

```python
# WRONG: never resets used flag
used[i] = True
current.append(nums[i])
solve(current)
current.pop()
# ❌ used[i] stays True — future iterations skip this element

# CORRECT
used[i] = True
current.append(nums[i])
solve(current)
current.pop()
used[i] = False   # ✅ undo
```

---

### Bug 15: Empty Generating Functions — Wrong Base Case

```python
# Generate Parentheses — WRONG: returns [''] for n=0
def gen_parens(n):
    if n == 0: return ['']   # ❌ may cause issues in callers expecting []

# CORRECT: return [] for n=0 (no valid parenthesizations of length 0)
# Better: check n==0 before calling

# Letter Combinations Phone — WRONG:
def letter_combinations(digits):
    # ...
    # Edge case: empty string
    if not digits: return ['']   # ❌ should return []
    if not digits: return []     # ✅
```

---

## Part 3 — Space & Time Complexity Cheatsheet

| Pattern | Time | Space (stack) | Memoized Time |
| :--- | :--- | :--- | :--- |
| Linear chain `f(n-1)` | O(2^N) naive | O(N) | O(N) with memo |
| Binary branch `f(n-1)+f(n-2)` | O(2^N) | O(N) | O(N) |
| Include/Exclude (subsets) | O(2^N × N) | O(N) depth | — |
| Permutations | O(N! × N) | O(N) depth | — |
| Combinations | O(C(N,K) × K) | O(K) depth | — |
| Tree DFS | O(N) | O(H) = O(log N) avg, O(N) worst | — |
| Graph DFS | O(V + E) | O(V) visited | — |
| Memoized `f(i,j)` two strings | O(M×N) | O(M×N) cache | — |
| Divide & Conquer (halving) | O(N log N) | O(log N) | — |
| Backtracking (no pruning) | O(branches^depth) | O(depth) | — |

### Master Theorem Quick Reference

| Recurrence | Result |
| :--- | :--- |
| `T(N) = T(N-1) + O(1)` | O(N) |
| `T(N) = 2T(N-1) + O(1)` | O(2^N) |
| `T(N) = T(N/2) + O(1)` | O(log N) |
| `T(N) = 2T(N/2) + O(N)` | O(N log N) |
| `T(N) = T(N-1) + T(N-2)` | O(2^N) → O(N) with memo |

---

## Part 4 — SDE-3 Interview Communication Framework

```
1. IDENTIFY the pattern (15 seconds)
   "This is a [backtracking / tree DFS / memoized recursion / D&C] problem because..."
   "The subproblem shrinks by [reducing index / going to children / halving]."

2. STATE the base case (30 seconds)
   "Base case: when [index reaches n / node is null / remaining = 0 / length target met]."
   Write it on the board FIRST.

3. DRAW the decision tree (1 minute)
   For small input (n=2 or n=3), sketch 2-3 levels.
   "Each node represents [state]; branches are [choices]."

4. WRITE the recursion (5-10 minutes)
   Match the code to the decision tree.
   "I'm making [choice], recursing, then [undoing the choice on return]."

5. ANALYZE complexity
   "Time: O([branches]^[depth]) = O([result]). Space: O([stack depth])."

6. MEMOIZE if applicable
   "I notice [same i/j arguments recur] — add @lru_cache."
   "This reduces from O(2^N) to O(N²) [or relevant bound]."

7. OFFER iteration alternative
   "For Python on large inputs, I'd convert to iterative with an explicit stack
    to avoid the recursion limit."
```

---

## Part 5 — When NOT to Use Recursion

| Scenario | Better Approach | Reason |
| :--- | :--- | :--- |
| Tail recursion in Python | Iterative loop | Python has no TCO; same O(N) stack |
| Deeply skewed tree (N > 1000) | Iterative + explicit stack | Recursion limit |
| Repeated subproblems without memo | Bottom-up DP | Exponential blowup |
| Simple array iteration | `for` loop | No self-similar structure |
| Greedy problems | Greedy | No need to explore all choices |

---

## Part 6 — 10 Patterns in One Line Each

```
Include/Exclude:  f(i+1, cur+[x]) AND f(i+1, cur); snapshot cur[:] at base
Permutations:     used[] array; loop all, skip used; depth==n base
Combinations:     start index; recurse i+1; prune loop end
Combo Sum Reuse:  recurse same i (not i+1); sort+break when too large
IP/OP String:     validity guard prunes; record at length target
Tree Structural:  base=null; return type = what parent needs
Tree DP:          return tuple (choice_A, choice_B); parent combines
Graph DFS:        mark visited BEFORE recursing; 3-color for directed cycles
Memoized:         if state in memo: return; compute; store; return
D&C:              split at mid; independent; merge results
```

---

## See also

- [README.md](README.md) — Core theory and 5 recursion types
- [aditya-verma.md](aditya-verma.md) — Pattern playbook with full code
- [recursion-to-dp.md](recursion-to-dp.md) — Recursion → DP transformation
- [questions-bank.md](questions-bank.md) — 60 tiered drill questions
