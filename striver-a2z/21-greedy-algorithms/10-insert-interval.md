---
module: striver-a2z/21-greedy-algorithms
lesson: 10
topic: Insert Interval
difficulty: Medium
source: https://takeuforward.org/learning/dsa/insert-interval?category=scheduling-and-interval-problems&source=strivers-a2z-dsa-sheet
tags: [striver, greedy-algorithms, intervals, array]
---
# 10. Insert Interval

← [Non-overlapping Intervals](09-non-overlapping-intervals.md) · [Part 21 index](README.md) · Next → [Merge Intervals](11-merge-intervals.md)

> [!abstract] Problem at a glance
> **Task:** Insert `newInterval` into a sorted list of disjoint intervals, merging where necessary.
> **Key insight:** The list splits into three runs: intervals entirely left of the new one, intervals that overlap it (merge into one by min start / max end), and intervals entirely right. One linear pass.
> **Difficulty:** Medium · **Pattern:** Three-phase linear merge · **Also on:** [LC 57](https://leetcode.com/problems/insert-interval/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/insert-interval?category=scheduling-and-interval-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Append and re-merge](#3-append-and-re-merge) · [4. Three-phase scan](#4-three-phase-scan) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`intervals` is sorted by start and non-overlapping. Insert `newInterval = [s, e]` so the result is still sorted and non-overlapping (merge overlaps; touching intervals merge). Return the result.

| Input | Output | Why |
|---|---|---|
| `intervals = [[1,3],[6,9]], new = [2,5]` | `[[1,5],[6,9]]` |  |
| `intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], new = [4,8]` | `[[1,2],[3,10],[12,16]]` |  |

**Constraints:** `0 ≤ n ≤ 10⁴`, `0 ≤ start ≤ end ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Append and re-merge | add new interval, sort, Merge Intervals | O(n log n) | O(n) |
| Three-phase scan | copy left · absorb overlaps · copy right | O(n) | O(n) output |

> [!tip] Interview angle
> Not really greedy — it's careful boundary handling. Say the three phases out loud and nail the comparisons: left run is `end < s`, overlap run is `start ≤ e`.

---

## 3. Append and re-merge

**Intuition.** Reduce to Merge Intervals. Fine as a first answer but wastes the input's sortedness.

```python
def insert_resort(intervals, new):
    arr = sorted(intervals + [new])
    out = []
    for s, e in arr:
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
```

**Complexity:** time **O(n log n)**, space **O(n)**.

---

## 4. Three-phase scan

**Intuition.** Walk once. Phase 1: copy intervals that end before the new one starts. Phase 2: while an interval starts no later than the new one's end, expand the new interval to cover it. Append the merged interval. Phase 3: copy the rest.

**Algorithm**

1. `i = 0`; while `i < n` and `iv[i].end < s`: output `iv[i]`, `i++`.
2. While `i < n` and `iv[i].start ≤ e`: `s = min(s, iv[i].start)`, `e = max(e, iv[i].end)`, `i++`.
3. Output `[s, e]`.
4. Output the remaining intervals.

**Dry run** — [[1,2],[3,5],[6,7],[8,10],[12,16]], [4,8]: copy [1,2]; absorb [3,5]→[3,8], [6,7], [8,10]→[3,10]; stop at [12,16]. Output [[1,2],[3,10],[12,16]].

**O(log n) to find the boundaries** with binary search, but building the output is still O(n) — unless you're allowed to splice a balanced tree / `std::set` of intervals.

**C++**
```cpp
vector<vector<int>> insert(vector<vector<int>>& iv, vector<int>& nw) {
    vector<vector<int>> out;
    int i = 0, n = iv.size(), s = nw[0], e = nw[1];
    while (i < n && iv[i][1] < s) out.push_back(iv[i++]);
    while (i < n && iv[i][0] <= e) {
        s = min(s, iv[i][0]);
        e = max(e, iv[i][1]);
        i++;
    }
    out.push_back({s, e});
    while (i < n) out.push_back(iv[i++]);
    return out;
}
```

**Java**
```java
static int[][] insert(int[][] iv, int[] nw) {
    List<int[]> out = new ArrayList<>();
    int i = 0, n = iv.length, s = nw[0], e = nw[1];
    while (i < n && iv[i][1] < s) out.add(iv[i++]);
    while (i < n && iv[i][0] <= e) {
        s = Math.min(s, iv[i][0]);
        e = Math.max(e, iv[i][1]);
        i++;
    }
    out.add(new int[]{s, e});
    while (i < n) out.add(iv[i++]);
    return out.toArray(new int[0][]);
}
```

**Python**
```python
def insert(intervals, new):
    s, e = new
    out, i, n = [], 0, len(intervals)
    while i < n and intervals[i][1] < s:
        out.append(intervals[i]); i += 1
    while i < n and intervals[i][0] <= e:
        s = min(s, intervals[i][0])
        e = max(e, intervals[i][1])
        i += 1
    out.append([s, e])
    out.extend(intervals[i:])
    return out
```

**Complexity:** time **O(n)**, space **O(n) output** — each input interval is visited once.

---

## Edge cases

- Empty list.
- New interval before all / after all.
- Touching endpoints merge (`[1,5] + [5,7] → [1,7]`).
- New interval swallows everything.

---

## Common mistakes

1. Using `≤` in phase 1 (`end ≤ s`) — then a touching interval isn't merged.
2. Forgetting to append the merged interval when no overlap occurred.
3. Mutating input intervals that are aliased in the output.

---

## Follow-ups

1. Many insertions online.
2. Remove an interval (LC 1272).

<details><summary>Answer sketches</summary>

**#1:** Keep a balanced BST / `std::map` keyed by start; erase the overlapping range per insert — amortised O(log n).

**#2:** Same scan; split partially covered intervals into ≤ 2 pieces.
</details>

---

## Flashcards

**Insert Interval phases?** #flashcard
Copy `end < s`; absorb while `start ≤ e` (min/max); output merged; copy rest.

**Why O(n) and not O(log n)?** #flashcard
Output may need every interval; binary search only finds the boundaries.

**Interview track →** [Greedy deep-dive](../../02-algorithms/16-greedy.md) · [Greedy walkthroughs](../../04-practice/algorithms/16-greedy.md)
