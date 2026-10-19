---
module: striver/17-strings-basic-medium
lesson: 3
topic: Roman to Integer
difficulty: Easy
source: https://takeuforward.org/learning/dsa/roman-to-integer?category=conversions&source=strivers-a2z-dsa-sheet
tags: [striver, strings-basic-and-medium, string, hashing, math]
---
# 3. Roman to Integer

← [Maximum Nesting Depth of the Parentheses](02-maximum-nesting-depth-of-the-parentheses.md) · [Part 17 index](README.md) · Next → [String to Integer (atoi)](04-string-to-integer-atoi.md)

> [!abstract] Problem at a glance
> **Task:** Convert a Roman numeral (1 to 3999) to an integer.
> **Key insight:** Add each symbol's value, except when it's smaller than the next symbol — then subtract it (IV = −1 + 5). Only six such pairs exist, and the rule covers all of them.
> **Difficulty:** Easy · **Pattern:** Lookup table + look-ahead · **Also on:** [LC 13](https://leetcode.com/problems/roman-to-integer/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/roman-to-integer?category=conversions&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Match two-char pairs first](#3-match-two-char-pairs-first) · [4. Subtract if smaller than the next](#4-subtract-if-smaller-than-the-next) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Roman numerals use `I=1, V=5, X=10, L=50, C=100, D=500, M=1000`, written largest to smallest left to right. Six subtractive forms exist: `IV=4, IX=9, XL=40, XC=90, CD=400, CM=900`. Given a valid numeral `s`, return its value.

| Input | Output | Why |
|---|---|---|
| `s = "III"` | `3` |  |
| `s = "LVIII"` | `58` | L + V + III |
| `s = "MCMXCIV"` | `1994` | M + CM + XC + IV |

**Constraints:** `1 ≤ |s| ≤ 15`, `s` is a valid Roman numeral in `[1, 3999]`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Match two-char pairs first | check 2-char subtractive forms, else 1 char | O(n) | O(1) |
| Subtract if smaller than the next | v < next → total −= v else total += v | O(n) | O(1) |

> [!tip] Interview angle
> Easy, but they watch whether you hard-code six special cases or find the general rule. State the rule: a symbol is subtracted iff a larger symbol follows it. Be ready for the reverse (LC 12, integer to Roman, greedy over 13 values).

---

## 3. Match two-char pairs first

**Intuition.** At each index, if `s[i:i+2]` is one of the six pairs, add its value and skip 2; otherwise add `s[i]` and skip 1. Correct, but needs a second table.

```python
def roman_pairs(s):
    one = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    two = {'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900}
    i = total = 0
    while i < len(s):
        if s[i:i + 2] in two:
            total += two[s[i:i + 2]]
            i += 2
        else:
            total += one[s[i]]
            i += 1
    return total
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Subtract if smaller than the next

**Intuition.** Valid numerals are non-increasing except at the six pairs, where a smaller symbol precedes a larger one. So `value(s[i]) < value(s[i+1])` exactly identifies a subtracted symbol.

**Dry run** — `MCMXCIV`: M +1000; C < M −100; M +1000; X < C −10; C +100; I < V −1; V +5 → 1994.

**Right-to-left variant:** keep `prev`; if `v < prev` subtract else add. Same rule, no look-ahead index.

**C++**
```cpp
int romanToInt(string s) {
    unordered_map<char, int> v = {{'I', 1}, {'V', 5}, {'X', 10}, {'L', 50},
                                  {'C', 100}, {'D', 500}, {'M', 1000}};
    int total = 0, n = s.size();
    for (int i = 0; i < n; i++) {
        if (i + 1 < n && v[s[i]] < v[s[i + 1]]) total -= v[s[i]];
        else total += v[s[i]];
    }
    return total;
}
```

**Java**
```java
static int romanToInt(String s) {
    java.util.Map<Character, Integer> v = java.util.Map.of('I', 1, 'V', 5, 'X', 10,
            'L', 50, 'C', 100, 'D', 500, 'M', 1000);
    int total = 0, n = s.length();
    for (int i = 0; i < n; i++) {
        int cur = v.get(s.charAt(i));
        if (i + 1 < n && cur < v.get(s.charAt(i + 1))) total -= cur;
        else total += cur;
    }
    return total;
}
```

**Python**
```python
def roman_to_int(s):
    v = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for i, c in enumerate(s):
        if i + 1 < len(s) and v[c] < v[s[i + 1]]:
            total -= v[c]
        else:
            total += v[c]
    return total
```

**Complexity:** time **O(n)**, space **O(1)** — ≤ 15 chars, constant table.

---

## Edge cases

- Single symbol.
- Subtractive pair at the end (`…IV`).
- Max value `MMMCMXCIX`.

---

## Common mistakes

1. Reading `s[i + 1]` without the bounds check.
2. Hard-coding six `if`s and missing one.
3. Assuming input validation is required — the problem guarantees validity.

---

## Follow-ups

1. Integer to Roman (LC 12).
2. Validate the numeral.

<details><summary>Answer sketches</summary>

**#1:** Greedy over `[1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]`, subtract while possible.

**#2:** Regex `^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$`.
</details>

---

## Flashcards

**Roman subtraction rule?** #flashcard
Subtract a symbol iff the next symbol is larger; otherwise add.

**The six subtractive pairs?** #flashcard
IV, IX, XL, XC, CD, CM — only I, X, C are ever subtracted, and only from the next two larger symbols.

**Interview track →** [Strings deep-dive](../../01-data-structures/03-string.md) · [String walkthroughs](../../coding/data-structures/03-string.md) · [Sliding window](../../02-algorithms/04-sliding-window.md)
