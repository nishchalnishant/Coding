---
module: striver/10-basic-hashing
lesson: 2
topic: Second Highest Occurring Element
difficulty: Easy
source: https://takeuforward.org/learning/dsa/second-highest-occurring-element?category=basic-hashing&source=strivers-a2z-dsa-sheet
tags: [striver, basic-hashing, hashing, frequency, top-2]
---
# 2. Second Highest Occurring Element

← [Highest Occurring Element in an Array](01-highest-occurring-element-in-an-array.md) · [Part 10 index](README.md) · Next → [Sum of Highest and Lowest Frequency](03-sum-of-highest-and-lowest-frequency.md)

> [!abstract] Problem at a glance
> **Task:** Return the element with the second-highest distinct frequency (smallest on ties), or −1 if there isn't one.
> **Key insight:** Track the top-two distinct frequencies and their best elements in one scan of the map, the same way you'd track first and second largest.
> **Difficulty:** Easy · **Pattern:** Frequency map + top-2
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/second-highest-occurring-element?category=basic-hashing&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — sort distinct frequencies](#3-brute--sort-distinct-frequencies) · [4. Optimal — top-2 scan](#4-optimal--top-2-scan) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `nums`, consider the distinct frequency values. Return the smallest element whose frequency equals the **second-largest** distinct frequency. If all elements share one frequency, return `-1`.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 2, 3, 3, 3]` | `2` | freqs 3 > 2 > 1; second = 2 → element 2 |
| `nums = [4, 4, 5, 5, 6, 7]` | `6` | freqs {2, 1}; second = 1 → min(6, 7) |
| `nums = [10, 9, 7, 7]` | `9` | freqs {2, 1}; elements with 1: 9, 10 → 9 |
| `nums = [1, 1, 2, 2]` | `-1` | only one distinct frequency |

**Constraints:** `1 ≤ n ≤ 10⁵`, `1 ≤ nums[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — sort distinct frequencies | sort the set of freqs, pick index 1 | O(n + k log k) | O(k) |
| Optimal — top-2 scan | maintain (f1, e1), (f2, e2) | O(n) | O(k) |

> [!tip] Interview angle
> Pin down "second highest" first: the second-largest *distinct* frequency, or the second element in sorted order? Striver's version is the distinct-frequency one.

---

## 3. Brute — sort distinct frequencies

**Intuition.** Count, collect the distinct frequencies, sort them descending, take the second, then find the smallest element with it.

```python
from collections import Counter

def second_most_sort(nums):
    freq = Counter(nums)
    fs = sorted(set(freq.values()), reverse=True)
    if len(fs) < 2:
        return -1
    return min(x for x, f in freq.items() if f == fs[1])
```

**Complexity:** time **O(n + k log k)**, space **O(k)**.

---

## 4. Optimal — top-2 scan

**Intuition.** Scan the map once, keeping the top frequency `f1` with its smallest element `e1`, and the runner-up `f2` with `e2`. A new top demotes the old top. Equal frequencies only update the element if it's smaller.

**Algorithm**

1. Count frequencies.
2. `f1 = f2 = 0`, `e1 = e2 = -1`.
3. For each `(x, f)`: if `f > f1` → `(f2, e2) = (f1, e1)`, `(f1, e1) = (f, x)`; elif `f == f1` → `e1 = min(e1, x)`; elif `f > f2` → `(f2, e2) = (f, x)`; elif `f == f2` → `e2 = min(e2, x)`.
4. Return `e2` (−1 if `f2` was never set).

**Dry run** — `[4, 4, 5, 5, 6, 7]` → {4: 2, 5: 2, 6: 1, 7: 1}

| x, f | (f1, e1) | (f2, e2) |
|---|---|---|
| 4, 2 | (2, 4) | (0, -1) |
| 5, 2 | (2, 4) | (0, -1) |
| 6, 1 | (2, 4) | (1, 6) |
| 7, 1 | (2, 4) | (1, 6) |

→ **6**.

**C++**
```cpp
int secondMostFrequentElement(vector<int>& nums) {
    unordered_map<int, int> freq;
    for (int x : nums) freq[x]++;
    int f1 = 0, f2 = 0, e1 = -1, e2 = -1;
    for (auto& [x, f] : freq) {
        if (f > f1) { f2 = f1; e2 = e1; f1 = f; e1 = x; }
        else if (f == f1) e1 = min(e1, x);
        else if (f > f2) { f2 = f; e2 = x; }
        else if (f == f2) e2 = min(e2, x);
    }
    return e2;
}
```

**Java**
```java
static int secondMostFrequentElement(int[] nums) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int x : nums) freq.merge(x, 1, Integer::sum);
    int f1 = 0, f2 = 0, e1 = -1, e2 = -1;
    for (Map.Entry<Integer, Integer> en : freq.entrySet()) {
        int x = en.getKey(), f = en.getValue();
        if (f > f1) { f2 = f1; e2 = e1; f1 = f; e1 = x; }
        else if (f == f1) e1 = Math.min(e1, x);
        else if (f > f2) { f2 = f; e2 = x; }
        else if (f == f2) e2 = Math.min(e2, x);
    }
    return e2;
}
```

**Python**
```python
from collections import Counter

def second_most_frequent(nums):
    f1 = f2 = 0
    e1 = e2 = -1
    for x, f in Counter(nums).items():
        if f > f1:
            f2, e2 = f1, e1
            f1, e1 = f, x
        elif f == f1:
            e1 = min(e1, x)
        elif f > f2:
            f2, e2 = f, x
        elif f == f2:
            e2 = min(e2, x)
    return e2
```

**Complexity:** time **O(n)**, space **O(k)** — one counting pass and one scan over k distinct keys.

---

## Edge cases

- All the same frequency → −1.
- Single element → −1.
- A demoted top with a larger element: `(f1, e1)` moves to second as a whole, so its element comes along.

---

## Common mistakes

1. Updating `e1 = min(e1, x)` when `e1 = −1` initially. The `f > f1` branch fires first (since `f ≥ 1 > 0`), so it's safe, but only because of that ordering.
2. Treating equal-to-top frequencies as second. They are first.
3. Forgetting to demote the old top into second.

---

## Follow-ups

1. k-th highest distinct frequency.
2. Second-largest element in an array (no hashing).

<details><summary>Answer sketches</summary>

**#1:** Collect the distinct frequencies, use quickselect or a heap of size k, then find the smallest element with that frequency.

**#2:** The same top-2 update on the values themselves; see [Part 14](../14-arrays/README.md).
</details>

---

## Flashcards

**Top-2 update when a new max arrives?** #flashcard
Demote: (f2, e2) ← (f1, e1); (f1, e1) ← (f, x).

**Second-highest frequency when all frequencies are equal?** #flashcard
Doesn't exist → −1.

**Interview track →** [Hashing deep-dive](../../01-data-structures/02-hashing.md) · [Concept: basic hashing](../07-concept-basics/03-basic-hashing.md)
