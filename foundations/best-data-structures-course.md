# Best Data Structures Course — Notes

Notes from a data structures course. Use as a **supplement** to the main topic files in [data-structures/](data-structures/README.md) and [algorithms/](algorithms/README.md).

---

## S01E01: Algorithms, Time Complexity, Merge Sort

### What is an algorithm and how to measure efficiency?

- **Algorithm**: A well-defined procedure: given input data, produce the intended output.
- **Efficiency**: Measured by **time complexity** — how the number of **operations** grows with input size, not wall-clock time (which depends on hardware).
- **Big O**: Upper bound on growth. For example, \(O(n)\) means the number of operations is at most \(C \cdot g(n)\) for large \(n\) (e.g. \(g(n) = n\) for linear).

### Time complexity for recursive algorithms

Recurrence relation describes the work. Example: a function that just recurses \(n\) times does \(O(n)\) work.

```python
def f(n):
    if n == 0:
        return
    f(n - 1)
```

- Base case: \(n = 0\) → constant work.
- Recursive step: one call with \(n - 1\). Total calls: \(n\), so time is \(O(n)\).

For more complex recurrences (e.g. merge sort \(T(n) = 2T(n/2) + O(n)\)), use the **Master Theorem** or expansion. See [algorithms/divide-and-conquer.md](algorithms/divide-and-conquer.md).

---

## Going further

- **Merge sort**: See [algorithms/sorting.md](algorithms/sorting.md) and [algorithms/divide-and-conquer.md](algorithms/divide-and-conquer.md).
- **Full DSA coverage**: Use [data-structures/](data-structures/README.md) and [algorithms/](algorithms/README.md) for SDE-3 level content.

---

## Interview Questions — Logic & Trickiness (complexity)

| Question style | Core logic | Trickiness & details |
|----------------|------------|----------------------|
| **Master theorem** `T(n)=aT(n/b)+f(n)` | Compare `n^(log_b a)` to `f(n)`: **case 1** leaf-heavy, **case 2** balanced, **case 3** root-heavy (regularity cond.). | State **`a,b`** and **`f(n)`** explicitly; **floors/ceilings** in `n/b` often ignored in interviews. |
| **`T(n)=2T(n/2)+n`** | Case 2: `n^(log_2 2)=n` matches `f(n)=n` → **Θ(n log n)**. | **Same** as merge sort recurrence. |
| **`T(n)=T(n/2)+O(1)`** | Height of recursion tree **log n** → **O(log n)** (binary search). | **Vs** `T(n)=T(n/2)+O(n)` → **O(n)** total. |
| **Compare O(n log n) sorts** | **Merge:** stable, **O(n)** extra space, worst **O(n log n)**. **Heap:** in-place, not stable. **Quick:** in-place avg **O(n log n)**, worst **O(n²)** without pivot tricks. | **Stable** needed for key-value round-trip; **external** sort favors merge. |
| **Why not O(n) sort always?** | **Comparison** sorts have **Ω(n log n)** lower bound. **Counting/radix/bucket** need **bounded key range** or structure. | **Integer** keys in small range → counting O(n+k). |
| **Amortized vs worst** | **Dynamic array** push amortized O(1); **hash table** rehash rare. | **Single** operation can be O(n); **aggregate** analysis. |
| **Space recursion** | Tree depth **h** → **O(h)** stack; skewed tree **O(n)**. | **Tail recursion** not optimized in Python; **iterative** DFS with explicit stack. |

---

## See also

- [algorithms/sorting.md](algorithms/sorting.md) — merge sort and complexity  
- [algorithms/divide-and-conquer.md](algorithms/divide-and-conquer.md) — merge sort recurrence
