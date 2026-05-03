# Templates (Copy/Paste)

Use these templates to practice in the same structure every time.

---

## Coding problem template

Timing target: **Pseudocode 2 min → Code 15 min → Test + complexity 8 min**

- Clarifications:
  - Input size bounds:
  - Duplicates? negatives?
  - Can we modify input?
- Approach:
  - Brute force + complexity:
  - Optimal pattern:
  - Invariant / key idea:
  - Why brute→optimal works (narrate out loud):
- Complexity:
  - Time:
  - Space:
- Test cases:
  - Normal:
  - Edge (empty / single):
  - Edge (all same / sorted / reversed):

---

## System design template (L4)

- Requirements
  - Functional:
  - Non-functional (latency, availability, consistency):
  - Out of scope:
- APIs
  - Write:
  - Read:
- Data model
  - Entities:
  - Keys/indexes:
- High-level architecture
  - Services:
  - Storage:
  - Cache:
  - Async (queue/stream):
- Deep dive
  - Read path:
  - Write path:
- Scale + reliability
  - Partitioning/sharding:
  - Hotspot risks:
  - Backpressure/timeouts/retries:
  - Replication + failover:
- Observability
  - Key metrics (latency p99, error rate, throughput):
  - Dashboards / alerting:
  - How you detect degradation before users do:
- Tradeoffs defended
  - Choice 1 (e.g., push vs pull, SQL vs NoSQL):
  - Choice 2 (e.g., consistency vs availability):

---

## AI / ML discussion template (30–45 min — adjust to your loop)

Use when the round is **not** classic DSA. Confirm format with the recruiter (theory, resume deep-dive, or **ML system** design).

- **Role & scope:** what *you* owned vs team (1 min)
- **Problem:** business or user impact in one sentence
- **Data:** sources, size, **label** quality, train vs serve features (**leakage** risks)
- **Model / approach:** baselines → what you chose; **metrics** and how you pick them; failure modes
- **Production:** training cadence, serving path **latency**, monitoring (**drift**, quality drops), rollbacks, A/B if relevant
- **Tradeoff you’d defend:** e.g. precision vs recall, cost vs quality; say what you gave up and why it was worth it
- **What you’d do next:** one improvement with **how you’d measure** success (metric before/after)

Deeper checklist: [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md) (AI / ML section).

---

## Mock interview scorecard (self-review)

- Did I ask constraints early?
- Did I explain the invariant before coding?
- Did I write clean code (no clutter / no “trial and error”)?
- Did I run at least 2 edge tests by hand?
- Did I state correct time/space?
- What is the one thing I will fix next time?

