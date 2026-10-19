---
module: striver/24-binary-trees
lesson: 12
topic: Check for symmetrical BTs
difficulty: Easy
source: https://takeuforward.org/learning/dsa/check-for-symmetrical-bts?category=medium-problems&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, dfs, comparison]
---
# 12. Check for symmetrical BTs

← [Maximum path sum](11-binary-tree-maximum-path-sum.md) · [Part 24 index](README.md) · Next → [Children Sum Property in Binary Tree](13-children-sum-property.md)

> [!abstract] Problem at a glance
> **Task:** Is the tree a mirror image of itself around its centre?
> **Key insight:** Compare the left and right subtrees as mirrors. `mirror(a, b)` holds when `a.val == b.val`, `mirror(a.left, b.right)` and `mirror(a.right, b.left)`. It's *same tree* with the second tree's children swapped.
> **Difficulty:** Easy · **Pattern:** Simultaneous DFS (mirrored) · **Also on:** [LC 101](https://leetcode.com/problems/symmetric-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-for-symmetrical-bts?category=medium-problems&source=strivers-a2z-dsa-sheet) · **Time:** 8 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Iterative pair queue](#3-iterative-pair-queue) · [4. Recursive mirror check](#4-recursive-mirror-check) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a binary tree, check whether it is a mirror of itself (symmetric around its centre).

| Input | Output | Why |
|---|---|---|
| `root = [1,2,2,3,4,4,3]` | `true` |  |
| `root = [1,2,2,null,3,null,3]` | `false` | both 3s hang on the right |

**Constraints:** `1 ≤ n ≤ 1000`; values `−100…100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Iterative pair queue | queue of (a, b) pairs; push (a.l, b.r) and (a.r, b.l) | O(n) | O(w) |
| Recursive mirror check | m(a,b) = a.val==b.val ∧ m(a.l,b.r) ∧ m(a.r,b.l) | O(n) | O(h) |

> [!tip] Interview angle
> Recursive first, then the iterative queue version: push pairs (outer, outer), (inner, inner). A common wrong idea is 'inorder is a palindrome'. Test 5 (`[1,2,2,2,null,2]`) has a palindromic inorder but isn't symmetric.

---

## 3. Iterative pair queue

**Intuition.** It's the same comparison as the recursion, with explicit pairs and no recursion depth.

```python
from collections import deque

def is_symmetric_iter(root):
    if not root:
        return True
    q = deque([(root.left, root.right)])
    while q:
        a, b = q.popleft()
        if not a and not b:
            continue
        if not a or not b or a.val != b.val:
            return False
        q.append((a.left, b.right))
        q.append((a.right, b.left))
    return True
```

**Complexity:** time **O(n)**, space **O(w)**.

---

## 4. Recursive mirror check

**Intuition.** The outer children pair up and the inner children pair up.

**Algorithm**

1. Empty root → true.
2. `m(a, b)`: both null → true; one null → false; else compare values and recurse outer & inner.
3. Return `m(root.left, root.right)`.

**Dry run** — [1,2,2,3,4,4,3]: m(2,2): vals equal → m(3,3) ✓, m(4,4) ✓ → true.

**C++**
```cpp
bool mir(TreeNode* a, TreeNode* b) {
    if (!a || !b) return a == b;
    return a->val == b->val && mir(a->left, b->right) && mir(a->right, b->left);
}
bool isSymmetric(TreeNode* root) { return !root || mir(root->left, root->right); }
```

**Java**
```java
static boolean mir(TreeNode a, TreeNode b) {
    if (a == null || b == null) return a == b;
    return a.val == b.val && mir(a.left, b.right) && mir(a.right, b.left);
}
static boolean isSymmetric(TreeNode root) { return root == null || mir(root.left, root.right); }
```

**Python**
```python
def is_symmetric(root):
    def m(a, b):
        if not a or not b:
            return a is b
        return a.val == b.val and m(a.left, b.right) and m(a.right, b.left)
    return not root or m(root.left, root.right)
```

**Complexity:** time **O(n)**, space **O(h)** — each mirrored pair compared once.

---

## Edge cases

- Empty / single node → true.
- Equal values, asymmetric shape → false.
- Palindromic inorder but not symmetric (test 5).

---

## Common mistakes

1. Comparing `a.left` with `b.left` (that's *same tree*).
2. Using the inorder palindrome check (ignores structure).

---

## Follow-ups

1. Mirror (invert) a tree?
2. Symmetric N-ary tree?

<details><summary>Answer sketches</summary>

**#1:** Swap children at every node (LC 226) — pre- or post-order.

**#2:** Compare children[i] with children[k−1−i] recursively.
</details>

---

## Flashcards

**Mirror check recursion?** #flashcard
m(a.left, b.right) && m(a.right, b.left) with equal values.

**Symmetric via inorder palindrome?** #flashcard
Wrong — ignores shape.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
