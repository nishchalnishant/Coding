---
module: striver-a2z/04-patterns
lesson: 13
topic: Pattern 13 — Increasing Number Triangle
source: https://takeuforward.org/learning/dsa/pattern-13?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 13. Pattern 13: Increasing Number Triangle

← [Pattern 12: Number Crown](12-pattern-12.md) · [Part 4 index](README.md) · Next → [Pattern 14: Letter Triangle](14-pattern-14.md)

> [!abstract] What this covers
> **Core idea:** The value lives across rows: a counter declared outside both loops, incremented every cell.
> **Shape:** 1 / 2 3 / 4 5 6 — a running counter.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-13?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
1
2 3
4 5 6
7 8 9 10
11 12 13 14 15
```

n = 3 (use this for dry runs):
```text
1
2 3
4 5 6
```

Cells are separated by a space, as in Striver's reference output.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Cells | First value | Row |
|---|---|---|---|
| 1 | 1 | 1 | 1 |
| 2 | 2 | 2 | 2 3 |
| 3 | 3 | 4 | 4 5 6 |
| 4 | 4 | 7 | 7 8 9 10 |
| 5 | 5 | 11 | 11 12 13 14 15 |
| **Formula** | **i** | **1 + i(i − 1)/2** | **first … first + i − 1** |

---

## 3. Derivation

No (i, j) formula is needed: just count. If you want one anyway, rows 1 … i − 1 hold 1 + 2 + … + (i − 1) = i(i − 1)/2 numbers, so row i starts at `1 + i(i − 1)/2` and cell j is `i(i − 1)/2 + j` (Floyd's triangle).

---

## 4. Code

**C++**
```cpp
void pattern13(int n) {
    int num = 1;                                 // outside BOTH loops
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) cout << num++ << " ";
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern13(int n) {
    int num = 1;                                 // outside BOTH loops
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) System.out.print(num++ + " ");
        System.out.println();
    }
}
```

**Python**
```python
def pattern13(n):
    num = 1
    for i in range(1, n + 1):
        row = []
        for _ in range(i):
            row.append(str(num))
            num += 1
        print(" ".join(row))
```

---

## 5. Complexity

| | |
|---|---|
| Time | O(n²) — proportional to the O(n²) characters printed |
| Extra space | O(1) in C++/Java; O(n) per row in Python (the row string is built before printing) |

**Edge cases:** Last number printed = n(n + 1)/2.

---

## Common mistakes

1. `int num = 1` inside the outer loop → every row restarts at 1 (that's pattern 3).

---

## Practice

Print only the last number of each row.

<details><summary>Answer sketch</summary>

Row i's last value is i(i + 1)/2.
</details>

---

## Flashcards

**Where must the counter be declared in pattern 13?** #flashcard
Outside both loops, so it keeps counting across rows.

**First value in row i?** #flashcard
1 + i(i − 1)/2 (triangular offset). This is Floyd's triangle.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
