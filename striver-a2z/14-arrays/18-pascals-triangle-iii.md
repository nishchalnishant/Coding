---
module: striver-a2z/14-arrays
lesson: 18
topic: Pascal's Triangle III
difficulty: Easy
source: https://takeuforward.org/learning/dsa/pascals-triangle-iii?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, math, dp, pascal]
---
# 18. Pascal's Triangle III

← [Pascal's Triangle II](17-pascals-triangle-ii.md) · [Part 14 index](README.md) · Next → [Rotate Matrix by 90 Degrees](19-rotate-matrix.md)

> [!abstract] Problem at a glance
> **Task:** Return the first `n` rows of Pascal's triangle.
> **Key insight:** Each row's inner values are sums of adjacent pairs from the previous row: `row[j] = prev[j − 1] + prev[j]`, with 1s at both ends. Generating each row independently with the incremental product works too.
> **Difficulty:** Easy · **Pattern:** DP on rows · **Also on:** [LC 118](https://leetcode.com/problems/pascals-triangle/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/pascals-triangle-iii?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Row by incremental product](#3-row-by-incremental-product) · [4. Additive DP](#4-additive-dp) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer `n`, return the first `n` rows of Pascal's triangle.

| Input | Output | Why |
|---|---|---|
| `n = 4` | `[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]]` |  |
| `n = 1` | `[[1]]` |  |

**Constraints:** `1 ≤ n ≤ 30`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Row by incremental product | generate each row with Pascal II | O(n²) | O(1) beyond the output |
| Additive DP | row[j] = prev[j − 1] + prev[j] | O(n²) | O(1) beyond the output |

---

## 3. Row by incremental product

**Intuition.** Row `i` is produced in O(i) by the product formula, giving O(n²) total. That's optimal, since the output itself has n(n + 1)/2 numbers.

```python
def pascal_rows_product(n):
    res = []
    for r in range(n):
        val, row = 1, []
        for k in range(r + 1):
            row.append(val)
            val = val * (r - k) // (k + 1)
        res.append(row)
    return res
```

**Complexity:** time **O(n²)**, space **O(1) beyond the output**.

---

## 4. Additive DP

**Intuition.** The defining rule: every inner value is the sum of the two above it. No multiplication or division, so no overflow concerns until the values themselves overflow.

**C++**
```cpp
vector<vector<int>> pascalTriangleIII(int n) {
    vector<vector<int>> res;
    for (int i = 0; i < n; i++) {
        vector<int> row(i + 1, 1);
        for (int j = 1; j < i; j++) row[j] = res[i - 1][j - 1] + res[i - 1][j];
        res.push_back(row);
    }
    return res;
}
```

**Java**
```java
static List<List<Integer>> pascalTriangleIII(int n) {
    List<List<Integer>> res = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        List<Integer> row = new ArrayList<>();
        for (int j = 0; j <= i; j++) {
            if (j == 0 || j == i) row.add(1);
            else row.add(res.get(i - 1).get(j - 1) + res.get(i - 1).get(j));
        }
        res.add(row);
    }
    return res;
}
```

**Python**
```python
def pascal_rows(n):
    res = []
    for i in range(n):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = res[i - 1][j - 1] + res[i - 1][j]
        res.append(row)
    return res
```

**Complexity:** time **O(n²)**, space **O(1) beyond the output**.

---

## Edge cases

- n = 1, n = 2 (no inner values).

---

## Common mistakes

1. Inner loop from `j = 0`, which reads `prev[−1]`.
2. Reusing one row object for every row (aliasing).

---

## Follow-ups

1. Sum of row r?
2. Pascal's triangle mod 2?

<details><summary>Answer sketches</summary>

**#1:** 2^(r − 1).

**#2:** Sierpiński pattern; C(n, k) is odd iff `k & n == k` (Lucas).
</details>

---

## Flashcards

**Pascal row recurrence?** #flashcard
row[j] = prev[j − 1] + prev[j]; ends are 1.

**Sum of the r-th row (1-indexed)?** #flashcard
2^(r − 1).

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../04-practice/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../04-practice/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
