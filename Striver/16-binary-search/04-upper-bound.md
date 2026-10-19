---
module: striver/16-binary-search
lesson: 4
topic: Upper Bound
difficulty: Easy
source: https://takeuforward.org/learning/dsa/upper-bound?category=fundamentals&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, upper-bound]
---
# 4. Upper Bound

← [Lower Bound](03-lower-bound.md) · [Part 16 index](README.md) · Next → [Search Insert Position](05-search-insert-position.md)

> [!abstract] Problem at a glance
> **Task:** Return the smallest index `i` with `nums[i] > x`, or `n` if none.
> **Key insight:** Identical to lower bound with `≥` replaced by `>`. `upper_bound(x) − lower_bound(x)` counts occurrences of `x`.
> **Difficulty:** Easy · **Pattern:** Binary search for first true
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/upper-bound?category=fundamentals&source=strivers-a2z-dsa-sheet) · **Time:** 8 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear scan](#3-linear-scan) · [4. Binary search](#4-binary-search) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a sorted array `nums` and an integer `x`, return the **upper bound** of `x`: the smallest index `i` with `nums[i] > x`, or `n` if none exists.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 2, 3], x = 2` | `3` | index of 3 |
| `nums = [3, 5, 8, 9, 15, 19], x = 9` | `4` | 15 |
| `nums = [1, 2, 3], x = 3` | `3` | returns n |

**Constraints:** `1 ≤ n ≤ 10⁵`, `−10⁵ ≤ nums[i], x ≤ 10⁵`, sorted non-decreasing.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear scan | first i with nums[i] > x | O(n) | O(1) |
| Binary search | nums[mid] > x → ans = mid, go left; else go right | O(log n) | O(1) |

---

## 3. Linear scan

**Intuition.** Walk until an element exceeds `x`.

```python
def upper_bound_linear(nums, x):
    for i, v in enumerate(nums):
        if v > x:
            return i
    return len(nums)
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Binary search

**Intuition.** Predicate `nums[i] > x` is monotone (F…F T…T). First true via the same answer-variable template. Library: `bisect_right` / `std::upper_bound`.

**Dry run** — `[3 5 8 9 15 19]`, x = 9: mid 2 (8) → lo 3; mid 4 (15 > 9) → ans 4, hi 3; mid 3 (9, not > 9) → lo 4. Answer 4.

**C++**
```cpp
int upperBound(vector<int>& nums, int x) {
    int lo = 0, hi = (int)nums.size() - 1, ans = nums.size();
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] > x) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Java**
```java
static int upperBound(int[] nums, int x) {
    int lo = 0, hi = nums.length - 1, ans = nums.length;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] > x) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Python**
```python
def upper_bound(nums, x):
    lo, hi, ans = 0, len(nums) - 1, len(nums)
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] > x:
            ans, hi = mid, mid - 1
        else:
            lo = mid + 1
    return ans
```

**Complexity:** time **O(log n)**, space **O(1)** — halving.

---

## Edge cases

- `x` ≥ last element → `n`.
- `x` < first → 0.
- All equal to `x` → `n`.

---

## Common mistakes

1. Confusing with lower bound (`≥` vs `>`).
2. Thinking upper bound is the *last* occurrence — it's one past it.

---

## Follow-ups

1. Last occurrence of x.
2. Number of elements ≤ x.

<details><summary>Answer sketches</summary>

**#1:** `upper_bound(x) − 1`, if that index holds `x`.

**#2:** `upper_bound(x)`.
</details>

---

## Flashcards

**Upper bound definition?** #flashcard
Smallest i with nums[i] > x; n if none.

**Occurrences of x in a sorted array?** #flashcard
upper_bound(x) − lower_bound(x).

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../coding/algorithms/11-binary-search.md)
