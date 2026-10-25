---
module: striver-a2z/16-binary-search
lesson: 12
topic: Single Element in a Sorted Array
difficulty: Medium
source: https://takeuforward.org/learning/dsa/single-element-in-sorted-array?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, parity]
---
# 12. Single Element in a Sorted Array

← [Find Out How Many Times the Array Is Rotated](11-rotation-count.md) · [Part 16 index](README.md) · Next → [Count Occurrences in a Sorted Array](13-count-occurrences.md)

> [!abstract] Problem at a glance
> **Task:** Every value appears exactly twice except one; the array is sorted. Find the single one in O(log n).
> **Key insight:** Before the single element, pairs start at **even** indices (`nums[2i] == nums[2i+1]`); after it, they start at odd indices. At an even `mid`, if `nums[mid] == nums[mid + 1]` the single is to the right; otherwise it's at `mid` or left.
> **Difficulty:** Medium · **Pattern:** Binary search on index parity · **Also on:** [LC 540](https://leetcode.com/problems/single-element-in-a-sorted-array/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/single-element-in-sorted-array?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. XOR everything](#3-xor-everything) · [4. Linear pair check](#4-linear-pair-check) · [5. Binary search on even indices](#5-binary-search-on-even-indices) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a sorted array where every element appears exactly twice except one that appears once, return the single element. O(log n) time, O(1) space.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 1, 2, 3, 3, 4, 4, 8, 8]` | `2` |  |
| `nums = [3, 3, 7, 7, 10, 11, 11]` | `10` |  |
| `nums = [5]` | `5` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, `n` odd, `0 ≤ nums[i] ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| XOR everything | pairs cancel; a ^ a = 0 | O(n) | O(1) |
| Linear pair check | step by 2; first i where nums[i] != nums[i+1] | O(n) | O(1) |
| Binary search on even indices | force mid even; pair intact → lo = mid + 2, else hi = mid | O(log n) | O(1) |

> [!tip] Interview angle
> Start with XOR (O(n)) to show you know the unsorted version, then point out that sortedness lets us binary-search on the *pairing pattern*, not on values.

---

## 3. XOR everything

**Intuition.** Works without sortedness. Doesn't meet the O(log n) requirement.

```python
def single_xor(nums):
    r = 0
    for x in nums:
        r ^= x
    return r
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Linear pair check

**Intuition.** Walk pairs `(0,1), (2,3), …`. The first broken pair starts at the single element.

```python
def single_pairs(nums):
    for i in range(0, len(nums) - 1, 2):
        if nums[i] != nums[i + 1]:
            return nums[i]
    return nums[-1]
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 5. Binary search on even indices

**Intuition.** The single element is always at an even index (an even number of elements precede it). Restrict `mid` to even values. If `nums[mid] == nums[mid + 1]`, the pairing is still intact up to `mid + 1`, so the single is at `mid + 2` or later. Otherwise the break is at `mid` or before. Predicate "pair at mid is broken" is monotone over even indices.

**Algorithm**

1. `lo = 0`, `hi = n − 1` (even, since n is odd).
2. While `lo < hi`: `mid = (lo + hi) / 2`; if odd, `mid −= 1`.
3. `nums[mid] == nums[mid + 1]` → `lo = mid + 2`; else `hi = mid`.
4. Return `nums[lo]`.

**Dry run** — `[1 1 2 3 3 4 4 8 8]`: lo 0 hi 8 mid 4 (3 vs 4 broken) → hi 4; mid 2 (2 vs 3 broken) → hi 2; mid 1 → 0 (1 == 1) → lo 2. Answer nums[2] = 2.

**Striver's variant** uses all indices and checks `nums[mid]` against both neighbours, eliminating the left half when `(mid even and nums[mid] == nums[mid+1])` or `(mid odd and nums[mid] == nums[mid−1])`. The XOR trick `mid ^ 1` gives the partner index in one expression: `nums[mid] == nums[mid ^ 1]` → go right.

**C++**
```cpp
int singleNonDuplicate(vector<int>& nums) {
    int lo = 0, hi = (int)nums.size() - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (mid % 2 == 1) mid--;
        if (nums[mid] == nums[mid + 1]) lo = mid + 2;
        else hi = mid;
    }
    return nums[lo];
}
```

**Java**
```java
static int singleNonDuplicate(int[] nums) {
    int lo = 0, hi = nums.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (mid % 2 == 1) mid--;
        if (nums[mid] == nums[mid + 1]) lo = mid + 2;
        else hi = mid;
    }
    return nums[lo];
}
```

**Python**
```python
def single_non_duplicate(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if mid % 2 == 1:
            mid -= 1
        if nums[mid] == nums[mid + 1]:
            lo = mid + 2
        else:
            hi = mid
    return nums[lo]
```

**Complexity:** time **O(log n)**, space **O(1)** — halving over even indices; `mid + 1 ≤ hi` always holds since mid < hi and hi is even.

---

## Edge cases

- n = 1.
- Single at index 0 or n − 1.

---

## Common mistakes

1. Letting `mid` be odd and comparing with `mid + 1` — pairs misalign.
2. Out-of-bounds `mid + 1` when using `lo ≤ hi`.

---

## Follow-ups

1. Unsorted array.
2. Every element thrice except one.

<details><summary>Answer sketches</summary>

**#1:** XOR all — O(n).

**#2:** Bit counting mod 3 — Part 20.
</details>

---

## Flashcards

**Single element in sorted pairs — pattern?** #flashcard
Before it, pairs start at even indices; after, at odd.

**Partner index of mid in one expression?** #flashcard
mid ^ 1.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
