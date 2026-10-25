---
module: striver-a2z/20-bit-manipulation
lesson: 2
topic: Check if the i-th Bit is Set
difficulty: Easy
source: https://takeuforward.org/learning/dsa/check-if-the-i-th-bit-is-set-or-not?category=bit-fundamentals&source=strivers-a2z-dsa-sheet
tags: [striver, bit-manipulation, bits, masks]
---
# 2. Check if the i-th Bit is Set

← [Bits and Tricks](01-bits-and-tricks.md) · [Part 20 index](README.md) · Next → [Check if a Number is Odd](03-check-if-a-number-is-odd.md)

> [!abstract] Problem at a glance
> **Task:** Return whether bit `k` (0-indexed from the LSB) of `n` is 1.
> **Key insight:** Build a mask with only bit k set (`1 << k`) and AND it with n, or shift n right by k and look at the last bit. Both are O(1).
> **Difficulty:** Easy · **Pattern:** Mask test
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-if-the-i-th-bit-is-set-or-not?category=bit-fundamentals&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Convert to binary string](#3-convert-to-binary-string) · [4. Right shift](#4-right-shift) · [5. Left-shift mask](#5-left-shift-mask) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a non-negative integer `n` and an index `k` (0 = least significant bit), return `true` if the k-th bit of `n` is set, else `false`.

| Input | Output | Why |
|---|---|---|
| `n = 4, k = 2` | `true` | 4 = 100₂ |
| `n = 500, k = 3` | `false` | 500 = 111110100₂ |

**Constraints:** `0 ≤ n ≤ 10⁹`, `0 ≤ k ≤ 30`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Convert to binary string | bin(n), index from the right | O(log n) | O(log n) |
| Right shift | (n >> k) & 1 | O(1) | O(1) |
| Left-shift mask | n & (1 << k) != 0 | O(1) | O(1) |

> [!tip] Interview angle
> Warm-up that checks you know both shift directions and operator precedence. In C/C++/Java `n & 1 << k == 0` parses as `n & ((1 << k) == 0)` — always parenthesise.

---

## 3. Convert to binary string

**Intuition.** Build the binary representation and read character k from the end. Works, but allocates and is what bitwise operators exist to avoid.

```python
def check_str(n, k):
    s = bin(n)[2:]
    return k < len(s) and s[-1 - k] == '1'
```

**Complexity:** time **O(log n)**, space **O(log n)**.

---

## 4. Right shift

**Intuition.** Shifting right by k moves bit k into position 0; `& 1` isolates it.

```python
def check_right(n, k):
    return (n >> k) & 1 == 1
```

**Complexity:** time **O(1)**, space **O(1)**.

---

## 5. Left-shift mask

**Intuition.** `1 << k` has exactly bit k set. AND keeps that bit of n and zeroes everything else, so the result is non-zero iff bit k is set. Compare with `!= 0`, not `== 1` — the result is `2ᵏ`, not 1.

**Dry run** — n = 4 (100), k = 2: mask 100 → 100 & 100 = 4 ≠ 0 → true.

**C++**
```cpp
bool checkKthBit(int n, int k) {
    return (n & (1 << k)) != 0;
}
```

**Java**
```java
static boolean checkKthBit(int n, int k) {
    return (n & (1 << k)) != 0;
}
```

**Python**
```python
def check_kth_bit(n, k):
    return n & (1 << k) != 0
```

**Complexity:** time **O(1)**, space **O(1)** — one shift and one AND.

---

## Edge cases

- k beyond the highest set bit → false.
- n = 0 → always false.
- k = 31 in a signed 32-bit int — `1 << 31` is INT_MIN; use `1u << k` or `1L << k`.

---

## Common mistakes

1. Missing parentheses: `n & 1 << k != 0`.
2. Comparing `n & (1 << k) == 1` — the result is 2ᵏ.
3. `1 << k` with k ≥ 31 on int — undefined/negative; use 64-bit.

---

## Follow-ups

1. Set, clear, toggle bit k.
2. Count bits set in positions [l, r].

<details><summary>Answer sketches</summary>

**#1:** `n | (1 << k)`, `n & ~(1 << k)`, `n ^ (1 << k)`.

**#2:** Mask `((1 << (r − l + 1)) − 1) << l`, AND, popcount.
</details>

---

## Flashcards

**Test bit k (two ways)?** #flashcard
`(n >> k) & 1` or `(n & (1 << k)) != 0`.

**Set / clear / toggle bit k?** #flashcard
`n | 1<<k`, `n & ~(1<<k)`, `n ^ 1<<k`.

**Interview track →** [Bit manipulation deep-dive](../../02-algorithms/17-bit-manipulation.md)
