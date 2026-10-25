---
module: striver-a2z/04-patterns
lesson: 18
topic: Pattern 18 — Alpha-Triangle
source: https://takeuforward.org/learning/dsa/pattern-18?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 18. Pattern 18: Alpha-Triangle

← [Pattern 17: Alpha-Hill](17-pattern-17.md) · [Part 4 index](README.md) · Next → [Pattern 19: Symmetric Void](19-pattern-19.md)

> [!abstract] What this covers
> **Core idea:** Row i starts at 'A' + n − i and runs up to 'A' + n − 1.
> **Shape:** E / D E / C D E — each row ends at the n-th letter.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-18?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
E
D E
C D E
B C D E
A B C D E
```

n = 3 (use this for dry runs):
```text
C
B C
A B C
```

Cells are separated by a space, as in Striver's reference output.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Cells | First letter | Last letter |
|---|---|---|---|
| 1 | 1 | E | E |
| 2 | 2 | D | E |
| 3 | 3 | C | E |
| 4 | 4 | B | E |
| 5 | 5 | A | E |
| **Formula** | **i** | **'A' + n − i** | **'A' + n − 1** |

---

## 3. Derivation

Two observations from the row table: every row **ends** at the same letter, and the start moves back one letter per row. So the loop runs from `'A' + n − i` to `'A' + n − 1` — a loop with a **moving start** rather than a moving end.

---

## 4. Code

**C++**
```cpp
void pattern18(int n) {
    for (int i = 1; i <= n; i++) {
        for (char ch = 'A' + n - i; ch <= 'A' + n - 1; ch++) cout << ch << " ";
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern18(int n) {
    for (int i = 1; i <= n; i++) {
        for (char ch = (char) ('A' + n - i); ch <= 'A' + n - 1; ch++) System.out.print(ch + " ");
        System.out.println();
    }
}
```

**Python**
```python
def pattern18(n):
    for i in range(1, n + 1):
        print(" ".join(chr(ord("A") + c) for c in range(n - i, n)))
```

---

## 5. Complexity

| | |
|---|---|
| Time | O(n²) — proportional to the O(n²) characters printed |
| Extra space | O(1) in C++/Java; O(n) per row in Python (the row string is built before printing) |

**Edge cases:** n = 1 → `A`.

---

## Common mistakes

1. Starting at `'E'` hard-coded → only correct for n = 5.

---

## Practice

Print the rows reversed: E / E D / E D C.

<details><summary>Answer sketch</summary>

Loop from `'A' + n − 1` down to `'A' + n − i`.
</details>

---

## Flashcards

**Loop range for row i of the alpha-triangle?** #flashcard
From 'A' + n − i up to 'A' + n − 1 (moving start, fixed end).

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
