from __future__ import annotations

from collections import Counter, deque
from typing import Deque, Dict, List


def longest_substring_without_repeating(s: str) -> int:
    left = 0
    last: Dict[str, int] = {}
    best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best


def min_window_substring(s: str, t: str) -> str:
    if not t:
        return ""
    need = Counter(t)
    have: Dict[str, int] = {}
    required = len(need)
    formed = 0
    best_len = float("inf")
    best_l = 0

    left = 0
    for right, ch in enumerate(s):
        have[ch] = have.get(ch, 0) + 1
        if ch in need and have[ch] == need[ch]:
            formed += 1

        while formed == required:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_l = left

            left_ch = s[left]
            have[left_ch] -= 1
            if left_ch in need and have[left_ch] < need[left_ch]:
                formed -= 1
            left += 1

    return "" if best_len == float("inf") else s[best_l : best_l + best_len]


def sliding_window_max(nums: List[int], k: int) -> List[int]:
    """Monotonic deque of indices (values decreasing)."""
    if k <= 0:
        return []
    q: Deque[int] = deque()
    out: List[int] = []
    for i, x in enumerate(nums):
        while q and nums[q[-1]] <= x:
            q.pop()
        q.append(i)

        if q[0] <= i - k:
            q.popleft()

        if i >= k - 1:
            out.append(nums[q[0]])
    return out

