---
module: striver-a2z/21-greedy-algorithms
lesson: 11
topic: Merge Intervals
difficulty: Medium
source: https://takeuforward.org/learning/dsa/merge-intervals?category=scheduling-and-interval-problems&source=strivers-a2z-dsa-sheet
tags: [striver, greedy-algorithms, intervals, sorting]
---
# 11. Merge Intervals

← [Insert Interval](10-insert-interval.md) · [Part 21 index](README.md) · Next → [Minimum Number of Platforms](12-minimum-number-of-platforms.md)

> [!abstract] Problem at a glance
> **Task:** Merge all overlapping intervals and return the disjoint result.
> **Key insight:** After sorting by start, overlapping intervals are contiguous. Extend the last output interval while the next one starts ≤ its end; otherwise start a new one.
> **Difficulty:** Medium · **Pattern:** Sort by start + extend last · **Also on:** [LC 56](https://leetcode.com/problems/merge-intervals/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/merge-intervals?category=scheduling-and-interval-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force: pairwise merge until stable](#3-brute-force-pairwise-merge-until-stable) · [4. Sort + single pass](#4-sort--single-pass) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array of `intervals[i] = [start, end]`, merge all overlapping intervals (touching ones count as overlapping) and return an array of non-overlapping intervals covering the same points.

| Input | Output | Why |
|---|---|---|
| `[[1,3],[2,6],[8,10],[15,18]]` | `[[1,6],[8,10],[15,18]]` |  |
| `[[1,4],[4,5]]` | `[[1,5]]` | touching merges |

**Constraints:** `1 ≤ n ≤ 10⁴`, `0 ≤ start ≤ end ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force: pairwise merge until stable | for each interval scan the rest | O(n²) | O(n) |
| Sort + single pass | if start ≤ last.end: extend, else push | O(n log n) | O(n) output |

> [!tip] Interview angle
> Top-5 most-asked array question at Google. Write it clean in 5 minutes; the follow-ups (streaming input, already-sorted input, interval trees) are where the signal is.

---

## 3. Brute force: pairwise merge until stable

**Intuition.** Sort, then for each interval scan forward and absorb everything that overlaps the growing range, skipping absorbed ones. Quadratic in the worst case; mostly a stepping stone.

```python
def merge_brute(intervals):
    arr = sorted(intervals)
    n, out, i = len(arr), [], 0
    while i < n:
        s, e = arr[i]
        j = i + 1
        while j < n and arr[j][0] <= e:
            e = max(e, arr[j][1])
            j += 1
        out.append([s, e])
        i = j
    return out
```

**Complexity:** time **O(n²)**, space **O(n)**.

---

## 4. Sort + single pass

**Intuition.** Sort by start. Any interval that overlaps the current merged block must start before the block's end — and because of sorting, all such intervals come consecutively. So one comparison with the **last** output interval suffices.

**Dry run** — [[1,3],[2,6],[8,10],[15,18]]: push [1,3]; 2 ≤ 3 → [1,6]; 8 > 6 → push; 15 > 10 → push.

**Take `max` of ends**, not the new end: `[1,10]` followed by `[2,3]` must stay `[1,10]`.

**C++**
```cpp
vector<vector<int>> merge(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end());
    vector<vector<int>> out;
    for (auto& iv : intervals) {
        if (!out.empty() && iv[0] <= out.back()[1])
            out.back()[1] = max(out.back()[1], iv[1]);
        else
            out.push_back(iv);
    }
    return out;
}
```

**Java**
```java
static int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
    List<int[]> out = new ArrayList<>();
    for (int[] iv : intervals) {
        if (!out.isEmpty() && iv[0] <= out.get(out.size() - 1)[1])
            out.get(out.size() - 1)[1] = Math.max(out.get(out.size() - 1)[1], iv[1]);
        else
            out.add(new int[]{iv[0], iv[1]});
    }
    return out.toArray(new int[0][]);
}
```

**Python**
```python
def merge(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
```

**Complexity:** time **O(n log n)**, space **O(n) output** — sorting dominates; the merge pass is linear.

---

## Edge cases

- One interval.
- Unsorted input.
- Nested intervals (`[1,10]`, `[2,3]`).
- Zero-length intervals `[0,0]`.

---

## Common mistakes

1. `out[-1][1] = e` instead of `max(...)` — breaks on nested intervals.
2. Comparing with the previous **input** interval instead of the last merged one.
3. Forgetting to sort.

---

## Follow-ups

1. Intervals arrive as a stream; query the merged set any time (LC 352).
2. Total covered length.

<details><summary>Answer sketches</summary>

**#1:** Ordered map keyed by start; on insert merge with neighbours — O(log n).

**#2:** Sum `e − s` of the merged list, or a sweep over ±1 events.
</details>

---

## Flashcards

**Merge Intervals in one line?** #flashcard
Sort by start; if `s ≤ last.end` set `last.end = max(last.end, e)` else push.

**Why compare only with the last merged interval?** #flashcard
After sorting by start, everything overlapping the current block is contiguous.

**Interview track →** [Greedy deep-dive](../../02-algorithms/16-greedy.md) · [Greedy walkthroughs](../../04-practice/algorithms/16-greedy.md)
