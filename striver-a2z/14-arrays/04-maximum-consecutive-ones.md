---
module: striver-a2z/14-arrays
lesson: 4
topic: Maximum Consecutive Ones
difficulty: Easy
source: https://takeuforward.org/learning/dsa/maximum-consecutive-ones?category=fundamentals&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, traversal]
---
# 4. Maximum Consecutive Ones

← [Second Largest Element](03-second-largest-element.md) · [Part 14 index](README.md) · Next → [Left Rotate Array by One](05-left-rotate-array-by-one.md)

> [!abstract] Problem at a glance
> **Task:** Return the length of the longest run of consecutive 1s in a binary array.
> **Key insight:** Keep a running streak: +1 on a 1, reset to 0 on a 0, and record the best after every step.
> **Difficulty:** Easy · **Pattern:** Array traversal: running streak · **Also on:** [LC 485](https://leetcode.com/problems/max-consecutive-ones/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/maximum-consecutive-ones?category=fundamentals&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Running streak](#3-running-streak) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a binary array `nums`, return the maximum number of consecutive `1`s.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 1, 0, 0, 1, 1, 1, 0]` | `3` |  |
| `nums = [0, 0, 0]` | `0` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, `nums[i] ∈ {0, 1}`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Running streak | cnt++ on 1, cnt = 0 on 0 | O(n) | O(1) |

---

## 3. Running streak

**Intuition.** `cnt` is the length of the run ending at the current index. Update `best` on every 1, not only when a 0 arrives, or a run that reaches the end of the array is missed.

**C++**
```cpp
int findMaxConsecutiveOnes(vector<int>& nums) {
    int cnt = 0, best = 0;
    for (int x : nums) {
        cnt = x == 1 ? cnt + 1 : 0;
        best = max(best, cnt);
    }
    return best;
}
```

**Java**
```java
static int findMaxConsecutiveOnes(int[] nums) {
    int cnt = 0, best = 0;
    for (int x : nums) {
        cnt = x == 1 ? cnt + 1 : 0;
        best = Math.max(best, cnt);
    }
    return best;
}
```

**Python**
```python
def max_consecutive_ones(nums):
    cnt = best = 0
    for x in nums:
        cnt = cnt + 1 if x == 1 else 0
        best = max(best, cnt)
    return best
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- All zeros → 0.
- All ones → n.
- Longest run at the end.

---

## Common mistakes

1. Updating `best` only when a 0 is seen → misses a trailing run.

---

## Follow-ups

1. Max Consecutive Ones III (LC 1004): flip at most k zeros.
2. Max Consecutive Ones II: flip at most one zero.

<details><summary>Answer sketches</summary>

**#1:** Sliding window keeping ≤ k zeros inside ([Part 22](../22-sliding-window-and-2-pointer/README.md)).

**#2:** Same window with k = 1, or track lengths of the previous and current runs.
</details>

---

## Flashcards

**Max consecutive ones: when to update best?** #flashcard
After every element, so a trailing run counts.

**Flip up to k zeros for the longest 1-run?** #flashcard
Sliding window with zero-count ≤ k.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../04-practice/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../04-practice/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
