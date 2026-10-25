---
module: striver-a2z/10-basic-hashing
lesson: 1
topic: Highest Occurring Element in an Array
difficulty: Easy
source: https://takeuforward.org/learning/dsa/highest-occurring-element-in-an-array?category=basic-hashing&source=strivers-a2z-dsa-sheet
tags: [striver, basic-hashing, hashing, frequency]
---
# 1. Highest Occurring Element in an Array

← [Part 10 index](README.md) · Next → [Second Highest Occurring Element](02-second-highest-occurring-element.md)

> [!abstract] Problem at a glance
> **Task:** Return the element with the highest frequency; on a tie, the smallest such element.
> **Key insight:** Count with a map, then do one scan with the comparison key `(-freq, value)`.
> **Difficulty:** Easy · **Pattern:** Frequency map + argmax
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/highest-occurring-element-in-an-array?category=basic-hashing&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — count each element](#3-brute--count-each-element) · [4. Optimal — frequency map](#4-optimal--frequency-map) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, return the element that occurs most often. If several elements share the maximum frequency, return the smallest of them.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 2, 3, 3, 3]` | `3` | 3 occurs 3× |
| `nums = [4, 4, 5, 5, 6]` | `4` | tie between 4 and 5 → smaller |
| `nums = [10, 9, 7, 7, 8, 8, 9]` | `7` | 7, 8, 9 tie at 2 |

**Constraints:** `1 ≤ n ≤ 10⁵`, `1 ≤ nums[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — count each element | nested loop counts | O(n²) | O(1) |
| Optimal — frequency map | count, then scan entries | O(n) | O(k) distinct |

> [!tip] Interview angle
> Ask about the tie rule before coding. It changes the comparison, and the interviewer is watching whether you clarify.

---

## 3. Brute — count each element

**Intuition.** For each element, count its occurrences with a second loop and keep the best under the tie rule.

```python
def most_frequent_brute(nums):
    best, best_f = None, 0
    for x in nums:
        f = sum(1 for y in nums if y == x)
        if f > best_f or (f == best_f and x < best):
            best, best_f = x, f
    return best
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Optimal — frequency map

**Intuition.** Count everything in one pass, then scan the map once. The tie rule lives in a single comparison.

**Algorithm**

1. `freq[x] += 1` for each `x`.
2. Scan `(x, f)` pairs: take `x` if `f > best_f`, or if `f == best_f and x < best`.
3. Return `best`.

**Dry run** — `[4, 4, 5, 5, 6]` → freq {4: 2, 5: 2, 6: 1}. Scan: 4 (2) best; 5 (2) tie but 5 > 4, keep 4; 6 (1) lower → **4**.

With values bounded by 10⁴, an `int cnt[10001]` array is faster, and scanning it in index order gives the smallest value on ties for free: use `>` only.

**C++**
```cpp
int mostFrequentElement(vector<int>& nums) {
    unordered_map<int, int> freq;
    for (int x : nums) freq[x]++;
    int best = 0, bestF = 0;
    for (auto& [x, f] : freq)
        if (f > bestF || (f == bestF && x < best)) { best = x; bestF = f; }
    return best;
}
```

**Java**
```java
static int mostFrequentElement(int[] nums) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int x : nums) freq.merge(x, 1, Integer::sum);
    int best = 0, bestF = 0;
    for (Map.Entry<Integer, Integer> e : freq.entrySet()) {
        int x = e.getKey(), f = e.getValue();
        if (f > bestF || (f == bestF && x < best)) { best = x; bestF = f; }
    }
    return best;
}
```

**Python**
```python
from collections import Counter

def most_frequent_element(nums):
    freq = Counter(nums)
    best, best_f = None, 0
    for x, f in freq.items():
        if f > best_f or (f == best_f and x < best):
            best, best_f = x, f
    return best
```

**Complexity:** time **O(n)**, space **O(k) distinct**.

---

## Edge cases

- All distinct → the minimum element.
- Single element → itself.
- Hashmap iteration order is arbitrary, so the tie rule must be explicit.

---

## Common mistakes

1. Relying on map iteration order for ties.
2. Python `Counter.most_common(1)` breaks ties by first insertion, not smallest value.
3. Initialising `best_f = 1`, which then can't beat ties correctly when all frequencies are 1.

---

## Follow-ups

1. Top-k frequent elements (LC 347).
2. Majority element (> n/2) in O(1) space.

<details><summary>Answer sketches</summary>

**#1:** Bucket sort by frequency (buckets 1..n), O(n); or a size-k min-heap, O(n log k).

**#2:** Boyer–Moore voting; covered in [Part 14](../14-arrays/README.md).
</details>

---

## Flashcards

**Tie-break comparison for most-frequent-smallest?** #flashcard
`f > best_f or (f == best_f and x < best)`.

**When does an array beat a hashmap for counting?** #flashcard
When the values fall in a small known range; index directly.

**Does Counter.most_common break ties by value?** #flashcard
No. It uses insertion order.

**Interview track →** [Hashing deep-dive](../../01-data-structures/02-hashing.md) · [Concept: basic hashing](../07-concept-basics/03-basic-hashing.md)
