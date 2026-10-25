---
module: striver-a2z/24-binary-trees
lesson: 30
topic: Serialize and De-serialize BT
difficulty: Hard
source: https://takeuforward.org/learning/dsa/serialize-and-de-serialize-bt?category=construction-problems&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, design, bfs, dfs, hard]
---
# 30. Serialize and De-serialize BT

← [Construct a BT from Postorder and Inorder](29-build-from-postorder-inorder.md) · [Part 24 index](README.md) · Next → [Morris Inorder Traversal](31-morris-inorder.md)

> [!abstract] Problem at a glance
> **Task:** Design `serialize(root) → str` and `deserialize(str) → root` so a round trip reproduces the tree exactly.
> **Key insight:** A traversal **with explicit null markers** is self-delimiting, so one sequence is enough and you don't need inorder. Level order with `#` for null (Striver's version) or preorder with `#` both work. The decoder replays the same traversal, consuming one token per slot.
> **Difficulty:** Hard · **Pattern:** Traversal + null sentinels · **Also on:** [LC 297](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/serialize-and-de-serialize-bt?category=construction-problems&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Preorder DFS with '#'](#3-preorder-dfs-with-) · [4. Level order with '#'](#4-level-order-with-) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Design an algorithm to serialize a binary tree to a string and deserialize the string back to the original tree structure. There is no restriction on the format; only the round trip must be lossless.

| Input | Output | Why |
|---|---|---|
| `root = [1,2,3,null,null,4,5]` | `[1,2,3,null,null,4,5]` | deserialize(serialize(root)) has the same shape and values |

**Constraints:** `0 ≤ n ≤ 10⁴`; `−1000 ≤ val ≤ 1000` (negatives → use a delimiter, not fixed width).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Preorder DFS with '#' | 'v,' for node, '#,' for null; decode recursively from an iterator | O(n) | O(n) |
| Level order with '#' | BFS writes every child slot; decoder BFS pops two tokens per node | O(n) | O(n) |

> [!tip] Interview angle
> Ask whether the codec must be stateless (yes: no globals). Pick a delimiter so negative and multi-digit values are safe. Preorder + `#` is the shortest to write. BFS avoids recursion depth issues on skewed trees with 10⁴ nodes. For a BST you can drop the null markers (bounds decoding).

---

## 3. Preorder DFS with '#'

**Intuition.** Preorder plus nulls determines the tree: each token is either a leaf-null or a root whose two subtrees follow.

```python
class CodecDFS:
    def serialize(self, root):
        out = []
        def go(n):
            if not n:
                out.append('#')
                return
            out.append(str(n.val))
            go(n.left)
            go(n.right)
        go(root)
        return ','.join(out)

    def deserialize(self, data):
        it = iter(data.split(','))
        def go():
            t = next(it)
            if t == '#':
                return None
            n = TreeNode(int(t))
            n.left = go()
            n.right = go()
            return n
        return go()
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Level order with '#'

**Intuition.** The decoder rebuilds in the same BFS order the encoder wrote in. Each dequeued parent consumes exactly two tokens.

**Algorithm**

1. serialize: empty → `''`. BFS from root; for each node write `val`, push both children (even null); write `#` for null.
2. deserialize: empty → null. Split on `,`; root = token 0; queue = [root]; `i = 1`.
3. Pop parent; token `i` → left (if not `#`, enqueue); token `i+1` → right; `i += 2`.

**Dry run** — [1,2,3,null,null,4,5] → '1,2,3,#,#,4,5,#,#,#,#'. Decode: 1 ← (2,3); 2 ← (#,#); 3 ← (4,5); 4, 5 ← (#,#).

**C++**
```cpp
class Codec {
public:
    string serialize(TreeNode* root) {
        if (!root) return "";
        string s;
        queue<TreeNode*> q;
        q.push(root);
        while (!q.empty()) {
            TreeNode* n = q.front(); q.pop();
            if (!n) { s += "#,"; continue; }
            s += to_string(n->val) + ",";
            q.push(n->left);
            q.push(n->right);
        }
        return s;
    }
    TreeNode* deserialize(string data) {
        if (data.empty()) return nullptr;
        stringstream ss(data);
        string tok;
        getline(ss, tok, ',');
        TreeNode* root = new TreeNode(stoi(tok));
        queue<TreeNode*> q;
        q.push(root);
        while (!q.empty()) {
            TreeNode* n = q.front(); q.pop();
            getline(ss, tok, ',');
            if (tok != "#") { n->left = new TreeNode(stoi(tok)); q.push(n->left); }
            getline(ss, tok, ',');
            if (tok != "#") { n->right = new TreeNode(stoi(tok)); q.push(n->right); }
        }
        return root;
    }
};
```

**Java**
```java
static class Codec {
    String serialize(TreeNode root) {
        if (root == null) return "";
        StringBuilder sb = new StringBuilder();
        Queue<TreeNode> q = new LinkedList<>();
        q.add(root);
        while (!q.isEmpty()) {
            TreeNode n = q.poll();
            if (n == null) { sb.append("#,"); continue; }
            sb.append(n.val).append(',');
            q.add(n.left);
            q.add(n.right);
        }
        return sb.toString();
    }
    TreeNode deserialize(String data) {
        if (data.isEmpty()) return null;
        String[] t = data.split(",");
        TreeNode root = new TreeNode(Integer.parseInt(t[0]));
        Queue<TreeNode> q = new LinkedList<>();
        q.add(root);
        int i = 1;
        while (!q.isEmpty()) {
            TreeNode n = q.poll();
            if (!t[i].equals("#")) { n.left = new TreeNode(Integer.parseInt(t[i])); q.add(n.left); }
            if (!t[i + 1].equals("#")) { n.right = new TreeNode(Integer.parseInt(t[i + 1])); q.add(n.right); }
            i += 2;
        }
        return root;
    }
}
```

**Python**
```python
from collections import deque

class Codec:
    def serialize(self, root):
        if not root:
            return ''
        out, q = [], deque([root])
        while q:
            n = q.popleft()
            if not n:
                out.append('#')
                continue
            out.append(str(n.val))
            q.append(n.left)
            q.append(n.right)
        return ','.join(out)

    def deserialize(self, data):
        if not data:
            return None
        t = data.split(',')
        root = TreeNode(int(t[0]))
        q, i = deque([root]), 1
        while q:
            n = q.popleft()
            if t[i] != '#':
                n.left = TreeNode(int(t[i]))
                q.append(n.left)
            if t[i + 1] != '#':
                n.right = TreeNode(int(t[i + 1]))
                q.append(n.right)
            i += 2
        return root
```

**Complexity:** time **O(n)**, space **O(n)** — every node and every null slot (n+1 of them) is written and read once. (Java uses `LinkedList` because `ArrayDeque` rejects nulls.)

---

## Edge cases

- Empty tree → empty string.
- Negative / multi-digit values (delimiter needed).
- Deep skewed tree: the DFS version recurses n deep, the BFS doesn't.

---

## Common mistakes

1. No null markers (preorder alone is ambiguous).
2. Java `ArrayDeque` with null children → NPE.
3. Storing state in fields between calls (codec must be reusable).

---

## Follow-ups

1. Serialize a BST more compactly?
2. N-ary tree?
3. Why can't preorder alone work without nulls?

<details><summary>Answer sketches</summary>

**#1:** Preorder without nulls; decode with (lo, hi) bounds (LC 449).

**#2:** Write `val, childCount` per node in preorder (LC 428).

**#3:** Different shapes share a preorder: [1,2] as left or right child.
</details>

---

## Flashcards

**Serialize BT: what makes one traversal enough?** #flashcard
Explicit null markers.

**Level-order deserialize: tokens per parent?** #flashcard
Exactly two (left, right), '#' for null.

**Java queue that accepts null?** #flashcard
LinkedList (ArrayDeque throws).

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
