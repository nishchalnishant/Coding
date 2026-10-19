---
module: striver/26-heaps
lesson: 18
topic: Maximum Sum Combination
difficulty: Medium
source: https://takeuforward.org/learning/dsa/maximum-sum-combination?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, best-first, top-k]
---
# 18. Maximum Sum Combination

← [Minimum cost to connect sticks](17-minimum-cost-to-connect-sticks.md) · [Part 26 index](README.md) · Next → [Find Median from Data Stream](19-find-median-from-data-stream.md)

> [!abstract] Problem at a glance
> **Task:** Given arrays `A`, `B` (size n each) and `K`, return the `K` largest sums `A[i] + B[j]` over all index pairs, in descending order.
> **Key insight:** Sort both descending. The sums form a grid that decreases along every row and column, so `(0,0)` is the max and the next candidate is always a neighbour `(i+1, j)` or `(i, j+1)` of something already taken. Expand best-first with a max-heap and a **visited set** so no cell is pushed twice: O(K log K).
> **Difficulty:** Medium · **Pattern:** Best-first expansion over a sorted grid
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/maximum-sum-combination?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. All sums, sort](#3-all-sums-sort) · [4. Max-heap best-first + visited](#4-max-heap-best-first--visited) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given integer arrays `A` and `B` and `K ≤ |A|·|B|`, return the K maximum values of `A[i] + B[j]` (pairs of indices, so equal sums may repeat), sorted in non-increasing order.

| Input | Output | Why |
|---|---|---|
| `A = [1,4,2,3], B = [2,5,1,6], K = 4` | `[10,9,9,8]` | 4+6, 4+5, 3+6, 3+5 |
| `A = [3,2], B = [1,4], K = 2` | `[7,6]` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, `1 ≤ K ≤ n`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| All sums, sort | n² sums, sort descending, take K | O(n² log n) | O(n²) |
| Max-heap best-first + visited | pop (i,j); push (i+1,j), (i,j+1) if unseen | O(n log n + K log K) | O(K) |

> [!tip] Interview angle
> This is the same engine as LC 373 (k smallest pairs) and k-th smallest in a sorted matrix. Explain why the visited set is needed: `(1,1)` is reachable from both `(0,1)` and `(1,0)`. The alternative is LC 373's trick of seeding row heads and only moving right.

---

## 3. All sums, sort

**Intuition.** Materialise the whole grid. Fails the constraints for n = 10⁵.

```python
def msc_brute(A, B, K):
    return sorted((a + b for a in A for b in B), reverse=True)[:K]
```

**Complexity:** time **O(n² log n)**, space **O(n²)**.

---

## 4. Max-heap best-first + visited

**Intuition.** After sorting descending, `A[i]+B[j]` dominates everything below and right of it. A popped cell's only new candidates are its right and down neighbours. Each pop adds at most two cells, so the heap stays O(K).

**Algorithm**

1. Sort A and B descending.
2. Push `(A[0]+B[0], 0, 0)`; mark `(0,0)` visited.
3. Repeat K times: pop `(s, i, j)`, append `s`; push `(i+1, j)` and `(i, j+1)` if in bounds and unvisited.

**Dry run** — A = [4,3,2,1], B = [6,5,2,1]. Pop 10 (0,0) → push 9 (1,0), 9 (0,1). Pop 9, pop 9 → pushes 8 (2,0), 8 (1,1), 6 (0,2). Pop 8 → [10,9,9,8].

**C++**
```cpp
vector<int> maxSumCombination(vector<int> A, vector<int> B, int K) {
    sort(A.rbegin(), A.rend());
    sort(B.rbegin(), B.rend());
    int n = A.size(), m = B.size();
    priority_queue<tuple<int, int, int>> pq;
    set<pair<int, int>> seen;
    pq.push({A[0] + B[0], 0, 0});
    seen.insert({0, 0});
    vector<int> res;
    while ((int)res.size() < K) {
        auto [s, i, j] = pq.top(); pq.pop();
        res.push_back(s);
        if (i + 1 < n && seen.insert({i + 1, j}).second) pq.push({A[i + 1] + B[j], i + 1, j});
        if (j + 1 < m && seen.insert({i, j + 1}).second) pq.push({A[i] + B[j + 1], i, j + 1});
    }
    return res;
}
```

**Java**
```java
static int[] maxSumCombination(int[] A, int[] B, int K) {
    Integer[] a = Arrays.stream(A).boxed().sorted(Collections.reverseOrder()).toArray(Integer[]::new);
    Integer[] b = Arrays.stream(B).boxed().sorted(Collections.reverseOrder()).toArray(Integer[]::new);
    int n = a.length, m = b.length;
    PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> Integer.compare(y[0], x[0]));
    Set<Long> seen = new HashSet<>();
    pq.offer(new int[]{a[0] + b[0], 0, 0});
    seen.add(0L);
    int[] res = new int[K];
    for (int t = 0; t < K; t++) {
        int[] e = pq.poll();
        res[t] = e[0];
        int i = e[1], j = e[2];
        if (i + 1 < n && seen.add((long) (i + 1) * m + j)) pq.offer(new int[]{a[i + 1] + b[j], i + 1, j});
        if (j + 1 < m && seen.add((long) i * m + j + 1)) pq.offer(new int[]{a[i] + b[j + 1], i, j + 1});
    }
    return res;
}
```

**Python**
```python
import heapq
def max_sum_combination(A, B, K):
    A, B = sorted(A, reverse=True), sorted(B, reverse=True)
    h, seen, res = [(-(A[0] + B[0]), 0, 0)], {(0, 0)}, []
    while len(res) < K:
        s, i, j = heapq.heappop(h)
        res.append(-s)
        for ni, nj in ((i + 1, j), (i, j + 1)):
            if ni < len(A) and nj < len(B) and (ni, nj) not in seen:
                seen.add((ni, nj))
                heapq.heappush(h, (-(A[ni] + B[nj]), ni, nj))
    return res
```

**Complexity:** time **O(n log n + K log K)**, space **O(K)** — K pops, ≤ 2K pushes, heap size ≤ K + 1.

---

## Edge cases

- K = n·m (entire grid).
- Duplicate values produce equal sums from different index pairs; all of them count.
- Negative numbers.

---

## Common mistakes

1. No visited set: the same cell gets pushed twice and its sum is reported twice.
2. Deduplicating by **sum** instead of by index pair, which drops legitimate repeats.
3. Forgetting to sort descending (the grid monotonicity is what makes best-first correct).

---

## Follow-ups

1. K smallest pairs (LC 373)?
2. K-th smallest in a row/column-sorted matrix (LC 378)?

<details><summary>Answer sketches</summary>

**#1:** Sort ascending (already sorted), min-heap; seed `(i, 0)` for i < K and only move right, so no visited set is needed.

**#2:** Same best-first, or binary search on the value with a staircase count.
</details>

---

## Flashcards

**Top-K pair sums: why a visited set?** #flashcard
Cell (i+1, j+1) is reachable from two parents.

**Top-K pair sums complexity?** #flashcard
O(n log n + K log K).

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
