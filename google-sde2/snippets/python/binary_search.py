from __future__ import annotations

from typing import Callable, List


def lower_bound(a: List[int], x: int) -> int:
    """First index i such that a[i] >= x."""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def search_rotated(nums: List[int], target: int) -> int:
    """Rotated sorted array, distinct values."""
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:  # left half sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # right half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


def binary_search_on_answer(lo: int, hi: int, valid: Callable[[int], bool]) -> int:
    """Return smallest x in [lo,hi] with valid(x)=True, assuming monotonic valid."""
    while lo < hi:
        mid = (lo + hi) // 2
        if valid(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

