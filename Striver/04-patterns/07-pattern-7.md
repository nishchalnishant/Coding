---
module: striver/04-patterns
lesson: 7
topic: Pattern 7 — Star Pyramid
source: https://takeuforward.org/learning/dsa/pattern-7?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 7. Pattern 7: Star Pyramid

← [Pattern 6: Inverted Number Triangle](06-pattern-6.md) · [Part 4 index](README.md) · Next → [Pattern 8: Inverted Star Pyramid](08-pattern-8.md)

> [!abstract] What this covers
> **Core idea:** Two segments per row: leading spaces (n − i) then stars (2i − 1); width stays 2n − 1.
> **Shape:** centred pyramid: n − i spaces, 2i − 1 stars.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-7?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

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
```

n = 3 (use this for dry runs):
```text
  *
 ***
*****
```

No separator between cells — the shape depends on exact column positions.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Spaces | Stars |
|---|---|---|
| 1 | 4 | 1 |
| 2 | 3 | 3 |
| 3 | 2 | 5 |
| 4 | 1 | 7 |
| 5 | 0 | 9 |
| **Formula** | **n − i** | **2i − 1** |

---

## 3. Derivation

Stars grow by 2 per row (1, 3, 5 …) → `2i − 1`. Spaces shrink by 1 → `n − i`. Width check: (n − i) + (2i − 1) + (n − i) = 2n − 1 for every row ✅. Striver's code also prints the trailing `n − i` spaces; they're invisible and optional.

---

## 4. Code

**C++**
```cpp
void pattern7(int n) {
    for (int i = 1; i <= n; i++) {
        for (int s = 0; s < n - i; s++) cout << ' ';
        for (int j = 0; j < 2 * i - 1; j++) cout << '*';
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern7(int n) {
    for (int i = 1; i <= n; i++) {
        for (int s = 0; s < n - i; s++) System.out.print(' ');
        for (int j = 0; j < 2 * i - 1; j++) System.out.print('*');
        System.out.println();
    }
}
```

**Python**
```python
def pattern7(n):
    for i in range(1, n + 1):
        print(" " * (n - i) + "*" * (2 * i - 1))
```

---

## 5. Complexity

| | |
|---|---|
| Time | O(n²) — proportional to the O(n²) characters printed |
| Extra space | O(1) in C++/Java; O(n) per row in Python (the row string is built before printing) |

**Edge cases:** n = 1 → `*` with no spaces.

---

## Common mistakes

1. Stars `2(i − 1)` → 0, 2, 4 … (lopsided).
2. Printing `"* "` (star + space) doubles the width and breaks centring.

---

## Practice

Number pyramid: row i prints 1 … 2i − 1.

<details><summary>Answer sketch</summary>

Replace `*` with the running column index.
</details>

---

## Flashcards

**Spaces and stars in pyramid row i (1-based)?** #flashcard
Spaces n − i, stars 2i − 1.

**Width invariant of the pyramid?** #flashcard
2n − 1 for every row (including trailing spaces).

**0-based version?** #flashcard
Spaces n − i − 1, stars 2i + 1.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
