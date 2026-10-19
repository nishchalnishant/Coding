---
module: striver/16-binary-search
lesson: 3
topic: Lower Bound
difficulty: Easy
source: https://takeuforward.org/learning/dsa/lower-bound-?category=fundamentals&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, lower-bound]
---
# 3. Lower Bound

← [Search X in Sorted Array](02-binary-search.md) · [Part 16 index](README.md) · Next → [Upper Bound](04-upper-bound.md)

> [!abstract] Problem at a glance
> **Task:** Return the smallest index `i` with `nums[i] ≥ x` in a sorted array, or `n` if every element is smaller.
> **Key insight:** Keep `ans = n`. When `nums[mid] ≥ x`, `mid` is a candidate — record it and look left for a smaller one. Otherwise go right. This "record and keep searching" shape solves every first/last-true question.
> **Difficulty:** Easy · **Pattern:** Binary search for first true
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/lower-bound-?category=fundamentals&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear scan](#3-linear-scan) · [4. Library call](#4-library-call) · [5. Binary search with an answer variable](#5-binary-search-with-an-answer-variable) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a sorted array `nums` (duplicates allowed) and an integer `x`, return the **lower bound** of `x`: the smallest index `i` such that `nums[i] ≥ x`. If no such index exists, return `n`.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 2, 3], x = 2` | `1` | first 2 |
| `nums = [3, 5, 8, 15, 19], x = 9` | `3` | 15 is the first ≥ 9 |
| `nums = [1, 2, 3], x = 7` | `3` | returns n |

**Constraints:** `1 ≤ n ≤ 10⁵`, `−10⁵ ≤ nums[i], x ≤ 10⁵`, sorted non-decreasing.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear scan | first i with nums[i] ≥ x | O(n) | O(1) |
| Library call | bisect_left / std::lower_bound | O(log n) | O(1) |
| Binary search with an answer variable | nums[mid] ≥ x → ans = mid, go left; else go right | O(log n) | O(1) |

> [!tip] Interview angle
> Lower bound is the single most reused primitive in this part: first occurrence, search insert, ceil, count occurrences, and the row-wise binary searches in 2D all reduce to it. Know the library versions: C++ `lower_bound`, Python `bisect_left`, Java has none for arrays-with-duplicates (`Arrays.binarySearch` returns *any* match).

---

## 3. Linear scan

**Intuition.** Walk until the first element that is ≥ x.

```python
def lower_bound_linear(nums, x):
    for i, v in enumerate(nums):
        if v >= x:
            return i
    return len(nums)
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Library call

**Intuition.** Python `bisect.bisect_left(a, x)` returns exactly the lower bound. In C++, `lower_bound(a.begin(), a.end(), x) − a.begin()`. Use these in production; write the loop in interviews unless told otherwise.

```python
from bisect import bisect_left
def lower_bound_lib(nums, x):
    return bisect_left(nums, x)
```

**Complexity:** time **O(log n)**, space **O(1)**.

---

## 5. Binary search with an answer variable

**Intuition.** The predicate `nums[i] ≥ x` is **monotone**: false, false, …, false, true, true, …. We want the first true. When `mid` is true it might be the first, so store it and continue in `[lo, mid − 1]`. When false, the first true is strictly right of `mid`.

**Algorithm**

1. `lo = 0`, `hi = n − 1`, `ans = n`.
2. While `lo ≤ hi`: if `nums[mid] ≥ x` → `ans = mid`, `hi = mid − 1`; else `lo = mid + 1`.
3. Return `ans`.

**Dry run** — `[3 5 8 15 19]`, x = 9: mid 2 (8 < 9) → lo 3; mid 3 (15 ≥ 9) → ans 3, hi 2; stop. Answer 3.

**Half-open variant** (no `ans`): `lo = 0, hi = n; while lo < hi: mid; if nums[mid] >= x: hi = mid else lo = mid + 1; return lo`. Same result — pick one style and use it everywhere.

**C++**
```cpp
int lowerBound(vector<int>& nums, int x) {
    int lo = 0, hi = (int)nums.size() - 1, ans = nums.size();
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] >= x) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Java**
```java
static int lowerBound(int[] nums, int x) {
    int lo = 0, hi = nums.length - 1, ans = nums.length;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] >= x) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Python**
```python
def lower_bound(nums, x):
    lo, hi, ans = 0, len(nums) - 1, len(nums)
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] >= x:
            ans, hi = mid, mid - 1
        else:
            lo = mid + 1
    return ans
```

**Complexity:** time **O(log n)**, space **O(1)** — halving; one comparison per step.

---

## Edge cases

- `x` below everything → 0.
- `x` above everything → `n` (not −1!).
- All elements equal to `x` → 0.

---

## Common mistakes

1. Returning −1 instead of `n` when nothing qualifies.
2. Using `>` instead of `≥` (that's upper bound).
3. Stopping at the first `nums[mid] == x` — it may not be the first occurrence.

---

## Follow-ups

1. Lower bound in a descending array.
2. Count elements < x.
3. Count elements in [a, b].

<details><summary>Answer sketches</summary>

**#1:** Predicate `nums[i] ≤ x` is monotone there; same template.

**#2:** That's exactly `lower_bound(x)`.

**#3:** `upper_bound(b) − lower_bound(a)`.
</details>

---

## Flashcards

**Lower bound definition?** #flashcard
Smallest i with nums[i] ≥ x; n if none.

**Python / C++ library for lower bound?** #flashcard
bisect_left / std::lower_bound.

**lower_bound(x) also equals…** #flashcard
The number of elements strictly less than x.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../coding/algorithms/11-binary-search.md)
