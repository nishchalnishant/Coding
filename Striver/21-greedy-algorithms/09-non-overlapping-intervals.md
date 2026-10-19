---
module: striver/21-greedy-algorithms
lesson: 9
topic: Non-overlapping Intervals
difficulty: Medium
source: https://takeuforward.org/learning/dsa/non-overlapping-intervals?category=scheduling-and-interval-problems&source=strivers-a2z-dsa-sheet
tags: [striver, greedy-algorithms, greedy, intervals, sorting]
---
# 9. Non-overlapping Intervals

← [N Meetings in One Room](08-n-meetings-in-one-room.md) · [Part 21 index](README.md) · Next → [Insert Interval](10-insert-interval.md)

> [!abstract] Problem at a glance
> **Task:** Return the minimum number of intervals to remove so the rest don't overlap (touching endpoints are fine).
> **Key insight:** Removing the minimum = keeping the maximum non-overlapping set, which is activity selection: sort by end and keep greedily. Answer = n − kept.
> **Difficulty:** Medium · **Pattern:** Activity selection (complement) · **Also on:** [LC 435](https://leetcode.com/problems/non-overlapping-intervals/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/non-overlapping-intervals?category=scheduling-and-interval-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Sort by end, count keepers](#3-sort-by-end-count-keepers) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `intervals[i] = [start, end]`, return the minimum number of intervals you need to remove to make the rest non-overlapping. Intervals `[1,2]` and `[2,3]` do not overlap.

| Input | Output | Why |
|---|---|---|
| `[[1,2],[2,3],[3,4],[1,3]]` | `1` | remove [1,3] |
| `[[1,2],[1,2],[1,2]]` | `2` |  |
| `[[1,2],[2,3]]` | `0` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, `−5·10⁴ ≤ start < end ≤ 5·10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Sort by end, count keepers | keep if start ≥ lastEnd; answer n − kept | O(n log n) | O(1) extra |

> [!tip] Interview angle
> Recognise it as N Meetings in disguise and say so. A common follow-up: "sort by start instead?" — works too if, on overlap, you keep the interval with the smaller end.

---

## 3. Sort by end, count keepers

**Intuition.** Exactly the activity-selection greedy with non-strict comparison (touching is allowed). Everything not kept is removed.

**Dry run** — Sorted by end: [1,2] keep (last 2), [2,3] keep (3), [1,3] 1 < 3 remove, [3,4] keep. Removed 1.

**Start-sorted variant:** sort by start; on overlap (`start < prevEnd`), remove one and set `prevEnd = min(prevEnd, end)` — i.e. keep the one ending first.

**C++**
```cpp
int eraseOverlapIntervals(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end(),
         [](const vector<int>& a, const vector<int>& b) { return a[1] < b[1]; });
    int kept = 0;
    long long last = LLONG_MIN;
    for (auto& iv : intervals)
        if (iv[0] >= last) { kept++; last = iv[1]; }
    return intervals.size() - kept;
}
```

**Java**
```java
static int eraseOverlapIntervals(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[1], b[1]));
    int kept = 0;
    long last = Long.MIN_VALUE;
    for (int[] iv : intervals)
        if (iv[0] >= last) { kept++; last = iv[1]; }
    return intervals.length - kept;
}
```

**Python**
```python
def erase_overlap_intervals(intervals):
    kept, last = 0, float('-inf')
    for s, e in sorted(intervals, key=lambda x: x[1]):
        if s >= last:
            kept += 1
            last = e
    return len(intervals) - kept
```

**Complexity:** time **O(n log n)**, space **O(1) extra** — sort plus one pass.

---

## Edge cases

- Touching endpoints don't overlap here (`≥`).
- Negative coordinates — don't initialise `last` to 0 or −1.
- All identical intervals → n − 1.

---

## Common mistakes

1. Initialising `last = 0` with negative starts.
2. Sorting by start and always removing the later interval.
3. Strict `>` — counts touching intervals as overlapping.

---

## Follow-ups

1. Minimum arrows to burst balloons (LC 452).
2. Return which intervals to remove.

<details><summary>Answer sketches</summary>

**#1:** Same sort-by-end greedy; touching **does** count as overlap, so use `>`.

**#2:** Track indices of non-kept intervals during the scan.
</details>

---

## Flashcards

**Min removals for non-overlap?** #flashcard
n − (max non-overlapping kept), via sort by end.

**Start-sorted alternative?** #flashcard
On overlap remove one and keep the smaller end: `prevEnd = min(prevEnd, end)`.

**Interview track →** [Greedy deep-dive](../../02-algorithms/16-greedy.md) · [Greedy walkthroughs](../../coding/algorithms/16-greedy.md)
