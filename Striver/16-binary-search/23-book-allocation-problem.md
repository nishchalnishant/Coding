---
module: striver/16-binary-search
lesson: 23
topic: Book Allocation Problem
difficulty: Hard
source: https://takeuforward.org/learning/dsa/book-allocation-problem?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, bs-on-answer, greedy]
---
# 23. Book Allocation Problem

← [Aggressive Cows](22-aggressive-cows.md) · [Part 16 index](README.md) · Next → [Find Peak Element](24-find-peak-element.md)

> [!abstract] Problem at a glance
> **Task:** Allocate books (contiguous, in order, each student ≥ 1 book) to `m` students minimising the maximum pages any student reads. Return −1 if `m > n`.
> **Key insight:** Exactly ship-within-days: binary search the max pages `[max, Σ]`, greedy-count students needed. The only extra is the `m > n` guard, because every student must get a book.
> **Difficulty:** Hard · **Pattern:** Binary search on answer + greedy partition
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/book-allocation-problem?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear over cap](#3-linear-over-cap) · [4. Binary search on max pages](#4-binary-search-on-max-pages) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `arr[i]` = pages in book `i` and `m` students: every book goes to exactly one student, each student gets at least one book, and each student's books are contiguous. Minimise the maximum number of pages assigned to a student. Return `-1` if allocation is impossible.

| Input | Output | Why |
|---|---|---|
| `arr = [12, 34, 67, 90], m = 2` | `113` | [12 34 67] [90] |
| `arr = [25, 46, 28, 49, 24], m = 4` | `71` | [25 46] [28] [49] [24] |
| `arr = [15, 17, 20], m = 5` | `-1` |  |

**Constraints:** `1 ≤ n, m ≤ 10⁴`, `1 ≤ arr[i] ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear over cap | cap = max … Σ, first with students ≤ m | O(n · (Σ − max)) | O(1) |
| Binary search on max pages | m > n → −1; first cap in [max, Σ] with students(cap) ≤ m | O(n log Σ) | O(1) |

> [!tip] Interview angle
> Why does "each student gets ≥ 1 book" not complicate the check? If the greedy uses fewer than `m` students at some cap, you can always split a multi-book student to use more (when `m ≤ n`) without raising the max. So `need(cap) ≤ m` is the right test.

---

## 3. Linear over cap

**Intuition.** Greedy check scanned upward.

```python
def book_alloc_linear(arr, m):
    if m > len(arr):
        return -1
    for cap in range(max(arr), sum(arr) + 1):
        s, cur = 1, 0
        for p in arr:
            if cur + p > cap:
                s, cur = s + 1, 0
            cur += p
        if s <= m:
            return cap
```

**Complexity:** time **O(n · (Σ − max))**, space **O(1)**.

---

## 4. Binary search on max pages

**Intuition.** Identical skeleton to Painter's Partition and Split Array.

**Dry run** — `[12 34 67 90]`, m 2: lo 90 hi 203 mid 146 → [12 34 67] [90] = 2 ✓ hi 145; … converges at 113 ([12 34 67] = 113).

**C++**
```cpp
int findPages(vector<int>& arr, int m) {
    if (m > (int)arr.size()) return -1;
    int lo = 0, hi = 0;
    for (int p : arr) { lo = max(lo, p); hi += p; }
    int ans = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2, s = 1, cur = 0;
        for (int p : arr) {
            if (cur + p > mid) { s++; cur = 0; }
            cur += p;
        }
        if (s <= m) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Java**
```java
static int findPages(int[] arr, int m) {
    if (m > arr.length) return -1;
    int lo = 0, hi = 0;
    for (int p : arr) { lo = Math.max(lo, p); hi += p; }
    int ans = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2, s = 1, cur = 0;
        for (int p : arr) {
            if (cur + p > mid) { s++; cur = 0; }
            cur += p;
        }
        if (s <= m) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Python**
```python
def find_pages(arr, m):
    if m > len(arr):
        return -1
    def need(cap):
        s, cur = 1, 0
        for p in arr:
            if cur + p > cap:
                s, cur = s + 1, 0
            cur += p
        return s
    lo, hi = max(arr), sum(arr)
    ans = hi
    while lo <= hi:
        mid = (lo + hi) // 2
        if need(mid) <= m:
            ans, hi = mid, mid - 1
        else:
            lo = mid + 1
    return ans
```

**Complexity:** time **O(n log Σ)**, space **O(1)** — log(Σ) greedy checks.

---

## Edge cases

- m > n → −1.
- m = n → max(arr).
- m = 1 → Σ.

---

## Common mistakes

1. Missing the m > n guard.
2. Checking `need == m` instead of `≤ m`.

---

## Follow-ups

1. Books can be in any order.
2. Minimise max − min load.

<details><summary>Answer sketches</summary>

**#1:** NP-hard (multiprocessor scheduling).

**#2:** Different objective; DP over partitions.
</details>

---

## Flashcards

**Book allocation — impossible when?** #flashcard
m > n (each student needs ≥ 1 book).

**Why need(cap) ≤ m, not == m?** #flashcard
Fewer groups can always be split further without raising the max.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../coding/algorithms/11-binary-search.md)
