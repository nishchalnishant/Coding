---
module: striver-a2z/14-arrays
lesson: 17
topic: Pascal's Triangle II
difficulty: Easy
source: https://takeuforward.org/learning/dsa/pascals-triangle-ii?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, math, combinatorics, pascal]
---
# 17. Pascal's Triangle II

← [Pascal's Triangle I](16-pascals-triangle-i.md) · [Part 14 index](README.md) · Next → [Pascal's Triangle III](18-pascals-triangle-iii.md)

> [!abstract] Problem at a glance
> **Task:** Return row `r` (1-indexed) of Pascal's triangle.
> **Key insight:** Row `r` is C(r − 1, 0), C(r − 1, 1), …, C(r − 1, r − 1). Each value follows from the previous one: `next = prev · (n − k) / (k + 1)`. That gives O(r) for the row, versus O(r²) to build every row above it.
> **Difficulty:** Easy · **Pattern:** Combinatorics: nCr row · **Also on:** [LC 119](https://leetcode.com/problems/pascals-triangle-ii/) (0-indexed)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/pascals-triangle-ii?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. nCr per column](#3-ncr-per-column) · [4. Incremental product](#4-incremental-product) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer `r`, return the `r`-th row (1-indexed) of Pascal's triangle.

| Input | Output | Why |
|---|---|---|
| `r = 4` | `[1, 3, 3, 1]` |  |
| `r = 1` | `[1]` |  |

**Constraints:** `1 ≤ r ≤ 30`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| nCr per column | compute each C(n, k) from scratch | O(r²) | O(1) beyond the output |
| Incremental product | val = val · (n − k) / (k + 1) | O(r) | O(1) beyond the output |

---

## 3. nCr per column

**Intuition.** Call the running-product nCr for every column. Correct, but it repeats work the neighbouring column already did.

```python
def pascal_row_ncr(r):
    def ncr(n, k):
        res = 1
        for i in range(k):
            res = res * (n - i) // (i + 1)
        return res
    return [ncr(r - 1, c) for c in range(r)]
```

**Complexity:** time **O(r²)**, space **O(1) beyond the output**.

---

## 4. Incremental product

**Intuition.** `C(n, k + 1) = C(n, k) · (n − k) / (k + 1)`. Start at 1 and derive each value from the one before it. The division is exact because the result is an integer.

**Dry run** — r = 5 (n = 4): 1 → 1·4/1 = 4 → 4·3/2 = 6 → 6·2/3 = 4 → 4·1/4 = 1.

**In-place DP alternative:** start from `[1]` and for each new row update `row[j] += row[j − 1]` from right to left, then append 1. That's O(r²) time but needs no division, which is useful when working mod p.

**C++**
```cpp
vector<int> pascalTriangleII(int r) {
    vector<int> row;
    long long val = 1;
    int n = r - 1;
    for (int k = 0; k <= n; k++) {
        row.push_back((int)val);
        val = val * (n - k) / (k + 1);
    }
    return row;
}
```

**Java**
```java
static List<Integer> pascalTriangleII(int r) {
    List<Integer> row = new ArrayList<>();
    long val = 1;
    int n = r - 1;
    for (int k = 0; k <= n; k++) {
        row.add((int) val);
        val = val * (n - k) / (k + 1);
    }
    return row;
}
```

**Python**
```python
def pascal_row(r):
    n, val, row = r - 1, 1, []
    for k in range(n + 1):
        row.append(val)
        val = val * (n - k) // (k + 1)
    return row
```

**Complexity:** time **O(r)**, space **O(1) beyond the output**.

---

## Edge cases

- r = 1 → [1].
- Rows are symmetric, so you could compute half and mirror it.

---

## Common mistakes

1. Updating the DP row left to right (it reads values that were already overwritten).
2. Integer division before the multiply.

---

## Follow-ups

1. Row r mod 1e9+7.
2. Only O(1) space besides the output (LC 119 follow-up).

<details><summary>Answer sketches</summary>

**#1:** Use the additive DP, or factorials with modular inverses.

**#2:** The incremental product is already that.
</details>

---

## Flashcards

**Next value in a Pascal row?** #flashcard
C(n, k + 1) = C(n, k) · (n − k) / (k + 1).

**In-place additive row update direction?** #flashcard
Right to left: row[j] += row[j − 1].

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../04-practice/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../04-practice/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
