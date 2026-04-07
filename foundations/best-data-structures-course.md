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

| Question style | Core logic | Trickiness |
|----------------|------------|------------|
| **What is T(n) for f(n)=2f(n/2)+n?** | Master theorem case 2 → O(n log n) | State a,b,f(n) |
| **Compare O(n log n) sorts** | Merge stable O(n) space; quick in-place | Worst case quick O(n²) |
| **Why not O(n) sort always?** | Comparison lower bound Ω(n log n); counting needs bounded keys | Problem constraints |

---

## See also

- [algorithms/sorting.md](algorithms/sorting.md) — merge sort and complexity  
- [algorithms/divide-and-conquer.md](algorithms/divide-and-conquer.md) — merge sort recurrence
