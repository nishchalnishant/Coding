---
module: striver/28-dynamic-programming
lesson: 33
topic: Largest divisible subset
difficulty: Medium
source: https://takeuforward.org/learning/dsa/largest-divisible-subset?category=lis-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, lis, math]
---
# 33. Largest divisible subset

← [Print longest increasing subsequence](32-print-longest-increasing-subsequence.md) · [Part 28 index](README.md) · Next → [Longest string chain](34-longest-string-chain.md)

> [!abstract] Problem at a glance
> **Task:** Largest subset of distinct positives where every pair `(a, b)` has `a | b` or `b | a`.
> **Key insight:** Sort ascending. Then a valid subset is a chain `x₁ | x₂ | … | x_k`, and divisibility is transitive, so checking only adjacent elements suffices. This is **LIS with `a[i] % a[j] == 0` instead of `a[j] < a[i]`**, plus parent reconstruction.
> **Difficulty:** Medium · **Pattern:** LIS variant (sort + chain condition) · **Also on:** LC 368
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/largest-divisible-subset?category=lis-dp&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Sort + LIS-style dp + parent](#3-sort--lis-style-dp--parent) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a set of distinct positive integers `nums`, return the largest subset `answer` such that for every pair, `answer[i] % answer[j] == 0` or `answer[j] % answer[i] == 0`. Any valid answer is accepted.

| Input | Output | Why |
|---|---|---|
| `[1,2,3]` | `[1,2]` | [1,3] also valid |
| `[1,2,4,8]` | `[1,2,4,8]` |  |

**Constraints:** `1 ≤ n ≤ 1000`, `1 ≤ nums[i] ≤ 2·10⁹`, all distinct.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Sort + LIS-style dp + parent | dp[i] = 1 + max dp[j] with a[i] % a[j] == 0 | O(n²) | O(n) |

> [!tip] Interview angle
> Justify the sort: after sorting, "pairwise divisible" collapses to "each divides the next" because of transitivity. Then it is the print-LIS code with one changed comparison.

---

## 3. Sort + LIS-style dp + parent

**Intuition.** After sorting, `dp[i]` = largest chain ending at `a[i]`. Reconstruct via `parent`.

**Algorithm**

1. Sort.
2. For `i`, `j < i`: if `a[i] % a[j] == 0` and `dp[j] + 1 > dp[i]`, update `dp[i]`, `parent[i]`.
3. Walk back from `argmax dp`.

**Dry run** — [1,2,4,8] sorted: dp = [1,2,3,4] → walk 8 → 4 → 2 → 1.

**C++**
```cpp
vector<int> largestDivisibleSubset(vector<int>& nums) {
    vector<int> a = nums;
    sort(a.begin(), a.end());
    int n = a.size(), last = 0;
    vector<int> dp(n, 1), parent(n);
    for (int i = 0; i < n; i++) {
        parent[i] = i;
        for (int j = 0; j < i; j++)
            if (a[i] % a[j] == 0 && dp[j] + 1 > dp[i]) {
                dp[i] = dp[j] + 1;
                parent[i] = j;
            }
        if (dp[i] > dp[last]) last = i;
    }
    vector<int> res = {a[last]};
    while (parent[last] != last) {
        last = parent[last];
        res.push_back(a[last]);
    }
    return res;
}
```

**Java**
```java
static int[] largestDivisibleSubset(int[] nums) {
    int[] a = nums.clone();
    Arrays.sort(a);
    int n = a.length, last = 0;
    int[] dp = new int[n], parent = new int[n];
    for (int i = 0; i < n; i++) {
        dp[i] = 1;
        parent[i] = i;
        for (int j = 0; j < i; j++)
            if (a[i] % a[j] == 0 && dp[j] + 1 > dp[i]) {
                dp[i] = dp[j] + 1;
                parent[i] = j;
            }
        if (dp[i] > dp[last]) last = i;
    }
    int[] res = new int[dp[last]];
    for (int k = 0; k < res.length; k++) {
        res[k] = a[last];
        last = parent[last];
    }
    return res;
}
```

**Python**
```python
def largest_divisible_subset(nums):
    a = sorted(nums)
    n = len(a)
    dp, parent = [1] * n, list(range(n))
    for i in range(n):
        for j in range(i):
            if a[i] % a[j] == 0 and dp[j] + 1 > dp[i]:
                dp[i], parent[i] = dp[j] + 1, j
    last = max(range(n), key=dp.__getitem__)
    res = [a[last]]
    while parent[last] != last:
        last = parent[last]
        res.append(a[last])
    return res
```

**Complexity:** time **O(n²)**, space **O(n)** — sort plus the O(n²) chain DP.

---

## Edge cases

- Single element: itself.
- Pairwise coprime (no 1): any single element.

---

## Common mistakes

1. Not sorting (then adjacency checks are insufficient).
2. Checking `a[j] % a[i]` after sorting ascending (reversed).

---

## Follow-ups

1. Count the subsets?
2. Why does transitivity matter?

<details><summary>Answer sketches</summary>

**#1:** Sum over predecessors instead of max.

**#2:** It means checking adjacent pairs in sorted order covers all pairs.
</details>

---

## Flashcards

**Largest divisible subset = ?** #flashcard
Sort, then LIS with `a[i] % a[j] == 0`.

**Why sort first?** #flashcard
It turns pairwise divisibility into an adjacent-chain condition.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
