---
module: striver/14-arrays
lesson: 27
topic: Majority Element II
difficulty: Medium
source: https://takeuforward.org/learning/dsa/majority-element-ii?category=faqs-hard&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, boyer-moore, voting]
---
# 27. Majority Element II

← [Next Permutation](26-next-permutation.md) · [Part 14 index](README.md) · Next → [Find the Repeating and Missing Number](28-repeating-and-missing.md)

> [!abstract] Problem at a glance
> **Task:** Return all elements appearing more than ⌊n/3⌋ times, sorted.
> **Key insight:** At most two elements can exceed n/3. Extended Boyer–Moore keeps two candidates and two counters: a third, different value decrements both. A second pass verifies the candidates, since none is guaranteed.
> **Difficulty:** Medium · **Pattern:** Boyer–Moore voting (k = 3) · **Also on:** [LC 229](https://leetcode.com/problems/majority-element-ii/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/majority-element-ii?category=faqs-hard&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Count every element](#3-count-every-element) · [4. Hash map counts](#4-hash-map-counts) · [5. Extended Boyer–Moore](#5-extended-boyermoore) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums` of size `n`, return all elements that appear more than `⌊n/3⌋` times, in increasing order.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 1, 1, 3, 2, 2]` | `[1, 2]` | 1 and 2 appear 3 > 2 times |
| `nums = [1, 2, 3]` | `[]` |  |

**Constraints:** `1 ≤ n ≤ 5·10⁴`, `−10⁹ ≤ nums[i] ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Count every element | nested loops, collect up to two | O(n²) | O(1) |
| Hash map counts | count, collect the ones over n/3 | O(n) | O(n) |
| Extended Boyer–Moore | two candidates; a third value decrements both; verify | O(n) | O(1) |

---

## 3. Count every element

**Intuition.** Count each distinct value; keep those above n/3. Stop once two are found.

```python
def majority2_brute(nums):
    n, res = len(nums), []
    for x in nums:
        if x not in res and nums.count(x) > n // 3:
            res.append(x)
            if len(res) == 2:
                break
    return sorted(res)
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Hash map counts

**Intuition.** One pass of counting. Add a value the moment its count reaches `⌊n/3⌋ + 1`, so each is added exactly once.

```python
def majority2_hash(nums):
    cnt, res, need = {}, [], len(nums) // 3 + 1
    for x in nums:
        cnt[x] = cnt.get(x, 0) + 1
        if cnt[x] == need:
            res.append(x)
    return sorted(res)
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 5. Extended Boyer–Moore

**Intuition.** Cancelling triples of three *distinct* values removes at most one copy of any element exceeding n/3 per triple, and there are at most n/3 triples. So any such element survives as a candidate. Survivors aren't necessarily majorities, hence the verification pass.

**Algorithm**

1. `c1, c2, n1 = n2 = 0`.
2. For each `x`: if `x == c1`: `n1++`; elif `x == c2`: `n2++`; elif `n1 == 0`: `c1 = x, n1 = 1`; elif `n2 == 0`: `c2 = x, n2 = 1`; else `n1−−, n2−−`.
3. Count `c1` and `c2` in a second pass; keep those `> n/3` (and `c1 != c2`).

**C++**
```cpp
vector<int> majorityElementTwo(vector<int>& nums) {
    int c1 = 0, c2 = 0, n1 = 0, n2 = 0;
    for (int x : nums) {
        if (n1 > 0 && x == c1) n1++;
        else if (n2 > 0 && x == c2) n2++;
        else if (n1 == 0) { c1 = x; n1 = 1; }
        else if (n2 == 0) { c2 = x; n2 = 1; }
        else { n1--; n2--; }
    }
    int k1 = 0, k2 = 0, n = nums.size();
    for (int x : nums) { if (x == c1) k1++; else if (x == c2) k2++; }
    vector<int> res;
    if (n1 > 0 && k1 > n / 3) res.push_back(c1);
    if (n2 > 0 && k2 > n / 3) res.push_back(c2);
    sort(res.begin(), res.end());
    return res;
}
```

**Java**
```java
static List<Integer> majorityElementTwo(int[] nums) {
    int c1 = 0, c2 = 0, n1 = 0, n2 = 0;
    for (int x : nums) {
        if (n1 > 0 && x == c1) n1++;
        else if (n2 > 0 && x == c2) n2++;
        else if (n1 == 0) { c1 = x; n1 = 1; }
        else if (n2 == 0) { c2 = x; n2 = 1; }
        else { n1--; n2--; }
    }
    int k1 = 0, k2 = 0, n = nums.length;
    for (int x : nums) { if (x == c1) k1++; else if (x == c2) k2++; }
    List<Integer> res = new ArrayList<>();
    if (n1 > 0 && k1 > n / 3) res.add(c1);
    if (n2 > 0 && k2 > n / 3) res.add(c2);
    Collections.sort(res);
    return res;
}
```

**Python**
```python
def majority_element_two(nums):
    c1 = c2 = None
    n1 = n2 = 0
    for x in nums:
        if n1 and x == c1:
            n1 += 1
        elif n2 and x == c2:
            n2 += 1
        elif n1 == 0:
            c1, n1 = x, 1
        elif n2 == 0:
            c2, n2 = x, 1
        else:
            n1 -= 1; n2 -= 1
    n = len(nums)
    res = [c for c, k in ((c1, n1), (c2, n2)) if k and nums.count(c) > n // 3]
    return sorted(res)
```

**Complexity:** time **O(n)**, space **O(1)** — check the equality branches before the zero-count branches, otherwise `c1` and `c2` can become the same value.

---

## Edge cases

- n = 1, n = 2 (both can qualify).
- No element qualifies.
- Value 0 as a candidate (don't confuse it with "empty").

---

## Common mistakes

1. Skipping verification.
2. Checking `n1 == 0` before `x == c2` → both candidates become the same value.
3. Using `>= n/3` instead of `> ⌊n/3⌋`.

---

## Follow-ups

1. More than n/k times.
2. Why at most two answers?

<details><summary>Answer sketches</summary>

**#1:** k − 1 candidates (Misra–Gries), O(nk) time, O(k) space, then verify.

**#2:** Three values each above n/3 would total more than n.
</details>

---

## Flashcards

**Max number of elements > ⌊n/3⌋?** #flashcard
Two.

**Extended Boyer–Moore: branch order?** #flashcard
Match c1, match c2, empty slot 1, empty slot 2, else decrement both.

**Is verification needed for n/3?** #flashcard
Yes, candidates are only potential majorities.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../coding/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../coding/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
