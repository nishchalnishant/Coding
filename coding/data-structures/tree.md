---
tags: [coding, data-structures, tree]
topic: tree
difficulty: mixed
---

# Tree Problems — Deep Dive

**Pattern map**: Tree problems reduce to one of five techniques — DFS traversal (preorder/inorder/postorder), level-order BFS, LCA (post-order recurse), Tree DP (post-order returning tuples), BST operations (exploit ordering). The remaining problems are construction/serialization and O(1)-space Morris traversal.

---

## DFS Traversal

### Binary Tree Inorder Traversal

> [!example] Problem
> Return inorder traversal (left → root → right) of a binary tree's node values. Implement iteratively (LC 94).

> [!info] Approach
> - **WHY:** Recursive inorder is trivial; the iterative version uses an explicit stack to simulate the call stack. Key pattern: push all left children first, then process on pop, then pivot to right child.
> - **WHAT:** Iterative inorder — maintain a stack; keep going left until None, then pop and visit, then move to right child.
> - **HOW:** `while curr or stack`: inner `while curr` pushes all lefts; `curr = stack.pop()` processes node, appends value; `curr = curr.right` to explore right subtree.

> [!note]- Python Solution
> ```python
> def inorderTraversal(root):
>     result, stack = [], []
>     curr = root
>     while curr or stack:
>         while curr:
>             stack.append(curr)
>             curr = curr.left
>         curr = stack.pop()
>         result.append(curr.val)
>         curr = curr.right
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(h).

> [!tip] Alternatives
> - Recursive: trivial but O(h) call stack — same space, disallowed in some interview variants.
> - Morris inorder: O(1) space by threading right pointers — only when space is critical. See Morris section.

---

### Invert Binary Tree

> [!example] Problem
> Given a binary tree root, mirror it — every left child becomes right and vice versa at every level.

> [!info] Approach
> **Post-order recursive swap.**
> WHY: Hierarchy is mirrored by swapping children at every node independently. What we need: visit every node once and swap its two children.
> WHAT: Post-order recursion — swap after both subtrees are inverted.
> HOW: Base case `not root → None`. Recurse left and right, then swap: `root.left, root.right = invertTree(root.right), invertTree(root.left)`. Pre-order also works since swapping is an O(1) local operation.

> [!note]- Python Solution
> ```python
> def invertTree(root):
>     if not root:
>         return None
>     root.left, root.right = invertTree(root.right), invertTree(root.left)
>     return root
> ```

> [!success] Complexity
> Time O(n), Space O(h) recursion stack.

> [!tip] Alternatives
> - BFS with queue: dequeue node, swap children, enqueue children. Same O(n)/O(n) but avoids call stack — better for skewed trees.
> - Iterative DFS with explicit stack: functionally identical to recursive pre-order, avoids recursion limit.

---

### Symmetric Tree

> [!example] Problem
> Check if a binary tree is a mirror of itself (symmetric around its center).

> [!info] Approach
> **Recursive mirror(l, r) — outer and inner pair matching.**
> WHY: Symmetry means the left subtree mirrors the right subtree. Two subtrees mirror each other iff their roots are equal AND the outer pair matches (left.left ↔ right.right) AND the inner pair matches (left.right ↔ right.left).
> WHAT: Define `mirror(l, r)` to check symmetry recursively.
> HOW: Base cases: both None → True (symmetric absence), exactly one None → False. Otherwise: `l.val == r.val and mirror(l.left, r.right) and mirror(l.right, r.left)`.

> [!note]- Python Solution
> ```python
> def isSymmetric(root):
>     def mirror(l, r):
>         if not l and not r:
>             return True
>         if not l or not r:
>             return False
>         return l.val == r.val and mirror(l.left, r.right) and mirror(l.right, r.left)
>     return mirror(root.left, root.right)
> ```

> [!success] Complexity
> Time O(n), Space O(h).

> [!tip] Alternatives
> - Iterative BFS with deque: push (l, r) pairs; compare and push cross-pairs. O(n)/O(n).
> - Serialize left and right subtrees with mirrored traversal and compare strings — fragile and slower, avoid.

---

### Maximum Depth of Binary Tree

> [!example] Problem
> Return the maximum depth (number of nodes on the longest root-to-leaf path).

> [!info] Approach
> **Post-order recursive max height.**
> WHY: Depth of a tree = 1 + max depth of its subtrees. This is the definition recursively applied.
> WHAT: Post-order recursion — a node can't contribute its depth until both subtrees report theirs.
> HOW: Base case `not root → 0`; otherwise `1 + max(maxDepth(left), maxDepth(right))`.

> [!note]- Python Solution
> ```python
> def maxDepth(root):
>     if not root:
>         return 0
>     return 1 + max(maxDepth(root.left), maxDepth(root.right))
> ```

> [!success] Complexity
> Time O(n), Space O(h).

> [!tip] Alternatives
> - BFS level-count: increment depth after each level. O(n)/O(width) — better for very deep trees where recursion overflows.
> - Iterative DFS with `(node, depth)` stack: track max depth seen. O(n)/O(h).

---

### Minimum Depth of Binary Tree

> [!example] Problem
> Return the minimum depth — number of nodes on the shortest root-to-leaf path. LC 111.

> [!info] Approach
> - **WHY:** Critical trap: a node with only one child is NOT a leaf. Minimum depth must reach a node where BOTH children are None. Simply returning `1 + min(left_depth, right_depth)` fails for nodes with a single child — the zero-depth from the absent child would win incorrectly.
> - **WHAT:** Post-order recursion with explicit single-child guard. If left is None, return `1 + right_depth`; if right is None, return `1 + left_depth`; otherwise `1 + min(left, right)`.
> - **HOW:** Base case: `not root → 0`. Then check left/right nullity before min.

> [!note]- Python Solution
> ```python
> def minDepth(root):
>     if not root:
>         return 0
>     left  = minDepth(root.left)
>     right = minDepth(root.right)
>     if not root.left:
>         return 1 + right
>     if not root.right:
>         return 1 + left
>     return 1 + min(left, right)
> ```

> [!success] Complexity
> Time O(n), Space O(h).

> [!tip] Alternatives
> - BFS with early exit: return depth the moment the first leaf is dequeued. O(d * w) where d = min depth, w = width — faster in practice when min depth is shallow.
> - Common bug: `1 + min(minDepth(left), minDepth(right))` — wrong for single-child nodes.

---

### Path Sum

> [!example] Problem
> Given a binary tree and `targetSum`, return True if any root-to-leaf path sums to `targetSum`.

> [!info] Approach
> **DFS subtracting current value — check at leaf.**
> WHY: A root-to-leaf path is uniquely defined by the sequence of nodes from root to a leaf. DFS naturally models path extension.
> WHAT: Subtract the current node's value from the target as we descend; at a leaf, check if remaining equals zero.
> HOW: The leaf check is critical — only return True at nodes where `not left and not right` (both children null), not at any node where partial sum matches.

> [!note]- Python Solution
> ```python
> def hasPathSum(root, targetSum):
>     if not root:
>         return False
>     if not root.left and not root.right:
>         return root.val == targetSum
>     remaining = targetSum - root.val
>     return hasPathSum(root.left, remaining) or hasPathSum(root.right, remaining)
> ```

> [!success] Complexity
> Time O(n) worst case, Space O(h).

> [!tip] Alternatives
> - BFS with `(node, running_sum)` queue: check at leaves. O(n)/O(n).
> - Path Sum II (all paths): backtracking — maintain current path list, append/pop during DFS, collect at leaves.

---

### Path Sum II

> [!example] Problem
> Return all root-to-leaf paths where the path sum equals `targetSum`. LC 113.

> [!info] Approach
> - **WHY:** Collecting all paths requires backtracking — extend the path on entry, collect at leaves, pop on exit. The pop on the way back up is essential; without it the path list carries values from sibling branches.
> - **WHAT:** DFS backtracking — maintain a mutable `path` list; append on enter, pop on exit; collect a copy at leaves.
> - **HOW:** At leaf (`not left and not right`) and `remaining == 0`: `result.append(list(path))` (copy! not reference). Then `path.pop()` on return regardless of whether this was a leaf.

> [!note]- Python Solution
> ```python
> def pathSum(root, targetSum):
>     result = []
>     def dfs(node, remaining, path):
>         if not node:
>             return
>         path.append(node.val)
>         remaining -= node.val
>         if not node.left and not node.right and remaining == 0:
>             result.append(list(path))  # copy — not a reference
>         dfs(node.left,  remaining, path)
>         dfs(node.right, remaining, path)
>         path.pop()  # backtrack
>     dfs(root, targetSum, [])
>     return result
> ```

> [!success] Complexity
> Time O(n²) worst case (copying path of length n at each leaf in a skewed tree). Space O(n) output + O(h) stack.

> [!tip] Alternatives
> - Pass immutable `path + [node.val]`: cleaner but O(n) copy per node → O(n²) time. Same complexity, higher constant.
> - Iterative DFS with `(node, remaining, path)` stack: avoids recursion limit; requires manual path bookkeeping.

---

### Sum Root to Leaf Numbers

> [!example] Problem
> Each root-to-leaf path represents a number (digits from root to leaf form an integer). Return the total sum. LC 129.

> [!info] Approach
> - **WHY:** As we descend, the current number is `parent_number * 10 + node.val`. At a leaf, this is the fully formed number. DFS naturally threads this accumulated value downward.
> - **WHAT:** DFS passing accumulated value; sum up leaf contributions.
> - **HOW:** `dfs(node, curr_num)` — `curr_num = curr_num * 10 + node.val`; at leaf return `curr_num`; otherwise return `dfs(left, curr_num) + dfs(right, curr_num)`.

> [!note]- Python Solution
> ```python
> def sumNumbers(root):
>     def dfs(node, curr):
>         if not node:
>             return 0
>         curr = curr * 10 + node.val
>         if not node.left and not node.right:
>             return curr
>         return dfs(node.left, curr) + dfs(node.right, curr)
>     return dfs(root, 0)
> ```

> [!success] Complexity
> Time O(n), Space O(h).

> [!tip] Alternatives
> - BFS with `(node, curr_num)` queue: same logic iteratively. O(n)/O(n).
> - Iterative DFS with `(node, curr)` stack: O(n)/O(h). Avoids recursion limit for deeply skewed trees.

---

### Count Complete Tree Nodes

> [!example] Problem
> Count the number of nodes in a complete binary tree. Must be better than O(n). LC 222.

> [!info] Approach
> - **WHY:** A naive O(n) traversal ignores the complete tree property. In a complete binary tree, every level except possibly the last is fully filled and the last level fills left to right. We can determine whether the left or right subtree is a perfect binary tree in O(log n) by comparing heights, then apply the formula `2^h - 1` for the perfect half and recurse on the other.
> - **WHAT:** At each node compare left height vs right height. If equal, left subtree is perfect → `left_count = 2^left_h - 1 + 1 (root)`, recurse only on right. If not equal, right subtree is a perfect tree of height (right_h): `right_count = 2^right_h - 1 + 1`, recurse only on left.
> - **HOW:** Height = keep going left (or right) until None. `left_h == right_h` means left subtree is perfect; otherwise right subtree is perfect (one level shorter).

> [!note]- Python Solution
> ```python
> def countNodes(root):
>     if not root:
>         return 0
>     left_h = right_h = 0
>     left = right = root
>     while left:
>         left_h += 1
>         left = left.left
>     while right:
>         right_h += 1
>         right = right.right
>     if left_h == right_h:
>         return (1 << left_h) - 1  # perfect tree: 2^h - 1
>     return 1 + countNodes(root.left) + countNodes(root.right)
> ```

> [!success] Complexity
> Time O(log²n) — O(log n) recursive calls, each doing O(log n) height computation. Space O(log n).

> [!tip] Alternatives
> - O(n) linear traversal: correct but misses the point of the problem.
> - Binary search on last level with bit-path encoding: same O(log²n) but more complex to implement.

---

### Count Good Nodes in Binary Tree

> [!example] Problem
> A node X is "good" if no node on the root-to-X path has a value greater than X.val. Count good nodes.

> [!info] Approach
> **DFS with propagated path_max.**
> WHY: Goodness depends on the path from root to the node — we need to carry the maximum value seen so far. Purely structural traversal can't determine goodness without ancestor context.
> WHAT: Pass `path_max` down; a node is good iff `node.val >= path_max`.
> HOW: Update `path_max = max(path_max, node.val)` before recursing; root is always good.

> [!note]- Python Solution
> ```python
> def goodNodes(root):
>     def dfs(node, path_max):
>         if not node:
>             return 0
>         is_good = 1 if node.val >= path_max else 0
>         new_max = max(path_max, node.val)
>         return is_good + dfs(node.left, new_max) + dfs(node.right, new_max)
>     return dfs(root, root.val)
> ```

> [!success] Complexity
> Time O(n), Space O(h).

> [!tip] Alternatives
> - BFS with `(node, path_max)` queue: same logic iteratively. O(n)/O(n).
> - Iterative DFS with `(node, path_max)` stack: O(n)/O(h) — preferred for deep trees.

---

### Same Tree

> [!example] Problem
> Given two binary trees, return true if they are structurally identical with the same node values at every position. LC 100.

> [!info] Approach
> - **WHY:** Two trees are the same iff their roots match and both subtrees are recursively the same. A null/non-null mismatch immediately returns false.
> - **WHAT:** Simultaneous pre-order DFS on both trees; fail on any structural or value mismatch.
> - **HOW:** Base cases: both None → True; exactly one None → False; `p.val != q.val` → False. Recurse: `isSameTree(p.left, q.left) and isSameTree(p.right, q.right)`.

> [!note]- Python Solution
> ```python
> def isSameTree(p, q):
>     if not p and not q:
>         return True
>     if not p or not q:
>         return False
>     if p.val != q.val:
>         return False
>     return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)
> ```

> [!success] Complexity
> Time O(n) where n = min(nodes in p, nodes in q). Space O(h).

> [!tip] Alternatives
> - Iterative with paired stack/queue: push `(p_node, q_node)` pairs; compare and push children. O(n)/O(h).
> - Serialize both and compare strings: O(n) but O(n) space and fragile with delimiter choices.

---

### Subtree of Another Tree

> [!example] Problem
> Given trees `root` and `subRoot`, return true if `subRoot` is a subtree of `root` (subRoot exists as an exact match rooted at some node in root). LC 572.

> [!info] Approach
> - **WHY:** For each node in `root`, check if the subtree rooted there matches `subRoot`. Reuses `isSameTree` as a subroutine — classic compositional approach.
> - **WHAT:** DFS over `root`; at each node invoke `isSameTree(node, subRoot)`. Short-circuit on match.
> - **HOW:** `isSubtree(root, subRoot)` — if not root: False; if `isSameTree(root, subRoot)`: True; else recurse left and right.

> [!note]- Python Solution
> ```python
> def isSubtree(root, subRoot):
>     def isSameTree(p, q):
>         if not p and not q: return True
>         if not p or not q:  return False
>         return p.val == q.val and isSameTree(p.left, q.left) and isSameTree(p.right, q.right)
> 
>     if not root:
>         return False
>     if isSameTree(root, subRoot):
>         return True
>     return isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)
> ```

> [!success] Complexity
> Time O(m * n) where m = nodes in root, n = nodes in subRoot. Space O(h_root).

> [!tip] Alternatives
> - Serialize both trees and use string substring search (KMP): O(m + n) time — optimal but tricky to handle null markers and delimiter collisions correctly.
> - Hashing subtrees: O(m + n) expected — hash each subtree, check if any hash matches subRoot's hash.

---

### Flatten Binary Tree to Linked List

> [!example] Problem
> Flatten a binary tree in-place into a linked list using right pointers in preorder order; all left pointers must be null.

> [!info] Approach
> **Morris-style in-place threading — find inorder predecessor.**
> WHY: Preorder = root → left → right. To flatten in-place without extra space: for each node with a left child, the end of the left subtree's rightmost chain should point to the original right subtree.
> WHAT: Morris-style threading applied to flattening. Move the left subtree to the right and null the left.
> HOW: For each `curr` with a left child: find rightmost node in left subtree (`prev`), wire `prev.right = curr.right`, move `curr.right = curr.left`, null `curr.left`. Advance `curr = curr.right`.

> [!note]- Python Solution
> ```python
> def flatten(root):
>     curr = root
>     while curr:
>         if curr.left:
>             prev = curr.left
>             while prev.right:
>                 prev = prev.right
>             prev.right = curr.right
>             curr.right = curr.left
>             curr.left = None
>         curr = curr.right
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Reverse preorder (right → left → root) with `prev` pointer: set each node's right to prev. O(h) stack space.
> - Collect preorder into list then relink: O(n) time and space — simple but uses extra memory.
> - Recursive with tail return: `flatten(node)` returns tail of flattened list. O(h) recursion stack.

---

### Step-By-Step Directions From a Binary Tree Node to Another

> [!example] Problem
> Given root, `startValue`, and `destValue`, return the shortest path as a string of `'L'`, `'R'`, `'U'` characters.

> [!info] Approach
> **DFS to root→start and root→dest paths, strip common prefix.**
> WHY: The shortest path between two nodes in a tree goes through their LCA.
> WHAT: Find root→start and root→dest as L/R sequences; strip the common prefix (= path to LCA); start's remaining path becomes all 'U's (going up to LCA), dest's remaining path is the L/R directions from LCA to dest.
> HOW: DFS to record L/R path from root to each target node, then strip common prefix.

> [!note]- Python Solution
> ```python
> def getDirections(root, startValue, destValue):
>     def find_path(node, target, path):
>         if not node:
>             return False
>         if node.val == target:
>             return True
>         path.append('L')
>         if find_path(node.left, target, path):
>             return True
>         path.pop()
>         path.append('R')
>         if find_path(node.right, target, path):
>             return True
>         path.pop()
>         return False
> 
>     path_s, path_d = [], []
>     find_path(root, startValue, path_s)
>     find_path(root, destValue, path_d)
> 
>     i = 0
>     while i < len(path_s) and i < len(path_d) and path_s[i] == path_d[i]:
>         i += 1
> 
>     return 'U' * (len(path_s) - i) + ''.join(path_d[i:])
> ```

> [!success] Complexity
> Time O(n), Space O(n) for paths.

> [!tip] Alternatives
> - Explicit LCA first, then DFS from LCA to start and LCA to dest: conceptually cleaner but same complexity.
> - BFS with parent map then path reconstruction: gives the path but doesn't produce L/R/U labels naturally without backtracking.

---

## Level Order BFS

### Binary Tree Level Order Traversal

> [!example] Problem
> Return node values grouped by level as a list of lists.

> [!info] Approach
> **BFS with level-size snapshot.**
> WHY: Level grouping requires knowing when one level ends and the next begins. BFS processes nodes in breadth-first order, which exactly corresponds to levels.
> WHAT: Snapshot the queue size at the start of each iteration — that many nodes form the current level.
> HOW: Inner loop runs exactly `level_size` times; enqueue children during inner loop; append collected level after inner loop.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def levelOrder(root):
>     if not root:
>         return []
>     result, queue = [], deque([root])
>     while queue:
>         level = []
>         for _ in range(len(queue)):
>             node = queue.popleft()
>             level.append(node.val)
>             if node.left:  queue.append(node.left)
>             if node.right: queue.append(node.right)
>         result.append(level)
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(n) — queue holds up to n/2 nodes at widest level.

> [!tip] Alternatives
> - DFS with depth parameter: `dfs(node, depth)` appends to `result[depth]`. O(n)/O(h) — better space for tall trees.
> - Two-list swap: maintain `current_level` and `next_level`, swap after each level. Same complexity.

---

### Binary Tree Zigzag Level Order Traversal

> [!example] Problem
> Return the level-order traversal of a binary tree where alternate levels are traversed right-to-left (zigzag). LC 103.

> [!info] Approach
> - **WHY:** Same as level-order BFS but every other level needs reversal. Toggle a flag per level rather than using a deque with dual-end insertion — simpler and avoids subtle off-by-one errors.
> - **WHAT:** BFS with level-size snapshot; after building each level list, conditionally reverse it before appending.
> - **HOW:** `left_to_right = True` initially; after collecting each level: if `not left_to_right`, `level.reverse()`; then `left_to_right = not left_to_right`.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def zigzagLevelOrder(root):
>     if not root:
>         return []
>     result = []
>     queue = deque([root])
>     left_to_right = True
>     while queue:
>         level = []
>         for _ in range(len(queue)):
>             node = queue.popleft()
>             level.append(node.val)
>             if node.left:  queue.append(node.left)
>             if node.right: queue.append(node.right)
>         if not left_to_right:
>             level.reverse()
>         result.append(level)
>         left_to_right = not left_to_right
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - Deque with appendleft/append based on direction: avoids the reverse() call; same O(n)/O(n) but harder to follow.
> - DFS with depth parity: `result[depth].append(val)` with conditional insert at front vs back. O(n)/O(n).

---

### Binary Tree Right Side View

> [!example] Problem
> Return the values visible when looking at the tree from the right side (rightmost node at each level).

> [!info] Approach
> **BFS — capture last node per level.**
> WHY: The rightmost visible node at each level is the last node processed in a BFS level sweep.
> WHAT: Level-order BFS; record the value of the last node processed per level.
> HOW: Snapshot level size; run inner loop; append value only when `i == level_size - 1`.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def rightSideView(root):
>     if not root:
>         return []
>     result, queue = [], deque([root])
>     while queue:
>         level_size = len(queue)
>         for i in range(level_size):
>             node = queue.popleft()
>             if i == level_size - 1:
>                 result.append(node.val)
>             if node.left:  queue.append(node.left)
>             if node.right: queue.append(node.right)
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - DFS right-first with depth: visit right before left; append only on first visit to a new depth. O(n)/O(h) — better for wide trees.

---

### Populating Next Right Pointers in Each Node

> [!example] Problem
> Given a perfect binary tree, populate each node's `next` pointer to its next right neighbor at the same level.

> [!info] Approach
> **O(1) space — walk current level to connect next level.**
> WHY: Perfect binary tree: every internal node has exactly two children; all leaves at the same level. Once level k is connected via next pointers, we can traverse it like a linked list to connect level k+1.
> WHAT: For each node in level k: `node.left.next = node.right` (sibling connection) and `node.right.next = node.next.left if node.next else None` (cousin connection).
> HOW: Start with `leftmost = root`; inner loop walks the current level using `head.next`; outer loop descends via `leftmost = leftmost.left`.

> [!note]- Python Solution
> ```python
> def connect(root):
>     if not root:
>         return root
>     leftmost = root
>     while leftmost.left:
>         head = leftmost
>         while head:
>             head.left.next = head.right
>             if head.next:
>                 head.right.next = head.next.left
>             head = head.next
>         leftmost = leftmost.left
>     return root
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - BFS with queue: works for any binary tree (not just perfect). O(n)/O(n). Use this for the follow-up problem with arbitrary binary trees.
> - Recursive: same logic; O(log n) space for perfect tree (height = log n).

---

### Vertical Order Traversal of a Binary Tree

> [!example] Problem
> Return nodes grouped by column, where each column is sorted by (row, value). Same (row, col) nodes sorted by value.

> [!info] Approach
> **DFS collect (col, row, val) tuples, sort, group.**
> WHY: Vertical order is defined by column assignment: root at col 0, left child at col-1, right child at col+1, row increases by 1 per level.
> WHAT: Sort-based approach — collect all (col, row, val) tuples and sorting by (col, row, val) handles ties correctly.
> HOW: DFS assigning (row, col) to each node, collect all tuples, sort, then group by column.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def verticalTraversal(root):
>     nodes = []
>     def dfs(node, row, col):
>         if not node:
>             return
>         nodes.append((col, row, node.val))
>         dfs(node.left,  row + 1, col - 1)
>         dfs(node.right, row + 1, col + 1)
>     dfs(root, 0, 0)
>     nodes.sort()
>     result = []
>     prev_col = None
>     for col, row, val in nodes:
>         if col != prev_col:
>             result.append([])
>             prev_col = col
>         result[-1].append(val)
>     return result
> ```

> [!success] Complexity
> Time O(n log n) — dominated by sort. Space O(n).

> [!tip] Alternatives
> - BFS with `(node, row, col)` tuples: identical result after sorting; BFS vs DFS collection order doesn't matter since we sort anyway.
> - Gotcha: nodes at the same (col, row) must be sorted by value — a commonly missed case.

---

### All Nodes Distance K in Binary Tree

> [!example] Problem
> Given a binary tree, a target node, and integer k, return all nodes at exactly k edges from the target.

> [!info] Approach
> **Build undirected graph, BFS k steps from target.**
> WHY: In a tree, distance can only go downward from any node. But from the target, distance can also go upward through parents — making this a graph problem. Adding parent edges allows BFS to spread in all directions from target.
> WHAT: Build an adjacency list (bidirectional) via one DFS, then BFS from target for exactly k steps.
> HOW: Build graph first, BFS second, collect nodes at distance == k.

> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> 
> def distanceK(root, target, k):
>     graph = defaultdict(list)
>     def build(node, parent):
>         if not node:
>             return
>         if parent:
>             graph[node.val].append(parent.val)
>             graph[parent.val].append(node.val)
>         build(node.left, node)
>         build(node.right, node)
>     build(root, None)
> 
>     seen = {target.val}
>     queue = deque([(target.val, 0)])
>     result = []
>     while queue:
>         node, dist = queue.popleft()
>         if dist == k:
>             result.append(node)
>         elif dist < k:
>             for nbr in graph[node]:
>                 if nbr not in seen:
>                     seen.add(nbr)
>                     queue.append((nbr, dist + 1))
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - Pure DFS without graph: `dfs(node)` returns distance to target if found in that subtree; spread outward from the ancestor at the appropriate distance. O(n)/O(h) but harder to implement cleanly.
> - DFS with parent map then BFS: equivalent — explicit {node: parent} dict instead of adjacency list.

---

## Lowest Common Ancestor

### Lowest Common Ancestor of a Binary Tree

> [!example] Problem
> Given a binary tree and two nodes p and q (both guaranteed to exist), find their LCA — the deepest node that has both as descendants (a node is a descendant of itself).

> [!info] Approach
> **Post-order recursion — converge at split node.**
> WHY: The LCA is determined by what comes back from both subtrees — we need children to report before the parent decides.
> WHAT: If the current node is None, p, or q, return it. Recurse left and right. If both return non-None, both targets were found in different subtrees → current node is LCA. If only one side returns non-None, the LCA is in that subtree.
> HOW: `if left and right: return root; return left or right`.

> [!note]- Python Solution
> ```python
> def lowestCommonAncestor(root, p, q):
>     if not root or root == p or root == q:
>         return root
>     left = lowestCommonAncestor(root.left, p, q)
>     right = lowestCommonAncestor(root.right, p, q)
>     if left and right:
>         return root
>     return left or right
> ```

> [!success] Complexity
> Time O(n), Space O(h).

> [!tip] Alternatives
> - Parent pointer map + ancestor set: BFS to build {node: parent}, walk ancestors of p into a set, walk ancestors of q until hit. O(n) time and space.
> - Euler tour + RMQ: O(n) preprocessing, O(1) per query — only for many queries on a static tree.

---

### Lowest Common Ancestor of a BST

> [!example] Problem
> Same as above but the tree is a BST. Exploit the ordering property.

> [!info] Approach
> **Iterative BST-guided descent — O(h) instead of O(n).**
> WHY: In a BST, if both p and q are less than root, their LCA must be in the left subtree. If both are greater, LCA is in the right subtree. The moment they "diverge" (one ≤ root ≤ other, or one equals root), the current root is the LCA.
> WHAT: Iteratively follow the BST property — no recursion into both subtrees.
> HOW: If both p, q < root, go left. If both > root, go right. Otherwise return root.

> [!note]- Python Solution
> ```python
> def lowestCommonAncestor(root, p, q):
>     while root:
>         if p.val < root.val and q.val < root.val:
>             root = root.left
>         elif p.val > root.val and q.val > root.val:
>             root = root.right
>         else:
>             return root
> ```

> [!success] Complexity
> Time O(h) — O(log n) balanced, O(n) skewed. Space O(1).

> [!tip] Alternatives
> - Recursive: same logic, O(h) space for call stack.
> - General binary tree LCA: works but ignores BST structure — O(n) unnecessarily.

---

## Tree DP

### Diameter of Binary Tree

> [!example] Problem
> Return the length of the longest path between any two nodes (measured in edges). The path need not pass through the root.

> [!info] Approach
> **Post-order height DFS with global diameter update.**
> WHY: The diameter through any node = left_height + right_height. We can't compute this without first knowing both subtree heights — post-order.
> WHAT: `height(node)` returns the height of the subtree; as a side effect, updates global `diameter = max(diameter, left + right)`.
> HOW: Return `1 + max(left, right)` upward; update `best[0]` with `l + r` at each node.

> [!note]- Python Solution
> ```python
> def diameterOfBinaryTree(root):
>     best = [0]
>     def height(node):
>         if not node:
>             return 0
>         l, r = height(node.left), height(node.right)
>         best[0] = max(best[0], l + r)
>         return 1 + max(l, r)
>     height(root)
>     return best[0]
> ```

> [!success] Complexity
> Time O(n), Space O(h).

> [!tip] Alternatives
> - Naive two-pass: for each node call a separate height function. O(n²) — avoid.
> - Return `(height, diameter)` tuple: no mutable state, same logic. Cleaner functional style.

---

### Binary Tree Maximum Path Sum

> [!example] Problem
> Find the maximum path sum between any two nodes. Values can be negative; a path can start and end anywhere.

> [!info] Approach
> **Post-order gain DFS — clamp negatives to 0.**
> WHY: A path should not extend into a subtree that contributes a negative sum — drop it (treat as 0).
> WHAT: Distinguish two roles — the "gain returned to parent" (extends into at most one child) vs. the "path through this node as apex" (can use both children).
> HOW: `gain(node) = node.val + max(l, r)` returned upward; global update = `node.val + l + r` (where l and r already have negatives clamped to 0).

> [!note]- Python Solution
> ```python
> def maxPathSum(root):
>     best = [float('-inf')]
>     def gain(node):
>         if not node:
>             return 0
>         l = max(gain(node.left), 0)
>         r = max(gain(node.right), 0)
>         best[0] = max(best[0], node.val + l + r)
>         return node.val + max(l, r)
>     gain(root)
>     return best[0]
> ```

> [!success] Complexity
> Time O(n), Space O(h).

> [!tip] Alternatives
> - Return `(max_path_through, max_single_arm)` tuple: avoids nonlocal/global, same O(n)/O(h).
> - Iterative post-order: same computation iteratively. More verbose.

---

### House Robber III

> [!example] Problem
> Houses are arranged in a binary tree. Adjacent nodes (parent-child) cannot both be robbed. Maximize total money robbed.

> [!info] Approach
> **Post-order DP returning (rob, skip) pair.**
> WHY: The parent's optimal choice (rob or skip its parent) depends on both options at each child — returning a single value forces suboptimal choices.
> WHAT: `dp(node)` returns `(rob, skip)` — maximum money if we rob vs. skip this node.
> HOW: `rob = node.val + l_skip + r_skip`; `skip = max(l_rob, l_skip) + max(r_rob, r_skip)`. Post-order: compute children first.

> [!note]- Python Solution
> ```python
> def rob(root):
>     def dp(node):
>         if not node:
>             return 0, 0  # rob, skip
>         l_rob, l_skip = dp(node.left)
>         r_rob, r_skip = dp(node.right)
>         rob   = node.val + l_skip + r_skip
>         skip  = max(l_rob, l_skip) + max(r_rob, r_skip)
>         return rob, skip
>     return max(dp(root))
> ```

> [!success] Complexity
> Time O(n), Space O(h).

> [!tip] Alternatives
> - Memoized top-down with `@lru_cache` on (node, can_rob): same complexity, more overhead.
> - Naive recursion without caching: O(2^n) — recomputes subproblems exponentially.

---

### Binary Tree Cameras

> [!example] Problem
> Place minimum cameras such that every node is monitored. A camera at node u monitors u, its parent, and its direct children.

> [!info] Approach
> **Greedy post-order — delay cameras upward.**
> WHY: It's always optimal to delay camera placement upward (put the camera at the parent of an uncovered leaf rather than at the leaf).
> WHAT: Three states per node — 0 = uncovered (needs a camera from parent), 1 = covered but no camera, 2 = has a camera.
> HOW: Null nodes return 1 (trivially covered). If any child returns 0, place a camera here (return 2, increment count). If any child has a camera (returns 2), this node is covered (return 1). Otherwise return 0 (push responsibility to parent).

> [!note]- Python Solution
> ```python
> def minCameraCover(root):
>     cameras = [0]
>     def dfs(node):
>         if not node:
>             return 1  # null nodes are covered
>         left, right = dfs(node.left), dfs(node.right)
>         if left == 0 or right == 0:
>             cameras[0] += 1
>             return 2
>         if left == 2 or right == 2:
>             return 1
>         return 0
>     if dfs(root) == 0:
>         cameras[0] += 1
>     return cameras[0]
> ```

> [!success] Complexity
> Time O(n), Space O(h).

> [!tip] Alternatives
> - DP tuple `(uncovered, covered_no_cam, has_cam)` per node: more explicit, same greedy result.
> - BFS bottom-up level sets: identify uncovered nodes level by level; harder to implement correctly.

---

### Path Sum III

> [!example] Problem
> Count paths that sum to `targetSum`. Paths must go downward (ancestor to descendant) but need not start at root or end at leaf.

> [!info] Approach
> **DFS with prefix sum hash map + backtracking.**
> WHY: A downward path ending at node X has sum = `running_sum[X] - running_sum[ancestor]`. If `running_sum[X] - targetSum` was seen at some ancestor, that ancestor→X path sums to targetSum.
> WHAT: Maintain `{prefix_sum: count}` hash map; initialize with `{0: 1}` (empty path from root).
> HOW: DFS — add node.val to running sum, query map for `running_sum - targetSum`, increment map, recurse children, then decrement map on backtrack (critical: prevents prefix sum from leaking into sibling branches).

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def pathSum(root, targetSum):
>     prefix = defaultdict(int)
>     prefix[0] = 1
>     count = [0]
> 
>     def dfs(node, running):
>         if not node:
>             return
>         running += node.val
>         count[0] += prefix[running - targetSum]
>         prefix[running] += 1
>         dfs(node.left, running)
>         dfs(node.right, running)
>         prefix[running] -= 1  # backtrack — essential for correctness
> 
>     dfs(root, 0)
>     return count[0]
> ```

> [!success] Complexity
> Time O(n), Space O(n) prefix map + O(h) stack.

> [!tip] Alternatives
> - Brute force DFS from every node: O(n²) — unacceptable.
> - DFS returning all path sums ending at each node: accumulate and count; O(n²) worst case.

---

## BST Operations

### Validate Binary Search Tree

> [!example] Problem
> Determine if a binary tree is a valid BST. Every node must satisfy the global BST property (all left descendants < node < all right descendants), not just the immediate children.

> [!info] Approach
> **Recursive range validation — propagate (lo, hi) bounds.**
> WHY: Checking only `node.left.val < node.val < node.right.val` misses global violations. Carry `(lo, hi)` bounds down the tree; each node must satisfy `lo < node.val < hi`.
> WHAT: Going left, tighten upper bound to `node.val`; going right, tighten lower bound.
> HOW: `validate(node, lo, hi)` — fail if not `lo < node.val < hi`, else recurse with tightened bounds.

> [!note]- Python Solution
> ```python
> def isValidBST(root):
>     def validate(node, lo, hi):
>         if not node:
>             return True
>         if not (lo < node.val < hi):
>             return False
>         return validate(node.left, lo, node.val) and validate(node.right, node.val, hi)
>     return validate(root, float('-inf'), float('inf'))
> ```

> [!success] Complexity
> Time O(n), Space O(h).

> [!tip] Alternatives
> - Inorder traversal with `prev` pointer: BST inorder is strictly increasing; fail if `curr <= prev`. O(n)/O(h).
> - Collect inorder values and check sorted: O(n) time and space — simpler but materializes the full list.
> - Morris inorder: O(1) space, O(n) time.

---

### Kth Smallest Element in a BST

> [!example] Problem
> Given a BST and integer k, return the kth smallest value (1-indexed).

> [!info] Approach
> **Iterative inorder with early exit at k.**
> WHY: BST inorder traversal yields values in ascending sorted order — the kth node visited is the kth smallest. Iterative form allows clean early termination at exactly k pops.
> WHAT: Standard iterative inorder — push all left children onto stack, pop, decrement k, if k == 0 return.
> HOW: `while stack or root`: push all left children, pop, decrement k, if k == 0 return val, else advance to right child.

> [!note]- Python Solution
> ```python
> def kthSmallest(root, k):
>     stack = []
>     while stack or root:
>         while root:
>             stack.append(root)
>             root = root.left
>         root = stack.pop()
>         k -= 1
>         if k == 0:
>             return root.val
>         root = root.right
> ```

> [!success] Complexity
> Time O(h + k), Space O(h).

> [!tip] Alternatives
> - Recursive inorder with early exit via nonlocal counter: O(h + k) time, O(h) space — less clean.
> - Augmented BST (rank tree): store subtree sizes; O(h) query — only worthwhile with many repeated queries on a mutable tree.
> - Morris inorder: O(1) space, O(n) time — if space is critical.

---

### Insert and Delete in BST

> [!example] Problem
> Insert a value into a BST (LC 701) and delete a node from a BST (LC 450). Return the root of the modified tree.

> [!info] Approach
> - **WHY:** Insert follows BST search path to find the null slot. Delete has three cases: leaf (just remove), one child (bypass the node), two children (replace with inorder successor or predecessor then delete that successor).
> - **WHAT:** Insert — recurse into left or right based on comparison; on hitting None, return a new node. Delete — recurse to find target; on finding it, handle the three cases.
> - **HOW:** Delete's two-child case: find inorder successor (leftmost in right subtree), copy its value to current node, then delete successor from right subtree.

> [!note]- Python Solution
> ```python
> def insertIntoBST(root, val):
>     if not root:
>         return TreeNode(val)
>     if val < root.val:
>         root.left  = insertIntoBST(root.left,  val)
>     else:
>         root.right = insertIntoBST(root.right, val)
>     return root
> 
> def deleteNode(root, key):
>     if not root:
>         return None
>     if key < root.val:
>         root.left  = deleteNode(root.left,  key)
>     elif key > root.val:
>         root.right = deleteNode(root.right, key)
>     else:  # found
>         if not root.left:  return root.right
>         if not root.right: return root.left
>         # two children: replace with inorder successor
>         successor = root.right
>         while successor.left:
>             successor = successor.left
>         root.val   = successor.val
>         root.right = deleteNode(root.right, successor.val)
>     return root
> ```

> [!success] Complexity
> Time O(h) — O(log n) balanced, O(n) skewed. Space O(h) call stack.

> [!tip] Alternatives
> - Iterative insert: track parent pointer, attach new node. O(h)/O(1).
> - Delete with inorder predecessor (rightmost in left subtree): symmetric approach.
> - Iterative delete: more complex; requires tracking parent pointer to relink.

---

### Range Sum of BST

> [!example] Problem
> Given a BST and bounds `[low, high]`, return the sum of all node values within the inclusive range.

> [!info] Approach
> **DFS with BST pruning — skip entire subtrees.**
> WHY: Unlike a general tree, BST allows skipping entire subtrees. If `node.val < low`, the left subtree contains only smaller values — skip it. If `node.val > high`, right subtree contains only larger values — skip it.
> WHAT: DFS that prunes based on BST ordering.
> HOW: Only recurse left if `node.val > low`; only recurse right if `node.val < high`.

> [!note]- Python Solution
> ```python
> def rangeSumBST(root, low, high):
>     if not root:
>         return 0
>     total = 0
>     if low <= root.val <= high:
>         total += root.val
>     if root.val > low:
>         total += rangeSumBST(root.left, low, high)
>     if root.val < high:
>         total += rangeSumBST(root.right, low, high)
>     return total
> ```

> [!success] Complexity
> Time O(n) worst case, O(log n + k) where k = nodes in range for balanced BST. Space O(h).

> [!tip] Alternatives
> - Inorder collect then sum: O(n) time and space — doesn't exploit BST pruning.
> - Iterative DFS with explicit stack: same pruning, avoids recursion limit. O(n)/O(h).

---

### Recover Binary Search Tree

> [!example] Problem
> Exactly two nodes of a BST have been swapped by mistake. Recover the tree in-place without changing its structure.

> [!info] Approach
> **Inorder DFS — detect inversion pair(s), swap values.**
> WHY: A correct BST's inorder traversal is strictly ascending. Two swapped nodes create inversions. If adjacent in inorder: one inversion. If non-adjacent: two inversions.
> WHAT: Inorder DFS tracking `prev`; on first inversion set `first = prev, second = curr`; on second inversion update `second = curr`. Swap `first.val` and `second.val`.
> HOW: One or two inversion sites. Always: `first = prev` at first inversion; `second = curr` at each inversion (covers both one and two inversion cases).

> [!note]- Python Solution
> ```python
> def recoverTree(root):
>     first = second = prev = None
> 
>     def inorder(node):
>         nonlocal first, second, prev
>         if not node:
>             return
>         inorder(node.left)
>         if prev and prev.val > node.val:
>             if not first:
>                 first = prev
>             second = node
>         prev = node
>         inorder(node.right)
> 
>     inorder(root)
>     first.val, second.val = second.val, first.val
> ```

> [!success] Complexity
> Time O(n), Space O(h) call stack.

> [!tip] Alternatives
> - Morris inorder: O(1) space — traverse without stack by threading the tree temporarily. Same O(n) time.
> - Iterative inorder with explicit stack: O(n)/O(h), avoids recursion limit for deep trees.
> - Collect inorder values, sort, reassign: O(n) time and space — simpler but not truly in-place.

---

## Construction / Serialization

### Serialize and Deserialize Binary Tree

> [!example] Problem
> Design an algorithm to serialize a binary tree to a string and reconstruct it from that string.

> [!info] Approach
> **Preorder DFS with null markers — iterator-based deserialization.**
> WHY: Preorder places the root first, so during deserialization we can reconstruct the root before its children — naturally recursive. Inorder alone is insufficient (can't determine split without knowing root).
> WHAT: DFS emitting node values and `#` for null, comma-delimited. Deserialize using an iterator over tokens.
> HOW: Serialize: DFS pre-order appending values or `#`. Deserialize: iterate tokens; `#` → return None; otherwise create node, recurse left, recurse right. Use an iterator to advance position across recursive calls.

> [!note]- Python Solution
> ```python
> class Codec:
>     def serialize(self, root):
>         res = []
>         def dfs(node):
>             if not node:
>                 res.append('#')
>                 return
>             res.append(str(node.val))
>             dfs(node.left)
>             dfs(node.right)
>         dfs(root)
>         return ','.join(res)
> 
>     def deserialize(self, data):
>         it = iter(data.split(','))
>         def dfs():
>             val = next(it)
>             if val == '#':
>                 return None
>             node = TreeNode(int(val))
>             node.left  = dfs()
>             node.right = dfs()
>             return node
>         return dfs()
> ```

> [!success] Complexity
> Time O(n) both directions. Space O(n) for string, O(h) call stack.

> [!tip] Alternatives
> - BFS level-order serialization: queue-based, easier to visualize. More null markers for sparse trees. Same asymptotic complexity.
> - Postorder: root comes last; deserialize right-to-left from end using a stack. Same complexity, less intuitive.

---

### Construct Binary Tree from Preorder and Inorder Traversal

> [!example] Problem
> Given `preorder` and `inorder` arrays of a binary tree's traversal, reconstruct the tree.

> [!info] Approach
> **Preorder index advance + inorder hash map for O(1) root lookup.**
> WHY: Preorder[0] is always the root; find it in inorder — everything left is the left subtree, everything right is the right subtree. Hash map gives O(1) inorder index lookup instead of O(n) linear scan.
> WHAT: Advance a global preorder index as you recurse; pass inorder bounds to slice logically without creating new arrays.
> HOW: `build(in_left, in_right)` — take `preorder[pre_idx]` as root, find its inorder position `mid`, build left subtree with `in_left..mid-1`, right subtree with `mid+1..in_right`.

> [!note]- Python Solution
> ```python
> def buildTree(preorder, inorder):
>     idx_map = {val: i for i, val in enumerate(inorder)}
>     pre_idx = [0]
> 
>     def build(in_left, in_right):
>         if in_left > in_right:
>             return None
>         root_val = preorder[pre_idx[0]]
>         pre_idx[0] += 1
>         root = TreeNode(root_val)
>         mid = idx_map[root_val]
>         root.left  = build(in_left, mid - 1)
>         root.right = build(mid + 1, in_right)
>         return root
> 
>     return build(0, len(inorder) - 1)
> ```

> [!success] Complexity
> Time O(n), Space O(n) for hash map + O(h) stack.

> [!tip] Alternatives
> - Slice arrays on each call: O(n²) due to repeated slicing — avoid for large inputs.
> - Iterative with explicit stack: simulate recursion; O(n) time and space, no recursion limit issues.
> - Postorder + inorder: symmetric — last element of postorder is root; construct right before left.

---

### Construct Binary Tree from Inorder and Postorder Traversal

> [!example] Problem
> Given `inorder` and `postorder` arrays, reconstruct the binary tree. LC 106.

> [!info] Approach
> - **WHY:** Postorder's last element is always the root. Find it in inorder — elements to its left form the left subtree, elements to its right form the right subtree. Symmetric to the preorder+inorder problem.
> - **WHAT:** Walk postorder array right-to-left (using a decrementing index); build right subtree before left (reversed postorder visits root, right, left).
> - **HOW:** `build(in_left, in_right)` — take `postorder[post_idx]` as root, decrement index, find root in inorder hash map as `mid`, build right subtree `(mid+1, in_right)` FIRST, then left `(in_left, mid-1)`.

> [!note]- Python Solution
> ```python
> def buildTree(inorder, postorder):
>     idx_map = {val: i for i, val in enumerate(inorder)}
>     post_idx = [len(postorder) - 1]
> 
>     def build(in_left, in_right):
>         if in_left > in_right:
>             return None
>         root_val = postorder[post_idx[0]]
>         post_idx[0] -= 1
>         root = TreeNode(root_val)
>         mid = idx_map[root_val]
>         root.right = build(mid + 1, in_right)   # right BEFORE left
>         root.left  = build(in_left, mid - 1)
>         return root
> 
>     return build(0, len(inorder) - 1)
> ```

> [!success] Complexity
> Time O(n), Space O(n) hash map + O(h) stack.

> [!tip] Alternatives
> - Slice arrays: O(n²) due to slicing — avoid.
> - Key trap: must build right subtree before left when consuming postorder right-to-left. Reversing this order corrupts the construction.

---

## Morris Traversal / Iterative Postorder

### Morris Inorder Traversal (Technique)

> [!info] Approach
> **Morris threading — O(1) space inorder via temporary right pointer threads.**
> WHY: Standard inorder traversal uses O(h) stack space. Morris traversal achieves O(1) auxiliary space by temporarily threading the tree — using unused right pointers of inorder predecessors to "remember" where to return after exploring a left subtree.
> WHAT: For each node `curr`: if no left child, visit and move right. Otherwise find inorder predecessor (rightmost in left subtree). If predecessor.right is None: create thread, go left. If predecessor.right is curr: unthread, visit, go right.
> HOW: The tree is temporarily mutated and fully restored on completion.

> [!note]- Python Solution
> ```python
> def morris_inorder(root) -> list:
>     result = []
>     curr = root
>     while curr:
>         if not curr.left:
>             result.append(curr.val)
>             curr = curr.right
>         else:
>             predecessor = curr.left
>             while predecessor.right and predecessor.right is not curr:
>                 predecessor = predecessor.right
>             if not predecessor.right:
>                 predecessor.right = curr      # thread
>                 curr = curr.left
>             else:
>                 predecessor.right = None      # unthread, restore
>                 result.append(curr.val)
>                 curr = curr.right
>     return result
> ```

> [!success] Complexity
> Time O(n) — each edge traversed at most twice. Space O(1) auxiliary (no stack, no recursion).

> [!tip] Alternatives
> - Morris Preorder: visit the node on the first encounter (when threading, before going left) instead of the second encounter (on unthreading).
> - Only use when space is explicitly constrained to O(1). Otherwise standard iterative inorder is cleaner. Mention to interviewer that tree is temporarily mutated and restored.

---

### Morris Preorder Traversal (Technique)

> [!info] Approach
> **Morris threading — visit on first encounter (threading), not second.**
> WHY: Preorder visits root before children. In Morris traversal, the first encounter with a node (when we create the thread) corresponds to preorder.
> WHAT: Same as Morris inorder but visit node when threading (first encounter) rather than when unthreading (second encounter).
> HOW: When `pre.right is None` (first encounter): set thread, visit node, go left. When `pre.right is curr` (second encounter): remove thread, go right (do NOT visit again).

> [!note]- Python Solution
> ```python
> def morris_preorder(root) -> list:
>     result = []
>     curr = root
>     while curr:
>         if not curr.left:
>             result.append(curr.val)
>             curr = curr.right
>         else:
>             pre = curr.left
>             while pre.right and pre.right is not curr:
>                 pre = pre.right
>             if not pre.right:
>                 pre.right = curr
>                 result.append(curr.val)  # visit on FIRST encounter (threading)
>                 curr = curr.left
>             else:
>                 pre.right = None
>                 curr = curr.right        # don't visit again on unthread
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(1) auxiliary.

> [!tip] Alternatives
> - Recursive preorder: O(h) stack. Much simpler; only use Morris when O(1) space is required.

---

### Iterative Postorder Traversal (Technique)

> [!info] Approach
> **1-stack iterative postorder with last_visited sentinel.**
> WHY: Postorder (L → R → Root) is the hardest iterative traversal. The root is encountered twice — once when first descending and once after returning from the right subtree. A `last_visited` pointer distinguishes these two cases.
> WHAT: Standard iterative inorder base — after exhausting left children, peek at the stack top. If it has an unvisited right child, go right. Otherwise process the node and record `last_visited`.
> HOW: Peek at `stack[-1]`. If `peek.right` exists and `peek.right is not last_visited`, go right. Otherwise: process (append), pop, set `last_visited = popped_node`.

> [!note]- Python Solution
> ```python
> def iterative_postorder(root) -> list:
>     result = []
>     stack = []
>     curr = root
>     last_visited = None
> 
>     while curr or stack:
>         if curr:
>             stack.append(curr)
>             curr = curr.left
>         else:
>             peek = stack[-1]
>             if peek.right and last_visited is not peek.right:
>                 curr = peek.right
>             else:
>                 result.append(peek.val)
>                 last_visited = stack.pop()
> 
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(h).

> [!tip] Alternatives
> - 2-stack "cheat": reverse-preorder trick — do iterative preorder with right-before-left and reverse the output. Works correctly but SDE-3 interviewers often explicitly ban it to test whether you understand the `last_visited` state machine. The 1-stack approach above is the expected answer.

---

## See Also

[[graph]] | [[dynamic-programming]] | [[recursion]] | [[heap]]
### Binary Tree Boundary Traversal

> [!example] Problem
> Return the boundary of a binary tree: root, left boundary, leaves, and right boundary in reverse.

> [!info] Approach
> - **WHY:** The boundary is not a standard traversal; it is a combination of three ordered pieces with non-overlapping responsibilities.
> - **WHAT:** Collect the left boundary excluding leaves, then all leaves left-to-right, then the right boundary excluding leaves and reverse it.
> - **HOW:** Handle edge cases carefully so the root and leaf nodes are not duplicated.

> [!note]- Python Solution
> ```python
> def boundaryOfBinaryTree(root):
>     if not root:
>         return []
> 
>     def is_leaf(node):
>         return node and not node.left and not node.right
> 
>     boundary = [root.val] if not is_leaf(root) else []
> 
>     node = root.left
>     while node:
>         if not is_leaf(node):
>             boundary.append(node.val)
>         node = node.left if node.left else node.right
> 
>     def add_leaves(node):
>         if not node:
>             return
>         if is_leaf(node):
>             boundary.append(node.val)
>             return
>         add_leaves(node.left)
>         add_leaves(node.right)
> 
>     add_leaves(root)
> 
>     right = []
>     node = root.right
>     while node:
>         if not is_leaf(node):
>             right.append(node.val)
>         node = node.right if node.right else node.left
> 
>     boundary.extend(reversed(right))
>     return boundary
> ```

> [!success] Complexity
> O(n) time, O(h) recursion/auxiliary stack in the leaf traversal.

> [!tip] Alternatives
> Standard boundary problems are mostly about careful node inclusion rules, not complex traversal logic.

---

## Special Tree Problems

### Count Complete Tree Nodes (LC 222)

> [!example] Problem
> Given a complete binary tree, count the total number of nodes. A complete binary tree has all levels fully filled except possibly the last, which is filled left to right. Aim for better than O(n).

> [!info] Approach
> - **WHY:** A full binary tree of height `h` has `2^h - 1` nodes. In a complete tree, at least one of the left or right subtrees is a perfect binary tree — we can use this to skip entire subtrees in O(log²n).
> - **WHAT:** Compute the height of the leftmost path and the rightmost path of any subtree. If equal, the subtree is perfect: return `2^height - 1`. Otherwise, recurse on both children.
> - **HOW:** `left_height` = length of left spine. `right_height` = length of right spine. If equal, return `(1 << left_height) - 1`. Else return `1 + count(root.left) + count(root.right)`.

> [!note]- Python Solution
> ```python
> def count_nodes(root: TreeNode | None) -> int:
>     if not root:
>         return 0
>     left_height = 0
>     node = root
>     while node:
>         left_height += 1
>         node = node.left
>     right_height = 0
>     node = root
>     while node:
>         right_height += 1
>         node = node.right
>     if left_height == right_height:
>         return (1 << left_height) - 1
>     return 1 + count_nodes(root.left) + count_nodes(root.right)
> ```

> [!success] Complexity
> Time O(log²n) — each recursion level does O(log n) work and there are O(log n) levels. Space O(log n) call stack.

> [!tip] Alternatives
> - O(n) full traversal — correct but ignores the complete tree property.
> - Binary search on node indices with path existence check: also O(log²n), more complex.

---

### Binary Tree Cameras (LC 968)

> [!example] Problem
> Place the minimum number of cameras on tree nodes such that every node is either covered by a camera or adjacent to a node with a camera. Return the minimum number of cameras needed.

> [!info] Approach
> - **WHY:** Greedy: leaf nodes should never have cameras — it's always better to place a camera on the parent, which then covers both the leaf and the grandparent.
> - **WHAT:** Post-order DFS. Each node returns one of three states: 0 = not covered, 1 = has a camera, 2 = covered (no camera). A parent places a camera if either child is uncovered (state 0).
> - **HOW:** For each node: if either child is uncovered (state 0), place a camera here (state 1, increment count). If either child has a camera (state 1), this node is covered (state 2). Otherwise (both children covered without cameras), return state 0 — let the parent handle coverage. After DFS, if root returns state 0, place one more camera.

> [!note]- Python Solution
> ```python
> def min_camera_cover(root: TreeNode | None) -> int:
>     cameras = 0
>
>     def dfs(node: TreeNode | None) -> int:
>         # returns: 0 = uncovered, 1 = has camera, 2 = covered
>         if node is None:
>             return 2   # null nodes are considered covered
>         left = dfs(node.left)
>         right = dfs(node.right)
>         if left == 0 or right == 0:
>             nonlocal cameras
>             cameras += 1
>             return 1
>         if left == 1 or right == 1:
>             return 2
>         return 0
>
>     if dfs(root) == 0:
>         cameras += 1
>     return cameras
> ```

> [!success] Complexity
> Time O(n), Space O(h) for the call stack.

> [!tip] Alternatives
> - DP with states: `dp[node][0/1/2]` = min cameras for subtree where node is uncovered/has camera/covered. Equivalent but more verbose.
> - Key insight: null nodes return "covered" (2) so that leaves default to "uncovered" (0) naturally, triggering the parent to place a camera.

---

### Recover Binary Search Tree (LC 99)

> [!example] Problem
> Two nodes of a BST have been swapped by mistake. Recover the tree without changing its structure.

> [!info] Approach
> - **WHY:** In an inorder traversal of a valid BST, values are strictly increasing. A swap creates at most two "inversions" (places where `prev > current`). The first node of the first inversion and the second node of the last inversion are the swapped pair.
> - **WHAT:** Inorder traversal (iterative or recursive). Track `prev`, `first_bad`, and `second_bad`. At each inversion (`prev.val > curr.val`): if `first_bad` is not set, set it to `prev`; always update `second_bad` to `curr`.
> - **HOW:** After traversal, swap `first_bad.val` and `second_bad.val`.

> [!note]- Python Solution
> ```python
> def recover_tree(root: TreeNode | None) -> None:
>     first_bad = None
>     second_bad = None
>     prev = None
>
>     def inorder(node: TreeNode | None) -> None:
>         nonlocal first_bad, second_bad, prev
>         if not node:
>             return
>         inorder(node.left)
>         if prev and prev.val > node.val:
>             if first_bad is None:
>                 first_bad = prev
>             second_bad = node
>         prev = node
>         inorder(node.right)
>
>     inorder(root)
>     if first_bad and second_bad:
>         first_bad.val, second_bad.val = second_bad.val, first_bad.val
> ```

> [!success] Complexity
> Time O(n), Space O(h) for the call stack. Can be done in O(1) space with Morris traversal.

> [!tip] Alternatives
> - Morris inorder traversal: O(1) space, no stack, temporarily threads pointers — harder to code under pressure.
> - Key edge case: if the two swapped nodes are adjacent in inorder, there is only one inversion, so `second_bad` is set from the first (and only) inversion's `curr`.

---

## See Also

[[queue]] | [[dynamic-programming]] | [[graph]] | [[hashing]]
