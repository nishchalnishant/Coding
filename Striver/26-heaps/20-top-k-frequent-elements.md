---
module: striver/26-heaps
lesson: 20
topic: Top K Frequent Elements
difficulty: Medium
source: https://takeuforward.org/learning/dsa/top-k-frequent-elements?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, hashing, bucket-sort, top-k]
---
# 20. Top K Frequent Elements

← [Find Median from Data Stream](19-find-median-from-data-stream.md) · [Part 26 index](README.md) · Next → [Part 27: Graphs](../27-graphs/README.md)

> [!abstract] Problem at a glance
> **Task:** Return the `k` most frequent values (any order).
> **Key insight:** Count, then select. A **min-heap of size k keyed by count** gives O(n log k). Better: frequencies lie in `1 … n`, so **bucket sort** by count and read buckets from high to low for O(n).
> **Difficulty:** Medium · **Pattern:** Count + bounded heap / bucket sort · **Also on:** [LC 347](https://leetcode.com/problems/top-k-frequent-elements/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/top-k-frequent-elements?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Sort by count](#3-sort-by-count) · [4. Min-heap of size k](#4-min-heap-of-size-k) · [5. Bucket sort by frequency](#5-bucket-sort-by-frequency) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `nums` and `k`, return the `k` most frequent elements in any order. The answer is guaranteed unique.

| Input | Output | Why |
|---|---|---|
| `nums = [1,1,1,2,2,3], k = 2` | `[1,2]` |  |
| `nums = [1], k = 1` | `[1]` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, `1 ≤ k ≤ number of distinct values`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Sort by count | Counter, sort distinct values by −count | O(n + d log d) | O(d) |
| Min-heap of size k | push (count, value); pop when > k | O(n + d log k) | O(d) |
| Bucket sort by frequency | bucket[count] = values; scan from n down | O(n) | O(n) |

> [!tip] Interview angle
> The follow-up asks you to beat O(n log n). Bucket sort is O(n) because counts are bounded by n. Quickselect on the distinct values by count is O(d) expected. The heap version is the one that survives streaming input.

---

## 3. Sort by count

**Intuition.** Count with a hash map, sort the distinct keys by frequency descending, take the first k.

```python
from collections import Counter
def top_k_sort(nums, k):
    c = Counter(nums)
    return sorted(c, key=lambda x: -c[x])[:k]
```

**Complexity:** time **O(n + d log d)**, space **O(d)**.

---

## 4. Min-heap of size k

**Intuition.** Same as k-th largest, keyed by count: the heap keeps the k highest counts seen.

```python
import heapq
from collections import Counter
def top_k_heap(nums, k):
    h = []
    for v, c in Counter(nums).items():
        heapq.heappush(h, (c, v))
        if len(h) > k:
            heapq.heappop(h)
    return [v for _, v in h]
```

**Complexity:** time **O(n + d log k)**, space **O(d)**.

---

## 5. Bucket sort by frequency

**Intuition.** A value's count is between 1 and n, so make `n + 1` buckets indexed by count and walk them from the top until k values are collected.

**Algorithm**

1. Count frequencies.
2. `bucket[c].append(v)` for each value v with count c.
3. Walk `c = n … 1`, appending bucket contents until you have k.

**Dry run** — [1,1,1,2,2,3], k=2: counts {1:3, 2:2, 3:1} → bucket[3]=[1], bucket[2]=[2], bucket[1]=[3] → take 1, 2.

**C++**
```cpp
vector<int> topKFrequent(vector<int>& nums, int k) {
    unordered_map<int, int> cnt;
    for (int x : nums) cnt[x]++;
    vector<vector<int>> bucket(nums.size() + 1);
    for (auto& [v, c] : cnt) bucket[c].push_back(v);
    vector<int> res;
    for (int c = nums.size(); c >= 1 && (int)res.size() < k; c--)
        for (int v : bucket[c]) {
            res.push_back(v);
            if ((int)res.size() == k) break;
        }
    return res;
}
```

**Java**
```java
static List<Integer> topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> cnt = new HashMap<>();
    for (int x : nums) cnt.merge(x, 1, Integer::sum);
    List<List<Integer>> bucket = new ArrayList<>();
    for (int i = 0; i <= nums.length; i++) bucket.add(new ArrayList<>());
    for (Map.Entry<Integer, Integer> e : cnt.entrySet()) bucket.get(e.getValue()).add(e.getKey());
    List<Integer> res = new ArrayList<>();
    for (int c = nums.length; c >= 1 && res.size() < k; c--)
        for (int v : bucket.get(c)) {
            res.add(v);
            if (res.size() == k) break;
        }
    return res;
}
```

**Python**
```python
from collections import Counter
def top_k_frequent(nums, k):
    bucket = [[] for _ in range(len(nums) + 1)]
    for v, c in Counter(nums).items():
        bucket[c].append(v)
    res = []
    for c in range(len(nums), 0, -1):
        for v in bucket[c]:
            res.append(v)
            if len(res) == k:
                return res
    return res
```

**Complexity:** time **O(n)**, space **O(n)** — counting and bucket scan are both O(n).

---

## Edge cases

- k = number of distinct values → all of them.
- Negative numbers (hash map, not an index array).
- Ties at the k-th position: excluded by the problem guarantee.

---

## Common mistakes

1. Max-heap of all d values then k pops: fine, O(d + k log d), but not the bounded-memory answer.
2. Bucket array sized by the max **value** instead of n.
3. Returning counts instead of values.

---

## Follow-ups

1. Top k frequent words sorted by count then alphabetically (LC 692)?
2. Stream, approximate, low memory?

<details><summary>Answer sketches</summary>

**#1:** Heap with comparator (count asc, word desc) of size k, then reverse.

**#2:** Count-Min Sketch + a size-k heap (heavy hitters) or Misra–Gries.
</details>

---

## Flashcards

**Top-k frequent in O(n)?** #flashcard
Bucket sort by count (buckets 1…n).

**Top-k frequent with a heap?** #flashcard
Min-heap of (count, value) capped at k: O(n + d log k).

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
