# Strings — SDE-3 Level

Arrays of characters; problems center on pattern matching, palindromes, sliding window, and DP (LCS, edit distance). SDE-3 expects KMP/LPS, rolling hash, and clean handling of immutability.

---

## 1. Concept Overview

**Problem space**: Pattern matching (KMP, Rabin-Karp), longest palindromic substring (expand or Manacher), anagrams (hash/count), minimum window substring (sliding window + frequency), LCS/edit distance (DP), parsing (valid number, decode).

**When to use**: "Substring match" → KMP or Rabin-Karp. "Palindrome" → expand from center or DP. "Anagram" → frequency array or sorted key. "Window with constraint" → sliding window + map.

---

## 2. Core Algorithms

### KMP (Knuth-Morris-Pratt)
- **LPS (Longest Proper Prefix which is also Suffix)**: For pattern P, lps[i] = length of longest border of P[0:i+1]. Build by comparing P[j] with P[len]; advance len or fall back.
- **Search**: Compare text T with P; on mismatch, shift P by (j - lps[j-1]) (don't move i). Time O(N+M).

### Rabin-Karp (Rolling Hash)
- Hash pattern; hash first window of text; roll: subtract left char contribution, multiply by base, add right. Use mod to avoid overflow; check collision with actual compare. O(N+M) average.

### Longest Palindromic Substring
- **Expand**: For each center (char or between chars), expand while s[l]==s[r]. O(N²).
- **Manacher**: Linear time with radius array and center bounds; SDE-3 can state and skip implementation.

### Sliding Window (Min Window Substring)
- Maintain window [i,j] with frequency map for t; expand j until valid, then shrink i while valid; track min length. O(N).

---

## 3. Advanced Variations

- **Multiple pattern match**: Trie of patterns + Aho-Corasick (or KMP per pattern). 
- **Edit distance (Levenshtein)**: 2D DP; insert/delete/replace; dp[i][j] from dp[i-1][j], dp[i][j-1], dp[i-1][j-1]. O(N*M).
- **Immutable strings**: Use list for in-place simulation or StringBuilder (Java); mention when concatenation in loop is O(N²).

### Edge Cases
- Empty string; single char; no match; multiple matches; case sensitivity; Unicode (often assume ASCII for interview).

---

## 4. Common Interview Problems

**Easy**: Valid Palindrome, Valid Anagram, Longest Common Prefix.  
**Medium**: Longest Substring Without Repeating Chars, Longest Palindromic Substring, Group Anagrams, Find All Anagrams in String.  
**Hard**: Minimum Window Substring, Edit Distance, Implement strStr() (KMP), Valid Number.

---

## 5. Pattern Recognition

- **Pattern match**: Single pattern → KMP or Rabin-Karp; multiple → Trie/Aho-Corasick.
- **Palindrome**: Expand from center; or DP (substring [i,j] is palindrome if s[i]==s[j] and [i+1,j-1] is).
- **Anagram**: Sort as key or 26-char count; sliding window for "anagram in string".
- **Window**: Min/max window with constraint → two pointers + frequency map.

---

## 6. Code (KMP LPS + Search)

```python
def build_lps(pattern):
    n = len(pattern)
    lps = [0] * n
    length = 0
    i = 1
    while i < n:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    lps = build_lps(pattern)
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j
        elif i < len(text) and text[i] != pattern[j]:
            if j:
                j = lps[j - 1]
            else:
                i += 1
    return -1
```

---

## 7. SDE-3 Level Thinking

- **Trade-offs**: KMP avoids backtracking in text (O(N)); Rabin-Karp simpler, probabilistic. For production: consider Unicode, large alphabet, and library (e.g., Boyer-Moore for long patterns).
- **Memory**: LPS O(M); rolling hash O(1) extra; sliding window O(distinct chars).

---

## 8. Interview Strategy

- **Identify**: "Find pattern" → KMP/Rabin-Karp. "Longest palindrome" → expand. "Anagram" → count/sort. "Min window" → sliding window.
- **Common mistakes**: LPS off-by-one; forgetting to verify on hash match (Rabin-Karp); window validity condition wrong.

---

## 9. Quick Revision

- **Tricks**: LPS = longest border; KMP never decrement text index. Anagram key = tuple(count) or sorted(s). Min window: expand until valid, shrink while valid.
- **Edge cases**: Empty pattern; no match; multiple matches; case.
- **Pattern tip**: "Substring" + "match" → KMP; "substring" + "anagram" → sliding window + count.

---

## See also

- [Array](../data-structures/array.md) — sliding window on arrays vs strings  
- [Hashing](../data-structures/hashing.md) — frequency maps  
- [Dynamic Programming](dynamic-programming/README.md) — LCS, edit distance
