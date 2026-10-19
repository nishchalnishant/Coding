---
module: striver/16-binary-search
lesson: 9
topic: Search in Rotated Sorted Array II
difficulty: Medium
source: https://takeuforward.org/learning/dsa/search-in-rotated-sorted-array-2?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, rotated-array]
---
# 9. Search in Rotated Sorted Array II

← [Search in Rotated Sorted Array I](08-search-in-rotated-sorted-array-i.md) · [Part 16 index](README.md) · Next → [Find Minimum in Rotated Sorted Array](10-minimum-in-rotated-sorted-array.md)

> [!abstract] Problem at a glance
> **Task:** Return whether `target` exists in a rotated sorted array that may contain duplicates.
> **Key insight:** Same "sorted half" logic — except when `nums[lo] == nums[mid] == nums[hi]` you can't tell which half is sorted. Then just drop both ends (`lo++`, `hi−−`); neither is the target since it equals `nums[mid]`, already checked.
> **Difficulty:** Medium · **Pattern:** Rotated binary search + shrink on ties · **Also on:** [LC 81](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/search-in-rotated-sorted-array-2?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear scan](#3-linear-scan) · [4. Rotated search with tie shrinking](#4-rotated-search-with-tie-shrinking) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Same as the previous problem, but `nums` may contain duplicates. Return `true` if `target` is in `nums`, else `false`.

| Input | Output | Why |
|---|---|---|
| `nums = [2, 5, 6, 0, 0, 1, 2], target = 0` | `true` |  |
| `nums = [2, 5, 6, 0, 0, 1, 2], target = 3` | `false` |  |
| `nums = [3, 1, 2, 3, 3, 3, 3], target = 2` | `true` | ends equal mid |

**Constraints:** `1 ≤ n ≤ 5000`, `−10⁴ ≤ nums[i], target ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear scan | `target in nums` | O(n) | O(1) |
| Rotated search with tie shrinking | if lo, mid, hi all equal: lo++, hi−−; else as in part I | O(log n) average, O(n) worst | O(1) |

> [!tip] Interview angle
> Expect the question "what's the worst case?" Answer: O(n), e.g. `[1, 1, 1, …, 1, 2, 1, 1]` — every step can only shrink by one. No algorithm beats Ω(n) here, since the lone different element could be anywhere.

---

## 3. Linear scan

**Intuition.** Matches the optimal worst case, but loses the O(log n) average.

```python
def search_rot2_linear(nums, target):
    return target in nums
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Rotated search with tie shrinking

**Intuition.** The only case where `nums[lo] ≤ nums[mid]` lies about the left half being sorted is when `nums[lo] == nums[mid]` and the rotation point is inside the left half, e.g. `[3, 1, 2, 3, 3, 3, 3]` — which forces `nums[hi]` to equal them too. Shrinking both ends removes the ambiguity without losing the target (both ends equal `nums[mid] ≠ target`).

**Dry run** — `[3 1 2 3 3 3 3]`, t = 2: lo 0 hi 6 mid 3: all three are 3 → lo 1, hi 5. mid 3 (3): `nums[1]=1 ≤ 3` left sorted; 2 ∈ [1, 3) → hi 2. mid 1 (1): left `[1]` sorted, 2 ∉ [1, 1) → lo 2. mid 2 → found.

**C++**
```cpp
bool searchII(vector<int>& nums, int target) {
    int lo = 0, hi = (int)nums.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return true;
        if (nums[lo] == nums[mid] && nums[mid] == nums[hi]) { lo++; hi--; continue; }
        if (nums[lo] <= nums[mid]) {
            if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {
            if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return false;
}
```

**Java**
```java
static boolean searchII(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return true;
        if (nums[lo] == nums[mid] && nums[mid] == nums[hi]) { lo++; hi--; continue; }
        if (nums[lo] <= nums[mid]) {
            if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {
            if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return false;
}
```

**Python**
```python
def search_rotated_ii(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return True
        if nums[lo] == nums[mid] == nums[hi]:
            lo, hi = lo + 1, hi - 1
            continue
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False
```

**Complexity:** time **O(log n) average, O(n) worst**, space **O(1)** — halving except on triple ties, each of which removes two elements.

---

## Edge cases

- All elements equal.
- Single different element hidden among duplicates.
- Not rotated.

---

## Common mistakes

1. Shrinking only one end — still correct but easy to get wrong; shrinking both is symmetric and safe.
2. Claiming O(log n) worst case.

---

## Follow-ups

1. Return an index instead of a boolean.
2. Minimum in rotated array with duplicates (LC 154).

<details><summary>Answer sketches</summary>

**#1:** Same algorithm; return `mid` on match.

**#2:** When `nums[mid] == nums[hi]`, `hi−−`.
</details>

---

## Flashcards

**Rotated search with duplicates — extra case?** #flashcard
nums[lo] == nums[mid] == nums[hi] → lo++, hi−−.

**Worst case with duplicates?** #flashcard
O(n), unavoidable.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../coding/algorithms/11-binary-search.md)
