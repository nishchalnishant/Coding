# Start Here — Google SDE-3 (L5) Prep Hub

**Goal:** Crack Google SDE-3 (L5) in a 6-week sprint.  
**Approach:** Topic-first navigation — pick a DS or algorithm category, read the deep-dive, drill problems, repeat.

---

## How to Use This Repo

1. **Don't read linearly.** Navigate by topic. Use the directory map below to jump to what you need.
2. **Pattern recognition first.** Before drilling problems, read `03-patterns/patterns-master.md` to learn *when* to use each technique.
3. **Dense > broad.** Spend 90 minutes going deep on one topic rather than 15 minutes skimming six.
4. **Track mistakes.** After each session, note what tripped you — edge cases, boundary conditions, off-by-ones.

---

## Directory Map

| Folder | Purpose |
|--------|---------|
| `00-start-here/` | This file. Navigation hub. |
| `01-data-structures/` | DS deep-dives + **[README index](01-data-structures/README.md)** (study order, L4 priorities, how to read each file) |
| `02-algorithms/` | Algorithm deep-dives + **[README index](02-algorithms/README.md)** (technique map, DP/recursion hubs) |
| `03-patterns/` | Pattern master, cheatsheets, revision guides, LC variants, system design |
| `04-behavioral/` | Google's 4 attributes + STAR story index |
| `05-revision/` | Complexity tables, Python gotchas, day-before checklist, coding rubric |
| `books/` | Algorithm design deep dives, CP3, DP book summaries |

---

## 6-Week SDE-3 Study Plan

| Week | Topics | Files |
|------|--------|-------|
| **Week 1** | Arrays, Strings, Hashing, Linked Lists | `01-data-structures/array.md`, `01-data-structures/hashing.md`, `01-data-structures/linked-list.md` + `02-algorithms/two-pointers.md`, `02-algorithms/sliding-window.md` |
| **Week 2** | Trees, BST, Graphs, BFS/DFS | `01-data-structures/tree.md`, `01-data-structures/graphs.md`, `02-algorithms/graph.md`, `02-algorithms/advanced-graphs.md` |
| **Week 3** | DP, Backtracking, Greedy, Recursion | `02-algorithms/dynamic-programming.md`, `02-algorithms/recursion-to-dp.md`, `02-algorithms/backtracking.md`, `02-algorithms/greedy.md`, `02-algorithms/recursion.md` |
| **Week 4** | Binary Search, Heap, Tries, Segment Tree, Union-Find, Bit Manipulation | `02-algorithms/binary-search.md`, `01-data-structures/heap.md`, `01-data-structures/trie.md`, `01-data-structures/segment-tree.md`, `02-algorithms/union-find.md` |
| **Week 5** | SDE-3 Hard Problems — full checklist | `05-revision/coding-rubric.md` §SDE-3 Hard Problem Checklist; log every attempt in `05-revision/mock-log.md` |
| **Week 6** | Mock interviews (2/week minimum), LLD round prep, behavioral polish | `03-patterns/lld.md`, `04-behavioral/behavioral.md`, `03-patterns/system-design.md` |

> **SDE-3 bar:** Mediums fluent, hards cold in < 25 min, system design at scale, LLD + SOLID, leadership signals in behavioral.

---

## Key Files — Quick Access

| What | Link |
|------|------|
| **Repo flowcharts (visual map)** | `FLOWCHARTS.md` |
| **Mind map (30-min DS/algo revision)** | [`MINDMAP.md`](../MINDMAP.md) |
| **Practice problem bank** | [`coding/`](../coding/) — see GitBook sidebar **Practice Problem Bank** |
| Pattern recognition master | `03-patterns/patterns-master.md` |
| Interview cheatsheet | `03-patterns/interview-cheatsheet.md` |
| Google revision guide | `03-patterns/GOOGLE_INTERVIEW_REVISION.md` |
| SDE-3 DSA completeness addendum | `coding/sde3-dsa-completeness.md` |
| Complexity + syntax quick sheet | `05-revision/README.md` |
| Behavioral STAR stories | `04-behavioral/behavioral.md` |
| System design guide | `03-patterns/system-design.md` |
| LLD guide (OOP/design patterns) | `03-patterns/lld.md` |
| Mock interview log | `05-revision/mock-log.md` |
| SDE-3 hard checklist + annotations | `05-revision/coding-rubric.md` |

---

## 48-Hour Sprint

If you have 48 hours before the interview:

**Hour 0–8**
- Read `03-patterns/patterns-master.md` end-to-end
- Drill 1 easy + 1 medium per pattern (Two Pointers, Sliding Window, Binary Search, BFS/DFS, DP)

**Hour 8–16**
- `05-revision/README.md` — complexity table + Python syntax gotchas
- `03-patterns/GOOGLE_QUICK_SHEET.md`
- `03-patterns/system-design.md` — review key stubs

**Hour 16–24**
- 3 full mock problems (timed, 35 min each): one DP, one Graph, one free choice
- `04-behavioral/behavioral.md` — rehearse 3 STAR stories aloud

**Hour 24–48**
- Sleep 8 hours
- Light review: patterns cheatsheet, complexity table
- Don't learn new topics

---

## Interview Day — Final 30 Minutes

Read in this order (skim, don't study):

1. `03-patterns/interview-cheatsheet.md` — pattern triggers
2. `05-revision/README.md` — complexity table + Python gotchas
3. Your 3 behavioral STAR stories (just titles + outcomes)

**Do NOT:** re-read DP recurrences, re-study graph algorithms, or open new files.
