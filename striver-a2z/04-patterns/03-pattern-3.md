---
module: striver-a2z/04-patterns
lesson: 3
topic: Pattern 3 — Number Triangle
source: https://takeuforward.org/learning/dsa/pattern-3?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 3. Pattern 3: Number Triangle

← [Pattern 2: Right-Angled Triangle](02-pattern-2.md) · [Part 4 index](README.md) · Next → [Pattern 4: Row-Number Triangle](04-pattern-4.md)

> [!abstract] What this covers
> **Core idea:** Same shape as pattern 2; the cell content is the column index j.
> **Shape:** row i prints 1 … i.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-3?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
1
1 2
1 2 3
1 2 3 4
1 2 3 4 5
```

n = 3 (use this for dry runs):
```text
1
1 2
1 2 3
```

Cells are separated by a space, as in Striver's reference output.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Cells | Content |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 1 2 |
| 3 | 3 | 1 2 3 |
| 4 | 4 | 1 2 3 4 |
| 5 | 5 | 1 2 3 4 5 |
| **Formula** | **i** | **j** |

---

## 3. Derivation

Shape first (it's pattern 2), then content: the value in column j is just `j`. This is the **separate shape from content** rule from [Part 3](../03-logic-building-patterns/01-easy-and-medium.md#5-what-goes-in-a-cell).

---

## 4. Code

**C++**
```cpp
void pattern3(int n) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) cout << j << " ";
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern3(int n) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) System.out.print(j + " ");
        System.out.println();
    }
}
```

**Python**
```python
def pattern3(n):
    for i in range(1, n + 1):
        print(" ".join(str(j) for j in range(1, i + 1)))
```

---

## 5. Complexity

| | |
|---|---|
| Time | O(n²) — proportional to the O(n²) characters printed |
| Extra space | O(1) in C++/Java; O(n) per row in Python (the row string is built before printing) |

**Edge cases:** n ≥ 10 → two-digit numbers break visual alignment; judges usually don't care.

---

## Common mistakes

1. Printing `i` instead of `j` → that's pattern 4.
2. Java: `j + ' '` (char) adds 32 to j; use `j + " "` (string).

---

## Practice

Print the triangle with each row reversed: 1, 2 1, 3 2 1.

<details><summary>Answer sketch</summary>

Inner loop `j = i` down to 1.
</details>

---

## Flashcards

**Pattern 3 cell content?** #flashcard
The column number `j`.

**Java trap when printing `j + ' '`?** #flashcard
char arithmetic: `' '` is 32, so it prints j + 32. Use a String `" "`.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
