---
module: striver-a2z/28-dynamic-programming
lesson: 35
topic: Longest bitonic subsequence
difficulty: Medium
source: https://takeuforward.org/learning/dsa/longest-bitonic-subsequence?category=lis-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, lis]
---
# 35. Longest bitonic subsequence

← [Longest string chain](34-longest-string-chain.md) · [Part 28 index](README.md) · Next → [Number of longest increasing subsequences](36-number-of-longest-increasing-subsequences.md)

> [!abstract] Problem at a glance
> **Task:** Longest subsequence that strictly increases, then strictly decreases.
> **Key insight:** `front[i]` = LIS ending at `i` (left to right) and `back[i]` = LIS **starting** at `i` going down (right to left). A bitonic sequence peaking at `i` has length `front[i] + back[i] − 1` (the peak is counted twice).
> **Difficulty:** Medium · **Pattern:** LIS from both ends
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/longest-bitonic-subsequence?category=lis-dp&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Two O(n²) LIS passes](#3-two-on²-lis-passes) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Return the length of the longest subsequence that is first strictly increasing and then strictly decreasing. A purely increasing or purely decreasing sequence counts (one side may be empty).

| Input | Output | Why |
|---|---|---|
| `[1,11,2,10,4,5,2,1]` | `6` | 1,2,10,4,2,1 |
| `[12,11,40,5,3,1]` | `5` | 12,40,5,3,1 |
| `[80,60,30,40,20,10]` | `5` | 80,60,40,20,10 |

**Constraints:** `1 ≤ n ≤ 10³`. Some versions (e.g. GFG) require both sides non-empty; then only peaks with `front > 1 and back > 1` count.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Two O(n²) LIS passes | front[i] + back[i] − 1 | O(n²) | O(n) |

> [!tip] Interview angle
> Clarify whether a monotone sequence counts. The two-pass LIS trick also solves "minimum removals to make a mountain array" (LC 1671) as `n − max bitonic` with both sides required.

---

## 3. Two O(n²) LIS passes

**Intuition.** Compute increasing-ending-at from the left and decreasing-starting-at (LIS from the right) and combine at every peak.

**Algorithm**

1. `front[i] = 1 + max front[j]` for `j < i, a[j] < a[i]`.
2. `back[i] = 1 + max back[j]` for `j > i, a[j] < a[i]`.
3. Return `max(front[i] + back[i] − 1)`.

**Dry run** — [1,11,2,10,4,5,2,1]: front = [1,2,2,3,3,4,2,1], back = [1,5,2,4,3,3,2,1] → peak at 10: 3 + 4 − 1 = 6.

**C++**
```cpp
int longestBitonicSequence(vector<int>& a) {
    int n = a.size(), best = 0;
    vector<int> front(n, 1), back(n, 1);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < i; j++)
            if (a[j] < a[i]) front[i] = max(front[i], front[j] + 1);
    for (int i = n - 1; i >= 0; i--)
        for (int j = n - 1; j > i; j--)
            if (a[j] < a[i]) back[i] = max(back[i], back[j] + 1);
    for (int i = 0; i < n; i++) best = max(best, front[i] + back[i] - 1);
    return best;
}
```

**Java**
```java
static int longestBitonicSequence(int[] a) {
    int n = a.length, best = 0;
    int[] front = new int[n], back = new int[n];
    Arrays.fill(front, 1);
    Arrays.fill(back, 1);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < i; j++)
            if (a[j] < a[i]) front[i] = Math.max(front[i], front[j] + 1);
    for (int i = n - 1; i >= 0; i--)
        for (int j = n - 1; j > i; j--)
            if (a[j] < a[i]) back[i] = Math.max(back[i], back[j] + 1);
    for (int i = 0; i < n; i++) best = Math.max(best, front[i] + back[i] - 1);
    return best;
}
```

**Python**
```python
def longest_bitonic(a):
    n = len(a)
    front, back = [1] * n, [1] * n
    for i in range(n):
        for j in range(i):
            if a[j] < a[i]:
                front[i] = max(front[i], front[j] + 1)
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            if a[j] < a[i]:
                back[i] = max(back[i], back[j] + 1)
    return max(f + b - 1 for f, b in zip(front, back))
```

**Complexity:** time **O(n²)**, space **O(n)** — two quadratic passes and a linear combine (O(n log n) with tails arrays per prefix/suffix).

---

## Edge cases

- Monotone input: n (allowed here).
- Equal neighbours: they can't both be used (strict).

---

## Common mistakes

1. Forgetting the `− 1` (the peak is counted twice).
2. Second pass using `a[j] > a[i]` (that's increasing again).

---

## Follow-ups

1. Both sides required (LC 1671)?
2. Bitonic subarray instead?

<details><summary>Answer sketches</summary>

**#1:** Only combine where `front[i] > 1 and back[i] > 1`.

**#2:** Linear: increasing-run and decreasing-run lengths at each index.
</details>

---

## Flashcards

**Bitonic length at peak i?** #flashcard
`front[i] + back[i] − 1`.

**back[i] means?** #flashcard
LIS of the suffix from i read right to left (strictly decreasing from a[i]).

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
