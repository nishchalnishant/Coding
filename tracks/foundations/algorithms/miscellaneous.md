# Miscellaneous Algorithms

Tips and cross-cutting techniques for problems that combine multiple categories (math, graph, DP, greedy, etc.). Use with the dedicated topic files in this folder for full depth.

#### 1. **Familiarize with Different Categories**

* Understand the categories of algorithms that don't fit neatly into standard data structures or problem types, such as geometry algorithms, string manipulation, and others.
* Be aware of common problems that can be solved using a combination of techniques from various algorithm categories.

#### 2. **Common Problem-Solving Techniques**

* **Brute Force**: Start with a brute-force solution to understand the problem better, then optimize if necessary.
* **Greedy Algorithms**: Use when local optimum choices lead to a global optimum, especially for problems involving optimization (like interval scheduling).
* **Dynamic Programming**: Use when the problem has overlapping subproblems and optimal substructure. Be prepared to break problems down into smaller, manageable components.

#### 3. **Mathematical Algorithms**

* Familiarize yourself with algorithms related to number theory, combinatorics, and probability. This includes GCD, LCM, prime factorization, and permutations.
* Understand basic combinatorial counting techniques, such as combinations and permutations, and how to implement them.

#### 4. **Graph-Related Problems**

* Recognize problems that can be solved using graph algorithms, even if they don't explicitly mention graphs (e.g., social network connections).
* Be comfortable applying graph algorithms (like BFS/DFS) in unique contexts.

#### 5. **Sorting and Searching Techniques**

* Master various sorting algorithms (quick sort, merge sort, heap sort) and understand their time and space complexities.
* Be able to apply binary search in non-traditional contexts, such as searching in a rotated sorted array or solving problems that require a search space reduction.

#### 6. **Utilize Data Structures Wisely**

* Use appropriate data structures (hash tables, sets, trees, heaps) to solve miscellaneous problems efficiently.
* Recognize when to use advanced data structures like segment trees or Fenwick trees for specific problems involving range queries.

#### 7. **Recursion and Backtracking**

* Be comfortable with recursive approaches, especially for problems that require exploring multiple solutions (like permutations or combinations).
* Use backtracking for constraint satisfaction problems, such as the N-Queens problem or Sudoku solver.

#### 8. **Precomputation and Caching**

* Use precomputation strategies for problems that require repeated calculations. This includes memoization in dynamic programming.
* Identify opportunities to cache results of expensive operations to improve performance.

#### 9. **Practice Common Miscellaneous Problems**

* Solve problems that require unique or creative solutions, such as:
  * Finding the longest increasing subsequence.
  * Solving the coin change problem.
  * Implementing the knapsack problem.
  * Working with intervals, like merging or overlapping intervals.

#### 10. **Performance Considerations**

* Analyze the time and space complexity of your algorithms, especially when working with large data sets or inputs.
* Be mindful of edge cases and constraints that could affect performance.

#### 11. **Debugging Techniques**

* If your algorithm isn’t producing the expected results, break it down into smaller parts and test each part individually.
* Use print statements or debugging tools to trace your algorithm's execution.

#### 12. **Communicate Your Thought Process**

* Clearly articulate your approach and reasoning during interviews. Explain your thought process, especially when you encounter challenges.
* Discuss any assumptions you make and how they impact your solution.

#### 13. **Edge Cases and Constraints**

* Consider potential edge cases, such as empty inputs, maximum input sizes, or constraints that could affect your algorithm's behavior.
* Test your solutions against various input scenarios to ensure robustness.

#### 14. **Refine Your Solution**

* After arriving at a solution, review it for possible optimizations or clearer implementations.
* Discuss how you could improve the efficiency or clarity of your approach.

#### 15. **Key Takeaways for Interviews**

* Be prepared to discuss various algorithm techniques and how they apply to the problems presented.
* If you encounter difficulties, talk through your thought process and consider alternative approaches.

By mastering these principles and practicing various miscellaneous algorithm problems, you'll be well-prepared for relevant questions in your software engineering interviews.

---

## Four Priorities When Writing a Function (in order)

1. **Correctness** — For every valid input the function returns the expected result; no ambiguous behavior.
2. **Time** — Minimize time complexity (choose the right algorithm and data structure).
3. **Space** — Minimize extra memory (in-place when possible; avoid unnecessary copies).
4. **Clarity** — Code should be easy to understand; prefer self-explanatory names and structure.

**Recursion vs iteration:** If both are equally easy to code and have similar complexity, prefer the iterative solution; it avoids stack depth limits and often has better constant factors.

---

## Quick Revision (Miscellaneous)

- **When a problem mixes topics**: Identify the main pattern first (e.g. "it's really a graph" or "it's interval scheduling"), then apply the right DS/algorithm. See [Reference Hub](../../../reference/README.md).
- **Edge cases**: Empty input, single element, duplicates, overflow, negative numbers, zero. Always state them.
- **Interview flow**: Clarify → brute force → optimize → code → test with examples and edge cases → state time/space.

---

## Interview Questions — Logic & Trickiness

Code references (Python): `../../google-sde2/snippets/python/arrays.py`, `../../google-sde2/snippets/python/two_pointers_window.py`, `../../google-sde2/snippets/python/graphs.py`, `../../google-sde2/snippets/python/dp.py`, `../../google-sde2/snippets/python/maths.py`.

Cross-topic problems — **name the underlying pattern** before coding. For each pattern: state **input shape**, **sort key** or **graph model**, then **algorithm** and **complexity**.

| Pattern | Example questions | Trickiness & details |
|---------|-------------------|----------------------|
| **Intervals** | Merge intervals, min arrows to burst balloons, meeting rooms I/II, non-overlapping intervals | **Sort by start** vs **end** changes the greedy; **touching** `[1,2]` vs `[2,3]`—clarify if merge. **Sweep line** + heap for max overlap. |
| **Graph disguised** | Word ladder, snakes and ladders, evaluate division, course schedule | Build **implicit** adjacency; **BFS** for unweighted shortest; **state** may include `(node, extra)` (e.g. stops). |
| **Simulation / matrix** | Rotate image, spiral matrix, game of life (next state), battleships | **Index** boundaries; **direction** array `(dx,dy)`; **in-place** rotation layer-by-layer. |
| **Greedy proof** | Jump game, gas station, task scheduler, assign cookies | **Exchange argument** or **interval** structure; **counterexample** when greedy fails (e.g. DP needed). |
| **Math + implementation** | Random pick with weight, factorial trailing zeros, integer sqrt, super pow | **Mod** arithmetic; **overflow** (`long`, divide before multiply); **precision** (float vs integer). |
| **Design / streaming** | LRU, LFU, rate limiter, moving average | **Amortized** O(1) vs **worst** case; **thread-safety** follow-up for prod. |
| **Bit + array** | Single number, missing number, sum of two integers without +/- | **XOR** cancellation; **sum** vs **xor** assumptions; **overflow** in languages. |

---

## See also

- [README](README.md) — full algorithm topic index  
- [patterns/leetcode-patterns.md](../../patterns/leetcode-patterns.md) — pattern catalog  
- [GOOGLE_INTERVIEW_REVISION.md](../GOOGLE_INTERVIEW_REVISION.md) — revision checklist
