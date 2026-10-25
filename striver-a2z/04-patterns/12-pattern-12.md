---
module: striver-a2z/04-patterns
lesson: 12
topic: Pattern 12 — Number Crown
source: https://takeuforward.org/learning/dsa/pattern-12?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 12. Pattern 12: Number Crown

← [Pattern 11: Binary Number Triangle](11-pattern-11.md) · [Part 4 index](README.md) · Next → [Pattern 13: Increasing Number Triangle](13-pattern-13.md)

> [!abstract] What this covers
> **Core idea:** Three segments per row: 1 … i, then 2(n − i) spaces, then i … 1.
> **Shape:** 1……1 / 12….21 — mirrored numbers with a shrinking gap.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-12?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
1        1
12      21
123    321
1234  4321
1234554321
```

n = 3 (use this for dry runs):
```text
1    1
12  21
123321
```

No separator between cells — the shape depends on exact column positions.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Left | Gap | Right |
|---|---|---|---|
| 1 | 1 | 8 | 1 |
| 2 | 1 2 | 6 | 2 1 |
| 3 | 1 2 3 | 4 | 3 2 1 |
| 4 | 1 2 3 4 | 2 | 4 3 2 1 |
| 5 | 1 2 3 4 5 | 0 | 5 4 3 2 1 |
| **Formula** | **1 … i** | **2(n − i)** | **i … 1** |

---

## 3. Derivation

First segmented row with **three** inner loops. Width check: i + 2(n − i) + i = 2n ✅ for every row. The right segment is the left one reversed — loop `j` downward. Striver's solution keeps a `space` variable starting at 2(n − 1) and subtracts 2 each row; same thing.

---

## 4. Code

**C++**
```cpp
void pattern12(int n) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) cout << j;
        for (int s = 0; s < 2 * (n - i); s++) cout << ' ';
        for (int j = i; j >= 1; j--) cout << j;
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern12(int n) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) System.out.print(j);
        for (int s = 0; s < 2 * (n - i); s++) System.out.print(' ');
        for (int j = i; j >= 1; j--) System.out.print(j);
        System.out.println();
    }
}
```

**Python**
```python
def pattern12(n):
    for i in range(1, n + 1):
        left = "".join(str(j) for j in range(1, i + 1))
        print(left + " " * (2 * (n - i)) + left[::-1])
```

---

## 5. Complexity

| | |
|---|---|
| Time | O(n²) — proportional to the O(n²) characters printed |
| Extra space | O(1) in C++/Java; O(n) per row in Python (the row string is built before printing) |

**Edge cases:** Last row has a 0-length gap: `12344321` for n = 4.

---

## Common mistakes

1. Gap `n − i` (forgot the factor 2) → rows don't line up.
2. Right loop counting up → `12  12` instead of `12  21`.

---

## Practice

Use letters instead of numbers: A……A / AB….BA.

<details><summary>Answer sketch</summary>

Print `(char)('A' + j − 1)`.
</details>

---

## Flashcards

**Gap in row i of the number crown?** #flashcard
2(n − i) spaces, so the width is always 2n.

**How many inner loops per row?** #flashcard
Three: left numbers, gap, right numbers (reversed).

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
