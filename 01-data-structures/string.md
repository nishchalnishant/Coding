# Strings — Data Structure Deep-Dive

## Mental Model

A string is an **immutable array of characters**. Every array technique applies — two pointers, sliding window, prefix sum (on char frequencies). The extra surface area comes from the alphabet structure: 26 lowercase letters → frequency arrays replace hash maps; character relationships (anagram, palindrome, subsequence) define most problem classes.

**Complexity at a glance**

| Operation | Time | Notes |
|-----------|------|-------|
| Access char at index | O(1) | Direct index |
| Substring (Python) | O(k) | k = length of slice |
| Concatenation in loop | O(n²) | Use `"".join(list)` instead |
| String comparison | O(n) | Character by character |
| Sort characters | O(n log n) | Or O(n) with counting sort |

---

## Core Properties

**Immutability (Python/Java):** Strings cannot be modified in-place. Every `s += c` creates a new string object → O(n²) in a loop. Always build into a list and `"".join()` at the end.

**Character frequency array:** For lowercase a–z, a `freq = [0] * 26` array is faster and cleaner than a dict. Index with `ord(c) - ord('a')`.

**Sliding window is the dominant technique.** Most substring problems → variable-size window. Most subarray problems that happen to be strings → same playbook.

---

## Key Patterns

### 1. Frequency Map / Anagram Check

**Trigger:** "same characters", "anagram", "permutation exists in string"

```python
from collections import Counter

def is_anagram(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)

# Sliding window anagram check — O(n)
def find_anagrams(s: str, p: str) -> list[int]:
    need = Counter(p)
    window = Counter()
    result = []
    left = 0
    for right, c in enumerate(s):
        window[c] += 1
        if right - left + 1 > len(p):
            lc = s[left]
            window[lc] -= 1
            if window[lc] == 0:
                del window[lc]
            left += 1
        if window == need:
            result.append(left)
    return result
```

### 2. Two Pointers — Palindrome / Reverse

**Trigger:** "palindrome", "reverse", "symmetric"

```python
def is_palindrome(s: str) -> bool:
    l, r = 0, len(s) - 1
    while l < r:
        while l < r and not s[l].isalnum(): l += 1
        while l < r and not s[r].isalnum(): r -= 1
        if s[l].lower() != s[r].lower(): return False
        l += 1; r -= 1
    return True

def longest_palindrome_expand(s: str) -> str:
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1; r += 1
        return s[l+1:r]
    best = ""
    for i in range(len(s)):
        for sub in (expand(i, i), expand(i, i+1)):  # odd, even
            if len(sub) > len(best): best = sub
    return best
```

### 3. Sliding Window — Substring with Constraint

**Trigger:** "longest substring without", "minimum window", "at most K distinct"

```python
def length_of_longest_substring(s: str) -> int:
    freq = {}
    left = best = 0
    for right, c in enumerate(s):
        freq[c] = freq.get(c, 0) + 1
        while freq[c] > 1:          # window invalid
            lc = s[left]
            freq[lc] -= 1
            if freq[lc] == 0: del freq[lc]
            left += 1
        best = max(best, right - left + 1)
    return best

def min_window_substring(s: str, t: str) -> str:
    need = Counter(t)
    have, total = {}, len(need)
    formed = 0
    left = 0
    best = (float('inf'), 0, 0)
    for right, c in enumerate(s):
        have[c] = have.get(c, 0) + 1
        if c in need and have[c] == need[c]:
            formed += 1
        while formed == total:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)
            lc = s[left]
            have[lc] -= 1
            if lc in need and have[lc] < need[lc]:
                formed -= 1
            left += 1
    return s[best[1]:best[2]+1] if best[0] != float('inf') else ""
```

### 4. Prefix Sum on Characters

**Trigger:** "number of substrings with exactly K vowels/distinct chars"

```python
# Substrings with sum == k (binary string, treat 0→-1)
def num_subarrays_with_sum(s: str, goal: int) -> int:
    prefix = {0: 1}
    total = count = 0
    for c in s:
        total += int(c)
        count += prefix.get(total - goal, 0)
        prefix[total] = prefix.get(total, 0) + 1
    return count
```

### 5. String Hashing — Duplicate / Equal Substrings

**Trigger:** "find duplicate substring", "longest duplicate substring", "repeated pattern"

```python
# Check if substring of length L exists twice — O(n)
def has_duplicate_of_length(s: str, L: int) -> bool:
    seen = set()
    for i in range(len(s) - L + 1):
        sub = s[i:i+L]
        if sub in seen: return True
        seen.add(sub)
    return False
```

---

## Canonical Problems

| Problem | Pattern | Key Insight |
|---------|---------|-------------|
| Valid Anagram | Frequency map | Counter(s) == Counter(t) |
| Group Anagrams | Frequency map + grouping | sorted(word) as key |
| Longest Substring Without Repeat | Sliding window | shrink when freq[c] > 1 |
| Minimum Window Substring | Sliding window + frequency | two counters: need vs have |
| Find All Anagrams in String | Sliding window fixed | fixed-size window, compare counters |
| Longest Palindromic Substring | Expand around center | O(n²); Manacher's for O(n) |
| Palindromic Substrings (count) | Expand around center | count both odd and even expansions |
| Encode/Decode Strings | Delimiter encoding | length-prefix: "4#word" |
| Longest Repeating Char Replacement | Sliding window | window valid if len - max_freq ≤ k |
| String to Integer (atoi) | Parsing | handle sign, overflow, non-digits |

---

## Common Mistakes

- **`s += c` in a loop** — O(n²). Use `chars = []; chars.append(c); "".join(chars)`.
- **Case sensitivity** — always `s.lower()` before comparing unless the problem is case-sensitive.
- **Unicode vs ASCII** — `ord(c) - ord('a')` only valid for lowercase a–z; use `Counter` for general case.
- **Off-by-one in substrings** — `s[l:r]` excludes `r`; `s[l:r+1]` includes it.
- **Palindrome check skipping non-alphanumeric** — use `isalnum()` and `lower()` together.
