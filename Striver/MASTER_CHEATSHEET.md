---
module: striver
topic: Master cheat sheet — every part's cheat sheet on one page
tags: [striver, cheatsheet, revision]
---
# Master Cheat Sheet

← [Striver course map](README.md) · [Pattern triggers](PATTERN_TRIGGERS.md)

> [!abstract] What this is
> Every part's cheat sheet in course order, for last-day revision. Each one is copied from its part README, so edit the part README and regenerate. If any line here feels unfamiliar, go back to that part's theory note.

[Part 1](#part-1-fundamentals-of-programming) · [Part 2](#part-2-language-basics) · [Part 3](#part-3-logic-building-patterns) · [Part 4](#part-4-patterns) · [Part 5](#part-5-time-complexity) · [Part 6](#part-6-standard-libraries--collections) · [Part 7](#part-7-concept-basics) · [Part 8](#part-8-basic-maths) · [Part 9](#part-9-basic-arrays) · [Part 10](#part-10-basic-hashing) · [Part 11](#part-11-basic-strings) · [Part 12](#part-12-basic-recursion) · [Part 13](#part-13-sorting) · [Part 14](#part-14-arrays) · [Part 15](#part-15-hashing) · [Part 16](#part-16-binary-search) · [Part 17](#part-17-strings-basic-and-medium) · [Part 18](#part-18-recursion) · [Part 19](#part-19-linked-list) · [Part 20](#part-20-bit-manipulation) · [Part 21](#part-21-greedy-algorithms) · [Part 22](#part-22-sliding-window--2-pointer) · [Part 23](#part-23-stack--queues) · [Part 24](#part-24-binary-trees) · [Part 25](#part-25-binary-search-trees) · [Part 26](#part-26-heaps) · [Part 27](#part-27-graphs) · [Part 28](#part-28-dynamic-programming) · [Part 29](#part-29-tries) · [Part 30](#part-30-strings-advanced) · [Part 31](#part-31-maths) · [Part 32](#part-32-beyond-the-sheet)

---

## Part 1: Fundamentals of Programming

[Part README](01-fundamentals-of-programming/README.md)

| Concept | Remember |
|---|---|
| Problem contract | Input · Output · Rules · Constraints · Edge cases |
| Computational thinking | Decomposition · Pattern recognition · Abstraction · Algorithmic thinking |
| Control structures | Sequence · Selection (diamond) · Iteration (loop with update) |
| Loop recipe | Initialize → check → body → update. N body runs means N+1 checks |
| Accumulator identity | Sum starts at `0`, product at `1`, max starts at the *first element* (not 0) |
| Boundary trio | Test `k-1`, `k`, `k+1` around every threshold `k` |
| Digit peeling | `d = n % 10`, `n = n / 10` until `n == 0` |
| Error families | Syntax (grammar) · Runtime (crash) · Logical (wrong answer, no crash) |
| Debug loop | Reproduce → expected by hand → shrink → trace → **first divergence** → explain → smallest fix → retest |
| Invariant | A fact true before or after every loop iteration; it proves the final answer |
| Language | One language, its essentials plus standard containers, then DSA |

---

## Part 2: Language Basics

[Part README](02-language-basics/README.md)

| Concept | C++ | Java | Python |
|---|---|---|---|
| Run | `g++ -std=c++17 -O2 a.cpp && ./a.out < in` | `java Main.java < in` | `python3 a.py < in` |
| 64-bit int | `long long` | `long` | `int` (unbounded) |
| Max sentinel | `INT_MAX`, `LLONG_MAX` | `Integer.MAX_VALUE` | `float('inf')` |
| Safe product | `1LL * a * b` | `(long) a * b` | `a * b` |
| `-7 / 2` | `-3` (truncate) | `-3` | `-7 // 2 = -4` (floor); `/` gives `-3.5` |
| `-7 % 3` | `-1` | `-1` (`Math.floorMod` → 2) | `2` |
| Fast input | `ios::sync_with_stdio(false); cin.tie(nullptr);` | `BufferedReader` + `StringTokenizer` | `sys.stdin.readline` / `sys.stdin.buffer.read().split()` |
| Fast output | `'\n'` not `endl` | `PrintWriter` + `flush()` / `StringBuilder` | `"\n".join(out)` once |
| Dynamic array | `vector<int> a(n)` | `ArrayList<Integer>` / `int[]` | `list` `[0] * n` |
| 2D array | `vector<vector<int>> g(r, vector<int>(c))` | `new int[r][c]` | `[[0]*c for _ in range(r)]` |
| Size | `a.size()` (unsigned!) | `arr.length`, `s.length()`, `list.size()` | `len(a)` |
| String mutable? | ✅ `s[i] = 'x'` | ❌ use `StringBuilder` / `char[]` | ❌ use `list` + `"".join` |
| Pass array to function | Copy by default → use `vector<int>&` | Reference value (mutations visible) | Reference (mutations visible) |
| Hash map | `unordered_map<int,int>` | `HashMap<Integer,Integer>` | `dict` / `defaultdict` |
| Equality trap | — | `==` on objects compares references | `is` vs `==` |
| Recursion depth | ~10⁵–10⁶ (stack size) | ~10⁴–10⁵ → `StackOverflowError` | 1000 → `setrecursionlimit` |
| Ops/sec (rough) | ~10⁸ | ~10⁸ (after JIT warm-up) | ~10⁷ |

#### Picking an integer type from constraints

| Largest value the answer can reach | Type |
|---|---|
| ≤ 2 × 10⁹ | `int` |
| ≤ 9 × 10¹⁸ (sums of 10⁵ values ≤ 10⁹, products of two ≤ 10⁹) | `long long` / `long` |
| Larger | Modular arithmetic (`% 1_000_000_007`), or Python int |

---

## Part 3: Logic Building (Patterns)

[Part README](03-logic-building-patterns/README.md)

| Shape / trick | Formula (1-based row i) |
|---|---|
| Right triangle | cells `i` |
| Inverted | replace i with `n − i + 1` |
| Centred pyramid | spaces `n − i`, stars `2i − 1`, width `2n − 1` |
| Inverted pyramid | spaces `i − 1`, stars `2(n − i) + 1` |
| Rise then fall over 2n − 1 rows | `n − |n − i|` |
| Number crown gap | `2(n − i)` |
| Alternating bits | `(i + j) % 2 == 0 ? 1 : 0` |
| Letters | `(char)('A' + k)` |
| Counter across rows | declare outside both loops |
| Hollow | print iff on a boundary row/column |
| Concentric square | `n − min(i, j, S−1−i, S−1−j)`, S = 2n − 1 |
| Complexity | O(total characters printed) time, O(1) space |

---

## Part 4: Patterns

[Part README](04-patterns/README.md)

| Family | Patterns | Formula (1-based i, j) |
|---|---|---|
| Fixed square | 1 | inner bound n |
| Growing triangle | 2, 3, 4, 14, 16 | bound `i`; content `j`, `i`, `'A'+j−1`, `'A'+i−1` |
| Inverted triangle | 5, 6, 15 | bound `n − i + 1` |
| Parity | 11 | `(i + j) % 2 == 0 ? 1 : 0` |
| Running counter | 13 | `num++`, declared outside both loops; row i starts at `1 + i(i−1)/2` |
| Moving start | 18 | letters `'A'+n−i … 'A'+n−1` |
| Pyramid / inverted | 7, 8 | spaces `n − i` / `i − 1`; stars `2i − 1` / `2(n − i) + 1` |
| Composition | 9 | pattern 7 then pattern 8 |
| Rise then fall | 10, 20 | `s = n − |n − i|` over 2n − 1 rows |
| Mirrored row | 12, 17 | crown gap `2(n − i)`; hill breakpoint `(2i − 1)/2` |
| Three segments | 12, 19, 20 | `s + gap + s = 2n` → derive the gap from s |
| Boundary | 21 | `i==0 ∥ j==0 ∥ i==n−1 ∥ j==n−1` (0-based) |
| Ring distance | 22 | `n − min(i, j, S−1−i, S−1−j)`, S = 2n − 1 |
| Complexity | all | O(n²) time, O(1) extra space |

---

## Part 5: Time Complexity

[Part README](05-time-complexity/README.md)

| Pattern | Complexity |
|---|---|
| Single loop, step +c | O(n) |
| Loop ×2 or ÷2 | O(log n) |
| `i * i ≤ n` | O(√n) |
| Nested independent | O(n·m) |
| Triangular `j ≥ i` | O(n²) |
| Harmonic `j += i` | O(n log n) |
| Two pointers / sliding window | O(n) |
| T(n) = T(n/2) + 1 | O(log n) |
| T(n) = 2T(n/2) + n | O(n log n) |
| T(n) = 2T(n−1) + 1 | O(2ⁿ) |
| n ≤ 20 / 10³ / 10⁵ / 10¹⁸ | 2ⁿ / n² / n log n / log n |

---

## Part 6: Standard Libraries & Collections

[Part README](06-standard-libraries-and-collections/README.md)

| Concept | C++ | Java | Python | Key ops cost |
|---|---|---|---|---|
| Dynamic array | `vector` | `ArrayList` | `list` | index O(1), push-back amortised O(1) |
| Deque | `deque` | `ArrayDeque` | `deque` | both ends O(1) |
| Stack | `stack` | `ArrayDeque` (push/pop) | `list` | O(1) |
| Queue | `queue` | `ArrayDeque` (offer/poll) | `deque` | O(1) |
| Min-heap | `priority_queue<T, vector<T>, greater<T>>` | `PriorityQueue` | `heapq` | push/pop O(log n), top O(1) |
| Max-heap | `priority_queue<T>` | `PriorityQueue(Collections.reverseOrder())` | `heapq` with `-x` | same |
| Hash set / map | `unordered_set/map` | `HashSet/HashMap` | `set/dict` | O(1) avg, O(n) worst |
| Ordered set / map | `set/map` | `TreeSet/TreeMap` | — (`sortedcontainers`) | O(log n) |
| Lower bound | `lower_bound` | `TreeMap.ceilingKey` | `bisect_left` | O(log n) |
| Sort | `sort` (introsort, unstable) | `Arrays.sort` / `Collections.sort` | `sort` (Timsort, stable) | O(n log n) |
| Frequency | `m[x]++` | `m.merge(x, 1, Integer::sum)` | `Counter` | O(1) avg |

---

## Part 7: Concept Basics

[Part README](07-concept-basics/README.md)

| Need | Tool | Cost |
|---|---|---|
| Last digit / drop digit | `n % 10`, `n / 10` | O(1) each; all digits O(log n) |
| Reverse a number | `rev = rev*10 + d` (watch overflow) | O(log n) |
| All divisors | pairs `(i, n/i)` for `i*i ≤ n` | O(√n) |
| Is prime | trial division to √n | O(√n) |
| All primes ≤ N | sieve | O(N log log N) |
| GCD / LCM | Euclid; `a / g * b` | O(log min) |
| Array access / middle insert | address formula / shift | O(1) / O(n) |
| Count small keys | `cnt[x]++`, `cnt[c-'a']++` | O(1) |
| Count large keys | `unordered_map` / `HashMap` / `dict` | O(1) avg |
| Build a string | `+=` (C++), `StringBuilder`, `''.join` | O(total) |

---

## Part 8: Basic Maths

[Part README](08-basic-maths/README.md)

| Template | Core lines | Cost | Used by |
|---|---|---|---|
| Digit loop | `while n > 0: d = n % 10; n //= 10` | O(log₁₀ n) | 1–5, 7 |
| Reverse | `rev = rev * 10 + d` | O(log₁₀ n) | 3, 4 |
| √n pairing | `for i in 1..√n: if n % i == 0: i, n // i` | O(√n) | 8, 9, 13 |
| Sieve | mark multiples of `p` from `p*p` | O(n log log n) | 10 |
| Euclid | `while b: a, b = b, a % b` | O(log min(a,b)) | 11, 12 |
| LCM | `a // gcd(a, b) * b` (divide first) | O(log min) | 12 |

**Overflow cheat:** reversing a 32-bit int can overflow → use 64-bit or check `rev > (INT_MAX - d) / 10`. `20!` is the last factorial that fits in `long long`. Compute LCM as `a / g * b`, never `a * b / g`.

**n = 0 trap:** a `while n > 0` loop runs zero times, so "count digits of 0" returns 0 unless you special-case it (answer is 1).

---

## Part 9: Basic Arrays

[Part README](09-basic-arrays/README.md)

| Problem | Accumulator / pointers | Early exit? | Cost |
|---|---|---|---|
| Sum | `s += x` (64-bit if values are large) | no | O(n) / O(1) |
| Count odd | `c += x & 1` | no | O(n) / O(1) |
| Is sorted | compare `a[i-1] > a[i]` | yes, first violation | O(n) / O(1) |
| Reverse | `l = 0, r = n-1`, swap, move inward | stop at `l ≥ r` | O(n) / O(1) |

**Adjacent-pair loops** start at `i = 1` and look at `a[i-1]`. That handles `n = 0` and `n = 1` with no special case.

---

## Part 10: Basic Hashing

[Part README](10-basic-hashing/README.md)

| Choice | When | Cost |
|---|---|---|
| Array `cnt[x]` | values in a small known range (e.g. `0..10⁴`) | O(n + range), fastest |
| Hashmap | arbitrary or large values | O(n) expected |
| Sorted map (`map` / `TreeMap`) | need keys in order | O(n log n) |

**Tie-break pattern:** `if f > best_f or (f == best_f and x < best_x)`. Write it as one condition so it can't drift between branches.

**Top-2 pattern:** `if f > first: second = first; first = f` · `elif second < f < first: second = f`.

---

## Part 11: Basic Strings

[Part README](11-basic-strings/README.md)

| Problem | Primitive | Time / Space |
|---|---|---|
| Reverse string (in place) | two pointers, swap | O(n) / O(1) |
| Palindrome check | two pointers, compare | O(n) / O(1) |
| Largest odd number | scan from the right for an odd digit, strip leading zeros | O(n) / O(1) extra |
| Longest common prefix | vertical scan column by column | O(total chars) / O(1) |
| Isomorphic strings | last-seen index per char, both strings | O(n) / O(Σ) |
| Rotate string | `len equal and goal in s + s` | O(n) with KMP |
| Valid anagram | `cnt[c] += 1` for s, `-= 1` for t, all zero | O(n) / O(26) |
| Sort by frequency | count + bucket by frequency | O(n) / O(n) |

**Language traps:** strings are immutable in Python and Java, so build with a list / `StringBuilder`, not `+=` in a loop (O(n²)). Java compares strings with `.equals`, never `==`. Use `c - 'a'` to index a lowercase char.

---

## Part 12: Basic Recursion

[Part README](12-basic-recursion/README.md)

| Problem | Base case | Recursive step | Time / Stack |
|---|---|---|---|
| Sum 1..N | `n == 0 → 0` | `n + f(n−1)` | O(n) / O(n) |
| Factorial | `n ≤ 1 → 1` | `n · f(n−1)` | O(n) / O(n) |
| Array sum | `i == n → 0` | `a[i] + f(i+1)` | O(n) / O(n) |
| Reverse string / array | `l ≥ r` | swap, `f(l+1, r−1)` | O(n) / O(n) |
| Palindrome | `l ≥ r → true` | `s[l]==s[r] and f(l+1, r−1)` | O(n) / O(n) |
| Prime | `i·i > n → true` | `n % i ≠ 0 and f(i+1)` | O(√n) / O(√n) |
| Sorted | `i ≥ n−1 → true` | `a[i] ≤ a[i+1] and f(i+1)` | O(n) / O(n) |
| Digit sum | `n == 0 → 0` | `n%10 + f(n/10)` | O(log₁₀ n) / same |
| Fibonacci | `n ≤ 1 → n` | `f(n−1) + f(n−2)` | O(φⁿ) naive → O(n) memo |

**Habits:** pass indices, never slices. Pass C++ containers by `&`. Expect a Python `RecursionError` beyond depth ~1000. Every linear recursion here has an O(1)-space loop twin; say so in interviews.

---

## Part 13: Sorting

[Part README](13-sorting/README.md)

| Sort | Best | Average | Worst | Extra space | Stable | In place | Core move |
|---|---|---|---|---|---|---|---|
| Selection | O(n²) | O(n²) | O(n²) | O(1) | ✗ | ✓ | put the min of `[i..n)` at `i` |
| Bubble | O(n) with flag | O(n²) | O(n²) | O(1) | ✓ | ✓ | swap adjacent inversions; max bubbles to the end |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | ✓ | ✓ | shift larger elements right, drop `key` in |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) + O(log n) stack | ✓ | ✗ | split in half, merge two sorted halves |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) stack avg | ✗ | ✓ | partition around a pivot, recurse on both sides |
| Counting | O(n + k) | O(n + k) | O(n + k) | O(k) | ✓ | ✗ | tally values 0..k |

**Facts interviewers test:** comparison sorts need Ω(n log n) comparisons (a decision tree with n! leaves has height log₂ n!). Insertion sort's running time is O(n + inversions). Selection sort makes at most n − 1 swaps. Quick sort's worst case comes from a bad pivot on sorted input; a random pivot gives expected O(n log n). Library sorts: C++ `std::sort` is introsort (not stable, `stable_sort` is merge-based); Java `Arrays.sort` is dual-pivot quicksort for primitives and TimSort for objects; Python `sorted` is TimSort (stable).

---

## Part 14: Arrays

[Part README](14-arrays/README.md)

| Pattern | Trigger | Time | Space | Problems here |
|---|---|---|---|---|
| Write pointer | "in place", "remove", "move to end" | O(n) | O(1) | remove duplicates, move zeroes |
| Reversal trick | rotate by k, reorder suffix | O(n) | O(1) | rotate array, next permutation |
| Two pointers on sorted | pairs/triplets with target sum | O(n²) for 3-sum | O(1) extra | 2-sum, 3-sum, 4-sum, merge sorted |
| Prefix sum + hash map | subarray sum/XOR = k, negatives allowed | O(n) | O(n) | longest subarray sum k, count subarrays |
| Kadane | max contiguous sum | O(n) | O(1) | max subarray, max product (with min) |
| Dutch national flag | 3 distinct values | O(n) one pass | O(1) | sort colors |
| Boyer–Moore voting | > n/2 or > n/3 frequency | O(n) | O(1) | majority I, majority II |
| Merge-sort counting | count pairs i < j with a[i] vs a[j] | O(n log n) | O(n) | inversions, reverse pairs |
| Matrix index math | rotate, spiral, set zeroes | O(mn) | O(1) | rotate matrix, spiral, set zeroes |
| Math / XOR | one missing or repeating value in 1..n | O(n) | O(1) | missing number, repeating and missing |

**Facts interviewers test:** prefix sum + map must store `{0: -1}` (or count 1) before the loop, and for "longest" store only the *first* index of each prefix. Sliding window only works for "sum ≤ k" when all values are non-negative. Kadane resets when the running sum drops below zero; for an all-negative array it returns the largest element, not 0. Rotate by `k` uses `k %= n` first. Boyer–Moore always needs a verification pass unless a majority is guaranteed. 3-sum dedupes by skipping equal neighbours after sorting, never with a set of tuples in the optimal answer. Inversions and reverse pairs overflow `int` (up to n²/2), and `2 * a[j]` overflows too — use `long long` / `long`.

---

## Part 15: Hashing

[Part README](15-hashing/README.md)

| Problem | Prefix | Map stores | Seed | Per step | Time / Space |
|---|---|---|---|---|---|
| Longest subarray sum k | running sum `p` | first index of each `p` | `{0: −1}` | `i − first[p − k]`; insert `p` only if new | O(n) / O(n) |
| Largest subarray sum 0 | running sum | first index | `{0: −1}` | `i − first[p]` | O(n) / O(n) |
| Count subarrays sum k | running sum | count of each `p` | `{0: 1}` | `ans += cnt[p − k]`, then `cnt[p]++` | O(n) / O(n) |
| Count subarrays XOR k | running XOR `x` | count of each `x` | `{0: 1}` | `ans += cnt[x ^ k]`, then `cnt[x]++` | O(n) / O(n) |
| Longest consecutive sequence | — | set of values | — | start only where `x − 1 ∉ set` | O(n) / O(n) |

**Facts interviewers test:** `sum(l..r) = P[r] − P[l − 1]`, so "subarray sum = k ending at r" means "some earlier prefix equals `P[r] − k`". XOR works the same because `a ^ b = k ⇔ a = b ^ k`. Seed the map *before* the loop or you miss subarrays starting at index 0. For "longest", never overwrite an existing prefix (you want the earliest). For "count", look up *before* incrementing the current prefix, or `k = 0` counts the empty subarray. The sliding window fails with negatives because extending the window no longer monotonically increases the sum. `unordered_map` / `HashMap` are O(1) average but O(n) worst case under adversarial collisions — mention it, and that sorting or a balanced tree (`map`, `TreeMap`) gives a guaranteed O(log n).

---

## Part 16: Binary Search

[Part README](16-binary-search/README.md)

| Shape | Range | Predicate | On true | Return |
|---|---|---|---|---|
| lower_bound (first ≥ x) | `[0, n)` | `a[mid] ≥ x` | `ans = mid, hi = mid − 1` | `ans` (init `n`) |
| upper_bound (first > x) | `[0, n)` | `a[mid] > x` | `ans = mid, hi = mid − 1` | `ans` (init `n`) |
| Rotated search | `[0, n)` | which half is sorted, is x in it | shrink to that half | index / −1 |
| Min in rotated | `[0, n)` | left half sorted → `ans = min(ans, a[lo])`, go right | — | `ans` |
| Min of max (ship, split, books, koko) | `[max, Σ]` / `[1, max]` | `need(mid) ≤ limit` | `ans = mid, hi = mid − 1` | `ans` |
| Max of min (cows) | `[1, max − min]` | `place(mid) ≥ k` | `ans = mid, lo = mid + 1` | `ans` |
| Real answer (gas stations) | `[0, maxgap]` | `need(mid) ≤ k` | `hi = mid` | `hi` after 100 iters |
| Two arrays median / kth | `c1 ∈ [0, n₁]` | `l1 ≤ r2 && l2 ≤ r1` | done | from `l*`, `r*` |
| Matrix median | `[min, max]` | `count(≤ mid) > nm/2` | `hi = mid − 1` | `lo` |

**Facts interviewers test:** `mid = lo + (hi − lo) / 2` avoids overflow (Java: `(lo + hi) >>> 1`). With `while lo ≤ hi`, both updates must be `mid ± 1`; with `while lo < hi` and `hi = mid`, the loop ends on `lo == hi` — mixing the two causes infinite loops. Sortedness isn't required, only a predicate that is `F…F T…T` (or which half holds an answer). For BS on answer, state the range bounds aloud (why `max(arr)` and not 0) and the check's cost: total O(check · log range). Rotated with duplicates degrades to O(n) worst case (`[1,1,1,0,1]`). For real-valued answers, loop a fixed number of times rather than `while hi − lo > ε`.

---

## Part 17: Strings (Basic and Medium)

[Part README](17-strings-basic-medium/README.md)

| Problem | Technique | Time / Space |
|---|---|---|
| Remove outermost parentheses | depth counter; keep char unless it moves depth 0↔1 | O(n) / O(n) output |
| Max nesting depth | running depth, track max | O(n) / O(1) |
| Roman to integer | add, but subtract when value < next value | O(n) / O(1) |
| String to integer (atoi) | skip spaces → sign → digits, clamp before overflow | O(n) / O(1) |
| Substrings with exactly k distinct | atMost(k) − atMost(k − 1), window + count map | O(n) / O(Σ) |
| Longest palindromic substring | expand around 2n − 1 centres | O(n²) / O(1) |
| Sum of beauty of all substrings | fix start, extend end, int[26] counts | O(26 · n²) / O(26) |

**Facts interviewers test:** one bracket type never needs a stack — an integer depth is the stack's height. In atoi, check overflow *before* multiplying: `res > (MAX − d) / 10` → clamp. "Exactly k" isn't monotone for a sliding window but "at most k" is, so subtract two at-most counts. There are `2n − 1` palindrome centres (n letters, n − 1 gaps). Counting all substrings is O(n²) because there are n(n + 1)/2 of them — say this when your answer is O(n²).

---

## Part 18: Recursion

[Part README](18-recursion/README.md)

| Problem | Shape | Time |
|---|---|---|
| Pow(x, n) | halve exponent | O(log n) |
| Count good numbers | fast power mod | O(log n) |
| Generate parentheses | open < n / close < open | O(4ⁿ/√n) |
| Power set / Subsets I | pick/not-pick | O(n · 2ⁿ) |
| Subsets II | sort + for-loop skip | O(n · 2ⁿ) |
| Sum-K exists / count | pick/not-pick, bool / int return | O(2ⁿ) |
| Combination Sum I / II / III | for-loop, reuse i / i+1 + skip / k digits | exponential |
| Letter combinations | one digit per level | O(4ⁿ · n) |
| Palindrome partitioning | for-loop over cut end + isPal table | O(n · 2ⁿ) |
| Word search / Rat in maze | grid DFS, mark & restore | O(mn · 3^L) |
| N-Queens | row recursion, col/diag sets | O(n!) |
| M-colouring | vertex recursion | O(mⁿ) |
| Sudoku | empty-cell recursion, 3 tables | O(9^E) |
| Expression add operators | operand loop + value/last | O(n · 4ⁿ) |

**Facts interviewers test:** a recursion tree's time is (#nodes) × (work per node) — 2ⁿ leaves for subsets, n! for permutations. Return `bool` to stop early; return `int` and add to count. Duplicate skip is `i > start` (same level), never `i > 0`. Reuse an element by recursing on `i`, not `i + 1`. Backtracking state must be restored exactly — every mark has an unmark.

---

## Part 19: Linked List

[Part README](19-linked-list/README.md)

| Problem | Primitive | Time / Space |
|---|---|---|
| Insert / delete head, tail, K, value | walk to predecessor | O(n) / O(1) |
| DLL delete node / insert before node | fix 2 / 4 links | O(1) / O(1) |
| Reverse SLL / DLL | 3-pointer / swap prev-next | O(n) / O(1) |
| Add two numbers | dummy + carry | O(max) / O(1) |
| Odd-even list, sort 0/1/2 | separate chains, stitch | O(n) / O(1) |
| Remove Nth from end | gap of N | O(n) / O(1) |
| Add one | rightmost non-9 / recursion | O(n) / O(1) |
| Middle / delete middle | fast/slow (head start for delete) | O(n) / O(1) |
| Palindrome | middle + reverse half + restore | O(n) / O(1) |
| Y intersection | pointer switching | O(m+n) / O(1) |
| Detect / start / length of loop | Floyd | O(n) / O(1) |
| Reverse in k-groups | detach, reverse, reconnect | O(n) / O(1) |
| Rotate | k mod n, ring, cut | O(n) / O(1) |
| Merge two sorted | dummy + splice | O(n+m) / O(1) |
| Flatten | merge along child | O(N·k) / O(k) |
| Sort list | merge sort, first middle | O(n log n) / O(log n) |
| Clone with random | interleave copies | O(n) / O(1) extra |
| DLL: delete key, dedupe, pair sum | unlink / skip run / two ends | O(n) / O(1) |

**Facts interviewers test:** use a dummy head whenever the head can change. `while fast and fast.next` gives the second middle; start `fast = head.next` for the first. Floyd's loop start comes from L = kC − d. Pointer switching terminates because both walk m + n. Save `next` before relinking. Restore input lists you temporarily modify (palindrome, clone).

---

## Part 20: Bit Manipulation

[Part README](20-bit-manipulation/README.md)

| Goal | Expression | Note |
|---|---|---|
| Test bit k | `(n >> k) & 1` | or `(n & (1 << k)) != 0` |
| Set / clear / toggle bit k | `n \| 1<<k` · `n & ~(1<<k)` · `n ^ 1<<k` | |
| Odd? | `n & 1` | correct for negatives |
| Clear lowest set bit | `n & (n − 1)` | Kernighan, power of 2 |
| Isolate lowest set bit | `n & −n` | unsigned in C++ for INT_MIN |
| Set lowest unset bit | `n \| (n + 1)` | |
| Power of 2 | `n > 0 && !(n & (n − 1))` | guard `n > 0` |
| Low k bits mask | `(1 << k) − 1` | `n mod 2ᵏ` = `n & mask` |
| XOR 0…n | `[n, 1, n+1, 0][n % 4]` | |
| Swap | `a ^= b; b ^= a; a ^= b` | breaks if aliased |
| Submasks of m | `s = (s − 1) & m` | O(3ⁿ) over all m |

**Facts interviewers test:** `&`, `|`, `^` bind **looser** than `==` in C/C++/Java — always parenthesise. `>>` is arithmetic on signed ints (fills with the sign bit); Java has `>>>` for logical shift. `1 << 31` overflows a signed int; use `1L`/`1LL`/`1u`. `−INT_MIN` and `abs(INT_MIN)` overflow. Python ints are unbounded — emulate 32-bit with `& 0xFFFFFFFF` and convert back by subtracting 2³² when ≥ 2³¹.

---

## Part 21: Greedy Algorithms

[Part README](21-greedy-algorithms/README.md)

| Problem shape | Greedy rule | Proof |
|---|---|---|
| Match demands to supplies | sort both; smallest supply that fits | exchange |
| Max non-overlapping intervals | sort by end; take if start ≥ / > last end | stays ahead |
| Min intervals to remove | n − max non-overlapping | complement |
| Merge intervals | sort by start; extend `last.end = max(...)` | contiguity |
| Min rooms / platforms | max concurrent = sweep events | lower bound met |
| Fractional knapsack | sort by v/w desc | exchange of units |
| Min total waiting (SJF) | sort by duration asc | adjacent swap |
| Deadlines, unit jobs | profit desc, latest free slot | exchange |
| Jump reachability | farthest reach prefix | invariant |
| Min jumps | BFS layers as windows | BFS |
| Neighbour inequalities | left pass + right pass, take max | both lower bounds |
| Wildcard balance | track `[lo, hi]` of balances | interval of states |

**Greedy fails on:** 0/1 knapsack, coin change with arbitrary denominations ({1, 3, 4}, target 6), longest path, weighted interval scheduling. When you can't produce a proof in two sentences, look for a counterexample on 3 elements before committing.

---

## Part 22: Sliding Window / 2 Pointer

[Part README](22-sliding-window-and-2-pointer/README.md)

| Question shape | Validity / state | Template | Answer update |
|---|---|---|---|
| Fixed size k (sum, avg, max points) | running sum | add `a[r]`, drop `a[r−k]` | at each full window |
| Longest with no repeats | last-seen index | `l = max(l, last[c] + 1)` | `max(r − l + 1)` |
| Longest with ≤ k bad elements | count of bad | shrink while `bad > k` | `max(r − l + 1)` |
| Longest with ≤ K distinct | count map + distinct | shrink while `distinct > K` | `max(r − l + 1)` |
| Longest fixable by k edits | `len − maxFreq ≤ k` | stale `maxFreq` is fine | `max(r − l + 1)` |
| Shortest covering t | deficit counter `need` | shrink while `need == 0` | `min` before removing `s[l]` |
| Shortest containing subsequence | order matters | forward match, backward shrink | `min`, leftmost on ties |
| Count ≤ K | as above | shrink while invalid | `+= r − l + 1` |
| Count exactly K | — | `atMost(K) − atMost(K − 1)` | subtraction |
| Count at least (all of a set) | last-seen positions | `+= 1 + min(last)` | per right end |

**Window works only when validity is monotone** in the left pointer: if `[l, r]` is valid then `[l+1, r]` is valid (for "≤" constraints). Negative numbers break sums; use prefix sums + hashmap. **Non-shrinking trick:** replace `while` with `if` for "longest" problems; return the final window size.

---

## Part 23: Stack / Queues

[Part README](23-stack-and-queues/README.md)

| Problem shape | Stack order (bottom → top) | Pop when | Answer read |
|---|---|---|---|
| Next greater (right) | decreasing | `top ≤ x` | top after popping, else −1 |
| Next smaller (right) | increasing | `top ≥ x` | top after popping |
| Previous greater / stock span | decreasing | `top ≤ x` | `i − top index` |
| Circular NGE | decreasing, iterate `2n` | `top ≤ a[i % n]` | fill only for `i < n` |
| Sum of subarray mins | increasing | PSE strict, NSE `≤` | `a[i]·left·right` |
| Histogram | increasing (+ sentinel 0) | `h[top] ≥ cur` | `h[t]·(i − newTop − 1)` |
| Remove K digits | increasing | `top > d` and `k > 0` | strip leading 0s, drop tail if k left |
| Asteroid collision | survivors | `top > 0 > x` and `|top| < |x|` | remaining stack |
| Sliding window max | deque decreasing | back `≤ x`; front `≤ i − k` | front |

**Amortised O(n):** every index is pushed once and popped at most once, so all the inner `while` loops together do ≤ n pops. **Indices, not values,** whenever you need distances or expiry. **Ties:** pick strict on one side and non-strict on the other so each subarray is counted exactly once.

---

## Part 24: Binary Trees

[Part README](24-binary-trees/README.md)

| Problem | Template | Key state | Complexity |
|---|---|---|---|
| Inorder / pre / post (iterative) | stack | left spine (in), push right then left (pre), 2 stacks or last-visited (post) | O(n) / O(h) |
| Level order, zigzag, right view | BFS by `len(q)` | level size, direction flag | O(n) / O(w) |
| Height, balanced, diameter | post-order | return height; update global answer | O(n) / O(h) |
| Max path sum | post-order | return `val + max(0, l, r)`; answer `val + max(0,l) + max(0,r)` | O(n) |
| Vertical / top / bottom view | BFS with column (and row) | `col → nodes` map; first/last seen | O(n log n) |
| LCA | post-order | return node if p/q found; both sides non-null → root | O(n) |
| Max width | BFS with indices | index `2i+1`, `2i+2`, normalised per level | O(n) |
| Distance K, burn tree | parent map + BFS | visited set, radius | O(n) |
| Count complete nodes | compare left/right heights | perfect → `2^h − 1` | O(log² n) |
| Build from pre/post + in | divide & conquer | inorder index map | O(n) |
| Serialise | BFS/DFS with `#` | null markers | O(n) |
| Morris | predecessor threads | `pred.right == cur`? | O(n) / O(1) |

**Height convention:** decide up front whether an empty tree has height 0 or −1, and keep to it. **Global answer vs return value:** the post-order pattern returns what the *parent* needs (a single path) and updates a separate answer (which may bend through the node).

---

## Part 25: Binary Search Trees

[Part README](25-binary-search-trees/README.md)

| Problem | Template | Key rule | Complexity |
|---|---|---|---|
| Search / insert | walk | `val < cur ? left : right`; insert at the null slot | O(h) / O(1) |
| Min / max | spine walk | leftmost / rightmost | O(h) |
| Floor / ceil | walk + candidate | floor: record when `cur < key`, go right; ceil mirrors | O(h) |
| Pred / succ | walk + candidate | succ: record when `cur > key`, go left; equal goes right | O(h) |
| Delete | walk + case split | 2 children → successor copy, or splice right under left's rightmost | O(h) |
| Kth smallest / largest | iterative inorder (reverse for largest) | stop at the kth pop | O(h + k) |
| Validate | bounds `(lo, hi)` | left `(lo, v)`, right `(v, hi)`; use long / ±∞ | O(n) |
| LCA | walk | first node between p and q | O(h) |
| Build from preorder | recursion with upper bound | left bound = val, right bound = parent's | O(n) |
| Iterator | stack of left spine | `next`: pop, push left spine of right | O(1) amortised / O(h) |
| Two sum | two iterators | move the side that fixes the sum; stop when they meet | O(n) / O(h) |
| Recover swapped | inorder with prev | descent: `first ← prev` once, `last ← cur` | O(n) |
| Largest BST subtree | post-order | `(min, max, size)`; invalid → `(−∞, +∞, best)` | O(n) |

**h is log n only if balanced.** Sorted inserts produce a linked list. In production, use `std::map`/`std::set` or `TreeMap`/`TreeSet`; Python has no built-in balanced BST, so use `bisect` on a list or `sortedcontainers`.

---

## Part 26: Heaps

[Part README](26-heaps/README.md)

| Operation / problem | Technique | Key rule | Complexity |
|---|---|---|---|
| Parent / children of `i` | 0-indexed array | `(i−1)/2`, `2i+1`, `2i+2` | O(1) |
| push / pop | sift up / sift down | pop: last → root, sift down to the **smaller** child | O(log n) |
| Build heap | bottom-up from `n/2−1` | subtrees already heaps | O(n) |
| Heap sort | max-heap, swap root to end | sift within shrinking size | O(n log n), O(1), unstable |
| k-th largest | min-heap size k | pop when size > k | O(n log k) |
| k-th largest (one-shot) | quickselect 3-way | target index `n−k` | O(n) expected |
| Sort k-sorted | min-heap size k+1 | element i is within k of its slot | O(n log k) |
| Merge k lists | heap of heads | push `next` of popped node | O(N log k) |
| Task scheduler | count formula | `max(n_tasks, (f−1)(n+1) + #maxf)` | O(n) |
| Hand of straights | ordered map from the smallest | start groups at the smallest card | O(n log n) |
| Connect sticks | min-heap | always join the two shortest | O(n log n) |
| Median stream | two heaps | rebalance after each insert | O(log n) add, O(1) query |
| Top-k frequent | bucket by count | buckets indexed 0..n | O(n) |
| Top-k pair sums | best-first + visited | from `(i,j)` push `(i+1,j)`, `(i,j+1)` | O(k log k) |

**Libraries:** C++ `priority_queue<T>` is a **max**-heap (`greater<T>` for min); Java `PriorityQueue` is a **min**-heap; Python `heapq` is a **min**-heap on a list (negate for max, push tuples for ties). None support decrease-key; push a new entry and skip stale ones on pop (lazy deletion).

---

## Part 27: Graphs

[Part README](27-graphs/README.md)

| Problem shape | Technique | Key rule | Complexity |
|---|---|---|---|
| Traverse / count components | BFS or DFS + visited | mark visited when **pushed** (BFS) | O(V + E) |
| Grid islands / flood fill | DFS/BFS on 4 neighbours | bounds check first, then cell value | O(R·C) |
| "Distance from the nearest X" | multi-source BFS | push **all** sources at distance 0 | O(R·C) |
| "Regions not touching the border" | BFS/DFS from the border | mark safe, flip the rest | O(R·C) |
| Cycle, undirected | DFS/BFS with parent | visited neighbour ≠ parent → cycle | O(V + E) |
| Cycle, directed | DFS with on-path flag / Kahn | back edge, or Kahn pops < V | O(V + E) |
| Bipartite | 2-colouring BFS/DFS | same-colour edge → not bipartite | O(V + E) |
| Topological order | Kahn (in-degree 0 queue) | DAG ⇔ all V popped | O(V + E) |
| Shortest path, unit weights | BFS | first visit = shortest | O(V + E) |
| Shortest path, DAG | topo order + relax | works with negative weights | O(V + E) |
| Shortest path, w ≥ 0 | Dijkstra + min-heap | skip stale `(d, u)` with `d > dist[u]` | O(E log V) |
| ≤ k edges / negative weights | Bellman-Ford | copy `dist` per round for "≤ k edges" | O(V·E) |
| All pairs | Floyd-Warshall | `k` loop **outermost** | O(V³) |
| Minimax path (effort, water) | Dijkstra on max / BS + BFS / DSU | path cost = max edge | O(E log V) |
| MST | Kruskal (sort + DSU) / Prim (heap) | cut property | O(E log E) |
| Dynamic connectivity | DSU, path compression + size | union returns whether it merged | ~O(α(n)) per op |
| SCC | Kosaraju (finish order, reverse, DFS) | 2 passes | O(V + E) |
| Bridges / articulation points | Tarjan `tin`, `low` | bridge: `low[v] > tin[u]`; AP: `low[v] ≥ tin[u]` (root: ≥ 2 children) | O(V + E) |

---

## Part 28: Dynamic Programming

[Part README](28-dynamic-programming/README.md)

| Family | State | Transition | Answer | Time / space |
|---|---|---|---|---|
| Fibonacci-like | `dp[i]` | `dp[i−1] + dp[i−2]` | `dp[n]` | O(n) / O(1) |
| Pick / not pick | `dp[i]` | `max(a[i] + dp[i−2], dp[i−1])` | `dp[n−1]` | O(n) / O(1) |
| Circular array | two linear runs | drop first or last | max of both | O(n) |
| Previous choice matters | `dp[i][last]` | over choices ≠ last | max of last row | O(n·k²) |
| Grid paths | `dp[i][j]` | up + left (min / sum) | `dp[m−1][n−1]` | O(mn) / O(n) |
| Variable start / end | whole first row init | three predecessors | best of last row | O(n²) |
| Two agents in lockstep | `(row, c1, c2)` | 9 moves | `dp[0][0][C−1]` | O(R·C²) |
| Subset sum / partition | `dp[i][t]` bool | `dp[i−1][t] or dp[i−1][t−a_i]` | `dp[n−1][T]` | O(nT) / O(T) |
| Count subsets | `dp[i][t]` count | `skip + take`; zeros need care | `dp[n−1][T]` | O(nT) |
| 0/1 knapsack | `dp[i][w]` | `max(skip, v_i + dp[i−1][w−w_i])` | `dp[n−1][W]` | O(nW) / O(W) |
| Unbounded (coins, rod) | `dp[i][w]` | take stays at `i` | `dp[n−1][W]` | O(nW) / O(W) |
| Stocks | `(i, buy?, cap)` | buy / sell / skip | `f(0, 1, k)` | O(n·k) / O(k) |
| LIS | `dp[i]` = LIS ending at i | `1 + max dp[j]`, `a[j] < a[i]` | `max dp` | O(n²); tails O(n log n) |
| LCS / two strings | `dp[i][j]` | match → diag + 1, else max(up, left) | `dp[n][m]` | O(nm) / O(m) |
| Edit distance | `dp[i][j]` | match → diag; else 1 + min(ins, del, rep) | `dp[n][m]` | O(nm) |
| Partition (MCM) | `dp[i][j]` | min over split k of `dp[i][k] + dp[k+1][j] + cost` | `dp[1][n−1]` | O(n³) / O(n²) |

---

## Part 29: Tries

[Part README](29-tries/README.md)

| Problem | Trie | Key move | Time |
|---|---|---|---|
| Insert / search / startsWith | 26-ary + `end` | shared `walk()` helper | O(L) |
| Count equal / prefix, erase | `pass`, `end` counters | ++ on insert, −− on erase | O(L) |
| Complete string | 26-ary + `end` | every node on path has `end` | O(Σ L) |
| Distinct substrings | suffix trie | count nodes created (+1 empty) | O(n²) |
| Max XOR pair | binary, 31 levels | take opposite bit if present | O(31 n) |
| Max XOR with `a ≤ m` | binary + offline | sort queries by `m`, sweep inserts | O((n+q) log + 31(n+q)) |

---

## Part 30: Strings (Advanced)

[Part README](30-strings-advanced/README.md)

| Problem | Tool | Key move | Time |
|---|---|---|---|
| Reverse words | scan from the right | skip spaces, slice word, join | O(n) |
| Bracket reversals | two counters | ⌈open/2⌉ + ⌈close/2⌉, −1 if odd | O(n) |
| Count and say | run-length encode | count then digit per run | O(Σ len) |
| Rabin-Karp | rolling hash | `((h − out·B^(m−1))·B + in) mod M`, verify | O(n + m) exp. |
| Z search | Z-box `[l, r)` | `z[i] = min(r − i, z[i − l])`, extend | O(n + m) |
| LPS / KMP | prefix function | `len = lps[len − 1]` on mismatch | O(n) |
| Shortest palindrome | lps of `s#rev(s)` | prepend `rev(s)[:n − k]` | O(n) |
| Longest happy prefix | prefix function | `s[:lps[n − 1]]` | O(n) |

---

## Part 31: Maths

[Part README](31-maths/README.md)

| Problem | Tool | Key move | Time |
|---|---|---|---|
| Is x prime? | trial division | d·d ≤ x | O(√x) |
| All primes ≤ n | sieve | outer i·i ≤ n, inner from i² | O(n log log n) |
| Factorise many x | SPF sieve | x /= spf[x] | O(X log log X + log x) per query |
| Primes in [L, R], many queries | sieve + prefix | pre[R] − pre[L−1] | O(1) per query |
| Primes in huge [L, R] | segmented sieve | start at max(p², ⌈L/p⌉·p) | O((R−L) log log R + √R) |

---

## Part 32: Beyond the Sheet

[Part README](32-beyond-the-sheet/README.md)

| Trigger | Tool |
|---|---|
| Static range sum | Prefix sum |
| Static range min/max | Sparse table |
| Point update + range sum | Fenwick |
| Range update + range query | Lazy segment tree |
| n ≤ 20 with "which used" | Bitmask DP |
| Count in [L, R] up to 10¹⁸ by digits | Digit DP |
| Answer for every root | Rerooting |
| Many LCA / k-th ancestor queries | Binary lifting |
| Subtree queries | Euler tour + BIT |
| Use every edge once | Hierholzer |
| 0/1 edge weights | 0-1 BFS |
| n ≈ 40 subset search | Meet in the middle |
| Interval overlaps | Sweep line |
| Uniform sample from a stream | Reservoir |

---
