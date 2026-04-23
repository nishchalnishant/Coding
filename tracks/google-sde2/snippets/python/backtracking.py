from __future__ import annotations

from typing import List


def subsets(nums: List[int]) -> List[List[int]]:
    res: List[List[int]] = []
    path: List[int] = []

    def dfs(i: int) -> None:
        if i == len(nums):
            res.append(path[:])
            return
        dfs(i + 1)
        path.append(nums[i])
        dfs(i + 1)
        path.pop()

    dfs(0)
    return res


def permutations(nums: List[int]) -> List[List[int]]:
    res: List[List[int]] = []
    used = [False] * len(nums)
    path: List[int] = []

    def dfs() -> None:
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i, x in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(x)
            dfs()
            path.pop()
            used[i] = False

    dfs()
    return res


def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """Unbounded: can reuse same index."""
    res: List[List[int]] = []
    path: List[int] = []
    candidates.sort()

    def dfs(start: int, remain: int) -> None:
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            x = candidates[i]
            if x > remain:
                break
            path.append(x)
            dfs(i, remain - x)
            path.pop()

    dfs(0, target)
    return res

