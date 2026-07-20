# Recursion — Complete Reference

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: This file is core Tier 2 material. Know patterns cold; skip niche edge cases.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Conceptual awareness only.





---

## First-Principles Map

```
WHY Recursion exists
└── Problems with self-similar structure: solution = f(smaller version of problem)
    ├── Trees: height(T) = 1 + max(height(L), height(R))
    ├── Strings: reverse(s) = reverse(s[1:]) + s[0]
    ├── Combinatorics: permutations(n) = n × permutations(n-1)
    └── Graphs: DFS = visit + recurse on unvisited neighbors

WHAT it is
└── A function that calls itself on a strictly smaller input
    ├── Base case: smallest input, handled directly — no recursion
    ├── Recursive case: reduce to smaller subproblem, trust the recursion
    └── Return: combine subproblem result with current node's contribution

HOW it works
├── The call stack is your explicit state machine
│   ├── Each frame holds: current node/index, partial result, local variables
│   ├── Returning from a frame = undoing that decision (backtracking for free)
│   └── Stack depth = recursion depth = O(h) space
├── Two canonical information-flow directions on trees
│   ├── Return-up (post-order): children compute → parent aggregates
│   └── Pass-down (pre-order): parent passes context to children
└── Memoization bridge to DP
    ├── Overlapping subproblems? → cache (state → result)
    └── State = function arguments → becomes dp table dimensions

WHEN to use
├── "Generate all X" → backtracking
├── "Find any valid assignment" → backtracking + constraint pruning
├── "Tree/graph property" → structural DFS
├── Problem has optimal substructure → memoize → DP
└── Divide problem into independent subproblems → divide & conquer

WHAT can go wrong
├── Missing base case → infinite recursion / stack overflow
├── Not making progress → infinite loop (must call on strictly smaller input)
├── Forgetting to undo mutation → corrupted sibling branches
├── Python recursion limit ~1000 → sys.setrecursionlimit or convert to iterative
└── Mutable list in @lru_cache → unhashable type error; use tuples
```

---

## L3 Gold Standard Mindmap

```
RECURSION
├── BASE CASE
│   ├── Empty input (n==0, node==None, i==len(s))
│   ├── Single element (n==1, leaf node)
│   └── Constraint met (remaining==0, target found)
│
├── RECURSIVE CASE
│   ├── Include / Exclude → subsets, knapsack
│   ├── Choose next → permutations, combinations
│   ├── Split & solve → divide-and-conquer, interval DP
│   ├── Traverse → tree DFS, graph DFS
│   └── Match & advance → regex, wildcard
│
├── RETURN VALUE DESIGN (most important decision)
│   ├── Single value → height, count, bool
│   ├── Tuple → (rob, skip), (is_bst, size, min, max)
│   └── Global + local → diameter, max path sum
│
├── OPTIMIZATIONS
│   ├── Memoize overlapping subproblems → top-down DP
│   ├── Convert to iterative → avoid stack overflow
│   ├── Prune early → backtracking (remaining < 0, constraint violated)
│   └── Space optimize after tabulation → rolling array
│
└── GOTCHAS
    ├── Always snapshot path[:] not path
    ├── Mark visited BEFORE recursing (graphs)
    ├── Directed cycle: 3-color (white/gray/black), not just visited
    ├── Duplicate dedup: i > start (not i > 0) for combos
    └── Permutation dedup: not used[i-1] (not used[i])
```

---

## Theory & Mental Models

### Five Recursion Types

| Type | Structure | Example |
| :--- | :--- | :--- |
| **Linear** | f(n) calls f(n-1) | Factorial, linked-list traversal |
| **Binary `🎯 T2`** | f(n) calls f(left) + f(right) | Tree traversal, merge sort |
| **Multi-branch** | f(n) calls f(n-c1), f(n-c2)... | Coin change, climbing stairs |
| **Exponential (backtracking)** | 2^n branches | Subsets, permutations |
| **Tail** | Result fully computed before recursive call | Accumulator-style fib |

### Iterative Conversion Templates

```python
# Preorder DFS (iterative)
def preorder_iterative(root):
    if not root: return []
    stack, result = [root], []
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right: stack.append(node.right)  # right first (LIFO)
        if node.left:  stack.append(node.left)
    return result

# Inorder DFS (iterative)
def inorder_iterative(root):
    stack, result, curr = [], [], root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result

# Postorder DFS (iterative — reverse trick)
def postorder_iterative(root):
    if not root: return []
    stack, result = [root], []
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.left:  stack.append(node.left)   # left first (reversed at end)
        if node.right: stack.append(node.right)
    return result[::-1]
```

### Python Recursion Limit

```python
import sys
sys.setrecursionlimit(10**5)   # stopgap; prefer iterative for prod code
```

### Memoization with `@lru_cache`

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def solve(i, j):            # args must be hashable (int, str, tuple — NOT list)
    ...

solve.cache_clear()         # call between test cases to avoid stale state
```

---

## Universal Recursion Recipe (Aditya Verma 4-Step)

```
Step 1 — DRAW THE CHOICE DIAGRAM
         Identify what choices exist at each level of the recursion tree.
         For include/exclude: 2 branches. For permutations: n branches.

Step 2 — WRITE IP/OP (Input/Output signature)
         IP = what changes per call (shrinks — index, remaining capacity, string suffix)
         OP = what you're building (path, count, running sum)
         Base case = when IP is exhausted or constraint is met.

Step 3 — CODE
         Write the recursive function: handle base case, then make choices.
         Trust the recursion — don't trace the full tree mentally.

Step 4 — CONVERT TO DP (if overlapping subproblems)
         State = function arguments → dp table dimensions
         Memoize → top-down done; then tabulate bottom-up for stack safety.
```

> [!IMPORTANT]
> The **state** in the recursive version directly becomes the **dp table dimensions**. If the recursion is `solve(i, w)`, your table is `dp[i][w]`. Never skip to the table without writing the recursion first.

---

## Pattern Map

| # | Pattern | Signal | Key Code Element |
| :--- | :--- | :--- | :--- |
| 1 | **Include/Exclude** | "all subsets / power set" | 2 branches at each index |
| 2 | **Permutations `🎯 T2`** | "all orderings / arrangements" | `used[]` array or swap-based |
| 3 | **IP/OP String Building** | "generate strings with constraints" | validity guard on each branch |
| 4 | **Divide & Combine** | "split → solve independently → merge" | `solve(left) + solve(right)` |
| 5 | **Mathematical** | "power, Hanoi, Josephus" | mathematical recurrence |
| 6 | **Tree/Graph DFS** | "tree property / graph traversal" | structural post/pre-order |
| 7 | **N-Queens / Constraint Satisfaction** | "place N things with constraints" | clash sets / bitmask |
| 8 | **Memoization Bridge** | "recursion TLEs → overlapping subproblems" | `@lru_cache` + same state |

---

## Pattern 1 — Include / Exclude (Subsets)

**Signal:** "find all subsets", "power set", "count subsets with property"

```python
def subsets(nums: list[int]) -> list[list[int]]:
    result = []
    def backtrack(start: int, current: list[int]) -> None:
        result.append(current[:])         # record at EVERY node (not just leaves)
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
    backtrack(0, [])
    return result

def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []
    def backtrack(start: int, current: list[int]) -> None:
        result.append(current[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i-1]:
                continue               # skip duplicate at same level
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
    backtrack(0, [])
    return result
```

> [!CAUTION]
> Duplicate dedup guard is `i > start` (NOT `i > 0`). This skips duplicates at the same recursion level but allows the same value to appear across different levels.

---

## Pattern 2 — Permutations

**Signal:** "all orderings", "all arrangements", "order matters"

```python
# Standard: used-array approach
def permute(nums: list[int]) -> list[list[int]]:
    result = []
    used = [False] * len(nums)
    def backtrack(current: list[int]) -> None:
        if len(current) == len(nums):
            result.append(current[:])
            return
        for i in range(len(nums)):
            if used[i]: continue
            used[i] = True
            current.append(nums[i])
            backtrack(current)
            current.pop()
            used[i] = False
    backtrack([])
    return result

# Swap-based: avoids used array (useful for in-place operations)
def permute_swap(nums: list[int]) -> list[list[int]]:
    result = []
    def backtrack(start: int) -> None:
        if start == len(nums):
            result.append(nums[:])
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]   # undo
    backtrack(0)
    return result

# Unique permutations (duplicates in input)
def permute_unique(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []
    used = [False] * len(nums)
    def backtrack(current: list[int]) -> None:
        if len(current) == len(nums):
            result.append(current[:])
            return
        for i in range(len(nums)):
            if used[i]: continue
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue           # skip same-value sibling (not used[i-1] = sibling, not ancestor)
            used[i] = True
            current.append(nums[i])
            backtrack(current)
            current.pop()
            used[i] = False
    backtrack([])
    return result
```

---

## Pattern 3 — IP/OP String Building

**Signal:** "generate all valid strings", "generate parentheses", "letter case permutation"

```python
def generate_parentheses(n: int) -> list[str]:
    result = []
    def backtrack(open_count: int, close_count: int, current: list[str]) -> None:
        if len(current) == 2 * n:
            result.append(''.join(current))
            return
        if open_count < n:
            current.append('(')
            backtrack(open_count + 1, close_count, current)
            current.pop()
        if close_count < open_count:
            current.append(')')
            backtrack(open_count, close_count + 1, current)
            current.pop()
    backtrack(0, 0, [])
    return result

def letter_case_permutation(s: str) -> list[str]:
    result = []
    def backtrack(i: int, current: list[str]) -> None:
        if i == len(s):
            result.append(''.join(current))
            return
        if s[i].isdigit():
            current.append(s[i])
            backtrack(i + 1, current)
            current.pop()
        else:
            for ch in [s[i].lower(), s[i].upper()]:
                current.append(ch)
                backtrack(i + 1, current)
                current.pop()
    backtrack(0, [])
    return result
```

---

## Pattern 4 — Divide & Combine

**Signal:** "different ways to evaluate", "split and combine results independently"

```python
def different_ways(expression: str) -> list[int]:
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def solve(expr: str) -> list[int]:
        results = []
        for i, ch in enumerate(expr):
            if ch in '+-*':
                for left in solve(expr[:i]):
                    for right in solve(expr[i+1:]):
                        if ch == '+': results.append(left + right)
                        elif ch == '-': results.append(left - right)
                        elif ch == '*': results.append(left * right)
        if not results:
            results.append(int(expr))   # pure number, no operator
        return results
    return solve(expression)

def merge_sort(nums: list[int]) -> list[int]:
    if len(nums) <= 1: return nums
    mid = len(nums) // 2
    left  = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]: merged.append(left[i]); i += 1
        else: merged.append(right[j]); j += 1
    return merged + left[i:] + right[j:]
```

---

## Pattern 5 — Mathematical Recursion

**Signal:** "fast exponentiation", "Tower of Hanoi", "Josephus problem"

```python
def my_pow(x: float, n: int) -> float:
    """Fast exponentiation: O(log N)"""
    if n == 0: return 1
    if n < 0:  return 1 / my_pow(x, -n)
    if n % 2 == 0:
        half = my_pow(x, n // 2)
        return half * half
    return x * my_pow(x, n - 1)

def hanoi(n: int, src: str, dst: str, aux: str) -> None:
    """Tower of Hanoi: 2^n - 1 moves"""
    if n == 0: return
    hanoi(n-1, src, aux, dst)
    print(f"Move disk {n} from {src} to {dst}")
    hanoi(n-1, aux, dst, src)

def josephus(n: int, k: int) -> int:
    """0-indexed position of the survivor. O(N) time."""
    if n == 1: return 0
    return (josephus(n-1, k) + k) % n
```

---

## Pattern 6 — Tree / Graph DFS

**Signal:** "tree property", "path in graph", "connected components", "cycle detection"

### Tree DFS

```python
def max_depth(root) -> int:
    """Post-order: children compute, parent aggregates."""
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

def diameter_of_binary_tree(root) -> int:
    """Global max + local height returned up."""
    best = [0]
    def height(node) -> int:
        if not node: return 0
        left  = height(node.left)
        right = height(node.right)
        best[0] = max(best[0], left + right)
        return 1 + max(left, right)
    height(root)
    return best[0]

def max_path_sum(root) -> int:
    best = [float('-inf')]
    def gain(node) -> int:
        if not node: return 0
        left  = max(gain(node.left),  0)   # clip negatives
        right = max(gain(node.right), 0)
        best[0] = max(best[0], node.val + left + right)
        return node.val + max(left, right)
    gain(root)
    return best[0]

def binary_tree_paths(root) -> list[str]:
    result = []
    def dfs(node, path):
        if not node.left and not node.right:
            result.append(path)
            return
        if node.left:  dfs(node.left,  path + f'->{node.left.val}')
        if node.right: dfs(node.right, path + f'->{node.right.val}')
    if root: dfs(root, str(root.val))
    return result
```

### Graph DFS

```python
def dfs(node, visited, graph):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited, graph)

def has_cycle_directed(graph, n) -> bool:
    """3-color: 0=unvisited, 1=in-stack(gray), 2=done(black)"""
    color = [0] * n
    def dfs(node) -> bool:
        color[node] = 1
        for neighbor in graph[node]:
            if color[neighbor] == 1: return True    # back edge
            if color[neighbor] == 0 and dfs(neighbor): return True
        color[node] = 2
        return False
    return any(dfs(i) for i in range(n) if color[i] == 0)
```

> [!CAUTION]
> For directed graphs, a simple `visited` set is insufficient for cycle detection — you need 3-color tracking. A node reachable via two paths can be legitimately visited twice; only a back edge (gray → gray) is a real cycle.

---

## Pattern 7 — N-Queens / Constraint Satisfaction

**Signal:** "place N items with constraints", "no two in same row/column/diagonal"

```python
def solve_n_queens(n: int) -> list[list[str]]:
    result = []
    cols = set()
    diag1 = set()   # row - col
    diag2 = set()   # row + col

    def backtrack(row: int, placement: list[int]) -> None:
        if row == n:
            board = []
            for col in placement:
                board.append('.' * col + 'Q' + '.' * (n - col - 1))
            result.append(board)
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col); diag1.add(row - col); diag2.add(row + col)
            backtrack(row + 1, placement + [col])
            cols.remove(col); diag1.remove(row - col); diag2.remove(row + col)

    backtrack(0, [])
    return result

def total_n_queens(n: int) -> int:
    """Bitmask version: O(N!) time but smaller constant."""
    def backtrack(row, cols, diag1, diag2):
        if row == n: return 1
        count = 0
        available = ((1 << n) - 1) & ~(cols | diag1 | diag2)
        while available:
            bit = available & (-available)   # lowest set bit
            available -= bit
            count += backtrack(row+1, cols|bit, (diag1|bit)<<1, (diag2|bit)>>1)
        return count
    return backtrack(0, 0, 0, 0)
```

---

## Pattern 8 — Memoization Bridge

**Signal:** recursion gives TLE → look for overlapping subproblems → memoize

```python
def word_break(s: str, word_dict: list[str]) -> bool:
    words = frozenset(word_dict)
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def solve(i: int) -> bool:
        if i == len(s): return True
        return any(s[i:j] in words and solve(j)
                   for j in range(i+1, len(s)+1))
    return solve(0)

def coin_change(coins: list[int], amount: int) -> int:
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def solve(rem: int) -> int:
        if rem == 0: return 0
        if rem < 0:  return float('inf')
        return 1 + min(solve(rem - c) for c in coins)
    result = solve(amount)
    return result if result != float('inf') else -1
```

---

## Combination Problems — Complete Family

### Theory — Combinations vs Permutations vs Subsets

```
Permutations: loop over ALL unused elements each time (order matters)
Combinations: loop from START index each time (order doesn't matter)
Subsets:      record at EVERY node, not just leaves (all sizes)
```

| Problem | Reuse | Dups in Input | Order | Key Trick |
| :--- | :--- | :--- | :--- | :--- |
| Subsets | No | No | No | Record at every node |
| Subsets II | No | Yes | No | Sort + skip `nums[j]==nums[j-1]` when `j>start` |
| Combinations | No | No | No | Prune: loop to `n-(k-len)+1` |
| Combination Sum I | Yes | No | No | Recurse with same `i` (not `i+1`) |
| Combination Sum II | No | Yes | No | Sort + skip `candidates[i]==candidates[i-1]` when `i>start` |
| Combination Sum III | No | No | No | Both size AND sum constraints at base |
| Combination Sum IV | Yes | No | Yes | DP: amount in outer loop |
| Permutations | No | No | Yes | `used[]` array or swap-based |
| Permutations II | No | Yes | Yes | Sort + `not used[i-1]` guard |

### Combination Sum I — Unlimited Reuse (LC 39)

```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    candidates.sort()
    result = []
    def backtrack(start: int, remaining: int, current: list[int]) -> None:
        if remaining == 0:
            result.append(current[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining: break
            current.append(candidates[i])
            backtrack(i, remaining - candidates[i], current)   # i not i+1: reuse
            current.pop()
    backtrack(0, target, [])
    return result
```

### Combination Sum II — Each Once, Duplicates in Input (LC 40)

```python
def combination_sum_ii(candidates: list[int], target: int) -> list[list[int]]:
    candidates.sort()
    result = []
    def backtrack(start: int, remaining: int, current: list[int]) -> None:
        if remaining == 0:
            result.append(current[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining: break
            if i > start and candidates[i] == candidates[i-1]: continue  # dedup
            current.append(candidates[i])
            backtrack(i + 1, remaining - candidates[i], current)
            current.pop()
    backtrack(0, target, [])
    return result
```

### Combination Sum III — Exactly K Numbers 1–9 (LC 216)

```python
def combination_sum_iii(k: int, n: int) -> list[list[int]]:
    result = []
    def backtrack(start: int, remaining: int, current: list[int]) -> None:
        if len(current) == k and remaining == 0:
            result.append(current[:])
            return
        if len(current) == k or remaining <= 0: return
        for i in range(start, 10):
            current.append(i)
            backtrack(i + 1, remaining - i, current)
            current.pop()
    backtrack(1, n, [])
    return result
```

### Combination Sum IV — Order Matters (LC 377)

```python
def combination_sum_iv(nums: list[int], target: int) -> int:
    # Order matters → DP with amount in outer loop
    dp = [0] * (target + 1)
    dp[0] = 1
    for t in range(1, target + 1):
        for n in nums:
            if t >= n:
                dp[t] += dp[t - n]
    return dp[target]
```

> [!TIP]
> **Order matters → amount outer loop.** Coins outer = combinations (Coin Change II). Amount outer = permutations with repetition (Combination Sum IV). This is the fundamental loop-order distinction.

### Letter Combinations of Phone Number (LC 17)

```python
def letter_combinations(digits: str) -> list[str]:
    if not digits: return []   # empty input → [], NOT ['']
    mapping = {'2':'abc','3':'def','4':'ghi','5':'jkl',
               '6':'mno','7':'pqrs','8':'tuv','9':'wxyz'}
    result = []
    def backtrack(i: int, current: list[str]) -> None:
        if i == len(digits):
            result.append(''.join(current))
            return
        for ch in mapping[digits[i]]:
            current.append(ch)
            backtrack(i + 1, current)
            current.pop()
    backtrack(0, [])
    return result
```

### Combinations — Choose K from 1..N (LC 77)

```python
def combine(n: int, k: int) -> list[list[int]]:
    result = []
    def backtrack(start: int, current: list[int]) -> None:
        if len(current) == k:
            result.append(current[:])
            return
        for i in range(start, n - (k - len(current)) + 2):   # pruning
            current.append(i)
            backtrack(i + 1, current)
            current.pop()
    backtrack(1, [])
    return result
```

### Restore IP Addresses (LC 93)

```python
def restore_ip_addresses(s: str) -> list[str]:
    result = []
    def backtrack(start: int, parts: list[str]) -> None:
        if len(parts) == 4:
            if start == len(s): result.append('.'.join(parts))
            return
        for length in range(1, 4):
            if start + length > len(s): break
            segment = s[start:start+length]
            if len(segment) > 1 and segment[0] == '0': break   # no leading zeros
            if int(segment) > 255: break
            parts.append(segment)
            backtrack(start + length, parts)
            parts.pop()
    backtrack(0, [])
    return result
```

---

## Graph Recursion — DFS-Based Algorithms

### Core Template

```python
def dfs(node, visited, graph):
    visited.add(node)              # mark BEFORE recursing
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited, graph)
```

> [!CAUTION]
> Always mark a node visited **before** recursing into its neighbors. Marking after allows two branches to simultaneously enter the same node on graphs with shared neighbors → infinite loop or double-counting.

### Flood Fill (LC 733) / Number of Islands (LC 200)

```python
def flood_fill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    original = image[sr][sc]
    if original == color: return image
    def dfs(r, c):
        if not (0 <= r < len(image) and 0 <= c < len(image[0])): return
        if image[r][c] != original: return
        image[r][c] = color
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            dfs(r + dr, c + dc)
    dfs(sr, sc)
    return image

def num_islands(grid: list[list[str]]) -> int:
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols): return
        if grid[r][c] != '1': return
        grid[r][c] = '#'
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            dfs(r + dr, c + dc)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    return count
```

### Cycle Detection — Directed (3-Color) and Undirected

```python
def has_cycle_directed(n: int, edges: list[list[int]]) -> bool:
    from collections import defaultdict
    graph = defaultdict(list)
    for u, v in edges: graph[u].append(v)
    color = [0] * n   # 0=unvisited, 1=gray(in-stack), 2=black(done)
    def dfs(node) -> bool:
        color[node] = 1
        for neighbor in graph[node]:
            if color[neighbor] == 1: return True
            if color[neighbor] == 0 and dfs(neighbor): return True
        color[node] = 2
        return False
    return any(dfs(i) for i in range(n) if color[i] == 0)

def has_cycle_undirected(n: int, edges: list[list[int]]) -> bool:
    from collections import defaultdict
    graph = defaultdict(list)
    for u, v in edges: graph[u].append(v); graph[v].append(u)
    visited = set()
    def dfs(node, parent) -> bool:
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor == parent: continue
            if neighbor in visited: return True
            if dfs(neighbor, node): return True
        return False
    for node in range(n):
        if node not in visited:
            if dfs(node, -1): return True
    return False
```

### Topological Sort (DFS Post-order) — Course Schedule I & II

```python
def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    from collections import defaultdict
    graph = defaultdict(list)
    for a, b in prerequisites: graph[b].append(a)
    state = [0] * num_courses
    def dfs(course) -> bool:
        if state[course] == 1: return False   # cycle
        if state[course] == 2: return True    # already verified
        state[course] = 1
        for next_course in graph[course]:
            if not dfs(next_course): return False
        state[course] = 2
        return True
    return all(dfs(c) for c in range(num_courses))

def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    from collections import defaultdict
    graph = defaultdict(list)
    for a, b in prerequisites: graph[b].append(a)
    state = [0] * num_courses
    order = []
    def dfs(course) -> bool:
        if state[course] == 1: return False
        if state[course] == 2: return True
        state[course] = 1
        for next_c in graph[course]:
            if not dfs(next_c): return False
        state[course] = 2
        order.append(course)   # add AFTER all descendants
        return True
    for c in range(num_courses):
        if state[c] == 0:
            if not dfs(c): return []
    return order[::-1]
```

### All Paths / Clone Graph / Surrounding Regions

```python
def all_paths_source_target(graph: list[list[int]]) -> list[list[int]]:
    result = []
    target = len(graph) - 1
    def dfs(node, path):
        if node == target:
            result.append(path[:])
            return
        for neighbor in graph[node]:
            path.append(neighbor)
            dfs(neighbor, path)
            path.pop()
    dfs(0, [0])
    return result

def clone_graph(node):
    if not node: return None
    cloned = {}
    def dfs(n):
        if n in cloned: return cloned[n]
        copy = Node(n.val, [])
        cloned[n] = copy           # register BEFORE recursing (handles cycles)
        for neighbor in n.neighbors:
            copy.neighbors.append(dfs(neighbor))
        return copy
    return dfs(node)

def solve_surrounded(board: list[list[str]]) -> None:
    if not board: return
    rows, cols = len(board), len(board[0])
    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != 'O': return
        board[r][c] = 'S'   # safe
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]: dfs(r+dr, c+dc)
    for r in range(rows):
        for c in [0, cols-1]:
            if board[r][c] == 'O': dfs(r, c)
    for c in range(cols):
        for r in [0, rows-1]:
            if board[r][c] == 'O': dfs(r, c)
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O': board[r][c] = 'X'
            elif board[r][c] == 'S': board[r][c] = 'O'
```

> [!TIP]
> **Reverse thinking for Surrounded Regions:** Instead of finding enclosed regions directly, flood-fill border-connected 'O's as 'S' (safe). Everything remaining is enclosed. Flip at end.

### Iterative DFS (Stack Overflow Prevention)

```python
def dfs_iterative(start, graph):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited: continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
```

> [!CAUTION]
> Graph DFS on large graphs (10^4+ nodes) can hit Python's default recursion limit of 1000. Use `sys.setrecursionlimit(10**5)` as a stopgap, or convert to iterative DFS for production code.

---

## String Recursion — Parsing, Matching & Manipulation

### Regular Expression Matching (LC 10)

**Pattern:** `.` matches any char. `*` matches zero or more of preceding char.

```python
from functools import lru_cache

def is_match_regex(s: str, p: str) -> bool:
    @lru_cache(maxsize=None)
    def dp(i: int, j: int) -> bool:
        if j == len(p): return i == len(s)
        first_match = i < len(s) and (p[j] == '.' or p[j] == s[i])
        if j + 1 < len(p) and p[j+1] == '*':
            return (dp(i, j+2)                         # zero occurrences
                    or (first_match and dp(i+1, j)))   # one+ occurrences
        else:
            return first_match and dp(i+1, j+1)
    return dp(0, 0)
```

> [!CAUTION]
> `*` means "zero or more of the PRECEDING character" — not a standalone wildcard. The zero-occurrence case `dp(i, j+2)` skips BOTH `p[j]` AND the `*`. This is the #1 regex bug.

### Wildcard Matching (LC 44)

**Pattern:** `?` matches any single char. `*` matches any sequence (including empty).

```python
from functools import lru_cache

def is_match_wildcard(s: str, p: str) -> bool:
    @lru_cache(maxsize=None)
    def dp(i: int, j: int) -> bool:
        if j == len(p): return i == len(s)
        if i == len(s): return all(c == '*' for c in p[j:])
        if p[j] == '*':
            return dp(i+1, j) or dp(i, j+1)   # consume s[i] | advance past '*'
        elif p[j] == '?' or p[j] == s[i]:
            return dp(i+1, j+1)
        return False
    return dp(0, 0)
```

### Expression Add Operators (LC 282)

```python
def add_operators(num: str, target: int) -> list[str]:
    result = []
    def backtrack(index: int, path: str, value: int, prev: int) -> None:
        if index == len(num):
            if value == target: result.append(path)
            return
        for i in range(index, len(num)):
            curr_str = num[index:i+1]
            if len(curr_str) > 1 and curr_str[0] == '0': break   # no leading zeros
            curr = int(curr_str)
            if index == 0:
                backtrack(i+1, curr_str, curr, curr)
            else:
                backtrack(i+1, path+'+'+curr_str, value+curr, curr)
                backtrack(i+1, path+'-'+curr_str, value-curr, -curr)
                backtrack(i+1, path+'*'+curr_str, value - prev + prev*curr, prev*curr)
    backtrack(0, '', 0, 0)
    return result
```

> [!IMPORTANT]
> **Multiplication tracking:** `prev` stores the last operand. For `*`, undo `prev`'s contribution with `value - prev`, then add `prev * curr`. This handles multiplication precedence without a stack.

### Decode String (LC 394)

```python
def decode_string(s: str) -> str:
    def decode(i: int) -> tuple[str, int]:
        result = []
        while i < len(s) and s[i] != ']':
            if s[i].isdigit():
                k = 0
                while i < len(s) and s[i].isdigit():
                    k = k * 10 + int(s[i]); i += 1
                i += 1                    # skip '['
                inner, i = decode(i)
                i += 1                    # skip ']'
                result.append(inner * k)
            else:
                result.append(s[i]); i += 1
        return ''.join(result), i
    return decode(0)[0]
```

### Palindrome Partitioning (LC 131)

```python
def partition(s: str) -> list[list[str]]:
    result = []
    def backtrack(start: int, current: list[str]) -> None:
        if start == len(s):
            result.append(current[:])
            return
        for end in range(start + 1, len(s) + 1):
            sub = s[start:end]
            if sub == sub[::-1]:
                current.append(sub)
                backtrack(end, current)
                current.pop()
    backtrack(0, [])
    return result
```

### Word Search (LC 79)

```python
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])
    def dfs(r: int, c: int, k: int) -> bool:
        if k == len(word): return True
        if not (0 <= r < rows and 0 <= c < cols): return False
        if board[r][c] != word[k]: return False
        temp, board[r][c] = board[r][c], '#'
        found = any(dfs(r+dr, c+dc, k+1) for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)])
        board[r][c] = temp
        return found
    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
```

---

## Tree Recursion — Advanced Patterns

### Return Value Design

| Return Style | Use When | Example |
| :--- | :--- | :--- |
| **Single value** | Children determine parent's answer | Max depth, count, sum |
| **Tuple / pair** | Node reports two independent quantities | House Robber III `(rob, skip)`, BST validity |
| **Global + local** | Answer crosses subtrees (path through node) | Diameter, Max Path Sum |

> [!IMPORTANT]
> **Design the return type before writing a single line of code.** Ask: "What does the parent need from its child to compute its own answer?" Getting this wrong leads to complex rewrites.

### Path Problems

```python
def has_path_sum(root, target: int) -> bool:
    if not root: return False
    if not root.left and not root.right: return root.val == target
    remaining = target - root.val
    return has_path_sum(root.left, remaining) or has_path_sum(root.right, remaining)

def path_sum_all(root, target: int) -> list[list[int]]:
    result = []
    def dfs(node, remaining, path):
        if not node: return
        path.append(node.val)
        if not node.left and not node.right and remaining == node.val:
            result.append(path[:])   # snapshot
        dfs(node.left, remaining - node.val, path)
        dfs(node.right, remaining - node.val, path)
        path.pop()                   # backtrack
    dfs(root, target, [])
    return result

def path_sum_iii(root, target: int) -> int:
    """Count paths summing to target — any start/end. Prefix sum technique."""
    from collections import defaultdict
    prefix_count = defaultdict(int)
    prefix_count[0] = 1
    count = [0]
    def dfs(node, running_sum):
        if not node: return
        running_sum += node.val
        count[0] += prefix_count[running_sum - target]
        prefix_count[running_sum] += 1
        dfs(node.left, running_sum)
        dfs(node.right, running_sum)
        prefix_count[running_sum] -= 1   # undo
    dfs(root, 0)
    return count[0]
```

### BST Recursion

```python
def is_valid_bst(root) -> bool:
    def validate(node, lo, hi):
        if not node: return True
        if not (lo < node.val < hi): return False
        return validate(node.left, lo, node.val) and validate(node.right, node.val, hi)
    return validate(root, float('-inf'), float('inf'))

def lca_bst(root, p, q):
    if p.val < root.val and q.val < root.val: return lca_bst(root.left, p, q)
    if p.val > root.val and q.val > root.val: return lca_bst(root.right, p, q)
    return root   # divergence point = LCA

def lca_tree(root, p, q):
    if not root or root == p or root == q: return root
    left  = lca_tree(root.left,  p, q)
    right = lca_tree(root.right, p, q)
    if left and right: return root   # p and q split across children
    return left or right

def kth_smallest(root, k: int) -> int:
    count = [0]; result = [None]
    def inorder(node):
        if not node or result[0] is not None: return
        inorder(node.left)
        count[0] += 1
        if count[0] == k: result[0] = node.val; return
        inorder(node.right)
    inorder(root)
    return result[0]
```

> [!CAUTION]
> For BST validation, pass `(lo, hi)` range down — do NOT just check `node.val > node.left.val`. That only catches immediate parent-child violations; BST invariant applies to ALL ancestors.

### Tree Structure Problems

```python
class Codec:
    def serialize(self, root) -> str:
        def preorder(node):
            if not node: return ['#']
            return [str(node.val)] + preorder(node.left) + preorder(node.right)
        return ','.join(preorder(root))

    def deserialize(self, data: str):
        tokens = iter(data.split(','))
        def build():
            val = next(tokens)
            if val == '#': return None
            node = TreeNode(int(val))
            node.left  = build()
            node.right = build()
            return node
        return build()

def rob_house_iii(root) -> int:
    def dfs(node):
        if not node: return 0, 0   # (rob_this, skip_this)
        l_rob, l_skip = dfs(node.left)
        r_rob, r_skip = dfs(node.right)
        rob_this  = node.val + l_skip + r_skip
        skip_this = max(l_rob, l_skip) + max(r_rob, r_skip)
        return rob_this, skip_this
    return max(dfs(root))

def count_nodes(root) -> int:
    """O(log² N) for complete binary tree."""
    if not root: return 0
    lh = rh = 0
    left, right = root, root
    while left:  lh += 1; left  = left.left
    while right: rh += 1; right = right.right
    if lh == rh: return (1 << lh) - 1   # perfect binary tree shortcut
    return 1 + count_nodes(root.left) + count_nodes(root.right)
```

---

## Recursion → Memoization → Tabulation

The mechanical 3-step bridge from naive recursion to optimized DP.

### The Three-Step Conversion

```
Step 1 — RECURSIVE: write naturally; identify state = function arguments
Step 2 — MEMOIZED: add cache keyed on arguments; check at entry, store at exit
Step 3 — TABULATED: define dp table of same shape; fill base cases first;
                     fill larger subproblems using smaller ones
Optional — SPACE OPTIMIZE: rolling row or two variables
```

**State → Table Mapping:**

| Recursive signature | Table dimensions | Fill order |
| :--- | :--- | :--- |
| `f(i)` | `dp[n+1]` | `i` from 0 to n |
| `f(i, j)` for two-string | `dp[m+1][n+1]` | row by row, left to right |
| `f(i, j)` for interval | `dp[n][n]` | by increasing `j - i` (length) |
| `f(i, w)` for knapsack | `dp[n+1][W+1]` | row by row; 1D: backward |
| `f(i, j)` for palindrome | `dp[n][n]` | by increasing length |

### Fibonacci: Recursive → Memo → Tabulated → O(1) Space

```python
# Step 1: O(2^N)
def fib_rec(n): return n if n <= 1 else fib_rec(n-1) + fib_rec(n-2)

# Step 2: O(N) with memo
from functools import lru_cache
@lru_cache(maxsize=None)
def fib_memo(n): return n if n <= 1 else fib_memo(n-1) + fib_memo(n-2)

# Step 3: O(N) tabulated
def fib_dp(n):
    if n <= 1: return n
    dp = [0] * (n+1); dp[1] = 1
    for i in range(2, n+1): dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# Step 4: O(1) space
def fib_opt(n):
    if n <= 1: return n
    prev2, prev1 = 0, 1
    for _ in range(2, n+1): prev2, prev1 = prev1, prev1 + prev2
    return prev1
```

### 0/1 Knapsack: Recursive → Tabulated → 1D

```python
def knapsack_1d(weights, values, W):
    dp = [0] * (W + 1)
    for i in range(len(weights)):
        for w in range(W, weights[i]-1, -1):   # BACKWARD — 0/1 invariant
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    return dp[W]
```

> [!CAUTION]
> The backward loop in the 1D knapsack is critical. Forward iteration lets you pick the same item multiple times (unbounded knapsack). This is the #1 knapsack bug.

### LCS / Edit Distance / Word Break (condensed)

```python
def lcs_dp(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            dp[i][j] = 1 + dp[i-1][j-1] if s1[i-1]==s2[j-1] else max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

def edit_distance_opt(w1, w2):
    m, n = len(w1), len(w2)
    dp = list(range(n + 1))
    for i in range(1, m+1):
        prev = dp[0]; dp[0] = i
        for j in range(1, n+1):
            temp = dp[j]
            dp[j] = prev if w1[i-1]==w2[j-1] else 1 + min(prev, dp[j], dp[j-1])
            prev = temp
    return dp[n]

def word_break_dp(s, word_dict):
    words = set(word_dict); n = len(s)
    dp = [False] * (n + 1); dp[0] = True
    for i in range(1, n+1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True; break
    return dp[n]
```

> [!TIP]
> Interval DP (LPS, MCM) must be filled by **increasing length** — base cases are single characters (length=1), then pairs, etc. You cannot fill row-by-row because `dp[i+1][j-1]` comes from a shorter interval, not a previous row.

---

## Common Bugs — The 15

| # | Bug | Fix |
| :--- | :--- | :--- |
| 1 | **Missing snapshot** — `result.append(current)` records reference | `result.append(current[:])` |
| 2 | **Mutable default argument** — `def f(path=[])` persists across calls | Use `None` sentinel; initialize inside |
| 3 | **Unhashable args in `@lru_cache`** — passing a list | Only pass hashable types (int, str, tuple) |
| 4 | **Wrong duplicate guard** — `i > 0` allows wrong dedup | Use `i > start` for subsets/combos |
| 5 | **Wrong permutation dedup** — `used[i-1]` vs `not used[i-1]` | `if i > 0 and nums[i]==nums[i-1] and not used[i-1]: continue` |
| 6 | **Forgetting to restore state** — `path.pop()` missing | Always undo mutations before returning |
| 7 | **Combination sum reuse `🎯 T2`** — `i+1` when reuse intended | `backtrack(i, ...)` (same `i`) for reuse; `i+1` for once-each |
| 8 | **Python recursion depth** — default limit ~1000 | `sys.setrecursionlimit(10**5)` or convert to iterative |
| 9 | **Regex `*` zero-occurrence** — forgetting `dp(i, j+2)` | Skip branch: `dp(i, j+2)` OR consume: `first_match and dp(i+1, j)` |
| 10 | **BST validation** — only checking immediate parent | Pass `(lo, hi)` range; check full ancestry |
| 11 | **Graph DFS visited timing** — marking after recursion | Mark visited BEFORE recursing into neighbors |
| 12 | **Directed cycle detection** — single visited set insufficient | 3-color: 0=white, 1=gray(in-stack), 2=black(done) |
| 13 | **LCA null check order** — `.val` before null check | Check `not root` before accessing `root.val` |
| 14 | **Forgetting to reset `used[]` after pop** | `used[i] = False` after `current.pop()` |
| 15 | **Empty generating functions** — `['']` vs `[]` | Empty digits in letter combinations → `[]` not `['']` |

### Bug Examples

```python
# Bug 1: snapshot
result.append(current[:])      # correct — copy
result.append(current)         # wrong — reference to same list

# Bug 3: unhashable
@lru_cache(maxsize=None)
def solve(i, remaining):       # OK: both ints
    ...
def solve(i, nums):            # WRONG: list is unhashable
    ...
# Fix: pass tuple(nums) or move nums to outer scope

# Bug 4/5: duplicate guard
if i > start and nums[i] == nums[i-1]: continue   # subsets/combos
if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue  # permutations

# Bug 9: regex '*' zero occurrence
if j + 1 < len(p) and p[j+1] == '*':
    return dp(i, j+2) or (first_match and dp(i+1, j))
    #      ^^^^^^^^^^^         skip 0 occurrences
```

---

## Complexity Cheatsheet

| Problem | Time | Space | Note |
| :--- | :--- | :--- | :--- |
| Subsets | O(2^n · n) | O(n) stack | 2 choices per element |
| Permutations | O(n! · n) | O(n) stack | n choices per position |
| Combinations C(n,k) | O(C(n,k) · k) | O(k) stack | |
| Combination Sum | O(2^target) | O(target) | small denominations worst case |
| N-Queens | O(n!) | O(n) | bitmask reduces constant |
| Graph DFS | O(V+E) | O(V) | each edge once |
| Tree DFS | O(n) | O(h) | h = height; skewed = O(n) |
| Regex/Interleaving (memo) | O(m·n) | O(m·n) | |

### Master Theorem (divide-and-conquer)

`T(n) = aT(n/b) + O(n^d)`

| Condition | Result | Example |
| :--- | :--- | :--- |
| `d > log_b(a)` | O(n^d) | Binary search: a=1, b=2, d=0 → O(1) |
| `d == log_b(a)` | O(n^d · log n) | Merge sort: a=2, b=2, d=1 → O(n log n) |
| `d < log_b(a)` | O(n^(log_b a)) | Strassen: a=7, b=2, d=2 → O(n^2.81) |

---

## L3 Interview Communication Framework

1. **State IP/OP** — "My function takes X and produces Y"
2. **Draw the tree** — trace a small example to ground the approach
3. **Identify base case** — "We stop when index == length / remaining == 0 / node is None"
4. **State choices** — "At each step, we branch into: include / exclude / try each neighbor"
5. **State invariant** — "Each recursive call operates on a strictly smaller subproblem"
6. **Call out pruning** — "We prune when remaining < 0 / constraint is already violated"
7. **Mention complexity** — "O(2^n) states × O(n) per state = O(n·2^n)"

---

## When NOT to Use Recursion

| Situation | Better Alternative |
| :--- | :--- |
| Need only optimal value (not all solutions) + overlapping subproblems | DP tabulation |
| Very deep recursion (n > 10^4) | Iterative + explicit stack |
| Simple linear scan | Loop |
| BFS / level-order traversal | Queue-based BFS |
| Union-Find (connectivity queries) | Union-Find data structure |
| No overlapping subproblems + just one path | Greedy |

---

## Signal → Pattern Map

| Signal in Problem | Pattern |
| :--- | :--- |
| "all subsets / power set" | Include/Exclude |
| "all permutations / orderings" | Permutations (used-set) |
| "all combinations of size k" | Combinations (start index) |
| "combination sum / partition" | Combination Sum (start + remaining) |
| "generate valid strings / parentheses" | IP/OP with validity guard |
| "tree height / diameter / LCA" | Tree DFS (return-up) |
| "BST validation / range constraint" | Tree DFS (pass-down) |
| "graph components / flood fill" | Graph DFS + visited set |
| "cycle in directed graph" | 3-color DFS |
| "topological order / course schedule" | Post-order DFS, reverse |
| "regex / wildcard matching" | Memoized string recursion |
| "expression evaluation / operators" | Backtracking + prev tracking |
| "Sudoku / N-Queens" | Constraint satisfaction backtracking |
| "slow recursion / TLE" | Memoize → tabulate |
| "recursion → DP" | State = args → table dimensions |

---

## Questions Bank — Tiered Drill

### Level 1: Foundation (Branching & Choice)

| Problem | Pattern | Key Insight |
| :--- | :--- | :--- |
| Subsets (Power Set) | Include/Exclude | 2 choices per element: `2^N` |
| Permutations | Choice-based | Pick any unused element; `N!` |
| Binary Tree Paths | Structural DFS | Leaf is base case; pass path string |
| Merge Sort | Divide & Conquer | Split until size 1; merge results |
| Fibonacci | Mathematical | `f(n) = f(n-1) + f(n-2)` |

### Level 2: L3 Standard (Pruning & Constraints)

| Problem | Pattern | The Twist |
| :--- | :--- | :--- |
| Combination Sum | Unbounded Choice | Can reuse same element: `recurse(i)` not `i+1` |
| Combination Sum II | Duplicate Input | Sort + skip sibling duplicates: `if j>i and nums[j]==nums[j-1]` |
| Generate Parentheses | Validity Guard | Add `(` if `open < n`, `)` if `close < open` |
| Word Search | Grid Backtracking | Mark `board[r][c]` visited; restore on undo |
| Palindrome Partitioning | String Splitting | Only recurse if prefix is a palindrome |
| Letter Case Permutation | IP/OP | Branch on alpha; skip digits |

### Level 3: L3 / Staff Level (Constraint Satisfaction)

| Problem | Pattern | Complexity / Optimization |
| :--- | :--- | :--- |
| N-Queens | Board Backtracking | Column and diagonal clash sets |
| Sudoku Solver | Matrix Search | Fill empty cells; 9 branches each; early exit on first valid |
| Word Search II | Trie + Backtracking | Use Trie to prune multiple word searches into one DFS |
| Unique Binary Search Trees II | Structural D&C | Build all left/right combos for each root `k` |
| Expression Add Operators | Mathematical Search | Handle `*` precedence by tracking `prev_added` |
| Robot Room Cleaner | State-Space Search | Track `(r, c)` in set; move + rotate; spiral-out |

### Full Interview Questions Table

| Problem | LC # | Pattern | Click Moment | Gotcha |
| :--- | :--- | :--- | :--- | :--- |
| Subsets | 78 | Include/Exclude | Record at every node (not just leaves) | Record before loop, not inside |
| Subsets II | 90 | Include/Exclude + dedup | Sort + skip same value at same level | `j > start` allows same value in different levels |
| Permutations | 46 | Used-set | Pick any unused each time | Mark used before recurse; unmark after |
| Permutations II | 47 | Used-set + dedup | Sort + `not used[i-1]` guard | `not used[i-1]` = sibling skip, not ancestor |
| Combinations | 77 | Start index | Prune: loop to `n-(k-len)+1` | Pruning bound is `n - (k-len) + 2` |
| Combination Sum I | 39 | Unlimited reuse | `backtrack(i, ...)` — same index | Sort + `break` when over remaining |
| Combination Sum II | 40 | Each once, dups | `backtrack(i+1, ...)` + skip guard | `i > start` not `i > 0` for skip |
| Combination Sum III | 216 | K digits 1–9 | Both `len==k` AND `remaining==0` at base | Range is 1..9 |
| Combination Sum IV | 377 | Order matters → DP | Amount outer loop → counts permutations | Really unbounded knapsack with order |
| Phone Letter Combos | 17 | IP/OP | Map each digit; build all strings | Empty digits → `[]` not `['']` |
| Restore IP Addresses | 93 | Partition + validate | Exactly 4 parts; break on leading zero or > 255 | `len > 1 and segment[0]=='0'` |
| Generate Parentheses | 22 | IP/OP + guard | Add `(` if `open < n`, `)` if `close < open` | Both counts needed |
| N-Queens | 51 | Backtracking | Column + two diagonal sets | Use sets for O(1) clash check |
| Flood Fill | 733 | DFS in-place | Spread to same-colored neighbors | Check `original == color` first |
| Number of Islands | 200 | DFS flood | Sink each island cell to `'#'` | 4-directional only |
| Clone Graph | 133 | DFS + memo | Register clone before recursing | Use original node as key (not val) |
| Course Schedule | 207 | 3-color cycle | Back edge = color==1 | `color==2` = already safe |
| Course Schedule II | 210 | Topo sort DFS | Add after all descendants | Reverse order at end |
| All Paths Source→Target | 797 | DFS backtrack | DAG: no visited set needed | Snapshot `path[:]` |
| Max Area of Island | 695 | DFS + area count | Return `1 + sum(dfs neighbors)` | Mark visited BEFORE recursing |
| Surrounded Regions | 130 | Reverse DFS | Mark border-connected safe first | 3 states: X, O, S |
| Regular Expression | 10 | Memoized recursion | `*` = zero-or-more of PRECEDING | Zero-occurrence: `dp(i, j+2)` |
| Wildcard Matching | 44 | Memoized recursion | `*` standalone matches any sequence | `dp(i+1,j)`: consume; `dp(i,j+1)`: `*` empty |
| Expression Add Operators | 282 | Backtracking | Track `prev` for multiplication undo | Leading zeros: break not continue |
| Decode String | 394 | Recursive descent | `[` triggers recursion; `]` returns | Pass and return index `i` |
| Word Search | 79 | DFS backtracking | Mark cell `'#'`; restore after | Restore even on failure |
| Palindrome Partitioning | 131 | Backtracking | Try all splits; add if palindrome | Precompute `is_pal[i][j]` |
| Path Sum I | 112 | Tree DFS pass-down | Subtract `node.val` each level | Leaf check: `not left AND not right` |
| Path Sum II | 113 | Tree DFS + backtrack | Backtrack: `path.pop()` on return | Must snapshot `path[:]` |
| Path Sum III | 437 | Prefix sum on tree | `prefix_count[curr - target]` | Undo prefix count on return |
| Max Path Sum | 124 | Global + local | Clip negatives: `max(gain(...), 0)` | Update global inside; return single arm |
| Validate BST | 98 | Pass-down range | Pass valid `(lo, hi)` range | Check full ancestry, not just parent |
| LCA BST | 235 | BST divergence | Both < root → go left; both > root → go right | Use val comparisons |
| LCA General | 236 | Sentinel propagation | Both non-null → current is LCA | Check `root == p or root == q` first |
| Serialize/Deserialize | 297 | Preorder + iter | Use `iter()` for stateful tokens | `'#'` for nulls |
| House Robber III | 337 | Tuple return | `(rob_this, skip_this)` | Return pair; preserve both choices |
| Kth Smallest BST | 230 | Inorder + count | Inorder = sorted; stop at k | Short-circuit after kth found |
| Word Break | 139 | Memoized recursion | `frozenset` word dict; `lru_cache` | O(2^N) without memo |
| Coin Change | 322 | Memoized recursion | `rem < 0 → inf`; min over coins | Forward loop = unbounded in tabulation |

---

## Flashcards

**Your backtracking result list contains N copies of the same final state. What went wrong?** #flashcard
`result.append(current)` stored a **reference** to the path list, which every later mutation and `pop()` continues to edit. Append a snapshot: `result.append(current[:])`. Immutable accumulators (str, tuple, int) do not need this.

**Why is the duplicate guard `i > start` for subsets/combinations but `not used[i-1]` for permutations?** #flashcard
In combinations, `i > start` skips a repeated value only among siblings *at the same depth*, preserving its use deeper in the branch. Permutations revisit all indices, so sameness must be judged by whether the identical prior value is currently placed: `if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue` — skip only when the twin is unused, meaning this branch was already explored.

**In graph DFS, why must a node be marked visited before recursing rather than after?** #flashcard
Marking after recursion lets a cycle re-enter a node already on the call stack, causing infinite recursion or exponential revisits. Mark on entry — the analogue of marking on *enqueue* in BFS.

**Why is a single visited set insufficient for cycle detection in a directed graph?** #flashcard
It cannot distinguish "already fully processed" from "currently on the recursion stack" — a cross-edge into a finished node is legal, a back-edge into an in-progress node is a cycle. Use 3-coloring: white unvisited, **gray in-stack**, black done. A cycle exists exactly when you reach a gray node.

**Combination Sum: when do you recurse with `i` versus `i + 1`?** #flashcard
`backtrack(i, ...)` — same index — allows the element to be reused unboundedly (LC 39). `backtrack(i + 1, ...)` consumes it once (LC 40). Passing `i + 1` when reuse was intended silently loses valid combinations rather than erroring.

**Python raises `RecursionError` on a deep but correct recursion. What are your two options?** #flashcard
Raise the ceiling with `sys.setrecursionlimit(10**5)`, or convert to an explicit stack / iterative form. Say out loud that CPython's ~1000-frame default is an implementation limit, not an algorithmic one — for `n > 10^4`, prefer the iterative version or bottom-up DP.
