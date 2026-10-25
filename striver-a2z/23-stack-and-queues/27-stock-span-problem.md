---
module: striver-a2z/23-stack-and-queues
lesson: 27
topic: Stock span problem
difficulty: Medium
source: https://takeuforward.org/learning/dsa/stock-span-problem?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, monotonic-stack, design]
---
# 27. Stock span problem

← [Maximum Rectangles](26-maximal-rectangle.md) · [Part 23 index](README.md) · Next → [The Celebrity Problem](28-celebrity-problem.md)

> [!abstract] Problem at a glance
> **Task:** For each day's price, how many consecutive days (ending today) had price ≤ today's.
> **Key insight:** Span = distance to the **previous greater** price. Online version: keep a stack of `(price, span)` with decreasing prices. When today's price arrives, pop every entry `≤` it and **absorb** their spans; push today's total.
> **Difficulty:** Medium · **Pattern:** Monotonic stack (previous greater), online · **Also on:** [LC 901](https://leetcode.com/problems/online-stock-span/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/stock-span-problem?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Store all prices, walk back](#3-store-all-prices-walk-back) · [4. Stack of (price, span)](#4-stack-of-price-span) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Design `StockSpanner` with `next(price)`, which returns today's span: the maximum number of consecutive days, ending today and going backwards, with price ≤ today's.

| Input | Output | Why |
|---|---|---|
| `next: 100, 80, 60, 70, 60, 75, 85` | `1, 1, 1, 2, 1, 4, 6` |  |

**Constraints:** `1 ≤ price ≤ 10⁵`; up to `10⁴` calls.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Store all prices, walk back | count backwards until a bigger price | O(n) per call | O(n) |
| Stack of (price, span) | pop ≤ price, add their spans | O(1) amortised | O(n) |

> [!tip] Interview angle
> Name it as 'previous greater element, distance form'. The trick for the online version is storing the span with each price so popped days are counted without being stored.

---

## 3. Store all prices, walk back

**Intuition.** Append the price; walk backwards while prices are ≤ today's.

```python
class SlowSpanner:
    def __init__(self):
        self.p = []
    def next(self, price):
        self.p.append(price)
        span, i = 0, len(self.p) - 1
        while i >= 0 and self.p[i] <= price:
            span += 1
            i -= 1
        return span
```

**Complexity:** time **O(n) per call**, space **O(n)**.

---

## 4. Stack of (price, span)

**Intuition.** A day with price ≤ today's is hidden behind today forever: any future query that reaches it must first pass today. So pop it and fold its span into today's. The stack stays strictly decreasing in price.

**Algorithm**

1. `span = 1`.
2. While `st.top.price ≤ price`: `span += st.top.span`, pop.
3. Push `(price, span)`; return `span`.

**Dry run** — 100 → [(100,1)] 1. 80 → 1. 60 → 1. 70 pops (60,1) → 2. 60 → 1. 75 pops (60,1),(70,2) → 4. 85 pops (75,4),(80,1) → 6.

**C++**
```cpp
class StockSpanner {
    vector<pair<int, int>> st;   // {price, span}
public:
    int next(int price) {
        int span = 1;
        while (!st.empty() && st.back().first <= price) { span += st.back().second; st.pop_back(); }
        st.push_back({price, span});
        return span;
    }
};
```

**Java**
```java
static class StockSpanner {
    private final Deque<int[]> st = new ArrayDeque<>();   // {price, span}
    int next(int price) {
        int span = 1;
        while (!st.isEmpty() && st.peek()[0] <= price) span += st.pop()[1];
        st.push(new int[]{price, span});
        return span;
    }
}
```

**Python**
```python
class StockSpanner:
    def __init__(self):
        self.st = []                  # (price, span)
    def next(self, price):
        span = 1
        while self.st and self.st[-1][0] <= price:
            span += self.st.pop()[1]
        self.st.append((price, span))
        return span
```

**Complexity:** time **O(1) amortised**, space **O(n)** — each day is pushed once and popped at most once.

---

## Edge cases

- Equal prices count (≤), so they're popped.
- Strictly increasing prices: span grows by 1 each day.
- Strictly decreasing: always 1.

---

## Common mistakes

1. Using `<` (equal-priced days would not be absorbed).
2. Storing only prices and recomputing spans by index without keeping indices.
3. Forgetting the `+1` for today.

---

## Follow-ups

1. Offline array version?
2. Daily temperatures (LC 739)?

<details><summary>Answer sketches</summary>

**#1:** Previous greater index `pge[i]`; span = `i − pge[i]`.

**#2:** Next greater, distance form.
</details>

---

## Flashcards

**Stock span is which monotonic-stack variant?** #flashcard
Previous greater element, as a distance.

**Online stock span: what does each stack entry store?** #flashcard
(price, span), so popped days are absorbed into the new span.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
