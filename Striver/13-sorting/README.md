---
module: striver/13-sorting
topic: Sorting
tags: [striver, algorithms]
---
# Part 13: Sorting

← [Striver course map](../README.md)

> [!abstract] What this part covers
> **Goal:** Implement the five classic sorts from memory, with their recursive variants, and state each one's best/average/worst time, space, stability and when it's the right choice.
> **Prereqs:** [Basic Recursion](../12-basic-recursion/README.md) (merge sort, quick sort, and the recursive variants are recursion). **Time:** ~5 h.
> **Outcome:** You can write merge sort and quick sort bug-free in under 10 minutes each, explain why comparison sorting is Ω(n log n), and reuse `merge` and `partition` as building blocks (inversion count, k-th element, Dutch flag).

---

## Theory

| # | Lesson | What you get | Source |
|---|---|---|---|
| 0 | [Sorting Theory](00-sorting-theory.md) | Stability/in-place/adaptive properties, full comparison table, the Ω(n log n) lower bound, counting/radix/bucket sort, library sorts and comparators, sort-first patterns and a chooser flowchart. | [link](https://takeuforward.org/learning/dsa/selection-sort?category=sorting-techniques&source=strivers-a2z-dsa-sheet) |

Read these first; the problems below apply them.

---

## Problems

| # | Problem | Difficulty | Key insight | Optimal | Source |
|---|---|---|---|---|---|
| 1 | [Selection Sort](01-selection-sort.md) | Easy | For each position `i`, find the minimum of the unsorted suffix `[i, n)` and swap it into `i`. After pass `i` the prefix `[0, i]` is final, so there are n − 1 passes and at most n − 1 swaps. | O(n²) in every case | [link](https://takeuforward.org/learning/dsa/selection-sort?category=algorithms&source=strivers-a2z-dsa-sheet) |
| 2 | [Bubble Sort](02-bubble-sort.md) | Easy | Each pass swaps adjacent out-of-order pairs, which carries the largest unsorted element to the end. If a pass makes no swap, the array is sorted, so the `swapped` flag gives O(n) on sorted input. | O(n²) worst / avg, O(n) best | [link](https://takeuforward.org/learning/dsa/bubble-sort?category=algorithms&source=strivers-a2z-dsa-sheet) |
| 3 | [Insertion Sort](03-insertion-sort.md) | Easy | Grow a sorted prefix: take `key = nums[i]`, shift every larger element of `[0, i)` one step right, and drop `key` into the gap. The cost is O(n + inversions), so it's O(n) on nearly sorted data. | O(n²) worst / avg, O(n) best | [link](https://takeuforward.org/learning/dsa/insertion-sorting?category=algorithms&source=strivers-a2z-dsa-sheet) |
| 4 | [Merge Sort](04-merge-sort.md) | Medium | Split in half, sort each half recursively, then merge the two sorted halves in O(n) with two pointers. The recursion tree has log n levels and each level does O(n) merge work, so it's O(n log n) in every case. | O(n log n) best / avg / worst | [link](https://takeuforward.org/learning/dsa/merge-sorting?category=algorithms&source=strivers-a2z-dsa-sheet) |
| 5 | [Quick Sort](05-quick-sort.md) | Medium | Partition around a pivot so that everything ≤ pivot is on its left and everything greater is on its right; the pivot is then in its final position. Recurse on both sides. A good pivot gives O(n log n) and in-place sorting; a bad one on sorted input gives O(n²). | O(n log n) avg / best, O(n²) worst (rare with random pivot) | [link](https://takeuforward.org/learning/dsa/quick-sorting?category=algorithms&source=strivers-a2z-dsa-sheet) |
| 6 | [Recursive Bubble Sort](06-recursive-bubble-sort.md) | Easy | One pass over `[0, n)` puts the maximum at index `n − 1`; then sort the first `n − 1` recursively. Base: `n ≤ 1`. If a pass made no swaps, return early. | O(n²) worst, O(n) best | [link](https://takeuforward.org/learning/dsa/recursive-bubble-sort?category=algorithms&source=strivers-a2z-dsa-sheet) |
| 7 | [Recursive Insertion Sort](07-recursive-insertion-sort.md) | Easy | To sort `[0, n)`: sort `[0, n − 1)` recursively, then insert `nums[n − 1]` into that sorted prefix. Equivalently, go forward: insert `nums[i]`, then call `f(i + 1)`. | O(n²) worst, O(n) best | [link](https://takeuforward.org/learning/dsa/recursive-insertion-sort?category=algorithms&source=strivers-a2z-dsa-sheet) |

---

## Which sort, when

```mermaid
flowchart TD
    S[Need to sort] --> Q1{n small, ≤ ~20, or nearly sorted?}
    Q1 -->|yes| INS["Insertion sort<br/>O(n) best, stable, in place"]
    Q1 -->|no| Q2{Need stability or a guaranteed O(n log n)?}
    Q2 -->|yes| MS["Merge sort<br/>O(n log n) always, stable, O(n) extra"]
    Q2 -->|"no, want in place and fast on average"| QS["Quick sort<br/>O(n log n) avg, O(n²) worst, O(log n) stack"]
    S --> Q3{Values are small integers?}
    Q3 -->|yes| CS["Counting / bucket sort<br/>O(n + k), not comparison-based"]
    SEL["Selection sort: fewest swaps, n − 1"] -.-> NOTE["Selection and bubble: teaching only"]
    BUB["Bubble sort: O(n) best with the swapped flag"] -.-> NOTE
```

---

## Part 13 cheat sheet

| Sort | Best | Average | Worst | Extra space | Stable | In place | Core move |
|---|---|---|---|---|---|---|---|
| Selection | O(n²) | O(n²) | O(n²) | O(1) | ✗ | ✓ | put the min of `[i..n)` at `i` |
| Bubble | O(n) with flag | O(n²) | O(n²) | O(1) | ✓ | ✓ | swap adjacent inversions; max bubbles to the end |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | ✓ | ✓ | shift larger elements right, drop `key` in |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) + O(log n) stack | ✓ | ✗ | split in half, merge two sorted halves |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) stack avg | ✗ | ✓ | partition around a pivot, recurse on both sides |
| Counting | O(n + k) | O(n + k) | O(n + k) | O(k) | ✓ | ✗ | tally values 0..k |

**Facts interviewers test:** comparison sorts need Ω(n log n) comparisons (a decision tree with n! leaves has height log₂ n!). Insertion sort's running time is O(n + inversions). Selection sort makes at most n − 1 swaps. Quick sort's worst case comes from a bad pivot on sorted input; a random pivot gives expected O(n log n). Library sorts: C++ `std::sort` is introsort (not stable, `stable_sort` is merge-based); Java `Arrays.sort` is dual-pivot quicksort for primitives and TimSort for objects; Python `sorted` is TimSort (stable).

---

## Mastery checklist

- [ ] Write all five sorts from memory, in place, on `nums`
- [ ] Dry-run one pass of each on `[5, 1, 4, 2, 8]`
- [ ] Explain the bubble-sort `swapped` flag and insertion sort's O(n) best case
- [ ] Write `merge(l, m, r)` with `<=`, and say why `<=` keeps it stable
- [ ] Write a `partition` that never runs out of bounds, and the random-pivot fix
- [ ] State the stable / in-place / worst-case profile of each sort without notes
- [ ] Convert bubble and insertion sort to recursion and back

**Interview track →** [Sorting deep-dive](../../02-algorithms/00-sorting.md) · [Sorting walkthroughs](../../coding/algorithms/00-sorting.md)

Next part → [Arrays](../14-arrays/README.md)
