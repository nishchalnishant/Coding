---
module: 01-data-structures
topic: Tree
subtopic: 
status: unread
tags: [data-structures, tree]
---

← [Data structures index](./README.md) · [DS decision tree](./ds_tree.md)
## First-Principles Map

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: This file is core Tier 2 material. Know patterns cold; skip niche edge cases.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Conceptual awareness only.


```
WHY trees exist → WHAT they are → HOW they work → WHEN to use → WHAT can go wrong
       │                │                │               │               │
  [Hierarchical data  [acyclic           [BST: left <    [file systems,  [unbalanced BST
   can't be stored     connected graph;   root < right;   expression     degrades to O(n)
   in flat arrays;     parent has 0+      traversal:      trees, DOM,     linked list;
   sorted search       children; nodes    in/pre/post     autocomplete,   off-by-one in
   needs O(log n)      form a rooted      order; height   sorted sets,    recursion base
   insert+lookup]      hierarchy]         determines      priority queue] cases]
       │                │                │
  [real-world:        [invariant        [BST ops O(h): h=log n balanced,
   org chart —         (BST): for every   h=n worst; AVL/Red-Black
   CEO → VP → Mgr]    node x: all left   keep h=O(log n) via rotations;
                       subtree < x.val    n-ary tree BFS uses queue,
                       < all right]       DFS uses stack/recursion]
       ↓
[Decision: Tree vs alternatives]
  ├── vs HashMap      → tree supports range queries + ordered iteration; hash O(1) exact
  ├── vs Heap         → heap O(1) min/max but no search; BST O(log n) all ops + order
  └── vs Trie         → trie for string prefix; BST for ordered comparable keys
```

## First-Principles Breakdown
- **Root problem**: Flat structures can't represent hierarchy; sorted arrays pay O(n) for insert to maintain order.
- **Core insight**: BST invariant (left < root < right) halves the search space at every node — O(log n) search without rebuilding.
- **Invariant**: In a BST, every node's left subtree contains only smaller values and right subtree only larger values.
- **Why it's fast**: A balanced tree of n nodes has height log₂n — binary search through levels, touching only log n nodes per operation.
- **Where it breaks**: Without balancing (AVL/RB), repeated sorted insertions produce a O(n)-height linked list; recursion depth can overflow call stack on skewed trees.

# Tree — L3 Core

```
[TREE]
├── WHY IT EXISTS
│   ├── Problem it solves: represent hierarchical relationships (file systems, DOM, org charts, syntax)
│   ├── Without it: flat arrays/lists cannot express parent-child containment efficiently
│   └── Real-world analogy: company org chart — CEO at root, each node owns its subtree
├── WHAT IT IS (First Principles)
│   ├── Core property: connected, acyclic graph with a designated root
│   ├── Every non-root node has exactly ONE parent → no cycles, no ambiguity
│   ├── Binary tree: each node has at most 2 children (left, right)
│   ├── BST invariant: left subtree values < node.val < right subtree values (ALL descendants, not just direct children)
│   ├── Height h: longest root-to-leaf path; balanced tree h = O(log N)
│   └── Memory model: nodes allocated on heap; each node stores value + child pointers
├── HOW IT WORKS
│   ├── Traversals (DFS)
│   │   ├── Inorder (L → Root → R): produces sorted sequence in BST
│   │   ├── Preorder (Root → L → R): serialization, tree copy
│   │   ├── Postorder (L → R → Root): deletion, subtree aggregation (Tree DP)
│   │   └── Morris traversal: O(1) space inorder using threaded pointers
│   ├── BFS (level-order): queue-based, processes nodes level by level
│   ├── BST operations: search/insert/delete all O(h); O(log N) balanced, O(N) skewed
│   ├── LCA (Lowest Common Ancestor)
│   │   ├── Naive: O(N) per query via ancestor sets
│   │   ├── Binary lifting: O(N log N) build, O(log N) per query
│   │   └── Euler tour + RMQ: O(N log N) build, O(1) per query
│   ├── Tree DP: post-order aggregation returning tuple of values per node
│   │   └── Pattern: solve subtree → combine children → return to parent
│   └── Serialization: preorder + null markers → unique reconstruction
├── SELF-BALANCING VARIANTS
│   ├── AVL: strict |balance_factor| ≤ 1, O(log N) guaranteed; more rotations
│   ├── Red-Black: looser balance, O(log N) amortized; fewer rotations (used in std::map, TreeMap)
│   ├── B-Tree: wide branching, disk-friendly, used in databases/filesystems
│   └── Segment Tree / Fenwick: range query/update trees (see separate files)
├── COMPLEXITY
│   ├── Time — BST search/insert/delete: O(log N) balanced, O(N) worst (skewed)
│   ├── Time — traversal (all nodes): O(N)
│   ├── Time — LCA (binary lifting): O(log N) query after O(N log N) build
│   └── Space: O(N) nodes + O(h) recursion stack; Morris = O(1) stack
└── WHEN TO USE vs ALTERNATIVES
    ├── Use BST when: sorted order + O(log N) search/insert/delete
    ├── Use heap when: only need min/max repeatedly (not full sorted order)
    ├── Use trie when: prefix-based string lookup
    ├── Use graph when: multiple parents or cycles are possible
    └── Avoid unbalanced BST: degenerates to O(N) linked list on sorted input
```

Hierarchical structure: root, parent-child relationships, leaves. L3 expects: all traversals (including O(1) space Morris), BST invariants, LCA derivation, Tree DP returning multiple values, and serialization.




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

> [!TIP]
> Think of LCA as finding the closest common ancestor in a family tree — the first person who is an ancestor of both people you are looking for. In code: when recursion returns a non-null result from both the left and the right subtree, the current node is exactly that common ancestor — both targets were found on opposite sides.

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
> **The Click Moment**: "Maximum/minimum **path sum `🎯 T2`** from any node to any node" — OR — "**diameter `🎯 T2`** of a tree" — OR — "**camera** coverage" — OR — any problem where the optimal solution through a node depends on both subtrees. The pattern: return a **tuple** of values from each DFS call instead of relying on a global variable per call.

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
1. **Diameter of Binary Tree `🎯 T2`**:
   - **What (The Problem & Goal):** Find the length of the longest path between any two nodes in a tree (path may or may not pass through the root).
   - **How (Intuition & Mental Model):** The "edge-count" twist on path sum. Instead of values, you count edges. Return the height of a subtree to its parent (`1 + max(left, right)`). Update the global diameter variable with the path passing through the current node (`left + right`).
2. **Binary Tree Maximum Path Sum `🎯 T2`**:
   - **What (The Problem & Goal):** Find the maximum path sum between any two nodes. Values can be negative.
   - **How (Intuition & Mental Model):** The "negative value" twist. A path can stop at any point. You use `max(0, dfs(child))` to drop negative branches entirely. A node's contribution to its parent is `node.val + max(left_gain, right_gain)`, but the global maximum path sum passing *through* the node is `node.val + left_gain + right_gain`.
3. **Binary Tree Cameras `🎯 T2`**:
   - **What (The Problem & Goal):** Place the minimum number of cameras to monitor all nodes (a camera monitors itself, its parent, and its children).
   - **How (Intuition & Mental Model):** The "state machine" twist. Run a postorder traversal returning states from children to parents: 0 (needs camera), 1 (has camera), 2 (covered). Install cameras greedily at the parents of uncovered leaves.

---

### BST Operations — Validate, Kth Smallest, Range Sum

> [!IMPORTANT]
> **The Click Moment**: "**Validate BST `🎯 T2`**" — OR — "Kth **smallest/largest** in BST" — OR — "**Range sum of BST values** (Segment Tree for dynamic: L4+)". The BST invariant (all left < node < all right, not just immediate children) is the source of most bugs.

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
    return result
```

---

### Morris Preorder Traversal — O(1) Space

> [!IMPORTANT]
> **The Click Moment**: Same as Morris Inorder, but you need **Preorder (Root → Left → Right)** order with O(1) auxiliary space. The only difference is the exact moment of visiting a node: we record the node's value the first time we establish a threaded link (before entering its left child), rather than on backtrack.

```python
def morris_preorder(root) -> list[int]:
    """
    Performs a preorder tree traversal in O(N) time and O(1) auxiliary space.
    Mutates pointers temporarily and restores them on backtrack.
    """
    result = []
    curr = root
    while curr:
        if not curr.left:
            result.append(curr.val)  # Visit node with no left subtree
            curr = curr.right
        else:
            # Find the inorder predecessor (rightmost node in left subtree)
            pre = curr.left
            while pre.right and pre.right is not curr:
                pre = pre.right
            
            if not pre.right:
                # Threading: Point predecessor's right to current
                pre.right = curr
                result.append(curr.val)  # Preorder visit: visit before going left!
                curr = curr.left
            else:
                # Unthreading: Restore the original tree structure
                pre.right = None
                curr = curr.right
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
> A common "cheat" for iterative postorder is the 2-stack approach: do an iterative preorder `Root → Right → Left` and reverse the output array. However, L3 interviewers explicitly ban the reverse trick to test your state-machine logic. The 1-stack `last_visited` approach above is the true gold standard.

#### Common Variants & Twists
1. **Binary Tree Right Side View `🎯 T2`**:
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

## 3. Production Context (L3 Note)

> [!NOTE]
> Distributed systems details (consistent hashing, lock-free structures, bloom filters, skip lists, etc.) are **L3+ system design** topics. For Google L3 coding interviews, focus on the patterns in sections 1–2 and the interview problems below.

---

## 4. Common Interview Problems

### Easy
- Invert Binary Tree — Swap children at each node; recursive or BFS.
- **Symmetric Tree `🎯 T2`** — Mirror check: `left.val == right.val` and recurse cross-ways.
- **Maximum Depth `🎯 T2`** — `1 + max(depth(left), depth(right))`.

### Medium
- Validate BST — Pass `(min, max)` bounds down.
- LCA of Binary Tree — "Both sides non-null" = LCA found.
- Kth Smallest in BST — Iterative inorder; stop at K.
- **Binary Tree Level Order `🎯 T2`** — BFS; separate levels by queue-size snapshot.
- **Diameter of Binary Tree `🎯 T2`** — Postorder height; update global `left + right`.
- **House Robber III `🎯 T2`** — Tree DP; return `(rob, skip)` pair.
- **Flatten Binary Tree to Linked List `🎯 T2`** — Morris-like threading; preorder rewiring.

### Hard
- Serialize and Deserialize — Preorder with `N` markers.
- Binary Tree Max Path Sum — Tree DP; `max(0, child)` to drop negatives.
- **Binary Tree Cameras `🎯 T2`** — Tree DP; 3 states per node: covered/has-camera/uncovered.
- **Recover BST `🎯 T2`** — Find two swapped nodes via inorder; `first` = node before first descent; `second` = last seen small node.
- **Vertical Order Traversal `🎯 T2`** — BFS with `(col, row, val)`; sort by col then row then val.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **Validate BST `🎯 T2`** | DFS with Range Bounds | "All left < node, all right > node" | Pass `(lo, hi)` range recursively | Checking only immediate children misses global BST violation. |
| **Max Path Sum `🎯 T2`** | "Any-to-any path, max sum" | `max(0, child)` to cut negatives; update global via closure | Path can start/end at any node; distinguish "gain returned up" from "path through node". |
| **LCA `🎯 T2`** | "First node that sees both p and q below it" | `left and right` both non-null → current is LCA | For BST LCA: exploit ordering; no need to search both sides. |
| **Kth Smallest `🎯 T2`** | "K-th in sorted BST order" | Iterative inorder; stop at count k | Recursive version risks stack overflow for skewed trees. |
| **Diameter `🎯 T2`** | "Longest path between any two nodes" | `height(left) + height(right)` at each node | Diameter doesn't have to pass through root; track global max. |
| **House Robber III `🎯 T2`** | "No adjacent nodes (parent-child), max sum" | Return `(rob_this, skip_this)` per node | Two values per node, not one — the novelty of tree DP. |
| **Serialize/Deserialize** | "Lossless tree → string → tree" | Preorder + `N` markers; use iterator for deserialize | Why preorder works: root first unambiguously determines left vs right subtrees. |
| **Morris Inorder** | "Inorder traversal without O(N) stack" | Thread predecessor.right → current; unthread on second visit | Temporarily mutates tree; restores on second pass — explain this explicitly. |
| **Recover BST `🎯 T2`** | "Two nodes swapped — find and fix" | Inorder gives one or two inversions | One inversion: adjacent swap (`first = prev, second = curr`); two inversions: `first` from first, `second` from second. |
| **Binary Tree Cameras `🎯 T2`** | "Minimum cameras to monitor all nodes" | Tree DP: 3 states — needs coverage, has camera, is covered | Greedy: install camera at parent of unmonitored leaf; process bottom-up. |
| **Invert Binary Tree `🎯 T2`** [E] | "Mirror the tree" | Swap left/right at every node (preorder) | Recursive one-liner; iterative uses a queue — BFS or DFS both work identically. |
| **Symmetric Tree `🎯 T2`** [E] | "Is tree a mirror of itself?" | Compare left-subtree and right-subtree simultaneously (two-pointer recursion) | Check `left.val == right.val` AND recurse `(left.left, right.right)` AND `(left.right, right.left)`. |
| **Path Sum `🎯 T2`** [E] | "Root-to-leaf path summing to target" | DFS; subtract node value from target; return True at leaf when target == 0 | Leaf check: `not node.left and not node.right` — not just `target == 0` (could be mid-path). |
| **Count Good Nodes `🎯 T2`** [M] | "Nodes ≥ all ancestors on its root path" | DFS with `max_so_far`; increment count at each node ≥ max | Pass updated max downward; root is always good. |
| **Binary Tree Level Order Traversal `🎯 T2`** [M] | "BFS layer by layer" | Deque; snapshot `len(queue)` at start of each level; process exactly that many | Snapshot length before inner loop — queue grows during processing. |
| **Construct Binary Tree from Preorder and Inorder `🎯 T2`** [M] | "Rebuild tree from two traversals" | Root = preorder[0]; split inorder at root index; recurse left/right | Hash `inorder` values → index for O(1) split. Preorder index advances globally via nonlocal/outer variable. |
| **Populating Next Right Pointers `🎯 T2`** [M] | "Connect level nodes with next pointer" | BFS or O(1) space: use already-connected `next` pointers of the level above | O(1) space trick: process level N using the `next` chain of level N-1 — no queue needed. |
| **Flatten Binary Tree to Linked List `🎯 T2`** [M] | "In-place preorder flattening" | Morris-like: connect right subtree after leftmost rightmost; move left to right | O(1) space: for each node, thread its right subtree to end of left subtree's rightmost chain. |
| **All Nodes Distance K in Binary Tree `🎯 T2`** [M] | "All nodes exactly K edges from target" | Build parent map (BFS); then BFS from target with visited set | Convert tree to undirected graph via parent map — enables upward traversal. |
| **Vertical Order Traversal `🎯 T2`** [H] | "Nodes grouped by column, sorted by row then value" | BFS/DFS with `(col, row, val)`; sort globally or per-column | Multiple nodes at same `(col, row)` must be sorted by value — a common missed case. |
| **Binary Tree Maximum Path Sum `🎯 T2`** [H] | "Max sum path (any node to any node)" | Post-order; at each node compute max one-arm gain; update global with both arms | Return single-arm to parent (max of left/right arm + node); update global with `node + left + right`. Drop negative arms (use 0 instead). |
| **Step-By-Step Directions** [M] | LCA Path Generation | "Shortest path from start node to dest node" | Find LCA. Generate path LCA → start (convert all to 'U') and LCA → dest ('L'/'R'); concatenate | Both paths go through LCA; generating full paths from root and trimming common prefix is simpler than post-order traversal. |
| **Path Sum III `🎯 T2`** [M] | DFS Prefix Sum Map | "Paths summing to target, not starting at root" | Running prefix sum DFS; look up `curr_sum - target` in complement count map; backtrack map on return | Must decrement `prefix_sum` count in map after child recursion to prevent leak into other branches. |

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

- [Graph](../02-algorithms/13-graph.md) — trees are acyclic connected graphs; BFS/DFS apply
- [Dynamic Programming](../02-algorithms/15-dynamic-programming.md) — Tree DP (postorder state propagation)
- [Backtracking](../02-algorithms/12-backtracking.md) — path sum with backtracking
- [Patterns Master](../03-patterns/patterns-master.md) — tree traversal pattern triggers

## Flashcards

**Why does validating a BST require range propagation rather than just comparing parent to immediate children?** #flashcard
A BST node must be greater than *all* nodes in its left subtree and smaller than *all* nodes in its right subtree, not just its immediate children. Range propagation passes `(lo, hi)` bounds down through recursion: `(lo, node.val)` for left, and `(node.val, hi)` for right, ensuring global validity.

**How does Morris Traversal achieve O(1) space tree traversal?** #flashcard
By utilizing temporary threads. For each `current` node, if it has a left child, find its inorder predecessor (rightmost node of the left subtree):
- If `predecessor.right` is `None`, set `predecessor.right = current` (thread created), move `current = current.left`.
- If `predecessor.right` is `current`, restore `predecessor.right = None` (thread cut), visit `current`, move `current = current.right`.

**Describe the postorder DFS logic for finding the Lowest Common Ancestor (LCA) of nodes P and Q in a binary tree.** #flashcard
- If the current node is `None` or matches `P` or `Q`, return `current`.
- Recurse left and right: `left_res = dfs(node.left)`, `right_res = dfs(node.right)`.
- If both `left_res` and `right_res` are non-null, the current node is the LCA.
- If only one is non-null, return that non-null result (propagates the found target upward).

**How do you calculate the maximum path sum in a binary tree (paths can start/end anywhere)?** #flashcard
Use Tree DP with a global max tracker. At each node:
1. Recursively compute maximum single-arm gains: `left = max(0, dfs(node.left))` and `right = max(0, dfs(node.right))`.
2. Update the global max with `node.val + left + right`.
3. Return the maximum single-arm path to the parent: `node.val + max(left, right)`.

**Why is preorder/postorder traversal with null markers preferred over inorder traversal for tree serialization?** #flashcard
Inorder traversal is not unique; multiple distinct trees can produce the same inorder sequence, even with null markers. Preorder or postorder traversal with null markers records structural parent-child relationships uniquely, allowing unambiguous reconstruction.

