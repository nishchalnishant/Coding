---
module: striver/18-recursion
lesson: 15
topic: Letter Combinations of a Phone Number
difficulty: Medium
source: https://takeuforward.org/learning/dsa/letter-combinations-of-a-phone-number?category=hard&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, backtracking, string]
---
# 15. Letter Combinations of a Phone Number

← [Combination Sum III](14-combination-sum-iii.md) · [Part 18 index](README.md) · Next → [Palindrome Partitioning](16-palindrome-partitioning.md)

> [!abstract] Problem at a glance
> **Task:** Return every letter string a digit string (2–9) could represent on a phone keypad.
> **Key insight:** One recursion level per digit, one branch per letter of that digit — a Cartesian product. Depth = number of digits, branching ≤ 4, so O(4ⁿ · n). Empty input returns `[]`, not `[""]`.
> **Difficulty:** Medium · **Pattern:** Cartesian-product backtracking · **Also on:** [LC 17](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/letter-combinations-of-a-phone-number?category=hard&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Iterative expansion](#3-iterative-expansion) · [4. Backtracking per digit](#4-backtracking-per-digit) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a string of digits `2`–`9`, return all possible letter combinations that the number could represent (standard phone mapping: 2 → abc, 3 → def, 4 → ghi, 5 → jkl, 6 → mno, 7 → pqrs, 8 → tuv, 9 → wxyz). Return them in any order.

| Input | Output | Why |
|---|---|---|
| `digits = "23"` | `["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]` |  |
| `digits = ""` | `[]` |  |
| `digits = "2"` | `["a", "b", "c"]` |  |

**Constraints:** `0 ≤ len ≤ 4`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Iterative expansion | res = ['']; for each digit, extend every string by each letter | O(4ⁿ · n) | O(4ⁿ · n) |
| Backtracking per digit | go(i): for ch in map[digits[i]]: push, go(i + 1), pop | O(4ⁿ · n) | O(n) |

> [!tip] Interview angle
> Easy to code; the signals are the empty-input edge case, a fixed mapping array instead of a hash map, and stating the complexity with the 4-letter digits (7, 9) as worst case. The iterative BFS-style expansion is a good second version.

---

## 3. Iterative expansion

**Intuition.** Like the cascading power set: after processing i digits the list holds all combinations of those digits.

```python
def letters_iter(digits):
    if not digits:
        return []
    m = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    res = [""]
    for d in digits:
        res = [s + ch for s in res for ch in m[d]]
    return res
```

**Complexity:** time **O(4ⁿ · n)**, space **O(4ⁿ · n)**.

---

## 4. Backtracking per digit

**Intuition.** Recursion depth equals the number of digits; at depth i, try each letter mapped to `digits[i]`. Record at `i == n`.

**Dry run** — "23": a → ad, ae, af; b → bd, be, bf; c → cd, ce, cf.

**C++**
```cpp
void go(int i, const string& d, const vector<string>& m, string& cur, vector<string>& out) {
    if (i == (int)d.size()) { out.push_back(cur); return; }
    for (char ch : m[d[i] - '0']) {
        cur.push_back(ch);
        go(i + 1, d, m, cur, out);
        cur.pop_back();
    }
}
vector<string> letterCombinations(string digits) {
    if (digits.empty()) return {};
    vector<string> m = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
    vector<string> out;
    string cur;
    go(0, digits, m, cur, out);
    return out;
}
```

**Java**
```java
static final String[] M = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
static void go(int i, String d, StringBuilder cur, List<String> out) {
    if (i == d.length()) { out.add(cur.toString()); return; }
    for (char ch : M[d.charAt(i) - '0'].toCharArray()) {
        cur.append(ch);
        go(i + 1, d, cur, out);
        cur.deleteCharAt(cur.length() - 1);
    }
}
static List<String> letterCombinations(String digits) {
    List<String> out = new ArrayList<>();
    if (digits.isEmpty()) return out;
    go(0, digits, new StringBuilder(), out);
    return out;
}
```

**Python**
```python
def letter_combinations(digits):
    if not digits:
        return []
    m = ["", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"]
    out, cur = [], []
    def go(i):
        if i == len(digits):
            out.append("".join(cur))
            return
        for ch in m[int(digits[i])]:
            cur.append(ch)
            go(i + 1)
            cur.pop()
    go(0)
    return out
```

**Complexity:** time **O(4ⁿ · n)**, space **O(n)** — ≤ 4ⁿ leaves, O(n) each.

---

## Edge cases

- Empty string → `[]`.
- Digits 7 and 9 have 4 letters.

---

## Common mistakes

1. Returning `[""]` for empty input.
2. Using a `HashMap` per call instead of a constant array (minor, but noted).

---

## Follow-ups

1. Digits 0/1 allowed with no letters.
2. Only combinations that are dictionary words.

<details><summary>Answer sketches</summary>

**#1:** Skip them or treat as single fixed char — clarify.

**#2:** Walk a trie in lockstep and prune dead prefixes.
</details>

---

## Flashcards

**Letter combinations empty input?** #flashcard
Return [] (not [""]).

**Letter combinations complexity?** #flashcard
O(4ⁿ · n) worst case (digits 7/9).

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../coding/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../coding/algorithms/12-backtracking.md)
