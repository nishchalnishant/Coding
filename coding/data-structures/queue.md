---
tags: [coding, data-structures, queue]
topic: queue
difficulty: mixed
---

# Queue Problems

---

## Monotonic Deque

### Sliding Window Maximum

> [!example] Problem
> Given array `nums` and window size `k`, return the maximum value in each contiguous window of size `k`.

> [!info] Approach
> - **WHY:** Naive O(nk) rescans the window on every step; we need O(n).
> - **WHAT:** A deque that is always sorted descending by value. The front is always the max of the current window.
> - **HOW:** For each index `i` — (1) evict from the back any index whose value ≤ `nums[i]` (they are dominated and can never be future maxima); (2) evict from the front if it has fallen outside the window; (3) append `i`; (4) once `i >= k-1`, the front of the deque is the answer. Each index is enqueued and dequeued at most once → O(n) total.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def maxSlidingWindow(nums: list[int], k: int) -> list[int]:
>     dq: deque[int] = deque()   # stores indices; values are monotonically decreasing
>     result: list[int] = []
>     for i, x in enumerate(nums):
>         # remove dominated indices from back
>         while dq and nums[dq[-1]] <= x:
>             dq.pop()
>         dq.append(i)
>         # remove expired index from front
>         if dq[0] < i - k + 1:
>             dq.popleft()
>         if i >= k - 1:
>             result.append(nums[dq[0]])
>     return result
> ```

> [!success] Complexity
> Time O(n) — each index pushed/popped once. Space O(k).

> [!tip] Alternatives
> - Max-heap with lazy deletion: O(n log n) — simpler to write but asymptotically worse.
> - Segment tree: O(n log n) build + O(log n) per query — overkill for a contiguous sliding window.

---

### Sliding Window Minimum

> [!example] Problem
> Same as Sliding Window Maximum but return the minimum of each window of size `k`.

> [!info] Approach
> - **WHY:** Same argument — need O(n), not O(nk).
> - **WHAT:** Monotonic increasing deque (front = minimum).
> - **HOW:** Identical to the maximum variant; flip one comparison — evict from the back when `nums[back] >= x` instead of `<=`. The front always holds the index of the current window minimum.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def minSlidingWindow(nums: list[int], k: int) -> list[int]:
>     dq: deque[int] = deque()   # indices; values monotonically increasing
>     result: list[int] = []
>     for i, x in enumerate(nums):
>         while dq and nums[dq[-1]] >= x:
>             dq.pop()
>         dq.append(i)
>         if dq[0] < i - k + 1:
>             dq.popleft()
>         if i >= k - 1:
>             result.append(nums[dq[0]])
>     return result
> ```

> [!success] Complexity
> Time O(n). Space O(k).

> [!tip] Alternatives
> Same as Sliding Window Maximum. The only change is the eviction comparison on the back.

---

### Shortest Subarray with Sum at Least K

> [!example] Problem
> Given integer array `nums` (may contain negatives) and integer `k`, return the length of the shortest subarray whose sum is ≥ k. Return -1 if none exists.

> [!info] Approach
> - **WHY:** Negative values break the simple two-pointer sliding window — shrinking from the left doesn't always decrease the sum. We need a different invariant.
> - **WHAT:** Prefix sums + a monotonic increasing deque of prefix-sum indices. `prefix[j] - prefix[i] >= k` with `j > i` means subarray `i..j-1` has sum ≥ k. We want to minimize `j - i`.
> - **HOW:** Compute prefix sums. Maintain a deque of indices with strictly increasing prefix-sum values. For each `j`: while the front of the deque satisfies `prefix[j] - prefix[front] >= k`, update the answer with `j - front` and pop the front (we want the smallest valid `j - i`, so once a shorter subarray is found the front is no longer useful). Then maintain the increasing invariant by popping from the back while `prefix[back] >= prefix[j]`, and append `j`.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def shortestSubarray(nums: list[int], k: int) -> int:
>     n = len(nums)
>     prefix = [0] * (n + 1)
>     for i in range(n):
>         prefix[i + 1] = prefix[i] + nums[i]
>
>     dq: deque[int] = deque()   # indices of prefix; monotonically increasing prefix values
>     ans = float('inf')
>     for j in range(n + 1):
>         # try to satisfy sum >= k using front as left boundary
>         while dq and prefix[j] - prefix[dq[0]] >= k:
>             ans = min(ans, j - dq.popleft())
>         # maintain increasing deque
>         while dq and prefix[dq[-1]] >= prefix[j]:
>             dq.pop()
>         dq.append(j)
>     return ans if ans != float('inf') else -1
> ```

> [!success] Complexity
> Time O(n). Space O(n).

> [!tip] Alternatives
> - Segment tree / sparse table for range min prefix sum: O(n log n) — correct but overcomplicated.
> - Brute force O(n²): try all `(i, j)` pairs — baseline only.

---

### Jump Game VI (DP + Sliding Window Max)

> [!example] Problem
> Given integer array `nums` and integer `k`, start at index 0. At each step you can jump forward 1 to `k` indices. Score = sum of values at visited indices (including first and last). Maximize the score.

> [!info] Approach
> - **WHY:** Naive DP `dp[i] = nums[i] + max(dp[i-k..i-1])` is O(nk) — the inner max over a window of size k is expensive.
> - **WHAT:** DP with a monotonic decreasing deque to maintain `max(dp[i-k..i-1])` in O(1) per step.
> - **HOW:** `dp[i] = nums[i] + max(dp[j] for j in range(max(0, i-k), i))`. Use a deque of indices in decreasing `dp` value order. Before computing `dp[i]`, evict indices outside the window `[i-k, i-1]` from the front. The front of the deque is `argmax` dp in the window.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def maxResult(nums: list[int], k: int) -> int:
>     n = len(nums)
>     dp = [0] * n
>     dp[0] = nums[0]
>     dq: deque[int] = deque([0])   # indices; dp values decreasing
>
>     for i in range(1, n):
>         # evict out-of-window front
>         while dq and dq[0] < i - k:
>             dq.popleft()
>         dp[i] = nums[i] + dp[dq[0]]
>         # maintain decreasing invariant on back
>         while dq and dp[dq[-1]] <= dp[i]:
>             dq.pop()
>         dq.append(i)
>
>     return dp[n - 1]
> ```

> [!success] Complexity
> Time O(n). Space O(n) for dp, O(k) for deque.

> [!tip] Alternatives
> - Max-heap: O(n log n) — store `(-dp[i], i)`, skip stale indices. Simpler to code, worse asymptotically.
> - Segment tree range-max: O(n log n) — overkill here.

---

### Maximum of Minimums of Every Window Size

> [!example] Problem
> Given an array of length `n`, for every window size `k` from 1 to `n`, find the maximum value among all minimums of contiguous windows of size `k`. Return an array of size `n`.

> [!info] Approach
> **WHY:** Brute force is O(n³) — enumerate all windows and compute each minimum. Monotonic stack gives O(n) by computing, for each element, the largest window size for which it is the minimum.
>
> **WHAT:** For each index `i`, find `left[i]` = nearest index to the left with a smaller value, and `right[i]` = nearest index to the right with a smaller value. Element `i` is the minimum for all windows of size up to `right[i] - left[i] - 1`.
>
> **HOW:**
> 1. Use monotonic stack (increasing) to compute `left[]` (previous smaller element index, defaulting to -1) and `right[]` (next smaller element index, defaulting to n).
> 2. For each `i`, `window_size = right[i] - left[i] - 1`; update `ans[window_size] = max(ans[window_size], nums[i])`.
> 3. Suffix maximum pass: for `k` from `n-1` down to `1`: `ans[k] = max(ans[k], ans[k+1])`. This handles the fact that the minimum of a larger window is ≤ the minimum of a smaller window — so a value that is the minimum for window size `w` is also a candidate for all smaller sizes.

> [!note]- Python Solution
> ```python
> def maxMinOfWindows(nums: list[int]) -> list[int]:
>     n = len(nums)
>     left = [-1] * n    # index of previous smaller element
>     right = [n] * n    # index of next smaller element
>     stack: list[int] = []
>
>     # previous smaller (left boundary)
>     for i in range(n):
>         while stack and nums[stack[-1]] >= nums[i]:
>             stack.pop()
>         left[i] = stack[-1] if stack else -1
>         stack.append(i)
>
>     stack.clear()
>
>     # next smaller (right boundary)
>     for i in range(n - 1, -1, -1):
>         while stack and nums[stack[-1]] >= nums[i]:
>             stack.pop()
>         right[i] = stack[-1] if stack else n
>         stack.append(i)
>
>     ans = [0] * (n + 1)   # ans[k] = max of minimums for window size k (1-indexed)
>     for i in range(n):
>         w = right[i] - left[i] - 1
>         ans[w] = max(ans[w], nums[i])
>
>     # suffix maximum: smaller windows can use larger-window answers
>     for k in range(n - 1, 0, -1):
>         ans[k] = max(ans[k], ans[k + 1])
>
>     return ans[1:]   # return 1-indexed results as 0-indexed array
> ```

> [!success] Complexity
> Time O(n) — two monotonic stack passes + one suffix pass. Space O(n).

> [!tip] Alternatives
> - Segment tree: O(n log n) build + O(log n) per query — for each window size enumerate all windows and take min via range-min query. O(n² log n) total for all sizes — worse.
> - Sparse table RMQ: O(n log n) build, O(1) range-min query — O(n²) total over all window sizes. Still worse than monotonic stack for this specific problem.

---

## BFS / Level-order

### Binary Tree Level Order Traversal

> [!example] Problem
> Given the root of a binary tree, return its level-order traversal as a list of lists, where each inner list contains node values at that depth (LC 102).

> [!info] Approach
> - **WHY:** DFS mixes levels; BFS processes nodes level-by-level naturally.
> - **WHAT:** BFS with level-size snapshotting — record `len(queue)` before processing each level so we know when one level ends and the next begins.
> - **HOW:** Enqueue root. At the start of each BFS iteration snapshot `size = len(queue)`. Dequeue exactly `size` nodes, collect their values, enqueue their children. Append the level list to results.

> [!note]- Python Solution
> ```python
> from collections import deque
> from typing import Optional
>
> class TreeNode:
>     def __init__(self, val: int = 0, left: 'Optional[TreeNode]' = None, right: 'Optional[TreeNode]' = None):
>         self.val = val; self.left = left; self.right = right
>
> def levelOrder(root: Optional[TreeNode]) -> list[list[int]]:
>     if not root:
>         return []
>     result: list[list[int]] = []
>     queue: deque[TreeNode] = deque([root])
>     while queue:
>         level: list[int] = []
>         for _ in range(len(queue)):
>             node = queue.popleft()
>             level.append(node.val)
>             if node.left:
>                 queue.append(node.left)
>             if node.right:
>                 queue.append(node.right)
>         result.append(level)
>     return result
> ```

> [!success] Complexity
> Time O(n). Space O(n) — queue holds at most one full level (up to n/2 nodes).

> [!tip] Alternatives
> - DFS with depth parameter: `dfs(node, depth)` appends to `result[depth]` — same O(n), avoids queue but uses call stack space.
> - Sentinel `None` in queue to mark level boundaries: works but is error-prone.

---

### Binary Tree Zigzag Level Order Traversal

> [!example] Problem
> Same as level-order traversal but alternate the direction each level: left-to-right at even depths, right-to-left at odd depths (LC 103).

> [!info] Approach
> - **WHY:** BFS naturally produces left-to-right order; reversing odd levels is cheaper than changing traversal direction.
> - **WHAT:** Standard level-order BFS with a `left_to_right` flag; reverse odd-depth level lists before appending.
> - **HOW:** Toggle `left_to_right` after each level. When False, reverse the collected level list. Children are always enqueued left-to-right; only the output list is reversed.

> [!note]- Python Solution
> ```python
> from collections import deque
> from typing import Optional
>
> def zigzagLevelOrder(root: Optional[TreeNode]) -> list[list[int]]:
>     if not root:
>         return []
>     result: list[list[int]] = []
>     queue: deque[TreeNode] = deque([root])
>     left_to_right = True
>     while queue:
>         level: list[int] = []
>         for _ in range(len(queue)):
>             node = queue.popleft()
>             level.append(node.val)
>             if node.left:
>                 queue.append(node.left)
>             if node.right:
>                 queue.append(node.right)
>         result.append(level if left_to_right else level[::-1])
>         left_to_right = not left_to_right
>     return result
> ```

> [!success] Complexity
> Time O(n). Space O(n).

> [!tip] Alternatives
> - Double-ended deque per level: append to front or back based on direction, avoiding the reversal. O(n) same, slightly more complex.
> - DFS with depth parity: same O(n), call-stack based.

---

### Binary Tree Right Side View

> [!example] Problem
> Given the root of a binary tree, return the values of nodes visible when looking at the tree from the right side — i.e., the last node at each level (LC 199).

> [!info] Approach
> - **WHY:** The rightmost node at each level is exactly the last node dequeued in a level-order BFS.
> - **WHAT:** Level-order BFS; record the last node value at each level.
> - **HOW:** Standard level-size snapshotting. After processing all nodes in a level, the most recently processed node value is the rightmost — append it to results.

> [!note]- Python Solution
> ```python
> from collections import deque
> from typing import Optional
>
> def rightSideView(root: Optional[TreeNode]) -> list[int]:
>     if not root:
>         return []
>     result: list[int] = []
>     queue: deque[TreeNode] = deque([root])
>     while queue:
>         rightmost = 0
>         for _ in range(len(queue)):
>             node = queue.popleft()
>             rightmost = node.val
>             if node.left:
>                 queue.append(node.left)
>             if node.right:
>                 queue.append(node.right)
>         result.append(rightmost)
>     return result
> ```

> [!success] Complexity
> Time O(n). Space O(n).

> [!tip] Alternatives
> - DFS right-first: visit right child before left; first node seen at each depth is the rightmost. O(n) time, O(h) space.
> - To get left side view: swap child enqueue order (right before left) or take `level[0]` instead of `level[-1]`.

---

## BFS Multi-Source

### Rotting Oranges

> [!example] Problem
> Grid of `0` (empty), `1` (fresh), `2` (rotten). Each minute every rotten orange infects its 4-directional fresh neighbors. Return time until no fresh orange remains, or -1 if impossible.

> [!info] Approach
> - **WHY:** All rotten oranges spread simultaneously — not sequentially. A single-source BFS from the "first" rotten orange would give wrong timing. Multi-source BFS models all sources spreading in parallel from time 0.
> - **WHAT:** Seed the queue with ALL rotten cells at distance 0. BFS level = 1 minute.
> - **HOW:** Count fresh oranges. Run BFS — each time a fresh orange is infected, decrement fresh count and enqueue the new cell with `time + 1`. After BFS, if fresh > 0, return -1 (blocked cells remain). Otherwise return the last timestamp used.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def orangesRotting(grid: list[list[int]]) -> int:
>     rows, cols = len(grid), len(grid[0])
>     queue: deque[tuple[int, int, int]] = deque()
>     fresh = 0
>     for r in range(rows):
>         for c in range(cols):
>             if grid[r][c] == 2:
>                 queue.append((r, c, 0))
>             elif grid[r][c] == 1:
>                 fresh += 1
>     if fresh == 0:
>         return 0
>     dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
>     minutes = 0
>     while queue:
>         r, c, t = queue.popleft()
>         for dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
>                 grid[nr][nc] = 2
>                 fresh -= 1
>                 minutes = t + 1
>                 queue.append((nr, nc, t + 1))
>     return minutes if fresh == 0 else -1
> ```

> [!success] Complexity
> Time O(m × n). Space O(m × n).

> [!tip] Alternatives
> - DFS: Can compute reachability but cannot model simultaneous spread timing correctly. BFS is required.
> - Repeated simulation passes: O(m × n × T) where T = answer — correct but wasteful.

---

### 01 Matrix

> [!example] Problem
> Given a binary matrix, for each cell return its distance to the nearest `0`. Distance is the count of steps (4-directional).

> [!info] Approach
> - **WHY:** Running BFS from each `1` independently is O((m×n)²) — too slow. All `0` cells are sources; they spread distance simultaneously.
> - **WHAT:** Multi-source BFS seeded with all `0` cells at distance 0.
> - **HOW:** Initialize all `0` cells with distance 0 in the queue. Initialize all `1` cells with `inf`. BFS outward — first time a `1` cell is reached sets its distance. BFS guarantees minimum distance.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def updateMatrix(mat: list[list[int]]) -> list[list[int]]:
>     rows, cols = len(mat), len(mat[0])
>     dist = [[float('inf')] * cols for _ in range(rows)]
>     queue: deque[tuple[int, int]] = deque()
>     for r in range(rows):
>         for c in range(cols):
>             if mat[r][c] == 0:
>                 dist[r][c] = 0
>                 queue.append((r, c))
>     dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
>     while queue:
>         r, c = queue.popleft()
>         for dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] > dist[r][c] + 1:
>                 dist[nr][nc] = dist[r][c] + 1
>                 queue.append((nr, nc))
>     return dist
> ```

> [!success] Complexity
> Time O(m × n). Space O(m × n).

> [!tip] Alternatives
> - BFS from each `1` separately: O((m×n)²) — correct, too slow.
> - DP in two passes (top-left, then bottom-right): O(m×n) with O(1) extra space — cleaner but harder to generalize.

---

### Walls and Gates

> [!example] Problem
> Grid with `-1` (wall), `0` (gate), `INF` (empty room). Fill each empty room with its distance to the nearest gate. Modify in place.

> [!info] Approach
> - **WHY:** Starting BFS from each room to find the nearest gate is O(G × m × n). Starting from all gates simultaneously is O(m × n).
> - **WHAT:** Multi-source BFS from all gates.
> - **HOW:** Enqueue all cells with value `0` (gates). BFS outward — each `INF` cell reached gets distance = parent's distance + 1. Walls (`-1`) are never enqueued or updated.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def wallsAndGates(rooms: list[list[int]]) -> None:
>     INF = 2**31 - 1
>     rows, cols = len(rooms), len(rooms[0])
>     queue: deque[tuple[int, int]] = deque()
>     for r in range(rows):
>         for c in range(cols):
>             if rooms[r][c] == 0:
>                 queue.append((r, c))
>     dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
>     while queue:
>         r, c = queue.popleft()
>         for dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == INF:
>                 rooms[nr][nc] = rooms[r][c] + 1
>                 queue.append((nr, nc))
> ```

> [!success] Complexity
> Time O(m × n). Space O(m × n).

> [!tip] Alternatives
> - BFS per gate: O(G × m × n) — correct, strictly worse.
> - Dijkstra: All edge weights = 1, so BFS suffices. Dijkstra adds log factor unnecessarily.

---

### Farthest Building from Land (As Far from Land as Possible)

> [!example] Problem
> Given binary grid where `1` = land and `0` = water, find the water cell that has the maximum Manhattan distance to the nearest land cell. Return that distance, or -1 if no water or no land exists.

> [!info] Approach
> - **WHY:** The cell farthest from all land is the last cell reached when BFS expands outward from all land cells simultaneously.
> - **WHAT:** Multi-source BFS from all land cells. The last cell dequeued gives the maximum distance.
> - **HOW:** Seed the queue with all `1` cells at distance 0. BFS outward filling `0` cells. Track the last distance assigned — that is the answer.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def maxDistance(grid: list[list[int]]) -> int:
>     n = len(grid)
>     queue: deque[tuple[int, int]] = deque()
>     for r in range(n):
>         for c in range(n):
>             if grid[r][c] == 1:
>                 queue.append((r, c))
>     if len(queue) == 0 or len(queue) == n * n:
>         return -1   # all water or all land
>     dist = -1
>     dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
>     while queue:
>         r, c = queue.popleft()
>         for dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
>                 grid[nr][nc] = grid[r][c] + 1
>                 dist = grid[nr][nc] - 1
>                 queue.append((nr, nc))
>     return dist
> ```

> [!success] Complexity
> Time O(n²). Space O(n²).

> [!tip] Alternatives
> - BFS from each water cell: O(n⁴) — correct, too slow.
> - DP two-pass: O(n²) time and O(1) extra space — valid, but multi-source BFS is more intuitive.

---

### Shortest Path in Binary Matrix

> [!example] Problem
> Given an `n × n` binary matrix, return the length of the shortest clear path from `(0,0)` to `(n-1, n-1)` where clear means all cells on the path are `0`. Movement is 8-directional. Return -1 if no such path exists.

> [!info] Approach
> - **WHY:** All edges have equal weight (each step costs 1), so BFS gives the shortest path.
> - **WHAT:** Single-source BFS from `(0,0)` over open (value `0`) cells.
> - **HOW:** If start or end is `1`, return -1 immediately. BFS with 8 directions. The first time `(n-1, n-1)` is dequeued, return the current distance + 1.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def shortestPathBinaryMatrix(grid: list[list[int]]) -> int:
>     n = len(grid)
>     if grid[0][0] == 1 or grid[n-1][n-1] == 1:
>         return -1
>     dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
>     queue: deque[tuple[int, int, int]] = deque([(0, 0, 1)])
>     grid[0][0] = 1   # mark visited by setting to 1
>     while queue:
>         r, c, dist = queue.popleft()
>         if r == n - 1 and c == n - 1:
>             return dist
>         for dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
>                 grid[nr][nc] = 1
>                 queue.append((nr, nc, dist + 1))
>     return -1
> ```

> [!success] Complexity
> Time O(n²). Space O(n²).

> [!tip] Alternatives
> - A* with Chebyshev heuristic: faster in practice for large grids with clear paths, but O(n²) worst case same as BFS.
> - DFS: finds a path but not guaranteed shortest.

---

### Minimum Knight Moves

> [!example] Problem
> On an infinite chessboard, find the minimum number of knight moves to reach `(x, y)` from `(0, 0)`.

> [!info] Approach
> - **WHY:** All moves have cost 1; BFS gives the minimum number of moves.
> - **WHAT:** BFS from `(0,0)` with 8 knight-move directions. Exploit symmetry to search in the first quadrant only, reducing state space by 4×.
> - **HOW:** Reflect `(x, y)` to `(|x|, |y|)` — knight distances are symmetric. BFS from `(0,0)`. A small boundary expansion (`abs(x) + 2`, `abs(y) + 2`) handles the initial wriggle room needed for corner cases near the origin.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def minKnightMoves(x: int, y: int) -> int:
>     x, y = abs(x), abs(y)   # exploit symmetry
>     MOVES = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
>     queue: deque[tuple[int, int, int]] = deque([(0, 0, 0)])
>     visited: set[tuple[int, int]] = {(0, 0)}
>     while queue:
>         r, c, steps = queue.popleft()
>         if r == x and c == y:
>             return steps
>         for dr, dc in MOVES:
>             nr, nc = r + dr, c + dc
>             # search in expanded first-quadrant region
>             if (nr, nc) not in visited and nr >= -2 and nc >= -2:
>                 visited.add((nr, nc))
>                 queue.append((nr, nc, steps + 1))
>     return -1
> ```

> [!success] Complexity
> Time O(|x| × |y|). Space O(|x| × |y|).

> [!tip] Alternatives
> - Bidirectional BFS: meets in the middle, ~4× fewer states explored — recommended for large `(x, y)`.
> - Math formula: closed-form exists for specific quadrant cases — not worth memorizing, but mention as O(1) follow-up.

---

## BFS Single-Source

### Word Ladder

> [!example] Problem
> Given `beginWord`, `endWord`, and a word list, return the length of the shortest transformation sequence from `beginWord` to `endWord` where each step changes exactly one letter and each intermediate word must exist in the word list. Return 0 if no sequence exists.

> [!info] Approach
> - **WHY:** Each word is a graph node; an edge exists between two words that differ by one letter. We want shortest path → BFS.
> - **WHAT:** BFS on the implicit word graph. Removing visited words from the word set avoids revisiting (and is faster than a separate visited set).
> - **HOW:** Enqueue `(beginWord, 1)`. For each dequeued word, generate all one-letter variants; if a variant is in the word set, enqueue it with distance + 1 and remove from the set. Return the distance when `endWord` is reached.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def ladderLength(beginWord: str, endWord: str, wordList: list[str]) -> int:
>     word_set = set(wordList)
>     if endWord not in word_set:
>         return 0
>     queue: deque[tuple[str, int]] = deque([(beginWord, 1)])
>     word_set.discard(beginWord)
>     while queue:
>         word, dist = queue.popleft()
>         for i in range(len(word)):
>             for c in 'abcdefghijklmnopqrstuvwxyz':
>                 neighbor = word[:i] + c + word[i+1:]
>                 if neighbor == endWord:
>                     return dist + 1
>                 if neighbor in word_set:
>                     word_set.discard(neighbor)
>                     queue.append((neighbor, dist + 1))
>     return 0
> ```

> [!success] Complexity
> Time O(N × L × 26) where N = word list size, L = word length. Space O(N × L).

> [!tip] Alternatives
> - Bidirectional BFS: expand from both `beginWord` and `endWord`, meet in the middle — reduces explored nodes to ~√ of one-directional BFS. Critical optimization for large word lists.
> - DFS: finds a path but not shortest.

---

### Open the Lock

> [!example] Problem
> A lock has 4 wheels, each digit 0–9. Starting at `"0000"`, find the minimum turns to reach `target`, avoiding `deadends`. Each turn rotates one wheel by ±1.

> [!info] Approach
> - **WHY:** Each lock state is a node; each valid turn is an edge with weight 1. Shortest path → BFS.
> - **WHAT:** BFS on the 4-digit string state space.
> - **HOW:** Each state has 8 neighbors (4 wheels × 2 directions). Mark deadends and the start as visited before BFS begins. The first time `target` is reached, return the current depth.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def openLock(deadends: list[str], target: str) -> int:
>     dead = set(deadends)
>     if "0000" in dead:
>         return -1
>     queue: deque[tuple[str, int]] = deque([("0000", 0)])
>     visited: set[str] = {"0000"}
>     while queue:
>         state, turns = queue.popleft()
>         if state == target:
>             return turns
>         for i in range(4):
>             d = int(state[i])
>             for delta in (1, -1):
>                 new_d = (d + delta) % 10
>                 neighbor = state[:i] + str(new_d) + state[i+1:]
>                 if neighbor not in visited and neighbor not in dead:
>                     visited.add(neighbor)
>                     queue.append((neighbor, turns + 1))
>     return -1
> ```

> [!success] Complexity
> Time O(10⁴ × 4 × 2) = O(1) — state space is fixed at 10,000 states. Space O(10⁴).

> [!tip] Alternatives
> - Bidirectional BFS: expand from `"0000"` and `target` simultaneously — halves explored states in practice. Worth mentioning.
> - A*: heuristic = number of digits differing from target — reduces explored states but adds implementation complexity.

---

### Bus Routes

> [!example] Problem
> Given bus routes (each route is a list of stops in a loop), and a `source` and `target` stop, return the minimum number of buses you must take. Return -1 if impossible.

> [!info] Approach
> - **WHY:** BFS over stops would revisit stops on the same route repeatedly. Model buses (routes) as nodes, not stops — each bus is taken at cost 1.
> - **WHAT:** BFS where each state is a bus route index, not a stop.
> - **HOW:** Build `stop → [bus_indices]` map. BFS starts from all buses that include `source`. For each bus dequeued, visit all its stops; if `target` is reached, return bus count. For each stop on this bus, enqueue all other buses that serve it and haven't been visited. Mark buses as visited to avoid re-boarding.

> [!note]- Python Solution
> ```python
> from collections import deque, defaultdict
>
> def numBusesToDestination(routes: list[list[int]], source: int, target: int) -> int:
>     if source == target:
>         return 0
>     stop_to_buses: dict[int, list[int]] = defaultdict(list)
>     for bus_idx, route in enumerate(routes):
>         for stop in route:
>             stop_to_buses[stop].append(bus_idx)
>
>     visited_buses: set[int] = set()
>     visited_stops: set[int] = {source}
>     queue: deque[tuple[int, int]] = deque()  # (bus_index, buses_taken)
>     for bus in stop_to_buses[source]:
>         queue.append((bus, 1))
>         visited_buses.add(bus)
>
>     while queue:
>         bus, count = queue.popleft()
>         for stop in routes[bus]:
>             if stop == target:
>                 return count
>             if stop not in visited_stops:
>                 visited_stops.add(stop)
>                 for next_bus in stop_to_buses[stop]:
>                     if next_bus not in visited_buses:
>                         visited_buses.add(next_bus)
>                         queue.append((next_bus, count + 1))
>     return -1
> ```

> [!success] Complexity
> Time O(sum of route lengths). Space O(sum of route lengths).

> [!tip] Alternatives
> - BFS over stops with state `(stop, buses_used)`: correct but revisits stops on the same route — slower.
> - Dijkstra: all edges have weight 1 so BFS suffices.

---

### Shortest Path in Grid with Obstacles Elimination

> [!example] Problem
> Given an `m × n` grid of `0` (free) and `1` (obstacle), you can eliminate at most `k` obstacles. Return the minimum steps from `(0,0)` to `(m-1, n-1)`, or -1 if impossible.

> [!info] Approach
> - **WHY:** Standard BFS doesn't capture how many eliminations have been used — two paths to the same cell may have different remaining `k`. The state must include `k`.
> - **WHAT:** BFS with 3D state `(row, col, remaining_k)`.
> - **HOW:** Enqueue `(0, 0, k)` with 0 steps. For each cell, try all 4 neighbors — if a neighbor is free, step to it; if it's an obstacle and `remaining_k > 0`, step to it and decrement `k`. Mark `(r, c, k)` as visited — not just `(r, c)`.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def shortestPath(grid: list[list[int]], k: int) -> int:
>     m, n = len(grid), len(grid[0])
>     if m == 1 and n == 1:
>         return 0
>     # State: (r, c, remaining_k)
>     visited: set[tuple[int, int, int]] = {(0, 0, k)}
>     queue: deque[tuple[int, int, int, int]] = deque([(0, 0, k, 0)])
>     dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
>     while queue:
>         r, c, rem, steps = queue.popleft()
>         for dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             if not (0 <= nr < m and 0 <= nc < n):
>                 continue
>             new_rem = rem - grid[nr][nc]
>             if new_rem < 0:
>                 continue
>             if nr == m - 1 and nc == n - 1:
>                 return steps + 1
>             if (nr, nc, new_rem) not in visited:
>                 visited.add((nr, nc, new_rem))
>                 queue.append((nr, nc, new_rem, steps + 1))
>     return -1
> ```

> [!success] Complexity
> Time O(m × n × k). Space O(m × n × k).

> [!tip] Alternatives
> - Greedy shortcut: if `k >= m + n - 2`, the entire path can be cleared — return `m + n - 2` directly (O(1)).
> - A* with `(steps + Manhattan)` heuristic: prunes states faster in practice but same worst-case.

---

### Cheapest Flights Within K Stops

> [!example] Problem
> Given `n` cities, a list of flights `[from, to, price]`, and integers `src`, `dst`, `k`, return the cheapest price from `src` to `dst` with at most `k` stops. Return -1 if impossible.

> [!info] Approach
> - **WHY:** Standard Dijkstra may revisit a node via a longer path that uses fewer stops, blocking a cheaper path that needs more stops. The stop count is part of the state.
> - **WHAT:** BFS level-by-level (level = number of stops used). At each level, update costs.
> - **HOW:** Use Bellman-Ford with exactly `k+1` relaxation rounds. Maintain `prices[node]` = cheapest price to reach `node` using at most `current_round` hops. Use a copy of prices per round to avoid using within-round updates.

> [!note]- Python Solution
> ```python
> def findCheapestPrice(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
>     prices = [float('inf')] * n
>     prices[src] = 0
>
>     for _ in range(k + 1):   # at most k+1 edges = k stops
>         temp = prices[:]
>         for u, v, w in flights:
>             if prices[u] != float('inf') and prices[u] + w < temp[v]:
>                 temp[v] = prices[u] + w
>         prices = temp
>
>     return prices[dst] if prices[dst] != float('inf') else -1
> ```

> [!success] Complexity
> Time O(k × E) where E = number of flights. Space O(n).

> [!tip] Alternatives
> - Dijkstra with state `(cost, node, stops)`: O(E log(n × k)). Valid, slightly faster for dense graphs.
> - BFS level-by-level over price: same as above, slightly different framing.

---

### Jump Game III

> [!example] Problem
> Given array `arr` and start index `start`, at each index `i` you can jump to `i + arr[i]` or `i - arr[i]`. Return true if you can reach any index with value 0.

> [!info] Approach
> - **WHY:** We need to determine reachability — BFS from `start` explores all reachable indices.
> - **WHAT:** BFS treating indices as graph nodes; edges are the two jump targets.
> - **HOW:** Enqueue `start`. For each index, compute both jump targets. If in bounds and unvisited, enqueue. Return True immediately if a target index has value 0.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def canReach(arr: list[int], start: int) -> bool:
>     n = len(arr)
>     visited: set[int] = set()
>     queue: deque[int] = deque([start])
>     while queue:
>         i = queue.popleft()
>         if arr[i] == 0:
>             return True
>         if i in visited:
>             continue
>         visited.add(i)
>         for ni in (i + arr[i], i - arr[i]):
>             if 0 <= ni < n and ni not in visited:
>                 queue.append(ni)
>     return False
> ```

> [!success] Complexity
> Time O(n). Space O(n).

> [!tip] Alternatives
> - DFS / recursion with visited set: same O(n) complexity, risk of stack overflow on large inputs.
> - Marking visited by negating `arr[i]` in place: avoids the set, O(1) extra space, but mutates input.

---

## Topological Sort (Kahn's BFS)

### Course Schedule

> [!example] Problem
> Given `numCourses` and a list of `prerequisites [a, b]` meaning "to take course `a`, you must first take course `b`", return `true` if it is possible to finish all courses (LC 207).

> [!info] Approach
> - **WHY:** The prerequisites form a directed graph; a cycle makes it impossible to finish all courses. Kahn's algorithm detects cycles via in-degree tracking.
> - **WHAT:** Topological sort using BFS (Kahn's algorithm). If all nodes are processed, the graph is a DAG (no cycle).
> - **HOW:** Build adjacency list and in-degree array. Enqueue all nodes with in-degree 0. For each dequeued node, decrement neighbors' in-degrees; enqueue any that reach 0. Count processed nodes — if count equals `numCourses`, return True.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
>     graph: list[list[int]] = [[] for _ in range(numCourses)]
>     in_degree = [0] * numCourses
>     for a, b in prerequisites:
>         graph[b].append(a)
>         in_degree[a] += 1
>
>     queue: deque[int] = deque(i for i in range(numCourses) if in_degree[i] == 0)
>     processed = 0
>     while queue:
>         node = queue.popleft()
>         processed += 1
>         for neighbor in graph[node]:
>             in_degree[neighbor] -= 1
>             if in_degree[neighbor] == 0:
>                 queue.append(neighbor)
>     return processed == numCourses
> ```

> [!success] Complexity
> Time O(V + E). Space O(V + E).

> [!tip] Alternatives
> - DFS cycle detection: color nodes white/grey/black; a back edge (grey → grey) indicates a cycle. O(V + E), same complexity, uses recursion stack.
> - Union-Find: detects cycles in undirected graphs but not directed — not applicable here.

---

### Course Schedule II

> [!example] Problem
> Same setup as Course Schedule, but return one valid ordering of courses to take. Return an empty list if impossible (LC 210).

> [!info] Approach
> - **WHY:** Topological sort produces a valid linear ordering of a DAG. Kahn's BFS directly yields this order.
> - **WHAT:** Same Kahn's BFS as Course Schedule, but record the processing order.
> - **HOW:** Append each dequeued node to `order`. If `len(order) == numCourses`, the graph is a DAG and `order` is a valid schedule. Otherwise return `[]`.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def findOrder(numCourses: int, prerequisites: list[list[int]]) -> list[int]:
>     graph: list[list[int]] = [[] for _ in range(numCourses)]
>     in_degree = [0] * numCourses
>     for a, b in prerequisites:
>         graph[b].append(a)
>         in_degree[a] += 1
>
>     queue: deque[int] = deque(i for i in range(numCourses) if in_degree[i] == 0)
>     order: list[int] = []
>     while queue:
>         node = queue.popleft()
>         order.append(node)
>         for neighbor in graph[node]:
>             in_degree[neighbor] -= 1
>             if in_degree[neighbor] == 0:
>                 queue.append(neighbor)
>     return order if len(order) == numCourses else []
> ```

> [!success] Complexity
> Time O(V + E). Space O(V + E).

> [!tip] Alternatives
> - DFS postorder: process a node after all its descendants; reverse postorder gives topological order. O(V + E).
> - Multiple valid orderings exist; both BFS and DFS give one valid answer but may differ.

---

### Alien Dictionary

> [!example] Problem
> Given a list of words from an alien dictionary sorted in alien lexicographic order, derive the order of letters in the alien alphabet. Return any valid order, or `""` if the ordering is invalid (contains a cycle or a word is a prefix-violated neighbor).

> [!info] Approach
> - **WHY:** Comparing adjacent words in the sorted list reveals ordering constraints between characters (directed edges). The full ordering is a topological sort of these constraints.
> - **WHAT:** Build a directed graph from character ordering constraints. Run Kahn's BFS topological sort.
> - **HOW:** For each adjacent word pair, find the first differing character — that gives an edge. If word A is a prefix of word B but appears after B, return `""` (invalid). Run Kahn's BFS. If all characters are processed, the BFS output is the alien alphabet order.

> [!note]- Python Solution
> ```python
> from collections import deque, defaultdict
>
> def alienOrder(words: list[str]) -> str:
>     # initialize all chars
>     graph: dict[str, list[str]] = defaultdict(list)
>     in_degree: dict[str, int] = {c: 0 for word in words for c in word}
>
>     for i in range(len(words) - 1):
>         w1, w2 = words[i], words[i + 1]
>         min_len = min(len(w1), len(w2))
>         # prefix violation: "abc" before "ab" is invalid
>         if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
>             return ""
>         for j in range(min_len):
>             if w1[j] != w2[j]:
>                 graph[w1[j]].append(w2[j])
>                 in_degree[w2[j]] += 1
>                 break
>
>     queue: deque[str] = deque(c for c in in_degree if in_degree[c] == 0)
>     order: list[str] = []
>     while queue:
>         c = queue.popleft()
>         order.append(c)
>         for neighbor in graph[c]:
>             in_degree[neighbor] -= 1
>             if in_degree[neighbor] == 0:
>                 queue.append(neighbor)
>
>     return "".join(order) if len(order) == len(in_degree) else ""
> ```

> [!success] Complexity
> Time O(C) where C = total characters across all words. Space O(U) where U = unique characters.

> [!tip] Alternatives
> - DFS with cycle detection: same complexity, different code structure.
> - Note: multiple valid orderings may exist; any one is acceptable.

---

## Design

### Design Hit Counter

> [!example] Problem
> Design a hit counter that counts hits in the past 5 minutes (300 seconds). Implement `hit(timestamp)` and `getHits(timestamp)` where timestamps are in seconds (LC 362).

> [!info] Approach
> - **WHY:** Hits older than 300 seconds are never useful again. A queue naturally evicts stale hits from the front.
> - **WHAT:** Deque of timestamps. At each operation, evict timestamps older than `timestamp - 300`.
> - **HOW:** `hit`: append timestamp. `getHits`: evict front while `front <= timestamp - 300`, then return `len(deque)`. Works even with out-of-order calls as long as timestamps are non-decreasing.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> class HitCounter:
>     def __init__(self) -> None:
>         self._q: deque[int] = deque()
>
>     def hit(self, timestamp: int) -> None:
>         self._q.append(timestamp)
>
>     def getHits(self, timestamp: int) -> int:
>         while self._q and self._q[0] <= timestamp - 300:
>             self._q.popleft()
>         return len(self._q)
> ```

> [!success] Complexity
> Time O(1) amortized per operation (each hit added/removed at most once). Space O(hits in last 300s).

> [!tip] Alternatives
> - Circular array of size 300: store `(count, timestamp)` per second bucket — O(1) time, O(300) fixed space. Better for high-throughput systems where many hits share the same second.
> - Follow-up: if hits come in multi-threaded, use locks around the deque operations.

---

### Design Circular Queue

> [!example] Problem
> Implement a circular queue supporting `enQueue(val)`, `deQueue()`, `Front()`, `Rear()`, `isEmpty()`, `isFull()`. Fixed capacity k, O(1) all operations.

> [!info] Approach
> - **WHY:** A plain list wastes space as the front pointer drifts forward. Modular arithmetic wraps pointers around, reusing vacated slots.
> - **WHAT:** Fixed-size array with `front`, `size`, and `capacity`. Rear index = `(front + size) % cap`. Using a `size` counter eliminates the ambiguity between full and empty (the "wasted slot" problem).
> - **HOW:** Enqueue writes to `(front + size) % cap` and increments size. Dequeue advances `front` by 1 (mod cap) and decrements size.

> [!note]- Python Solution
> ```python
> class MyCircularQueue:
>     def __init__(self, k: int) -> None:
>         self._data = [0] * k
>         self._front = 0
>         self._size = 0
>         self._cap = k
>
>     def enQueue(self, value: int) -> bool:
>         if self._size == self._cap:
>             return False
>         rear = (self._front + self._size) % self._cap
>         self._data[rear] = value
>         self._size += 1
>         return True
>
>     def deQueue(self) -> bool:
>         if self._size == 0:
>             return False
>         self._front = (self._front + 1) % self._cap
>         self._size -= 1
>         return True
>
>     def Front(self) -> int:
>         return -1 if self._size == 0 else self._data[self._front]
>
>     def Rear(self) -> int:
>         if self._size == 0:
>             return -1
>         return self._data[(self._front + self._size - 1) % self._cap]
>
>     def isEmpty(self) -> bool:
>         return self._size == 0
>
>     def isFull(self) -> bool:
>         return self._size == self._cap
> ```

> [!success] Complexity
> Time O(1) all operations. Space O(k).

> [!tip] Alternatives
> - Doubly linked list: O(1) all operations, dynamic sizing but more memory overhead per node.
> - Two-pointer without size counter ("wasted slot"): `(rear+1) % cap == front` means full — works but wastes one slot and is error-prone.

---

### Moving Average from Data Stream

> [!example] Problem
> Given a stream of integers and a window size `size`, compute the moving average of the last `size` elements for each new element added.

> [!info] Approach
> - **WHY:** Recomputing the sum from scratch on each insertion is O(size). Maintain a running sum and update it incrementally in O(1).
> - **WHAT:** Fixed-size deque with a running sum.
> - **HOW:** Append each new value to the deque and add to sum. If the deque exceeds `size`, pop from the front and subtract from sum. Return `sum / len(deque)`.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> class MovingAverage:
>     def __init__(self, size: int) -> None:
>         self._window: deque[int] = deque()
>         self._size = size
>         self._sum = 0
>
>     def next(self, val: int) -> float:
>         self._window.append(val)
>         self._sum += val
>         if len(self._window) > self._size:
>             self._sum -= self._window.popleft()
>         return self._sum / len(self._window)
> ```

> [!success] Complexity
> Time O(1) per call. Space O(size).

> [!tip] Alternatives
> - Circular array instead of deque: same O(1), avoids Python deque overhead — use when size is fixed and performance matters.
> - Recompute sum each time: O(size) per call — correct but unnecessary.

---

### Number of Recent Calls

> [!example] Problem
> Implement `RecentCounter` with `ping(t)` which adds a call at time `t` and returns the number of calls in the range `[t - 3000, t]`. Calls are always in strictly increasing order.

> [!info] Approach
> - **WHY:** Old timestamps outside the window are never useful again. A deque lets us discard them from the front in O(1).
> - **WHAT:** Deque storing timestamps. At each `ping`, evict all timestamps < `t - 3000` from the front. Deque size = answer.
> - **HOW:** Append `t`. Pop from front while `front < t - 3000`. Return `len(deque)`.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> class RecentCounter:
>     def __init__(self) -> None:
>         self._q: deque[int] = deque()
>
>     def ping(self, t: int) -> int:
>         self._q.append(t)
>         while self._q[0] < t - 3000:
>             self._q.popleft()
>         return len(self._q)
> ```

> [!success] Complexity
> Time O(1) amortized per ping (each timestamp appended and removed at most once). Space O(3000) = O(1).

> [!tip] Alternatives
> Binary search on a list of all timestamps: O(log n) per call — unnecessary since timestamps are monotonically increasing.

---

### Implement Queue Using Stacks

> [!example] Problem
> Implement a FIFO queue using only two stacks, with O(1) amortized push/pop/peek.

> [!info] Approach
> - **WHY:** A single stack gives LIFO, not FIFO. Two stacks reverse each other: push onto stack1; when stack2 is empty, transfer all of stack1 into stack2 — this reverses the order, making stack2's top the oldest element.
> - **WHAT:** `push_stack` receives all pushes. `pop_stack` is filled lazily from `push_stack` when empty.
> - **HOW:** Each element moves from push → pop exactly once, so amortized O(1) per dequeue.

> [!note]- Python Solution
> ```python
> class MyQueue:
>     def __init__(self) -> None:
>         self._push: list[int] = []
>         self._pop: list[int] = []
>
>     def push(self, x: int) -> None:
>         self._push.append(x)
>
>     def pop(self) -> int:
>         self._transfer()
>         return self._pop.pop()
>
>     def peek(self) -> int:
>         self._transfer()
>         return self._pop[-1]
>
>     def empty(self) -> bool:
>         return not self._push and not self._pop
>
>     def _transfer(self) -> None:
>         if not self._pop:
>             while self._push:
>                 self._pop.append(self._push.pop())
> ```

> [!success] Complexity
> Time O(1) amortized for all operations. Space O(n).

> [!tip] Alternatives
> Transfer on every push instead of lazily: same O(1) amortized but requires reversal back after each operation — more complex.

---

### Implement Stack Using Queues

> [!example] Problem
> Implement a LIFO stack using only queues with `push`, `pop`, `top`, `empty`.

> [!info] Approach
> - **WHY:** A queue is FIFO; to make the most recently pushed element accessible first, we must rotate older elements behind the new one after each push.
> - **WHAT:** Single queue. After each `push(x)`, rotate the queue by popping from the front and re-appending, `len(q) - 1` times — x is now at the front.
> - **HOW:** Push is O(n); pop and top are O(1). (Trade-off: opposite of queue-from-stacks.)

> [!note]- Python Solution
> ```python
> from collections import deque
>
> class MyStack:
>     def __init__(self) -> None:
>         self._q: deque[int] = deque()
>
>     def push(self, x: int) -> None:
>         self._q.append(x)
>         # rotate so x is at the front
>         for _ in range(len(self._q) - 1):
>             self._q.append(self._q.popleft())
>
>     def pop(self) -> int:
>         return self._q.popleft()
>
>     def top(self) -> int:
>         return self._q[0]
>
>     def empty(self) -> bool:
>         return not self._q
> ```

> [!success] Complexity
> Time O(n) push, O(1) pop/top. Space O(n).

> [!tip] Alternatives
> - Two queues: push to q2, move all of q1 behind it, swap names — same O(n) push but uses more memory.
> - Make pop O(n) instead: keep push O(1), rotate on pop. Choose based on which operation is called more frequently.

---

## Priority Queue / Heap

### Task Scheduler

> [!example] Problem
> Given a list of CPU tasks (letters) and a cooldown `n`, return the minimum intervals needed to finish all tasks. During cooldown, the CPU can be idle or execute a different task (LC 621).

> [!info] Approach
> - **WHY:** We always want to execute the most frequent remaining task next (greedy). A max-heap gives the most frequent task in O(log k). When a task is on cooldown, it sits in a queue until it can be re-used.
> - **WHAT:** Max-heap of `(-count, task)` + cooldown queue of `(count_after_use, available_at_time)`.
> - **HOW:** Build frequency map; push all `(-count,)` entries to the heap. At each time tick: if the cooldown queue front is ready (available_at <= time), push it back onto the heap. If the heap is non-empty, pop and execute the most frequent task, push it to the cooldown queue with updated count. Otherwise, idle. Increment time.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import Counter, deque
>
> def leastInterval(tasks: list[str], n: int) -> int:
>     freq = Counter(tasks)
>     heap = [-count for count in freq.values()]
>     heapq.heapify(heap)
>
>     cooldown: deque[tuple[int, int]] = deque()  # (neg_remaining, available_time)
>     time = 0
>     while heap or cooldown:
>         time += 1
>         if cooldown and cooldown[0][1] <= time:
>             neg_rem, _ = cooldown.popleft()
>             heapq.heappush(heap, neg_rem)
>         if heap:
>             neg_rem = heapq.heappop(heap)
>             neg_rem += 1  # task count decreases by 1
>             if neg_rem < 0:
>                 cooldown.append((neg_rem, time + n + 1))
>     return time
> ```

> [!success] Complexity
> Time O(T log k) where T = total intervals, k = unique task types. Space O(k).

> [!tip] Alternatives
> - Math formula: `max(len(tasks), (max_freq - 1) * (n + 1) + count_of_max_freq_tasks)` — O(T) computation, O(1) space. Derivation: most frequent task creates `(max_freq - 1)` cycles of length `(n + 1)` plus a final batch.
> - The heap simulation is easier to adapt for follow-ups (e.g., order must be preserved, variable cooldowns).

---

### Find Median from Data Stream

> [!example] Problem
> Design a data structure that supports `addNum(num)` and `findMedian()`. The median is the middle value of the sorted dataset; for even count it is the average of the two middle values (LC 295).

> [!info] Approach
> - **WHY:** Sorting on every query is O(n log n). Maintaining two heaps — a max-heap of the lower half and a min-heap of the upper half — lets us access the median in O(1).
> - **WHAT:** `lo` = max-heap (lower half), `hi` = min-heap (upper half). Invariant: `len(lo) == len(hi)` or `len(lo) == len(hi) + 1`. The median is `lo[0]` (odd count) or `(lo[0] + hi[0]) / 2` (even count).
> - **HOW:** `addNum`: push to `lo` (negate for max-heap), then balance by moving `lo`'s max to `hi` if `lo[0] > hi[0]` or sizes diverge. Rebalance so `lo` is never smaller than `hi`.

> [!note]- Python Solution
> ```python
> import heapq
>
> class MedianFinder:
>     def __init__(self) -> None:
>         self._lo: list[int] = []  # max-heap (negated)
>         self._hi: list[int] = []  # min-heap
>
>     def addNum(self, num: int) -> None:
>         heapq.heappush(self._lo, -num)
>         # ensure every element in lo <= every element in hi
>         if self._hi and -self._lo[0] > self._hi[0]:
>             heapq.heappush(self._hi, -heapq.heappop(self._lo))
>         # balance sizes: lo can have at most 1 more element than hi
>         if len(self._lo) > len(self._hi) + 1:
>             heapq.heappush(self._hi, -heapq.heappop(self._lo))
>         elif len(self._hi) > len(self._lo):
>             heapq.heappush(self._lo, -heapq.heappop(self._hi))
>
>     def findMedian(self) -> float:
>         if len(self._lo) > len(self._hi):
>             return float(-self._lo[0])
>         return (-self._lo[0] + self._hi[0]) / 2.0
> ```

> [!success] Complexity
> Time O(log n) per `addNum`, O(1) per `findMedian`. Space O(n).

> [!tip] Alternatives
> - Sorted list with bisect: O(n) insert, O(1) median — too slow for large streams.
> - Order statistics tree (e.g., `sortedcontainers.SortedList`): O(log n) insert, O(1) median — clean but not standard library.
> - Follow-up: if numbers are in range [0, 100], use a 101-bucket count array + prefix sums — O(100) per operation.

---

## See Also

[[stack]] | [[graph]] | [[sliding-window]] | [[binary-search]]
