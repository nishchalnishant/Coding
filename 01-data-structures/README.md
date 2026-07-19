# Data Structures — Google L3 Cheat Sheet

> [!NOTE]
> **Tier Legend**
> `⚡ T1` — **TIER 1 · Must Master**: Reflexive recall required. These appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: Know the core pattern cold; edge cases matter less.

---

## L3 at a Glance

Google L3 (SWE) loops are **4–5 coding rounds**, one problem each, **35–45 minutes**. Expect **medium** problems (occasionally medium-hard). You are graded on clarifying, communicating, choosing the right approach, clean code, dry-run, and stating complexity — not on memorizing obscure tricks.

| What L3 tests | What L3 does **not** test |
| :--- | :--- |
| BFS/DFS, heaps, sliding window, binary search on answer, tries, basic DP | System design, LLD, concurrency, SQL |
| Hash maps, two pointers, trees, union-find, topo sort | Segment trees, bitmask DP, Tarjan SCC |
| Googliness / behavioral (often 1 round) | ML theory (even on AI/ML loops — still DSA) |

**Companion files**

| Purpose | Link |
| :--- | :--- |
| Full L3 roadmap + 4-week schedule | [`coding/l3-google-roadmap.md`](../coding/l3-google-roadmap.md) |
| 45-min pacing + constraint → Big-O heuristics | [`00-L3-EXECUTION-META/L3_CHEATSHEET.md`](../00-L3-EXECUTION-META/L3_CHEATSHEET.md) |
| Problem walkthroughs (code + approach) | [`coding/data-structures/`](../coding/data-structures/) |
| 30-min pattern revision | [`MINDMAP.md`](../MINDMAP.md) · [`FLOWCHARTS.md`](../FLOWCHARTS.md) |
| Behavioral / Googliness | [`04-behavioral/BEHAVIORAL_GOOGLINESS.md`](../04-behavioral/BEHAVIORAL_GOOGLINESS.md) |

### L3 study order (data structures)

Study **T1 topics first**, in this order. Each block = read the deep-dive file, then solve 2–3 problems cold from the Questions table below.

| Week | Topics | Deep-dive files |
| :--- | :--- | :--- |
| 1 | Array, Hashing, Graphs (BFS/DFS) | `01-array.md`, `02-hashing.md`, `13-graphs.md` |
| 2 | Heap, Queue (BFS patterns), Trie | `10-heap.md`, `06-queue.md`, `09-trie.md` |
| 3 | Tree, Stack, Linked List | `08-tree.md`, `05-stack.md`, `07-linked-list.md` |
| 4 | String + integration mocks | `03-string.md` + timed mocks |

> **Practice bar:** For each `⚡ T1` topic, you should be able to code the top 3 problems **without notes** in under 25 minutes and explain time/space complexity out loud.

### L3 readiness checklist

Before your onsite, you should be able to say **yes** to all of these:

- [ ] **Array/Hashing:** Two Sum, Subarray Sum Equals K, 3Sum — pattern and complexity without hesitation
- [ ] **Graphs:** Number of Islands, Rotting Oranges, Course Schedule — BFS vs DFS choice in one sentence
- [ ] **Graphs:** Word Ladder, Pacific Atlantic — multi-source BFS / reverse-from-border explained
- [ ] **Heap:** Kth Largest, Merge K Lists, Find Median from Data Stream — min-heap vs two-heap
- [ ] **Trie:** Implement Trie, Word Search II — insert/search and grid DFS + prune
- [ ] **Tree:** LCA, Validate BST, Level Order, Max Path Sum — postorder vs BFS
- [ ] **Linked List:** Reverse, Cycle (Floyd), LRU Cache — three-pointer and DLL+map
- [ ] **Stack/Queue:** Valid Parentheses, Daily Temperatures, Sliding Window Maximum — monotonic stack/deque
- [ ] **Edge cases:** empty input, single element, duplicates, disconnected graph, skewed tree — mention proactively in every round

### Skip for L3

**Segment trees and Fenwick trees (BIT) are not L3 material** — know the one-line idea; do not implement. Use prefix sum, monotonic deque, or heap instead.

→ [What to Skip at L3](../00-L3-EXECUTION-META/L3_CHEATSHEET.md)

Also out of scope: consistent hashing, skip lists, Tarjan SCC, bitmask/digit DP. Ignore if you find old references elsewhere.

---

## Index

| Topic | Section | Tier |
| :---- | :------ | :--- |
| Array | [Deep-dive](01-array.md) | `⚡ T1` |
| Hashing | [Deep-dive](02-hashing.md) | `⚡ T1` |
| String | [Deep-dive](03-string.md) | `🎯 T2` |
| Stack | [Deep-dive](05-stack.md) | `🎯 T2` |
| Queue | [Deep-dive](06-queue.md) | `🎯 T2` |
| Linked List | [Deep-dive](07-linked-list.md) | `🎯 T2` |
| Tree | [Deep-dive](08-tree.md) | `⚡ T1` |
| Trie | [Deep-dive](09-trie.md) | `⚡ T1` |
| Heap / Priority Queue | [Deep-dive](10-heap.md) | `⚡ T1` |
| Graphs | [Deep-dive](13-graphs.md) | `⚡ T1` |

---

- [ ] Array
    - Alternatives
        - vs Linked List: Array O(1) random access vs Linked List O(n) access; LL wins on O(1) insert/delete at a known pointer.
        - vs HashMap: Array requires integer indices; HashMap supports arbitrary keys and O(1) lookup.
        - vs Deque: Array O(n) prepend; Deque O(1) push/pop at both ends.
    - When to choose Array: index-based access is frequent, memory locality matters (CPU cache), size is known or bounded.
    - Key Techniques
        - **Two Pointers:** In-place reversal, partition, sorted merge, no-extra-space subarray. O(N) time, O(1) space.
        - **Sliding Window:** Fixed or variable-length subarray problems. Variable window breaks on negatives — use prefix sums + map instead.
        - **Prefix Sum:** Range sum queries after O(N) build; works with negatives. Use `prefix[0] = 0` sentinel to avoid off-by-one.
        - **Difference Array:** Range increment/decrement updates; O(1) update, O(N) reconstruct.
        - **Kadane's Algorithm:** Maximum subarray sum in a single pass. Also track `min_prod` when doing max product (negatives flip sign).
        - **Dutch National Flag:** 3-way partition (sort 0/1/2) without extra space. Do NOT increment `mid` after swap with `hi`.
        - **Binary Search on Answer:** "Find minimum K such that condition holds" — `feasible(mid)` predicate; O(N log N).
    - Gotchas
        - Variable sliding window breaks on negatives — negative values mean shrinking the window doesn't decrease the sum; use prefix sums + map instead.
        - Prefix sum off-by-one — use `prefix[0] = 0` sentinel so `range(l, r)` sums to `prefix[r] - prefix[l]` without special cases.
        - Two-pointer collision — for unsorted arrays, two-pointer only works after sorting or with a specific invariant.
        - In-place reversal loses next pointer — save `arr[right]` before overwriting.
        - `list.pop(0)` in Python is O(N) — use `collections.deque` instead.
    - Questions — Array `⚡ T1 / 🎯 T2`
        - **Two Sum `⚡ T1`**
            - Description: Given an array and target, return indices of the two numbers that add up to target. Exactly one solution exists.
            - Pattern: Hash Map complement
            - Key insight: store `target - num → index` in a single pass; O(N) vs O(N log N) sort+binary search.
        - **Best Time to Buy and Sell Stock `⚡ T1`**
            - Description: Given daily prices, find the maximum profit from a single buy-then-sell transaction. Return 0 if no profit possible.
            - Pattern: Kadane's / Greedy
            - Key insight: track running min price; `max_profit = max(price - min_price_so_far)`. O(N) O(1).
        - **Maximum Subarray `⚡ T1`**
            - Description: Find the contiguous subarray (at least one element) with the largest sum and return its sum.
            - Pattern: Kadane's
            - Key insight: `curr = max(num, curr + num)`; if `curr < 0` reset; O(N) O(1).
        - **Product of Array Except Self `⚡ T1`**
            - Description: Return an array where output[i] is the product of all elements except nums[i]. No division allowed; O(N) time.
            - Pattern: Prefix + Suffix Product
            - Key insight: left pass stores prefix; right pass multiplies suffix in-place. O(1) extra space (output array doesn't count).
        - **Contains Duplicate `⚡ T1`**
            - Description: Given an integer array, return true if any value appears at least twice, false if all elements are distinct.
            - Pattern: Hash Set
            - Key insight: one-pass set membership check; O(N) time.
        - **Trapping Rain Water `⚡ T1`**
            - Description: Given an elevation map of bar heights, compute how much rainwater can be trapped after rain.
            - Pattern: Two Pointers / Monotonic Stack
            - Key insight: two pointers — `water[i] = min(left_max, right_max) - h[i]`; advance the shorter side. O(N) O(1).
            - Gotcha: two-pointer and monotonic stack are both O(N) — know both approaches.
        - **Sliding Window Maximum `⚡ T1`**
            - Description: Given an integer array and window size k, return the maximum value in each sliding window of size k.
            - Pattern: Monotonic Deque
            - Key insight: deque of indices in decreasing-value order; front = max; pop expired from front.
            - Gotcha: store indices, not values — you need the index to check if front is expired.
        - **Subarray Sum Equals K `⚡ T1`**
            - Description: Given an integer array and k, count the total number of contiguous subarrays whose sum equals k.
            - Pattern: Prefix Sum + HashMap
            - Key insight: `prefix_count[curr_sum - k]` gives count of subarrays ending here; O(N).
        - **Merge Intervals `⚡ T1`**
            - Description: Given a collection of intervals, merge all overlapping intervals and return the result.
            - Pattern: Sort + Greedy
            - Key insight: sort by start; merge if `curr_start <= prev_end`. Extend `prev_end = max(prev_end, curr_end)` for contained intervals.
        - **3Sum `⚡ T1`**
            - Description: Given an integer array, find all unique triplets [a,b,c] such that a + b + c = 0.
            - Pattern: Sort + Two Pointers
            - Key insight: sort; fix `nums[i]`; two-pointer on `[i+1..]`; skip duplicate anchors AND inner pointers.
            - Gotcha: skip ALL equal values at each pointer level, not just one.
        - **Container With Most Water `⚡ T1`**
            - Description: Given n vertical lines with heights, find two lines that form a container holding the most water.
            - Pattern: Converging Two Pointers
            - Key insight: move the **shorter** side — taller side can never increase `min(h[lo], h[hi])`.
        - **Maximum Product Subarray `🎯 T2`**
            - Description: Find the contiguous subarray with the largest product and return that product.
            - Pattern: Kadane's variant
            - Key insight: track both `max_prod` and `min_prod` — negatives flip sign on multiply.
        - **Find Minimum in Rotated Sorted Array `🎯 T2`**
            - Description: A sorted array rotated at some pivot. Find and return the minimum element in O(log N).
            - Pattern: Binary Search
            - Key insight: if `nums[mid] > nums[hi]`: min in right half; else `hi = mid`.
        - **Search in Rotated Sorted Array `🎯 T2`**
            - Description: A sorted array has been rotated at an unknown pivot. Search for a target and return its index, or -1.
            - Pattern: Binary Search
            - Key insight: determine which half is sorted; check if target falls within that half.
        - **Jump Game `🎯 T2`**
            - Description: Given nums[i] = max jump from index i, determine if you can reach the last index from index 0.
            - Pattern: Greedy
            - Key insight: track `farthest`; if `i > farthest` unreachable; else `farthest = max(farthest, i + nums[i])`.
        - **Next Permutation `🎯 T2`**
            - Description: Rearrange nums into the next lexicographically greater permutation in-place. If no greater permutation exists, rearrange to smallest.
            - Pattern: In-place Rearrangement
            - Key insight: find rightmost ascent; swap with smallest larger element to its right; reverse suffix.
        - **Rotate Array `🎯 T2`**
            - Description: Rotate an integer array to the right by k steps in-place.
            - Pattern: Triple Reversal
            - Key insight: reverse all → reverse first k → reverse last n-k. O(1) space.
        - **Majority Element `🎯 T2`**
            - Description: Find the element that appears more than ⌊n/2⌋ times in the array. It always exists.
            - Pattern: Boyer-Moore Voting
            - Key insight: `count = 0` → new candidate; majority always survives all cancellations.

---

- [ ] Hashing
    - Alternatives
        - vs Array: HashMap supports arbitrary key types and O(1) lookup; Array requires integer indices and is cache-friendlier.
        - vs BST/TreeMap: HashMap O(1) avg but no ordering; BST O(log N) all ops + range queries + sorted iteration.
        - vs Trie: HashMap for exact key lookup; Trie for O(L) prefix queries sharing memory for common prefixes.
    - When to choose HashMap: key is not a contiguous integer, frequent O(1) exact lookups, frequency counting, or complement-based matching.
    - Key Techniques
        - **Two-Sum pattern:** Store `complement → index` during a single pass.
        - **Frequency Counter:** `Counter(arr)` or `defaultdict(int)` — O(N) build.
        - **Grouping / Anagram:** Key = sorted chars or character frequency tuple.
        - **Seen-Before / Deduplication:** Set membership O(1) vs sorted array O(log N).
        - **LRU Cache:** HashMap + Doubly Linked List → O(1) get and put.
    - Gotchas
        - Mutable keys — Python `list` or `dict` cannot be dict keys; use `tuple` or `frozenset`.
        - Custom objects — must implement both `__hash__` and `__eq__`; changing one without the other breaks invariants.
        - Rolling hash overflow — use modular arithmetic; Python hides this but other languages don't.
        - Worst case O(N) — all keys can hash to the same bucket under adversarial input (hash DoS). Python uses random seed per session.
    - Questions — Hashing `⚡ T1 / 🎯 T2`
        - **Two Sum `⚡ T1`**
            - Description: Given an array and target, return indices of the two numbers that add up to target. Exactly one solution exists.
            - Pattern: HashMap Complement
            - Key insight: `seen[target - num]`; single pass; O(N).
        - **Group Anagrams `⚡ T1`**
            - Description: Given a list of strings, group the anagrams together. Return groups in any order.
            - Pattern: Sort-as-Key Grouping
            - Key insight: `defaultdict(list)`; key = `tuple(sorted(word))`.
        - **Top K Frequent Elements `⚡ T1`**
            - Description: Given an integer array, return the k most frequent elements. Answer may be in any order.
            - Pattern: Counter + Min-Heap or Bucket Sort
            - Key insight: bucket sort is O(N) — prefer when K ≈ N or K not given.
        - **Valid Anagram `⚡ T1`**
            - Description: Given two strings s and t, return true if t is an anagram of s (same chars, same frequency).
            - Pattern: Frequency Count
            - Key insight: two Counter dicts; or one dict — increment for s, decrement for t.
        - **Longest Consecutive Sequence `⚡ T1`**
            - Description: Find the length of the longest sequence of consecutive integers in an unsorted array. Must be O(N).
            - Pattern: HashSet + Smart Start
            - Key insight: only start counting from `n` if `n-1` not in set; O(N).
        - **Subarray Sum Equals K `⚡ T1`**
            - Description: Given an integer array and k, count the total number of contiguous subarrays whose sum equals k.
            - Pattern: Prefix Sum + Map
            - Key insight: `prefix_count[curr - k]` gives count of valid left endpoints; O(N).
        - **LRU Cache `🎯 T2`**
            - Description: Design a data structure supporting O(1) get(key) and put(key, value), evicting the Least Recently Used entry when capacity is exceeded.
            - Pattern: HashMap + DLL
            - Key insight: DLL for O(1) recency-order; map for O(1) node access; dummy head/tail.
            - Gotcha: `put` on key-hit must remove old node FIRST then insert fresh — skipping remove corrupts recency order.
        - **Ransom Note `🎯 T2`**
            - Description: Given two strings ransomNote and magazine, return true if ransomNote can be constructed using letters from magazine (each used once).
            - Pattern: Frequency Count
            - Key insight: magazine letter counter ≥ ransom letter counter for each char.
        - **4Sum II `🎯 T2`**
            - Description: Given four integer arrays A, B, C, D of length n, count tuples (i,j,k,l) such that A[i]+B[j]+C[k]+D[l] == 0.
            - Pattern: Two-Pair Hash Map
            - Key insight: count all `a+b` sums; for `c+d`, look up `-(c+d)`.

---

- [ ] String
    - Alternatives
        - vs Trie: String simple exact search; Trie O(L) prefix lookup across many patterns.
        - vs Suffix Array: Linear scan O(N·M); Suffix Array O((N+M) log N) pattern match after build.
        - vs KMP/Z-function: O(N·M) naive; KMP/Z O(N+M) single pattern match.
    - Key Techniques
        - **Sliding Window + Frequency Map:** "Minimum window containing all chars of T" — track `have` vs `need`; shrink left when valid.
        - **Two Pointers:** Valid palindrome; reverse words in-place.
        - **KMP / Z-function:** Single pattern matching in O(N+M).
        - **Rabin-Karp Rolling Hash:** Substring search; anagram matching.
        - **Palindrome — Expand Around Center:** Longest palindromic substring; O(N²) simple, O(N) Manacher.
    - Gotchas
        - Python strings are **immutable** — repeated concatenation is O(N²); always use `list` then `"".join()`.
        - `ord(ch) - ord('a')` for frequency arrays — safer than dict for fixed 26-char alphabet.
        - Sliding window with character counts: decrement count first, then check if it drops below 0 (not equal to 0) to know if the character was required.
    - Questions — String `⚡ T1 / 🎯 T2`
        - **Minimum Window Substring `⚡ T1`**
            - Description: Given strings s and t, find the minimum window in s that contains every character in t (including duplicates).
            - Pattern: Sliding Window + Frequency
            - Key insight: track `missing` count. Expand right to fulfill need; shrink left while `missing == 0` to minimize window. Record on valid shrink. O(N+M).
        - **Longest Substring Without Repeating `⚡ T1`**
            - Description: Find the length of the longest substring that contains no repeated characters.
            - Pattern: Sliding Window + Dict
            - Key insight: `left = max(left, seen[ch] + 1)` on duplicate — only jump if char is inside window; O(N).
        - **Find All Anagrams in a String `⚡ T1`**
            - Description: Given strings s and p, find all starting indices in s where a substring is an anagram of p.
            - Pattern: Fixed Sliding Window
            - Key insight: window size = `len(p)`; match-count trick avoids full dict compare each step.
        - **Permutation in String `⚡ T1`**
            - Description: Given strings s1 and s2, return true if any permutation of s1 is a substring of s2.
            - Pattern: Fixed Sliding Window
            - Key insight: identical to anagram check — window = `len(s1)`. Return True if any window matches.
        - **Group Anagrams `⚡ T1`**
            - Description: Given a list of strings, group the anagrams together. Return groups in any order.
            - Pattern: Sort-as-Key
            - Key insight: `tuple(sorted(s))` as group key; `defaultdict(list)`.
        - **Longest Repeating Character Replacement `⚡ T1`**
            - Description: Given string s and integer k, find the length of the longest substring where you can change at most k characters to all be the same letter.
            - Pattern: Variable Sliding Window
            - Key insight: window valid if `(window_len - max_freq) <= k`; never shrink `max_freq` — the answer only grows.
        - **Encode and Decode Strings `🎯 T2`**
            - Description: Design encode(list[str]) → str and decode(str) → list[str] functions. Must handle any characters including '#' and '/'.
            - Pattern: Length-Prefixed Framing
            - Key insight: `"4#word"` format; no delimiter collision regardless of content.
        - **Valid Palindrome `🎯 T2`**
            - Description: Given string s, return true if it reads the same forward and backward, considering only alphanumeric characters (case-insensitive).
            - Pattern: Two Pointers
            - Key insight: skip non-alphanumeric with `isalnum()`; `lower()` then compare.
        - **Longest Palindromic Substring `🎯 T2`**
            - Description: Given string s, find and return the longest substring that is a palindrome.
            - Pattern: Expand Around Center
            - Key insight: expand odd (index center) and even (gap center); O(N²).
        - **Palindromic Substrings `🎯 T2`**
            - Description: Count how many substrings of s are palindromes. Single characters count.
            - Pattern: Expand Around Center
            - Key insight: count both odd and even expansions from each center.
        - **Reverse Words in a String `🎯 T2`**
            - Description: Given a string of words separated by spaces, reverse the order of words. Remove leading/trailing/extra spaces.
            - Pattern: Two Pointers / Split
            - Key insight: `" ".join(s.split()[::-1])`; or in-place: reverse all, then reverse each word.

---

- [ ] Stack
    - Alternatives
        - vs Queue: Stack is LIFO — DFS, undo, backtrack; Queue is FIFO — BFS, level-order, scheduling.
        - vs Recursion: Explicit stack avoids call-stack overflow; recursion is cleaner but risks overflow on deep inputs.
        - vs Deque: Stack is LIFO-only; Deque O(1) at both ends — use when sliding window max/min needed.
    - Key Techniques
        - **Monotonic Stack (Decreasing):** "Next greater element", "daily temperatures" — O(N) vs O(N²) brute force.
        - **Monotonic Stack (Increasing):** "Largest rectangle in histogram" — pop on shorter bar, compute area.
        - **Valid Parentheses:** Push opens; pop and verify on close; empty stack at end = valid.
        - **Min Stack:** Parallel auxiliary stack tracking current minimum per depth level.
        - **Expression Evaluation:** Stack saves `(result, sign)` on `(`; restores on `)`.
        - **DFS Simulation:** Replace recursion with explicit stack; push neighbors in reverse order.
    - Gotchas
        - Check `not stack` before `pop()` or `stack[-1]` — IndexError on empty stack is the most common stack bug.
        - Store indices, not values — you need the index for distance computation (`i - j`) and result-array filling.
        - Monotonic stack invariant — if you get the push/pop condition backwards, you find "next smaller" instead of "next greater" — trace one small example first.
        - `while...else` in Python — the `else` block executes only if the loop completed without `break`; useful for asteroid collision pattern.
    - Questions — Stack `⚡ T1 / 🎯 T2`
        - **Valid Parentheses `⚡ T1`**
            - Description: Given a string of '(', ')', '{', '}', '[', ']', determine if the input string is valid (brackets open and close in correct order).
            - Pattern: Bracket Matching
            - Key insight: map `')':'('`; push opens, pop-and-match closes; empty stack at end = valid.
        - **Trapping Rain Water `⚡ T1`**
            - Description: Given an elevation map of bar heights, compute how much rainwater can be trapped after rain.
            - Pattern: Monotonic Stack / Two Pointers
            - Key insight: decreasing stack — pop bar, `width = i - stack[-1] - 1`, `height = diff`; or two-pointer O(1) space.
        - **Daily Temperatures `⚡ T1`**
            - Description: Given daily temperatures, return an array where answer[i] is the number of days until a warmer temperature. 0 if none.
            - Pattern: Monotonic Stack (Decreasing)
            - Key insight: stack of indices; `result[j] = i - j` when warmer temp found.
        - **Largest Rectangle in Histogram `⚡ T1`**
            - Description: Given bar heights of a histogram, find the area of the largest rectangle that can be formed within the histogram.
            - Pattern: Monotonic Stack (Increasing)
            - Key insight: pop on shorter bar; `width = i - stack[-1] - 1`; append sentinel `0` to flush at end.
        - **Min Stack `🎯 T2`**
            - Description: Design a stack that supports push, pop, top, and getMin() — all in O(1) time.
            - Pattern: Parallel Min-Stack
            - Key insight: push `min(val, min_stack[-1])` to aux; pop in sync.
        - **Implement Queue using Stacks `🎯 T2`**
            - Description: Implement a FIFO queue using only two stacks. push, pop, peek, and empty must all work correctly.
            - Pattern: Two-Stack Queue
            - Key insight: lazy transfer — pour s1→s2 only when s2 empty; amortized O(1).
        - **Next Greater Element I/II `🎯 T2`**
            - Description: I: For each element of nums1 find its next greater element in nums2. II: Find next greater element in a circular array.
            - Pattern: Monotonic Stack
            - Key insight: I — map next greater via stack + dict; II (circular) — iterate `0..2N-1` with `% N`.
        - **Evaluate RPN `🎯 T2`**
            - Description: Evaluate the value of an arithmetic expression in Reverse Polish Notation with operators +, -, *, /.
            - Pattern: Operand Stack
            - Key insight: operand → push. Operator → pop two, compute, push result.
        - **Decode String `🎯 T2`**
            - Description: Given an encoded string like '3[a2[bc]]', decode it to 'abcbcabcbc'. Numbers can be multi-digit.
            - Pattern: Context Stack
            - Key insight: push `(built_str, repeat_k)` on `[`; unwind on `]`; handle multi-digit k.
        - **Maximal Rectangle `🎯 T2`**
            - Description: Given a binary matrix of '0's and '1's, find the largest rectangle containing only '1's and return its area.
            - Pattern: Histogram per Row
            - Key insight: build height array row-by-row; apply Largest Rectangle per row.
        - **Basic Calculator I/II `🎯 T2`**
            - Description: Implement a calculator to evaluate an expression string containing +, -, (, ) and non-negative integers (I), or +, -, *, / (II).
            - Pattern: Expression Stack
            - Key insight: save `(result, sign)` on `(`; restore on `)`; handle `*`/`/` with prev-op slot.
        - **Asteroid Collision `🎯 T2`**
            - Description: Given asteroids moving left (negative) or right (positive), simulate collisions. Return the final state.
            - Pattern: LIFO Simulation
            - Key insight: stack = surviving right-movers; pop while left-mover larger; `while...else`.
        - **Remove K Digits `🎯 T2`**
            - Description: Remove k digits from a number string to get the smallest possible number. Return it without leading zeros.
            - Pattern: Monotonic Stack
            - Key insight: increasing stack; pop when `top > curr` and `k > 0`; strip leading zeros.

---

- [ ] Queue
    - Alternatives
        - vs Stack: Queue is FIFO — BFS, level-order; Stack is LIFO — DFS, undo.
        - vs Priority Queue: Queue processes in arrival order; PQ processes by priority O(log N) push/pop.
        - vs Deque: Queue is one-ended FIFO; Deque O(1) at both ends — sliding window, palindrome.
    - Key Techniques
        - **BFS Shortest Path:** Unweighted graph; mark visited **before enqueue** (not after dequeue — classic TLE bug).
        - **Multi-Source BFS:** Seed ALL sources at distance 0; single O(V+E) pass vs O(S×(V+E)) per-source.
        - **Monotonic Deque:** Sliding window max/min in O(N); store indices (not values) to detect window expiry.
        - **Two-Stack Queue:** "Implement queue using two stacks"; lazy O(1) amortized transfer.
        - **Circular Ring Buffer:** Fixed-capacity producer-consumer; `front`/`size`/`cap` + mod arithmetic.
    - Gotchas
        - `list.pop(0)` is O(N) — always use `collections.deque` with `.popleft()`; this is the #1 silent TLE cause.
        - Mark visited before enqueue, not after dequeue — marking after dequeue allows the same node to be enqueued multiple times → duplicate processing and wrong distances.
        - Multi-source BFS: never run independent BFS from each source — O(S × (V+E)) vs O(V+E) for multi-source.
        - Monotonic deque stores indices: storing values loses the ability to detect window expiry (`dq[0] <= i - k`).
    - Questions — Queue `⚡ T1 / 🎯 T2`
        - **Sliding Window Maximum `⚡ T1`**
            - Description: Given an integer array and window size k, return the maximum value in each sliding window of size k.
            - Pattern: Monotonic Deque
            - Key insight: indices in decreasing value order; front = max of current window; pop expired from front.
        - **Rotten Oranges `⚡ T1`**
            - Description: In a grid of fresh (1) and rotten (2) oranges, every minute rotten oranges spread to 4-adjacent fresh ones. Return min minutes to rot all, or -1 if impossible.
            - Pattern: Multi-Source BFS
            - Key insight: all rotten at t=0; count fresh; -1 if fresh remain after BFS.
        - **01 Matrix `⚡ T1`**
            - Description: Given a binary matrix, return a matrix where each cell contains the distance to the nearest 0 cell.
            - Pattern: Multi-Source BFS
            - Key insight: BFS from all 0s simultaneously; each 1 gets distance from nearest 0.
        - **Walls and Gates `⚡ T1`**
            - Description: Fill each empty room (INF) in a grid with the distance to its nearest gate (0). Walls are -1.
            - Pattern: Multi-Source BFS
            - Key insight: BFS from all gates simultaneously; distances propagate outward.
        - **Shortest Path in Binary Matrix `⚡ T1`**
            - Description: Find the length of the shortest clear path from top-left to bottom-right of a binary matrix (8-directional, through 0s). Return -1 if none.
            - Pattern: BFS (8-directional)
            - Key insight: 8-directional open (0) cells; return -1 if start/end blocked.
        - **Word Ladder `⚡ T1`**
            - Description: Given beginWord, endWord, and a word list, find the length of the shortest transformation sequence where each step changes one letter and every intermediate word is in the list.
            - Pattern: BFS on Words
            - Key insight: neighbors = one-letter edits in dict; remove from set when visited to avoid revisiting.
        - **Open the Lock `⚡ T1`**
            - Description: Starting at '0000', find the minimum number of turns to reach a target combination, avoiding a set of deadend combinations.
            - Pattern: BFS on States
            - Key insight: state = 4-digit string; 8 neighbors per state (±1 on each wheel).
        - **Minimum Knight Moves `⚡ T1`**
            - Description: Find the minimum number of knight moves to reach position (x, y) from (0, 0) on an infinite chessboard.
            - Pattern: BFS / Symmetry
            - Key insight: BFS from `(0,0)`; exploit `(abs(x), abs(y))` symmetry to limit state space.
        - **Design Circular Queue `🎯 T2`**
            - Description: Design a circular queue (ring buffer) with enQueue, deQueue, Front, Rear, isEmpty, isFull operations.
            - Pattern: Ring Buffer
            - Key insight: `rear = (front + size) % cap`; size counter avoids wasted-slot ambiguity.
        - **Implement Queue using Stacks `🎯 T2`**
            - Description: Implement a FIFO queue using only two stacks. push, pop, peek, and empty must all work correctly.
            - Pattern: Two-Stack Queue
            - Key insight: push to s1; pop from s2 (refill from s1 lazily if s2 empty); amortized O(1).
        - **Moving Average from Data Stream `🎯 T2`**
            - Description: Calculate the moving average of the last n numbers in a stream after each insertion.
            - Pattern: Fixed-Size Deque
            - Key insight: evict front when over capacity; maintain running sum.

---

- [ ] Linked List
    - Alternatives
        - vs Array: Linked list allows O(1) insert/delete at known pointer; lacks O(1) random access. Array O(1) random access; O(N) mid-insert.
        - vs Deque: Linked list is cache-unfriendly; no random access. Deque is array-backed; better cache performance.
        - vs Skip List: Linked list O(N) search; Skip List O(log N) probabilistic search (used in Redis ZSET).
    - When to choose DLL specifically: O(1) delete-given-node is required (LRU Cache, undo history).
    - Key Techniques
        - **Dummy Node:** Head may change (merge, delete head) — `dummy.next = head; return dummy.next`.
        - **Fast & Slow Pointers (Floyd's):** Find middle; detect cycle; find cycle entry. `slow += 1, fast += 2`.
        - **In-Place Reversal:** O(1) space reversal; palindrome; reorder list. `prev, curr, nxt` three-pointer dance.
        - **Two-Pointer with Offset:** Remove Nth from end without knowing length — advance fast by N first; both advance together.
        - **LRU Cache:** O(1) get/put with eviction — DLL (recency order) + HashMap (O(1) node access).
    - Gotchas
        - Save `nxt = curr.next` FIRST — overwriting `curr.next = prev` before saving `nxt` loses the rest of the list. The #1 linked list bug.
        - Use `is` not `==` for cycle detection — `slow is fast` (identity), not `slow == fast` (value); two nodes with equal values would give a false positive.
        - Dummy head eliminates edge cases — removing the actual head node, merging empty lists, or inserting at the front all need special handling without dummy node.
        - Even-length list middle — with `while fast and fast.next`, slow lands on the **left-middle**; clarify which middle the problem wants.
        - LRU Cache `put` must update on key-hit — remove old node first, then insert fresh; skipping remove on key-hit corrupts recency order.
    - Questions — Linked List `⚡ T1 / 🎯 T2`
        - **Reverse Linked List `⚡ T1`**
            - Description: Reverse a singly linked list and return the new head. Do it iteratively in O(1) space.
            - Pattern: Iterative Pointer Reversal
            - Key insight: `nxt = curr.next; curr.next = prev; prev, curr = curr, nxt` — save nxt FIRST or you lose the tail.
        - **Linked List Cycle `⚡ T1`**
            - Description: Given head of a linked list, determine if it contains a cycle. Return true/false.
            - Pattern: Fast & Slow Pointers
            - Key insight: `slow is fast` (identity, not value) → cycle exists; O(1) space.
        - **Merge Two Sorted Lists `⚡ T1`**
            - Description: Merge two sorted linked lists into one sorted list. Return the head of the merged list.
            - Pattern: Dummy Head + Two Pointers
            - Key insight: dummy node eliminates head-change edge case; attach smaller each step.
        - **Merge K Sorted Lists `⚡ T1`**
            - Description: Merge k sorted linked lists into one sorted linked list and return it.
            - Pattern: Min-Heap K-Way Merge
            - Key insight: `(val, list_idx, node)` tuple — `list_idx` breaks tie when ListNode is not directly comparable.
        - **Reorder List `⚡ T1`**
            - Description: Given a linked list L0→L1→…→Ln, reorder it to L0→Ln→L1→Ln-1→… in-place.
            - Pattern: Find Middle + Reverse + Weave
            - Key insight: 3 steps: fast/slow mid → reverse second half → weave alternating.
        - **Remove Nth From End `🎯 T2`**
            - Description: Given a linked list, remove the n-th node from the end and return the head.
            - Pattern: Two-Pointer Offset
            - Key insight: advance fast N steps first; both advance until `fast.next is None`.
        - **Linked List Cycle II `🎯 T2`**
            - Description: Given a linked list with a cycle, find the node where the cycle begins. Return null if no cycle.
            - Pattern: Floyd's Phase 2
            - Key insight: reset slow to head after meeting; both advance 1 step; meet again = cycle entry.
        - **Palindrome Linked List `🎯 T2`**
            - Description: Determine if a linked list is a palindrome. Must be O(N) time and O(1) space.
            - Pattern: Find Middle + Reverse Half
            - Key insight: find mid (fast/slow); reverse second half; compare; O(1) space.
        - **LRU Cache `🎯 T2`**
            - Description: Design a data structure supporting O(1) get(key) and put(key, value), evicting the Least Recently Used entry when capacity is exceeded.
            - Pattern: DLL + HashMap
            - Key insight: dummy head/tail sentinels; `_remove` + `_insert_after_head` helpers; O(1) all ops.
        - **Copy List with Random Pointer `🎯 T2`**
            - Description: Deep copy a linked list where each node has a 'next' and a 'random' pointer to any node or null.
            - Pattern: Old→Clone Map
            - Key insight: pass 1 — create clones; pass 2 — wire `.next` and `.random` via map.
        - **Reverse K-Group `🎯 T2`**
            - Description: Given a linked list, reverse the nodes of the list k at a time. If fewer than k nodes remain at the end, leave them as-is.
            - Pattern: Group Reversal + Recursion
            - Key insight: count K nodes; if < K return head; reverse K; `head.next = solve(rest, k)`.
        - **Sort List `🎯 T2`**
            - Description: Sort a linked list in O(N log N) time and O(1) space (merge sort).
            - Pattern: Merge Sort on LL
            - Key insight: find mid; split; sort halves; merge; O(N log N) time, O(log N) stack space.
        - **Intersection of Two Lists `🎯 T2`**
            - Description: Given heads of two linked lists, find the node where they intersect. Return null if no intersection.
            - Pattern: Dual-Pointer Length Equalizer
            - Key insight: each pointer walks `lenA + lenB` total; meet at intersection or both hit null.

---

- [ ] Tree
    - Alternatives
        - vs HashMap: BST O(log N) lookup but supports range queries + sorted order; HashMap O(1) avg exact lookup, no ordering.
        - vs Heap: BST O(log N) all ops + ordered iteration; Heap O(1) min/max but no search or sorted iteration.
        - vs Trie: BST for ordered comparable keys; Trie O(L) prefix-based string lookup.
        - vs Array: BST O(log N) insert while maintaining order; Sorted Array O(log N) search but O(N) insert.
    - Unbalanced BST degrades to O(N). Production uses AVL (strict balance) or Red-Black trees (looser, fewer rotations — Java `TreeMap`, Linux scheduler).
    - Key Techniques
        - **Postorder / Bottom-Up DFS:** Process children before parent — parent state depends on children (Tree DP, diameter, height).
        - **Inorder (L → Node → R):** Only traversal that gives sorted output for BST.
        - **BFS with queue:** Level-by-level processing — level order, zigzag, connect level pointers.
        - **Preorder with bounds:** Validate/range-check — pass `(min, max)` range down each recursion level.
        - **Tree DP returning tuple:** Multiple values per node — `(rob_this, skip_this)` — parent picks the better option.
        - **Morris Threading:** O(1) space traversal — temporarily thread predecessor.right → current; restore on visit.
    - Gotchas
        - BST validation — checking only immediate children misses global violations. Always pass `(lo, hi)` bounds through recursion.
        - Height vs depth — height = max edges to leaf below; depth = edges from root. Off-by-one in recursion is common.
        - Tree DP — if the problem needs the answer "through" a node (e.g., max path sum using both arms), you cannot return that to the parent. Return single-arm gain upward; update global via closure.
        - Preorder for serialization — inorder alone is insufficient; preorder + `None` markers uniquely reconstructs any binary tree.
        - Morris traversal mutates tree — explicitly tell the interviewer you restore all pointers after the traversal.
    - Questions — Tree `⚡ T1 / 🎯 T2`
        - **Binary Tree Level Order Traversal `⚡ T1`**
            - Description: Given a binary tree, return its node values level by level from left to right (as a list of lists).
            - Pattern: BFS
            - Key insight: snapshot `level_size = len(queue)` at start of each level; process exactly that many.
            - Gotcha: don't use `None` sentinel — use level-size snapshot instead.
        - **Validate BST `⚡ T1`**
            - Description: Given a binary tree, determine if it is a valid Binary Search Tree (left < root < right, including all descendants).
            - Pattern: DFS + Range Bounds
            - Key insight: pass `(lo, hi)` — checking only immediate children misses global violations.
        - **LCA of Binary Tree `⚡ T1`**
            - Description: Given a binary tree and two nodes p and q, find their Lowest Common Ancestor — the deepest node that has both as descendants.
            - Pattern: Postorder DFS
            - Key insight: both left and right return non-null → `node` is LCA; propagate found node upward.
        - **Binary Tree Max Path Sum `⚡ T1`**
            - Description: Find the path in a binary tree with the maximum sum. A path can start and end at any node.
            - Pattern: Tree DP
            - Key insight: `max(0, child)` prunes negative arms; global answer = `node.val + left + right`; return single arm up.
        - **Serialize / Deserialize Binary Tree `⚡ T1`**
            - Description: Design an algorithm to serialize a binary tree to a string and deserialize that string back to the original tree.
            - Pattern: Preorder + Null Markers
            - Key insight: preorder root-first + `None` markers uniquely reconstruct; inorder alone is insufficient.
        - **Diameter of Binary Tree `⚡ T1`**
            - Description: Find the length of the longest path between any two nodes in a binary tree (measured in edges).
            - Pattern: Tree DP
            - Key insight: `global_max = max(global_max, left_h + right_h)`; return `1 + max(left_h, right_h)` upward.
        - **Construct Tree from Pre+Inorder `⚡ T1`**
            - Description: Given preorder and inorder traversal arrays of a binary tree, reconstruct and return the binary tree.
            - Pattern: Recursion + HashMap
            - Key insight: `root = preorder[0]`; hash inorder for O(1) split; O(N) total.
        - **Maximum Depth of Binary Tree `🎯 T2`**
            - Description: Find the maximum depth (number of nodes along the longest root-to-leaf path) of a binary tree.
            - Pattern: Postorder DFS
            - Key insight: `1 + max(depth(left), depth(right))`; BFS alternative: count levels.
        - **Invert Binary Tree `🎯 T2`**
            - Description: Invert (mirror) a binary tree: swap left and right children at every node.
            - Pattern: Preorder DFS
            - Key insight: `node.left, node.right = node.right, node.left`; recurse both sides.
        - **Symmetric Tree `🎯 T2`**
            - Description: Determine if a binary tree is symmetric — a mirror image of itself around its center.
            - Pattern: Dual-Pointer Recursion
            - Key insight: recurse `(left.left, right.right)` AND `(left.right, right.left)` simultaneously.
        - **LCA of BST `🎯 T2`**
            - Description: Given a BST and two nodes p and q, find their Lowest Common Ancestor using BST properties.
            - Pattern: BST Property
            - Key insight: both < root → go left; both > root → go right; else root is LCA.
        - **Kth Smallest in BST `🎯 T2`**
            - Description: Find the k-th smallest element in a BST. Follow-up: handle frequent inserts/deletes efficiently.
            - Pattern: Iterative Inorder
            - Key insight: stop at k-th pop from stack; avoids full O(N) traversal.
        - **House Robber III `🎯 T2`**
            - Description: Houses are nodes in a binary tree. Adjacent parent-child nodes cannot both be robbed. Maximize money robbed.
            - Pattern: Tree DP (Tuple Return)
            - Key insight: `dfs(node)` → `(rob_this, skip_this)`; parent: `rob = skip_l + skip_r + val`, `skip = max(l) + max(r)`.
        - **Binary Tree Cameras `🎯 T2`**
            - Description: Place cameras on tree nodes to monitor all nodes. Each camera monitors its parent, itself, and children. Return minimum cameras needed.
            - Pattern: Tree DP (3 States)
            - Key insight: states — uncovered / covered-no-camera / has-camera; propagate bottom-up.
        - **Recover BST `🎯 T2`**
            - Description: Two nodes of a BST are swapped by mistake. Recover the tree without changing its structure.
            - Pattern: Inorder + Swap Detection
            - Key insight: inorder of valid BST is sorted; find first/second inversion pair; swap their values.
        - **Vertical Order Traversal `🎯 T2`**
            - Description: Return vertical order traversal of a binary tree: nodes in each column, sorted by row then value.
            - Pattern: BFS + Multi-key Sort
            - Key insight: track `(col, row, val)`; group by col; sort ties by `(row, val)`.
        - **Flatten Binary Tree to LL `🎯 T2`**
            - Description: Flatten a binary tree into a linked list in-place, following preorder traversal order.
            - Pattern: Morris-Like In-Place
            - Key insight: walk to left subtree's rightmost; thread its `.right` to current `.right`; move left subtree right.
        - **All Nodes Distance K `🎯 T2`**
            - Description: Given a binary tree, a target node, and integer k, return all node values that are exactly k edges away from the target.
            - Pattern: BFS with Parent Map
            - Key insight: build child→parent map in one BFS; second BFS from target node with visited set.
        - **Path Sum III `🎯 T2`**
            - Description: Count paths in a binary tree (going downward only) that sum to a given target. Path need not start or end at root/leaf.
            - Pattern: Prefix Sum + DFS Backtrack
            - Key insight: `count[curr_prefix - target]`; decrement on backtrack to isolate each path.

---

- [ ] Trie
    - Alternatives
        - vs HashMap: Trie O(L) prefix queries; shares prefix memory; HashMap O(L) per-word exact lookup with no prefix structure.
        - vs BST: Trie O(L) vs O(L × log N) for string keys in BST; slower for prefix but BST supports numeric range queries.
        - vs Suffix Array: Trie for prefix queries only; Suffix Array for substring queries; more complex build.
    - Key Techniques
        - **Trie Insert + DFS:** Autocomplete — walk to prefix node, DFS all `is_end` descendants.
        - **Trie + Grid DFS:** Word Search II — prune DFS branches when no prefix match; delete dead nodes after finding words.
        - **XOR Trie (Binary):** Maximum XOR of two numbers — process bits MSB→LSB; greedily choose opposite bit.
        - **Compressed Trie (Radix Tree):** Merge single-child chains; O(N) nodes for N words; used in IP routing.
    - Gotchas
        - `is_end` vs prefix reachability — `search("app")` must return `False` if only "apple" was inserted. Never conflate prefix walk success with word completion.
        - Word Search II deduplication — set `node.is_end = False` immediately after recording to prevent duplicate results.
        - XOR Trie bit width — use 31 bits for non-negative; 32 bits if negatives possible.
        - Pruning dead nodes — in Word Search II, `del node.children[ch]` after finding all words through it. Without this, TLE from re-exploring dead branches.
        - Fixed array vs dict children — `[None] * 26` is faster for pure lowercase ASCII; `{}` is necessary for arbitrary alphabets.
    - Questions — Trie `⚡ T1 / 🎯 T2`
        - **Implement Trie `⚡ T1`**
            - Description: Design a Trie with insert(word), search(word), and startsWith(prefix) methods, all running in O(L) where L is word length.
            - Pattern: Core Trie
            - Key insight: `TrieNode` with `children` dict + `is_end`; `_walk` helper for shared prefix traversal.
        - **Word Search II `⚡ T1`**
            - Description: Given a 2D board and a list of words, find all words that exist in the board (adjacent non-revisiting cells).
            - Pattern: Trie + Grid DFS Backtrack
            - Key insight: build trie from words; DFS from each cell; prune dead nodes on backtrack (`del node.children[ch]`).
        - **Maximum XOR of Two Numbers `⚡ T1`**
            - Description: Find the maximum XOR of any two numbers from the array. Use a binary Trie for O(N) time.
            - Pattern: XOR Trie (Binary, Greedy)
            - Key insight: binary trie bits MSB→LSB; greedily flip bit to maximize XOR.
        - **Replace Words `⚡ T1`**
            - Description: Given a dictionary of roots and a sentence, replace each word with its shortest root from the dictionary.
            - Pattern: Trie Prefix Lookup
            - Key insight: return shortest matching root prefix; walk until `is_end`.
        - **Design Search Autocomplete `⚡ T1`**
            - Description: Design an autocomplete system that returns the top 3 most frequently typed sentences matching a given prefix.
            - Pattern: Trie + Top-K Cache
            - Key insight: store top-3 words at each node to avoid DFS on every keystroke.
        - **Longest Word in Dictionary `🎯 T2`**
            - Description: Find the longest word that can be built one character at a time using words from the dictionary.
            - Pattern: Trie BFS on `is_end`
            - Key insight: only traverse via `is_end` nodes — word must be buildable one char at a time.
        - **Map Sum Pairs `🎯 T2`**
            - Description: Implement insert(key, val) and sum(prefix) where sum returns total val for all keys with the given prefix.
            - Pattern: Trie with Subtree Sums
            - Key insight: each node stores subtree value sum; subtract old value on key update.

---

- [ ] Heap / Priority Queue
    - Alternatives
        - vs Sorted Array: Heap O(log N) insert; O(1) peek. Sorted Array O(1) peek; O(N) insert.
        - vs BST/TreeMap: Heap O(log N) push/pop; only min/max access. BST O(log N) all ops + ordered iteration + arbitrary search.
        - vs Bucket Sort: Heap works on unknown/dynamic priorities. Bucket Sort O(N) but requires bounded key range.
        - vs Monotonic Deque: Heap O(log N) per element. Deque O(N) total for sliding window — prefer deque for windows.
    - Python: `heapq` is **min-heap only** — negate values to simulate max-heap; use `(-priority, counter, item)` for stability.
    - Key Techniques
        - **K Largest:** Min-heap of size K; pop when size > K; root = K-th largest.
        - **K Smallest:** Max-heap of size K (negate in Python); root = K-th smallest.
        - **K-Way Merge:** `(value, list_idx, element_idx)` tuples — list_idx breaks tie for non-comparable objects.
        - **Dynamic Median:** Max-heap lower half + Min-heap upper half; rebalance so `|len(lo) - len(hi)| <= 1`.
        - **Sliding Window Median:** Two heaps + lazy deletion counter — avoid O(N) re-heapification.
        - **Dijkstra:** Min-heap of `(dist, node)`; skip already-settled nodes.
    - Gotchas
        - Python max-heap: negate values before push, negate again after pop. For objects use `(-priority, counter, item)`.
        - Heap is not stable — equal-priority elements don't preserve insertion order; add a `counter` as tie-breaker.
        - Tuple tie-breaking: `(val, node)` works only if `node` is comparable. Use `(val, idx, node)` to avoid `TypeError`.
        - Build-heap is O(N) — `heapq.heapify()` calls sift-down from middle, not O(N log N). Mention this explicitly.
        - Lazy deletion: for sliding window median, don't remove from middle of heap; track invalid elements in a counter and discard when they surface at the top.
    - Questions — Heap `⚡ T1 / 🎯 T2`
        - **Kth Largest Element `⚡ T1`**
            - Description: Find the k-th largest element in an unsorted array. Note: it is the k-th largest in sorted order (not k-th distinct).
            - Pattern: Min-Heap of Size K
            - Key insight: root = K-th largest; QuickSelect is O(N) avg alternative — mention both.
        - **K Closest Points to Origin `⚡ T1`**
            - Description: Given a list of points, find the k closest to the origin (0,0) using Euclidean distance.
            - Pattern: Max-Heap of Size K
            - Key insight: use `x²+y²` — avoid `sqrt` for float precision.
        - **Top K Frequent Elements `⚡ T1`**
            - Description: Given an integer array, return the k most frequent elements. Answer may be in any order.
            - Pattern: Counter + Heap or Bucket Sort
            - Key insight: bucket sort O(N) — prefer when K ≈ N or K not given.
        - **Kth Largest in Stream `⚡ T1`**
            - Description: Design a class to find the k-th largest element in a stream. Initialize with an array; add numbers dynamically.
            - Pattern: Min-Heap of Size K
            - Key insight: `heappush` then `heappop` if size > K; root = K-th largest.
        - **Find Median from Stream `⚡ T1`**
            - Description: Design a class that supports addNum(int) and findMedian(), where findMedian() returns the median of all numbers seen so far.
            - Pattern: Two Heaps
            - Key insight: push to lo (max-heap); move lo's max to hi; rebalance if `len(lo) < len(hi)`.
        - **Merge K Sorted Lists `⚡ T1`**
            - Description: Merge k sorted linked lists into one sorted linked list and return it.
            - Pattern: K-Way Merge
            - Key insight: `(val, list_idx, node)`; advance same list's next on each pop.
        - **Task Scheduler `⚡ T1`**
            - Description: Given tasks (letters) and cooldown n (same task needs n intervals gap), find minimum total time to finish all tasks.
            - Pattern: Math / Max-Heap
            - Key insight: `(max_f - 1) * (n + 1) + count_max_f`; cap at `len(tasks)`.
        - **Reorganize String `⚡ T1`**
            - Description: Rearrange string s so no two adjacent characters are the same. Return any valid arrangement, or '' if impossible.
            - Pattern: Max-Heap by Freq
            - Key insight: place most frequent not equal to previous; impossible if `max_freq > (n+1)//2`.
        - **IPO (Maximize Capital) `⚡ T1`**
            - Description: Given k projects each with a profit and minimum capital requirement, find max capital starting with w capital after completing at most k projects.
            - Pattern: Sort + Max-Heap
            - Key insight: sort by capital; max-heap of unlocked profits; pointer into sorted list.
        - **Sliding Window Median `⚡ T1`**
            - Description: Given an array and window size k, return the median of each window of size k as a float array.
            - Pattern: Two Heaps + Lazy Delete
            - Key insight: lazy deletion — track invalid elements in counter; discard when they surface.
        - **Find K Pairs with Smallest Sums `⚡ T1`**
            - Description: Given two sorted arrays, find the k pairs (u,v) with the smallest sums where u comes from arr1 and v from arr2.
            - Pattern: K-Way Merge
            - Key insight: seed with `(nums1[i]+nums2[0], i, 0)`; push `(i, j+1)` on pop.
        - **Furthest Building `⚡ T1`**
            - Description: Given building heights, bricks, and ladders, find the furthest building you can reach by optimally using bricks/ladders.
            - Pattern: Min-Heap + Greedy
            - Key insight: assign ladders to largest jumps; swap smallest ladder for bricks when needed.
        - **Kth Smallest in Sorted Matrix `⚡ T1`**
            - Description: Given an n×n matrix where each row and column is sorted in ascending order, find the k-th smallest element.
            - Pattern: K-Way Merge
            - Key insight: treat each row as a sorted list; same K-way merge pattern.
        - **Ugly Number II `⚡ T1`**
            - Description: Find the n-th ugly number. Ugly numbers are positive integers whose only prime factors are 2, 3, or 5.
            - Pattern: Min-Heap or 3-Pointer DP
            - Key insight: push `n*2, n*3, n*5` on pop; deduplicate with visited set.
        - **Meeting Rooms II `🎯 T2`**
            - Description: Given meeting time intervals, find the minimum number of conference rooms required.
            - Pattern: Min-Heap of End Times
            - Key insight: sort by start; pop if `end <= new_start`; heap size = min rooms.
        - **Meeting Rooms I `🎯 T2`**
            - Description: Given meeting time intervals [start, end], determine if a person can attend all meetings (no two overlap).
            - Pattern: Sort + Single Check
            - Key insight: sort by start; if any `intervals[i].start < intervals[i-1].end` → overlap exists → return False.
        - **Single-Threaded CPU `🎯 T2`**
            - Description: Given tasks with enqueue time and processing time, simulate a single-threaded CPU picking the shortest available task. Return processing order.
            - Pattern: Min-Heap by Duration
            - Key insight: sort by enqueue time; push available tasks; advance time if CPU idle.
        - **Last Stone Weight `🎯 T2`**
            - Description: Repeatedly smash the two heaviest stones. If weights differ, put the difference back. Return the weight of the last stone, or 0.
            - Pattern: Max-Heap (negate)
            - Key insight: pop two; push difference if nonzero; final heap[-1] or 0.

---

- [ ] Graphs
    - Alternatives
        - vs Adj. Matrix: Adj. list O(V+E) space, sparse-efficient. Matrix O(V²) space; O(1) edge check; only for dense graphs (N ≤ 1000).
        - vs Tree: Graph can have cycles and multiple parents; Tree is acyclic + one parent — simpler invariants.
        - vs Union-Find: Graph supports full traversal and path finding; Union-Find O(α) connectivity checks only, no path structure.
    - Default: adjacency list `defaultdict(list)`. Adjacency matrix only if N ≤ 1000 and O(1) edge checks are critical.
    - Algorithm Selection Table

        | Goal | Algorithm | Complexity |
        |------|-----------|-----------|
        | Unweighted shortest path | BFS | O(V+E) |
        | Non-negative weighted shortest path | Dijkstra + min-heap | O((V+E) log V) |
        | Negative weights / negative cycle detect | Bellman-Ford | O(VE) |
        | All-pairs shortest path | Floyd-Warshall | O(V³) |
        | 0/1 weight edges | 0-1 BFS (deque) | O(V+E) |
        | Topological order / cycle in directed graph | Kahn's (BFS in-degree) | O(V+E) |
        | Connected components (undirected) | DFS / Union-Find | O(V+E) |
        | Minimum spanning tree | Kruskal (sparse) / Prim (dense) | O(E log E) |

    - Gotchas
        - Mark visited before enqueue, not after dequeue — marking after dequeue allows duplicates, wrong distances, and TLE.
        - Disconnected graph — always iterate over ALL nodes to start BFS/DFS from each unvisited one; don't assume one connected component.
        - Topological sort edge direction — "A requires B as prerequisite" → edge `B → A` (B before A). Getting this backwards is the #1 topo sort bug.
        - Recursive DFS stack overflow — Python default recursion limit is ~1000; for grids > 31×31, use iterative DFS with explicit stack.
        - Undirected graph: add edge in both directions in adjacency list.
    - Questions — BFS / DFS `⚡ T1 / 🎯 T2`
        - **Number of Islands `⚡ T1`**
            - Description: Given a 2D grid of '1' (land) and '0' (water), count the number of islands (connected components of land, 4-directional).
            - Pattern: DFS/BFS Flood Fill
            - Key insight: for each unvisited `'1'`, run DFS/BFS marking all connected `'1'`s as `'0'`. Count DFS calls. No separate visited set — mark in-place.
        - **Max Area of Island `⚡ T1`**
            - Description: Given a 2D binary grid, find the maximum area of an island (connected group of 1s, 4-directional).
            - Pattern: DFS + Size Counter
            - Key insight: DFS returns `1 + sum(dfs(neighbor))`; track global max.
        - **Flood Fill `⚡ T1`**
            - Description: Given an image (2D array), a starting pixel, and a new color, perform a flood fill starting from that pixel.
            - Pattern: DFS/BFS
            - Key insight: skip if `newColor == oldColor` — avoids infinite loop.
        - **Rotting Oranges `⚡ T1`**
            - Description: In a grid of fresh/rotten oranges, every minute rotten oranges spread to adjacent fresh ones. Return min minutes to rot all, or -1.
            - Pattern: Multi-Source BFS
            - Key insight: all rotten at t=0; track fresh count; -1 if fresh remain after BFS.
        - **Clone Graph `⚡ T1`**
            - Description: Given a reference to a node in an undirected connected graph, return a deep copy (clone) of the entire graph.
            - Pattern: DFS/BFS + old→clone Map
            - Key insight: create clone before recursing into neighbors to handle cycles.
        - **Course Schedule `⚡ T1`**
            - Description: Given numCourses and a list of [course, prerequisite] pairs, determine if it's possible to finish all courses (i.e., no cycle).
            - Pattern: Kahn's Topo Sort
            - Key insight: cycle iff `len(order) < n`; edge direction: `prereq → course`.
        - **Course Schedule II `⚡ T1`**
            - Description: Same as Course Schedule, but return one valid ordering of courses to take. Return [] if impossible.
            - Pattern: Kahn's Topo Sort
            - Key insight: return `order` list; return empty if cycle detected.
        - **Alien Dictionary `⚡ T1`**
            - Description: Given a sorted list of alien-language words, derive the character ordering of the alien alphabet. Return '' if invalid.
            - Pattern: Topo Sort from Word Pairs
            - Key insight: extract edges from first mismatch in adjacent words; detect invalid prefix (`"abc"` before `"ab"`).
        - **Word Ladder `⚡ T1`**
            - Description: Given beginWord, endWord, and a word list, find the length of the shortest transformation sequence where each step changes one letter and every intermediate word is in the list.
            - Pattern: BFS on Words
            - Key insight: remove words from set on visit; bidirectional BFS for follow-up.
        - **Pacific Atlantic Water Flow `⚡ T1`**
            - Description: In an m×n height grid, water flows to 4-adjacent cells of equal or lesser height. Find all cells that can flow to both the Pacific (top/left) and Atlantic (bottom/right) ocean.
            - Pattern: Reverse BFS from Borders
            - Key insight: BFS from Pacific border + BFS from Atlantic border; intersect reachable sets.
        - **Surrounded Regions `⚡ T1`**
            - Description: In a board of 'X' and 'O', flip all 'O's not connected to any border 'O' to 'X'.
            - Pattern: Reverse DFS from Border
            - Key insight: mark border-connected O's safe; flip remaining interior O→X.
        - **Is Graph Bipartite? `⚡ T1`**
            - Description: Given an undirected graph, determine if it can be 2-colored (bipartite) — i.e., no edge connects two same-colored nodes.
            - Pattern: BFS/DFS 2-Coloring
            - Key insight: conflict on same color → not bipartite; run from all unvisited nodes.
        - **Find Eventual Safe States `⚡ T1`**
            - Description: In a directed graph, a node is 'safe' if every path from it leads to a terminal node (no outgoing edges). Return all safe nodes.
            - Pattern: Reverse + Topo Sort
            - Key insight: nodes in topo order = safe; or 3-color DFS (white/gray/black).
        - **Redundant Connection `⚡ T1`**
            - Description: Given an undirected tree with one extra edge added (creating a cycle), find and return that redundant edge.
            - Pattern: Union-Find
            - Key insight: first edge where `find(u) == find(v)` creates a cycle.
        - **All Paths from Source to Target `⚡ T1`**
            - Description: Given a DAG, find all paths from node 0 to node n-1. Return them in any order.
            - Pattern: DFS + Backtrack
            - Key insight: DAG → no visited set needed; append path on reaching n-1.
        - **Minimum Vertices to Reach All Nodes `⚡ T1`**
            - Description: Find the minimum set of vertices from which all nodes in a directed acyclic graph are reachable.
            - Pattern: In-Degree Count
            - Key insight: nodes with in-degree 0 are the required starting vertices.
        - **Minimum Spanning Tree (Kruskal's) `⚡ T1`**
            - Description: Given a weighted undirected graph, find the minimum spanning tree (subset of edges connecting all nodes with minimum total weight).
            - Pattern: Union-Find + Sort Edges
            - Key insight: sort edges by weight; add if `find(u) != find(v)`; stop at N-1 edges.
        - **Network Delay Time `🎯 T2`**
            - Description: Given a directed weighted graph, a source k, and n nodes, find how long it takes for a signal to reach all nodes. Return -1 if unreachable.
            - Pattern: Dijkstra
            - Key insight: max of all shortest distances from source; -1 if any unreachable.
        - **Swim in Rising Water `🎯 T2`**
            - Description: In an n×n grid where grid[i][j] is the elevation, find the minimum time t such that you can travel from top-left to bottom-right through cells with elevation ≤ t.
            - Pattern: Dijkstra / Binary Search
            - Key insight: `dist[r][c]` = min max-elevation path to `(r,c)`; or binary search on answer.
        - **Shortest Path with Obstacle Elimination `🎯 T2`**
            - Description: Given a grid with walls, find the shortest path from top-left to bottom-right where you can remove at most k walls.
            - Pattern: BFS + State Dimension
            - Key insight: state = `(row, col, remaining_k)`; visited per `(r, c, k)`.

---

## DS Decision Tree

```
Does the problem involve...

Arbitrary key lookup (string/obj keys)?
  → HashMap / HashSet

Prefix-based string queries (autocomplete)?
  → Trie

Hierarchical data or BST operations?
  → Tree (BST / AVL / RB)

Repeatedly extract current min or max?
  → Heap / Priority Queue

Arbitrary relationships / shortest path / cycle detection?
  → Graph (BFS / DFS / Kahn's / Dijkstra)

Sequential data with O(1) random access?
  → Array

Frequent mid-sequence insert/delete at known pointer?
  → Linked List

LIFO order / expression / DFS simulation?
  → Stack

FIFO order / BFS / level-order?
  → Queue
```

---

## ⚡ Quick Pattern Triggers — Last-Minute Review

> Read this the morning of your interview. Each line is one 30-second recognition drill.

| If you see... | Reach for... | Critical edge case |
| :--- | :--- | :--- |
| "Two numbers sum to target" | HashMap complement in one pass | Index 0 sentinel matters for prefix sum variant |
| "Maximum subarray" or "best profit" | Kadane's — reset when negative | Max product: also track `min_prod` for negatives |
| "All words/things starting with prefix" | Trie — O(L) independent of dict size | `is_end ≠ prefix reachable`; prune dead nodes in Word Search II |
| "Shortest path" (unweighted) | BFS — first reach = shortest | Mark visited **before enqueue** not after dequeue |
| "Shortest path" (weighted, no negatives) | Dijkstra + min-heap | Skip stale: `if d > dist[u]: continue` |
| "Dependency ordering" / "detect cycle in directed" | Kahn's Topo Sort | Edge direction: prereq→course; cycle iff `len(order) < n` |
| "All cells spread simultaneously" | Multi-source BFS — seed all at t=0 | Never run BFS per source — O(S×(V+E)) vs O(V+E) |
| "Max/Min in sliding window of size K" | Monotonic Deque — store indices | Store indices not values; pop front when `dq[0] <= i-k` |
| "Always extract current min/max from dynamic set" | Heap (min-heap; negate for max) | `heapq` Python = min-heap only; add `counter` for stability |
| "K-th largest / smallest" | Min-heap size K | QuickSelect is O(N) avg — mention as alternative |
| "Merge K sorted lists/arrays" | K-way merge heap: `(val, idx, elem)` | `idx` breaks ties when elements aren't directly comparable |
| "Find median from stream" | Two heaps: max-heap lower + min-heap upper | Rebalance so `len(lo) - len(hi) <= 1`; median = `lo[0]` or avg |
| "Cycle in linked list" | Floyd's fast/slow | `slow is fast` (identity); Phase 2: reset slow to head |
| "Reverse linked list" | Three-pointer: `prev, curr, nxt` | Save `nxt = curr.next` FIRST or you lose the tail |
| "Max path through a tree" | Tree DP — postorder | Cannot return cross-arm value to parent; use closure for global max |
| "Tree level order / level count" | BFS — snapshot `len(queue)` | Don't use `None` sentinel — use level-size snapshot |
| "Count connected components / flood fill" | DFS/BFS over all unvisited | Disconnected graph: outer loop over all nodes |
| "Sort / order tasks with prerequisites" | Topological sort (Kahn's) | — |
| "0/1 pick items, hit target weight" | 0/1 Knapsack — iterate W **backward** | Forward = unbounded; backward = each item used at most once |
| "Count/enumerate all subsets/permutations" | Backtracking — always `undo` after recurse | Copy path at goal: `results.append(path[:])` not `path` |
| "Minimum cost / steps — monotone feasibility" | Binary search on answer | Write `feasible(mid)` predicate; find min `mid` where feasible |
| "XOR of pairs" | XOR Trie — process MSB→LSB | Bit width: 31 for non-negative; 32 if negatives possible |
| "Exact match lookup, no ordering needed" | HashMap/HashSet O(1) avg | Mutable keys (list/dict) → use tuple; worst case O(N) |

---

## L3 Must-Solve Problems (data structures)

Solve these **cold** before your loop. Full walkthroughs live in [`coding/data-structures/`](../coding/data-structures/).

| # | Problem | Topic | Pattern |
| :- | :--- | :--- | :--- |
| 1 | Two Sum | Hashing | Complement map |
| 2 | Subarray Sum Equals K | Array / Hashing | Prefix sum + count map |
| 3 | 3Sum | Array | Sort + two pointers |
| 4 | Trapping Rain Water | Array | Two pointers or monotonic stack |
| 5 | Minimum Window Substring | String | Variable sliding window |
| 6 | Number of Islands | Graph | DFS/BFS flood fill |
| 7 | Rotting Oranges | Graph / Queue | Multi-source BFS |
| 8 | Course Schedule | Graph | Kahn's topo sort |
| 9 | Word Ladder | Graph / Queue | BFS on implicit graph |
| 10 | Pacific Atlantic Water Flow | Graph | Reverse BFS from borders |
| 11 | Clone Graph | Graph | DFS + old→clone map |
| 12 | Redundant Connection | Graph | Union-Find |
| 13 | Kth Largest Element | Heap | Min-heap size K |
| 14 | Merge K Sorted Lists | Heap / LL | K-way merge |
| 15 | Find Median from Data Stream | Heap | Two heaps |
| 16 | Implement Trie | Trie | children + is_end |
| 17 | Word Search II | Trie | Trie + grid DFS + prune |
| 18 | Binary Tree Level Order | Tree | BFS level snapshot |
| 19 | LCA of Binary Tree | Tree | Postorder DFS |
| 20 | Validate BST | Tree | DFS with (lo, hi) bounds |
| 21 | Binary Tree Max Path Sum | Tree | Tree DP + global max |
| 22 | Reverse Linked List | Linked List | Three-pointer reversal |
| 23 | Linked List Cycle | Linked List | Floyd fast/slow |
| 24 | LRU Cache | Linked List | DLL + HashMap |
| 25 | Valid Parentheses | Stack | Push opens, match closes |
| 26 | Daily Temperatures | Stack | Monotonic decreasing stack |
| 27 | Sliding Window Maximum | Queue | Monotonic deque |
| 28 | Insert Interval | Array / Intervals | Three-phase scan: copy left non-overlapping, merge overlapping, copy right |

> **Mock cadence:** Weeks 3–4, do **2 timed mocks per week** (35 min, one problem, talk out loud). Log misses in [`questions.md`](../questions.md).

---

*Generated from source files in this repository. See individual `.md` files for full implementations, click moments, and flashcards.*
