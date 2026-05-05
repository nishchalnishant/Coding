# Advanced DP Optimizations

Techniques to reduce O(N²) or O(N²K) DP to O(N log N) or O(NK). For the DP foundation see [README.md](README.md).

---

## Overview

| Technique | Applicable When | Reduction |
| :--- | :--- | :--- |
| **Monotonic Deque (Sliding Window DP)** | `dp[i]` depends on `max/min` of a sliding window of previous values | O(N²) → O(N) |
| **Convex Hull Trick (CHT)** | Transition is linear: `dp[j] + a[j]*b[i]`; `b[i]` monotone | O(N²) → O(N) |
| **Li Chao Segment Tree** | CHT where `b[i]` is NOT monotone | O(N²) → O(N log N) |
| **Divide & Conquer Optimization** | `opt(i-1,j) ≤ opt(i,j)` (monotone optimal split) | O(N²) → O(N log N) |
| **SOS DP (Sum over Subsets)** | `f[mask] = sum of f[submask]` for all submasks | O(3^N) → O(N·2^N) |
| **Knuth-Yao Optimization** | Interval DP with quadrangle inequality | O(N³) → O(N²) |

---

## 1. Monotonic Deque Optimization (Sliding Window DP)

### When to use

`dp[i] = max/min over j in [i-k, i-1] of (dp[j] + cost)` where `k` is a fixed window size. A deque maintains the running max/min in O(1) amortized time.

### Template

```python
from collections import deque

def sliding_window_dp(nums: list[int], k: int) -> int:
    n = len(nums)
    dp = [0] * n
    dq = deque()   # stores indices; front = best (max) index in window

    for i in range(n):
        # Remove indices outside window [i-k, i-1]
        while dq and dq[0] < i - k:
            dq.popleft()

        # dp[i] = best from window + current cost
        dp[i] = (dp[dq[0]] if dq else 0) + nums[i]

        # Maintain deque: remove indices with worse dp values from back
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)

    return max(dp)
```

### Problem: Jump Game VI (LeetCode 1696)

Score = sum of selected elements; can jump 1 to k steps. Maximize score.

```python
def max_result(nums: list[int], k: int) -> int:
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    dq = deque([0])

    for i in range(1, n):
        # Remove out-of-window indices
        while dq and dq[0] < i - k:
            dq.popleft()
        dp[i] = dp[dq[0]] + nums[i]
        # Maintain decreasing deque
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)

    return dp[n-1]
```

### Problem: Sliding Window Maximum (LeetCode 239)

Not strictly DP, but uses the same deque pattern:

```python
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    dq = deque()   # stores indices; front = max index in current window
    result = []
    for i, x in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

> [!TIP]
> **Deque invariant:** Front = index of the maximum value; back = most recently added index. Deque is always in decreasing order of value. When the window moves, pop expired indices from the front.

---

## 2. Convex Hull Trick (CHT)

### When to use

Transition of the form: `dp[i] = min over j < i of (dp[j] + b[j] * a[i])` where `a[i]` is **monotonically increasing** (or we process queries sorted by `a[i]`).

Each candidate `j` defines a **line**: `y = b[j] * x + dp[j]`. We want the minimum y for each query x = `a[i]`. Maintaining a lower convex hull of lines lets us answer each query in O(1) (when x is monotone) or O(log N) (binary search).

### Template — Linear CHT (x monotonically increasing)

```python
class ConvexHullTrick:
    """Maintains lines y = m*x + b; queries minimum y for given x (x increasing)."""

    def __init__(self):
        self.lines = []   # (slope m, intercept b)
        self.ptr = 0      # pointer for monotone queries

    def _bad(self, l1, l2, l3):
        """True if l2 is never the minimum (lies above intersection of l1 and l3)."""
        m1, b1 = l1; m2, b2 = l2; m3, b3 = l3
        return (b3 - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m3)

    def add_line(self, m: int, b: int):
        new_line = (m, b)
        while len(self.lines) >= 2 and self._bad(self.lines[-2], self.lines[-1], new_line):
            self.lines.pop()
        self.lines.append(new_line)

    def query_min(self, x: int) -> int:
        """Query minimum y = m*x + b for monotone increasing x."""
        while self.ptr < len(self.lines) - 1:
            m1, b1 = self.lines[self.ptr]
            m2, b2 = self.lines[self.ptr + 1]
            if m1 * x + b1 >= m2 * x + b2:
                self.ptr += 1
            else:
                break
        m, b = self.lines[self.ptr]
        return m * x + b
```

### Example: Min Cost to Cut a Stick (with CHT)

`dp[i] = min over j of (dp[j] + cost(j, i))` where `cost` has a linear form.

> [!TIP]
> **CHT conditions to check:** (1) Transition = `dp[j] + f(j)*g(i)` for some functions f, g. (2) Either f(j) is monotone (add lines in order) OR g(i) is monotone (query in order). If both are monotone, use the linear O(N) CHT above. If only g(i) is sorted, use binary search on the hull. If neither is sorted, use Li Chao Tree (O(N log N)).

---

## 3. Divide & Conquer Optimization

### When to use

For DP of the form: `dp[i][j] = min over k in [lo, hi] of (dp[i-1][k] + cost(k+1, j))`

where the **optimal split point** `opt(i, j)` is **monotonically non-decreasing** in `j` (the quadrangle inequality / SMAWK condition): `opt(i, j) ≤ opt(i, j+1)`.

### Template

```python
def dp_divide_conquer(cost, n: int, layers: int) -> list[int]:
    """
    dp[l][j] = min cost to partition first j elements into l groups.
    cost(a, b) = cost of grouping elements a+1..b in one group.
    """
    INF = float('inf')
    prev = [cost(0, j) for j in range(n + 1)]
    prev[0] = 0

    for l in range(2, layers + 1):
        curr = [INF] * (n + 1)
        curr[0] = 0

        def solve(lo: int, hi: int, opt_lo: int, opt_hi: int):
            if lo > hi: return
            mid = (lo + hi) // 2
            best_k, best_val = opt_lo, INF
            for k in range(opt_lo, min(opt_hi, mid) + 1):
                val = prev[k] + cost(k, mid)
                if val < best_val:
                    best_val = val
                    best_k = k
            curr[mid] = best_val
            solve(lo, mid - 1, opt_lo, best_k)
            solve(mid + 1, hi, best_k, opt_hi)

        solve(1, n, 0, n - 1)
        prev = curr

    return prev

```

> [!CAUTION]
> Divide & Conquer optimization requires **verifying the monotone optimal split condition** before applying. If `opt(i,j)` is not monotone, this optimization produces wrong answers silently. Prove it holds via the quadrangle inequality: `cost(a,c) + cost(b,d) ≤ cost(a,d) + cost(b,c)` for `a ≤ b ≤ c ≤ d`.

---

## 4. SOS DP — Sum over Subsets

### When to use

Compute `f[mask] = sum of g[sub]` for all submasks `sub` of `mask`. The naïve O(3^N) approach (iterate all submasks) becomes O(N · 2^N) with SOS DP.

### Theory

For each bit position `i` from 0 to N-1:
`dp[mask] += dp[mask ^ (1 << i)]` if bit `i` is set in `mask`.

This is analogous to a multi-dimensional prefix sum over the hypercube.

```python
def sos_dp(g: list[int], n: int) -> list[int]:
    """
    Compute f[mask] = sum of g[sub] for all sub ⊆ mask.
    g: array of size 2^n
    n: number of bits
    """
    f = g[:]           # start with g values
    for i in range(n):
        for mask in range(1 << n):
            if mask >> i & 1:
                f[mask] += f[mask ^ (1 << i)]
    return f

# Example: f[mask] = count of subsets of mask (all g values = 1)
n = 3
g = [1] * (1 << n)  # each subset contributes 1
f = sos_dp(g, n)
# f[0b111] = 8 (all 2^3 subsets of {0,1,2})
```

> [!TIP]
> **SOS for "at most K bits" queries:** Replace `f[mask] += f[mask ^ (1<<i)]` with a superset sum by reversing: `if NOT (mask >> i & 1): f[mask] += f[mask | (1<<i)]`. This gives the sum of all g[sup] for all supersets of mask.

### Problem: Smallest Sufficient Team (LeetCode 1125)

```python
def smallest_sufficient_team(req_skills, people):
    n = len(req_skills)
    skill_idx = {s: i for i, s in enumerate(req_skills)}
    # Encode each person's skills as a bitmask
    person_masks = [0] * len(people)
    for i, skills in enumerate(people):
        for s in skills:
            if s in skill_idx:
                person_masks[i] |= 1 << skill_idx[s]

    FULL = (1 << n) - 1
    INF = float('inf')
    dp = [INF] * (FULL + 1)
    parent = [None] * (FULL + 1)
    dp[0] = 0; parent[0] = []

    for mask in range(FULL + 1):
        if dp[mask] == INF: continue
        for i, pm in enumerate(person_masks):
            new_mask = mask | pm
            if dp[new_mask] > dp[mask] + 1:
                dp[new_mask] = dp[mask] + 1
                parent[new_mask] = parent[mask] + [i]

    return parent[FULL]
```

---

## 5. Knuth-Yao Optimization

### When to use

Interval DP: `dp[i][j] = min over i≤k<j of (dp[i][k] + dp[k+1][j] + w(i,j))` where `w` satisfies the **quadrangle inequality** AND is a **monotone** weight function.

**Result:** The optimal split `opt[i][j]` satisfies `opt[i][j-1] ≤ opt[i][j] ≤ opt[i+1][j]`. This shrinks the inner loop from O(N) to O(1) amortized → O(N²) total.

```python
def knuth_yao(w: list[list[int]], n: int) -> list[list[int]]:
    INF = float('inf')
    dp  = [[0]*n for _ in range(n)]
    opt = [[0]*n for _ in range(n)]

    # Initialize
    for i in range(n):
        dp[i][i] = w[i][i]
        opt[i][i] = i

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = INF
            # Restrict k to [opt[i][j-1], opt[i+1][j]]
            k_lo = opt[i][j-1]
            k_hi = opt[i+1][j] if i+1 <= j else j
            for k in range(k_lo, min(k_hi, j-1) + 1):
                val = dp[i][k] + dp[k+1][j] + w[i][j]
                if val < dp[i][j]:
                    dp[i][j] = val
                    opt[i][j] = k

    return dp
```

---

## 6. WQS Binary Search (Aliens Trick)

### When to use

You must make **exactly K** "decisions" (e.g., transactions, jumps, groups) but K makes the DP 2D (`dp[i][k]`). If the answer is concave/convex in K, binary search on a penalty `λ` for each decision, solve the unconstrained (unlimited K) DP, then recover the K-decision answer.

**Idea:** Penalize each decision by `λ`. Binary search on `λ` to find the one where the optimal unconstrained solution uses exactly K decisions.

```python
def wqs_binary_search(prices: list[int], k: int) -> int:
    """Best Time to Buy/Sell Stock IV using WQS binary search."""
    n = len(prices)

    def solve(fee: int) -> tuple[int, int]:
        """Returns (max_profit, num_transactions) with penalty `fee` per transaction."""
        hold = (-prices[0] - fee, 1)   # (profit, transactions)
        free = (0, 0)
        for p in prices[1:]:
            new_hold = max(hold, (free[0] - p - fee, free[1] + 1))
            new_free = max(free, (hold[0] + p, hold[1]))
            hold, free = new_hold, new_free
        return free   # (profit, transactions)

    lo, hi = 0, max(prices)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        profit, txns = solve(mid)
        if txns >= k:
            lo = mid
        else:
            hi = mid - 1

    profit, txns = solve(lo)
    return profit + lo * k   # remove the penalty × k we added
```

> [!CAUTION]
> WQS binary search is an advanced competitive programming technique. In interviews, it's typically only expected at top-tier ICPC/competitive settings. Mention it as an optimization if the interviewer pushes for better than O(NK).

---

## Quick Decision Tree

```
O(N²) DP with a sliding window max/min dependency?
  └─ Yes → Monotonic Deque O(N)

dp[i] = min over j of (dp[j] + f(j)*g(i)), linear form?
  └─ g(i) monotone → Convex Hull Trick O(N)
  └─ g(i) not monotone → Li Chao Tree O(N log N)

Interval DP, optimal split monotone (quadrangle inequality)?
  └─ cost has quadrangle + monotone weight → Knuth-Yao O(N²)
  └─ otherwise → Divide & Conquer O(N log N)

f[mask] = sum over all submasks?
  └─ SOS DP O(N · 2^N)

Exactly-K decisions, concave/convex in K?
  └─ WQS binary search / Aliens Trick
```

---

## See also

- [README.md](README.md) — Core DP patterns
- [dp-aditya-verma.md](dp-aditya-verma.md) — Bitmask DP and interval DP
- [questions-bank.md](questions-bank.md) — Hard problems that use these techniques
