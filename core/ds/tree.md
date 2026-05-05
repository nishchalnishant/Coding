# Tree — SDE-3 Gold Standard

Hierarchical structure: root, parent-child relationships, leaves. SDE-3 expects: all traversals (including O(1) space Morris), BST invariants, LCA derivation, Tree DP returning multiple values, and serialization.

---

## Theory & Mental Models

**What it is:** A connected acyclic graph with a designated root. Every node has exactly one parent (except the root). Binary tree: each node has at most 2 children. BST invariant: all values in left subtree < node.val < all values in right subtree (not just immediate children).

**Why it exists:** Solves the problem of representing and querying hierarchical data efficiently. Real-world analogy: a company org chart — the CEO is root, departments are subtrees, individual employees are leaves.

**Memory layout:** Nodes allocated individually on the heap, linked via left/right child pointers. No cache locality between nodes. Height h determines all operation costs — balanced: h = O(log N); skewed (worst case): h = O(N).

**Key invariants:**
- Every node has at most one parent; root has none.
- BST: left subtree values < node < right subtree values — this must hold globally, not just locally.
- Height of tree: max depth of any leaf. Determines worst-case recursion depth.
- Traversal order is fixed: inorder (L → node → R) gives sorted output for BST; preorder (node → L → R) for serialization; postorder (L → R → node) for Tree DP.

**Complexity at a glance:**

| Operation | Balanced BST | Skewed BST | Notes |
| :--- | :--- | :--- | :--- |
| Search | O(log N) | O(N) | Follow BST property |
| Insert | O(log N) | O(N) | Find position, link node |
| Delete | O(log N) | O(N) | Handle 3 cases (0/1/2 children) |
| Traversal | O(N) | O(N) | All nodes visited once |
| LCA | O(log N) BST | O(N) | O(N) for general binary tree |

**When to reach for it:**
- Hierarchical data representation (file systems, org charts, XML/JSON parsing).
- Sorted range queries, predecessor/successor lookups (BST).
- Path problems — max path sum, LCA, distance between nodes.
- Level-order / BFS problems where level structure matters.
- Serialization/deserialization of structured data.

**Common mistakes:**
- Confusing height and depth: height of a node = max edges to a leaf below it; depth = edges from root to that node.
- Forgetting null checks before accessing `node.left` or `node.right` in recursion.
- BST validation checking only immediate children (not global bounds) — always pass `(lo, hi)` range down.
- Returning single value from tree DP when two values are needed (e.g., rob/skip, gain/path).

---

## 1. Concept Overview

### When to Use Which Traversal

| Goal | Technique | Why |
| :--- | :--- | :--- |
| **Process children before parent** | Postorder / Bottom-Up | Parent state depends on children (Tree DP, diameter, height) |
| **Sorted order of BST** | Inorder | Left < Root < Right gives sorted sequence |
| **Level-by-level processing** | BFS with queue | Level order, zigzag, connect level pointers |
| **O(1) space traversal** | Morris (threaded) | Temporarily threads tree; restores structure |
| **Validate/range-check** | Preorder with bounds | Pass `(min, max)` range down to each node |

---

## 2. Core Algorithms & Click Moments

### Lowest Common Ancestor (LCA)

> [!IMPORTANT]
> **The Click Moment**: "Find the **common parent**" — OR — "**distance between two nodes** in a tree" — OR — "**lowest shared ancestor**". In a binary tree, recurse: if you find either target, return it up. If both sides return non-null, the current node is the LCA.

```python
def lowest_common_ancestor(root, p, q):
    if not root or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root  # p and q are on opposite sides — this node is LCA
    return left or right

def lca_bst(root, p, q):
    # BST: use the ordering property — no need to search both subtrees
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root  # they diverge here — root is LCA
```

> [!CAUTION]
> The binary tree LCA assumes `p` and `q` both exist in the tree. If they might not exist, you need a modified version that tracks a `found_count` and only returns the LCA when both are confirmed found.

#### Common Variants & Twists
1. **LCA of BST**:
   - **What (The Problem & Goal):** Find the LCA in a Binary Search Tree instead of a standard Binary Tree.
   - **How (Intuition & Mental Model):** Use the BST ordering property. If `p` and `q` are both smaller than the root, go left. If both are greater, go right. The exact moment they diverge (one is smaller, one is larger) or when one of them equals the root, you have found the LCA. No need to search both subtrees.
2. **LCA of Deepest Leaves**:
   - **What (The Problem & Goal):** Find the LCA of the deepest leaves in the tree.
   - **How (Intuition & Mental Model):** This requires comparing heights. Find the depth of the left and right children. If they are equal, it means the deepest leaves span both subtrees, so the root is the LCA. If the left is deeper, the LCA must reside strictly in the left subtree, so recurse left (and vice versa).

---

### Tree DP — Bottom-Up with Multiple Return Values

> [!IMPORTANT]
> **The Click Moment**: "Maximum/minimum **path sum** from any node to any node" — OR — "**diameter** of a tree" — OR — "**camera** coverage" — OR — any problem where the optimal solution through a node depends on both subtrees. The pattern: return a **tuple** of values from each DFS call instead of relying on a global variable per call.

```python
def max_path_sum(root) -> int:
    best = [float('-inf')]

    def dfs(node) -> int:
        if not node:
            return 0
        left_gain = max(0, dfs(node.left))   # take 0 if subtree is negative
        right_gain = max(0, dfs(node.right))
        # Update global best: path through this node
        best[0] = max(best[0], node.val + left_gain + right_gain)
        # Return the best single-branch gain for parent
        return node.val + max(left_gain, right_gain)

    dfs(root)
    return best[0]

def diameter_of_tree(root) -> int:
    diameter = [0]

    def height(node) -> int:
        if not node:
            return 0
        left = height(node.left)
        right = height(node.right)
        diameter[0] = max(diameter[0], left + right)
        return 1 + max(left, right)

    height(root)
    return diameter[0]
```

> [!TIP]
> **The paired-return pattern** (return `(include_node, exclude_node)`): when a parent's optimal decision depends on whether the child is included or not, return both options and let the parent pick. Used in House Robber III, Binary Tree Cameras, and weighted independent set on trees.

```python
def rob_house_tree(root) -> int:
    def dfs(node):
        if not node:
            return 0, 0  # (rob_this_node, skip_this_node)
        left_rob, left_skip = dfs(node.left)
        right_rob, right_skip = dfs(node.right)
        rob = node.val + left_skip + right_skip
        skip = max(left_rob, left_skip) + max(right_rob, right_skip)
        return rob, skip
    return max(dfs(root))
```

#### Common Variants & Twists
1. **Diameter of Binary Tree**:
   - **What (The Problem & Goal):** Find the length of the longest path between any two nodes in a tree (path may or may not pass through the root).
   - **How (Intuition & Mental Model):** The "edge-count" twist on path sum. Instead of values, you count edges. Return the height of a subtree to its parent (`1 + max(left, right)`). Update the global diameter variable with the path passing through the current node (`left + right`).
2. **Binary Tree Maximum Path Sum**:
   - **What (The Problem & Goal):** Find the maximum path sum between any two nodes. Values can be negative.
   - **How (Intuition & Mental Model):** The "negative value" twist. A path can stop at any point. You use `max(0, dfs(child))` to drop negative branches entirely. A node's contribution to its parent is `node.val + max(left_gain, right_gain)`, but the global maximum path sum passing *through* the node is `node.val + left_gain + right_gain`.
3. **Binary Tree Cameras**:
   - **What (The Problem & Goal):** Place the minimum number of cameras to monitor all nodes (a camera monitors itself, its parent, and its children).
   - **How (Intuition & Mental Model):** The "state machine" twist. Run a postorder traversal returning states from children to parents: 0 (needs camera), 1 (has camera), 2 (covered). Install cameras greedily at the parents of uncovered leaves.

---

### BST Operations — Validate, Kth Smallest, Range Sum

> [!IMPORTANT]
> **The Click Moment**: "**Validate BST**" — OR — "Kth **smallest/largest** in BST" — OR — "**Range sum** of BST values". The BST invariant (all left < node < all right, not just immediate children) is the source of most bugs.

```python
def is_valid_bst(root, lo=float('-inf'), hi=float('inf')) -> bool:
    if not root:
        return True
    if not (lo < root.val < hi):
        return False
    return (is_valid_bst(root.left, lo, root.val) and
            is_valid_bst(root.right, root.val, hi))

def kth_smallest_bst(root, k: int) -> int:
    # Iterative inorder to avoid O(N) recursion for large trees
    stack, node = [], root
    count = 0
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        count += 1
        if count == k:
            return node.val
        node = node.right
```

> [!CAUTION]
> **BST validation trap**: Checking only that `node.val > node.left.val and node.val < node.right.val` is **wrong**. A right child that is smaller than the root's parent but larger than the root passes the local check but violates the global BST property. Always pass `(min_bound, max_bound)` through the recursion.

---

### Morris Inorder Traversal — O(1) Space

> [!IMPORTANT]
> **The Click Moment**: "Traverse a BST **without extra space** (no stack, no recursion)" — OR — any tree traversal problem where the interviewer adds the constraint "O(1) auxiliary space". Morris threading temporarily mutates the tree and restores it — zero stack space.

```python
def morris_inorder(root) -> list[int]:
    result = []
    current = root
    while current:
        if not current.left:
            result.append(current.val)
            current = current.right
        else:
            # Find inorder predecessor
            predecessor = current.left
            while predecessor.right and predecessor.right is not current:
                predecessor = predecessor.right

            if not predecessor.right:
                # Thread: link predecessor back to current
                predecessor.right = current
                current = current.left
            else:
                # Unthread: restore tree structure; visit current
                predecessor.right = None
                result.append(current.val)
                current = current.right
    return result
```

---

### Iterative Postorder Traversal (1-Stack)

> [!IMPORTANT]
> **The Click Moment**: "Traverse tree **L → R → Root iteratively** using only one stack." — OR — "You must process children before the parent, but avoid recursion due to stack overflow." Postorder is the hardest iterative traversal because you reach the root twice (once before going right, once after) and only process it the second time. You need a `last_visited` pointer to know if you're returning from the right child.

```python
def iterative_postorder(root) -> list[int]:
    result = []
    stack = []
    curr = root
    last_visited = None
    
    while curr or stack:
        if curr:
            stack.append(curr)
            curr = curr.left
        else:
            peek_node = stack[-1]
            # If right child exists and hasn't been visited yet, go right
            if peek_node.right and last_visited is not peek_node.right:
                curr = peek_node.right
            else:
                # Both left and right are done; process node
                result.append(peek_node.val)
                last_visited = stack.pop()
    
    return result
```

> [!TIP]
> A common "cheat" for iterative postorder is the 2-stack approach: do an iterative preorder `Root → Right → Left` and reverse the output array. However, SDE-3 interviewers explicitly ban the reverse trick to test your state-machine logic. The 1-stack `last_visited` approach above is the true gold standard.

#### Common Variants & Twists
1. **Binary Tree Right Side View**:
   - **What (The Problem & Goal):** Return the values of the nodes you can see if you look at the tree from the right side.
   - **How (Intuition & Mental Model):** Not strictly postorder, but relies on traversal order twists. You can use Level-Order (BFS) and grab the last element of each level. Alternatively, use a Preorder DFS but intentionally traverse `Right` before `Left`, keeping track of the `depth` and appending to the result list only the first time you visit a new depth.

---

### Serialize and Deserialize

> [!IMPORTANT]
> **The Click Moment**: "Convert a tree to a **string** and back" — OR — "store/transmit a tree". Preorder with explicit `null` markers uniquely represents any binary tree (unlike inorder, which requires additional information for reconstruction).

```python
def serialize(root) -> str:
    if not root:
        return 'N'
    return f"{root.val},{serialize(root.left)},{serialize(root.right)}"

def deserialize(data: str):
    vals = iter(data.split(','))
    def build():
        val = next(vals)
        if val == 'N':
            return None
        node = TreeNode(int(val))
        node.left = build()
        node.right = build()
        return node
    return build()
```

---

## 3. SDE-3 Deep Dives

### Scalability: Balanced BSTs and Self-Balancing Trees

> [!TIP]
> A plain BST degrades to O(N) in the worst case (sorted insertions = linked list). Production systems use:
> - **AVL tree**: Strict height balance (|left - right| ≤ 1); O(log N) guaranteed; more rotations on insert.
> - **Red-Black tree**: Relaxed balance; O(log N) amortized; fewer rotations; used in Java's `TreeMap`, Linux kernel's task scheduler.
> - **B-tree / B+ tree**: Branching factor >> 2; optimized for disk I/O; used in all relational databases.
>
> At Google scale: sharded B-trees underlie Bigtable's SSTable format.

### Scalability: Parallel Tree Traversal

> [!TIP]
> Tree DFS is naturally parallelizable: left and right subtrees are independent. For very large trees (file systems, ASTs), use a thread pool where each task processes a subtree and submits children as new tasks. In Python, use `concurrent.futures.ThreadPoolExecutor` with a work queue seeded from the root.

### Concurrency: Lock-Free BST

> [!TIP]
> Lock-free concurrent BSTs use **CAS on child pointers**. The key insight: reads of child pointers are safe without locks (pointer reads are atomic on 64-bit systems); writes use CAS to atomically update a child pointer only if it hasn't changed. Used in Java's `ConcurrentSkipListMap` (skip list ≈ probabilistic balanced BST) for lock-free ordered map.

### Trade-offs

| Operation | Sorted Array | Hash Map | BST | Balanced BST |
| :--- | :--- | :--- | :--- | :--- |
| Search | O(log N) BS | O(1) | O(log N) avg | O(log N) |
| Insert | O(N) shift | O(1) amort | O(log N) avg | O(log N) |
| Delete | O(N) shift | O(1) amort | O(log N) avg | O(log N) |
| Range query | O(log N + K) | O(N) | O(log N + K) | O(log N + K) |
| In-order iteration | O(N) | O(N) unsorted | O(N) | O(N) |

---

## 4. Common Interview Problems

### Easy
- [Invert Binary Tree](../algo/problem-deep-dives.md#invert-binary-tree) — Swap children at each node; recursive or BFS.
- **Symmetric Tree** — Mirror check: `left.val == right.val` and recurse cross-ways.
- **Maximum Depth** — `1 + max(depth(left), depth(right))`.

### Medium
- [Validate BST](../algo/problem-deep-dives.md#validate-bst) — Pass `(min, max)` bounds down.
- [LCA of Binary Tree](../algo/problem-deep-dives.md#lca) — "Both sides non-null" = LCA found.
- [Kth Smallest in BST](../algo/problem-deep-dives.md#kth-smallest-in-bst) — Iterative inorder; stop at K.
- **Binary Tree Level Order** — BFS; separate levels by queue-size snapshot.
- **Diameter of Binary Tree** — Postorder height; update global `left + right`.
- **House Robber III** — Tree DP; return `(rob, skip)` pair.
- **Flatten Binary Tree to Linked List** — Morris-like threading; preorder rewiring.

### Hard
- [Serialize and Deserialize](../algo/problem-deep-dives.md#serialize-and-deserialize-binary-tree) — Preorder with `N` markers.
- [Binary Tree Max Path Sum](../algo/problem-deep-dives.md#binary-tree-maximum-path-sum) — Tree DP; `max(0, child)` to drop negatives.
- **Binary Tree Cameras** — Tree DP; 3 states per node: covered/has-camera/uncovered.
- **Recover BST** — Find two swapped nodes via inorder; `first` = node before first descent; `second` = last seen small node.
- **Vertical Order Traversal** — BFS with `(col, row, val)`; sort by col then row then val.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **[Validate BST](../algo/problem-deep-dives.md#validate-bst)** | DFS with Range Bounds | "All left < node, all right > node" | Pass `(lo, hi)` range recursively | Checking only immediate children misses global BST violation. |
| **[Max Path Sum](../algo/problem-deep-dives.md#binary-tree-maximum-path-sum)** | "Any-to-any path, max sum" | `max(0, child)` to cut negatives; update global via closure | Path can start/end at any node; distinguish "gain returned up" from "path through node". |
| **[LCA](../algo/problem-deep-dives.md#lca)** | "First node that sees both p and q below it" | `left and right` both non-null → current is LCA | For BST LCA: exploit ordering; no need to search both sides. |
| **[Kth Smallest](../algo/problem-deep-dives.md#kth-smallest-in-bst)** | "K-th in sorted BST order" | Iterative inorder; stop at count k | Recursive version risks stack overflow for skewed trees. |
| **Diameter** | "Longest path between any two nodes" | `height(left) + height(right)` at each node | Diameter doesn't have to pass through root; track global max. |
| **House Robber III** | "No adjacent nodes (parent-child), max sum" | Return `(rob_this, skip_this)` per node | Two values per node, not one — the novelty of tree DP. |
| **Serialize/Deserialize** | "Lossless tree → string → tree" | Preorder + `N` markers; use iterator for deserialize | Why preorder works: root first unambiguously determines left vs right subtrees. |
| **Morris Inorder** | "Inorder traversal without O(N) stack" | Thread predecessor.right → current; unthread on second visit | Temporarily mutates tree; restores on second pass — explain this explicitly. |
| **Recover BST** | "Two nodes swapped — find and fix" | Inorder gives one or two inversions | One inversion: adjacent swap (`first = prev, second = curr`); two inversions: `first` from first, `second` from second. |
| **Binary Tree Cameras** | "Minimum cameras to monitor all nodes" | Tree DP: 3 states — needs coverage, has camera, is covered | Greedy: install camera at parent of unmonitored leaf; process bottom-up. |
| **Invert Binary Tree** [E] | "Mirror the tree" | Swap left/right at every node (preorder) | Recursive one-liner; iterative uses a queue — BFS or DFS both work identically. |
| **Symmetric Tree** [E] | "Is tree a mirror of itself?" | Compare left-subtree and right-subtree simultaneously (two-pointer recursion) | Check `left.val == right.val` AND recurse `(left.left, right.right)` AND `(left.right, right.left)`. |
| **Path Sum** [E] | "Root-to-leaf path summing to target" | DFS; subtract node value from target; return True at leaf when target == 0 | Leaf check: `not node.left and not node.right` — not just `target == 0` (could be mid-path). |
| **Count Good Nodes** [M] | "Nodes ≥ all ancestors on its root path" | DFS with `max_so_far`; increment count at each node ≥ max | Pass updated max downward; root is always good. |
| **Binary Tree Level Order Traversal** [M] | "BFS layer by layer" | Deque; snapshot `len(queue)` at start of each level; process exactly that many | Snapshot length before inner loop — queue grows during processing. |
| **Construct Binary Tree from Preorder and Inorder** [M] | "Rebuild tree from two traversals" | Root = preorder[0]; split inorder at root index; recurse left/right | Hash `inorder` values → index for O(1) split. Preorder index advances globally via nonlocal/outer variable. |
| **Populating Next Right Pointers** [M] | "Connect level nodes with next pointer" | BFS or O(1) space: use already-connected `next` pointers of the level above | O(1) space trick: process level N using the `next` chain of level N-1 — no queue needed. |
| **Flatten Binary Tree to Linked List** [M] | "In-place preorder flattening" | Morris-like: connect right subtree after leftmost rightmost; move left to right | O(1) space: for each node, thread its right subtree to end of left subtree's rightmost chain. |
| **All Nodes Distance K in Binary Tree** [M] | "All nodes exactly K edges from target" | Build parent map (BFS); then BFS from target with visited set | Convert tree to undirected graph via parent map — enables upward traversal. |
| **Vertical Order Traversal** [H] | "Nodes grouped by column, sorted by row then value" | BFS/DFS with `(col, row, val)`; sort globally or per-column | Multiple nodes at same `(col, row)` must be sorted by value — a common missed case. |
| **Binary Tree Maximum Path Sum** [H] | "Max sum path (any node to any node)" | Post-order; at each node compute max one-arm gain; update global with both arms | Return single-arm to parent (max of left/right arm + node); update global with `node + left + right`. Drop negative arms (use 0 instead). |

---

## Quick Revision Triggers

- If the problem says "validate BST" → think Range Propagation; pass `(lo, hi)` bounds through recursion, not just local child comparison.
- If the problem says "lowest common ancestor" → think Postorder DFS; if both sides return non-null, current node is LCA.
- If the problem says "diameter" or "maximum path sum" → think Tree DP with global variable; return single-arm gain to parent, update global with both arms at each node.
- If the problem says "K-th smallest in BST" → think Iterative Inorder; stop after K pops to avoid O(N) stack for large skewed trees.
- If the problem says "serialize/deserialize tree" → think Preorder with explicit `None` markers; inorder alone is insufficient for reconstruction.
- If the problem says "O(1) space traversal" → think Morris Threading; temporarily link predecessor back to current, restore on second visit.
- If the problem says "level-order" or "connect level pointers" → think BFS with `len(queue)` snapshot per level.

## See also

- [Graph](../algorithms/graph.md) — trees are acyclic connected graphs; BFS/DFS apply
- [Dynamic Programming](../algorithms/dynamic-programming/README.md) — Tree DP (postorder state propagation)
- [Backtracking](../algorithms/backtracking.md) — path sum with backtracking
- [Patterns Master](../../../reference/patterns/patterns-master.md) — tree traversal pattern triggers
