# Page 3

Here are detailed notes for **Day 6: Review Trees Basics**. This day focuses on understanding the core concepts of trees, especially binary trees and binary search trees (BSTs), along with key operations performed on them.

***

#### 1. **What is a Tree?**

A **tree** is a hierarchical data structure that consists of nodes, where each node stores data and references to its child nodes.

* **Key Terminology**:
  * **Node**: The fundamental part of a tree, which contains data.
  * **Root**: The top node in the tree, from which all other nodes descend.
  * **Edge**: A link between two nodes.
  * **Parent**: A node that has references to other nodes (its children).
  * **Child**: A node that descends from another node (its parent).
  * **Leaf**: A node with no children.
  * **Subtree**: A tree formed from any node and its descendants.
  * **Height**: The length of the longest path from a node to a leaf.
  * **Depth**: The number of edges from the root to a node.

#### 2. **Types of Trees**

There are many types of trees, but we’ll focus on **binary trees** and **binary search trees** (BSTs).

***

#### 3. **Binary Trees**

A **binary tree** is a tree where each node can have at most two children, referred to as the **left child** and the **right child**.

* **Properties of Binary Trees**:
  * Each node can have at most two children.
  * The maximum number of nodes at level `l` is (2^l).
  * The maximum number of nodes in a binary tree with `h` levels is (2^h - 1).
  * The minimum height of a binary tree with `n` nodes is (\lceil \log\_2(n + 1) \rceil).

***

#### 4. **Binary Tree Variants**

1. **Full Binary Tree**: A binary tree in which every node has 0 or 2 children (no nodes with only one child).
2. **Complete Binary Tree**: A binary tree where all levels are completely filled except possibly for the last level, which is filled from left to right.
3. **Perfect Binary Tree**: A binary tree that is both full and complete, meaning all interior nodes have two children and all leaves are at the same level.
4. **Balanced Binary Tree**: A binary tree where the height difference between the left and right subtrees of every node is at most one.

***

#### 5. **Binary Search Trees (BSTs)**

A **binary search tree (BST)** is a type of binary tree where the following property holds for every node:

* All nodes in the **left subtree** are smaller than the node.
* All nodes in the **right subtree** are greater than the node.

**Key Operations**:

1.  **Search**: O(h), where `h` is the height of the tree.

    * Recursively compare the target value with the current node, moving left or right depending on the comparison.

    ```python
    def search_bst(root, key):
        if not root or root.val == key:
            return root
        if key < root.val:
            return search_bst(root.left, key)
        else:
            return search_bst(root.right, key)
    ```
2.  **Insertion**: O(h).

    * Traverse the tree, find the correct spot where the new node should be inserted while maintaining the BST property.

    ```python
    def insert_bst(root, key):
        if not root:
            return TreeNode(key)
        if key < root.val:
            root.left = insert_bst(root.left, key)
        else:
            root.right = insert_bst(root.right, key)
        return root
    ```
3.  **Deletion**: O(h).

    * First, search for the node to delete. Once found, there are three cases to handle:
      * The node has no children (simply remove it).
      * The node has one child (replace it with its child).
      * The node has two children (replace it with the smallest node in the right subtree or the largest in the left subtree).

    ```python
    def delete_bst(root, key):
        if not root:
            return root
        if key < root.val:
            root.left = delete_bst(root.left, key)
        elif key > root.val:
            root.right = delete_bst(root.right, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            temp = find_min(root.right)
            root.val = temp.val
            root.right = delete_bst(root.right, temp.val)
        return root
    ```
4.  **Find Minimum and Maximum**: O(h).

    * To find the minimum value in a BST, keep traversing the left child until reaching a leaf. To find the maximum value, traverse the right child.

    ```python
    def find_min(node):
        while node.left:
            node = node.left
        return node

    def find_max(node):
        while node.right:
            node = node.right
        return node
    ```

***

#### 6. **Tree Traversal Techniques**

Traversal refers to visiting all nodes in a tree in a specific order. There are two types of tree traversal:

**1. Depth-First Search (DFS) Traversal:**

*   **In-order**: Left, Root, Right.

    * In a BST, an in-order traversal visits nodes in ascending order.
    * Time complexity: O(n).

    ```python
    def in_order_traversal(root):
        if root:
            in_order_traversal(root.left)
            print(root.val)
            in_order_traversal(root.right)
    ```
*   **Pre-order**: Root, Left, Right.

    * Pre-order traversal is used to create a copy of the tree.

    ```python
    def pre_order_traversal(root):
        if root:
            print(root.val)
            pre_order_traversal(root.left)
            pre_order_traversal(root.right)
    ```
*   **Post-order**: Left, Right, Root.

    * Post-order traversal is useful for deleting or freeing nodes.

    ```python
    def post_order_traversal(root):
        if root:
            post_order_traversal(root.left)
            post_order_traversal(root.right)
            print(root.val)
    ```

**2. Breadth-First Search (BFS) Traversal:**

*   **Level-order**: Visit nodes level by level (use a queue).

    * This traversal visits nodes from top to bottom and left to right.
    * Time complexity: O(n).

    ```python
    from collections import deque

    def level_order_traversal(root):
        if not root:
            return
        queue = deque([root])
        while queue:
            node = queue.popleft()
            print(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    ```

***

#### 7. **Balanced Binary Search Trees**

Balancing a tree ensures that the height remains close to the minimum possible, making operations like search, insertion, and deletion efficient.

1. **AVL Trees**:
   * A type of balanced BST where the height difference between the left and right subtrees of every node is at most 1.
   * If the tree becomes unbalanced after an insertion or deletion, **rotations** (single or double) are performed to restore balance.
   * Time complexity for search, insert, and delete: O(log n).
2. **Red-Black Trees**:
   * A type of self-balancing BST where nodes are colored either red or black to ensure balance properties.
   * Guarantees the longest path from the root to any leaf is no more than twice the length of the shortest path.
   * Time complexity for search, insert, and delete: O(log n).

***

#### 8. **Key Concepts to Understand**

1. **Binary Trees vs. Binary Search Trees (BSTs)**:
   * In a binary tree, there are no restrictions on the values of nodes relative to their children.
   * In a BST, the left child must be smaller and the right child must be larger than the parent node.
2. **Tree Traversals**:
   * **In-order** is essential for extracting sorted elements from a BST.
   * **Pre-order** is useful for copying a tree.
   * **Post-order** is necessary for freeing nodes or evaluating mathematical expressions stored in a tree.
3. **Balanced Trees**:
   * A **balanced BST** ensures operations like search, insert, and delete take logarithmic time (O(log n)) rather than linear time (O(n)).
4. **Use Cases of Trees**:
   * Trees are widely used in databases, file systems, compilers, and various algorithms like Huffman coding, which rely on the hierarchical structure of trees.

***

#### Recommended Practice Problems

1. **LeetCode**:
   * Validate Binary Search Tree
   * Insert into a Binary Search Tree
   * Delete Node in a BST
   * Invert Binary Tree
   * [Binary Tree Level Order Traversal](../../google-sde2/PROBLEM_DETAILS.md#binary-tree-level-order-traversal)
2. **HackerRank**:
   * Binary Search Tree: Insertion
   * Binary Search Tree: Lowest Common Ancestor
   * Tree: Preorder Traversal

By mastering these basics of trees, especially binary trees and binary search trees, and practicing key tree operations, you'll be prepared to solve more complex

tree-related problems.
