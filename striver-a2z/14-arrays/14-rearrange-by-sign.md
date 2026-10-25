---
module: striver-a2z/14-arrays
lesson: 14
topic: Rearrange Array Elements by Sign
difficulty: Medium
source: https://takeuforward.org/learning/dsa/rearrange-array-elements-by-sign?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, index-placement]
---
# 14. Rearrange Array Elements by Sign

← [Leaders in an Array](13-leaders-in-an-array.md) · [Part 14 index](README.md) · Next → [Print the Matrix in Spiral Manner](15-spiral-matrix.md)

> [!abstract] Problem at a glance
> **Task:** Given equal numbers of positives and negatives, return an array alternating positive, negative, starting with a positive, preserving each group's order.
> **Key insight:** Positives go to even indices and negatives to odd indices. Two write pointers, `pos = 0` and `neg = 1`, each advance by 2. One pass, O(n).
> **Difficulty:** Medium · **Pattern:** Index placement · **Also on:** [LC 2149](https://leetcode.com/problems/rearrange-array-elements-by-sign/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/rearrange-array-elements-by-sign?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Split then interleave](#3-split-then-interleave) · [4. Single pass, two write indices](#4-single-pass-two-write-indices) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums` of even length with equally many positive and negative integers (no zeros), return a new array in which consecutive elements have opposite signs, the first element is positive, and the relative order within the positives and within the negatives is preserved.

| Input | Output | Why |
|---|---|---|
| `nums = [2, 4, 5, -1, -3, -4]` | `[2, -1, 4, -3, 5, -4]` |  |
| `nums = [1, -1, -3, -4, 2, 3]` | `[1, -1, 2, -3, 3, -4]` |  |

**Constraints:** `2 ≤ n ≤ 2·10⁵`, `n` even, equal counts, `nums[i] ≠ 0`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Split then interleave | two lists, then merge alternately | O(n) | O(n) |
| Single pass, two write indices | pos → even slot, neg → odd slot | O(n) | O(n) for the output |

---

## 3. Split then interleave

**Intuition.** Collect positives and negatives separately (two passes), then write `pos[i]` to `2i` and `neg[i]` to `2i + 1`.

```python
def rearrange_split(nums):
    pos = [x for x in nums if x > 0]
    neg = [x for x in nums if x < 0]
    res = [0] * len(nums)
    for i in range(len(pos)):
        res[2 * i], res[2 * i + 1] = pos[i], neg[i]
    return res
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Single pass, two write indices

**Intuition.** We already know where each element goes: the k-th positive goes to `2k`, the k-th negative to `2k + 1`. So keep `pi = 0`, `ni = 1` and advance by 2.

**Unequal counts (the variant):** interleave while both lists have elements, then append the leftovers in order. That needs the split approach. An O(1)-space stable in-place version doesn't exist in O(n).

**C++**
```cpp
vector<int> rearrangeArray(vector<int>& nums) {
    vector<int> res(nums.size());
    int pi = 0, ni = 1;
    for (int x : nums) {
        if (x > 0) { res[pi] = x; pi += 2; }
        else { res[ni] = x; ni += 2; }
    }
    return res;
}
```

**Java**
```java
static int[] rearrangeArray(int[] nums) {
    int[] res = new int[nums.length];
    int pi = 0, ni = 1;
    for (int x : nums) {
        if (x > 0) { res[pi] = x; pi += 2; }
        else { res[ni] = x; ni += 2; }
    }
    return res;
}
```

**Python**
```python
def rearrange_array(nums):
    res = [0] * len(nums)
    pi, ni = 0, 1
    for x in nums:
        if x > 0:
            res[pi] = x; pi += 2
        else:
            res[ni] = x; ni += 2
    return res
```

**Complexity:** time **O(n)**, space **O(n) for the output**.

---

## Edge cases

- n = 2.
- All negatives first.
- Already alternating.

---

## Common mistakes

1. Swapping in place: breaks the relative order.
2. Starting with the negative index at 0.

---

## Follow-ups

1. Counts differ; append the extras at the end.
2. O(1) extra space, order not required.

<details><summary>Answer sketches</summary>

**#1:** Split, interleave up to min(len), then append the rest.

**#2:** Partition by sign, then swap every other element across the halves.
</details>

---

## Flashcards

**Rearrange by sign: where does the k-th positive go?** #flashcard
Index 2k (negatives at 2k + 1).

**Rearrange by sign with unequal counts?** #flashcard
Split into two lists, interleave, append leftovers.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../04-practice/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../04-practice/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
