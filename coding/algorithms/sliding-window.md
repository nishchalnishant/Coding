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

## Fixed Window — Threshold & Uniqueness

---

### Number of Sub-arrays of Size K and Average ≥ Threshold (LC 1343)

> [!example] Problem
> Given integer array `arr` and integers `k` and `threshold`, return the count of subarrays of size exactly `k` whose average is ≥ `threshold`.

> [!info] Approach
> - WHY: Fixed window of size `k`; average ≥ threshold ↔ sum ≥ k * threshold. Avoids float division per window.
> - WHAT: Maintain a sliding sum over every window of length `k`. Count windows where sum ≥ `k * threshold`.
> - HOW: Seed with sum of first `k` elements. Slide: add `arr[i]`, subtract `arr[i-k]`, check threshold.

> [!note]- Python Solution
> ```python
> def num_of_subarrays(arr: list[int], k: int, threshold: int) -> int:
>     target = k * threshold
>     window_sum = sum(arr[:k])
>     count = 1 if window_sum >= target else 0
>     for i in range(k, len(arr)):
>         window_sum += arr[i] - arr[i - k]
>         if window_sum >= target:
>             count += 1
>     return count
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Prefix sums give the same O(n) but with O(n) extra space; sliding sum is strictly better here.

---

### Maximum Sum of Almost Unique Subarray (LC 2841)

> [!example] Problem
> Array `nums`, integers `m` and `k`. Find the maximum sum of a subarray of length exactly `k` that contains at least `m` distinct elements.

> [!info] Approach
> - WHY: Fixed window of size `k`; track distinct count in the window alongside the running sum.
> - WHAT: Maintain a frequency map and window sum. A window qualifies when `len(freq) >= m`.
> - HOW: Slide in O(1): add right element to freq/sum, remove left element from freq/sum (delete key at 0). Check qualification after each full window.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def max_sum(nums: list[int], m: int, k: int) -> int:
>     freq: dict[int, int] = defaultdict(int)
>     window_sum = 0
>     best = 0
> 
>     for i in range(len(nums)):
>         freq[nums[i]] += 1
>         window_sum += nums[i]
>         if i >= k:
>             old = nums[i - k]
>             window_sum -= old
>             freq[old] -= 1
>             if freq[old] == 0:
>                 del freq[old]
>         if i >= k - 1 and len(freq) >= m:
>             best = max(best, window_sum)
>     return best
> ```

> [!success] Complexity
> O(n) time, O(k) space.

> [!tip] Alternatives
> Sorting within each window O(nk log k) — far too slow. Sliding window with freq map is optimal.

---

### Sliding Window Average from Data Stream (LC 346)

> [!example] Problem
> Design a class that accepts a stream of integers and, on each `next(val)` call, returns the moving average of the last `k` values.

> [!info] Approach
> - WHY: Classic FIFO fixed window over a stream. Use a circular buffer (deque) of size `k`.
> - WHAT: Maintain a running sum. When deque reaches size `k`, subtract the oldest element before appending new one.
> - HOW: `deque.popleft()` evicts oldest; `deque.append(val)` adds newest. No need to resum — O(1) update.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> class MovingAverage:
>     def __init__(self, size: int) -> None:
>         self.k = size
>         self.window: deque[int] = deque()
>         self.total = 0
> 
>     def next(self, val: int) -> float:
>         if len(self.window) == self.k:
>             self.total -= self.window.popleft()
>         self.window.append(val)
>         self.total += val
>         return self.total / len(self.window)
> ```

> [!success] Complexity
> O(1) per `next` call, O(k) space.

> [!tip] Alternatives
> Recompute sum each call O(k) per call — unnecessary; circular array with modulo index works but deque is cleaner.

---

## Variable Window — Max Length (Flip / Delete)

> [!info] Approach
> A class of problems where you can "spend" a budget (flip zeros, delete elements) to extend a valid window. The window tracks how much budget has been used; shrink when budget is exceeded. Equivalent to "at most K bad elements".

---

### Max Consecutive Ones III (LC 1004)

> [!example] Problem
> Binary array `nums`. You may flip at most `k` zeros to ones. Return the maximum number of consecutive ones.

> [!info] Approach
> - WHY: Window contains at most `k` zeros. Expanding right adds ones (free) or zeros (costs 1 from budget). When zeros in window exceed `k`, shrink left.
> - WHAT: Track `zeros` count in the window. While `zeros > k` → if `nums[left] == 0`, decrement zeros; advance left.
> - HOW: Answer is `right - left + 1` after each valid step — window never shrinks below the best size seen (LC 424 trick not needed here since we do want exact max).

> [!note]- Python Solution
> ```python
> def longest_ones(nums: list[int], k: int) -> int:
>     left = zeros = best = 0
>     for right in range(len(nums)):
>         if nums[right] == 0:
>             zeros += 1
>         while zeros > k:
>             if nums[left] == 0:
>                 zeros -= 1
>             left += 1
>         best = max(best, right - left + 1)
>     return best
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Same as "Longest Repeating Character Replacement" restricted to binary input. For k=0 this degenerates to counting max run of ones.

---

### Longest Subarray of 1s After Deleting One Element (LC 1493)

> [!example] Problem
> Binary array. Delete exactly one element. Return the length of the longest subarray of 1s in the result.

> [!info] Approach
> - WHY: Deleting one element = flipping one 0 to nothing, or dropping one 1. Equivalent to: longest window with at most one 0, minus 1 (for the deleted element).
> - WHAT: Slide window keeping `zeros <= 1`. The answer is `window_size - 1` at maximum valid window.
> - HOW: Exact same code as LC 1004 with `k=1`, subtract 1 from result. Edge: if whole array is ones, deleting one element gives `n-1`.

> [!note]- Python Solution
> ```python
> def longest_subarray(nums: list[int]) -> int:
>     left = zeros = best = 0
>     for right in range(len(nums)):
>         if nums[right] == 0:
>             zeros += 1
>         while zeros > 1:
>             if nums[left] == 0:
>                 zeros -= 1
>             left += 1
>         best = max(best, right - left + 1)
>     return best - 1   # subtract the one deleted element
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> LC 1004 with k=1 is identical before the -1 adjustment. If the array has no zeros, the answer is `len(nums) - 1`.

---

### Minimum Operations to Reduce X to Zero (LC 1658)

> [!example] Problem
> Array `nums`, integer `x`. Each operation removes either the leftmost or rightmost element and subtracts it from `x`. Find the minimum number of operations to reach exactly 0, or -1.

> [!info] Approach
> - WHY: Removing from both ends with minimum total elements ↔ keeping a maximum-length middle subarray with sum `total - x`. Reframe as max-window problem.
> - WHAT: Find the longest subarray with sum exactly `total - x`. Minimum operations = `n - len(longest subarray)`.
> - HOW: Use a variable window (shrink when sum exceeds target, track max length when sum == target). Requires all non-negative integers for monotone shrink property — guaranteed by constraints.

> [!note]- Python Solution
> ```python
> def min_operations(nums: list[int], x: int) -> int:
>     target = sum(nums) - x
>     if target < 0:
>         return -1
>     if target == 0:
>         return len(nums)
>     left = window_sum = 0
>     best = -1
>     for right in range(len(nums)):
>         window_sum += nums[right]
>         while window_sum > target and left <= right:
>             window_sum -= nums[left]
>             left += 1
>         if window_sum == target:
>             best = max(best, right - left + 1)
>     return len(nums) - best if best != -1 else -1
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Prefix sum + hashmap O(n) — works but window is cleaner. Direct two-pointer from both ends without reframe is O(n²) in naive form.

---

### Binary Subarrays with Sum (LC 930)

> [!example] Problem
> Binary array `nums`. Count subarrays with sum exactly `goal`.

> [!info] Approach
> - WHY: Exactly-k trick: binary values make at_most well-defined. `exactly(goal) = at_most(goal) - at_most(goal-1)`.
> - WHAT: `at_most(k)` counts subarrays with sum ≤ k. Each right position contributes `right - left + 1` valid subarrays when window is valid.
> - HOW: Shrink while sum > k. Handle `k < 0` edge case (return 0) to avoid infinite loop when goal=0.

> [!note]- Python Solution
> ```python
> def num_subarrays_with_sum(nums: list[int], goal: int) -> int:
>     def at_most(k: int) -> int:
>         if k < 0:
>             return 0
>         left = total = count = 0
>         for right in range(len(nums)):
>             total += nums[right]
>             while total > k:
>                 total -= nums[left]
>                 left += 1
>             count += right - left + 1
>         return count
> 
>     return at_most(goal) - at_most(goal - 1)
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Prefix sum + hashmap: `count[prefix_sum - goal]` at each position — O(n) time, O(n) space. Both are valid; at_most trick is more uniform with other sliding window problems.

---

## Variable Window — Minimum Length (All Characters / Distinct)

---

### Minimum Window with All Characters Including Duplicates

> [!example] Problem
> Generalisation of LC 76: given `s` and `t` (with duplicate characters in `t`), find the shortest window in `s` containing all characters of `t` with correct multiplicities.

> [!info] Approach
> - WHY: This IS LC 76 — the standard minimum window already handles duplicates via `missing` counter.
> - WHAT: `need[c]` tracks remaining required copies. `missing` = total characters still needed. Shrink while `missing == 0`.
> - HOW: On add: decrement `need[c]`; if it was positive, decrement `missing`. On remove: increment `need[s[left]]`; if it becomes positive, increment `missing`. This correctly handles excess copies.

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def min_window_with_duplicates(s: str, t: str) -> str:
>     need = Counter(t)
>     missing = len(t)
>     left = best_start = 0
>     best_len = float('inf')
> 
>     for right, c in enumerate(s):
>         if need[c] > 0:
>             missing -= 1
>         need[c] -= 1
> 
>         if missing == 0:
>             # Tighten from left: skip characters in excess
>             while need[s[left]] < 0:
>                 need[s[left]] += 1
>                 left += 1
>             if right - left + 1 < best_len:
>                 best_len = right - left + 1
>                 best_start = left
>             # Advance left to look for next candidate
>             need[s[left]] += 1
>             missing += 1
>             left += 1
> 
>     return s[best_start: best_start + best_len] if best_len != float('inf') else ""
> ```

> [!success] Complexity
> O(|s| + |t|) time, O(|alphabet|) space.

> [!tip] Alternatives
> Two separate left pointers (one for shrinking to exact fit, one for advancing) — functionally identical but more bookkeeping.

---

### Smallest Subarray with Distinct Element Count K

> [!example] Problem
> Given array `nums` and integer `k`, find the length of the shortest contiguous subarray that contains exactly `k` distinct elements.

> [!info] Approach
> - WHY: Minimum-length window with an exact distinct count. Expand until we have ≥ k distinct, then shrink while we still have ≥ k distinct, recording the minimum.
> - WHAT: Frequency map tracks distinct count. Once `len(freq) >= k` → window is valid → shrink left while still valid.
> - HOW: Shrink: remove `nums[left]` from freq (delete at 0); stop when `len(freq) < k`. Record window size before overshoot.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def smallest_subarray_k_distinct(nums: list[int], k: int) -> int:
>     freq: dict[int, int] = defaultdict(int)
>     left = 0
>     best = float('inf')
> 
>     for right in range(len(nums)):
>         freq[nums[right]] += 1
>         while len(freq) >= k:
>             best = min(best, right - left + 1)
>             freq[nums[left]] -= 1
>             if freq[nums[left]] == 0:
>                 del freq[nums[left]]
>             left += 1
> 
>     return best if best != float('inf') else -1
> ```

> [!success] Complexity
> O(n) time, O(k) space.

> [!tip] Alternatives
> Outer loop on left + inner scan right O(n²) — brute force. Sliding window is O(n).

---

## Sliding Window + Monotonic Deque — Variable Window

---

### Longest Continuous Subarray with Absolute Diff ≤ Limit (LC 1438)

> [!example] Problem
> Array `nums` and integer `limit`. Return the size of the longest subarray where the absolute difference between any two elements is ≤ `limit`.

> [!info] Approach
> - WHY: `max(window) - min(window) <= limit`. Need O(1) running max and min under variable window. Two deques: one decreasing (max), one increasing (min).
> - WHAT: Maintain `max_dq` (decreasing) and `min_dq` (increasing). Both store indices. When `max_dq[0] - min_dq[0] > limit` → shrink left, evicting stale front indices from both deques.
> - HOW: Shrink by advancing `left`; pop deque fronts when they equal `left` (no longer in window). Record `right - left + 1` after each valid state.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def longest_subarray(nums: list[int], limit: int) -> int:
>     max_dq: deque[int] = deque()  # decreasing → front is max
>     min_dq: deque[int] = deque()  # increasing → front is min
>     left = best = 0
> 
>     for right, val in enumerate(nums):
>         while max_dq and nums[max_dq[-1]] <= val:
>             max_dq.pop()
>         while min_dq and nums[min_dq[-1]] >= val:
>             min_dq.pop()
>         max_dq.append(right)
>         min_dq.append(right)
> 
>         while nums[max_dq[0]] - nums[min_dq[0]] > limit:
>             left += 1
>             if max_dq[0] < left:
>                 max_dq.popleft()
>             if min_dq[0] < left:
>                 min_dq.popleft()
> 
>         best = max(best, right - left + 1)
> 
>     return best
> ```

> [!success] Complexity
> O(n) time, O(n) space (deques store at most n indices total).

> [!tip] Alternatives
> Sorted container (SortedList) O(n log n) — valid but slower; segment tree O(n log n) — overkill. Two-deque is optimal O(n).

---

### Jump Game VI (LC 1696)

> [!example] Problem
> Array `nums`. Start at index 0. From index `i` you can jump to `i+1` through `i+k`. Score = sum of `nums` values at each visited index. Maximize score to reach last index.

> [!info] Approach
> - WHY: DP recurrence: `dp[i] = nums[i] + max(dp[i-k], ..., dp[i-1])`. Naive O(nk). Optimize with a decreasing deque of the last `k` dp values — front = max in range.
> - WHAT: `dp[i] = nums[i] + dp[deque_front]`. Maintain deque in decreasing dp-value order. Evict front when it's outside the `k`-window.
> - HOW: Before computing `dp[i]`: evict stale front (`dq[0] < i - k`). After computing `dp[i]`: evict back while `dp[dq[-1]] <= dp[i]`; append `i`. Space-optimise by storing dp in original array.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def max_result(nums: list[int], k: int) -> int:
>     n = len(nums)
>     dp = [0] * n
>     dp[0] = nums[0]
>     dq: deque[int] = deque()
>     dq.append(0)
> 
>     for i in range(1, n):
>         # Evict indices outside the k-window
>         while dq and dq[0] < i - k:
>             dq.popleft()
>         dp[i] = nums[i] + dp[dq[0]]
>         # Maintain decreasing deque by dp value
>         while dq and dp[dq[-1]] <= dp[i]:
>             dq.pop()
>         dq.append(i)
> 
>     return dp[n - 1]
> ```

> [!success] Complexity
> O(n) time, O(n) space (dp array + deque).

> [!tip] Alternatives
> Priority heap O(n log k) — correct but slower; sparse table for range max O(n log n) build + O(1) query, O(n log n) overall — more complex. Deque DP is the idiomatic O(n) solution.

---

## More Variable Window Problems

---

### Subarray Product Less Than K (LC 713)

> [!example] Problem
> Array of positive integers `nums` and integer `k`. Count contiguous subarrays where the product of all elements is strictly less than `k`.

> [!info] Approach
> - WHY: All elements are positive → product is monotonically non-decreasing as window expands. Shrink when product ≥ k.
> - WHAT: Maintain running product. Each valid window `[left, right]` contributes `right - left + 1` subarrays ending at `right` (all subarrays `[left..right], [left+1..right], ..., [right..right]` are valid).
> - HOW: Shrink by dividing out `nums[left]` and advancing left. Handle edge `k <= 1` upfront (product of positives is always ≥ 1).

> [!note]- Python Solution
> ```python
> def num_subarray_product_less_than_k(nums: list[int], k: int) -> int:
>     if k <= 1:
>         return 0
>     left = count = 0
>     product = 1
>     for right in range(len(nums)):
>         product *= nums[right]
>         while product >= k:
>             product //= nums[left]
>             left += 1
>         count += right - left + 1
>     return count
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Prefix products + binary search O(n log n) — works but unnecessary. Sliding window is O(n).

---

### Longest Subarray with Sum ≤ K (Nonnegative) 

> [!example] Problem
> Array of non-negative integers `nums` and integer `k`. Find the length of the longest subarray with sum ≤ `k`.

> [!info] Approach
> - WHY: Non-negative elements ensure monotone sum — expanding can only increase sum, so shrink-when-violated is valid.
> - WHAT: Expand right; when sum > k, shrink left. Track max window length after each step.
> - HOW: The while-loop shrink guarantees the window is valid at every right before recording length.

> [!note]- Python Solution
> ```python
> def longest_subarray_sum_leq_k(nums: list[int], k: int) -> int:
>     left = window_sum = best = 0
>     for right in range(len(nums)):
>         window_sum += nums[right]
>         while window_sum > k:
>             window_sum -= nums[left]
>             left += 1
>         best = max(best, right - left + 1)
>     return best
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> With negative numbers: monotone queue approach or Kadane variant needed — shrink-when-violated breaks without non-negativity guarantee.

---

### Minimum Number of Flips to Make Binary String Alternating (LC 1888)

> [!example] Problem
> Binary string `s`. In one operation you can move the leftmost character to the rightmost end. Find the minimum number of character flips to make the resulting string alternating.

> [!info] Approach
> - WHY: Rotating is equivalent to considering the string doubled (`s + s`) with a fixed window of size `n`. For each window, count mismatches with both possible alternating patterns ("0101..." and "1010..."). Answer is `min(mismatches)` over all windows.
> - WHAT: Use fixed sliding window of size `n` on `s + s`. Track mismatches with pattern-0 (`"01"` repeating) and pattern-1 (`"10"` repeating). Slide in O(1).
> - HOW: On slide out: if removed char matched pattern-0 at that position, decrement mismatch-0 count. On slide in: if new char mismatches pattern at new position, increment. Track min of both mismatch counts.

> [!note]- Python Solution
> ```python
> def min_flips(s: str) -> int:
>     n = len(s)
>     t = s + s
>     # mismatch counts with "010101..." and "101010..."
>     diff0 = diff1 = 0
>     for i in range(n):
>         expected0 = str(i % 2)          # pattern: 010101...
>         expected1 = str((i + 1) % 2)    # pattern: 101010...
>         if t[i] != expected0:
>             diff0 += 1
>         if t[i] != expected1:
>             diff1 += 1
> 
>     best = min(diff0, diff1)
>     for i in range(n, 2 * n):
>         # Add right element
>         expected0 = str(i % 2)
>         expected1 = str((i + 1) % 2)
>         if t[i] != expected0:
>             diff0 += 1
>         if t[i] != expected1:
>             diff1 += 1
>         # Remove left element (index i - n)
>         left = i - n
>         if t[left] != str(left % 2):
>             diff0 -= 1
>         if t[left] != str((left + 1) % 2):
>             diff1 -= 1
>         best = min(best, diff0, diff1)
> 
>     return best
> ```

> [!success] Complexity
> O(n) time, O(n) space (doubled string).

> [!tip] Alternatives
> Enumerate all n rotations naively O(n²) — too slow. Fixed window on doubled string is the canonical O(n) approach.

---

### Grumpy Bookstore Owner (LC 1052)

> [!example] Problem
> Arrays `customers` and `grumpy` (binary), integer `minutes`. Owner can suppress grumpiness for `minutes` consecutive minutes once. Customers in grumpy minutes are normally lost; find the maximum total satisfied customers.

> [!info] Approach
> - WHY: Base satisfied = customers where `grumpy[i] == 0`. Extra bonus = customers recovered in a window of size `minutes` where `grumpy[i] == 1`. Maximize base + max bonus window.
> - WHAT: Fixed window of size `minutes` tracking sum of `customers[i]` where `grumpy[i] == 1`. Find the window with maximum such sum.
> - HOW: Seed base with all non-grumpy customers. Slide window of size `minutes` summing only grumpy-window customers. Max bonus = best grumpy-window sum.

> [!note]- Python Solution
> ```python
> def max_satisfied(customers: list[int], grumpy: list[int], minutes: int) -> int:
>     base = sum(c for c, g in zip(customers, grumpy) if g == 0)
>     # Extra customers we can recover in a window of size `minutes`
>     extra = sum(customers[i] * grumpy[i] for i in range(minutes))
>     best_extra = extra
>     for i in range(minutes, len(customers)):
>         extra += customers[i] * grumpy[i]
>         extra -= customers[i - minutes] * grumpy[i - minutes]
>         best_extra = max(best_extra, extra)
>     return base + best_extra
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Brute force: try each starting position for the window O(n·minutes) — unnecessary; fixed sliding window is O(n).

---

### Diet Plan Performance (LC 1176)

> [!example] Problem
> Array `calories`, integers `k`, `lower`, `upper`. For every contiguous subarray of length `k`: score +1 if sum > upper, -1 if sum < lower, else 0. Return total score.

> [!info] Approach
> - WHY: Straightforward fixed window of size `k`. No state needed beyond running sum.
> - WHAT: Maintain sliding sum of exactly `k` elements. Compare to `lower` and `upper` each step.
> - HOW: Seed with first `k` elements. Slide: add right, remove left-k, evaluate.

> [!note]- Python Solution
> ```python
> def diet_plan_performance(calories: list[int], k: int, lower: int, upper: int) -> int:
>     window_sum = sum(calories[:k])
>     score = 0
>     if window_sum < lower:
>         score -= 1
>     elif window_sum > upper:
>         score += 1
>     for i in range(k, len(calories)):
>         window_sum += calories[i] - calories[i - k]
>         if window_sum < lower:
>             score -= 1
>         elif window_sum > upper:
>             score += 1
>     return score
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Prefix sums O(n) time, O(n) space — equivalent. Sliding sum is strictly more space-efficient.

---

### Count Vowel Substrings of a Word (LC 2062)

> [!example] Problem
> String `word` of lowercase letters. Count substrings that contain only vowels and include all 5 vowels at least once.

> [!info] Approach
> - WHY: Exactly-5-distinct-vowels, all characters must be vowels. Use the at_most trick restricted to vowel-only substrings.
> - WHAT: `at_most(k)` counts substrings (all vowels) with ≤ k distinct vowels. Filter non-vowels by resetting window.
> - HOW: On encountering a consonant, reset `left = right + 1` and clear freq. `exactly(5) = at_most(5) - at_most(4)`.

> [!note]- Python Solution
> ```python
> def count_vowel_substrings(word: str) -> int:
>     vowels = set("aeiou")
> 
>     def at_most(k: int) -> int:
>         freq: dict[str, int] = {}
>         left = count = 0
>         for right, c in enumerate(word):
>             if c not in vowels:
>                 freq.clear()
>                 left = right + 1
>                 continue
>             freq[c] = freq.get(c, 0) + 1
>             while len(freq) > k:
>                 lc = word[left]
>                 freq[lc] -= 1
>                 if freq[lc] == 0:
>                     del freq[lc]
>                 left += 1
>             count += right - left + 1
>         return count
> 
>     return at_most(5) - at_most(4)
> ```

> [!success] Complexity
> O(n) time, O(1) space (at most 5 keys in freq).

> [!tip] Alternatives
> Enumerate all substrings O(n²) with O(1) check — acceptable for small input but O(n) sliding window is preferred.

---

## See Also

[[two-pointers]] | [[hashing]] | [[string]] | [[queue]]
### Maximum Number of Vowels in a Substring of Given Length

> [!example] Problem
> Given a string and a fixed window length `k`, return the maximum number of vowels in any substring of length `k`.

> [!info] Approach
> - **WHY:** The window size is fixed, so every move only removes one character and adds one character. That makes the update O(1) per step.
> - **WHAT:** Maintain a running vowel count for the current window and slide it across the string.
> - **HOW:** Initialize the first window, then for each step subtract the left character, add the new right character, and update the best count.

> [!note]- Python Solution
> ```python
> def max_vowels(s: str, k: int) -> int:
>     vowels = set("aeiou")
>     cur = sum(ch in vowels for ch in s[:k])
>     best = cur
>     for i in range(k, len(s)):
>         cur += s[i] in vowels
>         cur -= s[i - k] in vowels
>         best = max(best, cur)
>     return best
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> The same fixed-window pattern works for average, distinct counts, and frequency-based substring problems.

---

## Sliding Window — More Problems

### Grumpy Bookstore Owner (LC 1052)

> [!example] Problem
> A bookstore owner is grumpy for some minutes (marked 1 in a binary array). When using a "secret technique" for `minutes` consecutive minutes, the owner is not grumpy during that window. Find the maximum total satisfied customers.

> [!info] Approach
> - **WHY:** Customers at non-grumpy minutes are always satisfied. Customers at grumpy minutes are only satisfied during the technique window. We want to choose the `minutes`-long window that maximises the extra customers gained.
> - **WHAT:** Base count = sum of `customers[i]` where `grumpy[i] == 0`. Extra count for a window = sum of `customers[i]` where `grumpy[i] == 1` within the window. Slide a fixed window of size `minutes` to find the maximum extra.
> - **HOW:** Compute base. Slide window: at each step, add `customers[right] * grumpy[right]` and subtract `customers[right - minutes] * grumpy[right - minutes]`. Track max window extra.

> [!note]- Python Solution
> ```python
> def max_satisfied(customers: list[int], grumpy: list[int], minutes: int) -> int:
>     n = len(customers)
>     base = sum(customers[i] for i in range(n) if grumpy[i] == 0)
>     window_extra = sum(customers[i] * grumpy[i] for i in range(minutes))
>     max_extra = window_extra
>     for i in range(minutes, n):
>         window_extra += customers[i] * grumpy[i]
>         window_extra -= customers[i - minutes] * grumpy[i - minutes]
>         max_extra = max(max_extra, window_extra)
>     return base + max_extra
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Brute force O(n * minutes): slide and recompute the window sum from scratch each step.
> - Key insight: separate "always satisfied" from "sometimes satisfied" — only the grumpy minutes within the window contribute to the extra gain.

---

### Minimum Number of Flips to Make Binary String Alternating (LC 1888)

> [!example] Problem
> Given a binary string, you can do cyclic shifts (moving the first character to the end). Find the minimum number of character flips to make the string alternating after any number of shifts.

> [!info] Approach
> - **WHY:** There are only two valid alternating patterns: "0101..." and "1010...". Simulate all cyclic shifts by doubling the string and using a sliding window of length `n`.
> - **WHAT:** Double the string (`s + s`). For each window of length `n`, count the differences from both target patterns. Take the minimum differences seen across all windows.
> - **HOW:** Use a sliding window on `s + s`. Maintain the count of mismatches with pattern "010101..." and "101010...". Slide: subtract the outgoing character's mismatch contribution, add the incoming character's. Track the minimum.

> [!note]- Python Solution
> ```python
> def min_flips(s: str) -> int:
>     n = len(s)
>     doubled = s + s
>     diff0 = 0   # mismatches vs "010101..."
>     diff1 = 0   # mismatches vs "101010..."
>     for i in range(n):
>         expected0 = '0' if i % 2 == 0 else '1'
>         expected1 = '1' if i % 2 == 0 else '0'
>         if doubled[i] != expected0:
>             diff0 += 1
>         if doubled[i] != expected1:
>             diff1 += 1
>     result = min(diff0, diff1)
>     for i in range(n, 2 * n):
>         incoming_pos = i % n
>         expected0_in = '0' if i % 2 == 0 else '1'
>         expected1_in = '1' if i % 2 == 0 else '0'
>         if doubled[i] != expected0_in:
>             diff0 += 1
>         if doubled[i] != expected1_in:
>             diff1 += 1
>         outgoing_pos = i - n
>         expected0_out = '0' if outgoing_pos % 2 == 0 else '1'
>         expected1_out = '1' if outgoing_pos % 2 == 0 else '0'
>         if doubled[outgoing_pos] != expected0_out:
>             diff0 -= 1
>         if doubled[outgoing_pos] != expected1_out:
>             diff1 -= 1
>         result = min(result, diff0, diff1)
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(n) for the doubled string.

> [!tip] Alternatives
> - O(n²) brute force: try every cyclic shift, count flips each time.
> - Key insight: doubling the string converts cyclic shifts into a standard sliding window on a linear string.

---

## See Also

[[two-pointers]] | [[array]] | [[hashing]] | [[string-algorithms]]
