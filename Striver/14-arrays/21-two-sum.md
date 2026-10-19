---
module: striver/14-arrays
lesson: 21
topic: Two Sum
difficulty: Easy
source: https://takeuforward.org/learning/dsa/two-sum?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, hashing, two-pointers]
---
# 21. Two Sum

← [Set Matrix Zeroes](20-set-matrix-zeroes.md) · [Part 14 index](README.md) · Next → [3 Sum](22-3-sum.md)

> [!abstract] Problem at a glance
> **Task:** Return the indices `[i, j]` (`i < j`) of the two numbers that add up to `target`. Exactly one solution exists.
> **Key insight:** For each `x`, the partner it needs is `target − x`. A hash map from value to index answers "have I seen the partner?" in O(1). Check before inserting, so an element isn't paired with itself.
> **Difficulty:** Easy · **Pattern:** Hash map complement lookup · **Also on:** [LC 1](https://leetcode.com/problems/two-sum/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/two-sum?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. All pairs](#3-all-pairs) · [4. Sort pairs + two pointers](#4-sort-pairs--two-pointers) · [5. One-pass hash map](#5-one-pass-hash-map) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums` and an integer `target`, return the indices of the two numbers that add up to `target`, in increasing order. Each input has exactly one solution, and the same element may not be used twice.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 6, 2, 10, 3], target = 7` | `[0, 1]` | 1 + 6 |
| `nums = [3, 3], target = 6` | `[0, 1]` |  |

**Constraints:** `2 ≤ n ≤ 10⁴`, `−10⁹ ≤ nums[i], target ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| All pairs | nested loops | O(n²) | O(1) |
| Sort pairs + two pointers | sort (value, index); shrink from both ends | O(n log n) | O(n) |
| One-pass hash map | seen[value] = index; look up target − x first | O(n) | O(n) |

> [!tip] Interview angle
> Ask whether they want indices or just yes/no, and whether the array is sorted. Sorted with two pointers is O(1) space but loses the original indices unless you sort `(value, index)` pairs.

---

## 3. All pairs

**Intuition.** Try every pair `i < j`.

```python
def two_sum_brute(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Sort pairs + two pointers

**Intuition.** Sort `(value, index)` pairs. If the sum at `l, r` is too small, `l++`; too big, `r−−`. This is the version that wins when the input is already sorted (Two Sum II, LC 167), because then it's O(n) time and O(1) space.

```python
def two_sum_two_ptr(nums, target):
    a = sorted((v, i) for i, v in enumerate(nums))
    l, r = 0, len(a) - 1
    while l < r:
        s = a[l][0] + a[r][0]
        if s == target:
            return sorted([a[l][1], a[r][1]])
        if s < target:
            l += 1
        else:
            r -= 1
```

**Complexity:** time **O(n log n)**, space **O(n)**.

---

## 5. One-pass hash map

**Intuition.** Walking left to right, `seen` holds the values at indices `< i`. If `target − nums[i]` is in it, those two indices are the answer. Looking up before inserting means `[3, 3]` with target 6 works, and `x` can never pair with itself.

**Dry run** — `[1 6 2 10 3]`, t = 7: i=0 need 6, seen {} → add 1:0; i=1 need 1 → found 0 → [0, 1].

**C++**
```cpp
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> seen;
    for (int i = 0; i < (int)nums.size(); i++) {
        auto it = seen.find(target - nums[i]);
        if (it != seen.end()) return {it->second, i};
        seen[nums[i]] = i;
    }
    return {-1, -1};
}
```

**Java**
```java
static int[] twoSum(int[] nums, int target) {
    HashMap<Integer, Integer> seen = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        Integer j = seen.get(target - nums[i]);
        if (j != null) return new int[]{j, i};
        seen.put(nums[i], i);
    }
    return new int[]{-1, -1};
}
```

**Python**
```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## Edge cases

- Duplicates that form the answer (`[3, 3]`).
- Negatives and zero.
- `target − x` overflows int in C++/Java at the extremes (use long if values reach ±2·10⁹).

---

## Common mistakes

1. Inserting before checking → an element pairs with itself when `x = target / 2`.
2. Sorting the values and returning their *new* indices.
3. Returning values instead of indices.

---

## Follow-ups

1. Sorted input (LC 167).
2. Count all pairs with sum = target.
3. 3Sum / 4Sum.
4. Data stream: add(x), find(target) (LC 170).

<details><summary>Answer sketches</summary>

**#1:** Two pointers, O(n)/O(1).

**#2:** Hash map of counts: add `cnt[target − x]` before incrementing `cnt[x]`.

**#3:** Sort + fix elements + two pointers: [3 Sum](22-3-sum.md), [4 Sum](23-4-sum.md).

**#4:** Count map; find is O(n) over distinct keys, or keep a set of all pair sums when finds dominate.
</details>

---

## Flashcards

**Two Sum O(n) idea?** #flashcard
Hash map value → index; look up target − x before inserting x.

**Two Sum on sorted input?** #flashcard
Two pointers from both ends: O(n), O(1).

**Why check before inserting?** #flashcard
So an element can't pair with itself.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../coding/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../coding/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
