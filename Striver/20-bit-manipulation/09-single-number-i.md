---
module: striver/20-bit-manipulation
lesson: 9
topic: Single Number I
difficulty: Easy
source: https://takeuforward.org/learning/dsa/single-number---i?category=problems&source=strivers-a2z-dsa-sheet
tags: [striver, bit-manipulation, bits, xor]
---
# 9. Single Number I

← [Minimum Bit Flips to Convert Number](08-minimum-bit-flips-to-convert-number.md) · [Part 20 index](README.md) · Next → [Single Number II](10-single-number-ii.md)

> [!abstract] Problem at a glance
> **Task:** Every element appears twice except one; find it in O(n) time, O(1) space.
> **Key insight:** XOR all elements: pairs cancel (`x ^ x = 0`), order doesn't matter (commutative, associative), and the survivor is the single number.
> **Difficulty:** Easy · **Pattern:** XOR cancellation · **Also on:** [LC 136](https://leetcode.com/problems/single-number/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/single-number---i?category=problems&source=strivers-a2z-dsa-sheet) · **Time:** 8 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Hash map count](#3-hash-map-count) · [4. Sort and pair up](#4-sort-and-pair-up) · [5. XOR everything](#5-xor-everything) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a non-empty array `nums` where every element appears twice except for one, find that single one using linear time and constant extra space.

| Input | Output | Why |
|---|---|---|
| `nums = [2, 2, 1]` | `1` |  |
| `nums = [4, 1, 2, 1, 2]` | `4` |  |

**Constraints:** `1 ≤ n ≤ 3·10⁴`, `−3·10⁴ ≤ nums[i] ≤ 3·10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Hash map count | count, return the one with count 1 | O(n) | O(n) |
| Sort and pair up | compare nums[i] with nums[i+1] in steps of 2 | O(n log n) | O(1) |
| XOR everything | pairs cancel | O(n) | O(1) |

> [!tip] Interview angle
> Walk up the ladder: hash map count (O(n) space) → sort and compare pairs (O(n log n)) → XOR. Explain *why* XOR works using its three identities.

---

## 3. Hash map count

**Intuition.** Straightforward; violates the O(1) space requirement.

```python
def single_map(nums):
    from collections import Counter
    for x, c in Counter(nums).items():
        if c == 1:
            return x
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Sort and pair up

**Intuition.** After sorting, pairs sit together. The first index i (even) with `nums[i] != nums[i+1]` holds the single; if none, it's the last element.

```python
def single_sort(nums):
    nums = sorted(nums)
    for i in range(0, len(nums) - 1, 2):
        if nums[i] != nums[i + 1]:
            return nums[i]
    return nums[-1]
```

**Complexity:** time **O(n log n)**, space **O(1)**.

---

## 5. XOR everything

**Intuition.** `a₁ ^ a₁ ^ a₂ ^ a₂ ^ … ^ s` regroups (commutative, associative) to `0 ^ 0 ^ … ^ s = s`.

**Dry run** — [4 1 2 1 2]: 4 → 5 → 7 → 6 → 4.

**C++**
```cpp
int singleNumber(vector<int>& nums) {
    int x = 0;
    for (int v : nums) x ^= v;
    return x;
}
```

**Java**
```java
static int singleNumber(int[] nums) {
    int x = 0;
    for (int v : nums) x ^= v;
    return x;
}
```

**Python**
```python
def single_number(nums):
    x = 0
    for v in nums:
        x ^= v
    return x
```

**Complexity:** time **O(n)**, space **O(1)** — one pass, one accumulator.

---

## Edge cases

- n = 1.
- The single number is 0 or negative — XOR handles both.

---

## Common mistakes

1. Summing instead of XOR (`2·Σdistinct − Σ` works but needs a set → O(n) space).

---

## Follow-ups

1. Missing number in 0…n (LC 268).
2. Find the duplicate when one value appears twice and 1…n−1 once.

<details><summary>Answer sketches</summary>

**#1:** XOR all indices 0…n and all values; the missing one survives.

**#2:** XOR values with 1…n−1.
</details>

---

## Flashcards

**Why does XOR-all find the single number?** #flashcard
x ^ x = 0, x ^ 0 = x, and XOR is commutative/associative, so pairs cancel.

**Missing number via XOR?** #flashcard
XOR of 0…n and all elements.

**Interview track →** [Bit manipulation deep-dive](../../02-algorithms/17-bit-manipulation.md)
