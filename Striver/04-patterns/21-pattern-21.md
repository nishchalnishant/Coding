---
module: striver/04-patterns
lesson: 21
topic: Pattern 21 — Hollow Rectangle
source: https://takeuforward.org/learning/dsa/pattern-21?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 21. Pattern 21: Hollow Rectangle

← [Pattern 20: Symmetric Butterfly](20-pattern-20.md) · [Part 4 index](README.md) · Next → [Pattern 22: Concentric Number Square](22-pattern-22.md)

> [!abstract] What this covers
> **Core idea:** Visit every cell; print '*' iff it's on the border (first/last row or column), else a space.
> **Shape:** n × n outline of stars.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-21?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
*****
*   *
*   *
*   *
*****
```

n = 3 (use this for dry runs):
```text
***
* *
***
```

No separator between cells — the shape depends on exact column positions.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Row type | Content |
|---|---|---|
| 1 | border | n stars |
| 2 | middle | * + (n − 2) spaces + * |
| 3 | middle | * + (n − 2) spaces + * |
| 4 | middle | * + (n − 2) spaces + * |
| 5 | border | n stars |
| **Formula** | **i = 1 or i = n** |  |

---

## 3. Derivation

The first **grid-formula** pattern: rather than counting segments, ask *is this cell on the boundary?* for every (i, j). The condition `i == 0 || j == 0 || i == n − 1 || j == n − 1` is the same boundary test used in matrix problems (border flood fill, *Surrounded Regions*). See [Part 3 Hard §5](../03-logic-building-patterns/02-hard.md#5-hollow-shapes-boundary-test).

---

## 4. Code

**C++**
```cpp
void pattern21(int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++)
            cout << ((i == 0 || j == 0 || i == n - 1 || j == n - 1) ? '*' : ' ');
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern21(int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++)
            System.out.print((i == 0 || j == 0 || i == n - 1 || j == n - 1) ? '*' : ' ');
        System.out.println();
    }
}
```

**Python**
```python
def pattern21(n):
    for i in range(n):
        print("".join("*" if i in (0, n - 1) or j in (0, n - 1) else " " for j in range(n)))
```

---

## 5. Complexity

| | |
|---|---|
| Time | O(n²) — proportional to the O(n²) characters printed |
| Extra space | O(1) in C++/Java; O(n) per row in Python (the row string is built before printing) |

**Edge cases:** n = 1 → `*`. n = 2 → a full 2 × 2 (no interior).

---

## Common mistakes

1. Missing one of the four conditions → an open side.
2. Not printing the inner spaces (skipping them) → the right border collapses left.

---

## Practice

Hollow n × m rectangle.

<details><summary>Answer sketch</summary>

Use `i == n − 1` for the bottom row and `j == m − 1` for the right column.
</details>

---

## Flashcards

**Boundary test for cell (i, j) in an n × n grid (0-based)?** #flashcard
`i == 0 || j == 0 || i == n−1 || j == n−1`.

**Why print the interior spaces explicitly?** #flashcard
Otherwise the right border shifts left — the grid loses its width.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
