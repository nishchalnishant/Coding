---
module: striver/18-recursion
lesson: 22
topic: Expression Add Operators
difficulty: Hard
source: https://takeuforward.org/learning/dsa/expression-add-operators?category=faqs-hard&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, backtracking, string, math]
---
# 22. Expression Add Operators

← [Sudoku Solver](21-sudoku-solver.md) · [Part 18 index](README.md) · Next → [Sort a stack using recursion](23-sort-a-stack-using-recursion.md)

> [!abstract] Problem at a glance
> **Task:** Insert `+`, `−`, `*` between the digits of a string so the expression evaluates to `target`; return all such expressions.
> **Key insight:** Backtrack over the next operand `num[i..j]` and its operator, carrying `value` (total so far) and `last` (the last multiplicative term). For `*`, undo the last term: `value − last + last·x`, new `last = last·x`. Skip operands with a leading zero.
> **Difficulty:** Hard · **Pattern:** Backtracking with an expression-evaluation state · **Also on:** [LC 282](https://leetcode.com/problems/expression-add-operators/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/expression-add-operators?category=faqs-hard&source=strivers-a2z-dsa-sheet) · **Time:** 30 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Generate all expressions, evaluate each](#3-generate-all-expressions-evaluate-each) · [4. Backtracking with value and last term](#4-backtracking-with-value-and-last-term) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a digit string `num` and an integer `target`, return all possibilities to insert the binary operators `'+'`, `'-'` and/or `'*'` between the digits so that the resulting expression evaluates to `target`. Operands may not have leading zeros (`"05"` is invalid, `"0"` is fine). Any order.

| Input | Output | Why |
|---|---|---|
| `num = "123", target = 6` | `["1*2*3", "1+2+3"]` |  |
| `num = "232", target = 8` | `["2*3+2", "2+3*2"]` |  |
| `num = "3456237490", target = 9191` | `[]` |  |

**Constraints:** `1 ≤ |num| ≤ 10`, `−2³¹ ≤ target ≤ 2³¹ − 1`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Generate all expressions, evaluate each | 4ⁿ⁻¹ operator strings (incl. concatenation), eval | O(n · 4ⁿ) | O(n) |
| Backtracking with value and last term | go(i, value, last): pick operand num[i..j], try +, −, * | O(n · 4ⁿ) | O(n) |

> [!tip] Interview angle
> The hard part is precedence: you can't evaluate left to right once `*` appears. Explain the `last` operand trick before coding. Use 64-bit values (10-digit operands overflow int), and note the cost: 4ⁿ⁻¹ operator choices × O(n) string building.

---

## 3. Generate all expressions, evaluate each

**Intuition.** Choose one of {none, +, −, *} between each pair of digits, reject leading-zero operands, and evaluate with precedence. Correct; re-parses every expression from scratch.

```python
from itertools import product as _p
def add_ops_eval(num, target):
    out = []
    for ops in _p(["", "+", "-", "*"], repeat=len(num) - 1):
        expr = num[0] + "".join(o + d for o, d in zip(ops, num[1:]))
        toks = expr.replace("+", " ").replace("-", " ").replace("*", " ").split()
        if any(len(t) > 1 and t[0] == "0" for t in toks):
            continue
        if eval(expr) == target:
            out.append(expr)
    return out
```

**Complexity:** time **O(n · 4ⁿ)**, space **O(n)**.

---

## 4. Backtracking with value and last term

**Intuition.** Maintain the evaluated value incrementally. `+x`: value + x, last = x. `−x`: value − x, last = −x. `*x`: value − last + last·x, last = last·x (so `2+3*4` becomes 5 − 3 + 12 = 14). The first operand has no operator. Break the operand loop when it starts with `0` and has length > 1.

**Algorithm**

1. `go(i, expr, value, last)`: if i == n → record expr if value == target.
2. For j = i … n−1: if j > i and num[i] == '0' break; x = int(num[i..j]).
3. If i == 0: go(j+1, s, x, x). Else try +, −, * with the updates above.

**Dry run** — "232", 8: 2 → +3 (v 5, last 3) → *2 (v 5 − 3 + 6 = 8) ✓ "2+3*2"; 2 → *3 (v 6, last 6) → +2 (v 8) ✓ "2*3+2".

**C++**
```cpp
void go(const string& num, long long target, int i, string expr, long long value, long long last, vector<string>& out) {
    int n = num.size();
    if (i == n) { if (value == target) out.push_back(expr); return; }
    for (int j = i; j < n; j++) {
        if (j > i && num[i] == '0') break;
        string s = num.substr(i, j - i + 1);
        long long x = stoll(s);
        if (i == 0) { go(num, target, j + 1, s, x, x, out); continue; }
        go(num, target, j + 1, expr + "+" + s, value + x, x, out);
        go(num, target, j + 1, expr + "-" + s, value - x, -x, out);
        go(num, target, j + 1, expr + "*" + s, value - last + last * x, last * x, out);
    }
}
vector<string> addOperators(string num, int target) {
    vector<string> out;
    go(num, target, 0, "", 0, 0, out);
    return out;
}
```

**Java**
```java
static void go(String num, long target, int i, String expr, long value, long last, List<String> out) {
    int n = num.length();
    if (i == n) { if (value == target) out.add(expr); return; }
    for (int j = i; j < n; j++) {
        if (j > i && num.charAt(i) == '0') break;
        String s = num.substring(i, j + 1);
        long x = Long.parseLong(s);
        if (i == 0) { go(num, target, j + 1, s, x, x, out); continue; }
        go(num, target, j + 1, expr + "+" + s, value + x, x, out);
        go(num, target, j + 1, expr + "-" + s, value - x, -x, out);
        go(num, target, j + 1, expr + "*" + s, value - last + last * x, last * x, out);
    }
}
static List<String> addOperators(String num, int target) {
    List<String> out = new ArrayList<>();
    go(num, target, 0, "", 0, 0, out);
    return out;
}
```

**Python**
```python
def add_operators(num, target):
    n, out = len(num), []
    def go(i, expr, value, last):
        if i == n:
            if value == target:
                out.append(expr)
            return
        for j in range(i, n):
            if j > i and num[i] == "0":
                break
            s = num[i:j + 1]
            x = int(s)
            if i == 0:
                go(j + 1, s, x, x)
                continue
            go(j + 1, expr + "+" + s, value + x, x)
            go(j + 1, expr + "-" + s, value - x, -x)
            go(j + 1, expr + "*" + s, value - last + last * x, last * x)
    go(0, "", 0, 0)
    return out
```

**Complexity:** time **O(n · 4ⁿ)**, space **O(n)** — ≤ 4ⁿ⁻¹ expressions, O(n) to build each.

---

## Edge cases

- Leading zeros: "105" allows `1*0+5`, `10-5`, not `1*05`.
- "00" with target 0 → `0+0`, `0-0`, `0*0`.
- 10-digit operand overflows 32-bit.

---

## Common mistakes

1. Evaluating left to right — `2+3*2` would give 10.
2. Allowing operand `"05"`.
3. Using int for operands/values.
4. Putting an operator before the first operand.

---

## Follow-ups

1. Add parentheses — all results (LC 241).
2. Only `+`/`−` with all digits as separate numbers (Target Sum).

<details><summary>Answer sketches</summary>

**#1:** Divide and conquer on each operator; memoise substrings.

**#2:** Subset-sum counting DP.
</details>

---

## Flashcards

**Expression Add Operators `*` update?** #flashcard
value − last + last·x; last = last·x.

**Leading-zero rule in operand loop?** #flashcard
If num[i] == '0', only the single-digit operand "0" is allowed (break when j > i).

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../coding/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../coding/algorithms/12-backtracking.md)
