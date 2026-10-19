---
module: striver/20-bit-manipulation
lesson: 11
topic: Single Number III
difficulty: Medium
source: https://takeuforward.org/learning/dsa/single-number---iii?category=problems&source=strivers-a2z-dsa-sheet
tags: [striver, bit-manipulation, bits, xor]
---
# 11. Single Number III

← [Single Number II](10-single-number-ii.md) · [Part 20 index](README.md) · Next → [Divide Two Integers](12-divide-two-integers.md)

> [!abstract] Problem at a glance
> **Task:** Every element appears twice except two; find both in O(n) time, O(1) space.
> **Key insight:** XOR of all = a ^ b ≠ 0, so a and b differ in at least one bit. Pick the lowest set bit of `a ^ b`, split the array by that bit — a and b land in different groups and every pair lands together — then XOR each group.
> **Difficulty:** Medium · **Pattern:** XOR + partition by lowest differing bit · **Also on:** [LC 260](https://leetcode.com/problems/single-number-iii/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/single-number---iii?category=problems&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Hash map count](#3-hash-map-count) · [4. XOR + split on lowest differing bit](#4-xor--split-on-lowest-differing-bit) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums` in which exactly two elements appear only once and all others appear exactly twice, return the two elements in ascending order.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 1, 3, 2, 5]` | `[3, 5]` |  |
| `nums = [-1, 0]` | `[-1, 0]` |  |

**Constraints:** `2 ≤ n ≤ 3·10⁴`, `−2³¹ ≤ nums[i] ≤ 2³¹ − 1`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Hash map count | collect keys with count 1 | O(n) | O(n) |
| XOR + split on lowest differing bit | x = a ^ b; low = x & −x; XOR each half | O(n) | O(1) |

> [!tip] Interview angle
> The hard part is justifying the split. Say: "`a ^ b` has a 1 where a and b differ; pick any such bit. Duplicates share every bit so each pair goes to the same side." Then mention `x & −x` overflows for INT_MIN in C++/Java signed ints.

---

## 3. Hash map count

**Intuition.** Baseline.

```python
def single3_map(nums):
    from collections import Counter
    return sorted(x for x, c in Counter(nums).items() if c == 1)
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. XOR + split on lowest differing bit

**Intuition.** Pass 1: `x = XOR(nums) = a ^ b`. `low = x & −x` isolates one bit where a and b differ. Pass 2: XOR numbers with that bit set into `a`, the rest into `b`. Pairs cancel within their group, leaving one single per group.

**Algorithm**

1. `x = XOR of all`.
2. `low = x & −x` (use unsigned / long to avoid INT_MIN overflow).
3. For each v: if `v & low` → `a ^= v` else `b ^= v`.
4. Return `[min(a, b), max(a, b)]`.

**Dry run** — [1 2 1 3 2 5]: x = 3 ^ 5 = 6 (110), low = 010. Bit-1 group: 2, 3, 2 → 3. Other: 1, 1, 5 → 5. → [3, 5].

**C++**
```cpp
vector<int> singleNumber(vector<int>& nums) {
    unsigned x = 0;
    for (int v : nums) x ^= (unsigned)v;
    unsigned low = x & (~x + 1);
    int a = 0, b = 0;
    for (int v : nums) {
        if ((unsigned)v & low) a ^= v;
        else b ^= v;
    }
    return {min(a, b), max(a, b)};
}
```

**Java**
```java
static int[] singleNumber(int[] nums) {
    int x = 0;
    for (int v : nums) x ^= v;
    int low = x & -x;          // Java int wraps, so INT_MIN & -INT_MIN = INT_MIN is fine
    int a = 0, b = 0;
    for (int v : nums) {
        if ((v & low) != 0) a ^= v;
        else b ^= v;
    }
    return new int[]{Math.min(a, b), Math.max(a, b)};
}
```

**Python**
```python
def single_number3(nums):
    x = 0
    for v in nums:
        x ^= v
    low = x & -x
    a = b = 0
    for v in nums:
        if v & low:
            a ^= v
        else:
            b ^= v
    return [min(a, b), max(a, b)]
```

**Complexity:** time **O(n)**, space **O(1)** — two passes.

---

## Edge cases

- One single is 0.
- Lowest differing bit is the sign bit (INT_MIN) — `x & −x` overflows for signed int in C++.
- Negative numbers.

---

## Common mistakes

1. `-x` on INT_MIN in C++ signed int — undefined behaviour; use unsigned.
2. Comparing `(v & low) == 1` — low may be a higher bit.
3. Returning unsorted when the judge expects order.

---

## Follow-ups

1. Three singles, rest pairs.
2. Missing and repeating number in 1…n.

<details><summary>Answer sketches</summary>

**#1:** No clean O(1)-space split; use a hash set, or bit tricks with multiple partitions (much harder).

**#2:** Same split trick on XOR of values and 1…n — then check which one is in the array.
</details>

---

## Flashcards

**Single Number III idea?** #flashcard
XOR all = a ^ b; split by its lowest set bit; XOR each group.

**Isolate lowest set bit?** #flashcard
`x & −x` (use unsigned in C++ to dodge INT_MIN UB).

**Why do duplicates stay in the same group?** #flashcard
Equal numbers have identical bits, including the split bit.

**Interview track →** [Bit manipulation deep-dive](../../02-algorithms/17-bit-manipulation.md)
