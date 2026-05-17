# Tree Recursion — Advanced Patterns

Advanced structural recursion on binary trees and BSTs. For the recursion foundation see [README.md](README.md).

---

## Theory — Designing the Return Value

The most important decision in tree recursion is **what the recursive function returns**. Three patterns:

| Return Style | Use When | Example |
| :--- | :--- | :--- |
| **Single value** | Answer at a node is determined by children's values | Max depth, sum, count nodes |
| **Tuple / pair** | Node needs to report two independent quantities to parent | House Robber III `(rob, skip)`, BST validation `(min, max, is_valid)` |
| **Global + local** | Answer crosses multiple subtrees (can't be returned up cleanly) | Diameter, Max Path Sum, any "path through node" problem |

> [!IMPORTANT]
> **Design the return type before writing a single line of code.** Getting this wrong leads to complex rewrites. Ask: "What does the parent need from its child to compute its own answer?"

---

## Part 1 — Path Problems

### 1.1 Path Sum I — Does a Root-to-Leaf Path Exist? (LC 112)

```python
def has_path_sum(root, target: int) -> bool:
    if not root: return False
    if not root.left and not root.right:
        return root.val == target
    remaining = target - root.val
    return has_path_sum(root.left, remaining) or has_path_sum(root.right, remaining)
```

### 1.2 Path Sum II — All Root-to-Leaf Paths with Target Sum (LC 113)

```python
def path_sum(root, target: int) -> list[list[int]]:
    result = []

    def dfs(node, remaining, path):
        if not node: return
        path.append(node.val)
        if not node.left and not node.right and remaining == node.val:
            result.append(path[:])   # snapshot — NOT path itself
        dfs(node.left, remaining - node.val, path)
        dfs(node.right, remaining - node.val, path)
        path.pop()                   # backtrack

    dfs(root, target, [])
    return result
```

> [!CAUTION]
> Always snapshot `path[:]` before appending to `result`. Appending `path` directly records a reference — all entries will reflect the final (empty) state of path after backtracking.

### 1.3 Path Sum III — Count Paths Summing to Target (Any Start/End) (LC 437)

```python
from collections import defaultdict

def path_sum_iii(root, target: int) -> int:
    prefix_count = defaultdict(int)
    prefix_count[0] = 1   # empty path prefix
    count = [0]

    def dfs(node, running_sum):
        if not node: return
        running_sum += node.val
        count[0] += prefix_count[running_sum - target]
        prefix_count[running_sum] += 1
        dfs(node.left, running_sum)
        dfs(node.right, running_sum)
        prefix_count[running_sum] -= 1   # backtrack prefix count

    dfs(root, 0)
    return count[0]
```

> [!TIP]
> **Prefix sum technique on trees:** `prefix_count[curr - target]` counts paths ending at the current node whose sum equals target. Decrement the prefix count on return to undo — same as how you'd undo in backtracking.

### 1.4 Maximum Path Sum (LC 124)

```python
def max_path_sum(root) -> int:
    best = [float('-inf')]

    def gain(node) -> int:
        if not node: return 0
        left  = max(gain(node.left),  0)   # clip negatives
        right = max(gain(node.right), 0)
        best[0] = max(best[0], node.val + left + right)  # path through node
        return node.val + max(left, right)               # single arm up

    gain(root)
    return best[0]
```

---

## Part 2 — BST Recursion

### 2.1 Validate BST (LC 98)

**Return type:** Pass valid range `(min_val, max_val)` down; return bool up.

```python
def is_valid_bst(root) -> bool:
    def validate(node, lo, hi):
        if not node: return True
        if not (lo < node.val < hi): return False
        return (validate(node.left, lo, node.val) and
                validate(node.right, node.val, hi))
    return validate(root, float('-inf'), float('inf'))
```

> [!CAUTION]
> Pass down the **valid range** `(lo, hi)` — do NOT just check `node.val > node.left.val`. That only catches immediate parent-child violations, not cross-subtree violations. BST rule applies to ALL ancestors.

### 2.2 BST Insert (LC 701)

```python
def insert_into_bst(root, val: int):
    if not root:
        from dataclasses import dataclass
        # Return new node (assume TreeNode class exists)
        return TreeNode(val)
    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    else:
        root.right = insert_into_bst(root.right, val)
    return root
```

### 2.3 BST Delete (LC 450)

```python
def delete_node(root, key: int):
    if not root: return None
    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        # Node to delete found
        if not root.left: return root.right
        if not root.right: return root.left
        # Has both children: replace with inorder successor (min of right subtree)
        successor = root.right
        while successor.left:
            successor = successor.left
        root.val = successor.val
        root.right = delete_node(root.right, successor.val)
    return root
```

### 2.4 Kth Smallest in BST (LC 230)

```python
def kth_smallest(root, k: int) -> int:
    count = [0]
    result = [None]

    def inorder(node):
        if not node or result[0] is not None: return
        inorder(node.left)
        count[0] += 1
        if count[0] == k:
            result[0] = node.val
            return
        inorder(node.right)

    inorder(root)
    return result[0]
```

### 2.5 Convert Sorted Array to BST (LC 108)

```python
def sorted_array_to_bst(nums: list[int]):
    if not nums: return None
    mid = len(nums) // 2
    node = TreeNode(nums[mid])
    node.left  = sorted_array_to_bst(nums[:mid])
    node.right = sorted_array_to_bst(nums[mid+1:])
    return node
```

### 2.6 Lowest Common Ancestor — BST (LC 235)

```python
def lca_bst(root, p, q):
    if p.val < root.val and q.val < root.val:
        return lca_bst(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        return lca_bst(root.right, p, q)
    return root   # divergence point = LCA
```

### 2.7 Lowest Common Ancestor — General Binary Tree (LC 236)

```python
def lca_tree(root, p, q):
    if not root or root == p or root == q:
        return root
    left  = lca_tree(root.left,  p, q)
    right = lca_tree(root.right, p, q)
    if left and right:
        return root   # p and q split across children → root is LCA
    return left or right
```

> [!TIP]
> **LCA logic:** If both `left` and `right` are non-null, the current node is the LCA — p is in one subtree, q in the other. If only one is non-null, that subtree contains both p and q, so return the non-null side.

---

## Part 3 — Tree Structure Problems

### 3.1 Serialize and Deserialize Binary Tree (LC 297)

```python
class Codec:
    def serialize(self, root) -> str:
        def preorder(node):
            if not node: return ['#']
            return [str(node.val)] + preorder(node.left) + preorder(node.right)
        return ','.join(preorder(root))

    def deserialize(self, data: str):
        tokens = iter(data.split(','))

        def build():
            val = next(tokens)
            if val == '#': return None
            node = TreeNode(int(val))
            node.left  = build()
            node.right = build()
            return node

        return build()
```

> [!TIP]
> Using `iter()` on the token list lets you consume tokens sequentially across recursive calls without passing an index. Each call to `next(tokens)` advances the global iterator.

### 3.2 Flatten Binary Tree to Linked List (LC 114)

```python
def flatten(root) -> None:
    """Flattens tree in-place to preorder linked list (using right pointers)."""
    def dfs(node):
        if not node: return None   # returns the tail of flattened subtree
        if not node.left and not node.right:
            return node            # leaf is its own tail

        left_tail  = dfs(node.left)
        right_tail = dfs(node.right)

        if left_tail:
            left_tail.right = node.right   # connect left's tail to right subtree
            node.right = node.left         # move left subtree to right
            node.left  = None

        return right_tail or left_tail     # rightmost tail

    dfs(root)
```

### 3.3 Symmetric Tree (LC 101)

```python
def is_symmetric(root) -> bool:
    def mirror(left, right) -> bool:
        if not left and not right: return True
        if not left or not right:  return False
        return (left.val == right.val and
                mirror(left.left, right.right) and
                mirror(left.right, right.left))
    return mirror(root.left, root.right)
```

### 3.4 Count Complete Tree Nodes (LC 222)

```python
def count_nodes(root) -> int:
    if not root: return 0
    # Measure left and right height by always going left/right respectively
    lh = rh = 0
    left, right = root, root
    while left:  lh += 1; left  = left.left
    while right: rh += 1; right = right.right
    if lh == rh:
        return (1 << lh) - 1   # perfect binary tree: 2^h - 1
    # Otherwise recurse (still O(log² N))
    return 1 + count_nodes(root.left) + count_nodes(root.right)
```

> [!TIP]
> The O(log² N) trick: if left height equals right height, the left subtree is a perfect binary tree. Count it in O(1) with `2^lh - 1`. Only recurse when heights differ. Each level halves the problem → O(log N) levels × O(log N) height calculation = O(log² N).

---

## Part 4 — Return Value Design Patterns

### 4.1 House Robber III — Tuple Return (LC 337)

```python
def rob(root) -> int:
    def dfs(node):
        if not node: return 0, 0   # (rob_this, skip_this)
        l_rob, l_skip = dfs(node.left)
        r_rob, r_skip = dfs(node.right)
        rob_this  = node.val + l_skip + r_skip
        skip_this = max(l_rob, l_skip) + max(r_rob, r_skip)
        return rob_this, skip_this
    return max(dfs(root))
```

### 4.2 Largest BST Subtree — Tuple Return (LC 333)

```python
def largest_bst_subtree(root) -> int:
    best = [0]

    def dfs(node):
        """Returns (is_bst, size, min_val, max_val)"""
        if not node: return True, 0, float('inf'), float('-inf')
        l_bst, l_size, l_min, l_max = dfs(node.left)
        r_bst, r_size, r_min, r_max = dfs(node.right)

        if (l_bst and r_bst and
                l_max < node.val < r_min):
            size = l_size + 1 + r_size
            best[0] = max(best[0], size)
            return True, size, min(l_min, node.val), max(r_max, node.val)
        return False, 0, 0, 0

    dfs(root)
    return best[0]
```

---

## Interview Questions — Logic & Trickiness

| Problem | LC # | Return Design | Click Moment | Gotcha |
| :--- | :--- | :--- | :--- | :--- |
| **Path Sum I** | 112 | `bool` | Reduce target by `node.val` each level | Leaf check: `not left AND not right` |
| **Path Sum II** | 113 | void + closure | Backtrack: `path.pop()` on return | Must snapshot `path[:]` not `path` |
| **Path Sum III** | 437 | count via prefix sum | `prefix_count[curr - target]` | Undo prefix count on return |
| **Max Path Sum** | 124 | int (single arm) | Clip negatives: `max(gain(...), 0)` | Update global inside recursion; return single arm up |
| **Validate BST** | 98 | `bool` | Pass valid `(lo, hi)` range down | Don't just check immediate parent — check full ancestry |
| **BST Insert** | 701 | node (updated tree) | Recurse left/right; connect returned node | Return root at end for clean reassignment |
| **BST Delete** | 450 | node (updated tree) | Find inorder successor (min of right subtree) | Replace value, then delete successor node |
| **LCA BST** | 235 | node | Divergence = both < root or both > root | Use val comparisons with BST property |
| **LCA General** | 236 | node | Both non-null returns → current is LCA | `root == p or root == q` → return root immediately |
| **Serialize/Deserialize** | 297 | string/node | Use `iter()` for stateful token consumption | Sentinel `'#'` for nulls; preorder ensures structure |
| **Flatten Tree** | 114 | tail node | Connect left tail to right; move left to right | Return `right_tail or left_tail` |
| **Symmetric Tree** | 101 | `bool` | Mirror check: `left.left == right.right` | Both null → True; one null → False |
| **Count Complete Nodes** | 222 | int | Perfect subtree shortcut: `2^h - 1` | Check by going always-left and always-right |
| **House Robber III** | 337 | `(rob, skip)` tuple | Parent: rob=val+skip_children; skip=max(child) | Return pair; don't lose the choice info |
| **Kth Smallest BST** | 230 | int via closure | Inorder = sorted BST; count k steps | Short-circuit after finding kth element |

---

## See also

- [README.md](README.md) — Structural recursion theory
- [aditya-verma.md](aditya-verma.md) — Pattern 6: Tree DFS
- [graph-recursion.md](graph-recursion.md) — DFS on graphs
- [questions-bank.md](questions-bank.md) — Tiered drill problems
