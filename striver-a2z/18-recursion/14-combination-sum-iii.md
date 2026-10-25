---
module: striver-a2z/18-recursion
lesson: 14
topic: Combination Sum III
difficulty: Medium
source: https://takeuforward.org/learning/dsa/combination-sum-iii?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, backtracking]
---
# 14. Combination Sum III

← [Subsets II](13-subsets-ii.md) · [Part 18 index](README.md) · Next → [Letter Combinations of a Phone Number](15-letter-combinations-of-a-phone-number.md)

> [!abstract] Problem at a glance
> **Task:** Find all combinations of `k` distinct digits from 1–9 that sum to `n`.
> **Key insight:** Choose digits in increasing order from `start`; stop when the size reaches k. Prune when the next digit exceeds the remaining sum (digits are increasing). The search space is at most C(9, k) ≤ 126.
> **Difficulty:** Medium · **Pattern:** Backtracking with size cap · **Also on:** [LC 216](https://leetcode.com/problems/combination-sum-iii/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/combination-sum-iii?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Enumerate 512 masks](#3-enumerate-512-masks) · [4. Backtracking in increasing order](#4-backtracking-in-increasing-order) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Find all valid combinations of `k` numbers that sum to `n` such that only digits 1 through 9 are used and each is used at most once. Return the list of combinations (no duplicates), in any order.

| Input | Output | Why |
|---|---|---|
| `k = 3, n = 7` | `[[1, 2, 4]]` |  |
| `k = 3, n = 9` | `[[1, 2, 6], [1, 3, 5], [2, 3, 4]]` |  |
| `k = 4, n = 1` | `[]` |  |

**Constraints:** `2 ≤ k ≤ 9`, `1 ≤ n ≤ 60`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Enumerate 512 masks | keep masks with k bits whose digits sum to n | O(9 · 2⁹) | O(1) extra |
| Backtracking in increasing order | for d in start..9: if d > rem break; push; recurse d + 1 | O(C(9, k) · k) | O(k) |

> [!tip] Interview angle
> A quick one — the value is in stating the tight bound (C(9, k)) and adding two prunes: `d > rem → break` and "not enough digits left". The bitmask version over 2⁹ = 512 masks is equally acceptable and shows you notice the tiny universe.

---

## 3. Enumerate 512 masks

**Intuition.** The universe is {1…9}, so all subsets fit in 9 bits. Filter by popcount and sum.

```python
def cs3_mask(k, n):
    out = []
    for m in range(1 << 9):
        ds = [d + 1 for d in range(9) if m >> d & 1]
        if len(ds) == k and sum(ds) == n:
            out.append(ds)
    return out
```

**Complexity:** time **O(9 · 2⁹)**, space **O(1) extra**.

---

## 4. Backtracking in increasing order

**Intuition.** Build increasing combinations; record when `len == k and rem == 0`; return when `len == k` regardless. Because digits increase, `d > rem` means every later digit fails too.

**Dry run** — k = 3, n = 9: 1 → 2 → 6 ✓; 1 → 3 → 5 ✓; 1 → 4 → (needs 4, but d starts at 5) ✗; 2 → 3 → 4 ✓.

**C++**
```cpp
void go(int start, int k, int rem, vector<int>& cur, vector<vector<int>>& out) {
    if ((int)cur.size() == k) { if (rem == 0) out.push_back(cur); return; }
    for (int d = start; d <= 9 && d <= rem; d++) {
        cur.push_back(d);
        go(d + 1, k, rem - d, cur, out);
        cur.pop_back();
    }
}
vector<vector<int>> combinationSum3(int k, int n) {
    vector<vector<int>> out;
    vector<int> cur;
    go(1, k, n, cur, out);
    return out;
}
```

**Java**
```java
static void go(int start, int k, int rem, List<Integer> cur, List<List<Integer>> out) {
    if (cur.size() == k) { if (rem == 0) out.add(new ArrayList<>(cur)); return; }
    for (int d = start; d <= 9 && d <= rem; d++) {
        cur.add(d);
        go(d + 1, k, rem - d, cur, out);
        cur.remove(cur.size() - 1);
    }
}
static List<List<Integer>> combinationSum3(int k, int n) {
    List<List<Integer>> out = new ArrayList<>();
    go(1, k, n, new ArrayList<>(), out);
    return out;
}
```

**Python**
```python
def combination_sum3(k, n):
    out, cur = [], []
    def go(start, rem):
        if len(cur) == k:
            if rem == 0:
                out.append(cur[:])
            return
        for d in range(start, 10):
            if d > rem:
                break
            cur.append(d)
            go(d + 1, rem - d)
            cur.pop()
    go(1, n)
    return out
```

**Complexity:** time **O(C(9, k) · k)**, space **O(k)** — at most C(9, k) leaves.

---

## Edge cases

- n > 45 or n < k(k+1)/2 → `[]`.
- k = 9 → only n = 45 works.

---

## Common mistakes

1. Not stopping at size k — recursion keeps adding digits.
2. Recording at size k without checking rem == 0.

---

## Follow-ups

1. Min/max sum quick reject.
2. Count only.

<details><summary>Answer sketches</summary>

**#1:** Smallest k digits sum k(k+1)/2, largest sum k(19−k)/2; outside → empty.

**#2:** DP over digits: `ways[c][s]` for count c and sum s.
</details>

---

## Flashcards

**Combination Sum III search-space bound?** #flashcard
C(9, k) ≤ 126 leaves.

**Combination Sum I / II / III one-line difference?** #flashcard
I: recurse on j (reuse). II: j + 1 + skip equal siblings. III: digits 1–9, j + 1, size k.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../04-practice/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../04-practice/algorithms/12-backtracking.md)
