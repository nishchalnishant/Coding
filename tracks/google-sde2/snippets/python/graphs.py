from __future__ import annotations

import heapq
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Deque, Dict, List, Optional, Set, Tuple


def topo_kahn(n: int, edges: List[Tuple[int, int]]) -> List[int]:
    """Edges are u -> v."""
    adj: Dict[int, List[int]] = defaultdict(list)
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q: Deque[int] = deque([i for i in range(n) if indeg[i] == 0])
    order: List[int] = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else []


def num_islands(grid: List[List[str]]) -> int:
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    seen: Set[Tuple[int, int]] = set()
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def bfs(sr: int, sc: int) -> None:
        q = deque([(sr, sc)])
        seen.add((sr, sc))
        while q:
            r, c = q.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen and grid[nr][nc] == "1":
                    seen.add((nr, nc))
                    q.append((nr, nc))

    ans = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "1" and (r, c) not in seen:
                ans += 1
                bfs(r, c)
    return ans


def rotting_oranges(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    q: Deque[Tuple[int, int]] = deque()
    fresh = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 2:
                q.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    minutes = 0
    while q and fresh:
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
        minutes += 1
    return minutes if fresh == 0 else -1


@dataclass
class Node:
    val: int
    neighbors: List["Node"]


def clone_graph(node: Optional[Node]) -> Optional[Node]:
    if not node:
        return None
    copies: Dict[Node, Node] = {}
    q = deque([node])
    copies[node] = Node(node.val, [])
    while q:
        cur = q.popleft()
        for nei in cur.neighbors:
            if nei not in copies:
                copies[nei] = Node(nei.val, [])
                q.append(nei)
            copies[cur].neighbors.append(copies[nei])
    return copies[node]


def dijkstra(n: int, edges: List[Tuple[int, int, int]], src: int) -> List[int]:
    """Edges are (u,v,w), directed. Returns dist (inf=unreachable)."""
    adj: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [10**30] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

