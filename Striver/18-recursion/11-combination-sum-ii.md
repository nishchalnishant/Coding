---
module: striver/18-recursion
lesson: 11
topic: Combination Sum II
difficulty: Medium
source: https://takeuforward.org/learning/dsa/combination-sum-ii?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, backtracking]
---
# 11. Combination Sum II

← [Combination Sum](10-combination-sum.md) · [Part 18 index](README.md) · Next → [Subsets I (Subset Sums)](12-subset-sums.md)

> [!abstract] Problem at a glance
> **Task:** Find all unique combinations (each element used at most once) summing to `target`, where the input may contain duplicates.
> **Key insight:** Sort, then in the loop at each level skip `c[j]` if `j > start` and `c[j] == c[j − 1]` — an equal value was already tried *at this position*. Recurse with `j + 1` for use-once. This dedupes without a set.
> **Difficulty:** Medium · **Pattern:** Backtracking with same-level duplicate skip · **Also on:** [LC 40](https://leetcode.com/problems/combination-sum-ii/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/combination-sum-ii?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Pick / not-pick + set of results](#3-pick--not-pick--set-of-results) · [4. Loop backtracking with sibling skip](#4-loop-backtracking-with-sibling-skip) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a collection `candidates` (may contain duplicates) and a `target`, return all unique combinations where the numbers sum to `target`. Each number in `candidates` may be used **once** per combination. The answer must not contain duplicate combinations.

| Input | Output | Why |
|---|---|---|
| `candidates = [10, 1, 2, 7, 6, 1, 5], target = 8` | `[[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]` |  |
| `candidates = [2, 5, 2, 1, 2], target = 5` | `[[1, 2, 2], [5]]` |  |

**Constraints:** `1 ≤ n ≤ 100`, `1 ≤ candidates[i] ≤ 50`, `1 ≤ target ≤ 30`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Pick / not-pick + set of results | enumerate subsets of the sorted array, dedupe with a set | O(2ⁿ · n) | O(2ⁿ · n) |
| Loop backtracking with sibling skip | sort; skip c[j] == c[j−1] when j > start; recurse j + 1 | O(2ⁿ · n) worst | O(n) |

> [!tip] Interview angle
> The duplicate-skip rule `j > start && c[j] == c[j−1]` is the whole question; be ready to explain why `j > start` (not `j > 0`): the first equal value at a level is allowed, so [1, 1, 6] still appears — you only skip *siblings*, not a child that reuses the next copy. Using a set of tuples works but is the answer they want you to improve on.

---

## 3. Pick / not-pick + set of results

**Intuition.** Sorting makes equal combinations produce identical tuples, so a set removes them. Correct but explores 2ⁿ subsets regardless of duplicates and needs the set.

```python
def comb2_set(candidates, target):
    c = sorted(candidates)
    seen, cur = set(), []
    def go(i, rem):
        if rem == 0:
            seen.add(tuple(cur))
            return
        if i == len(c) or c[i] > rem:
            return
        cur.append(c[i]); go(i + 1, rem - c[i]); cur.pop()
        go(i + 1, rem)
    go(0, target)
    return [list(t) for t in seen]
```

**Complexity:** time **O(2ⁿ · n)**, space **O(2ⁿ · n)**.

---

## 4. Loop backtracking with sibling skip

**Intuition.** At a given depth, the loop picks which value goes in the next slot. Picking two equal values for the same slot yields identical subtrees, so only the first is explored. Recursing on `j + 1` uses each index once; `break` on `c[j] > rem` prunes.

**Algorithm**

1. Sort.
2. `go(start, rem)`: rem == 0 → record.
3. For j = start …: if j > start and c[j] == c[j−1] → continue; if c[j] > rem → break; push; `go(j + 1, rem − c[j])`; pop.

**Dry run** — sorted [1, 1, 2, 5, 6, 7, 10], 8: slot 1 = 1(j0) → slot 2 = 1 → 6 ✓; slot 2 = 2 → 5 ✓; slot 2 = 7 ✓. slot 1 = 1(j1) skipped. slot 1 = 2 → 6 ✓.

**C++**
```cpp
void go(int start, int rem, vector<int>& c, vector<int>& cur, vector<vector<int>>& out) {
    if (rem == 0) { out.push_back(cur); return; }
    for (int j = start; j < (int)c.size(); j++) {
        if (j > start && c[j] == c[j - 1]) continue;
        if (c[j] > rem) break;
        cur.push_back(c[j]);
        go(j + 1, rem - c[j], c, cur, out);
        cur.pop_back();
    }
}
vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
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
    for (int j = start; j < c.length; j++) {
        if (j > start && c[j] == c[j - 1]) continue;
        if (c[j] > rem) break;
        cur.add(c[j]);
        go(j + 1, rem - c[j], c, cur, out);
        cur.remove(cur.size() - 1);
    }
}
static List<List<Integer>> combinationSum2(int[] candidates, int target) {
    Arrays.sort(candidates);
    List<List<Integer>> out = new ArrayList<>();
    go(0, target, candidates, new ArrayList<>(), out);
    return out;
}
```

**Python**
```python
def combination_sum2(candidates, target):
    c = sorted(candidates)
    out, cur = [], []
    def go(start, rem):
        if rem == 0:
            out.append(cur[:])
            return
        for j in range(start, len(c)):
            if j > start and c[j] == c[j - 1]:
                continue
            if c[j] > rem:
                break
            cur.append(c[j])
            go(j + 1, rem - c[j])
            cur.pop()
    go(0, target)
    return out
```

**Complexity:** time **O(2ⁿ · n) worst**, space **O(n)** — worst case all distinct → subsets; duplicates only shrink the tree.

---

## Edge cases

- All equal values → at most one combination.
- No solution → `[]`.
- Target larger than the total sum.

---

## Common mistakes

1. `j > 0` instead of `j > start` — drops [1, 1, 6].
2. Skip check without sorting — duplicates aren't adjacent.
3. `return` instead of `continue` on a duplicate.

---

## Follow-ups

1. Return only the count.
2. Permutations II (LC 47).

<details><summary>Answer sketches</summary>

**#1:** 0/1 subset-count DP over distinct value groups (bounded multiplicity).

**#2:** Same idea with a `used[]` array: skip `nums[j] == nums[j−1] && !used[j−1]`.
</details>

---

## Flashcards

**Combination Sum II dedupe rule?** #flashcard
Sorted; skip j if j > start and c[j] == c[j − 1].

**Why `j > start` rather than `j > 0`?** #flashcard
Only siblings at the same depth are duplicates; the child may use the next equal copy.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../coding/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../coding/algorithms/12-backtracking.md)
