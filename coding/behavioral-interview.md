---
tags: [coding, amazon-interview, behavioral, star, leadership-principles]
topic: Behavioral Interview — Amazon SDE-2
difficulty: meta
---

# Behavioral Interview Guide — Amazon SDE-2

> At Amazon, behavioral interviews are evaluated entirely through the lens of **Leadership Principles (LPs)**. Every question maps to one or more LPs. Prepare 2–3 STAR stories per LP that matters most (Customer Obsession, Ownership, Dive Deep, Deliver Results, Bias for Action, Earn Trust, Disagree and Commit).

---

## Amazon's 16 Leadership Principles

| # | LP | Core Signal |
|---|---|---|
| 1 | **Customer Obsession** | Start with the customer and work backwards |
| 2 | **Ownership** | Act like an owner, not just a role holder |
| 3 | **Invent and Simplify** | Find simpler solutions; simplicity is strength |
| 4 | **Are Right, A Lot** | Strong judgment; seek diverse perspectives |
| 5 | **Learn and Be Curious** | Continuously improve; explore new possibilities |
| 6 | **Hire and Develop the Best** | Raise the bar with every hire; mentor |
| 7 | **Insist on the Highest Standards** | Never settle; drive quality |
| 8 | **Think Big** | Bold direction; inspire results |
| 9 | **Bias for Action** | Speed matters; calculated risk-taking |
| 10 | **Frugality** | Accomplish more with less |
| 11 | **Earn Trust** | Listen attentively; be honest even when uncomfortable |
| 12 | **Dive Deep** | Operate at all levels; stay connected to details |
| 13 | **Have Backbone; Disagree and Commit** | Challenge respectfully; commit fully once decided |
| 14 | **Deliver Results** | Focus on key inputs; deliver with quality on time |
| 15 | **Strive to Be Earth's Best Employer** | Empathy, safety, inclusion |
| 16 | **Success and Scale Bring Broad Responsibility** | Do better for society |

**Most tested at SDE-2**: Customer Obsession, Ownership, Bias for Action, Dive Deep, Disagree and Commit, Deliver Results, Earn Trust, Invent and Simplify.

---

## The Bar Raiser

Every Amazon interview loop includes a **Bar Raiser** — a specially trained interviewer from a different team whose sole job is to maintain the hiring bar. They:
- Are not your future manager or teammate
- Ask harder follow-up questions than standard interviewers
- Can veto a hire even if the rest of the loop approves
- Focus heavily on behavioral signals and LP coverage

Prepare as if every interviewer is the bar raiser.

---

## The STAR Framework — Amazon Style

**S**ituation → **T**ask → **A**ction → **R**esult

Amazon expects STAR answers to be **specific, measurable, and LP-tagged**. After every answer, the interviewer should be able to say "that demonstrates [LP]."

### Wrong STAR:
> "My team had a difficult project. I helped lead it. We shipped it on time."

### Right STAR (Amazon wants):
> **Situation**: "Our team's checkout service was experiencing a 2% cart abandonment spike during peak traffic. We were two weeks before Prime Day."
>
> **Task**: "I was the owner of the checkout backend. No one explicitly asked me to investigate — I flagged it myself after seeing it in our dashboards."
>
> **Action**: "I pulled traces and found that our payment gateway was timing out on retries, but the timeout was set to 5 seconds — too long under load. I ran experiments in staging to find the optimal retry budget (1.5s + exponential backoff with jitter), confirmed the fix with load testing simulating 3x Prime Day traffic, and proposed the change at design review. Two other engineers pushed back saying the fix was too risky pre-Prime Day. I came prepared with the data: the retry storm was worse than the risk of the fix. We agreed to deploy behind a feature flag with instant rollback capability."
>
> **Result**: "Cart abandonment dropped from 2% to 0.3% within 30 minutes of the flag flip. Prime Day ran without incidents on this service. I also wrote a doc on retry budget best practices that became our team's standard reference."

**LP tags**: Ownership (didn't wait to be asked), Dive Deep (traces → root cause), Disagree and Commit (won with data, others committed), Deliver Results.

---

## High-Signal LP → Question Mapping

### Customer Obsession
- "Tell me about a time you made a decision that prioritized the customer over a short-term technical or business metric."
- "Describe a time you advocated for the customer when others didn't."
- "Tell me about a time you discovered an unmet customer need."

### Ownership
- "Tell me about a time you owned a project end to end."
- "Describe a time you stepped up to fix something outside your job description."
- "Tell me about a time you took responsibility for a failure."

### Invent and Simplify
- "Tell me about a time you simplified a complex process or system."
- "Describe an innovative solution you implemented."

### Bias for Action
- "Tell me about a time you made a decision without all the information you wanted."
- "Describe a time you took a calculated risk. What was the outcome?"
- "Tell me about a time you had to move fast despite uncertainty."

### Dive Deep
- "Tell me about a time you dug into a problem deeper than was expected."
- "Describe a time you found a root cause that others had missed."
- "Tell me about a time data changed your initial assumption."

### Disagree and Commit
- "Tell me about a time you disagreed with a decision and how you handled it."
- "Describe a time you committed to a direction you didn't initially agree with."
- "Tell me about a time you pushed back on a requirement or a direction."

### Deliver Results
- "Tell me about a time you delivered a result despite significant obstacles."
- "Describe a time you had to make hard tradeoffs to meet a deadline."
- "Tell me about a project you drove from idea to completion."

### Earn Trust
- "Tell me about a time you had to give difficult feedback."
- "Describe a time you made a mistake and how you communicated it."
- "Tell me about a time you earned the trust of a skeptical stakeholder."

---

## 8 Core Stories to Prepare

| Story | Primary LP | Secondary LPs |
|-------|-----------|--------------|
| **Your best technical project** | Deliver Results | Ownership, Dive Deep |
| **A time you went above and beyond scope** | Ownership | Bias for Action, Customer Obsession |
| **A time you disagreed and won (with data)** | Disagree and Commit | Are Right A Lot, Earn Trust |
| **A time you disagreed and committed** | Disagree and Commit | Earn Trust |
| **A real failure you caused and owned** | Ownership | Earn Trust, Learn and Be Curious |
| **A decision under ambiguity/incomplete info** | Bias for Action | Are Right A Lot |
| **A time you simplified something** | Invent and Simplify | Frugality |
| **Why Amazon / what excites you** | Customer Obsession | Think Big |

---

## Story Template

```
Story: [Name]
Primary LP:
Secondary LPs:

SITUATION (2 sentences):
- Context: project/team/timeline/stakes

TASK (1 sentence):
- Your specific role or what you were responsible for

ACTION (5–7 sentences — heaviest weight):
- What did YOU do? (use "I" not "we")
- What alternatives did you consider?
- Why this approach?
- What obstacles; how did you resolve them?

RESULT (2–3 sentences):
- Quantified impact (latency, revenue, users, error rate, time saved)
- What you learned or changed afterward

If asked "what would you do differently?":
- [Honest answer — shows self-awareness]
```

---

## Anti-Patterns That Get You Rejected at Amazon

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| "We did X" throughout | Can't evaluate YOUR contribution | Always use "I" for your actions |
| Vague results — "it went well" | No LP signal without impact | Quantify: "reduced p99 latency from 800ms to 120ms" |
| A story with no conflict or difficulty | Signals shallow experience | Pick stories with real tension and real stakes |
| Blaming teammates | Fails Earn Trust | Own your part; show empathy for constraints |
| Saying "I followed my manager's direction" for Ownership stories | Fails the LP | Ownership requires self-direction — you should initiate |
| Short answers (< 2 min) | Too little signal | Aim for 3–4 min per story |
| Generic answers not tied to LP | Misses the frame | Know which LP each question targets |

---

## Questions to Ask Your Interviewer

**About the role:**
- "What does success look like in this role after 6 months?"
- "What's the biggest technical challenge the team is working on right now?"
- "How does the team measure customer impact?"

**About working at Amazon:**
- "How does the team balance operational load with new feature work?"
- "How are technical decisions made — is there a design review process?"
- "What's something you wish you'd known before joining this team?"

**About the bar raiser (if applicable):**
- "What qualities in engineers have you seen raise the bar on this team?"

**Avoid:**
- "What's the compensation?" (ask recruiter)
- Questions answered by reading the job description
- "How many hours do people typically work?" (comes across wrong)

---

## Why Amazon (Not "Why Google")

Interviewers will ask "Why Amazon?" Be specific. Generic answers ("great company", "scale") are weak.

Good angles:
- A specific Amazon product/service that you use and have opinions about improving
- The LP framework itself — "I want to work somewhere that rewards ownership and customer focus explicitly, not just as values on a wall"
- A specific team's technical challenges (if you know them)
- Amazon's breadth: "I want the optionality of working across AWS, retail, devices — the range of hard problems is unmatched"

---

## See Also

- [amazon-interview-strategy.md](./google-interview-strategy.md) — now reframed for Amazon
- [system-design.md](./system-design.md) — SDE-2 scoped system design
