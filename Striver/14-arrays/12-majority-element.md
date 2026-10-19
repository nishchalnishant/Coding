---
module: striver/14-arrays
lesson: 12
topic: Majority Element I
difficulty: Easy
source: https://takeuforward.org/learning/dsa/majority-element-i?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, boyer-moore, voting]
---
# 12. Majority Element I

← [Intersection of Two Sorted Arrays](11-intersection-of-two-sorted-arrays.md) · [Part 14 index](README.md) · Next → [Leaders in an Array](13-leaders-in-an-array.md)

> [!abstract] Problem at a glance
> **Task:** Return the element that appears more than ⌊n/2⌋ times (it's guaranteed to exist).
> **Key insight:** Boyer–Moore voting: pair each majority vote with a different vote and cancel both. The majority has more than half, so it survives. Keep `(cand, cnt)`: if `cnt == 0` adopt the current element; same → +1, different → −1.
> **Difficulty:** Easy · **Pattern:** Boyer–Moore voting · **Also on:** [LC 169](https://leetcode.com/problems/majority-element/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/majority-element-i?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Count every element](#3-count-every-element) · [4. Hash map counts](#4-hash-map-counts) · [5. Boyer–Moore voting](#5-boyermoore-voting) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums` of size `n`, return the majority element, which appears more than `⌊n/2⌋` times. The majority element always exists.

| Input | Output | Why |
|---|---|---|
| `nums = [7, 0, 0, 1, 7, 7, 2, 7, 7]` | `7` | 7 appears 5 > 4 times |
| `nums = [1, 1, 1, 2, 1, 2]` | `1` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, `−10⁹ ≤ nums[i] ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Count every element | nested loops | O(n²) | O(1) |
| Hash map counts | count, return the one over n/2 | O(n) | O(n) |
| Boyer–Moore voting | cand/cnt; cancel unequal pairs | O(n) | O(1) |

> [!tip] Interview angle
> Boyer–Moore is the expected O(1)-space answer. If the majority is *not* guaranteed, add a second pass that counts the candidate, and say so before you're asked.

---

## 3. Count every element

**Intuition.** For each element, count its occurrences; return the first with count > n/2.

```python
def majority_brute(nums):
    n = len(nums)
    for x in nums:
        if nums.count(x) > n // 2:
            return x
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Hash map counts

**Intuition.** One pass to count, one pass over the map. Sorting and taking `nums[n/2]` is the O(n log n) / O(1) alternative: the majority must cover the middle index.

```python
def majority_hash(nums):
    cnt = {}
    for x in nums:
        cnt[x] = cnt.get(x, 0) + 1
        if cnt[x] > len(nums) // 2:
            return x
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 5. Boyer–Moore voting

**Intuition.** Think of it as pairing off unequal elements and deleting both. Each deletion removes at most one majority copy and at least one non-majority copy, so the majority can never be fully cancelled. `cnt == 0` means the prefix so far cancelled out completely, so start fresh with a new candidate.

**Algorithm**

1. `cand = None`, `cnt = 0`.
2. For each `x`: if `cnt == 0`, `cand = x`. Then `cnt += 1` if `x == cand` else `cnt −= 1`.
3. Return `cand` (verify with a count pass if a majority isn't guaranteed).

**Dry run** — `[7 0 0 1 7 7 2 7 7]`: 7(1) 0(0) 0→cand 0(1) 1(0) 7→cand 7(1) 7(2) 2(1) 7(2) 7(3) → 7.

**C++**
```cpp
int majorityElement(vector<int>& nums) {
    int cand = 0, cnt = 0;
    for (int x : nums) {
        if (cnt == 0) cand = x;
        cnt += (x == cand) ? 1 : -1;
    }
    return cand;
}
```

**Java**
```java
static int majorityElement(int[] nums) {
    int cand = 0, cnt = 0;
    for (int x : nums) {
        if (cnt == 0) cand = x;
        cnt += (x == cand) ? 1 : -1;
    }
    return cand;
}
```

**Python**
```python
def majority_element(nums):
    cand, cnt = None, 0
    for x in nums:
        if cnt == 0:
            cand = x
        cnt += 1 if x == cand else -1
    return cand
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- n = 1.
- Majority at the end only (candidate switches several times).
- Negative values.

---

## Common mistakes

1. Returning `cnt` instead of `cand`.
2. Setting `cand = x` and then also decrementing in the same step.
3. Skipping the verification pass when the majority isn't guaranteed.

---

## Follow-ups

1. Elements appearing more than ⌊n/3⌋ times.
2. General: more than ⌊n/k⌋.
3. Streaming data.

<details><summary>Answer sketches</summary>

**#1:** Two candidates, two counters, then verify: [Majority Element II](#).

**#2:** Misra–Gries: keep k − 1 candidates; O(nk) time, O(k) space.

**#3:** Boyer–Moore is already one-pass, O(1) memory; it's a streaming algorithm.
</details>

---

## Flashcards

**Boyer–Moore update rule?** #flashcard
cnt == 0 → cand = x; then cnt += (x == cand ? 1 : −1).

**Why does Boyer–Moore work?** #flashcard
Cancelling unequal pairs can't exhaust an element with > n/2 copies.

**Majority element via sorting?** #flashcard
nums[n/2] after sorting.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../coding/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../coding/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
