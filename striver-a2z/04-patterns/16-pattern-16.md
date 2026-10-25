---
module: striver-a2z/04-patterns
lesson: 16
topic: Pattern 16 — Alpha-Ramp
source: https://takeuforward.org/learning/dsa/pattern-16?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 16. Pattern 16: Alpha-Ramp

← [Pattern 15: Reverse Letter Triangle](15-pattern-15.md) · [Part 4 index](README.md) · Next → [Pattern 17: Alpha-Hill](17-pattern-17.md)

> [!abstract] What this covers
> **Core idea:** Pattern 4 with letters: row i repeats 'A' + i − 1, i times.
> **Shape:** A / B B / C C C.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-16?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
A
B B
C C C
D D D D
E E E E E
```

n = 3 (use this for dry runs):
```text
A
B B
C C C
```

Cells are separated by a space, as in Striver's reference output.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Cells | Letter |
|---|---|---|
| 1 | 1 | A |
| 2 | 2 | B |
| 3 | 3 | C |
| 4 | 4 | D |
| 5 | 5 | E |
| **Formula** | **i** | **'A' + i − 1** |

---

## 3. Derivation

The letter depends on the row only, so compute it once per row (outside the inner loop). Patterns 14 ↔ 16 mirror patterns 3 ↔ 4: column-driven vs row-driven content.

---

## 4. Code

**C++**
```cpp
void pattern16(int n) {
    for (int i = 1; i <= n; i++) {
        char ch = 'A' + i - 1;
        for (int j = 1; j <= i; j++) cout << ch << " ";
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern16(int n) {
    for (int i = 1; i <= n; i++) {
        char ch = (char) ('A' + i - 1);
        for (int j = 1; j <= i; j++) System.out.print(ch + " ");
        System.out.println();
    }
}
```

**Python**
```python
def pattern16(n):
    for i in range(1, n + 1):
        ch = chr(ord("A") + i - 1)
        print(" ".join([ch] * i))
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

1. Java `char ch = 'A' + i - 1;` doesn't compile (int → char narrowing); cast it.

---

## Practice

Row i repeats the letter `'A' + n − i` (E / D D / C C C …).

<details><summary>Answer sketch</summary>

Change the content formula only.
</details>

---

## Flashcards

**Content of row i in the alpha-ramp?** #flashcard
'A' + i − 1, repeated i times.

**Why does Java need `(char)` here but not in `for (char ch = 'A'; …; ch++)`?** #flashcard
`'A' + i − 1` is an int expression; `ch++` is a compound op with an implicit cast.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
