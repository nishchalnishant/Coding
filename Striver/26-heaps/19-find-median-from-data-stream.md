---
module: striver/26-heaps
lesson: 19
topic: Find Median from Data Stream
difficulty: Hard
source: https://takeuforward.org/learning/dsa/find-median-from-data-stream?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, design, two-heaps]
---
# 19. Find Median from Data Stream

← [Maximum Sum Combination](18-maximum-sum-combination.md) · [Part 26 index](README.md) · Next → [Top K Frequent Elements](20-top-k-frequent-elements.md)

> [!abstract] Problem at a glance
> **Task:** Design `addNum(x)` and `findMedian()` over a growing stream.
> **Key insight:** Split the numbers into a **low half (max-heap)** and a **high half (min-heap)**, with every low ≤ every high and sizes equal or low larger by one. The median is `low.top()` or the average of both tops. Each insert is O(log n) and each query O(1).
> **Difficulty:** Hard · **Pattern:** Two heaps · **Also on:** [LC 295](https://leetcode.com/problems/find-median-from-data-stream/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-median-from-data-stream?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Sorted list (insort)](#3-sorted-list-insort) · [4. Two heaps](#4-two-heaps) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Implement `MedianFinder`: `addNum(int num)` adds a number; `double findMedian()` returns the median of all numbers so far (mean of the two middle values when the count is even).

| Input | Output | Why |
|---|---|---|
| `addNum 1, addNum 2, findMedian, addNum 3, findMedian` | `1.5, 2.0` |  |

**Constraints:** `−10⁵ ≤ num ≤ 10⁵`, up to `5·10⁴` calls; `findMedian` is called on a non-empty stream.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Sorted list (insort) | binary-search insert; index the middle | add O(n), median O(1) | O(n) |
| Two heaps | low = max-heap, high = min-heap; |low| − |high| ∈ {0, 1} | add O(log n), median O(1) | O(n) |

> [!tip] Interview angle
> Write the insert as 'push to low, move low's top to high, rebalance if high got bigger'. Those three lines maintain both invariants without case analysis. Follow-ups: values in [0,100] → counting array; sliding-window median → two heaps with lazy deletion or two multisets.

---

## 3. Sorted list (insort)

**Intuition.** `bisect.insort` keeps the list sorted; the median is read by index. Inserting shifts O(n) elements.

```python
import bisect
class MedianFinderSorted:
    def __init__(self):
        self.a = []
    def addNum(self, x):
        bisect.insort(self.a, x)
    def findMedian(self):
        a, n = self.a, len(self.a)
        return float(a[n // 2]) if n % 2 else (a[n // 2 - 1] + a[n // 2]) / 2
```

**Complexity:** time **add O(n), median O(1)**, space **O(n)**.

---

## 4. Two heaps

**Intuition.** Push into `low`, then move `low`'s max to `high`. That guarantees max(low) ≤ min(high). If `high` is now larger, move its min back. The sizes end up equal or low has one extra.

**Algorithm**

1. `low.push(x)`; `high.push(low.pop())`.
2. If `high.size() > low.size()`: `low.push(high.pop())`.
3. Median: odd count → `low.top()`; even → `(low.top() + high.top()) / 2.0`.

**Dry run** — add 1: low {1}. add 2: low {2,1} → move 2 → high {2}; sizes 1/1. median (1+2)/2 = 1.5. add 3: low {3,1} → move 3 → high {2,3} → bigger → move 2 back → low {2,1}. median 2.0.

**C++**
```cpp
class MedianFinder {
    priority_queue<int> low;                                  // max-heap
    priority_queue<int, vector<int>, greater<int>> high;      // min-heap
public:
    void addNum(int x) {
        low.push(x);
        high.push(low.top()); low.pop();
        if (high.size() > low.size()) { low.push(high.top()); high.pop(); }
    }
    double findMedian() {
        if (low.size() > high.size()) return low.top();
        return ((double)low.top() + high.top()) / 2.0;
    }
};
```

**Java**
```java
static class MedianFinder {
    private final PriorityQueue<Integer> low = new PriorityQueue<>(Collections.reverseOrder());
    private final PriorityQueue<Integer> high = new PriorityQueue<>();
    void addNum(int x) {
        low.offer(x);
        high.offer(low.poll());
        if (high.size() > low.size()) low.offer(high.poll());
    }
    double findMedian() {
        if (low.size() > high.size()) return low.peek();
        return ((double) low.peek() + high.peek()) / 2.0;
    }
}
```

**Python**
```python
import heapq
class MedianFinder:
    def __init__(self):
        self.low, self.high = [], []          # low: max-heap via negation
    def addNum(self, x):
        heapq.heappush(self.low, -x)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))
    def findMedian(self):
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2
```

**Complexity:** time **add O(log n), median O(1)**, space **O(n)** — each add does ≤ 3 heap operations; the median reads two tops.

---

## Edge cases

- Single element.
- Even count: average as floating point, not integer division.
- Negative numbers and duplicates.

---

## Common mistakes

1. Integer division for the even case (`(a + b) / 2` in C++/Java).
2. Rebalancing by size only, without first routing through the other heap, which can break low ≤ high.
3. Overflow in `a + b` for wide ranges: cast to double/long first.

---

## Follow-ups

1. All numbers in [0, 100]?
2. Sliding window median (LC 480)?

<details><summary>Answer sketches</summary>

**#1:** Counting array of 101 buckets; the median is a prefix-count walk, O(100).

**#2:** Two heaps with lazy deletion (a hash map of pending removals), or two multisets with iterator erase.
</details>

---

## Flashcards

**Median of stream structure?** #flashcard
Max-heap for the low half, min-heap for the high half; sizes differ ≤ 1.

**Two-heap insert recipe?** #flashcard
Push to low, move low.top to high, move back if high is bigger.

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
