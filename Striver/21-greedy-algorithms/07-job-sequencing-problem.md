---
module: striver/21-greedy-algorithms
lesson: 7
topic: Job Sequencing Problem
difficulty: Medium
source: https://takeuforward.org/learning/dsa/job-sequencing-problem?category=scheduling-and-interval-problems&source=strivers-a2z-dsa-sheet
tags: [striver, greedy-algorithms, greedy, sorting, heap, union-find]
---
# 7. Job Sequencing Problem

← [Shortest Job First](06-shortest-job-first.md) · [Part 21 index](README.md) · Next → [N Meetings in One Room](08-n-meetings-in-one-room.md)

> [!abstract] Problem at a glance
> **Task:** Each job takes 1 unit of time and earns `profit[i]` if finished by `deadline[i]`; return `[jobs done, max profit]`.
> **Key insight:** Take jobs by decreasing profit and schedule each in the **latest** free slot ≤ its deadline, keeping earlier slots open for jobs with tighter deadlines.
> **Difficulty:** Medium · **Pattern:** Sort by profit + latest free slot (or deadline sort + min-heap)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/job-sequencing-problem?category=scheduling-and-interval-problems&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Profit-sorted, latest free slot scan](#3-profit-sorted-latest-free-slot-scan) · [4. DSU: next free slot](#4-dsu-next-free-slot) · [5. Deadline sort + min-heap](#5-deadline-sort--min-heap) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

There are n jobs; job i has a deadline `deadline[i]` and profit `profit[i]`. Each job takes one unit of time, only one job runs at a time, and a job earns its profit only if it finishes by its deadline (it occupies slot `t ∈ [1, deadline]`). Return `[count, totalProfit]` for a schedule maximising profit.

| Input | Output | Why |
|---|---|---|
| `deadline = [4,1,1,1], profit = [20,10,40,30]` | `[2,60]` | 40 in slot 1, 20 in slot 4 |
| `deadline = [2,1,2,1,1], profit = [100,19,27,25,15]` | `[2,127]` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, `1 ≤ deadline[i] ≤ n`, `1 ≤ profit[i] ≤ 500`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Profit-sorted, latest free slot scan | slots[1..maxD]; scan left from deadline | O(n · maxD) | O(maxD) |
| DSU: next free slot | find(d) = latest free slot ≤ d | O(n log n + n α(n)) | O(maxD) |
| Deadline sort + min-heap | keep the best ≤ d jobs in a heap | O(n log n) | O(n) |

> [!tip] Interview angle
> Classic exchange-argument greedy. Give the slot-array version first (easy to explain), then speed it up: DSU "next free slot to the left" or the deadline-sorted min-heap.

---

## 3. Profit-sorted, latest free slot scan

**Intuition.** Sort by profit descending. For each job, walk from `deadline` down to 1 and take the first empty slot. Putting it as late as possible leaves early slots for tight deadlines.

**Dry run** — Profits 40(d1), 30(d1), 20(d4), 10(d1): 40 → slot 1; 30 → none; 20 → slot 4; 10 → none. [2, 60].

```python
def job_seq_slots(deadline, profit):
    jobs = sorted(zip(profit, deadline), reverse=True)
    max_d = max(deadline)
    slot = [False] * (max_d + 1)
    cnt = tot = 0
    for p, d in jobs:
        for t in range(d, 0, -1):
            if not slot[t]:
                slot[t] = True
                cnt += 1; tot += p
                break
    return [cnt, tot]
```

**Complexity:** time **O(n · maxD)**, space **O(maxD)**.

---

## 4. DSU: next free slot

**Intuition.** Same greedy, but replace the leftward scan with union-find: `parent[t]` points to the latest free slot ≤ t. Taking slot t links it to `t − 1`. Slot 0 means "none".

```python
def job_seq_dsu(deadline, profit):
    max_d = max(deadline)
    parent = list(range(max_d + 1))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    cnt = tot = 0
    for p, d in sorted(zip(profit, deadline), reverse=True):
        t = find(d)
        if t:
            parent[t] = t - 1
            cnt += 1; tot += p
    return [cnt, tot]
```

**Complexity:** time **O(n log n + n α(n))**, space **O(maxD)**.

---

## 5. Deadline sort + min-heap

**Intuition.** Process jobs by increasing deadline, pushing profits into a min-heap. The heap holds the jobs currently scheduled; if its size exceeds the current deadline, some job must go — drop the least profitable. Every prefix of deadlines stays feasible.

**Algorithm**

1. Sort jobs by deadline ascending.
2. For each job push its profit; if `heap.size() > deadline`, pop the minimum.
3. Answer: `[heap.size(), sum(heap)]`.

**Dry run** — deadline=[1,1,1,4], profits 10,40,30,20 (sorted by d): push 10; push 40 → size 2 > 1 → pop 10; push 30 → pop 30; push 20 (d 4) → heap {40, 20}. [2, 60].

**C++**
```cpp
vector<int> jobSequencing(vector<int>& deadline, vector<int>& profit) {
    int n = deadline.size();
    vector<int> idx(n);
    iota(idx.begin(), idx.end(), 0);
    sort(idx.begin(), idx.end(), [&](int a, int b) { return deadline[a] < deadline[b]; });
    priority_queue<int, vector<int>, greater<int>> pq;
    for (int i : idx) {
        pq.push(profit[i]);
        if ((int)pq.size() > deadline[i]) pq.pop();
    }
    int cnt = pq.size(), tot = 0;
    while (!pq.empty()) { tot += pq.top(); pq.pop(); }
    return {cnt, tot};
}
```

**Java**
```java
static int[] jobSequencing(int[] deadline, int[] profit) {
    int n = deadline.length;
    Integer[] idx = new Integer[n];
    for (int i = 0; i < n; i++) idx[i] = i;
    Arrays.sort(idx, (a, b) -> deadline[a] - deadline[b]);
    PriorityQueue<Integer> pq = new PriorityQueue<>();
    for (int i : idx) {
        pq.add(profit[i]);
        if (pq.size() > deadline[i]) pq.poll();
    }
    int cnt = pq.size(), tot = 0;
    while (!pq.isEmpty()) tot += pq.poll();
    return new int[]{cnt, tot};
}
```

**Python**
```python
def job_sequencing(deadline, profit):
    heap = []
    for d, p in sorted(zip(deadline, profit)):
        heapq.heappush(heap, p)
        if len(heap) > d:
            heapq.heappop(heap)
    return [len(heap), sum(heap)]
```

**Complexity:** time **O(n log n)**, space **O(n)** — one sort plus n heap operations.

---

## Edge cases

- All deadlines ≥ n → take everything.
- All deadlines = 1 → only the max profit.
- Equal profits — any tie order works.

---

## Common mistakes

1. Placing a job in the **earliest** free slot — blocks tighter deadlines later.
2. Forgetting slot indices start at 1 (deadline d allows slots 1…d).
3. In the heap version, comparing size with `deadline` before pushing.

---

## Follow-ups

1. Jobs have different durations (LC 630 Course Schedule III).
2. Jobs have start/end times and profits (LC 1235).

<details><summary>Answer sketches</summary>

**#1:** Same heap trick on durations: sort by deadline, push durations, while total time > deadline pop the longest.

**#2:** Weighted interval scheduling: sort by end, DP + binary search.
</details>

---

## Flashcards

**Job sequencing greedy?** #flashcard
Highest profit first, placed in the latest free slot ≤ deadline.

**Speed up the slot search?** #flashcard
DSU where `find(t)` is the latest free slot ≤ t; or sort by deadline and keep a size-bounded min-heap.

**Interview track →** [Greedy deep-dive](../../02-algorithms/16-greedy.md) · [Greedy walkthroughs](../../coding/algorithms/16-greedy.md)
