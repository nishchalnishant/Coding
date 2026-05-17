# Sliding Window

## When to Use

**Trigger keywords:** contiguous subarray or substring, longest / shortest with constraint, maximum/minimum sum of size K, "at most K distinct", "exactly K", contains all characters of T.

**Use when:** brute force is O(n²) or O(n³) by re-examining every subarray from scratch — sliding window amortizes to O(n) by reusing computation.

---

## Variant 1: Fixed-Size Window

**Use for:** max/min/average of every window of size K, find all anagrams of P in S.

```python
def fixed_window(arr, k):
    # Build initial window
    window_sum = sum(arr[:k])
    best = window_sum

    for i in range(k, len(arr)):
        window_sum += arr[i]       # add incoming element
        window_sum -= arr[i - k]   # remove outgoing element
        best = max(best, window_sum)

    return best
```

**Anagram / frequency match template:**
```python
from collections import Counter

def find_anagrams(s, p):
    result = []
    need = Counter(p)
    window = Counter(s[:len(p)])
    if window == need:
        result.append(0)

    for i in range(len(p), len(s)):
        # Add right
        window[s[i]] += 1
        # Remove left
        left = s[i - len(p)]
        window[left] -= 1
        if window[left] == 0:
            del window[left]
        if window == need:
            result.append(i - len(p) + 1)

    return result
```

**Complexity:** O(n) time, O(k) or O(|alphabet|) space.

---

## Variant 2: Variable-Size Window (Expand Right, Shrink Left)

**Use for:** longest substring without repeating chars, longest substring with at most K distinct chars, minimum window substring, smallest subarray with sum ≥ target.

```python
def variable_window(s, condition_fn):
    left = 0
    best = 0
    window_state = {}  # or Counter, or int

    for right in range(len(s)):
        # Expand: add s[right] to window
        # ... update window_state ...

        # Shrink: while window is invalid
        while not condition_fn(window_state):
            # Remove s[left] from window
            # ... update window_state ...
            left += 1

        # Window [left..right] is valid
        best = max(best, right - left + 1)

    return best
```

**Longest Substring Without Repeating Characters:**
```python
def length_of_longest_substring(s):
    seen = {}
    left = 0
    best = 0

    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1  # jump left past the duplicate
        seen[ch] = right
        best = max(best, right - left + 1)

    return best
```

**At Most K Distinct Characters:**
```python
def longest_k_distinct(s, k):
    from collections import defaultdict
    freq = defaultdict(int)
    left = 0
    best = 0

    for right, ch in enumerate(s):
        freq[ch] += 1
        while len(freq) > k:          # window invalid: more than k distinct
            freq[s[left]] -= 1
            if freq[s[left]] == 0:
                del freq[s[left]]
            left += 1
        best = max(best, right - left + 1)

    return best
```

**Minimum Window Substring:**
```python
from collections import Counter

def min_window(s, t):
    need = Counter(t)
    missing = len(t)   # total chars still needed
    best = ""
    left = 0

    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1

        if missing == 0:             # valid window
            # Shrink from left
            while need[s[left]] < 0:
                need[s[left]] += 1
                left += 1
            # s[left] is now a required char — record window
            if not best or right - left + 1 < len(best):
                best = s[left:right+1]
            # Slide: remove s[left] to look for next window
            need[s[left]] += 1
            missing += 1
            left += 1

    return best
```

**Complexity:** O(n) time (each element enters and leaves window once), O(|alphabet|) space.

---

## Extension: With Frequency Map

When the window constraint involves character/element frequency (anagrams, permutations, "contains all of T"):

```python
# Pattern: use a "match" counter to avoid comparing full dicts each step
def count_with_matches(s, p):
    need = Counter(p)
    window = {}
    matches = 0                 # how many chars have exactly the right count
    required = len(need)        # distinct chars we need to satisfy

    left = 0
    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            matches += 1

        while matches == required:
            # window is valid — record result here
            lch = s[left]
            window[lch] -= 1
            if lch in need and window[lch] < need[lch]:
                matches -= 1
            left += 1
```

---

## Extension: Monotonic Deque (Sliding Window Max/Min)

For "maximum in every window of size K" in O(n):

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()   # stores indices; front = max of current window
    result = []

    for i, val in enumerate(nums):
        # Remove elements outside window
        if dq and dq[0] < i - k + 1:
            dq.popleft()

        # Maintain decreasing order: pop smaller elements from back
        while dq and nums[dq[-1]] < val:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

**Why it works:** The deque always stores indices in decreasing order of their values. The front is always the max of the current window.

---

## Complexity Summary

| Variant | Time | Space |
|---------|------|-------|
| Fixed-size | O(n) | O(1) or O(k) |
| Variable-size | O(n) amortized | O(window size) |
| Monotonic deque | O(n) | O(k) |

---

## Canonical Problems

| Problem | Variant | Key Insight | Gotcha |
|---------|---------|-------------|--------|
| Max Sum Subarray of Size K | Fixed | Simple add/remove | Remember to handle `k > len(arr)` |
| Find All Anagrams in S | Fixed | Fixed window = len(p); compare Counter dicts or use match count | Counter comparison is O(26) — use match counter for clarity |
| Longest Substring No Repeat | Variable | Jump left to `seen[ch]+1` when dup found | Only jump if `seen[ch] >= left` (char may be outside window) |
| Longest Substring K Distinct | Variable | Shrink when `len(freq) > k` | Don't forget to delete key when count hits 0 |
| Minimum Window Substring | Variable | Track `missing` count; shrink greedily | Shrink until `s[left]` is a required char, then record |
| Smallest Subarray Sum ≥ Target | Variable | Shrink while sum ≥ target to minimize length | Initialize best to float('inf'), check for no-solution case |
| Max Sliding Window | Monotonic deque | Deque front = current max | Pop from front when index out of window range |
| Permutation in String | Fixed | Fixed window = len(s1); frequency match | Same as anagram; use match-count trick to avoid full comparison |

---

## Edge Cases

- **k > len(arr):** Fixed window — return early or handle empty result.
- **No valid window exists:** Variable window — return `""` or `0` or `float('inf')` depending on problem.
- **All same characters:** Anagram problems — window always matches; verify logic handles this.
- **Single character string:** Works naturally; verify `left` doesn't go negative.
- **Unicode / case sensitivity:** Clarify with interviewer. `s.lower()` if case-insensitive.
- **"Exactly K" problems:** `exactly(k) = at_most(k) - at_most(k-1)` — key trick for "exactly K distinct" variants.
