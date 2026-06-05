# Constraint Analysis Heuristics `⚡ T1`

> [!tip] The Cheat Code
> If you are completely stuck on a problem, ask the interviewer for the maximum size of the input (`N`). By looking at `N`, you can immediately eliminate 80% of data structures and reverse-engineer the expected Big-O complexity.

In a standard Google coding environment, a solution needs to execute in roughly **$10^7$ to $10^8$ operations per second** to pass within the 1-2 second time limit.

Memorize this table. If the interviewer says $N = 10^5$, you immediately know an $O(N^2)$ brute force will fail ($10^{10}$ operations), and you **must** find an $O(N \log N)$ or $O(N)$ algorithm.

| If `N` is up to... | The Expected Big-O is... | Which means the algorithm is likely... |
|-------------------|--------------------------|----------------------------------------|
| **10 – 15** | $O(N!)$ or $O(N \cdot 2^N)$ | **Backtracking** (Permutations, Subsets), TSP, Bitmask DP. |
| **20 – 30** | $O(2^N)$ | **Backtracking** (Combinations), Meet-in-the-Middle. |
| **100** | $O(N^4)$ or $O(N^3)$ | **3D DP**, Floyd-Warshall (All Pairs Shortest Path). |
| **400 – 1,000** | $O(N^2)$ | **2D DP** (LCS, Edit Distance), Matrix Traversals, Nested Loops. |
| **$10^4$** | $O(N \sqrt{N})$ | **Square Root Decomposition**, Mo's Algorithm (Very rare at L3). |
| **$10^5$** | $O(N \log N)$ | **Sorting**, **Binary Search**, **Heaps/Priority Queue**, Divide & Conquer. |
| **$10^5$ – $10^6$** | $O(N)$ | **Sliding Window**, **Two Pointers**, **Hash Maps**, Stack/Queue, Graph Traversal (BFS/DFS). |
| **$10^9+$** | $O(\log N)$ or $O(1)$ | **Binary Search on Solution Space**, Math tricks, Bit Manipulation. |

## How to use this in the interview:
1. **Interviewer:** *"Given an array of integers..."*
2. **You:** *"Before we dive in, what are the constraints on the length of the array?"*
3. **Interviewer:** *"It can be up to $10^5$."*
4. **You:** (Internally: *Okay, it must be $O(N)$ or $O(N \log N)$. Sliding window, two pointers, or sorting. $O(N^2)$ DP is out of the question.*)
