---
module: striver-a2z/20-bit-manipulation
lesson: 14
topic: XOR of Numbers in a Given Range
difficulty: Medium
source: https://takeuforward.org/learning/dsa/xor-of-numbers-in-a-given-range?category=problems&source=strivers-a2z-dsa-sheet
tags: [striver, bit-manipulation, bits, xor, prefix]
---
# 14. XOR of Numbers in a Given Range

← [Power Set (Bit Manipulation)](13-power-set.md) · [Part 20 index](README.md) · Next → [Part 21: Greedy Algorithms](../21-greedy-algorithms/README.md)

> [!abstract] Problem at a glance
> **Task:** Return `L ^ (L+1) ^ … ^ R` in O(1).
> **Key insight:** Prefix XOR f(n) = 0 ^ 1 ^ … ^ n follows a period-4 pattern: n, 1, n + 1, 0 for n mod 4 = 0, 1, 2, 3. Then XOR(L…R) = f(R) ^ f(L − 1), just like prefix sums.
> **Difficulty:** Medium · **Pattern:** Prefix XOR with period 4
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/xor-of-numbers-in-a-given-range?category=problems&source=strivers-a2z-dsa-sheet) · **Time:** 12 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Loop](#3-loop) · [4. Prefix XOR f(R) ^ f(L − 1)](#4-prefix-xor-fr--fl--1) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given two integers `L ≤ R`, return the XOR of all integers from `L` to `R` inclusive.

| Input | Output | Why |
|---|---|---|
| `L = 3, R = 5` | `2` | 3 ^ 4 ^ 5 |
| `L = 1, R = 3` | `0` | 1 ^ 2 ^ 3 |
| `L = 4, R = 8` | `8` |  |

**Constraints:** `1 ≤ L ≤ R ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Loop | XOR every number L…R | O(R − L) | O(1) |
| Prefix XOR f(R) ^ f(L − 1) | f(n) by n mod 4 | O(1) | O(1) |

> [!tip] Interview angle
> Derive the pattern rather than reciting it: every block `4k, 4k+1, 4k+2, 4k+3` XORs to 0 (high bits cancel in pairs, low bits 00^01^10^11 = 0). So only the partial last block matters.

---

## 3. Loop

**Intuition.** Direct; up to 10⁹ iterations.

```python
def xor_range_loop(L, R):
    x = 0
    for v in range(L, R + 1):
        x ^= v
    return x
```

**Complexity:** time **O(R − L)**, space **O(1)**.

---

## 4. Prefix XOR f(R) ^ f(L − 1)

**Intuition.** `f(n) = 0 ^ 1 ^ … ^ n`. Since `4k ^ (4k+1) ^ (4k+2) ^ (4k+3) = 0`, only the tail after the last multiple of 4 survives: n mod 4 = 0 → n; 1 → n ^ (n−1) = 1; 2 → 1 ^ n = n + 1 (n even); 3 → (n + 1) ^ n = 0. Range XOR cancels the common prefix: `f(R) ^ f(L − 1)`.

**Dry run** — L = 3, R = 5: f(5) = 1 (5 mod 4 = 1), f(2) = 3 (2 mod 4 = 2 → 3) → 1 ^ 3 = 2.

**C++**
```cpp
int prefXor(int n) {
    switch (n % 4) {
        case 0: return n;
        case 1: return 1;
        case 2: return n + 1;
        default: return 0;
    }
}
int xorRange(int L, int R) {
    return prefXor(R) ^ prefXor(L - 1);
}
```

**Java**
```java
static int prefXor(int n) {
    switch (n % 4) {
        case 0: return n;
        case 1: return 1;
        case 2: return n + 1;
        default: return 0;
    }
}
static int xorRange(int L, int R) {
    return prefXor(R) ^ prefXor(L - 1);
}
```

**Python**
```python
def xor_range(L, R):
    def f(n):
        return [n, 1, n + 1, 0][n % 4]
    return f(R) ^ f(L - 1)
```

**Complexity:** time **O(1)**, space **O(1)** — two table lookups.

---

## Edge cases

- L = R → L.
- L = 1 → f(0) = 0.
- Large R — O(1) avoids the loop.

---

## Common mistakes

1. Using `f(R) ^ f(L)` (drops L).
2. Mixing up the cases 1 and 2 of the pattern.

---

## Follow-ups

1. XOR queries on an arbitrary array (LC 1310).
2. Count subarrays with XOR = k.

<details><summary>Answer sketches</summary>

**#1:** Prefix XOR array `px[i+1] = px[i] ^ a[i]`; query = `px[r+1] ^ px[l]`.

**#2:** Prefix XOR + hash map of counts — the XOR analogue of subarray sum = k.
</details>

---

## Flashcards

**f(n) = 0^1^…^n by n mod 4?** #flashcard
0 → n, 1 → 1, 2 → n + 1, 3 → 0.

**XOR of L…R?** #flashcard
f(R) ^ f(L − 1).

**Why period 4?** #flashcard
4k ^ (4k+1) ^ (4k+2) ^ (4k+3) = 0.

**Interview track →** [Bit manipulation deep-dive](../../02-algorithms/17-bit-manipulation.md)
