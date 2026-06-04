---
tags: [coding, algorithms, bit-manipulation]
topic: Bit Manipulation
difficulty: mixed
---

# Bit Manipulation — Problem Deep Dives


> [!abstract] Google Interview Legend
> `🔥 Google` — **Core** problem: extremely high frequency at Google SDE 2/3 interviews. Cover these first.
> `⭐ Google` — **Important** problem: medium frequency at Google SDE 2/3 level. Cover after core.
> Problems without a marker are good practice but less Google-specific at SDE 2/3 level.

---

## XOR Properties

### Single Number `🔥 Google`

> [!example] Problem
> Given a non-empty array of integers nums, every element appears twice except for one. Find that single one.
> You must implement a solution with a linear runtime complexity and use only constant extra space.
> 
> **Example 1:**
> ```
> Input: nums = [2,2,1]
> Output: 1
> ```
> 
> **Example 2:**
> ```
> Input: nums = [4,1,2,1,2]
> Output: 4
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1]
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 3 * 10^4
> - -3 * 10^4 <= nums[i] <= 3 * 10^4
> - Each element in the array appears twice except for one element which appears only once.

> [!info] Approach
> XOR is self-inverse: `a ^ a = 0` and `a ^ 0 = a`. All paired elements cancel; the unique element survives. XOR all elements together. Pairs annihilate; the lone value is the result. `reduce(xor, nums)`. One pass, no extra memory.

> [!note]- Python Solution
> ```python
> from functools import reduce
> from operator import xor
> 
> def single_number(nums):
>     return reduce(xor, nums)
> ```

> [!success] Complexity
> Time O(N), Space O(1).

> [!tip] Alternatives
> Hash set — add if not present, remove if present; O(N) time but O(N) space. Sort then check adjacent pairs — O(N log N). XOR is uniquely optimal.

---

### Single Number II (Three Copies — Bit Counting) `🔥 Google`

> [!example] Problem
> Given an integer array nums where every element appears three times except for one, which appears exactly once. Find the single element and return it.
> You must implement a solution with a linear runtime complexity and use only constant extra space.
> 
> **Example 1:**
> ```
> Input: nums = [2,2,3,2]
> Output: 3
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,1,0,1,0,1,99]
> Output: 99
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 3 * 10^4
> - -2^{31} <= nums[i] <= 2^{31} - 1
> - Each element in nums appears exactly three times except for one element which appears once.

> [!info] Approach
> XOR cancellation only works for pairs. With three copies, `x ^ x ^ x = x` — XOR fails. Instead, count bit occurrences: if a bit appears `3k` times across all numbers, it contributes 0 to the unique number. Count set bits at each of 32 positions. Take each count mod 3. Reconstruct the number from these remainders. Iterate bit positions 0–31. Sum how many numbers have bit `i` set. `count % 3` gives bit `i` of the unique number.

> [!note]- Python Solution
> ```python
> def single_number_ii(nums):
>     result = 0
>     for bit in range(32):
>         total = sum((num >> bit) & 1 for num in nums)
>         result |= (total % 3) << bit
>     # Handle Python's arbitrary precision for negative numbers
>     if result >= (1 << 31):
>         result -= (1 << 32)
>     return result
> ```

> [!success] Complexity
> Time O(32·N) = O(N), Space O(1).

> [!tip] Alternatives
> `ones` and `twos` bitmask state machine — tracks bits appearing 1 and 2 times mod 3; elegant but harder to explain. Hash map counting — O(N) time, O(N) space.

---

### Single Number III (Two Unique — XOR Split) `🔥 Google`

> [!example] Problem
> Given an integer array nums, in which exactly two elements appear only once and all the other elements appear exactly twice. Find the two elements that appear only once. You can return the answer in any order.
> You must write an algorithm that runs in linear runtime complexity and uses only constant extra space.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,1,3,2,5]
> Output: [3,5]
> Explanation:  [5, 3] is also a valid answer.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [-1,0]
> Output: [-1,0]
> ```
> 
> **Example 3:**
> ```
> Input: nums = [0,1]
> Output: [1,0]
> ```
> 
> **Constraints:**
> - 2 <= nums.length <= 3 * 10^4
> - -2^{31} <= nums[i] <= 2^{31} - 1
> - Each integer in nums will appear twice, only two integers will appear once.

> [!info] Approach
> XOR all elements → `xor_sum = x ^ y`. Since `x ≠ y`, at least one bit differs. That differing bit can partition the array so `x` and `y` end up in different groups. XOR each group independently to isolate each unique. Find any set bit in `xor_sum` (rightmost: `xor_sum & (-xor_sum)`). Partition array on that bit; XOR each partition. Two-pass: pass 1 computes `xor_sum`; pass 2 partitions and XORs each group.

> [!note]- Python Solution
> ```python
> from functools import reduce
> from operator import xor
> 
> def single_number_iii(nums):
>     xor_sum = reduce(xor, nums)
>     diff_bit = xor_sum & (-xor_sum)   # isolate rightmost differing bit
> 
>     x = y = 0
>     for num in nums:
>         if num & diff_bit:
>             x ^= num
>         else:
>             y ^= num
> 
>     return [x, y]
> ```

> [!success] Complexity
> Time O(N), Space O(1).

> [!tip] Alternatives
> Hash set/map — O(N) time, O(N) space. Sorting — O(N log N). XOR split is the only O(N)/O(1) solution.

---

### Missing Number `🔥 Google`

> [!example] Problem
> Given an array nums containing n distinct numbers in the range [0, n], return the only number in the range that is missing from the array.
> 
> **Example 1:**
> ```
> Input: nums = [3,0,1]
> Output: 2
> Explanation:
> n = 3 since there are 3 numbers, so all numbers are in the range [0,3] . 2 is the missing number in the range since it does not appear in nums .
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,1]
> Output: 2
> Explanation:
> n = 2 since there are 2 numbers, so all numbers are in the range [0,2] . 2 is the missing number in the range since it does not appear in nums .
> ```
> 
> **Example 3:**
> ```
> Input: nums = [9,6,4,2,3,5,7,0,1]
> Output: 8
> Explanation:
> n = 9 since there are 9 numbers, so all numbers are in the range [0,9] . 8 is the missing number in the range since it does not appear in nums .
> ```
> 
> **Constraints:**
> - n == nums.length
> - 1 <= n <= 10^4
> - 0 <= nums[i] <= n
> - All the numbers of nums are unique.

> [!info] Approach
> XOR of `[0..n] XOR [all nums]` cancels all present values; what's left is the missing value. XOR all indices `0..n` with all values in `nums`. Missing value survives. `reduce(xor, range(n+1)) ^ reduce(xor, nums)`.

> [!note]- Python Solution
> ```python
> from functools import reduce
> from operator import xor
> 
> def missing_number(nums):
>     n = len(nums)
>     return reduce(xor, range(n + 1)) ^ reduce(xor, nums)
> ```

> [!success] Complexity
> Time O(N), Space O(1).

> [!tip] Alternatives
> Gauss sum: `n*(n+1)//2 - sum(nums)` — O(N), O(1), simpler. Works if no overflow concern (Python integers are arbitrary precision). XOR approach avoids arithmetic overflow in other languages.

---

### Find the Difference `⭐ Google`

> [!example] Problem
> You are given two strings s and t.
> String t is generated by random shuffling string s and then add one more letter at a random position.
> Return the letter that was added to t.
> 
> **Example 1:**
> ```
> Input: s = "abcd", t = "abcde"
> Output: "e"
> Explanation: 'e' is the letter that was added.
> ```
> 
> **Example 2:**
> ```
> Input: s = "", t = "y"
> Output: "y"
> ```
> 
> **Constraints:**
> - 0 <= s.length <= 1000
> - t.length == s.length + 1
> - s and t consist of lowercase English letters.

> [!info] Approach
> Same as Single Number — every character in `s` appears once in `t` as a "pair", except the extra character. XOR all characters in both strings; pairs cancel. XOR all characters in `s` and `t` together. The unpaired character (the added one) survives. Convert chars to ord values; XOR all together.

> [!note]- Python Solution
> ```python
> from functools import reduce
> from operator import xor
> 
> def find_the_difference(s, t):
>     result = reduce(xor, (ord(c) for c in s + t))
>     return chr(result)
> ```

> [!success] Complexity
> Time O(N), Space O(1).

> [!tip] Alternatives
> Sum of ASCII values `sum(t) - sum(s)` — O(N), O(1), equally valid. Counter subtraction — O(N), O(1). XOR is most elegant.

---

## Bit Counting

### Number of 1 Bits (Hamming Weight) `🔥 Google`

> [!example] Problem
> Given a positive integer n, write a function that returns the number of set bits in its binary representation (also known as the Hamming weight).
> 
> **Example 1:**
> ```
> Input: n = 11
> Output: 3
> Explanation:
> The input binary string 1011 has a total of three set bits.
> ```
> 
> **Example 2:**
> ```
> Input: n = 128
> Output: 1
> Explanation:
> The input binary string 10000000 has a total of one set bit.
> ```
> 
> **Example 3:**
> ```
> Input: n = 2147483645
> Output: 30
> Explanation:
> The input binary string 1111111111111111111111111111101 has a total of thirty set bits.
> ```
> 
> **Constraints:**
> - 1 <= n <= 2^{31} - 1

> [!info] Approach
> `n & (n-1)` clears the lowest set bit. Each iteration removes exactly one set bit — O(k) where k = number of set bits, not O(32). Brian Kernighan's algorithm — loop while `n != 0`, clear lowest set bit each iteration. Count iterations until `n == 0`.

> [!note]- Python Solution
> ```python
> def hamming_weight(n):
>     count = 0
>     n &= 0xFFFFFFFF   # constrain to 32-bit
>     while n:
>         n &= n - 1    # clear lowest set bit
>         count += 1
>     return count
> ```

> [!success] Complexity
> Time O(k) where k = number of set bits ≤ 32, Space O(1).

> [!tip] Alternatives
> `bin(n).count('1')` or `n.bit_count()` (Python 3.10+) — idiomatic Python. Brian Kernighan's is the expected answer when interviewer says "without built-ins".

---

### Hamming Distance

> [!example] Problem
> The Hamming distance between two integers is the number of positions at which the corresponding bits are different.
> Given two integers x and y, return the Hamming distance between them.
> 
> **Example 1:**
> ```
> Input: x = 1, y = 4
> Output: 2
> Explanation:
> 1   (0 0 0 1)
> 4   (0 1 0 0)
>        ↑   ↑
> The above arrows point to positions where the corresponding bits are different.
> ```
> 
> **Example 2:**
> ```
> Input: x = 3, y = 1
> Output: 1
> ```
> 
> **Constraints:**
> - 0 <= x, y <= 2^{31} - 1

> [!info] Approach
> XOR produces a number with 1s exactly at positions where the inputs differ. Count those 1s. `hamming_distance(x, y) = popcount(x ^ y)`. XOR then apply Brian Kernighan's or `bin().count('1')`.

> [!note]- Python Solution
> ```python
> def hamming_distance(x, y):
>     diff = x ^ y
>     count = 0
>     while diff:
>         diff &= diff - 1
>         count += 1
>     return count
> ```

> [!success] Complexity
> Time O(k), Space O(1).

> [!tip] Alternatives
> `bin(x ^ y).count('1')` — one liner in Python. Same semantics.

---

### Counting Bits (DP Approach) `⭐ Google`

> [!example] Problem
> Given an integer n, return an array ans of length n + 1 such that for each i (0 <= i <= n), ans[i] is the number of 1's in the binary representation of i.
> 
> **Example 1:**
> ```
> Input: n = 2
> Output: [0,1,1]
> Explanation:
> 0 --> 0
> 1 --> 1
> 2 --> 10
> ```
> 
> **Example 2:**
> ```
> Input: n = 5
> Output: [0,1,1,2,1,2]
> Explanation:
> 0 --> 0
> 1 --> 1
> 2 --> 10
> 3 --> 11
> 4 --> 100
> 5 --> 101
> ```
> 
> **Constraints:**
> - 0 <= n <= 10^5

> [!info] Approach
> `i >> 1` is a smaller subproblem already solved. The number of bits in `i` = bits in `i >> 1` plus the lowest bit of `i`. DP recurrence: `dp[i] = dp[i >> 1] + (i & 1)`. Single pass `i = 1` to `n`; use previously computed values.

> [!note]- Python Solution
> ```python
> def count_bits(n):
>     dp = [0] * (n + 1)
>     for i in range(1, n + 1):
>         dp[i] = dp[i >> 1] + (i & 1)
>     return dp
> ```

> [!success] Complexity
> Time O(N), Space O(N).

> [!tip] Alternatives
> Call `bin(i).count('1')` per number — O(N·log N). Alternative DP: `dp[i] = dp[i & (i-1)] + 1` (clear lowest set bit + 1). Both correct.

---

### Reverse Bits `🔥 Google`

> [!example] Problem
> Reverse bits of a given 32 bits unsigned integer.
> Note
> 
> **Example 1:**
> ```
> Input: n = 43261596
> Output: 964176192
> Explanation:
> ```
> 
> **Example 2:**
> ```
> Input: n = 2147483644
> Output: 1073741822
> Explanation:
> ```
> 
> **Constraints:**
> - 0 <= n <= 2^{31} - 2
> - n is even.

> [!info] Approach
> Bit `i` of input should become bit `31-i` of output. Process each bit from LSB to MSB, shifting result left each step. Extract LSB of `n`; OR into `result`; shift `result` left, `n` right; repeat 32 times. 32 iterations. After 32 iterations, undo the final left shift (or structure the loop to avoid it).

> [!note]- Python Solution
> ```python
> def reverse_bits(n):
>     result = 0
>     for _ in range(32):
>         result = (result << 1) | (n & 1)
>         n >>= 1
>     return result & 0xFFFFFFFF    # ensure 32-bit unsigned
> ```

> [!success] Complexity
> Time O(32) = O(1), Space O(1).

> [!tip] Alternatives
> Divide-and-conquer byte swapping — cache 8-bit lookup table for repeated calls (`O(1)` per call after O(256) setup). In Python: `int(bin(n)[2:].zfill(32)[::-1], 2)` — readable but slow.

---

## Bit Tricks

### Power of Two `🔥 Google`

> [!example] Problem
> Given an integer n, return true if it is a power of two. Otherwise, return false.
> An integer n is a power of two, if there exists an integer x such that n == 2x.
> 
> **Example 1:**
> ```
> Input: n = 1
> Output: true
> Explanation: 20 = 1
> ```
> 
> **Example 2:**
> ```
> Input: n = 16
> Output: true
> Explanation: 24 = 16
> ```
> 
> **Example 3:**
> ```
> Input: n = 3
> Output: false
> ```
> 
> **Constraints:**
> - -2^{31} <= n <= 2^{31} - 1

> [!info] Approach
> A power of two has exactly one set bit. `n & (n-1)` clears the lowest set bit — if `n` is a power of two, the result is 0. Check `n > 0 and (n & (n-1)) == 0`. Guard `n > 0` is mandatory — `0 & (0-1) == 0` but 0 is not a power of two.

> [!note]- Python Solution
> ```python
> def is_power_of_two(n):
>     return n > 0 and (n & (n - 1)) == 0
> ```

> [!success] Complexity
> Time O(1), Space O(1).

> [!tip] Alternatives
> `n > 0 and n == (n & -n)` — isolates lowest set bit; equals `n` only if `n` is a power of two. Math: `n > 0 and math.log2(n) % 1 == 0` — floating point imprecision risk.

---

### Power of Four `🔥 Google`

> [!example] Problem
> Given an integer n, return true if it is a power of four. Otherwise, return false.
> An integer n is a power of four, if there exists an integer x such that n == 4x.
> 
> **Example 1:**
> ```
> Input: n = 16
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: n = 5
> Output: false
> ```
> 
> **Example 3:**
> ```
> Input: n = 1
> Output: true
> ```
> 
> **Constraints:**
> - -2^{31} <= n <= 2^{31} - 1

> [!info] Approach
> Powers of four are powers of two with the set bit at an even bit position (0, 2, 4, ...). Mask `0x55555555` = `0101...0101` in binary — has 1s at all even positions. Must be power of two AND the set bit must be at an even position. `n > 0 and (n & (n-1)) == 0 and (n & 0x55555555) != 0`.

> [!note]- Python Solution
> ```python
> def is_power_of_four(n):
>     return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0
> ```

> [!success] Complexity
> Time O(1), Space O(1).

> [!tip] Alternatives
> `n > 0 and n % 3 == 1` — powers of 4 are `≡ 1 (mod 3)`; elegant math alternative. Loop dividing by 4 — O(log n).

---

### Bitwise AND of Numbers Range

> [!example] Problem
> Given two integers left and right that represent the range [left, right], return the bitwise AND of all numbers in this range, inclusive.
> 
> **Example 1:**
> ```
> Input: left = 5, right = 7
> Output: 4
> ```
> 
> **Example 2:**
> ```
> Input: left = 0, right = 0
> Output: 0
> ```
> 
> **Example 3:**
> ```
> Input: left = 1, right = 2147483647
> Output: 0
> ```
> 
> **Constraints:**
> - 0 <= left <= right <= 2^{31} - 1

> [!info] Approach
> Any bit position where `left` and `right` differ will have both 0 and 1 values in the range — their AND is 0. Only the common prefix bits (where left = right from MSB down) survive. Right-shift both until equal; that common prefix is the answer. Shift count is the number of trailing zeros added back. Count shifts while `left != right`; shift both right; shift result back left.

> [!note]- Python Solution
> ```python
> def range_bitwise_and(left, right):
>     shift = 0
>     while left != right:
>         left >>= 1
>         right >>= 1
>         shift += 1
>     return left << shift
> ```

> [!success] Complexity
> Time O(log N) where N = right, Space O(1).

> [!tip] Alternatives
> Repeatedly clear the lowest set bit of `right` while `right > left`: `right &= right - 1`. Same O(log N).

---

### Sum of Two Integers Without + or - (LC 371)

> [!example] Problem
> Given two integers a and b, return the sum of the two integers without using the operators + and -.
> 
> **Example 1:**
> ```
> Input: a = 1, b = 2
> Output: 3
> ```
> 
> **Example 2:**
> ```
> Input: a = 2, b = 3
> Output: 5
> ```
> 
> **Constraints:**
> - -1000 <= a, b <= 1000

> [!info] Approach
> Addition in binary: sum-without-carry = `a XOR b`; carry = `(a AND b) << 1`. Repeat until no carry. Iterative XOR + AND until carry is zero. While `b != 0`: `carry = (a & b) << 1`; `a = a ^ b`; `b = carry`. Return `a`. In Python, need to handle 32-bit overflow with masking: `mask = 0xFFFFFFFF`; work modulo mask; at end if `a > 0x7FFFFFFF`: `a = ~(a ^ mask)`.

> [!note]- Python Solution
> ```python
> def get_sum(a, b):
>     mask = 0xFFFFFFFF
>     while b & mask:
>         carry = ((a & b) << 1) & mask
>         a = (a ^ b) & mask
>         b = carry
>     # If a is negative in 32-bit (MSB set), convert from unsigned to signed
>     if a > 0x7FFFFFFF:
>         a = ~(a ^ mask)
>     return a
> ```

> [!success] Complexity
> O(1) — at most 32 iterations. Space O(1).

> [!tip] Alternatives
> Use `ctypes` or `struct` to simulate 32-bit int — hacky. Recursive version — same logic, stack O(1) per call but logically cleaner.

---

## Bitmask DP

### Subsets via Bitmask

> [!example] Problem
> Given a set of `n` elements, enumerate all 2^n subsets.

> [!info] Approach
> Integer `mask` in `[0, 2^n)` bijects to subsets — bit `k` set means element `k` is included. Hardware-level iteration over all integers is faster than recursive backtracking. Iterate `mask` from `0` to `(1 << n) - 1`; for each mask, collect elements whose bit is set. For each `mask`, check each bit position `k`; include `nums[k]` if `mask & (1 << k)`.

> [!note]- Python Solution
> ```python
> def subsets(nums):
>     n = len(nums)
>     result = []
>     for mask in range(1 << n):
>         subset = [nums[k] for k in range(n) if mask & (1 << k)]
>         result.append(subset)
>     return result
> ```

> [!success] Complexity
> Time O(2^N · N), Space O(2^N · N).

> [!tip] Alternatives
> DFS backtracking — same O(2^N · N) but less cache-friendly. Cascading (iteratively add each element) — O(2^N · N), cleaner for LeetCode Subsets problem.

---

### Shortest Path Visiting All Nodes (BFS + Bitmask) `⭐ Google`

> [!example] Problem
> You have an undirected, connected graph of n nodes labeled from 0 to n - 1. You are given an array graph where graph[i] is a list of all the nodes connected with node i by an edge.
> Return the length of the shortest path that visits every node. You may start and stop at any node, you may revisit nodes multiple times, and you may reuse edges.
> 
> **Example 1:**
> ```
> Input: graph = [[1,2,3],[0],[0],[0]]
> Output: 4
> Explanation: One possible path is [1,0,2,0,3]
> ```
> 
> **Example 2:**
> ```
> Input: graph = [[1],[0,2,4],[1,3,4],[2],[1,2]]
> Output: 4
> Explanation: One possible path is [0,1,4,2,3]
> ```
> 
> **Constraints:**
> - n == graph.length
> - 1 <= n <= 12
> - 0 <= graph[i].length < n
> - graph[i] does not contain i.
> - If graph[a] contains b, then graph[b] contains a.
> - The input graph is always connected.

> [!info] Approach
> "Visit all nodes, revisits allowed" — standard BFS fails because visited state must encode which nodes have been visited, not just current position. Bitmask encodes the entire visit history. BFS on state `(node, visited_mask)`. Goal: `visited_mask == (1 << n) - 1`. Multi-source BFS — start from all nodes simultaneously (each with its own bit set). State space: O(N · 2^N). BFS guarantees minimum steps.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def shortest_path_length(graph):
>     n = len(graph)
>     target = (1 << n) - 1
> 
>     # Start from all nodes simultaneously
>     q: deque[tuple[int,int,int]] = deque((node, 1 << node, 0) for node in range(n))
>     visited = {(node, 1 << node) for node in range(n)}
> 
>     while q:
>         node, mask, steps = q.popleft()
>         if mask == target:
>             return steps
>         for nb in graph[node]:
>             new_mask = mask | (1 << nb)
>             state = (nb, new_mask)
>             if state not in visited:
>                 visited.add(state)
>                 q.append((nb, new_mask, steps + 1))
> 
>     return 0
> ```

> [!success] Complexity
> Time O(N · 2^N), Space O(N · 2^N).

> [!tip] Alternatives
> Bitmask DP with Floyd-Warshall precomputation — compute all-pairs shortest paths first, then DP over subsets. O(N² + N² · 2^N). BFS is simpler when revisits complicate the DP.

---

### Smallest Sufficient Team (Bitmask DP)

> [!example] Problem
> In a project, you have a list of required skills req_skills, and a list of people. The ith person people[i] contains a list of skills that the person has.
> Consider a sufficient team: a set of people such that for every required skill in req_skills, there is at least one person in the team who has that skill. We can represent these teams by the index of each person.
> Return any sufficient team of the smallest possible size, represented by the index of each person. You may return the answer in any order.
> It is guaranteed an answer exists.
> 
> **Example 1:**
> ```
> Input: req_skills = ["java","nodejs","reactjs"], people = [["java"],["nodejs"],["nodejs","reactjs"]]
> Output: [0,2]
> ```
> 
> **Example 2:**
> ```
> Input: req_skills = ["algorithms","math","java","reactjs","csharp","aws"], people = [["algorithms","math","java"],["algorithms","math","reactjs"],["java","csharp","aws"],["reactjs","csharp"],["csharp","math"],["aws","java"]]
> Output: [1,2]
> ```
> 
> **Constraints:**
> - 1 <= req_skills.length <= 16
> - 1 <= req_skills[i].length <= 16
> - req_skills[i] consists of lowercase English letters.
> - All the strings of req_skills are unique.
> - 1 <= people.length <= 60
> - 0 <= people[i].length <= 16
> - 1 <= people[i][j].length <= 16
> - people[i][j] consists of lowercase English letters.
> - All the strings of people[i] are unique.
> - Every skill in people[i] is a skill in req_skills.
> - It is guaranteed a sufficient team exists.

> [!info] Approach
> Skills are a finite set (≤ 16). State = bitmask of covered skills. DP over all 2^M skill subsets; for each state, try adding each person. `dp[mask]` = smallest list of people achieving skill coverage `mask`. Transition: for each person with skills `p_mask`, update `dp[mask | p_mask]`. Initialize `dp[0] = []`. For each existing state `mask` and each person, compute new coverage. Return `dp[(1<<m)-1]`.

> [!note]- Python Solution
> ```python
> def smallest_sufficient_team(req_skills: list[str],
>                             people: list[list[str]]) -> list[int]:
>     m = len(req_skills)
>     skill_idx = {s: i for i, s in enumerate(req_skills)}
>     full = (1 << m) - 1
> 
>     dp = [None] * (1 << m)
>     dp[0] = []
> 
>     for person_idx, skills in enumerate(people):
>         p_mask = 0
>         for s in skills:
>             if s in skill_idx:
>                 p_mask |= (1 << skill_idx[s])
>         for mask in range(1 << m):
>             if dp[mask] is None:
>                 continue
>             new_mask = mask | p_mask
>             if dp[new_mask] is None or len(dp[new_mask]) > len(dp[mask]) + 1:
>                 dp[new_mask] = dp[mask] + [person_idx]
> 
>     return dp[full] or []
> ```

> [!success] Complexity
> Time O(M · 2^M · P) where P = number of people, Space O(2^M · P).

> [!tip] Alternatives
> Greedy (maximize uncovered skills per person added) — O(P · M) but not optimal. Bitmask DP is exact.

---

### Travelling Salesman Problem (TSP) — N ≤ 20 (LC-style / classic)

> [!example] Problem
> Given `n` cities and a cost matrix, find the minimum cost to visit all cities exactly once and return to the start.

> [!info] Approach
> Brute force O(n!) is infeasible for n > 10. Bitmask DP on subsets reduces it to O(n² · 2^n) — feasible for n ≤ 20. `dp[mask][i]` = minimum cost to have visited exactly the cities in `mask`, currently at city `i`.

>   - **State:** `mask` (bitmask of visited cities), `i` (current city).
>   - **Base:** `dp[1<<0][0] = 0` (start at city 0, only city 0 visited).
>   - **Transition:** for each city `j` not in `mask`: `dp[mask|(1<<j)][j] = min(dp[mask|(1<<j)][j], dp[mask][i] + cost[i][j])`.
>   - **Answer:** `min over all i of dp[(1<<n)-1][i] + cost[i][0]`.

> [!note]- Python Solution
> ```python
> import math
> 
> def tsp(cost):
>     n = len(cost)
>     INF = math.inf
>     # dp[mask][i] = min cost reaching city i with visited set = mask
>     dp = [[INF] * n for _ in range(1 << n)]
>     dp[1][0] = 0  # start at city 0
> 
>     for mask in range(1 << n):
>         for i in range(n):
>             if dp[mask][i] == INF:
>                 continue
>             if not (mask & (1 << i)):
>                 continue  # city i not in mask, invalid state
>             for j in range(n):
>                 if mask & (1 << j):
>                     continue  # already visited
>                 new_mask = mask | (1 << j)
>                 new_cost = dp[mask][i] + cost[i][j]
>                 if new_cost < dp[new_mask][j]:
>                     dp[new_mask][j] = new_cost
> 
>     full = (1 << n) - 1
>     return int(min(dp[full][i] + cost[i][0] for i in range(1, n)))
> ```

> [!success] Complexity
> Time O(n² · 2^n), Space O(n · 2^n).

> [!tip] Alternatives
> Held-Karp algorithm — same complexity, different formulation. Branch and bound for larger `n`. Approximation algorithms (Christofides) for large instances.

---

## XOR Trie

### Maximum XOR with Element from Array (LC 1707)

> [!example] Problem
> You are given an array nums consisting of non-negative integers. You are also given a queries array, where queries[i] = [xi, mi].
> The answer to the ith query is the maximum bitwise XOR value of xi and any element of nums that does not exceed mi. In other words, the answer is max(nums[j] XOR xi) for all j such that nums[j] <= mi. If all elements in nums are larger than mi, then the answer is -1.
> Return an integer array answer where answer.length == queries.length and answer[i] is the answer to the ith query.
> 
> **Example 1:**
> ```
> Input: nums = [0,1,2,3,4], queries = [[3,1],[1,3],[5,6]]
> Output: [3,3,7]
> Explanation:
> 1) 0 and 1 are the only two integers not greater than 1. 0 XOR 3 = 3 and 1 XOR 3 = 2. The larger of the two is 3.
> 2) 1 XOR 2 = 3.
> 3) 5 XOR 2 = 7.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [5,2,4,6,6,3], queries = [[12,4],[8,1],[6,3]]
> Output: [15,-1,5]
> ```
> 
> **Constraints:**
> - 1 <= nums.length, queries.length <= 10^5
> - queries[i].length == 2
> - 0 <= nums[j], xi, mi <= 10^9

> [!info] Approach
> For each query we want max XOR with a constrained subset (`nums[j] ≤ mi`). If we process queries sorted by `mi` and `nums` sorted, we can insert elements incrementally into a Trie. Offline processing — sort queries by `mi`, sort `nums`. Two-pointer: for each query sorted by `mi`, insert all `nums ≤ mi` into XOR Trie, then query Trie for max XOR with `xi`.

>   1. Sort `nums`. Sort queries with original indices by `mi`.
>   2. Build XOR Trie supporting `insert` and `max_xor_query`.
>   3. For each query `(xi, mi, original_idx)`: insert all `nums ≤ mi` into Trie. Query Trie for max XOR with `xi`. If Trie empty, answer is -1.

> [!note]- Python Solution
> ```python
> class XORTrie:
>     def __init__(self):
>         self.root: dict = {}
>         self.size = 0
> 
>     def insert(self, num):
>         node = self.root
>         for bit in range(29, -1, -1):  # nums up to 10^9 < 2^30
>             b = (num >> bit) & 1
>             if b not in node:
>                 node[b] = {}
>             node = node[b]
>         self.size += 1
> 
>     def max_xor(self, num):
>         node = self.root
>         result = 0
>         for bit in range(29, -1, -1):
>             b = (num >> bit) & 1
>             want = 1 - b
>             if want in node:
>                 result |= (1 << bit)
>                 node = node[want]
>             else:
>                 node = node[b]
>         return result
> 
> def maximize_xor(nums, queries):
>     nums.sort()
>     indexed_queries = sorted(enumerate(queries), key=lambda x: x[1][1])
>     trie = XORTrie()
>     ans = [-1] * len(queries)
>     j = 0
>     for orig_idx, (xi, mi) in indexed_queries:
>         while j < len(nums) and nums[j] <= mi:
>             trie.insert(nums[j])
>             j += 1
>         if trie.size > 0:
>             ans[orig_idx] = trie.max_xor(xi)
>     return ans
> ```

> [!success] Complexity
> Time O((n + q) log(max_val)) where log(max_val) = 30. Space O(n · 30).

> [!tip] Alternatives
> For each query, brute force O(n·q) — TLE. Persistent Trie — O((n+q) log max_val) but complex implementation.

---

## Bitmask State Space Search

### Shortest Path with Keys and Locks

> [!example] Problem
> Grid with empty cells `.`, walls `#`, keys `a-f` (lowercase), locks `A-F` (uppercase). Start `@`, target `@` (only one of each). Find fewest steps to collect all keys.

> [!info] Approach
> State must encode current position AND which keys have been collected. Without keys in state, we can't determine which locks are passable. Bitmask of up to 6 keys = 64 possible key states. BFS on state `(r, c, keys_mask)`. Move onto a lock cell only if the corresponding key bit is set. Preprocess grid for start position, key count. BFS with state space O(R · C · 2^K). Goal: `keys_mask == (1 << num_keys) - 1`.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def shortest_path_all_keys(grid):
>     rows, cols = len(grid), len(grid[0])
>     start_r = start_c = 0
>     num_keys = 0
> 
>     for r in range(rows):
>         for c in range(cols):
>             ch = grid[r][c]
>             if ch == '@':
>                 start_r, start_c = r, c
>             elif ch.islower():
>                 num_keys += 1
> 
>     target = (1 << num_keys) - 1
>     q: deque[tuple[int,int,int,int]] = deque([(start_r, start_c, 0, 0)])
>     visited = {(start_r, start_c, 0)}
> 
>     while q:
>         r, c, keys, steps = q.popleft()
>         for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
>             nr, nc = r + dr, c + dc
>             if not (0 <= nr < rows and 0 <= nc < cols):
>                 continue
>             ch = grid[nr][nc]
>             if ch == '#':
>                 continue
>             if ch.isupper() and not (keys & (1 << (ord(ch) - ord('A')))):
>                 continue    # locked and don't have the key
>             new_keys = keys | (1 << (ord(ch) - ord('a'))) if ch.islower() else keys
>             if new_keys == target:
>                 return steps + 1
>             state = (nr, nc, new_keys)
>             if state not in visited:
>                 visited.add(state)
>                 q.append((nr, nc, new_keys, steps + 1))
> 
>     return -1
> ```

> [!success] Complexity
> Time O(R · C · 2^K), Space O(R · C · 2^K) where K ≤ 6.

> [!tip] Alternatives
> A* with heuristic (Manhattan to nearest uncollected key) — same worst case, faster in practice. Dijkstra with same state space — unnecessary since all moves cost 1.

---

## Encoding / Decoding with Bits

### UTF-8 Validation

> [!example] Problem
> Given an integer array data representing the data, return whether it is a valid UTF-8 encoding (i.e. it translates to a sequence of valid UTF-8 encoded characters).
> A character in UTF8 can be from 1 to 4 bytes long, subjected to the following rules:
> This is how the UTF-8 encoding would work:
> x denotes a bit in the binary form of a byte that may be either 0 or 1.
> Note: The input is an array of integers. Only the least significant 8 bits of each integer is used to store the data. This means each integer represents only 1 byte of data.
> 
> **Example 1:**
> ```
> Number of Bytes   |        UTF-8 Octet Sequence
>                        |              (binary)
>    --------------------+-----------------------------------------
>             1          |   0xxxxxxx
>             2          |   110xxxxx 10xxxxxx
>             3          |   1110xxxx 10xxxxxx 10xxxxxx
>             4          |   11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
> ```
> 
> **Example 2:**
> ```
> Input: data = [197,130,1]
> Output: true
> Explanation: data represents the octet sequence: 11000101 10000010 00000001.
> It is a valid utf-8 encoding for a 2-bytes character followed by a 1-byte character.
> ```
> 
> **Example 3:**
> ```
> Input: data = [235,140,4]
> Output: false
> Explanation: data represented the octet sequence: 11101011 10001100 00000100.
> The first 3 bits are all one's and the 4th bit is 0 means it is a 3-bytes character.
> The next byte is a continuation byte which starts with 10 and that's correct.
> But the second continuation byte does not start with 10, so it is invalid.
> ```
> 
> **Constraints:**
> - 1 <= data.length <= 2 * 10^4
> - 0 <= data[i] <= 255

> [!info] Approach
> Each byte's high bits determine its role. Bit masks isolate the relevant prefix bits. No parsing needed — pure bit-check. For each byte, determine if it's a 1-byte char, 2/3/4-byte leader, or continuation byte using masks. Track how many continuation bytes are expected; each subsequent byte must match `10xxxxxx`. Iterate bytes. If `expected_continuations > 0`, check `byte & 0xC0 == 0x80`. Otherwise classify the byte's prefix to set new expected count. Invalid if counts mismatch or byte is out of range.

> [!note]- Python Solution
> ```python
> def valid_utf8(data):
>     expected = 0
>     for byte in data:
>         byte &= 0xFF  # ensure 8-bit
>         if expected > 0:
>             if (byte >> 6) != 0b10:   # must be 10xxxxxx
>                 return False
>             expected -= 1
>         elif (byte >> 7) == 0:        # 0xxxxxxx — 1-byte
>             expected = 0
>         elif (byte >> 5) == 0b110:    # 110xxxxx — 2-byte leader
>             expected = 1
>         elif (byte >> 4) == 0b1110:   # 1110xxxx — 3-byte leader
>             expected = 2
>         elif (byte >> 3) == 0b11110:  # 11110xxx — 4-byte leader
>             expected = 3
>         else:
>             return False
>     return expected == 0
> ```

> [!success] Complexity
> Time O(N), Space O(1).

> [!tip] Alternatives
> Convert to binary string and use regex — readable but slow. This bitmask approach is the expected interview solution.

---

### Gray Code

> [!example] Problem
> An n-bit gray code sequence is a sequence of 2n integers where:
> Given an integer n, return any valid n-bit gray code sequence.
> 
> **Example 1:**
> ```
> Input: n = 2
> Output: [0,1,3,2]
> Explanation:
> The binary representation of [0,1,3,2] is [00,01,11,10].
> - 00 and 01 differ by one bit
> - 01 and 11 differ by one bit
> - 11 and 10 differ by one bit
> - 10 and 00 differ by one bit
> [0,2,3,1] is also a valid gray code sequence, whose binary representation is [00,10,11,01].
> - 00 and 10 differ by one bit
> - 10 and 11 differ by one bit
> - 11 and 01 differ by one bit
> - 01 and 00 differ by one bit
> ```
> 
> **Example 2:**
> ```
> Input: n = 1
> Output: [0,1]
> ```
> 
> **Constraints:**
> - 1 <= n <= 16

> [!info] Approach
> The standard binary-reflected Gray code has a closed-form formula: Gray code of integer `i` is `i ^ (i >> 1)`. Adjacent integers in Gray code differ by exactly one bit. Generate `[i ^ (i >> 1) for i in range(1 << n)]`. For `i` and `i+1`, `(i ^ (i>>1)) ^ ((i+1) ^ ((i+1)>>1))` always has exactly one bit set (the carry bit). This is provable by induction on the binary addition carry chain.

> [!note]- Python Solution
> ```python
> def gray_code(n):
>     return [i ^ (i >> 1) for i in range(1 << n)]
> ```

> [!success] Complexity
> Time O(2^N), Space O(2^N).

> [!tip] Alternatives
> Recursive bit-reflection construction — build for n-1, then reflect and prepend 0/1. Same O(2^N) but less concise. The `i ^ (i >> 1)` formula is the canonical closed-form answer.

---

### Decode XORed Array

> [!example] Problem
> There is a hidden integer array arr that consists of n non-negative integers.
> It was encoded into another integer array encoded of length n - 1, such that encoded[i] = arr[i] XOR arr[i + 1]. For example, if arr = [1,0,2,1], then encoded = [1,2,3].
> You are given the encoded array. You are also given an integer first, that is the first element of arr, i.e. arr[0].
> Return the original array arr. It can be proved that the answer exists and is unique.
> 
> **Example 1:**
> ```
> Input: encoded = [1,2,3], first = 1
> Output: [1,0,2,1]
> Explanation: If arr = [1,0,2,1], then first = 1 and encoded = [1 XOR 0, 0 XOR 2, 2 XOR 1] = [1,2,3]
> ```
> 
> **Example 2:**
> ```
> Input: encoded = [6,2,7,3], first = 4
> Output: [4,2,0,7,4]
> ```
> 
> **Constraints:**
> - 2 <= n <= 10^4
> - encoded.length == n - 1
> - 0 <= encoded[i] <= 10^5
> - 0 <= first <= 10^5

> [!info] Approach
> XOR is its own inverse: `encoded[i] = arr[i] ^ arr[i+1]` → `arr[i+1] = encoded[i] ^ arr[i]`. Given `arr[0]`, each subsequent element is uniquely determined. Sequential XOR: `arr[i+1] = encoded[i] ^ arr[i]`. Initialize `arr = [first]`. For each value in `encoded`, append `encoded[i] ^ arr[-1]`.

> [!note]- Python Solution
> ```python
> def decode(encoded, first):
>     arr = [first]
>     for val in encoded:
>         arr.append(val ^ arr[-1])
>     return arr
> ```

> [!success] Complexity
> Time O(N), Space O(N).

> [!tip] Alternatives
> No meaningful alternative — XOR inversion is the only O(N)/O(1)-extra approach. The problem is straightforwardly determined once `first` is known.

---

### Find the Duplicate Number (Bit Approach) `⭐ Google`

> [!example] Problem
> Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive.
> There is only one repeated number in nums, return this repeated number.
> You must solve the problem without modifying the array nums and using only constant extra space.
> 
> **Example 1:**
> ```
> Input: nums = [1,3,4,2,2]
> Output: 2
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,1,3,4,2]
> Output: 3
> ```
> 
> **Example 3:**
> ```
> Input: nums = [3,3,3,3,3]
> Output: 3
> ```
> 
> **Constraints:**
> - 1 <= n <= 10^5
> - nums.length == n + 1
> - 1 <= nums[i] <= n
> - All the integers in nums appear only once except for precisely one integer which appears two or more times.

> [!info] Approach
> For each bit position, count how many numbers in `[1, n]` have that bit set (call it `expected`) vs. how many in `nums` have it set (call it `actual`). If `actual > expected`, the duplicate has this bit set. For each of the 32 bit positions, compare bit frequency in `nums` vs. `[1..n]`. Reconstruct the duplicate from the differing bits. Outer loop over 32 bit positions; inner loop counts set bits in `nums` and in `range(1, n+1)`. If `count_nums > count_range`, set that bit in the answer.

> [!note]- Python Solution
> ```python
> def find_duplicate(nums):
>     n = len(nums) - 1
>     result = 0
>     for bit in range(32):
>         count_nums  = sum(1 for x in nums       if (x >> bit) & 1)
>         count_range = sum(1 for x in range(1, n + 1) if (x >> bit) & 1)
>         if count_nums > count_range:
>             result |= (1 << bit)
>     return result
> ```

> [!success] Complexity
> Time O(32·N) = O(N log N), Space O(1). Does not modify the array.

> [!tip] Alternatives
> Floyd's cycle detection (tortoise and hare) — O(N) time, O(1) space, treats array as linked list; optimal. Binary search on value space — O(N log N), O(1). Bit approach is a clean alternative when the interviewer asks for a non-pointer solution.

---

## See Also

[[dynamic-programming]] | [[graph-algorithms]] | [[trie]]
### Minimum XOR Sum of Two Arrays

> [!example] Problem
> You are given two integer arrays nums1 and nums2 of length n.
> The XOR sum of the two integer arrays is (nums1[0] XOR nums2[0]) + (nums1[1] XOR nums2[1]) + ... + (nums1[n - 1] XOR nums2[n - 1]) (0-indexed).
> Rearrange the elements of nums2 such that the resulting XOR sum is minimized.
> Return the XOR sum after the rearrangement.
> 
> **Example 1:**
> ```
> Input: nums1 = [1,2], nums2 = [2,3]
> Output: 2
> Explanation: Rearrange nums2 so that it becomes [3,2].
> The XOR sum is (1 XOR 3) + (2 XOR 2) = 2 + 0 = 2.
> ```
> 
> **Example 2:**
> ```
> Input: nums1 = [1,0,3], nums2 = [5,3,4]
> Output: 8
> Explanation: Rearrange nums2 so that it becomes [5,4,3]. 
> The XOR sum is (1 XOR 5) + (0 XOR 4) + (3 XOR 3) = 4 + 4 + 0 = 8.
> ```
> 
> **Constraints:**
> - n == nums1.length
> - n == nums2.length
> - 1 <= n <= 14
> - 0 <= nums1[i], nums2[i] <= 10^7

> [!info] Approach
> Bitwise greediness is not enough because pairings interact globally. The state is which elements of the second array are already used. Bitmask DP: `dp[mask]` is the minimum cost after assigning the first `popcount(mask)` elements of `nums1`. For each mask, try assigning the next `nums1[i]` to every unused `nums2[j]` and transition to `mask | (1 << j)`.

> [!note]- Python Solution
> ```python
> from functools import lru_cache
> 
> def minimum_xor_sum(nums1, nums2):
>     n = len(nums1)
> 
>     @lru_cache(None)
>     def dfs(mask):
>         i = mask.bit_count()
>         if i == n:
>             return 0
>         best = float("inf")
>         for j in range(n):
>             if not (mask & (1 << j)):
>                 best = min(best, (nums1[i] ^ nums2[j]) + dfs(mask | (1 << j)))
>         return best
> 
>     return dfs(0)
> ```

> [!success] Complexity
> O(n · 2^n) time, O(2^n) space.

> [!tip] Alternatives
> Brute-force permutations are factorial and too slow; bitmask DP is the standard interview answer.
