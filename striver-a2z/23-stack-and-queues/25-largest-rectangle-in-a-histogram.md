---
module: striver-a2z/23-stack-and-queues
lesson: 25
topic: Largest rectangle in a histogram
difficulty: Hard
source: https://takeuforward.org/learning/dsa/largest-rectangle-in-a-histogram?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, monotonic-stack, array]
---
# 25. Largest rectangle in a histogram

← [Trapping Rainwater](24-trapping-rainwater.md) · [Part 23 index](README.md) · Next → [Maximum Rectangles](26-maximal-rectangle.md)

> [!abstract] Problem at a glance
> **Task:** Largest rectangle that fits under a histogram.
> **Key insight:** The best rectangle has some bar `i` as its **shortest** bar, and it stretches from just after the previous smaller bar to just before the next smaller one: area `h[i]·(nse − pse − 1)`. In one pass: when a bar is **popped** from an increasing stack, the incoming index is its NSE and the new top is its PSE.
> **Difficulty:** Hard · **Pattern:** Monotonic increasing stack (PSE/NSE) · **Also on:** [LC 84](https://leetcode.com/problems/largest-rectangle-in-histogram/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/largest-rectangle-in-a-histogram?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Expand from each start](#3-expand-from-each-start) · [4. PSE + NSE, two passes](#4-pse--nse-two-passes) · [5. One pass, compute on pop](#5-one-pass-compute-on-pop) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `heights` (bar widths 1), return the area of the largest rectangle in the histogram.

| Input | Output | Why |
|---|---|---|
| `heights = [2,1,5,6,2,3]` | `10` | bars 5 and 6, height 5, width 2 |
| `heights = [2,4]` | `4` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`; `0 ≤ h[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Expand from each start | fix l, extend r, track min height | O(n²) | O(1) |
| PSE + NSE, two passes | width = nse − pse − 1 for each bar | O(n) | O(n) |
| One pass, compute on pop | sentinel 0 at the end; area when a bar is popped | O(n) | O(n) |

> [!tip] Interview angle
> Top-5 stack problem. Explain the 'shortest bar' argument first, then the two-pass PSE/NSE solution, then fold it into one pass with a sentinel height 0 at the end to flush the stack.

---

## 3. Expand from each start

**Intuition.** For each `l`, extend `r` and keep the running minimum; area = `min·(r − l + 1)`.

```python
def lrh_brute(h):
    best = 0
    for l in range(len(h)):
        m = h[l]
        for r in range(l, len(h)):
            m = min(m, h[r])
            best = max(best, m * (r - l + 1))
    return best
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. PSE + NSE, two passes

**Intuition.** Compute the previous and next strictly smaller indices with two monotonic-stack passes (standard NSE/PSE), then take the max of `h[i]·(nse[i] − pse[i] − 1)`.

```python
def lrh_two_pass(h):
    n = len(h)
    pse, nse, st = [-1] * n, [n] * n, []
    for i in range(n):
        while st and h[st[-1]] >= h[i]:
            st.pop()
        if st:
            pse[i] = st[-1]
        st.append(i)
    st = []
    for i in range(n - 1, -1, -1):
        while st and h[st[-1]] >= h[i]:
            st.pop()
        if st:
            nse[i] = st[-1]
        st.append(i)
    return max(h[i] * (nse[i] - pse[i] - 1) for i in range(n))
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 5. One pass, compute on pop

**Intuition.** Keep an increasing stack of indices. When `h[i]` is ≤ the top's height, the top's rectangle can't extend to `i`, so `i` is its right boundary and the element below it on the stack is its left boundary. A virtual bar of height 0 at index `n` flushes everything left.

**Algorithm**

1. For `i` in `0…n` with `cur = 0` if `i == n` else `h[i]`:
2. While stack non-empty and `h[top] ≥ cur`: pop `t`; `left = new top or −1`; `best = max(best, h[t]·(i − left − 1))`.
3. Push `i`.

**Dry run** — [2,1,5,6,2,3]: i1 pops 2 → 2·1. i4 (2) pops 6 → 6·1, pops 5 → 5·2 = 10. i6 (sentinel) pops 3 → 3, 2 → 2·4 = 8, 1 → 1·6. Best 10.

**C++**
```cpp
int largestRectangleArea(vector<int> h) {
    int n = h.size(), best = 0;
    vector<int> st;
    for (int i = 0; i <= n; i++) {
        int cur = i == n ? 0 : h[i];
        while (!st.empty() && h[st.back()] >= cur) {
            int t = st.back(); st.pop_back();
            int left = st.empty() ? -1 : st.back();
            best = max(best, h[t] * (i - left - 1));
        }
        st.push_back(i);
    }
    return best;
}
```

**Java**
```java
static int largestRectangleArea(int[] h) {
    int n = h.length, best = 0;
    Deque<Integer> st = new ArrayDeque<>();
    for (int i = 0; i <= n; i++) {
        int cur = i == n ? 0 : h[i];
        while (!st.isEmpty() && h[st.peek()] >= cur) {
            int t = st.pop();
            int left = st.isEmpty() ? -1 : st.peek();
            best = Math.max(best, h[t] * (i - left - 1));
        }
        st.push(i);
    }
    return best;
}
```

**Python**
```python
def largest_rectangle_area(h):
    n, best, st = len(h), 0, []
    for i in range(n + 1):
        cur = 0 if i == n else h[i]
        while st and h[st[-1]] >= cur:
            t = st.pop()
            left = st[-1] if st else -1
            best = max(best, h[t] * (i - left - 1))
        st.append(i)
    return best
```

**Complexity:** time **O(n)**, space **O(n)** — each index pushed and popped once.

---

## Edge cases

- All equal: n·h.
- Increasing heights: everything resolved by the sentinel.
- Zero-height bars split the histogram.

---

## Common mistakes

1. Forgetting the sentinel, which leaves bars on the stack unprocessed.
2. Width `i − t` instead of `i − left − 1`: the rectangle extends left past `t` to the previous smaller bar.
3. Popping on `>` only: still correct here (equal bars get resolved by the last one), but mixing conventions with the two-pass version causes bugs.

---

## Follow-ups

1. Maximal rectangle of 1s in a matrix?
2. Count rectangles / sum of minimums?

<details><summary>Answer sketches</summary>

**#1:** Build histogram heights row by row and run this per row (next problem).

**#2:** Same PSE/NSE machinery: contribution technique.
</details>

---

## Flashcards

**Largest rectangle with bar i as the shortest?** #flashcard
h[i] · (NSE[i] − PSE[i] − 1).

**One-pass histogram: when is a bar's area computed?** #flashcard
When it's popped; incoming index = right boundary, new top = left boundary.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
