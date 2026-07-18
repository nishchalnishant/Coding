---
tags: [l4-google, sde2, roadmap, delta]
topic: L4 (SDE-2) Delta — what changes on top of the L3 base
---

# Google L4 (SDE-2) Delta — Upgrade Layer

> **How to use this file:** Everything in the L3 track ([`l3-google-roadmap.md`](l3-google-roadmap.md)) is still the foundation — L4 loops draw from the *same* topic pool. This file lists only what **changes**: the higher bar, tier promotions, and ~35 gap problems the L3 track doesn't cover. Study the L3 base first; layer this on top.

---

## 1. What actually changes at L4

The topic list barely changes. The **bar** changes:

| Dimension | L3 bar | L4 bar |
| :--- | :--- | :--- |
| Problem difficulty | Solve one medium cleanly | Solve the medium **fast** (~20–25 min), then handle a **harder follow-up** in the same round |
| Follow-ups | Nice bonus | **Expected.** Rounds are follow-up chains: base → constraint change → scale change ("what if the input is a stream / doesn't fit in memory / has updates?") |
| Optimality | Near-optimal accepted with good communication | Optimal expected; you should *volunteer* the trade-off between approaches unprompted |
| Ambiguity | Problem is mostly well-specified | Problems are deliberately underspecified — driving the clarification is graded |
| Code quality | Correct and readable | Correct, readable, **and structured** — helper functions, good names, testable units |
| DP | Basic (T2) | Fluent (T1) — 1D/grid/string DP derived from recursion, not recalled |
| Dijkstra | Recognize (T2) | **Implement cold** (T1), including on implicit/grid graphs |
| Design-a-data-structure | LRU Cache | A whole problem family (see §3.1) — Google L4 loves these |
| Behavioral | Collaboration, learning | + **Ownership, influence, handling disagreement** — stories where *you* drove an outcome across people |

**Still skipped at L4** (unchanged from L3): segment trees / BIT implementation (concept sentence only), Tarjan SCC/bridges implementation, bitmask DP, digit DP, Manacher, suffix automata, system design (L4 loops at Google are still DSA + behavioral; design appears at L5).

---

## 2. Tier promotions (L3 → L4)

Update your mental tier table; the files still say L3 tiers.

| Topic | L3 tier | L4 tier | Why |
| :--- | :--- | :--- | :--- |
| Dynamic Programming (1D, grid, string) | 🎯 T2 | ⚡ T1 | Appears in most L4 loops; follow-ups escalate into DP |
| Dijkstra (incl. on grids) | 🎯 T2 | ⚡ T1 | Grid-Dijkstra (Min Effort, Swim in Water) is a Google favorite |
| Intervals / sweep line | 🎯 T2 | ⚡ T1 | Calendar/booking family is classic Google L4 |
| Design-a-data-structure | 🎯 T2 (LRU only) | ⚡ T1 | See §3.1 — hash+list/heap composition under op-complexity constraints |
| String parsing / simulation | 🎯 T2 | ⚡ T1 | Calculator/justification-style "messy but honest" problems |
| Monotonic stack (contribution variants) | 🎯 T2 | stays 🎯 T2 | but add Sum of Subarray Minimums, Car Fleet |
| Binary search on answer | ⚡ T1 | ⚡ T1 | unchanged, but drill the *harder* instances (Split Array Largest Sum) |

---

## 3. Gap problems (not in the L3 track)

Tiers below are **L4 tiers**. Format matches the topic indexes: tier, difficulty, key insight.

### 3.1 Design-a-data-structure `⚡ T1` — the biggest L3→L4 gap

The pattern behind all of these: **compose two structures so each covers the other's weak operation**, and reason out loud about per-op complexity. Full walkthroughs with code: [`coding/data-structures/14-design.md`](data-structures/14-design.md).

- **Insert Delete GetRandom O(1)** `⚡ T1` · Medium
  - Key insight: array (O(1) random via `random.choice`) + hashmap value→index. Delete = swap-with-last, pop. The swap trick is the whole problem.
- **LFU Cache** `⚡ T1` · Hard
  - Key insight: `freq → DLL of nodes` + `key → node` map + `min_freq` counter. On access, move node to freq+1 list; reset `min_freq = 1` on insert.
- **Random Pick with Weight** `⚡ T1` · Medium
  - Key insight: prefix-sum array + binary search (`bisect_left`) on a uniform random in `[1, total]`. Bridges two T1 patterns.
- **Design Hit Counter** `⚡ T1` · Medium
  - Key insight: deque of timestamps, evict `< t-300` on each call. Follow-up (huge traffic): 300-slot circular buffer of `(time, count)`.
- **Snapshot Array** `🎯 T2` · Medium
  - Key insight: per index store `[(snap_id, val)]`; `get` = binary search on snap_id. Copying the array per snapshot is the trap.
- **Stock Price Fluctuation** `🎯 T2` · Medium
  - Key insight: hashmap for latest + two heaps with **lazy deletion** (validate top against hashmap on pop). Same lazy-delete trick as Sliding Window Median.
- **Peeking Iterator / Flatten Nested List Iterator** `🎯 T2` · Medium
  - Key insight: cache one element ahead (`peek`); for nested — stack of iterators, flatten lazily in `hasNext`, not in constructor.
- **Logger Rate Limiter** `💤 warm-up` · Easy
  - Key insight: `msg → last_ts` map; use as a 5-minute warm-up before the family above.

### 3.2 Intervals / sweep line `⚡ T1`

Full walkthroughs with code: [`coding/algorithms/16-greedy.md` → "Intervals & Sweep — L4 additions"](algorithms/16-greedy.md#intervals--sweep--l4-additions).

- **Insert Interval** `⚡ T1` · Medium
  - Key insight: three phases — copy all ending before, merge all overlapping into one, copy rest. No sort needed (input sorted).
- **Interval List Intersections** `⚡ T1` · Medium
  - Key insight: two pointers; intersection = `[max(starts), min(ends)]`, valid if start ≤ end; advance the one that ends first.
- **My Calendar I / II** `⚡ T1` · Medium
  - Key insight: I — keep sorted list, overlap iff `start < e and s < end`. II — maintain a separate `overlaps` list; a triple booking is a conflict with an overlap. Generalization (My Calendar III / k-booking) = sweep line with a diff map.
- **Employee Free Time** `🎯 T2` · Hard
  - Key insight: flatten + sort all intervals (or k-way heap merge); gaps between merged intervals = free time.
- **Car Pooling** `🎯 T2` · Medium
  - Key insight: difference array over stops — `+passengers` at pickup, `-` at drop; prefix-scan, check ≤ capacity. Same trick as Meeting Rooms II via events.

### 3.3 Graphs — the harder layer `⚡ T1`

Full walkthroughs with code: [`coding/data-structures/13-graph.md` → "Implicit-Graph BFS — L4 additions"](data-structures/13-graph.md#implicit-graph-bfs--l4-additions); LIP: [`04-matrix.md` → "DP on the Grid"](data-structures/04-matrix.md#dp-on-the-grid--l4-addition).

- **Longest Increasing Path in a Matrix** `⚡ T1` · Hard
  - Key insight: DFS + memo; strictly-increasing rule means no cycles → no visited set needed. This *is* DP on an implicit DAG — say that.
- **Snakes and Ladders** `🎯 T2` · Medium
  - Key insight: pure BFS once you write the `square → (row, col)` decode (boustrophedon). The mapping *is* the problem.
- **Bus Routes** `🎯 T2` · Hard
  - Key insight: BFS on **routes**, not stops — `stop → routes` map; answer counts buses, so nodes must be routes.
- **Word Ladder II** `🎯 T2` · Hard
  - Key insight: BFS to record `parents` per word at its first level, then backtrack paths from end. Never collect paths during BFS itself.
- Already in the L3 track but promote to **must-implement-cold**: Network Delay Time, Path With Minimum Effort, Swim in Rising Water (grid Dijkstra), Cheapest Flights (Bellman-Ford K-rounds).

### 3.4 String parsing / simulation `⚡ T1`

Full walkthroughs with code: [`coding/data-structures/03-string.md` → "Parsing & Simulation — L4 additions"](data-structures/03-string.md#parsing--simulation--l4-additions).

- **Text Justification** `⚡ T1` · Hard
  - Key insight: greedy line packing, then distribute spaces left-heavy: `gaps = words-1`, each gap gets `total//gaps`, first `total%gaps` gaps get one extra. Last line + single-word lines are left-justified. Pure care, zero algorithms — exactly why Google asks it.
- **String to Integer (atoi)** `🎯 T2` · Medium
  - Key insight: strip → sign → digits → clamp. The grading is on your edge-case enumeration, not the loop.
- **Valid Number** `🎯 T2` · Hard
  - Key insight: state flags (`seen_digit`, `seen_dot`, `seen_exp`); after `e` reset `seen_digit`. Enumerate the grammar out loud before coding.
- Already present, promote to T1: Basic Calculator II, Decode String.

### 3.5 Monotonic stack — contribution counting `🎯 T2`

Full walkthroughs with code: [`coding/data-structures/05-stack.md` → "Contribution Counting — L4 additions"](data-structures/05-stack.md#contribution-counting--l4-additions).

- **Sum of Subarray Minimums** `🎯 T2` · Medium
  - Key insight: for each element, count subarrays where it's the min: `left[i] * right[i] * a[i]` via prev-smaller / next-smaller. Use strict `<` one side, `<=` the other to avoid double-counting equals.
- **Car Fleet** `🎯 T2` · Medium
  - Key insight: sort by position desc; compute arrival time; a car joins the fleet ahead if its time ≤ fleet's time. Stack of fleet arrival times.

### 3.6 Randomization `🎯 T2`

- **Reservoir Sampling (Linked List Random Node)** `🎯 T2` · Medium
  - Key insight: keep i-th element with probability 1/i. State the inductive proof in one sentence — that's the whole interview.
- **Shuffle an Array (Fisher–Yates)** `🎯 T2` · Medium
  - Key insight: `for i from n-1 down: swap(i, rand(0..i))`. Know why naive "swap with any index" is biased (nⁿ vs n! outcomes).

### 3.7 DP — the L4 layer (on top of the L3 T2 list)

- **Longest Increasing Path in Matrix** — see §3.3; the canonical "DP meets graphs" bridge.
- **Maximum Profit in Job Scheduling** `🎯 T2` · Hard — [walkthrough](algorithms/15-dynamic-programming.md#dp--binary-search--l4-addition)
  - Key insight: sort by end; `dp[i] = max(dp[i-1], profit + dp[bisect(ends, start)])`. DP + binary search composition — very Google.
- **Partition to K Equal Sum Subsets** `🎯 T2` · Medium — [walkthrough](algorithms/12-backtracking.md#partition-to-k-equal-sum-subsets--t2)
  - Key insight: backtracking filling one bucket at a time + pruning (sort desc, skip equal failures). Mention bitmask-DP exists; don't implement it.
- **Cherry Pickup II / Minimum Falling Path** `💤 T3` — only if time remains.

---

## 4. L4 6-week schedule

Weeks 1–4 = the L3 schedule ([roadmap](l3-google-roadmap.md)), with two amendments: treat DP as T1 from week 3, and implement Dijkstra cold in week 1. Then:

| Week | Focus |
| :--- | :--- |
| **5** | §3.1 design-DS family + §3.2 intervals + §3.4 parsing. One 45-min mock mid-week. |
| **6** | §3.3 hard graphs + §3.5–3.7 + **follow-up drills**: for every T1 problem you know, answer "what if it's a stream?", "what if it doesn't fit in memory?", "what if there are updates?" out loud. 3 timed mocks from the [L4 mock rounds](../03-patterns/MOCK_INTERVIEW_SET.md#l4-sde-2-mock-rounds--follow-up-chains). |

**Follow-up drill table** (the L4-defining skill):

| Base problem | Standard follow-up chain |
| :--- | :--- |
| Two Sum | sorted input → two pointers · data is a stream → design class · count pairs |
| Kth Largest | stream → heap class · distributed data → partial heaps / quickselect trade-off |
| Merge Intervals | intervals arrive one-by-one → My Calendar · count max overlap → sweep line |
| Number of Islands | grid is huge/sparse → hashset of land · islands added dynamically → Union-Find (Islands II) |
| LRU Cache | frequency instead of recency → LFU · thread-safety question → talk locks, don't code |
| Word Search | many words → Trie + prune (Word Search II) |
| Course Schedule | return order → II · parallel semesters → level-by-level Kahn's |

---

## 5. Behavioral delta

Same STAR bank ([`04-behavioral/`](../04-behavioral/BEHAVIORAL_GOOGLINESS.md)), but L4 interviewers probe for **scope and ownership**. Make sure at least 3 stories hit:

1. **Drove a decision across disagreement** — you changed the outcome, not just participated.
2. **Owned a failure end-to-end** — detection, fix, prevention, what you'd do differently.
3. **Influenced without authority** — convinced another team/senior, or mentored someone to a result.

If your current stories are "I completed my task well," upgrade them: same events, re-told at the level of decisions you made and their blast radius.
