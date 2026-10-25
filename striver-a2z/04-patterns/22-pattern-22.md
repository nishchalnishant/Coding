---
module: striver-a2z/04-patterns
lesson: 22
topic: Pattern 22 — Concentric Number Square
source: https://takeuforward.org/learning/dsa/pattern-22?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 22. Pattern 22: Concentric Number Square

← [Pattern 21: Hollow Rectangle](21-pattern-21.md) · [Part 4 index](README.md) · Next → [Part 5: Time Complexity](../05-time-complexity/README.md)

> [!abstract] What this covers
> **Core idea:** Cell value = n − min(distance to top, left, bottom, right).
> **Shape:** rings n, n − 1, … 1 on a (2n − 1)² grid.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-22?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
555555555
544444445
543333345
543222345
543212345
543222345
543333345
544444445
555555555
```

n = 3 (use this for dry runs):
```text
33333
32223
32123
32223
33333
```

No separator between cells — the shape depends on exact column positions.

---

## 2. Row table

Ring table for n = 5 (side S = 9):

| Ring d (distance to nearest edge) | Cells on ring | Value printed |
|---|---|---|
| 0 | 32 | 5 |
| 1 | 24 | 4 |
| 2 | 16 | 3 |
| 3 | 8 | 2 |
| 4 | 1 | 1 |
| **Formula** | 4(S − 2d − 1), centre 1 | **n − d** |

---

## 3. Derivation

Row tables fail here — every row is different and non-monotone. Switch to a **per-cell** view. Ring 0 is the border, ring 1 the next square in, … A cell's ring is its distance to the nearest edge: `d = min(i, j, size − 1 − i, size − 1 − j)`. The value printed is `n − d`. Equivalent: `1 + max(|i − c|, |j − c|)` with centre c = n − 1 (Chebyshev distance). See [Part 3 Hard §6](../03-logic-building-patterns/02-hard.md#6-distance-formulas-the-grid-view).

---

## 4. Code

**C++**
```cpp
void pattern22(int n) {
    int size = 2 * n - 1;
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            int top = i, left = j, bottom = size - 1 - i, right = size - 1 - j;
            cout << n - min(min(top, bottom), min(left, right));
        }
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern22(int n) {
    int size = 2 * n - 1;
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            int top = i, left = j, bottom = size - 1 - i, right = size - 1 - j;
            System.out.print(n - Math.min(Math.min(top, bottom), Math.min(left, right)));
        }
        System.out.println();
    }
}
```

**Python**
```python
def pattern22(n):
    size = 2 * n - 1
    for i in range(size):
        print("".join(str(n - min(i, j, size - 1 - i, size - 1 - j)) for j in range(size)))
```

---

## 5. Complexity

| | |
|---|---|
| Time | O(n²) — proportional to the (2n − 1)² digits printed |
| Extra space | O(1) in C++/Java; O(n) per row in Python (the row string is built before printing) |

**Edge cases:** n = 1 → `1`. n ≥ 10 → two-digit values break alignment.

---

## Common mistakes

1. Grid of side 2n instead of 2n − 1 → no single centre cell.
2. Using max instead of min for edge distances → inverted rings.

---

## Practice

Make the centre n and the border 1.

<details><summary>Answer sketch</summary>

Print `d + 1` instead of `n − d`.
</details>

---

## Flashcards

**Value of cell (i, j) in the concentric square?** #flashcard
n − min(i, j, size−1−i, size−1−j) with size = 2n − 1.

**Alternative distance formula?** #flashcard
1 + max(|i − c|, |j − c|) where c = n − 1 — Chebyshev distance from the centre.

**Why can't a row table solve this cleanly?** #flashcard
Each row is non-monotone (falls then rises), so a per-cell formula is simpler.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
