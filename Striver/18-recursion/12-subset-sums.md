---
module: striver/18-recursion
lesson: 12
topic: Subsets I (Subset Sums)
difficulty: Medium
source: https://takeuforward.org/learning/dsa/subsets-i?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, subsequence]
---
# 12. Subsets I (Subset Sums)

← [Combination Sum II](11-combination-sum-ii.md) · [Part 18 index](README.md) · Next → [Subsets II](13-subsets-ii.md)

> [!abstract] Problem at a glance
> **Task:** Return the sums of all 2ⁿ subsets of an array.
> **Key insight:** Pick/not-pick carrying only the running sum — no list to copy, so each leaf costs O(1). 2ⁿ leaves → O(2ⁿ) plus sorting if a sorted output is required.
> **Difficulty:** Medium · **Pattern:** Pick / not-pick with an accumulator · **Also on:** [GfG Subset Sums](https://www.geeksforgeeks.org/problems/subset-sums2234/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/subsets-i?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Bitmask sums](#3-bitmask-sums) · [4. Recursion with running sum](#4-recursion-with-running-sum) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums` of `n` integers, return the sums of all `2ⁿ` subsets (including the empty subset, sum 0). Any order.

| Input | Output | Why |
|---|---|---|
| `nums = [2, 3]` | `[0, 2, 3, 5]` |  |
| `nums = [5, 2, 1]` | `[0, 1, 2, 3, 5, 6, 7, 8]` |  |

**Constraints:** `1 ≤ n ≤ 15`, `0 ≤ nums[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Bitmask sums | for each mask sum the selected elements | O(n · 2ⁿ) | O(2ⁿ) |
| Recursion with running sum | go(i, s): skip → go(i+1, s); take → go(i+1, s + a[i]) | O(2ⁿ) | O(n) stack + output |

> [!tip] Interview angle
> Warm-up: recognise that you don't need the subsets themselves, only the accumulator — a cheaper state. It's also the building block for meet-in-the-middle (split in halves, enumerate each half's sums, combine by sorting/two pointers) when n ≈ 40.

---

## 3. Bitmask sums

**Intuition.** Same enumeration as the power set, accumulating values instead of building lists.

```python
def subset_sums_mask(nums):
    n = len(nums)
    return [sum(nums[i] for i in range(n) if m >> i & 1) for m in range(1 << n)]
```

**Complexity:** time **O(n · 2ⁿ)**, space **O(2ⁿ)**.

---

## 4. Recursion with running sum

**Intuition.** Each node does O(1) work and passes the sum by value, so nothing needs undoing.

**Dry run** — [2, 3]: skip 2 → skip 3 → 0, take 3 → 3; take 2 → skip 3 → 2, take 3 → 5.

**C++**
```cpp
void go(int i, int s, vector<int>& a, vector<int>& out) {
    if (i == (int)a.size()) { out.push_back(s); return; }
    go(i + 1, s, a, out);
    go(i + 1, s + a[i], a, out);
}
vector<int> subsetSums(vector<int>& nums) {
    vector<int> out;
    go(0, 0, nums, out);
    return out;
}
```

**Java**
```java
static void go(int i, int s, int[] a, List<Integer> out) {
    if (i == a.length) { out.add(s); return; }
    go(i + 1, s, a, out);
    go(i + 1, s + a[i], a, out);
}
static List<Integer> subsetSums(int[] nums) {
    List<Integer> out = new ArrayList<>();
    go(0, 0, nums, out);
    return out;
}
```

**Python**
```python
def subset_sums(nums):
    out = []
    def go(i, s):
        if i == len(nums):
            out.append(s)
            return
        go(i + 1, s)
        go(i + 1, s + nums[i])
    go(0, 0)
    return out
```

**Complexity:** time **O(2ⁿ)**, space **O(n) stack + output** — 2ⁿ leaves, O(1) per node.

---

## Edge cases

- Zeros produce repeated sums — keep them (2ⁿ entries).
- n = 1 → `[0, x]`.

---

## Common mistakes

1. Dropping the empty subset's 0.
2. Deduping sums — the problem wants all 2ⁿ.

---

## Follow-ups

1. n = 40, count subsets with sum ≤ K.
2. Closest subsequence sum (LC 1755).

<details><summary>Answer sketches</summary>

**#1:** Meet in the middle: 2²⁰ sums per half, sort one, binary search for each of the other.

**#2:** Same split; two pointers over the two sorted lists.
</details>

---

## Flashcards

**Subset sums recursion cost?** #flashcard
O(2ⁿ) — O(1) per node, nothing to copy.

**Meet in the middle for n ≈ 40?** #flashcard
Enumerate 2^(n/2) sums of each half, sort, combine with binary search / two pointers.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../coding/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../coding/algorithms/12-backtracking.md)
