---
module: striver-a2z/15-hashing
lesson: 2
topic: Longest Consecutive Sequence in an Array
difficulty: Medium
source: https://takeuforward.org/learning/dsa/longest-consecutive-sequence-in-an-array?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, hashing, hashing, set, array]
---
# 2. Longest Consecutive Sequence in an Array

← [Basic Hashing](01-basic-hashing.md) · [Part 15 index](README.md) · Next → [Longest Subarray with Sum K](03-longest-subarray-with-sum-k.md)

> [!abstract] Problem at a glance
> **Task:** Return the length of the longest run of consecutive integers (`x, x + 1, x + 2, …`) whose values all appear in `nums`, in any order.
> **Key insight:** Put everything in a set. Only start counting at a value `x` with `x − 1` missing (a run's start); walk up while `x + 1` exists. Each value is visited by at most one walk, so the total is O(n).
> **Difficulty:** Medium · **Pattern:** Hash set + run starts · **Also on:** [LC 128](https://leetcode.com/problems/longest-consecutive-sequence/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/longest-consecutive-sequence-in-an-array?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force: linear search for the next value](#3-brute-force-linear-search-for-the-next-value) · [4. Sort and scan](#4-sort-and-scan) · [5. Hash set, start only at run starts](#5-hash-set-start-only-at-run-starts) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an unsorted integer array `nums`, return the length of the longest sequence of consecutive integers that can be formed from its elements. Elements don't need to be adjacent in the array. Duplicates count once.

| Input | Output | Why |
|---|---|---|
| `nums = [100, 4, 200, 1, 3, 2]` | `4` | 1, 2, 3, 4 |
| `nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]` | `9` | 0..8 |
| `nums = [1, 2, 2, 3]` | `3` | duplicate ignored |

**Constraints:** `0 ≤ n ≤ 10⁵`, `−10⁹ ≤ nums[i] ≤ 10⁹`. Aim for O(n).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force: linear search for the next value | for each x, scan for x + 1, x + 2, … | O(n³) worst / O(n²) typical | O(1) |
| Sort and scan | sort; extend the run on +1, ignore duplicates, reset otherwise | O(n log n) | O(1) extra (in-place sort) |
| Hash set, start only at run starts | x is a start iff x − 1 ∉ set; walk up from starts | O(n) average | O(n) |

> [!tip] Interview angle
> The interviewer asks for O(n) specifically to rule out sorting. If they allow O(n log n), sorting is simpler and uses O(1) extra space — say both.

---

## 3. Brute force: linear search for the next value

**Intuition.** For every element, repeatedly search the array for the next integer. Each search is O(n).

```python
def longest_consecutive_brute(nums):
    best = 0
    for x in nums:
        cur, length = x, 1
        while cur + 1 in nums:      # linear scan on a list
            cur += 1
            length += 1
        best = max(best, length)
    return best
```

**Complexity:** time **O(n³) worst / O(n²) typical**, space **O(1)**.

---

## 4. Sort and scan

**Intuition.** After sorting, consecutive values sit next to each other. Walk once: if `a[i] == a[i − 1] + 1`, extend; if equal, skip (duplicate); else restart at 1.

```python
def longest_consecutive_sort(nums):
    if not nums:
        return 0
    a = sorted(nums)
    best = cur = 1
    for i in range(1, len(a)):
        if a[i] == a[i - 1]:
            continue
        cur = cur + 1 if a[i] == a[i - 1] + 1 else 1
        best = max(best, cur)
    return best
```

**Complexity:** time **O(n log n)**, space **O(1) extra (in-place sort)**.

---

## 5. Hash set, start only at run starts

**Intuition.** Without the start check, `[1..n]` would walk from every element: O(n²). With it, only `1` walks, and the walk touches each value once. Summed over all runs, the inner `while` does at most `n` steps total. Iterate over the **set**, not the array, so a duplicated start doesn't walk twice.

**Dry run** — set `{100, 4, 200, 1, 3, 2}`: 100 (99 ∉) → run 1; 4 (3 ∈) skip; 200 → 1; 1 (0 ∉) → 1, 2, 3, 4 → 4; 3, 2 skip. Answer 4.

**C++**
```cpp
int longestConsecutive(vector<int>& nums) {
    unordered_set<int> s(nums.begin(), nums.end());
    int best = 0;
    for (int x : s) {
        if (s.count(x - 1)) continue;
        int cur = x, len = 1;
        while (s.count(cur + 1)) { cur++; len++; }
        best = max(best, len);
    }
    return best;
}
```

**Java**
```java
static int longestConsecutive(int[] nums) {
    HashSet<Integer> s = new HashSet<>();
    for (int x : nums) s.add(x);
    int best = 0;
    for (int x : s) {
        if (s.contains(x - 1)) continue;
        int cur = x, len = 1;
        while (s.contains(cur + 1)) { cur++; len++; }
        best = Math.max(best, len);
    }
    return best;
}
```

**Python**
```python
def longest_consecutive(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 in s:
            continue
        cur = x
        while cur + 1 in s:
            cur += 1
        best = max(best, cur - x + 1)
    return best
```

**Complexity:** time **O(n) average**, space **O(n)** — each value is a walk step at most once, plus one start check.

---

## Edge cases

- Empty array → 0.
- Duplicates (count once).
- Negatives; runs crossing 0.
- `x + 1` overflow at `INT_MAX` in C++/Java — use `long` if values can hit the limit.

---

## Common mistakes

1. Walking from every element (no start check) → O(n²) on `[1..n]`.
2. Iterating over the array instead of the set → repeated walks on duplicates.
3. Treating duplicates as breaking the run in the sorted version.

---

## Follow-ups

1. Return the sequence itself.
2. Stream of inserts, query longest run.
3. Consecutive in a binary tree path (LC 298).

<details><summary>Answer sketches</summary>

**#1:** Track the start `x` of the best run; output `x..x + best − 1`.

**#2:** Union-Find: union `x` with `x ± 1` when present; track component sizes.

**#3:** DFS carrying the current run length.
</details>

---

## Flashcards

**Longest consecutive sequence in O(n)?** #flashcard
Hash set; start a walk only at x with x − 1 missing.

**Why is the set solution O(n) and not O(n²)?** #flashcard
Only run starts walk, and each value is walked over once in total.

**Interview track →** [Hashing deep-dive](../../01-data-structures/02-hashing.md) · [Hashing walkthroughs](../../04-practice/data-structures/02-hashing.md) · [Sliding window](../../02-algorithms/04-sliding-window.md)
