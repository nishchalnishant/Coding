# Recursion — Aditya Verma Pattern Playbook

Pattern-first recursion: name the technique, sketch the decision tree, write IP/OP code, then convert to DP. For the formal template see [recursion/README.md](README.md) and [backtracking.md](../backtracking.md).

---

## The Universal Recursion Recipe

Every recursion problem follows this four-step build order.

```
Step 1 — Identify: What shrinks? (index, string, remaining budget, subtree)
Step 2 — Draw the decision tree for a small example (2–3 elements)
Step 3 — Write IP/OP recursive code matching the tree
Step 4 — Identify overlapping subproblems → memoize or tabulate
```

**Identify recursion:** At each call you make a **choice** (include/exclude, left/right, which character) on a **smaller input**. If no choice exists — use iteration.

**IP/OP naming rule:**
- **IP (Input):** What is left to process — index `i`, remaining string `s`, remaining budget.
- **OP (Output):** What you are building — current path, current subset, current count.

**Decision tree rule:** Every branch is one choice. The tree has `O(branches^depth)` nodes. Sketch this before writing a single line of code.

---

## Pattern Map — Choose in 30 Seconds

| What the problem asks | Pattern |
| :--- | :--- |
| All subsets / power set | **Include/Exclude (Binary Tree)** |
| All permutations / arrangements | **Swap-based or Used-array** |
| Build all valid strings (parens, palindromes) | **IP/OP with validity guard** |
| Optimise over choices (max/min/count) | **Recursion + Memoization → DP** |
| Structural recursion on tree/graph | **DFS with return value** |
| Mathematical series defined by smaller terms | **Divide → Combine** |
| Simulate game / puzzle | **State-space search + pruning** |

---

## Pattern 1 — Include / Exclude (Subsets)

### Theory

**Core idea:** For each element you have exactly two choices: include it in the current output or skip it. This produces a complete binary decision tree of depth `n`.

**State (IP/OP):**
- IP: current index `i`
- OP: current subset (list being built)

**Recurrence:**
```
subsets(i, current):
    if i == n:
        record current; return
    subsets(i+1, current + [nums[i]])   # include
    subsets(i+1, current)               # exclude
```

**Base case:** `i == n` → record the snapshot of `current`.

**Complexity:** O(2^N) calls, O(N) stack depth.

```python
def subsets(nums: list[int]) -> list[list[int]]:
    result = []

    def solve(i: int, current: list[int]) -> None:
        if i == len(nums):
            result.append(current[:])
            return
        # include nums[i]
        current.append(nums[i])
        solve(i + 1, current)
        current.pop()
        # exclude nums[i]
        solve(i + 1, current)

    solve(0, [])
    return result
```

> [!TIP]
> `current[:]` snapshot must be taken at the base case (or wherever you record). If you append `current` directly you will record a reference that keeps mutating.

> [!CAUTION]
> **Subsets II (duplicates):** Sort `nums` first. On the **exclude** branch, skip all subsequent elements equal to `nums[i]` (fast-forward `i` past duplicates). Without this, duplicate elements generate duplicate subsets.

```python
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []

    def solve(i: int, current: list[int]) -> None:
        result.append(current[:])
        for j in range(i, len(nums)):
            if j > i and nums[j] == nums[j - 1]:   # skip duplicate choices
                continue
            current.append(nums[j])
            solve(j + 1, current)
            current.pop()

    solve(0, [])
    return result
```

### Variations

| Variant | Change from base |
|---------|-----------------|
| Subsets II (duplicates) | Sort + skip `nums[j]==nums[j-1]` when `j>i` |
| Subsets of size K | Only record when `len(current)==K` |
| Power Set sum | Accumulate `total` instead of list; base case checks target |

---

## Pattern 2 — Permutations

### Theory

**Core idea:** At each position, choose any *unused* element. Two implementations:

1. **Used-array:** `used[i]` boolean; push `nums[i]`, recurse, pop.
2. **Swap-based:** Swap `nums[i]` with `nums[pos]`, recurse `pos+1`, swap back.

**State (IP/OP):**
- IP: depth (number of elements placed so far)
- OP: current permutation

**Recurrence:**
```
permute(depth, current, used):
    if depth == n:
        record current; return
    for i in 0..n-1:
        if not used[i]:
            pick nums[i]; recurse(depth+1); unpick
```

**Complexity:** O(N! × N) — N! leaves, each takes O(N) to snapshot.

```python
def permute(nums: list[int]) -> list[list[int]]:
    result = []
    used = [False] * len(nums)

    def solve(current: list[int]) -> None:
        if len(current) == len(nums):
            result.append(current[:])
            return
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                current.append(nums[i])
                solve(current)
                current.pop()
                used[i] = False

    solve([])
    return result
```

> [!TIP]
> **Swap-based** avoids allocating a `used[]` array and is O(1) extra space per frame. Prefer it when memory is tight.

```python
def permute_swap(nums: list[int]) -> list[list[int]]:
    result = []

    def solve(start: int) -> None:
        if start == len(nums):
            result.append(nums[:])
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            solve(start + 1)
            nums[start], nums[i] = nums[i], nums[start]

    solve(0)
    return result
```

> [!CAUTION]
> **Permutations II (duplicates):** Sort first. In the used-array version, add guard: `if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue`. The `not used[i-1]` ensures the duplicate sibling was skipped at this level, not used in a child.

```python
def permute_unique(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []
    used = [False] * len(nums)

    def solve(current: list[int]) -> None:
        if len(current) == len(nums):
            result.append(current[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue                               # skip duplicate branch
            used[i] = True
            current.append(nums[i])
            solve(current)
            current.pop()
            used[i] = False

    solve([])
    return result
```

### Variations

| Variant | Change from base |
|---------|-----------------|
| Permutations II | Sort + `not used[i-1]` duplicate guard |
| Next Permutation | In-place: find rightmost ascent, swap with next larger, reverse suffix |
| Permutation Sequence | Math: `(k-1) // (n-1)!` index selection; no recursion needed |

---

## Pattern 3 — IP/OP with Validity Guard (String Building)

### Theory

**Core idea:** Build a string character by character. At each step, only add a character if it keeps the current prefix **valid**. Stop when the output reaches the target length.

**State (IP/OP):**
- IP: counters tracking what is still available (e.g., `open_remaining`, `close_allowed`)
- OP: `current` string being built

**Canonical example: Generate Parentheses**

```
Rules:
  Add '(' if open < n
  Add ')' if close < open
  Record when len(current) == 2*n
```

```python
def generate_parentheses(n: int) -> list[str]:
    result = []

    def solve(current: str, open_count: int, close_count: int) -> None:
        if len(current) == 2 * n:
            result.append(current)
            return
        if open_count < n:
            solve(current + '(', open_count + 1, close_count)
        if close_count < open_count:
            solve(current + ')', open_count, close_count + 1)

    solve('', 0, 0)
    return result
```

> [!TIP]
> The validity guard (`close < open`) prunes the tree from O(4^N / sqrt(N)) to exactly the Catalan number C(N) leaves. This is why explicit validity checking is more efficient than generating all strings and filtering.

**Generalisation — Letter Case Permutation:**

```python
def letter_case_permutation(s: str) -> list[str]:
    result = []

    def solve(i: int, current: list[str]) -> None:
        if i == len(s):
            result.append(''.join(current))
            return
        current.append(s[i].lower())
        solve(i + 1, current)
        current.pop()
        if s[i].isalpha():
            current.append(s[i].upper())
            solve(i + 1, current)
            current.pop()

    solve(0, [])
    return result
```

### Variations

| Variant | Validity guard | Depth |
|---------|---------------|-------|
| Generate Parentheses | `close < open` and `open < n` | `2n` |
| Letter Case Permutation | Always valid; branch only on alpha | `len(s)` |
| Palindrome Partitioning | Add partition only if substring is palindrome | variable |
| Phone Number Letter Combinations | For each digit, try all mapped letters | `len(digits)` |

---

## Pattern 4 — Divide and Combine

### Theory

**Core idea:** Split the problem into two or more independent subproblems, recurse on each, then combine results. No backtracking — results from children are merged, not undone.

**State:** The interval or index range `[left, right]` or `[i, j]`.

**Recurrence:**
```
solve(left, right):
    if base: return trivial answer
    mid = (left + right) // 2
    left_result  = solve(left, mid)
    right_result = solve(mid+1, right)
    return combine(left_result, right_result)
```

**Canonical example: Different Ways to Add Parentheses**

For each operator, split the expression into left and right subexpressions, recurse both, combine all pairs.

```python
def different_ways(expression: str) -> list[int]:
    from functools import lru_cache
    import operator as op

    ops = {'+': op.add, '-': op.sub, '*': op.mul}

    @lru_cache(maxsize=None)
    def solve(expr: str) -> list[int]:
        results = []
        for i, ch in enumerate(expr):
            if ch in ops:
                for left in solve(expr[:i]):
                    for right in solve(expr[i+1:]):
                        results.append(ops[ch](left, right))
        if not results:                     # base: pure number
            results.append(int(expr))
        return results

    return solve(expression)
```

> [!TIP]
> **Memoize on the string slice** — identical subexpressions appear multiple times across different parenthesisations. `@lru_cache` on the string key gives you free top-down DP.

**Merge Sort as divide-and-combine:**

```python
def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    # combine step
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    return merged + left[i:] + right[j:]
```

### Variations

| Problem | Split | Combine |
|---------|-------|---------|
| Merge Sort | halves | merge two sorted arrays |
| Different Ways to Add Parentheses | at each operator | cartesian product of left × right results |
| Unique BSTs II | root = each value; left/right subtrees | attach all left-right subtree pairs |
| Count of Range Sum | halves (merge sort style) | count cross-half pairs during merge |

---

## Pattern 5 — Mathematical Recursion

### Theory

**Core idea:** Problem has a closed recursive formula. The recursion IS the definition. No decision tree — just reduce `n` to smaller `n`.

**Common forms:**
```
Fibonacci:   f(n) = f(n-1) + f(n-2)
Power:       pow(x, n) = pow(x, n//2)^2  [fast exponentiation]
GCD:         gcd(a, b) = gcd(b, a % b)
Factorial:   f(n) = n * f(n-1)
Tower of Hanoi: move(n, A, B, C) uses move(n-1, ...)
```

**Fast Exponentiation (Exponentiation by Squaring):**

```python
def my_pow(x: float, n: int) -> float:
    if n == 0:
        return 1.0
    if n < 0:
        x, n = 1 / x, -n
    half = my_pow(x, n // 2)
    if n % 2 == 0:
        return half * half
    else:
        return half * half * x
```

> [!TIP]
> Fast exponentiation is O(log N) because the exponent halves each call. This comes up in: modular exponentiation, matrix exponentiation for Fibonacci in O(log N), Super Pow (LC 372).

**Tower of Hanoi:**

```python
def hanoi(n: int, src: str, aux: str, dst: str) -> None:
    if n == 1:
        print(f"Move disk 1 from {src} to {dst}")
        return
    hanoi(n - 1, src, dst, aux)        # move n-1 disks to aux
    print(f"Move disk {n} from {src} to {dst}")
    hanoi(n - 1, aux, src, dst)        # move n-1 disks from aux to dst
```

> [!CAUTION]
> Tower of Hanoi requires exactly **2^N − 1** moves. You cannot do better — this is a mathematical lower bound, not an implementation detail.

**Josephus Problem:**

```python
def josephus(n: int, k: int) -> int:
    # Returns 0-based survivor position
    if n == 1:
        return 0
    return (josephus(n - 1, k) + k) % n
```

> [!CAUTION]
> The formula is **0-based**. Add 1 to get the 1-based survivor: `josephus(n, k) + 1`. The recurrence `(f(n-1, k) + k) % n` shifts the survivor index back from the (n-1) circle to the n circle.

### Variations

| Problem | Recurrence | Complexity |
|---------|-----------|------------|
| Fibonacci | `f(n-1) + f(n-2)` | O(N) with memo |
| Fast Power | `pow(x, n//2)^2` | O(log N) |
| GCD | `gcd(b, a % b)` | O(log min(a,b)) |
| Tower of Hanoi | `move(n-1)` × 2 + 1 step | O(2^N) |
| Josephus | `(f(n-1,k)+k) % n` | O(N) |

---

## Pattern 6 — Tree / Graph DFS (Structural Recursion)

### Theory

**Core idea:** The recursion mirrors the structure of the data. For trees: process left subtree, right subtree, combine at root. The "decision" is which child to recurse into.

**Key insight:** The **return value** from each child is what you combine. Design the return type carefully — often you return two values (e.g., rob/skip, diameter/height, max-path/any-path).

**State:** The current `node` (the "input" shrinks structurally, not by index).

**Canonical examples:**

```python
# Path Sum — does a root-to-leaf path sum to target?
def has_path_sum(root, target: int) -> bool:
    if not root:
        return False
    if not root.left and not root.right:    # leaf
        return root.val == target
    return (has_path_sum(root.left,  target - root.val) or
            has_path_sum(root.right, target - root.val))

# Diameter of Binary Tree — pass height up, update diameter via closure
def diameter_of_binary_tree(root) -> int:
    diameter = [0]

    def height(node) -> int:
        if not node:
            return 0
        lh = height(node.left)
        rh = height(node.right)
        diameter[0] = max(diameter[0], lh + rh)   # update at each node
        return 1 + max(lh, rh)

    height(root)
    return diameter[0]

# Maximum Path Sum — each node returns best single-arm; update global at each node
def max_path_sum(root) -> int:
    best = [float('-inf')]

    def gain(node) -> int:
        if not node:
            return 0
        left  = max(gain(node.left),  0)
        right = max(gain(node.right), 0)
        best[0] = max(best[0], node.val + left + right)
        return node.val + max(left, right)          # return single arm

    gain(root)
    return best[0]
```

> [!TIP]
> **Two-value return pattern:** When the answer at a node depends on a **global** quantity (diameter, maximum path through the node) AND a **local** quantity returned to the parent (height, single-arm gain), use a closure variable for the global update and the return value for the local result.

> [!CAUTION]
> For path problems, `max(..., 0)` clips negative contributions — only include a subtree if it helps. Forgetting this clip causes wrong answers on trees with negative node values.

```python
# All Paths from Root to Leaf
def binary_tree_paths(root) -> list[str]:
    result = []

    def dfs(node, path: str) -> None:
        if not node:
            return
        path += str(node.val)
        if not node.left and not node.right:
            result.append(path)
            return
        dfs(node.left,  path + '->')
        dfs(node.right, path + '->')

    dfs(root, '')
    return result
```

### Variations

| Problem | Return value design |
|---------|-------------------|
| Path Sum | `bool` — found path |
| Max Path Sum | `int` best single-arm; global tracks full path |
| Diameter | `int` height; global tracks `lh + rh` |
| House Robber III | `(rob, skip)` tuple per node |
| Lowest Common Ancestor | node reference (the LCA itself) |
| Flatten Tree to Linked List | rightmost leaf pointer for O(1) linking |

---

## Pattern 7 — N-Queens / Constraint Satisfaction

### Theory

**Core idea:** Backtracking with hard constraints. Place one element per row/slot; prune branches that violate constraints immediately. The recursion explores a search tree and backtracks when stuck.

**State:** Row (or slot) index; sets/arrays tracking which columns, diagonals are occupied.

**Constraint check for queens:** column clash (`col[c]`), main diagonal (`diag1[r-c]`), anti-diagonal (`diag2[r+c]`).

```python
def solve_n_queens(n: int) -> list[list[str]]:
    results = []
    board = [['.' ] * n for _ in range(n)]
    cols   = set()
    diag1  = set()   # row - col  (constant along \ diagonal)
    diag2  = set()   # row + col  (constant along / diagonal)

    def backtrack(row: int) -> None:
        if row == n:
            results.append([''.join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col); diag1.add(row - col); diag2.add(row + col)
            board[row][col] = 'Q'
            backtrack(row + 1)
            board[row][col] = '.'
            cols.remove(col); diag1.remove(row - col); diag2.remove(row + col)

    backtrack(0)
    return results
```

> [!TIP]
> **Bitmask version:** Replace sets with three integers (`cols`, `diag1`, `diag2`). Available columns = `((1<<n)-1) & ~(cols | diag1 | diag2)`. Iterate set bits with `bit = avail & -avail`. This is ~3x faster in practice.

```python
def total_n_queens(n: int) -> int:
    count = [0]

    def backtrack(row: int, cols: int, diag1: int, diag2: int) -> None:
        if row == n:
            count[0] += 1
            return
        avail = ((1 << n) - 1) & ~(cols | diag1 | diag2)
        while avail:
            bit = avail & (-avail)             # lowest set bit
            avail &= avail - 1                 # remove it
            backtrack(row + 1,
                      cols | bit,
                      (diag1 | bit) << 1,
                      (diag2 | bit) >> 1)

    backtrack(0, 0, 0, 0)
    return count[0]
```

### Variations

| Problem | One element per | Constraint |
|---------|----------------|------------|
| N-Queens | row | no col/diag clash |
| Sudoku Solver | cell | no row/col/box clash |
| Word Search | grid cell | visited set; character match |
| Rat in a Maze | grid cell | not wall, not visited |

---

## Pattern 8 — Recursion → Memoization Bridge

### Theory

**Core idea:** Every recursion with overlapping subproblems can become top-down DP by adding a memo dict keyed on the function's parameters. This is the mechanical bridge between recursion and DP.

**Identify overlapping subproblems:** Draw the recursion tree. If the same `(i, j)` or `(i, remaining)` appears at multiple nodes — add memo.

**Two-step conversion:**
1. Add `memo = {}` (or `@lru_cache`).
2. At function entry: `if state in memo: return memo[state]`.
3. At function exit: `memo[state] = result; return result`.

```python
# Word Break — can s be segmented using words in word_dict?
def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)
    memo  = {}

    def solve(i: int) -> bool:
        if i == len(s):
            return True
        if i in memo:
            return memo[i]
        for j in range(i + 1, len(s) + 1):
            if s[i:j] in words and solve(j):
                memo[i] = True
                return True
        memo[i] = False
        return False

    return solve(0)

# Coin Change — minimum coins to make amount
def coin_change(coins: list[int], amount: int) -> int:
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def solve(remaining: int) -> int:
        if remaining == 0:
            return 0
        if remaining < 0:
            return float('inf')
        return 1 + min(solve(remaining - c) for c in coins)

    result = solve(amount)
    return result if result != float('inf') else -1
```

> [!TIP]
> `@lru_cache(maxsize=None)` is syntactic sugar for the manual `memo` dict. Use it when the function takes only hashable arguments. Clear with `solve.cache_clear()` if called multiple times on different inputs.

> [!CAUTION]
> Memoization only helps when the **same subproblem recurs**. If every call has a unique state (e.g., pure tree DFS where no node is visited twice), memo adds overhead with zero benefit.

**When to stop at memo vs. convert to bottom-up:**
- Memo (top-down): sparse state space, natural recursion structure, easier to derive.
- Bottom-up: dense state space, need to optimize space with rolling arrays, avoid Python recursion limit.

### Recursion Limit in Python

Python default stack limit is 1000 frames. For `n > 1000`, either:

```python
import sys
sys.setrecursionlimit(10**6)   # risky — can crash the interpreter on deep stacks
```

Or convert to iterative (bottom-up DP / explicit stack).

---

## 5. Interview Questions — All Patterns

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
|----------|-------------|------------|----------------------|
| **Subsets** [E] | Every element has include/exclude choice | `solve(i+1, cur+[x])` and `solve(i+1, cur)` | Snapshot `cur[:]` at base; returning without copy gives wrong answer |
| **Subsets II** [M] | Sort + skip duplicate exclude branches | Same as Subsets; add `if j>i and nums[j]==nums[j-1]: continue` | Sort is mandatory; guard only on same recursive level |
| **Permutations** [M] | All orderings of distinct elements | `used[]` array or swap-based; depth = n | Swap-based modifies input — restore swap after recursion |
| **Permutations II** [M] | Duplicate elements → skip at same level | Sort + `not used[i-1]` guard | `not used[i-1]` (not `used[i-1]`) — sibling must be unused, not used |
| **Combinations** [M] | Choose K elements; no order | Pass `start` index to avoid re-using earlier elements | Pruning: `for j in range(start, n-(k-len(cur))+1)` shrinks range |
| **Combination Sum** [M] | Unlimited reuse of elements allowed | Same element can be picked again: recurse with same `i` not `i+1` | Sort + prune: `if candidates[i] > remaining: break` |
| **Combination Sum II** [M] | Each element used once; duplicates in input | Sort + `if j>start and candidates[j]==candidates[j-1]: continue` | Identical to Subsets II guard but with a target sum check |
| **Generate Parentheses** [M] | Validity guard prunes tree | Add `(` if `open<n`; add `)` if `close<open` | No need to store intermediate invalid states; guard is sufficient |
| **Letter Case Permutation** [M] | Branch only when character is alpha | Include lower branch always; upper branch only if `s[i].isalpha()` | Works cleanly with IP/OP: pass char list, join at base |
| **Palindrome Partitioning** [M] | Partition string; each part must be palindrome | At index `i`, try all end positions `j`; check palindrome; recurse | `is_palindrome` check at every split is O(N); overall O(N × 2^N) |
| **Phone Number Letter Combinations** [M] | Each digit maps to letters | For each digit, branch on its mapped characters | Empty input edge case: return `[]` not `[""]` |
| **Word Search** [M] | Backtracking on grid; mark visited | DFS from each cell; mark visited; unmark on backtrack | Mark in-place (`board[r][c] = '#'`); restore after recursion |
| **N-Queens** [H] | One queen per row; prune on col/diag clash | Sets for `cols`, `diag1 = r-c`, `diag2 = r+c` | Bitmask version ~3x faster; anti-diag key is `r+c` not `r-c` |
| **Sudoku Solver** [H] | Fill empty cells; backtrack on conflict | Row/col/box sets; try 1–9 at each empty cell; backtrack on fail | Box index = `(r//3)*3 + c//3` |
| **Different Ways to Add Parentheses** [M] | Split at every operator | `left × right` cartesian product; memo on substring | Same substring recurs — `@lru_cache` or memo dict on string slice |
| **Unique Binary Search Trees II** [M] | Root = each value 1..n; left/right subtrees | `for val in range(lo, hi+1)`: left = solve(lo, val-1), right = solve(val+1, hi) | Empty range returns `[None]` not `[]` (so one "empty tree" option exists) |
| **Tower of Hanoi** [E] | Move n-1 to aux, move disk n to dst, move n-1 to dst | Three-argument recursion; 2^N−1 moves | Minimum moves is exactly 2^N−1; cannot improve |
| **Josephus Problem** [M] | Circular elimination; recursive formula | `f(n, k) = (f(n-1, k) + k) % n`; base `f(1,k)=0` | Answer is 0-based; add 1 for 1-based; `%n` not `%(n-1)` |
| **Pow(x, n)** [M] | Halve exponent each call | `half = pow(x, n//2)`; multiply; handle odd n | Handle `n<0`: invert x and negate n; avoid overflow on `n = INT_MIN` |
| **Expression Evaluation / Basic Calculator** [H] | Recursive descent parser or two-stack | Recursion handles nested `()`; two-stack handles operator precedence | `'+'` resets sign; `'('` triggers recursive call |
| **Decode Ways** [M] | At each index: 1-digit or 2-digit decode | `solve(i) = solve(i+1)` + `solve(i+2)` if valid 2-digit | `'0'` cannot start a valid decode; `"06"` is not `"F"` |
| **Word Break** [M] | Can s be segmented using dict words | Try all prefix lengths at each index; memo on index | Memo is critical — without it, exponential blowup on strings like `"aaaaab"` |
| **Binary Tree Paths** [E] | DFS; record path string at each leaf | Pass `path` string; append `"->"` before each child call | Leaf check: `not node.left and not node.right` |
| **Path Sum II** [M] | All root-to-leaf paths with given sum | DFS; pass `remaining`; record path at leaf when `remaining==node.val` | Must snapshot path (`path[:]`) before appending to result |
| **Diameter of Binary Tree** [M] | Max path length through any node = `lh + rh` | `height()` returns depth; update global `diameter[0]` at each node | Path passes **through** the node — do not confuse with height |
| **Maximum Path Sum** [H] | Max path can start and end anywhere | `gain(node)` returns best single arm; update `best` at each node | Clip negative arms with `max(gain(...), 0)`; missing this breaks on negatives |
| **Flatten Binary Tree** [M] | In-place preorder flattening | Recursive: flatten left and right; stitch left subtree into right slot | Right pointer of leftmost leaf in left subtree connects to old right child |
| **Lowest Common Ancestor** [M] | LCA = first node where p and q diverge | If `root == p or root == q`: return root; combine left/right non-null returns | Works for both BST and general tree (general version shown above) |

---

## Quick Revision Triggers

- If asked for **all subsets / combinations** → Include/Exclude tree; `solve(i+1, cur+[x])` and `solve(i+1, cur)`; snapshot at base.
- If asked for **all permutations** → `used[]` boolean or swap-based; depth = n; sort + `not used[i-1]` guard for duplicates.
- If the recursion tree has **repeated states** (`f(i, w)` seen twice) → add `@lru_cache` immediately; that's top-down DP.
- If the problem is on a **tree** → DFS returning a value; design the return type first (single value vs. tuple); use closure for global answer.
- If the constraint is **hard** (n-queens, sudoku) → add sets for forbidden states; prune before recursing; undo on return.
- If asked to **build a valid string** (parentheses, palindromes) → IP/OP with validity guard; guard replaces explicit backtracking.
- If problem involves **exponentiation or series** → check if it has a clean recurrence (fast-pow: `pow(x, n//2)^2`); mathematical recursion, not decision tree.
- If Python stack blows up (`RecursionError`) → either `sys.setrecursionlimit` (quick fix) or convert to bottom-up DP (proper fix).

---

## See also

**Recursion Sub-files (this folder):**
- [README.md](README.md) — Formal theory and complexity analysis
- [recursion-to-dp.md](recursion-to-dp.md) — Recursion → DP bridge (8 problems)
- [tree-recursion.md](tree-recursion.md) — Advanced tree recursion: BST, LCA, serialize
- [graph-recursion.md](graph-recursion.md) — DFS: flood fill, cycle detection, topo sort
- [combination-problems.md](combination-problems.md) — Full Combination Sum I–IV with code (Pattern 9)
- [string-recursion.md](string-recursion.md) — Regex, wildcard, expression eval (Pattern 10)
- [questions-bank.md](questions-bank.md) — 60 tiered drill questions
- [tips-and-gotchas.md](tips-and-gotchas.md) — 15 bugs, recognition triggers, interview framework

**Related files:**
- [backtracking.md](../backtracking.md) — constraint satisfaction and pruning deep dive
- [dp-aditya-verma.md](../dynamic-programming/dp-aditya-verma.md) — when recursion + memo becomes DP
- [Patterns Master](../../../reference/patterns/patterns-master.md)

