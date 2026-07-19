---
module: 03-patterns
topic: Interview Judgment — reasoning tools & live decision-making
tags: [logic, proof, counterexamples, decision-making, interview-strategy, google-l3, l4]
---

# Interview Judgment — Reasoning Tools & Live Decision-Making

> [!IMPORTANT]
> **The missing layer this file adds.** [HOW_TO_THINK.md](HOW_TO_THINK.md) teaches you to *derive* patterns. [The L3 Cheatsheet](../00-L3-EXECUTION-META/L3_CHEATSHEET.md) maps keywords → structures. Neither teaches the two skills that actually decide close interviews: **convincing yourself an idea is correct before spending 15 minutes coding it**, and **making good calls under uncertainty** — commit or pivot, which of two approaches, what to do with a hint, how to recover from a wrong path. Strong candidates don't fail because they lack patterns; they fail because they coded the wrong idea confidently or abandoned the right idea nervously. This file trains that judgment.

---

# PART A — REASONING TOOLS (logic you run before and while coding)

## A1. Examples are experiments — design them, don't just "try one"

Most candidates use examples passively (trace the given sample). Examples are actually your **hypothesis-testing instrument**, and there are exactly four kinds worth constructing, each answering a different question:

| Example type | Question it answers | How to build it |
|---|---|---|
| **Smallest interesting case** | "What does the mechanism look like with no noise?" | n = 2 or 3, the minimum where a real decision occurs. (n = 0/1 are edge cases, not insight cases.) |
| **Structure-revealing case** | "What does my hand do when solving this?" | ~8–10 elements, solve it manually, then *introspect the procedure your eyes ran* — it's often the algorithm |
| **Adversarial case** | "What input would embarrass my current idea?" | Attack your idea's assumption directly: duplicates if you assumed distinct, negatives if you assumed positive, ties if you sort, all-equal elements, already-sorted / reverse-sorted |
| **Boundary case** | "Does the code survive the edges?" | Saved for the dry run — see [Universal Edge Cases](../00-L3-EXECUTION-META/L3_CHEATSHEET.md) |

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

1. **Invariant + induction** (for loops): "True initially; each step preserves it; at termination it implies the answer." This is the loop version of the DP contract / leap of faith ([Masterclass §1.2](RECURSION_AND_DP_MASTERCLASS.md)) — the same induction, standing up instead of recursing down.
2. **Exchange argument** (for greedy): "Take any optimal solution that disagrees with my first choice; swap my choice in; it got no worse; induct." Thirty spoken seconds. If you can't sketch it, downgrade your confidence in the greedy ([HOW_TO_THINK.md — Greedy](HOW_TO_THINK.md)).
3. **No-candidate-escapes** (for discard-based patterns — two pointers, monotonic stack, binary search halving): "I only ever discard candidates that are *dominated* — here's the one-line domination proof — so the answer is never discarded." When you move a pointer, be able to finish the sentence "…and this can't skip the answer because ___."

L3 bar: run these when asked. L4 bar: run move 2 or 3 *unprompted* in one sentence as you make the choice ("moving the shorter wall is safe because keeping it caps every future area"). One sentence, not a lecture.

## A4. Estimate before you build — the 30-second feasibility check

Before committing to an approach, multiply it out: *states × work per state*, or *iterations × cost per iteration*, against ~10⁷–10⁸ simple operations/second. "n = 10⁵, my idea is O(n²) = 10¹⁰ — dead on arrival, don't code it." This one habit prevents the most expensive interview failure mode: 20 minutes implementing something that could never pass, discovered only when the interviewer asks for complexity. Feasibility math comes *before* implementation, always — it's step 2 of the [solve loop](HOW_TO_THINK.md) for exactly this reason.

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
3. **Extendability** — only as a tiebreak, and only if you've internalized the [escalation grammar](HOW_TO_THINK.md): which version survives "now it's a stream / now return all of them"?

Then do the senior move: **offer the decision.** "I see a two-heap O(log n) design and a simpler sort-based O(n log n) per query; given 45 minutes I'd code the sort version and talk through the heap upgrade — sound good?" This shows both ideas, converts a private gamble into a shared plan, and interviewers almost always respond well to it. Choosing silently forfeits the credit for the road not taken.

## B3. Hints are data — decode them, don't survive them

A hint is not a deduction on your scorecard by itself; *missing* the hint is. Interviewer utterances come in three intensities, and each demands a different response:

| Signal | What it actually means | Correct response |
|---|---|---|
| "Are you sure that handles X?" / "Walk me through X" | **There is a bug, and X triggers it.** This is never idle curiosity. | Stop. Trace X honestly and slowly. Do not say "yes it's fine" from memory — that answer, wrong, is the worst moment available in an interview. |
| "Is there anything about the input you're not using?" / "What if it were sorted?" | You've missed the intended lever; they're pointing at it. | Take it fully: re-run the [stuck moves](HOW_TO_THINK.md) *with their ingredient as the axis*. Half-taking a hint (nodding, continuing as before) reads worse than needing it. |
| "OK. What's the complexity?" (mid-implementation) | Your approach is too slow and they're inviting you to notice. | Actually recompute it fresh — don't repeat your earlier claim. Then: "…which is n², too slow for this n — the bottleneck is this inner scan; replacing it with ___." |
| Silence while you're stuck | You've been quiet too long. | Narrate your candidate directions and *ask a real question*: "I'm deciding between modeling this as a graph or as intervals — is one of those a dead end?" Asking a specific question is fine; asking "am I on the right track?" repeatedly is not. |

Meta-rule: **a used hint costs a little; a wasted hint costs a lot.** When one arrives, treat it as the highest-priority input in the room — the interviewer just told you where the points are.

## B4. Recovery playbook — the three failure moments, scripted

Pre-scripting these turns panic moments into procedure. Each has a wrong instinct to override.

**Dry run exposes a bug (minute ~37).** Wrong instinct: patch the symptom at the line where the trace went wrong. Right procedure: (1) say "good — found a bug" in an even tone (composure here is graded); (2) classify before touching code — is it the *invariant* (idea wrong: needs thought, maybe a `while` should be `if`) or the *transcription* (idea right, code wrong: off-by-one, swapped args — safe to fix locally)? (3) fix at the cause, re-run the trace *from the failing step*, and also check the fix against one boundary case — symptom-patches breed sibling bugs and interviewers watch for whack-a-mole.

**Approach collapses at minute 25.** (You now have evidence it can't work.) Not recoverable to full marks — recoverable to a hire: (1) say precisely *what* broke: "this window invariant dies with negative numbers — growing the window no longer moves the sum one way"; naming the cause proves the understanding the broken code can't. (2) Ask for the direction check *once*: "I think the fix is prefix sums + a hashmap — before I rebuild, does that direction make sense?" (When one approach has died, one direction-check is free; two is a pattern.) (3) Rebuild only what changed — most scaffolding (I/O, loops, helpers) usually survives.

**Total blank at minute 5.** Wrong instinct: silence, or re-reading the problem a fourth time. Right procedure — this is exactly what the [solve loop](HOW_TO_THINK.md) steps 3–5 are *for*: solve a 10-element case by hand and watch your hand; say the brute force out loud with its complexity (this always exists — "try every subarray: O(n²)"); name its waste. Speaking the brute force has a second function beyond points: it breaks the freeze. Motion creates thought, not the other way around.

## B5. Trade-offs — always present them as a menu, never as a monologue

When multiple legitimate versions exist (time vs space, simple vs optimal, sorted vs hashed), the L4-shaped move is a **priced menu plus a recommendation**:

> "Option A: sort in place, O(n log n), destroys input order. Option B: hashmap, O(n) time but O(n) extra space. If the array is reusable I'd take B; if memory is the constraint, A. I'll default to B."

Three sentences. It demonstrates you see the whole space, it hands the interviewer a steering wheel (they often reveal hidden requirements in response — "actually, memory is tight" tells you the follow-up), and it's the miniature of real engineering judgment, which is what the whole exercise is a proxy for. Deciding silently gets you graded only on the branch you took.

## B6. The judgment drill (how to train any of this)

Judgment doesn't improve by reading — it improves by *forcing the decision points to be explicit* in practice:

1. **Timestamp your mocks.** Note the clock when you commit to an approach, when doubts appear, and when you pivot. Review: was each pivot evidence-based or discomfort-based (B1)? Most people discover they pivot on discomfort and grind on sunk cost — the exact opposite of the rule.
2. **Pre-mortem every commit.** Before coding, one sentence: "the most likely way this approach fails is ___." (Trains A1's adversarial instinct; also catches missing state dimensions early.)
3. **Play interviewer.** Once a week, take a problem you know cold and write the three hints you'd give a struggling candidate, in escalating order. Nothing teaches hint-*decoding* (B3) faster than authoring hints.
4. **Log misses by decision, not by topic** — extend the [training protocol](HOW_TO_THINK.md): was the failure a pattern gap, or a judgment failure (ignored the 10-minute checkpoint, defended instead of traced, silent trade-off)? Most candidates past 100 solved problems miss on judgment, not patterns — which means this log, not more problems, is where the next hire-signal comes from.

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

## See Also

- [HOW_TO_THINK.md](HOW_TO_THINK.md) — the solve loop, four levers, stuck moves, escalation grammar
- [RECURSION_AND_DP_MASTERCLASS.md](RECURSION_AND_DP_MASTERCLASS.md) — the contract/induction method this file's proof moves generalize
- [`00-L3-EXECUTION-META/L3_CHEATSHEET.md`](../00-L3-EXECUTION-META/L3_CHEATSHEET.md) — execution timeline, edge-case checklist, keyword → structure tables
- [MOCK_INTERVIEW_SET.md](MOCK_INTERVIEW_SET.md) — where to run the judgment drills
