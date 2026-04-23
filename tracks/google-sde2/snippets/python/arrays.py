from __future__ import annotations

from collections import defaultdict
from typing import List, Tuple


def two_sum(nums: List[int], target: int) -> List[int]:
    """Return indices of one pair summing to target; empty if none."""
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
    return []


def subarray_sum_equals_k(nums: List[int], k: int) -> int:
    """Count subarrays with sum k. Works with negative numbers."""
    prefix = 0
    count_by_prefix = defaultdict(int)
    count_by_prefix[0] = 1
    ans = 0
    for x in nums:
        prefix += x
        ans += count_by_prefix[prefix - k]
        count_by_prefix[prefix] += 1
    return ans


def max_subarray_sum(nums: List[int]) -> int:
    """Kadane: maximum sum of a non-empty contiguous subarray."""
    best = nums[0]
    cur = nums[0]
    for i in range(1, len(nums)):
        cur = max(nums[i], cur + nums[i])
        best = max(best, cur)
    return best


def product_except_self(nums: List[int]) -> List[int]:
    """No division. O(n) time, O(1) extra (excluding output)."""
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):
        out[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= nums[i]
    return out


def merge_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged

