---
tags: [coding, data-structures, tree]
topic: tree
difficulty: mixed
---

# Tree Problems — Deep Dive

**Pattern map**: Tree problems reduce to one of five techniques — DFS traversal (preorder/inorder/postorder), level-order BFS, LCA (post-order recurse), Tree DP (post-order returning tuples), BST operations (exploit ordering). The remaining problems are construction/serialization and O(1)-space Morris traversal.


> [!abstract] Google Interview Legend
> `🔥 Google` — **Core** problem: extremely high frequency at Google SDE 2/3 interviews. Cover these first.
> `⭐ Google` — **Important** problem: medium frequency at Google SDE 2/3 level. Cover after core.
> Problems without a marker are good practice but less Google-specific at SDE 2/3 level.

---

## DFS Traversal

### Binary Tree Inorder Traversal `🔥 Google`

> [!example] Problem
> Given the root of a binary tree, return the inorder traversal of its nodes' values.
> 
> **Example 1:**
> ```
> Input: root = [1,null,2,3]
> Output: [1,3,2]
> Explanation:
> ```
> 
> **Example 2:**
> ```
> Input: root = [1,2,3,4,5,null,8,null,null,6,7,9]
> Output: [4,2,6,5,7,1,3,9,8]
> Explanation:
> ```
> 
> **Example 3:**
> ```
> Input: root = []
> Output: []
> ```
> 
> **Example 4:**
> ```
> Input: root = [1]
> Output: [1]
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 100].
> - -100 <= Node.val <= 100

> [!info] Approach
> Recursive inorder is trivial; the iterative version uses an explicit stack to simulate the call stack. Key pattern: push all left children first, then process on pop, then pivot to right child. Iterative inorder — maintain a stack; keep going left until None, then pop and visit, then move to right child. `while curr or stack`: inner `while curr` pushes all lefts; `curr = stack.pop()` processes node, appends value; `curr = curr.right` to explore right subtree.

> [!note]- Python Solution
> ```python
> def inorder_traversal(root):
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

### Invert Binary Tree `🔥 Google`

> [!example] Problem
> Given the root of a binary tree, invert the tree, and return its root.
> 
> **Example 1:**
> ```
> Input: root = [4,2,7,1,3,6,9]
> Output: [4,7,2,9,6,3,1]
> ```
> 
> **Example 2:**
> ```
> Input: root = [2,1,3]
> Output: [2,3,1]
> ```
> 
> **Example 3:**
> ```
> Input: root = []
> Output: []
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 100].
> - -100 <= Node.val <= 100

> [!info] Approach
> **Post-order recursive swap.** Hierarchy is mirrored by swapping children at every node independently. What we need: visit every node once and swap its two children. Post-order recursion — swap after both subtrees are inverted. Base case `not root → None`. Recurse left and right, then swap: `root.left, root.right = invertTree(root.right), invertTree(root.left)`. Pre-order also works since swapping is an O(1) local operation.

> [!note]- Python Solution
> ```python
> def invert_tree(root):
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
> Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).
> 
> **Example 1:**
> ```
> Input: root = [1,2,2,3,4,4,3]
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: root = [1,2,2,null,3,null,3]
> Output: false
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [1, 1000].
> - -100 <= Node.val <= 100

> [!info] Approach
> **Recursive mirror(l, r) — outer and inner pair matching.** Symmetry means the left subtree mirrors the right subtree. Two subtrees mirror each other iff their roots are equal AND the outer pair matches (left.left ↔ right.right) AND the inner pair matches (left.right ↔ right.left). Define `mirror(l, r)` to check symmetry recursively. Base cases: both None → True (symmetric absence), exactly one None → False. Otherwise: `l.val == r.val and mirror(l.left, r.right) and mirror(l.right, r.left)`.

> [!note]- Python Solution
> ```python
> def is_symmetric(root):
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

### Maximum Depth of Binary Tree `🔥 Google`

> [!example] Problem
> Given the root of a binary tree, return its maximum depth.
> A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.
> 
> **Example 1:**
> ```
> Input: root = [3,9,20,null,null,15,7]
> Output: 3
> ```
> 
> **Example 2:**
> ```
> Input: root = [1,null,2]
> Output: 2
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 10^4].
> - -100 <= Node.val <= 100

> [!info] Approach
> **Post-order recursive max height.** Depth of a tree = 1 + max depth of its subtrees. This is the definition recursively applied. Post-order recursion — a node can't contribute its depth until both subtrees report theirs. Base case `not root → 0`; otherwise `1 + max(maxDepth(left), maxDepth(right))`.

> [!note]- Python Solution
> ```python
> def max_depth(root):
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
> Given a binary tree, find its minimum depth.
> The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.
> Note: A leaf is a node with no children.
> 
> **Example 1:**
> ```
> Input: root = [3,9,20,null,null,15,7]
> Output: 2
> ```
> 
> **Example 2:**
> ```
> Input: root = [2,null,3,null,4,null,5,null,6]
> Output: 5
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 10^5].
> - -1000 <= Node.val <= 1000

> [!info] Approach
> Critical trap: a node with only one child is NOT a leaf. Minimum depth must reach a node where BOTH children are None. Simply returning `1 + min(left_depth, right_depth)` fails for nodes with a single child — the zero-depth from the absent child would win incorrectly. Post-order recursion with explicit single-child guard. If left is None, return `1 + right_depth`; if right is None, return `1 + left_depth`; otherwise `1 + min(left, right)`. Base case: `not root → 0`. Then check left/right nullity before min.

> [!note]- Python Solution
> ```python
> def min_depth(root):
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

### Path Sum `⭐ Google`

> [!example] Problem
> Given the root of a binary tree and an integer targetSum, return true if the tree has a root-to-leaf path such that adding up all the values along the path equals targetSum.
> A leaf is a node with no children.
> 
> **Example 1:**
> ```
> Input: root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22
> Output: true
> Explanation: The root-to-leaf path with the target sum is shown.
> ```
> 
> **Example 2:**
> ```
> Input: root = [1,2,3], targetSum = 5
> Output: false
> Explanation: There are two root-to-leaf paths in the tree:
> (1 --> 2): The sum is 3.
> (1 --> 3): The sum is 4.
> There is no root-to-leaf path with sum = 5.
> ```
> 
> **Example 3:**
> ```
> Input: root = [], targetSum = 0
> Output: false
> Explanation: Since the tree is empty, there are no root-to-leaf paths.
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 5000].
> - -1000 <= Node.val <= 1000
> - -1000 <= targetSum <= 1000

> [!info] Approach
> **DFS subtracting current value — check at leaf.** A root-to-leaf path is uniquely defined by the sequence of nodes from root to a leaf. DFS naturally models path extension. Subtract the current node's value from the target as we descend; at a leaf, check if remaining equals zero. The leaf check is critical — only return True at nodes where `not left and not right` (both children null), not at any node where partial sum matches.

> [!note]- Python Solution
> ```python
> def has_path_sum(root, targetSum):
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

### Path Sum II `⭐ Google`

> [!example] Problem
> Given the root of a binary tree and an integer targetSum, return all root-to-leaf paths where the sum of the node values in the path equals targetSum. Each path should be returned as a list of the node values, not node references.
> A root-to-leaf path is a path starting from the root and ending at any leaf node. A leaf is a node with no children.
> 
> **Example 1:**
> ```
> Input: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
> Output: [[5,4,11,2],[5,8,4,5]]
> Explanation: There are two paths whose sum equals targetSum:
> 5 + 4 + 11 + 2 = 22
> 5 + 8 + 4 + 5 = 22
> ```
> 
> **Example 2:**
> ```
> Input: root = [1,2,3], targetSum = 5
> Output: []
> ```
> 
> **Example 3:**
> ```
> Input: root = [1,2], targetSum = 0
> Output: []
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 5000].
> - -1000 <= Node.val <= 1000
> - -1000 <= targetSum <= 1000

> [!info] Approach
> Collecting all paths requires backtracking — extend the path on entry, collect at leaves, pop on exit. The pop on the way back up is essential; without it the path list carries values from sibling branches. DFS backtracking — maintain a mutable `path` list; append on enter, pop on exit; collect a copy at leaves. At leaf (`not left and not right`) and `remaining == 0`: `result.append(list(path))` (copy! not reference). Then `path.pop()` on return regardless of whether this was a leaf.

> [!note]- Python Solution
> ```python
> def path_sum(root, targetSum):
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

### Sum Root to Leaf Numbers `⭐ Google`

> [!example] Problem
> You are given the root of a binary tree containing digits from 0 to 9 only.
> Each root-to-leaf path in the tree represents a number.
> Return the total sum of all root-to-leaf numbers. Test cases are generated so that the answer will fit in a 32-bit integer.
> A leaf node is a node with no children.
> 
> **Example 1:**
> ```
> Input: root = [1,2,3]
> Output: 25
> Explanation:
> The root-to-leaf path 1->2 represents the number 12.
> The root-to-leaf path 1->3 represents the number 13.
> Therefore, sum = 12 + 13 = 25.
> ```
> 
> **Example 2:**
> ```
> Input: root = [4,9,0,5,1]
> Output: 1026
> Explanation:
> The root-to-leaf path 4->9->5 represents the number 495.
> The root-to-leaf path 4->9->1 represents the number 491.
> The root-to-leaf path 4->0 represents the number 40.
> Therefore, sum = 495 + 491 + 40 = 1026.
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [1, 1000].
> - 0 <= Node.val <= 9
> - The depth of the tree will not exceed 10.

> [!info] Approach
> As we descend, the current number is `parent_number * 10 + node.val`. At a leaf, this is the fully formed number. DFS naturally threads this accumulated value downward. DFS passing accumulated value; sum up leaf contributions. `dfs(node, curr_num)` — `curr_num = curr_num * 10 + node.val`; at leaf return `curr_num`; otherwise return `dfs(left, curr_num) + dfs(right, curr_num)`.

> [!note]- Python Solution
> ```python
> def sum_numbers(root):
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

### Count Complete Tree Nodes `⭐ Google`

> [!example] Problem
> Given the root of a complete binary tree, return the number of the nodes in the tree.
> According to Wikipedia, every level, except possibly the last, is completely filled in a complete binary tree, and all nodes in the last level are as far left as possible. It can have between 1 and 2h nodes inclusive at the last level h.
> Design an algorithm that runs in less than O(n) time complexity.
> 
> **Example 1:**
> ```
> Input: root = [1,2,3,4,5,6]
> Output: 6
> ```
> 
> **Example 2:**
> ```
> Input: root = []
> Output: 0
> ```
> 
> **Example 3:**
> ```
> Input: root = [1]
> Output: 1
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 5 * 10^4].
> - 0 <= Node.val <= 5 * 10^4
> - The tree is guaranteed to be complete.

> [!info] Approach
> A naive O(n) traversal ignores the complete tree property. In a complete tree, every level except possibly the last is full, and the last level fills left to right. That lets us detect when one subtree is perfect and count it with `2^h - 1` instead of visiting every node. Compare the leftmost height of `root.left` and `root.right`. If they are equal, the left subtree is perfect, so count it in O(1) and recurse only on the right. Otherwise, the right subtree is perfect, so count it in O(1) and recurse only on the left. `height(node)` follows `.left` pointers only. If `left_h == right_h`, return `2^left_h + countNodes(root.right)`; else return `2^right_h + countNodes(root.left)`.

> [!note]- Python Solution
> ```python
> def count_nodes(root):
>     if not root:
>         return 0
>     def height(node):
>         h = 0
>         while node:
>             h += 1
>             node = node.left
>         return h
> >
>     left_h = height(root.left)
>     right_h = height(root.right)
>     if left_h == right_h:
>         return (1 << left_h) + countNodes(root.right)
>     return (1 << right_h) + countNodes(root.left)
> ```

> [!success] Complexity
> Time O(log²n) — each recursive step computes a height in O(log n), and recursion follows only one subtree. Space O(log n).

> [!tip] Alternatives
> - O(n) linear traversal: correct but misses the point of the problem.
> - Binary search on last level with bit-path encoding: same O(log²n) but more complex to implement.

---

### Count Good Nodes in Binary Tree

> [!example] Problem
> Given a binary tree root, a node X in the tree is named good if in the path from root to X there are no nodes with a value greater than X.
> Return the number of good nodes in the binary tree.
> 
> **Example 1:**
> ```
> Input: root = [3,1,4,3,null,1,5]
> Output: 4
> Explanation: Nodes in blue are good.
> Root Node (3) is always a good node.
> Node 4 -> (3,4) is the maximum value in the path starting from the root.
> Node 5 -> (3,4,5) is the maximum value in the path
> Node 3 -> (3,1,3) is the maximum value in the path.
> ```
> 
> **Example 2:**
> ```
> Input: root = [3,3,null,4,2]
> Output: 3
> Explanation: Node 2 -> (3, 3, 2) is not good, because "3" is higher than it.
> ```
> 
> **Example 3:**
> ```
> Input: root = [1]
> Output: 1
> Explanation: Root is considered as good.
> ```
> 
> **Constraints:**
> - The number of nodes in the binary tree is in the range [1, 10^5].
> - Each node's value is between [-10^4, 10^4].

> [!info] Approach
> **DFS with propagated path_max.** Goodness depends on the path from root to the node — we need to carry the maximum value seen so far. Purely structural traversal can't determine goodness without ancestor context. Pass `path_max` down; a node is good iff `node.val >= path_max`. Update `path_max = max(path_max, node.val)` before recursing; root is always good.

> [!note]- Python Solution
> ```python
> def good_nodes(root):
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
> Given the roots of two binary trees p and q, write a function to check if they are the same or not.
> Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.
> 
> **Example 1:**
> ```
> Input: p = [1,2,3], q = [1,2,3]
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: p = [1,2], q = [1,null,2]
> Output: false
> ```
> 
> **Example 3:**
> ```
> Input: p = [1,2,1], q = [1,1,2]
> Output: false
> ```
> 
> **Constraints:**
> - The number of nodes in both trees is in the range [0, 100].
> - -10^4 <= Node.val <= 10^4

> [!info] Approach
> Two trees are the same iff their roots match and both subtrees are recursively the same. A null/non-null mismatch immediately returns false. Simultaneous pre-order DFS on both trees; fail on any structural or value mismatch. Base cases: both None → True; exactly one None → False; `p.val != q.val` → False. Recurse: `isSameTree(p.left, q.left) and isSameTree(p.right, q.right)`.

> [!note]- Python Solution
> ```python
> def is_same_tree(p, q):
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

### Subtree of Another Tree `⭐ Google`

> [!example] Problem
> Given the roots of two binary trees root and subRoot, return true if there is a subtree of root with the same structure and node values of subRoot and false otherwise.
> A subtree of a binary tree tree is a tree that consists of a node in tree and all of this node's descendants. The tree tree could also be considered as a subtree of itself.
> 
> **Example 1:**
> ```
> Input: root = [3,4,5,1,2], subRoot = [4,1,2]
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]
> Output: false
> ```
> 
> **Constraints:**
> - The number of nodes in the root tree is in the range [1, 2000].
> - The number of nodes in the subRoot tree is in the range [1, 1000].
> - -10^4 <= root.val <= 10^4
> - -10^4 <= subRoot.val <= 10^4

> [!info] Approach
> For each node in `root`, check if the subtree rooted there matches `subRoot`. Reuses `isSameTree` as a subroutine — classic compositional approach. DFS over `root`; at each node invoke `isSameTree(node, subRoot)`. Short-circuit on match. `isSubtree(root, subRoot)` — if not root: False; if `isSameTree(root, subRoot)`: True; else recurse left and right.

> [!note]- Python Solution
> ```python
> def is_subtree(root, subRoot):
>     def is_same_tree(p, q):
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
> Given the root of a binary tree, flatten the tree into a "linked list"
> 
> **Example 1:**
> ```
> Input: root = [1,2,5,3,4,null,6]
> Output: [1,null,2,null,3,null,4,null,5,null,6]
> ```
> 
> **Example 2:**
> ```
> Input: root = []
> Output: []
> ```
> 
> **Example 3:**
> ```
> Input: root = [0]
> Output: [0]
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 2000].
> - -100 <= Node.val <= 100

> [!info] Approach
> **Morris-style in-place threading — find inorder predecessor.** Preorder = root → left → right. To flatten in-place without extra space: for each node with a left child, the end of the left subtree's rightmost chain should point to the original right subtree. Morris-style threading applied to flattening. Move the left subtree to the right and null the left. For each `curr` with a left child: find rightmost node in left subtree (`prev`), wire `prev.right = curr.right`, move `curr.right = curr.left`, null `curr.left`. Advance `curr = curr.right`.

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

### Step-By-Step Directions From a Binary Tree Node to Another `⭐ Google`

> [!example] Problem
> You are given the root of a binary tree with n nodes. Each node is uniquely assigned a value from 1 to n. You are also given an integer startValue representing the value of the start node s, and a different integer destValue representing the value of the destination node t.
> Find the shortest path starting from node s and ending at node t. Generate step-by-step directions of such path as a string consisting of only the uppercase letters 'L', 'R', and 'U'. Each letter indicates a specific direction:
> Return the step-by-step directions of the shortest path from node s to node t.
> 
> **Example 1:**
> ```
> Input: root = [5,1,2,3,null,6,4], startValue = 3, destValue = 6
> Output: "UURL"
> Explanation: The shortest path is: 3 → 1 → 5 → 2 → 6.
> ```
> 
> **Example 2:**
> ```
> Input: root = [2,1], startValue = 2, destValue = 1
> Output: "L"
> Explanation: The shortest path is: 2 → 1.
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is n.
> - 2 <= n <= 10^5
> - 1 <= Node.val <= n
> - All the values in the tree are unique.
> - 1 <= startValue, destValue <= n
> - startValue != destValue

> [!info] Approach
> **DFS to root→start and root→dest paths, strip common prefix.** The shortest path between two nodes in a tree goes through their LCA. Find root→start and root→dest as L/R sequences; strip the common prefix (= path to LCA); start's remaining path becomes all 'U's (going up to LCA), dest's remaining path is the L/R directions from LCA to dest. DFS to record L/R path from root to each target node, then strip common prefix.

> [!note]- Python Solution
> ```python
> def get_directions(root, startValue, destValue):
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

### Binary Tree Zigzag Level Order Traversal `⭐ Google`

> [!example] Problem
> Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. (i.e., from left to right, then right to left for the next level and alternate between).
> 
> **Example 1:**
> ```
> Input: root = [3,9,20,null,null,15,7]
> Output: [[3],[20,9],[15,7]]
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
> - -100 <= Node.val <= 100

> [!info] Approach
> Same as level-order BFS but every other level needs reversal. Toggle a flag per level rather than using a deque with dual-end insertion — simpler and avoids subtle off-by-one errors. BFS with level-size snapshot; after building each level list, conditionally reverse it before appending. `left_to_right = True` initially; after collecting each level: if `not left_to_right`, `level.reverse()`; then `left_to_right = not left_to_right`.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def zigzag_level_order(root):
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

### Populating Next Right Pointers in Each Node `⭐ Google`

> [!example] Problem
> You are given a perfect binary tree where all leaves are on the same level, and every parent has two children. The binary tree has the following definition:
> Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to NULL.
> Initially, all next pointers are set to NULL.
> 
> **Example 1:**
> ```
> struct Node {
>   int val;
>   Node *left;
>   Node *right;
>   Node *next;
> }
> ```
> 
> **Example 2:**
> ```
> Input: root = [1,2,3,4,5,6,7]
> Output: [1,#,2,3,#,4,5,6,7,#]
> Explanation: Given the above perfect binary tree (Figure A), your function should populate each next pointer to point to its next right node, just like in Figure B. The serialized output is in level order as connected by the next pointers, with '#' signifying the end of each level.
> ```
> 
> **Example 3:**
> ```
> Input: root = []
> Output: []
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 212 - 1].
> - -1000 <= Node.val <= 1000

> [!info] Approach
> **O(1) space — walk current level to connect next level.** Perfect binary tree: every internal node has exactly two children; all leaves at the same level. Once level k is connected via next pointers, we can traverse it like a linked list to connect level k+1. For each node in level k: `node.left.next = node.right` (sibling connection) and `node.right.next = node.next.left if node.next else None` (cousin connection). Start with `leftmost = root`; inner loop walks the current level using `head.next`; outer loop descends via `leftmost = leftmost.left`.

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

### Vertical Order Traversal of a Binary Tree `⭐ Google`

> [!example] Problem
> Given the root of a binary tree, calculate the vertical order traversal of the binary tree.
> For each node at position (row, col), its left and right children will be at positions (row + 1, col - 1) and (row + 1, col + 1) respectively. The root of the tree is at (0, 0).
> The vertical order traversal of a binary tree is a list of top-to-bottom orderings for each column index starting from the leftmost column and ending on the rightmost column. There may be multiple nodes in the same row and same column. In such a case, sort these nodes by their values.
> Return the vertical order traversal of the binary tree.
> 
> **Example 1:**
> ```
> Input: root = [3,9,20,null,null,15,7]
> Output: [[9],[3,15],[20],[7]]
> Explanation:
> Column -1: Only node 9 is in this column.
> Column 0: Nodes 3 and 15 are in this column in that order from top to bottom.
> Column 1: Only node 20 is in this column.
> Column 2: Only node 7 is in this column.
> ```
> 
> **Example 2:**
> ```
> Input: root = [1,2,3,4,5,6,7]
> Output: [[4],[2],[1,5,6],[3],[7]]
> Explanation:
> Column -2: Only node 4 is in this column.
> Column -1: Only node 2 is in this column.
> Column 0: Nodes 1, 5, and 6 are in this column.
>           1 is at the top, so it comes first.
>           5 and 6 are at the same position (2, 0), so we order them by their value, 5 before 6.
> Column 1: Only node 3 is in this column.
> Column 2: Only node 7 is in this column.
> ```
> 
> **Example 3:**
> ```
> Input: root = [1,2,3,4,6,5,7]
> Output: [[4],[2],[1,5,6],[3],[7]]
> Explanation:
> This case is the exact same as example 2, but with nodes 5 and 6 swapped.
> Note that the solution remains the same since 5 and 6 are in the same location and should be ordered by their values.
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [1, 1000].
> - 0 <= Node.val <= 1000

> [!info] Approach
> **DFS collect (col, row, val) tuples, sort, group.** Vertical order is defined by column assignment: root at col 0, left child at col-1, right child at col+1, row increases by 1 per level. Sort-based approach — collect all (col, row, val) tuples and sorting by (col, row, val) handles ties correctly. DFS assigning (row, col) to each node, collect all tuples, sort, then group by column.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def vertical_traversal(root):
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

### All Nodes Distance K in Binary Tree `⭐ Google`

> [!example] Problem
> Given the root of a binary tree, the value of a target node target, and an integer k, return an array of the values of all nodes that have a distance k from the target node.
> You can return the answer in any order.
> 
> **Example 1:**
> ```
> Input: root = [3,5,1,6,2,0,8,null,null,7,4], target = 5, k = 2
> Output: [7,4,1]
> Explanation: The nodes that are a distance 2 from the target node (with value 5) have values 7, 4, and 1.
> ```
> 
> **Example 2:**
> ```
> Input: root = [1], target = 1, k = 3
> Output: []
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [1, 500].
> - 0 <= Node.val <= 500
> - All the values Node.val are unique.
> - target is the value of one of the nodes in the tree.
> - 0 <= k <= 1000

> [!info] Approach
> **Build undirected graph, BFS k steps from target.** In a tree, distance can only go downward from any node. But from the target, distance can also go upward through parents — making this a graph problem. Adding parent edges allows BFS to spread in all directions from target. Build an adjacency list (bidirectional) via one DFS, then BFS from target for exactly k steps. Build graph first, BFS second, collect nodes at distance == k.

> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> 
> def distance_k(root, target, k):
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

### Lowest Common Ancestor of a Binary Tree `🔥 Google`

> [!example] Problem
> Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.
> According to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself).”
> 
> **Example 1:**
> ```
> Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
> Output: 3
> Explanation: The LCA of nodes 5 and 1 is 3.
> ```
> 
> **Example 2:**
> ```
> Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
> Output: 5
> Explanation: The LCA of nodes 5 and 4 is 5, since a node can be a descendant of itself according to the LCA definition.
> ```
> 
> **Example 3:**
> ```
> Input: root = [1,2], p = 1, q = 2
> Output: 1
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [2, 10^5].
> - -10^9 <= Node.val <= 10^9
> - All Node.val are unique.
> - p != q
> - p and q will exist in the tree.

> [!info] Approach
> **Post-order recursion — converge at split node.** The LCA is determined by what comes back from both subtrees — we need children to report before the parent decides. If the current node is None, p, or q, return it. Recurse left and right. If both return non-None, both targets were found in different subtrees → current node is LCA. If only one side returns non-None, the LCA is in that subtree. `if left and right: return root; return left or right`.

> [!note]- Python Solution
> ```python
> def lowest_common_ancestor(root, p, q):
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

### Lowest Common Ancestor of a BST `🔥 Google`

> [!example] Problem
> Same as above but the tree is a BST. Exploit the ordering property.

> [!info] Approach
> **Iterative BST-guided descent — O(h) instead of O(n).** In a BST, if both p and q are less than root, their LCA must be in the left subtree. If both are greater, LCA is in the right subtree. The moment they "diverge" (one ≤ root ≤ other, or one equals root), the current root is the LCA. Iteratively follow the BST property — no recursion into both subtrees. If both p, q < root, go left. If both > root, go right. Otherwise return root.

> [!note]- Python Solution
> ```python
> def lowest_common_ancestor(root, p, q):
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

### Diameter of Binary Tree `🔥 Google`

> [!example] Problem
> Given the root of a binary tree, return the length of the diameter of the tree.
> The diameter of a binary tree is the length of the longest path between any two nodes in a tree. This path may or may not pass through the root.
> The length of a path between two nodes is represented by the number of edges between them.
> 
> **Example 1:**
> ```
> Input: root = [1,2,3,4,5]
> Output: 3
> Explanation: 3 is the length of the path [4,2,1,3] or [5,2,1,3].
> ```
> 
> **Example 2:**
> ```
> Input: root = [1,2]
> Output: 1
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [1, 10^4].
> - -100 <= Node.val <= 100

> [!info] Approach
> **Post-order height DFS with global diameter update.** The diameter through any node = left_height + right_height. We can't compute this without first knowing both subtree heights — post-order. `height(node)` returns the height of the subtree; as a side effect, updates global `diameter = max(diameter, left + right)`. Return `1 + max(left, right)` upward; update `best[0]` with `l + r` at each node.

> [!note]- Python Solution
> ```python
> def diameter_of_binary_tree(root):
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

### Binary Tree Maximum Path Sum `🔥 Google`

> [!example] Problem
> A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.
> The path sum of a path is the sum of the node's values in the path.
> Given the root of a binary tree, return the maximum path sum of any non-empty path.
> 
> **Example 1:**
> ```
> Input: root = [1,2,3]
> Output: 6
> Explanation: The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6.
> ```
> 
> **Example 2:**
> ```
> Input: root = [-10,9,20,null,null,15,7]
> Output: 42
> Explanation: The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42.
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [1, 3 * 10^4].
> - -1000 <= Node.val <= 1000

> [!info] Approach
> **Post-order gain DFS — clamp negatives to 0.** A path should not extend into a subtree that contributes a negative sum — drop it (treat as 0). Distinguish two roles — the "gain returned to parent" (extends into at most one child) vs. the "path through this node as apex" (can use both children). `gain(node) = node.val + max(l, r)` returned upward; global update = `node.val + l + r` (where l and r already have negatives clamped to 0).

> [!note]- Python Solution
> ```python
> def max_path_sum(root):
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

### House Robber III `🔥 Google`

> [!example] Problem
> The thief has found himself a new place for his thievery again. There is only one entrance to this area, called root.
> Besides the root, each house has one and only one parent house. After a tour, the smart thief realized that all houses in this place form a binary tree. It will automatically contact the police if two directly-linked houses were broken into on the same night.
> Given the root of the binary tree, return the maximum amount of money the thief can rob without alerting the police.
> 
> **Example 1:**
> ```
> Input: root = [3,2,3,null,3,null,1]
> Output: 7
> Explanation: Maximum amount of money the thief can rob = 3 + 3 + 1 = 7.
> ```
> 
> **Example 2:**
> ```
> Input: root = [3,4,5,1,3,null,1]
> Output: 9
> Explanation: Maximum amount of money the thief can rob = 4 + 5 = 9.
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [1, 10^4].
> - 0 <= Node.val <= 10^4

> [!info] Approach
> **Post-order DP returning (rob, skip) pair.** The parent's optimal choice (rob or skip its parent) depends on both options at each child — returning a single value forces suboptimal choices. `dp(node)` returns `(rob, skip)` — maximum money if we rob vs. skip this node. `rob = node.val + l_skip + r_skip`; `skip = max(l_rob, l_skip) + max(r_rob, r_skip)`. Post-order: compute children first.

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
> - Memo dict on `(node, can_rob)` — same complexity; explicit cache is easier to explain than a decorator.
> - Naive recursion without caching: O(2^n) — recomputes subproblems exponentially.

---

### Binary Tree Cameras `⭐ Google`

> [!example] Problem
> You are given the root of a binary tree. We install cameras on the tree nodes where each camera at a node can monitor its parent, itself, and its immediate children.
> Return the minimum number of cameras needed to monitor all nodes of the tree.
> 
> **Example 1:**
> ```
> Input: root = [0,0,null,0,0]
> Output: 1
> Explanation: One camera is enough to monitor all nodes if placed as shown.
> ```
> 
> **Example 2:**
> ```
> Input: root = [0,0,null,0,null,0,null,null,0]
> Output: 2
> Explanation: At least two cameras are needed to monitor all nodes of the tree. The above image shows one of the valid configurations of camera placement.
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [1, 1000].
> - Node.val == 0

> [!info] Approach
> **Greedy post-order — delay cameras upward.** It's always optimal to delay camera placement upward (put the camera at the parent of an uncovered leaf rather than at the leaf). Three states per node — 0 = uncovered (needs a camera from parent), 1 = covered but no camera, 2 = has a camera. Null nodes return 1 (trivially covered). If any child returns 0, place a camera here (return 2, increment count). If any child has a camera (returns 2), this node is covered (return 1). Otherwise return 0 (push responsibility to parent).

> [!note]- Python Solution
> ```python
> def min_camera_cover(root):
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

### Path Sum III `⭐ Google`

> [!example] Problem
> Given the root of a binary tree and an integer targetSum, return the number of paths where the sum of the values along the path equals targetSum.
> The path does not need to start or end at the root or a leaf, but it must go downwards (i.e., traveling only from parent nodes to child nodes).
> 
> **Example 1:**
> ```
> Input: root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
> Output: 3
> Explanation: The paths that sum to 8 are shown.
> ```
> 
> **Example 2:**
> ```
> Input: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
> Output: 3
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 1000].
> - -10^9 <= Node.val <= 10^9
> - -1000 <= targetSum <= 1000

> [!info] Approach
> **DFS with prefix sum hash map + backtracking.** A downward path ending at node X has sum = `running_sum[X] - running_sum[ancestor]`. If `running_sum[X] - targetSum` was seen at some ancestor, that ancestor→X path sums to targetSum. Maintain `{prefix_sum: count}` hash map; initialize with `{0: 1}` (empty path from root). DFS — add node.val to running sum, query map for `running_sum - targetSum`, increment map, recurse children, then decrement map on backtrack (critical: prevents prefix sum from leaking into sibling branches).

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def path_sum(root, targetSum):
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

### Validate Binary Search Tree `🔥 Google`

> [!example] Problem
> Given the root of a binary tree, determine if it is a valid binary search tree (BST).
> A valid BST is defined as follows
> 
> **Example 1:**
> ```
> Input: root = [2,1,3]
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: root = [5,1,4,null,null,3,6]
> Output: false
> Explanation: The root node's value is 5 but its right child's value is 4.
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [1, 10^4].
> - -2^{31} <= Node.val <= 2^{31} - 1

> [!info] Approach
> **Recursive range validation — propagate (lo, hi) bounds.** Checking only `node.left.val < node.val < node.right.val` misses global violations. Carry `(lo, hi)` bounds down the tree; each node must satisfy `lo < node.val < hi`. Going left, tighten upper bound to `node.val`; going right, tighten lower bound. `validate(node, lo, hi)` — fail if not `lo < node.val < hi`, else recurse with tightened bounds.

> [!note]- Python Solution
> ```python
> def is_valid_bst(root):
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

### Kth Smallest Element in a BST `🔥 Google`

> [!example] Problem
> Given the root of a binary search tree, and an integer k, return the kth smallest value (1-indexed) of all the values of the nodes in the tree.
> 
> **Example 1:**
> ```
> Input: root = [3,1,4,null,2], k = 1
> Output: 1
> ```
> 
> **Example 2:**
> ```
> Input: root = [5,3,6,2,4,null,null,1], k = 3
> Output: 3
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is n.
> - 1 <= k <= n <= 10^4
> - 0 <= Node.val <= 10^4

> [!info] Approach
> **Iterative inorder with early exit at k.** BST inorder traversal yields values in ascending sorted order — the kth node visited is the kth smallest. Iterative form allows clean early termination at exactly k pops. Standard iterative inorder — push all left children onto stack, pop, decrement k, if k == 0 return. `while stack or root`: push all left children, pop, decrement k, if k == 0 return val, else advance to right child.

> [!note]- Python Solution
> ```python
> def kth_smallest(root, k):
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
> Insert follows BST search path to find the null slot. Delete has three cases: leaf (just remove), one child (bypass the node), two children (replace with inorder successor or predecessor then delete that successor). Insert — recurse into left or right based on comparison; on hitting None, return a new node. Delete — recurse to find target; on finding it, handle the three cases. Delete's two-child case: find inorder successor (leftmost in right subtree), copy its value to current node, then delete successor from right subtree.

> [!note]- Python Solution
> ```python
> def insert_into_bst(root, val):
>     if not root:
>         return TreeNode(val)
>     if val < root.val:
>         root.left  = insertIntoBST(root.left,  val)
>     else:
>         root.right = insertIntoBST(root.right, val)
>     return root
> 
> def delete_node(root, key):
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
> Given the root node of a binary search tree and two integers low and high, return the sum of values of all nodes with a value in the inclusive range [low, high].
> 
> **Example 1:**
> ```
> Input: root = [10,5,15,3,7,null,18], low = 7, high = 15
> Output: 32
> Explanation: Nodes 7, 10, and 15 are in the range [7, 15]. 7 + 10 + 15 = 32.
> ```
> 
> **Example 2:**
> ```
> Input: root = [10,5,15,3,7,13,18,1,null,6], low = 6, high = 10
> Output: 23
> Explanation: Nodes 6, 7, and 10 are in the range [6, 10]. 6 + 7 + 10 = 23.
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [1, 2 * 10^4].
> - 1 <= Node.val <= 10^5
> - 1 <= low <= high <= 10^5
> - All Node.val are unique.

> [!info] Approach
> **DFS with BST pruning — skip entire subtrees.** Unlike a general tree, BST allows skipping entire subtrees. If `node.val < low`, the left subtree contains only smaller values — skip it. If `node.val > high`, right subtree contains only larger values — skip it. DFS that prunes based on BST ordering. Only recurse left if `node.val > low`; only recurse right if `node.val < high`.

> [!note]- Python Solution
> ```python
> def range_sum_bst(root, low, high):
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

### Recover Binary Search Tree `⭐ Google`

> [!example] Problem
> You are given the root of a binary search tree (BST), where the values of exactly two nodes of the tree were swapped by mistake. Recover the tree without changing its structure.
> 
> **Example 1:**
> ```
> Input: root = [1,3,null,null,2]
> Output: [3,1,null,null,2]
> Explanation: 3 cannot be a left child of 1 because 3 > 1. Swapping 1 and 3 makes the BST valid.
> ```
> 
> **Example 2:**
> ```
> Input: root = [3,1,4,null,null,2]
> Output: [2,1,4,null,null,3]
> Explanation: 2 cannot be in the right subtree of 3 because 2 < 3. Swapping 2 and 3 makes the BST valid.
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [2, 1000].
> - -2^{31} <= Node.val <= 2^{31} - 1

> [!info] Approach
> **Inorder DFS — detect inversion pair(s), swap values.** A correct BST's inorder traversal is strictly ascending. Two swapped nodes create inversions. If adjacent in inorder: one inversion. If non-adjacent: two inversions. Inorder DFS tracking `prev`; on first inversion set `first = prev, second = curr`; on second inversion update `second = curr`. Swap `first.val` and `second.val`. One or two inversion sites. Always: `first = prev` at first inversion; `second = curr` at each inversion (covers both one and two inversion cases).

> [!note]- Python Solution
> ```python
> def recover_tree(root):
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

### Serialize and Deserialize Binary Tree `🔥 Google`

> [!example] Problem
> Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.
> Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.
> Clarification: The input/output format is the same as how LeetCode serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.
> 
> **Example 1:**
> ```
> Input: root = [1,2,3,null,null,4,5]
> Output: [1,2,3,null,null,4,5]
> ```
> 
> **Example 2:**
> ```
> Input: root = []
> Output: []
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 10^4].
> - -1000 <= Node.val <= 1000

> [!info] Approach
> **Preorder DFS with null markers — iterator-based deserialization.** Preorder places the root first, so during deserialization we can reconstruct the root before its children — naturally recursive. Inorder alone is insufficient (can't determine split without knowing root). DFS emitting node values and `#` for null, comma-delimited. Deserialize using an iterator over tokens. Serialize: DFS pre-order appending values or `#`. Deserialize: iterate tokens; `#` → return None; otherwise create node, recurse left, recurse right. Use an iterator to advance position across recursive calls.

> [!note]- Python Solution
> ```python
> class Codec:
>     def serialize(self, root):
>         result = []
>         def dfs(node):
>             if not node:
>                 result.append('#')
>                 return
>             result.append(str(node.val))
>             dfs(node.left)
>             dfs(node.right)
>         dfs(root)
>         return ','.join(result)
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

### Construct Binary Tree from Preorder and Inorder Traversal `🔥 Google`

> [!example] Problem
> Given two integer arrays preorder and inorder where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.
> 
> **Example 1:**
> ```
> Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
> Output: [3,9,20,null,null,15,7]
> ```
> 
> **Example 2:**
> ```
> Input: preorder = [-1], inorder = [-1]
> Output: [-1]
> ```
> 
> **Constraints:**
> - 1 <= preorder.length <= 3000
> - inorder.length == preorder.length
> - -3000 <= preorder[i], inorder[i] <= 3000
> - preorder and inorder consist of unique values.
> - Each value of inorder also appears in preorder.
> - preorder is guaranteed to be the preorder traversal of the tree.
> - inorder is guaranteed to be the inorder traversal of the tree.

> [!info] Approach
> **Preorder index advance + inorder hash map for O(1) root lookup.** Preorder[0] is always the root; find it in inorder — everything left is the left subtree, everything right is the right subtree. Hash map gives O(1) inorder index lookup instead of O(n) linear scan. Advance a global preorder index as you recurse; pass inorder bounds to slice logically without creating new arrays. `build(in_left, in_right)` — take `preorder[pre_idx]` as root, find its inorder position `mid`, build left subtree with `in_left..mid-1`, right subtree with `mid+1..in_right`.

> [!note]- Python Solution
> ```python
> def build_tree(preorder, inorder):
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

### Construct Binary Tree from Inorder and Postorder Traversal `⭐ Google`

> [!example] Problem
> Given two integer arrays inorder and postorder where inorder is the inorder traversal of a binary tree and postorder is the postorder traversal of the same tree, construct and return the binary tree.
> 
> **Example 1:**
> ```
> Input: inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]
> Output: [3,9,20,null,null,15,7]
> ```
> 
> **Example 2:**
> ```
> Input: inorder = [-1], postorder = [-1]
> Output: [-1]
> ```
> 
> **Constraints:**
> - 1 <= inorder.length <= 3000
> - postorder.length == inorder.length
> - -3000 <= inorder[i], postorder[i] <= 3000
> - inorder and postorder consist of unique values.
> - Each value of postorder also appears in inorder.
> - inorder is guaranteed to be the inorder traversal of the tree.
> - postorder is guaranteed to be the postorder traversal of the tree.

> [!info] Approach
> Postorder's last element is always the root. Find it in inorder — elements to its left form the left subtree, elements to its right form the right subtree. Symmetric to the preorder+inorder problem. Walk postorder array right-to-left (using a decrementing index); build right subtree before left (reversed postorder visits root, right, left). `build(in_left, in_right)` — take `postorder[post_idx]` as root, decrement index, find root in inorder hash map as `mid`, build right subtree `(mid+1, in_right)` FIRST, then left `(in_left, mid-1)`.

> [!note]- Python Solution
> ```python
> def build_tree(inorder, postorder):
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

### Morris Inorder Traversal (Technique) `⭐ Google`

> **Morris threading — O(1) space inorder via temporary right pointer threads.** Standard inorder traversal uses O(h) stack space. Morris traversal achieves O(1) auxiliary space by temporarily threading the tree — using unused right pointers of inorder predecessors to "remember" where to return after exploring a left subtree. For each node `curr`: if no left child, visit and move right. Otherwise find inorder predecessor (rightmost in left subtree). If predecessor.right is None: create thread, go left. If predecessor.right is curr: unthread, visit, go right. The tree is temporarily mutated and fully restored on completion.

> [!note]- Python Solution
> ```python
> def morris_inorder(root):
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

> **Morris threading — visit on first encounter (threading), not second.** Preorder visits root before children. In Morris traversal, the first encounter with a node (when we create the thread) corresponds to preorder. Same as Morris inorder but visit node when threading (first encounter) rather than when unthreading (second encounter). When `pre.right is None` (first encounter): set thread, visit node, go left. When `pre.right is curr` (second encounter): remove thread, go right (do NOT visit again).

> [!note]- Python Solution
> ```python
> def morris_preorder(root):
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

> **1-stack iterative postorder with last_visited sentinel.** Postorder (L → R → Root) is the hardest iterative traversal. The root is encountered twice — once when first descending and once after returning from the right subtree. A `last_visited` pointer distinguishes these two cases. Standard iterative inorder base — after exhausting left children, peek at the stack top. If it has an unvisited right child, go right. Otherwise process the node and record `last_visited`. Peek at `stack[-1]`. If `peek.right` exists and `peek.right is not last_visited`, go right. Otherwise: process (append), pop, set `last_visited = popped_node`.

> [!note]- Python Solution
> ```python
> def iterative_postorder(root):
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
> The boundary is not a standard traversal; it is a combination of three ordered pieces with non-overlapping responsibilities. Collect the left boundary excluding leaves, then all leaves left-to-right, then the right boundary excluding leaves and reverse it. Handle edge cases carefully so the root and leaf nodes are not duplicated.

> [!note]- Python Solution
> ```python
> def boundary_of_binary_tree(root):
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

### Count Complete Tree Nodes (LC 222) `⭐ Google`

> [!example] Problem
> Given the root of a complete binary tree, return the number of the nodes in the tree.
> According to Wikipedia, every level, except possibly the last, is completely filled in a complete binary tree, and all nodes in the last level are as far left as possible. It can have between 1 and 2h nodes inclusive at the last level h.
> Design an algorithm that runs in less than O(n) time complexity.
> 
> **Example 1:**
> ```
> Input: root = [1,2,3,4,5,6]
> Output: 6
> ```
> 
> **Example 2:**
> ```
> Input: root = []
> Output: 0
> ```
> 
> **Example 3:**
> ```
> Input: root = [1]
> Output: 1
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 5 * 10^4].
> - 0 <= Node.val <= 5 * 10^4
> - The tree is guaranteed to be complete.

> [!info] Approach
> A full binary tree of height `h` has `2^h - 1` nodes. In a complete tree, at least one of the left or right subtrees is a perfect binary tree — we can use this to skip entire subtrees in O(log²n). Compute the height of the leftmost path and the rightmost path of any subtree. If equal, the subtree is perfect: return `2^height - 1`. Otherwise, recurse on both children. `left_height` = length of left spine. `right_height` = length of right spine. If equal, return `(1 << left_height) - 1`. Else return `1 + count(root.left) + count(root.right)`.

> [!note]- Python Solution
> ```python
> def count_nodes(root):
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

### Binary Tree Cameras (LC 968) `⭐ Google`

> [!example] Problem
> You are given the root of a binary tree. We install cameras on the tree nodes where each camera at a node can monitor its parent, itself, and its immediate children.
> Return the minimum number of cameras needed to monitor all nodes of the tree.
> 
> **Example 1:**
> ```
> Input: root = [0,0,null,0,0]
> Output: 1
> Explanation: One camera is enough to monitor all nodes if placed as shown.
> ```
> 
> **Example 2:**
> ```
> Input: root = [0,0,null,0,null,0,null,null,0]
> Output: 2
> Explanation: At least two cameras are needed to monitor all nodes of the tree. The above image shows one of the valid configurations of camera placement.
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [1, 1000].
> - Node.val == 0

> [!info] Approach
> Greedy: leaf nodes should never have cameras — it's always better to place a camera on the parent, which then covers both the leaf and the grandparent. Post-order DFS. Each node returns one of three states: 0 = not covered, 1 = has a camera, 2 = covered (no camera). A parent places a camera if either child is uncovered (state 0). For each node: if either child is uncovered (state 0), place a camera here (state 1, increment count). If either child has a camera (state 1), this node is covered (state 2). Otherwise (both children covered without cameras), return state 0 — let the parent handle coverage. After DFS, if root returns state 0, place one more camera.

> [!note]- Python Solution
> ```python
> def min_camera_cover(root):
>     cameras = 0
> >
>     def dfs(node):
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
> >
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

### Recover Binary Search Tree (LC 99) `⭐ Google`

> [!example] Problem
> You are given the root of a binary search tree (BST), where the values of exactly two nodes of the tree were swapped by mistake. Recover the tree without changing its structure.
> 
> **Example 1:**
> ```
> Input: root = [1,3,null,null,2]
> Output: [3,1,null,null,2]
> Explanation: 3 cannot be a left child of 1 because 3 > 1. Swapping 1 and 3 makes the BST valid.
> ```
> 
> **Example 2:**
> ```
> Input: root = [3,1,4,null,null,2]
> Output: [2,1,4,null,null,3]
> Explanation: 2 cannot be in the right subtree of 3 because 2 < 3. Swapping 2 and 3 makes the BST valid.
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [2, 1000].
> - -2^{31} <= Node.val <= 2^{31} - 1

> [!info] Approach
> In an inorder traversal of a valid BST, values are strictly increasing. A swap creates at most two "inversions" (places where `prev > current`). The first node of the first inversion and the second node of the last inversion are the swapped pair. Inorder traversal (iterative or recursive). Track `prev`, `first_bad`, and `second_bad`. At each inversion (`prev.val > curr.val`): if `first_bad` is not set, set it to `prev`; always update `second_bad` to `curr`. After traversal, swap `first_bad.val` and `second_bad.val`.

> [!note]- Python Solution
> ```python
> def recover_tree(root):
>     first_bad = None
>     second_bad = None
>     prev = None
> >
>     def inorder(node):
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
> >
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
