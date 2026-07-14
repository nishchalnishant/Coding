# Start Here — Google L3/L4 (SWE / SDE-2) Prep

**Goal:** Pass Google coding + Googliness rounds. The base track targets L3; the [L4 delta](../coding/l4-sde2-delta.md) layers the SDE-2 bar on top.
**Approach:** Derive patterns from invariants (don't memorize problems) → build breadth over the topic indexes → integrate under time pressure.

---

## The three-phase loop

### Phase 1 — Derive the patterns (weeks 1–3)
Work through [**Pattern Ladders**](../03-patterns/PATTERN_LADDERS.md), one ladder at a time. Each ladder gives you one *invariant* and a sequence of problems that each change exactly one thing. Follow its study protocol: 20–25 min honest attempts before reading anything, and log the trigger you missed — not the solution.

This phase is where problem-solving ability actually forms. Do not skip to Phase 2 because reading indexes feels faster; recognition without derivation collapses on unseen problems.

### Phase 2 — Breadth (weeks 3–5)
Sweep the topic indexes — [`01-data-structures/README.md`](../01-data-structures/README.md) and [`02-algorithms/README.md`](../02-algorithms/README.md) — and the walkthrough bank in [`coding/`](../coding/). Everything here should now feel like "another rung on a ladder I know." Where it doesn't, that's a gap: return to the ladder, don't memorize the entry.

Skip list still applies: [What to Skip](../00-L3-EXECUTION-META/04-l3-what-to-skip.md) (segment trees, BIT, Tarjan — at L4 too).

### Phase 3 — Integration (weeks 5–6)
- Timed mocks: [`03-patterns/MOCK_INTERVIEW_SET.md`](../03-patterns/MOCK_INTERVIEW_SET.md), 35–45 min each.
- Execution mechanics: [`00-L3-EXECUTION-META/`](../00-L3-EXECUTION-META/) — 45-min plan, constraint heuristics, edge-case taxonomy.
- **L4 only:** follow-up drills and gap problems from the [L4 delta](../coding/l4-sde2-delta.md).
- Behavioral: 5–8 STAR stories in [`04-behavioral/`](../04-behavioral/); L4 stories need ownership/influence framing (delta §5).

---

## Interviewing at L3 or L4?

| | L3 | L4 (SDE-2) |
|---|---|---|
| Schedule | [4-week roadmap](../coding/l3-google-roadmap.md) | [6-week: roadmap + delta](../coding/l4-sde2-delta.md) |
| DP / Dijkstra | recognize (T2) | implement cold (T1) |
| Design-a-DS | LRU only | full family ([Ladder 12](../03-patterns/PATTERN_LADDERS.md#ladder-12--design-a-data-structure-l4-signature)) |
| Follow-up chains | bonus | expected — drill them |
| Not tested (both) | system design, LLD, SQL, concurrency, segment trees/BIT | same |

---

## Directory map

| Folder | Purpose |
|--------|---------|
| `03-patterns/PATTERN_LADDERS.md` | **Phase 1 — start here** |
| `coding/l3-google-roadmap.md` + `coding/l4-sde2-delta.md` | Schedules and L4 gap problems |
| `01-data-structures/`, `02-algorithms/` | Phase 2 breadth indexes + deep-dives |
| `coding/` | Problem walkthrough bank |
| `00-L3-EXECUTION-META/` | 45-min plan, constraint heuristics, Python cheatsheet, edge cases |
| `03-patterns/` | Triggers, mock set, revision sheets |
| `04-behavioral/` | STAR stories and Googliness |

---

## 48-hour sprint (interview is imminent)

**Hours 0–8:** ladder invariants only (the bold paragraph atop each ladder in [`PATTERN_LADDERS.md`](../03-patterns/PATTERN_LADDERS.md)) + 2 problems each: sliding window, BFS, binary search
**Hours 8–16:** quick triggers in both README indexes; Part A of [`GOOGLE_INTERVIEW_REVISION.md`](../03-patterns/GOOGLE_INTERVIEW_REVISION.md); L4 → skim delta §1 and the follow-up table
**Hours 16–24:** 3 timed mocks (35–45 min); rehearse 3 STAR stories
**Hours 24–48:** sleep; light review only — no new topics

---

## Interview day (30 minutes)

1. [`03-patterns/GOOGLE_INTERVIEW_REVISION.md`](../03-patterns/GOOGLE_INTERVIEW_REVISION.md) — Part A only (pattern triggers + gotchas)
2. The 12 ladder invariants — read the bold paragraphs, nothing else
3. Three behavioral story titles + outcomes

**Do not** open new topics or hard DP variants.
