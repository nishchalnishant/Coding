---
module: striver-a2z/18-recursion
lesson: 7
topic: Check if There Exists a Subsequence with Sum K
difficulty: Medium
source: https://takeuforward.org/learning/dsa/check-if-there-exists-a-subsequence-with-sum-k?category=subsequence-pattern-problems&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, dp, subsequence]
---
# 7. Check if There Exists a Subsequence with Sum K

← [Reverse a Stack](06-reverse-a-stack.md) · [Part 18 index](README.md) · Next → [Count All Subsequences with Sum K](08-count-subsequences-sum-k.md)

> [!abstract] Problem at a glance
> **Task:** Return whether some subsequence (subset) of a positive array sums to `k`.
> **Key insight:** Pick/not-pick recursion with a **boolean return**: return true as soon as any branch succeeds, which prunes the rest. Positive values let you also stop when the sum exceeds k. Memoising on (i, remaining) turns 2ⁿ into O(n · k) subset-sum DP.
> **Difficulty:** Medium · **Pattern:** Pick / not-pick → subset-sum DP · **Also on:** [GfG Subset Sum](https://www.geeksforgeeks.org/problems/subset-sum-problem-1611555638/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-if-there-exists-a-subsequence-with-sum-k?category=subsequence-pattern-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Pick / not-pick recursion](#3-pick--not-pick-recursion) · [4. Memoised recursion](#4-memoised-recursion) · [5. 1D subset-sum DP](#5-1d-subset-sum-dp) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums` of positive integers and an integer `k`, return `true` if there is a subsequence (elements in original order, not necessarily contiguous) whose sum is exactly `k`.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 3, 4, 5], k = 8` | `true` | [1, 2, 5] or [3, 5] … |
| `nums = [4, 3, 9, 2], k = 10` | `false` |  |
| `nums = [1, 10, 4, 5], k = 16` | `true` | 1 + 10 + 5 |

**Constraints:** `1 ≤ n ≤ 2000`, `1 ≤ nums[i] ≤ 1000`, `1 ≤ k ≤ 2000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Pick / not-pick recursion | f(i, s): take nums[i] or skip; true if either is | O(2ⁿ) | O(n) |
| Memoised recursion | cache f(i, rem) | O(n · k) | O(n · k) |
| 1D subset-sum DP | can[s] |= can[s − x], s from k down to x | O(n · k) | O(k) |

> [!tip] Interview angle
> This is the "return as soon as found" variant of the subsequence template: `if (take) return true; return skip`. Then the interviewer asks for better than 2ⁿ — show memoisation and the 1D DP (iterate sums downward so each item is used once). It is the classic 0/1 knapsack feasibility problem.

---

## 3. Pick / not-pick recursion

**Intuition.** `f(i, rem)`: if `rem == 0` → true; if `i == n` or `rem < 0` → false. Return `f(i + 1, rem − nums[i]) or f(i + 1, rem)`. Short-circuit `or` stops after the first success.

```python
def has_sum_rec(nums, k):
    def f(i, rem):
        if rem == 0:
            return True
        if i == len(nums) or rem < 0:
            return False
        return f(i + 1, rem - nums[i]) or f(i + 1, rem)
    return f(0, k)
```

**Complexity:** time **O(2ⁿ)**, space **O(n)**.

---

## 4. Memoised recursion

**Intuition.** Only n · (k + 1) distinct states exist, so cache them. This is the bridge from recursion to DP.

```python
from functools import lru_cache
def has_sum_memo(nums, k):
    @lru_cache(None)
    def f(i, rem):
        if rem == 0:
            return True
        if i == len(nums) or rem < 0:
            return False
        return f(i + 1, rem - nums[i]) or f(i + 1, rem)
    return f(0, k)
```

**Complexity:** time **O(n · k)**, space **O(n · k)**.

---

## 5. 1D subset-sum DP

**Intuition.** `can[s]` = some subset of the items seen so far sums to s. Start `can[0] = true`. For each `x`, update `s = k … x` **downwards** so `can[s − x]` still refers to the previous items (each item used at most once).

**Algorithm**

1. `can = [true, false × k]`.
2. For each x: for s = k down to x: `can[s] = can[s] || can[s − x]`.
3. Return `can[k]`.

**Dry run** — [4, 3, 9, 2], k = 10: after 4 → {0,4}; 3 → {0,3,4,7}; 9 → {…,9}; 2 → {0,2,3,4,5,6,7,9} — 10 missing → false.

**C++**
```cpp
bool checkSubsequenceSum(vector<int>& nums, int k) {
    vector<char> can(k + 1, 0);
    can[0] = 1;
    for (int x : nums)
        for (int s = k; s >= x; s--)
            if (can[s - x]) can[s] = 1;
    return can[k];
}
```

**Java**
```java
static boolean checkSubsequenceSum(int[] nums, int k) {
    boolean[] can = new boolean[k + 1];
    can[0] = true;
    for (int x : nums)
        for (int s = k; s >= x; s--)
            if (can[s - x]) can[s] = true;
    return can[k];
}
```

**Python**
```python
def check_subsequence_sum(nums, k):
    can = [True] + [False] * k
    for x in nums:
        for s in range(k, x - 1, -1):
            if can[s - x]:
                can[s] = True
    return can[k]
```

**Complexity:** time **O(n · k)**, space **O(k)** — n items × k sums; one row reused.

---

## Edge cases

- Single element equal / not equal to k.
- All elements larger than k.
- k equals the total sum.

---

## Common mistakes

1. Iterating sums upward in the 1D DP — reuses an item (unbounded knapsack).
2. Forgetting `rem < 0` pruning (or relying on it with negative numbers, where it's wrong).
3. Exploring the skip branch even after take returned true.

---

## Follow-ups

1. Print one such subsequence.
2. Elements may be negative.
3. Partition into two equal-sum halves (LC 416).

<details><summary>Answer sketches</summary>

**#1:** Recursion: push, recurse, return true up the chain without popping; or backtrack through a 2D DP table.

**#2:** `rem < 0` pruning is invalid; shift sums by the negative total or use a set of reachable sums.

**#3:** Same DP with k = total / 2 (total must be even).
</details>

---

## Flashcards

**Subsequence-sum exists: recursion shape?** #flashcard
return f(i+1, rem − a[i]) || f(i+1, rem); base rem == 0 → true.

**Why iterate s downward in 1D 0/1 subset-sum?** #flashcard
So can[s − x] still describes subsets without the current item.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../04-practice/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../04-practice/algorithms/12-backtracking.md)
