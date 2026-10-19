---
module: striver
topic: Problem index — every note across all parts
tags: [striver, index]
---
# Problem Index

← [Striver course map](README.md)

> [!abstract] What this is
> Every theory lesson and problem note in one place, in course order. *Key insight* is the first sentence of the part README's row; open the note for the full walkthrough. Generated from the part READMEs, so re-generate rather than hand-edit.

**506 notes across 32 parts.** [Part 1](#part-1-fundamentals-of-programming) (7) · [Part 2](#part-2-language-basics) (3) · [Part 3](#part-3-logic-building-patterns) (2) · [Part 4](#part-4-patterns) (22) · [Part 5](#part-5-time-complexity) (1) · [Part 6](#part-6-standard-libraries--collections) (4) · [Part 7](#part-7-concept-basics) (4) · [Part 8](#part-8-basic-maths) (13) · [Part 9](#part-9-basic-arrays) (4) · [Part 10](#part-10-basic-hashing) (3) · [Part 11](#part-11-basic-strings) (8) · [Part 12](#part-12-basic-recursion) (12) · [Part 13](#part-13-sorting) (8) · [Part 14](#part-14-arrays) (34) · [Part 15](#part-15-hashing) (6) · [Part 16](#part-16-binary-search) (33) · [Part 17](#part-17-strings-basic-and-medium) (8) · [Part 18](#part-18-recursion) (23) · [Part 19](#part-19-linked-list) (45) · [Part 20](#part-20-bit-manipulation) (14) · [Part 21](#part-21-greedy-algorithms) (16) · [Part 22](#part-22-sliding-window--2-pointer) (13) · [Part 23](#part-23-stack--queues) (31) · [Part 24](#part-24-binary-trees) (32) · [Part 25](#part-25-binary-search-trees) (15) · [Part 26](#part-26-heaps) (20) · [Part 27](#part-27-graphs) (46) · [Part 28](#part-28-dynamic-programming) (54) · [Part 29](#part-29-tries) (7) · [Part 30](#part-30-strings-advanced) (9) · [Part 31](#part-31-maths) (5) · [Part 32](#part-32-beyond-the-sheet) (4)

---

## Part 1: Fundamentals of Programming

[Part README](01-fundamentals-of-programming/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Breaking the Myth](01-fundamentals-of-programming/01-breaking-the-myth.md) | — | 📘 Theory | — | DSA is language-independent: logic first, syntax second |
| 2 | [Programming & What Are Computers](01-fundamentals-of-programming/02-programming-and-what-are-computers.md) | — | 📘 Theory | — | Computer = speed + obedience; storage → RAM → CPU |
| 3 | [How to Think Like a Programmer](01-fundamentals-of-programming/03-how-to-think-like-a-programmer.md) | — | 📘 Theory | — | Read every problem as a contract; computational thinking |
| 4 | [Flowcharts & Pseudocode](01-fundamentals-of-programming/04-flowcharts-and-pseudocode.md) | — | 📘 Theory | — | Sequence, selection, iteration: three ways to write one algorithm |
| 5 | [Flowchart Problem-Solving Lab](01-fundamentals-of-programming/05-flowchart-problem-solving.md) | — | 📘 Theory | — | 8 worked problems: validation, champion, slabs, digit peeling |
| 6 | [Dry Runs, Edge Cases & Debugging](01-fundamentals-of-programming/06-dry-runs-edge-cases-and-debugging.md) | — | 📘 Theory | — | Trace tables, first divergence, invariants |
| 7 | [Programming Languages & Choosing a Path](01-fundamentals-of-programming/07-programming-languages-and-choosing-a-path.md) | — | 📘 Theory | — | Pick one language (C++/Java/Python) and learn its DSA subset |

## Part 2: Language Basics

[Part README](02-language-basics/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Learn C++](02-language-basics/01-learn-cpp.md) | — | 📘 Theory | — | g++ setup, fast I/O, `long long`, references, `vector`/`string`, template |
| 2 | [Learn Java](02-language-basics/02-learn-java.md) | — | 📘 Theory | — | JDK setup, BufferedReader I/O, `long`, `.equals` vs `==`, `StringBuilder`, template |
| 3 | [Learn Python](02-language-basics/03-learn-python.md) | — | 📘 Theory | — | `sys.stdin` I/O, `//` and `%` semantics, aliasing, recursion limit, speed, template |

## Part 3: Logic Building (Patterns)

[Part README](03-logic-building-patterns/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Easy and Medium](03-logic-building-patterns/01-easy-and-medium.md) | — | 📘 Theory | — | Row table → bounds and content as formulas in i; pyramids via `n − i` spaces and `2i − 1` stars |
| 2 | [Hard](03-logic-building-patterns/02-hard.md) | — | 📘 Theory | — | Composition, mirroring, hollow boundary tests, distance formulas |

## Part 4: Patterns

[Part README](04-patterns/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Square of Stars](04-patterns/01-pattern-1.md) | — | 📘 Theory | — | Both loops run a fixed n times — the inner bound does not depend on i. |
| 2 | [Right-Angled Triangle](04-patterns/02-pattern-2.md) | — | 📘 Theory | — | Inner bound = i: the first pattern where the inner loop depends on the outer variable. |
| 3 | [Number Triangle](04-patterns/03-pattern-3.md) | — | 📘 Theory | — | Same shape as pattern 2; the cell content is the column index j. |
| 4 | [Row-Number Triangle](04-patterns/04-pattern-4.md) | — | 📘 Theory | — | Same shape as pattern 2; the cell content is the row index i. |
| 5 | [Inverted Right Triangle](04-patterns/05-pattern-5.md) | — | 📘 Theory | — | Inversion rule: replace i with n − i + 1 in pattern 2's bound. |
| 6 | [Inverted Number Triangle](04-patterns/06-pattern-6.md) | — | 📘 Theory | — | Pattern 5's shape with pattern 3's content. |
| 7 | [Star Pyramid](04-patterns/07-pattern-7.md) | — | 📘 Theory | — | Two segments per row: leading spaces (n − i) then stars (2i − 1); width stays 2n − 1. |
| 8 | [Inverted Star Pyramid](04-patterns/08-pattern-8.md) | — | 📘 Theory | — | Pattern 7 with i → n − i + 1: spaces grow, stars shrink by 2. |
| 9 | [Diamond](04-patterns/09-pattern-9.md) | — | 📘 Theory | — | Composition: run pattern 7's loop, then pattern 8's loop (middle row printed twice). |
| 10 | [Half Diamond](04-patterns/10-pattern-10.md) | — | One loop over 2n − 1 rows; stars = i ≤ n ? i : 2n − i (= n − | ). | n − i |
| 11 | [Binary Number Triangle](04-patterns/11-pattern-11.md) | — | 📘 Theory | — | Cell (i, j) prints 1 when i + j is even, else 0 — parity of the position. |
| 12 | [Number Crown](04-patterns/12-pattern-12.md) | — | 📘 Theory | — | Three segments per row: 1 … i, then 2(n − i) spaces, then i … 1. |
| 13 | [Increasing Number Triangle](04-patterns/13-pattern-13.md) | — | 📘 Theory | — | The value lives across rows: a counter declared outside both loops, incremented every cell. |
| 14 | [Letter Triangle](04-patterns/14-pattern-14.md) | — | 📘 Theory | — | Pattern 3 with letters: cell j prints 'A' + j. |
| 15 | [Reverse Letter Triangle](04-patterns/15-pattern-15.md) | — | 📘 Theory | — | Pattern 14's content with pattern 5's shape: n − i + 1 letters per row. |
| 16 | [Alpha-Ramp](04-patterns/16-pattern-16.md) | — | 📘 Theory | — | Pattern 4 with letters: row i repeats 'A' + i − 1, i times. |
| 17 | [Alpha-Hill](04-patterns/17-pattern-17.md) | — | 📘 Theory | — | Pyramid shape (n − i spaces, 2i − 1 cells) with mirrored letters: rise to the peak 'A' + i − 1, then fall. |
| 18 | [Alpha-Triangle](04-patterns/18-pattern-18.md) | — | 📘 Theory | — | Row i starts at 'A' + n − i and runs up to 'A' + n − 1. |
| 19 | [Symmetric Void](04-patterns/19-pattern-19.md) | — | 📘 Theory | — | Two halves; each row = stars, gap, stars. |
| 20 | [Symmetric Butterfly](04-patterns/20-pattern-20.md) | — | 📘 Theory | — | 2n − 1 rows; stars s = i ≤ n ? |
| 21 | [Hollow Rectangle](04-patterns/21-pattern-21.md) | — | 📘 Theory | — | Visit every cell; print '*' iff it's on the border (first/last row or column), else a space. |
| 22 | [Concentric Number Square](04-patterns/22-pattern-22.md) | — | 📘 Theory | — | Cell value = n − min(distance to top, left, bottom, right). |

## Part 5: Time Complexity

[Part README](05-time-complexity/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Theory with Examples](05-time-complexity/01-theory-with-examples.md) | — | 📘 Theory | — | Count steps, keep the dominant term; loops, recursion, amortised, space, constraints |

## Part 6: Standard Libraries & Collections

[Part README](06-standard-libraries-and-collections/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [STL (C++)](06-standard-libraries-and-collections/01-stl.md) | — | 📘 Theory | — | vector, deque, stack/queue/priority_queue, set/map vs unordered, iterators, `<algorithm>`, comparators |
| 2 | [Java Collections](06-standard-libraries-and-collections/02-java-collections.md) | — | 📘 Theory | — | List/Set/Map hierarchy, boxing traps, TreeMap, ArrayDeque, PriorityQueue, Comparator |
| 3 | [Python Libraries: Part 1](06-standard-libraries-and-collections/03-python-libraries-part-1.md) | — | 📘 Theory | — | list/tuple/set/dict/str costs, slicing, comprehensions, `sort(key=)`, aliasing |
| 4 | [Python Libraries: Part 2](06-standard-libraries-and-collections/04-python-libraries-part-2.md) | — | 📘 Theory | — | deque, Counter, defaultdict, heapq, bisect, lru_cache, itertools, math, fast I/O |

## Part 7: Concept Basics

[Part README](07-concept-basics/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Basic Maths](07-concept-basics/01-basic-maths.md) | — | 📘 Theory | — | `%10` / `/10` digit peeling, √n divisor pairs, primes and sieve, Euclid GCD, modulo rules |
| 2 | [Basic Arrays](07-concept-basics/02-basic-arrays.md) | — | 📘 Theory | — | Contiguous memory → O(1) access, O(n) middle insert; 2D row-major; traversal patterns |
| 3 | [Basic Hashing](07-concept-basics/03-basic-hashing.md) | — | 📘 Theory | — | Pre-compute counts; count array for small keys, hash map otherwise; collisions |
| 4 | [Basic String](07-concept-basics/04-basic-string.md) | — | 📘 Theory | — | Strings are char arrays; ASCII arithmetic, immutability, builder pattern, costs |

## Part 8: Basic Maths

[Part README](08-basic-maths/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Count All Digits of a Number](08-basic-maths/01-count-all-digits-of-a-number.md) | — | Easy | O(1) | Each `n //= 10` strips one digit, so the loop runs once per digit; `0` has one digit. |
| 2 | [Count Number of Odd Digits in a Number](08-basic-maths/02-count-number-of-odd-digits-in-a-number.md) | — | Easy | O(log₁₀ n) | Use the digit loop and test each digit `d` with `d % 2 == 1`. |
| 3 | [Reverse a Number](08-basic-maths/03-reverse-a-number.md) | — | Easy | O(log₁₀ n) | `rev = rev * 10 + n % 10` shifts the reversed number left by one digit and appends the next digit. |
| 4 | [Palindrome Number](08-basic-maths/04-palindrome-number.md) | — | Easy | O(log₁₀ n) | Reverse only the back half of the digits and compare it with the front half. |
| 5 | [Return the Largest Digit in a Number](08-basic-maths/05-return-the-largest-digit-in-a-number.md) | — | Easy | O(log₁₀ n) | Use the digit loop with a running max. |
| 6 | [Factorial of a Given Number](08-basic-maths/06-factorial-of-a-given-number.md) | — | Easy | O(n) | Use a running product with `0! |
| 7 | [Check if the Number is Armstrong](08-basic-maths/07-check-if-the-number-is-armstrong.md) | — | Easy | O(d · log k) ≈ O(log n) | Use two digit loops: one counts the digits `k`, the other sums `dᵏ`. |
| 8 | [Check for Perfect Number](08-basic-maths/08-check-for-perfect-number.md) | — | Easy | O(√n) | Divisors come in pairs `(i, n/i)` with `i ≤ √n`. |
| 9 | [Check for Prime Number](08-basic-maths/09-check-for-prime-number.md) | — | Easy | O(√n / 3) | Composite `n` has a factor ≤ √n, so trial division up to √n settles it. |
| 10 | [Count of Prime Numbers till N](08-basic-maths/10-count-of-prime-numbers-till-n.md) | — | Medium | O(n log log n) | Sieve of Eratosthenes: cross out the multiples of each prime starting at `p²`. |
| 11 | [GCD of Two Numbers](08-basic-maths/11-gcd-of-two-numbers.md) | — | Easy | O(log min(a,b)) | Euclid: `gcd(a, b) = gcd(b, a mod b)`, and `gcd(a, 0) = a`. |
| 12 | [LCM of Two Numbers](08-basic-maths/12-lcm-of-two-numbers.md) | — | Easy | O(log min(a,b)) | `lcm · gcd = a · b`, so `lcm = a / gcd(a, b) * b`. |
| 13 | [Divisors of a Number](08-basic-maths/13-divisors-of-a-number.md) | — | Easy | O(√n) | Loop `i` up to √n. |

## Part 9: Basic Arrays

[Part README](09-basic-arrays/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Sum of Array Elements](09-basic-arrays/01-sum-of-array-elements.md) | — | Easy | x | One pass with an accumulator that starts at 0. |
| 2 | [Count of Odd Numbers in Array](09-basic-arrays/02-count-of-odd-numbers-in-array.md) | — | Easy | O(n) | `x & 1` is 1 for odd `x`, including negatives in two's complement, so `cnt += x & 1` needs no branch. |
| 3 | [Check if the Array is Sorted](09-basic-arrays/03-check-if-the-array-is-sorted.md) | — | Easy | O(n) | Sortedness is a local property. |
| 4 | [Reverse an Array](09-basic-arrays/04-reverse-an-array.md) | — | Easy | O(n) | Swap `a[l]` and `a[r]` and move both pointers inward until they meet. |

## Part 10: Basic Hashing

[Part README](10-basic-hashing/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Highest Occurring Element in an Array](10-basic-hashing/01-highest-occurring-element-in-an-array.md) | — | Easy | O(n) | Count with a map, then do one scan with the comparison key `(-freq, value)`. |
| 2 | [Second Highest Occurring Element](10-basic-hashing/02-second-highest-occurring-element.md) | — | Easy | O(n) | Track the top-two distinct frequencies and their best elements in one scan of the map, the same way you'd track first and second largest. |
| 3 | [Sum of Highest and Lowest Frequency](10-basic-hashing/03-sum-of-highest-and-lowest-frequency.md) | — | Easy | O(n) | After counting, only the frequency values matter, so take the max and min of `freq.values()`. |

## Part 11: Basic Strings

[Part README](11-basic-strings/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Reverse a String](11-basic-strings/01-reverse-a-string.md) | — | Easy | O(n) | This is the array reverse from Part 9 on chars: swap `s[l]` and `s[r]`, move inward, stop at `l ≥ r`. |
| 2 | [Palindrome Check](11-basic-strings/02-palindrome-check.md) | — | Easy | O(n) | Compare `s[l]` with `s[r]` while moving inward. |
| 3 | [Largest Odd Number in a String](11-basic-strings/03-largest-odd-number-in-a-string.md) | — | Easy | O(n) | A number is odd iff its last digit is odd. |
| 4 | [Longest Common Prefix](11-basic-strings/04-longest-common-prefix.md) | — | Easy | O(S) total chars | Scan column by column (vertical scan). |
| 5 | [Isomorphic Strings](11-basic-strings/05-isomorphic-strings.md) | — | Easy | O(n) | The mapping must be a bijection. |
| 6 | [Rotate String](11-basic-strings/06-rotate-string.md) | — | Easy | O(n) with KMP; O(n²) worst case naive | Every rotation of `s` is a length-n window of `s + s`. |
| 7 | [Valid Anagram](11-basic-strings/07-valid-anagram.md) | — | Easy | O(n) | Anagrams have identical character counts. |
| 8 | [Sort Characters by Frequency](11-basic-strings/08-sort-characters-by-frequency.md) | — | Medium | O(n + Σ) | Count, then bucket by frequency: `bucket[f]` holds the chars that occur `f` times. |

## Part 12: Basic Recursion

[Part README](12-basic-recursion/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Recursion Theory](12-basic-recursion/01-recursion-theory.md) | — | 📘 Theory | — | Base case, call stack, stack overflow, recursion trees, head vs tail printing, complexity |
| 2 | [Recursion Concepts with Parameters](12-basic-recursion/02-recursion-concepts-with-parameters.md) | — | 📘 Theory | — | Parameterised vs functional, index parameters instead of slices, pass-by-value traps, multiple calls |
| 3 | [Sum of First N Numbers](12-basic-recursion/03-sum-of-first-n-numbers.md) | — | Easy | O(N) | `S(N) = N + S(N − 1)`, with `S(0) = 0`. |
| 4 | [Factorial of a Given Number](12-basic-recursion/04-factorial-of-a-given-number.md) | — | Easy | O(n) | `n! |
| 5 | [Sum of Array Elements](12-basic-recursion/05-sum-of-array-elements.md) | — | Easy | O(n) | Recurse on an **index**, not a slice: `f(i) = nums[i] + f(i + 1)`, `f(n) = 0`. |
| 6 | [Reverse a String (Recursive)](12-basic-recursion/06-reverse-a-string-recursive.md) | — | Easy | O(n) | Swap the ends and recurse inward on `(l + 1, r − 1)`, stopping at `l ≥ r`. |
| 7 | [Check if String is Palindrome or Not](12-basic-recursion/07-check-if-string-is-palindrome.md) | — | Easy | O(n) | `isPal(l, r) = s[l] == s[r] and isPal(l + 1, r − 1)`, with `l ≥ r → true`. |
| 8 | [Check if a Number is Prime or Not](12-basic-recursion/08-check-if-a-number-is-prime.md) | — | Easy | O(√n) | Only divisors up to `√num` matter. |
| 9 | [Reverse an Array (Recursive)](12-basic-recursion/09-reverse-an-array-recursive.md) | — | Easy | O(n) | The same two-ended recursion as the string: swap `nums[l]` and `nums[r]`, then call `f(l + 1, r − 1)`. |
| 10 | [Check if the Array is Sorted](12-basic-recursion/10-check-if-the-array-is-sorted-recursive.md) | — | Easy | O(n) | Sorted means every adjacent pair is in order: `f(i) = nums[i] ≤ nums[i + 1] and f(i + 1)`, base `i ≥ n − 1 → true`. |
| 11 | [Sum of Digits in a Given Number](12-basic-recursion/11-sum-of-digits.md) | — | Easy | O(d) = O(log n) | Peel off the last digit: `f(n) = n % 10 + f(n / 10)`, `f(0) = 0`. |
| 12 | [Fibonacci Number](12-basic-recursion/12-fibonacci-number.md) | — | Easy | O(n) | Naive `F(n−1) + F(n−2)` recomputes the same subproblems, which is O(φⁿ). |

## Part 13: Sorting

[Part README](13-sorting/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 0 | [Sorting Theory](13-sorting/00-sorting-theory.md) | — | 📘 Theory | — | Stability/in-place/adaptive properties, full comparison table, the Ω(n log n) lower bound, counting/radix/bucket sort, library sorts and comparators, sort-first patterns and a c… |
| 1 | [Selection Sort](13-sorting/01-selection-sort.md) | — | Easy | O(n²) in every case | For each position `i`, find the minimum of the unsorted suffix `[i, n)` and swap it into `i`. |
| 2 | [Bubble Sort](13-sorting/02-bubble-sort.md) | — | Easy | O(n²) worst / avg, O(n) best | Each pass swaps adjacent out-of-order pairs, which carries the largest unsorted element to the end. |
| 3 | [Insertion Sort](13-sorting/03-insertion-sort.md) | — | Easy | O(n²) worst / avg, O(n) best | Grow a sorted prefix: take `key = nums[i]`, shift every larger element of `[0, i)` one step right, and drop `key` into the gap. |
| 4 | [Merge Sort](13-sorting/04-merge-sort.md) | — | Medium | O(n log n) best / avg / worst | Split in half, sort each half recursively, then merge the two sorted halves in O(n) with two pointers. |
| 5 | [Quick Sort](13-sorting/05-quick-sort.md) | — | Medium | O(n log n) avg / best, O(n²) worst (rare with random pivot) | Partition around a pivot so that everything ≤ pivot is on its left and everything greater is on its right; the pivot is then in its final position. |
| 6 | [Recursive Bubble Sort](13-sorting/06-recursive-bubble-sort.md) | — | Easy | O(n²) worst, O(n) best | One pass over `[0, n)` puts the maximum at index `n − 1`; then sort the first `n − 1` recursively. |
| 7 | [Recursive Insertion Sort](13-sorting/07-recursive-insertion-sort.md) | — | Easy | O(n²) worst, O(n) best | To sort `[0, n)`: sort `[0, n − 1)` recursively, then insert `nums[n − 1]` into that sorted prefix. |

## Part 14: Arrays

[Part README](14-arrays/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 0 | [Array Techniques](14-arrays/00-array-techniques-theory.md) | — | 📘 Theory | — | Cost model, read/write pointers, reversal trick, two pointers, prefix/difference/2D prefix, Kadane, Dutch flag, Boyer–Moore, index-as-hash, matrix moves and a technique map. |
| 1 | [Linear Search](14-arrays/01-linear-search.md) | Fundamentals | Easy | O(n) | Scan left to right and return at the first match. |
| 2 | [Largest Element](14-arrays/02-largest-element.md) | Fundamentals | Easy | O(n) | Seed `best` with `nums[0]` (not 0 and not `INT_MIN` by habit) and update it in a single pass. |
| 3 | [Second Largest Element](14-arrays/03-second-largest-element.md) | Fundamentals | Easy | O(n) | Keep `first` and `second` in one pass. |
| 4 | [Maximum Consecutive Ones](14-arrays/04-maximum-consecutive-ones.md) | Fundamentals | Easy | O(n) | Keep a running streak: +1 on a 1, reset to 0 on a 0, and record the best after every step. |
| 5 | [Left Rotate Array by One](14-arrays/05-left-rotate-array-by-one.md) | Fundamentals | Easy | O(n) | Save `nums[0]`, shift `nums[1..n−1]` left by one, put the saved value at `n − 1`. |
| 6 | [Left Rotate Array by K Places](14-arrays/06-left-rotate-array-by-k.md) | Fundamentals | Easy | O(n) | Reduce `k %= n`. |
| 7 | [Move Zeros to End](14-arrays/07-move-zeros-to-end.md) | Logic building | Easy | O(n) | Two pointers: `j` marks where the next non-zero belongs. |
| 8 | [Remove Duplicates from Sorted Array](14-arrays/08-remove-duplicates-from-sorted-array.md) | Logic building | Easy | O(n) | Sorted means duplicates are adjacent. |
| 9 | [Find Missing Number](14-arrays/09-find-missing-number.md) | Logic building | Easy | O(n) | The expected total is `n(n + 1)/2`, so the missing number is that minus `sum(nums)`. |
| 10 | [Union of Two Sorted Arrays](14-arrays/10-union-of-two-sorted-arrays.md) | Logic building | Easy | O(n + m) | Merge with two pointers like merge sort, but append a value only if it differs from the last value appended. |
| 11 | [Intersection of Two Sorted Arrays](14-arrays/11-intersection-of-two-sorted-arrays.md) | Logic building | Easy | O(n + m) | Two pointers: advance the smaller side; on equality, record the value and advance both. |
| 12 | [Majority Element I](14-arrays/12-majority-element.md) | FAQs — Medium | Easy | O(n) | Boyer–Moore voting: pair each majority vote with a different vote and cancel both. |
| 13 | [Leaders in an Array](14-arrays/13-leaders-in-an-array.md) | FAQs — Medium | Easy | O(n) | Scan from the right keeping `maxRight`. |
| 14 | [Rearrange Array Elements by Sign](14-arrays/14-rearrange-by-sign.md) | FAQs — Medium | Medium | O(n) | Positives go to even indices and negatives to odd indices. |
| 15 | [Print the Matrix in Spiral Manner](14-arrays/15-spiral-matrix.md) | FAQs — Medium | Medium | O(m · n) | Keep four boundaries: `top`, `bottom`, `left`, `right`. |
| 16 | [Pascal's Triangle I](14-arrays/16-pascals-triangle-i.md) | FAQs — Medium | Easy | O(min(k, n − k)) | That element is C(r − 1, c − 1). |
| 17 | [Pascal's Triangle II](14-arrays/17-pascals-triangle-ii.md) | FAQs — Medium | Easy | O(r) | Row `r` is C(r − 1, 0), C(r − 1, 1), …, C(r − 1, r − 1). |
| 18 | [Pascal's Triangle III](14-arrays/18-pascals-triangle-iii.md) | FAQs — Medium | Easy | O(n²) | Each row's inner values are sums of adjacent pairs from the previous row: `row[j] = prev[j − 1] + prev[j]`, with 1s at both ends. |
| 19 | [Rotate Matrix by 90 Degrees](14-arrays/19-rotate-matrix.md) | FAQs — Medium | Medium | O(n²) | A clockwise rotation is a transpose (swap across the main diagonal) followed by reversing each row. |
| 20 | [Set Matrix Zeroes](14-arrays/20-set-matrix-zeroes.md) | FAQs — Medium | Medium | O(m · n) | Use the first row and first column as the marker arrays. |
| 21 | [Two Sum](14-arrays/21-two-sum.md) | FAQs — Medium | Easy | O(n) | For each `x`, the partner it needs is `target − x`. |
| 22 | [3 Sum](14-arrays/22-3-sum.md) | FAQs — Medium | Medium | O(n²) | Sort. |
| 23 | [4 Sum](14-arrays/23-4-sum.md) | FAQs — Medium | Medium | O(n³) | Exactly 3Sum with one more fixed loop: sort, fix `i` and `j` (skipping duplicates of each), then two-pointer for the remainder. |
| 24 | [Sort an Array of 0s, 1s and 2s](14-arrays/24-sort-colors.md) | FAQs — Medium | Medium | O(n), one pass | Dutch National Flag: three pointers `low`, `mid`, `high`. |
| 25 | [Kadane's Algorithm: Maximum Subarray Sum](14-arrays/25-kadanes-algorithm.md) | FAQs — Medium | Medium | O(n) | At each index, either extend the best subarray ending at `i − 1` or start fresh: `cur = max(x, cur + x)`. |
| 26 | [Next Permutation](14-arrays/26-next-permutation.md) | FAQs — Medium | Medium | O(n) | From the right, find the first `i` with `nums[i] < nums[i + 1]` (the pivot). |
| 27 | [Majority Element II](14-arrays/27-majority-element-ii.md) | FAQs — Hard | Medium | O(n) | At most two elements can exceed n/3. |
| 28 | [Find the Repeating and Missing Number](14-arrays/28-repeating-and-missing.md) | FAQs — Hard | Hard | O(n) | Two equations in `x` (repeating) and `y` (missing): `S − Sₙ = x − y` and `S₂ − S₂ₙ = x² − y²`. |
| 29 | [Count Inversions](14-arrays/29-count-inversions.md) | FAQs — Hard | Hard | O(n log n) | Piggyback on merge sort. |
| 30 | [Reverse Pairs](14-arrays/30-reverse-pairs.md) | FAQs — Hard | Hard | O(n log n) | Merge-sort counting again, but the condition isn't the merge's comparison. |
| 31 | [Maximum Product Subarray](14-arrays/31-maximum-product-subarray.md) | FAQs — Hard | Medium | O(n) | A negative number turns the smallest product into the largest. |
| 32 | [Merge Two Sorted Arrays Without Extra Space](14-arrays/32-merge-sorted-arrays.md) | FAQs — Hard | Medium | O(m + n) | Fill `nums1` from the back. |
| 33 | [Check if array is sorted and rotated](14-arrays/33-check-if-array-is-sorted-and-rotated.md) | Extra (A2Z sheet) | Easy | O(n) | Walk the array circularly and count the **drops**, places where `a[i] > a[(i+1) % n]`. |

## Part 15: Hashing

[Part README](15-hashing/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Basic Hashing](15-hashing/01-basic-hashing.md) | — | 📘 Theory | — | Hash functions, collisions, load factor, array vs map hashing, language APIs and their worst cases |
| 2 | [Longest Consecutive Sequence in an Array](15-hashing/02-longest-consecutive-sequence.md) | FAQs | Medium | O(n) average | Put everything in a set. |
| 3 | [Longest Subarray with Sum K](15-hashing/03-longest-subarray-with-sum-k.md) | FAQs | Medium | O(n) average | `sum(l..i) = P[i] − P[l − 1]`. |
| 4 | [Largest Subarray with Sum 0](15-hashing/04-largest-subarray-with-sum-0.md) | FAQs | Medium | O(n) average | Sum of `(j, i]` is 0 iff `P[i] == P[j]`. |
| 5 | [Count Subarrays with Given Sum](15-hashing/05-count-subarrays-with-given-sum.md) | FAQs | Medium | O(n) average | Every earlier prefix equal to `P[i] − k` starts one valid subarray ending at `i`. |
| 6 | [Count Subarrays with Given XOR K](15-hashing/06-count-subarrays-with-xor-k.md) | FAQs | Medium | O(n) average | `xor(l..r) = X[r] ^ X[l − 1]`, and `a ^ b = k ⇔ b = a ^ k`. |

## Part 16: Binary Search

[Part README](16-binary-search/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Binary Search Templates](16-binary-search/01-binary-search-templates.md) | — | 📘 Theory | — | Closed vs half-open loops, first-true / last-true, overflow-safe mid, BS on answer, rotated arrays, real-valued search |
| 2 | [Search X in Sorted Array](16-binary-search/02-binary-search.md) | Fundamentals | Easy | O(log n) | Compare with the middle element and throw away the half that cannot contain the target. |
| 3 | [Lower Bound](16-binary-search/03-lower-bound.md) | Fundamentals | Easy | O(log n) | Keep `ans = n`. |
| 4 | [Upper Bound](16-binary-search/04-upper-bound.md) | Fundamentals | Easy | O(log n) | Identical to lower bound with `≥` replaced by `>`. |
| 5 | [Search Insert Position](16-binary-search/05-search-insert-position.md) | Logic building — 1D arrays | Easy | O(log n) | Both answers are the same number: the first index with `nums[i] ≥ target`. |
| 6 | [Floor and Ceil in Sorted Array](16-binary-search/06-floor-and-ceil.md) | Logic building — 1D arrays | Easy | O(log n) | Ceil is the value at lower bound. |
| 7 | [First and Last Occurrence](16-binary-search/07-first-and-last-occurrence.md) | Logic building — 1D arrays | Easy | O(log n) | First = lower bound (if it holds target). |
| 8 | [Search in Rotated Sorted Array I](16-binary-search/08-search-in-rotated-sorted-array-i.md) | Logic building — 1D arrays | Medium | O(log n) | Any `mid` splits the array into two halves and **at least one of them is sorted** (`nums[lo] ≤ nums[mid]` → left is sorted). |
| 9 | [Search in Rotated Sorted Array II](16-binary-search/09-search-in-rotated-sorted-array-ii.md) | Logic building — 1D arrays | Medium | O(log n) average, O(n) worst | Same "sorted half" logic — except when `nums[lo] == nums[mid] == nums[hi]` you can't tell which half is sorted. |
| 10 | [Find Minimum in Rotated Sorted Array](16-binary-search/10-minimum-in-rotated-sorted-array.md) | Logic building — 1D arrays | Medium | O(log n) | Compare `nums[mid]` with `nums[hi]`. |
| 11 | [Find Out How Many Times the Array Is Rotated](16-binary-search/11-rotation-count.md) | Logic building — 1D arrays | Easy | O(log n) | The rotation count is the **index of the minimum**. |
| 12 | [Single Element in a Sorted Array](16-binary-search/12-single-element-in-sorted-array.md) | Logic building — 1D arrays | Medium | O(log n) | Before the single element, pairs start at **even** indices (`nums[2i] == nums[2i+1]`); after it, they start at odd indices. |
| 13 | [Count Occurrences in a Sorted Array](16-binary-search/13-count-occurrences.md) | Logic building — 1D arrays | Easy | O(log n) | `upper_bound(target) − lower_bound(target)`. |
| 14 | [Find Square Root of a Number](16-binary-search/14-square-root.md) | Binary search on answers | Easy | O(log n) | `mid² ≤ n` is true for small `mid` and false for large — monotone. |
| 15 | [Find Nth Root of a Number](16-binary-search/15-nth-root.md) | Binary search on answers | Medium | O(n log m) | Binary search `x` in `[1, m]`. |
| 16 | [Find the Smallest Divisor](16-binary-search/16-smallest-divisor.md) | Binary search on answers | Medium | O(n log max) | Larger `d` → every ceiling shrinks → sum is non-increasing. |
| 17 | [Koko Eating Bananas](16-binary-search/17-koko-eating-bananas.md) | Binary search on answers | Medium | O(n log max) | Hours needed at speed `k` = `Σ ⌈pile / k⌉`, non-increasing in `k`. |
| 18 | [Minimum Days to Make M Bouquets](16-binary-search/18-minimum-days-to-make-m-bouquets.md) | Binary search on answers | Medium | O(n log(max − min)) | By day `d` the bloomed set only grows, so `bouquets(d)` is non-decreasing. |
| 19 | [Capacity to Ship Packages Within D Days](16-binary-search/19-ship-within-days.md) | Binary search on answers | Medium | O(n log Σw) | Range `[max(w), Σw]`: below max a package never fits, at Σw it all ships in one day. |
| 20 | [Kth Missing Positive Number](16-binary-search/20-kth-missing-positive-number.md) | Binary search on answers | Easy | O(log n) | Missing count before index `i` is `arr[i] − (i + 1)`, and it's non-decreasing. |
| 21 | [Painter's Partition](16-binary-search/21-painters-partition.md) | Binary search on answers | Hard | O(n log Σ) | Same as shipping packages with `days = k`: binary search the max load in `[max, Σ]`, greedy-count painters needed. |
| 22 | [Aggressive Cows](16-binary-search/22-aggressive-cows.md) | FAQs | Hard | O(n log n + n log range) | If a gap `d` is achievable, every smaller gap is too — T…T F…F. |
| 23 | [Book Allocation Problem](16-binary-search/23-book-allocation-problem.md) | FAQs | Hard | O(n log Σ) | Exactly ship-within-days: binary search the max pages `[max, Σ]`, greedy-count students needed. |
| 24 | [Find Peak Element](16-binary-search/24-find-peak-element.md) | FAQs | Medium | O(log n) | Compare `nums[mid]` with `nums[mid + 1]`. |
| 25 | [Median of 2 Sorted Arrays](16-binary-search/25-median-of-two-sorted-arrays.md) | FAQs | Hard | O(log min(n₁, n₂)) | Binary search how many elements `c1` the **left half** takes from the smaller array; `c2 = half − c1` come from the other. |
| 26 | [Kth Element of 2 Sorted Arrays](16-binary-search/26-kth-element-of-two-sorted-arrays.md) | FAQs | Medium | O(log min(n₁, n₂)) | Same partition search as the median, with left-half size `k`. |
| 27 | [Minimize Max Distance to Gas Station](16-binary-search/27-minimise-max-distance-to-gas-station.md) | FAQs | Hard | O(n · 100) | Binary search on a **real** answer `d`: a gap `g` needs `⌈g / d⌉ − 1` new stations to bring every piece ≤ d. |
| 28 | [Split Array — Largest Sum](16-binary-search/28-split-array-largest-sum.md) | FAQs | Hard | O(n log Σ) | Third name for the same problem (Book Allocation, Painter's Partition). |
| 29 | [Find Row with Maximum 1's](16-binary-search/29-row-with-maximum-ones.md) | 2D arrays | Easy | O(n log m) | In a sorted 0/1 row, ones = `m − lower_bound(row, 1)`. |
| 30 | [Search in a 2D Matrix](16-binary-search/30-search-in-a-2d-matrix.md) | 2D arrays | Medium | O(log(n · m)) | The matrix is one sorted array of length `n·m` laid out row by row. |
| 31 | [Search in 2D Matrix II](16-binary-search/31-search-in-2d-matrix-ii.md) | 2D arrays | Medium | O(n + m) | Start at the top-right. |
| 32 | [Find Peak Element II](16-binary-search/32-find-peak-element-ii.md) | 2D arrays | Hard | O(n log m) | Binary search **columns**. |
| 33 | [Matrix Median](16-binary-search/33-matrix-median.md) | 2D arrays | Hard | O(n log m · log(max − min)) | Binary search on the **value** `x ∈ [min, max]`. |

## Part 17: Strings (Basic and Medium)

[Part README](17-strings-basic-medium/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 0 | [String Fundamentals](17-strings-basic-medium/00-string-basics-theory.md) | — | 📘 Theory | — | Immutability and builder costs, char arithmetic, frequency tables, overflow-safe parsing, balance counters, palindrome expansion, substring enumeration, rotation and where advan… |
| 1 | [Remove Outermost Parentheses](17-strings-basic-medium/01-remove-outermost-parentheses.md) | Parentheses | Easy | O(n) | Track depth. |
| 2 | [Maximum Nesting Depth of the Parentheses](17-strings-basic-medium/02-maximum-nesting-depth-of-the-parentheses.md) | Parentheses | Easy | O(n) | Depth goes up on `(` and down on `)`; the answer is the highest value it reaches. |
| 3 | [Roman to Integer](17-strings-basic-medium/03-roman-to-integer.md) | String conversions | Easy | O(n) | Add each symbol's value, except when it's smaller than the next symbol — then subtract it (IV = −1 + 5). |
| 4 | [String to Integer (atoi)](17-strings-basic-medium/04-string-to-integer-atoi.md) | String conversions | Medium | O(n) | It's a 4-state machine: skip spaces → optional sign → digits → stop at the first non-digit. |
| 5 | [Count Substrings with Exactly K Distinct Characters](17-strings-basic-medium/05-count-substrings-k-distinct.md) | Substring problems | Medium | O(n) | "At most k distinct" is monotone, so a sliding window counts it in O(n): every valid window ending at `r` contributes `r − l + 1` substrings. |
| 6 | [Longest Palindromic Substring](17-strings-basic-medium/06-longest-palindromic-substring.md) | Substring problems | Medium | O(n²) | Every palindrome mirrors around a centre — a character (odd length) or a gap (even length). |
| 7 | [Sum of Beauty of All Substrings](17-strings-basic-medium/07-sum-of-beauty-of-all-substrings.md) | Substring problems | Medium | O(26 · n²) | Fix the start, extend the end one char at a time, and update a 26-entry count array incrementally — no recount per substring. |

## Part 18: Recursion

[Part README](18-recursion/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Subsequence Patterns](18-recursion/01-subsequence-patterns.md) | — | 📘 Theory | — | Pick/not-pick tree, print all / print one / count, sum-K variants, for-loop template, duplicate skipping, complexity of recursion trees |
| 2 | [Pow(x, n)](18-recursion/02-pow-x-n.md) | Implementation problems | Medium | n | xⁿ = (x^(n/2))² when n is even, and x · xⁿ⁻¹ when odd. |
| 3 | [Generate Parentheses](18-recursion/03-generate-parentheses.md) | Implementation problems | Medium | O(4ⁿ / √n) | Build left to right and only make legal moves: add `(` while `open < n`, add `)` while `close < open`. |
| 4 | [Power Set](18-recursion/04-power-set.md) | Implementation problems | Medium | O(n · 2ⁿ) | Each element is either in or out — two branches per element, 2ⁿ leaves. |
| 5 | [Count Good Numbers](18-recursion/05-count-good-numbers.md) | Implementation problems | Medium | O(log n) | Positions are independent: ⌈n/2⌉ even indices with 5 choices {0,2,4,6,8}, ⌊n/2⌋ odd indices with 4 choices {2,3,5,7}. |
| 6 | [Reverse a Stack](18-recursion/06-reverse-a-stack.md) | Implementation problems | Medium | O(n²) | Two recursions: `reverse` pops the top, reverses the rest, then pushes the saved element to the *bottom*. |
| 7 | [Check if There Exists a Subsequence with Sum K](18-recursion/07-subsequence-sum-k-exists.md) | Subsequence pattern problems | Medium | O(n · k) | Pick/not-pick recursion with a **boolean return**: return true as soon as any branch succeeds, which prunes the rest. |
| 8 | [Count All Subsequences with Sum K](18-recursion/08-count-subsequences-sum-k.md) | Subsequence pattern problems | Medium | O(n · k) | Same pick/not-pick tree, but **return a count**: base cases return 1 or 0, and each node returns `take + skip`. |
| 9 | [Generate Binary Strings Without Consecutive 1s](18-recursion/09-binary-strings-no-consecutive-ones.md) | Subsequence pattern problems | Medium | O(n · Fib(n)) | At each position you can always place `0`; place `1` only if the previous char isn't `1`. |
| 10 | [Combination Sum](18-recursion/10-combination-sum.md) | FAQs (Medium) | Medium | O(2^(t/m) · t) | Loop-based backtracking from a start index: choosing `c[j]` recurses with start `j` (not `j + 1`) so it can be reused, and never looks back at earlier candidates — that's what m… |
| 11 | [Combination Sum II](18-recursion/11-combination-sum-ii.md) | FAQs (Medium) | Medium | O(2ⁿ · n) worst | Sort, then in the loop at each level skip `c[j]` if `j > start` and `c[j] == c[j − 1]` — an equal value was already tried *at this position*. |
| 12 | [Subsets I (Subset Sums)](18-recursion/12-subset-sums.md) | FAQs (Medium) | Medium | O(2ⁿ) | Pick/not-pick carrying only the running sum — no list to copy, so each leaf costs O(1). |
| 13 | [Subsets II](18-recursion/13-subsets-ii.md) | FAQs (Medium) | Medium | O(n · 2ⁿ) | Sort, then use the loop form: every recursion node *is* a subset (record it on entry), and the loop picks the next element with the sibling-skip `j > i && a[j] == a[j−1]`. |
| 14 | [Combination Sum III](18-recursion/14-combination-sum-iii.md) | FAQs (Medium) | Medium | O(C(9, k) · k) | Choose digits in increasing order from `start`; stop when the size reaches k. |
| 15 | [Letter Combinations of a Phone Number](18-recursion/15-letter-combinations-of-a-phone-number.md) | Hard | Medium | O(4ⁿ · n) | One recursion level per digit, one branch per letter of that digit — a Cartesian product. |
| 16 | [Palindrome Partitioning](18-recursion/16-palindrome-partitioning.md) | FAQs (Hard) | Medium | O(n · 2ⁿ) | Recurse on the start index: for every end `e ≥ start` where `s[start..e]` is a palindrome, cut there and recurse on `e + 1`. |
| 17 | [Word Search](18-recursion/17-word-search.md) | FAQs (Hard) | Medium | O(m·n·3^L) | DFS from every cell matching `word[0]`; at depth k the cell must equal `word[k]`. |
| 18 | [N-Queens](18-recursion/18-n-queens.md) | FAQs (Hard) | Hard | O(n!) | One queen per row, so recurse on the row and choose a column. |
| 19 | [Rat in a Maze](18-recursion/19-rat-in-a-maze.md) | FAQs (Hard) | Medium | O(3^(n²) · n²) | Grid DFS with a visited mark and backtracking. |
| 20 | [M-Coloring Problem](18-recursion/20-m-coloring.md) | FAQs (Hard) | Medium | O(mⁿ) worst | Colour vertices 0, 1, 2, … in order; for vertex v try each colour not used by an already-coloured neighbour, recurse, and undo on failure. |
| 21 | [Sudoku Solver](18-recursion/21-sudoku-solver.md) | FAQs (Hard) | Hard | O(9^E) | Find the next empty cell, try digits 1–9 that are absent from its row, column and box, recurse, and undo on failure. |
| 22 | [Expression Add Operators](18-recursion/22-expression-add-operators.md) | FAQs (Hard) | Hard | O(n · 4ⁿ) | Backtrack over the next operand `num[i..j]` and its operator, carrying `value` (total so far) and `last` (the last multiplicative term). |
| 23 | [Sort a stack using recursion](18-recursion/23-sort-a-stack-using-recursion.md) | Extra (A2Z sheet) | Medium | O(n²) | Do the same thing as reverse-a-stack, but with *sorted* insertion. |

## Part 19: Linked List

[Part README](19-linked-list/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Singly Linked List](19-linked-list/01-singly-linked-list.md) | — | 📘 Theory | — | Node anatomy, array vs list, traversal, insert/delete at head/tail/K/value, dummy head, memory and pointer safety |
| 2 | [Doubly Linked List](19-linked-list/02-doubly-linked-list.md) | — | 📘 Theory | — | prev pointer, building from an array, four-link insertion, unlinking a node, reversal by swapping prev/next, when DLL beats SLL |
| 3 | [Traversal in Linked List](19-linked-list/03-traversal-in-linked-list.md) | Singly linked list — fundamentals | Easy | O(n) | Copy the head into a moving pointer `cur` and advance `cur = cur.next` until it is null. |
| 4 | [Deletion of the Head of LL](19-linked-list/04-deletion-of-the-head-of-ll.md) | Singly linked list — fundamentals | Easy | O(1) | The new head is `head.next`. |
| 5 | [Deletion of the Tail of LL](19-linked-list/05-deletion-of-the-tail-of-ll.md) | Singly linked list — fundamentals | Easy | O(n) | Stop at the **second-to-last** node (`cur.next.next == null`) and set `cur.next = null`. |
| 6 | [Deletion of the Kth Element of LL](19-linked-list/06-deletion-of-the-kth-element-of-ll.md) | Singly linked list — fundamentals | Easy | O(k) | `k = 1` is the head case. |
| 7 | [Delete the Element with Value X](19-linked-list/07-delete-the-element-with-value-x.md) | Singly linked list — fundamentals | Easy | O(n) | Same bypass as deleting by position, but the stop condition is `prev.next.val == x`. |
| 8 | [Insertion at the Head of LL](19-linked-list/08-insertion-at-the-head-of-ll.md) | Singly linked list — fundamentals | Easy | O(1) | `return new Node(x, head)` — one allocation, one pointer. |
| 9 | [Insertion at the Tail of LL](19-linked-list/09-insertion-at-the-tail-of-ll.md) | Singly linked list — fundamentals | Easy | O(n) | Walk to the node whose `next` is null and hang the new node there. |
| 10 | [Insertion at the Kth Position of LL](19-linked-list/10-insertion-at-the-kth-position-of-ll.md) | Singly linked list — fundamentals | Easy | O(k) | Reach node `k − 1` (the predecessor) and splice: `node.next = prev.next; prev.next = node`. |
| 11 | [Insertion Before the Value X in LL](19-linked-list/11-insertion-before-the-value-x-in-ll.md) | Singly linked list — fundamentals | Easy | O(n) | Search with the predecessor: stop when `prev.next.val == x`, then splice. |
| 12 | [Find the Length of the Linked List](19-linked-list/12-find-the-length-of-the-linked-list.md) | Singly linked list — fundamentals | Easy | O(n) | Traverse and count. |
| 13 | [Search in Linked List](19-linked-list/13-search-in-linked-list.md) | Singly linked list — fundamentals | Easy | O(n) | Linear scan with early exit. |
| 14 | [Convert Array to DLL](19-linked-list/14-convert-array-to-dll.md) | Doubly linked list — fundamentals | Easy | O(n) | Keep a `tail`; each new node gets `prev = tail`, then `tail.next = node; tail = node`. |
| 15 | [Delete Head of DLL](19-linked-list/15-delete-head-of-dll.md) | Doubly linked list — fundamentals | Easy | O(1) | `head = head.next`, then **clear the new head's `prev`** — the step singly lists don't have. |
| 16 | [Delete Tail of DLL](19-linked-list/16-delete-tail-of-dll.md) | Doubly linked list — fundamentals | Easy | O(n) | Walk to the tail itself (not its predecessor — `tail.prev` gives that), then `tail.prev.next = null`. |
| 17 | [Delete Kth Element of DLL](19-linked-list/17-delete-kth-element-of-dll.md) | Doubly linked list — fundamentals | Easy | O(k) | Walk **to** the k-th node (no predecessor needed). |
| 18 | [Removing Given Node in DLL](19-linked-list/18-removing-given-node-in-dll.md) | Doubly linked list — fundamentals | Easy | O(1) | A DLL node knows both neighbours, so no head and no walk are needed: `node.prev.next = node.next`, and if `node.next` exists, `node.next.prev = node.prev`. |
| 19 | [Insert Node Before Head in DLL](19-linked-list/19-insert-node-before-head-in-dll.md) | Doubly linked list — fundamentals | Easy | O(1) | `node = Node(x, next = head)`; then `head.prev = node` if head exists. |
| 20 | [Insert Node Before Tail in DLL](19-linked-list/20-insert-node-before-tail-in-dll.md) | Doubly linked list — fundamentals | Easy | O(n) | Walk to the tail; then the generic "insert before node `t`": `node = Node(x, next = t, prev = t.prev)`, `t.prev.next = node` (or new head), `t.prev = node`. |
| 21 | [Insert Node Before Kth Node in DLL](19-linked-list/21-insert-node-before-kth-node-in-dll.md) | Doubly linked list — fundamentals | Easy | O(k) | Walk to the k-th node `t`, then the same insert-before-`t` primitive. |
| 22 | [Insert Before Given Node in DLL](19-linked-list/22-insert-before-given-node-in-dll.md) | Doubly linked list — fundamentals | Easy | O(1) | No head needed: `node.prev` exists (not the head), so `p = node.prev; new = Node(x, next = node, prev = p); p.next = new; node.prev = new`. |
| 23 | [Reverse a Doubly Linked List](19-linked-list/23-reverse-a-doubly-linked-list.md) | Doubly linked list — fundamentals | Easy | O(n) | Swap `prev` and `next` in every node. |
| 24 | [Add Two Numbers in LL](19-linked-list/24-add-two-numbers-in-ll.md) | Logic building | Medium | O(max(m, n)) | Grade-school addition read left to right: `s = d1 + d2 + carry`, emit `s % 10`, carry `s // 10`. |
| 25 | [Segregate Odd and Even Nodes in LL](19-linked-list/25-segregate-odd-and-even-nodes-in-ll.md) | Logic building | Medium | O(n) | Two chains woven out of one list: `odd.next = even.next; odd = odd.next; even.next = odd.next; even = even.next`. |
| 26 | [Sort a LL of 0's, 1's and 2's](19-linked-list/26-sort-a-ll-of-0-s-1-s-and-2-s.md) | Logic building | Medium | O(n) | Three dummy-headed chains (zeros, ones, twos); append each node to its chain, then join `zero → one → two`. |
| 27 | [Remove Nth Node from the Back of the LL](19-linked-list/27-remove-nth-node-from-the-back-of-the-ll.md) | Logic building | Medium | O(n) | Gap of n between two pointers: move `fast` n steps ahead, then move both until `fast.next` is null — `slow` is the predecessor. |
| 28 | [Reverse a LL](19-linked-list/28-reverse-a-ll.md) | Logic building | Easy | O(n) | Three pointers: save `nxt = cur.next`, flip `cur.next = prev`, advance `prev = cur; cur = nxt`. |
| 29 | [Add One to a Number Represented by LL](19-linked-list/29-add-one-to-a-number-represented-by-ll.md) | FAQs (Medium) | Medium | O(n) | The carry starts at the **tail** but the list only goes forward. |
| 30 | [Find Middle of Linked List](19-linked-list/30-find-middle-of-linked-list.md) | FAQs (Medium) | Easy | O(n) | Tortoise and hare: slow moves 1, fast moves 2; when fast can't move, slow is at the middle. |
| 31 | [Delete the Middle Node in LL](19-linked-list/31-delete-the-middle-node-in-ll.md) | FAQs (Medium) | Medium | O(n) | You need the node **before** the middle. |
| 32 | [Check if LL is Palindrome or Not](19-linked-list/32-check-if-ll-is-palindrome-or-not.md) | FAQs (Medium) | Medium | O(n) | Find the middle, reverse the second half, compare the halves node by node, then (politely) reverse it back. |
| 33 | [Find the Intersection Point of Y LL](19-linked-list/33-find-the-intersection-point-of-y-ll.md) | FAQs (Medium) | Easy | O(m + n) | Two pointers that switch to the other list's head on reaching the end each walk `a + c + b` nodes — they meet at the junction (or both reach null together). |
| 34 | [Detect a Loop in LL](19-linked-list/34-detect-a-loop-in-ll.md) | FAQs (Medium) | Easy | O(n) | Floyd: slow moves 1, fast moves 2. |
| 35 | [Find the Starting Point in LL](19-linked-list/35-find-the-starting-point-in-ll.md) | FAQs (Medium) | Medium | O(n) | After Floyd's meeting, reset one pointer to head; move both one step at a time — they meet at the loop start. |
| 36 | [Length of Loop in LL](19-linked-list/36-length-of-loop-in-ll.md) | FAQs (Medium) | Easy | O(n) | Floyd's meeting point is inside the cycle; keep one pointer there and walk the other around until it returns, counting steps. |
| 37 | [Reverse LL in Group of Given Size K](19-linked-list/37-reverse-ll-in-group-of-given-size-k.md) | FAQs (Hard) | Hard | O(n) | Loop: find the k-th node from the current group start (null → stop). |
| 38 | [Rotate a LL](19-linked-list/38-rotate-a-ll.md) | FAQs (Hard) | Medium | O(n) | k %= n. |
| 39 | [Merge Two Sorted Lists](19-linked-list/39-merge-two-sorted-lists.md) | FAQs (Hard) | Easy | O(n+m) | Dummy node + tail pointer; attach the smaller head each step; attach the leftover list in one go at the end. |
| 40 | [Flattening of LL](19-linked-list/40-flattening-of-ll.md) | FAQs (Hard) | Hard | O(N · k) | It's merge-k-sorted-lists on the `child` pointer. |
| 41 | [Sort LL](19-linked-list/41-sort-ll.md) | FAQs (Hard) | Medium | O(n log n) | Merge sort is the natural fit: split at the **first** middle (fast/slow), sort halves recursively, merge. |
| 42 | [Clone a LL with Random and Next Pointer](19-linked-list/42-clone-a-ll-with-random-and-next-pointer.md) | FAQs (Hard) | Medium | O(n) | The hard part is mapping old → new for `random`. |
| 43 | [Delete All Occurrences of a Key in DLL](19-linked-list/43-delete-all-occurrences-of-a-key-in-dll.md) | FAQs (DLL) | Medium | O(n) | With `prev` available, deleting a node is local: `prev.next = nxt`, `nxt.prev = prev`. |
| 44 | [Remove Duplicates from Sorted DLL](19-linked-list/44-remove-duplicates-from-sorted-dll.md) | FAQs (DLL) | Medium | O(n) | Duplicates are adjacent. |
| 45 | [Find Pairs with Given Sum in DLL](19-linked-list/45-find-pairs-with-given-sum-in-dll.md) | FAQs (DLL) | Medium | O(n) | Two pointers from both ends — exactly the sorted-array 2-sum — because a DLL can walk backward. |

## Part 20: Bit Manipulation

[Part README](20-bit-manipulation/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Bits and Tricks](20-bit-manipulation/01-bits-and-tricks.md) | — | 📘 Theory | — | Binary and two's complement, operators and shifts, get/set/clear/toggle, n & (n−1), x & −x, XOR identities, masks and subsets, language pitfalls |
| 2 | [Check if the i-th Bit is Set](20-bit-manipulation/02-check-if-the-i-th-bit-is-set.md) | Bit fundamentals | Easy | O(1) | Build a mask with only bit k set (`1 << k`) and AND it with n, or shift n right by k and look at the last bit. |
| 3 | [Check if a Number is Odd](20-bit-manipulation/03-check-if-a-number-is-odd.md) | Bit fundamentals | Easy | O(1) | Every power of two except 2⁰ is even, so parity is decided entirely by bit 0: `n & 1`. |
| 4 | [Check if a Number is Power of 2](20-bit-manipulation/04-check-if-a-number-is-power-of-2.md) | Bit fundamentals | Easy | O(1) | A power of two has exactly one set bit. |
| 5 | [Count the Number of Set Bits](20-bit-manipulation/05-count-the-number-of-set-bits.md) | Bit fundamentals | Easy | O(popcount) | Brian Kernighan: `n &= n − 1` deletes one set bit per iteration, so the loop runs popcount(n) times instead of 32. |
| 6 | [Set the Rightmost Unset Bit](20-bit-manipulation/06-set-the-rightmost-unset-bit.md) | Bit fundamentals | Easy | (n + 1)`. | `n + 1` flips the trailing 1s to 0 and the lowest 0 to 1. |
| 7 | [Swap Two Numbers](20-bit-manipulation/07-swap-two-numbers.md) | Bit fundamentals | Easy | O(1) | XOR is its own inverse: `a ^= b; b ^= a; a ^= b` — after step 2, `b = b ^ (a ^ b) = a`; after step 3, `a = (a ^ b) ^ a = b`. |
| 8 | [Minimum Bit Flips to Convert Number](20-bit-manipulation/08-minimum-bit-flips-to-convert-number.md) | Problems | Easy | O(popcount) | XOR marks exactly the positions that differ; each one needs one flip. |
| 9 | [Single Number I](20-bit-manipulation/09-single-number-i.md) | Problems | Easy | O(n) | XOR all elements: pairs cancel (`x ^ x = 0`), order doesn't matter (commutative, associative), and the survivor is the single number. |
| 10 | [Single Number II](20-bit-manipulation/10-single-number-ii.md) | Problems | Medium | O(n) | XOR no longer cancels triples. |
| 11 | [Single Number III](20-bit-manipulation/11-single-number-iii.md) | Problems | Medium | O(n) | XOR of all = a ^ b ≠ 0, so a and b differ in at least one bit. |
| 12 | [Divide Two Integers](20-bit-manipulation/12-divide-two-integers.md) | Problems | Medium | O(log² n) | Repeated subtraction is O(quotient). |
| 13 | [Power Set (Bit Manipulation)](20-bit-manipulation/13-power-set.md) | Problems | Medium | O(n·2ⁿ) | Masks 0 … 2ⁿ − 1 are in one-to-one correspondence with subsets: bit i of the mask says whether `nums[i]` is included. |
| 14 | [XOR of Numbers in a Given Range](20-bit-manipulation/14-xor-of-numbers-in-a-given-range.md) | Problems | Medium | O(1) | Prefix XOR f(n) = 0 ^ 1 ^ … ^ n follows a period-4 pattern: n, 1, n + 1, 0 for n mod 4 = 0, 1, 2, 3. |

## Part 21: Greedy Algorithms

[Part README](21-greedy-algorithms/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Greedy Fundamentals](21-greedy-algorithms/01-greedy-fundamentals.md) | — | 📘 Theory | — | Greedy-choice property, exchange and stay-ahead proofs, when greedy fails (0/1 knapsack, coin systems), the sort-key decision table, interval patterns |
| 2 | [Assign Cookies](21-greedy-algorithms/02-assign-cookies.md) | Easy | Easy | O(n log n + m log m) | Sort both. |
| 3 | [Lemonade Change](21-greedy-algorithms/03-lemonade-change.md) | Easy | Easy | O(n) | Only $5 and $10 bills are useful as change. |
| 4 | [Fractional Knapsack](21-greedy-algorithms/04-fractional-knapsack.md) | Easy | Medium | O(n log n) | Sort by value per unit weight (`v / w`) descending and take as much as possible of the best ratio. |
| 5 | [Jump Game I](21-greedy-algorithms/05-jump-game-i.md) | Easy | Medium | O(n) | Track the farthest index reachable so far. |
| 6 | [Shortest Job First](21-greedy-algorithms/06-shortest-job-first.md) | Scheduling and intervals | Easy | O(n log n) | Running shorter jobs first minimises total waiting time — each job's burst is added to the waiting time of every job after it, so the smallest bursts should be counted most often. |
| 7 | [Job Sequencing Problem](21-greedy-algorithms/07-job-sequencing-problem.md) | Scheduling and intervals | Medium | O(n log n) | Take jobs by decreasing profit and schedule each in the **latest** free slot ≤ its deadline, keeping earlier slots open for jobs with tighter deadlines. |
| 8 | [N Meetings in One Room](21-greedy-algorithms/08-n-meetings-in-one-room.md) | Scheduling and intervals | Easy | O(n log n) | Activity selection: always pick the meeting that **ends earliest** among those compatible with what you've chosen — it leaves the most room for the rest. |
| 9 | [Non-overlapping Intervals](21-greedy-algorithms/09-non-overlapping-intervals.md) | Scheduling and intervals | Medium | O(n log n) | Removing the minimum = keeping the maximum non-overlapping set, which is activity selection: sort by end and keep greedily. |
| 10 | [Insert Interval](21-greedy-algorithms/10-insert-interval.md) | Scheduling and intervals | Medium | O(n) | The list splits into three runs: intervals entirely left of the new one, intervals that overlap it (merge into one by min start / max end), and intervals entirely right. |
| 11 | [Merge Intervals](21-greedy-algorithms/11-merge-intervals.md) | Scheduling and intervals | Medium | O(n log n) | After sorting by start, overlapping intervals are contiguous. |
| 12 | [Minimum Number of Platforms](21-greedy-algorithms/12-minimum-number-of-platforms.md) | Scheduling and intervals | Medium | O(n log n) | Answer = maximum number of trains present at the same instant. |
| 13 | [Valid Parenthesis String](21-greedy-algorithms/13-valid-parenthesis-string.md) | Hard | Medium | O(n) | Track the **range** `[lo, hi]` of possible open-bracket counts. |
| 14 | [Candy](21-greedy-algorithms/14-candy.md) | Hard | Hard | O(n) | Split the two-sided constraint into two one-sided ones. |
| 15 | [Jump Game II](21-greedy-algorithms/15-jump-game-ii.md) | Hard | Medium | O(n) | Implicit BFS: indices reachable in exactly k jumps form a contiguous window. |
| 16 | [Minimum coins (greedy, canonical denominations)](21-greedy-algorithms/16-minimum-coins-greedy-canonical-denominations.md) | Extra (A2Z sheet) | Easy | O(k + answer) | For **canonical** coin systems like real currencies, always taking the largest coin `≤` the remaining amount is optimal. |

## Part 22: Sliding Window / 2 Pointer

[Part README](22-sliding-window-and-2-pointer/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Sliding Window & Two Pointers: Patterns and Templates](22-sliding-window-and-2-pointer/01-sliding-window-theory.md) | — | 📘 Theory | — | Fixed vs variable windows, the monotone-validity condition, shrink-while vs non-shrinking windows, counting by right end, atMost(K) − atMost(K − 1), two pointers vs window, amor… |
| 2 | [Maximum Points You Can Obtain from Cards](22-sliding-window-and-2-pointer/02-maximum-points-you-can-obtain-from-cards.md) | Constant window | Medium | O(k) | Whatever you take, the cards you leave form one contiguous block of length `n − k`. |
| 3 | [Longest Substring Without Repeating Characters](22-sliding-window-and-2-pointer/03-longest-substring-without-repeating-characters.md) | Longest and smallest window | Medium | O(n) | Keep a window `[l, r]` with no repeats. |
| 4 | [Max Consecutive Ones III](22-sliding-window-and-2-pointer/04-max-consecutive-ones-iii.md) | Longest and smallest window | Medium | O(n) | Rephrase: longest window containing at most `k` zeros. |
| 5 | [Fruit Into Baskets](22-sliding-window-and-2-pointer/05-fruit-into-baskets.md) | Longest and smallest window | Medium | O(n) | This is "longest subarray with at most K distinct values" with K = 2. |
| 6 | [Longest Substring With At Most K Distinct Characters](22-sliding-window-and-2-pointer/06-longest-substring-with-at-most-k-distinct-characters.md) | Longest and smallest window | Medium | O(n) | Same template as Fruit Into Baskets with a general `k`: expand, count, and shrink while the map holds more than `k` keys. |
| 7 | [Longest Repeating Character Replacement](22-sliding-window-and-2-pointer/07-longest-repeating-character-replacement.md) | Longest and smallest window | Medium | O(n) | A window is fixable iff `len − maxFreq ≤ k`: keep the most common letter, change the rest. |
| 8 | [Minimum Window Substring](22-sliding-window-and-2-pointer/08-minimum-window-substring.md) | Longest and smallest window | Hard | O( | Expand right until the window covers `t`, then shrink left as long as it still covers, recording each covering window. |
| 9 | [Minimum Window Subsequence](22-sliding-window-and-2-pointer/09-minimum-window-subsequence.md) | Longest and smallest window | Hard | O(n·m) | Scan forward matching `s2` in order; when the last character matches at `r`, scan **backwards** from `r` matching `s2` in reverse to find the latest start `l`. |
| 10 | [Number of Substrings Containing All Three Characters](22-sliding-window-and-2-pointer/10-number-of-substrings-containing-all-three-characters.md) | Counting subarrays / substrings | Medium | O(n) | For each right end `r`, the substring `s[l..r]` contains all three letters iff `l ≤ min(last[a], last[b], last[c])`. |
| 11 | [Binary Subarrays With Sum](22-sliding-window-and-2-pointer/11-binary-subarrays-with-sum.md) | Counting subarrays / substrings | Medium | O(n) | "Exactly goal" isn't monotone for a window, but "at most goal" is. |
| 12 | [Count Number of Nice Subarrays](22-sliding-window-and-2-pointer/12-count-number-of-nice-subarrays.md) | Counting subarrays / substrings | Medium | O(n) | Map each number to `x % 2` and it's Binary Subarrays With Sum with `goal = k`. |
| 13 | [Subarrays with K Different Integers](22-sliding-window-and-2-pointer/13-subarrays-with-k-different-integers.md) | Counting subarrays / substrings | Hard | O(n) | Exactly-k distinct isn't monotone, but at-most-k is: if `[l, r]` has ≤ k distinct, so does every `[l', r]` with `l' ≥ l`. |

## Part 23: Stack / Queues

[Part README](23-stack-and-queues/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Stacks & Queues: Implementations, Monotonic Stacks and Design](23-stack-and-queues/01-stack-queue-implementation-theory.md) | — | 📘 Theory | — | LIFO/FIFO contracts, array/circular-buffer/linked-list implementations, stack↔queue simulation and amortised cost, deque, expression notation, monotonic stack/deque templates, c… |
| 2 | [Implement Stack using Arrays](23-stack-and-queues/02-implement-stack-using-arrays.md) | Implementation | Easy | O(1) amortised | One index `t` marks the top element. |
| 3 | [Implement Queue using Arrays](23-stack-and-queues/03-implement-queue-using-arrays.md) | Implementation | Easy | O(1) amortised | Use a **circular buffer**. |
| 4 | [Implement Stack using Queue](23-stack-and-queues/04-implement-stack-using-queue.md) | Implementation | Easy | push O(n), pop O(1) | Make **push** the expensive operation. |
| 5 | [Implement Queue using Stack](23-stack-and-queues/05-implement-queue-using-stack.md) | Implementation | Easy | O(1) amortised | Use two stacks: `in` for pushes and `out` for pops. |
| 6 | [Implement stack using Linkedlist](23-stack-and-queues/06-implement-stack-using-linkedlist.md) | Implementation | Easy | O(1) per op | The **head** of the list is the top. |
| 7 | [Implement queue using Linkedlist](23-stack-and-queues/07-implement-queue-using-linkedlist.md) | Implementation | Easy | O(1) per op | Keep **two** pointers: dequeue at `head`, enqueue after `tail`. |
| 8 | [Balanced Paranthesis](23-stack-and-queues/08-balanced-parenthesis.md) | Implementation | Easy | O(n) | The most recently opened bracket must close first, which is exactly LIFO. |
| 9 | [Infix to Postfix Conversion](23-stack-and-queues/09-infix-to-postfix-conversion.md) | Prefix, infix and postfix conversions | Medium | O(n) | This is **shunting-yard**. |
| 10 | [Infix to Prefix Conversion](23-stack-and-queues/10-infix-to-prefix-conversion.md) | Prefix, infix and postfix conversions | Medium | O(n) | Reverse the string and swap `(` with `)`. |
| 11 | [Prefix to Infix Conversion](23-stack-and-queues/11-prefix-to-infix-conversion.md) | Prefix, infix and postfix conversions | Medium | O(n²) strings · O(n) with a tree | Scan **right to left**. |
| 12 | [Prefix to Postfix Conversion](23-stack-and-queues/12-prefix-to-postfix-conversion.md) | Prefix, infix and postfix conversions | Medium | O(n²) strings · O(n) with a tree | Scan **right to left** with a stack of finished sub-expressions. |
| 13 | [Postfix to Infix Conversion](23-stack-and-queues/13-postfix-to-infix-conversion.md) | Prefix, infix and postfix conversions | Medium | O(n²) strings · O(n) with a tree | Scan **left to right**. |
| 14 | [Postfix to Prefix Conversion](23-stack-and-queues/14-postfix-to-prefix-conversion.md) | Prefix, infix and postfix conversions | Medium | O(n²) strings · O(n) with a tree | Scan **left to right**. |
| 15 | [Next Greater Element](23-stack-and-queues/15-next-greater-element.md) | Monotonic stack | Medium | O(n) | Scan **right to left** and keep a stack that **decreases from bottom to top**. |
| 16 | [Next Greater Element - 2](23-stack-and-queues/16-next-greater-element-ii.md) | Monotonic stack | Medium | O(n) | Pretend the array is written twice: scan `i` from `2n−1` down to 0 using `a[i % n]`. |
| 17 | [Asteroid Collision](23-stack-and-queues/17-asteroid-collision.md) | Monotonic stack | Medium | O(n) | A collision happens only when a **left-mover meets a right-mover that came before it**. |
| 18 | [Sum of Subarray Minimums](23-stack-and-queues/18-sum-of-subarray-minimums.md) | Monotonic stack | Medium | O(n) | Flip it around: count how many subarrays have `arr[i]` as their minimum. |
| 19 | [Sum of Subarray Ranges](23-stack-and-queues/19-sum-of-subarray-ranges.md) | Monotonic stack | Medium | O(n) | Linearity: Σ(max − min) = Σ max − Σ min. |
| 20 | [Remove K Digits](23-stack-and-queues/20-remove-k-digits.md) | Monotonic stack | Medium | O(n) | Greedy from the left: a digit followed by a smaller digit should be removed, because lowering an earlier position beats anything later. |
| 21 | [Next Smaller Element](23-stack-and-queues/21-next-smaller-element.md) | Monotonic stack | Medium | O(n) | Mirror of NGE: keep the stack **increasing** from bottom to top. |
| 22 | [Implement Min Stack](23-stack-and-queues/22-implement-min-stack.md) | FAQs | Medium | O(1) all ops | The minimum only changes on push or pop, so **remember it per level**. |
| 23 | [Sliding Window Maximum](23-stack-and-queues/23-sliding-window-maximum.md) | FAQs | Hard | O(n) | Keep a **deque of indices whose values are decreasing**. |
| 24 | [Trapping Rainwater](23-stack-and-queues/24-trapping-rainwater.md) | FAQs | Hard | O(n) | Water above bar `i` = `min(maxLeft[i], maxRight[i]) − h[i]`. |
| 25 | [Largest rectangle in a histogram](23-stack-and-queues/25-largest-rectangle-in-a-histogram.md) | FAQs | Hard | O(n) | The best rectangle has some bar `i` as its **shortest** bar, and it stretches from just after the previous smaller bar to just before the next smaller one: area `h[i]·(nse − pse… |
| 26 | [Maximum Rectangles](23-stack-and-queues/26-maximal-rectangle.md) | FAQs | Hard | O(R·C) | Treat each row as the **floor of a histogram**: `heights[j]` = number of consecutive 1s ending at this row in column `j` (reset to 0 on a 0). |
| 27 | [Stock span problem](23-stack-and-queues/27-stock-span-problem.md) | FAQs | Medium | O(1) amortised | Span = distance to the **previous greater** price. |
| 28 | [The Celebrity Problem](23-stack-and-queues/28-celebrity-problem.md) | FAQs | Medium | O(n) | One query `knows(a, b)` **eliminates one person**: if `a` knows `b`, `a` isn't the celebrity; otherwise `b` isn't. |
| 29 | [LRU Cache](23-stack-and-queues/29-lru-cache.md) | FAQs | Hard | O(1) per op | Recency order needs O(1) **move-to-front** and O(1) **remove-from-back**: a **doubly linked list**. |
| 30 | [LFU Cache](23-stack-and-queues/30-lfu-cache.md) | FAQs | Hard | O(1) per op | Group keys into **buckets by frequency**, each bucket an LRU list. |
| 31 | [Number of Greater Elements to the Right](23-stack-and-queues/31-count-greater-to-the-right.md) | FAQs | Medium | O(n log n + q) | Unlike NGE, a monotonic stack doesn't help here: you need a **count**, not the nearest one. |

## Part 24: Binary Trees

[Part README](24-binary-trees/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Binary Trees: Terminology, Representation and Traversal Templates](24-binary-trees/01-binary-tree-theory.md) | — | 📘 Theory | — | Node/edge/height/depth vocabulary, tree types (full, complete, perfect, balanced, degenerate), array vs pointer representation, DFS/BFS traversal templates, the post-order 'retu… |
| 2 | [Inorder Traversal](24-binary-trees/02-inorder-traversal.md) | Traversals | Easy | O(n) | Recursively it's three lines. |
| 3 | [Preorder Traversal](24-binary-trees/03-preorder-traversal.md) | Traversals | Easy | O(n) | Iterative preorder is the simplest stack traversal. |
| 4 | [Postorder Traversal](24-binary-trees/04-postorder-traversal.md) | Traversals | Easy | O(n) | The hard iterative traversal: a node may be visited only after **both** subtrees are done. |
| 5 | [Level Order Traversal](24-binary-trees/05-level-order-traversal.md) | Traversals | Medium | O(n) | BFS with a queue. |
| 6 | [Pre, Post, Inorder in one traversal](24-binary-trees/06-all-traversals-in-one-pass.md) | Traversals | Medium | O(n) | Push `(node, state)`. |
| 7 | [Maximum Depth in BT](24-binary-trees/07-maximum-depth.md) | Medium problems | Easy | O(n) | `depth(n) = 1 + max(depth(left), depth(right))`, with `depth(null) = 0`. |
| 8 | [Check if two trees are identical or not](24-binary-trees/08-same-tree.md) | Medium problems | Easy | O(min(n, m)) | Both null → true. |
| 9 | [Check for balanced binary tree](24-binary-trees/09-balanced-binary-tree.md) | Medium problems | Easy | O(n) | Compute height bottom-up and use **−1 as an 'unbalanced' sentinel**. |
| 10 | [Diameter of Binary Tree](24-binary-trees/10-diameter-of-binary-tree.md) | Medium problems | Easy | O(n) | Every path has a single highest node. |
| 11 | [Maximum path sum](24-binary-trees/11-binary-tree-maximum-path-sum.md) | Medium problems | Hard | O(n) | Same skeleton as diameter. |
| 12 | [Check for symmetrical BTs](24-binary-trees/12-symmetric-tree.md) | Medium problems | Easy | O(n) | Compare the left and right subtrees as mirrors. |
| 13 | [Children Sum Property in Binary Tree](24-binary-trees/13-children-sum-property.md) | Medium problems | Medium | O(n) | You can't decrease, so fix the deficit **on the way down**. |
| 14 | [Zig Zag Traversal Of Binary Tree](24-binary-trees/14-zigzag-level-order.md) | FAQs | Medium | O(n) | Run the normal level-size BFS. |
| 15 | [Boundary Traversal of a Binary Tree](24-binary-trees/15-boundary-traversal.md) | FAQs | Medium | O(n) | Split it into three independent walks and stitch them together. |
| 16 | [Vertical Order Traversal](24-binary-trees/16-vertical-order-traversal.md) | FAQs | Hard | O(n log n) | Label each node with `(col, row)` during any traversal, then **sort by (col, row, val)** and group by col. |
| 17 | [Top View of Binary Tree](24-binary-trees/17-top-view.md) | FAQs | Medium | O(n) | BFS with horizontal distance (HD). |
| 18 | [Bottom view of Binary Tree](24-binary-trees/18-bottom-view.md) | FAQs | Medium | O(n) | It's the top view with the update rule flipped: **overwrite on every visit**. |
| 19 | [Right/Left View of Binary Tree](24-binary-trees/19-right-left-view.md) | FAQs | Medium | O(n) | DFS with depth, visiting the preferred side first. |
| 20 | [Print root to node path in BT](24-binary-trees/20-root-to-leaf-paths.md) | FAQs | Medium | O(n·h) (copies at leaves) | DFS with a shared `path` list: **push on entry, pop on exit** (backtracking). |
| 21 | [LCA in BT](24-binary-trees/21-lowest-common-ancestor.md) | FAQs | Medium | O(n) | Ask each subtree: 'do you contain p or q?' Return the node itself if it **is** p or q. |
| 22 | [Maximum width of a Binary Tree](24-binary-trees/22-maximum-width.md) | FAQs | Medium | O(n) | Number nodes as in a heap: root `i`, children `2i+1`, `2i+2`. |
| 23 | [Print all the Nodes at a distance of K in a BT](24-binary-trees/23-all-nodes-distance-k.md) | FAQs | Medium | O(n) | A tree is an undirected graph whose edges to parents are missing. |
| 24 | [Minimum time taken to burn the BT from a given Node](24-binary-trees/24-burn-binary-tree.md) | FAQs | Hard | O(n) | The answer is the **eccentricity** of the start node, its farthest distance in the tree. |
| 25 | [Count total Nodes in a COMPLETE BT](24-binary-trees/25-count-complete-tree-nodes.md) | FAQs | Medium | O(log² n) | Measure the leftmost and rightmost depths. |
| 26 | [Flatten Binary Tree to LinkedList](24-binary-trees/26-flatten-binary-tree.md) | FAQs | Medium | O(n) | O(1) space, Morris-style. |
| 27 | [Requirements needed to construct a unique BT](24-binary-trees/27-unique-bt-requirements.md) | Construction problems | Easy | O(1) | Preorder and postorder each tell you **where the root is** (first or last element) but not where the left subtree ends. |
| 28 | [Construct a BT from Preorder and Inorder](24-binary-trees/28-build-from-preorder-inorder.md) | Construction problems | Medium | O(n) | `pre[0]` is the root. |
| 29 | [Construct a BT from Postorder and Inorder](24-binary-trees/29-build-from-postorder-inorder.md) | Construction problems | Medium | O(n) | It mirrors the preorder version: the root is `post[pR]`. |
| 30 | [Serialize and De-serialize BT](24-binary-trees/30-serialize-deserialize.md) | Construction problems | Hard | O(n) | A traversal **with explicit null markers** is self-delimiting, so one sequence is enough and you don't need inorder. |
| 31 | [Morris Inorder Traversal](24-binary-trees/31-morris-inorder.md) | Traversal in constant space (Morris) | Medium | O(n) | Use the null `right` pointer of each node's **inorder predecessor** (the rightmost node of its left subtree) as a temporary **thread back to the node**. |
| 32 | [Morris Preorder Traversal](24-binary-trees/32-morris-preorder.md) | Traversal in constant space (Morris) | Medium | O(n) | It's identical to Morris inorder except for **when you output**. |

## Part 25: Binary Search Trees

[Part README](25-binary-search-trees/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Binary Search Trees: Invariant, Walks, Insert/Delete and Inorder](25-binary-search-trees/01-bst-theory.md) | — | 📘 Theory | — | The BST invariant (whole subtrees, not just children), why inorder is sorted, O(h) vs O(log n), the walk template with candidate tracking (floor/ceil/successor), insert and the… |
| 2 | [Search in BST](25-binary-search-trees/02-search-in-bst.md) | Theory and basics | Easy | O(h) | The BST invariant tells you which side the target must be on, so you never explore both children. |
| 3 | [Floor and Ceil in a BST](25-binary-search-trees/03-floor-and-ceil-in-a-bst.md) | Theory and basics | Medium | O(h) | Walk as if searching for `key`. |
| 4 | [Minimum and Maximum in BST](25-binary-search-trees/04-minimum-and-maximum-in-bst.md) | Theory and basics | Easy | O(h) | The minimum is the **leftmost** node and the maximum is the **rightmost** node. |
| 5 | [Insert a given node in BST](25-binary-search-trees/05-insert-into-bst.md) | Medium | Medium | O(h) | Search for `val`. |
| 6 | [Delete a node in BST](25-binary-search-trees/06-delete-node-in-bst.md) | Medium | Medium | O(h) | Leaves and one-child nodes are easy: replace the node with its only child (or null). |
| 7 | [Kth Smallest and Largest element in BST](25-binary-search-trees/07-kth-smallest-largest-in-bst.md) | Medium | Medium | O(h + k) | Inorder visits a BST in ascending order, so the kth node popped is the kth smallest. |
| 8 | [Check if a tree is a BST or not](25-binary-search-trees/08-validate-bst.md) | Medium | Medium | O(n) | Comparing a node only with its children is the classic trap. |
| 9 | [LCA in BST](25-binary-search-trees/09-lca-in-bst.md) | Medium | Medium | O(h) | While both values are smaller than the current node, the LCA is to the left; while both are larger, it's to the right. |
| 10 | [Construct a BST from a preorder traversal](25-binary-search-trees/10-bst-from-preorder.md) | Medium | Medium | O(n) | For a BST, preorder alone is enough because the ordering is the missing inorder. |
| 11 | [Inorder successor and predecessor in BST](25-binary-search-trees/11-inorder-successor-predecessor.md) | Medium | Medium | O(h) | This is floor/ceil with **strict** inequalities. |
| 12 | [BST iterator](25-binary-search-trees/12-bst-iterator.md) | FAQs | Medium | O(1) amortised | Turn iterative inorder into a resumable object. |
| 13 | [Two sum in BST](25-binary-search-trees/13-two-sum-in-bst.md) | FAQs | Medium | O(n) | The inorder sequence is sorted, so this is two-sum on a sorted array: a left pointer moving up and a right pointer moving down. |
| 14 | [Correct BST with two nodes swapped](25-binary-search-trees/14-recover-bst.md) | FAQs | Hard | O(n) | In the inorder sequence, a swap produces either **one** descent (adjacent elements swapped) or **two** descents (distant elements). |
| 15 | [Largest BST in Binary Tree](25-binary-search-trees/15-largest-bst-subtree.md) | FAQs | Hard | O(n) | Post-order information passing. |

## Part 26: Heaps

[Part README](26-heaps/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Heaps: Array Layout, Sift Operations, Build-Heap and Priority Queues](26-heaps/01-heap-theory.md) | — | 📘 Theory | — | Complete-tree array layout and index formulas, the heap property, sift up / sift down, push/pop/top, O(n) bottom-up build with the height-sum proof, heap sort, library priority… |
| 2 | [Heapify Algorithm](26-heaps/02-heapify-algorithm.md) | Theory and implementation | Medium | O(log n) | A single changed key is wrong in only one direction. |
| 3 | [Build heap from a given Array](26-heaps/03-build-heap-from-a-given-array.md) | Theory and implementation | Medium | O(n) | Leaves (the last ⌈n/2⌉ indices) are already one-node heaps. |
| 4 | [Implement Min Heap](26-heaps/04-implement-min-heap.md) | Theory and implementation | Medium | push/pop O(log n), top/size O(1) | Complete-tree shape lives in an array: `push` = append at the end + sift up, `pop` = move the last element to the root + sift down. |
| 5 | [Implement Max Heap](26-heaps/05-implement-max-heap.md) | Theory and implementation | Medium | push/pop O(log n) | Identical to the min-heap with every key comparison flipped. |
| 6 | [Check if an array represents a min heap](26-heaps/06-check-if-an-array-represents-a-min-heap.md) | Theory and implementation | Easy | O(n) | The heap property is local: it's enough that every **parent ≤ child** edge holds. |
| 7 | [Convert Min Heap to Max Heap](26-heaps/07-convert-min-heap-to-max-heap.md) | Theory and implementation | Medium | O(n) | The min-heap ordering is no help: a max-heap needs the opposite partial order. |
| 8 | [Heap Sort](26-heaps/08-heap-sort.md) | Theory and implementation | Medium | O(n log n) | Build a **max**-heap in place (O(n)). |
| 9 | [K-th Largest element in an array](26-heaps/09-k-th-largest-element-in-an-array.md) | Theory and implementation | Medium | O(n) expected | Keep a **min-heap of size k**: it holds the k largest seen so far, and its root is the k-th largest. |
| 10 | [Kth largest element in a stream of running integers](26-heaps/10-kth-largest-in-a-stream.md) | FAQs | Easy | add O(log k) | A **min-heap holding exactly the k largest** values so far. |
| 11 | [Sort K sorted array](26-heaps/11-sort-k-sorted-array.md) | FAQs | Medium | O(n log k) | The element that belongs at index `i` must be among `nums[i … i+k]`. |
| 12 | [Merge K sorted Lists](26-heaps/12-merge-k-sorted-lists.md) | FAQs | Hard | O(N log k) | The next output node is the smallest of the k current heads. |
| 13 | [Replace elements by its rank in the array](26-heaps/13-replace-elements-by-rank.md) | FAQs | Easy | O(n log n) | Rank = 1 + number of **distinct** values smaller than it. |
| 14 | [Task Scheduler](26-heaps/14-task-scheduler.md) | FAQs | Medium | O(T) | Only the **most frequent** task forces idling. |
| 15 | [Hand of Straights](26-heaps/15-hand-of-straights.md) | FAQs | Medium | O(n log n) | The **smallest remaining card** can only be the start of a group (nothing smaller is left to precede it). |
| 16 | [Design twitter](26-heaps/16-design-twitter.md) | FAQs | Medium | feed O(f + 10 log f) | Each user's tweets are already sorted by time (append-only). |
| 17 | [Minimum cost to connect sticks](26-heaps/17-minimum-cost-to-connect-sticks.md) | FAQs | Medium | O(n log n) | Every stick's length is paid once per join it takes part in, i.e. |
| 18 | [Maximum Sum Combination](26-heaps/18-maximum-sum-combination.md) | FAQs | Medium | O(n log n + K log K) | Sort both descending. |
| 19 | [Find Median from Data Stream](26-heaps/19-find-median-from-data-stream.md) | FAQs | Hard | add O(log n), median O(1) | Split the numbers into a **low half (max-heap)** and a **high half (min-heap)**, with every low ≤ every high and sizes equal or low larger by one. |
| 20 | [Top K Frequent Elements](26-heaps/20-top-k-frequent-elements.md) | FAQs | Medium | O(n) | Count, then select. |

## Part 27: Graphs

[Part README](27-graphs/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Graphs: Representations, BFS/DFS, Cycles, Topological Order and Shortest Paths](27-graphs/01-graph-theory.md) | — | 📘 Theory | — | Vocabulary, adjacency matrix vs list vs edge list, grid graphs, BFS and DFS with their invariants, connected components, cycle detection in undirected and directed graphs, bipar… |
| 2 | [Minimum Spanning Trees and Disjoint Set Union](27-graphs/02-mst-and-dsu-theory.md) | — | 📘 Theory | — | Spanning trees, the cut and cycle properties, Prim and Kruskal with proofs and complexity, union-find with path compression and union by rank/size, the inverse-Ackermann bound,… |
| 3 | [Traversal Techniques](27-graphs/03-traversal-techniques-bfs-dfs.md) | Theory and traversals | Easy | O(V + E) | Both traversals are 'pop a node, expand its unvisited neighbours'. |
| 4 | [Connected Components](27-graphs/04-connected-components.md) | Theory and traversals | Easy | O(V + E) | Every traversal started from an unvisited node visits exactly one whole component. |
| 5 | [Number of provinces](27-graphs/05-number-of-provinces.md) | Traversal problems | Medium | O(n²) | A province is a connected component. |
| 6 | [Number of islands](27-graphs/06-number-of-islands.md) | Traversal problems | Medium | O(m·n) | A grid is an implicit graph: cells are nodes and the 4 neighbours are edges. |
| 7 | [Flood fill algorithm](27-graphs/07-flood-fill.md) | Traversal problems | Easy | O(m·n) | DFS from `(sr, sc)` over neighbours that still have the **original** colour, repainting as you go. |
| 8 | [Number of enclaves](27-graphs/08-number-of-enclaves.md) | Traversal problems | Medium | O(m·n) | Turn the question around. |
| 9 | [Rotten Oranges](27-graphs/09-rotten-oranges.md) | Traversal problems | Medium | O(m·n) | All rotten oranges spread **simultaneously**, which is exactly multi-source BFS: put every rotten orange in the queue at time 0. |
| 10 | [Distance of nearest cell having one](27-graphs/10-distance-of-nearest-cell-having-1.md) | Traversal problems | Medium | O(m·n) | Run one BFS backwards from the targets instead of a BFS forwards from every cell. |
| 11 | [Surrounded Regions](27-graphs/11-surrounded-regions.md) | Traversal problems | Medium | O(m·n) | A region survives exactly when it touches the border. |
| 12 | [Number of distinct islands](27-graphs/12-number-of-distinct-islands.md) | Traversal problems | Medium | O(m·n) | Translate each island so its **first-visited cell** sits at the origin. |
| 13 | [Detect a cycle in an undirected graph](27-graphs/13-cycle-in-undirected-graph.md) | Cycles | Medium | O(V + E) | During a traversal, every edge either reaches a new node (a tree edge) or points to an already-visited node. |
| 14 | [Bipartite graph](27-graphs/14-bipartite-graph.md) | Cycles | Medium | O(V + E) | Colour greedily. |
| 15 | [Topological sort or Kahn's algorithm](27-graphs/15-topological-sort-dfs-and-kahn.md) | Hard problems (topological sort and BFS) | Medium | O(V + E) | Two equivalent views. |
| 16 | [Detect a cycle in a directed graph](27-graphs/16-cycle-in-directed-graph.md) | Hard problems (topological sort and BFS) | Medium | O(V + E) | Unlike the undirected case, reaching a visited node is not enough: in the diamond `0→1→3, 0→2→3`, node 3 is reached twice without a cycle. |
| 17 | [Find eventual safe states](27-graphs/17-find-eventual-safe-states.md) | Hard problems (topological sort and BFS) | Medium | O(V + E) | A node is unsafe exactly when some path from it can reach a cycle. |
| 18 | [Course Schedule I](27-graphs/18-course-schedule-i.md) | Hard problems (topological sort and BFS) | Medium | O(V + E) | Courses are nodes and the edge `b → a` means `b` comes before `a`. |
| 19 | [Course Schedule II](27-graphs/19-course-schedule-ii.md) | Hard problems (topological sort and BFS) | Medium | O(V + E) | Same graph as Course Schedule I, but now output Kahn's processing order. |
| 20 | [Alien dictionary](27-graphs/20-alien-dictionary.md) | Hard problems (topological sort and BFS) | Hard | O(N·L + k) | Compare **adjacent** words only. |
| 21 | [Shortest path in DAG](27-graphs/21-shortest-path-in-dag.md) | Hard problems (topological sort and BFS) | Medium | O(V + E) | In topological order, every edge into `v` comes from a node processed earlier. |
| 22 | [Shortest path in undirected graph with unit weights](27-graphs/22-shortest-path-unit-weights.md) | Shortest path algorithms | Medium | O(V + E) | With every edge weighing 1, BFS **is** Dijkstra. |
| 23 | [Word ladder I](27-graphs/23-word-ladder-i.md) | Shortest path algorithms | Hard | O(N·L²·26) | Words are nodes, and an edge joins two words that differ in one letter, so this is unweighted shortest path, i.e. |
| 24 | [Word ladder II](27-graphs/24-word-ladder-ii.md) | Shortest path algorithms | Hard | O(N·L²·26 + paths·len) | Do it in two phases. |
| 25 | [Dijkstra's algorithm](27-graphs/25-dijkstra.md) | Shortest path algorithms | Medium | O((V + E) log V) | Dijkstra is greedy. |
| 26 | [Print shortest path](27-graphs/26-print-shortest-path-dijkstra.md) | Shortest path algorithms | Medium | O((n + m) log n) | Run Dijkstra and, every time `dist[v]` improves via `u`, set `parent[v] = u`. |
| 27 | [Shortest distance in a binary maze](27-graphs/27-shortest-distance-binary-maze.md) | Shortest path algorithms | Medium | O(nm) | Every move costs 1, so BFS from the source gives final distances at discovery. |
| 28 | [Path with minimum effort](27-graphs/28-path-with-minimum-effort.md) | Shortest path algorithms | Medium | h[v] − h[u] | Path cost here is a **bottleneck**, `max` of the edge weights, not a sum. |
| 29 | [Cheapest flights within K stops](27-graphs/29-cheapest-flights-within-k-stops.md) | Shortest path algorithms | Medium | O(k·E) | The stop limit breaks plain Dijkstra. |
| 30 | [Minimum multiplications to reach end](27-graphs/30-minimum-multiplications-to-reach-end.md) | Shortest path algorithms | Medium | O(10⁵· | It is a graph in disguise. |
| 31 | [Number of ways to arrive at destination](27-graphs/31-number-of-ways-to-arrive-at-destination.md) | Shortest path algorithms | Medium | O(E log V) | Run Dijkstra and carry `ways[v]` with it. |
| 32 | [Bellman-Ford algorithm](27-graphs/32-bellman-ford.md) | Shortest path algorithms | Medium | O(V·E) | A shortest path without cycles has at most `V − 1` edges. |
| 33 | [Floyd Warshall algorithm](27-graphs/33-floyd-warshall.md) | Shortest path algorithms | Medium | O(n³) | DP over allowed intermediate nodes. |
| 34 | [Find the city with the smallest number of neighbors at a threshold distance](27-graphs/34-city-with-smallest-neighbors-at-threshold.md) | Shortest path algorithms | Medium | O(n³) | It needs every city's distance to every other city, i.e. |
| 35 | [Network delay time](27-graphs/35-network-delay-time.md) | Shortest path algorithms | Medium | O(E log n) | Each node receives the signal at its shortest-path distance from `k`. |
| 36 | [Swim in rising water](27-graphs/36-swim-in-rising-water.md) | Shortest path algorithms | Hard | O(n² log n) | A path is usable at time `t` iff its highest cell is ≤ `t`. |
| 37 | [Disjoint Set (Union-Find)](27-graphs/37-disjoint-set.md) | Minimum spanning tree | Medium | O(α(n)) amortised | Represent each set as a tree whose root is the set's name. |
| 38 | [Find the MST weight](27-graphs/38-find-the-mst-weight.md) | Minimum spanning tree | Medium | O(E log E) | **Cut property:** for any split of the vertices into two sides, the lightest edge crossing the split belongs to some MST. |
| 39 | [Number of operations to make network connected](27-graphs/39-number-of-operations-to-make-network-connected.md) | Hard problems II (disjoint set) | Medium | O(n + E·α(n)) | Joining `c` components needs exactly `c − 1` cables. |
| 40 | [Accounts merge](27-graphs/40-accounts-merge.md) | Hard problems II (disjoint set) | Medium | O(N log N) | Accounts are nodes; a shared email is an edge. |
| 41 | [Number of islands II](27-graphs/41-number-of-islands-ii.md) | Hard problems II (disjoint set) | Hard | O(n·m + k·α) | Adding land is a union-only process, so the count can be maintained online: a new cell adds one island, and each union with a **different** neighbouring island subtracts one. |
| 42 | [Making a large island](27-graphs/42-making-a-large-island.md) | Hard problems II (disjoint set) | Hard | O(n²·α) | Label every island once (DSU or DFS) and store its size. |
| 43 | [Most stones removed with same row or column](27-graphs/43-most-stones-removed-with-same-row-or-column.md) | Hard problems II (disjoint set) | Medium | O(n·α) | Stones sharing a row or column form connected components, and every component can be peeled down to exactly **one** stone (remove leaves of a spanning tree first). |
| 44 | [Kosaraju's algorithm](27-graphs/44-kosarajus-algorithm.md) | Additional algorithms | Hard | O(V + E) | Two DFS passes. |
| 45 | [Bridges in graph](27-graphs/45-bridges-in-graph.md) | Additional algorithms | Hard | O(V + E) | DFS with discovery time `tin[u]` and `low[u]` = earliest `tin` reachable from u's subtree using **one back edge**. |
| 46 | [Articulation point in graph](27-graphs/46-articulation-point-in-graph.md) | Additional algorithms | Hard | O(V + E) | Same `tin`/`low` DFS as bridges, two changes. |

## Part 28: Dynamic Programming

[Part README](28-dynamic-programming/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Dynamic Programming: From Recursion to Tabulation](28-dynamic-programming/01-dp-theory.md) | — | 📘 Theory | — | Overlapping subproblems and optimal substructure, the 4-stage pipeline (recurrence → memo → tabulation → space optimisation), how to choose a state, base cases and sentinels, lo… |
| 2 | [Climbing stairs](28-dynamic-programming/02-climbing-stairs.md) | 1D DP | Easy | O(n) | The last move was either a 1-step from `n−1` or a 2-step from `n−2`, so `ways(n) = ways(n−1) + ways(n−2)`, which is Fibonacci. |
| 3 | [Frog Jump](28-dynamic-programming/03-frog-jump.md) | 1D DP | Easy | h[i]−h[i−1] | Stone `i` is reached from `i−1` or `i−2`, so `dp[i] = min(dp[i−1] + |
| 4 | [Frog jump with K distances](28-dynamic-programming/04-frog-jump-with-k-distances.md) | 1D DP | Medium | h[i] − h[i−j] | Generalise the last-move recurrence: `dp[i] = min_{j=1..k, i−j≥0} dp[i−j] + |
| 5 | [Maximum sum of non adjacent elements](28-dynamic-programming/05-maximum-sum-of-non-adjacent-elements.md) | 1D DP | Medium | O(n) | At index `i` you either **pick** it (then `i−1` is forbidden, so add `dp[i−2]`) or **skip** it (keep `dp[i−1]`): `dp[i] = max(a[i] + dp[i−2], dp[i−1])`. |
| 6 | [House robber](28-dynamic-programming/06-house-robber.md) | 1D DP | Medium | O(n) | The circle only adds one constraint: the first and last house are adjacent. |
| 7 | [Ninja's training](28-dynamic-programming/07-ninjas-training.md) | 2D DP | Medium | O(n·9) | Today's choice depends on yesterday's, so the state needs that too: `dp[day][last]` = best points for days `0..day` when activity `last` is forbidden on `day`. |
| 8 | [Grid unique paths](28-dynamic-programming/08-grid-unique-paths.md) | DP on grids | Medium | O(m·n) | A cell is entered from above or from the left: `dp[i][j] = dp[i−1][j] + dp[i][j−1]`, with the first row and column all 1. |
| 9 | [Unique paths II](28-dynamic-programming/09-unique-paths-ii.md) | DP on grids | Medium | O(m·n) | Same recurrence as Unique Paths, but an obstacle cell has 0 paths. |
| 10 | [Minimum Falling Path Sum](28-dynamic-programming/10-minimum-falling-path-sum.md) | DP on grids | Medium | O(n²) | This is a grid DP with a **variable start and end**: `dp[i][j] = a[i][j] + min(dp[i−1][j−1], dp[i−1][j], dp[i−1][j+1])`. |
| 11 | [Triangle](28-dynamic-programming/11-triangle.md) | DP on grids | Medium | O(n²) | Going **bottom-up** removes the variable-end problem: start with the last row as `dp`, then `dp[j] = t[i][j] + min(dp[j], dp[j+1])` moving upward. |
| 12 | [Cherry pickup II](28-dynamic-programming/12-cherry-pickup-ii.md) | DP on grids | Hard | O(R·C²·9) | Both robots are always on the **same row**, so the state is `(row, c1, c2)`, which is 3D rather than 4D. |
| 13 | [Count Square Submatrices with All Ones](28-dynamic-programming/13-count-square-submatrices-with-all-ones.md) | DP on grids | Medium | O(m·n) | Let `dp[i][j]` = side of the largest all-ones square with **bottom-right corner** `(i, j)`. |
| 14 | [Best time to buy and sell stock](28-dynamic-programming/14-best-time-to-buy-and-sell-stock.md) | DP on stocks | Easy | O(n) | If you sell on day `i`, the best buy is the minimum price before `i`. |
| 15 | [Best time to buy and sell stock II](28-dynamic-programming/15-best-time-to-buy-and-sell-stock-ii.md) | DP on stocks | Medium | O(n) | State `(i, holding)`. |
| 16 | [Best time to buy and sell stock III](28-dynamic-programming/16-best-time-to-buy-and-sell-stock-iii.md) | DP on stocks | Hard | O(n) | Add a transaction counter to the state: `(i, canBuy, capLeft)`. |
| 17 | [Best time to buy and sell stock IV](28-dynamic-programming/17-best-time-to-buy-and-sell-stock-iv.md) | DP on stocks | Hard | O(n·k) | Generalise Stock III: `buy[j] = max(buy[j], sell[j−1] − p)`, `sell[j] = max(sell[j], buy[j] + p)` for `j = 1..k`. |
| 18 | [Best time to buy and sell stock with transaction fees](28-dynamic-programming/18-best-time-to-buy-and-sell-stock-with-transaction-fee.md) | DP on stocks | Medium | O(n) | This is the Stock II state machine with `−fee` on the sell transition (or on buy, not both). |
| 19 | [Best time to buy and sell stock with cooldown](28-dynamic-programming/19-best-time-to-buy-and-sell-stock-with-cooldown.md) | DP on stocks | Medium | O(n) | In the backward state machine, selling on day `i` jumps to `f(i + 2, canBuy)` instead of `f(i + 1, …)`. |
| 20 | [Subset sum equals to target](28-dynamic-programming/20-subset-sum-equals-to-target.md) | DP on subsequences | Medium | O(n·k) | `f(i, t)` = can `a[0..i]` make `t`? |
| 21 | [Partition equal subset sum](28-dynamic-programming/21-partition-equal-subset-sum.md) | DP on subsequences | Medium | O(n·S) | Equal halves means each sums to `total/2`. |
| 22 | [Partition a set into two subsets with minimum absolute sum difference](28-dynamic-programming/22-partition-min-absolute-sum-difference.md) | DP on subsequences | Hard | S − 2·s1 | If one group sums to `s1`, the other is `S − s1`, and the difference is ` |
| 23 | [Count subsets with sum K](28-dynamic-programming/23-count-subsets-with-sum-k.md) | DP on subsequences | Medium | O(n·k) | Turn the boolean OR into a sum: `dp[i][t] = dp[i−1][t] + dp[i−1][t − a[i]]`. |
| 24 | [Count partitions with given difference](28-dynamic-programming/24-count-partitions-with-given-difference.md) | DP on subsequences | Medium | O(n·S) | `s1 − s2 = d` and `s1 + s2 = S` give `s1 = (S + d) / 2`. |
| 25 | [0 and 1 Knapsack](28-dynamic-programming/25-0-1-knapsack.md) | DP on subsequences | Medium | O(n·W) | `dp[i][w] = max(dp[i−1][w], val[i] + dp[i−1][w − wt[i]])`. |
| 26 | [Minimum coins](28-dynamic-programming/26-minimum-coins.md) | DP on subsequences | Medium | O(n·amount) | Unbounded choice: when you **take** coin `i` you stay at `i`. |
| 27 | [Target sum](28-dynamic-programming/27-target-sum.md) | DP on subsequences | Medium | O(n·S) | Let `P` be the `+` set and `N` the `−` set. |
| 28 | [Coin change II](28-dynamic-programming/28-coin-change-ii.md) | DP on subsequences | Medium | O(n·amount) | Loop **coins outside, amount inside (ascending)**: `dp[t] += dp[t − c]`. |
| 29 | [Unbounded knapsack](28-dynamic-programming/29-unbounded-knapsack.md) | DP on subsequences | Medium | O(n·W) | Identical to 0/1 knapsack except taking stays at `i`: `dp[i][w] = max(dp[i−1][w], v_i + dp[i][w − wt_i])`. |
| 30 | [Rod cutting problem](28-dynamic-programming/30-rod-cutting-problem.md) | DP on subsequences | Medium | O(n²) | Every piece length `1..n` is an item with weight `L` and value `price[L−1]`, usable any number of times, with capacity `n`. |
| 31 | [Longest increasing subsequence](28-dynamic-programming/31-longest-increasing-subsequence.md) | Longest increasing subsequence | Medium | O(n log n) | O(n²): `dp[i]` = LIS ending at `i` = `1 + max dp[j]` over `j < i, a[j] < a[i]`. |
| 32 | [Print longest increasing subsequence](28-dynamic-programming/32-print-longest-increasing-subsequence.md) | Longest increasing subsequence | Medium | O(n²) | Run the O(n²) `dp[i]` = LIS ending at `i` and also record `parent[i]`, the `j` that gave the best extension. |
| 33 | [Largest divisible subset](28-dynamic-programming/33-largest-divisible-subset.md) | Longest increasing subsequence | Medium | x₂ | Sort ascending. |
| 34 | [Longest string chain](28-dynamic-programming/34-longest-string-chain.md) | Longest increasing subsequence | Medium | O(n·L²) | Sort by length, then LIS where "`a` can precede `b`" means `len(b) = len(a) + 1` and `a` is `b` with one character removed (a two-pointer check). |
| 35 | [Longest bitonic subsequence](28-dynamic-programming/35-longest-bitonic-subsequence.md) | Longest increasing subsequence | Medium | O(n²) | `front[i]` = LIS ending at `i` (left to right) and `back[i]` = LIS **starting** at `i` going down (right to left). |
| 36 | [Number of longest increasing subsequences](28-dynamic-programming/36-number-of-longest-increasing-subsequences.md) | Longest increasing subsequence | Medium | O(n²) | Alongside `dp[i]` (LIS length ending at `i`), keep `cnt[i]` (how many such LIS end at `i`). |
| 37 | [Longest common subsequence](28-dynamic-programming/37-longest-common-subsequence.md) | DP on strings | Medium | O(n·m) | `dp[i][j]` = LCS of prefixes `a[0..i)` and `b[0..j)`. |
| 38 | [Longest common substring](28-dynamic-programming/38-longest-common-substring.md) | DP on strings | Medium | O(n·m) | Contiguity changes the recurrence: `dp[i][j]` = length of the common substring **ending exactly** at `a[i−1]` and `b[j−1]`. |
| 39 | [Longest palindromic subsequence](28-dynamic-programming/39-longest-palindromic-subsequence.md) | DP on strings | Medium | O(n²) | **LPS(s) = LCS(s, reverse(s))**. |
| 40 | [Minimum insertions to make string palindrome](28-dynamic-programming/40-minimum-insertions-to-make-string-palindrome.md) | DP on strings | Hard | O(n²) | Keep the longest palindromic subsequence untouched. |
| 41 | [Minimum insertions or deletions to convert string A to B](28-dynamic-programming/41-min-insertions-deletions-a-to-b.md) | DP on strings | Medium | a | Keep their LCS untouched: delete the other ` |
| 42 | [Shortest common supersequence](28-dynamic-programming/42-shortest-common-supersequence.md) | DP on strings | Hard | a | Its length is ` |
| 43 | [Distinct subsequences](28-dynamic-programming/43-distinct-subsequences.md) | DP on strings | Hard | O(n·m) | `dp[i][j]` = ways to form `t[0..j)` from `s[0..i)`. |
| 44 | [Edit distance](28-dynamic-programming/44-edit-distance.md) | DP on strings | Hard | O(n·m) | `dp[i][j]` for prefixes. |
| 45 | [Wildcard matching](28-dynamic-programming/45-wildcard-matching.md) | DP on strings | Hard | O(n·m) | `dp[i][j]` = does `p[0..i)` match `s[0..j)`? |
| 46 | [Word break](28-dynamic-programming/46-word-break.md) | DP on strings | Medium | O(n·L²) | `dp[i]` = can the prefix `s[0..i)` be segmented? |
| 47 | [Count palindromic subsequences](28-dynamic-programming/47-count-palindromic-subsequences.md) | DP on strings | Hard | O(n²) | Interval DP with inclusion–exclusion: `dp[i][j] = dp[i+1][j] + dp[i][j−1] − dp[i+1][j−1]` counts subsequences avoiding at least one end. |
| 48 | [Matrix chain multiplication](28-dynamic-programming/48-matrix-chain-multiplication.md) | Partition DP (MCM) | Hard | O(n³) | Matrix `i` is `arr[i−1] × arr[i]`. |
| 49 | [Minimum cost to cut the stick](28-dynamic-programming/49-minimum-cost-to-cut-the-stick.md) | Partition DP (MCM) | Hard | O(m³) | Sort the cuts and add the endpoints `0` and `n`. |
| 50 | [Burst balloons](28-dynamic-programming/50-burst-balloons.md) | Partition DP (MCM) | Hard | O(n³) | Choosing the **first** balloon to burst breaks independence, because neighbours change. |
| 51 | [Evaluate boolean expression to true](28-dynamic-programming/51-evaluate-boolean-expression-to-true.md) | Partition DP (MCM) | Hard | ` is false only on `lF·rF`; `^` is true on `lT·rF + lF·rT`. True-only DP fails because `^` and ` | Track **both** counts per interval: `T(i, j)` and `F(i, j)`. |
| 52 | [Palindrome partitioning II](28-dynamic-programming/52-palindrome-partitioning-ii.md) | Partition DP (MCM) | Hard | O(n²) | This is **front partitioning**, not interval DP. |
| 53 | [Partition array for maximum sum](28-dynamic-programming/53-partition-array-for-maximum-sum.md) | Partition DP (MCM) | Medium | O(n·k) | Front partition: `dp[i]` = best for the suffix `arr[i..]`. |
| 54 | [Minimum path sum in a grid](28-dynamic-programming/54-minimum-path-sum-in-a-grid.md) | Extra (A2Z sheet) | Medium | O(mn) | `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`, with the first row and first column filled as prefix sums. |

## Part 29: Tries

[Part README](29-tries/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Tries and Binary Tries](29-tries/01-trie-theory.md) | — | 📘 Theory | — | Trie node design (array vs map children, end flag, pass/end counters), insert / search / startsWith / erase, complexity and memory, bit prerequisites (testing, setting and clear… |
| 2 | [Implement Trie (prefix tree)](29-tries/02-implement-trie-prefix-tree.md) | Theory & implementation | Medium | O(L) per op | Each node holds up to 26 child pointers and an `end` flag. |
| 3 | [Implement Trie II (count and erase)](29-tries/03-implement-trie-ii-count-and-erase.md) | Theory & implementation | Medium | O(L) per op | Replace the `end` flag with two counters per node: `pass` = how many inserted words go **through** this node, `end` = how many **finish** here. |
| 4 | [Longest word with all prefixes (complete string)](29-tries/04-longest-word-with-all-prefixes-complete-string.md) | Problems | Medium | O(Σ L) | Insert every word into a trie. |
| 5 | [Number of distinct substrings in a string](29-tries/05-number-of-distinct-substrings-in-a-string.md) | Problems | Hard | O(n²) | Every substring is a prefix of some suffix. |
| 6 | [Maximum XOR of two numbers in an array](29-tries/06-maximum-xor-of-two-numbers-in-an-array.md) | Problems | Medium | O(31·n) | XOR is maximised greedily from the **most significant bit**: a 1 at bit 30 beats anything in the lower bits. |
| 7 | [Maximum XOR with an element from the array](29-tries/07-maximum-xor-with-an-element-from-the-array.md) | Problems | Hard | O((n + q) log + 31(n + q)) | The `a ≤ m` filter changes per query, so answer the queries **offline**. |

## Part 30: Strings (Advanced)

[Part README](30-strings-advanced/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [String Hashing and Pattern Matching](30-strings-advanced/01-string-hashing-and-matching-theory.md) | — | 📘 Theory | — | Polynomial rolling hash (base, modulus, overflow, negative mod), collision probability and double hashing, Rabin-Karp, the Z-function and its Z-box, the KMP prefix function and… |
| 2 | [Reverse every word in a string](30-strings-advanced/02-reverse-every-word-in-a-string.md) | Medium problems | Medium | O(n) | Scan from the **right**: skip spaces, mark the end of a word, walk left to its start, and append it. |
| 3 | [Minimum number of bracket reversals to balance an expression](30-strings-advanced/03-minimum-number-of-bracket-reversals-to-balance-an-expression.md) | Medium problems | Medium | O(n) | Cancel matched pairs greedily. |
| 4 | [Count and say](30-strings-advanced/04-count-and-say.md) | Medium problems | Medium | O(Σ term lengths) | Each term is the **run-length encoding** of the previous one, read aloud: for every maximal block of equal digits, write its length, then the digit. |
| 5 | [Rabin-Karp algorithm](30-strings-advanced/05-rabin-karp-algorithm.md) | Advanced pattern matching | Hard | O(n + m) expected, O(n·m) worst | Hash the pattern and the first window as base-B polynomials mod a prime. |
| 6 | [Z-function](30-strings-advanced/06-z-function.md) | Advanced pattern matching | Hard | pat | `z[i]` is the length of the longest substring starting at `i` that matches a **prefix** of the string. |
| 7 | [KMP algorithm (LPS array)](30-strings-advanced/07-kmp-algorithm-lps-array.md) | Advanced pattern matching | Hard | O(n) | `lps[i]` is the length of the longest proper prefix of `s[0..i]` that is also a suffix of it. |
| 8 | [Shortest palindrome](30-strings-advanced/08-shortest-palindrome.md) | Advanced pattern matching | Hard | O(n) | Only the part after the **longest palindromic prefix** must be mirrored in front. |
| 9 | [Longest happy prefix](30-strings-advanced/09-longest-happy-prefix.md) | Advanced pattern matching | Hard | O(n) | This is literally `lps[n − 1]`, the last value of the KMP prefix function. |

## Part 31: Maths

[Part README](31-maths/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Primes and the Sieve](31-maths/01-sieve-theory.md) | — | 📘 Theory | — | Trial division to √n, the sieve of Eratosthenes and why it starts at i², the n log log n bound, linear sieve and SPF tables, factorisation and divisor functions, prefix counts,… |
| 5 | [Modular Arithmetic and Combinatorics](31-maths/05-modular-arithmetic-and-combinatorics-theory.md) | — | 📘 Theory | — | Mod rules, binary/matrix exponentiation, extended Euclid, Fermat and linear-time inverses, nCr mod p (factorials, Pascal, Lucas), Catalan, stars and bars, inclusion–exclusion, φ… |
| 2 | [Print all primes till N](31-maths/02-print-all-primes-till-n.md) | Sieve of Eratosthenes | Easy | O(n log log n) | Mark multiples instead of testing each number. |
| 3 | [Prime factorisation of a number](31-maths/03-prime-factorisation-of-a-number.md) | Sieve of Eratosthenes | Medium | O(X log log X + Σ log x) | Precompute the **smallest prime factor** `spf[x]` for every `x ≤ max` with a sieve: when a prime `p` crosses out `j`, set `spf[j] = p` if it is still unset. |
| 4 | [Count primes in range L to R](31-maths/04-count-primes-in-range-l-to-r.md) | Sieve of Eratosthenes | Medium | O(R log log R + q) | Sieve once up to the largest `R`, then build a prefix count `pre[i]` = the number of primes `≤ i`. |

## Part 32: Beyond the Sheet

[Part README](32-beyond-the-sheet/README.md)

| # | Note | Group | Difficulty | Optimal | Key insight |
|---|---|---|---|---|---|
| 1 | [Range Queries](32-beyond-the-sheet/01-range-queries-theory.md) | — | 📘 Theory | — | A chooser flowchart; prefix/difference/2D prefix; sparse table; Fenwick (inversions, range add, two BITs); segment tree templates with custom merges; lazy propagation; offline t… |
| 2 | [Advanced DP](32-beyond-the-sheet/02-advanced-dp-theory.md) | — | 📘 Theory | — | Family recognition; bitmask DP (TSP, assignment, submask enumeration); the digit-DP template; tree DP states; rerooting (sum of distances); expected-value DP; optimisation tricks. |
| 3 | [Advanced Trees and Graphs](32-beyond-the-sheet/03-advanced-trees-and-graphs-theory.md) | — | 📘 Theory | — | Binary lifting (k-th ancestor, LCA); an LCA method comparison; Euler tour subtree ranges; Hierholzer Eulerian paths (Reconstruct Itinerary); 0-1, multi-source, state, bidirectio… |
| 4 | [Techniques Toolbox](32-beyond-the-sheet/04-techniques-toolbox-theory.md) | — | 📘 Theory | — | Meet in the middle, sweep line (rooms, skyline), coordinate compression, reservoir sampling, Fisher–Yates and other randomisation, streaming structures, O(1) design recipes (LRU… |
