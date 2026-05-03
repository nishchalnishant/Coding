# Google SDE-2 (L4) Track — Start Here

This folder is the **Google SDE-2 (L4)** prep hub: what to practice, in what order, and what questions are likely.

**Minimum effective dose:** pattern recognition + clean implementation + mock discipline. Volume alone doesn't move the needle.

**Pick a timeline:** [ROADMAP.md](ROADMAP.md) (4–6 weeks) or [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md) (14 days, compressed).

---

## Interview loops (recruiter-dependent — confirm before prepping)

| Loop shape | What to emphasize |
|------------|-------------------|
| **2× DSA** + **1× system design** + **behavioral** (classic L4) | [PROBLEM_SET.md](PROBLEM_SET.md), [SYSTEM_DESIGN_L4.md](SYSTEM_DESIGN_L4.md), [BEHAVIORAL_GOOGLINESS.md](BEHAVIORAL_GOOGLINESS.md) |
| **2× DSA** (one video / one on-site) + **1× AI / ML** | Same DSA materials + [AIML_PREP.md](AIML_PREP.md) + [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md) for EET vs in-person logistics |
| **More than two** coding rounds | More mocks; same [PROBLEM_SET.md](PROBLEM_SET.md) + [PRACTICE_TRACKER.md](PRACTICE_TRACKER.md) mistake log |

---

## What Google SDE-2 (L4) actually tests

### Coding rounds
- Pattern recognition in < 60 seconds
- Correct data structure choice + clean implementation
- Communication: clarify → brute force → optimize → code → test
- Handling edge cases without prompting
- Complexity analysis stated before and after coding

### System design (confirm it's on your loop)
- Requirements + APIs + data model + HLD
- Scaling discussion: hot spots, sharding, caching, async
- Explicit tradeoffs: consistency vs availability, cost vs latency

### AI / ML round (confirm format with recruiter)
- Could be: theory, resume deep-dive, ML system design, or all three
- See [AIML_PREP.md](AIML_PREP.md) for full prep guide

### Behavioral / Googliness
- Embedded in most rounds; sometimes a dedicated conversation
- Collaboration, learning mindset, handling ambiguity, ownership

---

## How to use this track

1. **Confirm loop shape** — ask recruiter exactly how many rounds and what type.
2. **Pick timeline** — [ROADMAP.md](ROADMAP.md) or [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md).
3. **Code daily** — [PROBLEM_SET.md](PROBLEM_SET.md) + [PROBLEM_DETAILS.md](PROBLEM_DETAILS.md) for pseudocode.
4. **Log every failure** — [PRACTICE_TRACKER.md](PRACTICE_TRACKER.md) mistake log + redo schedule.
5. **Run mocks like the real thing** — [CODING_ROUNDS.md](CODING_ROUNDS.md) for the 7-step flow.
6. **Patterns for speed** — [../../reference/patterns/patterns-master.md](../../reference/patterns/patterns-master.md).
7. **Last-minute review** — [../../reference/quick-sheets/](../../reference/quick-sheets/).

---

## Files in this folder

| File | Purpose |
|------|---------|
| [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md) | 14-day day-by-day plan (2 DSA + AI-ML); EET vs in-person logistics |
| [ROADMAP.md](ROADMAP.md) | 4–6 week week-by-week plan + mock targets |
| [PROBLEM_SET.md](PROBLEM_SET.md) | Curated ~90 coding problems by pattern, difficulty-labeled |
| [PROBLEM_DETAILS.md](PROBLEM_DETAILS.md) | Pseudocode + key insight for every problem in PROBLEM_SET |
| [CODING_ROUNDS.md](CODING_ROUNDS.md) | 7-step round flow, brute→optimal progressions, virtual vs in-person notes |
| [PRACTICE_TRACKER.md](PRACTICE_TRACKER.md) | Weekly tracker + mistake log + mistake library by pattern |
| [QUESTION_BANK.md](QUESTION_BANK.md) | Canonical tricks per topic; "what usually goes wrong" |
| [SYSTEM_DESIGN_L4.md](SYSTEM_DESIGN_L4.md) | L4 template + 3 worked walkthroughs (URL shortener, rate limiter, news feed) |
| [AIML_PREP.md](AIML_PREP.md) | AI/ML round: core ML, metrics, system design pipeline, STAR templates |
| [BEHAVIORAL_GOOGLINESS.md](BEHAVIORAL_GOOGLINESS.md) | Story bank, STAR template, anti-patterns, Googleyness signals |
| [LANGUAGE_TEMPLATES.md](LANGUAGE_TEMPLATES.md) | Python + Java templates: BFS, topo, DSU, heap, monotonic stack, binary search |
| [TEMPLATES.md](TEMPLATES.md) | Copy/paste structure for coding, system design, AI/ML, mock scorecard |
| [COVERAGE_MAP.md](COVERAGE_MAP.md) | Topic coverage check — ensure no blind spots |
| [SNIPPETS.md](SNIPPETS.md) | Index of Python snippet files; reference during practice, not interviews |
