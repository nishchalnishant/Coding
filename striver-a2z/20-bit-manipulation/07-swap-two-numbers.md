---
module: striver-a2z/20-bit-manipulation
lesson: 7
topic: Swap Two Numbers
difficulty: Easy
source: https://takeuforward.org/learning/dsa/swap-two-numbers?category=bit-fundamentals&source=strivers-a2z-dsa-sheet
tags: [striver, bit-manipulation, bits, xor]
---
# 7. Swap Two Numbers

← [Set the Rightmost Unset Bit](06-set-the-rightmost-unset-bit.md) · [Part 20 index](README.md) · Next → [Minimum Bit Flips to Convert Number](08-minimum-bit-flips-to-convert-number.md)

> [!abstract] Problem at a glance
> **Task:** Swap `a` and `b` without a temporary variable.
> **Key insight:** XOR is its own inverse: `a ^= b; b ^= a; a ^= b` — after step 2, `b = b ^ (a ^ b) = a`; after step 3, `a = (a ^ b) ^ a = b`.
> **Difficulty:** Easy · **Pattern:** XOR self-inverse
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/swap-two-numbers?category=bit-fundamentals&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Arithmetic](#3-arithmetic) · [4. XOR swap](#4-xor-swap) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given two integers `a` and `b`, swap them without using a third variable and return `[a, b]` after swapping.

| Input | Output | Why |
|---|---|---|
| `a = 5, b = 10` | `[10, 5]` |  |
| `a = -3, b = 7` | `[7, -3]` |  |

**Constraints:** `−10⁹ ≤ a, b ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Arithmetic | a = a + b; b = a − b; a = a − b | O(1) | O(1) |
| XOR swap | a ^= b; b ^= a; a ^= b | O(1) | O(1) |

> [!tip] Interview angle
> Show you know the XOR identities, then say you wouldn't use this in production: `std::swap` / tuple assignment is clearer, and XOR swap **zeroes the value if both references alias the same memory**.

---

## 3. Arithmetic

**Intuition.** Works mathematically, but `a + b` can overflow in fixed-width ints (well-defined wraparound for unsigned only).

```python
def swap_arith(a, b):
    a = a + b
    b = a - b
    a = a - b
    return [a, b]
```

**Complexity:** time **O(1)**, space **O(1)**.

---

## 4. XOR swap

**Intuition.** XOR facts: `x ^ x = 0`, `x ^ 0 = x`, commutative and associative. Step 1 stores `a ^ b` in a. Step 2: `b ^ (a ^ b) = a`. Step 3: `(a ^ b) ^ a = b`. No overflow possible.

**Dry run** — a = 5 (101), b = 10 (1010): a = 1111; b = 1111 ^ 1010 = 0101 = 5; a = 1111 ^ 0101 = 1010 = 10.

**C++**
```cpp
vector<int> swapNumbers(int a, int b) {
    a ^= b;
    b ^= a;
    a ^= b;
    return {a, b};
}
```

**Java**
```java
static int[] swapNumbers(int a, int b) {
    a ^= b;
    b ^= a;
    a ^= b;
    return new int[]{a, b};
}
```

**Python**
```python
def swap_numbers(a, b):
    a ^= b
    b ^= a
    a ^= b
    return [a, b]
```

**Complexity:** time **O(1)**, space **O(1)** — three XORs.

---

## Edge cases

- a == b (as values) — fine.
- Same variable passed by reference twice (`swap(x, x)`) — XOR version sets it to 0.

---

## Common mistakes

1. `a ^= b ^= a ^= b` in one expression — unsequenced modification, undefined behaviour in C/C++.
2. Arithmetic version overflow.

---

## Follow-ups

1. Why isn't XOR swap faster on modern CPUs?

<details><summary>Answer sketches</summary>

**#1:** The three XORs are serially dependent; a temp-variable swap is just register renaming. Compilers emit the temp version for `std::swap`.
</details>

---

## Flashcards

**XOR swap steps?** #flashcard
`a ^= b; b ^= a; a ^= b`.

**When does XOR swap fail?** #flashcard
When both operands are the same memory location — result becomes 0.

**Three XOR identities?** #flashcard
`x ^ x = 0`, `x ^ 0 = x`, commutative + associative.

**Interview track →** [Bit manipulation deep-dive](../../02-algorithms/17-bit-manipulation.md)
