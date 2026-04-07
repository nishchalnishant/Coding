# Sorting

Arranging data in a specific order to optimize subsequent operations (like searching or merging).

## Big-O Overview
| Algorithm      | Average Time | Worst Time | Space | Stable? | Best Used For |
| -------------- | ------------ | ---------- | ----- | ------- | ------------- |
| **Bubble** | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes | Educational only |
| **Insertion** | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes | Nearly sorted or tiny arrays |
| **Merge Sort** | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | Yes | Linked Lists, guaranteed $N \log N$ |
| **Quick Sort** | $O(N \log N)$ | $O(N^2)$ | $O(\log N)$| No | Large arrays in-memory (fastest practically) |
| **Heap Sort** | $O(N \log N)$ | $O(N \log N)$ | $O(1)$ | No | $O(1)$ space requirement with $O(N \log N)$ guarantee |
| **Counting** | $O(N + K)$| $O(N + K)$ | $O(K)$ | Yes | Small integer ranges |
| **Radix** | $O(d(N+b))$| $O(d(N+b))$| $O(N+b)$| Yes | Fixed-width keys or digit processing |

## Core Techniques

SDE-2 reference implementations (Python): `../../google-sde2/snippets/python/sorting.py`.

- **Merge Process**: Two-pointer iteration to combine two sorted structures in $O(N)$ time.
- **Partitioning (QuickSort)**: Choosing a pivot and placing all smaller elements to the left, larger to the right. Use the Dutch National Flag algorithm for 3-way partitioning.
- **Top K Elements (QuickSelect)**: A variation of QuickSort that only recurses into the partition containing the target rank $K$. Average time $O(N)$.
- **Custom Comparators**: Implement custom sorting logic when dealing with complex objects or intervals (e.g., sort intervals by start time).

## Common SDE-3 Sorting Problems
- *Easy*: Merge Sorted Array, Squares of a Sorted Array, Valid Anagram (by sorting).
- *Medium*: Sort Colors (Dutch National Flag), Merge Intervals, Sort List, Top K Frequent Elements (Bucket sort).
- *Hard*: Count Inversions, Maximum Gap (Pigeonhole principle), Optimal Account Balancing.

---

## Pattern Recognition

- **Need sorted order** → Merge sort (stable, O(N log N) guaranteed), Quick sort (in-place, average O(N log N)), or library sort.
- **Linked list sort** → Merge sort (O(1) space with pointer rewiring; no random access for quick sort).
- **Top K / Kth largest** → QuickSelect (average O(N)) or heap of size K (O(N log K)).
- **Small integer range** → Counting sort O(N + K). **Fixed-width keys** → Radix sort.
- **Intervals** → Sort by start or end; then merge or sweep.

## Interview Strategy

- **Identify**: "Sort" requirement → choose by stability, space, and data structure (array vs list). "Kth largest" → QuickSelect or heap.
- **Approach**: State why you chose the algorithm (e.g. "Merge sort for linked list because we need O(1) extra space and stable sort"). For custom order, define comparator.
- **Common mistakes**: Wrong comparator (off-by-one or wrong field); forgetting to handle duplicates; QuickSelect partition logic.

## Quick Revision

- **Merge sort**: Split mid, sort halves, merge with two pointers. T(N) = 2T(N/2) + O(N) = O(N log N). Stable.
- **Quick sort**: Partition around pivot (e.g. last); recurse left and right. Average O(N log N); worst O(N²). QuickSelect: recurse only the partition that contains rank K.
- **Stable**: Merge, insertion, counting, radix. **Unstable**: Quick, heap. **In-place**: Quick (stack O(log N)), heap, insertion.

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness & details |
|----------|------------|----------------------|
| **Merge Intervals** | Sort by **start**; sweep: if overlap with last (`curr.start <= last.end`), merge `end = max(...)`; else append. | **Contained** intervals; **sort by end** for “max non-overlapping” / meeting room variants. |
| **Meeting Rooms II** | Sort starts; **min-heap** of **end** times of ongoing meetings; pop ended, push new end. | Answers **min rooms** = max overlap; **wrong:** one pass without heap. |
| **Sort Colors (DNF)** | Three pointers: `0..low-1` are 0s, `low..mid-1` are 1s, `mid..high` unknown, `high+1..` are 2s. | Only **`mid++`** when swap with `low`; **swap with high** without mid++. |
| **Kth Largest Element** | **QuickSelect** partition until pivot at `n-k`; or **min-heap** of size k. | **k** from largest vs smallest; **QuickSelect** worst O(n²)—randomized pivot helps. |
| **Merge Sorted Array** | Merge into `nums1` **from the end** using pointers `i=m-1, j=n-1, k=m+n-1`. | **Overwrite** risk if merge front; **trailing** zeros in nums1. |
| **Largest Number** | Sort digit strings with **`cmp(a,b) = (a+b) vs (b+a)`**. | **All zeros** → single `"0"`; comparator must define **strict weak ordering**. |
| **Reorder Log Files** | Letter-logs: sort by **content**, then **identifier**; digit-logs keep **relative order** after letter-logs. | **Custom** key extraction; **stable** partition between letter vs digit logs. |
| **H-Index** | After **sort desc**, find max `i` with `citations[i] >= i+1`; or **counting bucket** O(n). | **h** papers with **≥ h** citations each; index vs count off-by-one. |
| **Insert Interval** | Insert new interval into sorted list: **merge once** with neighbors. | **Binary search** insert position; **merge** left and right expansions. |

---

## See also

- [Greedy](greedy.md) — sort first, then greedy scan  
- [Divide and Conquer](divide-and-conquer.md) — merge sort, quicksort  
- [Heap](../data-structures/heap.md) — heap sort
