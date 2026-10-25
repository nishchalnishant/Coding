---
module: striver-a2z/24-binary-trees
lesson: 27
topic: Requirements needed to construct a unique BT
difficulty: Easy
source: https://takeuforward.org/learning/dsa/requirements-needed-to-construct-a-unique-bt?category=construction-problems&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, theory, construction]
---
# 27. Requirements needed to construct a unique BT

← [Flatten Binary Tree to LinkedList](26-flatten-binary-tree.md) · [Part 24 index](README.md) · Next → [Construct a BT from Preorder and Inorder](28-build-from-preorder-inorder.md)

> [!abstract] Problem at a glance
> **Task:** Given two traversal codes (1 = preorder, 2 = inorder, 3 = postorder), can they always reconstruct a unique binary tree?
> **Key insight:** Preorder and postorder each tell you **where the root is** (first or last element) but not where the left subtree ends. Inorder tells you **how the remaining nodes split around the root**. You need both kinds of information, so the answer is yes iff one of the two is inorder and the other is pre or post.
> **Difficulty:** Easy · **Pattern:** Theory / case analysis · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/unique-binary-tree-requirements/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/requirements-needed-to-construct-a-unique-bt?category=construction-problems&source=strivers-a2z-dsa-sheet) · **Time:** 3 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Case check](#3-case-check) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given two integers `a` and `b` denoting traversal types (1 = preorder, 2 = inorder, 3 = postorder), return `true` if a unique binary tree can be constructed from those two traversals (with distinct values), else `false`.

| Input | Output | Why |
|---|---|---|
| `a = 1, b = 2` | `true` | pre + in |
| `a = 1, b = 3` | `false` | pre + post: [1,2] can be 1→left 2 or 1→right 2 |

**Constraints:** `1 ≤ a, b ≤ 3`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Case check | exactly one is inorder and they differ | O(1) | O(1) |

> [!tip] Interview angle
> The counterexample is the whole answer. With pre `[1,2]` and post `[2,1]`, node 2 can be either the left or the right child. Pre + post is enough only for a **full** binary tree (every node has 0 or 2 children), as in LC 889. Mention that exception.

---

## 3. Case check

**Intuition.** Same-type pairs add no information. Pre + post can't resolve one-child ambiguity.

**Algorithm**

1. Return `a != b and (a == 2 or b == 2)`.

**Dry run** — (1,2) → true; (1,3) → false; (2,2) → false.

**C++**
```cpp
bool isPossible(int a, int b) {
    return a != b && (a == 2 || b == 2);
}
```

**Java**
```java
static boolean isPossible(int a, int b) {
    return a != b && (a == 2 || b == 2);
}
```

**Python**
```python
def is_possible(a, b):
    return a != b and (a == 2 or b == 2)
```

**Complexity:** time **O(1)**, space **O(1)** — constant-time check.

---

## Edge cases

- Same traversal twice → false.
- Pre + post with a full binary tree → unique (special case, LC 889).

---

## Common mistakes

1. Saying pre + post works in general.
2. Forgetting duplicate values break uniqueness even with inorder.

---

## Follow-ups

1. Pre + post for a full binary tree?
2. Level order + inorder?

<details><summary>Answer sketches</summary>

**#1:** Root = pre[0], left root = pre[1]; find it in post to size the left subtree (LC 889).

**#2:** Also unique: the first level-order element present in an inorder range is that range's root.
</details>

---

## Flashcards

**Which traversal pairs give a unique BT?** #flashcard
Inorder + (preorder or postorder).

**Why not pre + post?** #flashcard
One-child nodes: can't tell left from right child.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
