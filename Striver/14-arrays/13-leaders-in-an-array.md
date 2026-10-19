---
module: striver/14-arrays
lesson: 13
topic: Leaders in an Array
difficulty: Easy
source: https://takeuforward.org/learning/dsa/leaders-in-an-array?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, suffix-max]
---
# 13. Leaders in an Array

← [Majority Element I](12-majority-element.md) · [Part 14 index](README.md) · Next → [Rearrange Array Elements by Sign](14-rearrange-by-sign.md)

> [!abstract] Problem at a glance
> **Task:** Return all leaders in order of appearance: elements strictly greater than every element to their right.
> **Key insight:** Scan from the right keeping `maxRight`. An element is a leader iff it beats `maxRight`. Collect, then reverse to restore left-to-right order. O(n) instead of O(n²).
> **Difficulty:** Easy · **Pattern:** Suffix maximum · **Also on:** GfG Leaders in an Array
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/leaders-in-an-array?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Check every right side](#3-check-every-right-side) · [4. Right-to-left suffix max](#4-right-to-left-suffix-max) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, return all leaders, in the order they appear. An element is a leader if it is strictly greater than all elements to its right. The last element is always a leader.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 5, 3, 1, 2]` | `[5, 3, 2]` |  |
| `nums = [-3, 4, 5, 1, -4, -5]` | `[5, 1, -4, -5]` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, `−10⁹ ≤ nums[i] ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Check every right side | nested loops | O(n²) | O(1) |
| Right-to-left suffix max | leader iff nums[i] > maxRight | O(n) | O(1) beyond the output |

---

## 3. Check every right side

**Intuition.** For each `i`, scan `i + 1..n − 1` for anything `>=`; if none, it's a leader.

```python
def leaders_brute(nums):
    n = len(nums)
    return [nums[i] for i in range(n) if all(nums[i] > nums[j] for j in range(i + 1, n))]
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Right-to-left suffix max

**Intuition.** `maxRight` = max of everything to the right of `i`. Walking from the right maintains it in O(1) per step. Strict `>` because the definition is "strictly greater": with `[5, 5]`, only the last 5 is a leader.

**C++**
```cpp
vector<int> leaders(vector<int>& nums) {
    vector<int> res;
    int maxRight = INT_MIN;
    for (int i = (int)nums.size() - 1; i >= 0; i--) {
        if (nums[i] > maxRight) {
            res.push_back(nums[i]);
            maxRight = nums[i];
        }
    }
    reverse(res.begin(), res.end());
    return res;
}
```

**Java**
```java
static List<Integer> leaders(int[] nums) {
    ArrayList<Integer> res = new ArrayList<>();
    long maxRight = Long.MIN_VALUE;
    for (int i = nums.length - 1; i >= 0; i--) {
        if (nums[i] > maxRight) {
            res.add(nums[i]);
            maxRight = nums[i];
        }
    }
    Collections.reverse(res);
    return res;
}
```

**Python**
```python
def leaders(nums):
    res, max_right = [], float("-inf")
    for x in reversed(nums):
        if x > max_right:
            res.append(x)
            max_right = x
    return res[::-1]
```

**Complexity:** time **O(n)**, space **O(1) beyond the output**.

---

## Edge cases

- Strictly decreasing → all are leaders.
- Increasing → only the last.
- Equal neighbours: only the rightmost counts.

---

## Common mistakes

1. `>=` instead of `>` (duplicates become leaders).
2. Seeding `maxRight` with 0 or −1 when negatives exist.
3. Forgetting to reverse the collected list.

---

## Follow-ups

1. Replace each element with the greatest element to its right (LC 1299).
2. Next greater element for every index.

<details><summary>Answer sketches</summary>

**#1:** Same right-to-left scan; write `maxRight` before updating it.

**#2:** Monotonic stack ([Part 23](../23-stack-and-queues/README.md)).
</details>

---

## Flashcards

**Leaders: scan direction and state?** #flashcard
Right to left with maxRight.

**Leader condition?** #flashcard
nums[i] > maxRight (strict).

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../coding/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../coding/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
