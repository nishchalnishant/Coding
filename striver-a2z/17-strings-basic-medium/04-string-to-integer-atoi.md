---
module: striver-a2z/17-strings-basic-medium
lesson: 4
topic: String to Integer (atoi)
difficulty: Medium
source: https://takeuforward.org/learning/dsa/string-to-integer-atoi?category=conversions&source=strivers-a2z-dsa-sheet
tags: [striver, strings-basic-and-medium, string, parsing]
---
# 4. String to Integer (atoi)

← [Roman to Integer](03-roman-to-integer.md) · [Part 17 index](README.md) · Next → [Count Substrings with Exactly K Distinct Characters](05-count-substrings-k-distinct.md)

> [!abstract] Problem at a glance
> **Task:** Parse a 32-bit signed integer from a string following C `atoi` rules, clamping on overflow.
> **Key insight:** It's a 4-state machine: skip spaces → optional sign → digits → stop at the first non-digit. The only hard part is overflow, and you check it *before* `res = res·10 + d`.
> **Difficulty:** Medium · **Pattern:** Parsing state machine · **Also on:** [LC 8](https://leetcode.com/problems/string-to-integer-atoi/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/string-to-integer-atoi?category=conversions&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Wide accumulator, early stop](#3-wide-accumulator-early-stop) · [4. Recursive digit reader](#4-recursive-digit-reader) · [5. Iterative with pre-multiply overflow guard](#5-iterative-with-pre-multiply-overflow-guard) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Implement `myAtoi(s)`: (1) skip leading spaces, (2) read an optional `+` or `-`, (3) read digits until a non-digit or the end — leading zeros are fine, (4) no digits → 0, (5) clamp to `[−2³¹, 2³¹ − 1]`. Return the integer.

| Input | Output | Why |
|---|---|---|
| `s = "42"` | `42` |  |
| `s = "   -042"` | `-42` | spaces, sign, leading zero |
| `s = "1337c0d3"` | `1337` | stops at c |
| `s = "0-1"` | `0` | stops at - |
| `s = "words and 987"` | `0` | first non-space is not a digit or sign |
| `s = "-91283472332"` | `-2147483648` | clamped |

**Constraints:** `0 ≤ |s| ≤ 200`, `s` has letters, digits, `' '`, `+`, `-`, `.`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Wide accumulator, early stop | accumulate in Python int / long, clamp as soon as it leaves range | O(n) | O(1) |
| Recursive digit reader | read(i, acc) recurses on the next digit | O(n) | O(n) stack |
| Iterative with pre-multiply overflow guard | if res > (MAX − d) / 10 → clamp | O(n) | O(1) |

> [!tip] Interview angle
> A favourite because the spec is the test: interviewers want you to list the cases (spaces, sign, leading zeros, junk, empty, overflow both ways, `"+-1"`) *before* coding. In C++/Java show the overflow guard without a wider type; mention a `long` accumulator is acceptable only if you stop as soon as it exceeds the range.

---

## 3. Wide accumulator, early stop

**Intuition.** Use an integer wider than 32 bits; after each digit, if `res > 2³¹` stop and clamp. Simple, but in Java/C++ an unbounded digit string would overflow even a `long` without the early stop.

```python
def atoi_wide(s):
    i, n = 0, len(s)
    while i < n and s[i] == ' ':
        i += 1
    sign = 1
    if i < n and s[i] in '+-':
        sign = -1 if s[i] == '-' else 1
        i += 1
    res = 0
    while i < n and s[i].isdigit():
        res = res * 10 + int(s[i])
        if res > 2**31:
            break
        i += 1
    return max(-2**31, min(2**31 - 1, sign * res))
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Recursive digit reader

**Intuition.** Striver's recursion-practice framing: after the sign, `read(i, acc)` returns `acc` when `s[i]` isn't a digit, otherwise recurses with `acc·10 + d`, clamping on the way. Good for practising base cases, worse in production (stack depth).

```python
def atoi_rec(s):
    i, n = 0, len(s)
    while i < n and s[i] == ' ':
        i += 1
    sign = 1
    if i < n and s[i] in '+-':
        sign = -1 if s[i] == '-' else 1
        i += 1
    LIM = 2**31 if sign < 0 else 2**31 - 1
    def read(j, acc):
        if j == n or not s[j].isdigit():
            return acc
        acc = acc * 10 + int(s[j])
        return LIM if acc >= LIM else read(j + 1, acc)
    return sign * read(i, 0)
```

**Complexity:** time **O(n)**, space **O(n) stack**.

---

## 5. Iterative with pre-multiply overflow guard

**Intuition.** Keep `res` as a non-negative 32-bit int. Before `res·10 + d`, check `res > (INT_MAX − d) / 10`: if true, the next value exceeds INT_MAX, so return INT_MAX for `+` and INT_MIN for `−`. Returning INT_MIN for every negative overflow is right because −(INT_MAX + 1) = INT_MIN is the clamp anyway.

**Algorithm**

1. Skip spaces.
2. Read one sign char if present.
3. While digit: guard overflow, then `res = res·10 + d`.
4. Return `sign · res`.

**Dry run** — `"   -042"`: skip 3 spaces; sign −1; 0 → 0; 4 → 4; 2 → 42; end → −42.

**C++**
```cpp
int myAtoi(string s) {
    int i = 0, n = s.size(), sign = 1, res = 0;
    while (i < n && s[i] == ' ') i++;
    if (i < n && (s[i] == '+' || s[i] == '-')) sign = (s[i++] == '-') ? -1 : 1;
    while (i < n && isdigit(s[i])) {
        int d = s[i++] - '0';
        if (res > (INT_MAX - d) / 10) return sign == 1 ? INT_MAX : INT_MIN;
        res = res * 10 + d;
    }
    return sign * res;
}
```

**Java**
```java
static int myAtoi(String s) {
    int i = 0, n = s.length(), sign = 1, res = 0;
    while (i < n && s.charAt(i) == ' ') i++;
    if (i < n && (s.charAt(i) == '+' || s.charAt(i) == '-')) sign = (s.charAt(i++) == '-') ? -1 : 1;
    while (i < n && Character.isDigit(s.charAt(i))) {
        int d = s.charAt(i++) - '0';
        if (res > (Integer.MAX_VALUE - d) / 10) return sign == 1 ? Integer.MAX_VALUE : Integer.MIN_VALUE;
        res = res * 10 + d;
    }
    return sign * res;
}
```

**Python**
```python
def my_atoi(s):
    INT_MAX, INT_MIN = 2**31 - 1, -2**31
    i, n, sign, res = 0, len(s), 1, 0
    while i < n and s[i] == ' ':
        i += 1
    if i < n and s[i] in '+-':
        sign = -1 if s[i] == '-' else 1
        i += 1
    while i < n and s[i].isdigit():
        d = ord(s[i]) - 48
        if res > (INT_MAX - d) // 10:
            return INT_MAX if sign == 1 else INT_MIN
        res = res * 10 + d
        i += 1
    return sign * res
```

**Complexity:** time **O(n)**, space **O(1)** — each char visited once; the guard keeps `res` in range, so no wider type is needed.

---

## Edge cases

- Empty / all spaces → 0.
- Sign with no digits (`"-"`, `"+-1"`) → 0.
- Exactly INT_MAX, INT_MAX + 1, INT_MIN.
- Many leading zeros — they must not trigger overflow.
- Junk right after digits.

---

## Common mistakes

1. `res * 10 + d` then checking — the overflow already happened (UB in C++).
2. Accepting two signs, or a sign after spaces after digits.
3. Skipping all whitespace with `isspace` when the spec says only `' '`.
4. Using `Integer.parseInt` — throws instead of clamping.

---

## Follow-ups

1. Parse a double / scientific notation (LC 65 Valid Number).
2. Return an error instead of clamping.
3. Implement `itoa`.

<details><summary>Answer sketches</summary>

**#1:** Extend the state machine: digits → `.` → digits → `e/E` → sign → digits; write it as a transition table.

**#2:** Return `(ok, value)`; `ok = false` on no digits or overflow.

**#3:** Repeated `% 10` / `/ 10`, handle 0 and INT_MIN (can't negate in 32 bits).
</details>

---

## Flashcards

**atoi overflow guard without a long?** #flashcard
Before res = res·10 + d, if res > (INT_MAX − d)/10 → clamp.

**atoi states?** #flashcard
Spaces → optional sign → digits → stop at first non-digit.

**Why is INT_MIN fine as the negative clamp?** #flashcard
Magnitude INT_MAX + 1 overflows the positive accumulator, and any larger magnitude clamps to INT_MIN anyway.

**Interview track →** [Strings deep-dive](../../01-data-structures/03-string.md) · [String walkthroughs](../../04-practice/data-structures/03-string.md) · [Sliding window](../../02-algorithms/04-sliding-window.md)
