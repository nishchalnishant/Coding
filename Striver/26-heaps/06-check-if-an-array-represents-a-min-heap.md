---
module: striver/26-heaps
lesson: 6
topic: Check if an array represents a min heap
difficulty: Easy
source: https://takeuforward.org/learning/dsa/check-if-an-array-represents-a-min-heap-?category=theory-and-implementation&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, array]
---
# 6. Check if an array represents a min heap

← [Implement Max Heap](05-implement-max-heap.md) · [Part 26 index](README.md) · Next → [Convert Min Heap to Max Heap](07-convert-min-heap-to-max-heap.md)

> [!abstract] Problem at a glance
> **Task:** Return whether `nums` (level order) satisfies the min-heap property.
> **Key insight:** The heap property is local: it's enough that every **parent ≤ child** edge holds. Shape is free, since any array is a complete tree. So check each `i ≥ 1` against its parent `(i − 1)/2`.
> **Difficulty:** Easy · **Pattern:** Edge-by-edge invariant check
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-if-an-array-represents-a-min-heap-?category=theory-and-implementation&source=strivers-a2z-dsa-sheet) · **Time:** 8 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursive per-node check](#3-recursive-per-node-check) · [4. Loop over internal nodes](#4-loop-over-internal-nodes) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums` representing a complete binary tree in level order, return `true` if it is a min-heap: every node is ≤ each of its children.

| Input | Output | Why |
|---|---|---|
| `nums = [10,20,30,21,23]` | `true` |  |
| `nums = [10,20,30,25,15]` | `false` | 15 is under 20 |

**Constraints:** `1 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursive per-node check | node ≤ children && both subtrees are heaps | O(n) | O(log n) stack |
| Loop over internal nodes | for i < n/2: check both children | O(n) | O(1) |

> [!tip] Interview angle
> One loop. Mention that the same idea checks a max-heap by flipping the comparison, and that the transitivity of ≤ is why checking edges is enough (grandparent ≤ parent ≤ child).

---

## 3. Recursive per-node check

**Intuition.** Mirror of tree validation: a node is fine if it's ≤ its existing children and both child subtrees are heaps.

```python
def is_heap_rec(nums):
    n = len(nums)
    def ok(i):
        for c in (2 * i + 1, 2 * i + 2):
            if c < n and (nums[c] < nums[i] or not ok(c)):
                return False
        return True
    return ok(0)
```

**Complexity:** time **O(n)**, space **O(log n) stack**.

---

## 4. Loop over internal nodes

**Intuition.** Only indices `0 … n/2 − 1` have children. For each, compare with `2i+1` and (if present) `2i+2`.

**Algorithm**

1. For `i` in `0 … n/2 − 1`:
2.   if `nums[2i+1] < nums[i]` → false;
3.   if `2i+2 < n` and `nums[2i+2] < nums[i]` → false.
4. Return true.

**Dry run** — [10,20,30,25,15]: i=0: 20, 30 ≥ 10 ✓. i=1: 25 ≥ 20 ✓, 15 < 20 ✗ → false.

**C++**
```cpp
bool isHeap(vector<int>& nums) {
    int n = nums.size();
    for (int i = 0; 2 * i + 1 < n; i++) {
        if (nums[2 * i + 1] < nums[i]) return false;
        if (2 * i + 2 < n && nums[2 * i + 2] < nums[i]) return false;
    }
    return true;
}
```

**Java**
```java
static boolean isHeap(int[] nums) {
    int n = nums.length;
    for (int i = 0; 2 * i + 1 < n; i++) {
        if (nums[2 * i + 1] < nums[i]) return false;
        if (2 * i + 2 < n && nums[2 * i + 2] < nums[i]) return false;
    }
    return true;
}
```

**Python**
```python
def is_heap(nums):
    n = len(nums)
    for i in range(n // 2):
        if nums[2 * i + 1] < nums[i]:
            return False
        if 2 * i + 2 < n and nums[2 * i + 2] < nums[i]:
            return False
    return True
```

**Complexity:** time **O(n)**, space **O(1)** — each edge is checked once; n − 1 edges.

---

## Edge cases

- Single element → true.
- Last internal node with only a left child.
- Equal parent and child → still a heap (≤).

---

## Common mistakes

1. Using `<=` in the failure test, which rejects equal keys.
2. Indexing `2i+2` without the bounds check.
3. Checking only the root against everyone (that's 'root is the min', a weaker property).

---

## Follow-ups

1. Check a max-heap.
2. Check a binary-tree-with-pointers heap.

<details><summary>Answer sketches</summary>

**#1:** Flip the comparisons.

**#2:** Also verify completeness (BFS: no node after the first null) plus the order property.
</details>

---

## Flashcards

**Why is checking parent–child edges enough for a heap?** #flashcard
≤ is transitive along every root-to-leaf path.

**Which indices have children?** #flashcard
`0 … n/2 − 1`.

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
