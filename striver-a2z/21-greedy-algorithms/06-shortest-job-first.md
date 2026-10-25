---
module: striver-a2z/21-greedy-algorithms
lesson: 6
topic: Shortest Job First
difficulty: Easy
source: https://takeuforward.org/learning/dsa/shortest-job-first?category=scheduling-and-interval-problems&source=strivers-a2z-dsa-sheet
tags: [striver, greedy-algorithms, greedy, sorting, scheduling]
---
# 6. Shortest Job First

← [Jump Game I](05-jump-game-i.md) · [Part 21 index](README.md) · Next → [Job Sequencing Problem](07-job-sequencing-problem.md)

> [!abstract] Problem at a glance
> **Task:** All processes arrive at time 0 with burst times `bt`; under non-preemptive SJF return the average waiting time (floored).
> **Key insight:** Running shorter jobs first minimises total waiting time — each job's burst is added to the waiting time of every job after it, so the smallest bursts should be counted most often.
> **Difficulty:** Easy · **Pattern:** Sort ascending; prefix sums
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/shortest-job-first?category=scheduling-and-interval-problems&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Sort + running time](#3-sort--running-time) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given burst times `bt[0…n−1]` of n processes all arriving at time 0, schedule with Shortest Job First (non-preemptive). Return the floor of the average waiting time. A job's waiting time is the time it spends before starting.

| Input | Output | Why |
|---|---|---|
| `bt = [4,3,7,1,2]` | `4` | order 1,2,3,4,7: waits 0,1,3,6,10 → 20/5 |
| `bt = [1,2,3,4]` | `2` | waits 0,1,3,6 → 10/4 = 2.5 |

**Constraints:** `1 ≤ n ≤ 10⁵`, `1 ≤ bt[i] ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Sort + running time | sort; wait += elapsed; elapsed += b | O(n log n) | O(1) extra |

> [!tip] Interview angle
> Expect the scheduling proof: total wait = Σ (n − 1 − k) · b₍ₖ₎ for the k-th job run, so pair the largest multipliers with the smallest bursts (rearrangement inequality).

---

## 3. Sort + running time

**Intuition.** Sort bursts ascending. Keep `t` = time elapsed before the current job starts; that is its waiting time. Sum the waits, then divide by n.

**Dry run** — [1,2,3,4,7]: waits 0, 1, 3, 6, 10 → total 20 → 20 // 5 = 4.

**With different arrival times**, SJF becomes a min-heap simulation (pick the shortest among arrived jobs); preemptive SJF is Shortest Remaining Time First.

**C++**
```cpp
long long solve(vector<int>& bt) {
    sort(bt.begin(), bt.end());
    long long t = 0, wait = 0;
    for (int b : bt) { wait += t; t += b; }
    return wait / (long long)bt.size();
}
```

**Java**
```java
static long solve(int[] bt) {
    Arrays.sort(bt);
    long t = 0, wait = 0;
    for (int b : bt) { wait += t; t += b; }
    return wait / bt.length;
}
```

**Python**
```python
def solve(bt):
    t = wait = 0
    for b in sorted(bt):
        wait += t
        t += b
    return wait // len(bt)
```

**Complexity:** time **O(n log n)**, space **O(1) extra** — sorting dominates.

---

## Edge cases

- One job → 0.
- Total wait can exceed 2³¹ (n = 10⁵, bursts 10⁵) — use 64-bit.

---

## Common mistakes

1. Adding the job's own burst to its waiting time (that's turnaround time).
2. 32-bit overflow of the sum.
3. Rounding instead of flooring.

---

## Follow-ups

1. Jobs arrive at different times.
2. Minimise weighted completion time Σ wᵢCᵢ.

<details><summary>Answer sketches</summary>

**#1:** Min-heap of arrived jobs by burst; jump time forward when idle.

**#2:** Smith's rule: sort by `bᵢ / wᵢ` ascending — same exchange argument.
</details>

---

## Flashcards

**Why does SJF minimise average waiting time?** #flashcard
Each burst delays every later job; smallest bursts should come first (exchange two adjacent jobs to see it).

**Waiting vs turnaround time?** #flashcard
Waiting = start time − arrival; turnaround = completion − arrival = waiting + burst.

**Interview track →** [Greedy deep-dive](../../02-algorithms/16-greedy.md) · [Greedy walkthroughs](../../04-practice/algorithms/16-greedy.md)
