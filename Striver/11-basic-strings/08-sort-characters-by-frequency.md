---
module: striver/11-basic-strings
lesson: 8
topic: Sort Characters by Frequency
difficulty: Medium
source: https://takeuforward.org/learning/dsa/sort-characters-by-frequency?category=basic-strings&source=strivers-a2z-dsa-sheet
tags: [striver, basic-strings, strings, hashing, bucket-sort]
---
# 8. Sort Characters by Frequency

← [Valid Anagram](07-valid-anagram.md) · [Part 11 index](README.md) · Next → [Part 12: Basic Recursion](../12-basic-recursion/README.md)

> [!abstract] Problem at a glance
> **Task:** Return `s` rearranged so that chars appear in decreasing order of frequency, with equal frequencies in ascending char order.
> **Key insight:** Count, then bucket by frequency: `bucket[f]` holds the chars that occur `f` times. Walking the buckets from `n` down to 1 emits the answer in O(n) with no comparison sort.
> **Difficulty:** Medium · **Pattern:** Count + bucket sort · **Also on:** 451
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/sort-characters-by-frequency?category=basic-strings&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — sort the chars by key](#3-brute--sort-the-chars-by-key) · [4. Better — sort the distinct chars](#4-better--sort-the-distinct-chars) · [5. Optimal — bucket by frequency](#5-optimal--bucket-by-frequency) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `s`, sort it so that more frequent chars come first, with all copies of a char contiguous. Break frequency ties by ascending ASCII value. (LeetCode accepts any tie order; this note fixes one so the output is deterministic.)

| Input | Output | Why |
|---|---|---|
| `s = "tree"` | `"eert"` | e×2, then r and t (r < t) |
| `s = "cccaaa"` | `"aaaccc"` | tie → a before c |
| `s = "Aabb"` | `"bbAa"` | A (65) < a (97) |

**Constraints:** `1 ≤ n ≤ 5·10⁵`, ASCII letters and digits.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — sort the chars by key | sort s by (−freq[c], c) | O(n log n) | O(n) |
| Better — sort the distinct chars | sort ≤ Σ distinct chars, then expand | O(n + Σ log Σ) | O(n) |
| Optimal — bucket by frequency | bucket[f] ← chars; walk f = n..1 | O(n + Σ) | O(n) |

> [!tip] Interview angle
> Say the tie-break out loud. Then offer both versions: a sort by `(-freq, char)` (O(n + Σ log Σ)) and buckets (O(n)). Σ is tiny, so either is fine, but the bucket version shows you know the trick.

---

## 3. Brute — sort the chars by key

**Intuition.** Count the chars, then sort the whole string by the key `(−freq, char)`. Equal chars land together because they share a key.

```python
from collections import Counter

def freq_sort_brute(s):
    f = Counter(s)
    return "".join(sorted(s, key=lambda c: (-f[c], c)))
```

**Complexity:** time **O(n log n)**, space **O(n)**.

---

## 4. Better — sort the distinct chars

**Intuition.** Only the distinct chars need sorting. Sort them by `(−freq, char)` and emit each `freq` times.

```python
from collections import Counter

def freq_sort_distinct(s):
    f = Counter(s)
    return "".join(c * f[c] for c in sorted(f, key=lambda c: (-f[c], c)))
```

**Complexity:** time **O(n + Σ log Σ)**, space **O(n)**.

---

## 5. Optimal — bucket by frequency

**Intuition.** A frequency is between 1 and n, so use it as an index. Filling the buckets by scanning chars 0..255 in order keeps each bucket in ascending char order, which handles the tie-break for free.

**Algorithm**

1. `cnt[256]` from `s`.
2. For `c` in 0..255 with `cnt[c] > 0`: append `c` to `bucket[cnt[c]]`.
3. For `f = n .. 1`: for each `c` in `bucket[f]`, emit `c` × f.

**Dry run** — `tree` → cnt e: 2, r: 1, t: 1 → bucket[2] = [e], bucket[1] = [r, t] → `ee` + `r` + `t` = **eert**.

**C++**
```cpp
string frequencySort(string& s) {
    int n = s.size(), cnt[256] = {0};
    for (unsigned char c : s) cnt[c]++;
    vector<vector<char>> bucket(n + 1);
    for (int c = 0; c < 256; c++) if (cnt[c]) bucket[cnt[c]].push_back((char)c);
    string out;
    out.reserve(n);
    for (int f = n; f >= 1; f--)
        for (char c : bucket[f]) out.append(f, c);
    return out;
}
```

**Java**
```java
static String frequencySort(String s) {
    int n = s.length();
    int[] cnt = new int[256];
    for (int i = 0; i < n; i++) cnt[s.charAt(i)]++;
    List<List<Character>> bucket = new ArrayList<>();
    for (int f = 0; f <= n; f++) bucket.add(new ArrayList<>());
    for (int c = 0; c < 256; c++) if (cnt[c] > 0) bucket.get(cnt[c]).add((char) c);
    StringBuilder out = new StringBuilder(n);
    for (int f = n; f >= 1; f--)
        for (char c : bucket.get(f)) for (int k = 0; k < f; k++) out.append(c);
    return out.toString();
}
```

**Python**
```python
def frequency_sort(s):
    n = len(s)
    cnt = [0] * 256
    for c in s:
        cnt[ord(c)] += 1
    bucket = [[] for _ in range(n + 1)]
    for c in range(256):
        if cnt[c]:
            bucket[cnt[c]].append(chr(c))
    out = []
    for f in range(n, 0, -1):
        for c in bucket[f]:
            out.append(c * f)
    return "".join(out)
```

**Complexity:** time **O(n + Σ)**, space **O(n)** — n buckets + 256 chars + n output chars.

---

## Edge cases

- All the same char → unchanged.
- All distinct → sorted ascending (all frequency 1).
- Mixed case and digits: ASCII order puts digits < upper < lower.

---

## Common mistakes

1. Sorting with key `-freq` only, which leaves equal-frequency chars interleaved under some sort orders. Add the char as a secondary key.
2. Building the output with `+=` on a Java `String` in a loop (O(n²)).

---

## Follow-ups

1. Return only the k most frequent chars / words (LC 692).
2. Reorganise a string so no two adjacent chars are equal (LC 767).

<details><summary>Answer sketches</summary>

**#1:** The same buckets, stopping after k; for words with lexicographic ties, a heap of size k with a custom comparator.

**#2:** Max-heap by count: pop the top two each round; it's impossible iff `maxFreq > (n+1)/2` ([Part 26](../26-heaps/README.md)).
</details>

---

## Flashcards

**O(n) sort-by-frequency?** #flashcard
Bucket by frequency (1..n), walk from high to low.

**Why do buckets give ascending ties for free?** #flashcard
They're filled by scanning chars in increasing ASCII order.

**Tie-break key for sort by frequency?** #flashcard
(−freq, char).

**Interview track →** [Strings deep-dive](../../01-data-structures/03-string.md) · [String algorithms](../../02-algorithms/02-string-algorithms.md) · [Concept: basic strings](../07-concept-basics/04-basic-string.md)
