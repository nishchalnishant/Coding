# Stock Trading DP — State Machine Approach

Six LC stock problems unified under one `dp[i][k][holding]` state machine. For the broader DP guide see [README.md](README.md).

---

## Theory — The Unified State Machine

All stock problems share the same structure:

```
State: dp[i][k][0 or 1]
  i       = day index (0 to n-1)
  k       = transactions remaining (or unlimited)
  holding = 0 (no stock held) | 1 (stock held)

Transitions:
  dp[i][k][0] = max(dp[i-1][k][0],          # rest
                    dp[i-1][k][1] + prices[i])  # sell today
  dp[i][k][1] = max(dp[i-1][k][1],           # rest
                    dp[i-1][k-1][0] - prices[i]) # buy today

Base cases:
  dp[-1][k][0] = 0      (before day 0, no stock, any k)
  dp[-1][k][1] = -inf   (can't hold stock before day 0)
  dp[i][0][0]  = 0      (0 transactions left, no stock)
  dp[i][0][1]  = -inf   (can't hold stock with 0 transactions left)
```

> [!IMPORTANT]
> **Transaction = 1 buy + 1 sell.** Decrement `k` on **buy** (not sell). This way `k` tracks remaining complete transactions.

---

## Problem 1 — Best Time to Buy and Sell Stock I (LeetCode 121)

**k = 1 transaction, no cooldown, no fee.**

```python
def max_profit_1(prices: list[int]) -> int:
    min_price = float('inf')
    max_profit = 0
    for p in prices:
        min_price = min(min_price, p)
        max_profit = max(max_profit, p - min_price)
    return max_profit
```

> [!TIP]
> With k=1, this degenerates to "buy at global min, sell at global max after the min." O(N) greedy scan suffices; no DP table needed.

---

## Problem 2 — Best Time to Buy and Sell Stock II (LeetCode 122)

**k = unlimited transactions, no cooldown, no fee.** Buy and sell on the same day is allowed (effectively: you can hold on any day).

```python
def max_profit_2(prices: list[int]) -> int:
    # Greedy: capture every upward move
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            profit += prices[i] - prices[i-1]
    return profit
```

**DP formulation (unlimited k):**

```python
def max_profit_2_dp(prices: list[int]) -> int:
    hold, free = -prices[0], 0
    for p in prices[1:]:
        hold, free = max(hold, free - p), max(free, hold + p)
    return free
```

> [!TIP]
> With unlimited k, the DP collapses to 2 states: `hold` and `free` (not holding). This is equivalent to capturing all profitable day-to-day increases.

---

## Problem 3 — Best Time to Buy and Sell Stock III (LeetCode 123)

**k = 2 transactions max.**

```python
def max_profit_3(prices: list[int]) -> int:
    # Explicit 4 states: buy1, sell1, buy2, sell2
    buy1 = buy2 = float('-inf')
    sell1 = sell2 = 0
    for p in prices:
        buy1  = max(buy1,  -p)           # best profit after 1st buy
        sell1 = max(sell1, buy1 + p)     # best profit after 1st sell
        buy2  = max(buy2,  sell1 - p)    # best profit after 2nd buy
        sell2 = max(sell2, buy2 + p)     # best profit after 2nd sell
    return sell2
```

**Why this works:** `sell1 - p` means: profit from first transaction, minus cost of buying again. Propagating `sell1` into `buy2` captures the chaining of two transactions in O(N) time.

> [!TIP]
> Generalize: for k=3, add `buy3 = max(buy3, sell2 - p)` and `sell3 = max(sell3, buy3 + p)`. The pattern scales linearly.

---

## Problem 4 — Best Time to Buy and Sell Stock IV (LeetCode 188)

**k = at most K transactions.**

**Edge case:** if `2K >= N`, unlimited transactions (Problem 2). Otherwise, use O(K×N) DP.

```python
def max_profit_4(k: int, prices: list[int]) -> int:
    n = len(prices)
    if n == 0: return 0

    # If k >= n//2, effectively unlimited
    if k >= n // 2:
        return sum(max(0, prices[i] - prices[i-1]) for i in range(1, n))

    # dp[j][0] = max profit with j transactions remaining, not holding
    # dp[j][1] = max profit with j transactions remaining, holding
    dp = [[0, float('-inf')] * 1 for _ in range(k + 1)]
    dp = [[0, float('-inf')] for _ in range(k + 1)]

    for p in prices:
        for j in range(k, 0, -1):          # iterate backwards to avoid using updated values
            dp[j][0] = max(dp[j][0], dp[j][1] + p)    # sell
            dp[j][1] = max(dp[j][1], dp[j-1][0] - p)  # buy (use j-1 free state)
    return dp[k][0]
```

> [!CAUTION]
> Iterate `j` from `k` down to `1` to avoid using the updated `dp[j-1][0]` value (which has already been modified in the current price iteration). Think of this like backward iteration in 0/1 knapsack.

---

## Problem 5 — Best Time to Buy and Sell Stock with Cooldown (LeetCode 309)

**k = unlimited, but must wait 1 day after selling before buying again.**

**States:**
- `hold` — currently holding stock
- `sold` — just sold today (must cool down tomorrow)
- `rest` — not holding, not just sold (can buy)

```python
def max_profit_cooldown(prices: list[int]) -> int:
    hold = float('-inf')
    sold = 0
    rest = 0
    for p in prices:
        prev_sold = sold
        sold = hold + p           # sell today: was holding
        hold = max(hold, rest - p)  # buy today: must come from rest (not sold)
        rest = max(rest, prev_sold) # rest: either stayed resting or came from cooldown
    return max(sold, rest)
```

> [!TIP]
> The key: you can only **buy** from the `rest` state, not immediately after `sold`. The `prev_sold` variable ensures we use yesterday's `sold` value (not today's updated one) when computing `rest`.

---

## Problem 6 — Best Time to Buy and Sell Stock with Transaction Fee (LeetCode 714)

**k = unlimited, but pay `fee` per transaction (on sell).**

```python
def max_profit_with_fee(prices: list[int], fee: int) -> int:
    hold = -prices[0]
    free = 0
    for p in prices[1:]:
        hold = max(hold, free - p)
        free = max(free, hold + p - fee)   # subtract fee on sell
    return free
```

> [!TIP]
> Same as Problem 2 but subtract `fee` on every sell. The fee can be applied at buy OR sell — just be consistent. Applying at sell (`hold + p - fee`) is standard.

---

## Full State Machine Summary

| Variant | k | Extra Constraint | Code Pattern |
| :--- | :--- | :--- | :--- |
| **I** | 1 | None | Greedy: track `min_price` |
| **II** | ∞ | None | Greedy: capture all upward moves |
| **III** | 2 | None | 4 explicit states: `buy1, sell1, buy2, sell2` |
| **IV** | K | None | 2D DP: `dp[k][0/1]`; backward k-loop |
| **Cooldown** | ∞ | 1-day cooldown after sell | 3 states: `hold, sold, rest` |
| **Fee** | ∞ | Fee per transaction | 2 states + `fee` subtracted on sell |

---

## Interview Questions — Logic & Trickiness

| Problem | LC # | Click Moment | Core Trick | Gotcha |
| :--- | :--- | :--- | :--- | :--- |
| **Stock I** | 121 | One buy, one sell | Track running minimum | Answer = max(price - min_seen_so_far) |
| **Stock II** | 122 | Unlimited transactions | Capture all upward slopes | Holding on same day = 0 gain; greedy is optimal |
| **Stock III** | 123 | Exactly 2 transactions | Chain `sell1` into `buy2` | `sell2` is the answer, not `sell1` |
| **Stock IV** | 188 | K transactions | Backwards k-loop in 1D DP | If `2k ≥ n`, reduce to unlimited case |
| **Cooldown** | 309 | Can't buy day after sell | 3-state machine | Use `prev_sold` to avoid using today's sell value |
| **With Fee** | 714 | Fee per transaction | Subtract fee on sell | Fee at buy works too — don't apply at both |

---

## Common Mistakes

> [!CAUTION]
> **Stock III / IV**: Decrement `k` on **buy**, not sell. If you count k on sell, the recurrence produces off-by-one transaction counts.

> [!CAUTION]
> **Cooldown**: Using `sold` (today's value) when computing `rest` in the same iteration gives wrong results. Always capture `prev_sold = sold` before updating.

> [!TIP]
> **General tip**: Start by solving the unlimited-k version (Problem 2) to understand the base structure, then add constraints (k limit, cooldown, fee) one at a time. Each variant adds one constraint to the same state machine.

---

## See also

- [README.md](README.md) — DP overview and 4-step framework
- [dp-aditya-verma.md](dp-aditya-verma.md) — Knapsack and Fibonacci patterns
- [questions-bank.md](questions-bank.md) — Tiered drill questions including all 6 stock variants
