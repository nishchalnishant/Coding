# Greedy Algorithms

A problem-solving approach that makes the **locally optimal choice** at each step with the hope that this sequence of local optimizations leads to a **globally optimal solution**.

## Key Concepts
- **Greedy Choice Property**: A global optimum can be reached by selecting the local optimum at every step.
- **Optimal Substructure**: An optimal solution to the problem contains optimal solutions to its subproblems.
- **Irrevocable**: Once a choice is made, the algorithm never goes back to reconsider it (unlike Backtracking / DP).

## Common Patterns
- **Sorting First**: Most greedy problems require sorting the input array first (e.g., sort intervals by start/end time, sort items by weight/value ratio) so you can make local optimal choices sequentially.
- **Priority Queue / Max Heap**: Use a heap to always pull the highest-value or lowest-cost item dynamically as the state changes.

## Classic SDE-3 Greedy Problems
- *Easy*: Assign Cookies, Array Partition I, Largest Perimeter Triangle, Minimum Operations to Make the Array Increasing.
- *Medium*: Jump Game, Jump Game II, Gas Station, Task Scheduler, Non-overlapping Intervals, Minimum Number of Arrows to Burst Balloons.
- *Hard*: Minimum Number of Refueling Stops, Reaching Points, Candy.

## Greedy vs. Dynamic Programming
If you need to explore *all possible paths* or choices have overlapping future implications that are complex, use **Dynamic Programming**. If you can *prove* that picking the "best looking" immediate option will never hurt the final result, use **Greedy**. Note that DP can solve Greedy problems, but Greedy algorithms are usually much faster ($O(N \log N)$ or $O(N)$ vs DP's $O(N^2)$).
