---
module: striver/27-graphs
lesson: 40
topic: Accounts merge
difficulty: Medium
source: https://takeuforward.org/learning/dsa/accounts-merge?category=hard-problems-ii&source=strivers-a2z-dsa-sheet
tags: [striver, graph, union-find, hashing, strings]
---
# 40. Accounts merge

← [Number of operations to make network connected](39-number-of-operations-to-make-network-connected.md) · [Part 27 index](README.md) · Next → [Number of islands II](41-number-of-islands-ii.md)

> [!abstract] Problem at a glance
> **Task:** Merge accounts that share any email; return each person's name followed by their sorted emails.
> **Key insight:** Accounts are nodes; a shared email is an edge. Map each email to the **first account index** that owned it and union later owners into it. Then group every email by `find(owner)` and sort each group. Same names alone never merge.
> **Difficulty:** Medium · **Pattern:** DSU over indices, keyed by a hash map · **Also on:** LC 721
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/accounts-merge?category=hard-problems-ii&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DFS on the email graph](#3-dfs-on-the-email-graph) · [4. DSU on account indices](#4-dsu-on-account-indices) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`accounts[i] = [name, email1, email2, …]`. Two accounts belong to the same person if they share an email (transitively). Accounts with the same name may belong to different people. Return the merged accounts: `[name, sorted emails…]`, in any order.

| Input | Output | Why |
|---|---|---|
| `[["John","js@m","jny@m"],["John","js@m","j00@m"],["Mary","m@m"],["John","jb@m"]]` | `[["John","j00@m","jny@m","js@m"],["Mary","m@m"],["John","jb@m"]]` | first two share js@m; the third John is a different person |

**Constraints:** `1 ≤ accounts.length ≤ 1000`, `2 ≤ accounts[i].length ≤ 10`, emails up to 30 chars.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DFS on the email graph | link each account's emails to its first email; DFS components | O(N log N) | O(N) |
| DSU on account indices | email → first owner; union owners; group emails by root | O(N log N) | O(N) |

> [!tip] Interview angle
> The trap is merging by name. Say 'union account indices through an email → owner map', which keeps the DSU size at n accounts instead of all emails. Mention the DFS-on-email-graph alternative and that both are O(N·α + N log N) with the sort dominating.

---

## 3. DFS on the email graph

**Intuition.** Build an undirected graph on emails: connect every email of an account to that account's first email. Each connected component is one person; DFS it, sort, and prefix the name.

```python
from collections import defaultdict

def accounts_merge_dfs(accounts):
    adj, name = defaultdict(list), {}
    for acc in accounts:
        first = acc[1]
        for e in acc[1:]:
            adj[first].append(e)
            adj[e].append(first)
            name[e] = acc[0]
    seen, out = set(), []
    for e in name:
        if e in seen:
            continue
        seen.add(e)
        st, comp = [e], []
        while st:
            u = st.pop()
            comp.append(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    st.append(v)
        out.append([name[e]] + sorted(comp))
    return out
```

**Complexity:** time **O(N log N)**, space **O(N)**.

---

## 4. DSU on account indices

**Intuition.** Walk accounts in order. For each email: if unseen, record `owner[email] = i`; if seen, `union(i, owner[email])`. Afterwards every email belongs to `find(owner[email])`. Collect, sort each list, prefix `accounts[root][0]`.

**Algorithm**

1. DSU over `n` account indices; empty map `owner`.
2. For each account `i`, each email `e`: `owner[e]` exists → union; else set it.
3. `groups[find(owner[e])].append(e)` for every email.
4. For each root: `[accounts[root][0]] + sorted(group)`.

**Dry run** — Example: account 0 claims js, jny. Account 1 sees js → union(1, 0); claims j00. Mary claims m. Account 3 claims jb. Roots: {0: js, jny, j00}, {2: m}, {3: jb}.

**C++**
```cpp
vector<vector<string>> accountsMerge(vector<vector<string>>& accounts) {
    int n = accounts.size();
    vector<int> parent(n);
    iota(parent.begin(), parent.end(), 0);
    function<int(int)> find = [&](int x) { return parent[x] == x ? x : parent[x] = find(parent[x]); };
    unordered_map<string, int> owner;
    for (int i = 0; i < n; i++)
        for (int j = 1; j < (int)accounts[i].size(); j++) {
            auto it = owner.find(accounts[i][j]);
            if (it == owner.end()) owner[accounts[i][j]] = i;
            else parent[find(i)] = find(it->second);
        }
    vector<vector<string>> groups(n);
    for (auto& [e, i] : owner) groups[find(i)].push_back(e);
    vector<vector<string>> out;
    for (int r = 0; r < n; r++) {
        if (groups[r].empty()) continue;
        sort(groups[r].begin(), groups[r].end());
        vector<string> row{accounts[r][0]};
        row.insert(row.end(), groups[r].begin(), groups[r].end());
        out.push_back(row);
    }
    return out;
}
```

**Java**
```java
static int[] parent;
static int find(int x) { return parent[x] == x ? x : (parent[x] = find(parent[x])); }
static List<List<String>> accountsMerge(String[][] accounts) {
    int n = accounts.length;
    parent = new int[n];
    for (int i = 0; i < n; i++) parent[i] = i;
    Map<String, Integer> owner = new HashMap<>();
    for (int i = 0; i < n; i++)
        for (int j = 1; j < accounts[i].length; j++) {
            Integer o = owner.get(accounts[i][j]);
            if (o == null) owner.put(accounts[i][j], i);
            else parent[find(i)] = find(o);
        }
    Map<Integer, List<String>> groups = new HashMap<>();
    for (Map.Entry<String, Integer> en : owner.entrySet())
        groups.computeIfAbsent(find(en.getValue()), k -> new ArrayList<>()).add(en.getKey());
    List<List<String>> out = new ArrayList<>();
    for (Map.Entry<Integer, List<String>> g : groups.entrySet()) {
        List<String> emails = g.getValue();
        Collections.sort(emails);
        List<String> row = new ArrayList<>();
        row.add(accounts[g.getKey()][0]);
        row.addAll(emails);
        out.add(row);
    }
    return out;
}
```

**Python**
```python
from collections import defaultdict

def accounts_merge(accounts):
    n = len(accounts)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    owner = {}
    for i, acc in enumerate(accounts):
        for e in acc[1:]:
            if e in owner:
                parent[find(i)] = find(owner[e])
            else:
                owner[e] = i
    groups = defaultdict(list)
    for e, i in owner.items():
        groups[find(i)].append(e)
    return [[accounts[r][0]] + sorted(es) for r, es in groups.items()]
```

**Complexity:** time **O(N log N)**, space **O(N)** — N = total emails; sorting the groups dominates the near-linear DSU pass.

---

## Edge cases

- Two different people with the same name: separate rows.
- Duplicate email inside one account: the map dedupes it.
- Chain merges (A–B via e1, B–C via e2): transitivity handled by DSU.

---

## Common mistakes

1. Merging accounts by name.
2. Unioning `i` with `owner[e]` but then grouping by `owner[e]` instead of `find(owner[e])`.
3. Forgetting to sort emails, or sorting the name into them.

---

## Follow-ups

1. 10⁸ accounts across machines?
2. Stream of new accounts?

<details><summary>Answer sketches</summary>

**#1:** Shard by email hash, emit (email, account) pairs, run distributed connected components (iterative label propagation).

**#2:** DSU is incremental: process each new account as it arrives; merges never need undoing.
</details>

---

## Flashcards

**Accounts merge DSU nodes?** #flashcard
Account indices; emails map to their first owner.

**Accounts merge trap?** #flashcard
Same name ≠ same person; only shared emails merge.

**Interview track →** [Union-find deep-dive](../../02-algorithms/14-union-find.md)
