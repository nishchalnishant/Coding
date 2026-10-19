---
module: striver/10-basic-hashing
lesson: 3
topic: Sum of Highest and Lowest Frequency
difficulty: Easy
source: https://takeuforward.org/learning/dsa/sum-of-highest-and-lowest-frequency?category=basic-hashing&source=strivers-a2z-dsa-sheet
tags: [striver, basic-hashing, hashing, frequency]
---
# 3. Sum of Highest and Lowest Frequency

← [Second Highest Occurring Element](02-second-highest-occurring-element.md) · [Part 10 index](README.md) · Next → [Part 11: Basic Strings](../11-basic-strings/README.md)

> [!abstract] Problem at a glance
> **Task:** Return `max frequency + min frequency` over the distinct elements of `nums`.
> **Key insight:** After counting, only the frequency values matter, so take the max and min of `freq.values()`.
> **Difficulty:** Easy · **Pattern:** Frequency map + min/max
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/sum-of-highest-and-lowest-frequency?category=basic-hashing&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — count with nested loops](#3-brute--count-with-nested-loops) · [4. Optimal — map, then min/max](#4-optimal--map-then-minmax) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `nums`, let `F` be the multiset of frequencies of its distinct elements. Return `max(F) + min(F)`.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 2, 3, 3, 3]` | `4` | 3 + 1 |
| `nums = [4, 4, 5, 5, 6]` | `3` | 2 + 1 |
| `nums = [7, 7, 7]` | `6` | only one element: 3 + 3 |

**Constraints:** `1 ≤ n ≤ 10⁵`, `1 ≤ nums[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — count with nested loops | count each distinct value by rescanning | O(n²) | O(k) |
| Optimal — map, then min/max | one count pass + one scan | O(n) | O(k) |

---

## 3. Brute — count with nested loops

**Intuition.** For each distinct value, rescan the array to count it. Track the min and max counts.

```python
def sum_hi_lo_brute(nums):
    seen, hi, lo = set(), 0, float("inf")
    for x in nums:
        if x in seen:
            continue
        seen.add(x)
        f = nums.count(x)
        hi, lo = max(hi, f), min(lo, f)
    return hi + lo
```

**Complexity:** time **O(n²)**, space **O(k)**.

---

## 4. Optimal — map, then min/max

**Intuition.** Count once, then compute the max and min over the counts in the same scan.

**Algorithm**

1. Count frequencies.
2. `hi = 0`, `lo = n`; for each count `f`: `hi = max(hi, f)`, `lo = min(lo, f)`.
3. Return `hi + lo`.

**Dry run** — `[1, 2, 2, 3, 3, 3]` → counts 1, 2, 3 → hi 3, lo 1 → **4**.

**C++**
```cpp
int sumHighestAndLowestFrequency(vector<int>& nums) {
    unordered_map<int, int> freq;
    for (int x : nums) freq[x]++;
    int hi = 0, lo = (int)nums.size();
    for (auto& [x, f] : freq) { hi = max(hi, f); lo = min(lo, f); }
    return hi + lo;
}
```

**Java**
```java
static int sumHighestAndLowestFrequency(int[] nums) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int x : nums) freq.merge(x, 1, Integer::sum);
    int hi = 0, lo = nums.length;
    for (int f : freq.values()) { hi = Math.max(hi, f); lo = Math.min(lo, f); }
    return hi + lo;
}
```

**Python**
```python
from collections import Counter

def sum_highest_lowest_freq(nums):
    fs = Counter(nums).values()
    return max(fs) + min(fs)
```

**Complexity:** time **O(n)**, space **O(k)**.

---

## Edge cases

- One distinct element → `2 · n`, since it is both the highest and the lowest.
- All distinct → `1 + 1 = 2`.

---

## Common mistakes

1. Initialising `lo = 0`, so the min never updates.
2. Returning elements instead of frequencies.

---

## Follow-ups

1. Difference between the highest and lowest frequency.
2. Minimum deletions to make all frequencies unique (LC 1647).

<details><summary>Answer sketches</summary>

**#1:** `max(F) − min(F)`.

**#2:** Sort the frequencies descending; greedily lower each to `min(f, prev − 1)` (floored at 0) and sum the reductions.
</details>

---

## Flashcards

**Init for min-frequency tracking?** #flashcard
n (or ∞). Any real frequency is ≤ n.

**Highest + lowest freq when there's one distinct value?** #flashcard
2n.

**Interview track →** [Hashing deep-dive](../../01-data-structures/02-hashing.md) · [Concept: basic hashing](../07-concept-basics/03-basic-hashing.md)
