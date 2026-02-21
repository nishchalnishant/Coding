# Day 8: Binary Search Trees (BST)

Here are detailed notes for **Day 8: Binary Search Trees (BST)**. This day focuses on understanding the properties, operations, and common problems associated with binary search trees.

***

#### 1. **What is a Binary Search Tree (BST)?**

A **Binary Search Tree (BST)** is a data structure that maintains a sorted order of elements, allowing for efficient search, insertion, and deletion operations.

**Key Properties**:

* Each node has at most two children.
* The left child contains nodes with values less than the parent node.
* The right child contains nodes with values greater than the parent node.
* There are no duplicate nodes in a BST.

***

#### 2. **Basic Operations on BST**

The primary operations on a BST are **search**, **insert**, and **delete**. Each of these operations has an average time complexity of O(log n) but can degrade to O(n) in the worst case if the tree becomes unbalanced.

**2.1 Search Operation**

To search for a value in a BST:

1. Start at the root.
2. If the value equals the root's value, return the root.
3. If the value is less than the root's value, search in the left subtree.
4. If the value is greater, search in the right subtree.

**Implementation**:

```python
def search_bst(root, key):
    if not root or root.val == key:
        return root
    if key < root.val:
        return search_bst(root.left, key)
    else:
        return search_bst(root.right, key)
```

***

**2.2 Insertion Operation**

To insert a new value into a BST:

1. Start at the root.
2. If the new value is less than the root, go to the left child; if greater, go to the right child.
3. Repeat until you find a null child position where you can insert the new node.

**Implementation**:

```python
def insert_bst(root, key):
    if not root:
        return TreeNode(key)  # Create a new node
    if key < root.val:
        root.left = insert_bst(root.left, key)
    else:
        root.right = insert_bst(root.right, key)
    return root
```

***

**2.3 Deletion Operation**

To delete a value from a BST:

1. Search for the node to be deleted.
2. There are three cases to handle:
   * **Case 1**: Node to be deleted has no children (leaf node). Simply remove it.
   * **Case 2**: Node to be deleted has one child. Remove the node and replace it with its child.
   * **Case 3**: Node to be deleted has two children. Find the node's in-order successor (smallest node in the right subtree) or in-order predecessor (largest node in the left subtree), replace the value of the node to be deleted with that of the successor/predecessor, and then delete the successor/predecessor.

**Implementation**:

```python
def delete_bst(root, key):
    if not root:
        return root
    if key < root.val:
        root.left = delete_bst(root.left, key)
    elif key > root.val:
        root.right = delete_bst(root.right, key)
    else:
        # Node with one child or no child
        if not root.left:
            return root.right
        elif not root.right:
            return root.left
        # Node with two children: get the inorder successor (smallest in the right subtree)
        temp = find_min(root.right)
        root.val = temp.val  # Copy the inorder successor's value to this node
        root.right = delete_bst(root.right, temp.val)  # Delete the inorder successor
    return root

def find_min(node):
    while node.left:
        node = node.left
    return node
```

***

#### 3. **Traversal of a BST**

Traversing a BST can be done in several ways:

* **In-order Traversal**: Returns nodes in ascending order.
* **Pre-order Traversal**: Useful for copying or serializing the tree.
* **Post-order Traversal**: Useful for deleting the tree.

**Implementation (In-order)**:

```python
def in_order_traversal(root):
    if root:
        in_order_traversal(root.left)
        print(root.val)
        in_order_traversal(root.right)
```

***

#### 4. **Balancing BSTs**

A standard BST can become unbalanced, leading to O(n) search time. To maintain balance, consider using:

* **AVL Trees**: A self-balancing BST that maintains balance through rotations.
* **Red-Black Trees**: A type of self-balancing BST that uses color properties to ensure balance.

***

#### 5. **Common Problems Involving BSTs**

Here are some common problems that involve binary search trees:

1. **Validate Binary Search Tree**:
   * Check if a given tree is a valid BST.
   * Use a helper function that maintains the range of valid values for each node.
2. **Lowest Common Ancestor (LCA)**:
   * Find the lowest common ancestor of two nodes in a BST. Start from the root and check if both nodes lie in the left or right subtree to decide the direction.
3. **Kth Smallest Element in a BST**:
   * Perform an in-order traversal and keep count until you reach the kth element.
4. **Convert Sorted Array to BST**:
   * Given a sorted array, convert it into a balanced BST by recursively choosing the middle element as the root.
5. **Range Sum of BST**:
   * Given a range \[low, high], return the sum of values of all nodes within that range.

***

#### 6. **Recommended Practice Problems**

1. **LeetCode**:
   * Validate Binary Search Tree
   * Kth Smallest Element in a BST
   * Lowest Common Ancestor of a BST
   * Convert Sorted Array to Binary Search Tree
   * Range Sum of BST
2. **HackerRank**:
   * Binary Search Tree: Insertion
   * Binary Search Tree: Lowest Common Ancestor

***

#### 7. **Key Concepts to Remember**

* The average time complexity for search, insertion, and deletion operations in a balanced BST is O(log n).
* A BST is a powerful data structure for maintaining sorted data and supporting efficient search and modification operations.
* Understanding how to traverse and manipulate BSTs is crucial for solving a wide range of problems in data structures and algorithms.

By mastering the operations and applications of binary search trees, you'll be well-prepared to tackle more complex problems involving trees in coding interviews.
