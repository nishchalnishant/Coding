---
module: striver/24-binary-trees
lesson: 31
topic: Morris Inorder Traversal
difficulty: Medium
source: https://takeuforward.org/learning/dsa/morris-inorder-traversal-?category=traversal-in-constant-space&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, morris, constant-space, inorder]
---
# 31. Morris Inorder Traversal

← [Serialize and De-serialize BT](30-serialize-deserialize.md) · [Part 24 index](README.md) · Next → [Morris Preorder Traversal](32-morris-preorder.md)

> [!abstract] Problem at a glance
> **Task:** Inorder traversal in O(1) extra space: no stack, no recursion. The tree must be restored afterwards.
> **Key insight:** Use the null `right` pointer of each node's **inorder predecessor** (the rightmost node of its left subtree) as a temporary **thread back to the node**. First visit: no thread yet, so create it and go left. Second visit, arriving through the thread: remove it, output the node and go right.
> **Difficulty:** Medium · **Pattern:** Threaded binary tree · **Also on:** [LC 94](https://leetcode.com/problems/binary-tree-inorder-traversal/) (follow-up)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/morris-inorder-traversal-?category=traversal-in-constant-space&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Morris inorder](#3-morris-inorder) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Return the inorder traversal of a binary tree using O(1) auxiliary space by temporarily modifying the tree (Morris traversal). The tree must be unchanged when the function returns.

| Input | Output | Why |
|---|---|---|
| `root = [1,2,3,4,5,null,6]` | `[4,2,5,1,3,6]` |  |

**Constraints:** `0 ≤ n ≤ 100` (algorithm works for any n).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Morris inorder | no left → visit, go right; else find pred: no thread → make it, go left; thread → cut, visit, go right | O(n) | O(1) |

> [!tip] Interview angle
> Draw the thread, then show why it's O(n): every edge on a predecessor path is walked at most twice (once to create the thread, once to remove it). Mention it's not safe for concurrent readers, since the tree is temporarily mutated. It's the main L4 'O(1) space' follow-up for any inorder problem: kth smallest, recover BST, validate BST.

---

## 3. Morris inorder

**Intuition.** The thread replaces the stack frame that would tell us where to return after finishing the left subtree.

**Algorithm**

1. `cur = root`.
2. If `cur.left` is null: output `cur`, `cur = cur.right`.
3. Else `pred = cur.left`; walk right while `pred.right` and `pred.right ≠ cur`.
4. If `pred.right` is null: `pred.right = cur`; `cur = cur.left`.
5. Else (thread found): `pred.right = null`; output `cur`; `cur = cur.right`.

**Dry run** — T7: at 1, pred 5 → thread 5→1, go 2; at 2, pred 4 → thread, go 4; 4 no left → out 4, follow thread to 2; pred 4 threaded → cut, out 2, go 5; out 5, thread → 1; cut, out 1, go 3; 3 no left → out 3; 6 → out 6.

**C++**
```cpp
vector<int> morrisInorder(TreeNode* root) {
    vector<int> res;
    TreeNode* cur = root;
    while (cur) {
        if (!cur->left) { res.push_back(cur->val); cur = cur->right; continue; }
        TreeNode* pred = cur->left;
        while (pred->right && pred->right != cur) pred = pred->right;
        if (!pred->right) { pred->right = cur; cur = cur->left; }
        else { pred->right = nullptr; res.push_back(cur->val); cur = cur->right; }
    }
    return res;
}
```

**Java**
```java
static List<Integer> morrisInorder(TreeNode root) {
    List<Integer> res = new ArrayList<>();
    TreeNode cur = root;
    while (cur != null) {
        if (cur.left == null) { res.add(cur.val); cur = cur.right; continue; }
        TreeNode pred = cur.left;
        while (pred.right != null && pred.right != cur) pred = pred.right;
        if (pred.right == null) { pred.right = cur; cur = cur.left; }
        else { pred.right = null; res.add(cur.val); cur = cur.right; }
    }
    return res;
}
```

**Python**
```python
def morris_inorder(root):
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
            pred.right = cur
            cur = cur.left
        else:
            pred.right = None
            res.append(cur.val)
            cur = cur.right
    return res
```

**Complexity:** time **O(n)**, space **O(1)** — each predecessor path is traversed twice in total, so O(n) amortised, with no auxiliary structures.

---

## Edge cases

- Empty tree.
- Right-skewed: never threads.
- Left-skewed: deep predecessor chains, still O(n).

---

## Common mistakes

1. Missing the `pred.right != cur` stop condition, which loops forever around the thread.
2. Not removing the thread, which leaves a corrupted tree (cycles).
3. Outputting on thread creation (that's preorder).

---

## Follow-ups

1. Morris preorder?
2. Morris postorder?
3. Kth smallest in O(1) space?

<details><summary>Answer sketches</summary>

**#1:** Output when *creating* the thread instead of when removing it.

**#2:** Possible (reverse right edges of the left subtree) — rarely asked.

**#3:** Morris inorder with a counter.
</details>

---

## Flashcards

**Morris inorder: what's the thread?** #flashcard
Inorder predecessor's right pointer → current node.

**Morris inorder: when to output?** #flashcard
When cur has no left, or when removing the thread.

**Morris time complexity?** #flashcard
O(n) — each edge walked at most twice (plus once).

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
