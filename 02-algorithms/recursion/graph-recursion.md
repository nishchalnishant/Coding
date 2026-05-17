# Graph Recursion — DFS-Based Algorithms

Recursive DFS on graphs: traversal, connectivity, cycle detection, topological sort, and pathfinding. For the recursion foundation see [README.md](README.md).

---

## Theory — Graph DFS Template

**Why recursion for graphs?** DFS naturally maps to recursion: push onto call stack when visiting a node, pop on return. The key addition vs. tree DFS: **visited tracking** to avoid infinite loops on cycles.

**Core template:**
```python
def dfs(node, visited, graph):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited, graph)
```

**Key decisions:**
1. **Visited set vs visited array:** Set for arbitrary node labels; array for 0-indexed nodes.
2. **When to mark visited:** Before recursing (standard) prevents re-visiting. For backtracking problems (paths), mark on enter and unmark on exit.
3. **Return value:** True/False (path exists), int (count), list (path), or modify global.

> [!CAUTION]
> For graphs (unlike trees), always mark a node visited **before** recursing into its neighbors. Marking after can cause infinite recursion on cycles.

---

## Pattern 1 — Connected Components / Flood Fill

### Flood Fill (LC 733)

```python
def flood_fill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    original = image[sr][sc]
    if original == color: return image   # already the target color

    def dfs(r, c):
        if not (0 <= r < len(image) and 0 <= c < len(image[0])): return
        if image[r][c] != original: return
        image[r][c] = color              # mark in-place
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            dfs(r + dr, c + dc)

    dfs(sr, sc)
    return image
```

### Number of Islands (LC 200)

```python
def num_islands(grid: list[list[str]]) -> int:
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols): return
        if grid[r][c] != '1': return
        grid[r][c] = '#'    # mark visited in-place
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            dfs(r + dr, c + dc)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)   # sink the island
                count += 1

    return count
```

> [!TIP]
> Mutating the grid in-place (`grid[r][c] = '#'`) avoids a separate visited set. Restore if the problem requires the original grid unchanged.

### Connected Components in Undirected Graph (LC 323)

```python
def count_components(n: int, edges: list[list[int]]) -> int:
    from collections import defaultdict
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    count = 0
    for node in range(n):
        if node not in visited:
            dfs(node)
            count += 1
    return count
```

---

## Pattern 2 — Cycle Detection

### Cycle in Undirected Graph

```python
def has_cycle_undirected(n: int, edges: list[list[int]]) -> bool:
    from collections import defaultdict
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()

    def dfs(node, parent) -> bool:
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor == parent: continue       # ignore edge back to parent
            if neighbor in visited: return True   # found a back edge = cycle
            if dfs(neighbor, node): return True
        return False

    for node in range(n):
        if node not in visited:
            if dfs(node, -1): return True
    return False
```

### Cycle in Directed Graph (White-Gray-Black Coloring)

```python
def has_cycle_directed(n: int, edges: list[list[int]]) -> bool:
    from collections import defaultdict
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    # 0=unvisited, 1=in-stack (gray), 2=done (black)
    color = [0] * n

    def dfs(node) -> bool:
        color[node] = 1       # mark in-stack
        for neighbor in graph[node]:
            if color[neighbor] == 1: return True    # back edge = cycle
            if color[neighbor] == 0 and dfs(neighbor): return True
        color[node] = 2       # mark done
        return False

    return any(dfs(i) for i in range(n) if color[i] == 0)
```

> [!IMPORTANT]
> **White-Gray-Black (0-1-2) coloring** is the correct approach for directed graphs. A back edge (neighbor in gray/state-1) indicates a cycle. Using just a visited set misses the case where a node is reachable via two paths — one with and one without a cycle.

---

## Pattern 3 — Topological Sort

### DFS-Based Topological Sort

```python
def topological_sort(n: int, edges: list[list[int]]) -> list[int]:
    from collections import defaultdict
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    visited = set()
    stack = []

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)   # add to stack AFTER all descendants are processed

    for node in range(n):
        if node not in visited:
            dfs(node)

    return stack[::-1]   # reverse for topological order
```

### Course Schedule — Can All Courses Be Completed? (LC 207)

```python
def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    from collections import defaultdict
    graph = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)   # b must come before a

    # 0=unvisited, 1=in-progress, 2=done
    state = [0] * num_courses

    def dfs(course) -> bool:
        if state[course] == 1: return False   # cycle
        if state[course] == 2: return True    # already verified
        state[course] = 1
        for next_course in graph[course]:
            if not dfs(next_course): return False
        state[course] = 2
        return True

    return all(dfs(c) for c in range(num_courses))
```

### Course Schedule II — Return Valid Order (LC 210)

```python
def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    from collections import defaultdict
    graph = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)

    state = [0] * num_courses
    order = []

    def dfs(course) -> bool:
        if state[course] == 1: return False
        if state[course] == 2: return True
        state[course] = 1
        for next_c in graph[course]:
            if not dfs(next_c): return False
        state[course] = 2
        order.append(course)   # add AFTER all descendants
        return True

    for c in range(num_courses):
        if state[c] == 0:
            if not dfs(c): return []

    return order[::-1]
```

---

## Pattern 4 — Path Finding

### Clone Graph (LC 133)

```python
def clone_graph(node):
    if not node: return None
    cloned = {}

    def dfs(n):
        if n in cloned: return cloned[n]
        copy = Node(n.val, [])
        cloned[n] = copy
        for neighbor in n.neighbors:
            copy.neighbors.append(dfs(neighbor))
        return copy

    return dfs(node)
```

> [!TIP]
> Store cloned nodes by the **original node** (not val) as the key. This handles graphs with duplicate values correctly. Register the clone in `cloned` **before** recursing into neighbors to handle cycles.

### All Paths from Source to Target (LC 797)

```python
def all_paths_source_target(graph: list[list[int]]) -> list[list[int]]:
    result = []
    target = len(graph) - 1

    def dfs(node, path):
        if node == target:
            result.append(path[:])
            return
        for neighbor in graph[node]:
            path.append(neighbor)
            dfs(neighbor, path)
            path.pop()   # backtrack

    dfs(0, [0])
    return result
```

> [!TIP]
> This is a DAG (directed acyclic graph) — no visited set needed since there are no cycles. For general graphs with cycles, add a visited set.

### Word Ladder II — All Shortest Paths (LC 126)

```python
from collections import defaultdict, deque

def find_ladders(begin_word: str, end_word: str, word_list: list[str]) -> list[list[str]]:
    word_set = set(word_list)
    if end_word not in word_set: return []

    # BFS to build layers (shortest path distances)
    layer = {begin_word}
    parents = defaultdict(set)
    found = False

    while layer and not found:
        word_set -= layer
        next_layer = set()
        for word in layer:
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    new_word = word[:i] + c + word[i+1:]
                    if new_word in word_set:
                        next_layer.add(new_word)
                        parents[new_word].add(word)
                        if new_word == end_word: found = True
        layer = next_layer

    if not found: return []

    # DFS to reconstruct all paths
    result = []
    def dfs(word, path):
        if word == begin_word:
            result.append(path[::-1])
            return
        for parent in parents[word]:
            path.append(parent)
            dfs(parent, path)
            path.pop()

    dfs(end_word, [end_word])
    return result
```

---

## Pattern 5 — Island/Region Problems

### Max Area of Island (LC 695)

```python
def max_area_of_island(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c) -> int:
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] == 0:
            return 0
        grid[r][c] = 0   # mark visited
        return 1 + sum(dfs(r+dr, c+dc) for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)])

    return max(dfs(r, c) for r in range(rows) for c in range(cols))
```

### Surrounded Regions (LC 130)

```python
def solve(board: list[list[str]]) -> None:
    if not board: return
    rows, cols = len(board), len(board[0])

    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != 'O': return
        board[r][c] = 'S'   # safe — connected to border
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            dfs(r+dr, c+dc)

    # Mark border-connected O's as safe
    for r in range(rows):
        for c in [0, cols-1]:
            if board[r][c] == 'O': dfs(r, c)
    for c in range(cols):
        for r in [0, rows-1]:
            if board[r][c] == 'O': dfs(r, c)

    # Flip: remaining O's are surrounded; restore S's
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O': board[r][c] = 'X'
            elif board[r][c] == 'S': board[r][c] = 'O'
```

> [!TIP]
> **Reverse thinking:** Instead of finding surrounded regions directly, find regions connected to the border and mark them safe. Everything remaining is surrounded.

---

## Interview Questions — Logic & Trickiness

| Problem | LC # | Pattern | Click Moment | Gotcha |
| :--- | :--- | :--- | :--- | :--- |
| **Flood Fill** | 733 | DFS + in-place mark | Spread color to same-colored neighbors | Check `original == color` first to avoid infinite loop |
| **Number of Islands** | 200 | DFS + sink | Sink each island cell to `'#'` | 4-directional only; restore grid if needed |
| **Clone Graph** | 133 | DFS + memo | Register clone before recursing into neighbors | Use original node as key (not val) |
| **Course Schedule** | 207 | Cycle detection (directed) | 3-color: 0=unvisited, 1=in-stack, 2=done | Back edge (color==1) = cycle; `color==2` = already safe |
| **Course Schedule II** | 210 | Topo sort DFS | Add to `order` AFTER all descendants | Reverse the order at end |
| **All Paths Source→Target** | 797 | DFS backtrack | DAG: no visited set needed | Snapshot `path[:]` before appending to result |
| **Number of Connected Components** | 323 | DFS count | Each unvisited DFS start = new component | Undirected: add both directions to adj list |
| **Max Area of Island** | 695 | DFS + area count | Return `1 + sum(dfs neighbors)` | Mark visited BEFORE recursing to avoid double-count |
| **Surrounded Regions** | 130 | Reverse DFS | Mark border-connected O's safe first | 3 states: X, O, S (safe); restore at end |
| **Has Cycle Undirected** | — | DFS + parent | Back edge = neighbor that is NOT parent | Pass parent to avoid flagging the traversal edge |
| **Has Cycle Directed** | — | White-Gray-Black | Gray = in-stack; second visit to gray = cycle | Can't use single visited set for directed graphs |
| **Word Ladder II** | 126 | BFS + DFS | BFS builds parent map; DFS reconstructs paths | Remove visited words from set per BFS layer |

---

## Recursion Limit Warning

> [!CAUTION]
> Graph DFS on large graphs (10^4+ nodes) can hit Python's default recursion limit of 1000. Use `sys.setrecursionlimit(10**5)` as a stopgap, or convert to **iterative DFS with an explicit stack** for production code.

```python
def dfs_iterative(start, graph):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited: continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
```

---

## See also

- [README.md](README.md) — Core recursion theory and iterative conversion
- [tree-recursion.md](tree-recursion.md) — DFS on trees (no cycle risk)
- [questions-bank.md](questions-bank.md) — Graph recursion drill problems
