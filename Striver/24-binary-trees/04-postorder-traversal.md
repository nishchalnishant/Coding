---
module: striver/24-binary-trees
lesson: 4
topic: Postorder Traversal
difficulty: Easy
source: https://takeuforward.org/learning/dsa/postorder-traversal?category=theory-and-traversals&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, dfs, traversal, stack]
---
# 4. Postorder Traversal

← [Preorder Traversal](03-preorder-traversal.md) · [Part 24 index](README.md) · Next → [Level Order Traversal](05-level-order-traversal.md)

> [!abstract] Problem at a glance
> **Task:** Return node values in **Left → Right → Root** order.
> **Key insight:** The hard iterative traversal: a node may be visited only after **both** subtrees are done. When you look at the stack top, you need to know whether you just came back from its right child. Track the `last` visited node: visit the top if it has no right child or `top.right == last`. Otherwise go right.
> **Difficulty:** Easy · **Pattern:** DFS (stack + last-visited) · **Also on:** [LC 145](https://leetcode.com/problems/binary-tree-postorder-traversal/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/postorder-traversal?category=theory-and-traversals&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursive](#3-recursive) · [4. Two stacks / reversed preorder](#4-two-stacks--reversed-preorder) · [5. One stack + last visited](#5-one-stack--last-visited) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a binary tree, return the postorder traversal of its nodes' values.

| Input | Output | Why |
|---|---|---|
| `root = [1,2,3,4,5,null,6]` | `[4,5,2,6,3,1]` | children always before parent; root last |
| `root = [1,null,2,null,3]` | `[3,2,1]` |  |

**Constraints:** `0 ≤ n ≤ 100`; values `−100…100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursive | go(left); go(right); visit | O(n) | O(h) |
| Two stacks / reversed preorder | Root→R→L preorder, then reverse | O(n) | O(n) |
| One stack + last visited | descend left; at top: go right unless right is done; else visit | O(n) | O(h) |

> [!tip] Interview angle
> Postorder is the 'bottom-up' traversal. Height, diameter, balanced check, max path sum and tree DP all compute a node's answer from its children's answers. The two-stack trick (reverse of Root-R-L) is accepted. The one-stack version shows you understand the state machine.

---

## 3. Recursive

**Intuition.** Recurse into both subtrees, then visit the node.

```python
def postorder_rec(root):
    out = []
    def go(n):
        if not n:
            return
        go(n.left)
        go(n.right)
        out.append(n.val)
    go(root)
    return out
```

**Complexity:** time **O(n)**, space **O(h)**.

---

## 4. Two stacks / reversed preorder

**Intuition.** Postorder L→R→Root reversed is Root→R→L, which is a preorder with the push order swapped. Collect it and reverse. It is simple, but the output buffer is O(n), so it doesn't stream.

```python
def postorder_two_stacks(root):
    if not root:
        return []
    out, st = [], [root]
    while st:
        n = st.pop()
        out.append(n.val)
        if n.left:
            st.append(n.left)
        if n.right:
            st.append(n.right)
    return out[::-1]
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 5. One stack + last visited

**Intuition.** Same descent as iterative inorder. At the stack top, its left subtree is done. If it has a right child that we have *not* just finished, go into it. Otherwise both subtrees are done: pop, visit and record it as `last`.

**Algorithm**

1. `cur = root`, `last = null`.
2. Loop while `cur` or stack:
3. • push left spine from `cur`.
4. • `top = st.peek()`. If `top.right` and `top.right != last`: `cur = top.right`.
5. • else pop `top`, visit, `last = top` (cur stays null).

**Dry run** — [1,2,3,4,5,null,6]: push 1,2,4 → 4 no right → visit 4 → top 2, right 5 ≠ last → push 5 → visit 5 (last=5) → top 2, right==last → visit 2 → top 1 → go 3 → push 3 → right 6 → visit 6 → visit 3 → visit 1.

**C++**
```cpp
vector<int> postorder(TreeNode* root) {
    vector<int> out;
    stack<TreeNode*> st;
    TreeNode *cur = root, *last = nullptr;
    while (cur || !st.empty()) {
        while (cur) { st.push(cur); cur = cur->left; }
        TreeNode* top = st.top();
        if (top->right && top->right != last) cur = top->right;
        else { st.pop(); out.push_back(top->val); last = top; }
    }
    return out;
}
```

**Java**
```java
static List<Integer> postorder(TreeNode root) {
    List<Integer> out = new ArrayList<>();
    Deque<TreeNode> st = new ArrayDeque<>();
    TreeNode cur = root, last = null;
    while (cur != null || !st.isEmpty()) {
        while (cur != null) { st.push(cur); cur = cur.left; }
        TreeNode top = st.peek();
        if (top.right != null && top.right != last) cur = top.right;
        else { st.pop(); out.add(top.val); last = top; }
    }
    return out;
}
```

**Python**
```python
def postorder(root):
    out, st, cur, last = [], [], root, None
    while cur or st:
        while cur:
            st.append(cur)
            cur = cur.left
        top = st[-1]
        if top.right and top.right is not last:
            cur = top.right
        else:
            st.pop()
            out.append(top.val)
            last = top
    return out
```

**Complexity:** time **O(n)**, space **O(h)** — every node is pushed once and popped once; peeks are O(1). The stack is one root-to-leaf path.

---

## Edge cases

- Empty tree.
- Right-skewed: the right-child check fires at every level.
- Node with only a right child (test `[1,2,3,null,4,5]`).

---

## Common mistakes

1. Comparing values instead of node identity for `last` (fails with duplicate values).
2. Forgetting to leave `cur = null` after visiting, which re-descends the same left spine forever.
3. Two-stack version: pushing right before left (gives the wrong reversal).

---

## Follow-ups

1. All three traversals in one pass?
2. Delete a tree safely?

<details><summary>Answer sketches</summary>

**#1:** Stack of (node, state) pairs — next problem.

**#2:** Postorder: free children before parent.
</details>

---

## Flashcards

**One-stack postorder: when do you visit the top?** #flashcard
When it has no right child or `top.right is last` (just finished).

**Postorder via preorder?** #flashcard
Root→Right→Left preorder, reversed.

**Which problems are postorder-shaped?** #flashcard
Height, diameter, balanced, max path sum — answer depends on children's answers.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
