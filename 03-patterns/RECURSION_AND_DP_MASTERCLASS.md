---
module: 03-patterns
topic: Recursion & DP Masterclass — from first call to bottom-up tables
tags: [recursion, dp, memoization, top-down, bottom-up, teaching, google-l3, l4]
---

# Recursion & DP Masterclass — Taught From Zero

> [!IMPORTANT]
> **How to read this file.** This is a lesson, not a reference. Read it in order — each section builds on the previous one, and the examples are the curriculum. Work every "✍️ Do this now" exercise on paper before reading past it; the file is designed so that skipping them makes later sections feel like magic, and doing them makes later sections feel obvious.
>
> The arc: **what a recursive call really is → how to design one → why recursion explodes → memoization (top-down DP) → converting to bottom-up tables → state design → when to use which.** By the end, "DP problem" should stop being a category of fear and become a two-step procedure you run.

---

# LESSON 1 — What a recursive call actually is

## 1.1 The machine model (30 seconds of truth)

When `f(5)` calls `f(4)`, the computer:
1. **Freezes** `f(5)` exactly where it is — its local variables, its position in the code — and pushes that frozen frame onto the **call stack**.
2. Runs `f(4)` from the top, as a completely fresh, independent execution.
3. When `f(4)` returns a value, **unfreezes** `f(5)` at the exact line it stopped, with the returned value plugged in.

That's all recursion is: a stack of frozen frames. Two consequences you must internalize:

- **Each call has its own locals.** The `i` inside `f(4)` is a different variable from the `i` inside `f(5)`. Recursion is not a loop revisiting the same variables; it's n copies of the function, each with private state.
- **Code after the recursive call runs later, on the way back up.** This is why recursion has a "going down" phase (arguments shrink toward the base case) and a "coming back up" phase (return values combine). Most designs put the work in exactly one of the two — knowing which phase you're working in is half of tree-problem design.

## 1.2 The leap of faith — the single most important idea in this file

Beginners try to **trace** recursion: "f(5) calls f(4) which calls f(3) which…". This fails past depth 3 for everyone, at any skill level. The trace is not how recursion is designed. It's designed by **contract**:

> **Write one sentence stating what `f(args)` returns. Then, while writing the body, assume the recursive calls already satisfy that sentence perfectly — as if a brilliant colleague implemented them.**

This is mathematical induction wearing programming clothes: prove the base case, prove that step k works *if* step k−1 works, done. You never verify the whole chain by hand; the structure guarantees it.

**Worked example — the contract method on `reverse a linked list`:**

Contract: *"`reverse(head)` returns the head of the reversed version of the list starting at `head`."*

Body, written with pure faith:
```python
def reverse(head):
    if not head or not head.next:      # base: empty or single node is its own reverse
        return head
    new_head = reverse(head.next)      # FAITH: rest of list is now perfectly reversed
    head.next.next = head              # my old next is the reversed part's TAIL; attach me after it
    head.next = None                   # I'm the new tail
    return new_head
```
Notice what we never did: imagine the pointers of a 5-node list mid-recursion. We answered three local questions — base case, what the sub-call gives me (by contract), how to add my one node to it — and the induction did the rest.

**✍️ Do this now:** using only the contract method, write `sum_list(head)` (sum of a linked list) and `count_down(n)` (print n…1). One sentence contract first, then base, then faith-based body. If you caught yourself mentally simulating three levels deep — stop, go back to the contract.

## 1.3 The three questions that design any recursion

Every recursive function you will ever write in an interview is designed by answering, in order:

1. **Contract** — what does `f(args)` return? (One sentence. Written down or spoken. Non-negotiable.)
2. **Base case** — for which smallest inputs can I return the answer *without* recursing? (Empty list, `n == 0`, null node, empty string. Ask: "what's the identity value?" — 0 for sums, 1 for products, `True` for AND-chains, `-inf` for maxes.)
3. **One step** — assuming sub-calls honor the contract, how do I combine their answers (plus my own element) into mine?

When a recursion is buggy, the bug is almost always a *mismatch* between the contract you stated and what the body actually returns — e.g., contract says "height of subtree" but a branch returns a node. Restate the contract and audit each `return` against it.

## 1.4 The shape of the call tree = the complexity

A recursion's cost is the **number of nodes in its call tree × work per call**.

- One recursive call per invocation (`f(n) → f(n-1)`): a chain, depth n → **O(n)** calls. (Factorial, linked-list walks.)
- Two calls per invocation (`f(n) → f(n-1), f(n-2)`): a binary tree of depth n → **O(2ⁿ)** calls. (Naive Fibonacci, naive subset-sum.)
- Two calls but on *halves* (`f(n) → f(n/2), f(n/2)`): depth log n, still n leaves → **O(n log n)** total for merge-sort-shaped work.

Rule of thumb to say out loud: **branching factor ^ depth**. This is why Lesson 3's discovery matters so much: an exponential call tree is only a disaster if the nodes are all *different*…

---

# LESSON 2 — The five shapes of recursive problems

Nearly every interview recursion is one of five shapes. Knowing the shape tells you the contract format before you've thought about the problem at all.

| Shape | Contract template | Examples |
|---|---|---|
| **1. Linear** — decide about element i, recurse on the rest | `f(i)` = answer for suffix/prefix starting at i | House Robber, Climbing Stairs, word break |
| **2. Two-sequence** — walk two strings/arrays together | `f(i, j)` = answer for `a[i:]` vs `b[j:]` | LCS, Edit Distance, regex matching |
| **3. Structural** — the data itself is recursive | `f(node)` = answer for the subtree at node | height, path sums, validate BST |
| **4. Divide & conquer** — split, solve halves, merge | `f(lo, hi)` = answer for range | merge sort, quickselect, build-BST-from-sorted |
| **5. Enumerative** — build all candidates choice by choice | `f(path, options)`: extends path every way | subsets, permutations, N-Queens (= backtracking) |

Shapes 1 and 2 are the ones that become DP (Lesson 3 explains exactly why). Shape 3 occasionally does (tree DP). Shapes 4 and 5 usually don't — their sub-calls rarely repeat.

**The decision sentence.** For shapes 1 and 2, the entire intellectual work is articulating **the first (or last) decision**:

- Climbing Stairs: *"The first move is either 1 step or 2 steps."* → `f(n) = f(n-1) + f(n-2)`
- House Robber: *"I either rob house i (and skip i+1) or I don't."* → `f(i) = max(nums[i] + f(i+2), f(i+1))`
- Coin Change: *"The last coin used is one of the denominations."* → `f(amt) = 1 + min(f(amt - c) for c in coins)`
- Edit Distance: *"Look at the last characters: they match (free), or I insert, delete, or replace."*
- LCS: *"If a[i] == b[j], both advance and score 1; otherwise the answer skips one of the two."*

Say the decision sentence before writing any code. If you can't state it, you don't have a recursion yet — you have a wish. Practice converting problem statements into decision sentences as its own drill; it's the highest-leverage 10 minutes/day in all of DP prep.

**✍️ Do this now:** write decision sentences (just the sentence, no code) for: (a) minimum path sum in a grid moving only right/down; (b) number of ways to decode a digit string where '1'–'26' are letters; (c) can `nums` be partitioned into two equal-sum halves? Check yourself: (a) "the last step into cell (i,j) came from above or from the left"; (b) "the first letter is one digit, or two digits if they form 10–26"; (c) "element i is in the left pile or the right pile."

---

# LESSON 3 — The disease: overlapping subproblems

Now the pivot from recursion to DP. Watch it happen concretely.

## 3.1 Autopsy of naive Fibonacci

```
                        f(5)
                 ┌───────┴───────┐
               f(4)             f(3)
            ┌───┴───┐         ┌──┴──┐
          f(3)    f(2)      f(2)   f(1)
         ┌──┴──┐  ┌─┴─┐    ┌─┴─┐
       f(2) f(1) f(1) f(0) f(1) f(0)
      ┌─┴─┐
    f(1) f(0)
```

Count the labels: `f(3)` computed **2** times, `f(2)` **3** times, `f(1)` **5** times. For `f(50)`, `f(2)` is computed ~5 billion times — and *every single one returns the same answer*, because the function's output depends only on its argument.

There's the disease and the cure in one sentence: **the call tree has 2ⁿ nodes but only n distinct labels.** We're not doing exponential *work*, we're doing linear work exponentially many times.

## 3.2 The cure: memoization

If the function is **pure** — return value depends only on the arguments, no side effects, no reading mutating globals — then the second call with the same arguments is guaranteed to return the same thing. So: cache it.

```python
def fib(n, memo={}):                    # or @functools.lru_cache(None)
    if n <= 1: return n
    if n not in memo:
        memo[n] = fib(n-1) + fib(n-2)
    return memo[n]
```

What just happened to the call tree: every *repeated* label becomes a cache hit — an O(1) leaf. The tree collapses to **one real computation per distinct label**. New complexity law, the only DP complexity formula you'll ever need:

> **Time = (number of distinct states) × (work per state, excluding recursion)**
> Fibonacci: n states × O(1) each = **O(n)**. LCS: n·m states × O(1) = **O(nm)**. Coin change: amount states × O(#coins) = **O(amount · coins)**.

## 3.3 What "DP problem" actually means

You now have the honest definition. A problem is a DP problem when its natural recursion has:
1. **Overlapping subproblems** — the call tree repeats labels (otherwise memoization buys nothing; merge sort has no repeats and isn't DP), and
2. **Optimal substructure** — the contract can be honored using only the sub-contracts' answers (the optimal solution to the whole is assembled from optimal solutions to parts).

And "solving a DP problem" means exactly: **write the shape-1/2/3 recursion via a decision sentence, then cache it.** That's the whole secret. Top-down DP is not a separate technique from recursion — it is recursion plus a dictionary.

---

# LESSON 4 — Top-down DP (memoization), the production method

This is the method to run in an interview, every time, in this order. We'll run it on a real problem end-to-end.

> **The 5-step method**
> 1. Say the **decision sentence** (first/last choice).
> 2. Write the **contract**: `f(state) = …` — one sentence, precise.
> 3. Write the **brute recursion**: base case + decision-driven recursive cases. Ignore efficiency completely.
> 4. **Memoize**: `@lru_cache(None)` on top (or a dict keyed by the argument tuple). Arguments must be hashable — indices and numbers, never lists; pass indices *into* shared data instead of slicing.
> 5. State **complexity** via states × work-per-state.

## 4.1 Full worked example — Coin Change (min coins for `amount`)

**Step 1, decision sentence:** "The last coin in the optimal pile is one of the denominations — I don't know which, so try all."

**Step 2, contract:** `f(a)` = minimum coins to make amount `a` exactly (∞ if impossible).

**Step 3, brute recursion:**
```python
def f(a):
    if a == 0: return 0            # identity: zero coins make zero
    if a < 0:  return float('inf') # overshot: poison this branch
    return 1 + min(f(a - c) for c in coins)
```
Read it as prose: *the best way to make `a` = pick some last coin `c`, pay 1 for it, plus the best way to make what's left.* The `inf` is a beautiful trick worth naming: impossible branches return a value that **loses every `min`** automatically — no special-casing. (For `max` problems use `-inf`; for counting, return 0; for feasibility, return `False`.)

**Step 4, memoize:**
```python
from functools import lru_cache
@lru_cache(None)
def f(a): ...                      # body unchanged
ans = f(amount)
return ans if ans != float('inf') else -1
```

**Step 5, complexity:** states = amounts `0..amount`; work per state = one loop over coins → **O(amount × len(coins)) time, O(amount) space** for the cache (+ recursion stack).

Total elapsed thinking: five sentences. This *is* the interview performance — the five steps, narrated, are exactly what the interviewer wants to hear.

## 4.2 Second worked example — Longest Common Subsequence (shape 2)

**Decision sentence:** "Compare `a[i]` and `b[j]`: if equal, they pair up and both advance; if not, the LCS skips `a[i]` or skips `b[j]` — try both."

**Contract:** `f(i, j)` = length of the LCS of `a[i:]` and `b[j:]`.

```python
@lru_cache(None)
def f(i, j):
    if i == len(a) or j == len(b): return 0        # an empty string shares nothing
    if a[i] == b[j]:  return 1 + f(i+1, j+1)
    return max(f(i+1, j), f(i, j+1))
```

Complexity: n·m states × O(1) = **O(nm)**. Notice how *little* changed from the method: two indices instead of one, because two sequences are being walked. That's the entire difference between "1D DP" and "2D DP" — it was never a different technique, just a different argument count.

**✍️ Do this now:** run the 5-step method, on paper, for **Decode Ways** (digit string, '1'–'26' are letters, count decodings). Don't look anything up. Check: contract `f(i)` = ways to decode `s[i:]`; bases `f(len(s)) = 1` (empty suffix = one way: stop) and `s[i] == '0' → 0`; body `f(i+1) + (f(i+2) if 10 <= int(s[i:i+2]) <= 26 else 0)`; complexity O(n). If you got the base case `f(n)=1` wrong — most people do — sit with *why*: it's the count of ways to decode nothing, and there is exactly one way to do nothing. Identity values again.

## 4.3 Top-down mechanics: the gotcha list

- **Cache key = complete argument tuple.** If your recursion secretly depends on something not in the arguments (a global you mutate, a `path` list), the cache returns wrong answers. That's not a memoization bug — it's the signal your **state is incomplete** (Lesson 6).
- **Never pass slices** (`f(s[1:])`) — O(n) copy per call *and* unhashable-adjacent mess. Pass indices into the one shared string.
- **Python recursion limit** (~1000): for n up to 10⁵ linear-state problems, top-down will crash. Options: `sys.setrecursionlimit(1_000_100)` (say it, slightly ugly), or convert to bottom-up (Lesson 5 — the clean answer, and a great reason to volunteer the conversion).
- `lru_cache(None)` means unbounded; that's what you want here.

---

# LESSON 5 — Bottom-up DP (tabulation): the same tree, walked in reverse

## 5.1 What bottom-up actually is

Top-down starts at the *question* (`f(amount)`) and lazily discovers which subproblems it needs. Bottom-up observes: "I can list every state in advance and I know which states each depends on — so skip the call stack entirely, compute them **in dependency order**, smallest first, into a table."

Same states. Same recurrence. Same complexity. The only things that change: recursion → loop, cache → array, and *you* now own the responsibility of ordering (the call stack used to handle it silently). That ordering responsibility is the only new skill in this lesson.

## 5.2 The mechanical translation (memorize this procedure, it never varies)

Given a working memoized solution:

1. **`dp` array indexed by the state**: `f(i)` → `dp[i]`; `f(i, j)` → `dp[i][j]`. Size = state-space size (usually n+1 — the +1 holds the base case).
2. **Base cases first**, into the table: whatever the recursion's `if` guards returned.
3. **Loop over states in dependency order** — each state computed *after* everything it reads. If `f(i)` calls `f(i+1)` (suffix-style contract), fill i from **high to low**; if `dp[i]` reads `dp[i-1]` (prefix-style), fill **low to high**. Derive the direction every time from "what does this cell read?" — never from memory.
4. **Recurrence body copied verbatim**, calls → table reads.
5. **Answer** = the cell the original question asked for (`dp[amount]`, `dp[0][0]` for suffix-style 2D).

## 5.3 Watch the translation — Coin Change again

Top-down from Lesson 4 → bottom-up:

```python
dp = [float('inf')] * (amount + 1)
dp[0] = 0                                  # base case, verbatim
for a in range(1, amount + 1):             # f(a) reads f(a-c), i.e. smaller a → ascend
    for c in coins:
        if c <= a:
            dp[a] = min(dp[a], 1 + dp[a - c])
return dp[amount] if dp[amount] != float('inf') else -1
```

Line-by-line, this is the recursion with the plumbing swapped. Nothing new was invented. **This is the answer to "how do people come up with these tables?" — they don't. They come up with recursions, and translate.**

And now the payoff for having a table — **let's actually fill one**, coins = [1,2,5], amount = 7:

```
a:      0   1   2   3   4   5   6   7
dp[a]:  0   1   1   2   2   1   2   2
                                    ↑
        e.g. dp[7] = 1 + min(dp[6], dp[5], dp[2]) = 1 + min(2, 1, 1) = 2   (5+2 ✓)
```

**✍️ Do this now:** fill the same table for coins = [2, 5], amount = 7 by hand. (You should get `dp = [0, ∞, 1, ∞, 2, 1, 3, 2]` — the ∞s surviving at odd-impossible amounts are the `inf`-poison trick visible in table form.)

## 5.4 The 2D case — LCS as a table, filled before your eyes

Contract was suffix-style `f(i, j)` reading `f(i+1, ·)` — so fill i descending. `a = "abcde"`, `b = "ace"`:

```
            j=0(a) 1(c)  2(e)  3(end)
 i=5(end)     0     0     0     0
 i=4(e)       1     1     1     0     ← 'e'=='e' → 1 + dp[5][3]
 i=3(d)       1     1     1     0
 i=2(c)       2     2     1     0     ← 'c'=='c' → 1 + dp[3][2]
 i=1(b)       2     2     1     0
 i=0(a)       3     2     1     0     ← 'a'=='a' → 1 + dp[1][1]   answer: dp[0][0] = 3
```

Filling three cells of such a table *by hand, slowly* teaches more than reading ten solutions. Every "hard" 2D DP (Edit Distance, Interleaving Strings, regex) is this same grid with a different one-line cell rule.

## 5.5 Space optimization — the standard follow-up

Look at the LCS fill: row `i` reads **only row `i+1`**. So keep two rows, not the grid: **O(nm) time, O(m) space**. Linear DPs that read only `dp[i-1], dp[i-2]` collapse to two variables (Fibonacci/Climbing Stairs/House Robber in O(1) space). This is the single most common DP follow-up at Google; pre-decide your answer: *"each row depends only on the previous → two rows"* and know the rolling-variable version of the linear ones cold.

**The 1D-knapsack direction trap** — the one place space optimization can silently change semantics. 0/1 knapsack (each item once) collapsed to one row must iterate capacity **backward**: going forward, `dp[c - w]` has already been updated *this round*, meaning the current item gets reused — which is exactly **unbounded** knapsack (Coin Change). The loop direction *is* the use-once constraint. Interviewers probe this deliberately; being able to explain *why* backward (you must read last round's value, which forward iteration has already destroyed) is a strong-hire moment.

Relatedly, for **counting** DPs, loop nesting order changes the meaning: coins outer / amounts inner counts **combinations** (each coin's uses are committed in a block, orderings not distinguished); amounts outer / coins inner counts **permutations** (every position freshly chooses any coin — Climbing Stairs is exactly this). Don't memorize which is which; reconstruct it from "when is the decision about coin c finalized?"

---

# LESSON 6 — State design: the actual hard part

Everything so far was mechanical. Here is the one genuinely creative act in DP, so it gets its own lesson.

## 6.1 The principle

> **The state is the minimal information about the past that makes the future solvable.**

Test your candidate state with this question: *"If two different histories arrive at the same state, is their best future identical?"* If yes, the state is sufficient — histories can share a cache entry. If no — if it "matters how you got here" — **the thing that matters is a missing state dimension.** That diagnostic converts vague stuck-ness into a concrete search: *what about the past leaks into the future?*

## 6.2 Watch a state get discovered — Best Time to Buy/Sell Stock with Cooldown

Attempt 1: `f(i)` = best profit from day i on. Write the body… and immediately hit a wall: "can I buy today?" depends on whether I'm *holding* a stock and whether I *sold yesterday* — the past is leaking. Name the leaks, promote them to dimensions:

`f(i, holding)` where after a sell we skip a day: on day i, holding → sell (`prices[i] + f(i+2, False)`) or wait; not holding → buy (`-prices[i] + f(i+1, True)`) or wait. States: n × 2. Done. **The wall wasn't failure — it was the state-design procedure working.** You *want* to hit that wall fast; it tells you the missing dimension by name.

## 6.3 The standard state inventory

Learn these as *derivations* (each one is the answer to "what leaks?"), not as a list:

| Problem flavor | What leaks from the past | State |
|---|---|---|
| take/skip along a line (House Robber) | whether the neighbor was taken — but that's captured by *position* if contract = "best from i onward" | `i` |
| two sequences (LCS, Edit Distance) | progress in each | `(i, j)` |
| budget being spent (knapsack, Target Sum) | money/capacity left | `(i, remaining)` |
| buy/sell with constraints | in-position or not; trades left | `(i, holding)`, `(i, k)` |
| range problems (palindromes, Burst Balloons) | which contiguous chunk remains | `(l, r)` |
| grid paths | current cell | `(r, c)` |
| tree problems | current node (+ "am I allowed to use it") | `node`, `(node, took_parent)` |

Burst Balloons deserves one sentence, because its state is famously non-obvious: bursting a balloon changes the *neighbors* of everything — history leaks everywhere — until you flip the decision to "which balloon pops **last** in the range (l, r)?" — the last balloon's neighbors are the range's fixed boundaries, and the leak vanishes. When forward decisions leak, **try deciding the last action instead of the first.** That flip is a general tool.

## 6.4 Reading the combiner off the question

Same skeleton, three combiners — classify before writing:

- "**how many ways**" → `dp = Σ` over choices (base = 1: one way to do nothing)
- "**min/max cost/length**" → `dp = min/max` over choices (base = 0 or ±inf-poison)
- "**is it possible**" → `dp = OR` over choices (base = True)

Target Sum, Partition Equal Subset, Coin Change I & II are one recursion with different combiners. Seeing this collapses ~40% of "different" DP problems into things you've already solved.

---

# LESSON 7 — Top-down vs bottom-up: an actual decision procedure

Both compute the identical answer at identical asymptotic cost. Choose deliberately:

| | Top-down (memo) | Bottom-up (table) |
|---|---|---|
| Design effort | lower — it *is* the recursion | needs dependency-order thinking |
| Under interview pressure | **default choice** — fewer off-by-one traps | shine-move when volunteered |
| Computes | only states the answer needs (sparse state spaces win big) | every state, even useless ones |
| Recursion-limit risk (Python) | yes, at n ≳ 10³ linear depth | none |
| Space optimization (rows → variables) | not really possible | natural — the standard follow-up |
| Constant factors | function-call overhead | tight loops, faster in practice |

**The interview playbook, spelled out:** derive top-down first, always — narrate the 5-step method; it shows your reasoning, and it's hard to get structurally wrong. Then say: *"I can convert this to bottom-up to remove the recursion limit and optimize space to O(m) — want me to?"* That sentence costs nothing, signals you own both forms and the translation between them, and lets the interviewer choose how to spend the remaining time. Only *start* in bottom-up when the problem is a known-linear classic (Climbing Stairs tier) or n makes recursion depth an immediate problem.

---

# LESSON 8 — The bug catalog (read before every mock)

1. **Base case off by one.** `dp` sized n+1 exists to hold the empty-prefix/suffix base. If your answer is wrong on tiny inputs, audit bases first — and audit them against *identity* semantics ("ways to make 0 = 1", not 0).
2. **Contract drift.** `f(i)` meaning "prefix ending at i" in one branch and "suffix from i" in another. Symptom: indices like `i+1` and `i-1` in the same body. Cure: re-say the contract, fix every return against it.
3. **Missing state dimension.** Wrong answers only on inputs where history matters. Run the §6.1 diagnostic; add the leaking fact.
4. **Wrong fill order.** Bottom-up reading cells not yet written (often 0s — silently wrong, not crashed). Cure: point at the recurrence, ask "does this cell read larger or smaller indices?", set loop direction from that, every time.
5. **1D-knapsack forward/backward** (§5.5). Backward = use-once, forward = unbounded. Know why, not just which.
6. **Mutable/incomplete cache keys.** Passing lists or depending on mutated globals. Arguments must be the whole state, and hashable.
7. **`max()` on empty choices / missing poison values.** Impossible branches must return the combiner's identity-loser (∞ for min, −∞ for max, 0 for count, False for OR) so they lose silently.
8. **Answer read from the wrong cell.** Suffix contracts answer at `dp[0]`, prefix contracts at `dp[n]`. Comes free if the contract sentence was ever actually said.

---

# LESSON 9 — The practice ladder (in order, with the lesson each teaches)

Attempt each cold with the 5-step method — decision sentence and contract *on paper* — before any hints. Full walkthroughs: [`coding/algorithms/15-dynamic-programming.md`](../coding/algorithms/15-dynamic-programming.md); bridge drills: [`02-algorithms/10-recursion-to-dp.md`](../02-algorithms/10-recursion-to-dp.md).

| # | Problem | It teaches |
|---|---|---|
| 1 | Climbing Stairs | the whole pipeline on the smallest canvas; O(1)-space rolling variables |
| 2 | House Robber | decision sentence with a constraint baked into the recursion (`i+2`) |
| 3 | House Robber II (circle) | reduction: circular = max of two linear runs (drop first / drop last) |
| 4 | Decode Ways | base-case identity discipline; '0' as poison |
| 5 | Coin Change | min-combiner, ∞-poison, the translation to bottom-up |
| 6 | Coin Change II | count-combiner; combinations vs permutations loop order |
| 7 | Unique Paths → Min Path Sum | first 2D grid; same grid, different combiner |
| 8 | Partition Equal Subset Sum | `(i, remaining)` state; 1D compression + the backward loop |
| 9 | LCS | two-sequence shape; hand-fill the table once |
| 10 | Edit Distance | LCS + one more choice per cell; nothing else new — notice that |
| 11 | Word Break | linear state, but the *choice set* is "every dictionary word" |
| 12 | Longest Increasing Subsequence | O(n²) DP → the O(n log n) escalation (binary search crossover) |
| 13 | Stock with Cooldown | live state discovery (§6.2) |
| 14 | Longest Palindromic Substring / Subsequence | `(l, r)` range states |
| 15 | Burst Balloons | decide-the-last-action flip; hardest state in the common canon |
| 16 | Maximum Profit in Job Scheduling | DP + binary search composition — the L4 seam ([HOW_TO_THINK.md](HOW_TO_THINK.md) Part III) |

**Per-problem protocol:** 25 min cold → if stuck, re-run: *decision sentence? contract? what leaks?* (that sequence un-sticks ~80% of attempts) → after solving, do the space-optimization follow-up aloud → log which Lesson-8 bug (if any) you hit. Your bug log converging on one or two entries after ~10 problems tells you exactly what to drill.

---

## The one-card summary

> 1. Recursion is designed by **contract + leap of faith**, never by tracing.
> 2. A DP problem = a shape-1/2/3 recursion whose call tree **repeats labels**.
> 3. Top-down = that recursion + a cache. **Time = states × work per state.**
> 4. Bottom-up = the same recurrence, filled in **dependency order**; derive loop direction from what each cell reads.
> 5. The creative act is the **state**: the minimal past that makes the future solvable. Stuck ⇒ ask *"what leaks?"* — the leak is the missing dimension.
> 6. Read the combiner off the question: ways ⇒ Σ, best ⇒ min/max, possible ⇒ OR.
> 7. Interview default: top-down first, **offer** the bottom-up + space-optimized conversion.

## See Also

- [HOW_TO_THINK.md](HOW_TO_THINK.md) — the Recursion → DP chapter in the full pattern framework
- [PATTERN_LADDERS.md](PATTERN_LADDERS.md) — the DP ladder for graded pressure-testing
- [`02-algorithms/09-recursion.md`](../02-algorithms/09-recursion.md) · [`02-algorithms/10-recursion-to-dp.md`](../02-algorithms/10-recursion-to-dp.md) · [`02-algorithms/15-dynamic-programming.md`](../02-algorithms/15-dynamic-programming.md) — topic deep-dives
- [`coding/algorithms/15-dynamic-programming.md`](../coding/algorithms/15-dynamic-programming.md) — full problem walkthroughs
