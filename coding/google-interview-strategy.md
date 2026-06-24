---
tags: [coding, amazon-interview, strategy, meta]
topic: Amazon SDE-2 Interview Strategy
difficulty: meta
---

# Amazon SDE-2 Interview Strategy

---

## The Amazon Loop Format

A typical Amazon SDE-2 onsite loop:

| Round | Focus |
|-------|-------|
| Coding 1 | DSA problem (45 min) + behavioral questions (15 min) |
| Coding 2 | DSA problem (45 min) + behavioral questions (15 min) |
| System Design | SDE-2 scoped design (60 min) |
| Behavioral (Bar Raiser) | Deep LP dive — no coding; pure behavioral (60 min) |
| Hiring Manager | Role fit + behavioral + questions (30–45 min) |

**Every round includes behavioral questions.** Come ready with LP stories in every interview, not just the behavioral round.

---

## Amazon Hiring Decision Framework

Amazon uses a **"raise the bar" standard** — not just "can this person do the job?" but "is this person better than half of the current people in this role?"

| Signal | What Amazon looks for |
|--------|----------------------|
| **Strong Hire** | Solves problem cleanly, handles edge cases, communicates tradeoffs; strong LP signals throughout |
| **Hire** | Solves the problem with minor help; adequate LP coverage |
| **No Hire** | Needs significant prompting; shallow LP answers; can't articulate tradeoffs |
| **Strong No Hire** | Can't reach a working solution; LP stories don't demonstrate ownership or impact |

The **Bar Raiser** (a trained interviewer from a different org) has veto power. They look for whether you'd raise the team's overall bar, not just whether you can do the role.

---

## The 35-Minute Coding Session Blueprint

Amazon coding rounds typically give you 45 min total — use the first ~5 min on clarification and the last 5 on wrap-up.

```
[0–2 min]  Clarify
           - Confirm input types, constraints, edge cases
           - Ask about duplicates, null/empty inputs, integer overflow
           - State what you're about to do before writing

[2–5 min]  Brute Force First
           - Verbally state the O(n²) or O(n) brute force
           - Say "I know this isn't optimal, let me think about how to improve it"

[5–20 min]  Optimal Solution
           - Talk through the approach before coding
           - State the pattern trigger: "This looks like a sliding window because..."
           - Code it up; keep variable names clear

[20–25 min] Dry-run / Trace
           - Walk through a simple example manually
           - Catch off-by-one errors before Amazon does

[25–30 min] Edge Cases
           - Empty input, single element, all duplicates, all same values
           - Handle them in code, not just verbally

[30–35 min] Complexity + Follow-up
           - State time and space complexity unprompted
           - Common follow-up: "Can you reduce space?" or "What if the array is sorted?"
```

---

## Communication Scripts That Work at Amazon

**When you're stuck:**
> "I can see we need [pattern], but I'm not immediately sure about [specific part]. Let me think through a simpler subproblem first."

**Stating complexity:**
> "Time complexity is O(n log n) because the sort dominates, and space is O(n) for the auxiliary array."

**When you catch a bug mid-coding:**
> "I see a problem here — if the input is empty, this would throw. Let me add a guard."

**Proposing the brute force:**
> "The naive approach is O(n²) — for each element, scan the rest. That's probably too slow, but it confirms the logic before we optimize."

**When transitioning to optimal:**
> "The bottleneck is this inner loop. If I cache [X] in a hash map, I can drop this to O(1) lookup and bring the whole thing to O(n)."

---

## Amazon-Specific Coding Round Signals

### What Amazon Interviewers Look For

| Signal | Positive | Negative |
|--------|---------|----------|
| **Ownership** | Self-corrects bugs without prompting | Waits for interviewer to point out every bug |
| **Dive Deep** | Explains root cause of each decision | Says "I'll just use a hash map" without explaining why |
| **Deliver Results** | Reaches a working solution | Gets stuck on trivia, never ships working code |
| **Earn Trust** | Explicitly states tradeoffs | Confident but wrong; doesn't verify edge cases |
| **Bias for Action** | Moves forward under uncertainty | Spends 15 min clarifying instead of attempting |

---

## Amazon Topic Frequency (SDE-2, 2022–2024)

Based on reported Amazon interviews:

| Topic | Frequency | Notes |
|-------|-----------|-------|
| Arrays / Two Pointers | Very High | Nearly every loop |
| Trees (BT/BST + traversals) | Very High | LC 102, 104, 236, 543, 124 |
| Dynamic Programming | High | 1D and 2D DP; LCS, coin change, knapsack variants |
| Graphs (BFS/DFS) | High | Islands, word ladder, course schedule |
| Linked Lists | High | Reverse, merge, cycle detection |
| Heaps / Priority Queue | High | Top-K, merge K sorted, median stream |
| Backtracking | Medium | Subsets, permutations, combination sum |
| Binary Search | Medium | Rotated array, binary search on answer |
| Sliding Window | Medium | Usually combined with strings/arrays |
| Tries | Low-Medium | Word search II, autocomplete |
| Union-Find | Low-Medium | Accounts merge, connected components |
| Stack / Monotonic Stack | Low-Medium | Histogram, daily temperatures |
| Topological Sort | Low | Course schedule, alien dictionary |

---

## System Design at SDE-2 — Amazon Scope

**Expected scope**: You should design a working system with reasonable scale decisions. You are NOT expected to handle petabyte-scale distributed consensus or ML pipeline design.

**Universal framework (5-step):**
1. **Requirements**: Functional (what it does) + Non-functional (latency, throughput, availability)
2. **Capacity**: DAU × request/sec → storage and throughput estimates
3. **High-Level Design**: Core components drawn out (client, API layer, DB, cache, queue)
4. **Deep Dive**: Pick the 1–2 hardest components; design them in detail
5. **Tradeoffs**: What does your design sacrifice? (Consistency vs availability, latency vs cost)

**Systems you must be able to design at SDE-2:**
- URL Shortener
- Rate Limiter
- Distributed Cache
- News Feed (simplified — fan-out on write vs read)

**Awareness-level (understand at high level, don't need deep detail):**
- Chat System
- Search Autocomplete

**See [system-design.md](./system-design.md) for full walkthroughs.**

---

## Behavioral LP Alignment in Coding Rounds

Amazon interviewers often ask 1–2 LP behavioral questions within coding rounds. Know which LP maps to which coding behavior:

| Coding behavior | LP being tested |
|----------------|----------------|
| "I caught a subtle off-by-one here" | Insist on the Highest Standards |
| "I'd add monitoring and an alert here in production" | Ownership |
| "Let me consider whether this scales to 10× the input" | Think Big |
| "I've seen a similar pattern before — let me try X" | Learn and Be Curious |
| "The tradeoff is correctness vs speed; I'll go with correctness" | Are Right, A Lot |

---

## Day-Of Checklist

**Before the loop:**
- [ ] Review your 8 core STAR stories (see `behavioral-interview.md`)
- [ ] Confirm which 4–5 LPs you're most likely to be asked about
- [ ] Review complexity table for the 8–10 most common data structures
- [ ] Review at least one pattern template from `patterns-quick-reference.md`

**During coding rounds:**
- [ ] Clarify before you code
- [ ] State your approach before writing
- [ ] Name the pattern you're using
- [ ] State complexity unprompted before being asked
- [ ] Handle at least 2 edge cases explicitly in code

**During behavioral rounds:**
- [ ] Use "I" not "we" in action steps
- [ ] Quantify every result
- [ ] Know which LP you're answering when you tell the story

---

## See Also

- [behavioral-interview.md](./behavioral-interview.md) — LP guide, STAR framework, 8 core stories
- [patterns-quick-reference.md](./patterns-quick-reference.md) — pattern templates
- [system-design.md](./system-design.md) — SDE-2 system design walkthroughs
- [complexity-cheatsheet.md](./complexity-cheatsheet.md) — complexity reference
