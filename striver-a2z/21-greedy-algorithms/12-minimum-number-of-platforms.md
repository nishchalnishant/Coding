---
module: striver-a2z/21-greedy-algorithms
lesson: 12
topic: Minimum Number of Platforms
difficulty: Medium
source: https://takeuforward.org/learning/dsa/minimum-number-of-platforms-required-for-a-railway?category=scheduling-and-interval-problems&source=strivers-a2z-dsa-sheet
tags: [striver, greedy-algorithms, greedy, sweep-line, intervals]
---
# 12. Minimum Number of Platforms

← [Merge Intervals](11-merge-intervals.md) · [Part 21 index](README.md) · Next → [Valid Parenthesis String](13-valid-parenthesis-string.md)

> [!abstract] Problem at a glance
> **Task:** Given arrival and departure times of trains, return the minimum platforms so no train waits.
> **Key insight:** Answer = maximum number of trains present at the same instant. Sort arrivals and departures separately and sweep: an arrival adds one, a departure frees one.
> **Difficulty:** Medium · **Pattern:** Sweep line over sorted events
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimum-number-of-platforms-required-for-a-railway?category=scheduling-and-interval-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force: overlap count per train](#3-brute-force-overlap-count-per-train) · [4. Sorted events, two pointers](#4-sorted-events-two-pointers) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given arrays `arr` and `dep` (times as HHMM integers) for n trains, return the minimum number of platforms needed so that no train waits. A platform freed at time t **cannot** be reused by a train arriving at t (arrival and departure at the same time need two platforms).

| Input | Output | Why |
|---|---|---|
| `arr = [900,940,950,1100,1500,1800], dep = [910,1200,1120,1130,1900,2000]` | `3` | 940–1120 window holds three trains |
| `arr = [900,1100,1235], dep = [1000,1200,1240]` | `1` |  |

**Constraints:** `1 ≤ n ≤ 5·10⁴`, `0000 ≤ arr[i] ≤ dep[i] ≤ 2359`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force: overlap count per train | for each train count trains overlapping it | O(n²) | O(1) |
| Sorted events, two pointers | if arr[i] ≤ dep[j]: +1 else −1 | O(n log n) | O(1) extra |

> [!tip] Interview angle
> Same as Meeting Rooms II (LC 253). Two clean solutions: separate-sort two pointers, or a min-heap of departure times. Clarify the tie rule — it decides `<=` vs `<`.

---

## 3. Brute force: overlap count per train

**Intuition.** The peak occurs at some arrival time. For each train i, count trains j with `arr[j] ≤ arr[i] ≤ dep[j]`. Take the max.

```python
def platforms_brute(arr, dep):
    best = 0
    for a in arr:
        best = max(best, sum(1 for x, y in zip(arr, dep) if x <= a <= y))
    return best
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Sorted events, two pointers

**Intuition.** Sort both arrays. Merge-scan: whenever the next arrival is **≤** the next departure (tie → the arrival is processed first, so both trains are present), one more platform is in use; otherwise a train leaves. Track the peak.

**Algorithm**

1. Sort `arr` and `dep`.
2. `i = j = cur = best = 0`.
3. While `i < n`: if `arr[i] ≤ dep[j]`: `cur++`, `i++`, `best = max(best, cur)`; else `cur−−`, `j++`.
4. Return `best`.

**Dry run** — arr 900 940 950 1100 1500 1800, dep 910 1120 1130 1200 1900 2000: 900 (1), 910 out (0), 940 (1), 950 (2), 1100 (3), 1120 out (2), …, peak 3.

**Min-heap version:** sort trains by arrival; heap of departures; pop while `top < arrival`; push departure; answer = max heap size. Also works when you must assign platform numbers.

**C++**
```cpp
int findPlatform(vector<int>& arr, vector<int>& dep) {
    sort(arr.begin(), arr.end());
    sort(dep.begin(), dep.end());
    int n = arr.size(), i = 0, j = 0, cur = 0, best = 0;
    while (i < n) {
        if (arr[i] <= dep[j]) { cur++; i++; best = max(best, cur); }
        else { cur--; j++; }
    }
    return best;
}
```

**Java**
```java
static int findPlatform(int[] arr, int[] dep) {
    Arrays.sort(arr);
    Arrays.sort(dep);
    int n = arr.length, i = 0, j = 0, cur = 0, best = 0;
    while (i < n) {
        if (arr[i] <= dep[j]) { cur++; i++; best = Math.max(best, cur); }
        else { cur--; j++; }
    }
    return best;
}
```

**Python**
```python
def find_platform(arr, dep):
    arr, dep = sorted(arr), sorted(dep)
    i = j = cur = best = 0
    while i < len(arr):
        if arr[i] <= dep[j]:
            cur += 1; i += 1
            best = max(best, cur)
        else:
            cur -= 1; j += 1
    return best
```

**Complexity:** time **O(n log n)**, space **O(1) extra** — two sorts plus a linear merge.

---

## Edge cases

- Arrival equal to another train's departure → both on platforms (`≤`).
- Train arriving and departing at the same minute.
- All trains overlap → n.

---

## Common mistakes

1. Using `<` and undercounting at ties.
2. Sorting `(arr, dep)` pairs and sweeping only arrivals.
3. Resetting the count instead of tracking the max.

---

## Follow-ups

1. Departure at t frees the platform for an arrival at t (LC 253).
2. Times can cross midnight.

<details><summary>Answer sketches</summary>

**#1:** Use `arr[i] < dep[j]`.

**#2:** Add 2400 to departures earlier than arrivals, or split the interval.
</details>

---

## Flashcards

**Minimum platforms = ?** #flashcard
Maximum number of trains simultaneously present — sweep sorted arrivals and departures.

**Tie rule for `arr ≤ dep`?** #flashcard
Same-time arrival and departure need two platforms → process arrival first (`≤`).

**Interview track →** [Greedy deep-dive](../../02-algorithms/16-greedy.md) · [Greedy walkthroughs](../../04-practice/algorithms/16-greedy.md)
