---
module: striver/22-sliding-window-and-2-pointer
lesson: 4
topic: Max Consecutive Ones III
difficulty: Medium
source: https://takeuforward.org/learning/dsa/max-consecutive-ones-iii?category=longest-and-smallest-window-problems&source=strivers-a2z-dsa-sheet
tags: [striver, sliding-window-and-2-pointer, sliding-window, arrays, budget-window]
---
# 4. Max Consecutive Ones III

← [Longest Substring Without Repeating Characters](03-longest-substring-without-repeating-characters.md) · [Part 22 index](README.md) · Next → [Fruit Into Baskets](05-fruit-into-baskets.md)

> [!abstract] Problem at a glance
> **Task:** Longest run of 1s in a binary array if you may flip at most `k` zeros.
> **Key insight:** Rephrase: longest window containing at most `k` zeros. Expand right, count zeros, shrink left while zeros exceed `k`. The no-shrink variant moves `l` by at most one per step, so the window size never decreases and its final size is the answer.
> **Difficulty:** Medium · **Pattern:** Variable window with a budget (at most k bad elements) · **Also on:** [LC 1004](https://leetcode.com/problems/max-consecutive-ones-iii/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/max-consecutive-ones-iii?category=longest-and-smallest-window-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force: every start](#3-brute-force-every-start) · [4. Shrinking window](#4-shrinking-window) · [5. Non-shrinking window](#5-non-shrinking-window) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a binary array `nums` and an integer `k`, return the maximum number of consecutive 1s in the array if you can flip at most `k` 0s.

| Input | Output | Why |
|---|---|---|
| `nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2` | `6` | flip the zeros at indices 5 and 10 → window 5..10 is all 1s |
| `nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3` | `10` |  |

**Constraints:** `1 ≤ nums.length ≤ 10⁵`, `nums[i] ∈ {0, 1}`, `0 ≤ k ≤ nums.length`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force: every start | extend each start until zeros > k | O(n²) | O(1) |
| Shrinking window | while zeros > k: drop nums[l] | O(n) | O(1) |
| Non-shrinking window | if zeros > k: move l once | O(n) | O(1) |

> [!tip] Interview angle
> The rephrase is the whole problem: "flip at most k" is "window with at most k zeros". Interviewers like the no-shrink trick as a follow-up; know why it's correct.

---

## 3. Brute force: every start

**Intuition.** For each start, extend right while the zero count stays ≤ k. Track the longest.

```python
def longest_ones_brute(nums, k):
    best = 0
    for i in range(len(nums)):
        zeros = 0
        for j in range(i, len(nums)):
            zeros += nums[j] == 0
            if zeros > k:
                break
            best = max(best, j - i + 1)
    return best
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Shrinking window

**Intuition.** Expand `r`; on a zero increment the count. While the count exceeds `k`, remove `nums[l]` and move `l`. The window is always valid, so record its length.

```python
def longest_ones_shrink(nums, k):
    l = zeros = best = 0
    for r, x in enumerate(nums):
        zeros += x == 0
        while zeros > k:
            zeros -= nums[l] == 0
            l += 1
        best = max(best, r - l + 1)
    return best
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 5. Non-shrinking window

**Intuition.** Replace `while` with `if`. When the window becomes invalid, slide it (both ends move by one) instead of shrinking it. The window length never drops, it only grows when a longer valid window exists, so `n − l` at the end is the answer.

**Algorithm**

1. `l = zeros = 0`.
2. For each `r`: if `nums[r] == 0`, `zeros += 1`.
3. If `zeros > k`: if `nums[l] == 0`, `zeros -= 1`; `l += 1`.
4. Return `len(nums) − l`.

**Dry run** — [1,0,0,1], k=1: r0 → r1 z=1 → r2 z=2 > 1: drop nums[0]=1, l=1 (window size stays 2) → r3: z=2 > 1: drop nums[1]=0, z=1, l=2. Answer 4−2 = 2.

**C++**
```cpp
int longestOnes(vector<int>& nums, int k) {
    int l = 0, zeros = 0;
    for (int r = 0; r < (int)nums.size(); r++) {
        if (nums[r] == 0) zeros++;
        if (zeros > k) {
            if (nums[l] == 0) zeros--;
            l++;
        }
    }
    return nums.size() - l;
}
```

**Java**
```java
static int longestOnes(int[] nums, int k) {
    int l = 0, zeros = 0;
    for (int r = 0; r < nums.length; r++) {
        if (nums[r] == 0) zeros++;
        if (zeros > k) {
            if (nums[l] == 0) zeros--;
            l++;
        }
    }
    return nums.length - l;
}
```

**Python**
```python
def longest_ones(nums, k):
    l = zeros = 0
    for x in nums:
        zeros += x == 0
        if zeros > k:
            zeros -= nums[l] == 0
            l += 1
    return len(nums) - l
```

**Complexity:** time **O(n)**, space **O(1)** — each index enters once and `l` advances at most once per step.

---

## Edge cases

- `k = 0` → longest run of 1s.
- `k ≥ number of zeros` → `n`.
- All zeros with `k = 0` → 0.

---

## Common mistakes

1. Counting flipped 1s instead of zeros.
2. Recording `best` inside the non-shrinking version (the window may be invalid at that moment; only the final size is meaningful).
3. Flipping greedily the first k zeros, with no window at all.

---

## Follow-ups

1. Exactly k flips must be used.
2. Stream of bits, answer after each.

<details><summary>Answer sketches</summary>

**#1:** If there are at least k zeros the answer is unchanged (an optimal window uses all k); otherwise flips must hit 1s and the answer is n.

**#2:** The shrinking window works online; keep the zero positions in a deque for O(1) jumps.
</details>

---

## Flashcards

**Max Consecutive Ones III rephrased?** #flashcard
Longest window with at most k zeros.

**Why is the non-shrinking window correct?** #flashcard
Its length never decreases and only grows when a valid longer window ends at r; final length = best length.

**Interview track →** [Sliding-window deep-dive](../../02-algorithms/04-sliding-window.md) · [Two-pointers deep-dive](../../02-algorithms/03-two-pointers.md) · [Sliding-window walkthroughs](../../coding/algorithms/04-sliding-window.md)
