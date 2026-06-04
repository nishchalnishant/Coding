---
tags: [coding, data-structures, queue]
topic: queue
difficulty: mixed
---

# Queue Problems

## Queue Patterns to Recognize

- **FIFO BFS:** Use when every move has equal cost and you want the shortest path or minimum number of steps.
- **Monotonic deque:** Use when the queue must maintain a running minimum or maximum over a sliding window.
- **Multi-source BFS:** Use when many starting points spread simultaneously, like infection, distance-to-nearest, or nearest gate.
- **State-augmented BFS:** Use when position alone is not enough and you must track extra state such as remaining `k`, stops used, or visited mask.
- **Kahn's BFS:** Use when the queue stores zero in-degree nodes for topological ordering or cycle detection.
- **Common pitfalls:** Mark visited when enqueuing, snapshot the queue size for level order, and always handle stale deque entries before using the front element.


> [!abstract] Google Interview Legend
> `🔥 Google` — **Core** problem: extremely high frequency at Google SDE 2/3 interviews. Cover these first.
> `⭐ Google` — **Important** problem: medium frequency at Google SDE 2/3 level. Cover after core.
> Problems without a marker are good practice but less Google-specific at SDE 2/3 level.

---

## Monotonic Deque

### Sliding Window Maximum `🔥 Google`

> [!example] Problem
> You are given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.
> Return the max sliding window.
> 
> **Example 1:**
> ```
> Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
> Output: [3,3,5,5,6,7]
> Explanation: 
> Window position                Max
> ---------------               -----
> [1  3  -1] -3  5  3  6  7       3
>  1 [3  -1  -3] 5  3  6  7       3
>  1  3 [-1  -3  5] 3  6  7       5
>  1  3  -1 [-3  5  3] 6  7       5
>  1  3  -1  -3 [5  3  6] 7       6
>  1  3  -1  -3  5 [3  6  7]      7
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1], k = 1
> Output: [1]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - -10^4 <= nums[i] <= 10^4
> - 1 <= k <= nums.length

> [!info] Approach
> Naive O(nk) rescans the window on every step; we need O(n). A deque that is always sorted descending by value. The front is always the max of the current window. For each index `i` — (1) evict from the back any index whose value ≤ `nums[i]` (they are dominated and can never be future maxima; using `<=` also drops older duplicates); (2) evict from the front if it has fallen outside the window; (3) append `i`; (4) once `i >= k-1`, the front of the deque is the answer. Each index is enqueued and dequeued at most once → O(n) total.

> - **EDGE CASES:** `k = 1` returns the original array; `k = len(nums)` returns a single maximum.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def max_sliding_window(nums, k):
>     dq: deque[int] = deque()   # stores indices; values are monotonically decreasing
>     result = []
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
> Same argument — need O(n), not O(nk). Monotonic increasing deque (front = minimum). Identical to the maximum variant; flip one comparison — evict from the back when `nums[back] >= x` instead of `<=`. The front always holds the index of the current window minimum. Using `>=` keeps the deque short by discarding older duplicates.

> - **EDGE CASES:** `k = 1` returns the original array; duplicate values are safe because the deque stores indices, not values.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def min_sliding_window(nums, k):
>     dq: deque[int] = deque()   # indices; values monotonically increasing
>     result = []
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
> Given an integer array nums and an integer k, return the length of the shortest non-empty subarray of nums with a sum of at least k. If there is no such subarray, return -1.
> A subarray is a contiguous part of an array.
> 
> **Example 1:**
> ```
> Input: nums = [1], k = 1
> Output: 1
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2], k = 4
> Output: -1
> ```
> 
> **Example 3:**
> ```
> Input: nums = [2,-1,2], k = 3
> Output: 3
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - -10^5 <= nums[i] <= 10^5
> - 1 <= k <= 10^9

> [!info] Approach
> Negative values break the simple two-pointer sliding window — shrinking from the left doesn't always decrease the sum. We need a different invariant. Prefix sums + a monotonic increasing deque of prefix-sum indices. `prefix[j] - prefix[i] >= k` with `j > i` means subarray `i..j-1` has sum ≥ k. We want to minimize `j - i`. Compute prefix sums. Maintain a deque of indices with strictly increasing prefix-sum values. For each `j`: while the front of the deque satisfies `prefix[j] - prefix[front] >= k`, update the answer with `j - front` and pop the front (we want the smallest valid `j - i`, so once a shorter subarray is found the front is no longer useful). Then maintain the increasing invariant by popping from the back while `prefix[back] >= prefix[j]`, and append `j`.

> - **EDGE CASES:** Keep `prefix[0] = 0` so subarrays starting at index `0` are handled naturally; if no qualifying subarray exists, return `-1`.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def shortest_subarray(nums, k):
>     n = len(nums)
>     prefix = [0] * (n + 1)
>     for i in range(n):
>         prefix[i + 1] = prefix[i] + nums[i]
> >
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

### Jump Game VI (DP + Sliding Window Max) `🔥 Google`

> [!example] Problem
> You are given a 0-indexed integer array nums and an integer k.
> You are initially standing at index 0. In one move, you can jump at most k steps forward without going outside the boundaries of the array. That is, you can jump from index i to any index in the range [i + 1, min(n - 1, i + k)] inclusive.
> You want to reach the last index of the array (index n - 1). Your score is the sum of all nums[j] for each index j you visited in the array.
> Return the maximum score you can get.
> 
> **Example 1:**
> ```
> Input: nums = [1,-1,-2,4,-7,3], k = 2
> Output: 7
> Explanation: You can choose your jumps forming the subsequence [1,-1,4,3] (underlined above). The sum is 7.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [10,-5,-2,4,0,3], k = 3
> Output: 17
> Explanation: You can choose your jumps forming the subsequence [10,4,3] (underlined above). The sum is 17.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,-5,-20,4,-1,3,-6,-3], k = 2
> Output: 0
> ```
> 
> **Constraints:**
> - 1 <= nums.length, k <= 10^5
> - -10^4 <= nums[i] <= 10^4

> [!info] Approach
> Naive DP `dp[i] = nums[i] + max(dp[i-k..i-1])` is O(nk) — the inner max over a window of size k is expensive. DP with a monotonic decreasing deque to maintain `max(dp[i-k..i-1])` in O(1) per step. `dp[i] = nums[i] + max(dp[j] for j in range(max(0, i-k), i))`. Use a deque of indices in decreasing `dp` value order. Before computing `dp[i]`, evict indices outside the window `[i-k, i-1]` from the front. The front of the deque is `argmax` dp in the window.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def max_result(nums, k):
>     n = len(nums)
>     dp = [0] * n
>     dp[0] = nums[0]
>     dq: deque[int] = deque([0])   # indices; dp values decreasing
> >
>     for i in range(1, n):
>         # evict out-of-window front
>         while dq and dq[0] < i - k:
>             dq.popleft()
>         dp[i] = nums[i] + dp[dq[0]]
>         # maintain decreasing invariant on back
>         while dq and dp[dq[-1]] <= dp[i]:
>             dq.pop()
>         dq.append(i)
> >
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
> Brute force is O(n³). Instead, for each index `i`, find the nearest smaller element on the left and right with a monotonic stack. Then `i` is the minimum for any window up to size `right[i] - left[i] - 1`. Record `ans[window_size] = max(ans[window_size], nums[i])`. Finally run a suffix max on `ans` — a value that wins for a large window also works for smaller ones.

> [!note]- Python Solution
> ```python
> def max_min_of_windows(nums):
>     n = len(nums)
>     left = [-1] * n    # index of previous smaller element
>     right = [n] * n    # index of next smaller element
>     stack = []
> >
>     # previous smaller (left boundary)
>     for i in range(n):
>         while stack and nums[stack[-1]] >= nums[i]:
>             stack.pop()
>         left[i] = stack[-1] if stack else -1
>         stack.append(i)
> >
>     stack.clear()
> >
>     # next smaller (right boundary)
>     for i in range(n - 1, -1, -1):
>         while stack and nums[stack[-1]] >= nums[i]:
>             stack.pop()
>         right[i] = stack[-1] if stack else n
>         stack.append(i)
> >
>     ans = [0] * (n + 1)   # ans[k] = max of minimums for window size k (1-indexed)
>     for i in range(n):
>         w = right[i] - left[i] - 1
>         ans[w] = max(ans[w], nums[i])
> >
>     # suffix maximum: smaller windows can use larger-window answers
>     for k in range(n - 1, 0, -1):
>         ans[k] = max(ans[k], ans[k + 1])
> >
>     return ans[1:]   # return 1-indexed results as 0-indexed array
> ```

> [!success] Complexity
> Time O(n) — two monotonic stack passes + one suffix pass. Space O(n).

> [!tip] Alternatives
> - Segment tree: O(n log n) build + O(log n) per query — for each window size enumerate all windows and take min via range-min query. O(n² log n) total for all sizes — worse.
> - Sparse table RMQ: O(n log n) build, O(1) range-min query — O(n²) total over all window sizes. Still worse than monotonic stack for this specific problem.

---

## BFS / Level-order

### Binary Tree Level Order Traversal `🔥 Google`

> [!example] Problem
> Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).
> 
> **Example 1:**
> ```
> Input: root = [3,9,20,null,null,15,7]
> Output: [[3],[9,20],[15,7]]
> ```
> 
> **Example 2:**
> ```
> Input: root = [1]
> Output: [[1]]
> ```
> 
> **Example 3:**
> ```
> Input: root = []
> Output: []
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 2000].
> - -1000 <= Node.val <= 1000

> [!info] Approach
> DFS mixes levels; BFS processes nodes level-by-level naturally. BFS with level-size snapshotting — record `len(queue)` before processing each level so we know when one level ends and the next begins. Enqueue root. At the start of each BFS iteration snapshot `size = len(queue)`. Dequeue exactly `size` nodes, collect their values, enqueue their children. Append the level list to results.

> [!note]- Python Solution
> ```python
> from collections import deque
> from typing import Optional
> >
> class TreeNode:
>     def __init__(self, val=0, left=None, right=None):
>         self.val = val; self.left = left; self.right = right
> >
> def level_order(root):
>     if not root:
>         return []
>     result = []
>     queue: deque[TreeNode] = deque([root])
>     while queue:
>         level = []
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

### Binary Tree Right Side View `🔥 Google`

> [!example] Problem
> Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.
> 
> **Example 1:**
> ```
> Input: root = [1,2,3,null,5,null,4]
> Output: [1,3,4]
> Explanation:
> ```
> 
> **Example 2:**
> ```
> Input: root = [1,2,3,4,null,null,null,5]
> Output: [1,3,4,5]
> Explanation:
> ```
> 
> **Example 3:**
> ```
> Input: root = [1,null,3]
> Output: [1,3]
> ```
> 
> **Example 4:**
> ```
> Input: root = []
> Output: []
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 100].
> - -100 <= Node.val <= 100

> [!info] Approach
> The rightmost node at each level is exactly the last node dequeued in a level-order BFS. Level-order BFS; record the last node value at each level. Standard level-size snapshotting. After processing all nodes in a level, the most recently processed node value is the rightmost — append it to results.

> [!note]- Python Solution
> ```python
> from collections import deque
> from typing import Optional
> >
> def right_side_view(root):
>     if not root:
>         return []
>     result = []
>     queue: deque[TreeNode] = deque([root])
>     while queue:
>         level_size = len(queue)
>         rightmost = queue[0].val
>         for _ in range(level_size):
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

### 01 Matrix

> [!example] Problem
> Given an m x n binary matrix mat, return the distance of the nearest 0 for each cell.
> The distance between two cells sharing a common edge is 1.
> 
> **Example 1:**
> ```
> Input: mat = [[0,0,0],[0,1,0],[0,0,0]]
> Output: [[0,0,0],[0,1,0],[0,0,0]]
> ```
> 
> **Example 2:**
> ```
> Input: mat = [[0,0,0],[0,1,0],[1,1,1]]
> Output: [[0,0,0],[0,1,0],[1,2,1]]
> ```
> 
> **Constraints:**
> - m == mat.length
> - n == mat[i].length
> - 1 <= m, n <= 10^4
> - 1 <= m * n <= 10^4
> - mat[i][j] is either 0 or 1.
> - There is at least one 0 in mat.

> [!info] Approach
> Running BFS from each `1` independently is O((m×n)²) — too slow. All `0` cells are sources; they spread distance simultaneously. Multi-source BFS seeded with all `0` cells at distance 0. Initialize all `0` cells with distance 0 in the queue. Initialize all `1` cells with `inf`. BFS outward — first time a `1` cell is reached sets its distance. BFS guarantees minimum distance.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def update_matrix(mat):
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
> You are given an `m x n` grid `rooms` initialized with these three possible values.
> 
> 	
> - `-1` A wall or an obstacle.
> 	
> - `0` A gate.
> 	
> - `INF` Infinity means an empty room. We use the value `2^31 - 1 = 2147483647` to represent `INF` as you may assume that the distance to a gate is less than `2147483647`.
> 
> Fill each empty room with the distance to *its nearest gate*. If it is impossible to reach a gate, it should be filled with `INF`.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** rooms = [[2147483647,-1,0,2147483647],[2147483647,2147483647,2147483647,-1],[2147483647,-1,2147483647,-1],[0,-1,2147483647,2147483647]]
> **Output:** [[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,4]]
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** rooms = [[-1]]
> **Output:** [[-1]]
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `m == rooms.length`
> 	
> - `n == rooms[i].length`
> 	
> - `1 <= m, n <= 250`
> 	
> - `rooms[i][j]` is `-1`, `0`, or `2^31 - 1`.

> [!info] Approach
> Starting BFS from each room to find the nearest gate is O(G × m × n). Starting from all gates simultaneously is O(m × n). Multi-source BFS from all gates. Enqueue all cells with value `0` (gates). BFS outward — each `INF` cell reached gets distance = parent's distance + 1. Walls (`-1`) are never enqueued or updated.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def walls_and_gates(rooms):
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
> The cell farthest from all land is the last cell reached when BFS expands outward from all land cells simultaneously. Multi-source BFS from all land cells. The last cell dequeued gives the maximum distance. Seed the queue with all `1` cells at distance 0. BFS outward filling `0` cells. Track the last distance assigned — that is the answer.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def max_distance(grid):
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

### Shortest Path in Binary Matrix `🔥 Google`

> [!example] Problem
> Given an n x n binary matrix grid, return the length of the shortest clear path in the matrix. If there is no clear path, return -1.
> A clear path in a binary matrix is a path from the top-left cell (i.e., (0, 0)) to the bottom-right cell (i.e., (n - 1, n - 1)) such that:
> The length of a clear path is the number of visited cells of this path.
> 
> **Example 1:**
> ```
> Input: grid = [[0,1],[1,0]]
> Output: 2
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[0,0,0],[1,1,0],[1,1,0]]
> Output: 4
> ```
> 
> **Example 3:**
> ```
> Input: grid = [[1,0,0],[1,1,0],[1,1,0]]
> Output: -1
> ```
> 
> **Constraints:**
> - n == grid.length
> - n == grid[i].length
> - 1 <= n <= 100
> - grid[i][j] is 0 or 1

> [!info] Approach
> All edges have equal weight (each step costs 1), so BFS gives the shortest path. Single-source BFS from `(0,0)` over open (value `0`) cells. If start or end is `1`, return -1 immediately. BFS with 8 directions. The first time `(n-1, n-1)` is dequeued, return the current distance + 1.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def shortest_path_binary_matrix(grid):
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

### Minimum Knight Moves `⭐ Google`

> [!example] Problem
> In an **infinite** chess board with coordinates from `-infinity` to `+infinity`, you have a **knight** at square `[0, 0]`.
> 
> A knight has 8 possible moves it can make, as illustrated below. Each move is two squares in a cardinal direction, then one square in an orthogonal direction.
> 
> Return *the minimum number of steps needed to move the knight to the square* `[x, y]`. It is guaranteed the answer exists.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** x = 2, y = 1
> **Output:** 1
> **Explanation: **[0, 0] → [2, 1]
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** x = 5, y = 5
> **Output:** 4
> **Explanation: **[0, 0] → [2, 1] → [4, 2] → [3, 4] → [5, 5]
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `-300 <= x, y <= 300`
> 	
> - `0 <= |x| + |y| <= 300`

> [!info] Approach
> All moves have cost 1; BFS gives the minimum number of moves. BFS from `(0,0)` with 8 knight-move directions. Exploit symmetry to search in the first quadrant only, reducing state space by 4×. Reflect `(x, y)` to `(|x|, |y|)` — knight distances are symmetric. BFS from `(0,0)` inside a bounded box `[-2..x+2] × [-2..y+2]`; the `+2` buffer handles the small detours needed near the origin.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def min_knight_moves(x, y):
>     x, y = abs(x), abs(y)   # exploit symmetry
>     MOVES = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
>     queue: deque[tuple[int, int, int]] = deque([(0, 0, 0)])
>     visited = {(0, 0)}
>     while queue:
>         r, c, steps = queue.popleft()
>         if r == x and c == y:
>             return steps
>         for dr, dc in MOVES:
>             nr, nc = r + dr, c + dc
>             # search in expanded first-quadrant region
>             if (nr, nc) not in visited and -2 <= nr <= x + 2 and -2 <= nc <= y + 2:
>                 visited.add((nr, nc))
>                 queue.append((nr, nc, steps + 1))
>     return -1
> ```

> [!success] Complexity
> Time O((|x| + |y|)^2). Space O((|x| + |y|)^2).

> [!tip] Alternatives
> - Bidirectional BFS: meets in the middle, ~4× fewer states explored — recommended for large `(x, y)`.
> - Math formula: closed-form exists for specific quadrant cases — not worth memorizing, but mention as O(1) follow-up.

---

## BFS Single-Source

### Open the Lock

> [!example] Problem
> You have a lock in front of you with 4 circular wheels. Each wheel has 10 slots: '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'. The wheels can rotate freely and wrap around: for example we can turn '9' to be '0', or '0' to be '9'. Each move consists of turning one wheel one slot.
> The lock initially starts at '0000', a string representing the state of the 4 wheels.
> You are given a list of deadends dead ends, meaning if the lock displays any of these codes, the wheels of the lock will stop turning and you will be unable to open it.
> Given a target representing the value of the wheels that will unlock the lock, return the minimum total number of turns required to open the lock, or -1 if it is impossible.
> 
> **Example 1:**
> ```
> Input: deadends = ["0201","0101","0102","1212","2002"], target = "0202"
> Output: 6
> Explanation: 
> A sequence of valid moves would be "0000" -> "1000" -> "1100" -> "1200" -> "1201" -> "1202" -> "0202".
> Note that a sequence like "0000" -> "0001" -> "0002" -> "0102" -> "0202" would be invalid,
> because the wheels of the lock become stuck after the display becomes the dead end "0102".
> ```
> 
> **Example 2:**
> ```
> Input: deadends = ["8888"], target = "0009"
> Output: 1
> Explanation: We can turn the last wheel in reverse to move from "0000" -> "0009".
> ```
> 
> **Example 3:**
> ```
> Input: deadends = ["8887","8889","8878","8898","8788","8988","7888","9888"], target = "8888"
> Output: -1
> Explanation: We cannot reach the target without getting stuck.
> ```
> 
> **Constraints:**
> - 1 <= deadends.length <= 500
> - deadends[i].length == 4
> - target.length == 4
> - target will not be in the list deadends.
> - target and deadends[i] consist of digits only.

> [!info] Approach
> Each lock state is a node; each valid turn is an edge with weight 1. Shortest path → BFS. BFS on the 4-digit string state space. Each state has 8 neighbors (4 wheels × 2 directions). Mark deadends and the start as visited before BFS begins. The first time `target` is reached, return the current depth.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def open_lock(deadends, target):
>     dead = set(deadends)
>     if "0000" in dead:
>         return -1
>     queue: deque[tuple[str, int]] = deque([("0000", 0)])
>     visited = {"0000"}
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
> You are given an array routes representing bus routes where routes[i] is a bus route that the ith bus repeats forever.
> You will start at the bus stop source (You are not on any bus initially), and you want to go to the bus stop target. You can travel between bus stops by buses only.
> Return the least number of buses you must take to travel from source to target. Return -1 if it is not possible.
> 
> **Example 1:**
> ```
> Input: routes = [[1,2,7],[3,6,7]], source = 1, target = 6
> Output: 2
> Explanation: The best strategy is take the first bus to the bus stop 7, then take the second bus to the bus stop 6.
> ```
> 
> **Example 2:**
> ```
> Input: routes = [[7,12],[4,5,15],[6],[15,19],[9,12,13]], source = 15, target = 12
> Output: -1
> ```
> 
> **Constraints:**
> - 1 <= routes.length <= 500.
> - 1 <= routes[i].length <= 10^5
> - All the values of routes[i] are unique.
> - sum(routes[i].length) <= 10^5
> - 0 <= routes[i][j] < 10^6
> - 0 <= source, target < 10^6

> [!info] Approach
> BFS over stops would revisit stops on the same route repeatedly. Model buses (routes) as nodes, not stops — each bus is taken at cost 1. BFS where each state is a bus route index, not a stop. Build `stop → [bus_indices]` map. BFS starts from all buses that include `source`. For each bus dequeued, visit all its stops; if `target` is reached, return bus count. For each stop on this bus, enqueue all other buses that serve it and haven't been visited. Mark buses as visited to avoid re-boarding.

> [!note]- Python Solution
> ```python
> from collections import deque, defaultdict
> >
> def num_buses_to_destination(routes, source, target):
>     if source == target:
>         return 0
>     stop_to_buses = defaultdict(list)
>     for bus_idx, route in enumerate(routes):
>         for stop in route:
>             stop_to_buses[stop].append(bus_idx)
> >
>     visited_buses = set()
>     visited_stops = {source}
>     queue: deque[tuple[int, int]] = deque()  # (bus_index, buses_taken)
>     for bus in stop_to_buses[source]:
>         queue.append((bus, 1))
>         visited_buses.add(bus)
> >
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
> Standard BFS doesn't capture how many eliminations have been used — two paths to the same cell may have different remaining `k`. The state must include `k`. BFS with 3D state `(row, col, remaining_k)`. Enqueue `(0, 0, k)` with 0 steps. For each cell, try all 4 neighbors — if a neighbor is free, step to it; if it's an obstacle and `remaining_k > 0`, step to it and decrement `k`. Mark `(r, c, k)` as visited — not just `(r, c)`.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def shortest_path(grid, k):
>     m, n = len(grid), len(grid[0])
>     if m == 1 and n == 1:
>         return 0
>     # State: (r, c, remaining_k)
>     visited = {(0, 0, k)}
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

### Cheapest Flights Within K Stops `⭐ Google`

> [!example] Problem
> There are n cities connected by some number of flights. You are given an array flights where flights[i] = [fromi, toi, pricei] indicates that there is a flight from city fromi to city toi with cost pricei.
> You are also given three integers src, dst, and k, return the cheapest price from src to dst with at most k stops. If there is no such route, return -1.
> 
> **Example 1:**
> ```
> Input: n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], src = 0, dst = 3, k = 1
> Output: 700
> Explanation:
> The graph is shown above.
> The optimal path with at most 1 stop from city 0 to 3 is marked in red and has cost 100 + 600 = 700.
> Note that the path through cities [0,1,2,3] is cheaper but is invalid because it uses 2 stops.
> ```
> 
> **Example 2:**
> ```
> Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 1
> Output: 200
> Explanation:
> The graph is shown above.
> The optimal path with at most 1 stop from city 0 to 2 is marked in red and has cost 100 + 100 = 200.
> ```
> 
> **Example 3:**
> ```
> Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 0
> Output: 500
> Explanation:
> The graph is shown above.
> The optimal path with no stops from city 0 to 2 is marked in red and has cost 500.
> ```
> 
> **Constraints:**
> - 1 <= n <= 100
> - 0 <= flights.length <= (n * (n - 1) / 2)
> - flights[i].length == 3
> - 0 <= fromi, toi < n
> - fromi != toi
> - 1 <= pricei <= 10^4
> - There will not be any multiple flights between two cities.
> - 0 <= src, dst, k < n
> - src != dst

> [!info] Approach
> Standard Dijkstra may revisit a node via a longer path that uses fewer stops, blocking a cheaper path that needs more stops. The stop count is part of the state. BFS level-by-level (level = number of stops used). At each level, update costs. Use Bellman-Ford with exactly `k+1` relaxation rounds. Maintain `prices[node]` = cheapest price to reach `node` using at most `current_round` hops. Use a copy of prices per round to avoid using within-round updates.

> [!note]- Python Solution
> ```python
> def find_cheapest_price(n, flights, src, dst, k):
>     prices = [float('inf')] * n
>     prices[src] = 0
> >
>     for _ in range(k + 1):   # at most k+1 edges = k stops
>         temp = prices[:]
>         for u, v, w in flights:
>             if prices[u] != float('inf') and prices[u] + w < temp[v]:
>                 temp[v] = prices[u] + w
>         prices = temp
> >
>     return prices[dst] if prices[dst] != float('inf') else -1
> ```

> [!success] Complexity
> Time O(k × E) where E = number of flights. Space O(n).

> [!tip] Alternatives
> - Dijkstra with state `(cost, node, stops)`: O(E log(n × k)). Valid, slightly faster for dense graphs.
> - BFS level-by-level over price: same as above, slightly different framing.

---

### Jump Game III `🔥 Google`

> [!example] Problem
> Given an array of non-negative integers arr, you are initially positioned at start index of the array. When you are at index i, you can jump to i + arr[i] or i - arr[i], check if you can reach any index with value 0.
> Notice that you can not jump outside of the array at any time.
> 
> **Example 1:**
> ```
> Input: arr = [4,2,3,0,3,1,2], start = 5
> Output: true
> Explanation: 
> All possible ways to reach at index 3 with value 0 are: 
> index 5 -> index 4 -> index 1 -> index 3 
> index 5 -> index 6 -> index 4 -> index 1 -> index 3
> ```
> 
> **Example 2:**
> ```
> Input: arr = [4,2,3,0,3,1,2], start = 0
> Output: true 
> Explanation: 
> One possible way to reach at index 3 with value 0 is: 
> index 0 -> index 4 -> index 1 -> index 3
> ```
> 
> **Example 3:**
> ```
> Input: arr = [3,0,2,1,2], start = 2
> Output: false
> Explanation: There is no way to reach at index 1 with value 0.
> ```
> 
> **Constraints:**
> - 1 <= arr.length <= 5 * 10^4
> - 0 <= arr[i] < arr.length
> - 0 <= start < arr.length

> [!info] Approach
> We need to determine reachability — BFS from `start` explores all reachable indices. BFS treating indices as graph nodes; edges are the two jump targets. Enqueue `start`. For each index, compute both jump targets. If in bounds and unvisited, enqueue. Return True immediately if a target index has value 0.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def can_reach(arr, start):
>     n = len(arr)
>     visited = set()
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

### Course Schedule `🔥 Google`

> [!example] Problem
> There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.
> Return true if you can finish all courses. Otherwise, return false.
> 
> **Example 1:**
> ```
> Input: numCourses = 2, prerequisites = [[1,0]]
> Output: true
> Explanation: There are a total of 2 courses to take. 
> To take course 1 you should have finished course 0. So it is possible.
> ```
> 
> **Example 2:**
> ```
> Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
> Output: false
> Explanation: There are a total of 2 courses to take. 
> To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.
> ```
> 
> **Constraints:**
> - 1 <= numCourses <= 2000
> - 0 <= prerequisites.length <= 5000
> - prerequisites[i].length == 2
> - 0 <= ai, bi < numCourses
> - All the pairs prerequisites[i] are unique.

> [!info] Approach
> The prerequisites form a directed graph; a cycle makes it impossible to finish all courses. Kahn's algorithm detects cycles via in-degree tracking. Topological sort using BFS (Kahn's algorithm). If all nodes are processed, the graph is a DAG (no cycle). Build adjacency list and in-degree array. Enqueue all nodes with in-degree 0. For each dequeued node, decrement neighbors' in-degrees; enqueue any that reach 0. Count processed nodes — if count equals `numCourses`, return True.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def can_finish(numCourses, prerequisites):
>     graph = [[] for _ in range(numCourses)]
>     in_degree = [0] * numCourses
>     for a, b in prerequisites:
>         graph[b].append(a)
>         in_degree[a] += 1
> >
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

### Alien Dictionary `⭐ Google`

> [!example] Problem
> There is a new alien language that uses the English alphabet. However, the order of the letters is unknown to you.
> 
> You are given a list of strings `words` from the alien language's dictionary. Now it is claimed that the strings in `words` are **sorted lexicographically** by the rules of this new language.
> 
> If this claim is incorrect, and the given arrangement of string in `words` cannot correspond to any order of letters, return `"".`
> 
> Otherwise, return *a string of the unique letters in the new alien language sorted in **lexicographically increasing order** by the new language's rules**. *If there are multiple solutions, return* **any of them***.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** words = ["wrt","wrf","er","ett","rftt"]
> **Output:** "wertf"
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** words = ["z","x"]
> **Output:** "zx"
> 
> ```
> 
> Example 3:
> 
> ```
> 
> **Input:** words = ["z","x","z"]
> **Output:** ""
> **Explanation:** The order is invalid, so return `""`.
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= words.length <= 100`
> 	
> - `1 <= words[i].length <= 100`
> 	
> - `words[i]` consists of only lowercase English letters.

> [!info] Approach
> Comparing adjacent words in the sorted list reveals ordering constraints between characters (directed edges). The full ordering is a topological sort of these constraints. Build a directed graph from character ordering constraints. Run Kahn's BFS topological sort. For each adjacent word pair, find the first differing character — that gives an edge. If word A is a prefix of word B but appears after B, return `""` (invalid). Run Kahn's BFS. If all characters are processed, the BFS output is the alien alphabet order.

> [!note]- Python Solution
> ```python
> from collections import deque, defaultdict
> >
> def alien_order(words):
>     # initialize all chars
>     graph = defaultdict(list)
>     in_degree = {c: 0 for word in words for c in word}
> >
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
> >
>     queue: deque[str] = deque(c for c in in_degree if in_degree[c] == 0)
>     order = []
>     while queue:
>         c = queue.popleft()
>         order.append(c)
>         for neighbor in graph[c]:
>             in_degree[neighbor] -= 1
>             if in_degree[neighbor] == 0:
>                 queue.append(neighbor)
> >
>     return "".join(order) if len(order) == len(in_degree) else ""
> ```

> [!success] Complexity
> Time O(C) where C = total characters across all words. Space O(U) where U = unique characters.

> [!tip] Alternatives
> - DFS with cycle detection: same complexity, different code structure.
> - Note: multiple valid orderings may exist; any one is acceptable.

---

## Design

### Design Hit Counter `⭐ Google`

> [!example] Problem
> Design a hit counter which counts the number of hits received in the past `5` minutes (i.e., the past `300` seconds).
> 
> Your system should accept a `timestamp` parameter (**in seconds** granularity), and you may assume that calls are being made to the system in chronological order (i.e., `timestamp` is monotonically increasing). Several hits may arrive roughly at the same time.
> 
> Implement the `HitCounter` class:
> 
> 	
> - `HitCounter()` Initializes the object of the hit counter system.
> 	
> - `void hit(int timestamp)` Records a hit that happened at `timestamp` (**in seconds**). Several hits may happen at the same `timestamp`.
> 	
> - `int getHits(int timestamp)` Returns the number of hits in the past 5 minutes from `timestamp` (i.e., the past `300` seconds).
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input**
> ["HitCounter", "hit", "hit", "hit", "getHits", "hit", "getHits", "getHits"]
> [[], [1], [2], [3], [4], [300], [300], [301]]
> **Output**
> [null, null, null, null, 3, null, 4, 3]
> 
> **Explanation**
> HitCounter hitCounter = new HitCounter();
> hitCounter.hit(1);       // hit at timestamp 1.
> hitCounter.hit(2);       // hit at timestamp 2.
> hitCounter.hit(3);       // hit at timestamp 3.
> hitCounter.getHits(4);   // get hits at timestamp 4, return 3.
> hitCounter.hit(300);     // hit at timestamp 300.
> hitCounter.getHits(300); // get hits at timestamp 300, return 4.
> hitCounter.getHits(301); // get hits at timestamp 301, return 3.
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= timestamp <= 2 * 10^9`
> 	
> - All the calls are being made to the system in chronological order (i.e., `timestamp` is monotonically increasing).
> 	
> - At most `300` calls will be made to `hit` and `getHits`.
> 
>  
> 
> **Follow up:** What if the number of hits per second could be huge? Does your design scale?

> [!info] Approach
> Hits older than 300 seconds are never useful again. A queue naturally evicts stale hits from the front. Deque of timestamps. At each operation, evict timestamps older than `timestamp - 300`. `hit`: append timestamp. `getHits`: evict front while `front <= timestamp - 300`, then return `len(deque)`. This assumes calls arrive with non-decreasing timestamps, which is the usual interview contract.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> class HitCounter:
>     def __init__(self):
>         self._q: deque[int] = deque()
> >
>     def hit(self, timestamp):
>         self._q.append(timestamp)
> >
>     def get_hits(self, timestamp):
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

### Design Circular Queue `⭐ Google`

> [!example] Problem
> Design your implementation of the circular queue. The circular queue is a linear data structure in which the operations are performed based on FIFO (First In First Out) principle, and the last position is connected back to the first position to make a circle. It is also called "Ring Buffer".
> One of the benefits of the circular queue is that we can make use of the spaces in front of the queue. In a normal queue, once the queue becomes full, we cannot insert the next element even if there is a space in front of the queue. But using the circular queue, we can use the space to store new values.
> Implement the MyCircularQueue class:
> You must solve the problem without using the built-in queue data structure in your programming language.
> 
> **Example 1:**
> ```
> Input
> ["MyCircularQueue", "enQueue", "enQueue", "enQueue", "enQueue", "Rear", "isFull", "deQueue", "enQueue", "Rear"]
> [[3], [1], [2], [3], [4], [], [], [], [4], []]
> Output
> [null, true, true, true, false, 3, true, true, true, 4]
> 
> Explanation
> MyCircularQueue myCircularQueue = new MyCircularQueue(3);
> myCircularQueue.enQueue(1); // return True
> myCircularQueue.enQueue(2); // return True
> myCircularQueue.enQueue(3); // return True
> myCircularQueue.enQueue(4); // return False
> myCircularQueue.Rear();     // return 3
> myCircularQueue.isFull();   // return True
> myCircularQueue.deQueue();  // return True
> myCircularQueue.enQueue(4); // return True
> myCircularQueue.Rear();     // return 4
> ```
> 
> **Constraints:**
> - 1 <= k <= 1000
> - 0 <= value <= 1000
> - At most 3000 calls will be made to enQueue, deQueue, Front, Rear, isEmpty, and isFull.

> [!info] Approach
> A plain list wastes space as the front pointer drifts forward. Modular arithmetic wraps pointers around, reusing vacated slots. Fixed-size array with `front`, `size`, and `capacity`. Rear index = `(front + size) % cap`. Using a `size` counter eliminates the ambiguity between full and empty (the "wasted slot" problem). Enqueue writes to `(front + size) % cap` and increments size. Dequeue advances `front` by 1 (mod cap) and decrements size.

> [!note]- Python Solution
> ```python
> class MyCircularQueue:
>     def __init__(self, k):
>         self._data = [0] * k
>         self._front = 0
>         self._size = 0
>         self._cap = k
> >
>     def en_queue(self, value):
>         if self._size == self._cap:
>             return False
>         rear = (self._front + self._size) % self._cap
>         self._data[rear] = value
>         self._size += 1
>         return True
> >
>     def de_queue(self):
>         if self._size == 0:
>             return False
>         self._front = (self._front + 1) % self._cap
>         self._size -= 1
>         return True
> >
>     def front(self):
>         return -1 if self._size == 0 else self._data[self._front]
> >
>     def rear(self):
>         if self._size == 0:
>             return -1
>         return self._data[(self._front + self._size - 1) % self._cap]
> >
>     def is_empty(self):
>         return self._size == 0
> >
>     def is_full(self):
>         return self._size == self._cap
> ```

> [!success] Complexity
> Time O(1) all operations. Space O(k).

> [!tip] Alternatives
> - Doubly linked list: O(1) all operations, dynamic sizing but more memory overhead per node.
> - Two-pointer without size counter ("wasted slot"): `(rear+1) % cap == front` means full — works but wastes one slot and is error-prone.

---

### Moving Average from Data Stream `⭐ Google`

> [!example] Problem
> Given a stream of integers and a window size, calculate the moving average of all integers in the sliding window.
> 
> Implement the `MovingAverage` class:
> 
> 	
> - `MovingAverage(int size)` Initializes the object with the size of the window `size`.
> 	
> - `double next(int val)` Returns the moving average of the last `size` values of the stream.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input**
> ["MovingAverage", "next", "next", "next", "next"]
> [[3], [1], [10], [3], [5]]
> **Output**
> [null, 1.0, 5.5, 4.66667, 6.0]
> 
> **Explanation**
> MovingAverage movingAverage = new MovingAverage(3);
> movingAverage.next(1); // return 1.0 = 1 / 1
> movingAverage.next(10); // return 5.5 = (1 + 10) / 2
> movingAverage.next(3); // return 4.66667 = (1 + 10 + 3) / 3
> movingAverage.next(5); // return 6.0 = (10 + 3 + 5) / 3
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= size <= 1000`
> 	
> - `-10^5 <= val <= 10^5`
> 	
> - At most `10^4` calls will be made to `next`.

> [!info] Approach
> Recomputing the sum from scratch on each insertion is O(size). Maintain a running sum and update it incrementally in O(1). Fixed-size deque with a running sum. Append each new value to the deque and add to sum. If the deque exceeds `size`, pop from the front and subtract from sum. Return `sum / len(deque)`.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> class MovingAverage:
>     def __init__(self, size):
>         self._window: deque[int] = deque()
>         self._size = size
>         self._sum = 0
> >
>     def next(self, val):
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
> You have a RecentCounter class which counts the number of recent requests within a certain time frame.
> Implement the RecentCounter class:
> It is guaranteed that every call to ping uses a strictly larger value of t than the previous call.
> 
> **Example 1:**
> ```
> Input
> ["RecentCounter", "ping", "ping", "ping", "ping"]
> [[], [1], [100], [3001], [3002]]
> Output
> [null, 1, 2, 3, 3]
> 
> Explanation
> RecentCounter recentCounter = new RecentCounter();
> recentCounter.ping(1);     // requests = [1], range is [-2999,1], return 1
> recentCounter.ping(100);   // requests = [1, 100], range is [-2900,100], return 2
> recentCounter.ping(3001);  // requests = [1, 100, 3001], range is [1,3001], return 3
> recentCounter.ping(3002);  // requests = [1, 100, 3001, 3002], range is [2,3002], return 3
> ```
> 
> **Constraints:**
> - 1 <= t <= 10^9
> - Each test case will call ping with strictly increasing values of t.
> - At most 10^4 calls will be made to ping.

> [!info] Approach
> Old timestamps outside the window are never useful again. A deque lets us discard them from the front in O(1). Deque storing timestamps. At each `ping`, evict all timestamps < `t - 3000` from the front. Deque size = answer. Append `t`. Pop from front while `front < t - 3000`. Return `len(deque)`.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> class RecentCounter:
>     def __init__(self):
>         self._q: deque[int] = deque()
> >
>     def ping(self, t):
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

### Implement Stack Using Queues

> [!example] Problem
> Implement a last-in-first-out (LIFO) stack using only two queues. The implemented stack should support all the functions of a normal stack (push, top, pop, and empty).
> Implement the MyStack class:
> Notes
> 
> **Example 1:**
> ```
> Input
> ["MyStack", "push", "push", "top", "pop", "empty"]
> [[], [1], [2], [], [], []]
> Output
> [null, null, null, 2, 2, false]
> 
> Explanation
> MyStack myStack = new MyStack();
> myStack.push(1);
> myStack.push(2);
> myStack.top(); // return 2
> myStack.pop(); // return 2
> myStack.empty(); // return False
> ```
> 
> **Constraints:**
> - 1 <= x <= 9
> - At most 100 calls will be made to push, pop, top, and empty.
> - All the calls to pop and top are valid.

> [!info] Approach
> A queue is FIFO; to make the most recently pushed element accessible first, we must rotate older elements behind the new one after each push. Single queue. After each `push(x)`, rotate the queue by popping from the front and re-appending, `len(q) - 1` times — x is now at the front. Push is O(n); pop and top are O(1). (Trade-off: opposite of queue-from-stacks.)

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> class MyStack:
>     def __init__(self):
>         self._q: deque[int] = deque()
> >
>     def push(self, x):
>         self._q.append(x)
>         # rotate so x is at the front
>         for _ in range(len(self._q) - 1):
>             self._q.append(self._q.popleft())
> >
>     def pop(self):
>         return self._q.popleft()
> >
>     def top(self):
>         return self._q[0]
> >
>     def empty(self):
>         return not self._q
> ```

> [!success] Complexity
> Time O(n) push, O(1) pop/top. Space O(n).

> [!tip] Alternatives
> - Two queues: push to q2, move all of q1 behind it, swap names — same O(n) push but uses more memory.
> - Make pop O(n) instead: keep push O(1), rotate on pop. Choose based on which operation is called more frequently.

---

## Priority Queue / Heap

### Task Scheduler `🔥 Google`

> [!example] Problem
> You are given an array of CPU tasks, each labeled with a letter from A to Z, and a number n. Each CPU interval can be idle or allow the completion of one task. Tasks can be completed in any order, but there's a constraint: there has to be a gap of at least n intervals between two tasks with the same label.
> Return the minimum number of CPU intervals required to complete all tasks.
> 
> **Example 1:**
> ```
> Input: tasks = ["A","A","A","B","B","B"], n = 2
> Output: 8
> Explanation: A possible sequence is: A -> B -> idle -> A -> B -> idle -> A -> B.
> After completing task A, you must wait two intervals before doing A again. The same applies to task B. In the 3 rd interval, neither A nor B can be done, so you idle. By the 4 th interval, you can do A again as 2 intervals have passed.
> ```
> 
> **Example 2:**
> ```
> Input: tasks = ["A","C","A","B","D","B"], n = 1
> Output: 6
> Explanation: A possible sequence is: A -> B -> C -> D -> A -> B.
> With a cooling interval of 1, you can repeat a task after just one other task.
> ```
> 
> **Example 3:**
> ```
> Input: tasks = ["A","A","A", "B","B","B"], n = 3
> Output: 10
> Explanation: A possible sequence is: A -> B -> idle -> idle -> A -> B -> idle -> idle -> A -> B.
> There are only two types of tasks, A and B, which need to be separated by 3 intervals. This leads to idling twice between repetitions of these tasks.
> ```
> 
> **Constraints:**
> - 1 <= tasks.length <= 10^4
> - tasks[i] is an uppercase English letter.
> - 0 <= n <= 100

> [!info] Approach
> We always want to execute the most frequent remaining task next (greedy). A max-heap gives the most frequent task in O(log k). When a task is on cooldown, it sits in a queue until it can be re-used. Max-heap of `(-count, task)` + cooldown queue of `(count_after_use, available_at_time)`. Build frequency map; push all `(-count,)` entries to the heap. At each time tick: if the cooldown queue front is ready (available_at <= time), push it back onto the heap. If the heap is non-empty, pop and execute the most frequent task, push it to the cooldown queue with updated count. Otherwise, idle. Increment time.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import Counter, deque
> >
> def least_interval(tasks, n):
>     freq = Counter(tasks)
>     heap = [-count for count in freq.values()]
>     heapq.heapify(heap)
> >
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

### Find Median from Data Stream `🔥 Google`

> [!example] Problem
> The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.
> Implement the MedianFinder class
> 
> **Example 1:**
> ```
> Input
> ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
> [[], [1], [2], [], [3], []]
> Output
> [null, null, null, 1.5, null, 2.0]
> 
> Explanation
> MedianFinder medianFinder = new MedianFinder();
> medianFinder.addNum(1);    // arr = [1]
> medianFinder.addNum(2);    // arr = [1, 2]
> medianFinder.findMedian(); // return 1.5 (i.e., (1 + 2) / 2)
> medianFinder.addNum(3);    // arr[1, 2, 3]
> medianFinder.findMedian(); // return 2.0
> ```
> 
> **Constraints:**
> - -10^5 <= num <= 10^5
> - There will be at least one element in the data structure before calling findMedian.
> - At most 5 * 10^4 calls will be made to addNum and findMedian.

> [!info] Approach
> Sorting on every query is O(n log n). Maintaining two heaps — a max-heap of the lower half and a min-heap of the upper half — lets us access the median in O(1). `lo` = max-heap (lower half), `hi` = min-heap (upper half). Invariant: `len(lo) == len(hi)` or `len(lo) == len(hi) + 1`. The median is `lo[0]` (odd count) or `(lo[0] + hi[0]) / 2` (even count). `addNum`: push to `lo` (negate for max-heap), then balance by moving `lo`'s max to `hi` if `lo[0] > hi[0]` or sizes diverge. Rebalance so `lo` is never smaller than `hi`.

> [!note]- Python Solution
> ```python
> import heapq
> >
> class MedianFinder:
>     def __init__(self):
>         self._lo: list[int] = []  # max-heap (negated)
>         self._hi: list[int] = []  # min-heap
> >
>     def add_num(self, num):
>         heapq.heappush(self._lo, -num)
>         # ensure every element in lo <= every element in hi
>         if self._hi and -self._lo[0] > self._hi[0]:
>             heapq.heappush(self._hi, -heapq.heappop(self._lo))
>         # balance sizes: lo can have at most 1 more element than hi
>         if len(self._lo) > len(self._hi) + 1:
>             heapq.heappush(self._hi, -heapq.heappop(self._lo))
>         elif len(self._hi) > len(self._lo):
>             heapq.heappush(self._lo, -heapq.heappop(self._hi))
> >
>     def find_median(self):
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
### Design Circular Deque

> [!example] Problem
> Design your implementation of the circular double-ended queue (deque).
> Implement the MyCircularDeque class
> 
> **Example 1:**
> ```
> Input
> ["MyCircularDeque", "insertLast", "insertLast", "insertFront", "insertFront", "getRear", "isFull", "deleteLast", "insertFront", "getFront"]
> [[3], [1], [2], [3], [4], [], [], [], [4], []]
> Output
> [null, true, true, true, false, 2, true, true, true, 4]
> 
> Explanation
> MyCircularDeque myCircularDeque = new MyCircularDeque(3);
> myCircularDeque.insertLast(1);  // return True
> myCircularDeque.insertLast(2);  // return True
> myCircularDeque.insertFront(3); // return True
> myCircularDeque.insertFront(4); // return False, the queue is full.
> myCircularDeque.getRear();      // return 2
> myCircularDeque.isFull();       // return True
> myCircularDeque.deleteLast();   // return True
> myCircularDeque.insertFront(4); // return True
> myCircularDeque.getFront();     // return 4
> ```
> 
> **Constraints:**
> - 1 <= k <= 1000
> - 0 <= value <= 1000
> - At most 2000 calls will be made to insertFront, insertLast, deleteFront, deleteLast, getFront, getRear, isEmpty, isFull.

> [!info] Approach
> A circular buffer lets us use O(1) index arithmetic without shifting elements. Maintain `front`, `rear`, `size`, and an array of capacity `k`. Update indices with modulo arithmetic. For example, moving left uses `(idx - 1 + k) % k` and moving right uses `(idx + 1) % k`.

> [!note]- Python Solution
> ```python
> class MyCircularDeque:
>     def __init__(self, k):
>         self.arr = [0] * k
>         self.k = k
>         self.front = 0
>         self.size = 0
> 
>     def insert_front(self, value):
>         if self.isFull():
>             return False
>         self.front = (self.front - 1 + self.k) % self.k
>         self.arr[self.front] = value
>         self.size += 1
>         return True
> ```

> [!success] Complexity
> O(1) for every operation, O(k) space.

> [!tip] Alternatives
> Linked-list deque is easier to generalize but has more pointer overhead than a circular array.

---

## Sliding Window with Queue

### Sliding Window Median (LC 480) `⭐ Google`

> [!example] Problem
> The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value. So the median is the mean of the two middle values.
> You are given an integer array nums and an integer k. There is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.
> Return the median array for each window in the original array. Answers within 10-5 of the actual value will be accepted.
> 
> **Example 1:**
> ```
> Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
> Output: [1.00000,-1.00000,-1.00000,3.00000,5.00000,6.00000]
> Explanation: 
> Window position                Median
> ---------------                -----
> [1  3  -1] -3  5  3  6  7        1
>  1 [3  -1  -3] 5  3  6  7       -1
>  1  3 [-1  -3  5] 3  6  7       -1
>  1  3  -1 [-3  5  3] 6  7        3
>  1  3  -1  -3 [5  3  6] 7        5
>  1  3  -1  -3  5 [3  6  7]       6
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3,4,2,3,1,4,2], k = 3
> Output: [2.00000,3.00000,3.00000,3.00000,2.00000,3.00000,2.00000]
> ```
> 
> **Constraints:**
> - 1 <= k <= nums.length <= 10^5
> - -2^{31} <= nums[i] <= 2^{31} - 1

> [!info] Approach
> Recalculating the median from scratch for each window is O(k log k) per step — too slow. Maintaining two heaps (like the "Find Median from Data Stream" problem) allows O(log k) updates, but removal of the outgoing element requires lazy deletion. Use a max-heap `lo` (lower half) and min-heap `hi` (upper half). On each step, add the incoming element and lazy-delete the outgoing element. Rebalance heaps after each operation. Lazy deletion: track counts of "dead" elements in each heap. When computing the median, first pop any dead elements from the heap tops. Balance rule: `len(lo) == len(hi)` or `len(lo) == len(hi) + 1`.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
> >
> def median_sliding_window(nums, k):
>     lo = []   # max-heap (negated), lower half
>     hi = []   # min-heap, upper half
>     dead = defaultdict(int)
>     result = []
> >
>     def push(x):
>         heapq.heappush(lo, -x)
>         heapq.heappush(hi, -heapq.heappop(lo))
>         if len(hi) > len(lo):
>             heapq.heappush(lo, -heapq.heappop(hi))
> >
>     def prune(heap, is_max):
>         while heap and dead[(-heap[0] if is_max else heap[0])] > 0:
>             val = -heapq.heappop(heap) if is_max else heapq.heappop(heap)
>             dead[val] -= 1
> >
>     for i, num in enumerate(nums):
>         push(num)
>         if i >= k:
>             out = nums[i - k]
>             dead[out] += 1
>             prune(lo, is_max=True)
>             prune(hi, is_max=False)
>             if len(lo) - len(hi) > 1:
>                 heapq.heappush(hi, -heapq.heappop(lo))
>             elif len(hi) > len(lo):
>                 heapq.heappush(lo, -heapq.heappop(hi))
>         if i >= k - 1:
>             prune(lo, is_max=True)
>             if k % 2 == 1:
>                 result.append(float(-lo[0]))
>             else:
>                 result.append((-lo[0] + hi[0]) / 2.0)
>     return result
> ```

> [!success] Complexity
> Time O(n log k), Space O(n).

> [!tip] Alternatives
> - `SortedList` from `sortedcontainers`: O(log k) insert and delete, O(1) median access — cleaner code but not standard library.
> - Segment tree on compressed values: O(n log n) with precise deletion, no lazy bookkeeping.
> - Key insight: lazy deletion works because dead elements only affect the heap top when computing the median; they stay valid otherwise.

---

## Scheduling

### Task Scheduler with Cooldown (LC 621)

> [!example] Problem
> You are given an array of CPU tasks, each labeled with a letter from A to Z, and a number n. Each CPU interval can be idle or allow the completion of one task. Tasks can be completed in any order, but there's a constraint: there has to be a gap of at least n intervals between two tasks with the same label.
> Return the minimum number of CPU intervals required to complete all tasks.
> 
> **Example 1:**
> ```
> Input: tasks = ["A","A","A","B","B","B"], n = 2
> Output: 8
> Explanation: A possible sequence is: A -> B -> idle -> A -> B -> idle -> A -> B.
> After completing task A, you must wait two intervals before doing A again. The same applies to task B. In the 3 rd interval, neither A nor B can be done, so you idle. By the 4 th interval, you can do A again as 2 intervals have passed.
> ```
> 
> **Example 2:**
> ```
> Input: tasks = ["A","C","A","B","D","B"], n = 1
> Output: 6
> Explanation: A possible sequence is: A -> B -> C -> D -> A -> B.
> With a cooling interval of 1, you can repeat a task after just one other task.
> ```
> 
> **Example 3:**
> ```
> Input: tasks = ["A","A","A", "B","B","B"], n = 3
> Output: 10
> Explanation: A possible sequence is: A -> B -> idle -> idle -> A -> B -> idle -> idle -> A -> B.
> There are only two types of tasks, A and B, which need to be separated by 3 intervals. This leads to idling twice between repetitions of these tasks.
> ```
> 
> **Constraints:**
> - 1 <= tasks.length <= 10^4
> - tasks[i] is an uppercase English letter.
> - 0 <= n <= 100

> [!info] Approach
> The bottleneck is the most frequent task — it dictates the minimum frame length. Tasks can be arranged in cycles of length `n+1`; less frequent tasks or idle slots fill the gaps. Count task frequencies. The answer is `max(total_tasks, (max_freq - 1) * (n + 1) + count_of_tasks_with_max_freq)`. Count frequencies with a Counter. `max_freq` = highest frequency. `max_count` = number of tasks that share that frequency. Formula accounts for `max_freq - 1` complete cycles, each of length `n+1`, plus the final partial cycle of `max_count` tasks.

> [!note]- Python Solution
> ```python
> from collections import Counter
> >
> def least_interval(tasks, n):
>     freq = Counter(tasks)
>     max_freq = max(freq.values())
>     max_count = sum(1 for f in freq.values() if f == max_freq)
>     slots_needed = (max_freq - 1) * (n + 1) + max_count
>     return max(len(tasks), slots_needed)
> ```

> [!success] Complexity
> Time O(n) where n = number of tasks, Space O(1) (26 letters max).

> [!tip] Alternatives
> - Greedy simulation with a max-heap and cooldown queue: at each step, pick the most frequent available task. Enqueue tasks back after their cooldown expires. O(n * cycles) but demonstrates the scheduling more concretely.
> - The formula is the cleanest O(n) solution; the heap simulation is useful to explain the intuition.

---

## See Also

[[stack]] | [[graph]] | [[sliding-window]] | [[binary-search]]
