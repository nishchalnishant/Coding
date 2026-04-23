# Bit Manipulation — SDE-3 Gold Standard

Use binary representation and bitwise operators for compact state and O(1) constant-time operations. SDE-3 mastery: masking, subset enumeration, bitmask DP, and XOR tries.

---

## 1. Concept Overview

### Core Operators

| Operator | Use | Key Identity |
| :--- | :--- | :--- |
| **AND `&`** | Mask / clear bits | `n & (n-1)` clears lowest set bit |
| **OR `\|`** | Set bits | `n \| (1 << k)` sets bit k |
| **XOR `^`** | Toggle; detect difference | `a ^ a = 0`, `a ^ 0 = a` — cancels pairs |
| **NOT `~`** | Flip all bits | In Python: `~x == -(x+1)`, not a 32-bit flip |
| **Left shift `<<`** | Multiply by 2^k | `1 << k` = 2^k |
| **Right shift `>>`** | Divide by 2^k (floor) | Arithmetic (sign-preserving) in Python |

> [!CAUTION]
> **Python integer gotcha — the #1 interview trap**: Python integers have **arbitrary precision** — there is no 32-bit overflow. When a problem says "treat as 32-bit unsigned integer", you must mask with `& 0xFFFFFFFF` after operations to simulate wrap-around. `~x` in Python equals `-(x+1)`, not the bitwise complement you get in C/Java. Always clarify the language's integer model with your interviewer.

---

## 2. Core Algorithms & Click Moments

### Single Number — XOR Cancellation

> [!IMPORTANT]
> **The Click Moment**: "Every element appears **exactly twice** except one" — OR — "find the **unpaired** element" — OR — "one number is **missing** from a complete sequence 1..N" — AND — the constraint is O(1) space. If you see those words together, XOR is the answer before you finish reading the problem.

- **Idea**: XOR all elements. Paired values cancel (`a ^ a = 0`); the unique value survives (`x ^ 0 = x`).
- **Complexity**: O(N) time, O(1) space.

```python
from functools import reduce
from operator import xor

def single_number(nums: list[int]) -> int:
    if not nums:
        raise ValueError("nums must be non-empty")
    return reduce(xor, nums)

def missing_number(nums: list[int]) -> int:
    n = len(nums)
    return reduce(xor, range(n + 1)) ^ reduce(xor, nums)
```

> [!CAUTION]
> XOR cancellation **only** works when every other element appears an **even** number of times. If others appear 3× (Single Number II), XOR alone fails — you need bit counting mod 3.

---

### Count Set Bits — Brian Kernighan's Algorithm

> [!IMPORTANT]
> **The Click Moment**: "Number of 1-bits", "Hamming weight", "popcount", "Hamming distance between two integers", "parity check". Any problem asking you to measure how many bits are set should trigger this pattern immediately.

- **Idea**: `n &= (n - 1)` clears the **lowest** set bit in one step. Count iterations until `n == 0`.
- **Complexity**: O(k) where k = number of set bits (≤ 32 or 64 for fixed-width integers).

```python
def count_set_bits(n: int) -> int:
    count = 0
    n &= 0xFFFFFFFF  # constrain to 32-bit for problems specifying unsigned int
    while n:
        n &= n - 1
        count += 1
    return count

def hamming_distance(x: int, y: int) -> int:
    return count_set_bits(x ^ y)
```

> [!TIP]
> In production Python, use `bin(n).count('1')` or `n.bit_count()` (Python 3.10+). Brian Kernighan's is the answer when the interviewer explicitly asks "how would you do this **without built-ins**?" — show you know why it works, not just that it does.

---

### Bitmask Subset Enumeration

> [!IMPORTANT]
> **The Click Moment**: "All possible **subsets**" — OR — "**power set**" — OR — **N ≤ 20** with exponential state. Also: "try all combinations of N items" — if N is small, bitmask enumeration replaces backtracking and is cleaner in DP transitions.

- **Idea**: Integers 0 to 2^N−1 biject to subsets. Bit k of integer `mask` = is element k included?

```python
def all_subsets(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    result = []
    for mask in range(1 << n):
        subset = [nums[k] for k in range(n) if mask & (1 << k)]
        result.append(subset)
    return result  # 2^n subsets including empty set
```

> [!TIP]
> **SDE-3 trick — enumerate sub-subsets in O(3^N) total**: To iterate over all subsets of a given bitmask `mask`:
> ```python
> sub = mask
> while sub:
>     process(sub)
>     sub = (sub - 1) & mask
> ```
> This is the core loop in subset-sum DP optimizations. The total work across all masks is O(3^N) — a non-obvious but provable bound that separates SDE-3 candidates.

---

### Power of Two Check

> [!IMPORTANT]
> **The Click Moment**: "Is N a power of 2?" — OR — "exactly one bit is set" — OR — memory allocator / block-size validation problems.

```python
def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0
```

> [!CAUTION]
> Always check `n > 0` first. The expression `n & (n - 1)` equals 0 for `n = 0`, but zero is **not** a power of two. This is a classic one-liner trap.

---

### Bitmask DP — Subset State Tracking

> [!IMPORTANT]
> **The Click Moment**: "Assign N tasks/cities/people optimally" with N ≤ 20 — OR — "minimum cost to cover all elements" — OR — TSP-style problems. The key signal: you need to track **which elements have been used** and N is small.

- **State**: `dp[mask][i]` = optimal value for the subset `mask` with last element being i.
- **Transition**: For each unvisited element `v` not in `mask`, update `dp[mask | (1<<v)][v]`.

```python
def min_cost_tsp(cost: list[list[int]]) -> int:
    n = len(cost)
    if n == 0:
        return 0
    FULL_MASK = (1 << n) - 1
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # start at city 0, visited = {city 0}

    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == INF or not (mask & (1 << u)):
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                new_mask = mask | (1 << v)
                dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + cost[u][v])

    return min(dp[FULL_MASK][v] + cost[v][0] for v in range(1, n))
```

---

### XOR Trie — Maximum XOR Pair

> [!IMPORTANT]
> **The Click Moment**: "Maximum XOR of **two numbers** in an array" — OR — "find the pair with largest bitwise XOR". When you need the globally maximum XOR across all pairs, XOR sort/brute-force is O(N²); Trie is O(N×32).

- **Idea**: Insert numbers MSB-first into a binary trie. For each query number, greedily take the **opposite** branch at each bit level to maximize XOR.
- **Complexity**: O(N × 32) time and space.

```python
class XORTrie:
    def __init__(self):
        self.children: dict = {}

    def insert(self, num: int) -> None:
        node = self.children
        for bit in range(31, -1, -1):
            b = (num >> bit) & 1
            if b not in node:
                node[b] = {}
            node = node[b]

    def max_xor_with(self, num: int) -> int:
        node = self.children
        result = 0
        for bit in range(31, -1, -1):
            b = (num >> bit) & 1
            want = 1 - b  # greedily take the opposite bit
            if want in node:
                result |= (1 << bit)
                node = node[want]
            elif b in node:
                node = node[b]
            else:
                break
        return result

def find_maximum_xor(nums: list[int]) -> int:
    if len(nums) < 2:
        return 0
    trie = XORTrie()
    for num in nums:
        trie.insert(num)
    return max(trie.max_xor_with(num) for num in nums)
```

---

## 3. SDE-3 Deep Dives

### Scalability: Streaming & Distributed Bit Operations

> [!TIP]
> **XOR is associative and commutative** — it can be computed across a distributed cluster without ordering. Each worker XORs its data shard; the coordinator XORs the worker results. This is how "find the missing number" or "detect data corruption" works at petabyte scale without loading everything into RAM.

For **popcount at scale**:
- Redis `BITCOUNT` operates on bitstrings stored in memory with an O(N/8) scan.
- CPU-native: x86 `POPCNT` instruction processes 64 bits in a single cycle.
- Software fallback: split 64-bit integers into 4 × 16-bit chunks with a precomputed 65536-entry lookup table — O(1) per integer.

For **streaming unique element detection**, XOR-based algorithms are naturally **single-pass** and **O(1) space** — ideal for log-based anomaly detection at scale.

### Concurrency: Atomic Bit Operations

> [!TIP]
> Use a single **`AtomicLong`** (Java) or **`std::atomic<uint64_t>`** (C++) to store 64 boolean flags. `fetch_or` / `fetch_and` with Compare-And-Swap (CAS) lets you set/clear individual bits **lock-free** — far cheaper than 64 `AtomicBoolean` objects due to cache-line efficiency.

In Python (CPython): basic `int` mutations are GIL-protected within a single process, but not across subprocesses or native threads modifying shared memory. For multi-process bit state, use `multiprocessing.Value('I', 0, lock=True)`.

> [!CAUTION]
> **ABA problem**: CAS-based bit operations can succeed spuriously if another thread toggles a bit and restores it between your read and write. Use versioned CAS (`compare_exchange_strong` with an expected-value check) for flag fields that must be monotonic.

### Trade-offs: Memory vs. CPU vs. Code Complexity

| Approach | Memory | CPU | Code Complexity | When to Prefer |
| :--- | :--- | :--- | :--- | :--- |
| XOR trick (unique element) | O(1) | O(N) | Very low | Single unique, all others paired exactly |
| Bit counting mod-K | O(1) | O(32N) | Low | Others appear K times, find unique |
| Bitmask DP (N ≤ 20) | O(2^N × N) | O(2^N × N²) | Medium | Small N, need to track used subset |
| XOR Trie | O(N × 32) | O(N × 32) | Medium-High | Maximum XOR pair across entire array |
| Backtracking (N > 20) | O(N) stack | O(N!) worst | Low | N too large for bitmask, pruning helps |

---

## 4. Common Interview Problems

### Easy
- [Number of 1 Bits](../../google-sde2/PROBLEM_DETAILS.md#number-of-1-bits) — Brian Kernighan's or `n.bit_count()`.
- **Power of Two** — `n > 0 and (n & (n-1)) == 0`.
- **Reverse Bits** — Swap bit `i` with bit `31-i` using masks.

### Medium
- [Single Number II](../../google-sde2/PROBLEM_DETAILS.md#single-number-ii) — Others appear 3×; bit count mod 3.
- **Maximum XOR of Two Numbers** — XOR Trie; O(N×32).
- **Counting Bits** — 1D DP: `dp[i] = dp[i >> 1] + (i & 1)`.
- **Sum of Two Integers (without +)** — Carry simulation with XOR and AND.

### Hard
- **Maximum XOR with Element from Array** — Offline queries + sorted XOR Trie.
- **Smallest Sufficient Team** — Bitmask DP on skill coverage; `dp[mask | skill_mask]`.
- **Travelling Salesman (N ≤ 20)** — Bitmask DP as above.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **[Single Number](../../google-sde2/PROBLEM_DETAILS.md#single-number)** | "Pairs cancel" | `reduce(xor, nums)` | Only works when all others appear **exactly twice**. |
| **[Single Number II](../../google-sde2/PROBLEM_DETAILS.md#single-number-ii)** | "Appear 3× except one" | Count each bit mod 3 across all nums | XOR alone doesn't work; need separate mod-3 bit counter. |
| **Power of Two** | "Single bit set" | `n > 0 and n & (n-1) == 0` | `n = 0` satisfies `n & (n-1) == 0` but is not a power of 2. |
| **Reverse Bits** | "Bit symmetry" | Shift and OR, 32 iterations | Must pad to exactly 32 bits; Python needs `& 0xFFFFFFFF`. |
| **Hamming Distance** | "Differing bits between x and y" | `count_set_bits(x ^ y)` | Watch for signed integer representation in Java/C++. |
| **Counting Bits** | "Reuse sub-results" | `dp[i] = dp[i >> 1] + (i & 1)` | Recognize as 1D DP, not just a loop with bit tricks. |
| **Find Missing Number** | "One missing from 0..N" | `xor(0..N) ^ xor(nums)` | Only works when **exactly one** number is missing. |
| **Sum Without `+`** | "Add using bits" | XOR for sum, AND<<1 for carry, loop until carry=0 | Python needs `& 0xFFFFFFFF` mask; infinite loop risk without it. |
| **Smallest Sufficient Team** | "Cover all skills, min people" | Bitmask DP on skill union | Model each person's skills as a bitmask; 2^N states. |

---

## See also

- [Dynamic Programming](dynamic-programming/README.md) — bitmask DP and O(3^N) subset enumeration
- [Patterns Master](../../../reference/patterns/patterns-master.md) — bitmask recognition triggers
- [Trie](../data-structures/trie.md) — XOR Trie for maximum XOR pair
