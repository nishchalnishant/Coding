---
module: striver/20-bit-manipulation
lesson: 10
topic: Single Number II
difficulty: Medium
source: https://takeuforward.org/learning/dsa/single-number---ii?category=problems&source=strivers-a2z-dsa-sheet
tags: [striver, bit-manipulation, bits, counting]
---
# 10. Single Number II

← [Single Number I](09-single-number-i.md) · [Part 20 index](README.md) · Next → [Single Number III](11-single-number-iii.md)

> [!abstract] Problem at a glance
> **Task:** Every element appears three times except one; find it in O(n) time, O(1) space.
> **Key insight:** XOR no longer cancels triples. Count each bit position across all numbers: a bit belongs to the single number iff its count isn't a multiple of 3. The `ones`/`twos` state machine does that count mod 3 for all 32 bits at once.
> **Difficulty:** Medium · **Pattern:** Per-bit count mod 3 · **Also on:** [LC 137](https://leetcode.com/problems/single-number-ii/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/single-number---ii?category=problems&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Hash map count](#3-hash-map-count) · [4. Sort and step by 3](#4-sort-and-step-by-3) · [5. Count each bit mod 3](#5-count-each-bit-mod-3) · [6. ones / twos state machine](#6-ones--twos-state-machine) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums` where every element appears **three times** except for one, which appears exactly once, find the single element. Use linear runtime and constant extra space.

| Input | Output | Why |
|---|---|---|
| `nums = [2, 2, 3, 2]` | `3` |  |
| `nums = [0, 1, 0, 1, 0, 1, 99]` | `99` |  |

**Constraints:** `1 ≤ n ≤ 3·10⁴`, `−2³¹ ≤ nums[i] ≤ 2³¹ − 1`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Hash map count | return the key with count 1 | O(n) | O(n) |
| Sort and step by 3 | nums[i] != nums[i+1] → single | O(n log n) | O(1) |
| Count each bit mod 3 | for 32 bits, set bit b if count % 3 == 1 | O(32n) | O(1) |
| ones / twos state machine | ones = (ones ^ x) & ~twos; twos = (twos ^ x) & ~ones | O(n) | O(1) |

> [!tip] Interview angle
> Expect to explain the bit-count approach first — it generalises to "appears k times". The `ones`/`twos` version is the follow-up; derive it as a two-bit counter per bit position rather than reciting it.

---

## 3. Hash map count

**Intuition.** Baseline; uses extra space.

```python
def single2_map(nums):
    from collections import Counter
    return next(x for x, c in Counter(nums).items() if c == 1)
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Sort and step by 3

**Intuition.** After sorting, triples sit together; check index 1, 4, 7, … against the one before it.

```python
def single2_sort(nums):
    nums = sorted(nums)
    for i in range(1, len(nums), 3):
        if nums[i] != nums[i - 1]:
            return nums[i - 1]
    return nums[-1]
```

**Complexity:** time **O(n log n)**, space **O(1)**.

---

## 5. Count each bit mod 3

**Intuition.** Every tripled number contributes 0 or 3 to each bit's count. So `count_b mod 3` is exactly the single number's bit b. In Python, convert from 32-bit two's complement at the end to get negatives right.

```python
def single2_bits(nums):
    ans = 0
    for b in range(32):
        cnt = sum((x >> b) & 1 for x in nums)
        if cnt % 3:
            ans |= 1 << b
    return ans - (1 << 32) if ans >= 1 << 31 else ans
```

**Complexity:** time **O(32n)**, space **O(1)**.

---

## 6. ones / twos state machine

**Intuition.** Per bit, track count mod 3 as two bits: (twos, ones) ∈ {00, 01, 10}. Seeing a 1 moves 00 → 01 → 10 → 00. The two update lines implement that transition for all 32 positions in parallel. After processing everything, tripled bits are back at 00, so `ones` holds the single number.

**Algorithm**

1. `ones = twos = 0`.
2. For each x: `ones = (ones ^ x) & ~twos` — add x to ones unless that bit is already in twos.
3. `twos = (twos ^ x) & ~ones` — add x to twos unless it just went to ones.
4. Return `ones`.

**Dry run** — Per-bit view of [2 2 3 2] = 10, 10, 11, 10: bit 1 is seen 4 times → 4 mod 3 = 1; bit 0 is seen once → 1. Answer 11₂ = 3. The state machine reaches the same: after the three 2s, bit 1 cycles 01 → 10 → 00 (with the 3 in between contributing one extra), ending with ones = 11.

**C++**
```cpp
int singleNumber(vector<int>& nums) {
    int ones = 0, twos = 0;
    for (int x : nums) {
        ones = (ones ^ x) & ~twos;
        twos = (twos ^ x) & ~ones;
    }
    return ones;
}
```

**Java**
```java
static int singleNumber(int[] nums) {
    int ones = 0, twos = 0;
    for (int x : nums) {
        ones = (ones ^ x) & ~twos;
        twos = (twos ^ x) & ~ones;
    }
    return ones;
}
```

**Python**
```python
def single_number2(nums):
    ones = twos = 0
    for x in nums:
        ones = (ones ^ x) & ~twos
        twos = (twos ^ x) & ~ones
    return ones
```

**Complexity:** time **O(n)**, space **O(1)** — two bitwise updates per element.

---

## Edge cases

- Negative single number — the bit-count version must handle bit 31 (sign).
- n = 1.

---

## Common mistakes

1. Using XOR alone — triples don't cancel.
2. Python bit-count without the 32-bit sign fix → returns 4294967292 instead of −4.
3. Swapping the order of the ones/twos updates.

---

## Follow-ups

1. Every element appears k times except one (appears once).
2. Single appears p times (p not multiple of k).

<details><summary>Answer sketches</summary>

**#1:** Bit count mod k — O(32n). The state machine needs ⌈log₂ k⌉ counter bits.

**#2:** Bit b of the answer is set iff count_b mod k ≠ 0.
</details>

---

## Flashcards

**Single Number II: core idea?** #flashcard
Each bit's total count mod 3 equals the single number's bit.

**ones/twos update lines?** #flashcard
`ones = (ones ^ x) & ~twos; twos = (twos ^ x) & ~ones`; return ones.

**Python pitfall for the bit-count version?** #flashcard
Convert from 32-bit two's complement: subtract 2³² if ≥ 2³¹.

**Interview track →** [Bit manipulation deep-dive](../../02-algorithms/17-bit-manipulation.md)
