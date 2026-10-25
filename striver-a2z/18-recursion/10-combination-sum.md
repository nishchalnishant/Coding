---
module: striver-a2z/18-recursion
lesson: 10
topic: Combination Sum
difficulty: Medium
source: https://takeuforward.org/learning/dsa/combination-sum?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, backtracking]
---
# 10. Combination Sum

← [Generate Binary Strings Without Consecutive 1s](09-binary-strings-no-consecutive-ones.md) · [Part 18 index](README.md) · Next → [Combination Sum II](11-combination-sum-ii.md)

> [!abstract] Problem at a glance
> **Task:** Find all unique combinations of distinct candidates (each reusable any number of times) that sum to `target`.
> **Key insight:** Loop-based backtracking from a start index: choosing `c[j]` recurses with start `j` (not `j + 1`) so it can be reused, and never looks back at earlier candidates — that's what makes combinations unique. Sort first so you can `break` when `c[j] > remaining`.
> **Difficulty:** Medium · **Pattern:** Backtracking with reuse (start index stays) · **Also on:** [LC 39](https://leetcode.com/problems/combination-sum/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/combination-sum?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Pick / not-pick with reuse](#3-pick--not-pick-with-reuse) · [4. Loop-based backtracking (sorted, with break)](#4-loop-based-backtracking-sorted-with-break) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array of **distinct** integers `candidates` and a `target`, return all unique combinations where the chosen numbers sum to `target`. The same number may be chosen unlimited times. Two combinations are different if the frequency of at least one number differs. Order of output is free.

| Input | Output | Why |
|---|---|---|
| `candidates = [2, 3, 6, 7], target = 7` | `[[2, 2, 3], [7]]` |  |
| `candidates = [2, 3, 5], target = 8` | `[[2, 2, 2, 2], [2, 3, 3], [3, 5]]` |  |
| `candidates = [2], target = 1` | `[]` |  |

**Constraints:** `1 ≤ n ≤ 30`, `2 ≤ candidates[i] ≤ 40`, distinct, `1 ≤ target ≤ 40`; fewer than 150 combinations.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Pick / not-pick with reuse | take c[i] (stay at i) or move to i + 1 | O(2^(t/m) · t) | O(t/m) |
| Loop-based backtracking (sorted, with break) | for j in [start, n): take c[j], recurse from j | O(2^(t/m) · t) | O(t/m) |

> [!tip] Interview angle
> The first of the Combination Sum family; interviewers move straight to II (duplicates, use once) and III (fixed size). Explain the difference in one line each: I recurses on `j`, II recurses on `j + 1` and skips equal neighbours, III also caps the length. Complexity is exponential — bound it by O(2^(t/min) · t) and move on.

---

## 3. Pick / not-pick with reuse

**Intuition.** Binary tree: at index i, either take `c[i]` again (stay at i, remaining shrinks) or move on to `i + 1`. Terminates because remaining strictly decreases or i increases. m = the smallest candidate.

```python
def comb_sum_pick(candidates, target):
    c = sorted(candidates)
    out, cur = [], []
    def go(i, rem):
        if rem == 0:
            out.append(cur[:])
            return
        if i == len(c) or c[i] > rem:
            return
        cur.append(c[i]); go(i, rem - c[i]); cur.pop()
        go(i + 1, rem)
    go(0, target)
    return out
```

**Complexity:** time **O(2^(t/m) · t)**, space **O(t/m)**.

---

## 4. Loop-based backtracking (sorted, with break)

**Intuition.** Each recursion level chooses the next element ≥ the previous one (by index). Starting the loop at `start` forbids permutations of the same multiset. Because `c` is sorted, once `c[j] > rem` every later candidate is too — `break`.

**Algorithm**

1. Sort candidates.
2. `go(start, rem)`: if rem == 0 → record copy.
3. For j = start … n − 1: if c[j] > rem break; push c[j]; `go(j, rem − c[j])`; pop.

**Dry run** — [2, 3, 6, 7], 7: 2 → 2 → 2 (rem 1, break) · 3 → rem 0 ✓ [2, 2, 3]; … 7 → ✓ [7].

**C++**
```cpp
void go(int start, int rem, vector<int>& c, vector<int>& cur, vector<vector<int>>& out) {
    if (rem == 0) { out.push_back(cur); return; }
    for (int j = start; j < (int)c.size() && c[j] <= rem; j++) {
        cur.push_back(c[j]);
        go(j, rem - c[j], c, cur, out);
        cur.pop_back();
    }
}
vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
    sort(candidates.begin(), candidates.end());
    vector<vector<int>> out;
    vector<int> cur;
    go(0, target, candidates, cur, out);
    return out;
}
```

**Java**
```java
static void go(int start, int rem, int[] c, List<Integer> cur, List<List<Integer>> out) {
    if (rem == 0) { out.add(new ArrayList<>(cur)); return; }
    for (int j = start; j < c.length && c[j] <= rem; j++) {
        cur.add(c[j]);
        go(j, rem - c[j], c, cur, out);
        cur.remove(cur.size() - 1);
    }
}
static List<List<Integer>> combinationSum(int[] candidates, int target) {
    Arrays.sort(candidates);
    List<List<Integer>> out = new ArrayList<>();
    go(0, target, candidates, new ArrayList<>(), out);
    return out;
}
```

**Python**
```python
def combination_sum(candidates, target):
    c = sorted(candidates)
    out, cur = [], []
    def go(start, rem):
        if rem == 0:
            out.append(cur[:])
            return
        for j in range(start, len(c)):
            if c[j] > rem:
                break
            cur.append(c[j])
            go(j, rem - c[j])
            cur.pop()
    go(0, target)
    return out
```

**Complexity:** time **O(2^(t/m) · t)**, space **O(t/m)** — depth ≤ t/m; each leaf copied in O(t/m).

---

## Edge cases

- No combination → `[]`.
- A single candidate equal to target.
- Unsorted input — sort before using `break`.

---

## Common mistakes

1. Recursing with `j + 1` — forbids reuse.
2. Starting the loop at 0 every level — emits [2, 3, 2], [3, 2, 2] as different answers.
3. `break` without sorting first.

---

## Follow-ups

1. Count combinations only (Coin Change II, LC 518).
2. Count ordered sequences (Combination Sum IV, LC 377).

<details><summary>Answer sketches</summary>

**#1:** 1D DP: for each coin, `ways[s] += ways[s − coin]` with s increasing.

**#2:** Outer loop on s, inner loop on coins — counts permutations.
</details>

---

## Flashcards

**Combination Sum: how is reuse allowed?** #flashcard
Recurse with start = j (same index).

**Why loop from `start` in combination backtracking?** #flashcard
Keeps chosen indices non-decreasing → each multiset once.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../04-practice/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../04-practice/algorithms/12-backtracking.md)
