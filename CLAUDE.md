# Coding Interview Prep Hub — CLAUDE.md

## What this repo is
Google **L3 SWE / L4 SDE-2** interview prep: DSA coding rounds + Googliness/behavioral. Base track is L3; `coding/l4-sde2-delta.md` layers the L4 bar on top. All content is Markdown — no source code to build or test.

**Out of scope:** system design, LLD, concurrency, SQL, segment trees, advanced graphs (Tarjan/SCC).

**In scope but capped:** bit manipulation and math/number theory are covered at interview depth (`02-algorithms/17`, `02-algorithms/18`) — common tricks and tier-tagged problems, not deep-dives.

## Directory layout (don't explore, use this)
```
00-L3-EXECUTION-META/    # L3_CHEATSHEET.md — pacing, constraints, decision guide, edge cases, Big-O, skip list
01-data-structures/      # DS deep-dives (array, hashing, string, stack, queue, linked-list, tree, trie, heap, graph)
02-algorithms/           # Algo deep-dives (two-pointers, sliding-window, binary-search, sorting, graph, union-find, greedy, backtracking, string, DP, recursion)
03-patterns/             # Pattern triggers, canonical questions, Google revision
04-behavioral/           # STAR stories, Googliness
coding/                  # Problem walkthrough bank + l3-google-roadmap.md
```

## Common tasks and where to go

| Task | File |
|---|---|
| L3 study schedule | `coding/l3-google-roadmap.md` |
| L4 (SDE-2) delta: bar, tier promotions, gap problems | `coding/l4-sde2-delta.md` |
| Intuition-first pattern curriculum | `03-patterns/PATTERN_LADDERS.md` |
| First-principles pattern thinking guide | `03-patterns/HOW_TO_THINK.md` |
| In-interview judgment: proofs, pivots, hints, recovery | `03-patterns/INTERVIEW_JUDGMENT.md` |
| DS / algo indexes + must-solve | `01-data-structures/README.md`, `02-algorithms/README.md` |
| Add / update a DSA topic | `01-data-structures/` or `02-algorithms/` |
| Add a problem walkthrough | matching file under `coding/data-structures/` or `coding/algorithms/` |
| Add a pattern trigger | `03-patterns/patterns-master.md` |
| Add canonical problem + logic | `03-patterns/TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md` |
| Behavioral / googliness | `04-behavioral/BEHAVIORAL_GOOGLINESS.md` |
| L3 scope (what to skip) | `00-L3-EXECUTION-META/L3_CHEATSHEET.md` §8 |
| Complexity cheatsheet | `00-L3-EXECUTION-META/L3_CHEATSHEET.md` §6–7 |
| Interview strategy | `03-patterns/GOOGLE_INTERVIEW_REVISION.md` |
| GitBook navigation | `SUMMARY.md` |

## Working norms
- All files are Markdown. Edit in place — don't create new files unless asked.
- No code is executed; no tests to run.
- Prefer editing existing structure over creating new files.
- When adding problems: include tier (`⚡ T1` / `🎯 T2` / `💤 T3`), difficulty, and key insight.
- Mark `💤 T3` for overkill-at-L3; exclude from SUMMARY and MINDMAP.
- Keep notes dense and high-signal. No padding.
