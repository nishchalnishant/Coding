---
module: 02-algorithms
topic: Sliding Window
subtopic: 
status: unread
tags: [algorithms, sliding-window]
---

← [Algorithms index](./README.md) · [Algorithm decision tree](./algorithm_tree.md)
## First-Principles Map

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop. Do not move on until these are reflexive.
> `🎯 T2` — **TIER 2 · Build Fluidity**: Highly probable; know the core patterns cold. Edge cases matter less.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Know what it is conceptually; skip deep implementation practice.


```text
WHY Sliding Window exists
├── Brute-force O(n²) / O(n³) over all subarrays is too slow
│   ├── Adjacent subarrays share n-1 elements — recomputing from scratch wastes work
│   └── Maintain a running aggregate; update it in O(1) per step
WHAT it is
├── Two pointers [left, right] defining a contiguous subarray/substring
│   ├── Fixed window: right - left == k always; slide both by 1 each step
│   └── Variable window: expand right greedily; shrink left when constraint violated
HOW it works
├── Expand right by 1 → update window state (sum, freq map, count)
│   ├── While constraint violated → shrink from left by 1, update state
│   └── Record answer at each valid [left, right] → O(n) total
WHEN to use
├── "longest / shortest subarray/substring satisfying condition" → variable window
├── "maximum sum / average over k elements" → fixed window O(n)
└── "number of subarrays with at most K distinct" → sliding window + at-most trick
WHAT can go wrong
├── Off-by-one on window size: right - left + 1 vs right - left
├── Not shrinking left far enough → window state stale / constraint still violated
└── Hashmap not cleaned up when left advances → incorrect frequency counts
DECISION
└── Contiguous subarray + monotone constraint → sliding window O(n); non-contiguous → two-pointers or DP
```

## First-Principles Breakdown

- **Root problem**: Evaluate a property of every contiguous subarray in better than O(n²) time.
- **Core insight**: Moving the window by one position changes exactly two elements (add right+1, remove left) — maintain state incrementally rather than recomputing.
- **Invariant**: The window [left, right] always satisfies the problem constraint; the answer is extracted at each valid state.
- **Why it works**: Each element enters the window once and leaves once → O(n) pointer movements total regardless of window size.
- **Where it breaks**: Non-contiguous subsets, or constraints that are not monotone (adding more elements doesn't consistently worsen/improve) — the shrink step becomes ambiguous.




---

# Sliding Window

```
[SLIDING WINDOW — MINDMAP]
├── WHY IT EXISTS
│   ├── Brute force subarray problems → O(N²) or O(N³)
│   ├── Contiguous subarrays share overlap — recomputing from scratch wastes work
│   └── Maintain a window state incrementally: add right element, remove left element
├── WHAT IT IS
│   ├── Core invariant: [left, right] window satisfies a constraint at all times
│   ├── Right pointer expands window; left pointer shrinks it
│   └── Answer is derived from window size, content, or running aggregate
├── HOW IT WORKS
│   ├── Fixed-size window (size K)
│   │   ├── Step 1: build window for first K elements
│   │   ├── Step 2: slide — add arr[right], remove arr[right-K]
│   │   └── Step 3: record max/min/sum each step
│   ├── Variable-size window — longest valid
│   │   ├── Step 1: right++ always (expand)
│   │   ├── Step 2: while constraint violated → left++ (shrink)
│   │   └── Step 3: update ans = max(ans, right - left + 1)
│   └── Variable-size window — shortest valid
│       ├── Step 1: right++ (expand until valid)
│       ├── Step 2: while valid → record ans, then left++ (shrink)
│       └── Step 3: update ans = min(ans, right - left + 1)
├── COMPLEXITY
│   ├── Time:  O(N) — left and right each traverse array once
│   └── Space: O(K) or O(charset) for frequency map
├── TRIGGER PATTERNS (when to use)
│   ├── "Longest subarray/substring with at most K distinct" → variable window
│   ├── "Maximum sum subarray of size K" → fixed window
│   ├── "Minimum window substring containing all chars of T" → shortest valid
│   ├── "Exactly K" → convert to atMost(K) - atMost(K-1)
│   ├── "No repeating characters" → window + last-seen index map
│   └── "Permutation of pattern in string" → fixed window with freq map
└── GOTCHAS
    ├── "Exactly K" is hard — reframe as difference of two at-most problems
    ├── Char frequency map: decrement on left exit, only shrink when map invalid
    ├── Negative numbers invalidate fixed-window sum assumption → use Kadane's instead
    ├── Right pointer is inclusive — window length = right - left + 1
    └── For character windows, reset is O(charset) not O(1) — account for it
```

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

**Longest Substring Without Repeating Characters: `⚡ T1`**
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

**Minimum Window Substring: `⚡ T1`**
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

---

## Interview Questions — Logic & Trickiness

| Question | Variant | Click moment | Core logic | Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **Longest Substring Without Repeat** | Variable | Jump `left` past last index of char | `while s[right] in seen: left = max(left, seen[c]+1)` | Only jump if char is **inside** window. |
| **Minimum Window Substring `⚡ T1`** | Variable + freq | Expand until valid; shrink while valid | Track `have` vs `need` per character | Shrink only when window still valid; record on valid shrink. |
| **Longest Repeating Char Replacement** | Variable | Window valid if `len - max_freq <= k` | Track max frequency in window | Answer uses max freq seen — OK if max_freq drops on shrink. |
| **Subarray Sum ≥ Target** | Variable | Shrink while sum ≥ target | Greedy shrink minimizes length | Return 0 or -1 if no window; all-positive enables this variant. |
| **Sliding Window Maximum `⚡ T1`** | Monotonic deque | Front = max; pop expired indices | Each index in/out deque once | Store **indices** in deque, not values. |
| **Find All Anagrams `⚡ T1`** | Fixed | Window size = len(p) | Match frequency or match-count | Fixed window — slide by one char at a time. |
| **Permutation in String `⚡ T1`** | Fixed | Same as anagram | `have == need` when all chars satisfied | Clarify if permutation must be contiguous (yes). |
| **Subarrays with K Distinct** | At-most trick | `exactly(K) = atMost(K) - atMost(K-1)` | Two passes with helper | "Exactly K" is not monotonic — never use one sliding window for exactly. |

Walkthroughs: [problem-deep-dives.md](../20-problem-deep-dives.md). String windows: [string.md](../01-data-structures/02-string.md).

---

## Quick Revision Triggers

- **Contiguous + longest/shortest with constraint** → sliding window (variable unless fixed size given).
- **Fixed size K** → add on enter, subtract on leave; O(n).
- **Negatives in numeric subarray sum** → prefix sum + map, **not** sliding window ([array.md](../01-data-structures/01-array.md)).
- **Max/min in each window** → monotonic deque ([queue.md](../01-data-structures/06-queue.md)).
- **Exactly K distinct** → at-most(K) − at-most(K−1).

---

## See also

- [two-pointers.md](./03-two-pointers.md) — opposite-end scans; often combined with windows on strings
- [string.md](./02-string.md) — KMP, Rabin-Karp (pattern matching, not window)
- [01-data-structures/string.md](../01-data-structures/02-string.md) — anagram / window canonical problems
- [01-data-structures/array.md](../01-data-structures/01-array.md) — prefix sum when window fails
- [03-patterns/patterns-master.md](../03-patterns/patterns-master.md) — sliding window triggers

---

## Flashcards

**Contiguous subarray/substring with constraint → variable sliding window: expand right, shrink left while invalid.?** #flashcard  
Contiguous subarray/substring with constraint → variable sliding window: expand right, shrink left while invalid.

**Exactly K distinct subarrays → atMost(K) - atMost(K-1); do not use one window for "exactly".?** #flashcard  
Exactly K distinct subarrays → atMost(K) - atMost(K-1); do not use one window for "exactly".

**Sliding window maximum → monotonic deque of indices; O(n) because each index pushed/popped once.?** #flashcard  
Sliding window maximum → monotonic deque of indices; O(n) because each index pushed/popped once.
