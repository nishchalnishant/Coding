# Amazon SDE-2 — Coding Round Execution Guide

## Time Budget Per Problem (45 min round, 1–2 problems)

**One problem:** 40 min coding + 5 min clean-up/Q&A
**Two problems:** 18 min first + 2 min transition + 18 min second + 7 min clean-up

| Phase | Time | What to do |
|---|---|---|
| Understand + clarify | 3–5 min | Ask questions, confirm constraints |
| Brute force + think aloud | 3–5 min | State naive solution, identify bottleneck |
| Optimal approach | 5–7 min | Pattern match, agree on approach before coding |
| Code | 15–20 min | Write clean code, narrate what you're doing |
| Test | 3–5 min | Trace through example, then edge cases |
| Complexity analysis | 1–2 min | State time + space with reasoning |

---

## Clarification Questions to Ask (first 3–5 min)

Always ask at least 2–3 of these before writing code:

**Input constraints:**
- "What's the range of n? Can it be 10^9 or fits in int?"
- "Can the array be empty? Can values be negative?"
- "Is the input sorted or unsorted?"
- "Are there duplicates?"

**Output format:**
- "Should I return indices or values?"
- "If multiple answers exist, return any one or all?"

**Edge cases to confirm:**
- "What should I return if there's no valid answer?"
- "Is the graph directed or undirected? Can it have cycles?"

**Clarifications that reveal the solution:**
- "Can I modify the input in-place?" → signals space optimization expected
- "Is it guaranteed there's always a solution?" → no need for null-case handling
- "Can I use extra space?" → if no, must be O(1) space

---

## How to Think Out Loud

Amazon interviewers evaluate your **thought process**, not just the answer. Structure your verbal output:

**Pattern 1 — Brute force first, then optimize:**
> "A naive approach would be [X] which is O(n²). The bottleneck is [Y]. If I use [data structure / pattern], I can bring it down to O(n log n) because [reason]."

**Pattern 2 — Pattern recognition:**
> "This looks like a [sliding window / BFS / DP] problem because [trigger]. Let me define [state / window / transition]."

**Pattern 3 — Trade-off narration:**
> "I can either [approach A] which is faster but uses O(n) space, or [approach B] which is O(1) space but O(n log n) time. Given the constraints, I'll go with [choice] because [reason]."

---

## If You're Stuck — What to Do

**Step 1 — Try a small example by hand.** Draw it out. Often unlocks the pattern.

**Step 2 — State what you know:**
> "I know the answer involves [X], I'm not sure how to handle [Y] yet."

**Step 3 — Ask for a hint without losing credibility:**
> "I'm considering [approach], does that seem like the right direction?"

**Step 4 — Restate the problem in a simpler form:**
> "If the input was just [trivial case], the answer would be [X]. What's different in the general case?"

**Step 5 — Try adjacent patterns:**
- Stuck on DP? Try recursion + memoization first, then convert.
- Stuck on graph? Try BFS and see if it works before thinking DFS.
- Stuck on optimal? Code brute force first, get it correct, then optimize.

**Never go silent for more than 60 seconds.** Narrate your thinking even when uncertain.

---

## Coding Best Practices (Amazon expects clean code)

**Naming:**
```python
# Bad
def f(a, b):
    r = []
    for i in range(len(a)):
        ...

# Good
def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    result = []
    for start, end in sorted(intervals):
        ...
```

**Helper functions — use them for readability:**
```python
def is_valid(board, row, col, num): ...
def can_reach(graph, src, dst, visited): ...
```

**Avoid:**
- Magic numbers (`if n == 26` → use `NUM_CHARS = 26`)
- Nested ternaries
- Single-letter variables except `i`, `j`, `l`, `r`, `n`, `m`

**Edge cases to always check before saying "done":**
- Empty input (`[]`, `""`, `None`)
- Single element
- All same elements
- Already sorted / reverse sorted
- Integer overflow (mention it, use Python's arbitrary precision or note `long` in Java)

---

## Testing Your Solution (3–5 min at the end)

**Step 1 — Happy path:** trace through the given example manually
**Step 2 — Edge cases:**
```
- [] or "" → what does your code return?
- [1] → single element
- [1, 1, 1] → all same
- Negative numbers if applicable
- Very large n (mention, don't trace)
```
**Step 3 — State complexity:**
> "Time: O(n log n) for sorting + O(n) for the scan = O(n log n). Space: O(n) for the result array, O(1) auxiliary."

---

## After You Write the Code

1. **Don't ask "Is this right?"** — say "Let me verify this by tracing through the example."
2. **Proactively mention trade-offs:** "This is O(n) space; if space is a constraint, I could [alternative]."
3. **Mention what you'd add in production:** "In production I'd add input validation, handle overflow, and add logging."
4. **If the interviewer says "can you optimize?"** — they want you to do it, not just say it's possible.

---

## Red Flags to Avoid

| Red Flag | What It Signals | Fix |
|---|---|---|
| Silent for > 1 min | Can't communicate under pressure | Narrate your thinking always |
| Jump to code without agreeing on approach | Overconfident, wastes time | Confirm approach before line 1 |
| Never test your own code | Won't catch bugs in production | Always trace through at least one example |
| "I'd use a library for this" without knowing the internals | Shallow knowledge | Know the underlying DS (e.g., what OrderedDict does for LRU) |
| Overly complex solution when simple works | Doesn't recognize simple patterns | State brute force first, optimize only if needed |
| Give up when interviewer hints | Low grit | Treat hints as collaboration, not failure |

---

## Round-by-Round Expectations at Amazon SDE-2

| Round | Focus | LP Likely Asked |
|---|---|---|
| Phone Screen 1 (coding) | 1–2 medium LC problems | Ownership, Deliver Results |
| Onsite Round 1 (coding) | 1–2 med/hard, may include LLD | Dive Deep, Invent & Simplify |
| Onsite Round 2 (coding) | 1–2 med/hard, follow-up questions | Customer Obsession, Are Right A Lot |
| Onsite Round 3 (system design) | HLD + trade-offs | Think Big, Frugality |
| Onsite Round 4 (bar raiser) | Mixed — coding or design or LP heavy | Backbone, Highest Standards |

**Bar Raiser round:** This person has no stake in hiring you. They are calibrated across Amazon. They will push back, probe gaps, and sometimes ask something unexpected. Stay calm, be honest about what you don't know, and reason through it.
