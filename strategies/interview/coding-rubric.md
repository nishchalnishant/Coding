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
- Two-week + AI-ML + EET / on-site plan: [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md)

