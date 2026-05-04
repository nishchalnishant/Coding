# Probability & Combinatorics DP

DP problems involving expected values, counting paths, game theory, and combinatorial structures. For the DP foundation see [README.md](README.md).

---

## Theory — Expected Value DP

**Expected value DP** computes E[outcome] when transitions are probabilistic. The state is `dp[state] = expected value starting from this state`.

**Recurrence pattern:**
```
dp[state] = Σ over transitions t:
                prob(t) * (cost(t) + dp[next_state(t)])
```

**Key:** Solve the system of equations — sometimes states form cycles (random walks) requiring algebraic substitution.

---

## 1. Knight Probability in Chessboard (LeetCode 688)

**Problem:** N×N board. Knight starts at `(r, c)`. After K moves, probability it's still on board.

**State:** `dp[k][i][j]` = probability of being at `(i,j)` after `k` moves.

```python
def knight_probability(n: int, k: int, row: int, col: int) -> float:
    moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
    # dp[i][j] = probability of being at (i,j) at current step
    dp = [[0.0]*n for _ in range(n)]
    dp[row][col] = 1.0

    for _ in range(k):
        ndp = [[0.0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if dp[i][j] == 0: continue
                for di, dj in moves:
                    ni, nj = i+di, j+dj
                    if 0 <= ni < n and 0 <= nj < n:
                        ndp[ni][nj] += dp[i][j] / 8.0
        dp = ndp

    return sum(dp[i][j] for i in range(n) for j in range(n))
```

> [!TIP]
> Work **forwards** (probability distribution propagation) instead of backwards. Each step, spread probability from each cell to its 8 neighbors (with 1/8 each). Only on-board cells accumulate; off-board transitions are simply discarded.

---

## 2. Soup Servings (LeetCode 808)

**Problem:** Two soups, serve from A and B with 4 operations of varying amounts. Probability that A empties first (+ half prob of both emptying simultaneously).

**Key insight:** For large N (≥ 4800), the answer converges to 1.0 due to statistical bias toward A running out first.

```python
def soup_servings(n: int) -> float:
    if n >= 4800:
        return 1.0   # converges asymptotically

    # Scale down: all operations are multiples of 25
    n = (n + 24) // 25

    from functools import lru_cache
    @lru_cache(maxsize=None)
    def dp(a: int, b: int) -> float:
        if a <= 0 and b <= 0: return 0.5   # both empty simultaneously
        if a <= 0: return 1.0              # A empties first
        if b <= 0: return 0.0              # B empties first
        return 0.25 * (dp(a-4, b) + dp(a-3, b-1) + dp(a-2, b-2) + dp(a-1, b-3))

    return dp(n, n)
```

---

## 3. New 21 Game (LeetCode 837)

**Problem:** Draw numbers 1..maxPts until total ≥ n. Probability total ≤ maxN.

**State:** `dp[x]` = probability of reaching exactly score `x`.

**Optimization:** Use a sliding window sum to compute `dp[x]` in O(1) each step.

```python
def new21game(n: int, k: int, maxPts: int) -> float:
    if k == 0 or n >= k + maxPts:
        return 1.0  # always win

    dp = [0.0] * (n + 1)
    dp[0] = 1.0
    window_sum = 1.0   # sum of dp[max(0, x-maxPts)..x-1]
    result = 0.0

    for x in range(1, n + 1):
        dp[x] = window_sum / maxPts
        if x < k:
            window_sum += dp[x]      # still drawing
        else:
            result += dp[x]          # score in [k, n] — wins
        if x >= maxPts:
            window_sum -= dp[x - maxPts]   # slide window

    return result
```

---

## 4. Dice Roll Simulation (LeetCode 1223)

**Problem:** Roll a dice n times. Each face `f` can appear at most `rollMax[f]` consecutive times. Count distinct sequences.

**State:** `dp[i][f][c]` = ways to fill `i` positions where last face is `f` with consecutive count `c`.

```python
def die_simulator(n: int, rollMax: list[int]) -> int:
    MOD = 10**9 + 7
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(rolls_left: int, last_face: int, consec: int) -> int:
        if rolls_left == 0: return 1
        total = 0
        for face in range(6):
            if face == last_face:
                if consec < rollMax[face]:
                    total += dp(rolls_left - 1, face, consec + 1)
            else:
                total += dp(rolls_left - 1, face, 1)
        return total % MOD

    return dp(n, -1, 0)
```

---

## 5. Stone Game (Nim / Game Theory DP)

### Stone Game I (LeetCode 877)

**Problem:** Alice and Bob alternately pick from either end of a pile array. Both play optimally. Does Alice win?

**Math fact:** Alice always wins (she picks first and piles are even in count). But the DP is instructive:

```python
def stone_game(piles: list[int]) -> bool:
    # Math: Alice always wins with even number of piles
    return True

def stone_game_dp(piles: list[int]) -> bool:
    """DP version: dp[i][j] = score difference (current - other) for piles[i..j]."""
    n = len(piles)
    dp = piles[:]  # dp[i] = piles[i] for single pile
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i] = max(piles[i] - dp[i+1], piles[j] - dp[i])
    return dp[0] > 0
```

### Stone Game II (LeetCode 1140)

**Problem:** Can take 1 to 2M piles; M updates based on how many piles taken. Maximize Alice's stones.

```python
def stone_game_ii(piles: list[int]) -> int:
    n = len(piles)
    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i+1] + piles[i]

    from functools import lru_cache
    @lru_cache(maxsize=None)
    def dp(i: int, M: int) -> int:
        if i + 2 * M >= n:
            return suffix[i]      # can take all remaining piles
        return suffix[i] - min(dp(i + x, max(M, x)) for x in range(1, 2*M+1))
    return dp(0, 1)
```

### Stone Game III (LeetCode 1406)

**Problem:** Take 1, 2, or 3 stones from the front each turn. Both optimal. Who wins?

```python
def stone_game_iii(stoneValue: list[int]) -> str:
    n = len(stoneValue)
    dp = [float('-inf')] * (n + 1)
    dp[n] = 0
    for i in range(n - 1, -1, -1):
        take = 0
        for k in range(1, 4):
            if i + k <= n:
                take += stoneValue[i + k - 1]
                dp[i] = max(dp[i], take - dp[i + k])
    score = dp[0]
    if score > 0: return "Alice"
    if score < 0: return "Bob"
    return "Tie"
```

> [!TIP]
> **Minimax insight:** `dp[i]` = max score difference (current player − opponent) from position `i`. If `dp[0] > 0` → Alice wins; `< 0` → Bob wins; `= 0` → tie.

---

## 6. Nim and Sprague-Grundy Theorem

**Nim game:** N piles of stones. Players alternately remove any number from one pile. Last to move wins. 

**Winner:** First player wins iff XOR of all pile sizes ≠ 0.

```python
def can_win_nim(piles: list[int]) -> bool:
    xor = 0
    for p in piles: xor ^= p
    return xor != 0
```

**Sprague-Grundy:** Assigns a Grundy number (nimber) to each game position. A position is a losing position iff its Grundy number = 0.

```python
from functools import lru_cache

def grundy(n: int, moves: list[int]) -> int:
    """Compute Grundy number for position n with given allowed move sizes."""
    @lru_cache(maxsize=None)
    def g(pos: int) -> int:
        reachable = set()
        for m in moves:
            if pos >= m:
                reachable.add(g(pos - m))
        # mex = minimum excludant
        mex = 0
        while mex in reachable:
            mex += 1
        return mex
    return g(n)
```

---

## 7. Egg Drop Problem (LeetCode 887)

**Problem:** `k` eggs, `n` floors. Find the minimum number of trials to determine the critical floor in the worst case.

### Approach 1 — Classic O(KN²) DP

**State:** `dp[k][n]` = min trials with `k` eggs and `n` floors.

```python
def super_egg_drop_n2(k: int, n: int) -> int:
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def dp(eggs: int, floors: int) -> int:
        if floors <= 1: return floors
        if eggs == 1: return floors      # must check every floor linearly
        lo, hi = 1, floors
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            breaks = dp(eggs - 1, mid - 1)    # egg breaks
            no_break = dp(eggs, floors - mid)  # egg survives
            if breaks < no_break:
                lo = mid
            elif breaks > no_break:
                hi = mid
            else:
                lo = hi = mid
        return 1 + min(max(dp(eggs-1, x-1), dp(eggs, floors-x)) for x in [lo, hi])
    return dp(k, n)
```

### Approach 2 — Inverted DP O(KN log N)

**Invert the problem:** `dp[m][k]` = maximum floors checkable with `m` trials and `k` eggs.

```python
def super_egg_drop(k: int, n: int) -> int:
    # dp[m][k] = max floors checkable with m moves and k eggs
    # dp[m][k] = dp[m-1][k-1] + 1 + dp[m-1][k]
    #              (below floor)    (above floor)
    m = 0
    dp = [0] * (k + 1)
    while dp[k] < n:
        m += 1
        new_dp = [0] * (k + 1)
        for j in range(1, k + 1):
            new_dp[j] = dp[j-1] + 1 + dp[j]
        dp = new_dp
    return m
```

> [!IMPORTANT]
> The inverted DP is O(K × answer) which is O(K × log N). This is the expected SDE-3 solution. The recurrence `dp[m][k] = dp[m-1][k-1] + 1 + dp[m-1][k]` comes from: drop egg at some floor — if it breaks, check `dp[m-1][k-1]` floors below; if it survives, check `dp[m-1][k]` floors above.

---

## 8. Catalan Numbers via DP

**Catalan(n)** = number of valid bracket sequences, BSTs with n nodes, paths avoiding diagonal, etc.

```python
def catalan(n: int) -> int:
    """Catalan(n) = C(2n,n) / (n+1) = sum_{i=0}^{n-1} Catalan(i)*Catalan(n-1-i)"""
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        for j in range(i):
            dp[i] += dp[j] * dp[i - 1 - j]
    return dp[n]

# Catalan sequence: 1, 1, 2, 5, 14, 42, 132, 429, ...
```

**Applications of Catalan(n):**
- Number of unique BSTs with n keys (LeetCode 96)
- Number of valid parenthesizations of n+1 matrices
- Number of monotone paths in n×n grid not crossing diagonal
- Number of full binary trees with n+1 leaves

---

## Interview Questions — Logic & Trickiness

| Problem | LC # | Type | Click Moment | Gotcha |
| :--- | :--- | :--- | :--- | :--- |
| **Knight Probability** | 688 | Expected value | Propagate probability forward | 8 moves; off-board transitions just disappear |
| **Soup Servings** | 808 | Probability DP | Asymptotic: return 1.0 for N ≥ 4800 | Always scale N down by 25 first |
| **New 21 Game** | 837 | Probability + sliding window | `window_sum` tracks Σdp[x-maxPts..x-1] | Sliding window prevents O(N·maxPts) |
| **Dice Roll Simulation** | 1223 | Count DP | State = `(rolls_left, last_face, consec_count)` | Rolling `face` again is OK if `consec < rollMax[face]` |
| **Stone Game I** | 877 | Game theory | Math: Alice always wins | DP insight: `dp[i] = piles[i] - dp[i+1]` (difference) |
| **Stone Game III** | 1406 | Minimax DP | `dp[i]` = score advantage from position i | `dp[i] = max over k=1,2,3 of (take_k - dp[i+k])` |
| **Egg Drop** | 887 | Inverted DP | Invert: "max floors with m moves and k eggs" | Standard DP is O(KN²); inverted is O(K log N) |
| **Unique BSTs** | 96 | Catalan DP | Root = i splits into left (i-1 nodes) and right (n-i nodes) | Answer = Catalan(n) |
| **Nim Game** | 292 | Sprague-Grundy | Win iff XOR of all piles ≠ 0 | Generalizes with Sprague-Grundy for multi-pile games |

---

## See also

- [README.md](README.md) — Core DP patterns
- [advanced-dp-optimizations.md](advanced-dp-optimizations.md) — SOS DP for bitmask subset sums
- [questions-bank.md](questions-bank.md) — Tiered drill including game theory problems
