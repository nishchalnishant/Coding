---
module: 05-revision
topic: Coding Rubric
subtopic: 
status: unread
tags: [revision, coding-rubric]
---
# First-Principles Map — Coding Interview Rubric

```
WHY a Scoring Rubric exists
├── Interviewers don't score "did they solve it" — they score on 4–5 axes independently
├── A candidate can solve the problem and still get a no-hire on communication or testing axes
└── Knowing the rubric lets you optimize for all axes, not just correctness

WHAT it is
├── A multi-axis scoring framework: Problem Solving, Coding, Testing, Communication + optional Optimization
├── Each axis has explicit "hire" and "no-hire" signals — these are the actual levers
└── Examples:
    ├── Problem Solving hire signal: arrives at optimal approach, states tradeoffs
    ├── Coding hire signal: clean variable names, no major bugs, handles edge cases in code
    ├── Testing hire signal: tests happy path + 2 edge cases voluntarily, catches own bugs
    └── Communication hire signal: thinks aloud, names patterns, non-defensive to feedback

HOW it works
├── Problem Solving axis:
│   ├── Hire: correct approach within 10 min, awareness of suboptimal alternatives
│   ├── Strong hire: optimal approach + proactively discusses tradeoffs
│   └── No hire: brute force only, can't move toward optimal with hints
├── Coding axis:
│   ├── Hire: compiles mentally, no major bugs, readable names, appropriate abstractions
│   ├── Strong hire: concise + handles edge cases inline + no dead code
│   └── No hire: major logic bugs, unreadable variable names, can't debug own code
├── Testing axis:
│   ├── Hire: tests with example + 1 edge case + 1 stress case voluntarily
│   ├── Strong hire: derives test cases from invariants, not just examples given
│   └── No hire: no testing step, or only tests the given example
├── Communication axis:
│   ├── Hire: narrates reasoning, asks clarifying questions, responsive to hints
│   ├── Strong hire: structures the conversation ("I'll start with brute force, then optimize")
│   └── No hire: silent coding, defensive when corrected, never clarifies
└── Complexity scoring:
    ├── Must state both time AND space complexity unprompted
    ├── Must be able to derive it, not just recite it
    └── Wrong complexity = downgrade on Problem Solving axis

WHEN to use
├── During every mock: self-score on all 4 axes after each problem
├── Before the real interview: internalize what "hire" looks like on each axis
└── Decision:
    ├── Time running out → prioritize working brute force + complexity over clean optimal
    ├── Bug found late → fix and say "I caught a bug here" — shows testing signal
    └── Hint received → incorporate cleanly, acknowledge it — shows non-defensiveness

WHAT can go wrong
├── Solving optimally but silently → Communication = no hire → overall no hire
├── Clean code but no complexity stated → Problem Solving downgrade
├── Testing only the happy path → Testing = no hire at L4+
└── Getting defensive when interviewer probes a mistake → Googleyness anti-signal
```

## First-Principles Breakdown

- **Root problem:** Candidates optimize for the wrong signal (correctness) when the actual scoring is multi-axis — a rubric-aware candidate allocates effort across all scored dimensions.
- **Core insight:** Communication and testing axes are scored even when you solve correctly — they are not bonus points, they are required for a hire signal at L4.
- **Invariant:** A no-hire on any single axis can override strong performance on others — all axes must clear the bar, not just problem solving.
- **Why it works:** The rubric externalizes the interviewer's internal scoring model — once you know the model, you can practice to each axis explicitly rather than practicing blind.
- **Where it breaks:** Rubric-gaming (performing communication without genuine understanding) is detectable under probing — the rubric guides practice focus, not interview theater.

---

# Google Coding Rounds (SDE-2) — Rubric + Checklist

Use this as a “runbook” for every timed practice and mock.

---

## What “strong” looks like

- **Correctness**: handles edge cases, doesn’t crash, passes examples.
- **Algorithm choice**: avoids brute force when a standard pattern fits.
- **Code quality**: readable names, clean control flow, no over-engineering.
- **Communication**: constraints → approach → invariants → tests → complexity.

---

## The 7-step flow (practice until automatic)

1. **Restate** the problem and confirm constraints.
2. **Examples**: run 1 normal + 1 edge case verbally.
3. **Brute force** quickly (time/space), then explain why it’s too slow (if needed).
4. **Optimal approach**: name the pattern (e.g., “prefix sum + hash map”) and the invariant.
5. **Code**: implement in small, testable chunks.
6. **Test**: run through 2–3 cases by hand (incl. edge case).
7. **Close**: time + space; mention one follow-up direction.

---

## Time Budget Per Step (45-minute round)

| Step | Budget | If running over |
|------|--------|-----------------|
| Restate + clarify | 2–3 min | Hard stop — don't over-clarify |
| Examples (normal + edge) | 2–3 min | Pick the most adversarial edge case, drop the rest |
| Brute force (name it, don't code it) | 1–2 min | Just say "O(N²) nested loop" and move on |
| Optimal approach + invariant | 3–5 min | This is the most valuable time — don't rush it |
| Code | 15–20 min | If stuck >5 min, state the assumption and move forward |
| Test (trace 2 cases by hand) | 3–5 min | At minimum trace the one edge case you mentioned earlier |
| Complexity + follow-up | 1–2 min | Always reserve this — interviewers dock for skipping it |

> [!CAUTION]
> If you hit 20 minutes and haven't started coding, you will almost certainly not finish. When approach discussion runs long, say: "I think I have enough to code — let me start and talk through it as I go."

## SDE-3 Differentiators (beyond just solving it)

- State the invariant before writing the loop, not after: "At all times, `left` points to the first unprocessed element."
- Call out the edge case *before* the interviewer does: "I'll handle the empty input case first."
- Drive the complexity conversation: "This is O(N log N) — if we need O(N) I'd switch to a counting sort approach."
- After coding, proactively ask: "Want me to extend this to handle [natural follow-up]?" — shows you're thinking ahead.
- Self-correct out loud: "Wait, this fails when all elements are negative — let me fix the initialization." Never silently patch a bug.

---

## Must-say edge cases (default set)

- Empty input, length 1, all duplicates, negative numbers, overflow (if sums).
- Graph/tree: empty, single node, disconnected components.
- Strings: unicode/case sensitivity (ask), repeated chars.

---

## Debugging checklist (when you get stuck)

- Off-by-one (`<` vs `<=`, window length, bounds in binary search)
- Wrong invariant (what exactly is “valid” in sliding window?)
- Visited/state bugs (graph BFS/DFS)
- Mutation hazards (in-place edits, shared lists in recursion)
- Forgot base case / return value meaning (tree DP)

---

## When You're Stuck — Recovery Protocol

**Step 1 — Verbalize the block** (30 sec): “I know I need to find X but I'm not sure how to efficiently track Y. Let me think out loud.”

**Step 2 — Fall back to brute force** (1 min): Code the O(N²) or naive version. A working slow solution scores better than no solution.

**Step 3 — Ask a scoped question**: Not “can you give me a hint?” — instead: “Is it safe to assume the input fits in memory?” or “Would a hash map be the right data structure here?” Interviewers respond better to specific questions.

**Step 4 — Pattern match out loud**: “This feels like it could be a sliding window problem because I'm looking for a contiguous subarray. Is that the right direction?”

**Step 5 — State your plan, then code it**: Even if uncertain, say: “I'm going to try prefix sums here — I can optimize later if this doesn't work.”

> [!TIP]
> The worst response to being stuck is silence. An interviewer who sees you methodically working through possibilities will score you higher than one who sees you frozen. Thinking out loud IS part of the evaluation.

---

## “Google-style” communication lines (copy/paste into your brain)

- “Let me confirm constraints: can input be empty? duplicates? size limits?”
- “Brute force is O(n²) by checking all pairs; we can do O(n) using a hash map…”
- “The invariant is: the window `[i..j]` always contains at most K distinct…”
- “Time is O(n) because each pointer moves at most n times.”

---

## Virtual (video) vs in-person DSA (same bar, different logistics)

| Setting | What to practice |
|--------|-------------------|
| **Virtual** (e.g. Google Meet, screen share, shared doc) | **Audio first**: think out loud even when not typing. **Test once**: camera, mic, **screen share**, and the **IDE / language** you will use. One monitor is fine; know how to **split** problem statement and editor. **Time zone** and **link** in calendar. Minimize **keyboard noise**; have water nearby. If you have **two** DSA rounds in different formats, do at least one full mock in **video** before the virtual round — see [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md). |
| **In person** | Confirm whether you will **type on a laptop** or use a **whiteboard** (varies by site). Practice that medium: if whiteboard, **bigger** print, leave space for corrections; if laptop, same hygiene as home. Arrive with **buffer** for check-in. |

Both settings: the rubric in **What “strong” looks like** is unchanged. Weak communication hurts more on video when the interviewer cannot read your full scratch work.

---

## Brute → optimal progressions (practice saying these out loud)

The interviewer expects you to start with the brute force, explain why it's slow, then optimize. Practice narrating each transition.

### Two Sum
- Brute: try all pairs → O(n²) time, O(1) space
- Optimal: one-pass hash map — store `target - x` as we go → O(n) time, O(n) space
- Say: "I can eliminate the inner loop by storing complements in a hash map."

### Subarray Sum = K
- Brute: all subarrays O(n²), sum each → O(n³) or O(n²) with running sum
- Optimal: prefix sum + hash map counting occurrences of `prefix[i] - k` → O(n)
- Say: "The key insight is that a subarray sum equals K iff two prefix sums differ by K."

### Longest Substring Without Repeating
- Brute: try all substrings, check uniqueness → O(n³)
- Better: fix left, expand right → O(n²)
- Optimal: sliding window — jump `left` directly to `last_seen[char] + 1` → O(n)
- Say: "Instead of shrinking one step at a time, I jump left past the duplicate."

### Maximum Subarray (Kadane)
- Brute: all subarrays, sum each → O(n²)
- Optimal: running sum — reset to 0 when negative → O(n)
- Say: "A negative prefix only hurts any extension of it, so I discard it."

### Search in Rotated Sorted Array
- Brute: linear scan → O(n)
- Optimal: binary search — at each mid, one half is guaranteed sorted → O(log n)
- Say: "I check which half is sorted, then decide which half to search."

### Coin Change
- Brute: recursion, try every denomination → exponential
- Optimal: DP bottom-up — `dp[i] = min(dp[i], dp[i-coin] + 1)` → O(amount × coins)
- Say: "This has overlapping subproblems — the minimum coins to make amount X is reused many times."

### Course Schedule (cycle detection)
- Brute: DFS from every node, mark visited → O(V²) if not careful
- Optimal: topo sort (Kahn's BFS with in-degree) → O(V+E); if all nodes processed, no cycle
- Say: "I count in-degrees and process zero-in-degree nodes; if any remain at the end, there's a cycle."

### Trapping Rain Water
- Brute: for each cell, scan left and right for max heights → O(n²)
- Better: precompute left_max and right_max arrays → O(n), O(n) space
- Optimal: two pointers — process from shorter side, no extra arrays → O(n), O(1) space
- Say: "The water at any cell is determined by the shorter of the two sides. Two pointers let me process the shorter side without precomputing."

### Merge K Sorted Lists
- Brute: collect all, sort → O(n log n) where n = total nodes
- Better: merge pairs repeatedly → O(n log k) but more complex
- Optimal: min-heap of size k → push next node when one is popped → O(n log k)
- Say: "A heap gives me the minimum of k front-of-list values in O(log k) per step."

### LIS (Longest Increasing Subsequence)
- Brute: all subsequences → O(2^n)
- DP: `dp[i] = max(dp[j]+1 for j<i if a[j]<a[i])` → O(n²)
- Optimal: patience sorting — maintain `tails` array, binary search → O(n log n)
- Say: "I maintain an array `tails` where `tails[i]` is the smallest tail of any increasing subsequence of length i+1. Binary search tells me where to place each element."

---

## Where to revise inside this repo

- Full revision guide: [../03-patterns/GOOGLE_INTERVIEW_REVISION.md](../03-patterns/GOOGLE_INTERVIEW_REVISION.md)
- One-page sheet: [../03-patterns/GOOGLE_QUICK_SHEET.md](../03-patterns/GOOGLE_QUICK_SHEET.md)
- Canonical question index: [../03-patterns/TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md](../03-patterns/TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md)
- [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md)

---

## 🎙️ The Coach's Dialogue: The "SDE-3 Vibe"

**Student:** "Coach, everyone says I'm good at coding, but I keep getting leveled at SDE-2. What am I missing for that SDE-3 / Senior signal?"

**Coach:** "It’s not your code; it’s your **Leadership**. An SDE-2 solves the problem. An SDE-3 **owns** the problem. When I give you a vague prompt, don't just start coding. Stop. Ask about the 'Why.' If I say 'Merge these logs,' don't just say 'Merge Sort.' Ask if they're coming in as a stream, if they're already partially sorted, or if we need to handle multi-terabyte files."

**Student:** "So I should spend more time talking?"

**Coach:** "No, you should spend more time **Driving**. You're the pilot; I'm the air traffic controller. I want to see you weigh trade-offs. 'I could use a Hash Map here for O(N) time, but the space might blow up if we have 100 million keys. Since memory is tight, I'll use a two-pointer approach even if it's O(N log N).' That is music to a senior interviewer's ears."

**Student:** "What about when I make a mistake?"

**Coach:** "Senior candidates catch their own bugs. If you realize your logic is flawed, don't panic. Say: 'Actually, I just realized this greedy approach fails for [X] case. Let me pivot to DP.' That self-correction is a massive positive signal. It shows you're not just following a script—you're thinking from first principles."

**Student:** "And the communication during the code?"

**Coach:** "Keep it high-level. Don't explain `i++`. Explain the **Invariant**. Instead of 'I'm incrementing the index,' say 'I'm moving the window boundary to maintain the uniqueness constraint.' Talk like a software architect, not a code monkey."

---

## SDE-3 Hard Problem Checklist

Problems that appear at the ceiling of SDE-3 coding rounds. If you can solve these fluently, you are prepared.

### Dynamic Programming
- [ ] Edit Distance — **2D DP**; `dp[i][j]` = edit distance of `s1[:i]` and `s2[:j]`; transition: match → diagonal, else min(insert, delete, replace) + 1
- [ ] Burst Balloons — **Interval DP**; key trick: think of `k` as the *last* balloon burst in range `[l,r]`, not the first; avoids dependency on already-burst neighbors
- [ ] Strange Printer — **Interval DP**; key trick: a turn can extend an existing character's print range for free; `dp[i][j] = dp[i+1][j]` then check if any `k` where `s[k]==s[i]` can merge
- [ ] Regular Expression Matching — **2D DP with `*` lookahead**; `*` means 0 or more of preceding; key: `dp[i][j]` = does `s[:i]` match `p[:j]`; `*` case: zero uses (`dp[i][j-2]`) or one-more use (`dp[i-1][j]` if chars match)
- [ ] Minimum Cost to Cut a Stick — **Interval DP**; add 0 and n as sentinel cuts; `dp[i][j]` = min cost to make all cuts between sentinel[i] and sentinel[j]; cost of a cut = length of current segment
- [ ] Longest Increasing Path in Matrix — **DFS + memoization on DAG**; key: no visited set needed because strictly increasing means no cycles; memoize result per cell

### Graphs
- [ ] Word Ladder II — **BFS for shortest path length + DFS/backtrack for all paths**; key trick: build neighbor graph during BFS, then DFS only along edges that decrease level (next level = current + 1)
- [ ] Alien Dictionary — **Topological sort on implicit graph**; key: compare adjacent words in list — if `word[i]` is a prefix of `word[i+1]` but longer, return `""`; each differing char gives a directed edge
- [ ] Reconstruct Itinerary — **Eulerian path via Hierholzer's**; key: use min-heap for lexicographic order; post-order DFS (add to result *after* all neighbors visited); reverse at end
- [ ] Critical Connections (Tarjan's) — **DFS with `disc[]` and `low[]`**; edge `u→v` is a bridge iff `low[v] > disc[u]`; `low[v]` = earliest disc reachable from v's subtree without using parent edge
- [ ] Swim in Rising Water — **Dijkstra** (min-cost path where cost = max edge weight); or binary search on answer + BFS/DFS to verify reachability at that water level

### Arrays / Sliding Window
- [ ] Minimum Window Substring — **Sliding window with frequency map**; expand right until valid, then contract left; track `have` vs `need` counts; O(n)
- [ ] Trapping Rain Water — **Two pointers**; key: water at cell = `min(left_max, right_max) - height[i]`; process from the shorter-max side, no precompute needed; O(n) O(1)
- [ ] Median of Two Sorted Arrays — **Binary search on partition**; partition both arrays such that left halves ≤ right halves; binary search on the smaller array's partition index; O(log min(m,n))
- [ ] Sliding Window Maximum — **Monotonic deque** (decreasing); deque stores indices; pop front if out of window, pop back if smaller than current; front is always max
- [ ] Count of Smaller Numbers After Self — **Merge sort**: during merge, count how many right-half elements end up before each left-half element; or **BIT** with coordinate compression

### Trees
- [ ] Serialize/Deserialize Binary Tree — **Preorder with null markers**; serialize: `val,left,right`; deserialize: use a queue/iterator, build node then recurse; no delimiter needed if you use fixed-width or comma-separated
- [ ] Binary Tree Maximum Path Sum — **Tree DP**; at each node: `gain = node.val + max(0, left_gain) + max(0, right_gain)`; update global max; return `node.val + max(0, left_gain, right_gain)` (single path up)
- [ ] Recover Binary Search Tree — **Morris in-order traversal** (O(1) space); find two swapped nodes: first swap = where `prev > curr` first time, second swap = where it happens again (or same `curr`); swap their values
- [ ] Vertical Order Traversal — **BFS with (row, col) coordinates**; group nodes by col, sort by row within col, sort by val within same (row, col); use `collections.defaultdict` + sort

### Design
- [ ] LRU Cache — **HashMap + Doubly Linked List**; map stores key→node; DLL maintains recency order; `get` and `put` both O(1); use sentinel head/tail to avoid null checks
- [ ] LFU Cache — **HashMap of key→(val, freq) + HashMap of freq→OrderedDict**; track min_freq; on access, move key from `freq[f]` to `freq[f+1]`; evict from `freq[min_freq]`; all O(1)
- [ ] Design Twitter / Top-K tweets — **Heap** of size 10; each user has a tweet list (id, timestamp); merge across followees using min-heap; maintain follow/unfollow sets per user
- [ ] Implement Trie with Wildcard Search — **Trie + DFS for `.` wildcard**; `search` recurses into all children at `.` nodes; `addWord` is standard trie insert; key: wildcard only in search, not insert

> [!TIP]
> Track which of these you can solve in < 25 minutes without hints. That is the SDE-3 bar. Any you cannot → add to your next week's practice queue.
