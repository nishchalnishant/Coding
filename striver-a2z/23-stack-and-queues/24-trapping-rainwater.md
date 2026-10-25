---
module: striver-a2z/23-stack-and-queues
lesson: 24
topic: Trapping Rainwater
difficulty: Hard
source: https://takeuforward.org/learning/dsa/trapping-rainwater?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, two-pointers, prefix-max, stack]
---
# 24. Trapping Rainwater

← [Sliding Window Maximum](23-sliding-window-maximum.md) · [Part 23 index](README.md) · Next → [Largest rectangle in a histogram](25-largest-rectangle-in-a-histogram.md)

> [!abstract] Problem at a glance
> **Task:** Total water trapped between bars of an elevation map.
> **Key insight:** Water above bar `i` = `min(maxLeft[i], maxRight[i]) − h[i]`. With **two pointers**, move the side with the smaller bar: that side's water is decided by its own running max, because the other side is already known to be at least as tall.
> **Difficulty:** Hard · **Pattern:** Prefix/suffix max → two pointers · **Also on:** [LC 42](https://leetcode.com/problems/trapping-rain-water/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/trapping-rainwater?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Per-bar scans](#3-per-bar-scans) · [4. Prefix and suffix maxima](#4-prefix-and-suffix-maxima) · [5. Two pointers](#5-two-pointers) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given non-negative `height` (bar widths 1), compute how much water is trapped after raining.

| Input | Output | Why |
|---|---|---|
| `height = [0,1,0,2,1,0,1,3,2,1,2,1]` | `6` |  |
| `height = [4,2,0,3,2,5]` | `9` |  |

**Constraints:** `1 ≤ n ≤ 2·10⁴`; `0 ≤ h[i] ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Per-bar scans | for each i, scan left and right for maxima | O(n²) | O(1) |
| Prefix and suffix maxima | precompute maxLeft and maxRight | O(n) | O(n) |
| Two pointers | move the lower side; its running max decides its water | O(n) | O(1) |

> [!tip] Interview angle
> Walk the ladder: brute (per-bar scans) → prefix/suffix arrays → two pointers with O(1) space. The two-pointer proof is what they probe: when `h[l] < h[r]`, there is a bar of height ≥ `h[r] > h[l]` on the right, so bar `l`'s water is limited by `lmax`, never by the right side.

---

## 3. Per-bar scans

**Intuition.** Directly apply the formula, finding both maxima by scanning.

```python
def trap_brute(h):
    total = 0
    for i in range(len(h)):
        total += min(max(h[:i + 1]), max(h[i:])) - h[i]
    return total
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Prefix and suffix maxima

**Intuition.** `maxLeft[i] = max(maxLeft[i−1], h[i])` and `maxRight` symmetrically; then sum the formula.

```python
def trap_prefix(h):
    n = len(h)
    L, R = h[:], h[:]
    for i in range(1, n):
        L[i] = max(L[i - 1], h[i])
    for i in range(n - 2, -1, -1):
        R[i] = max(R[i + 1], h[i])
    return sum(min(L[i], R[i]) - h[i] for i in range(n))
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 5. Two pointers

**Intuition.** Keep `lmax` = max of `h[0..l]` and `rmax` = max of `h[r..n−1]`. If `h[l] < h[r]`, then `maxRight[l] ≥ h[r]`. Also `lmax ≤ h[r]`: the left pointer only advances while its bar is smaller than some right bar, so every bar `lmax` came from was below a right bar. So `min(maxLeft[l], maxRight[l]) = lmax`, and bar `l`'s water is `lmax − h[l]`. The right side is symmetric.

**Algorithm**

1. `l = 0, r = n−1, lmax = rmax = 0, water = 0`.
2. While `l < r`: if `h[l] < h[r]`: `lmax = max(lmax, h[l])`, `water += lmax − h[l]`, `l++`.
3. Else: `rmax = max(rmax, h[r])`, `water += rmax − h[r]`, `r−−`.

**Dry run** — [4,2,0,3,2,5]: h[0]=4 < 5: lmax 4, +0. l1: 2 → +2. l2: 0 → +4. l3: 3 → +1. l4: 2 → +2. Total 9.

**C++**
```cpp
int trap(vector<int> h) {
    int l = 0, r = (int)h.size() - 1, lmax = 0, rmax = 0, water = 0;
    while (l < r) {
        if (h[l] < h[r]) { lmax = max(lmax, h[l]); water += lmax - h[l]; l++; }
        else { rmax = max(rmax, h[r]); water += rmax - h[r]; r--; }
    }
    return water;
}
```

**Java**
```java
static int trap(int[] h) {
    int l = 0, r = h.length - 1, lmax = 0, rmax = 0, water = 0;
    while (l < r) {
        if (h[l] < h[r]) { lmax = Math.max(lmax, h[l]); water += lmax - h[l]; l++; }
        else { rmax = Math.max(rmax, h[r]); water += rmax - h[r]; r--; }
    }
    return water;
}
```

**Python**
```python
def trap(h):
    l, r = 0, len(h) - 1
    lmax = rmax = water = 0
    while l < r:
        if h[l] < h[r]:
            lmax = max(lmax, h[l])
            water += lmax - h[l]
            l += 1
        else:
            rmax = max(rmax, h[r])
            water += rmax - h[r]
            r -= 1
    return water
```

**Complexity:** time **O(n)**, space **O(1)** — each index is visited once by one of the pointers.

---

## Edge cases

- Monotonic heights: 0.
- n < 3: 0.
- Plateaus and equal walls: the `else` branch handles `h[l] == h[r]`.

---

## Common mistakes

1. Forgetting to include `h[i]` itself in maxLeft/maxRight, which gives negative water.
2. Moving the taller side in two pointers.
3. Summing `min(L, R) − h` with L/R excluding i and not clamping at 0.

---

## Follow-ups

1. Stack approach?
2. 2D version (LC 407)?
3. Container with most water (LC 11)?

<details><summary>Answer sketches</summary>

**#1:** Monotonic decreasing stack of indices; when a taller bar arrives, pop the bottom and add `(min(h[left], h[i]) − h[bottom])·(i − left − 1)`. It fills water layer by layer.

**#2:** Min-heap from the border inward (Dijkstra-like).

**#3:** Different problem: two lines only, area `min·width`; also two pointers.
</details>

---

## Flashcards

**Water above bar i?** #flashcard
min(maxLeft[i], maxRight[i]) − h[i], with both maxima including i.

**Trapping rain water two-pointer rule?** #flashcard
Advance the side with the smaller height; add its running max − its height.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
