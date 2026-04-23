# Google SDE-2 (L4) Track — Start Here

This folder is the **Google SDE-2 (L4)** “front door” for this repository: what to practice, in what order, and what questions are likely.

**Minimum effective dose:** `ROADMAP.md` (or `TWO_WEEK_REVISION.md` if you have ~2 weeks) + `PROBLEM_SET.md` + **6–10** timed mocks.

---

## Interview loops (recruiter-dependent)

Google’s onsite or virtual loop varies by team and level. Treat the list your recruiter sends as **source of truth**. Common shapes:

| Loop shape | What to emphasize in this repo |
|------------|--------------------------------|
| **2× DSA** + **1× system design** + **behavioral** (classic L4) | `PROBLEM_SET.md`, [SYSTEM_DESIGN_L4.md](SYSTEM_DESIGN_L4.md), [BEHAVIORAL_GOOGLINESS.md](BEHAVIORAL_GOOGLINESS.md), [ROADMAP.md](ROADMAP.md) |
| **2× DSA** (e.g. one video / one on-site) + **1× AI / ML** | Same DSA materials; add [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md) (EET vs in-person + **AI-ML checklist**). **General** system design is optional unless another round is scheduled. |
| **More than two** coding rounds | Increase mock count; keep using `PROBLEM_SET.md` + mistake log in [PRACTICE_TRACKER.md](PRACTICE_TRACKER.md) |

---

## What Google SDE-2 typically tests

### Coding rounds (most common)
- Pattern recognition + correct data structure choice
- Clean implementation (edge cases, no bugs)
- Complexity analysis + tradeoffs
- Communication and iteration (clarify → design → code → test)

### System design (common at L4 — confirm on your loop)
- Requirements + APIs + data model
- High-level architecture and scaling
- Correct tradeoffs (latency, cost, consistency, reliability)  
  If your loop has an **AI / ML** round instead of (or in addition to) general SD, rehearse **ML system** thinking (data, training, serving, monitoring) using the checklist in [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md); [SYSTEM_DESIGN_L4.md](SYSTEM_DESIGN_L4.md) stays the default for **general** distributed systems.

### Behavioral / Googliness
- Often overlap with technical rounds; questions can also appear in **dedicated** HR/leadership conversations
- Collaboration, humility, learning mindset
- Handling ambiguity, conflict, influence without authority
- Ownership and delivering outcomes

---

## How to use this track

1. **Pick a timeline:** [ROADMAP.md](ROADMAP.md) (4–6 weeks) or [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md) (14 days).
2. **Do the coding set:** [PROBLEM_SET.md](PROBLEM_SET.md) → details in [PROBLEM_DETAILS.md](PROBLEM_DETAILS.md).
3. **Run coding rounds like the real thing:** [CODING_ROUNDS.md](CODING_ROUNDS.md) (virtual vs in-person notes).
4. **Revise by topic:** See `tracks/foundations/` for core DSA reference.
5. **Patterns for speed:** [../../reference/patterns/patterns-master.md](../../reference/patterns/patterns-master.md).
6. **Quick sheets:** [../../reference/quick-sheets/](../../reference/quick-sheets/) for last-minute review.

---

## Files in this folder

- `TWO_WEEK_REVISION.md` — **2-week** plan for **2 DSA** (1× virtual EET + 1× in person) + **1 AI-ML**; internal DSA links + AI-ML checklist
- `ROADMAP.md` — 4–6 week plan + mocks
- `PROBLEM_SET.md` — curated coding problems by pattern (L4-weighted)
- `CODING_ROUNDS.md` — how to run a Google-style coding round (rubric + checklist)
- `SYSTEM_DESIGN_L4.md` — L4 system design template + common questions
- `BEHAVIORAL_GOOGLINESS.md` — behavioral prompts + story bank template
- `PRACTICE_TRACKER.md` — weekly tracker + mistake log
- `TEMPLATES.md` — copy/paste templates for coding + system design + **AI/ML discussion** + mocks
- `LANGUAGE_TEMPLATES.md` — Python/Java templates (BFS/DFS/topo/DSU/etc.)
- `COVERAGE_MAP.md` — ensure you’re not missing core topics
- `SNIPPETS.md` — Python snippet library (solutions/templates)
- `QUESTION_BANK.md` — canonical questions + tricks + code pointers
- `PROBLEM_DETAILS.md` — short descriptions + pseudocode for every coding question in this track
