# Tree

A hierarchical data structure consisting of nodes connected by edges, starting from a single root node.

## Key Concepts
- **Structure**: Parent-child relationship. Leaves have no children.
- **Binary Tree**: Each node has at most two children.
- **Binary Search Tree (BST)**: Left child $<$ Parent $<$ Right child. Inorder traversal yields sorted elements.

## Traversals
- **Depth-First Search (DFS)**:
  - *Preorder* (Root, Left, Right): Best for copying a tree or serialization.
  - *Inorder* (Left, Root, Right): Best for BSTs to get sorted order.
  - *Postorder* (Left, Right, Root): Best for deleting a tree or bottom-up calculations (e.g., getting height).
- **Breadth-First Search (BFS)**:
  - Level-order traversal. Implemented using a Queue.

## Advanced Trees
- **Trie (Prefix Tree)**: Efficient string matching and autocomplete.
- **Balanced Trees (AVL, Red-Black)**: Self-adjusts to maintain $O(\log N)$ height.
- **Segment Tree**: Fast range queries and updates over arrays.

## Core Techniques
- **Recursion**: Most tree problems are solved elegantly with recursion (DFS). Trust the recurrence relation.
- **Lowest Common Ancestor (LCA)**: 
  - *BST*: Move left/right based on values.
  - *Binary Tree*: Return non-null node from left/right subtrees.
- **Backtracking**: Often used in Path Sum problems to undo the path variable.

## Common SDE-3 Tree Problems
- *Easy*: Maximum Depth, Invert Binary Tree, Diameter of Binary Tree, Same Tree, Symmetric Tree.
- *Medium*: Construct Binary Tree from Preorder and Inorder, Validate BST, Lowest Common Ancestor, Binary Tree Right Side View, Kth Smallest Element in BST.
- *Hard*: Serialize and Deserialize Binary Tree, Binary Tree Maximum Path Sum, Recover Binary Search Tree.
