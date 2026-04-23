from __future__ import annotations

from typing import List


def valid_parentheses(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: List[str] = []
    for ch in s:
        if ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
        else:
            stack.append(ch)
    return not stack


def daily_temperatures(temps: List[int]) -> List[int]:
    res = [0] * len(temps)
    stack: List[int] = []  # indices, decreasing temperatures
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            res[j] = i - j
        stack.append(i)
    return res


def largest_rectangle_area(heights: List[int]) -> int:
    """Monotonic increasing stack of indices; sentinel flush."""
    stack: List[int] = []
    best = 0
    for i in range(len(heights) + 1):
        cur = 0 if i == len(heights) else heights[i]
        while stack and cur < heights[stack[-1]]:
            h = heights[stack.pop()]
            left = stack[-1] + 1 if stack else 0
            best = max(best, h * (i - left))
        stack.append(i)
    return best

