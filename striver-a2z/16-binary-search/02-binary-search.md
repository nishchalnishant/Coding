---
module: striver-a2z/16-binary-search
lesson: 2
topic: Search X in Sorted Array
difficulty: Easy
source: https://takeuforward.org/learning/dsa/search-x-in-sorted-array?category=fundamentals&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search]
---
# 2. Search X in Sorted Array

← [Binary Search Templates](01-binary-search-templates.md) · [Part 16 index](README.md) · Next → [Lower Bound](03-lower-bound.md)

> [!abstract] Problem at a glance
> **Task:** Return the index of `target` in a sorted array of distinct integers, or −1.
> **Key insight:** Compare with the middle element and throw away the half that cannot contain the target. Each step halves the range, so ≤ ⌈log₂(n + 1)⌉ comparisons.
> **Difficulty:** Easy · **Pattern:** Classic binary search · **Also on:** [LC 704](https://leetcode.com/problems/binary-search/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/search-x-in-sorted-array?category=fundamentals&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear scan](#3-linear-scan) · [4. Recursive binary search](#4-recursive-binary-search) · [5. Iterative binary search](#5-iterative-binary-search) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a sorted (ascending) array `nums` of **distinct** integers and an integer `target`, return the index of `target`, or `-1` if it's absent. The solution must run in O(log n).

| Input | Output | Why |
|---|---|---|
| `nums = [-1, 0, 3, 5, 9, 12], target = 9` | `4` |  |
| `nums = [-1, 0, 3, 5, 9, 12], target = 2` | `-1` | absent |

**Constraints:** `1 ≤ n ≤ 10⁴`, `−10⁴ < nums[i], target < 10⁴`, all values distinct, sorted ascending.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear scan | check every index | O(n) | O(1) |
| Recursive binary search | search(lo, hi) recurses into one half | O(log n) | O(log n) stack |
| Iterative binary search | closed interval [lo, hi]; drop the half that can't hold target | O(log n) | O(1) |

> [!tip] Interview angle
> Warm-up question. They're checking that you write it bug-free first time: closed interval `[lo, hi]`, `while lo <= hi`, `mid = lo + (hi − lo) / 2`, and `lo = mid + 1` / `hi = mid − 1`. Say the invariant out loud.

---

## 3. Linear scan

**Intuition.** Ignores sortedness. Fine as a baseline, but the problem demands O(log n).

```python
def search_linear(nums, target):
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Recursive binary search

**Intuition.** Same halving, expressed as recursion: base case `lo > hi` (empty range) returns −1. Each call does O(1) work and recurses once, so depth is log n. Interviewers sometimes ask for this form to check the base case.

```python
def search_rec(nums, target, lo=0, hi=None):
    if hi is None:
        hi = len(nums) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if nums[mid] == target:
        return mid
    if nums[mid] < target:
        return search_rec(nums, target, mid + 1, hi)
    return search_rec(nums, target, lo, mid - 1)
```

**Complexity:** time **O(log n)**, space **O(log n) stack**.

---

## 5. Iterative binary search

**Intuition.** **Invariant:** if `target` is present, its index is in `[lo, hi]`. If `nums[mid] < target`, everything at or left of `mid` is too small (sorted), so `lo = mid + 1`. If larger, `hi = mid − 1`. The loop ends when the range is empty (`lo > hi`) — then the target is absent.

**Algorithm**

1. `lo = 0`, `hi = n − 1`.
2. While `lo ≤ hi`: `mid = lo + (hi − lo) / 2`.
3. Equal → return `mid`; `nums[mid] < target` → `lo = mid + 1`; else `hi = mid − 1`.
4. Return −1.

**Dry run** — `[-1 0 3 5 9 12]`, t = 9: lo 0 hi 5 mid 2 (3 < 9) → lo 3; mid 4 (9) → return 4.

**Why `lo + (hi − lo) / 2`?** `lo + hi` overflows a 32-bit int when both are near 2³¹. Python ints don't overflow, but write it the safe way in C++/Java.

**C++**
```cpp
int search(vector<int>& nums, int target) {
    int lo = 0, hi = (int)nums.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

**Java**
```java
static int search(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

**Python**
```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

**Complexity:** time **O(log n)**, space **O(1)** — the range halves every iteration.

---

## Edge cases

- Single element, hit and miss.
- Target smaller than all / larger than all.
- Two elements — off-by-one bugs show up here first.

---

## Common mistakes

1. `while lo < hi` with `hi = n − 1` — misses the last candidate when `lo == hi`.
2. `hi = mid` with `while lo <= hi` — infinite loop when `lo == hi`.
3. `(lo + hi) / 2` overflow in C++/Java.
4. Using it on unsorted input.

---

## Follow-ups

1. Array has duplicates — return any index / first index.
2. Array size unknown (LC 702, `ArrayReader`).
3. Descending order.

<details><summary>Answer sketches</summary>

**#1:** Any: unchanged. First: lower bound, then check `nums[lb] == target`.

**#2:** Double `hi` (1, 2, 4, …) until `reader.get(hi) ≥ target`, then binary search in `[hi/2, hi]` — O(log idx).

**#3:** Flip the comparison: `nums[mid] > target → lo = mid + 1`.
</details>

---

## Flashcards

**Binary search invariant (closed interval)?** #flashcard
If present, target ∈ [lo, hi]; loop while lo ≤ hi; mid ± 1 on updates.

**Overflow-safe midpoint?** #flashcard
mid = lo + (hi − lo) / 2.

**Max comparisons for n = 10⁶?** #flashcard
⌈log₂(10⁶ + 1)⌉ = 20.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
