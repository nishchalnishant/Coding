---
module: striver-a2z/24-binary-trees
lesson: 23
topic: Print all the Nodes at a distance of K in a BT
difficulty: Medium
source: https://takeuforward.org/learning/dsa/print-all-the-nodes-at-a-distance-of-k-in-a-bt?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, bfs, parent-map, graph]
---
# 23. Print all the Nodes at a distance of K in a BT

← [Maximum width of a Binary Tree](22-maximum-width.md) · [Part 24 index](README.md) · Next → [Minimum time taken to burn the BT from a given Node](24-burn-binary-tree.md)

> [!abstract] Problem at a glance
> **Task:** Values of all nodes exactly `k` edges from `target`, sorted ascending.
> **Key insight:** A tree is an undirected graph whose edges to parents are missing. **Add parent pointers** (one BFS/DFS into a hash map), then BFS from `target` for `k` rounds, moving to left, right and parent with a visited set.
> **Difficulty:** Medium · **Pattern:** Parent map + BFS · **Also on:** [LC 863](https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/print-all-the-nodes-at-a-distance-of-k-in-a-bt?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Parent map + BFS from target](#3-parent-map--bfs-from-target) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a binary tree, a `target` node and an integer `k`, return the values of all nodes at distance `k` from the target node. (LC accepts any order; this note returns them sorted.)

| Input | Output | Why |
|---|---|---|
| `root = [3,5,1,6,2,0,8,null,null,7,4], target = 5, k = 2` | `[1,4,7]` | 7 and 4 below; 1 via the parent 3 |

**Constraints:** `1 ≤ n ≤ 500`; unique values; `0 ≤ k ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Parent map + BFS from target | map child→parent, then K BFS rounds over {L, R, parent} | O(n) | O(n) |

> [!tip] Interview angle
> Name the transformation: tree → graph via parent pointers. The same idea solves 'burn the tree' and 'min time to infect'. A DFS-only alternative returns the distance-to-target from each subtree and collects nodes at `k − d − 1` on the other side. Mention it as a bonus.

---

## 3. Parent map + BFS from target

**Intuition.** With parents, every node has up to three neighbours. Level `k` of a BFS from target is the answer.

**Algorithm**

1. BFS/DFS from root filling `par[child] = node`.
2. BFS from `target` with `seen = {target}`; repeat `k` times: expand every node in the level to its unseen L, R, parent.
3. Return the values of the remaining queue (sorted).

**Dry run** — target 5, k=2: L0 {5}; L1 {6,2,3}; L2 {7,4,1} → [1,4,7].

**C++**
```cpp
vector<int> distanceK(TreeNode* root, TreeNode* target, int k) {
    unordered_map<TreeNode*, TreeNode*> par;
    vector<TreeNode*> st{root};
    while (!st.empty()) {
        TreeNode* n = st.back(); st.pop_back();
        for (TreeNode* c : {n->left, n->right})
            if (c) { par[c] = n; st.push_back(c); }
    }
    queue<TreeNode*> q;
    unordered_set<TreeNode*> seen{target};
    q.push(target);
    while (k-- > 0 && !q.empty()) {
        int sz = q.size();
        while (sz--) {
            TreeNode* n = q.front(); q.pop();
            for (TreeNode* m : {n->left, n->right, par.count(n) ? par[n] : nullptr})
                if (m && !seen.count(m)) { seen.insert(m); q.push(m); }
        }
    }
    vector<int> res;
    while (!q.empty()) { res.push_back(q.front()->val); q.pop(); }
    sort(res.begin(), res.end());
    return res;
}
```

**Java**
```java
static List<Integer> distanceK(TreeNode root, TreeNode target, int k) {
    Map<TreeNode, TreeNode> par = new HashMap<>();
    Deque<TreeNode> st = new ArrayDeque<>();
    st.push(root);
    while (!st.isEmpty()) {
        TreeNode n = st.pop();
        for (TreeNode c : new TreeNode[]{n.left, n.right})
            if (c != null) { par.put(c, n); st.push(c); }
    }
    Queue<TreeNode> q = new ArrayDeque<>();
    Set<TreeNode> seen = new HashSet<>();
    q.add(target); seen.add(target);
    while (k-- > 0 && !q.isEmpty()) {
        int sz = q.size();
        while (sz-- > 0) {
            TreeNode n = q.poll();
            for (TreeNode m : new TreeNode[]{n.left, n.right, par.get(n)})
                if (m != null && seen.add(m)) q.add(m);
        }
    }
    List<Integer> res = new ArrayList<>();
    for (TreeNode n : q) res.add(n.val);
    Collections.sort(res);
    return res;
}
```

**Python**
```python
from collections import deque

def distance_k(root, target, k):
    par, st = {}, [root]
    while st:
        n = st.pop()
        for c in (n.left, n.right):
            if c:
                par[c] = n
                st.append(c)
    q, seen = deque([target]), {target}
    for _ in range(k):
        for _ in range(len(q)):
            n = q.popleft()
            for m in (n.left, n.right, par.get(n)):
                if m and m not in seen:
                    seen.add(m)
                    q.append(m)
    return sorted(n.val for n in q)
```

**Complexity:** time **O(n)**, space **O(n)** — parent pass O(n) + BFS O(n); sorting the output adds O(m log m).

---

## Edge cases

- `k = 0` → `[target]`.
- `k` larger than any distance → `[]`.
- Target is the root (no parent).

---

## Common mistakes

1. No visited set: BFS bounces between a node and its parent forever.
2. Stopping when the queue empties but still returning stale contents (guard `k-- > 0 && !q.empty()`).
3. Keying the parent map by value when duplicates are possible.

---

## Follow-ups

1. Without a parent map?
2. Min time to burn the tree?

<details><summary>Answer sketches</summary>

**#1:** DFS returns dist-to-target; at an ancestor with distance d, collect nodes at depth k−d−1 in the other subtree.

**#2:** Same BFS; count rounds until the queue is empty.
</details>

---

## Flashcards

**Tree → graph trick?** #flashcard
Store parent pointers in a hash map; BFS over {left, right, parent}.

**Why the visited set in distance-K?** #flashcard
Parent edges make the graph undirected — avoid bouncing back.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
