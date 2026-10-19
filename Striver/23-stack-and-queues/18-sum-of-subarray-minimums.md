---
module: striver/23-stack-and-queues
lesson: 18
topic: Sum of Subarray Minimums
difficulty: Medium
source: https://takeuforward.org/learning/dsa/sum-of-subarray-minimums?category=monotonic-stack&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, monotonic-stack, contribution, math]
---
# 18. Sum of Subarray Minimums

← [Asteroid Collision](17-asteroid-collision.md) · [Part 23 index](README.md) · Next → [Sum of Subarray Ranges](19-sum-of-subarray-ranges.md)

> [!abstract] Problem at a glance
> **Task:** Sum of `min(subarray)` over all contiguous subarrays, mod 1e9+7.
> **Key insight:** Flip it around: count how many subarrays have `arr[i]` as their minimum. If `L` = distance to the previous **smaller** element and `R` = distance to the next **smaller-or-equal** element, then `arr[i]` is the min of exactly `L·R` subarrays. Answer = `Σ arr[i]·L·R`. Using strict on one side and non-strict on the other counts ties exactly once.
> **Difficulty:** Medium · **Pattern:** Contribution technique + PSE/NSE · **Also on:** [LC 907](https://leetcode.com/problems/sum-of-subarray-minimums/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/sum-of-subarray-minimums?category=monotonic-stack&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Running minimum](#3-running-minimum) · [4. Contribution with previous/next smaller](#4-contribution-with-previousnext-smaller) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `arr`, return the sum of `min(b)` over every contiguous subarray `b`, modulo `10⁹+7`.

| Input | Output | Why |
|---|---|---|
| `arr = [3,1,2,4]` | `17` | mins: 3,1,2,4,1,1,2,1,1,1 → 17 |
| `arr = [11,81,94,43,3]` | `444` |  |

**Constraints:** `1 ≤ n ≤ 3·10⁴`; `1 ≤ arr[i] ≤ 3·10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Running minimum | fix i, extend j, track min | O(n²) | O(1) |
| Contribution with previous/next smaller | arr[i]·(i − pse)·(nse − i) | O(n) | O(n) |

> [!tip] Interview angle
> This is the key 'contribution' problem. Interviewers probe the tie-break: with `[2,2]`, if both sides use strict `<`, the subarray `[2,2]` is counted twice. Explain why one side must be `≤`.

---

## 3. Running minimum

**Intuition.** For each start `i`, extend `j` and keep the running minimum; add it each step.

```python
def sum_sub_mins_brute(arr):
    MOD = 10**9 + 7
    total = 0
    for i in range(len(arr)):
        m = arr[i]
        for j in range(i, len(arr)):
            m = min(m, arr[j])
            total += m
    return total % MOD
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Contribution with previous/next smaller

**Intuition.** Subarray `[l, r]` has minimum `arr[i]` (taking the leftmost minimum on ties) iff `l` is in `(pse, i]` and `r` is in `[i, nse)`. Here `pse` is the last index left of `i` with value `≤ arr[i]` and `nse` is the first index right of `i` with value `< arr[i]`. Either assignment of strictness works, as long as the two sides differ. Two monotonic-stack passes give `pse` and `nse`.

**Algorithm**

1. `nse[i]`: right-to-left; pop while `arr[top] ≥ arr[i]`; `nse[i] = top` or `n`; push `i`.
2. `pse[i]`: left-to-right; pop while `arr[top] > arr[i]`; `pse[i] = top` or `−1`; push `i`.
3. Answer `= Σ arr[i]·(i − pse[i])·(nse[i] − i)` mod 1e9+7.

**Dry run** — [3,1,2,4]: i0: pse −1, nse 1 → 3·1·1=3. i1: pse −1, nse 4 → 1·2·3=6. i2: pse 1, nse 4 → 2·1·2=4. i3: pse 2, nse 4 → 4·1·1=4. Total 17.

**C++**
```cpp
int sumSubarrayMins(vector<int> arr) {
    const long long MOD = 1e9 + 7;
    int n = arr.size();
    vector<int> pse(n), nse(n), st;
    for (int i = n - 1; i >= 0; i--) {
        while (!st.empty() && arr[st.back()] >= arr[i]) st.pop_back();
        nse[i] = st.empty() ? n : st.back();
        st.push_back(i);
    }
    st.clear();
    for (int i = 0; i < n; i++) {
        while (!st.empty() && arr[st.back()] > arr[i]) st.pop_back();
        pse[i] = st.empty() ? -1 : st.back();
        st.push_back(i);
    }
    long long total = 0;
    for (int i = 0; i < n; i++)
        total = (total + (long long)arr[i] * (i - pse[i]) % MOD * (nse[i] - i)) % MOD;
    return (int)total;
}
```

**Java**
```java
static int sumSubarrayMins(int[] arr) {
    final long MOD = 1_000_000_007L;
    int n = arr.length;
    int[] pse = new int[n], nse = new int[n];
    Deque<Integer> st = new ArrayDeque<>();
    for (int i = n - 1; i >= 0; i--) {
        while (!st.isEmpty() && arr[st.peek()] >= arr[i]) st.pop();
        nse[i] = st.isEmpty() ? n : st.peek();
        st.push(i);
    }
    st.clear();
    for (int i = 0; i < n; i++) {
        while (!st.isEmpty() && arr[st.peek()] > arr[i]) st.pop();
        pse[i] = st.isEmpty() ? -1 : st.peek();
        st.push(i);
    }
    long total = 0;
    for (int i = 0; i < n; i++)
        total = (total + (long) arr[i] * (i - pse[i]) % MOD * (nse[i] - i)) % MOD;
    return (int) total;
}
```

**Python**
```python
def sum_subarray_mins(arr):
    MOD = 10**9 + 7
    n = len(arr)
    nse, pse, st = [n] * n, [-1] * n, []
    for i in range(n - 1, -1, -1):
        while st and arr[st[-1]] >= arr[i]:
            st.pop()
        if st:
            nse[i] = st[-1]
        st.append(i)
    st = []
    for i in range(n):
        while st and arr[st[-1]] > arr[i]:
            st.pop()
        if st:
            pse[i] = st[-1]
        st.append(i)
    return sum(arr[i] * (i - pse[i]) * (nse[i] - i) for i in range(n)) % MOD
```

**Complexity:** time **O(n)**, space **O(n)** — two O(n) stack passes plus one O(n) sum.

---

## Edge cases

- Duplicates: the strict/non-strict split prevents double counting.
- Strictly increasing or decreasing arrays.
- Overflow: `arr[i]·L·R` can reach ~3·10⁴ · 3·10⁴ · 3·10⁴; use 64-bit and mod.

---

## Common mistakes

1. Strict comparison on both sides, which double-counts subarrays with repeated minimums.
2. Non-strict on both sides, which misses them.
3. Multiplying in 32-bit before taking the mod.

---

## Follow-ups

1. One-pass version?
2. Sum of subarray maximums?
3. Sum of ranges?

<details><summary>Answer sketches</summary>

**#1:** DP: `dp[i] = dp[pse[i]] + arr[i]·(i − pse[i])` is the sum of mins of subarrays ending at i; answer = Σ dp[i].

**#2:** Same with previous/next greater.

**#3:** Σ max − Σ min (next problem).
</details>

---

## Flashcards

**Contribution of arr[i] to the sum of subarray minimums?** #flashcard
arr[i] · (i − PSE) · (NSE − i).

**How do you avoid double-counting equal minimums?** #flashcard
Strict on one side, non-strict (≤ / ≥) on the other.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
