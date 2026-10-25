---
module: striver-a2z/21-greedy-algorithms
lesson: 8
topic: N Meetings in One Room
difficulty: Easy
source: https://takeuforward.org/learning/dsa/n-meetings-in-one-room?category=scheduling-and-interval-problems&source=strivers-a2z-dsa-sheet
tags: [striver, greedy-algorithms, greedy, intervals, sorting]
---
# 8. N Meetings in One Room

← [Job Sequencing Problem](07-job-sequencing-problem.md) · [Part 21 index](README.md) · Next → [Non-overlapping Intervals](09-non-overlapping-intervals.md)

> [!abstract] Problem at a glance
> **Task:** Given meeting start and end times, return the maximum number of meetings that fit in one room (a meeting may not start at the exact time the previous ends).
> **Key insight:** Activity selection: always pick the meeting that **ends earliest** among those compatible with what you've chosen — it leaves the most room for the rest.
> **Difficulty:** Easy · **Pattern:** Sort by end time (activity selection)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/n-meetings-in-one-room?category=scheduling-and-interval-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Sort by end, pick compatible](#3-sort-by-end-pick-compatible) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `start[i]` and `end[i]` for n meetings and one room, return the maximum number of meetings that can be held. A meeting can start only strictly after the previous selected one ends (`start > lastEnd`).

| Input | Output | Why |
|---|---|---|
| `start = [1,3,0,5,8,5], end = [2,4,6,7,9,9]` | `4` | (1,2) (3,4) (5,7) (8,9) |
| `start = [10,12,20], end = [20,25,30]` | `1` | all overlap at the boundaries |

**Constraints:** `1 ≤ n ≤ 10⁵`, `0 ≤ start[i] < end[i] ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Sort by end, pick compatible | if start > lastEnd: take it | O(n log n) | O(n) |

> [!tip] Interview angle
> The canonical greedy proof: "greedy stays ahead" — after k picks, greedy's k-th end time ≤ any optimal schedule's k-th end time, so greedy can always fit at least as many. Be precise about strict vs non-strict comparison at the boundary.

---

## 3. Sort by end, pick compatible

**Intuition.** Order meetings by end time (ties: any order). Keep `lastEnd`. Take a meeting iff it starts after `lastEnd`; then update `lastEnd`.

**Algorithm**

1. Pair `(end, start)` and sort.
2. `lastEnd = −∞`, `count = 0`.
3. For each: if `start > lastEnd`, `count++`, `lastEnd = end`.

**Dry run** — Sorted by end: (1,2) take, (3,4) take, (0,6) skip, (5,7) take, (8,9) take, (5,9) skip → 4.

**Sorting by start time is wrong:** one long early meeting would block many short ones. Sorting by duration is also wrong: a short meeting can straddle two compatible long ones.

**C++**
```cpp
int maxMeetings(vector<int>& start, vector<int>& end) {
    int n = start.size();
    vector<pair<int,int>> m(n);
    for (int i = 0; i < n; i++) m[i] = {end[i], start[i]};
    sort(m.begin(), m.end());
    int count = 0, last = INT_MIN;
    for (auto& [e, s] : m)
        if (s > last) { count++; last = e; }
    return count;
}
```

**Java**
```java
static int maxMeetings(int[] start, int[] end) {
    int n = start.length;
    int[][] m = new int[n][];
    for (int i = 0; i < n; i++) m[i] = new int[]{end[i], start[i]};
    Arrays.sort(m, (a, b) -> Integer.compare(a[0], b[0]));
    int count = 0, last = Integer.MIN_VALUE;
    for (int[] x : m)
        if (x[1] > last) { count++; last = x[0]; }
    return count;
}
```

**Python**
```python
def max_meetings(start, end):
    count, last = 0, float('-inf')
    for e, s in sorted(zip(end, start)):
        if s > last:
            count += 1
            last = e
    return count
```

**Complexity:** time **O(n log n)**, space **O(n)** — sort plus one linear pass.

---

## Edge cases

- Meetings that touch at a boundary — strict `>` per this problem; LC 435 treats touching as compatible.
- One meeting.
- Identical meetings.

---

## Common mistakes

1. Sorting by start or by duration.
2. Using `≥` when the problem requires strict inequality (or vice versa).
3. Losing the pairing between start and end when sorting.

---

## Follow-ups

1. Return the chosen meeting indices.
2. Several rooms: minimum rooms needed.

<details><summary>Answer sketches</summary>

**#1:** Sort `(end, index)` tuples; record indices when picking (Striver's variant).

**#2:** Minimum Platforms / LC 253 — sweep or min-heap of end times (problem 11).
</details>

---

## Flashcards

**Activity selection rule?** #flashcard
Sort by end time; take each meeting that starts after the last chosen end.

**Proof technique?** #flashcard
Greedy stays ahead: greedy's k-th finish time is never later than any schedule's k-th finish time.

**Interview track →** [Greedy deep-dive](../../02-algorithms/16-greedy.md) · [Greedy walkthroughs](../../04-practice/algorithms/16-greedy.md)
