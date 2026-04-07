# Day 7: Tree Traversal Techniques

Here are detailed notes for **Day 7: Tree Traversal Techniques**. This day will focus on implementing and understanding different tree traversal methods, particularly for binary trees.

***

#### 1. **What is Tree Traversal?**

Tree traversal refers to the process of visiting all the nodes in a tree data structure systematically. There are several ways to traverse a tree, and the method you choose can affect the outcome based on the structure of the tree.

#### 2. **Types of Tree Traversals**

Tree traversals can be categorized into two main types:

1. **Depth-First Traversals (DFS)**:
   * **In-order Traversal**
   * **Pre-order Traversal**
   * **Post-order Traversal**
2. **Breadth-First Traversals (BFS)**:
   * **Level-order Traversal**

***

#### 3. **Depth-First Search (DFS) Traversals**

**3.1 In-order Traversal**

In in-order traversal, the nodes are visited in the following order:

1. Traverse the left subtree.
2. Visit the root node.
3. Traverse the right subtree.

**Properties**:

* In a binary search tree (BST), in-order traversal returns the nodes in ascending order.

**Implementation** (recursive):

```python
def in_order_traversal(root):
    if root:
        in_order_traversal(root.left)  # Visit left subtree
        print(root.val)                 # Visit root
        in_order_traversal(root.right) # Visit right subtree
```

**Implementation** (iterative):

```python
def in_order_traversal_iterative(root):
    stack = []
    current = root
    while stack or current:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        print(current.val)
        current = current.right
```

***

**3.2 Pre-order Traversal**

In pre-order traversal, the nodes are visited in the following order:

1. Visit the root node.
2. Traverse the left subtree.
3. Traverse the right subtree.

**Properties**:

* Pre-order traversal is useful for copying trees and constructing trees from a serialized format.

**Implementation** (recursive):

```python
def pre_order_traversal(root):
    if root:
        print(root.val)                 # Visit root
        pre_order_traversal(root.left)  # Visit left subtree
        pre_order_traversal(root.right) # Visit right subtree
```

**Implementation** (iterative):

```python
def pre_order_traversal_iterative(root):
    if not root:
        return
    stack = [root]
    while stack:
        node = stack.pop()
        print(node.val)
        if node.right:  # Push right first so left is processed first
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
```

***

**3.3 Post-order Traversal**

In post-order traversal, the nodes are visited in the following order:

1. Traverse the left subtree.
2. Traverse the right subtree.
3. Visit the root node.

**Properties**:

* Post-order traversal is useful for deleting trees or evaluating postfix expressions.

**Implementation** (recursive):

```python
def post_order_traversal(root):
    if root:
        post_order_traversal(root.left)  # Visit left subtree
        post_order_traversal(root.right) # Visit right subtree
        print(root.val)                  # Visit root
```

**Implementation** (iterative):

```python
def post_order_traversal_iterative(root):
    if not root:
        return
    stack = []
    output = []
    stack.append(root)
    while stack:
        node = stack.pop()
        output.append(node.val)  # Store node value
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    while output:  # Reverse the output to get post-order
        print(output.pop())
```

***

#### 4. **Breadth-First Search (BFS) Traversal**

**4.1 Level-order Traversal**

In level-order traversal, nodes are visited level by level, starting from the root and moving down to the leaves. Nodes on the same level are visited from left to right.

**Properties**:

* It is implemented using a queue.
* Useful for finding the shortest path in unweighted graphs.

**Implementation**:

```python
from collections import deque

def level_order_traversal(root):
    if not root:
        return
    queue = deque([root])
    while queue:
        node = queue.popleft()  # Dequeue the front node
        print(node.val)
        if node.left:           # Enqueue left child
            queue.append(node.left)
        if node.right:          # Enqueue right child
            queue.append(node.right)
```

***

#### 5. **Time Complexity of Traversals**

* **In-order, Pre-order, Post-order Traversal**: O(n), where n is the number of nodes in the tree.
* **Level-order Traversal**: O(n).

#### 6. **Use Cases of Tree Traversals**

* **In-order Traversal**: Retrieve data from a BST in sorted order.
* **Pre-order Traversal**: Create a copy of the tree or generate a prefix expression.
* **Post-order Traversal**: Free nodes in a tree or evaluate expressions in post-fix notation.
* **Level-order Traversal**: Print the tree level by level, find the maximum width, or locate nodes at a certain level.

***

#### 7. **Key Concepts to Understand**

1. **Recursive vs. Iterative Implementations**:
   * Recursive implementations are more straightforward and often easier to read, but they can lead to stack overflow for very deep trees.
   * Iterative implementations typically use an explicit stack or queue, which can be more efficient in terms of memory.
2. **Applications of Tree Traversals**:
   * Tree traversals are foundational in understanding more complex tree-based algorithms and data structures, including heaps and segment trees.
   * They are also crucial in various applications like compiler design, databases, and AI algorithms.

***

#### 8. **Recommended Practice Problems**

1. **LeetCode**:
   * Binary Tree Inorder Traversal
   * Binary Tree Preorder Traversal
   * Binary Tree Postorder Traversal
   * [Binary Tree Level Order Traversal](../../google-sde2/PROBLEM_DETAILS.md#binary-tree-level-order-traversal)
   * Construct Binary Tree from Preorder and Inorder Traversal
2. **HackerRank**:
   * Tree: Level Order Traversal
   * Tree: Postorder Traversal
   * Tree: Inorder Traversal

By mastering these traversal techniques and their applications, you'll enhance your ability to work with trees and solve a variety of tree-related problems effectively.
