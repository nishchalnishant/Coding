---
module: striver/04-patterns
lesson: 15
topic: Pattern 15 — Reverse Letter Triangle
source: https://takeuforward.org/learning/dsa/pattern-15?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 15. Pattern 15: Reverse Letter Triangle

← [Pattern 14: Letter Triangle](14-pattern-14.md) · [Part 4 index](README.md) · Next → [Pattern 16: Alpha-Ramp](16-pattern-16.md)

> [!abstract] What this covers
> **Core idea:** Pattern 14's content with pattern 5's shape: n − i + 1 letters per row.
> **Shape:** A B C D E / A B C D / ….
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-15?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
A B C D E
A B C D
A B C
A B
A
```

n = 3 (use this for dry runs):
```text
A B C
A B
A
```

Cells are separated by a space, as in Striver's reference output.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Cells | Last letter |
|---|---|---|
| 1 | 5 | E |
| 2 | 4 | D |
| 3 | 3 | C |
| 4 | 2 | B |
| 5 | 1 | A |
| **Formula** | **n − i + 1** | **'A' + n − i** |

---

## 3. Derivation

Inversion rule again: pattern 14's last letter was `'A' + i − 1`; substituting i → n − i + 1 gives `'A' + n − i`.

---

## 4. Code

**C++**
```cpp
void pattern15(int n) {
    for (int i = 1; i <= n; i++) {
        for (char ch = 'A'; ch <= 'A' + (n - i); ch++) cout << ch << " ";
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern15(int n) {
    for (int i = 1; i <= n; i++) {
        for (char ch = 'A'; ch <= 'A' + (n - i); ch++) System.out.print(ch + " ");
        System.out.println();
    }
}
```

**Python**
```python
def pattern15(n):
    for i in range(n, 0, -1):
        print(" ".join(chr(ord("A") + j) for j in range(i)))
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

1. `ch < 'A' + (n − i)` (strict) → each row one letter short.

---

## Practice

Rows end at E: A B C D E / B C D E / C D E …

<details><summary>Answer sketch</summary>

Start the char at `'A' + i − 1`, stop at `'A' + n − 1`.
</details>

---

## Flashcards

**Last letter in row i of pattern 15?** #flashcard
'A' + n − i.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
