---
module: striver/20-bit-manipulation
lesson: 8
topic: Minimum Bit Flips to Convert Number
difficulty: Easy
source: https://takeuforward.org/learning/dsa/minimum-bit-flips-to-convert-number?category=problems&source=strivers-a2z-dsa-sheet
tags: [striver, bit-manipulation, bits, xor]
---
# 8. Minimum Bit Flips to Convert Number

← [Swap Two Numbers](07-swap-two-numbers.md) · [Part 20 index](README.md) · Next → [Single Number I](09-single-number-i.md)

> [!abstract] Problem at a glance
> **Task:** Count the bit positions where `start` and `goal` differ.
> **Key insight:** XOR marks exactly the positions that differ; each one needs one flip. Answer = popcount(start ^ goal).
> **Difficulty:** Easy · **Pattern:** XOR + popcount · **Also on:** [LC 2220](https://leetcode.com/problems/minimum-bit-flips-to-convert-number/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimum-bit-flips-to-convert-number?category=problems&source=strivers-a2z-dsa-sheet) · **Time:** 8 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Compare bit by bit](#3-compare-bit-by-bit) · [4. XOR + Kernighan](#4-xor--kernighan) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A bit flip changes one bit of a number from 0 to 1 or 1 to 0. Given `start` and `goal`, return the minimum number of flips to convert `start` into `goal`.

| Input | Output | Why |
|---|---|---|
| `start = 10, goal = 7` | `3` | 1010 vs 0111 → 1101 |
| `start = 3, goal = 4` | `3` | 011 vs 100 |

**Constraints:** `0 ≤ start, goal ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Compare bit by bit | check each of 31 positions | O(log max) | O(1) |
| XOR + Kernighan | popcount(start ^ goal) | O(popcount) | O(1) |

> [!tip] Interview angle
> Same as Hamming distance (LC 461). Say "XOR gives the diff mask, popcount counts it" and you're done in two lines.

---

## 3. Compare bit by bit

**Intuition.** For every bit i, compare `(start >> i) & 1` with `(goal >> i) & 1`.

```python
def flips_scan(start, goal):
    c = 0
    while start or goal:
        c += (start & 1) != (goal & 1)
        start >>= 1
        goal >>= 1
    return c
```

**Complexity:** time **O(log max)**, space **O(1)**.

---

## 4. XOR + Kernighan

**Intuition.** `start ^ goal` has a 1 exactly where the bits differ. Each must be flipped once and flips are independent, so the minimum is the number of 1s.

**Dry run** — 10 ^ 7 = 1010 ^ 0111 = 1101 → 3 set bits.

**C++**
```cpp
int minBitFlips(int start, int goal) {
    int x = start ^ goal, c = 0;
    while (x) {
        x &= x - 1;
        c++;
    }
    return c;
}
```

**Java**
```java
static int minBitFlips(int start, int goal) {
    int x = start ^ goal, c = 0;
    while (x != 0) {
        x &= x - 1;
        c++;
    }
    return c;
}
```

**Python**
```python
def min_bit_flips(start, goal):
    x, c = start ^ goal, 0
    while x:
        x &= x - 1
        c += 1
    return c
```

**Complexity:** time **O(popcount)**, space **O(1)** — one iteration per differing bit.

---

## Edge cases

- start == goal → 0.
- One of them is 0 → popcount of the other.

---

## Common mistakes

1. Stopping the scan loop when only one number reaches 0.

---

## Follow-ups

1. Total Hamming distance over all pairs (LC 477).
2. Min flips so that a OR b == c (LC 1318).

<details><summary>Answer sketches</summary>

**#1:** For each bit, if c numbers have it set, it contributes c·(n − c). O(32n).

**#2:** Per bit: if c-bit is 1 need ≥ one of a, b set (1 flip if neither); if 0, flip every set bit among a, b.
</details>

---

## Flashcards

**Min bit flips start → goal?** #flashcard
popcount(start ^ goal).

**Sum of pairwise Hamming distances?** #flashcard
Σ over bits of c·(n − c).

**Interview track →** [Bit manipulation deep-dive](../../02-algorithms/17-bit-manipulation.md)
