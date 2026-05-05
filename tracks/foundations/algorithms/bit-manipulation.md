# Bit Manipulation — SDE-3 Gold Standard

Use binary representation and bitwise operators for compact state and O(1) constant-time operations. SDE-3 mastery: masking, subset enumeration, bitmask DP, and XOR tries.

---

## Theory & Mental Models

**What it is.** Operations directly on the binary representations of integers — 2–10× faster than arithmetic on modern CPUs. Core invariant: each bit is an independent boolean flag; bitwise ops process all 32/64 flags simultaneously in a single instruction.

**Why it exists.** Integer hardware supports AND/OR/XOR/SHIFT natively at the register level. Problems with small N (≤ 20) or intrinsic binary structure (power-of-two checks, flag sets, XOR cancellation) collapse from O(N) or O(2^N) loops to O(1) or O(N × 32) with the right bit operator.

**The mental model.** A row of 32 light switches. AND = "keep only the switches that are on in both rows"; OR = "turn on any switch that is on in either row"; XOR = "flip switches where the two rows differ"; shift left = double the binary number (multiply by 2).

**Complexity at a glance.**

| Operation | Time | Space |
| :--- | :--- | :--- |
| Any single bitwise op (AND, OR, XOR, shift) | O(1) | O(1) |
| Count set bits (Brian Kernighan) | O(k), k = #set bits | O(1) |
| Bitmask DP (N ≤ 20) | O(2^N × N) | O(2^N × N) |
| XOR Trie (max XOR pair) | O(N × 32) | O(N × 32) |
| Subset enumeration over all masks | O(3^N) total | O(1) extra |

**When to reach for it.**
- Power-of-two checks: `n > 0 and (n & (n-1)) == 0`.
- Finding a unique element among pairs: XOR cancellation.
- Subset enumeration when N ≤ 20 — bitmask DP replaces backtracking.
- Toggling feature flags / visited states as a single integer.
- Maximum XOR of two numbers in an array — XOR trie.

**When NOT to use it.**
- Readability matters and the problem has no intrinsic bit structure — use plain arithmetic.
- N > 20 for bitmask DP — state space is 2^N > 10^6; use regular DP or backtracking with pruning.
- 32-bit overflow simulation in Python — Python integers are arbitrary precision; always mask with `& 0xFFFFFFFF` explicitly.

**Common mistakes.**
- Python `~x` equals `-(x+1)`, not a 32-bit flip — use `x ^ 0xFFFFFFFF` for 32-bit complement.
- Forgetting `n > 0` in power-of-two check — `0 & (0-1) == 0` is true but 0 is not a power of 2.
- Signed vs unsigned right-shift behavior in Java/C++ (`>>>` vs `>>`); Python always arithmetic.
- Not masking with `& 0xFFFFFFFF` when simulating 32-bit wrap-around in Python.

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
> **Python integer gotcha — the #1 interview trap**: Python integers have **arbitrary precision** — there is no 32-bit overflow. When a problem says "treat as 32-bit unsigned integer", you must mask with `& 0xFFFFFFFF` after operations to simulate wrap-around.
> ```python
> # WRONG: ~x gives -(x+1) in Python
> print(bin(~5))  # output: -0b110
> 
> # CORRECT: XOR with all 1s for 32-bit complement
> print(bin(5 ^ 0xFFFFFFFF))  # output: 0b11111111111111111111111111111010
> ```
> Always clarify the language's integer model with your interviewer.

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

```python
def single_number_iii(nums: list[int]) -> list[int]:
    # 1. XOR all elements to get xor_sum = x ^ y
    xor_sum = reduce(xor, nums)
    
    # 2. Find the lowest set bit in xor_sum (this bit differs between x and y)
    lowest_set_bit = xor_sum & (-xor_sum)
    
    # 3. Partition array into two groups based on that bit and XOR each group
    x = y = 0
    for num in nums:
        if num & lowest_set_bit:
            x ^= num
        else:
            y ^= num
            
    return [x, y]

#### Common Variants & Twists
1. **Single Number II**:
   - **What (The Problem & Goal):** Every element appears three times except for one which appears exactly once.
   - **How (Intuition & Mental Model):** XOR cancellation fails here because `x ^ x ^ x = x`. Instead, count the number of set bits at each of the 32 bit positions across all numbers. The remainder of each count when divided by 3 (`count % 3`) will be the bits of the unique number.
2. **Single Number III**:
   - **What (The Problem & Goal):** Two elements appear once, and all other elements appear twice.
   - **How (Intuition & Mental Model):** XORing all numbers gives `xor_sum = x ^ y`. Since `x` and `y` are distinct, `xor_sum` must have at least one set bit. Find the lowest set bit using `diff = xor_sum & (-xor_sum)`. This bit exists in either `x` or `y`, but not both. Partition the array into two groups based on this bit and XOR each group separately to find the two unique numbers.
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

#### Common Variants & Twists
1. **Counting Bits (DP)**:
   - **What (The Problem & Goal):** For every number `i` in the range `[0, n]`, return an array of the number of 1-bits in their binary representation.
   - **How (Intuition & Mental Model):** This is a DP twist. Notice that `i >> 1` is a number we've already processed. The number of bits in `i` is the number of bits in `i >> 1` plus 1 if `i` is odd (`i & 1`). `dp[i] = dp[i >> 1] + (i & 1)`.
2. **Hamming Distance**:
   - **What (The Problem & Goal):** Calculate the number of positions at which the corresponding bits of two integers are different.
   - **How (Intuition & Mental Model):** XOR the two numbers (`x ^ y`) to get a number where bits are set only at differing positions. Then use Brian Kernighan's algorithm to count the set bits in the result.
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

#### Common Variants & Twists
1. **Generalized Subset Sum**:
   - **What (The Problem & Goal):** Check if any subset of numbers sums to a specific `target`.
   - **How (Intuition & Mental Model):** Iterate through all `2^N` masks. For each mask, calculate the sum of elements corresponding to set bits. If the sum matches the target, return `True`. This is effective for `N <= 20`.
2. **Generate All Possible String Permutations via Bitmask**:
   - **What (The Problem & Goal):** Given a string, generate all subsequences.
   - **How (Intuition & Mental Model):** Use a bitmask where each bit represents whether to include the character at that index in the current subsequence.
```

### O(3^N) Submask Enumeration (Advanced DP)

> [!IMPORTANT]
> **The Click Moment**: You are doing Bitmask DP, but instead of adding one element at a time, you need to transition by choosing an entire **subset** of the available elements (e.g., assigning a subset of tasks to one worker). 

If you iterate `0` to `mask` checking `(sub & mask) == sub`, that's O(4^N). The SDE-3 trick is to generate *only* the valid submasks directly.

```python
def process_submasks(mask: int):
    sub = mask
    while sub:
        # process(sub)
        sub = (sub - 1) & mask  # The magic step: subtract 1, then clear invalid bits
```

**Complexity Insight**: If you run this loop inside an outer loop over all `2^N` masks, the total number of inner loop executions across all masks is exactly `3^N`. This non-obvious bound separates SDE-3 candidates in DP optimization questions.

---

### Power of Two Check

> [!IMPORTANT]
> **The Click Moment**: "Is N a power of 2?" — OR — "exactly one bit is set" — OR — memory allocator / block-size validation problems.

```python
def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0

#### Common Variants & Twists
1. **Power of Four**:
   - **What (The Problem & Goal):** Check if a number is a power of 4.
   - **How (Intuition & Mental Model):** First, check if it's a power of 2 using `n > 0 and (n & (n-1)) == 0`. Then, ensure the only set bit is at an even position. Use the mask `0x55555555` (binary `010101...`) to check if `n & 0x55555555` is non-zero.
2. **Find the Single Bit Position**:
   - **What (The Problem & Goal):** Given a power of 2, find the index of the only set bit.
   - **How (Intuition & Mental Model):** Use `n.bit_length() - 1` or calculate it using `math.log2(n)`.
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

#### Common Variants & Twists
1. **Smallest Sufficient Team**:
   - **What (The Problem & Goal):** Given a list of required skills and people with specific skills, find the smallest group of people that covers all required skills.
   - **How (Intuition & Mental Model):** Represent the set of required skills as a bitmask of length `M`. `dp[mask]` stores the smallest list of people to achieve the skill set `mask`. For each person, update `dp[mask | person_skills] = min(dp[mask | person_skills], dp[mask] + [person])`.
2. **Can I Win?**:
   - **What (The Problem & Goal):** Two players take turns picking numbers from `1` to `maxInt`. The first player to reach a total sum wins. Can the first player force a win?
   - **How (Intuition & Mental Model):** Use a bitmask to represent the set of available numbers. Use memoized recursion `solve(current_sum, used_mask)` to determine if the current state is a winning or losing state for the player whose turn it is.
```

---

### Bitmask + BFS (State Space Search)

> [!IMPORTANT]
> **The Click Moment**: "Find the shortest path visiting all nodes" — BUT — nodes can be visited multiple times. Standard BFS fails because you can't just use a `visited_nodes` set. 

- **Idea**: The state of the BFS is not just the `current_node`, but the tuple `(current_node, visited_bitmask)`. You only stop exploring if you reach the *exact same node* with the *exact same visited mask*.
- **Complexity**: O(N × 2^N) states.

```python
def shortest_path_all_nodes(graph: list[list[int]]) -> int:
    n = len(graph)
    target_mask = (1 << n) - 1
    
    from collections import deque
    # Queue stores: (node, mask, steps)
    # Start BFS from all nodes simultaneously
    q = deque([(i, 1 << i, 0) for i in range(n)])
    visited = {(i, 1 << i) for i in range(n)}
    
    while q:
        node, mask, steps = q.popleft()
        if mask == target_mask:
            return steps
            
        for neighbor in graph[node]:
            next_mask = mask | (1 << neighbor)
            state = (neighbor, next_mask)
            if state not in visited:
                visited.add(state)
                q.append((neighbor, next_mask, steps + 1))
                
    return 0

#### Common Variants & Twists
1. **Find Shortest Path with Keys and Locks**:
   - **What (The Problem & Goal):** Find the shortest path to a target in a grid containing keys and locks. You can only open a lock if you have the corresponding key.
   - **How (Intuition & Mental Model):** Your BFS state is `(r, c, keys_mask)`. When you pick up a key, update the `keys_mask`. When you hit a lock, only proceed if `keys_mask` has the corresponding bit set.
2. **Bus Routes (via Mask)**:
   - **What (The Problem & Goal):** Find the minimum number of buses to take to get from source to destination.
   - **How (Intuition & Mental Model):** While typically BFS on a graph of routes, if the number of routes is small, you can use a mask to track which routes have been taken. This ensures we don't circle through already-visited lines.
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

#### Common Variants & Twists
1. **Maximum XOR with an Element From Array**:
   - **What (The Problem & Goal):** Given an array and queries `(x, m)`, find the max XOR of `x` with any `nums[i] <= m`.
   - **How (Intuition & Mental Model):** Offline query processing. Sort both the array and the queries by their limit `m`. Gradually insert elements into the XOR Trie as you iterate through the sorted queries.
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

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **[Single Number](../../google-sde2/PROBLEM_DETAILS.md#single-number)** | XOR Cancellation | "Pairs cancel" | `reduce(xor, nums)` | Only works when all others appear **exactly twice**. |
| **[Single Number II](../../google-sde2/PROBLEM_DETAILS.md#single-number-ii)** | "Appear 3× except one" | Count each bit mod 3 across all nums | XOR alone doesn't work; need separate mod-3 bit counter. |
| **Power of Two** | "Single bit set" | `n > 0 and n & (n-1) == 0` | `n = 0` satisfies `n & (n-1) == 0` but is not a power of 2. |
| **Reverse Bits** | "Bit symmetry" | Shift and OR, 32 iterations | Must pad to exactly 32 bits; Python needs `& 0xFFFFFFFF`. |
| **Hamming Distance** | "Differing bits between x and y" | `count_set_bits(x ^ y)` | Watch for signed integer representation in Java/C++. |
| **Counting Bits** | "Reuse sub-results" | `dp[i] = dp[i >> 1] + (i & 1)` | Recognize as 1D DP, not just a loop with bit tricks. |
| **Find Missing Number** | "One missing from 0..N" | `xor(0..N) ^ xor(nums)` | Only works when **exactly one** number is missing. |
| **Sum Without `+`** | "Add using bits" | XOR for sum, AND<<1 for carry, loop until carry=0 | Python needs `& 0xFFFFFFFF` mask; infinite loop risk without it. |
| **Smallest Sufficient Team** | "Cover all skills, min people" | Bitmask DP on skill union | Model each person's skills as a bitmask; 2^N states. |
| **Number of 1 Bits** [E] | "Count set bits (popcount)" | Brian Kernighan: `n &= (n-1)` clears lowest set bit; repeat until 0 | Alternative: `bin(n).count('1')` in Python; Brian Kernighan is language-agnostic. |
| **Reverse Bits** [E] | "Reverse all 32 bits" | Shift result left and OR in LSB of n; shift n right; repeat 32 times | Caching 8-bit chunks speeds repeated calls — mention as follow-up. |
| **Missing Number** [E] | "Find missing in [0,N]" | `XOR(0..N) ^ XOR(nums)` cancels all present values | Sum approach also O(N) O(1) but risks overflow for large N in non-Python languages. |
| **Number Complement** [E] | "Flip all bits of number's binary representation" | Create mask of all 1s with same bit length; XOR with mask | `mask = (1 << num.bit_length()) - 1`; XOR flips all bits within that width. |
| **Bitwise AND of Numbers Range** [M] | "AND of all numbers in [left, right]" | Right-shift both until equal; that common prefix is the answer | The differing suffix bits all become 0 due to a number in the range having 0 in that position. |
| **Decode XORed Array** [M] | "Recover original array from XOR differences" | `a[0]` is given; `a[i] = encoded[i-1] ^ a[i-1]` | Straightforward once you know `a XOR b = c → b = a XOR c`. |
| **Divide Two Integers** [M] | "Divide without `*`, `/`, `%`" | Bit-shift divisor left until it exceeds dividend; subtract and accumulate | Handle overflow: `INT_MIN / -1 = INT_MAX + 1` → clamp. Work in negatives to avoid unsigned issue. |
| **UTF-8 Validation** [M] | "Check if byte sequence is valid UTF-8" | Check leading bits per byte; count continuation bytes | Continuation bytes must start with `10`; count how many follow-bytes expected from first byte. |
| **Maximum XOR of Two Numbers** [M] | "Largest XOR of any pair" | Build XOR Trie or use prefix greedy with set | Trie approach: insert all numbers; for each number greedily pick opposite bit. O(32N). |
| **Find Two Non-Repeating Numbers** [H] | "Two numbers appear once, rest twice" | `diff = xor_sum & (-xor_sum)`; partition array | The set bit distinguishes x and y — any set bit works; use lowest for simplicity: `diff & (-diff)`. |
| **Shortest Path Visiting All Nodes** [H] | "Shortest path touching all nodes, revisits allowed" | BFS with state `(node, visited_mask)` | Standard BFS fails when revisits are needed. Bitmask captures the "history" to prevent infinite loops while allowing necessary revisits. |

---

## Quick Revision Triggers

- "Check / set / clear the k-th bit" → `n >> k & 1`, `n | (1<<k)`, `n & ~(1<<k)`.
- "Count set bits" → `bin(n).count('1')` or `n & (n-1)` loop or `popcount`.
- "Find the single non-repeating element; all others appear twice" → XOR all elements.
- "Enumerate all subsets of N items (N ≤ 20)" → bitmask `0` to `(1<<N)-1`; each bit = include/exclude.
- "Maximize XOR of two numbers in an array" → XOR Trie; greedy bit-by-bit from MSB.
- "In Python, `~x` gives `-(x+1)`, not the unsigned complement" → mask with `& 0xFFFFFFFF` for 32-bit semantics.
- "DP state is a subset of N elements (N ≤ 20)" → bitmask DP, O(2^N × N) time.

---

## See also

- [Dynamic Programming](dynamic-programming/README.md) — bitmask DP and O(3^N) subset enumeration
- [Patterns Master](../../../reference/patterns/patterns-master.md) — bitmask recognition triggers
- [Trie](../data-structures/trie.md) — XOR Trie for maximum XOR pair
