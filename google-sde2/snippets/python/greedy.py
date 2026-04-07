from __future__ import annotations

from typing import List, Tuple


def jump_game_ii(nums: List[int]) -> int:
    """Minimum jumps to reach end (assumes reachable)."""
    jumps = 0
    end = 0
    furthest = 0
    for i in range(len(nums) - 1):
        furthest = max(furthest, i + nums[i])
        if i == end:
            jumps += 1
            end = furthest
    return jumps


def gas_station(gas: List[int], cost: List[int]) -> int:
    if sum(gas) < sum(cost):
        return -1
    start = 0
    tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start = i + 1
            tank = 0
    return start


def erase_overlap_intervals(intervals: List[Tuple[int, int]]) -> int:
    """Min removals so remaining intervals are non-overlapping."""
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])  # sort by end
    removed = 0
    last_end = intervals[0][1]
    for s, e in intervals[1:]:
        if s < last_end:
            removed += 1
        else:
            last_end = e
    return removed

