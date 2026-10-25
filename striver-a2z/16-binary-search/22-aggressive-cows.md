---
module: striver-a2z/16-binary-search
lesson: 22
topic: Aggressive Cows
difficulty: Hard
source: https://takeuforward.org/learning/dsa/aggressive-cows?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, bs-on-answer, greedy]
---
# 22. Aggressive Cows

← [Painter's Partition](21-painters-partition.md) · [Part 16 index](README.md) · Next → [Book Allocation Problem](23-book-allocation-problem.md)

> [!abstract] Problem at a glance
> **Task:** Place `k` cows in stalls (positions given) to **maximise the minimum** distance between any two cows.
> **Key insight:** If a gap `d` is achievable, every smaller gap is too — T…T F…F. Sort stalls, binary search the **last true** `d ∈ [1, max − min]`; the check greedily places each cow at the first stall ≥ previous + d.
> **Difficulty:** Hard · **Pattern:** Binary search on answer — max feasible
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/aggressive-cows?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Try every distance](#3-try-every-distance) · [4. Binary search on distance](#4-binary-search-on-distance) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `n` stall positions (unsorted, distinct) and `k` cows, assign cows to stalls so that the minimum distance between any two cows is as large as possible. Return that maximum possible minimum distance.

| Input | Output | Why |
|---|---|---|
| `stalls = [0, 3, 4, 7, 10, 9], k = 4` | `3` | 0, 3, 7, 10 |
| `stalls = [4, 2, 1, 3, 6], k = 2` | `5` | 1 and 6 |

**Constraints:** `2 ≤ k ≤ n ≤ 10⁵`, `0 ≤ stalls[i] ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Try every distance | d = 1 … max − min, last feasible | O(n log n + n · range) | O(1) |
| Binary search on distance | sort; can_place(d) → ans = d, go right | O(n log n + n log range) | O(1) extra |

> [!tip] Interview angle
> The canonical "max of min" problem. Contrast it with ship packages ("min of max"): there you go left on true; here you go **right** on true. Explain why greedy placement is optimal: putting the first cow at the leftmost stall and each next cow as early as allowed leaves the most room for the rest.

---

## 3. Try every distance

**Intuition.** Same greedy check, scanned upward until it fails.

```python
def aggressive_cows_linear(stalls, k):
    s = sorted(stalls)
    def ok(d):
        cnt, last = 1, s[0]
        for x in s[1:]:
            if x - last >= d:
                cnt, last = cnt + 1, x
        return cnt >= k
    d = 1
    while ok(d + 1):
        d += 1
    return d
```

**Complexity:** time **O(n log n + n · range)**, space **O(1)**.

---

## 4. Binary search on distance

**Intuition.** Sort once. For a candidate `d`, place the first cow at `s[0]`, then scan: whenever a stall is ≥ `d` past the last cow, place one there. Feasible iff we place ≥ `k`. Search the largest feasible `d`.

**Dry run** — sorted `[0 3 4 7 9 10]`, k 4: lo 1 hi 10 mid 5 → 0, 7 → 2 ✗ hi 4; mid 2 → 0 3 7 9 → 4 ✓ lo 3; mid 3 → 0 3 7 10 → 4 ✓ lo 4; mid 4 → 0 4 9 → 3 ✗ hi 3 → 3.

**C++**
```cpp
int aggressiveCows(vector<int>& stalls, int k) {
    sort(stalls.begin(), stalls.end());
    int lo = 1, hi = stalls.back() - stalls[0], ans = 0;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2, cnt = 1, last = stalls[0];
        for (int x : stalls)
            if (x - last >= mid) { cnt++; last = x; }
        if (cnt >= k) { ans = mid; lo = mid + 1; }
        else hi = mid - 1;
    }
    return ans;
}
```

**Java**
```java
static int aggressiveCows(int[] stalls, int k) {
    Arrays.sort(stalls);
    int lo = 1, hi = stalls[stalls.length - 1] - stalls[0], ans = 0;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2, cnt = 1, last = stalls[0];
        for (int x : stalls)
            if (x - last >= mid) { cnt++; last = x; }
        if (cnt >= k) { ans = mid; lo = mid + 1; }
        else hi = mid - 1;
    }
    return ans;
}
```

**Python**
```python
def aggressive_cows(stalls, k):
    s = sorted(stalls)
    def ok(d):
        cnt, last = 1, s[0]
        for x in s[1:]:
            if x - last >= d:
                cnt, last = cnt + 1, x
        return cnt >= k
    lo, hi, ans = 1, s[-1] - s[0], 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if ok(mid):
            ans, lo = mid, mid + 1
        else:
            hi = mid - 1
    return ans
```

**Complexity:** time **O(n log n + n log range)**, space **O(1) extra** — sort, then log(range) greedy checks.

---

## Edge cases

- k = 2 → max − min.
- k = n → smallest adjacent gap.
- Unsorted input — sort first.

---

## Common mistakes

1. Forgetting to sort.
2. Going left on true (that finds the *min* feasible, here always 1).
3. `hi = max` instead of `max − min`.

---

## Follow-ups

1. Return the placement.
2. Positions on a circle.

<details><summary>Answer sketches</summary>

**#1:** Re-run the greedy at the answer.

**#2:** Fix one cow's stall, check the wrap gap too; try each start or use a doubled array.
</details>

---

## Flashcards

**Max-of-min → which direction on true?** #flashcard
Record ans, go right (lo = mid + 1).

**Aggressive cows — check(d)?** #flashcard
Sorted stalls, greedily place each cow at the first stall ≥ last + d; count ≥ k.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
