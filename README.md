# Google L3 (SWE) Interview Prep

Topic-first prep for **Google L3** coding loops: 4–5 rounds, one medium problem each, 35–45 minutes. Dense notes, curated must-solve lists, no 500-problem grind.

> **Segment trees & Fenwick trees are not L3 material** — do not drill them. Use prefix sum, deque, or heap instead. Details: [What to Skip at L3](00-start-here/L3_CHEATSHEET.md)

---

## What this repo covers

| Area | Topics | Where |
|---|---|---|
| **Data structures** | array, hashing, string, matrix/grid, stack, queue/deque, linked list, tree/BST, trie, heap, graph | [`01-data-structures/`](01-data-structures/README.md) |
| **Algorithms** | sorting, string matching, two pointers, sliding window, recursion, recursion → DP, binary search, backtracking, union-find, DP (9 patterns), greedy/intervals, bit manipulation & math (interview depth) | [`02-algorithms/`](02-algorithms/README.md) |
| **Practice bank** | 128 walkthrough problems, tier-tagged, one file per topic + design-a-data-structure | [`04-practice/`](04-practice/README.md) |
| **Thinking & patterns** | first-principles derivation, pattern triggers, ladders, in-interview judgment, mocks | [`03-patterns/`](03-patterns/README.md) |
| **Behavioral** | Googliness attributes, STAR story bank | [`05-behavioral/`](05-behavioral/README.md) |
| **Round execution** | 45-min clock, constraint → Big-O, edge cases, what to skip | [L3 Cheatsheet](00-start-here/L3_CHEATSHEET.md) |

**Not in scope:** system design, LLD, concurrency, SQL, **segment trees / Fenwick trees**, advanced graphs (Floyd-Warshall, Tarjan/SCC), bitmask/digit DP — see [What to Skip at L3](00-start-here/L3_CHEATSHEET.md).

**Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](00-start-here/l3-google-roadmap.md#tier-legend)). L4/senior bars layer on top via the [L4 delta](00-start-here/l4-sde2-delta.md) and [senior delta](00-start-here/sde3-senior-delta.md).

---

## How every lecture is laid out

1. **What this covers**: scope, what you'll be able to do, prereqs, paired practice file, time budget, section links.
2. **First-Principles Map / Breakdown**: why the structure or technique exists, its invariant, where it breaks.
3. **Theory → techniques → templates**: the mental model, then code templates with complexity.
4. **Interview questions, logic & traps**, then **Quick Revision Triggers** and flashcards.

Each concept file (`01-`, `02-`) links to its practice file in `04-practice/` and the practice file links back.

---

## Start here: study path

| Step | Do | Link |
|---|---|---|
| 1 | Read the plan and the round clock | [L3 roadmap](00-start-here/l3-google-roadmap.md) · [L3 Cheatsheet](00-start-here/L3_CHEATSHEET.md) |
| 2 | Learn how to derive patterns | [How to Think](03-patterns/HOW_TO_THINK.md) |
| 3 | Per topic: lecture, then the practice file, T1 first | [DS index](01-data-structures/README.md) · [Algo index](02-algorithms/README.md) |
| 4 | Recursion & DP from zero | [Masterclass](03-patterns/RECURSION_AND_DP_MASTERCLASS.md) |
| 5 | Pressure-test with ladders and mocks | [Pattern Ladders](03-patterns/PATTERN_LADDERS.md) · [Mock set](03-patterns/MOCK_INTERVIEW_SET.md) · [Interview Judgment](03-patterns/INTERVIEW_JUDGMENT.md) |
| 6 | Behavioral stories | [Behavioral + Googliness](05-behavioral/BEHAVIORAL_GOOGLINESS.md) |
| 7 | Final week | [Revision guide](03-patterns/GOOGLE_INTERVIEW_REVISION.md) · [Mind map](03-patterns/maps/mindmap.md) |

---

## Quick revision

| What | Link |
|------|------|
| Mind map | [`mindmap.md`](03-patterns/maps/mindmap.md) |
| Flowcharts | [`flowcharts.md`](03-patterns/maps/flowcharts.md) |
| Pattern triggers | [`03-patterns/patterns-master.md`](03-patterns/patterns-master.md) |
| Full problem index (128, by topic) | [`04-practice/README.md`](04-practice/README.md) |
| Interview strategy / day-of revision | [`03-patterns/GOOGLE_INTERVIEW_REVISION.md`](03-patterns/GOOGLE_INTERVIEW_REVISION.md) |
| L4 (SDE-2) delta | [`00-start-here/l4-sde2-delta.md`](00-start-here/l4-sde2-delta.md) |
| SDE-3 / senior delta | [`00-start-here/sde3-senior-delta.md`](00-start-here/sde3-senior-delta.md) |
| Senior follow-up chains | [`03-patterns/SENIOR_FOLLOWUPS.md`](03-patterns/SENIOR_FOLLOWUPS.md) |
| Decision trees, pattern triggers, problem recognition | [`03-patterns/maps/`](03-patterns/maps/) |
| Striver A2Z course notes (lesson-by-lesson) | [`striver-a2z/`](striver-a2z/README.md) |

### Flashcards (147 cards, spaced repetition)

Every lecture ends with a `## Flashcards` section. A card is a bold question line tagged `#flashcard`, followed by the answer up to the next blank line:

```
**What does `lps[i]` mean in KMP?** #flashcard
Longest proper prefix of pattern[:i+1] that is also a suffix…
```

- **Anki:** export every card to a tab-separated file, then *File → Import* into a Basic note type with "Allow HTML" on. Multi-line answers are joined with `<br>`.
  ```sh
  grep -rl --include='*.md' '#flashcard$' . | xargs awk '/#flashcard$/{if(q)print q"\t"a; q=$0; sub(/ *#flashcard$/,"",q); a=""; next} q&&/^(---)?$/{if(a!=""){print q"\t"a; q=""}; next} q{a=(a==""?$0:a"<br>"$0)} END{if(q)print q"\t"a}' > flashcards.tsv
  ```
- **Obsidian:** filter with tag search `tag:#flashcard` to review in-vault. The Spaced Repetition plugin expects `?` / `::` separators, so the Anki export is the supported route for scheduled review.

---

## 4-week overview

| Week | Focus |
|------|-------|
| **1** | Arrays, hashing, graphs (BFS/DFS), two pointers, sliding window |
| **2** | Heaps, tries, queues, binary search (incl. search on answer) |
| **3** | Trees, stacks, linked lists, union-find, greedy |
| **4** | Core DP, backtracking, recursion + **4–6 timed mocks** + behavioral |

Full daily plan: [`00-start-here/l3-google-roadmap.md`](00-start-here/l3-google-roadmap.md)
