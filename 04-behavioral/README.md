## First-Principles Map

```text
WHY Google asks behavioral questions
├── Coding alone underpredicts job performance at L4+
│   ├── GCA (General Cognitive Ability)  — how you think, structure ambiguity
│   ├── Googleyness                       — collaboration, ethics, comfort with uncertainty
│   ├── Leadership                        — influence without authority, driving outcomes
│   └── Role-Related Knowledge (RRK)      — domain depth, technical judgment
├── Behavioral questions surface real past behavior = best predictor of future behavior
└── Missing behavioral bar → rejected even with perfect coding score
│
WHAT the STAR framework is
├── S — Situation: specific context, time, team, project (1-2 sentences, no padding)
├── T — Task: your specific responsibility or challenge in that situation
├── A — Action: what YOU did (first-person, specific steps, not "we decided to")
└── R — Result: measurable outcome (%, latency, $, user count, timeline) + learning
│
HOW to structure stories
├── Length         — 2-3 minutes per story; practice out loud with a timer
├── Specificity    — name the project, system, stakeholder, metric; vague = weak signal
├── First-person   — "I designed", "I proposed", "I pushed back" — not "the team"
├── Measurable     — latency reduced 40%, user growth 2x, shipped 2 weeks early
├── Failure stories— show self-awareness: what went wrong, what you changed, result
└── Story bank     — 6-8 stories that can flex across multiple question types
│
WHEN to use which story (story → Google attribute)
├── Conflict / disagreement          → Googleyness (collaboration, respectful pushback)
├── Ambiguous / undefined problem    → GCA (structuring ambiguity, first-principles)
├── Influence without authority      → Leadership (alignment, buy-in across teams)
├── Technical decision under pressure → RRK (tradeoffs, depth, judgment)
├── Failure / mistake                → Googleyness + GCA (ownership, growth mindset)
└── Going above and beyond           → Leadership + Googleyness (initiative, impact)
│
WHAT CAN GO WRONG
├── Vague results ("it went well", "team was happy")    → no signal, sounds weak
├── "We" instead of "I"                                 → interviewer can't assess you
├── Story too long (>4 min)                             → loses interviewer, seems unfocused
├── No failure / conflict stories                       → signals low self-awareness
├── Repeating same story for all questions              → thin story bank, red flag
├── Praising the team without showing own contribution → credit-diffusion anti-pattern
└── Mismatch: using conflict story for ambiguity question → wrong attribute signaled
│
DECISION — question type → story mapping
├── "Tell me about a time you disagreed"       → Conflict story → Googleyness
├── "Most complex technical problem"           → Technical decision story → RRK
├── "Worked with ambiguous requirements"       → Ambiguity story → GCA
├── "Influenced without authority"             → Leadership story → Leadership
├── "Biggest failure / mistake"                → Failure story → Googleyness + GCA
└── "Went beyond job scope"                    → Initiative story → Leadership + Googleyness
```

## First-Principles Breakdown

- **Root problem:** Coding signals IQ but not judgment, collaboration, or resilience — Google explicitly evaluates these through behavioral signals because they predict L4+ success independently.
- **Core insight:** STAR is not a format constraint but a signal-extraction protocol — Situation/Task establish stakes, Action isolates your judgment, Result proves real-world impact.
- **Invariant:** Every answer must be first-person, specific, and measurable; anything that can't be falsified (vague outcomes, team-credited actions) provides zero signal to the interviewer.
- **Why it works:** Past behavior under real constraints is the strongest predictor of future behavior — specific stories with measurable results are much harder to fabricate than generic claims.
- **Where it breaks:** Story bank too small (fewer than 6 stories), results unmeasured, or wrong attribute signaled for the question — all cause the behavioral bar to fail even with strong coding.

# Behavioral — Google L4 Guide

Full STAR stories and templates: [`behavioral.md`](./behavioral.md)

---

## Google's 4 Hiring Attributes

Every behavioral question at Google maps to one or more of these:

| Attribute | What it measures | Sample question |
|-----------|-----------------|-----------------|
| **General Cognitive Ability (GCA)** | How you think and learn, not just what you know. Structured problem-solving, learning from failure, handling ambiguity. | "Tell me about a time you had to learn something completely new under time pressure." |
| **Googleyness** | Comfort with ambiguity, collaborative spirit, humility, "doing what's right" over politics, bias for action. | "Describe a situation where you disagreed with your team's direction. What did you do?" |
| **Leadership** | Taking ownership beyond your role, influencing without authority, driving outcomes, mentoring. | "Tell me about a project where you took the lead even though it wasn't your responsibility." |
| **Role-Related Knowledge (RRK)** | Technical depth, engineering judgment, quality of solutions you've built. | "Walk me through the most complex technical problem you've solved in the last year." |

> Google does not weight these equally — GCA and Googleyness are baseline filters. Leadership and RRK differentiate L4 from L3.

---

## Full STAR Stories → [`behavioral.md`](./behavioral.md)

---

## 10-Question Self-Assessment

Rate yourself 1–5. Anything below 3 needs a prepared story.

1. Tell me about a time you failed and what you learned.
2. Describe a project where you had significant technical ownership.
3. Tell me about a time you disagreed with your manager or team. What happened?
4. Give an example of when you had to influence others without direct authority.
5. Describe a situation where requirements were ambiguous and you had to make a judgment call.
6. Tell me about a time you had to learn a new technology or domain quickly.
7. Give an example of a time you went above and beyond your role's expectations.
8. Describe a time when you had to make a difficult trade-off (speed vs quality, scope vs deadline).
9. Tell me about a time you mentored or helped a colleague grow.
10. Describe a project where you made a significant technical decision. What were the trade-offs?

---

## The Situation Density Rule

Every STAR story must have a **measurable outcome**. Vague endings kill otherwise good stories.

**Weak ending:** "The project was a success and the team was happy."

**Strong ending:** "We reduced API latency by 40%, the service handled 3x the original traffic, and the feature shipped 2 weeks ahead of schedule."

**Checklist for each story:**
- [ ] Situation is specific (team size, timeline, constraint)
- [ ] Task is clearly your responsibility, not the team's
- [ ] Action is first-person ("I did X") not third-person ("We did X")
- [ ] Result has at least one concrete metric (latency, throughput, users, time saved, bugs fixed)
- [ ] Result connects back to business or user impact

---

## Behavioral Quick Prep (30 minutes before interview)

1. Read your 3 strongest STAR stories — titles + outcomes only (don't memorize verbatim)
2. Map each story to the 4 Google attributes — know which story covers which attribute
3. Prepare a "failure" story — Google specifically looks for self-awareness and growth
4. Have a "conflict resolution" story ready — Googleyness test
