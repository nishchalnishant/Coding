# SDE Interview Click Logic: Pattern Recognition Master Hub

This guide is designed to help you identify the underlying DSA pattern of a problem within the first 60 seconds of an interview. It focuses on **Triggers**—the specific constraints, keywords, and phrases that reveal the solution.

---

## 1. The "Click" by Constraint (Input Size $N$)

If the interviewer gives you constraints, they are the biggest hint.

| Constraint | Expected Complexity | Likely Pattern |
| :--- | :--- | :--- |
| $N \le 10$ | $O(N!)$ | Permutations, Travelling Salesman. |
| $N \le 20$ | $O(2^N)$ | Backtracking, Subsets, Bitmask DP. |
| $N \le 500$ | $O(N^3)$ | Floyd-Warshall, 3D DP, Interval DP (Burst Balloons). |
| $N \le 2000$ | $O(N^2)$ | 2D DP, Nested Loops, Matrix pathfinding. |
| $N \le 10^5$ | $O(N \log N)$ or $O(N)$ | Sorting, Binary Search, Heaps, Two Pointers, Sliding Window. |
| $N \le 10^6$ | $O(N)$ or $O(\log N)$ | Single pass, Greedy, Math, Binary Search. |

---

## 2. The "Click" by Keyword

| If you hear/see... | It almost always means... | Why? |
| :--- | :--- | :--- |
| **"Contiguous subarray"** | Sliding Window / Prefix Sum | Window covers a range; Prefix sum calculates any range in $O(1)$. |
| **"Subsequence"** | Dynamic Programming / LIS | Elements aren't together; you must decide "take or skip" for each. |
| **"Sorted array"** | Binary Search / Two Pointers | Sorting is a gift for $O(\log N)$ or $O(N)$ search/convergence. |
| **"Top K / Frequent"** | Heap / Hash Map | Map counts; Heap maintains the top order dynamically. |
| **"Dependencies / Ordering"** | Topological Sort (DAG) | Node A must happen before Node B. |
| **"Shortest path" (unweighted)** | BFS | BFS explores "layers" equally. First time it hits target, it's shortest. |
| **"Shortest path" (weighted)** | Dijkstra | Priority Queue ensures you always expand the cheapest known node. |
| **"Maximize the minimum"** | Binary Search on Answer | You can guess a "limit" and check if it's feasible (monotonicity). |
| **"All possible ways"** | Backtracking / DP | Backtracking if you need to *list* them; DP if you only need the *count*. |

---

## 3. The "If-Not-X-Then-Y" Logic

Use this to pivot when your first idea is too slow.

*   **If it's an Array problem and $O(N^2)$ is too slow:**
    *   Try **Hash Map** (Trade space for time).
    *   Try **Sorting** first, then Two Pointers.
    *   Try **Sliding Window** (If contiguous).
    *   Try **Prefix Sums**.
*   **If it's a Tree problem and you are stuck:**
    *   Does the answer for the parent depend on the children? $\rightarrow$ **Post-order traversal (Tree DP)**.
    *   Do you need to pass info down? $\rightarrow$ **Pre-order with a state/variable**.
*   **If it's a Graph problem and weights are 1 or 0:**
    *   Don't use Dijkstra. Use **BFS** or **0/1 BFS** (Deque) for $O(V+E)$.
*   **If it's a DP problem and the state is too large:**
    *   Can you reduce 2D to 1D? (Space optimization).
    *   Is there a **Bitmask** hidden? (If $N$ is small).

---

## 4. Mental Models: The "Shift"

How to rephrase complex problems into canonical ones:

1.  **"Meeting Rooms"** $\rightarrow$ Merge Intervals.
2.  **"Word Transformation"** $\rightarrow$ BFS on a graph where words are nodes and one-char difference is an edge.
3.  **"Assigning Tasks to Workers"** $\rightarrow$ Bin Packing (Backtracking/Bitmask) or Flow (Advanced).
4.  **"Collecting Gold in a Grid"** $\rightarrow$ 2D DP Pathfinding.
5.  **"Next Greater Temperature"** $\rightarrow$ Monotonic Stack.

---

## 5. 60-Second Blitz Drill

Before you write a single line of code, ask the interviewer:
1.  **Duplicates?** (Impacts Hash Map/Set logic).
2.  **Sorted?** (Enables Binary Search/Two Pointers).
3.  **Empty/Null?** (Base case for recursion/pointers).
4.  **Memory constraints?** (If $N$ is huge, you can't store everything).
5.  **Negative values?** (Breaks simple sliding window or Dijkstra).
