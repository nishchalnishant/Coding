---
module: striver-a2z/28-dynamic-programming
lesson: 36
topic: Number of longest increasing subsequences
difficulty: Medium
source: https://takeuforward.org/learning/dsa/number-of-longest-increasing-subsequences?category=lis-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, lis, counting]
---
# 36. Number of longest increasing subsequences

← [Longest bitonic subsequence](35-longest-bitonic-subsequence.md) · [Part 28 index](README.md) · Next → [Longest common subsequence](37-longest-common-subsequence.md)

> [!abstract] Problem at a glance
> **Task:** Count the strictly increasing subsequences that have the maximum length.
> **Key insight:** Alongside `dp[i]` (LIS length ending at `i`), keep `cnt[i]` (how many such LIS end at `i`). For `a[j] < a[i]`: if `dp[j] + 1 > dp[i]`, **reset** `cnt[i] = cnt[j]`; if equal, **add** `cnt[i] += cnt[j]`. The answer sums `cnt[i]` over all `i` with `dp[i] == max`.
> **Difficulty:** Medium · **Pattern:** LIS + counting · **Also on:** LC 673
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/number-of-longest-increasing-subsequences?category=lis-dp&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. dp + cnt arrays](#3-dp--cnt-arrays) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `nums`, return the number of longest strictly increasing subsequences (counted by index positions).

| Input | Output | Why |
|---|---|---|
| `[1,3,5,4,7]` | `2` | 1,3,4,7 and 1,3,5,7 |
| `[2,2,2,2,2]` | `5` | each single element |

**Constraints:** `1 ≤ n ≤ 2000`, `−10⁶ ≤ nums[i] ≤ 10⁶`, answer fits in 32-bit.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| dp + cnt arrays | reset on longer, add on equal | O(n²) | O(n) |

> [!tip] Interview angle
> State both arrays and the reset-vs-add rule clearly. The common bug is adding when the length strictly improves.

---

## 3. dp + cnt arrays

**Intuition.** Each `j` with `a[j] < a[i]` either gives a longer chain (replace the count) or an equally long one (add its count).

**Algorithm**

1. `dp = cnt = [1]*n`.
2. For `i`, `j < i`, `a[j] < a[i]`: if `dp[j]+1 > dp[i]`: `dp[i] = dp[j]+1, cnt[i] = cnt[j]`; elif equal: `cnt[i] += cnt[j]`.
3. `L = max dp`; return `Σ cnt[i]` where `dp[i] == L`.

**Dry run** — [1,3,5,4,7]: dp = [1,2,3,3,4], cnt = [1,1,1,1,2] → 2.

**C++**
```cpp
int findNumberOfLIS(vector<int>& a) {
    int n = a.size(), L = 0, ans = 0;
    vector<int> dp(n, 1), cnt(n, 1);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (a[j] >= a[i]) continue;
            if (dp[j] + 1 > dp[i]) {
                dp[i] = dp[j] + 1;
                cnt[i] = cnt[j];
            } else if (dp[j] + 1 == dp[i]) {
                cnt[i] += cnt[j];
            }
        }
        L = max(L, dp[i]);
    }
    for (int i = 0; i < n; i++)
        if (dp[i] == L) ans += cnt[i];
    return ans;
}
```

**Java**
```java
static int findNumberOfLIS(int[] a) {
    int n = a.length, L = 0, ans = 0;
    int[] dp = new int[n], cnt = new int[n];
    for (int i = 0; i < n; i++) {
        dp[i] = cnt[i] = 1;
        for (int j = 0; j < i; j++) {
            if (a[j] >= a[i]) continue;
            if (dp[j] + 1 > dp[i]) {
                dp[i] = dp[j] + 1;
                cnt[i] = cnt[j];
            } else if (dp[j] + 1 == dp[i]) {
                cnt[i] += cnt[j];
            }
        }
        L = Math.max(L, dp[i]);
    }
    for (int i = 0; i < n; i++)
        if (dp[i] == L) ans += cnt[i];
    return ans;
}
```

**Python**
```python
def find_number_of_lis(a):
    n = len(a)
    dp, cnt = [1] * n, [1] * n
    for i in range(n):
        for j in range(i):
            if a[j] < a[i]:
                if dp[j] + 1 > dp[i]:
                    dp[i], cnt[i] = dp[j] + 1, cnt[j]
                elif dp[j] + 1 == dp[i]:
                    cnt[i] += cnt[j]
    L = max(dp)
    return sum(c for d, c in zip(dp, cnt) if d == L)
```

**Complexity:** time **O(n²)**, space **O(n)** — the O(n²) LIS with one extra array (O(n log n) needs a Fenwick tree over values).

---

## Edge cases

- All equal: n (each element alone).
- Strictly increasing: 1.

---

## Common mistakes

1. `cnt[i] += cnt[j]` on a strict improvement (must reset).
2. Returning `cnt[argmax]` instead of summing over every index with max length.

---

## Follow-ups

1. O(n log n)?
2. Count all increasing subsequences?

<details><summary>Answer sketches</summary>

**#1:** Fenwick/segment tree keyed by value storing (best length, count) pairs.

**#2:** `cnt[i] = 1 + Σ cnt[j]` over smaller earlier elements.
</details>

---

## Flashcards

**Number of LIS update rule?** #flashcard
Longer → reset to cnt[j]; equal → add cnt[j].

**Final answer?** #flashcard
Σ cnt[i] over i with dp[i] == max.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
