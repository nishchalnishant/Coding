---
module: striver/22-sliding-window-and-2-pointer
lesson: 2
topic: Maximum Points You Can Obtain from Cards
difficulty: Medium
source: https://takeuforward.org/learning/dsa/maximum-points-you-can-obtain-from-cards-?category=constant-window&source=strivers-a2z-dsa-sheet
tags: [striver, sliding-window-and-2-pointer, sliding-window, prefix-sum, fixed-window]
---
# 2. Maximum Points You Can Obtain from Cards

← [Sliding Window & Two Pointers: Patterns and Templates](01-sliding-window-theory.md) · [Part 22 index](README.md) · Next → [Longest Substring Without Repeating Characters](03-longest-substring-without-repeating-characters.md)

> [!abstract] Problem at a glance
> **Task:** Take exactly `k` cards, each from the left or right end of the row, and maximise the total points.
> **Key insight:** Whatever you take, the cards you leave form one contiguous block of length `n − k`. So try every split of `i` cards from the left and `k − i` from the right with a fixed-size window that slides around the ends. The equivalent view: minimise the sum of a middle window of size `n − k`.
> **Difficulty:** Medium · **Pattern:** Fixed-size window (wraps around the ends) · **Also on:** [LC 1423](https://leetcode.com/problems/maximum-points-you-can-obtain-from-cards/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/maximum-points-you-can-obtain-from-cards-?category=constant-window&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force: recursion on both ends](#3-brute-force-recursion-on-both-ends) · [4. Slide the split](#4-slide-the-split) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Cards are in a row with points `cardPoints[i]`. In one step you take a card from the beginning or the end of the row. You take exactly `k` cards. Return the maximum score.

| Input | Output | Why |
|---|---|---|
| `cardPoints = [1,2,3,4,5,6,1], k = 3` | `12` | take the three rightmost cards: 1 + 6 + 5 |
| `cardPoints = [9,7,7,9,7,7,9], k = 7` | `55` | take everything |

**Constraints:** `1 ≤ cardPoints.length ≤ 10⁵`, `1 ≤ cardPoints[i] ≤ 10⁴`, `1 ≤ k ≤ cardPoints.length`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force: recursion on both ends | try left or right at each step | O(2^k) | O(k) |
| Slide the split | start with k left cards, swap one left for one right k times | O(k) | O(1) |

> [!tip] Interview angle
> Candidates often start a recursion of left/right choices (2^k). The interviewer wants the observation that the choices collapse to `k + 1` splits. Either form (slide the split, or minimise the middle window) is fine; say which and why.

---

## 3. Brute force: recursion on both ends

**Intuition.** At each step take the left card or the right card and recurse. Correct, but exponential, and it recomputes the same `(l, r)` states that differ only in order.

```python
def max_score_brute(card_points, k):
    def go(l, r, left):
        if left == 0:
            return 0
        return max(card_points[l] + go(l + 1, r, left - 1),
                   card_points[r] + go(l, r - 1, left - 1))
    return go(0, len(card_points) - 1, k)
```

**Complexity:** time **O(2^k)**, space **O(k)**.

---

## 4. Slide the split

**Intuition.** Start with the first `k` cards from the left. Then, `k` times, give back the innermost left card and take the next card from the right end. Track the best total. Every legal choice is one of these `k + 1` splits.

**Algorithm**

1. `lsum = sum(cardPoints[0..k-1])`, `rsum = 0`, `best = lsum`.
2. For `i = k-1` down to `0`: `lsum -= cardPoints[i]`, `rsum += cardPoints[n-k+i]`, `best = max(best, lsum + rsum)`.
3. Return `best`.

**Dry run** — [1,2,3,4,5,6,1], k=3: L=6 (1+2+3) → drop 3, take 1: 3+1=4 → drop 2, take 6: 1+7=8 → drop 1, take 5: 0+12=12. Best 12.

**C++**
```cpp
int maxScore(vector<int>& cardPoints, int k) {
    int n = cardPoints.size(), lsum = 0, rsum = 0;
    for (int i = 0; i < k; i++) lsum += cardPoints[i];
    int best = lsum;
    for (int i = k - 1, r = n - 1; i >= 0; i--, r--) {
        lsum -= cardPoints[i];
        rsum += cardPoints[r];
        best = max(best, lsum + rsum);
    }
    return best;
}
```

**Java**
```java
static int maxScore(int[] cardPoints, int k) {
    int n = cardPoints.length, lsum = 0, rsum = 0;
    for (int i = 0; i < k; i++) lsum += cardPoints[i];
    int best = lsum;
    for (int i = k - 1, r = n - 1; i >= 0; i--, r--) {
        lsum -= cardPoints[i];
        rsum += cardPoints[r];
        best = Math.max(best, lsum + rsum);
    }
    return best;
}
```

**Python**
```python
def max_score(card_points, k):
    n = len(card_points)
    lsum, rsum = sum(card_points[:k]), 0
    best = lsum
    for i in range(k - 1, -1, -1):
        lsum -= card_points[i]
        rsum += card_points[n - k + i]
        best = max(best, lsum + rsum)
    return best
```

**Complexity:** time **O(k)**, space **O(1)** — `k` initial adds plus `k` swaps; the right index is `n − k + i`, which counts down from `n − 1` as `i` does.

---

## Edge cases

- `k = n` → sum of everything.
- `k = 1` → max of the two ends.
- Best split takes everything from one side.

---

## Common mistakes

1. Greedily taking the larger end card each step: [1, 1000, 1, 1, 1] style inputs where a small card hides a big one.
2. Off-by-one on the right index: the first right card is `n − 1`, not `n − k`.
3. Treating it as a normal subarray window instead of a window that wraps around the ends.

---

## Follow-ups

1. Cards can only be taken in pairs from the same side.
2. Minimise the sum instead.

<details><summary>Answer sketches</summary>

**#1:** Still enumerate splits, but only even `i`.

**#2:** Same splits, take `min`, or maximise the middle window of size `n − k`.
</details>

---

## Flashcards

**Max Points from Cards key observation?** #flashcard
The untaken cards form one contiguous window of size n − k; enumerate the k + 1 left/right splits.

**Why not greedy on the larger end?** #flashcard
A small end card can hide large cards behind it; greedy can't see past it.

**Interview track →** [Sliding-window deep-dive](../../02-algorithms/04-sliding-window.md) · [Two-pointers deep-dive](../../02-algorithms/03-two-pointers.md) · [Sliding-window walkthroughs](../../coding/algorithms/04-sliding-window.md)
