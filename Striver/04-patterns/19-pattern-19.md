---
module: striver/04-patterns
lesson: 19
topic: Pattern 19 — Symmetric Void
source: https://takeuforward.org/learning/dsa/pattern-19?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 19. Pattern 19: Symmetric Void

← [Pattern 18: Alpha-Triangle](18-pattern-18.md) · [Part 4 index](README.md) · Next → [Pattern 20: Symmetric Butterfly](20-pattern-20.md)

> [!abstract] What this covers
> **Core idea:** Two halves; each row = stars, gap, stars. Top: stars n − i + 1, gap 2(i − 1). Bottom: stars i, gap 2(n − i).
> **Shape:** stars frame a diamond-shaped hole.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-19?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
**********
****  ****
***    ***
**      **
*        *
*        *
**      **
***    ***
****  ****
**********
```

n = 3 (use this for dry runs):
```text
******
**  **
*    *
*    *
**  **
******
```

No separator between cells — the shape depends on exact column positions.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Half | Stars each side | Gap |
|---|---|---|---|
| 1 | top | 5 | 0 |
| 2 | top | 4 | 2 |
| 3 | top | 3 | 4 |
| 4 | top | 2 | 6 |
| 5 | top | 1 | 8 |
| 6 | bottom | 1 | 8 |
| 7 | bottom | 2 | 6 |
| 8 | bottom | 3 | 4 |
| 9 | bottom | 4 | 2 |
| 10 | bottom | 5 | 0 |
| **Formula** |  | **top n − i + 1 · bottom k** | **top 2(i − 1) · bottom 2(n − k)** |

k = i − n is the row number inside the bottom half. Width is 2n in every row.

---

## 3. Derivation

Each half is the number crown's skeleton ([pattern 12](12-pattern-12.md)) with stars: three segments. The top half shrinks the stars and grows the gap; the bottom half is the exact reverse. Striver keeps one `gap` variable: start 0, `+= 2` per row on top; start 2(n − 1), `−= 2` per row on the bottom.

---

## 4. Code

**C++**
```cpp
void pattern19(int n) {
    for (int i = 1; i <= n; i++) {                       // top half
        for (int j = 0; j < n - i + 1; j++) cout << '*';
        for (int j = 0; j < 2 * (i - 1); j++) cout << ' ';
        for (int j = 0; j < n - i + 1; j++) cout << '*';
        cout << '\n';
    }
    for (int i = 1; i <= n; i++) {                       // bottom half
        for (int j = 0; j < i; j++) cout << '*';
        for (int j = 0; j < 2 * (n - i); j++) cout << ' ';
        for (int j = 0; j < i; j++) cout << '*';
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern19(int n) {
    for (int i = 1; i <= n; i++) {                       // top half
        for (int j = 0; j < n - i + 1; j++) System.out.print('*');
        for (int j = 0; j < 2 * (i - 1); j++) System.out.print(' ');
        for (int j = 0; j < n - i + 1; j++) System.out.print('*');
        System.out.println();
    }
    for (int i = 1; i <= n; i++) {                       // bottom half
        for (int j = 0; j < i; j++) System.out.print('*');
        for (int j = 0; j < 2 * (n - i); j++) System.out.print(' ');
        for (int j = 0; j < i; j++) System.out.print('*');
        System.out.println();
    }
}
```

**Python**
```python
def pattern19(n):
    for i in range(1, n + 1):                      # top half
        s, gap = n - i + 1, 2 * (i - 1)
        print("*" * s + " " * gap + "*" * s)
    for i in range(1, n + 1):                      # bottom half
        s, gap = i, 2 * (n - i)
        print("*" * s + " " * gap + "*" * s)
```

---

## 5. Complexity

| | |
|---|---|
| Time | O(n²) — proportional to the O(n²) characters printed |
| Extra space | O(1) in C++/Java; O(n) per row in Python (the row string is built before printing) |

**Edge cases:** n = 1 → `**` twice.

---

## Common mistakes

1. Gap `i − 1` instead of `2(i − 1)` → hole is lopsided.
2. Bottom half reusing the top formulas → the shape repeats instead of mirroring.

---

## Practice

Print with 2n − 1 rows (single middle row).

<details><summary>Answer sketch</summary>

Run the bottom loop from i = 2.
</details>

---

## Flashcards

**Top half formulas of the symmetric void?** #flashcard
Stars n − i + 1 each side, gap 2(i − 1).

**Width of every row?** #flashcard
2n.

**How does the butterfly (pattern 20) relate?** #flashcard
Swap which segment grows: stars grow and the gap shrinks.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
