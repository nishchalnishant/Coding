---
module: striver-a2z/18-recursion
lesson: 13
topic: Subsets II
difficulty: Medium
source: https://takeuforward.org/learning/dsa/subsets-ii?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, backtracking]
---
# 13. Subsets II

← [Subsets I (Subset Sums)](12-subset-sums.md) · [Part 18 index](README.md) · Next → [Combination Sum III](14-combination-sum-iii.md)

> [!abstract] Problem at a glance
> **Task:** Return all distinct subsets of an array that may contain duplicates.
> **Key insight:** Sort, then use the loop form: every recursion node *is* a subset (record it on entry), and the loop picks the next element with the sibling-skip `j > i && a[j] == a[j−1]`. Duplicates never get generated.
> **Difficulty:** Medium · **Pattern:** Loop backtracking with sibling skip · **Also on:** [LC 90](https://leetcode.com/problems/subsets-ii/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/subsets-ii?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Power set + set of sorted tuples](#3-power-set--set-of-sorted-tuples) · [4. Pick / not-pick, skip copies on not-pick](#4-pick--not-pick-skip-copies-on-not-pick) · [5. Loop backtracking, record every node](#5-loop-backtracking-record-every-node) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums` that may contain duplicates, return all possible subsets without duplicate subsets, in any order.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 2]` | `[[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]` | 6 instead of 8 |
| `nums = [0]` | `[[], [0]]` |  |

**Constraints:** `1 ≤ n ≤ 10`, `−10 ≤ nums[i] ≤ 10`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Power set + set of sorted tuples | generate 2ⁿ subsets of the sorted array, dedupe | O(n · 2ⁿ) | O(n · 2ⁿ) |
| Pick / not-pick, skip copies on not-pick | take a[i] → i+1; skip → jump past all copies of a[i] | O(n · 2ⁿ) | O(n) |
| Loop backtracking, record every node | record cur; for j ≥ i: skip equal siblings, push, recurse j + 1 | O(n · 2ⁿ) | O(n) |

> [!tip] Interview angle
> Pairs with Combination Sum II — same skip rule, but no target, so every node is recorded. If you present the pick/not-pick version, the dedupe there is: after deciding *not* to take `a[i]`, skip all following copies of it too.

---

## 3. Power set + set of sorted tuples

**Intuition.** Sorting first makes equal multisets equal tuples. Works, but generates every duplicate before discarding it.

```python
def subsets2_set(nums):
    a = sorted(nums)
    n, seen = len(a), set()
    for m in range(1 << n):
        seen.add(tuple(a[i] for i in range(n) if m >> i & 1))
    return [list(t) for t in seen]
```

**Complexity:** time **O(n · 2ⁿ)**, space **O(n · 2ⁿ)**.

---

## 4. Pick / not-pick, skip copies on not-pick

**Intuition.** If you decide not to take value v, taking a later copy of v at this point would create a subset you also get by taking the first copy. So the not-pick branch jumps to the first index with a different value.

```python
def subsets2_pick(nums):
    a = sorted(nums)
    out, cur = [], []
    def go(i):
        if i == len(a):
            out.append(cur[:])
            return
        cur.append(a[i]); go(i + 1); cur.pop()
        j = i
        while j < len(a) and a[j] == a[i]:
            j += 1
        go(j)
    go(0)
    return out
```

**Complexity:** time **O(n · 2ⁿ)**, space **O(n)**.

---

## 5. Loop backtracking, record every node

**Intuition.** The node reached by choosing indices i₁ < i₂ < … is the subset of those indices. Recording on entry captures every size. Sibling skip guarantees each multiset appears once.

**Algorithm**

1. Sort.
2. `go(i)`: record copy of cur.
3. For j = i … n − 1: if j > i and a[j] == a[j − 1] continue; push a[j]; `go(j + 1)`; pop.

**Dry run** — [1, 2, 2]: [] → [1] → [1,2] → [1,2,2]; (second 2 at depth 2 skipped) → [2] → [2,2]; (second 2 at depth 1 skipped).

**C++**
```cpp
void go(int i, vector<int>& a, vector<int>& cur, vector<vector<int>>& out) {
    out.push_back(cur);
    for (int j = i; j < (int)a.size(); j++) {
        if (j > i && a[j] == a[j - 1]) continue;
        cur.push_back(a[j]);
        go(j + 1, a, cur, out);
        cur.pop_back();
    }
}
vector<vector<int>> subsetsWithDup(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    vector<vector<int>> out;
    vector<int> cur;
    go(0, nums, cur, out);
    return out;
}
```

**Java**
```java
static void go(int i, int[] a, List<Integer> cur, List<List<Integer>> out) {
    out.add(new ArrayList<>(cur));
    for (int j = i; j < a.length; j++) {
        if (j > i && a[j] == a[j - 1]) continue;
        cur.add(a[j]);
        go(j + 1, a, cur, out);
        cur.remove(cur.size() - 1);
    }
}
static List<List<Integer>> subsetsWithDup(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> out = new ArrayList<>();
    go(0, nums, new ArrayList<>(), out);
    return out;
}
```

**Python**
```python
def subsets_with_dup(nums):
    a = sorted(nums)
    out, cur = [], []
    def go(i):
        out.append(cur[:])
        for j in range(i, len(a)):
            if j > i and a[j] == a[j - 1]:
                continue
            cur.append(a[j])
            go(j + 1)
            cur.pop()
    go(0)
    return out
```

**Complexity:** time **O(n · 2ⁿ)**, space **O(n)** — at most 2ⁿ nodes, O(n) copy each.

---

## Edge cases

- All equal → n + 1 subsets.
- All distinct → 2ⁿ (same as Subsets).
- Unsorted input.

---

## Common mistakes

1. Forgetting to sort.
2. Recording only at leaves in the loop form — loses most subsets.
3. Using `j > 0` in the skip.

---

## Follow-ups

1. Count distinct subsets.
2. Distinct subsequences of a string (LC 940).

<details><summary>Answer sketches</summary>

**#1:** Product over distinct values of (frequency + 1).

**#2:** DP: `dp = 2·dp − dp[last occurrence − 1]`.
</details>

---

## Flashcards

**Subsets II: where do you record?** #flashcard
At every node (on entry), not only at leaves.

**Number of distinct subsets of a multiset?** #flashcard
Π (freqᵥ + 1).

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../04-practice/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../04-practice/algorithms/12-backtracking.md)
