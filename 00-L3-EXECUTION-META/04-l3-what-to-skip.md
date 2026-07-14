---
tags: [l3-google, meta, scope]
topic: What to Skip at L3
---

# What to Skip at Google L3

> **Read this once** so you do not waste study time on topics that rarely (or never) appear in L3 coding rounds.

Full T3 table with every skipped topic: [Tier 3 — Overkill for L3](../coding/l3-google-roadmap.md#tier-3-skip) in the roadmap.

---

## Segment trees & Fenwick trees (BIT)

### Verdict: **not important for L3 — skip implementation practice**

| | |
| :--- | :--- |
| **Do you need to code one?** | No |
| **Do you need to know the name?** | Yes — one sentence is enough |
| **Time to spend** | ~5 min conceptual read, not a study week |

**What they are:** Data structures for **range queries** (sum / min / max over `[l, r]`) with **point updates**, both in O(log n).

**Why L3 skips them:**

- Rare in documented Google L3 loops
- Heavy boilerplate — easy to lose 15+ minutes in a 45-min round
- Almost every L3 “range” problem is solvable with **prefix sum**, **hash map**, **monotonic deque**, or **heap**

### Use this instead (L3 pattern map)

| You hear… | Reach for… |
| :--- | :--- |
| Subarray sum, static array | Prefix sum + hash map (`seen[0]=1`) |
| Max/min in a **sliding window** | Monotonic deque |
| Range sum, **no updates** | Prefix sum only |
| Dynamic connectivity | Union-Find |
| Top-K / merge streams | Heap |

**Interview line (optional):** *“If we had many range updates and simpler structures don’t fit, a segment tree or Fenwick tree would work — but I’d try prefix sum or a deque first.”*

---

## Other topics to skip at L3

| Topic | L3 action |
| :--- | :--- |
| System design, LLD, SQL, concurrency | Not tested |
| Tarjan / Kosaraju SCC, Floyd-Warshall | Skip entirely |
| Bit manipulation deep-dives, bitmask DP, digit DP | Skim concept only |
| Divide & conquer as a dedicated topic | Merge sort lives in sorting reference only |

---

## What changes at L4 (SDE-2)

The skip list barely shrinks — the *bar* on the kept topics rises. Full details: [L4 delta](../coding/l4-sde2-delta.md).

**Still skipped at L4:** segment trees / BIT implementation, Tarjan/Kosaraju, Floyd-Warshall, bitmask DP, digit DP, system design (appears at L5, not L4 loops).

**Promoted at L4 (T2 → T1):**

| Topic | Why |
| :--- | :--- |
| Dynamic programming (1D/grid/string) | In most L4 loops; follow-ups escalate into DP |
| Dijkstra, including on grids | Min Effort / Swim in Water family is a Google favorite |
| Intervals / sweep line | Calendar & booking problems are classic L4 |
| Design-a-data-structure | LFU, GetRandom O(1), Hit Counter — the L4 signature family |
| String parsing / simulation | Text Justification, calculator-style care problems |

---

## What to prioritize instead

1. Graphs — BFS, DFS, topo, union-find, Dijkstra  
2. Sliding window + two pointers  
3. Binary search (including **search on answer**)  
4. Heaps, tries  
5. Core DP + backtracking  

→ [L3 Roadmap (4-week plan)](../coding/l3-google-roadmap.md) · [DS index](../01-data-structures/README.md) · [Algorithms index](../02-algorithms/README.md)
