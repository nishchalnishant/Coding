---
module: striver-a2z/04-patterns
lesson: 5
topic: Pattern 5 — Inverted Right Triangle
source: https://takeuforward.org/learning/dsa/pattern-5?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 5. Pattern 5: Inverted Right Triangle

← [Pattern 4: Row-Number Triangle](04-pattern-4.md) · [Part 4 index](README.md) · Next → [Pattern 6: Inverted Number Triangle](06-pattern-6.md)

> [!abstract] What this covers
> **Core idea:** Inversion rule: replace i with n − i + 1 in pattern 2's bound.
> **Shape:** row i has n − i + 1 stars.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-5?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
* * * * *
* * * *
* * *
* *
*
```

n = 3 (use this for dry runs):
```text
* * *
* *
*
```

Cells are separated by a space, as in Striver's reference output.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Stars |
|---|---|
| 1 | 5 |
| 2 | 4 |
| 3 | 3 |
| 4 | 2 |
| 5 | 1 |
| **Formula** | **n − i + 1** |

---

## 3. Derivation

Two equivalent views: (a) keep i increasing and use the bound `n − i + 1`; (b) run i **downwards** from n to 1 and reuse pattern 2's bound `j ≤ i` (the Python version). View (a) generalises better when a row has several segments.

---

## 4. Code

**C++**
```cpp
void pattern5(int n) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n - i + 1; j++) cout << "* ";
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern5(int n) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n - i + 1; j++) System.out.print("* ");
        System.out.println();
    }
}
```

**Python**
```python
def pattern5(n):
    for i in range(n, 0, -1):
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

1. `n − i` with 1-based i → first row has n−1 stars, last row empty.

---

## Practice

Right-aligned inverted triangle.

<details><summary>Answer sketch</summary>

Spaces `i − 1`, stars `n − i + 1`.
</details>

---

## Flashcards

**Inversion rule?** #flashcard
Replace i with n − i + 1 (1-based) or n − 1 − i (0-based), or run i downwards.

**Pattern 5 bound with 0-based i?** #flashcard
`j < n − i`.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
