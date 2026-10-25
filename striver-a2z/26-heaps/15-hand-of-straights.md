---
module: striver-a2z/26-heaps
lesson: 15
topic: Hand of Straights
difficulty: Medium
source: https://takeuforward.org/learning/dsa/hand-of-straights?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, greedy, ordered-map]
---
# 15. Hand of Straights

← [Task Scheduler](14-task-scheduler.md) · [Part 26 index](README.md) · Next → [Design twitter](16-design-twitter.md)

> [!abstract] Problem at a glance
> **Task:** Can the cards be split into groups of `groupSize` consecutive values?
> **Key insight:** The **smallest remaining card** can only be the start of a group (nothing smaller is left to precede it). So greedily start a group there and consume `x, x+1, …, x+g−1`. If any is missing, fail. With counts, start `c[x]` groups at once.
> **Difficulty:** Medium · **Pattern:** Greedy from the minimum (ordered map / min-heap) · **Also on:** [LC 846](https://leetcode.com/problems/hand-of-straights/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/hand-of-straights?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Min-heap + counts, one group at a time](#3-min-heap--counts-one-group-at-a-time) · [4. Sorted distinct keys, batch groups](#4-sorted-distinct-keys-batch-groups) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given integer cards `hand` and `groupSize`, return `true` if the cards can be rearranged into groups of `groupSize` consecutive cards each.

| Input | Output | Why |
|---|---|---|
| `hand = [1,2,3,6,2,3,4,7,8], groupSize = 3` | `true` | [1,2,3] [2,3,4] [6,7,8] |
| `hand = [1,2,3,4,5], groupSize = 4` | `false` |  |

**Constraints:** `1 ≤ n ≤ 10⁴`, `0 ≤ hand[i] ≤ 10⁹`, `1 ≤ groupSize ≤ n`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Min-heap + counts, one group at a time | peek min; consume min…min+g−1 | O(n log n) | O(n) |
| Sorted distinct keys, batch groups | for x ascending: open c[x] groups at x | O(n log n) | O(n) |

> [!tip] Interview angle
> State the exchange argument for 'start at the smallest' out loud; it's the whole proof. Early exit if `n % groupSize ≠ 0`. Same problem as LC 1296 (Divide Array in Sets of K Consecutive Numbers).

---

## 3. Min-heap + counts, one group at a time

**Intuition.** Min-heap of distinct values plus a counter. Take the heap top as the group start and decrement each of the next g values. If a value hits 0 it must be the heap top at that moment (else some smaller value is stranded), so pop it.

```python
import heapq
from collections import Counter
def is_straight_heap(hand, g):
    if len(hand) % g:
        return False
    c = Counter(hand)
    h = list(c)
    heapq.heapify(h)
    while h:
        s = h[0]
        for x in range(s, s + g):
            if c[x] == 0:
                return False
            c[x] -= 1
            if c[x] == 0:
                if x != h[0]:
                    return False
                heapq.heappop(h)
    return True
```

**Complexity:** time **O(n log n)**, space **O(n)**.

---

## 4. Sorted distinct keys, batch groups

**Intuition.** Walk distinct values ascending. If `k = c[x] > 0` cards remain at x, they must all start groups, so subtract k from each of `x … x+g−1`; fail if any count is short. Sorting dominates.

**Algorithm**

1. If `n % g ≠ 0` → false.
2. Count cards in an ordered map.
3. For each key `x` ascending with `k = c[x] > 0`: for `y = x … x+g−1`, if `c[y] < k` → false, else `c[y] −= k`.
4. Return true.

**Dry run** — [1,2,3,6,2,3,4,7,8], g=3: c = {1:1,2:2,3:2,4:1,6:1,7:1,8:1}. x=1, k=1 → 2:1, 3:1. x=2, k=1 → 3:0, 4:0. x=6, k=1 → 7:0, 8:0 → true.

**C++**
```cpp
bool isNStraightHand(vector<int>& hand, int groupSize) {
    if (hand.size() % groupSize) return false;
    map<int, int> c;
    for (int x : hand) c[x]++;
    for (auto& [x, k] : c) {
        if (k == 0) continue;
        int need = k;
        for (int y = x; y < x + groupSize; y++) {
            auto it = c.find(y);
            if (it == c.end() || it->second < need) return false;
            it->second -= need;
        }
    }
    return true;
}
```

**Java**
```java
static boolean isNStraightHand(int[] hand, int groupSize) {
    if (hand.length % groupSize != 0) return false;
    TreeMap<Integer, Integer> c = new TreeMap<>();
    for (int x : hand) c.merge(x, 1, Integer::sum);
    for (int x : c.keySet()) {
        int k = c.get(x);
        if (k == 0) continue;
        for (int y = x; y < x + groupSize; y++) {
            int have = c.getOrDefault(y, 0);
            if (have < k) return false;
            c.put(y, have - k);
        }
    }
    return true;
}
```

**Python**
```python
from collections import Counter
def is_n_straight_hand(hand, group_size):
    if len(hand) % group_size:
        return False
    c = Counter(hand)
    for x in sorted(c):
        k = c[x]
        if k:
            for y in range(x, x + group_size):
                if c[y] < k:
                    return False
                c[y] -= k
    return True
```

**Complexity:** time **O(n log n)**, space **O(n)** — sorting d distinct keys plus O(d·g) updates, bounded by O(n) because each update consumes ≥ 1 card.

---

## Edge cases

- `groupSize = 1` → always true.
- `n % groupSize ≠ 0` → false immediately.
- Large gaps between values (don't index an array by value).

---

## Common mistakes

1. Starting groups from an arbitrary card (not the minimum).
2. Java: modifying a `TreeMap` *value* during `keySet()` iteration is fine; removing keys is not (ConcurrentModificationException).
3. Python: `Counter[y]` for a missing key returns 0 but also doesn't insert, so it's safe here.

---

## Follow-ups

1. Split into consecutive subsequences of length ≥ 3 (LC 659)?
2. Values up to 10⁹, n up to 10⁵?

<details><summary>Answer sketches</summary>

**#1:** Greedy with `need[x]` (chains wanting x): extend an existing chain before starting a new one.

**#2:** Same algorithm; the ordered map handles sparsity.
</details>

---

## Flashcards

**Hand of straights greedy?** #flashcard
Smallest remaining card must start a group; consume it…it+g−1.

**Hand of straights quick reject?** #flashcard
`n % groupSize ≠ 0`.

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
