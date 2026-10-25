---
module: striver-a2z/24-binary-trees
lesson: 32
topic: Morris Preorder Traversal
difficulty: Medium
source: https://takeuforward.org/learning/dsa/morris-preorder-traversal-?category=traversal-in-constant-space&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, morris, constant-space, preorder]
---
# 32. Morris Preorder Traversal

← [Morris Inorder Traversal](31-morris-inorder.md) · [Part 24 index](README.md) · Next → [Part 25: Binary Search Trees](../25-binary-search-trees/README.md)

> [!abstract] Problem at a glance
> **Task:** Preorder traversal in O(1) extra space using Morris threads.
> **Key insight:** It's identical to Morris inorder except for **when you output**. In preorder a node is visited before its left subtree, so output at the moment the thread is **created**, not when it is removed. Nodes without a left child are still output immediately.
> **Difficulty:** Medium · **Pattern:** Threaded binary tree · **Also on:** [LC 144](https://leetcode.com/problems/binary-tree-preorder-traversal/) (follow-up)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/morris-preorder-traversal-?category=traversal-in-constant-space&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Morris preorder](#3-morris-preorder) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Return the preorder traversal of a binary tree using O(1) auxiliary space (Morris traversal), restoring the tree before returning.

| Input | Output | Why |
|---|---|---|
| `root = [1,2,3,4,5,null,6]` | `[1,2,4,5,3,6]` |  |

**Constraints:** `0 ≤ n ≤ 100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Morris preorder | no left → visit, right; pred unthreaded → visit, thread, left; threaded → cut, right | O(n) | O(1) |

> [!tip] Interview angle
> Present it as a one-line diff from Morris inorder. That shows you understand the mechanism rather than memorising two programs. The thread logic is untouched; only the output moves.

---

## 3. Morris preorder

**Intuition.** The first arrival at a node with a left subtree is exactly its preorder visit time.

**Algorithm**

1. `cur = root`.
2. No left: output, go right.
3. Else find `pred` (rightmost of left, stopping at `cur`).
4. No thread: **output cur**, `pred.right = cur`, go left.
5. Thread: `pred.right = null`, go right (no output).

**Dry run** — T7: 1 (thread 5→1) out 1; 2 (thread 4→2) out 2; 4 out; back to 2: cut, go 5; 5 out; back to 1: cut, go 3; 3 out; 6 out.

**C++**
```cpp
vector<int> morrisPreorder(TreeNode* root) {
    vector<int> res;
    TreeNode* cur = root;
    while (cur) {
        if (!cur->left) { res.push_back(cur->val); cur = cur->right; continue; }
        TreeNode* pred = cur->left;
        while (pred->right && pred->right != cur) pred = pred->right;
        if (!pred->right) { res.push_back(cur->val); pred->right = cur; cur = cur->left; }
        else { pred->right = nullptr; cur = cur->right; }
    }
    return res;
}
```

**Java**
```java
static List<Integer> morrisPreorder(TreeNode root) {
    List<Integer> res = new ArrayList<>();
    TreeNode cur = root;
    while (cur != null) {
        if (cur.left == null) { res.add(cur.val); cur = cur.right; continue; }
        TreeNode pred = cur.left;
        while (pred.right != null && pred.right != cur) pred = pred.right;
        if (pred.right == null) { res.add(cur.val); pred.right = cur; cur = cur.left; }
        else { pred.right = null; cur = cur.right; }
    }
    return res;
}
```

**Python**
```python
def morris_preorder(root):
    res, cur = [], root
    while cur:
        if not cur.left:
            res.append(cur.val)
            cur = cur.right
            continue
        pred = cur.left
        while pred.right and pred.right is not cur:
            pred = pred.right
        if not pred.right:
            res.append(cur.val)
            pred.right = cur
            cur = cur.left
        else:
            pred.right = None
            cur = cur.right
    return res
```

**Complexity:** time **O(n)**, space **O(1)** — same O(n) amortised bound as Morris inorder.

---

## Edge cases

- Empty tree.
- Left-only chain: every node outputs when threading.
- Right-skewed: no threads.

---

## Common mistakes

1. Also outputting when removing the thread (duplicates).
2. Forgetting the restore step.

---

## Follow-ups

1. Morris inorder?
2. Flatten to linked list in O(1)?

<details><summary>Answer sketches</summary>

**#1:** Move the output to the thread-removal branch.

**#2:** Same predecessor idea, but permanent rewiring.
</details>

---

## Flashcards

**Morris preorder vs inorder: the only difference?** #flashcard
Preorder outputs when creating the thread; inorder when removing it.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
