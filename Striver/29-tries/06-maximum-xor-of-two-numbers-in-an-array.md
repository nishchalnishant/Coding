---
module: striver/29-tries
lesson: 6
topic: Maximum XOR of two numbers in an array
difficulty: Medium
source: https://takeuforward.org/learning/dsa/maximum-xor-of-two-numbers-in-an-array?category=problems&source=strivers-a2z-dsa-sheet
tags: [striver, tries, trie, bit-manipulation, greedy]
---
# 6. Maximum XOR of two numbers in an array

← [Number of distinct substrings in a string](05-number-of-distinct-substrings-in-a-string.md) · [Part 29 index](README.md) · Next → [Maximum XOR with an element from the array](07-maximum-xor-with-an-element-from-the-array.md)

> [!abstract] Problem at a glance
> **Task:** Max of `a[i] XOR a[j]` over all pairs.
> **Key insight:** XOR is maximised greedily from the **most significant bit**: a 1 at bit 30 beats anything in the lower bits. Insert every number's 31 bits into a binary trie (MSB first). For each `x`, walk down preferring the child with the **opposite** bit. Taking it sets that bit of the result.
> **Difficulty:** Medium · **Pattern:** Binary trie, greedy opposite bit · **Also on:** [LC 421](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/maximum-xor-of-two-numbers-in-an-array?category=problems&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. All pairs](#3-all-pairs) · [4. Binary trie, greedy from MSB](#4-binary-trie-greedy-from-msb) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, return the maximum value of `nums[i] XOR nums[j]` with `0 ≤ i ≤ j < n`.

| Input | Output | Why |
|---|---|---|
| `[3,10,5,25,2,8]` | `28` | 5 XOR 25 |
| `[14,70,53,83,49,91,36,80,92,51,66,70]` | `127` |  |
| `[0]` | `0` |  |

**Constraints:** `1 ≤ n ≤ 2·10⁵`, `0 ≤ nums[i] < 2³¹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| All pairs | try every (i, j) | O(n²) | O(1) |
| Binary trie, greedy from MSB | insert bits 30..0; query takes the opposite bit when it exists | O(31·n) | O(31·n) |

> [!tip] Interview angle
> Explain the greedy exchange argument: once you can set bit `b`, nothing in bits `< b` can make up for losing it (`2^b > 2^b − 1`). Then show the binary trie. The 31-bit width is fixed, so this is O(31·n) = O(n).

---

## 3. All pairs

**Intuition.** Compute `a ^ b` for every pair and keep the maximum. Fine for small `n`, but TLE at `2·10⁵`.

```python
def max_xor_pairs(nums):
    return max(a ^ b for a in nums for b in nums)
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Binary trie, greedy from MSB

**Intuition.** Each trie node has two children (bit 0/1). For query `x`, at bit `b` let `want = 1 − bit(x, b)`. If that child exists, go there and set bit `b` of the answer; otherwise follow the same bit.

**Algorithm**

1. Insert every number, bits 30 down to 0.
2. For each `x`: `node = root, cur = 0`; for `b = 30..0`: `want = ((x >> b) & 1) ^ 1`; if `child[want]` exists, `cur |= 1 << b` and go there, else go to `child[want ^ 1]`.
3. Answer = max `cur`.

**Dry run** — x = 5 (00101) vs trie holding 25 (11001): bits 4, 3 differ → take them; bit 2: 5 has 1, 25 has 0 → take; bit 0 both 1. 11100 = 28.

**C++**
```cpp
int findMaximumXOR(vector<int>& nums) {
    vector<array<int, 2>> t(1, {0, 0});
    for (int x : nums) {
        int n = 0;
        for (int b = 30; b >= 0; b--) {
            int bit = (x >> b) & 1;
            if (!t[n][bit]) { t[n][bit] = t.size(); t.push_back({0, 0}); }
            n = t[n][bit];
        }
    }
    int best = 0;
    for (int x : nums) {
        int n = 0, cur = 0;
        for (int b = 30; b >= 0; b--) {
            int want = ((x >> b) & 1) ^ 1;
            if (t[n][want]) { cur |= 1 << b; n = t[n][want]; }
            else n = t[n][want ^ 1];
        }
        best = max(best, cur);
    }
    return best;
}
```

**Java**
```java
static int findMaximumXOR(int[] nums) {
    int[][] t = new int[31 * nums.length + 1][2];
    int sz = 1;
    for (int x : nums) {
        int n = 0;
        for (int b = 30; b >= 0; b--) {
            int bit = (x >> b) & 1;
            if (t[n][bit] == 0) t[n][bit] = sz++;
            n = t[n][bit];
        }
    }
    int best = 0;
    for (int x : nums) {
        int n = 0, cur = 0;
        for (int b = 30; b >= 0; b--) {
            int want = ((x >> b) & 1) ^ 1;
            if (t[n][want] != 0) { cur |= 1 << b; n = t[n][want]; }
            else n = t[n][want ^ 1];
        }
        best = Math.max(best, cur);
    }
    return best;
}
```

**Python**
```python
def find_maximum_xor(nums):
    t = [[0, 0]]
    for x in nums:
        n = 0
        for b in range(30, -1, -1):
            bit = (x >> b) & 1
            if not t[n][bit]:
                t[n][bit] = len(t)
                t.append([0, 0])
            n = t[n][bit]
    best = 0
    for x in nums:
        n = cur = 0
        for b in range(30, -1, -1):
            want = ((x >> b) & 1) ^ 1
            if t[n][want]:
                cur |= 1 << b
                n = t[n][want]
            else:
                n = t[n][want ^ 1]
        best = max(best, cur)
    return best
```

**Complexity:** time **O(31·n)**, space **O(31·n)** — each insert/query is 31 steps; node count ≤ 31·n + 1.

---

## Edge cases

- Single element → 0 (`i = j`).
- Values up to 2³¹ − 1 → start at bit 30.
- All equal → 0.

---

## Common mistakes

1. Walking bits LSB first (the greedy only works MSB first).
2. Querying before inserting anything (an empty trie has no children). Insert all first, or insert-then-query each.
3. Using 32 bits with signed shifts on negative input.

---

## Follow-ups

1. Prefix-sum version: max XOR subarray?
2. Without a trie?

<details><summary>Answer sketches</summary>

**#1:** Insert prefix XORs `P[0..i−1]` and query with `P[i]`: `XOR(l..r) = P[r+1] ^ P[l]`.

**#2:** Bit-by-bit prefix set: for `b = 30..0`, guess `ans | 1<<b` and check whether two prefixes XOR to it via a hash set. Also O(31·n).
</details>

---

## Flashcards

**Why go MSB first for max XOR?** #flashcard
Bit b is worth more than all lower bits combined (2^b > 2^b − 1).

**Binary trie query for max XOR?** #flashcard
At each bit, go to the child with the opposite bit if it exists and set that bit of the answer.

**Interview track →** [Trie deep-dive](../../01-data-structures/09-trie.md) · [Bit manipulation](../../02-algorithms/17-bit-manipulation.md) · [Trie walkthroughs](../../coding/data-structures/09-trie.md)
