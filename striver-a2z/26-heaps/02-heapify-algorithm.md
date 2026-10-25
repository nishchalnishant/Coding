---
module: striver-a2z/26-heaps
lesson: 2
topic: Heapify Algorithm
difficulty: Medium
source: https://takeuforward.org/learning/dsa/heapify-algorithm?category=theory-and-implementation&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, array]
---
# 2. Heapify Algorithm

← [Heaps: Array Layout, Sift Operations, Build-Heap and Priority Queues](01-heap-theory.md) · [Part 26 index](README.md) · Next → [Build heap from a given Array](03-build-heap-from-a-given-array.md)

> [!abstract] Problem at a glance
> **Task:** In a min-heap array, set `nums[ind] = val` and restore the heap property in O(log n).
> **Key insight:** A single changed key is wrong in only one direction. If it got **smaller** it can only conflict with its parent, so sift **up**. If it got **larger** it can only conflict with its children, so sift **down**. One of the two loops does nothing.
> **Difficulty:** Medium · **Pattern:** Heap repair: sift up / sift down
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/heapify-algorithm?category=theory-and-implementation&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Rebuild the whole heap](#3-rebuild-the-whole-heap) · [4. Sift up or sift down from `ind`](#4-sift-up-or-sift-down-from-ind) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

You are given `nums`, a valid min-heap stored as an array (children of `i` at `2i+1`, `2i+2`). Replace `nums[ind]` by `val` and rearrange `nums` in place so it is again a min-heap, using the standard sift operations.

| Input | Output | Why |
|---|---|---|
| `nums = [1,3,2,7,4,5], ind = 0, val = 6` | `[2,3,5,7,4,6]` | 6 sinks: swaps with 2, then with 5 |
| `nums = [1,3,2,7,4,5], ind = 5, val = 0` | `[0,3,1,7,4,2]` | 0 rises to the root |

**Constraints:** `1 ≤ n ≤ 10⁵`, `0 ≤ ind < n`, values fit in `int`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Rebuild the whole heap | assign, then bottom-up build | O(n) | O(1) |
| Sift up or sift down from `ind` | smaller → bubble up; larger → sink | O(log n) | O(1) |

> [!tip] Interview angle
> This is the primitive behind every heap operation: push is 'append + sift up', pop is 'move last to root + sift down', decrease-key is 'sift up'. Say which direction and why before coding.

---

## 3. Rebuild the whole heap

**Intuition.** After the assignment, run the bottom-up build (sift down every internal node from the last one to the root). Correct, but it ignores the fact that only one position is broken.

```python
def heapify_rebuild(nums, ind, val):
    nums[ind] = val
    n = len(nums)
    for i in range(n // 2 - 1, -1, -1):
        j = i
        while True:
            s, l, r = j, 2 * j + 1, 2 * j + 2
            if l < n and nums[l] < nums[s]: s = l
            if r < n and nums[r] < nums[s]: s = r
            if s == j: break
            nums[j], nums[s] = nums[s], nums[j]
            j = s
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Sift up or sift down from `ind`

**Intuition.** Only the edges touching `ind` can be violated. If `val` is smaller than the parent, swap upward until the parent is ≤. Otherwise swap downward with the **smaller** child until both children are ≥. Choosing the smaller child keeps the other child valid under the new parent.

**Algorithm**

1. `nums[ind] = val`.
2. Sift up: while `i > 0` and `nums[parent(i)] > nums[i]`, swap and move to the parent.
3. Sift down from the resulting `i`: pick the smallest of `i`, `2i+1`, `2i+2`; if it isn't `i`, swap and continue there.
4. At most one of the two loops does any work.

**Dry run** — [1,3,2,7,4,5], ind 0 ← 6: [6,3,2,7,4,5]. No parent. Children 3 and 2 → swap with 2: [2,3,6,7,4,5]. Child of index 2 is 5 < 6 → swap: [2,3,5,7,4,6].

**C++**
```cpp
void heapify(vector<int>& nums, int ind, int val) {
    int n = nums.size();
    nums[ind] = val;
    int i = ind;
    while (i > 0 && nums[(i - 1) / 2] > nums[i]) {
        swap(nums[i], nums[(i - 1) / 2]);
        i = (i - 1) / 2;
    }
    while (true) {
        int s = i, l = 2 * i + 1, r = 2 * i + 2;
        if (l < n && nums[l] < nums[s]) s = l;
        if (r < n && nums[r] < nums[s]) s = r;
        if (s == i) break;
        swap(nums[i], nums[s]);
        i = s;
    }
}
```

**Java**
```java
static void heapify(int[] nums, int ind, int val) {
    int n = nums.length;
    nums[ind] = val;
    int i = ind;
    while (i > 0 && nums[(i - 1) / 2] > nums[i]) {
        int p = (i - 1) / 2, t = nums[i]; nums[i] = nums[p]; nums[p] = t;
        i = p;
    }
    while (true) {
        int s = i, l = 2 * i + 1, r = 2 * i + 2;
        if (l < n && nums[l] < nums[s]) s = l;
        if (r < n && nums[r] < nums[s]) s = r;
        if (s == i) break;
        int t = nums[i]; nums[i] = nums[s]; nums[s] = t;
        i = s;
    }
}
```

**Python**
```python
def heapify(nums, ind, val):
    n = len(nums)
    nums[ind] = val
    i = ind
    while i > 0 and nums[(i - 1) // 2] > nums[i]:          # sift up
        p = (i - 1) // 2
        nums[i], nums[p] = nums[p], nums[i]
        i = p
    while True:                                             # sift down
        s, l, r = i, 2 * i + 1, 2 * i + 2
        if l < n and nums[l] < nums[s]: s = l
        if r < n and nums[r] < nums[s]: s = r
        if s == i:
            break
        nums[i], nums[s] = nums[s], nums[i]
        i = s
```

**Complexity:** time **O(log n)**, space **O(1)** — each loop walks one root-to-leaf path, so at most ⌊log₂ n⌋ swaps.

---

## Edge cases

- `val` equal to the old value: neither loop moves.
- `ind` is a leaf and the value grew: nothing to do.
- Duplicates: use strict `<` / `>` so equal keys don't swap pointlessly.

---

## Common mistakes

1. Sifting down by swapping with the **left** child instead of the smaller child, which breaks the right subtree.
2. Parent index `i / 2` (that's the 1-indexed formula); 0-indexed is `(i − 1) / 2`.
3. Running only sift down, which is wrong when the key decreased.

---

## Follow-ups

1. Max-heap version?
2. Delete an arbitrary index.

<details><summary>Answer sketches</summary>

**#1:** Flip both comparisons: sift up while the parent is **smaller**, sift down to the **larger** child.

**#2:** Move the last element into `ind`, shrink, then run this same repair, since the moved value could need either direction.
</details>

---

## Flashcards

**Heap key decreased (min-heap): direction?** #flashcard
Sift up: it can only violate its parent.

**Sift down swaps with which child?** #flashcard
The smaller one (min-heap), so the other child stays ≥ its new parent.

**0-indexed parent / children of i?** #flashcard
Parent `(i−1)/2`; children `2i+1`, `2i+2`.

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
