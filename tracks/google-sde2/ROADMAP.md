# Google SDE-2 (L4) Roadmap (4–6 Weeks)

Optimized for **Google SDE-2**: strong coding rounds, system design when scheduled, optional AI/ML depth, and focused behavioral prep.

**Short on time?** Use [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md) instead — same DSA priorities compressed to 14 days with virtual vs in-person logistics and AI-ML checklist.

**Targets (adjust based on your loop):**
- Coding: 60–90 high-quality problems (mostly Medium; some Easy for speed, some Hard as stretch)
- Mocks: 6–10 sessions (45–60 min each); at least 2 video and 1 on-site/paper style if you have both DSA formats
- System design (only if on loop): 6–10 run-throughs (30–45 min) from [SYSTEM_DESIGN_L4.md](SYSTEM_DESIGN_L4.md)
- AI/ML (only if on loop): follow [AIML_PREP.md](AIML_PREP.md) + revision block in [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md)
- Behavioral: 6–8 STAR stories, practiced out loud — [BEHAVIORAL_GOOGLINESS.md](BEHAVIORAL_GOOGLINESS.md)

---

## Week 0 — Setup (1 day)

- Confirm with recruiter: number of DSA rounds, system design vs AI/ML, video vs on-site order.
- Lock your language (Python/Java) and load templates into muscle memory: [LANGUAGE_TEMPLATES.md](LANGUAGE_TEMPLATES.md).
- Create your mistake log in [PRACTICE_TRACKER.md](PRACTICE_TRACKER.md) — start it today, not Week 4.
- Read [CODING_ROUNDS.md](CODING_ROUNDS.md) once and practice saying your brute-force-then-optimize transition out loud.
- If AI/ML is confirmed on your loop, start [AIML_PREP.md](AIML_PREP.md) now — don't save it for Week 5.

---

## Week 1 — Arrays, strings, hashing, sliding window

Goal: become fast on the highest-frequency Google patterns.

**Cover:**
- Arrays + prefix sums (subarray sum = K, product except self, Kadane)
- Two pointers (3Sum, container with water, trapping rain water)
- Sliding window (longest substring, minimum window, sliding max)
- Hash map / frequency (group anagrams, longest consecutive)

**Do:** 15–20 problems from [PROBLEM_SET.md](PROBLEM_SET.md) — arrays, two pointers, sliding window sections.

**Mock:** 1 mock at end of week (2 problems, 45 min). Log every failure in [PRACTICE_TRACKER.md](PRACTICE_TRACKER.md).

**Revision:** [../../reference/patterns/patterns-master.md](../../reference/patterns/patterns-master.md) sections 1–2.

**If you're already strong here:** solve 8–10 problems cold, confirm your mistake log stays empty, and move to Week 2 early.

---

## Week 2 — Trees, binary search, stack/queue

**Cover:**
- Trees: pre/in/post/level-order; LCA (BST + general); validate BST; tree DP (max path sum); serialize/deserialize idea
- Binary search: lower/upper bound, rotated array, binary search on answer (Koko, split array)
- Stack/queue: monotonic stack (daily temperatures, histogram), monotonic deque (sliding max), valid parentheses

**Do:** 15–20 problems.

**Mock:** 1 mock. Redo any failures from Week 1 cold before the mock.

**Revision:** [../../reference/quick-sheets/revision-guide.md](../../reference/quick-sheets/revision-guide.md) Parts B4–B7.

---

## Week 3 — Graphs + BFS patterns

**Cover:**
- Graph basics: BFS/DFS, connected components, topological sort (Kahn's)
- Grid BFS/DFS and multi-source BFS (rotting oranges)
- Shortest path: BFS vs Dijkstra — know when each applies
- Union-Find for connectivity problems

**Do:** 12–18 problems.

**Mocks:** 2 mocks — at least one graph-heavy. If you have a video DSA round, do one mock with camera + screen share.

**Revision:** [../../reference/patterns/patterns-master.md](../../reference/patterns/patterns-master.md) sections 7 + 8 (graphs + Union-Find).

---

## Week 4 — DP + backtracking + mixed

**Cover:**
- DP core: 1D (house robber, climbing stairs), coin change (unbounded knapsack), LIS (O(n log n)), LCS (2D DP), word break
- Backtracking: subsets, permutations, combination sum — understand the start/used distinction
- Greedy: interval scheduling, jump game

**Do:** 12–18 problems.

**Mocks:** 2 mocks (mixed patterns). Redo all logged failures cold.

**Revision:** [../../reference/patterns/patterns-master.md](../../reference/patterns/patterns-master.md) sections 8–10 (DP, greedy, backtracking).

---

## Week 5 — System design + AI/ML + polish

**If general SD is on your loop:**
- Do 6–10 run-throughs of prompts from [SYSTEM_DESIGN_L4.md](SYSTEM_DESIGN_L4.md). Use the 3 worked examples as templates.
- Practice talking through each design in 35 minutes without notes.

**If AI/ML is on your loop (instead of or in addition to SD):**
- Work through [AIML_PREP.md](AIML_PREP.md) sections you haven't covered yet.
- Do 1 full "walk through an ML project end to end" session out loud (20–30 min).
- Prepare 2 STAR stories for ML-specific behavioral prompts.

**If neither is on your loop:** spend the full week on coding failures + mocks.

**All candidates:**
- Redo 8–12 problems you previously failed (from your mistake log). No new content.
- 2 mocks under strict timing.

---

## Week 6 — Behavioral + final readiness (optional)

- Finalize 6–8 STAR stories using [BEHAVIORAL_GOOGLINESS.md](BEHAVIORAL_GOOGLINESS.md). Practice each one out loud — not just in your head.
- Do 2 mixed mocks under strict conditions (no pausing, camera on if virtual).
- Zero new topics. Review [../../reference/quick-sheets/quick-recall.md](../../reference/quick-sheets/quick-recall.md) only.
- Logistics: test your EET link, charge laptop, confirm time zone and interview order.

---

## Redo discipline (applies every week)

Every problem you fail goes into [PRACTICE_TRACKER.md](PRACTICE_TRACKER.md) with:
- Failure mode (wrong DS, wrong invariant, off-by-one, etc.)
- Fix in 1–2 lines
- Redo schedule: same day → +2 days → +7 days

If mock score drops below 50%, pause new content and redo failures before moving on.
