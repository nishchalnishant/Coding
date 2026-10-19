---
module: striver/26-heaps
lesson: 17
topic: Minimum cost to connect sticks
difficulty: Medium
source: https://takeuforward.org/learning/dsa/minimum-cost-to-connect-sticks?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, greedy]
---
# 17. Minimum cost to connect sticks

← [Design twitter](16-design-twitter.md) · [Part 26 index](README.md) · Next → [Maximum Sum Combination](18-maximum-sum-combination.md)

> [!abstract] Problem at a glance
> **Task:** Repeatedly join two sticks at a cost equal to their total length until one remains; minimise the total cost.
> **Key insight:** Every stick's length is paid once per join it takes part in, i.e. its depth in the merge tree. To minimise Σ length × depth, the shortest sticks should be deepest. **Always join the two shortest** (Huffman coding), using a min-heap.
> **Difficulty:** Medium · **Pattern:** Greedy min-heap (Huffman) · **Also on:** [LC 1167](https://leetcode.com/problems/minimum-cost-to-connect-sticks/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimum-cost-to-connect-sticks?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 12 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Re-sort every round](#3-re-sort-every-round) · [4. Min-heap greedy](#4-min-heap-greedy) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given positive stick lengths, you may connect any two sticks of lengths `x` and `y` into one of length `x + y` at cost `x + y`. Return the minimum cost to connect all sticks into one.

| Input | Output | Why |
|---|---|---|
| `sticks = [2,4,3]` | `14` | 2+3=5 (5), 5+4=9 (9) |
| `sticks = [1,8,3,5]` | `30` | 1+3, 4+5, 9+8 |
| `sticks = [5]` | `0` |  |

**Constraints:** `1 ≤ n ≤ 10⁴`, `1 ≤ sticks[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Re-sort every round | sort, join two smallest, repeat | O(n² log n) | O(n) |
| Min-heap greedy | pop two smallest, add cost, push sum | O(n log n) | O(n) |

> [!tip] Interview angle
> Give the exchange argument: in an optimal merge tree the two smallest can be made siblings at the deepest level without increasing cost. Then the problem recurses on n − 1 sticks. Note the identical structure to optimal file merge and Huffman codes.

---

## 3. Re-sort every round

**Intuition.** Correct greedy, poor data structure: re-sorting each round.

```python
def connect_sticks_sort(sticks):
    a, cost = list(sticks), 0
    while len(a) > 1:
        a.sort()
        x = a.pop(0) + a.pop(0)
        cost += x
        a.append(x)
    return cost
```

**Complexity:** time **O(n² log n)**, space **O(n)**.

---

## 4. Min-heap greedy

**Intuition.** Heapify all sticks. While more than one remains, pop the two smallest, pay their sum, push the sum back.

**Algorithm**

1. Heapify `sticks`.
2. While size > 1: `x = pop() + pop()`; `cost += x`; push `x`.
3. Return `cost`.

**Dry run** — [1,8,3,5]: 1+3=4 (cost 4) → {4,5,8}; 4+5=9 (13) → {8,9}; 8+9=17 (30).

**C++**
```cpp
int connectSticks(vector<int>& sticks) {
    priority_queue<int, vector<int>, greater<int>> pq(sticks.begin(), sticks.end());
    int cost = 0;
    while (pq.size() > 1) {
        int a = pq.top(); pq.pop();
        int b = pq.top(); pq.pop();
        cost += a + b;
        pq.push(a + b);
    }
    return cost;
}
```

**Java**
```java
static int connectSticks(int[] sticks) {
    PriorityQueue<Integer> pq = new PriorityQueue<>();
    for (int s : sticks) pq.offer(s);
    int cost = 0;
    while (pq.size() > 1) {
        int x = pq.poll() + pq.poll();
        cost += x;
        pq.offer(x);
    }
    return cost;
}
```

**Python**
```python
import heapq
def connect_sticks(sticks):
    h = list(sticks)
    heapq.heapify(h)
    cost = 0
    while len(h) > 1:
        x = heapq.heappop(h) + heapq.heappop(h)
        cost += x
        heapq.heappush(h, x)
    return cost
```

**Complexity:** time **O(n log n)**, space **O(n)** — n − 1 rounds, each O(log n).

---

## Edge cases

- One stick → 0.
- All equal lengths.
- Total cost can exceed `int` for larger constraints: use `long` if the bounds grow.

---

## Common mistakes

1. Joining greedily left-to-right in the given order.
2. Joining the two *largest*.
3. Adding the new stick's length twice (once on creation, once more when it's consumed is correct; the bug is adding the inputs again).

---

## Follow-ups

1. Huffman code lengths?
2. Merge stones with exactly k piles at a time, contiguous only (LC 1000)?

<details><summary>Answer sketches</summary>

**#1:** Same merge tree; a symbol's code length is its leaf depth.

**#2:** Greedy fails: interval DP.
</details>

---

## Flashcards

**Connect sticks greedy?** #flashcard
Always join the two shortest (min-heap) = Huffman.

**Why does Huffman greedy work?** #flashcard
Exchange argument: the two smallest can be deepest siblings without increasing cost.

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
