# Tree — SDE-3 Level

Hierarchical structure: root, parent-child, leaves. SDE-3 expects traversals, BST invariants, LCA, tree DP (return multiple values), and when to use recursion vs iteration.

---

## 1. Concept Overview

**Problem space**: Traversals (pre/in/post/level), path sum, diameter, LCA, BST (validate, kth smallest, range queries), serialize/deserialize, max path sum (tree DP).

**When to use**: Recursion for "subtree returns value"; tree DP when node needs info from children (e.g., max path through node = left + right + node); BST → inorder gives sorted order.

---

## 2. Core Algorithms

### Traversals
- **Preorder** (Root, Left, Right): Copy/serialize, prefix expression.
- **Inorder** (Left, Root, Right): BST sorted order; validate BST (inorder must be strictly increasing).
- **Postorder** (Left, Right, Root): Delete subtree; tree DP (children before parent).
- **Level-order**: BFS with queue; right-side view = last node per level.

### LCA
- **BST**: If both p,q < root → LCA in left; both > root → right; else root.
- **Binary tree**: Recursive: if root is p or q or null return root; left=LCA(left), right=LCA(right); if both non-null return root else return non-null.

### Tree DP (e.g., Max Path Sum)
- Return (max path ending at node, global max). Path ending at node = node + max(0, left) + max(0, right); global = max(global, path_through_node). Postorder.

---

## 3. Advanced Variations

- **Morris Inorder**: O(1) space by threading; use rightmost of left subtree to point to current (then restore).
- **Serialize/Deserialize**: Preorder with null markers; single string; deserialize by consuming tokens.
- **BST**: Inorder successor (right exists → leftmost of right; else first ancestor that is left child); range sum (inorder with range filter).
- **Kth smallest in BST**: Inorder with counter; or store subtree sizes and binary search on rank.

### Edge Cases
- Empty tree; single node; skew (linked list); duplicate values (BST definition: left <= vs left <); integer overflow in path sum.

---

## 4. Common Interview Problems

**Easy**: Max Depth, Invert Binary Tree, Diameter of Binary Tree, Same Tree, Symmetric Tree.  
**Medium**: Construct from Preorder+Inorder, Validate BST, LCA, Right Side View, Kth Smallest in BST.  
**Hard**: Serialize/Deserialize, Binary Tree Max Path Sum, Recover BST (two swapped nodes).

---

## 5. Pattern Recognition

- **Path/Sum**: DFS with running sum; backtrack path (add node, recurse, remove). Tree DP when "path through node" depends on both subtrees.
- **BST**: Inorder sorted; search O(h); range queries by pruning.
- **LCA**: BST by value comparison; general tree by "return node if match, else combine left/right".
- **Level**: BFS; right/left view = last/first per level.

---

## 6. Code Implementations

```python
def max_path_sum(root):
    best = float('-inf')
    def dfs(node):
        nonlocal best
        if not node:
            return 0
        l = max(0, dfs(node.left))
        r = max(0, dfs(node.right))
        best = max(best, node.val + l + r)
        return node.val + max(l, r)
    dfs(root)
    return best

def lowest_common_ancestor_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
    return None
```

---

## 7. SDE-3 Level Thinking

- **Trade-offs**: Recursion vs iterative (stack): recursion simpler but O(h) stack; Morris for O(1) space. Tree DP avoids repeated traversal when one pass can carry multiple values.
- **Scalability**: For very deep trees, iterative or Morris to avoid stack overflow. Serialization format affects size (binary vs string).

---

## 8. Interview Strategy

- **Identify**: "Path" that can go through root → tree DP. "BST" → inorder or search. "LCA" → BST compare values; general return node.
- **Common mistakes**: Confusing path "ending at node" vs "through node"; not handling negative values (use max(0, child)); BST equality (left < root vs left <= root).

---

## 9. Quick Revision

- **Formulas**: Diameter = max(left_d, right_d, left_h+right_h+1). Max path through node = node + max(0,L) + max(0,R).
- **Tricks**: Postorder for tree DP; inorder for BST; null markers for serialize.
- **Edge cases**: Empty, single node, negatives, overflow.
- **Pattern tip**: "Through root" or "any path" → tree DP with global max.
