---
module: striver/30-strings-advanced
lesson: 6
topic: Z-function
difficulty: Hard
source: https://takeuforward.org/learning/dsa/z-function?category=advanced-problems-(less-asked)&source=strivers-a2z-dsa-sheet
tags: [striver, strings--advanced-algo, string, z-function, pattern-matching]
---
# 6. Z-function

← [Rabin-Karp algorithm](05-rabin-karp-algorithm.md) · [Part 30 index](README.md) · Next → [KMP algorithm (LPS array)](07-kmp-algorithm-lps-array.md)

> [!abstract] Problem at a glance
> **Task:** Find all occurrences of `pat` in `text` with the Z-algorithm on `pat + '#' + text`.
> **Key insight:** `z[i]` is the length of the longest substring starting at `i` that matches a **prefix** of the string. The algorithm keeps the rightmost matched window `[l, r)`. Inside it, `z[i]` starts at `min(r − i, z[i − l])` for free, so `r` only ever moves right, which gives O(n) total. On `pat#text`, the pattern occurs wherever `z[i] == |pat|`.
> **Difficulty:** Hard · **Pattern:** Z-box (rightmost prefix-match window) · **Also on:** [CP-algorithms](https://cp-algorithms.com/string/z-function.html)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/z-function?category=advanced-problems-(less-asked)&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Naive Z-array](#3-naive-z-array) · [4. Linear Z-algorithm](#4-linear-z-algorithm) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `text` and `pat`, return the 0-based start indices of every occurrence of `pat` in `text`, using the Z-function. (`z[0]` is defined as 0.)

| Input | Output | Why |
|---|---|---|
| `text = "xabcabzabc", pat = "abc"` | `[1, 7]` |  |
| `text = "aaaaa", pat = "aa"` | `[0, 1, 2, 3]` |  |

**Constraints:** `1 ≤ |pat|, |text| ≤ 10⁵`; lowercase letters (so `#` is a safe separator).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Naive Z-array | extend each z[i] from 0 | O(n²) | O(n) |
| Linear Z-algorithm | reuse the Z-box [l, r) | O(n + m) | O(n + m) |

> [!tip] Interview angle
> Define `z[i]`, draw the Z-box `[l, r)`, and explain the two cases: `i ≥ r` (compare from scratch) and `i < r` (copy `z[i − l]`, capped at `r − i`, then extend). The separator stops a match from running past the pattern, so `z[i] ≤ |pat|`.

---

## 3. Naive Z-array

**Intuition.** For every `i`, compare `s[k]` with `s[i + k]` from `k = 0` until they differ. Same output, no reuse.

```python
def z_search_naive(text, pat):
    s, m = pat + '#' + text, len(pat)
    res = []
    for i in range(m + 1, len(s)):
        k = 0
        while i + k < len(s) and s[k] == s[i + k]:
            k += 1
        if k == m:
            res.append(i - m - 1)
    return res
```

**Complexity:** time **O(n²)**, space **O(n)**.

---

## 4. Linear Z-algorithm

**Intuition.** Build `s = pat + '#' + text`. For each `i ≥ 1`: if `i < r`, set `z[i] = min(r − i, z[i − l])`; extend while characters match; if `i + z[i] > r`, move the box to `[i, i + z[i])`. Report `i − m − 1` when `z[i] == m`.

**Algorithm**

1. `s = pat + '#' + text`, `z = [0] * |s|`, `l = r = 0`.
2. For `i = 1..|s|−1`: if `i < r`, `z[i] = min(r − i, z[i − l])`.
3. While `s[z[i]] == s[i + z[i]]`, `z[i]++`.
4. If `i + z[i] > r`: `l = i`, `r = i + z[i]`.
5. If `z[i] == m`, record `i − m − 1`.

**Dry run** — s = aa#aaaaa. z: i=3 → 2 (match at 0), i=4 → box gives min(…), extends to 2 → match at 1, … → [0, 1, 2, 3].

**C++**
```cpp
vector<int> zSearch(const string& text, const string& pat) {
    string s = pat + '#' + text;
    int n = s.size(), m = pat.size();
    vector<int> z(n, 0), res;
    for (int i = 1, l = 0, r = 0; i < n; i++) {
        if (i < r) z[i] = min(r - i, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
        if (i + z[i] > r) { l = i; r = i + z[i]; }
        if (z[i] == m) res.push_back(i - m - 1);
    }
    return res;
}
```

**Java**
```java
static List<Integer> zSearch(String text, String pat) {
    String s = pat + "#" + text;
    int n = s.length(), m = pat.length();
    int[] z = new int[n];
    List<Integer> res = new ArrayList<>();
    for (int i = 1, l = 0, r = 0; i < n; i++) {
        if (i < r) z[i] = Math.min(r - i, z[i - l]);
        while (i + z[i] < n && s.charAt(z[i]) == s.charAt(i + z[i])) z[i]++;
        if (i + z[i] > r) { l = i; r = i + z[i]; }
        if (z[i] == m) res.add(i - m - 1);
    }
    return res;
}
```

**Python**
```python
def z_array(s):
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z

def z_search(text, pat):
    s, m = pat + '#' + text, len(pat)
    z = z_array(s)
    return [i - m - 1 for i in range(m + 1, len(s)) if z[i] == m]
```

**Complexity:** time **O(n + m)**, space **O(n + m)** — every successful comparison in the while loop pushes r right, and r ≤ n, so the total extension work is O(n).

---

## Edge cases

- Pattern longer than the text (no index reaches z == m).
- Whole text is one character repeated.

---

## Common mistakes

1. Separator that can appear in the input.
2. Forgetting the cap `r − i` when copying `z[i − l]`.
3. Off-by-one when converting the index back (`i − m − 1`).

---

## Follow-ups

1. Count distinct substrings / string period?
2. Z vs KMP?

<details><summary>Answer sketches</summary>

**#1:** The smallest period p is the first i with i + z[i] == n (and n % p == 0 for a full repetition).

**#2:** Equivalent power for matching; Z is easier to reason about for 'prefix match at every position' questions, KMP streams the text without concatenating.
</details>

---

## Flashcards

**Define z[i].** #flashcard
Length of the longest common prefix of s and s[i:].

**Z-box initial value for i < r?** #flashcard
min(r − i, z[i − l]).

**Pattern search with Z?** #flashcard
Z of pat + '#' + text; matches where z[i] == |pat|.

**Interview track →** [String algorithms deep-dive](../../02-algorithms/02-string-algorithms.md) · [String algorithm walkthroughs](../../coding/algorithms/02-string-algorithms.md)
