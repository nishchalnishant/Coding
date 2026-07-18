# Complexity Analysis Deep-Dive `⚡ T1`

> Quick-reference tables (constraint → complexity, DS/algo Big-O): [`coding/complexity-cheatsheet.md`](../coding/complexity-cheatsheet.md)

> [!important] Interview Signal
> Saying "O(n log n)" is table stakes. Saying *why* — referencing amortized cost, the master theorem, or auxiliary vs. input space — is what separates L3 from L4.

---

## Section 1: Asymptotic Notation

### Formal Definitions

| Notation | Name | Formal Definition | Practical Read |
| :--- | :--- | :--- | :--- |
| O(f(n)) | Big-O | ∃c>0, n₀: T(n) ≤ c·f(n) ∀n ≥ n₀ | Upper bound — T grows **no faster** than f |
| Ω(f(n)) | Big-Omega | ∃c>0, n₀: T(n) ≥ c·f(n) ∀n ≥ n₀ | Lower bound — T grows **at least** as fast as f |
| Θ(f(n)) | Big-Theta | T(n) = O(f(n)) AND T(n) = Ω(f(n)) | Tight bound — T grows **exactly like** f |
| o(f(n)) | Little-o | lim(n→∞) T(n)/f(n) = 0 | Strictly slower than f (not tight) |
| ω(f(n)) | Little-omega | lim(n→∞) T(n)/f(n) = ∞ | Strictly faster than f (not tight) |

### Common Misconception

> "O is worst case, Ω is best case."

This is **imprecise**. O/Ω/Θ describe *bounds on a function* — they say nothing about which case (best/worst/average) you're analyzing. When engineers say "O(n) worst case," they mean: *on the worst-case input, the runtime function is O(n)*. You can have O(n) best case too.

**Interview phrasing:** *"Merge sort is Θ(n log n) in all cases. Quicksort is O(n²) worst case and O(n log n) average case."*

---

## Section 2: Complexity Hierarchy

| Complexity | Name | Example |
| :--- | :--- | :--- |
| O(1) | Constant | Hash map lookup, array index, stack push |
| O(log n) | Logarithmic | Binary search, balanced BST ops, heap push |
| O(√n) | Root-n | Trial division primality, some number theory |
| O(n) | Linear | Single scan, prefix sum, BFS/DFS |
| O(n log n) | Linearithmic | Merge sort, Timsort, heap sort, FFT |
| O(n²) | Quadratic | Bubble/insertion sort, naïve substring search |
| O(n³) | Cubic | Naïve matrix multiply, Floyd-Warshall (3 loops) |
| O(2ⁿ) | Exponential | Recursive Fibonacci, all subsets, brute-force TSP |
| O(n!) | Factorial | All permutations, brute-force TSP |

### Growth Comparison

| Complexity | n=10 | n=100 | n=1,000 |
| :--- | ---: | ---: | ---: |
| O(1) | 1 | 1 | 1 |
| O(log n) | ~3 | ~7 | ~10 |
| O(√n) | ~3 | 10 | ~32 |
| O(n) | 10 | 100 | 1,000 |
| O(n log n) | ~33 | ~664 | ~9,966 |
| O(n²) | 100 | 10,000 | 1,000,000 |
| O(n³) | 1,000 | 1,000,000 | 10⁹ |
| O(2ⁿ) | 1,024 | 10³⁰ | 10³⁰⁰ |
| O(n!) | 3,628,800 | astronomical | impossible |

**Rule of thumb:** modern CPUs do ~10⁸–10⁹ simple ops/sec. At n=10⁵, O(n²)=10¹⁰ → TLE. At n=10⁶, O(n log n)=2×10⁷ → fine.

---

## Section 3: Amortized Analysis

**Why amortized:** Individual operations may be expensive, but the *average cost per operation over a sequence of N operations* is cheap. Amortized ≠ average case — it's a worst-case guarantee over a sequence.

### Three Methods

#### 1. Aggregate Method
Total cost of N operations / N = amortized cost per op.

**Dynamic array doubling:**
- Capacity doubles: 1 → 2 → 4 → 8 → ... → n
- Copy costs: 1 + 2 + 4 + ... + n/2 = n-1 copies total
- N appends total cost: N (writes) + (n-1) (copies) = O(N)
- Amortized per append: O(N)/N = **O(1)**

#### 2. Accounting Method
Assign artificial "credits" to cheap operations. Credits stored on data structure elements. Expensive operations draw from saved credits.

**Dynamic array (accounting view):**
- Charge each append 3 credits: 1 to write, 2 to save
- On doubling (copy k elements): each element already has 2 saved credits → pays its own copy
- No operation ever goes into debt → amortized O(1) per append

#### 3. Potential Method
Define Φ(state) = potential (stored work). Amortized cost = actual cost + ΔΦ.

- ΔΦ = Φ(state_after) − Φ(state_before)
- If an op is cheap and increases Φ, it stores work for future expensive ops
- Sum of amortized costs = total actual cost + Φ(final) − Φ(initial) ≥ total actual cost (if Φ ≥ 0 always)

### Worked Examples

**Dynamic array (potential method):**
- Φ = 2·(num_elements) − capacity
- Append without resize: actual=1, ΔΦ=+2 → amortized=3=O(1)
- Append with resize to 2k: actual=k+1 (copy k + write 1), ΔΦ = (2·(k+1)−2k) − (2k−k) = 2−k → amortized=k+1+(2−k)=3=O(1)

**Stack with multipop(k):**
- push: O(1) actual — charges 1 credit to element
- pop: O(1) actual — uses element's credit
- multipop(k): O(k) actual — uses k credits from k elements
- Total across N ops: each element is pushed once (1 credit), popped at most once (1 credit used). N pushes → N credits → total O(N). Amortized **O(1)** per op.

**Union-Find with path compression + union by rank:**
- Single op worst case: O(log n)
- Amortized per op: **O(α(n))** where α is the inverse Ackermann function (≤4 for all practical n → effectively O(1))

### Interview Application
> "Python `list.append()` is O(1) **amortized**, not O(1) worst case. Each individual append is O(1) except when the array must double (O(n)), but that happens rarely enough that the average is O(1)."

---

## Section 4: Recurrence Solving

### Substitution Method
1. Guess the closed form (e.g., T(n) = O(n log n))
2. Prove by strong induction: assume T(k) ≤ c·k·log(k) for all k < n, show T(n) ≤ c·n·log(n)

**Merge sort example:** T(n) = 2T(n/2) + n
- Guess T(n) = cn log n
- T(n) = 2c(n/2)log(n/2) + n = cn(log n − 1) + n = cn log n − cn + n ≤ cn log n ✓ (for c ≥ 1)

### Recursion Tree Method
1. Draw the call tree
2. At depth d: subproblem size = n/bᵈ, cost per node = f(n/bᵈ), nodes = aᵈ
3. Sum level costs across all depths

**Binary search T(n) = T(n/2) + 1:**
- Depth d: 1 node, cost 1
- Tree depth = log₂n levels × cost 1 each = **O(log n)**

### Master Theorem

For T(n) = aT(n/b) + f(n), where a ≥ 1, b > 1:

Let **p = log_b(a)** (critical exponent).

| Case | Condition | Solution | Intuition |
| :--- | :--- | :--- | :--- |
| Case 1 | f(n) = O(n^(p−ε)) for ε>0 | T(n) = Θ(nᵖ) | Leaves dominate |
| Case 2 | f(n) = Θ(nᵖ · logᵏn), k≥0 | T(n) = Θ(nᵖ · log^(k+1)n) | Leaves ≈ root, log factor accumulates |
| Case 3 | f(n) = Ω(n^(p+ε)) AND af(n/b) ≤ cf(n) | T(n) = Θ(f(n)) | Root dominates |

**Worked examples:**

| Recurrence | a | b | p=log_b(a) | f(n) | Case | Result |
| :--- | :---: | :---: | :---: | :--- | :---: | :--- |
| Merge sort: 2T(n/2)+n | 2 | 2 | 1 | n = Θ(n¹·log⁰n) | 2 (k=0) | Θ(n log n) |
| Binary search: T(n/2)+1 | 1 | 2 | 0 | 1 = Θ(n⁰·log⁰n) | 2 (k=0) | Θ(log n) |
| Strassen: 7T(n/2)+n² | 7 | 2 | ~2.807 | n² = O(n^(2.807−ε)) | 1 | Θ(n^2.807) |
| 4T(n/2)+n² | 4 | 2 | 2 | n² = Θ(n²) | 2 (k=0) | Θ(n² log n) |
| 3T(n/2)+n² | 3 | 2 | ~1.585 | n² = Ω(n^(1.585+ε)) | 3 | Θ(n²) |

**When Master Theorem doesn't apply:**
- b is not a constant (e.g., T(n) = 2T(n−1) + 1 — subtract, not divide)
- f(n) is not polynomially larger/smaller than nᵖ (e.g., f(n) = nᵖ / log n falls in gap between Case 1 and 2)
- a < 1 or b ≤ 1
- Use substitution or recursion tree in these cases

---

## Section 5: Space Complexity

### Input vs Auxiliary Space

| Term | Definition | Example |
| :--- | :--- | :--- |
| Input space | Space for the input itself | Array of n integers = O(n) |
| Auxiliary space | Extra space beyond input | In-place sort = O(1) auxiliary |
| Total space | Input + auxiliary | Merge sort = O(n) total |

**Interview convention:** When asked for space complexity, report **auxiliary space** unless told otherwise.

### Recursive Call Stack

- Each stack frame = O(1) space (local vars, return addr)
- Depth d frames → O(d) stack space
- Python default recursion limit: 1000 frames

| Algorithm | Call depth | Stack space |
| :--- | :--- | :--- |
| DFS on tree (balanced) | O(log n) | O(log n) |
| DFS on tree (skewed/worst) | O(n) | O(n) |
| DFS on graph | O(V) worst | O(V) |
| Binary search (recursive) | O(log n) | O(log n) |
| Merge sort | O(log n) splits | O(log n) |
| Recursive Fibonacci | O(n) | O(n) |
| Factorial(n) | n | O(n) |

**Key insight:** DFS tree space = O(h) where h = height. Balanced tree: h = O(log n). Linked-list-shaped tree: h = O(n).

### BFS vs DFS Space

| Traversal | Space | Worst case |
| :--- | :--- | :--- |
| DFS (recursive) | O(h) stack | O(n) skewed tree |
| DFS (iterative stack) | O(h) | O(n) |
| BFS (queue) | O(w) where w = max width | O(n) complete binary tree last level |

BFS on a complete binary tree: bottom level has n/2 nodes → queue holds O(n) nodes → **O(n) space**.

### Memoization Space
- Top-down DP: O(states) memo table + O(depth) call stack
- Bottom-up DP: O(states) table, no call stack
- Space-optimized DP: O(1 row) when only previous row needed (e.g., 0/1 knapsack rolling array)

### In-Place Algorithms
- Heapsort: O(1) auxiliary — heap built in-place within input array
- Two-pointer reversal: O(1) auxiliary
- Quicksort: O(log n) auxiliary (call stack for recursion, even "in-place")

---

## Section 6: Common Complexity Mistakes

| Mistake | Wrong | Correct | Why |
| :--- | :--- | :--- | :--- |
| Hash map operations | O(1) | O(1) **amortized average**; O(n) worst | All keys can collide into same bucket |
| Python list append | O(1) | O(1) **amortized**; O(n) worst case | Doubling resize copies all elements |
| Python sort (Timsort) | O(n log n), O(1) space | O(n log n), **O(n) space** | Merge step needs auxiliary buffer |
| String concat in loop | O(n) | **O(n²)** naive; O(n) with `"".join(list)` | Each `s += t` copies entire string |
| Recursive Fibonacci | O(n) | **O(2ⁿ) time**, O(n) space | Exponential repeated subproblems |
| BFS space | O(1) | **O(V)** — queue holds frontier | All nodes at one level can be enqueued |
| Binary search space | O(1) | O(1) iterative; **O(log n)** recursive | Call stack for recursive version |
| DFS space "always O(n)" | O(n) | **O(h)** where h = tree height | Balanced: O(log n), skewed: O(n) |
| Hash set membership | O(1) | O(1) **average**; O(n) worst | Same as hash map collision argument |

### String Concatenation Detail (Python)

```python
# O(n²) total — each += copies full string
result = ""
for s in words:          # n words, avg length L
    result += s          # copies len(result) chars each time

# O(n) total — single join at end
parts = []
for s in words:
    parts.append(s)      # O(1) amortized
result = "".join(parts)  # O(total_length) once
```

---

## Section 7: Quick Derivation Cheatsheet

### Algorithm → Recurrence → Solution

| Algorithm | Recurrence | Master Case | Result |
| :--- | :--- | :--- | :--- |
| Merge sort | T(n) = 2T(n/2) + O(n) | Case 2 (k=0) | O(n log n) |
| Binary search | T(n) = T(n/2) + O(1) | Case 2 (k=0) | O(log n) |
| Quicksort (avg) | T(n) = 2T(n/2) + O(n) | Case 2 (k=0) | O(n log n) |
| Quicksort (worst) | T(n) = T(n−1) + O(n) | N/A (subtract) | O(n²) |
| Strassen multiply | T(n) = 7T(n/2) + O(n²) | Case 1 | O(n^2.807) |
| Karatsuba multiply | T(n) = 3T(n/2) + O(n) | Case 1 | O(n^1.585) |
| Heap build | — (not recurrence) | — | O(n) aggregate |
| Recursive fib (no memo) | T(n) = T(n−1) + T(n−2) | N/A | O(2ⁿ) |

### Constraint → Expected Complexity

| Constraint | Target complexity | Typical algorithms |
| :--- | :--- | :--- |
| n ≤ 10–15 | O(2ⁿ) or O(n!) | Backtracking, brute-force permutations |
| n ≤ 20 | O(2ⁿ) | Bitmask DP, meet-in-the-middle |
| n ≤ 200 | O(n³) | Floyd-Warshall, 3-nested-loop DP |
| n ≤ 3,000 | O(n²) | O(n²) DP (LCS, edit distance naïve), bubble sort |
| n ≤ 10⁴ | O(n² log n) stretch | — |
| n ≤ 10⁵ | O(n log n) | Merge sort, heap, binary search in loop |
| n ≤ 10⁶ | O(n) or O(n log n) | Linear scan, hash map, BFS/DFS |
| n ≤ 10⁷ | O(n) strict | Counting sort, two-pointer, prefix sum |
| n ≤ 10⁸+ | O(log n) or O(1) | Binary search on answer, math formula |

### Deriving Complexity on the Fly

1. **Count nested loops:** k nested loops over n → O(nᵏ)
2. **Halving at each step** → O(log n)
3. **Recursion with branching factor b, depth d** → O(bᵈ) nodes total
4. **Work at each level constant across levels** → multiply depth × work per level
5. **Sum over all nodes in recursion tree** → use geometric series if needed
