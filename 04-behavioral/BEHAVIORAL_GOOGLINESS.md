# Behavioral + Googliness — Google SDE-2

Google evaluates every candidate on four attributes. This file covers all four with signal phrases, anti-patterns, and STAR story guidance.

---

## The Four Google Attributes

### 1. General Cognitive Ability (GCA)

Not IQ — it's **structured thinking under ambiguity**.

**What interviewers look for:**
- You decompose problems before diving into solutions
- You handle new information mid-conversation without derailing
- You can reason about tradeoffs (speed vs correctness, simple vs robust)
- You ask clarifying questions that reveal clear mental models

**Signal phrases (use these):**
- "Before I start coding, let me think about the edge cases..."
- "I see two approaches — the simpler one is O(n²) but here's why the O(n log n) version is worth the complexity..."
- "I initially assumed X, but if Y is true instead, my approach would change to..."

**Anti-patterns:**
- Jumping to code before restating the problem
- Freezing when constraints change mid-problem
- Saying "I don't know" without attempting to reason through it

---

### 2. Leadership

Google means **emergent leadership** — stepping up when needed, stepping back when appropriate.

**What interviewers look for:**
- Influence without authority (convinced someone without having power over them)
- Took ownership when no one else did
- Knew when to escalate vs resolve yourself
- Made a decision under uncertainty and owned the outcome

**Signal phrases:**
- "No one was owning X, so I set up a weekly sync and drove it to completion..."
- "I disagreed with the approach but the team decided to proceed — I raised my concern once clearly, then committed fully..."
- "I noticed the junior dev was blocked — I pair-programmed with them for 2 hours to unblock the sprint..."

**Anti-patterns:**
- Stories where you were the lone hero (no collaboration)
- Stories where you deferred every decision to your manager
- Vague outcomes ("it went better", "the team was happier")

---

### 3. Role-Related Knowledge (RRK)

Your **depth in software engineering**, not trivia recall.

**What interviewers look for:**
- You know your tools deeply (not just "I used Python" but why and when)
- You understand the tradeoffs behind design decisions you've made
- You can discuss failure modes, not just happy paths
- You know when to reach for which data structure, algorithm, or architecture

**Signal phrases:**
- "We chose eventual consistency here because strong consistency would have added 3x latency at that scale..."
- "The bug was caused by a race condition between X and Y — I found it by instrumenting the lock acquisition order..."
- "I benchmarked three approaches; the B-tree index won over the hash index because our queries were predominantly range scans..."

**Anti-patterns:**
- Surface-level answers ("I used a hashmap because it's fast")
- Can't explain why you made a design decision beyond "best practice"
- No discussion of what went wrong or what you'd do differently

---

### 4. Googliness

**"Would this person make our team better?"** It's cultural but it's real.

**Components:**
- **Scrappiness** — Figure it out without hand-holding
- **Intellectual humility** — Say what you don't know; ask to learn
- **Integrity** — Credit others; admit mistakes; don't spin failures
- **Team amplification** — Make those around you better, not just yourself
- **Bias for action** — Don't wait for perfect information; iterate

**Signal phrases:**
- "I didn't know X, so I read the RFC / source code / ran an experiment..."
- "My approach was wrong — [colleague] caught it in code review and I refactored..."
- "I wrote the internal docs so the next person wouldn't hit the same wall I did..."

**Anti-patterns:**
- Taking sole credit for team wins
- No acknowledgment of any mistake or learning
- "I just followed the process" — no initiative shown

---

## STAR Story Template

```
Situation: [1-2 sentences — just enough context]
Task:      [What was your specific responsibility?]
Action:    [What YOU specifically did — not "we"]
Result:    [Quantified outcome: %, $, time saved, users impacted]
```

**Rule:** If you can't quantify the result, estimate and say so. "Reduced build time by roughly 40%" is better than "made it faster."

---

## Question → Attribute Map

| Question | Primary Attribute |
|----------|------------------|
| Tell me about yourself | RRK + Googliness |
| Why Google? | Googliness |
| Tell me about a time you disagreed with your team | Leadership + GCA |
| Tell me about a challenging bug you fixed | RRK + GCA |
| Tell me about a time you failed | Googliness (integrity) |
| Tell me about a project you led | Leadership |
| Tell me about a time you influenced without authority | Leadership |
| Tell me about a time you had to learn something quickly | GCA + Googliness |
| Tell me about your most impactful project | RRK + Leadership |
| Tell me about a time you handled ambiguity | GCA |

---

## Red Flags in Behavioral Rounds

| Red Flag | What It Signals |
|----------|----------------|
| No quantified results | Didn't measure impact; may not own outcomes |
| Always "we", never "I" | Can't isolate own contribution |
| No failure stories | Lack of self-awareness or honesty |
| One-person hero stories | Doesn't collaborate well |
| Badmouthing previous team/company | Low Googliness — team trust risk |
| "I just did what I was told" | No leadership signal |
| Overly polished, rehearsed-sounding | May be fabricating; poke with follow-ups |

---

## Rapid Prep Checklist

Before the interview, have these stories ready:

- [ ] **Biggest impact project** — lead role, quantified result
- [ ] **Conflict or disagreement** — how you handled it, resolution
- [ ] **Something you failed at** — what you learned, what changed
- [ ] **Ambiguous or undefined problem** — how you structured it
- [ ] **Technical deep-dive** — something you built end-to-end, tradeoffs explained
- [ ] **Influencing without authority** — cross-team or peer situation
- [ ] **Learning something fast** — self-taught under pressure

---

## Googliness Quick Checklist (Interview Day)

- Did I give credit where it's due?
- Did I use "I" for my actions and "we" for team wins?
- Did I quantify at least one result per story?
- Did I admit something I didn't know or got wrong?
- Did I show curiosity — asked at least one thoughtful question at the end?
