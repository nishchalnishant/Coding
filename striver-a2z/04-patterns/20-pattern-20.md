---
module: striver-a2z/04-patterns
lesson: 20
topic: Pattern 20 — Symmetric Butterfly
source: https://takeuforward.org/learning/dsa/pattern-20?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 20. Pattern 20: Symmetric Butterfly

← [Pattern 19: Symmetric Void](19-pattern-19.md) · [Part 4 index](README.md) · Next → [Pattern 21: Hollow Rectangle](21-pattern-21.md)

> [!abstract] What this covers
> **Core idea:** 2n − 1 rows; stars s = i ≤ n ? i : 2n − i on each side, gap 2(n − s).
> **Shape:** wings of stars meeting in the middle row.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-20?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
*        *
**      **
***    ***
****  ****
**********
****  ****
***    ***
**      **
*        *
```

n = 3 (use this for dry runs):
```text
*    *
**  **
******
**  **
*    *
```

No separator between cells — the shape depends on exact column positions.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Stars each side (s) | Gap |
|---|---|---|
| 1 | 1 | 8 |
| 2 | 2 | 6 |
| 3 | 3 | 4 |
| 4 | 4 | 2 |
| 5 | 5 | 0 |
| 6 | 4 | 2 |
| 7 | 3 | 4 |
| 8 | 2 | 6 |
| 9 | 1 | 8 |
| **Formula** | **i ≤ n ? i : 2n − i** | **2(n − s)** |

---

## 3. Derivation

Compute the star count once per row with [pattern 10](10-pattern-10.md)'s piecewise bound, then derive the gap from the width invariant: s + gap + s = 2n → gap = 2(n − s). **Deriving one segment from another** removes half the formulas you have to get right.

---

## 4. Code

**C++**
```cpp
void pattern20(int n) {
    for (int i = 1; i <= 2 * n - 1; i++) {
        int s = (i <= n) ? i : 2 * n - i;
        for (int j = 0; j < s; j++) cout << '*';
        for (int j = 0; j < 2 * (n - s); j++) cout << ' ';
        for (int j = 0; j < s; j++) cout << '*';
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern20(int n) {
    for (int i = 1; i <= 2 * n - 1; i++) {
        int s = (i <= n) ? i : 2 * n - i;
        for (int j = 0; j < s; j++) System.out.print('*');
        for (int j = 0; j < 2 * (n - s); j++) System.out.print(' ');
        for (int j = 0; j < s; j++) System.out.print('*');
        System.out.println();
    }
}
```

**Python**
```python
def pattern20(n):
    for i in range(1, 2 * n):
        s = n - abs(n - i)
        print("*" * s + " " * (2 * (n - s)) + "*" * s)
```

---

## 5. Complexity

| | |
|---|---|
| Time | O(n²) — proportional to the O(n²) characters printed |
| Extra space | O(1) in C++/Java; O(n) per row in Python (the row string is built before printing) |

**Edge cases:** n = 1 → `**`.

---

## Common mistakes

1. Looping to 2n → an extra row of 0 stars and a full-width gap.
2. Writing a separate gap formula for each half and getting one wrong.

---

## Practice

Hollow butterfly: print only the outline of each wing.

<details><summary>Answer sketch</summary>

Within each wing, print `*` only at the first and last cell, or in the middle row.
</details>

---

## Flashcards

**Stars each side in butterfly row i?** #flashcard
s = i ≤ n ? i : 2n − i (= n − |n − i|).

**Gap in the butterfly?** #flashcard
2(n − s) — derived from the width 2n.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
