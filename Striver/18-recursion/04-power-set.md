---
module: striver/18-recursion
lesson: 4
topic: Power Set
difficulty: Medium
source: https://takeuforward.org/learning/dsa/power-set?category=implementation-problems&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, backtracking, bit-manipulation]
---
# 4. Power Set

← [Generate Parentheses](03-generate-parentheses.md) · [Part 18 index](README.md) · Next → [Count Good Numbers](05-count-good-numbers.md)

> [!abstract] Problem at a glance
> **Task:** Return all 2ⁿ subsets of an array of distinct integers.
> **Key insight:** Each element is either in or out — two branches per element, 2ⁿ leaves. Equivalently, the numbers 0 … 2ⁿ − 1 enumerate the subsets: bit i set means "take nums[i]".
> **Difficulty:** Medium · **Pattern:** Pick / not-pick recursion · bitmask enumeration · **Also on:** [LC 78](https://leetcode.com/problems/subsets/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/power-set?category=implementation-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Bitmask enumeration](#3-bitmask-enumeration) · [4. Cascading (iterative doubling)](#4-cascading-iterative-doubling) · [5. Pick / not-pick recursion](#5-pick--not-pick-recursion) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums` of **distinct** integers, return all possible subsets (the power set), in any order, without duplicates.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 3]` | `[[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]` | 2³ = 8 subsets |
| `nums = [0]` | `[[], [0]]` |  |

**Constraints:** `1 ≤ n ≤ 10`, `−10 ≤ nums[i] ≤ 10`, all distinct.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Bitmask enumeration | mask 0 … 2ⁿ − 1; bit i → include nums[i] | O(n · 2ⁿ) | O(n) per subset |
| Cascading (iterative doubling) | start with [[]]; for each x, add x to every existing subset | O(n · 2ⁿ) | O(n · 2ⁿ) |
| Pick / not-pick recursion | at index i: recurse without nums[i], then with it | O(n · 2ⁿ) | O(n) recursion |

> [!tip] Interview angle
> The template every subset/combination problem is built on — interviewers expect both the recursive and the bitmask version. State the cost: 2ⁿ subsets × O(n) to copy each = O(n · 2ⁿ), which is optimal since that's the output size.

---

## 3. Bitmask enumeration

**Intuition.** The binary digits of `mask` are an include/exclude vector. Iterating every mask visits every subset exactly once. No recursion; handy when you also need to index subsets (DP over masks).

```python
def subsets_mask(nums):
    n, out = len(nums), []
    for mask in range(1 << n):
        out.append([nums[i] for i in range(n) if mask >> i & 1])
    return out
```

**Complexity:** time **O(n · 2ⁿ)**, space **O(n) per subset**.

---

## 4. Cascading (iterative doubling)

**Intuition.** After processing the first i elements, the list holds all 2ⁱ subsets of them. Element `x` doubles it: the old subsets plus each old subset with `x` appended.

```python
def subsets_cascade(nums):
    out = [[]]
    for x in nums:
        out += [s + [x] for s in out]
    return out
```

**Complexity:** time **O(n · 2ⁿ)**, space **O(n · 2ⁿ)**.

---

## 5. Pick / not-pick recursion

**Intuition.** `go(i)` decides element `i`. Not-pick: recurse to `i + 1`. Pick: push `nums[i]`, recurse, pop. At `i == n` the current list is one subset — copy it. This exact shape solves subset sum, count subsequences, combination sum.

**Algorithm**

1. `go(i)`: if `i == n` → record a copy of `cur`.
2. `go(i + 1)` (skip).
3. `cur.push(nums[i])`; `go(i + 1)`; `cur.pop()` (take).

**Dry run** — [1, 2]: skip 1 → skip 2 [] · take 2 [2]; take 1 → skip 2 [1] · take 2 [1, 2].

**C++**
```cpp
void go(int i, vector<int>& nums, vector<int>& cur, vector<vector<int>>& out) {
    if (i == (int)nums.size()) { out.push_back(cur); return; }
    go(i + 1, nums, cur, out);
    cur.push_back(nums[i]);
    go(i + 1, nums, cur, out);
    cur.pop_back();
}
vector<vector<int>> subsets(vector<int>& nums) {
    vector<vector<int>> out;
    vector<int> cur;
    go(0, nums, cur, out);
    return out;
}
```

**Java**
```java
static void go(int i, int[] nums, List<Integer> cur, List<List<Integer>> out) {
    if (i == nums.length) { out.add(new ArrayList<>(cur)); return; }
    go(i + 1, nums, cur, out);
    cur.add(nums[i]);
    go(i + 1, nums, cur, out);
    cur.remove(cur.size() - 1);
}
static List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> out = new ArrayList<>();
    go(0, nums, new ArrayList<>(), out);
    return out;
}
```

**Python**
```python
def subsets(nums):
    out, cur = [], []
    def go(i):
        if i == len(nums):
            out.append(cur[:])
            return
        go(i + 1)
        cur.append(nums[i])
        go(i + 1)
        cur.pop()
    go(0)
    return out
```

**Complexity:** time **O(n · 2ⁿ)**, space **O(n) recursion** — 2ⁿ leaves, O(n) copy each; depth n.

---

## Edge cases

- n = 1 → `[[], [x]]`.
- Negative values — irrelevant to the logic.
- Output order is free; inner order follows the input.

---

## Common mistakes

1. Appending `cur` itself instead of a copy — every entry ends up identical (empty).
2. Forgetting the `pop` after the take branch.
3. `1 << n` overflow for n ≥ 31 in C++/Java (not an issue at n ≤ 10).

---

## Follow-ups

1. Array has duplicates (Subsets II).
2. Only subsets of size k.
3. Return subset sums only (Subsets I).

<details><summary>Answer sketches</summary>

**#1:** Sort, then in the loop-based recursion skip `nums[j] == nums[j−1]` for `j > i`.

**#2:** Prune when `len(cur) + (n − i) < k`; that's Combinations (LC 77).

**#3:** Carry the running sum instead of the list.
</details>

---

## Flashcards

**Power set size and cost to list it?** #flashcard
2ⁿ subsets, O(n · 2ⁿ) total.

**Bitmask meaning of subset `mask`?** #flashcard
Bit i set ⇔ nums[i] is included.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../coding/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../coding/algorithms/12-backtracking.md)
