---
tags: [coding, algorithms, bit-manipulation]
topic: Bit Manipulation
difficulty: mixed
---

# Bit Manipulation — Problem Deep Dives

---

## XOR Properties

### Single Number

> [!example] Problem
> Every element in `nums` appears exactly twice except one. Find that one element. O(N) time, O(1) space.

> [!info] Approach
> - **WHY:** XOR is self-inverse: `a ^ a = 0` and `a ^ 0 = a`. All paired elements cancel; the unique element survives.
> - **WHAT:** XOR all elements together. Pairs annihilate; the lone value is the result.
> - **HOW:** `reduce(xor, nums)`. One pass, no extra memory.

> [!note]- Python Solution
> ```python
> from functools import reduce
> from operator import xor
> 
> def singleNumber(nums: list[int]) -> int:
>     return reduce(xor, nums)
> ```

> [!success] Complexity
> Time O(N), Space O(1).

> [!tip] Alternatives
> Hash set — add if not present, remove if present; O(N) time but O(N) space. Sort then check adjacent pairs — O(N log N). XOR is uniquely optimal.

---

### Single Number II (Three Copies — Bit Counting)

> [!example] Problem
> Every element appears exactly three times except one (appears once). Find it. O(N) time, O(1) space.

> [!info] Approach
> - **WHY:** XOR cancellation only works for pairs. With three copies, `x ^ x ^ x = x` — XOR fails. Instead, count bit occurrences: if a bit appears `3k` times across all numbers, it contributes 0 to the unique number.
> - **WHAT:** Count set bits at each of 32 positions. Take each count mod 3. Reconstruct the number from these remainders.
> - **HOW:** Iterate bit positions 0–31. Sum how many numbers have bit `i` set. `count % 3` gives bit `i` of the unique number.

> [!note]- Python Solution
> ```python
> def singleNumberII(nums: list[int]) -> int:
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

### Single Number III (Two Unique — XOR Split)

> [!example] Problem
> Two elements appear once, all others appear twice. Find both unique elements. O(N) time, O(1) space.

> [!info] Approach
> - **WHY:** XOR all elements → `xor_sum = x ^ y`. Since `x ≠ y`, at least one bit differs. That differing bit can partition the array so `x` and `y` end up in different groups. XOR each group independently to isolate each unique.
> - **WHAT:** Find any set bit in `xor_sum` (rightmost: `xor_sum & (-xor_sum)`). Partition array on that bit; XOR each partition.
> - **HOW:** Two-pass: pass 1 computes `xor_sum`; pass 2 partitions and XORs each group.

> [!note]- Python Solution
> ```python
> from functools import reduce
> from operator import xor
> 
> def singleNumberIII(nums: list[int]) -> list[int]:
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

### Missing Number

> [!example] Problem
> Array `nums` contains `n` distinct numbers in range `[0, n]`. Find the missing number.

> [!info] Approach
> - **WHY:** XOR of `[0..n] XOR [all nums]` cancels all present values; what's left is the missing value.
> - **WHAT:** XOR all indices `0..n` with all values in `nums`. Missing value survives.
> - **HOW:** `reduce(xor, range(n+1)) ^ reduce(xor, nums)`.

> [!note]- Python Solution
> ```python
> from functools import reduce
> from operator import xor
> 
> def missingNumber(nums: list[int]) -> int:
>     n = len(nums)
>     return reduce(xor, range(n + 1)) ^ reduce(xor, nums)
> ```

> [!success] Complexity
> Time O(N), Space O(1).

> [!tip] Alternatives
> Gauss sum: `n*(n+1)//2 - sum(nums)` — O(N), O(1), simpler. Works if no overflow concern (Python integers are arbitrary precision). XOR approach avoids arithmetic overflow in other languages.

---

### Find the Difference

> [!example] Problem
> String `t` is string `s` with one extra character appended and shuffled. Find the added character.

> [!info] Approach
> - **WHY:** Same as Single Number — every character in `s` appears once in `t` as a "pair", except the extra character. XOR all characters in both strings; pairs cancel.
> - **WHAT:** XOR all characters in `s` and `t` together. The unpaired character (the added one) survives.
> - **HOW:** Convert chars to ord values; XOR all together.

> [!note]- Python Solution
> ```python
> from functools import reduce
> from operator import xor
> 
> def findTheDifference(s: str, t: str) -> str:
>     result = reduce(xor, (ord(c) for c in s + t))
>     return chr(result)
> ```

> [!success] Complexity
> Time O(N), Space O(1).

> [!tip] Alternatives
> Sum of ASCII values `sum(t) - sum(s)` — O(N), O(1), equally valid. Counter subtraction — O(N), O(1). XOR is most elegant.

---

## Bit Counting

### Number of 1 Bits (Hamming Weight)

> [!example] Problem
> Return the number of set bits (1-bits) in a 32-bit unsigned integer.

> [!info] Approach
> - **WHY:** `n & (n-1)` clears the lowest set bit. Each iteration removes exactly one set bit — O(k) where k = number of set bits, not O(32).
> - **WHAT:** Brian Kernighan's algorithm — loop while `n != 0`, clear lowest set bit each iteration.
> - **HOW:** Count iterations until `n == 0`.

> [!note]- Python Solution
> ```python
> def hammingWeight(n: int) -> int:
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
> Return the number of positions at which the corresponding bits of two integers differ.

> [!info] Approach
> - **WHY:** XOR produces a number with 1s exactly at positions where the inputs differ. Count those 1s.
> - **WHAT:** `hamming_distance(x, y) = popcount(x ^ y)`.
> - **HOW:** XOR then apply Brian Kernighan's or `bin().count('1')`.

> [!note]- Python Solution
> ```python
> def hammingDistance(x: int, y: int) -> int:
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

### Counting Bits (DP Approach)

> [!example] Problem
> For every number `i` in `[0, n]`, return `dp[i]` = number of 1-bits in `i`. O(N) time, O(N) space.

> [!info] Approach
> - **WHY:** `i >> 1` is a smaller subproblem already solved. The number of bits in `i` = bits in `i >> 1` plus the lowest bit of `i`.
> - **WHAT:** DP recurrence: `dp[i] = dp[i >> 1] + (i & 1)`.
> - **HOW:** Single pass `i = 1` to `n`; use previously computed values.

> [!note]- Python Solution
> ```python
> def countBits(n: int) -> list[int]:
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

### Reverse Bits

> [!example] Problem
> Reverse the bits of a 32-bit unsigned integer.

> [!info] Approach
> - **WHY:** Bit `i` of input should become bit `31-i` of output. Process each bit from LSB to MSB, shifting result left each step.
> - **WHAT:** Extract LSB of `n`; OR into `result`; shift `result` left, `n` right; repeat 32 times.
> - **HOW:** 32 iterations. After 32 iterations, undo the final left shift (or structure the loop to avoid it).

> [!note]- Python Solution
> ```python
> def reverseBits(n: int) -> int:
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

### Power of Two

> [!example] Problem
> Determine if a given integer `n` is a power of two.

> [!info] Approach
> - **WHY:** A power of two has exactly one set bit. `n & (n-1)` clears the lowest set bit — if `n` is a power of two, the result is 0.
> - **WHAT:** Check `n > 0 and (n & (n-1)) == 0`.
> - **HOW:** Guard `n > 0` is mandatory — `0 & (0-1) == 0` but 0 is not a power of two.

> [!note]- Python Solution
> ```python
> def isPowerOfTwo(n: int) -> bool:
>     return n > 0 and (n & (n - 1)) == 0
> ```

> [!success] Complexity
> Time O(1), Space O(1).

> [!tip] Alternatives
> `n > 0 and n == (n & -n)` — isolates lowest set bit; equals `n` only if `n` is a power of two. Math: `n > 0 and math.log2(n) % 1 == 0` — floating point imprecision risk.

---

### Power of Four

> [!example] Problem
> Determine if a given integer `n` is a power of four.

> [!info] Approach
> - **WHY:** Powers of four are powers of two with the set bit at an even bit position (0, 2, 4, ...). Mask `0x55555555` = `0101...0101` in binary — has 1s at all even positions.
> - **WHAT:** Must be power of two AND the set bit must be at an even position.
> - **HOW:** `n > 0 and (n & (n-1)) == 0 and (n & 0x55555555) != 0`.

> [!note]- Python Solution
> ```python
> def isPowerOfFour(n: int) -> bool:
>     return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0
> ```

> [!success] Complexity
> Time O(1), Space O(1).

> [!tip] Alternatives
> `n > 0 and n % 3 == 1` — powers of 4 are `≡ 1 (mod 3)`; elegant math alternative. Loop dividing by 4 — O(log n).

---

### Bitwise AND of Numbers Range

> [!example] Problem
> Given `[left, right]`, return the bitwise AND of all numbers in that range.

> [!info] Approach
> - **WHY:** Any bit position where `left` and `right` differ will have both 0 and 1 values in the range — their AND is 0. Only the common prefix bits (where left = right from MSB down) survive.
> - **WHAT:** Right-shift both until equal; that common prefix is the answer. Shift count is the number of trailing zeros added back.
> - **HOW:** Count shifts while `left != right`; shift both right; shift result back left.

> [!note]- Python Solution
> ```python
> def rangeBitwiseAnd(left: int, right: int) -> int:
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
> Given two integers `a` and `b`, return `a + b` without using `+` or `-`.

> [!info] Approach
> - **WHY:** Addition in binary: sum-without-carry = `a XOR b`; carry = `(a AND b) << 1`. Repeat until no carry.
> - **WHAT:** Iterative XOR + AND until carry is zero.
> - **HOW:** While `b != 0`: `carry = (a & b) << 1`; `a = a ^ b`; `b = carry`. Return `a`. In Python, need to handle 32-bit overflow with masking: `mask = 0xFFFFFFFF`; work modulo mask; at end if `a > 0x7FFFFFFF`: `a = ~(a ^ mask)`.

> [!note]- Python Solution
> ```python
> def getSum(a: int, b: int) -> int:
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
> - **WHY:** Integer `mask` in `[0, 2^n)` bijects to subsets — bit `k` set means element `k` is included. Hardware-level iteration over all integers is faster than recursive backtracking.
> - **WHAT:** Iterate `mask` from `0` to `(1 << n) - 1`; for each mask, collect elements whose bit is set.
> - **HOW:** For each `mask`, check each bit position `k`; include `nums[k]` if `mask & (1 << k)`.

> [!note]- Python Solution
> ```python
> def subsets(nums: list[int]) -> list[list[int]]:
>     n = len(nums)
>     result: list[list[int]] = []
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

### Shortest Path Visiting All Nodes (BFS + Bitmask)

> [!example] Problem
> Undirected graph of `n` nodes. Find the shortest path that visits every node at least once. Nodes can be revisited.

> [!info] Approach
> - **WHY:** "Visit all nodes, revisits allowed" — standard BFS fails because visited state must encode which nodes have been visited, not just current position. Bitmask encodes the entire visit history.
> - **WHAT:** BFS on state `(node, visited_mask)`. Goal: `visited_mask == (1 << n) - 1`.
> - **HOW:** Multi-source BFS — start from all nodes simultaneously (each with its own bit set). State space: O(N · 2^N). BFS guarantees minimum steps.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def shortestPathLength(graph: list[list[int]]) -> int:
>     n = len(graph)
>     target = (1 << n) - 1
> 
>     # Start from all nodes simultaneously
>     q: deque[tuple[int,int,int]] = deque((node, 1 << node, 0) for node in range(n))
>     visited: set[tuple[int,int]] = {(node, 1 << node) for node in range(n)}
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
> `req_skills` = required skills. People have subsets of skills. Find the smallest group covering all required skills.

> [!info] Approach
> - **WHY:** Skills are a finite set (≤ 16). State = bitmask of covered skills. DP over all 2^M skill subsets; for each state, try adding each person.
> - **WHAT:** `dp[mask]` = smallest list of people achieving skill coverage `mask`. Transition: for each person with skills `p_mask`, update `dp[mask | p_mask]`.
> - **HOW:** Initialize `dp[0] = []`. For each existing state `mask` and each person, compute new coverage. Return `dp[(1<<m)-1]`.

> [!note]- Python Solution
> ```python
> def smallestSufficientTeam(req_skills: list[str],
>                             people: list[list[str]]) -> list[int]:
>     m = len(req_skills)
>     skill_idx = {s: i for i, s in enumerate(req_skills)}
>     full = (1 << m) - 1
> 
>     dp: list[list[int] | None] = [None] * (1 << m)
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
> - **WHY:** Brute force O(n!) is infeasible for n > 10. Bitmask DP on subsets reduces it to O(n² · 2^n) — feasible for n ≤ 20.
> - **WHAT:** `dp[mask][i]` = minimum cost to have visited exactly the cities in `mask`, currently at city `i`.
> - **HOW:**
>   - **State:** `mask` (bitmask of visited cities), `i` (current city).
>   - **Base:** `dp[1<<0][0] = 0` (start at city 0, only city 0 visited).
>   - **Transition:** for each city `j` not in `mask`: `dp[mask|(1<<j)][j] = min(dp[mask|(1<<j)][j], dp[mask][i] + cost[i][j])`.
>   - **Answer:** `min over all i of dp[(1<<n)-1][i] + cost[i][0]`.

> [!note]- Python Solution
> ```python
> import math
> 
> def tsp(cost: list[list[int]]) -> int:
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

### Maximum XOR of Two Numbers in an Array

> [!example] Problem
> Given integer array `nums`, find the maximum result of `nums[i] XOR nums[j]`.

> [!info] Approach
> - **WHY:** Brute force is O(N²). A trie lets us greedily maximize XOR bit-by-bit from MSB. For each query number, at each bit, we want the opposite bit — if it exists in the trie, take it; otherwise take the same bit.
> - **WHAT:** Insert all numbers MSB-first into a binary trie. For each number, query the trie greedily for maximum XOR.
> - **HOW:** Trie node has children `{0: ..., 1: ...}`. Insert: bit-by-bit from bit 31 to 0. Query: at each level, try to go to `1 - bit`; if present, add `1 << bit_pos` to result.

> [!note]- Python Solution
> ```python
> class XORTrie:
>     def __init__(self) -> None:
>         self.root: dict = {}
> 
>     def insert(self, num: int) -> None:
>         node = self.root
>         for bit in range(31, -1, -1):
>             b = (num >> bit) & 1
>             if b not in node:
>                 node[b] = {}
>             node = node[b]
> 
>     def max_xor(self, num: int) -> int:
>         node = self.root
>         result = 0
>         for bit in range(31, -1, -1):
>             b = (num >> bit) & 1
>             want = 1 - b               # greedily take opposite bit
>             if want in node:
>                 result |= (1 << bit)
>                 node = node[want]
>             elif b in node:
>                 node = node[b]
>             else:
>                 break
>         return result
> 
> def findMaximumXOR(nums: list[int]) -> int:
>     trie = XORTrie()
>     for num in nums:
>         trie.insert(num)
>     return max(trie.max_xor(num) for num in nums)
> ```

> [!success] Complexity
> Time O(N · 32) = O(N), Space O(N · 32) = O(N).

> [!tip] Alternatives
> Bit-by-bit greedy with prefix set — for each bit from MSB, check if any pair can achieve this XOR bit. O(32 · N). Brute force O(N²). Trie is canonical.

---

### Maximum XOR with Element from Array (LC 1707)

> [!example] Problem
> Given `nums` array and `queries[i] = [xi, mi]`: for each query find the maximum XOR of `xi` with any element from `nums` that is ≤ `mi`. Return array of answers (-1 if no valid element exists).

> [!info] Approach
> - **WHY:** For each query we want max XOR with a constrained subset (`nums[j] ≤ mi`). If we process queries sorted by `mi` and `nums` sorted, we can insert elements incrementally into a Trie.
> - **WHAT:** Offline processing — sort queries by `mi`, sort `nums`. Two-pointer: for each query sorted by `mi`, insert all `nums ≤ mi` into XOR Trie, then query Trie for max XOR with `xi`.
> - **HOW:**
>   1. Sort `nums`. Sort queries with original indices by `mi`.
>   2. Build XOR Trie supporting `insert` and `max_xor_query`.
>   3. For each query `(xi, mi, original_idx)`: insert all `nums ≤ mi` into Trie. Query Trie for max XOR with `xi`. If Trie empty, answer is -1.

> [!note]- Python Solution
> ```python
> class XORTrie:
>     def __init__(self) -> None:
>         self.root: dict = {}
>         self.size = 0
> 
>     def insert(self, num: int) -> None:
>         node = self.root
>         for bit in range(29, -1, -1):  # nums up to 10^9 < 2^30
>             b = (num >> bit) & 1
>             if b not in node:
>                 node[b] = {}
>             node = node[b]
>         self.size += 1
> 
>     def max_xor(self, num: int) -> int:
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
> def maximizeXor(nums: list[int], queries: list[list[int]]) -> list[int]:
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
> - **WHY:** State must encode current position AND which keys have been collected. Without keys in state, we can't determine which locks are passable. Bitmask of up to 6 keys = 64 possible key states.
> - **WHAT:** BFS on state `(r, c, keys_mask)`. Move onto a lock cell only if the corresponding key bit is set.
> - **HOW:** Preprocess grid for start position, key count. BFS with state space O(R · C · 2^K). Goal: `keys_mask == (1 << num_keys) - 1`.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def shortestPathAllKeys(grid: list[str]) -> int:
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
>     visited: set[tuple[int,int,int]] = {(start_r, start_c, 0)}
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

## See Also

[[dynamic-programming]] | [[graph-algorithms]] | [[trie]]
