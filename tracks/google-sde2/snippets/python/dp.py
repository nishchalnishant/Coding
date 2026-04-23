from __future__ import annotations

from typing import List, Set


def house_robber(nums: List[int]) -> int:
    take = 0
    skip = 0
    for x in nums:
        take, skip = skip + x, max(skip, take)
    return max(take, skip)


def coin_change_min(coins: List[int], amount: int) -> int:
    INF = 10**9
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
    return -1 if dp[amount] >= INF else dp[amount]


def lis_length(nums: List[int]) -> int:
    """Patience sorting: O(n log n)."""
    tails: List[int] = []
    for x in nums:
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if tails[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(tails):
            tails.append(x)
        else:
            tails[lo] = x
    return len(tails)


def lcs_length(a: str, b: str) -> int:
    """O(mn) time, O(n) space."""
    if len(b) > len(a):
        a, b = b, a
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]


def edit_distance(a: str, b: str) -> int:
    """Levenshtein distance."""
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])
        prev = cur
    return prev[-1]


def word_break(s: str, word_dict: Set[str]) -> bool:
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for w in word_dict:
            if len(w) <= i and dp[i - len(w)] and s[i - len(w) : i] == w:
                dp[i] = True
                break
    return dp[n]

