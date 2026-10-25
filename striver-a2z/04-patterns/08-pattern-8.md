---
module: striver-a2z/04-patterns
lesson: 8
topic: Pattern 8 — Inverted Star Pyramid
source: https://takeuforward.org/learning/dsa/pattern-8?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 8. Pattern 8: Inverted Star Pyramid

← [Pattern 7: Star Pyramid](07-pattern-7.md) · [Part 4 index](README.md) · Next → [Pattern 9: Diamond](09-pattern-9.md)

> [!abstract] What this covers
> **Core idea:** Pattern 7 with i → n − i + 1: spaces grow, stars shrink by 2.
> **Shape:** i − 1 spaces, 2(n − i) + 1 stars.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-8?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
*********
 *******
  *****
   ***
    *
```

n = 3 (use this for dry runs):
```text
*****
 ***
  *
```

No separator between cells — the shape depends on exact column positions.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Spaces | Stars |
|---|---|---|
| 1 | 0 | 9 |
| 2 | 1 | 7 |
| 3 | 2 | 5 |
| 4 | 3 | 3 |
| 5 | 4 | 1 |
| **Formula** | **i − 1** | **2(n − i) + 1** |

---

## 3. Derivation

Apply the inversion rule to pattern 7: spaces `n − (n − i + 1) = i − 1`, stars `2(n − i + 1) − 1 = 2(n − i) + 1`. No new thinking — algebra on a solved pattern.

---

## 4. Code

**C++**
```cpp
void pattern8(int n) {
    for (int i = 1; i <= n; i++) {
        for (int s = 0; s < i - 1; s++) cout << ' ';
        for (int j = 0; j < 2 * (n - i) + 1; j++) cout << '*';
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern8(int n) {
    for (int i = 1; i <= n; i++) {
        for (int s = 0; s < i - 1; s++) System.out.print(' ');
        for (int j = 0; j < 2 * (n - i) + 1; j++) System.out.print('*');
        System.out.println();
    }
}
```

**Python**
```python
def pattern8(n):
    for i in range(1, n + 1):
        print(" " * (i - 1) + "*" * (2 * (n - i) + 1))
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

1. Stars `2(n − i)` → even counts; the top row is one short.

---

## Practice

Print pattern 7 and 8 back to back.

<details><summary>Answer sketch</summary>

That's pattern 9.
</details>

---

## Flashcards

**Inverted pyramid formulas (1-based)?** #flashcard
Spaces i − 1, stars 2(n − i) + 1.

**How do you derive pattern 8 from pattern 7?** #flashcard
Substitute i → n − i + 1 into both formulas.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
