# Coding Interview Prep Hub — CLAUDE.md

## What this repo is
Google **L3 SWE** interview prep: DSA coding rounds + Googliness/behavioral. All content is Markdown — no source code to build or test.

**Out of scope:** system design, LLD, concurrency, SQL, segment trees, advanced graphs (Tarjan/SCC), bit-manipulation deep-dives, maths deep-dives.

## Directory layout (don't explore, use this)
```
00-start-here/           # Navigation hub
00-L3-EXECUTION-META/    # 45-min plan, constraints, Python cheatsheet, decision guides
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
| DS / algo indexes + must-solve | `01-data-structures/README.md`, `02-algorithms/README.md` |
| Add / update a DSA topic | `01-data-structures/` or `02-algorithms/` |
| Add a problem walkthrough | matching file under `coding/data-structures/` or `coding/algorithms/` |
| Regenerate problem mindmap | `python3 scripts/regen_l3_maps.py` |
| Add a pattern trigger | `03-patterns/patterns-master.md` |
| Add canonical problem + logic | `03-patterns/TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md` |
| Behavioral / googliness | `04-behavioral/BEHAVIORAL_GOOGLINESS.md` |
| Complexity cheatsheet | `coding/complexity-cheatsheet.md` |
| Interview strategy | `coding/google-interview-strategy.md` |
| GitBook navigation | `SUMMARY.md` |

## Working norms
- All files are Markdown. Edit in place — don't create new files unless asked.
- No code is executed; no tests to run.
- Prefer editing existing structure over creating new files.
- When adding problems: include tier (`⚡ T1` / `🎯 T2` / `💤 T3`), difficulty, and key insight.
- Mark `💤 T3` for overkill-at-L3; exclude from SUMMARY and MINDMAP.
- Keep notes dense and high-signal. No padding.
