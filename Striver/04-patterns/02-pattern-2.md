---
module: striver/04-patterns
lesson: 2
topic: Pattern 2 — Right-Angled Triangle
source: https://takeuforward.org/learning/dsa/pattern-2?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 2. Pattern 2: Right-Angled Triangle

← [Pattern 1: Square of Stars](01-pattern-1.md) · [Part 4 index](README.md) · Next → [Pattern 3: Number Triangle](03-pattern-3.md)

> [!abstract] What this covers
> **Core idea:** Inner bound = i: the first pattern where the inner loop depends on the outer variable.
> **Shape:** row i has i stars.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-2?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
*
* *
* * *
* * * *
* * * * *
```

n = 3 (use this for dry runs):
```text
*
* *
* * *
```

Cells are separated by a space, as in Striver's reference output.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Stars |
|---|---|
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 4 |
| 5 | 5 |
| **Formula** | **i** |

---

## 3. Derivation

Row table: row 1 → 1 star, row 2 → 2 … the stars column *is* i. So `for j in 1..i`. Total stars = 1 + 2 + … + n = **n(n+1)/2**, still O(n²).

---

## 4. Code

**C++**
```cpp
void pattern2(int n) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) cout << "* ";
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern2(int n) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) System.out.print("* ");
        System.out.println();
    }
}
```

**Python**
```python
def pattern2(n):
    for i in range(1, n + 1):
        print("* " * i)
```

---

## 5. Complexity

| | |
|---|---|
| Time | O(n²) — proportional to the O(n²) characters printed |
| Extra space | O(1) in C++/Java; O(n) per row in Python (the row string is built before printing) |

**Edge cases:** n = 1 → `*`.

---

## Common mistakes

1. 0-based outer loop with `j < i` → first row empty, only n−1 visible rows. Use `j <= i` or `j < i + 1`.

---

## Practice

Right-align it (stars hug the right edge).

<details><summary>Answer sketch</summary>

Prefix `n − i` spaces (single-width cells) before the `i` stars.
</details>

---

## Flashcards

**Inner-loop bound for the right triangle?** #flashcard
`j ≤ i` (1-based).

**How many stars does pattern 2 print in total?** #flashcard
n(n+1)/2 — the triangular number; O(n²).

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
