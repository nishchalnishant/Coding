---
module: 03-patterns
topic: Interview Judgment — reasoning tools & live decision-making
tags: [logic, proof, counterexamples, decision-making, interview-strategy, google-l3, l4]
---
# Interview Judgment — Reasoning Tools & Live Decision-Making

## What this covers

> [!abstract] In this file
> **Covers:** Reasoning tools (examples as experiments, invariants, quick proofs, feasibility estimates), live decisions (commit vs pivot, hints, recovery, trade-offs), the one-page round cheatsheet + revision schedules, a 25-problem mock set with L4 chains, and senior follow-up chains.
> **You'll be able to:** Make and justify decisions out loud during a 45-minute round, run a final-week revision, and extend any solve along senior follow-up axes.
> **Prereqs:** How to think · **Pair with:** [How to think](HOW_TO_THINK.md) · [L3 cheatsheet](../00-start-here/L3_CHEATSHEET.md) · [Senior delta](../00-start-here/sde3-senior-delta.md) · **Time:** 1.5 h + 25 × 45 min mocks

**Sections:** [A1. Examples are experiments — design them, don't just "try one"](#a1-examples-are-experiments--design-them-dont-just-try-one) · [A2. Invariants — the sentence that makes code correct by construction](#a2-invariants--the-sentence-that-makes-code-correct-by-construction) · [A3. The three proof moves you can actually run in 45 minutes](#a3-the-three-proof-moves-you-can-actually-run-in-45-minutes) · [A4. Estimate before you build — the 30-second feasibility check](#a4-estimate-before-you-build--the-30-second-feasibility-check) · [B1. Commit vs pivot — the explicit rule](#b1-commit-vs-pivot--the-explicit-rule) · [B2. Choosing between two plausible approaches](#b2-choosing-between-two-plausible-approaches) · [B3. Hints are data — decode them, don't survive them](#b3-hints-are-data--decode-them-dont-survive-them) · [B4. Recovery playbook — the three failure moments, scripted](#b4-recovery-playbook--the-three-failure-moments-scripted) · [B5. Trade-offs — always present them as a menu, never as a monologue](#b5-trade-offs--always-present-them-as-a-menu-never-as-a-monologue) · [B6. The judgment drill (how to train any of this)](#b6-the-judgment-drill-how-to-train-any-of-this) · [The one-card summary](#the-one-card-summary) · [Round cheatsheet (one page)](#round-cheatsheet-one-page) · [Communication (how to sound clear at Google)](#communication-how-to-sound-clear-at-google) · [Revision schedules](#revision-schedules) · [After the interview](#after-the-interview) · [Set 1: Must Solve Cleanly (No Hints)](#set-1-must-solve-cleanly-no-hints) · [Set 2: Build Fluency (Aim for Clean First Attempt)](#set-2-build-fluency-aim-for-clean-first-attempt) · [Set 3: Stretch Problems (Common at Google, Separates Offers)](#set-3-stretch-problems-common-at-google-separates-offers) · [Mock Interview Scoring Guide](#mock-interview-scoring-guide) · [Weak Area Drill List](#weak-area-drill-list) · [L4 (SDE-2) Mock Rounds — follow-up chains](#l4-sde-2-mock-rounds--follow-up-chains) · [1. Count-vs-existence](#1-count-vs-existence) · [2. Streaming / online](#2-streaming--online) · [3. Update-heavy / deletion-heavy](#3-update-heavy--deletion-heavy) · [4. Memory-constrained](#4-memory-constrained) · [5. Concurrency discussion](#5-concurrency-discussion) · [6. One-vs-all](#6-one-vs-all) · [7. Scale-change (100x)](#7-scale-change-100x) · [See Also](#see-also)

---

> [!IMPORTANT]
> **The missing layer this file adds.** [HOW_TO_THINK.md](HOW_TO_THINK.md) teaches you to *derive* patterns. [The L3 Cheatsheet](../00-start-here/L3_CHEATSHEET.md) maps keywords → structures. Neither teaches the two skills that actually decide close interviews: **convincing yourself an idea is correct before spending 15 minutes coding it**, and **making good calls under uncertainty** — commit or pivot, which of two approaches, what to do with a hint, how to recover from a wrong path. Strong candidates don't fail because they lack patterns; they fail because they coded the wrong idea confidently or abandoned the right idea nervously. This file trains that judgment.

---

# PART A — REASONING TOOLS (logic you run before and while coding)

## A1. Examples are experiments — design them, don't just "try one"

Most candidates use examples passively (trace the given sample). Examples are actually your **hypothesis-testing instrument**, and there are exactly four kinds worth constructing, each answering a different question:

| Example type | Question it answers | How to build it |
|---|---|---|
| **Smallest interesting case** | "What does the mechanism look like with no noise?" | n = 2 or 3, the minimum where a real decision occurs. (n = 0/1 are edge cases, not insight cases.) |
| **Structure-revealing case** | "What does my hand do when solving this?" | ~8–10 elements, solve it manually, then *introspect the procedure your eyes ran* — it's often the algorithm |
| **Adversarial case** | "What input would embarrass my current idea?" | Attack your idea's assumption directly: duplicates if you assumed distinct, negatives if you assumed positive, ties if you sort, all-equal elements, already-sorted / reverse-sorted |
| **Boundary case** | "Does the code survive the edges?" | Saved for the dry run — see [Universal Edge Cases](../00-start-here/L3_CHEATSHEET.md) |

The discipline: after forming an approach and *before* coding it, spend 60 seconds deliberately trying to **break** it with an adversarial case. Finding your own counterexample at minute 8 costs one minute; the interviewer finding it at minute 35 costs the round. The mindset shift is from lawyer (defending your idea) to scientist (attacking it) — interviews reward scientists.

**The counterexample-hunting procedure** (for "is this greedy/shortcut valid?"):
1. State the *assumption* your shortcut relies on, explicitly. ("Taking the largest first is never wrong.")
2. Build the smallest input where that assumption is *under tension* — where a locally-worse choice could plausibly win. Tension usually needs only 3–4 elements with skewed values (coins {1,3,4} target 6; intervals where the longest one blocks two short ones).
3. Two minutes without a counterexample + a sketchable exchange argument (A3) → commit. Counterexample found → you just earned the pivot *with proof in hand* — say it out loud; disproving your own idea cleanly is a hire signal, not a stumble.

## A2. Invariants — the sentence that makes code correct by construction

An **invariant** is one sentence that is true before and after every iteration. It is not academic decoration; it's the difference between *writing* a loop and *hoping* a loop:

- Binary search: "the answer, if it exists, is always inside `[lo, hi]`." Every line of the loop either preserves this or is a bug — and every off-by-one question ("`mid` or `mid+1`?") is answered by the sentence, not by memory.
- Partition/writer loops: "everything left of `write` is final output." 
- Kadane: "`cur` = best subarray *ending exactly here*."
- Sliding window: "`[left, right]` is the largest valid window ending at `right`."
- Heap top-k: "the heap holds the best k seen so far."

**The practice:** before coding any loop, say its invariant in one sentence. While coding, each statement's job is "restore the invariant after admitting the new element." During the dry run, *check the invariant at each step* instead of re-deriving what the variables mean — it converts dry runs from re-solving into auditing. If you can't state an invariant, you don't yet understand your own algorithm; that discovery costs 30 seconds now versus a rewrite later.

## A3. The three proof moves you can actually run in 45 minutes

Interviewers ask "why does this work?" — and there are only three answer shapes. Knowing them by name means never being speechless:

1. **Invariant + induction** (for loops): "True initially; each step preserves it; at termination it implies the answer." This is the loop version of the DP contract / leap of faith ([Masterclass §1.2](RECURSION_AND_DP_MASTERCLASS.md#12-the-leap-of-faith--the-single-most-important-idea-in-this-file)) — the same induction, standing up instead of recursing down.
2. **Exchange argument** (for greedy): "Take any optimal solution that disagrees with my first choice; swap my choice in; it got no worse; induct." Thirty spoken seconds. If you can't sketch it, downgrade your confidence in the greedy ([HOW_TO_THINK.md — Greedy](HOW_TO_THINK.md#greedy--the-only-pattern-that-requires-a-proof)).
3. **No-candidate-escapes** (for discard-based patterns — two pointers, monotonic stack, binary search halving): "I only ever discard candidates that are *dominated* — here's the one-line domination proof — so the answer is never discarded." When you move a pointer, be able to finish the sentence "…and this can't skip the answer because ___."

L3 bar: run these when asked. L4 bar: run move 2 or 3 *unprompted* in one sentence as you make the choice ("moving the shorter wall is safe because keeping it caps every future area"). One sentence, not a lecture.

## A4. Estimate before you build — the 30-second feasibility check

Before committing to an approach, multiply it out: *states × work per state*, or *iterations × cost per iteration*, against ~10⁷–10⁸ simple operations/second. "n = 10⁵, my idea is O(n²) = 10¹⁰ — dead on arrival, don't code it." This one habit prevents the most expensive interview failure mode: 20 minutes implementing something that could never pass, discovered only when the interviewer asks for complexity. Feasibility math comes *before* implementation, always — it's step 2 of the [solve loop](HOW_TO_THINK.md#2-the-solve-loop-run-this-every-single-time) for exactly this reason.

---

# PART B — LIVE DECISION-MAKING (the judgment calls, with actual rules)

Every rule below exists because the natural instinct under pressure is wrong: sunk cost says keep digging, ego says hide the confusion, anxiety says start coding. These are the overrides.

## B1. Commit vs pivot — the explicit rule

The worst outcomes come from the two extremes: grinding a dead approach for 25 minutes, or hopping between three approaches and finishing none. The rule:

> **Pivot only on *evidence*, never on *discomfort*.** Evidence = a counterexample, a failed feasibility estimate (A4), or a missing piece you can name ("this needs deletions and my heap can't"). Discomfort = "this feels hard / I don't remember how" — that is a signal to push, not switch, because the next approach will hit the same wall plus a time deficit.

Operational form — the **10-minute checkpoint**: if 10 minutes past problem-read you have no approach that survives A4's math, *stop optimizing in your head* and say: "Let me implement the brute force cleanly and then optimize the bottleneck." A working brute force is points on the board, the raw material for the four levers, and evidence of structured thinking. Zero code at minute 25 is the single most common reject shape — brute-force-first is the insurance against it.

And its mirror — the **one-pivot budget**: past minute 20, you get at most one approach change, and only with evidence in hand. After that, ship the best thing you have and state its limitation honestly. A correct O(n²) with a spoken "the O(n log n) version would replace this scan with a heap" beats a broken O(n log n) every time — interviewers can grade the sentence; they can't grade code that doesn't run.

## B2. Choosing between two plausible approaches

When both ideas pass the feasibility math, stop weighing "which is cleverer" — decide on **implementation risk**, in priority order:

1. **Fewer moving parts under pressure.** BFS over Dijkstra when both work; sorting + one pass over a clever structure; iterative over recursive when depth is scary. You are choosing what your minute-30 self has to debug.
2. **Which failure is recoverable?** An approach that degrades gracefully (works, but slower) beats one that's all-or-nothing (either the invariant is exactly right or the output is garbage).
3. **Extendability** — only as a tiebreak, and only if you've internalized the [escalation grammar](HOW_TO_THINK.md#the-escalation-grammar-what-follow-ups-will-be): which version survives "now it's a stream / now return all of them"?

Then do the senior move: **offer the decision.** "I see a two-heap O(log n) design and a simpler sort-based O(n log n) per query; given 45 minutes I'd code the sort version and talk through the heap upgrade — sound good?" This shows both ideas, converts a private gamble into a shared plan, and interviewers almost always respond well to it. Choosing silently forfeits the credit for the road not taken.

## B3. Hints are data — decode them, don't survive them

A hint is not a deduction on your scorecard by itself; *missing* the hint is. Interviewer utterances come in three intensities, and each demands a different response:

| Signal | What it actually means | Correct response |
|---|---|---|
| "Are you sure that handles X?" / "Walk me through X" | **There is a bug, and X triggers it.** This is never idle curiosity. | Stop. Trace X honestly and slowly. Do not say "yes it's fine" from memory — that answer, wrong, is the worst moment available in an interview. |
| "Is there anything about the input you're not using?" / "What if it were sorted?" | You've missed the intended lever; they're pointing at it. | Take it fully: re-run the [stuck moves](HOW_TO_THINK.md#4-when-you-are-truly-stuck--the-seven-moves) *with their ingredient as the axis*. Half-taking a hint (nodding, continuing as before) reads worse than needing it. |
| "OK. What's the complexity?" (mid-implementation) | Your approach is too slow and they're inviting you to notice. | Actually recompute it fresh — don't repeat your earlier claim. Then: "…which is n², too slow for this n — the bottleneck is this inner scan; replacing it with ___." |
| Silence while you're stuck | You've been quiet too long. | Narrate your candidate directions and *ask a real question*: "I'm deciding between modeling this as a graph or as intervals — is one of those a dead end?" Asking a specific question is fine; asking "am I on the right track?" repeatedly is not. |

Meta-rule: **a used hint costs a little; a wasted hint costs a lot.** When one arrives, treat it as the highest-priority input in the room — the interviewer just told you where the points are.

## B4. Recovery playbook — the three failure moments, scripted

Pre-scripting these turns panic moments into procedure. Each has a wrong instinct to override.

**Dry run exposes a bug (minute ~37).** Wrong instinct: patch the symptom at the line where the trace went wrong. Right procedure: (1) say "good — found a bug" in an even tone (composure here is graded); (2) classify before touching code — is it the *invariant* (idea wrong: needs thought, maybe a `while` should be `if`) or the *transcription* (idea right, code wrong: off-by-one, swapped args — safe to fix locally)? (3) fix at the cause, re-run the trace *from the failing step*, and also check the fix against one boundary case — symptom-patches breed sibling bugs and interviewers watch for whack-a-mole.

**Approach collapses at minute 25.** (You now have evidence it can't work.) Not recoverable to full marks — recoverable to a hire: (1) say precisely *what* broke: "this window invariant dies with negative numbers — growing the window no longer moves the sum one way"; naming the cause proves the understanding the broken code can't. (2) Ask for the direction check *once*: "I think the fix is prefix sums + a hashmap — before I rebuild, does that direction make sense?" (When one approach has died, one direction-check is free; two is a pattern.) (3) Rebuild only what changed — most scaffolding (I/O, loops, helpers) usually survives.

**Total blank at minute 5.** Wrong instinct: silence, or re-reading the problem a fourth time. Right procedure — this is exactly what the [solve loop](HOW_TO_THINK.md#2-the-solve-loop-run-this-every-single-time) steps 3–5 are *for*: solve a 10-element case by hand and watch your hand; say the brute force out loud with its complexity (this always exists — "try every subarray: O(n²)"); name its waste. Speaking the brute force has a second function beyond points: it breaks the freeze. Motion creates thought, not the other way around.

## B5. Trade-offs — always present them as a menu, never as a monologue

When multiple legitimate versions exist (time vs space, simple vs optimal, sorted vs hashed), the L4-shaped move is a **priced menu plus a recommendation**:

> "Option A: sort in place, O(n log n), destroys input order. Option B: hashmap, O(n) time but O(n) extra space. If the array is reusable I'd take B; if memory is the constraint, A. I'll default to B."

Three sentences. It demonstrates you see the whole space, it hands the interviewer a steering wheel (they often reveal hidden requirements in response — "actually, memory is tight" tells you the follow-up), and it's the miniature of real engineering judgment, which is what the whole exercise is a proxy for. Deciding silently gets you graded only on the branch you took.

## B6. The judgment drill (how to train any of this)

Judgment doesn't improve by reading — it improves by *forcing the decision points to be explicit* in practice:

1. **Timestamp your mocks.** Note the clock when you commit to an approach, when doubts appear, and when you pivot. Review: was each pivot evidence-based or discomfort-based (B1)? Most people discover they pivot on discomfort and grind on sunk cost — the exact opposite of the rule.
2. **Pre-mortem every commit.** Before coding, one sentence: "the most likely way this approach fails is ___." (Trains A1's adversarial instinct; also catches missing state dimensions early.)
3. **Play interviewer.** Once a week, take a problem you know cold and write the three hints you'd give a struggling candidate, in escalating order. Nothing teaches hint-*decoding* (B3) faster than authoring hints.
4. **Log misses by decision, not by topic** — extend the [training protocol](HOW_TO_THINK.md#the-training-protocol-how-to-study-this-file): was the failure a pattern gap, or a judgment failure (ignored the 10-minute checkpoint, defended instead of traced, silent trade-off)? Most candidates past 100 solved problems miss on judgment, not patterns — which means this log, not more problems, is where the next hire-signal comes from.

---

## The one-card summary

> 1. Examples are experiments: build the **adversarial case** against your own idea *before* coding — scientist, not lawyer.
> 2. Every loop gets an **invariant sentence** before it gets code; dry-run by auditing the invariant.
> 3. Three proof moves cover every "why does this work": **invariant+induction · exchange · no-candidate-escapes.**
> 4. **Multiply it out** (states × work vs ~10⁸/sec) before implementing, never after.
> 5. Pivot on **evidence** (counterexample, failed math, nameable gap) — never on discomfort. One pivot after minute 20, max.
> 6. No approach by minute 10 → **brute force on the board**, then optimize its named waste.
> 7. Between two viable approaches: pick the one your **minute-30 self can debug**; offer the choice out loud.
> 8. Hints are targeting data. "Are you sure about X?" means X breaks it — trace X, don't reassure.
> 9. Bug found: classify **invariant vs transcription** before touching a line.
> 10. Trade-offs are a **menu with prices and a recommendation**, spoken in three sentences.

---

# PART C — ROUND EXECUTION & REVISION

## Round cheatsheet (one page)

### What Google looks for (coding round)

- **Problem-solving**: Clarify → brute force → optimize → code → test → complexity.
- **Communication**: Think out loud; state assumptions; ask about constraints (empty input, duplicates, size limits).
- **Code quality**: Clear names, handle edge cases, correct complexity analysis.

### Topic priority (typical frequency)

| Priority | Topics | Patterns to nail |
|----------|--------|------------------|
| **1** | Arrays, Strings, Hashing | Two pointers, sliding window, prefix sum + map, frequency map |
| **2** | Trees, Graphs | BFS/DFS, LCA, topo sort, shortest path (BFS / Dijkstra) |
| **3** | DP | 1D recurrence, 2D (LCS/grid), interval DP basics |
| **4** | Heap, Binary Search | Top-K, merge K lists, BS on answer, rotated array |
| **5** | Stack/Queue | Monotonic stack, monotonic deque |

### Complexity you must state correctly

Sound bites — say them exactly like this:

- “We visit each node/edge at most once → **O(V + E)**” (BFS/DFS); Dijkstra: **O((V + E) log V)** with min-heap.
- “Sorting dominates → **O(N log N)**.”
- “Hash map gives O(1) average lookup, so overall **O(N)**.”
- “Binary search on answer: O(N) check per mid × O(log range) mids → **O(N log range)**.”
- Sliding window: usually **O(N)** time.

### Edge cases & complexity table

Single-sourced in the cheatsheet — reread them there, not here:
[edge cases](../00-start-here/L3_CHEATSHEET.md#5-universal-edge-cases) · [pattern → time/space table](../00-start-here/L3_CHEATSHEET.md#6-big-o-reference) · [pattern triggers](./patterns-master.md#quick-decision-trees).

### Open with / Close with

**Open:** repeat the problem in your words; ask — size limits? duplicates? can we modify input?
**Close:** state time and space; run two test cases (normal + edge); name a follow-up (stream, huge n).

---

## Communication (how to sound clear at Google)

1. **Start:** “Let me restate the problem and confirm constraints: can the array be empty? Are numbers non-negative?”
2. **Brute force:** “A naive approach would be O(…) because …”
3. **Optimize:** “We can improve by … which brings it to O(…) because …”
4. **While coding:** Narrate non-obvious indices and invariants (“`left` is always the start of the valid window”).
5. **End:** “Time is O(…), space is O(…). Edge cases: empty input, single element, …”

If stuck: “I’m considering BFS vs DFS — for shortest path in an unweighted graph I’ll use BFS because…”

---

## Revision schedules

### If you have 7 days

| Day | Focus | Action |
|-----|--------|--------|
| 1 | Arrays + hashing | Review [array](../01-data-structures/01-array.md) + [hashing](../01-data-structures/02-hashing.md); 4 problems |
| 2 | Strings + two pointers | [string](../01-data-structures/03-string.md) + sliding window pattern; 4 problems |
| 3 | Trees + BST | [tree](../01-data-structures/08-tree.md); 3 problems |
| 4 | Graphs | [graph](../01-data-structures/13-graphs.md); BFS/DFS/topo; 4 problems |
| 5 | DP | [15-dynamic-programming.md](../02-algorithms/15-dynamic-programming.md) + [recursion-to-dp.md](../02-algorithms/10-recursion-to-dp.md); 4 problems |
| 6 | Heap + binary search + stack | [heap](../01-data-structures/10-heap.md), [binary search](../02-algorithms/11-binary-search.md), [stack](../01-data-structures/05-stack.md); 4 problems |
| 7 | Mixed mock | 2 timed problems (45 min each) + review mistakes |

### If you have 48 hours

- **Hour 0–4:** [Round cheatsheet](#round-cheatsheet-one-page) + redo 2 Medium problems you failed recently.
- **Hour 4–12:** Skim Quick Revision in: array, tree, graph, DP, heap, binary search.
- **Hour 12–24:** One full mock (2 problems); note gaps only.
- **Hour 24–36:** Only gaps + Union-Find + topo sort if weak.
- **Hour 36–48:** Sleep, light review of the round cheatsheet, no new problems.

### Night before

- Skim the **round cheatsheet** and the [L3 cheatsheet](../00-start-here/L3_CHEATSHEET.md) (edge cases, Big-O).
- Do **not** cram new topics; review **one** problem per weak area only.
- Prepare 2–3 questions for your interviewers (team, code review, on-call).

---

## After the interview

- Jot down problems you saw (titles only) while memory is fresh — helps if you have future rounds.
- Regardless of outcome, note **one** pattern to drill next time.

---

# PART D — MOCK ROUNDS

> [!IMPORTANT]
> **How to use this part**: Do these 25 problems **cold** (no notes, 35–45 min per problem). They are ranked by Google L3 frequency. If you can solve all 25 cleanly, you are ready. Do them in order — early problems unlock the patterns you need for later ones.

## Set 1: Must Solve Cleanly (No Hints)

These cover the patterns that appear in **every** Google L3 loop. Inability to solve any of these is a direct reject signal.

| # | Problem | Pattern | Expected Time | Notes |
|---|---------|---------|---------------|-------|
| 1 | **Two Sum** | Hash map | 5 min | Warm-up. Should be reflex. |
| 2 | **Longest Substring Without Repeating Characters** | Sliding window | 10 min | Canonical variable window |
| 3 | **Number of Islands** | DFS/BFS flood fill | 15 min | Grid graph — must be clean |
| 4 | **Binary Tree Level Order Traversal** | BFS | 10 min | Layered BFS template |
| 5 | **Course Schedule** (Cycle detection) | Kahn's topo sort | 20 min | Edge direction gotcha |
| 6 | **Coin Change** | DP (unbounded knapsack) | 20 min | `dp[0]=0`; build bottom-up |
| 7 | **Merge Intervals** | Sorting + greedy | 15 min | Sort by start; check overlap |
| 8 | **Search in Rotated Sorted Array** | Binary search | 15 min | Identify sorted half first |
| 9 | **Valid Parentheses** | Stack | 10 min | Map close→open; stack match |
| 10 | **Group Anagrams** | Hash map + sorted key | 15 min | Key = sorted string |

---

## Set 2: Build Fluency (Aim for Clean First Attempt)

These are the problems that separate L3 hires from strong L3 rejects. You should need no hints.

| # | Problem | Pattern | Expected Time | Notes |
|---|---------|---------|---------------|-------|
| 11 | **Minimum Window Substring** | Sliding window + freq | 30 min | `have` vs `need`; two counters |
| 12 | **Longest Common Subsequence** | 2D DP | 25 min | `dp[i][j]` from scratch |
| 13 | **Word Search** | Backtracking + DFS | 25 min | Mark visited in-place; restore |
| 14 | **Find Median from Data Stream** | Two heaps | 25 min | Max-heap left, min-heap right |
| 15 | **Lowest Common Ancestor (Binary Tree)** | Tree DFS postorder | 20 min | Return node if found; if both sides non-null → LCA |
| 16 | **Pacific Atlantic Water Flow** | Reverse BFS from borders | 30 min | Two BFS sets; intersect |
| 17 | **Jump Game** | Greedy | 15 min | Track furthest reachable |
| 18 | **Kth Largest Element in an Array** | Heap or quickselect | 15 min | Min-heap of size K |
| 19 | **Clone Graph** | BFS + hash map | 20 min | Create clone before recursing |
| 20 | **Combination Sum** | Backtracking | 20 min | `start` index; recurse with `i` (reuse allowed) |

---

## Set 3: Stretch Problems (Common at Google, Separates Offers)

If you can solve all of these, you are overperforming L3 and will likely get a strong hire.

| # | Problem | Pattern | Expected Time | Notes |
|---|---------|---------|---------------|-------|
| 21 | **Word Ladder** | BFS on implicit graph | 35 min | One-letter edits = neighbors; remove from set when visited |
| 22 | **Serialize and Deserialize Binary Tree** | DFS preorder | 35 min | Use `None` markers; split on `,` |
| 23 | **Trapping Rain Water** | Two pointers or monotonic stack | 25 min | Two-pointer: `min(max_l, max_r) - height[i]` |
| 24 | **Maximum Profit in Job Scheduling** | DP + binary search | 40 min | Sort by end time; BS to find non-overlapping previous job |
| 25 | **Alien Dictionary** | Topo sort + edge extraction | 35 min | Compare adjacent words → first diff = edge; cycle → return `""` |

---

## Mock Interview Scoring Guide

For each attempt, score yourself:

| Score | Criteria |
|-------|----------|
| ✅ **Clean** | Solved within time, correct on first run (or found own bug in dry-run), stated complexity correctly |
| ⚠️ **Partial** | Solved but needed 5+ min extra, OR found bug only after interviewer hinted |
| ❌ **Fail** | Did not solve, or solved with major hint, or couldn't state complexity |

**Target before the interview:** ≥ 17/20 on Sets 1+2 at ✅ Clean.

---

## Weak Area Drill List

Use this when a mock attempt reveals a gap:

| Weak Area | Drill These |
|-----------|-------------|
| Sliding window | Minimum Window Substring → Find All Anagrams → Longest Repeating Char Replacement |
| Graph BFS | Rotting Oranges → Walls and Gates → Shortest Path in Binary Matrix |
| Topo sort | Course Schedule II → Alien Dictionary → Sequence Reconstruction |
| Tree DP | Max Path Sum → Diameter → House Robber III |
| 2D DP | Unique Paths → LCS → Edit Distance → Interleaving Strings |
| Backtracking | Subsets → Permutations → N-Queens → Sudoku Solver |
| Heap | Merge K Sorted → Task Scheduler → Ugly Number II |
| Binary search | Koko Eating Bananas → Find Minimum in Rotated Array → Split Array Largest Sum |

---

## L4 (SDE-2) Mock Rounds — follow-up chains

> [!IMPORTANT]
> An L4 round is not one problem — it's a **chain**. Budget 45 min per round: base problem solved cleanly in ~20–25 min, then the interviewer escalates. Simulate that: solve the base, then *without a break* attempt each follow-up. A round "passes" only if you get through follow-up 1. Full L4 bar: [`00-start-here/l4-sde2-delta.md`](../00-start-here/l4-sde2-delta.md).

| Round | Base (20–25 min) | Follow-up 1 | Follow-up 2 (stretch) |
|---|---|---|---|
| A | Insert Delete GetRandom O(1) | allow duplicates | weighted `getRandom` (→ Random Pick with Weight) |
| B | Merge Intervals | bookings arrive online (→ My Calendar I) | reject only triple bookings (→ My Calendar II) |
| C | Network Delay Time (Dijkstra cold) | grid version, minimize max edge (→ Path With Minimum Effort) | at most k stops — why Dijkstra breaks (→ Cheapest Flights) |
| D | LRU Cache | evict by frequency (→ LFU) | thread safety — discuss locking, don't code |
| E | Word Search | many words to find (→ Word Search II, Trie) | prune trie nodes after matches |
| F | Kth Largest in a Stream | median of a stream (→ two heaps) | values can be *corrected* later (→ lazy deletion, Stock Price Fluctuation) |
| G | Longest Increasing Subsequence | O(n log n) version | 2-D: Longest Increasing Path in a Matrix |
| H | Rotting Oranges | BFS from all targets (→ 01 Matrix) | answer counts *routes* not cells (→ Bus Routes) |

Scoring per round: base unsolved = not ready; base + F1 = on the bar; base + F1 + F2 = strong hire territory. Log which *invariant* failed, per the [Pattern Ladders](HOW_TO_THINK.md#the-study-protocol-non-negotiable) protocol.

---

# PART E — SENIOR FOLLOW-UP CHAINS

> [!IMPORTANT]
> **How to use this part:** These are not new problems — they're the standard **third link** in a chain, attached to the `⚡ T1` / `🎯 T2` bases in [Part D](#part-d--mock-rounds) and [`00-start-here/l4-sde2-delta.md`](../00-start-here/l4-sde2-delta.md). At senior level you should propose these escalations yourself before the interviewer asks. Bare `T3` = senior follow-up tier; full tier context: [`00-start-here/sde3-senior-delta.md`](../00-start-here/sde3-senior-delta.md).

## 1. Count-vs-existence

The cheapest senior escalation: "can you also tell me *how many*, not just whether one exists?" Existence checks (any/DFS-early-exit/binary search) often can't be trivially converted — the follow-up is graded on recognizing *when* the existing structure transfers and when it forces a rewrite.

| Base (existence) | Follow-up (count) | Does the structure transfer? |
|---|---|---|
| Word Search (does word exist) | Count all occurrences | Yes — remove early exit, sum instead of return |
| Number of Islands (are there islands) | Max Area of Island / count sizes | Yes — accumulate size during flood fill |
| Course Schedule (can finish) | Count all valid orderings | **No** — becomes combinatorial, needs different approach (backtracking or DP over bitmask, out of scope — say so) |
| Two Sum (does pair exist) | Count pairs summing to target | Yes — hashmap of counts instead of indices |

---

## 2. Streaming / online

Full base structures: [`04-practice/data-structures/10-heap.md`](../04-practice/data-structures/10-heap.md), [`04-practice/data-structures/14-design.md`](../04-practice/data-structures/14-design.md).

| Base (offline, all data upfront) | Streaming follow-up | Key insight |
|---|---|---|
| Kth Largest Element in an Array | Kth Largest in a Stream | Maintain a min-heap of size k; O(log k) per insert instead of full re-sort |
| Find Median of Two Sorted Arrays | Find Median from Data Stream | Two heaps (max-heap left, min-heap right), rebalance on insert |
| Merge Intervals | My Calendar I/II (bookings arrive online) | No global sort available — check overlap against existing intervals on each insert |
| Top K Frequent Elements | Top K Frequent in a stream (bounded memory) | Exact top-k needs full counts; unbounded stream forces approximate (count-min sketch) — name the trade-off |

---

## 3. Update-heavy / deletion-heavy

| Base (static or insert-only) | Follow-up | Key insight |
|---|---|---|
| Kth Largest in a Stream | Values can be corrected/removed later (Stock Price Fluctuation) | Heap doesn't support arbitrary deletion — use **lazy deletion**: pop-and-check against a "stale" hashmap when the top is read |
| LRU Cache | Support deleting a key besides eviction | Must unlink from DLL *and* remove from hashmap — same invariant, extra edge case (key not present) |
| Union-Find (static components) | Support disconnecting an edge | Classic union-find doesn't support split — say so. If all deletions are known upfront, replay them backward as unions; otherwise rebuild (link-cut trees are out of scope) |

---

## 4. Memory-constrained

| Base | Follow-up | Key insight |
|---|---|---|
| Two Sum (hashmap, O(n) space) | What if array doesn't fit in memory? | Sort externally (or if sorted already) → two pointers, O(1) extra space, trade time for space |
| BFS shortest path (visited set) | Graph too large for a visited set in memory | Bidirectional BFS reduces frontier size; or bitset instead of hashset if node IDs are dense integers |
| Sliding Window Maximum (deque) | Window is huge, deque still bounded — note it already *is* memory-efficient (O(k)) | Good place to demonstrate you recognize when no further reduction is needed |

---

## 5. Concurrency discussion

**Discussion only — never implement.** State the shared mutable state, name the hazard, name the fix at a level of "which primitive," not code.

| Structure | Shared state | Hazard | Fix (name it, don't implement) |
|---|---|---|---|
| LRU/LFU Cache | hashmap + DLL | Two threads evict + insert concurrently → corrupted list | Coarse lock around get/put, or read-write lock if reads dominate |
| Rate limiter | request counter/window | Check-then-increment race lets two requests both pass the limit | Atomic compare-and-swap, or move counter to a single-threaded owner (actor model) |
| Producer-consumer (Design Hit Counter under load) | shared counter or queue | Lost updates | Blocking queue with internal lock, or atomic increment |

---

## 6. One-vs-all

| Base (one target) | Follow-up (all targets) | Key insight |
|---|---|---|
| Shortest path to a target node | Shortest path to *all* nodes | Already what BFS/Dijkstra compute — the follow-up is free if you didn't early-exit |
| Validate one BST | Count all ways to build a BST from n nodes | Different problem class (Catalan number / DP) — recognize it's not a tweak |
| Find one anagram substring | Find all anagram substrings (Find All Anagrams) | Same sliding window, don't return early — collect all valid start indices |

---

## 7. Scale-change (100x)

The reflex being tested: does a complexity-class change trigger an unprompted redesign proposal?

| Problem | At n ~ 10^4 | At n ~ 10^7–10^9 | What changes |
|---|---|---|---|
| Any O(n²) DP | Fine | Must reduce — look for O(n log n) reformulation (e.g. LIS via binary search) or state-space reduction | Approach swap, not micro-optimization |
| Any O(n log n) sort-based | Fine | Still fine, usually | Say so and move on — don't over-engineer |
| In-memory hashmap/set of all elements | Fine | May not fit in memory | External sort, streaming, or approximate structure (bloom filter / count-min sketch) |
| Recursive DFS | Fine | Stack overflow risk | Convert to iterative with an explicit stack |

---

## See Also

- [HOW_TO_THINK.md](HOW_TO_THINK.md) — the solve loop, four levers, stuck moves, escalation grammar, pattern ladders
- [RECURSION_AND_DP_MASTERCLASS.md](RECURSION_AND_DP_MASTERCLASS.md) — the contract/induction method this file's proof moves generalize
- [patterns-master.md](patterns-master.md) — triggers, decision trees, DS/algorithm selection
- [TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md](TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md) — canonical problems + variants playbook
- [`00-start-here/L3_CHEATSHEET.md`](../00-start-here/L3_CHEATSHEET.md) — execution timeline, edge-case checklist, keyword → structure tables
- [`00-start-here/sde3-senior-delta.md`](../00-start-here/sde3-senior-delta.md) — senior tier definitions and bar
