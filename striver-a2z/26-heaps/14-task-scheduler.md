---
module: striver-a2z/26-heaps
lesson: 14
topic: Task Scheduler
difficulty: Medium
source: https://takeuforward.org/learning/dsa/task-scheduler?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, greedy, counting]
---
# 14. Task Scheduler

← [Replace elements by its rank in the array](13-replace-elements-by-rank.md) · [Part 26 index](README.md) · Next → [Hand of Straights](15-hand-of-straights.md)

> [!abstract] Problem at a glance
> **Task:** Minimum number of CPU intervals to run all tasks when two runs of the same task must be at least `n` intervals apart (idle allowed).
> **Key insight:** Only the **most frequent** task forces idling. With max frequency `f` and `m` tasks sharing it, the frame is `f − 1` blocks of length `n + 1`, plus a final block of `m`. Other tasks fill the gaps. If they overflow the gaps there's no idling at all. Answer: `max(len(tasks), (f−1)(n+1) + m)`.
> **Difficulty:** Medium · **Pattern:** Greedy by frequency (max-heap) → counting formula · **Also on:** [LC 621](https://leetcode.com/problems/task-scheduler/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/task-scheduler?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Max-heap + cooldown queue](#3-max-heap--cooldown-queue) · [4. Counting formula](#4-counting-formula) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `tasks` (uppercase letters) and a cooldown `n`, each interval runs one task or idles. Identical tasks must be separated by at least `n` intervals. Return the minimum number of intervals.

| Input | Output | Why |
|---|---|---|
| `tasks = ["A","A","A","B","B","B"], n = 2` | `8` | A B _ A B _ A B |
| `tasks = ["A","C","A","B","D","B"], n = 1` | `6` | no idling needed |

**Constraints:** `1 ≤ tasks.length ≤ 10⁴`, `0 ≤ n ≤ 100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Max-heap + cooldown queue | run the most-remaining ready task; park it until time + n | O(T log 26) | O(26) |
| Counting formula | max(T, (f−1)(n+1) + #tasks with freq f) | O(T) | O(26) |

> [!tip] Interview angle
> Lead with the heap simulation (it's the general technique: always run the most-remaining available task), then derive the formula from its structure. Explain why the `max` with `len(tasks)` is needed: when gaps overflow, frames just stretch and nothing idles.

---

## 3. Max-heap + cooldown queue

**Intuition.** Each tick: pop the task with the most remaining count from the max-heap, run it, and if it still has copies park `(ready_time, count)` in a FIFO queue. When the front of the queue becomes ready, push it back. If the heap is empty, the CPU idles (jump the clock to the next ready time).

```python
import heapq
from collections import Counter, deque
def least_interval_heap(tasks, n):
    h = [-c for c in Counter(tasks).values()]
    heapq.heapify(h)
    q, t = deque(), 0                       # q: (ready_time, -remaining)
    while h or q:
        t += 1
        if h:
            c = heapq.heappop(h) + 1
            if c:
                q.append((t + n, c))
        else:
            t = q[0][0]                     # idle until the next task is ready
        if q and q[0][0] == t:
            heapq.heappush(h, q.popleft()[1])
    return t
```

**Complexity:** time **O(T log 26)**, space **O(26)**.

---

## 4. Counting formula

**Intuition.** Lay out the most frequent task(s) first: `f − 1` frames of `n + 1` slots, then a last partial frame holding the `m` max-frequency tasks. Fill the remaining slots with other tasks; each has frequency ≤ f − 1 (or = f and is counted in m), so it never collides with itself. If tasks overflow the slots, add them to frames without any idle: the answer is just T.

**Algorithm**

1. Count frequencies; `f` = max, `m` = number of tasks with count `f`.
2. `frame = (f − 1)(n + 1) + m`.
3. Return `max(len(tasks), frame)`.

**Dry run** — AAABBB, n=2: f=3, m=2 → (2)(3)+2 = 8 ≥ 6 → 8. ACABDB, n=1: f=2, m=2 → 1·2+2 = 4 < 6 → 6.

**C++**
```cpp
int leastInterval(vector<char>& tasks, int n) {
    int cnt[26] = {0}, f = 0, m = 0;
    for (char c : tasks) f = max(f, ++cnt[c - 'A']);
    for (int x : cnt) if (x == f) m++;
    return max((int)tasks.size(), (f - 1) * (n + 1) + m);
}
```

**Java**
```java
static int leastInterval(char[] tasks, int n) {
    int[] cnt = new int[26];
    int f = 0, m = 0;
    for (char c : tasks) f = Math.max(f, ++cnt[c - 'A']);
    for (int x : cnt) if (x == f) m++;
    return Math.max(tasks.length, (f - 1) * (n + 1) + m);
}
```

**Python**
```python
from collections import Counter
def least_interval(tasks, n):
    cnt = Counter(tasks).values()
    f = max(cnt)
    m = sum(1 for c in cnt if c == f)
    return max(len(tasks), (f - 1) * (n + 1) + m)
```

**Complexity:** time **O(T)**, space **O(26)** — one counting pass over T tasks; 26 buckets.

---

## Edge cases

- n = 0 → answer = T.
- One task type with many copies: `(f−1)(n+1) + 1`.
- Many distinct tasks: no idle, answer T.

---

## Common mistakes

1. Forgetting the `max(T, …)`: the frame undercounts when tasks overflow the gaps.
2. Counting only one max-frequency task (`+1` instead of `+m`).
3. Simulating tick by tick without jumping the clock across idle stretches: still correct, just slower.

---

## Follow-ups

1. Return an actual schedule?
2. Task order is fixed (LC 2365)?

<details><summary>Answer sketches</summary>

**#1:** Use the heap simulation and record the task (or idle) each tick.

**#2:** No reordering: track `next_allowed[task]` and jump the clock; O(T) with a hash map.
</details>

---

## Flashcards

**Task scheduler formula?** #flashcard
`max(T, (f−1)(n+1) + m)`, f = max freq, m = number of tasks with freq f.

**Task scheduler greedy?** #flashcard
Always run the available task with the most copies left (max-heap + cooldown queue).

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
