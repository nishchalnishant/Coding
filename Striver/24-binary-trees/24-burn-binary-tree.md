---
module: striver/24-binary-trees
lesson: 24
topic: Minimum time taken to burn the BT from a given Node
difficulty: Hard
source: https://takeuforward.org/learning/dsa/minimum-time-taken-to-burn-the-bt-from-a-given-node?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, bfs, parent-map, graph, hard]
---
# 24. Minimum time taken to burn the BT from a given Node

← [Print all the Nodes at a distance of K in a BT](23-all-nodes-distance-k.md) · [Part 24 index](README.md) · Next → [Count total Nodes in a COMPLETE BT](25-count-complete-tree-nodes.md)

> [!abstract] Problem at a glance
> **Task:** Fire spreads 1 edge per minute (to children and parent). Minutes until every node burns, starting at value `start`.
> **Key insight:** The answer is the **eccentricity** of the start node, its farthest distance in the tree. Build parent pointers and run a level BFS from the start. The number of rounds after the first is the answer.
> **Difficulty:** Hard · **Pattern:** Parent map + multi-round BFS · **Also on:** [LC 2385](https://leetcode.com/problems/amount-of-time-for-binary-tree-to-be-infected/) · [GfG](https://www.geeksforgeeks.org/problems/burning-tree/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimum-time-taken-to-burn-the-bt-from-a-given-node?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Parent map + BFS](#3-parent-map--bfs) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a binary tree with unique values and a `start` value, the node with value `start` catches fire at minute 0. Each minute, fire spreads from every burning node to its adjacent nodes (children and parent). Return the number of minutes until the whole tree is burnt.

| Input | Output | Why |
|---|---|---|
| `root = [1,5,3,null,4,10,6,9,2], start = 3` | `4` | 3 → {1,10,6} → {5} → {4} → {9,2} |
| `root = [1], start = 1` | `0` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`; unique values.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Parent map + BFS | find start + parents, BFS over {L, R, parent} counting rounds | O(n) | O(n) |

> [!tip] Interview angle
> It's distance-K again: count rounds until the queue empties instead of stopping at k. The one-pass DFS (combining depth and distance-to-start) is an elegant O(n)/O(h) alternative, but explaining it under pressure is risky. Lead with the BFS.

---

## 3. Parent map + BFS

**Intuition.** Each BFS round is one minute. Count the rounds in which at least one new node catches fire.

**Algorithm**

1. DFS from root: fill `par`, locate `start` node.
2. BFS from start with `seen`.
3. Each round: expand the level; if anything new was enqueued, `t += 1`.
4. Return `t`.

**Dry run** — start 3: round1 {1,10,6} t=1; round2 {5} t=2; round3 {4} t=3; round4 {9,2} t=4; round5 none → 4.

**C++**
```cpp
int amountOfTime(TreeNode* root, int start) {
    unordered_map<TreeNode*, TreeNode*> par;
    TreeNode* src = nullptr;
    vector<TreeNode*> st{root};
    while (!st.empty()) {
        TreeNode* n = st.back(); st.pop_back();
        if (n->val == start) src = n;
        for (TreeNode* c : {n->left, n->right})
            if (c) { par[c] = n; st.push_back(c); }
    }
    queue<TreeNode*> q;
    unordered_set<TreeNode*> seen{src};
    q.push(src);
    int t = 0;
    while (!q.empty()) {
        bool spread = false;
        int sz = q.size();
        while (sz--) {
            TreeNode* n = q.front(); q.pop();
            for (TreeNode* m : {n->left, n->right, par.count(n) ? par[n] : nullptr})
                if (m && !seen.count(m)) { seen.insert(m); q.push(m); spread = true; }
        }
        if (spread) t++;
    }
    return t;
}
```

**Java**
```java
static int amountOfTime(TreeNode root, int start) {
    Map<TreeNode, TreeNode> par = new HashMap<>();
    TreeNode src = null;
    Deque<TreeNode> st = new ArrayDeque<>();
    st.push(root);
    while (!st.isEmpty()) {
        TreeNode n = st.pop();
        if (n.val == start) src = n;
        for (TreeNode c : new TreeNode[]{n.left, n.right})
            if (c != null) { par.put(c, n); st.push(c); }
    }
    Queue<TreeNode> q = new ArrayDeque<>();
    Set<TreeNode> seen = new HashSet<>();
    q.add(src); seen.add(src);
    int t = 0;
    while (!q.isEmpty()) {
        boolean spread = false;
        int sz = q.size();
        while (sz-- > 0) {
            TreeNode n = q.poll();
            for (TreeNode m : new TreeNode[]{n.left, n.right, par.get(n)})
                if (m != null && seen.add(m)) { q.add(m); spread = true; }
        }
        if (spread) t++;
    }
    return t;
}
```

**Python**
```python
from collections import deque

def burn_time(root, start):
    par, st, src = {}, [root], None
    while st:
        n = st.pop()
        if n.val == start:
            src = n
        for c in (n.left, n.right):
            if c:
                par[c] = n
                st.append(c)
    q, seen, t = deque([src]), {src}, 0
    while q:
        spread = False
        for _ in range(len(q)):
            n = q.popleft()
            for m in (n.left, n.right, par.get(n)):
                if m and m not in seen:
                    seen.add(m)
                    q.append(m)
                    spread = True
        t += spread
    return t
```

**Complexity:** time **O(n)**, space **O(n)** — each node enters the queue once.

---

## Edge cases

- Single node → 0.
- Start at a leaf deep on one side: fire must climb, then descend the other side.
- Start is the root → answer = height − 1 (edges).

---

## Common mistakes

1. Counting the final empty round (off by one): only count rounds that ignite something.
2. Forgetting the parent edge (the answer becomes 'height below start').

---

## Follow-ups

1. One-pass DFS?
2. Multiple fire sources?

<details><summary>Answer sketches</summary>

**#1:** Return depth normally; once the start is found, return −(dist to start) and combine `dist + other-side depth` at ancestors.

**#2:** Multi-source BFS: start the queue with all of them.
</details>

---

## Flashcards

**Burn tree answer = ?** #flashcard
Max distance from start (eccentricity) — BFS rounds over {L, R, parent}.

**Burn tree off-by-one?** #flashcard
Increment time only when a round ignites a new node.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
