---
module: striver-a2z/20-bit-manipulation
lesson: 13
topic: Power Set (Bit Manipulation)
difficulty: Medium
source: https://takeuforward.org/learning/dsa/power-set-bit-manipulation?category=problems&source=strivers-a2z-dsa-sheet
tags: [striver, bit-manipulation, bits, subsets]
---
# 13. Power Set (Bit Manipulation)

← [Divide Two Integers](12-divide-two-integers.md) · [Part 20 index](README.md) · Next → [XOR of Numbers in a Given Range](14-xor-of-numbers-in-a-given-range.md)

> [!abstract] Problem at a glance
> **Task:** Return all subsets of an array of distinct integers using bitmasks.
> **Key insight:** Masks 0 … 2ⁿ − 1 are in one-to-one correspondence with subsets: bit i of the mask says whether `nums[i]` is included.
> **Difficulty:** Medium · **Pattern:** Enumerate masks 0 … 2ⁿ − 1 · **Also on:** [LC 78](https://leetcode.com/problems/subsets/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/power-set-bit-manipulation?category=problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursive pick / not-pick](#3-recursive-pick--not-pick) · [4. Bitmask enumeration](#4-bitmask-enumeration) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums` of **unique** elements, return all possible subsets (the power set). The answer may be in any order and must not contain duplicates.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 3]` | `[[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]` | 2³ = 8 subsets |
| `nums = [0]` | `[[], [0]]` |  |

**Constraints:** `1 ≤ n ≤ 10`, `−10 ≤ nums[i] ≤ 10`, distinct.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursive pick / not-pick | branch on each element | O(n·2ⁿ) | O(n) stack |
| Bitmask enumeration | for mask in 0…2ⁿ−1, include nums[i] if bit i set | O(n·2ⁿ) | O(n·2ⁿ) output |

> [!tip] Interview angle
> Contrast with the recursive pick/not-pick version from [Recursion](../18-recursion/README.md). The bitmask version is iterative and has no stack depth; both are O(n·2ⁿ). Mention that n ≤ 20 is the usual bound where 2ⁿ enumeration is acceptable.

---

## 3. Recursive pick / not-pick

**Intuition.** At index i, either include `nums[i]` or don't; record the subset at the end.

```python
def subsets_rec(nums):
    out, cur = [], []
    def go(i):
        if i == len(nums):
            out.append(cur[:])
            return
        cur.append(nums[i]); go(i + 1); cur.pop()
        go(i + 1)
    go(0)
    return out
```

**Complexity:** time **O(n·2ⁿ)**, space **O(n) stack**.

---

## 4. Bitmask enumeration

**Intuition.** Each mask encodes one subset. Iterate all `1 << n` masks; for each, test bits 0…n−1 and collect the selected elements.

**Dry run** — n = 3, mask 5 = 101 → bits 0 and 2 → [1, 3].

**C++**
```cpp
vector<vector<int>> subsets(vector<int>& nums) {
    int n = nums.size();
    vector<vector<int>> out;
    for (int mask = 0; mask < (1 << n); mask++) {
        vector<int> cur;
        for (int i = 0; i < n; i++)
            if (mask & (1 << i)) cur.push_back(nums[i]);
        out.push_back(cur);
    }
    return out;
}
```

**Java**
```java
static List<List<Integer>> subsets(int[] nums) {
    int n = nums.length;
    List<List<Integer>> out = new ArrayList<>();
    for (int mask = 0; mask < (1 << n); mask++) {
        List<Integer> cur = new ArrayList<>();
        for (int i = 0; i < n; i++)
            if ((mask & (1 << i)) != 0) cur.add(nums[i]);
        out.add(cur);
    }
    return out;
}
```

**Python**
```python
def subsets(nums):
    n = len(nums)
    out = []
    for mask in range(1 << n):
        out.append([nums[i] for i in range(n) if mask >> i & 1])
    return out
```

**Complexity:** time **O(n·2ⁿ)**, space **O(n·2ⁿ) output** — 2ⁿ masks × n bit tests.

---

## Edge cases

- n = 1 → [[], [x]].
- Empty subset must be included (mask 0).

---

## Common mistakes

1. `1 << n` for n ≥ 31 in int.
2. Forgetting the empty subset.
3. Using this on arrays with duplicates and expecting unique subsets.

---

## Follow-ups

1. Subsets with duplicates (LC 90).
2. Iterate only submasks of a mask m.
3. Gray-code order (each subset differs by one element).

<details><summary>Answer sketches</summary>

**#1:** Sort + recursion skipping equal siblings; or bitmask + set of tuples (wasteful).

**#2:** `for (s = m; s; s = (s − 1) & m)` — enumerates all submasks over all m in O(3ⁿ) total.

**#3:** `mask ^ (mask >> 1)`.
</details>

---

## Flashcards

**Subset ↔ mask mapping?** #flashcard
Bit i of mask set ⇔ nums[i] in the subset; masks 0…2ⁿ−1.

**Enumerate submasks of m?** #flashcard
`s = m; while s: …; s = (s − 1) & m` (+ empty).

**i-th Gray code?** #flashcard
`i ^ (i >> 1)`.

**Interview track →** [Bit manipulation deep-dive](../../02-algorithms/17-bit-manipulation.md)
