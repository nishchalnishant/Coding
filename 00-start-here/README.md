# Start Here — Google SDE-2 (L4) Prep Hub

**Goal:** Crack Google SDE-2 (L4) in a 4–6 week sprint.  
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
| `01-data-structures/` | 12 DS deep-dive files (arrays → segment trees) + topic index |
| `02-algorithms/` | Algorithm deep-dives + standalone technique files |
| `03-patterns/` | Pattern master, cheatsheets, revision guides, LC variants, system design |
| `04-behavioral/` | Google's 4 attributes + STAR story index |
| `05-revision/` | Complexity tables, Python gotchas, day-before checklist, coding rubric |
| `books/` | Algorithm design deep dives, CP3, DP book summaries |

---

## Recommended 4-Week Study Order

| Week | Topics | Files |
|------|--------|-------|
| **Week 1** | Arrays, Strings, Hashing, Linked Lists | `01-data-structures/array.md`, `01-data-structures/hashing.md`, `01-data-structures/linked-list.md` + `02-algorithms/two-pointers.md`, `02-algorithms/sliding-window.md` |
| **Week 2** | Trees, BST, Graphs, BFS/DFS | `01-data-structures/tree.md`, `01-data-structures/graphs.md`, `02-algorithms/graph.md`, `02-algorithms/advanced-graphs.md` |
| **Week 3** | DP, Backtracking, Greedy, Recursion | `02-algorithms/dynamic-programming/`, `02-algorithms/backtracking.md`, `02-algorithms/greedy.md`, `02-algorithms/recursion/` |
| **Week 4** | Binary Search, Heap, Tries, Behavioral | `02-algorithms/binary-search.md`, `01-data-structures/heap.md`, `01-data-structures/trie.md`, `04-behavioral/` |

> **If you have 6 weeks:** Add a Week 5 (Segment Trees, Union-Find, Bit Manipulation, Math) and Week 6 (full mock interviews + revision).

---

## Key Files — Quick Access

| What | Link |
|------|------|
| Pattern recognition master | `03-patterns/patterns-master.md` |
| Interview cheatsheet | `03-patterns/interview-cheatsheet.md` |
| Google revision guide | `03-patterns/GOOGLE_INTERVIEW_REVISION.md` |
| Complexity + syntax quick sheet | `05-revision/README.md` |
| Behavioral STAR stories | `04-behavioral/behavioral.md` |
| System design guide | `03-patterns/system-design.md` |

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
