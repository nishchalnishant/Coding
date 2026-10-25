---
module: striver-a2z/22-sliding-window-and-2-pointer
lesson: 5
topic: Fruit Into Baskets
difficulty: Medium
source: https://takeuforward.org/learning/dsa/fruit-into-baskets?category=longest-and-smallest-window-problems&source=strivers-a2z-dsa-sheet
tags: [striver, sliding-window-and-2-pointer, sliding-window, hashing, at-most-k]
---
# 5. Fruit Into Baskets

← [Max Consecutive Ones III](04-max-consecutive-ones-iii.md) · [Part 22 index](README.md) · Next → [Longest Substring With At Most K Distinct Characters](06-longest-substring-with-at-most-k-distinct-characters.md)

> [!abstract] Problem at a glance
> **Task:** Longest contiguous run of trees that contains at most 2 distinct fruit types.
> **Key insight:** This is "longest subarray with at most K distinct values" with K = 2. Keep a count map for the window and shrink from the left whenever it holds more than two keys.
> **Difficulty:** Medium · **Pattern:** Variable window + frequency map (≤ K distinct) · **Also on:** [LC 904](https://leetcode.com/problems/fruit-into-baskets/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/fruit-into-baskets?category=longest-and-smallest-window-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force: every start](#3-brute-force-every-start) · [4. Window with counts](#4-window-with-counts) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`fruits[i]` is the type of fruit on tree `i`. You have two baskets, each holding unlimited fruit of a single type. Starting at any tree, you pick one fruit from every tree moving right, and stop when a fruit doesn't fit either basket. Return the maximum number of fruits you can pick.

| Input | Output | Why |
|---|---|---|
| `fruits = [1,2,1]` | `3` | all three |
| `fruits = [0,1,2,2]` | `3` | [1,2,2] |
| `fruits = [1,2,3,2,2]` | `4` | [2,3,2,2] |

**Constraints:** `1 ≤ fruits.length ≤ 10⁵`, `0 ≤ fruits[i] < fruits.length`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force: every start | extend each start until a 3rd type appears | O(n²) | O(1) |
| Window with counts | shrink while > 2 keys | O(n) | O(1) |

> [!tip] Interview angle
> A disguised template problem. Say the rephrase first; then the code is the standard at-most-K window. Mention that removing a key at count 0 is what keeps `len(map)` honest.

---

## 3. Brute force: every start

**Intuition.** For each start, add fruits to a set until it would hold three types.

```python
def total_fruit_brute(fruits):
    best = 0
    for i in range(len(fruits)):
        types = set()
        for j in range(i, len(fruits)):
            types.add(fruits[j])
            if len(types) > 2:
                break
            best = max(best, j - i + 1)
    return best
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Window with counts

**Intuition.** Add `fruits[r]` to the count map. While the map has more than two keys, decrement `fruits[l]` (deleting it at zero) and advance `l`. Record the window length.

**Algorithm**

1. `cnt = {}`, `l = best = 0`.
2. For each `r`: `cnt[fruits[r]] += 1`.
3. While `len(cnt) > 2`: decrement `cnt[fruits[l]]`, delete at 0, `l += 1`.
4. `best = max(best, r − l + 1)`.

**Dry run** — [1,2,3,2,2]: r=2 → {1,2,3}: drop 1 → l=1 {2:1,3:1} → r=3,4 → {2:3,3:1}, window 1..4 = 4.

**C++**
```cpp
int totalFruit(vector<int>& fruits) {
    unordered_map<int, int> cnt;
    int l = 0, best = 0;
    for (int r = 0; r < (int)fruits.size(); r++) {
        cnt[fruits[r]]++;
        while (cnt.size() > 2) {
            if (--cnt[fruits[l]] == 0) cnt.erase(fruits[l]);
            l++;
        }
        best = max(best, r - l + 1);
    }
    return best;
}
```

**Java**
```java
static int totalFruit(int[] fruits) {
    Map<Integer, Integer> cnt = new HashMap<>();
    int l = 0, best = 0;
    for (int r = 0; r < fruits.length; r++) {
        cnt.merge(fruits[r], 1, Integer::sum);
        while (cnt.size() > 2) {
            if (cnt.merge(fruits[l], -1, Integer::sum) == 0) cnt.remove(fruits[l]);
            l++;
        }
        best = Math.max(best, r - l + 1);
    }
    return best;
}
```

**Python**
```python
def total_fruit(fruits):
    cnt, l, best = {}, 0, 0
    for r, f in enumerate(fruits):
        cnt[f] = cnt.get(f, 0) + 1
        while len(cnt) > 2:
            cnt[fruits[l]] -= 1
            if cnt[fruits[l]] == 0:
                del cnt[fruits[l]]
            l += 1
        best = max(best, r - l + 1)
    return best
```

**Complexity:** time **O(n)**, space **O(1)** — each index enters and leaves the window once; the map never holds more than 3 keys.

---

## Edge cases

- Single type → n.
- Every tree a new type → 2.
- n = 1 → 1.

---

## Common mistakes

1. Forgetting to delete keys at count 0, so the map size never drops.
2. Resetting the window to start at `r` when a third type appears (loses the valid suffix).
3. Treating it as "two most frequent types overall".

---

## Follow-ups

1. K baskets.
2. Count the subarrays with at most 2 types.

<details><summary>Answer sketches</summary>

**#1:** Same code with `> K` — see Longest Substring With At Most K Distinct Characters.

**#2:** Add `r − l + 1` per step instead of taking the max.
</details>

---

## Flashcards

**Fruit Into Baskets rephrased?** #flashcard
Longest subarray with at most 2 distinct values.

**Why delete keys at zero count?** #flashcard
The window's distinct count is the map size; zero-count keys would inflate it.

**Interview track →** [Sliding-window deep-dive](../../02-algorithms/04-sliding-window.md) · [Two-pointers deep-dive](../../02-algorithms/03-two-pointers.md) · [Sliding-window walkthroughs](../../04-practice/algorithms/04-sliding-window.md)
