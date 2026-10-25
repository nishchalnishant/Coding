---
module: striver-a2z/26-heaps
lesson: 13
topic: Replace elements by its rank in the array
difficulty: Easy
source: https://takeuforward.org/learning/dsa/replace-elements-by-their-rank?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, sorting, hashing]
---
# 13. Replace elements by its rank in the array

← [Merge K sorted Lists](12-merge-k-sorted-lists.md) · [Part 26 index](README.md) · Next → [Task Scheduler](14-task-scheduler.md)

> [!abstract] Problem at a glance
> **Task:** Replace each element by its rank: 1 for the smallest distinct value, equal values share a rank.
> **Key insight:** Rank = 1 + number of **distinct** values smaller than it. Sort the distinct values once and map each to its position. It's coordinate compression, the same step that precedes Fenwick-tree problems.
> **Difficulty:** Easy · **Pattern:** Coordinate compression · **Also on:** [LC 1331](https://leetcode.com/problems/rank-transform-of-an-array/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/replace-elements-by-their-rank?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 8 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Count smaller distinct values](#3-count-smaller-distinct-values) · [4. Min-heap of (value, index)](#4-min-heap-of-value-index) · [5. Sort distinct values + hash map](#5-sort-distinct-values--hash-map) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `arr`, return an array where each element is replaced by its rank. Ranks start at 1, larger values get larger ranks, equal values get equal ranks, and ranks are as small as possible.

| Input | Output | Why |
|---|---|---|
| `arr = [40,10,20,30]` | `[4,1,2,3]` |  |
| `arr = [100,100,100]` | `[1,1,1]` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`, `−10⁹ ≤ arr[i] ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Count smaller distinct values | for each x: |{y distinct : y < x}| + 1 | O(n·d) | O(d) |
| Min-heap of (value, index) | pop in order; bump rank on a new value | O(n log n) | O(n) |
| Sort distinct values + hash map | rank[v] = index in sorted(set(arr)) + 1 | O(n log n) | O(n) |

> [!tip] Interview angle
> Sort + map is the expected answer. The heap version (pop in order, increment rank when the value changes) is what Striver uses to practise heaps; mention both and that both are O(n log n).

---

## 3. Count smaller distinct values

**Intuition.** Direct from the definition. Quadratic in the worst case.

```python
def rank_brute(arr):
    d = set(arr)
    return [1 + sum(1 for y in d if y < x) for x in arr]
```

**Complexity:** time **O(n·d)**, space **O(d)**.

---

## 4. Min-heap of (value, index)

**Intuition.** Popping a min-heap yields values in sorted order. Keep `rank` and `prev`; when the popped value differs from `prev`, increment rank.

```python
import heapq
def rank_heap(arr):
    h = [(v, i) for i, v in enumerate(arr)]
    heapq.heapify(h)
    out, rank, prev = [0] * len(arr), 0, None
    while h:
        v, i = heapq.heappop(h)
        if v != prev:
            rank, prev = rank + 1, v
        out[i] = rank
    return out
```

**Complexity:** time **O(n log n)**, space **O(n)**.

---

## 5. Sort distinct values + hash map

**Intuition.** Coordinate compression: sorted distinct values get consecutive ranks; look each element up.

**Algorithm**

1. `s = sorted(distinct(arr))`.
2. `rank[s[i]] = i + 1`.
3. Map each element through `rank`.

**Dry run** — [40,10,20,30] → s = [10,20,30,40] → ranks 1..4 → [4,1,2,3].

**C++**
```cpp
vector<int> arrayRankTransform(vector<int> arr) {
    vector<int> s = arr;
    sort(s.begin(), s.end());
    s.erase(unique(s.begin(), s.end()), s.end());
    for (int& x : arr) x = lower_bound(s.begin(), s.end(), x) - s.begin() + 1;
    return arr;
}
```

**Java**
```java
static int[] arrayRankTransform(int[] arr) {
    int[] s = arr.clone();
    Arrays.sort(s);
    Map<Integer, Integer> rank = new HashMap<>();
    for (int x : s) rank.putIfAbsent(x, rank.size() + 1);
    int[] out = new int[arr.length];
    for (int i = 0; i < arr.length; i++) out[i] = rank.get(arr[i]);
    return out;
}
```

**Python**
```python
def array_rank_transform(arr):
    rank = {v: i + 1 for i, v in enumerate(sorted(set(arr)))}
    return [rank[v] for v in arr]
```

**Complexity:** time **O(n log n)**, space **O(n)** — dominated by the sort; lookups are O(1) (or O(log d) with binary search in C++).

---

## Edge cases

- Empty array.
- All equal → all 1.
- Negative and large values (don't use a counting array).

---

## Common mistakes

1. Ranking by sorted index without deduplicating: `[100,100]` would get `[1,2]`.
2. 0-based ranks.

---

## Follow-ups

1. Rank transform of a matrix (LC 1632)?
2. Why compress at all?

<details><summary>Answer sketches</summary>

**#1:** Union-find per row/column for equal values, then process values in increasing order.

**#2:** To index Fenwick/segment trees or count arrays when values are huge but n is small.
</details>

---

## Flashcards

**Rank transform recipe?** #flashcard
Sort distinct values; map value → index + 1.

**Another name for rank transform?** #flashcard
Coordinate compression.

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
