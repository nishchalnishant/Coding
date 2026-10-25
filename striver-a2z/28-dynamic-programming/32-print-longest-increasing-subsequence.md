---
module: striver-a2z/28-dynamic-programming
lesson: 32
topic: Print longest increasing subsequence
difficulty: Medium
source: https://takeuforward.org/learning/dsa/print-longest-increasing-subsequence?category=lis-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, lis, reconstruction]
---
# 32. Print longest increasing subsequence

← [Longest increasing subsequence](31-longest-increasing-subsequence.md) · [Part 28 index](README.md) · Next → [Largest divisible subset](33-largest-divisible-subset.md)

> [!abstract] Problem at a glance
> **Task:** Return one longest strictly increasing subsequence (the elements, not just the length).
> **Key insight:** Run the O(n²) `dp[i]` = LIS ending at `i` and also record `parent[i]`, the `j` that gave the best extension. Start at `argmax dp` and follow parents back, then reverse. This is the standard DP reconstruction: **store the choice, walk it backward**.
> **Difficulty:** Medium · **Pattern:** LIS + parent pointers
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/print-longest-increasing-subsequence?category=lis-dp&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. dp + parent array](#3-dp--parent-array) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `arr`, return any longest strictly increasing subsequence as a list of values.

| Input | Output | Why |
|---|---|---|
| `[5,4,11,1,16,8]` | `[5,11,16]` | length 3; [4,11,16] is also valid |
| `[1,2,2]` | `[1,2]` |  |

**Constraints:** `1 ≤ n ≤ 10³`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| dp + parent array | parent[i] = best predecessor | O(n²) | O(n) |

> [!tip] Interview angle
> Ask whether any LIS is fine or a specific one (lexicographically smallest, first-occurring). The parent array works for either with a tie rule. For O(n log n) reconstruction, store for each tail slot the index it came from.

---

## 3. dp + parent array

**Intuition.** While computing `dp[i]`, set `parent[i] = j` whenever `dp[j] + 1` improves it. `parent[i] = i` marks a start.

**Algorithm**

1. `dp = [1]*n`, `parent[i] = i`.
2. For `i`, for `j < i` with `a[j] < a[i]` and `dp[j] + 1 > dp[i]`: update both.
3. From `last = argmax dp`, follow `parent` until it is a self-loop; reverse.

**Dry run** — [5,4,11,1,16,8]: dp = [1,1,2,1,3,2], parent[4] = 2, parent[2] = 0 → [5,11,16].

**C++**
```cpp
vector<int> longestIncreasingSubsequence(vector<int>& a) {
    int n = a.size(), last = 0;
    vector<int> dp(n, 1), parent(n);
    for (int i = 0; i < n; i++) {
        parent[i] = i;
        for (int j = 0; j < i; j++)
            if (a[j] < a[i] && dp[j] + 1 > dp[i]) {
                dp[i] = dp[j] + 1;
                parent[i] = j;
            }
        if (dp[i] > dp[last]) last = i;
    }
    vector<int> seq = {a[last]};
    while (parent[last] != last) {
        last = parent[last];
        seq.push_back(a[last]);
    }
    reverse(seq.begin(), seq.end());
    return seq;
}
```

**Java**
```java
static int[] longestIncreasingSubsequence(int[] a) {
    int n = a.length, last = 0;
    int[] dp = new int[n], parent = new int[n];
    for (int i = 0; i < n; i++) {
        dp[i] = 1;
        parent[i] = i;
        for (int j = 0; j < i; j++)
            if (a[j] < a[i] && dp[j] + 1 > dp[i]) {
                dp[i] = dp[j] + 1;
                parent[i] = j;
            }
        if (dp[i] > dp[last]) last = i;
    }
    int[] seq = new int[dp[last]];
    for (int k = seq.length - 1; k >= 0; k--) {
        seq[k] = a[last];
        last = parent[last];
    }
    return seq;
}
```

**Python**
```python
def print_lis(a):
    n = len(a)
    dp, parent = [1] * n, list(range(n))
    for i in range(n):
        for j in range(i):
            if a[j] < a[i] and dp[j] + 1 > dp[i]:
                dp[i], parent[i] = dp[j] + 1, j
    last = max(range(n), key=dp.__getitem__)
    seq = [a[last]]
    while parent[last] != last:
        last = parent[last]
        seq.append(a[last])
    return seq[::-1]
```

**Complexity:** time **O(n²)**, space **O(n)** — the O(n²) LIS plus an O(LIS) walk.

---

## Edge cases

- Several LIS exist: any is accepted unless a tie rule is specified.
- Single element: `[a[0]]`.

---

## Common mistakes

1. Following parents from `n − 1` instead of from `argmax dp`.
2. Forgetting to reverse.

---

## Follow-ups

1. Reconstruct from the O(n log n) method?
2. All LIS?

<details><summary>Answer sketches</summary>

**#1:** Store `tailIdx[k]` and `prev[i] = tailIdx[k−1]` at insertion; walk back from `tailIdx[len−1]`.

**#2:** DFS over the predecessor DAG of indices with `dp[j] = dp[i] − 1`.
</details>

---

## Flashcards

**LIS reconstruction?** #flashcard
parent[i] = best predecessor; walk from argmax dp; reverse.

**Self-parent marks?** #flashcard
The start of the chain.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
