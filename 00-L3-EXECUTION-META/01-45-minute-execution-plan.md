# The 45-Minute Google Execution Plan `⚡ T1`

> [!important] The Silent Failure
> Most L3 candidates fail because they start writing code at Minute 5. You are graded heavily on **communication** and **design**. Follow this exact pacing to ensure you hit every metric on the Google rubric.

## Minute 0 – 5: De-risk and Clarify
**Goal:** Prove you don't make blind assumptions.
1. **Listen:** Write down the key constraints while the interviewer speaks.
2. **Repeat:** Summarize the problem back to them. *"Just to make sure I understand, you're asking me to..."*
3. **Clarify Edge Cases:** 
   - *"Can the array be empty?"*
   - *"Are there negative numbers?"*
   - *"Does the graph have cycles?"*
   - *"Will the inputs fit in memory?"*
4. **Write an Example:** Do NOT use the example they gave you. Write a small, slightly tricky example yourself to prove you understand the problem.

## Minute 5 – 15: The Design Phase
**Goal:** Agree on the optimal algorithm *before* writing a single line of code.
1. **State the Brute Force:** *"The naive approach would be X, which takes O(N^2) time. We can do better."*
2. **Reverse Engineer Constraints:** Use the Big-O Constraint Heuristic to guess the expected algorithm. (e.g. *"Since N=10^5, I'm thinking of an O(N) sliding window."*)
3. **Pitch the Optimal Solution:** Verbally explain the algorithm. Draw it out using pseudo-code or ASCII arrays.
4. **Get the Green Light:** *"Does this approach sound good to you, or would you like me to optimize further?"* **Do not code until they say yes.**

## Minute 15 – 35: Silent Coding
**Goal:** Write clean, modular, bug-free code.
1. **Pacing:** Stop talking. It slows you down. Say: *"I'm going to take a few minutes to write this out, and then I'll walk you through it."*
2. **Modularity:** Abstract complex logic into helper functions. *"I'll write a `is_valid()` helper function here, I'll implement it later if we have time."*
3. **Clean Code:** Use highly descriptive variable names (`max_window_size` instead of `m`). 
4. **No Hacks:** Don't use obscure language tricks. Keep it readable.

## Minute 35 – 45: Dry Run and Big-O (Crucial!)
**Goal:** Find your own bugs before the interviewer points them out.
1. **Trace the Code:** Take your custom example from Minute 5 and walk through your code line-by-line. Literally write down the state of your variables in a comment block.
   ```python
   # i = 0, curr_sum = 5, max_sum = 5
   # i = 1, curr_sum = -2, max_sum = 5 ...
   ```
2. **Fix Bugs Gracefully:** If you find a bug during the dry run, say *"Ah, I see a bug here, let me fix that."* This is a massive positive signal!
3. **State Complexity:** *"The time complexity is O(N) because we visit each node at most twice. The space complexity is O(N) due to the recursive call stack."*
4. **Answer Follow-ups:** Be prepared for: *"What if the data was too large to fit in memory?"*
