from __future__ import annotations

from typing import List, Tuple


class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def redundant_connection(n: int, edges: List[Tuple[int, int]]) -> Tuple[int, int]:
    """Nodes are assumed 1..n; returns an edge that forms a cycle."""
    dsu = DSU(n + 1)
    last = (-1, -1)
    for u, v in edges:
        if not dsu.union(u, v):
            last = (u, v)
    return last

