from __future__ import annotations

import random
from typing import List


def kth_largest(nums: List[int], k: int) -> int:
    """Quickselect average O(n). k is 1-based."""
    target = len(nums) - k

    def partition(lo: int, hi: int, pivot_idx: int) -> int:
        pivot = nums[pivot_idx]
        nums[pivot_idx], nums[hi] = nums[hi], nums[pivot_idx]
        store = lo
        for i in range(lo, hi):
            if nums[i] < pivot:
                nums[store], nums[i] = nums[i], nums[store]
                store += 1
        nums[store], nums[hi] = nums[hi], nums[store]
        return store

    lo, hi = 0, len(nums) - 1
    while True:
        pivot_idx = random.randint(lo, hi)
        p = partition(lo, hi, pivot_idx)
        if p == target:
            return nums[p]
        if p < target:
            lo = p + 1
        else:
            hi = p - 1

