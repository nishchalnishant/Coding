---
module: striver-a2z/16-binary-search
lesson: 17
topic: Koko Eating Bananas
difficulty: Medium
source: https://takeuforward.org/learning/dsa/koko-eating-bananas?category=on-answers&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, bs-on-answer]
---
# 17. Koko Eating Bananas

← [Find the Smallest Divisor](16-smallest-divisor.md) · [Part 16 index](README.md) · Next → [Minimum Days to Make M Bouquets](18-minimum-days-to-make-m-bouquets.md)

> [!abstract] Problem at a glance
> **Task:** Find the minimum eating speed `k` so Koko finishes all piles within `h` hours.
> **Key insight:** Hours needed at speed `k` = `Σ ⌈pile / k⌉`, non-increasing in `k`. Binary search the smallest `k ∈ [1, max(piles)]` with hours ≤ h. Structurally identical to the smallest divisor.
> **Difficulty:** Medium · **Pattern:** Binary search on answer — min feasible · **Also on:** [LC 875](https://leetcode.com/problems/koko-eating-bananas/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/koko-eating-bananas?category=on-answers&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Try every speed](#3-try-every-speed) · [4. Binary search on speed](#4-binary-search-on-speed) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

There are `n` piles of bananas; pile `i` has `piles[i]`. Each hour Koko picks one pile and eats `k` bananas from it (if fewer remain, she eats them all and idles for the rest of the hour). Return the minimum integer `k` that lets her finish within `h` hours.

| Input | Output | Why |
|---|---|---|
| `piles = [3, 6, 7, 11], h = 8` | `4` | 1+2+2+3 = 8 |
| `piles = [30, 11, 23, 4, 20], h = 5` | `30` | one pile per hour |
| `piles = [30, 11, 23, 4, 20], h = 6` | `23` |  |

**Constraints:** `1 ≤ n ≤ 10⁴`, `n ≤ h ≤ 10⁹`, `1 ≤ piles[i] ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Try every speed | k = 1, 2, … until hours ≤ h | O(n · max) | O(1) |
| Binary search on speed | hours(k) ≤ h → ans = k, go left; else go right | O(n log max) | O(1) |

> [!tip] Interview angle
> The flagship BS-on-answer problem at Google-style interviews. State why the upper bound is `max(piles)`: at that speed every pile takes one hour, and going faster can't help. Use 64-bit for the hour sum — `10⁴` piles × `10⁹` hours each overflows int when `k = 1`.

---

## 3. Try every speed

**Intuition.** Correct but up to 10⁹ × 10⁴ operations.

```python
def min_eating_speed_linear(piles, h):
    k = 1
    while sum((p + k - 1) // k for p in piles) > h:
        k += 1
    return k
```

**Complexity:** time **O(n · max)**, space **O(1)**.

---

## 4. Binary search on speed

**Intuition.** Feasibility `hours(k) ≤ h` is monotone in `k`. First true in `[1, max(piles)]`.

**Dry run** — `[3 6 7 11]`, h 8: lo 1 hi 11 mid 6 (1+1+2+2 = 6 ✓) ans 6, hi 5; mid 3 (1+2+3+4 = 10 ✗) lo 4; mid 4 (1+2+2+3 = 8 ✓) ans 4, hi 3 → 4.

**C++**
```cpp
int minEatingSpeed(vector<int>& piles, int h) {
    int lo = 1, hi = *max_element(piles.begin(), piles.end()), ans = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        long long hours = 0;
        for (int p : piles) hours += (p + (long long)mid - 1) / mid;
        if (hours <= h) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Java**
```java
static int minEatingSpeed(int[] piles, int h) {
    int hi = 0;
    for (int p : piles) hi = Math.max(hi, p);
    int lo = 1, ans = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        long hours = 0;
        for (int p : piles) hours += (p + (long) mid - 1) / mid;
        if (hours <= h) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Python**
```python
def min_eating_speed(piles, h):
    lo, hi = 1, max(piles)
    ans = hi
    while lo <= hi:
        mid = (lo + hi) // 2
        if sum((p + mid - 1) // mid for p in piles) <= h:
            ans, hi = mid, mid - 1
        else:
            lo = mid + 1
    return ans
```

**Complexity:** time **O(n log max)**, space **O(1)** — log(max) checks of O(n).

---

## Edge cases

- h = n → max(piles).
- h huge → 1.
- `p + mid − 1` overflows int when p ≈ 10⁹ — cast first.

---

## Common mistakes

1. 32-bit hour counter.
2. `p + mid − 1` overflow in C++/Java.
3. Lower bound 0 → divide by zero.

---

## Follow-ups

1. Koko can switch piles mid-hour.
2. Tighter lower bound.

<details><summary>Answer sketches</summary>

**#1:** Then hours = ⌈Σ piles / k⌉ — direct formula, no search.

**#2:** `⌈Σ piles / h⌉` — saves a few iterations.
</details>

---

## Flashcards

**Koko — search range?** #flashcard
[1, max(piles)].

**Koko — hours at speed k?** #flashcard
Σ ⌈p / k⌉, use 64-bit.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
