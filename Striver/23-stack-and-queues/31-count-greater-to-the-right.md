---
module: striver/23-stack-and-queues
lesson: 31
topic: Number of Greater Elements to the Right
difficulty: Medium
source: https://takeuforward.org/learning/dsa/number-of-greater-elements-to-the-right?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, array, merge-sort, counting]
---
# 31. Number of Greater Elements to the Right

← [LFU Cache](30-lfu-cache.md) · [Part 23 index](README.md) · Next → [Part 24: Binary Trees](../24-binary-trees/README.md)

> [!abstract] Problem at a glance
> **Task:** For each queried index `i`, count elements to the right of `i` that are strictly greater than `arr[i]`.
> **Key insight:** Unlike NGE, a monotonic stack doesn't help here: you need a **count**, not the nearest one. Per query it's an O(n) scan. To answer all indices at once, use **merge sort**: when merging two sorted halves and placing a left element `x`, every remaining right element is `> x`, so add their count to `x`'s answer.
> **Difficulty:** Medium · **Pattern:** Brute force / merge-sort counting · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/number-of-nges-to-the-right/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/number-of-greater-elements-to-the-right?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Scan right per query](#3-scan-right-per-query) · [4. Merge-sort counting for all indices](#4-merge-sort-counting-for-all-indices) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `arr` and a list of query `indices`, return for each query `i` the number of `j > i` with `arr[j] > arr[i]`.

| Input | Output | Why |
|---|---|---|
| `arr = [3,4,2,7,5,8,10,6], indices = [0,5]` | `[6,1]` | right of 3: 4,7,5,8,10,6; right of 8: 10 |

**Constraints:** `1 ≤ n ≤ 10⁴`; `1 ≤ q ≤ 100` (GfG). The merge-sort approach also handles `q = n`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Scan right per query | count arr[j] > arr[i] for j > i | O(n·q) | O(1) extra |
| Merge-sort counting for all indices | on merge, left x gains (#remaining right) | O(n log n + q) | O(n) |

> [!tip] Interview angle
> The sheet places this here to test whether you'll wrongly reach for a monotonic stack. Say why it fails: popped elements still count for future queries. With few queries, brute force is optimal (O(n·q)). For all indices, this is 'count of greater elements on the right', the mirror of LC 315, solved with merge sort or a BIT.

---

## 3. Scan right per query

**Intuition.** For each query, one pass over the suffix.

```python
def count_nge_brute(arr, indices):
    return [sum(1 for j in range(i + 1, len(arr)) if arr[j] > arr[i]) for i in indices]
```

**Complexity:** time **O(n·q)**, space **O(1) extra**.

---

## 4. Merge-sort counting for all indices

**Intuition.** Sort an array of indices by value with merge sort. Every pair `(i, j)` with `i < j` is in a left half and a right half at exactly one merge. When the left element `x` is placed, the right elements still unplaced are exactly those `> x` (we place a right element first whenever it is `≤ x`). Adding `hi − j` to `cnt[x]` counts every such pair once.

**Algorithm**

1. `idx = [0…n−1]`, `cnt = [0]·n`.
2. Merge-sort `idx` by value. In the merge, if `arr[R[j]] ≤ arr[L[i]]` take the right one; else `cnt[L[i]] += (#right remaining)` and take the left one.
3. Return `cnt[q]` for each query.

**Dry run** — [3,4,2,7]: merge [3]|[4] → 3 gains 1. [2]|[7] → 2 gains 1. Merge [3,4]|[2,7]: 2 ≤ 3 → take 2; 3 < 7 → 3 gains 1; 4 < 7 → 4 gains 1; take 7. cnt = [2,1,1,0].

**C++**
```cpp
void msort(const vector<int>& a, vector<int>& idx, vector<int>& cnt, int lo, int hi) {
    if (hi - lo <= 1) return;
    int mid = (lo + hi) / 2;
    msort(a, idx, cnt, lo, mid);
    msort(a, idx, cnt, mid, hi);
    vector<int> merged;
    int i = lo, j = mid;
    while (i < mid && j < hi) {
        if (a[idx[j]] <= a[idx[i]]) merged.push_back(idx[j++]);
        else { cnt[idx[i]] += hi - j; merged.push_back(idx[i++]); }
    }
    while (i < mid) merged.push_back(idx[i++]);
    while (j < hi) merged.push_back(idx[j++]);
    copy(merged.begin(), merged.end(), idx.begin() + lo);
}
vector<int> countNGE(vector<int> arr, vector<int> indices) {
    int n = arr.size();
    vector<int> idx(n), cnt(n, 0), ans;
    iota(idx.begin(), idx.end(), 0);
    msort(arr, idx, cnt, 0, n);
    for (int q : indices) ans.push_back(cnt[q]);
    return ans;
}
```

**Java**
```java
static void msort(int[] a, int[] idx, int[] cnt, int lo, int hi) {
    if (hi - lo <= 1) return;
    int mid = (lo + hi) / 2;
    msort(a, idx, cnt, lo, mid);
    msort(a, idx, cnt, mid, hi);
    int[] merged = new int[hi - lo];
    int i = lo, j = mid, k = 0;
    while (i < mid && j < hi) {
        if (a[idx[j]] <= a[idx[i]]) merged[k++] = idx[j++];
        else { cnt[idx[i]] += hi - j; merged[k++] = idx[i++]; }
    }
    while (i < mid) merged[k++] = idx[i++];
    while (j < hi) merged[k++] = idx[j++];
    System.arraycopy(merged, 0, idx, lo, merged.length);
}
static int[] countNGE(int[] arr, int[] indices) {
    int n = arr.length;
    int[] idx = new int[n], cnt = new int[n], ans = new int[indices.length];
    for (int i = 0; i < n; i++) idx[i] = i;
    msort(arr, idx, cnt, 0, n);
    for (int t = 0; t < indices.length; t++) ans[t] = cnt[indices[t]];
    return ans;
}
```

**Python**
```python
def count_nge(arr, indices):
    n = len(arr)
    idx, cnt = list(range(n)), [0] * n
    def msort(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        msort(lo, mid)
        msort(mid, hi)
        merged, i, j = [], lo, mid
        while i < mid and j < hi:
            if arr[idx[j]] <= arr[idx[i]]:
                merged.append(idx[j]); j += 1
            else:
                cnt[idx[i]] += hi - j
                merged.append(idx[i]); i += 1
        merged += idx[i:mid] + idx[j:hi]
        idx[lo:hi] = merged
    msort(0, n)
    return [cnt[q] for q in indices]
```

**Complexity:** time **O(n log n + q)**, space **O(n)** — standard merge sort, O(n) extra work per level.

---

## Edge cases

- Last index: always 0.
- Equal values aren't greater.
- Duplicate queries.

---

## Common mistakes

1. Using a monotonic stack: popped elements are lost but still count for earlier indices.
2. Counting `≥` instead of `>` (take the right element on `≤` to keep it strict).
3. Losing original positions by sorting values instead of indices.

---

## Follow-ups

1. Count of smaller elements to the right (LC 315)?
2. Count inversions?

<details><summary>Answer sketches</summary>

**#1:** Same merge with the roles flipped, or a BIT over compressed values.

**#2:** Sum of 'smaller to the right' over all i; one counter instead of per-index.
</details>

---

## Flashcards

**Why doesn't a monotonic stack solve 'count of greater elements to the right'?** #flashcard
It discards dominated elements, but a count needs every greater element, not just the nearest.

**Merge-sort counting: when do you add to a left element's count?** #flashcard
When placing it; add the number of right elements still unplaced (all are greater).

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
