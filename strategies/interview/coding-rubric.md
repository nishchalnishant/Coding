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

- Full revision guide: [../foundations/GOOGLE_INTERVIEW_REVISION.md](../foundations/GOOGLE_INTERVIEW_REVISION.md)
- One-page sheet: [../foundations/GOOGLE_QUICK_SHEET.md](../foundations/GOOGLE_QUICK_SHEET.md)
- Canonical question index: [../foundations/TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md](../foundations/TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md)
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
- [ ] Edit Distance (2D DP, string alignment)
- [ ] Burst Balloons (interval DP, non-standard state)
- [ ] Strange Printer (interval DP)
- [ ] Regular Expression Matching (2D DP with wildcards)
- [ ] Minimum Cost to Cut a Stick (interval DP)
- [ ] Longest Increasing Path in Matrix (DFS + memoization)

### Graphs
- [ ] Word Ladder II (BFS + backtracking, hard)
- [ ] Alien Dictionary (topological sort, implicit graph)
- [ ] Reconstruct Itinerary (Eulerian path, Hierholzer's)
- [ ] Critical Connections (Tarjan's bridges)
- [ ] Swim in Rising Water (Dijkstra or binary search + BFS)

### Arrays / Sliding Window
- [ ] Minimum Window Substring (sliding window, hard)
- [ ] Trapping Rain Water (two pointers, hard)
- [ ] Median of Two Sorted Arrays (binary search, very hard)
- [ ] Sliding Window Maximum (monotonic deque)
- [ ] Count of Smaller Numbers After Self (merge sort / BIT)

### Trees
- [ ] Serialize/Deserialize Binary Tree
- [ ] Binary Tree Maximum Path Sum (tree DP)
- [ ] Recover Binary Search Tree (Morris traversal)
- [ ] Vertical Order Traversal of Binary Tree

### Design
- [ ] LRU Cache (O(1) get/put)
- [ ] LFU Cache (O(1) get/put) — harder
- [ ] Design Twitter / Top-K tweets (heap + hash map)
- [ ] Implement Trie with Wildcard Search

> [!TIP]
> Track which of these you can solve in < 25 minutes without hints. That is the SDE-3 bar. Any you cannot → add to your next week's practice queue.
