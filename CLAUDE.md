# Coding Interview Prep Hub — CLAUDE.md

## What this repo is
Google **L3 SWE / L4 SDE-2** interview prep: DSA coding rounds + Googliness/behavioral. Base track is L3; `00-start-here/l4-sde2-delta.md` layers the L4 bar on top, `00-start-here/sde3-senior-delta.md` layers an SDE-3/senior bar on top of that. All content is Markdown — no source code to build or test.

**Out of scope:** system design, LLD, concurrency, SQL, segment trees, advanced graphs (Tarjan/SCC).

**In scope but capped:** bit manipulation and math/number theory are covered at interview depth (`02-algorithms/17`, `02-algorithms/18`) — common tricks and tier-tagged problems, not deep-dives.

## Directory layout (don't explore, use this)
```
00-start-here/        # L3_CHEATSHEET.md + l3-google-roadmap, l4-sde2-delta, sde3-senior-delta
01-data-structures/   # DS deep-dives (array, hashing, string, matrix, stack, queue, linked-list, tree, trie, heap, graph)
02-algorithms/        # Algo deep-dives (sorting, string, two-pointers, sliding-window, recursion, binary-search, backtracking, union-find, DP, greedy, bits, math)
03-patterns/          # 6 files: patterns-master (triggers/trees), HOW_TO_THINK (+ladders), RECURSION_AND_DP_MASTERCLASS, TOPIC_QUESTIONS (+variants), INTERVIEW_JUDGMENT (+round cheatsheet, mocks, senior chains), mindmap
04-practice/          # Problem walkthrough bank (data-structures/, algorithms/); README = 128-problem index
05-behavioral/        # STAR stories, Googliness
striver-a2z/          # Striver A2Z course notes, one folder per course category (self-contained track)
```

## Common tasks and where to go

| Task | File |
|---|---|
| L3 study schedule | `00-start-here/l3-google-roadmap.md` |
| L4 (SDE-2) delta: bar, tier promotions, gap problems | `00-start-here/l4-sde2-delta.md` |
| SDE-3/senior delta: bar, `T3` promotions, senior-only variants | `00-start-here/sde3-senior-delta.md` |
| Senior follow-up chains (streaming, concurrency discussion, scale-change, etc.) | `03-patterns/INTERVIEW_JUDGMENT.md` Part E |
| Intuition-first pattern curriculum | `03-patterns/HOW_TO_THINK.md` Part IV |
| First-principles pattern thinking guide | `03-patterns/HOW_TO_THINK.md` |
| In-interview judgment: proofs, pivots, hints, recovery | `03-patterns/INTERVIEW_JUDGMENT.md` |
| DS / algo indexes + must-solve | `01-data-structures/README.md`, `02-algorithms/README.md` |
| Add / update a DSA topic | `01-data-structures/` or `02-algorithms/` |
| Add a problem walkthrough | matching file under `04-practice/data-structures/` or `04-practice/algorithms/` |
| Add a pattern trigger | `03-patterns/patterns-master.md` |
| Add canonical problem + logic | `03-patterns/TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md` |
| Behavioral / googliness | `05-behavioral/BEHAVIORAL_GOOGLINESS.md` |
| L3 scope (what to skip) | `00-start-here/L3_CHEATSHEET.md` §8 |
| Complexity cheatsheet | `00-start-here/L3_CHEATSHEET.md` §6–7 |
| Interview strategy | `03-patterns/INTERVIEW_JUDGMENT.md` Part C |
| Decision trees / mind map | `03-patterns/patterns-master.md`, `03-patterns/mindmap.md` |
| GitBook navigation | `SUMMARY.md` |

## Working norms
- All files are Markdown. Edit in place — don't create new files unless asked.
- No code is executed; no tests to run.
- Prefer editing existing structure over creating new files.
- When adding problems: include tier (`⚡ T1` / `🎯 T2` / `💤 T3`), difficulty, and key insight.
- Mark `💤 T3` for overkill-at-L3; exclude from SUMMARY and `03-patterns/mindmap.md`.
- Bare `` `T3` `` (no emoji, used only in `00-start-here/sde3-senior-delta.md` and `03-patterns/INTERVIEW_JUDGMENT.md` Part E) means **senior follow-up tier** — unrelated to `💤 T3` "skip at L3." Do not conflate the two; keep the emoji on skip-tier and bare on senior-tier so they stay visually distinct.
- Keep notes dense and high-signal. No padding.
