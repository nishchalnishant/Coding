---
module: striver/04-patterns
lesson: 9
topic: Pattern 9 — Diamond
source: https://takeuforward.org/learning/dsa/pattern-9?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 9. Pattern 9: Diamond

← [Pattern 8: Inverted Star Pyramid](08-pattern-8.md) · [Part 4 index](README.md) · Next → [Pattern 10: Half Diamond](10-pattern-10.md)

> [!abstract] What this covers
> **Core idea:** Composition: run pattern 7's loop, then pattern 8's loop (middle row printed twice).
> **Shape:** pyramid on top of an inverted pyramid.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-9?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
    *
   ***
  *****
 *******
*********
*********
 *******
  *****
   ***
    *
```

n = 3 (use this for dry runs):
```text
  *
 ***
*****
*****
 ***
  *
```

No separator between cells — the shape depends on exact column positions.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Half | Spaces | Stars |
|---|---|---|---|
| 1 | top | 4 | 1 |
| 2 | top | 3 | 3 |
| 3 | top | 2 | 5 |
| 4 | top | 1 | 7 |
| 5 | top | 0 | 9 |
| 6 | bottom | 0 | 9 |
| 7 | bottom | 1 | 7 |
| 8 | bottom | 2 | 5 |
| 9 | bottom | 3 | 3 |
| 10 | bottom | 4 | 1 |
| **Formula** |  | **top n − i · bottom k − 1** | **top 2i − 1 · bottom 2(n − k) + 1** |

Rows n+1 … 2n are the bottom half; k = i − n is the row number inside that half.

---

## 3. Derivation

Spot the seam: the top half is pattern 7, the bottom is pattern 8. Two loops, no new formulas. Striver's output has **2n rows** (the widest row appears twice). For a 2n − 1-row diamond, start the second loop at i = 2.

---

## 4. Code

**C++**
```cpp
void pattern9(int n) {
    for (int i = 1; i <= n; i++) {                       // pattern 7
        for (int s = 0; s < n - i; s++) cout << ' ';
        for (int j = 0; j < 2 * i - 1; j++) cout << '*';
        cout << '\n';
    }
    for (int i = 1; i <= n; i++) {                       // pattern 8
        for (int s = 0; s < i - 1; s++) cout << ' ';
        for (int j = 0; j < 2 * (n - i) + 1; j++) cout << '*';
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern9(int n) {
    for (int i = 1; i <= n; i++) {                       // pattern 7
        for (int s = 0; s < n - i; s++) System.out.print(' ');
        for (int j = 0; j < 2 * i - 1; j++) System.out.print('*');
        System.out.println();
    }
    for (int i = 1; i <= n; i++) {                       // pattern 8
        for (int s = 0; s < i - 1; s++) System.out.print(' ');
        for (int j = 0; j < 2 * (n - i) + 1; j++) System.out.print('*');
        System.out.println();
    }
}
```

**Python**
```python
def pattern9(n):
    for i in range(1, n + 1):                      # pattern 7
        print(" " * (n - i) + "*" * (2 * i - 1))
    for i in range(1, n + 1):                      # pattern 8
        print(" " * (i - 1) + "*" * (2 * (n - i) + 1))
```

---

## 5. Complexity

| | |
|---|---|
| Time | O(n²) — proportional to the O(n²) characters printed |
| Extra space | O(1) in C++/Java; O(n) per row in Python (the row string is built before printing) |

**Edge cases:** n = 1 → two `*` rows (Striver's version).

---

## Common mistakes

1. Copy-paste the first loop and forget to change both formulas in the second.
2. Not reading the expected output: 2n vs 2n − 1 rows.

---

## Practice

Diamond with 2n − 1 rows using a single loop.

<details><summary>Answer sketch</summary>

Row i in 1..2n − 1: stars = 2(n − |n − i|) − 1, spaces = |n − i|.
</details>

---

## Flashcards

**How is the diamond built?** #flashcard
Pattern 7 then pattern 8 — composition of two solved shapes.

**How many rows does Striver's diamond have?** #flashcard
2n (middle row repeated). Skip one copy for 2n − 1.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
