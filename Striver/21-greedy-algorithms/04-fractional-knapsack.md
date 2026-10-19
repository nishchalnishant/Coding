---
module: striver/21-greedy-algorithms
lesson: 4
topic: Fractional Knapsack
difficulty: Medium
source: https://takeuforward.org/learning/dsa/fractional-knapsack?category=easy&source=strivers-a2z-dsa-sheet
tags: [striver, greedy-algorithms, greedy, sorting, knapsack]
---
# 4. Fractional Knapsack

← [Lemonade Change](03-lemonade-change.md) · [Part 21 index](README.md) · Next → [Jump Game I](05-jump-game-i.md)

> [!abstract] Problem at a glance
> **Task:** Maximise total value in a knapsack of capacity `W` when items can be taken fractionally.
> **Key insight:** Sort by value per unit weight (`v / w`) descending and take as much as possible of the best ratio. Fractions make the greedy optimal; for 0/1 knapsack it is not (use DP).
> **Difficulty:** Medium · **Pattern:** Sort by ratio
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/fractional-knapsack?category=easy&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Sort by ratio, fill greedily](#3-sort-by-ratio-fill-greedily) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `val[i]` and `wt[i]` for n items and capacity `W`, you may take any fraction of an item (getting the same fraction of its value). Return the maximum total value, accurate to 1e-6.

| Input | Output | Why |
|---|---|---|
| `val = [60,100,120], wt = [10,20,30], W = 50` | `240.00000` | all of 1, 2 and 20/30 of 3 |
| `val = [60,100], wt = [10,20], W = 50` | `160.00000` | everything fits |

**Constraints:** `1 ≤ n ≤ 10⁵`, `1 ≤ val[i], wt[i] ≤ 10⁴`, `1 ≤ W ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Sort by ratio, fill greedily | best v/w first; last item fractional | O(n log n) | O(n) |

> [!tip] Interview angle
> The classic contrast with 0/1 knapsack. Expect: "why is greedy optimal here but not there?" Answer: any unit of capacity spent on a lower ratio can be swapped for a unit of a higher ratio (exchange), and fractions make the swap always possible.

---

## 3. Sort by ratio, fill greedily

**Intuition.** Each unit of capacity is worth at most the best remaining ratio. Take items in decreasing ratio order — whole while they fit, then the fraction `W_left / w` of the first one that doesn't.

**Algorithm**

1. Order item indices by `val[i] / wt[i]` descending.
2. For each: if `wt ≤ W`, take it whole (`W −= wt`, `ans += val`).
3. Otherwise `ans += val · W / wt` and stop.

**Dry run** — Ratios 6, 5, 4. Take 60 (W 40), 100 (W 20), then 20/30 × 120 = 80. Total 240.

**Avoid floating ratios in the comparator** if you want exactness: compare `v1 · w2 > v2 · w1` (fits in 64-bit for these bounds). O(n) is possible with weighted-median selection, but nobody expects it.

**C++**
```cpp
double fractionalKnapsack(vector<int>& val, vector<int>& wt, int W) {
    int n = val.size();
    vector<int> idx(n);
    iota(idx.begin(), idx.end(), 0);
    sort(idx.begin(), idx.end(), [&](int a, int b) {
        return (long long)val[a] * wt[b] > (long long)val[b] * wt[a];
    });
    double ans = 0;
    long long cap = W;
    for (int i : idx) {
        if (wt[i] <= cap) { ans += val[i]; cap -= wt[i]; }
        else { ans += (double)val[i] * cap / wt[i]; break; }
    }
    return ans;
}
```

**Java**
```java
static double fractionalKnapsack(int[] val, int[] wt, int W) {
    int n = val.length;
    Integer[] idx = new Integer[n];
    for (int i = 0; i < n; i++) idx[i] = i;
    Arrays.sort(idx, (a, b) -> Long.compare((long) val[b] * wt[a], (long) val[a] * wt[b]));
    double ans = 0;
    long cap = W;
    for (int i : idx) {
        if (wt[i] <= cap) { ans += val[i]; cap -= wt[i]; }
        else { ans += (double) val[i] * cap / wt[i]; break; }
    }
    return ans;
}
```

**Python**
```python
def fractional_knapsack(val, wt, W):
    items = sorted(zip(val, wt), key=lambda x: x[0] / x[1], reverse=True)
    ans = 0.0
    for v, w in items:
        if w <= W:
            ans += v; W -= w
        else:
            ans += v * W / w
            break
    return ans
```

**Complexity:** time **O(n log n)**, space **O(n)** — sorting dominates; one linear fill pass.

---

## Edge cases

- Capacity exceeds total weight → sum of all values.
- Ties in ratio → order doesn't matter.
- Capacity smaller than every item → fraction of the best-ratio item.

---

## Common mistakes

1. Sorting by value or by weight instead of by ratio.
2. Integer division when computing the fraction.
3. Applying this greedy to 0/1 knapsack.

---

## Follow-ups

1. 0/1 knapsack.
2. Unbounded supply of each item, fractional.

<details><summary>Answer sketches</summary>

**#1:** DP over capacity: O(n·W) — Part 28.

**#2:** Fill everything with the single best-ratio item: `W · max(v/w)`.
</details>

---

## Flashcards

**Fractional knapsack greedy?** #flashcard
Sort by `v/w` descending; take whole items, then a fraction of the first that doesn't fit.

**Why doesn't it work for 0/1 knapsack?** #flashcard
Without fractions a high-ratio item can leave unusable leftover capacity: val=[60,100,120], wt=[10,20,30], W=50 → greedy 160, optimal 220.

**Interview track →** [Greedy deep-dive](../../02-algorithms/16-greedy.md) · [Greedy walkthroughs](../../coding/algorithms/16-greedy.md)
