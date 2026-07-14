---
module: 03-patterns
topic: How to Think — first-principles pattern intuition
tags: [patterns, intuition, first-principles, google-l3, l4]
---

# How to Think — Building Pattern Intuition from First Principles

> [!IMPORTANT]
> **What this file is.** Every other file in this repo tells you *what* the patterns are. This one builds the machine in your head that **derives** them. Read a chapter, close the file, and re-derive the pattern on paper from its core question — if you can't, re-read. The goal: given a problem you have never seen, you reconstruct the right approach from reasoning, not recall.
>
> Pair it with [PATTERN_LADDERS.md](PATTERN_LADDERS.md): this file = *why each pattern works*; the ladders = *graded problems to pressure-test it*.

---

# PART I — THE OPERATING SYSTEM

Before any pattern: the fixed mental procedure that every solve runs on. Patterns are plugins; this is the OS.

## 1. There are only four ways an algorithm gets faster

Every optimization you will ever perform in an interview is one of these four levers. When your brute force is too slow, you are not searching a library of 200 tricks — you are asking four questions:

| # | Lever | The question you ask | Patterns it spawns |
|---|---|---|---|
| 1 | **Remember instead of recompute** | "Am I calculating the same thing twice?" | Hashing, prefix sums, memoization/DP |
| 2 | **Exploit order** | "If the data were sorted / processed in the right order, what becomes obvious?" | Sorting, binary search, two pointers, greedy, sweep line, topo sort |
| 3 | **Discard provably useless work** | "Can I *prove* some candidate can never be the answer?" | Two pointers, sliding window, monotonic stack/deque, greedy exchange, pruning |
| 4 | **Choose a structure whose cheap operation is your hot operation** | "What operation do I do millions of times, and what makes *that one* O(1)/O(log n)?" | Heap, hash map, trie, union-find, deque, design-a-DS composition |

This is the deepest idea in the file. **A brute force is slow because it contains waste. Name the waste, and the waste names the pattern.**

- Recomputing overlapping windows → lever 3 → sliding window.
- Re-scanning for a partner element → lever 1 → hash map.
- Re-solving the same subproblem in recursion → lever 1 → DP.
- Re-scanning right for the next greater element → lever 3 → monotonic stack.
- Repeatedly finding min of a shrinking set → lever 4 → heap.

## 2. The solve loop (run this every single time)

```
1. RESTATE   — say the problem back in your own words; ask 2–3 clarifying
               questions (empty input? duplicates? negative numbers? sorted?)
2. CONSTRAINTS → BUDGET — read n; convert to target complexity (§3)
3. EXAMPLES  — work ONE small example BY HAND, slowly. Watch what your
               brain does. Your hand-solution usually contains the algorithm.
4. BRUTE FORCE — state it out loud with its complexity. Never skip this;
               it is the raw material the levers act on.
5. NAME THE WASTE — what does the brute force recompute / re-scan / re-check?
6. PULL A LEVER — the waste points at one of the four levers → pattern.
7. INVARIANT  — before coding, state the one sentence that stays true
               throughout your algorithm ("everything left of `write` is
               final", "the heap holds the k best so far"). Code enforces
               the invariant; the invariant IS the solution.
8. CODE      — smallest clean version. Helper functions for anything ≥ 5 lines.
9. DRY RUN   — trace your example + one edge case through the actual code,
               tracking variables in a table. Not in your head.
10. COMPLEXITY — state time and space unprompted.
```

Steps 3–7 are the thinking. Steps 1, 2, 9, 10 are where hires and rejects are separated at equal skill. Step 5 is the one nobody practices — drill it deliberately.

## 3. Constraints are the answer key

The interviewer hands you the target complexity inside `n`. Decode it *before* thinking about approaches — it eliminates most of the pattern space instantly:

| n up to | Budget | What it's telling you |
|---|---|---|
| ~20 | O(2ⁿ), O(n·2ⁿ) | Exhaustive search is *intended*: backtracking, subsets, bitmask |
| ~500 | O(n³) | Nested DP (interval DP), Floyd-style thinking |
| ~5,000 | O(n²) | 2D DP, all-pairs comparison is fine |
| ~10⁵–10⁶ | O(n log n), O(n) | Sort / heap / binary search / one pass with a structure |
| ~10⁹+ or "stream" | O(log n), O(1)/element | Binary search on answer, math, or fixed-size state |

Two corollaries:
- If n ≤ 20 and you're constructing a clever greedy, **stop** — they want the search tree.
- If n = 10⁵ and your idea is O(n²), don't code it hoping — return to step 5 and find the waste.

## 4. When you are truly stuck — the seven moves

Run these in order; each takes under a minute. This list is what "solving an unseen problem" actually looks like from inside:

1. **Solve it by hand, bigger.** Take a 10-element example and get the answer manually. Then introspect: *how did my eyes find it?* Your eyes ran an algorithm — often the intended one (they jumped to the largest? sorted mentally? scanned once keeping a running best?).
2. **Sort it and look again.** Half of all array problems become easy under a sort the moment the problem doesn't depend on original positions (and if you need positions back, sort `(value, index)` pairs).
3. **Ask "what would I precompute?"** If someone let you build any lookup table before answering queries, what table makes each query O(1)? That table is often a prefix sum, hash map, or next-smaller array — buildable in one pass.
4. **Reverse the direction.** Process right-to-left, leaves-to-root, destination-to-source, last decision instead of first. (Pacific-Atlantic: flowing water *from* the oceans inward turns 2n BFS into 2. "Last stone to be removed" → think about what's removed first from the reversed sequence, i.e., union-find additions.)
5. **Reframe as a graph.** If there are "states" and "moves" — configurations, words differing by one letter, (position, fuel) pairs — the problem is BFS/DFS/Dijkstra over an implicit graph, and the hard part is only defining node + edge (§Graphs).
6. **Fix one variable, solve for the rest.** "For each right endpoint, what's the best left?" "For each element, in how many subarrays is it the minimum?" Fixing one thing converts a 2D question into n instances of a 1D question — the reframe behind sliding window, contribution counting, and most hard-medium problems.
7. **Binary search the answer.** If you can't *find* the optimum but could *verify* a proposed value ("could we finish within capacity c?") — and verification is monotone — you don't need to find it; bisect it (§Binary Search).

If all seven fail, simplify the problem (drop a constraint, shrink to 1D, assume no duplicates), solve the simplification, then add the constraint back and see what breaks. What breaks tells you what the missing dimension of state is.

---

# PART II — THE PATTERNS, DERIVED

Each chapter has the same shape: **core question → derivation from the brute force → the invariant → triggers → where it breaks → how interviewers escalate it.** The derivation is the part to internalize; the day you can reproduce it, you no longer need the template.

---

## Hashing — buy O(1) answers to "have I seen it?"

**Core question:** *does X exist / how many times / where* — answered in O(1) instead of a scan.

**Derivation.** Two Sum brute force is O(n²): for each element, scan for its partner. Notice what the inner loop *is*: a lookup. The element you're searching for is **computable** from the current one (`target - x`). Any time the inner loop of a double-loop is "find a value with a computable property," replace it with a map you fill as you go: *for each element, (a) ask the map about the partner it needs, (b) insert itself for future elements.* One pass, each element plays both roles.

**The deeper skill — canonical keys.** Hashing groups things that are "the same under some equivalence." You make them *literally equal* by mapping each to a canonical form, then group by key:
- Anagrams → key = sorted string (or 26-count tuple).
- "Same set of characters" → frozenset.
- Points on one line through origin → key = slope as a *reduced fraction pair*, never a float.
- Shifted strings ("abc"~"bcd") → key = tuple of gaps between consecutive chars.

Inventing the canonical key **is** the solution; the dictionary is bookkeeping.

**Prefix + hash (the composed form).** "Count subarrays with sum exactly k" — sums of subarrays are differences of prefix sums, so `sum(i..j) = k` ⟺ `prefix[j] - prefix[i-1] = k` ⟺ *I'm at j with prefix p; how many earlier prefixes equal p - k?* — a seen-count question. Store `count[prefix] += 1` as you sweep. (Seed `count[0] = 1`: the empty prefix is a legal left boundary — forgetting it is *the* classic bug.) This works where sliding window fails (negative numbers), and the same skeleton handles "sum divisible by k" (key = prefix mod k) and "equal 0s and 1s" (map 0→−1, key = running sum).

**Triggers:** count/exists/first duplicate · pairs with computable partner · "group the …" · subarray sums with negatives · O(n) demanded where the obvious answer is O(n log n).
**Breaks when:** the question is a *range or inequality* ("nearest value ≤ x") — hash keys are exact; you need sorted order (binary search / SortedList) · keys are floats — canonicalize to integers/fractions first.
**Escalation:** "input is a stream" → same map, wrapped in a class · "memory-bound" → talk hashing per-shard / count-min sketch conceptually.

---

## Two Pointers — discard candidates with a one-line proof

**Core question:** which pairs/ranges can I *prove* useless without looking at them?

**Derivation.** Pair-sum in a **sorted** array, pointers at both ends. If `a[l] + a[r] < target`: every other partner for `l` is `≤ a[r]`, so every pair involving `l` is *also* too small — all n of them die in one comparison, and `l++` is proven safe. That's the whole pattern: **each step eliminates a whole family of candidates, with a proof that sortedness supplies.** O(n²) candidates, O(n) steps.

**Don't memorize which pointer moves — derive it live:** "which pointer's remaining candidate set just became provably empty?" That question answers every variant, including container-with-most-water (move the shorter wall: keeping it caps every future area at its height × smaller width) and 3Sum (fix one element, two-pointer the rest — move 6 of §4).

**Three shapes, one idea:**
1. **Opposite ends, converging** — pair sums, container, palindrome check.
2. **Same direction, reader/writer** — in-place dedup/removal. Invariant: *everything left of `write` is the final answer so far.* The writer never waits; the reader skips garbage.
3. **Two sequences, merge walk** — merge step, intersection of sorted lists, interval intersection. Invariant: *everything behind both pointers is fully processed;* advance whichever element is smaller (it can't match anything ahead).

**Triggers:** sorted (or sortable) + pairs/triples · in-place with O(1) space · palindromes · merging two sorted anythings.
**Breaks when:** you can't prove either move safe (both directions might hold the answer) — you don't have the discard proof, you have a search problem: hash, binary search, or DP instead · original indices required and sorting scrambles them → sort `(val, idx)` or use hashing.
**Escalation:** 2Sum → 3Sum → 3Sum-closest → k-Sum (recursive reduction: k-Sum = fix one + (k−1)-Sum, base case two pointers).

---

## Sliding Window — two pointers where the answer is a range

**Core question:** best/count of **contiguous** subarrays satisfying a condition — without re-examining O(n²) of them.

**Derivation.** Brute force enumerates all windows: O(n²) windows × O(n) evaluation. Two separate wastes, two separate fixes:
1. *Evaluation waste:* adjacent windows share almost everything — maintain the stats (running sum, char counts) incrementally: +arriving element, −leaving element. Evaluation becomes O(1).
2. *Enumeration waste:* this is the subtle one, and it needs a property called **monotonicity of validity**: growing the window only pushes it one way (e.g., adding chars can only *add* duplicates; removing chars can only *fix* them). Under that property, for each right endpoint there is a single frontier left endpoint, and the frontier only moves rightward — so `left` moves ≤ n times total. Both pointers move n times: **O(n) amortized**, even with the nested `while`.

**The universal template, derived not recalled:**
```
for right in range(n):        # admit a[right] into the window's stats
    while window invalid:     # restore the invariant
        evict a[left]; left += 1
    record answer             # window [left, right] is the best ending at right
```
For "longest valid" you record after restoring validity; for "shortest satisfying" flip it — shrink *while still valid*, recording as you shrink. Don't memorize the flip; re-derive it from *which side of the validity boundary the answer sits on*.

**Two power moves:**
- **"Exactly k" is hard, "at most k" is easy** → `exactly(k) = atMost(k) − atMost(k−1)`. (Subarrays with exactly k odd numbers / k distinct elements.)
- **Window max/min** → sums update incrementally but max doesn't (evicting the max forces a re-scan). Fix with a **monotonic deque**: as `x` arrives, pop from the back everything smaller — those elements are *younger-side-dominated*: older AND smaller than x, so never the max of any future window. Front = current max; pop the front when it slides out. Same discard-with-proof logic as the monotonic stack.

**Triggers:** "longest/shortest/count subarray|substring with …" · "at most/exactly k distinct" · fixed window size k.
**Breaks when:** **negative numbers** with a sum condition — growing the window no longer monotonically grows the sum, the frontier logic dies → prefix sum + hash (exact sum) or prefix + monotonic deque (shortest subarray ≥ k, hard) · condition on a non-contiguous subsequence → it was never a window problem; think DP/greedy.
**Escalation:** fixed window → variable → "exactly k" → stream version ("design a class receiving one element at a time" — your incremental stats *are already* that class; say so).

---

## Prefix Sums & Difference Arrays — answer ranges by subtracting

**Core question:** many range-sum queries, or many range-updates, on data that (mostly) doesn't change.

**Derivation.** `sum(i..j)` re-adds the same elements across queries → lever 1: precompute cumulative `P` where `P[i] = a[0..i-1]`, then any range is `P[j+1] − P[i]`, O(1) per query after O(n) once. The **dual** trick: many range *updates*, one final read → difference array: `d[l] += v, d[r+1] -= v`, prefix-scan at the end materializes every update simultaneously. (Car Pooling: +passengers at pickup, − at drop, scan and compare to capacity. Meeting Rooms II is the same with +1/−1 events.)

**Recognize the disguises:** "equal number of 0s and 1s" (map to ±1, look for repeated running sum) · 2D version for submatrix sums (inclusion–exclusion corners) · "product of array except self" = prefix product × suffix product — prefix thinking isn't only about `+`, it's about any operation you can accumulate from both sides.

**Triggers:** repeated range queries, no updates · many range updates, deferred read · "subarray sum/count" with negatives present.
**Breaks when:** interleaved updates *and* queries → that's segment-tree territory, which is **out of scope — say the name and move on**; in-scope problems always let you use one of the two pure forms.

---

## Binary Search — bisect a monotone predicate, not an array

**Core question:** where does a predicate flip from False to True?

**Derivation.** Forget "find x in a sorted array" — that's one special case. The general object is a predicate `check(v)` over an ordered domain that looks like `F F F F T T T` — once true, true forever. One probe at the midpoint kills half the domain, because monotonicity extends one sample to an infinite conclusion. Everything else is bookkeeping. Designing a binary search = exactly two steps:
1. **Invent `check` and argue its monotonicity out loud.** This is the entire intellectual content.
2. Run the boundary template you never vary: `lo, hi = first_possible, last_possible; while lo < hi: mid = (lo+hi)//2; hi = mid if check(mid) else (lo := mid+1)` → `lo` is the first True. One template, memorized once, zero off-by-one bugs — all four "which template?" dilemmas dissolve if you always search for *the boundary*.

**Search on answer — the L4 form.** You can't compute "minimum ship capacity to finish in D days" directly, but you can **verify** a proposed capacity in O(n) (greedy-fill the days). And feasibility is monotone: more capacity never hurts. So bisect capacity: Koko's bananas, Split Array Largest Sum, Minimum Days to Make Bouquets — all the same three sentences: *identify the answer axis, write the O(n) feasibility check, argue monotonicity.* Trigger phrase: **"minimize the maximum"** or **"maximize the minimum"** — that phrasing is nearly always this pattern.

**Rotated arrays** — no global order, but `mid` vs `hi` tells you which half is internally sorted; the sorted half answers "is the target in me?" in O(1), so you always discard half. The lesson generalizes: binary search survives *partial* order if every probe still yields a provable half-discard.

**Triggers:** sorted anything · O(log n) demanded · min-max / max-min phrasing · "least/greatest value such that…" · answer numeric with checkable feasibility.
**Breaks when:** the predicate isn't monotone (feasibility flickers) — no boundary exists to find · unsorted and unsortable → hashing or selection algorithms.
**Escalation:** array search → rotated → rotated with duplicates (worst case degrades to O(n) — say why: `a[mid] == a[hi]` gives no discard proof) → search on answer → 2D (treat matrix as one flat sorted array, or staircase-walk from a corner).

---

## Stacks & Monotonic Stacks — deferred work, resolved most-recent-first

**Core question (plain stack):** things open and must close in reverse order — who's waiting, and who's next to resolve?

Parentheses, nested parsing (`decode string`, calculators), undo, DFS — whenever the *innermost/most recent* pending thing completes first, the stack is the physically correct structure, not a trick. For nested parsing the invariant is: **on entering a nested scope push the outer context (result-so-far, multiplier/sign), on leaving pop and combine.** Derive any calculator/decoder from that sentence.

**Monotonic stack — derivation.** "Next greater element to the right," brute force O(n²) re-scans. Watch what happens when a new element `x` arrives: every unresolved element *smaller than x* just found its answer (it's x). Pop them, record, done — and here's the crucial second observation: after x arrives, those popped elements could never have been anyone's "nearest greater" anyway (x is closer *and* bigger — they're dominated). So nothing is lost by removing them. What survives on the stack is always a decreasing sequence — not because you enforce it, but as a *consequence* of resolving on arrival. Each element pushes once, pops once: O(n).

**To re-derive the direction rules** (instead of memorizing four cases): the stack holds *the unresolved*; you pop when the newcomer *is* someone's answer. Looking for next **greater** → pops happen when newcomer is bigger → stack stays decreasing. Next smaller → mirror. Scanning right-to-left answers "nearest to the right" questions with what's ahead — but the left-to-right resolve-on-arrival form usually reads cleaner.

**Contribution counting — the L4 reframe.** "Sum of min over all subarrays" looks like it needs all O(n²) subarrays. Flip which thing you enumerate (move 6 of §4): *for each element, count the subarrays where it is the minimum* — that's `(distance to previous smaller) × (distance to next smaller)` choices of boundary, both distances read off a monotonic stack. Largest Rectangle in Histogram is the same idea with area; use strict `<` on one side and `≤` on the other so ties are counted exactly once. When you see "sum/max over all subarrays of some per-subarray statistic," think contribution, not enumeration.

**Triggers:** nested/matched structure · next/previous greater/smaller · spans, temperatures, "how far can it see" · histogram areas · "sum over all subarrays of …".
**Breaks when:** resolution order isn't most-recent-first (earliest-first → queue; priority-based → heap).
**Escalation:** Daily Temperatures → Largest Rectangle → Maximal Rectangle (histogram per row) → Sum of Subarray Minimums → Car Fleet (stack of fleet arrival times).

---

## Heaps — a changing collection where only the extreme matters

**Core question:** repeatedly fetch the min/max of a set that keeps changing.

**Derivation.** Sorting gives all n ranks but costs O(n log n) *per change*. If between changes you only ever look at the top, sorting maintains n−1 answers nobody asked for. A heap maintains exactly one guarantee — root is the extreme — for O(log n) per change. **Weakest sufficient structure = fastest.** Same logic downstream: need full sorted order → sort; need arbitrary-rank queries → SortedList/BST; need only the top → heap.

**The k-gatekeeper.** "kth largest / top-k of a big stream": min-heap of size k. Invariant: *the heap holds the k best seen so far; the root is the worst of the best* — the gatekeeper every newcomer must beat to enter. n elements × log k. Note the polarity flip that trips everyone: k **largest** ⇒ **min**-heap (you evict the smallest of your keepers, so the smallest must be on top). Re-derive from "who gets evicted?" every time.

**Two heaps = a maintained partition.** Stream median: max-heap owns the smaller half, min-heap the larger; the two roots bracket the median. Invariants: every left ≤ every right, sizes within 1 — rebalance by shuttling one root across. Whenever an answer is defined by a *cut point* in sorted order (median, k-th boundary, IQR), maintain the two sides as opposing heaps.

**K-way merge.** Merging k sorted lists: the next output is the min of k candidate heads → heap of `(value, which_list)`, pop one push one. Also the shape of "smallest range covering k lists" and "k smallest pair sums."

**Lazy deletion — the L4 trick.** Heaps can't delete from the middle. Don't: keep a source-of-truth map, let stale entries rot in the heap, and **validate on pop** ("is the top still what the map says? no → discard, pop again"). Amortized fine — each element is purged once. This is Stock Price Fluctuation and Sliding Window Median; naming the trick unprompted is an L4 signal.

**Triggers:** kth / top-k / k closest · stream + extremes · merge k sorted · "most frequent first" scheduling (Task Scheduler) · repeatedly combine two smallest.
**Breaks when:** static array, single kth query → quickselect gives O(n) average (mention it, code the heap) · need arbitrary-position queries → sorted structure · need FIFO within priority → note tie-breaking in the tuple.
**Escalation:** Kth Largest → stream class → two-heap median → lazy deletion → "heap doesn't fit in memory?" (per-shard top-k, merge the k-lists — say it, don't code it).

---

## Linked Lists — pointer surgery under an invariant

**Core question:** re-wire nodes in place without losing the rest of the list.

There is no algorithmic depth here; there is *procedural* depth. Three disciplines cover every problem:
1. **Draw it.** Boxes and arrows for a 3-node example. Every operation = redirecting arrows; the code transcribes your drawing. Reversal derived, not recalled: `nxt = cur.next` (save before breaking — the rule that prevents every lost-list bug), `cur.next = prev`, advance both.
2. **Dummy head.** A sentinel before the real head makes "the head might change / be deleted" a non-special case. Cost: one line. Use it by default in merge/delete/partition problems.
3. **Fast & slow.** Two runners, speeds 2 and 1. Cycle detection: in a cycle the gap closes by exactly 1 per step, so they *must* meet (that one-line proof is what interviewers want). Midpoint: when fast hits the end, slow is halfway. Kth-from-end: two pointers offset by k — a *gap* invariant instead of a speed invariant.

**Composition role:** linked lists reappear at L4 inside design problems — LRU = hash map (O(1) find) + doubly linked list (O(1) reorder/evict), each structure covering the other's weak op. See §Design.

**Triggers:** in-place, O(1) space, "reverse/reorder/merge/split" on a list · cycle questions · "middle/kth from end in one pass".
**Breaks when:** you need random access or sorting → copy to array first *if allowed*; the interviewer forbidding it is precisely the point of the question.

---

## Trees & Recursion — trust the contract, don't trace the calls

**Core question:** the structure is recursive; make your reasoning recursive too.

**The mental leap that unlocks all tree problems:** stop simulating the call stack. Define the function by its **contract** and *assume it works* on subtrees while writing it — the same act of faith as induction. Design any tree recursion by answering three questions:
1. **What does a call return to its parent?** (the contract — e.g., "height of my subtree", "is my subtree a valid BST and what's its min/max")
2. **How do I combine children's answers** (+ my node) into mine?
3. **Base case** — almost always `if not node: return <identity>`.

**The classic wrinkle — path answers.** Diameter / max path sum: the value the *parent needs* (best downward path through me — parent can only extend one arm) differs from the value the *answer needs* (best arch through me — both arms). Resolution: **return the parent's quantity, update a global/nonlocal with the answer's quantity.** Whenever a tree problem feels impossible, check if you're forcing one return value to serve both roles.

**Top-down vs bottom-up — choose by information flow:** data flows parent→child (path sums so far, depth, allowed min/max bounds) → pass parameters, preorder-shaped. Data flows children→parent (heights, subtree sums, validity) → use return values, postorder-shaped. Both at once is fine — parameters down, returns up. **BFS instead of DFS** exactly when *levels* are the subject: level order, right side view, zigzag, minimum depth (BFS may stop early; DFS must finish).

**BST = the invariant "inorder is sorted."** Every BST problem exploits it: validation (pass down (lo, hi) bounds — comparing only to the parent is *the* famous wrong answer), kth smallest (inorder walk, count down), LCA in BST (both smaller → go left; both bigger → go right; split → found; no recursion needed). If a "tree" problem gives you a BST and your solution never uses the ordering, you've missed the intended solution.

**Serialization:** preorder + explicit `None` markers makes structure recoverable by a recursive reader that consumes tokens in order — the same trust-the-contract construction run in reverse.

**Triggers:** any tree · "…of the subtree" (bottom-up) · "…along a path from root" (top-down) · levels (BFS) · sorted-order anything on a BST (inorder).
**Breaks when:** n up to 10⁵ with a skewed tree → Python recursion limit; mention the iterative-stack rewrite exists, `sys.setrecursionlimit` in a pinch.
**Escalation:** height → balanced → diameter → max path sum (each adds one twist to the same contract) · LCA → LCA with parent pointers (→ intersection-of-lists) → LCA of deepest leaves.

---

## Tries — pay for each prefix once

**Core question:** many string queries that share prefixes — stop re-walking the shared part.

**Derivation.** Searching m words against a dictionary compares common prefixes over and over (lever 1). Merge all words into one tree where each node = "the set of words beginning with this prefix": now every prefix in the universe is walked exactly once, lookups cost O(len), independent of dictionary size. A trie node is honestly just `{children: dict, is_word: bool}` — 6 lines; never let the "class Trie" framing make it feel heavier than that.

**The real power move — trie as a search-state machine.** Word Search II (find 100 words in a grid): DFS-ing per word repeats grid work 100×. Instead, DFS the grid **once** carrying a trie pointer: the current trie node *is* "the set of dictionary words still consistent with my path," and `char not in node.children` prunes the entire branch for all words simultaneously. Whenever you'd run the same backtracking once per pattern, ask if a trie can carry all patterns through one search.

**Triggers:** prefix queries / autocomplete / startsWith · many words, one text or grid · "word formed of other words" (word break with dictionary) · wildcard `.` matching (branch over all children at the dot).
**Breaks when:** substring (not prefix) queries — trie of suffixes is out of scope; say "suffix structures exist" and offer the n² DP or rolling-hash alternative.
**Escalation:** implement Trie → wildcard search → Word Search II → prune dead trie nodes after a match (delete `is_word`, drop empty children — the natural F2).

---

## Graphs — the skill is modeling; the algorithms are a lookup table

**Core question:** what are the nodes, what are the edges? Everything after that is mechanical.

**The inversion to internalize:** interview graph problems are rarely hard because of the algorithm — BFS is 10 lines — they're hard because **the graph is hidden.** Nodes are *states*, not necessarily things named in the problem:

| Problem surface | Actual node | Actual edge |
|---|---|---|
| Word Ladder | a word | differs by one letter |
| Snakes & Ladders | board square (post-teleport) | one dice roll |
| Bus Routes | a **route** (not a stop!) | routes sharing a stop |
| Open the Lock | 4-digit combination | one wheel turn |
| Water-jug / game puzzles | full configuration | one legal move |
| Course Schedule | a course | prerequisite |

The Bus Routes row is the meta-lesson: **choose the node so that edge-count = the quantity being minimized.** BFS counts edges; if the answer counts buses, nodes must be routes. When a BFS gives "right structure, wrong number," your node choice is off by one level.

**Algorithm selection — decided by two questions** (*are edges weighted? what's being asked?*):

| Ask | Unweighted | Weighted ≥ 0 | Notes |
|---|---|---|---|
| Shortest path | **BFS** | **Dijkstra** | BFS-with-costs is the classic wrong answer — queue order stops meaning distance the moment edges have weights |
| Reachability / components / count / flood fill | DFS or BFS | same | pick whichever you write cleanest |
| Valid ordering under dependencies / cycle in a DAG | **Topo (Kahn's)** | — | `processed < n` ⟺ cycle |
| Connectivity that *changes* (edges added over time, merge accounts) | **Union-Find** | — | inverse thinking: deletions offline = additions reversed |
| Shortest with ≤ k edges / negative edges | — | **Bellman-Ford, k rounds** | Dijkstra's greedy commit is exactly what a stop-budget breaks |
| Minimize the *maximum* edge on a path | — | Dijkstra variant (relax with `max`) or binary search + BFS | Path With Minimum Effort, Swim in Water |

**The five mechanical disciplines** (every graph bug in interviews is one of these):
1. Mark visited **on enqueue**, not on dequeue — else the queue fills with duplicates (correct but silently quadratic).
2. Multi-source BFS: seed the queue with *all* sources at distance 0 (Rotting Oranges, 01-Matrix, distance-from-any-exit). "Distance to nearest X" ⇒ BFS **from all X**, not from each cell.
3. Grid = graph with 4 implicit edges; directions tuple `((1,0),(-1,0),(0,1),(0,-1))`, bounds-check helper.
4. Dijkstra in Python = `(dist, node)` heap + skip-if-stale on pop (`if d > dist[node]: continue` — lazy deletion again). Know it cold at L4.
5. Kahn's: in-degrees, queue of zeros, count processed. Topological order also = the safe evaluation order for **DAG DP** (Longest Increasing Path: strictly-increasing moves ⇒ no cycles ⇒ DFS + memo with no visited set — say "it's a DAG" out loud, that's the point being tested).

**Triggers:** explicit graphs · grids · dependencies ("must come before") · transformations between states ("minimum operations to reach") · "connected", "spread", "infection", "islands".
**Escalation ladders:** Islands → count → largest → number of *distinct shapes* (canonical path-signature — hashing crossover!) → islands added dynamically (Union-Find, Islands II) · Network Delay → Min Effort (minimize max) → Cheapest Flights (k stops — why Dijkstra breaks) · Word Ladder → Word Ladder II (BFS parents + backtrack; never collect paths during BFS).

---

## Backtracking — exhaustive search with a disciplined skeleton

**Core question:** enumerate all solutions (or find one) when n is small enough that trying everything is *intended*.

**Derivation.** When n ≤ ~20 (§3) the constraint is announcing that the solution space itself — all subsets, permutations, placements — is the object. What's needed isn't cleverness but a **decision tree walked without duplication or omission.** Every backtracking problem is these four questions:
1. **What is a partial solution?** (the `path`)
2. **What are the choices at this node?** — this single answer differentiates the whole family:
   - Subsets/combinations: elements from `start` onward (forward-only ⇒ no permuted duplicates)
   - Permutations: any unused element (`used` set)
   - Grid problems: the ≤4 neighbors
   - K-buckets partition: which bucket gets item i
3. **When do I record?** (at leaves / at every node / on constraint satisfaction)
4. **What do I prune?** — see below.

The skeleton is always `choose → recurse → un-choose`; the un-choose restores shared state exactly, which is why the same list can travel the whole tree.

**Pruning is the real skill** (the difference between "backtracking" and "timeout"):
- **Feasibility:** stop the moment the partial can't extend (remaining sum < needed; word prefix not in trie).
- **Duplicate values:** sort, then at each depth skip a value equal to the previous *sibling* — the first occurrence explores everything the second would (Subsets II, the k-buckets `tried` set: two buckets with equal sums have identical futures).
- **Ordering:** try large/most-constrained items first so contradictions surface near the root, where cutting a branch saves the most.

**Triggers:** "all possible …" · n ≤ 20 · placements under constraints (N-Queens, Sudoku) · "can it be partitioned/formed" where DP state would be exponential anyway.
**Breaks when:** only a *count* or *optimum* is asked and n is large → the tree has repeating subtrees → memoize → you've walked into DP (that boundary is the next chapter).
**Escalation:** Subsets → Subsets II (dup skip) → Combination Sum I/II → Permutations → Word Search → Word Search II (trie) → Partition to K Equal Sum Subsets.

---

## Recursion → DP — same tree, cached; the skill is state design

**Core question:** the brute-force recursion revisits identical subproblems — cache them.

> Full lesson-format treatment of this chapter — recursion from zero, top-down, bottom-up, state design, worked tables: [RECURSION_AND_DP_MASTERCLASS.md](RECURSION_AND_DP_MASTERCLASS.md).

**The derivation path — always the same three steps, never skip to step 3:**
1. **Write the brute-force recursion** by articulating *the last (or first) decision*: "the answer for the first i items either uses item i or doesn't" · "this path came from the cell above or the left" · "either these two characters match, or one gets deleted." Getting this sentence right is 80% of the problem.
2. **Look at the arguments.** The argument tuple *is* the state. If wildly many calls share the same arguments (Fibonacci-style blowup), memoize: `@lru_cache` or a dict. Done — this already passes.
3. **Optionally invert to a table** (bottom-up) by computing states in dependency order; collapse to O(1) space if only the previous row/two values are read. Mention it; do it if asked.

**State design — the actual hard skill.** The state must be the *minimal information that makes the future independent of the past* (the Markov property, informally). Diagnostic: if your recursion gives wrong answers because "it matters how we got here," **the missing 'how' is a missing state dimension.** Standard inventory:

| Situation | State |
|---|---|
| Linear sequence, take/skip | `i` (House Robber: `dp[i] = max(dp[i-1], dp[i-2]+a[i])`) |
| Two sequences aligned | `(i, j)` (LCS, Edit Distance — the 2D grid *is* all alignment prefixes) |
| Capacity/budget being spent | `(i, remaining)` (knapsack, Coin Change, Target Sum) |
| A mode you can be in | `(i, holding?)`, `(i, k transactions left)` (stock problems) |
| Range/interval decisions | `(l, r)` (palindromes, burst balloons) |
| Position in a DAG | the node (Longest Increasing Path — graph crossover) |

**Reading the recurrence type from the question:** "how many ways" → sum over choices · "min/max" → min/max over choices · "is it possible" → OR over choices. Same skeleton, different combiner — recognizing this collapses dozens of "different" problems into three.

**The classic traps:** Coin Change *ways*: loop coins outer, amount inner (combinations) vs the reverse (permutations — Climbing Stairs is exactly permutation-counting); be ready to say which and why · 0/1 knapsack in 1D: iterate capacity **backward** so this item isn't reused (forward = unbounded — the direction *is* the take-once constraint) · always define `dp[0..k]` semantics in one spoken sentence *before* writing transitions; interviewers grade that sentence.

**Triggers:** "how many ways / min cost / longest / can you" over sequential or paired structure · choices now affecting options later · n ≤ 5000-ish with a 2D flavor · a backtracking problem that only asks for a count/optimum.
**Breaks when:** state must include a full subset of arbitrary items (which cities visited) → bitmask DP, out of scope: name it · greedy has a valid exchange argument → DP is overkill (next chapter).
**Escalation:** Climbing Stairs → House Robber → circular (run twice, exclude one end) → Coin Change → LCS → Edit Distance → Maximum Profit Job Scheduling (DP + binary search — composition, §Part III).

---

## Greedy — the only pattern that requires a proof

**Core question:** can locally-best commitments reach the global optimum — and can I *argue* it?

**The honest framing:** greedy isn't a technique so much as a *claim*, and the claim is often false. What distinguishes valid greedy is a working **exchange argument**: *take any optimal solution that disagrees with greedy's first choice; swap that choice in; show the solution got no worse.* Then greedy's first move is safe, and by induction all of them. The 30-second version of this argument, spoken aloud, is what the interviewer is buying.

**The families whose proofs you should be able to sketch cold:**
- **Interval scheduling — sort by earliest END.** Exchange: any optimal set's first meeting can be swapped for the earliest-ending one; it frees no less room after it. (Sort by start or by shortest — both have 10-second counterexamples; produce them.) → Non-overlapping Intervals is the same with complements.
- **Reach/jump (Jump Game):** maintain `furthest`; a single pass, because any square ≤ furthest is reachable and extends via its own jump — invariant maintenance, nothing subtle.
- **Pair extremes (Boats to Save People):** heaviest + lightest together if possible; exchange: whatever partner the heaviest had, the lightest fits at least as well.
- **Fuel-circuit (Gas Station):** if you die at station j starting from i, every start in (i..j] also dies (they arrive with ≤ your fuel) → restart from j+1; O(n) with a *discard proof* — greedy and two-pointers share DNA.
- **Combine cheapest two** (Huffman-shaped, heap-assisted): connecting ropes, etc.

**The decision procedure when you suspect greedy:** try to sketch the exchange in 30 seconds. Can't? **Assume DP** and look for the recurrence — the expected-value play at interview stakes. Fastest disproof: hunt a small counterexample (coins {1, 3, 4}, amount 6: greedy 4+1+1=3 coins, optimal 3+3=2 — canonical US-coins-vs-arbitrary-coins lesson). Structural tell: if a local choice *changes what future choices cost* in a way sorting can't neutralize, greedy is likely wrong.

**Triggers:** "minimum number of intervals/jumps/boats/…" with a sort that makes commitments obviously safe · problems where after sorting, one pass with a running invariant suffices.
**Breaks when:** the counterexample exists (usually found in 60 seconds of trying) → DP.
**Escalation:** interviewers escalate by *breaking* the greedy — adding a constraint (k stops on Cheapest Flights breaks Dijkstra's greedy) and watching whether you notice the proof no longer holds. Noticing out loud is the senior signal.

---

## Intervals & Sweep Line — sort, then one pass with the right invariant

**Core question:** overlapping ranges — merge them, count them, schedule them, find gaps.

**The three facts that generate every interval solution:**
1. **The overlap test:** `A` and `B` overlap ⟺ `startA < endB and startB < endA`. Memorize this one (derive it as "NOT (A entirely before B OR B entirely before A)"). It is My Calendar I in its entirety.
2. **Sort direction encodes intent:** merging/combining → sort by **start** (a new interval either extends the current merged block or starts a fresh one — one running block is the whole state). Selecting max non-overlapping → sort by **end** (greedy chapter). If a one-pass interval solution feels impossible, you usually sorted by the wrong endpoint.
3. **Counting concurrency = event sweep:** shatter intervals into `(start, +1)` and `(end, −1)` events, sort, running sum = live count; the max is Meeting Rooms II. When coordinates are small integers, the same thing as an array = **difference array** (Car Pooling — §Prefix Sums; these chapters are one idea in two coats).

**Online versions** (intervals arrive one at a time — the L4 form): keep a sorted list of bookings; on each insert, locate the neighbors by bisect and run fact 1 against them (My Calendar I). Double bookings allowed but not triple → maintain a second list holding just *the pairwise overlaps*; a new booking conflicting with any overlap = triple (My Calendar II). k-bookings → back to the event sweep with a map.

**Triggers:** the word "intervals/meetings/bookings" · "merge / insert / min rooms / max attend / free time" · timestamped ranges of any kind.
**Escalation:** Merge Intervals → Insert (no sort needed — exploit given order, three phases) → Meeting Rooms II → My Calendar I → II → Employee Free Time (k sorted lists — heap crossover).

---

## Design-a-Data-Structure — compose, so each part covers the other's weakness

**Core question:** support *this* set of operations, each within *this* complexity budget.

**The method (it is completely systematic):**
1. Write the ops and budgets as a table before any structure-talk.
2. For each single structure, mark which ops it wins and which it fails.
3. **Compose:** pick two whose strengths cover each other's failures; the composite's real cost is keeping them *consistent* — every mutation updates both.

Worked cold: Insert/Delete/GetRandom O(1). Random needs index-access → array. Delete-by-value needs find → hash `val → idx`. Array's weakness: deleting mid-array is O(n) — but order was never required, so **swap the victim with the last element, pop the end** — O(1). The swap trick is the whole problem; and the canonical bug is update-order (repoint the moved element's hash entry *before* deleting the victim's, or deleting the last element corrupts the map).

**The standard composition table** (derive each row by the 3-step method; walkthroughs in [`coding/data-structures/14-design.md`](../coding/data-structures/14-design.md)):

| Need | Composition |
|---|---|
| O(1) lookup + O(1) recency ordering | hash map + doubly linked list (LRU) |
| …by frequency | + `freq → DLL` buckets + `min_freq` (LFU) |
| O(1) insert/delete + O(1) random | array + hash of positions (swap trick) |
| Extremes of a stream **with corrections** | hash (truth) + heaps (candidates) + lazy deletion |
| Point-in-time reads (snapshots) | per-key version list `[(version, val)]` + bisect |
| Weighted random | prefix sums + bisect |
| Sliding rate-limits | deque of timestamps, evict expired on each call |

**Why Google L4 leans on these:** they're miniature systems problems — invariants between components, consistency on mutation, per-op complexity accounting — the interview-sized version of real engineering. Narrate the consistency discipline ("every write touches both structures; here's the order and why") — that narration *is* the evaluation.

**Triggers:** "Design/implement a class with operations …" · any "O(1) per operation" demand · "with getRandom / snapshots / at-timestamp".
**Escalation is built-in:** base class → one op's constraint tightens ("now getRandom must be uniform over duplicates") → thread safety (talk locks; don't code them).

---

# PART III — COMPOSITION, ESCALATION, AND THE TRAINING PROTOCOL

## Hard problems are two patterns with a seam

Genuinely hard interview problems are rarely a *new* idea — they're two chapters of this file composed, and the skill is finding the **seam**: split the problem into an *outer* question and an *inner* question, and pattern-match each separately.

| Problem | Outer | Inner |
|---|---|---|
| Maximum Profit in Job Scheduling | DP over jobs sorted by end | binary search for the last compatible job |
| Word Search II | grid backtracking | trie carrying all words at once |
| Word Ladder II | BFS for level structure | backtracking over recorded parents |
| Count subarrays, sum k, negatives | prefix sums | hash-count of earlier prefixes |
| Sliding Window Median | sliding window | two heaps + lazy deletion |
| Employee Free Time | interval merging | k-way heap merge |
| LFU Cache | hash map | frequency-bucketed ordered dicts |
| Minimum Days to X | binary search on answer | greedy/BFS feasibility check |

When stuck on a hard problem, explicitly ask: *"is there an inner subproblem here I already know?"* — usually the inner one is a T1 pattern, and identifying it cracks the outer shell.

## The escalation grammar (what follow-ups will be)

Every follow-up an interviewer asks is one of five transformations. Pre-compute your answers for each T1 problem you know — this table is the L4 bar in one place:

| Transformation | What it does to your solution | Standard response |
|---|---|---|
| **"It's a stream now"** | no random access, no second pass | wrap state in a class; incremental maintenance (your window stats / heap / map already are this) |
| **"It doesn't fit in memory"** | no global structure | shard/partition + merge partials (per-shard top-k); external sort; talk, don't code |
| **"Now there are updates"** | precomputed answers go stale | versioning (Snapshot Array), lazy deletion, or "this is where a segment tree would enter — out of my 45 minutes, here's the shape" |
| **"Return all of them, not the count"** | need reconstruction | store parents/choices during the forward pass; backtrack after (Word Ladder II, DP path recovery) |
| **"k of them / at most k"** | one more dimension | add k to the DP state; k-th via heap; k-rounds Bellman-Ford |

## The training protocol (how to study this file)

Knowing the derivations and *producing them under pressure* are different skills; the second is trained, not read.

1. **Derivation reps.** For one pattern per day: blank paper, write the core question, reconstruct the derivation and invariant from memory, then check against this file. 15 minutes. When you can do all ~16 chapters cold, the "which pattern is this?" anxiety disappears — you're recognizing *waste types*, not problem titles.
2. **Solve with the loop, visibly.** Every practice problem, run §2's ten steps *out loud* — especially 4 (brute force), 5 (name the waste), and 7 (state the invariant). Solving silently trains the wrong skill; the interview is a spoken exam.
3. **Log misses by cause, not by problem.** After a failed attempt, record *which step failed*: didn't decode constraints? wrong waste named? invariant never stated? state dimension missing? Your miss-log will cluster hard around 2–3 causes within twenty problems — those are what you drill, via the matching rungs in [PATTERN_LADDERS.md](PATTERN_LADDERS.md).
4. **Escalate every solve.** After each clean solve, ask yourself the five grammar transformations and answer aloud in one minute each. This is 80% of the L3→L4 delta at ~zero extra cost.
5. **The 20-minute rule.** Stuck past 20 minutes → read *only* the key insight, not the code — then implement from the insight alone. You keep the derivation practice, lose only the trivia.

## The interview-day card

The compressed version of this entire file — the nine sentences to hold in working memory:

1. Constraints first: **n tells you the complexity, complexity tells you the pattern family.**
2. Always state the brute force; then **name its waste** — the waste names the pattern.
3. Contiguous + monotone validity → window. Negatives kill windows → prefix + hash.
4. Sorted (or sortable) → two pointers / binary search. **"Minimize the max" → binary search the answer.**
5. Nearest greater/smaller, or per-element contribution → monotonic stack.
6. k / top / stream extremes → heap. Middles need two heaps; deletions are lazy.
7. States + moves → it's a graph; **pick nodes so edges = the counted quantity.** Weighted → Dijkstra, cold.
8. Choices now affecting later → recursion; repeated argument-tuples → memo → DP. **The state = minimal info making the future independent of the past.**
9. Greedy only with an exchange argument you can *say*. Can't say it → DP.

---

## See Also

- [INTERVIEW_JUDGMENT.md](INTERVIEW_JUDGMENT.md) — counterexample hunting, invariant proofs, commit-vs-pivot, hint decoding, recovery playbooks
- [PATTERN_LADDERS.md](PATTERN_LADDERS.md) — graded problem sequences to pressure-test each chapter
- [patterns-master.md](patterns-master.md) — trigger-phrase quick reference
- [MOCK_INTERVIEW_SET.md](MOCK_INTERVIEW_SET.md) — 25-problem cold set + L4 follow-up chains
- [`coding/l4-sde2-delta.md`](../coding/l4-sde2-delta.md) — the L4 bar, tier promotions, gap problems
- [`00-L3-EXECUTION-META/01-45-minute-execution-plan.md`](../00-L3-EXECUTION-META/01-45-minute-execution-plan.md) — minute-by-minute round plan
