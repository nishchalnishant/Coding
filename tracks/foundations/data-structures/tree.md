# Tree — SDE-2+ Level

Hierarchical structure: root, parent-child, leaves. SDE-3 expects traversals, BST invariants, LCA, and tree DP (return multiple values).

---

## 1. Concept Overview

### Problem Space
- **Traversals**: Pre/in/post (recursive vs iterative), Level-order (BFS).
- **Paths**: Path sum, diameter, max path sum (any to any).
- **BST**: Validate, kth smallest, range sum, successor.
- **Structural**: Serialize/Deserialize, flatten to list, invert.

### When to Use
| Goal | Technique |
| :--- | :--- |
| **Sorted Order** | Inorder traversal of BST. |
| **Subtree Values** | Postorder traversal (Bottom-up). |
| **Level-by-Level** | BFS with a queue. |
| **O(1) Space** | Morris Traversal. |

---

## 2. Core Algorithms & Click Moments

### Lowest Common Ancestor (LCA)
> [!IMPORTANT]
> **The Click Moment**: "Find common parent", "Distance between nodes", "Lowest shared ancestor".

- **Binary Tree**: Recursive: if `root` is `p` or `q`, return `root`. Recurse left/right. If both non-null, `root` is LCA.
- **BST**: If both `p, q < root`, go left; if both `> root`, go right; else `root` is LCA.

### Tree DP (Max Path Sum)
> [!IMPORTANT]
> **The Click Moment**: "Path from any node to any node", "Global max sum", "Postorder gain calculation".

```python
def dfs(node):
    if not node: return 0
    left = max(0, dfs(node.left))
    right = max(0, dfs(node.right))
    global_max = max(global_max, node.val + left + right)
    return node.val + max(left, right)
```

---

## 3. Advanced Variations

- **Morris Inorder**: O(1) space traversal by threading.
- **Serialize/Deserialize**: Use preorder with `null` markers for consistent representation.
- **Recover BST**: Find two swapped nodes using inorder traversal (they will be out of order).

---

## 4. Common Interview Problems

### Easy
- [Invert Binary Tree](../google-sde2/PROBLEM_DETAILS.md#invert-binary-tree) — Recursive swap.
- **Diameter of Binary Tree** — Postorder height + global max.

### Medium
- [Validate BST](../google-sde2/PROBLEM_DETAILS.md#validate-bst) — Use `(min, max)` range or inorder check.
- [LCA of Binary Tree](../google-sde2/PROBLEM_DETAILS.md#lca) — The classic "both sides non-null" logic.

### Hard
- [Serialize and Deserialize](../google-sde2/PROBLEM_DETAILS.md#serialize-and-deserialize-binary-tree) — Preorder with delimiters.
- [Binary Tree Max Path Sum](../google-sde2/PROBLEM_DETAILS.md#binary-tree-maximum-path-sum) — Bottom-up gain return.

---

## 5. Pattern Recognition

- **"Sorted BST"** → Inorder.
- **"Level by Level"** → BFS.
- **"Any to Any Path"** → Tree DP with global max.
- **"Range/Boundaries"** → Pruning or (min, max) recursion.

---

## 6. Interview Strategy

- **Null Handling**: Always handle `if not root: return ...`.
- **Bottom-Up**: Most tree problems are solved by getting info from children (postorder).
- **BST Invariant**: Remember that left < root < right.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **[Validate BST](../google-sde2/PROBLEM_DETAILS.md#validate-bst)** | "Strict range" | `min < val < max` | Only checking children is **not** enough. |
| **[Max Path Sum](../google-sde2/PROBLEM_DETAILS.md#binary-tree-maximum-path-sum)** | "Bottom-up gain" | `max(0, child_gain)` | Path can stop at node (negatives). |
| **[LCA](../google-sde2/PROBLEM_DETAILS.md#lca)** | "Split point" | `left and right` | Nodes might not exist (validate). |
| **[Kth Smallest](../google-sde2/PROBLEM_DETAILS.md#kth-smallest-in-bst)** | "Sorted rank" | Inorder traversal | Iterative stop at `k`. |

---

## See also

- [Graph](../algorithms/graph.md) — trees are special graphs  
- [Dynamic Programming](../algorithms/dynamic-programming/README.md) — tree DP  
- [Patterns Master](../../reference/patterns/patterns-master.md)
- [Backtracking](../algorithms/backtracking.md) — path sum with backtrack
