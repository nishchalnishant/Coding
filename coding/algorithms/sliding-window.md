---
tags: [coding, algorithms, sliding-window]
topic: Sliding Window
difficulty: mixed
---

# Sliding Window — Problem Set

---

## Fixed-Size Window

> [!info] Approach
> For a window of exactly size `k`, every slide adds one element on the right and removes one on the left. Maintain state incrementally in O(1) per step rather than recomputing from scratch — reduces O(nk) to O(n).

---

### Find All Anagrams in a String (LC 438)

> [!example] Problem
> Given string `s` and pattern `p`, find all start indices in `s` where an anagram of `p` begins.

> [!info] Approach
> - WHY: An anagram is a permutation — same character frequencies, different order. Fixed window of size `len(p)`.
> - WHAT: Maintain a frequency diff between window and `need`. Track how many characters are "satisfied" with a `matches` counter — avoids O(26) dict comparison each step.
> - HOW: On adding `s[right]`: if freq reaches exactly `need[c]` → `matches += 1`. On removing `s[left]`: if freq drops below `need[c]` → `matches -= 1`. When `matches == len(need)` → anagram found.

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def find_anagrams(s: str, p: str) -> list[int]:
>     need = Counter(p)
>     window: dict[str, int] = {}
>     matches = 0
>     required = len(need)
>     result = []
>     k = len(p)
> 
>     for right in range(len(s)):
>         c = s[right]
>         window[c] = window.get(c, 0) + 1
>         if c in need and window[c] == need[c]:
>             matches += 1
> 
>         if right >= k:   # window overflows — remove leftmost
>             lc = s[right - k]
>             if lc in need and window[lc] == need[lc]:
>                 matches -= 1
>             window[lc] -= 1
>             if window[lc] == 0:
>                 del window[lc]
> 
>         if right >= k - 1 and matches == required:
>             result.append(right - k + 1)
> 
>     return result
> ```

> [!success] Complexity
> O(n) time, O(|alphabet|) space.

> [!tip] Alternatives
> Compare `Counter` dicts directly each step — O(26) per slide vs O(1) with match counter; both O(n) overall but match counter is cleaner.

---

### Maximum Average Subarray I (LC 643)

> [!example] Problem
> Find a contiguous subarray of length exactly `k` with the maximum average. Return the average.

> [!info] Approach
> - WHY: Maximizing average is equivalent to maximizing sum (k is fixed). Fixed-size sliding window on sum.
> - WHAT: Build initial window sum for first `k` elements. Slide: add `nums[i]`, remove `nums[i-k]`, update max.
> - HOW: Trivial incremental sum — no auxiliary data structure needed.

> [!note]- Python Solution
> ```python
> def find_max_average(nums: list[int], k: int) -> float:
>     window_sum = sum(nums[:k])
>     best = window_sum
>     for i in range(k, len(nums)):
>         window_sum += nums[i] - nums[i - k]
>         best = max(best, window_sum)
>     return best / k
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Compute sum for every window from scratch O(nk) — unnecessary; prefix sum O(n) equivalent.

---

### Permutation in String (LC 567)

> [!example] Problem
> Return True if any permutation of `s1` appears as a contiguous substring of `s2`.

> [!info] Approach
> - WHY: A permutation has the same character frequencies. Fixed window of size `len(s1)` with frequency matching.
> - WHAT: Same match-counter technique as Find All Anagrams — identical logic, just return True/False.
> - HOW: When `matches == required` at any valid window position → return True.

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def check_inclusion(s1: str, s2: str) -> bool:
>     if len(s1) > len(s2):
>         return False
>     need = Counter(s1)
>     window: dict[str, int] = {}
>     matches = 0
>     required = len(need)
>     k = len(s1)
> 
>     for right in range(len(s2)):
>         c = s2[right]
>         window[c] = window.get(c, 0) + 1
>         if c in need and window[c] == need[c]:
>             matches += 1
> 
>         if right >= k:
>             lc = s2[right - k]
>             if lc in need and window[lc] == need[lc]:
>                 matches -= 1
>             window[lc] -= 1
>             if window[lc] == 0:
>                 del window[lc]
> 
>         if right >= k - 1 and matches == required:
>             return True
> 
>     return False
> ```

> [!success] Complexity
> O(n) time where n = len(s2), O(|alphabet|) space.

> [!tip] Alternatives
> Sort both strings per window O(nk log k) — too slow; direct Counter comparison O(n · 26) — correct but slower constant.

---

## Variable Window — At Most K

> [!info] Approach
> Expand `right` greedily; when the constraint is violated, shrink `left` until it's satisfied again. Each element enters and exits the window exactly once → O(n) amortized. Window length `right - left + 1` at any valid state is a candidate for the maximum.

---

### Longest Substring Without Repeating Characters (LC 3)

> [!example] Problem
> Find the length of the longest substring with all unique characters.

> [!info] Approach
> - WHY: At most 0 duplicate characters per window. Expanding right adds a character; if it duplicates, shrink left past the previous occurrence.
> - WHAT: Track last-seen index of each character. On duplicate: `left = last_seen[c] + 1` (jump, not step-by-step).
> - HOW: Only jump `left` if `last_seen[c] >= left` (character might be outside current window — stale).

> [!note]- Python Solution
> ```python
> def length_of_longest_substring(s: str) -> int:
>     last_seen: dict[str, int] = {}
>     left = 0
>     best = 0
>     for right, c in enumerate(s):
>         if c in last_seen and last_seen[c] >= left:
>             left = last_seen[c] + 1   # jump past previous occurrence
>         last_seen[c] = right
>         best = max(best, right - left + 1)
>     return best
> ```

> [!success] Complexity
> O(n) time, O(|alphabet|) space.

> [!tip] Alternatives
> Frequency map + step-by-step shrink — also O(n) but more steps; jump optimization is constant-factor faster.

---

### Longest Repeating Character Replacement (LC 424)

> [!example] Problem
> String of uppercase letters. Replace at most `k` characters. Find the longest substring with all same characters after replacements.

> [!info] Approach
> - WHY: In a window of length `L`, we need `L - max_count <= k` (replace all non-max-frequency characters). Expand while valid; shrink otherwise.
> - WHAT: Track `max_count` — the frequency of the most common character in the window. When `(window_size - max_count) > k` → shrink.
> - HOW: Key insight: `max_count` never needs to decrease (we only care about the *best* window seen so far). When we shrink, `max_count` stays the same, and the window stays the same size or shrinks — we're looking for a *longer* window.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def character_replacement(s: str, k: int) -> int:
>     freq: dict[str, int] = defaultdict(int)
>     max_count = 0
>     left = 0
>     best = 0
> 
>     for right, c in enumerate(s):
>         freq[c] += 1
>         max_count = max(max_count, freq[c])
>         # Window invalid: replacements needed exceed k
>         if (right - left + 1) - max_count > k:
>             freq[s[left]] -= 1
>             left += 1   # shrink by 1; don't update max_count (intentional)
>         best = max(best, right - left + 1)
> 
>     return best
> ```

> [!success] Complexity
> O(n) time, O(26) = O(1) space.

> [!tip] Alternatives
> Binary search on answer + sliding window validation — O(n log n); direct sliding window is O(n).

---

### Fruits Into Baskets (At Most 2 Distinct) (LC 904)

> [!example] Problem
> Array of fruit types. Two baskets, each holds one type. Pick from a contiguous subarray (one basket per type). Maximize fruits picked.

> [!info] Approach
> - WHY: Longest subarray with at most 2 distinct values. Direct application of at-most-K window.
> - WHAT: Frequency map. While `len(freq) > 2` → shrink left: decrement `freq[s[left]]`; delete key if 0.
> - HOW: Window length `right - left + 1` after shrinking is the candidate answer.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def total_fruit(fruits: list[int]) -> int:
>     freq: dict[int, int] = defaultdict(int)
>     left = 0
>     best = 0
> 
>     for right, f in enumerate(fruits):
>         freq[f] += 1
>         while len(freq) > 2:
>             freq[fruits[left]] -= 1
>             if freq[fruits[left]] == 0:
>                 del freq[fruits[left]]
>             left += 1
>         best = max(best, right - left + 1)
> 
>     return best
> ```

> [!success] Complexity
> O(n) time, O(1) space (at most 3 keys ever in freq map).

> [!tip] Alternatives
> Identical to "Longest Substring with At Most K Distinct" with k=2.

---

### Longest Substring with At Most K Distinct Characters (LC 340)

> [!example] Problem
> Find the longest substring with at most `k` distinct characters.

> [!info] Approach
> - WHY: General form of the "at most K distinct" pattern. Shrink window when distinct count exceeds k.
> - WHAT: Frequency map. While `len(freq) > k` → shrink left. Window length is candidate answer.
> - HOW: Remove key from freq map when its count reaches 0 to keep `len(freq)` accurate.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
>     freq: dict[str, int] = defaultdict(int)
>     left = 0
>     best = 0
> 
>     for right, c in enumerate(s):
>         freq[c] += 1
>         while len(freq) > k:
>             freq[s[left]] -= 1
>             if freq[s[left]] == 0:
>                 del freq[s[left]]
>             left += 1
>         best = max(best, right - left + 1)
> 
>     return best
> ```

> [!success] Complexity
> O(n) time, O(k) space.

> [!tip] Alternatives
> For k=1 or k=2, trivial optimizations possible but not needed.

---

## Variable Window — Exactly K

> [!info] Approach
> "Exactly K" windows are hard to count directly because shrinking can overshoot. The trick: `exactly(k) = at_most(k) - at_most(k-1)`. Both `at_most` calls are O(n), giving O(n) total.

---

### Subarrays with K Different Integers (LC 992)

> [!example] Problem
> Count subarrays containing exactly `k` different integers.

> [!info] Approach
> - WHY: The "exactly k" constraint is not monotone for a window — adding elements can go over or under. Reframe as difference of two at-most problems.
> - WHAT: `at_most(k)` counts subarrays with ≤ k distinct values. Use a window where every valid `[left, right]` contributes `right - left + 1` subarrays (all subarrays ending at `right`).
> - HOW: `count(exactly k) = at_most(k) - at_most(k-1)`.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def subarrays_with_k_distinct(nums: list[int], k: int) -> int:
>     def at_most(k: int) -> int:
>         freq: dict[int, int] = defaultdict(int)
>         left = count = 0
>         for right, n in enumerate(nums):
>             freq[n] += 1
>             while len(freq) > k:
>                 freq[nums[left]] -= 1
>                 if freq[nums[left]] == 0:
>                     del freq[nums[left]]
>                 left += 1
>             count += right - left + 1   # all subarrays [left..right], [left+1..right], ...
>         return count
> 
>     return at_most(k) - at_most(k - 1)
> ```

> [!success] Complexity
> O(n) time, O(k) space.

> [!tip] Alternatives
> Prefix sums + hashing O(n) — more complex; sliding window `exactly` without the trick requires two separate left pointers.

---

### Count Number of Nice Subarrays (LC 1248)

> [!example] Problem
> Array of integers. A subarray is "nice" if it contains exactly `k` odd numbers. Count nice subarrays.

> [!info] Approach
> - WHY: Remap: odd → 1, even → 0. Problem becomes: count subarrays with sum exactly k. Same `at_most(k) - at_most(k-1)` trick applies.
> - WHAT: `at_most(k)` counts subarrays with at most k odd numbers. Sum of `right - left + 1` across valid windows.
> - HOW: Window is valid when count of odds ≤ k. Shrink when count > k.

> [!note]- Python Solution
> ```python
> def number_of_subarrays(nums: list[int], k: int) -> int:
>     def at_most(k: int) -> int:
>         left = count = odds = 0
>         for right in range(len(nums)):
>             if nums[right] % 2 == 1:
>                 odds += 1
>             while odds > k:
>                 if nums[left] % 2 == 1:
>                     odds -= 1
>                 left += 1
>             count += right - left + 1
>         return count
> 
>     return at_most(k) - at_most(k - 1)
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Prefix sum approach: count prefix sums, use `prefix[i] - prefix[j] == k` → O(n) with hashmap. Equivalent in complexity.

---

## Variable Window — Minimum Length

> [!info] Approach
> Expand `right` until the window satisfies the constraint (becomes valid). Then shrink `left` as long as the window remains valid, recording the minimum length. Swap the "update answer" location from the expansion step to the shrink step.

---

### Minimum Size Subarray Sum (LC 209)

> [!example] Problem
> Array of positive integers. Find the minimal length of a contiguous subarray with sum ≥ `target`. Return 0 if none.

> [!info] Approach
> - WHY: Positive integers mean adding elements always increases sum, removing always decreases. Window constraint is monotone → shrink while valid.
> - WHAT: Expand right; once sum ≥ target, shrink left while still valid. Record minimum length at each valid state.
> - HOW: Inner while loop shrinks and records — the answer is updated at the tightest valid window for each right.

> [!note]- Python Solution
> ```python
> def min_subarray_len(target: int, nums: list[int]) -> int:
>     left = 0
>     window_sum = 0
>     best = float('inf')
> 
>     for right in range(len(nums)):
>         window_sum += nums[right]
>         while window_sum >= target:
>             best = min(best, right - left + 1)
>             window_sum -= nums[left]
>             left += 1
> 
>     return best if best != float('inf') else 0
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Binary search on length + prefix sum O(n log n) — works but unnecessary here; negative numbers would break window approach → use Kadane-style DP instead.

---

### Minimum Window Substring (LC 76)

> [!example] Problem
> Given strings `s` and `t`, find the minimum window in `s` that contains all characters of `t` (including duplicates). Return "" if none.

> [!info] Approach
> - WHY: Need to cover all characters of `t`. Use a `missing` counter — total characters still needed. Once 0 → window is valid → shrink.
> - WHAT: Expand right: if `need[c] > 0` before decrement, `missing -= 1`. Shrink while `missing == 0`: advance left past non-required characters (those with `need[s[left]] < 0`), record window, then remove `s[left]` from window.
> - HOW: `need` can go negative (excess characters) — only decrement `missing` when `need[c]` was positive (character was still required).

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def min_window(s: str, t: str) -> str:
>     need = Counter(t)
>     missing = len(t)    # total characters still needed
>     best_start = best_len = 0
>     found = False
>     left = 0
> 
>     for right, c in enumerate(s):
>         if need[c] > 0:
>             missing -= 1
>         need[c] -= 1
> 
>         if missing == 0:                    # valid window found
>             while need[s[left]] < 0:       # shrink: skip excess characters
>                 need[s[left]] += 1
>                 left += 1
>             # s[left] is now required — record this tightest window
>             if not found or right - left + 1 < best_len:
>                 best_start = left
>                 best_len = right - left + 1
>                 found = True
>             # Slide: invalidate window to search for next candidate
>             need[s[left]] += 1
>             missing += 1
>             left += 1
> 
>     return s[best_start:best_start + best_len] if found else ""
> ```

> [!success] Complexity
> O(|s| + |t|) time, O(|alphabet|) space.

> [!tip] Alternatives
> Two-pointer with explicit char counts O(n) — equivalent; the `missing` trick avoids full dict comparison.

---

## Sliding Window + Monotonic Deque

> [!info] Approach
> A monotonic deque stores indices in order of decreasing value (for max) or increasing value (for min). The front always holds the extreme element for the current window. Amortized O(1) per element: each index is pushed and popped at most once.

---

### Sliding Window Maximum (LC 239)

> [!example] Problem
> Array of integers, window size `k`. Return max of each window as it slides.

> [!info] Approach
> - WHY: Recomputing max per window is O(nk). A deque maintaining a decreasing sequence of indices gives O(1) max lookup.
> - WHAT: Deque stores indices in decreasing order of their values. Front = index of max for current window.
> - HOW: Before adding `i`: (1) pop front if it's outside window `[i-k+1, i]`; (2) pop back while `nums[deque[-1]] <= nums[i]` (smaller elements can never be max while `i` is in window). Append `i`. Record `nums[deque[0]]` once `i >= k-1`.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def max_sliding_window(nums: list[int], k: int) -> list[int]:
>     dq: deque[int] = deque()  # stores indices; front = max of current window
>     result = []
> 
>     for i, val in enumerate(nums):
>         # Remove indices outside current window
>         if dq and dq[0] < i - k + 1:
>             dq.popleft()
>         # Maintain decreasing order: evict smaller elements from back
>         while dq and nums[dq[-1]] < val:
>             dq.pop()
>         dq.append(i)
>         if i >= k - 1:
>             result.append(nums[dq[0]])
> 
>     return result
> ```

> [!success] Complexity
> O(n) time, O(k) space.

> [!tip] Alternatives
> Segment tree or sparse table — O(n log n) build + O(1) query; overkill. Max-heap O(n log k) — correct but slower. Deque is optimal for this specific problem.

---

### Sliding Window Minimum (LC variant)

> [!example] Problem
> Array of integers, window size `k`. Return min of each window as it slides.

> [!info] Approach
> - WHY: Symmetric to sliding window maximum. Monotonic increasing deque where front = current min.
> - WHAT: Deque stores indices in increasing order of their values. Pop back while `nums[deque[-1]] >= val` (larger elements evicted — they can never be min while `val` is in window).
> - HOW: Only change from max version: reverse comparison `nums[dq[-1]] > val` (use `>=` to maintain strictly increasing, or `>` for non-strictly).

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def min_sliding_window(nums: list[int], k: int) -> list[int]:
>     dq: deque[int] = deque()  # stores indices; front = min of current window
>     result = []
> 
>     for i, val in enumerate(nums):
>         if dq and dq[0] < i - k + 1:
>             dq.popleft()
>         while dq and nums[dq[-1]] > val:
>             dq.pop()
>         dq.append(i)
>         if i >= k - 1:
>             result.append(nums[dq[0]])
> 
>     return result
> ```

> [!success] Complexity
> O(n) time, O(k) space.

> [!tip] Alternatives
> Same as sliding window maximum — deque is optimal at O(n).

> [!info] Deque Invariant
> For max → deque is decreasing (pop smaller from back). For min → deque is increasing (pop larger from back). Front always holds the extreme index for the current window; expiry check (`dq[0] < i - k + 1`) ensures it stays within bounds.

---

## See Also

[[two-pointers]] | [[hashing]] | [[string]] | [[queue]]
