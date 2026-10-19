---
module: striver/20-bit-manipulation
lesson: 6
topic: Set the Rightmost Unset Bit
difficulty: Easy
source: https://takeuforward.org/learning/dsa/set-the-rightmost-unset-bit?category=bit-fundamentals&source=strivers-a2z-dsa-sheet
tags: [striver, bit-manipulation, bits]
---
# 6. Set the Rightmost Unset Bit

← [Count the Number of Set Bits](05-count-the-number-of-set-bits.md) · [Part 20 index](README.md) · Next → [Swap Two Numbers](07-swap-two-numbers.md)

> [!abstract] Problem at a glance
> **Task:** Turn the lowest 0 bit of `n` into 1.
> **Key insight:** `n + 1` flips the trailing 1s to 0 and the lowest 0 to 1. ORing with n restores the trailing 1s, leaving exactly the lowest 0 set: `n | (n + 1)`.
> **Difficulty:** Easy · **Pattern:** n | (n + 1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/set-the-rightmost-unset-bit?category=bit-fundamentals&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Scan bits](#3-scan-bits) · [4. n | (n + 1)](#4-n--n--1) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a non-negative integer `n`, set the rightmost (least significant) unset bit of its binary representation and return the result.

| Input | Output | Why |
|---|---|---|
| `n = 10` | `11` | 1010 → 1011 |
| `n = 7` | `15` | 0111 → 1111 |
| `n = 6` | `7` | 110 → 111 |

**Constraints:** `0 ≤ n < 2³⁰`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Scan bits | find the first k with bit k = 0 | O(log n) | O(1) |
| n | (n + 1) | +1 carries through trailing 1s into the lowest 0 | O(1) | O(1) |

> [!tip] Interview angle
> Part of a family of one-liners — know all four: clear lowest set `n & (n−1)`, isolate lowest set `n & −n`, set lowest unset `n | (n+1)`, isolate lowest unset `~n & (n+1)`.

---

## 3. Scan bits

**Intuition.** Walk k = 0, 1, 2, … until bit k is 0, then OR in `1 << k`.

```python
def set_scan(n):
    k = 0
    while n >> k & 1:
        k += 1
    return n | (1 << k)
```

**Complexity:** time **O(log n)**, space **O(1)**.

---

## 4. n | (n + 1)

**Intuition.** Write n = `…0 111` (lowest 0 followed by t ones). Then n + 1 = `…1 000`. OR = `…1 111`: the lowest 0 became 1 and nothing else changed.

**Dry run** — 10 = 1010, 11 = 1011 → 1010 | 1011 = 1011 = 11.

**C++**
```cpp
int setRightmostUnsetBit(int n) {
    return n | (n + 1);
}
```

**Java**
```java
static int setRightmostUnsetBit(int n) {
    return n | (n + 1);
}
```

**Python**
```python
def set_rightmost_unset_bit(n):
    return n | (n + 1)
```

**Complexity:** time **O(1)**, space **O(1)** — two operations.

---

## Edge cases

- n = 0 → 1.
- n = 2ᵏ − 1 (all ones) → sets bit k. GFG's variant instead returns n unchanged when all bits *within n's length* are set — check which one the judge wants.

---

## Common mistakes

1. Confusing it with `n & (n − 1)` (which clears the lowest set bit).
2. Overflow when n = INT_MAX.

---

## Follow-ups

1. Return n unchanged if all bits up to its MSB are set.
2. Clear the rightmost set bit.
3. Turn off trailing 1s.

<details><summary>Answer sketches</summary>

**#1:** If `(n & (n + 1)) == 0` (n is 2ᵏ − 1) return n, else `n | (n + 1)`.

**#2:** `n & (n − 1)`.

**#3:** `n & (n + 1)`.
</details>

---

## Flashcards

**Set lowest unset bit?** #flashcard
`n | (n + 1)`.

**Isolate lowest unset bit?** #flashcard
`~n & (n + 1)`.

**Clear trailing ones?** #flashcard
`n & (n + 1)`.

**Interview track →** [Bit manipulation deep-dive](../../02-algorithms/17-bit-manipulation.md)
