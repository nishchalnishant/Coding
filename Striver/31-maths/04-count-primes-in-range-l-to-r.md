---
module: striver/31-maths
lesson: 4
topic: Count primes in range L to R
difficulty: Medium
source: https://takeuforward.org/learning/dsa/count-primes-in-range-l-to-r?category=sieve-of-eratosthenes&source=strivers-a2z-dsa-sheet
tags: [striver, maths, math, primes, sieve, prefix-sum]
---
# 4. Count primes in range L to R

← [Prime factorisation of a number](03-prime-factorisation-of-a-number.md) · [Part 31 index](README.md) · Next → [Modular arithmetic and combinatorics](05-modular-arithmetic-and-combinatorics-theory.md)

> [!abstract] Problem at a glance
> **Task:** Answer many queries `[L, R]`: how many primes lie in the inclusive range?
> **Key insight:** Sieve once up to the largest `R`, then build a prefix count `pre[i]` = the number of primes `≤ i`. Each query is `pre[R] − pre[L − 1]` in O(1). This is the prefix-sum pattern on top of a sieve.
> **Difficulty:** Medium · **Pattern:** Sieve + prefix sums · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/count-primes-in-range1604/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-primes-in-range-l-to-r?category=sieve-of-eratosthenes&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Trial division per number](#3-trial-division-per-number) · [4. Sieve + prefix counts](#4-sieve--prefix-counts) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `queries`, a list of pairs `[L, R]` with `1 ≤ L ≤ R`, return for each the count of primes `p` with `L ≤ p ≤ R`.

| Input | Output | Why |
|---|---|---|
| `[[1, 10], [10, 20]]` | `[4, 4]` | 2 3 5 7; 11 13 17 19 |
| `[[2, 2], [14, 16]]` | `[1, 0]` |  |

**Constraints:** `1 ≤ |queries| ≤ 10⁵`; `1 ≤ L ≤ R ≤ 10⁶`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Trial division per number | test each x in [L, R] | O(q·(R − L)·√R) | O(1) |
| Sieve + prefix counts | pre[R] − pre[L − 1] | O(R log log R + q) | O(R) |

> [!tip] Interview angle
> Per query, a sieve on `[L, R]` costs O(R) each. Precomputing once makes every query O(1). Get the `L − 1` index right (`pre[0] = 0`). For `R` up to 10⁹ with a short range, switch to a segmented sieve.

---

## 3. Trial division per number

**Intuition.** For each query, count the `x` in range that pass the `√x` primality test.

```python
def count_trial(queries):
    def is_prime(x):
        if x < 2:
            return False
        d = 2
        while d * d <= x:
            if x % d == 0:
                return False
            d += 1
        return True
    return [sum(is_prime(x) for x in range(l, r + 1)) for l, r in queries]
```

**Complexity:** time **O(q·(R − L)·√R)**, space **O(1)**.

---

## 4. Sieve + prefix counts

**Intuition.** Sieve to `M = max R`. `pre[i] = pre[i − 1] + (prime[i] ? 1 : 0)`. Answer each query in O(1).

**Algorithm**

1. `M = max R` over the queries; sieve `prime[0..M]`.
2. `pre[0] = 0`; `pre[i] = pre[i − 1] + prime[i]`.
3. Answer `pre[R] − pre[L − 1]` for each query.

**Dry run** — pre for 0..20: pre[9] = 4, pre[20] = 8 → [10, 20] gives 8 − 4 = 4.

**C++**
```cpp
vector<int> countPrimes(const vector<vector<int>>& queries) {
    int M = 1;
    for (auto& q : queries) M = max(M, q[1]);
    vector<bool> prime(M + 1, true);
    prime[0] = prime[1] = false;
    for (long long i = 2; i * i <= M; i++)
        if (prime[i])
            for (long long j = i * i; j <= M; j += i) prime[j] = false;
    vector<int> pre(M + 1, 0);
    for (int i = 1; i <= M; i++) pre[i] = pre[i - 1] + prime[i];
    vector<int> res;
    for (auto& q : queries) res.push_back(pre[q[1]] - pre[q[0] - 1]);
    return res;
}
```

**Java**
```java
static int[] countPrimes(int[][] queries) {
    int M = 1;
    for (int[] q : queries) M = Math.max(M, q[1]);
    boolean[] composite = new boolean[M + 1];
    composite[0] = composite[1] = true;
    for (long i = 2; i * i <= M; i++)
        if (!composite[(int) i])
            for (long j = i * i; j <= M; j += i) composite[(int) j] = true;
    int[] pre = new int[M + 1];
    for (int i = 1; i <= M; i++) pre[i] = pre[i - 1] + (composite[i] ? 0 : 1);
    int[] res = new int[queries.length];
    for (int k = 0; k < queries.length; k++) res[k] = pre[queries[k][1]] - pre[queries[k][0] - 1];
    return res;
}
```

**Python**
```python
def count_primes(queries):
    M = max(max(r for _, r in queries), 1)
    prime = [True] * (M + 1)
    prime[0] = prime[1] = False
    i = 2
    while i * i <= M:
        if prime[i]:
            for j in range(i * i, M + 1, i):
                prime[j] = False
        i += 1
    pre = [0] * (M + 1)
    for i in range(1, M + 1):
        pre[i] = pre[i - 1] + prime[i]
    return [pre[r] - pre[l - 1] for l, r in queries]
```

**Complexity:** time **O(R log log R + q)**, space **O(R)** — one sieve and one prefix pass up to max R, then O(1) per query.

---

## Edge cases

- L = 1 (pre[0] = 0).
- Range with no primes ([24, 28]).
- L = R prime.

---

## Common mistakes

1. `pre[R] − pre[L]`, which drops L itself.
2. Sieve size of max L instead of max R.
3. Re-sieving per query.

---

## Follow-ups

1. R up to 10⁹, R − L ≤ 10⁶?
2. Count primes ≤ n only (LC 204, strict <)?

<details><summary>Answer sketches</summary>

**#1:** Segmented sieve on [L, R] using primes ≤ √R.

**#2:** Same sieve; mind that LC 204 counts primes strictly less than n.
</details>

---

## Flashcards

**Range prime count?** #flashcard
pre[R] − pre[L − 1] with pre from a sieve.

**Range [L, R] with huge R?** #flashcard
Segmented sieve: primes to √R, mark multiples from max(p², ⌈L/p⌉·p).

**Interview track →** [Math & number theory](../../02-algorithms/18-math-and-number-theory.md) · [Bit manipulation](../../02-algorithms/17-bit-manipulation.md)
