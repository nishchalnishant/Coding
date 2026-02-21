# CP3

## <mark style="color:blue;">Chapter 1</mark> <mark style="color:blue;"></mark>_<mark style="color:blue;">Competitive Programming 3</mark>_

**1.1 Competitive Programming**

* This section introduces competitive programming, emphasizing its importance and relevance.
* It highlights the benefits of participating in programming contests, such as improving problem-solving skills, coding proficiency, and learning efficient algorithms and data structures.

**1.2 Tips to be Competitive**

*   This section provides seven essential tips for excelling in competitive programming.

    <mark style="color:red;">**1.2.1 Tip 1: Type Code Faster!**</mark>

    * Emphasizes the importance of typing speed in competitive programming.
    * Suggests practicing typing to achieve faster speeds, mentioning a typing test website for improvement.

    <mark style="color:red;">**1.2.2 Tip 2: Quickly Identify Problem Types**</mark>

    * Stresses the importance of recognizing common problem types quickly during contests.
    * Discusses several common types like sorting, searching, graph algorithms, and dynamic programming.

    <mark style="color:red;">**1.2.3 Tip 3: Do Algorithm Analysis**</mark>

    * Encourages understanding the complexity of algorithms to choose the most efficient one.
    * Discusses Big O notation and how to analyze time and space complexity.

    <mark style="color:red;">**1.2.4 Tip 4: Master Programming Languages**</mark>

    * Recommends mastering one or more programming languages commonly used in contests (e.g., C++, Java, Python).
    * Discusses specific language features and libraries that can be advantageous in contests.

    <mark style="color:red;">**1.2.5 Tip 5: Master the Art of Testing Code**</mark>

    * Highlights the importance of testing code thoroughly to avoid runtime errors and incorrect results.
    * Suggests techniques for creating comprehensive test cases.

    <mark style="color:red;">**1.2.6 Tip 6: Practice and More Practice**</mark>

    * Encourages regular practice by solving problems from various online judges and past contest problems.
    * Mentions resources like UVa Online Judge and others for practice.

    **1.2.7 Tip 7: Team Work (for ICPC)**

    * <mark style="color:red;">Offers advice for team-based contests like ICPC, emphasizing the importance of teamwork and collaboration.</mark>
    * Suggests strategies for dividing tasks among team members.

**1.3 Getting Started: The Easy Problems**

*   This section is aimed at beginners, guiding them on how to start solving simpler problems.

    **1.3.1 Anatomy of a Programming Contest Problem**

    * Breaks down the typical structure of a programming contest problem, including the problem statement, input, and output specifications.

    **1.3.2 Typical Input/Output Routines**

    * Discusses common input and output routines in different programming languages.
    * Provides examples of how to handle input and output efficiently in C++, Java, and Python.

    **1.3.3 Time to Start the Journey**

    * Encourages readers to start solving easy problems to build confidence and foundational skills.
    * Recommends specific problems and problem sets to begin with.

**1.4 The Ad Hoc Problems**

* Focuses on a category of problems that don't fit into standard algorithmic categories and often require creative or unorthodox solutions.
* Provides examples and strategies for solving ad hoc problems.

**1.5 Solutions to Non-Starred Exercises**

* Contains detailed solutions to the non-starred exercises presented in the chapter.
* These solutions are intended for self-checking and practice.

**1.6 Chapter Notes**

* Summarizes key points and provides additional notes or references for further reading and exploration.

These notes provide a comprehensive overview of Chapter 1 from _Competitive Programming 3_, focusing on introductory concepts, practical tips for competitive programming, and guidance for beginners starting their problem-solving journey【8:3†source】【8:4†source】.



***

## <mark style="color:blue;">Chapter 2: Data Structures and Libraries</mark>

**2.1 Overview and Motivation**

* **Purpose of Data Structures (DS):**
  * Efficiently store and organize data.
  * Allow efficient insertions, searches, deletions, queries, and updates.
  * Choosing the right DS is crucial for optimal algorithm performance.
* **Context in Competitive Programming:**
  * A strong understanding of DS can mean the difference between passing or failing due to time limits.
  * Different DS can organize the same data in varied ways, impacting efficiency.
* **Importance of Familiarity:**
  * Basic DS from Section 2.2-2.3 are assumed to be known.
  * Built-in implementations are available in C++ STL and Java API.
  * Knowledge of DS strengths, weaknesses, and complexities is essential for problem-solving.

**2.2 Linear Data Structures with Built-in Libraries**

* **Static Array:**
  * Most common DS in programming contests.
  * Used for sequential data accessed by indices.
  * Size is declared based on the problem's maximum input size.
  * Operations: element access, sorting, linear scan, binary search.
* **Dynamically-Resizeable Array (C++ STL vector / Java ArrayList or Vector):**
  * Handles runtime resizing.
  * Preferred when the sequence size is unknown at compile-time.
  * Operations: `push_back()`, `at()`, `[]`, `assign()`, `clear()`, `erase()`, iterators for traversal.
* **Sorting Algorithms:**
  * **O(n²) Comparison-Based:** Bubble, Selection, Insertion Sort (generally avoided).
  * **O(n log n) Comparison-Based:** Merge, Heap, Quick Sort (optimal for contests).
  * C++ STL and Java provide built-in sort functions.

**2.3 Non-Linear Data Structures with Built-in Libraries**

* **Binary Search Tree (BST):**
  * Maintains sorted order, allowing fast search, insert, and delete operations.
  * C++ STL set and map, Java TreeSet and TreeMap implement balanced BSTs.
  * Operations: insertion, deletion, search, and traversal.
* **Heap:**
  * Complete binary tree, maintaining the heap property.
  * Fast insertion and extraction of the maximum (or minimum) element.
  * Used for priority queues.
* **Hash Table:**
  * Provides average O(1) time complexity for insertions, deletions, and lookups.
  * C++ STL unordered\_set and unordered\_map, Java HashSet and HashMap.
  * Operations: insertion, deletion, and search.

**2.4 Data Structures with Our Own Libraries**

* **Graph:**
  * Represented using adjacency lists or matrices.
  * Used for problems involving nodes and edges.
* **Union-Find Disjoint Sets:**
  * Supports union and find operations.
  * Useful for connectivity queries in a network.
* **Segment Tree:**
  * Supports range queries and updates.
  * Efficient for scenarios requiring frequent updates and queries over an interval.
* **Binary Indexed Tree (Fenwick Tree):**
  * Similar use-case to Segment Tree but often simpler to implement.
  * Efficient for cumulative frequency tables.

**2.5 Solutions to Non-Starred Exercises**

* **Approach:**
  * Practice through solving exercises.
  * Understanding the implementation details strengthens comprehension.

**2.6 Chapter Notes**

* **Review and Re-read:**
  * Revisiting the concepts and exercises multiple times helps solidify understanding.
  * Continuous practice is essential for mastery.

By understanding and mastering the various data structures outlined in this chapter, you can enhance your efficiency and effectiveness in solving complex problems in competitive programming contexts.



***

## <mark style="color:blue;">Chapter 3: Problem Solving Paradigms</mark>

**Overview and Motivation**

Chapter 3 discusses four fundamental problem-solving paradigms crucial for competitive programming: Complete Search (Brute Force), Divide and Conquer, Greedy algorithms, and Dynamic Programming. Mastery of these paradigms allows programmers to effectively approach a wide array of problems encountered in contests like IOI and ICPC.

**Key Problems Illustrated:**

1. <mark style="color:red;">**Finding the Largest and Smallest Element:**</mark>
   * **Approach:** Linear scan through the array.
   * **Complexity:** O(n).
2. <mark style="color:red;">**Finding the k-th Smallest Element:**</mark>
   * **Initial Solution:** Repeatedly find and "delete" the smallest element.
   * **Complexity:** O(k \* n) = O(n^2) for k = n/2.
   * **Improved Solution:** Sort the array and pick the k-th element.
   * **Complexity:** O(n log n).
   * **Best Solution:** Expected O(n) using advanced techniques (discussed in Section 9.29).
3. <mark style="color:red;">**Finding the Largest Gap:**</mark>
   * **Initial Solution:** Compare all pairs.
   * **Complexity:** O(n^2).
   * **Improved Solution:** Find the gap between the minimum and maximum elements.
   * **Complexity:** O(n).
4. <mark style="color:red;">**Finding the Longest Increasing Subsequence:**</mark>
   * **Initial Solution:** Check all subsequences.
   * **Complexity:** O(2^n).
   * **Improved Solution:** Dynamic Programming approach.
   * **Complexity:** O(n^2).
   * **Best Solution:** Greedy approach.
   * **Complexity:** O(n log k).

**3.2 Complete Search (Brute Force)**

* **Definition:** Complete search, or brute force, involves traversing the entire search space to find a solution.
* **Usage:** Effective when:
  * No better algorithm is available.
  * The problem size is small enough to allow brute force.

**Advice:**

* **Focus on Thought Process:** Rather than memorizing solutions, focus on understanding the problem-solving strategies.
* **Pruning:** Optimize brute force by pruning unnecessary paths in the search space.

**Complete Search Techniques:**

1. <mark style="color:red;">**Iterative Solutions:**</mark>
   * **One Loop:** Linear scan (e.g., UVa 00102 - Ecological Bin Packing).
   * **Two Nested Loops:** Often used for pairwise comparisons (e.g., UVa 00105 - The Skyline Problem).
   * **Three or More Nested Loops:** For problems requiring multiple levels of iteration (e.g., UVa 00154 - Recycling).
2. <mark style="color:red;">**More Advanced Search Techniques:**</mark>
   * **Backtracking:** Recursive solution with state-space pruning (e.g., UVa 00131 - The Psychic Poker Player).
   * **State-Space Search:** Using BFS or Dijkstra's for complex state management (e.g., UVa 00321 - The New Villa).

**3.3 Divide and Conquer**

* **Definition:** Solving a problem by breaking it into smaller subproblems, solving each subproblem recursively, and then combining their solutions.
* **Key Characteristics:**
  * Efficient for problems that can be split into independent subproblems.
  * Commonly used in sorting algorithms (e.g., merge sort, quicksort).

**3.4 Greedy Algorithms**

* **Definition:** Making a series of choices, each of which looks best at the moment.
* **Key Characteristics:**
  * Locally optimal choices lead to a globally optimal solution.
  * Often simpler and more efficient but not always correct.

**3.5 Dynamic Programming (DP)**

* **Definition:** Solving problems by breaking them into overlapping subproblems and storing the results to avoid redundant computations.
* **Key Characteristics:**
  * Used for optimization problems.
  * Requires identifying the subproblems and the recursive relationship between them.

**Programming Exercises:**

* Exercises provided for each technique to practice and internalize the problem-solving strategies. These include tasks ranging from simple linear scans to more complex backtracking problems with pruning.

**Conclusion:**

* **Versatility and Adaptation:** Competitive programmers must be versatile and adapt different paradigms to tackle diverse problems effectively.
* **Continuous Learning:** Beyond the paradigms discussed, further research into advanced data structures and algorithms is encouraged for continued improvement.

By mastering these paradigms and practicing with the provided exercises, competitive programmers can enhance their problem-solving skills and perform better in contests.





## <mark style="color:blue;">Chapter 4: Greedy Algorithms</mark>

**Overview and Motivation**

Greedy algorithms are a crucial problem-solving paradigm used in competitive programming. They make locally optimal choices at each step with the hope of finding a global optimum. This chapter explores the fundamentals, strategies, and examples of greedy algorithms, providing a solid foundation for understanding and applying them in various problem-solving scenarios.

**4.1 Characteristics of Greedy Algorithms**

* **Local Optimization:** Greedy algorithms make the best choice at each step, aiming for a locally optimal solution.
* **Global Optimality:** The hope is that these local optimizations lead to a globally optimal solution, but this is not always guaranteed.
* **Simplicity and Efficiency:** Greedy algorithms are often simpler and more efficient compared to other paradigms like dynamic programming.

**4.2 Common Greedy Strategies**

1. **Activity Selection:**
   * **Problem:** Select the maximum number of non-overlapping activities.
   * **Approach:** Sort activities by their finish times and iteratively select the next activity that starts after the last selected activity.
   * **Example:** UVa 00531 - Compromise.
2. **Fractional Knapsack Problem:**
   * **Problem:** Maximize the total value of items that can be carried in a knapsack with a weight limit.
   * **Approach:** Sort items by their value-to-weight ratio and take as much as possible of the highest ratio items.
   * **Complexity:** O(n log n) due to sorting.
   * **Example:** UVa 10382 - Watering Grass.
3. **Huffman Coding:**
   * **Problem:** Construct an optimal prefix code for a set of characters with given frequencies.
   * **Approach:** Build a Huffman tree by repeatedly merging the two least frequent nodes.
   * **Complexity:** O(n log n) due to priority queue operations.
   * **Example:** UVa 10020 - Minimal Coverage.
4. **Job Sequencing with Deadlines:**
   * **Problem:** Maximize the total profit of jobs to be completed within given deadlines.
   * **Approach:** Sort jobs by profit in descending order and schedule each job to the latest possible slot before its deadline.
   * **Example:** UVa 10026 - Shoemaker's Problem.

**4.3 Proving Greedy Algorithms Correct**

* **Greedy Choice Property:** The algorithm makes a choice that looks best at the moment.
* **Optimal Substructure:** An optimal solution to the problem contains optimal solutions to subproblems.
* **Mathematical Proofs:** Often required to ensure that a greedy algorithm provides an optimal solution.
* **Counterexamples:** Useful for demonstrating when a greedy algorithm does not yield an optimal solution.

**4.4 Implementing Greedy Algorithms**

* **Sorting:** Many greedy algorithms involve sorting, which usually dominates the time complexity.
* **Priority Queues:** Useful for efficiently finding and extracting the best candidate at each step.
* **Greedy Heuristics:** Heuristics help in designing greedy solutions, though they may not always be provably correct.

**4.5 Greedy Algorithm Problems**

1. **Interval Scheduling Maximization:**
   * **Problem:** Schedule the maximum number of non-overlapping intervals.
   * **Approach:** Select intervals with the earliest finish times.
   * **Example:** UVa 00531 - Compromise.
2. **Optimal File Merge Patterns:**
   * **Problem:** Minimize the total computation time required to merge several files.
   * **Approach:** Use a priority queue to repeatedly merge the two smallest files.
   * **Example:** UVa 10954 - Add All.
3. **Coin Change Problem:**
   * **Problem:** Given a set of coin denominations, find the minimum number of coins needed to make a given amount.
   * **Approach:** Use the largest denomination possible at each step.
   * **Note:** This works only for specific coin systems, such as those where the denominations are multiples of each other.
   * **Example:** UVa 00624 - CD.
4. **Minimum Spanning Tree (MST):**
   * **Problem:** Find a subset of edges that connect all vertices with the minimum total weight.
   * **Approach:** Use Kruskal's or Prim's algorithm, both of which employ greedy strategies.
   * **Example:** UVa 00978 - Lemmings Battle.
5. **Dijkstra’s Shortest Path:**
   * **Problem:** Find the shortest path from a source vertex to all other vertices in a weighted graph.
   * **Approach:** Greedily select the vertex with the smallest known distance at each step.
   * **Example:** UVa 10048 - Audiophobia.

**Conclusion**

Greedy algorithms are powerful tools for solving optimization problems efficiently. While not always guaranteeing an optimal solution, their simplicity and speed make them valuable in many competitive programming scenarios. Understanding the principles, strategies, and common problems associated with greedy algorithms equips programmers with essential techniques for tackling a wide range of challenges.

***

By mastering the content of this chapter, competitive programmers can improve their ability to devise and implement efficient solutions using greedy algorithms. Regular practice with diverse problems helps in recognizing patterns and applying the right strategy effectively.



## <mark style="color:blue;">Chapter 5: Mathematics</mark>

***

**5.1 Overview and Motivation**

* **Mathematics in Competitive Programming**: The importance of mathematics in solving competitive programming problems.
* **Categories**: Problems range from ad hoc mathematics to advanced topics such as combinatorics, number theory, and game theory.

***

**5.2 Ad Hoc Mathematics Problems**

* **Simpler Ones**: Problems solvable with a few lines of code.
* **Mathematical Simulation**: Problems solvable using brute force or iterative methods.
  * Example: Counting numbers less than a given value in a large set.
* **Finding Pattern or Formula**: Problems requiring identification of patterns or formulas for efficient solutions.
  * Example: Determining the number of square integers less than a given number.
* **Grid Problems**: Involving grid manipulation and pattern finding.
* **Number Systems or Sequences**: Involving production or validation of numbers or sequences based on given rules.

***

**5.3 Java BigInteger Class**

* **Basic Features**: Supports operations like addition, subtraction, multiplication, division, and power.
* **Usage Example**: Illustrated through the solution for UVa 10925 - Krakovia, showing the simplicity and clarity of using BigInteger in Java.
* **Performance Note**: BigInteger operations are slower than standard integer operations; prefer built-in types when possible.

***

**5.4 Combinatorics**

* **Fibonacci Numbers**: Series and methods for computation.
* **Binomial Coefficients**: Methods for calculating combinations.
* **Catalan Numbers**: Their significance and computation.
* **Contest Remarks**: Importance of combinatorial problems in contests and typical patterns.

***

**5.5 Number Theory**

* **Prime Numbers**: Algorithms for prime identification and generation.
* **GCD and LCM**: Methods for computing greatest common divisor and least common multiple.
* **Factorial**: Computation and applications.
* **Prime Factorization**: Efficient algorithms for finding prime factors.
* **Modulo Arithmetic**: Operations and properties, including solving linear Diophantine equations with extended Euclid's algorithm.
* **Sieve of Eratosthenes**: Techniques for optimized sieve operations.

***

**5.6 Probability Theory**

* **Basic Concepts**: Analysis of random phenomena and deriving statistical patterns.
* **Monty Hall Problem**: Explanation and derivation of probability in switching doors.
* **Approaches**:
  * **Closed-form Formula**: Deriving solutions using mathematical formulas.
  * **Sample Space Exploration**: Using combinatorics, complete search, or dynamic programming to count events.

***

**5.7 Cycle-Finding**

* **Problem Definition**: Finding the start and length of cycles in sequences generated by functions.
* **Example**: Using pseudo-random number generators to illustrate cycle lengths.
* **Efficient Data Structures**: Methods for solving cycle-finding problems.

***

**5.8 Game Theory**

* **Basic Concepts**: Introduction to game theory in the context of competitive programming.
* **Zero-Sum Games**: Analysis and strategies for games where one player's gain is another's loss.
* **Decision Trees and Minimax**: Techniques for making optimal decisions in games.
* **Nim Game**: A classic example of game theory problem involving strategic moves.

***

These notes provide a concise yet detailed summary of Chapter 5 from "Competitive Programming 3," covering essential mathematical concepts and their applications in competitive programming.





## <mark style="color:blue;">Chapter 6: Graphs</mark>

**Overview and Motivation**

Chapter 6 covers the essential concepts and algorithms related to graphs, which are crucial for solving a wide range of problems in competitive programming. Graphs are versatile data structures that model relationships between pairs of objects, making them applicable in numerous domains.

**6.1 Graph Representation**

* **Adjacency Matrix:**
  * A 2D array used to represent a graph, where `adj[i][j]` is true if there is an edge between vertices `i` and `j`.
  * Suitable for dense graphs.
  * Space complexity: O(V^2), where V is the number of vertices.
* **Adjacency List:**
  * An array of lists used to represent a graph, where each list contains the neighbors of a vertex.
  * Suitable for sparse graphs.
  * Space complexity: O(V + E), where E is the number of edges.
* **Edge List:**
  * A list of all edges in the graph.
  * Useful for algorithms that process edges individually, like Kruskal's algorithm.

**6.2 Traversal Algorithms**

* **Breadth-First Search (BFS):**
  * Explores vertices in layers, starting from a source vertex.
  * Uses a queue to manage the frontier.
  * Useful for finding the shortest path in unweighted graphs.
  * Time complexity: O(V + E).
* **Depth-First Search (DFS):**
  * Explores as far as possible along each branch before backtracking.
  * Uses a stack (or recursion) to manage the frontier.
  * Useful for pathfinding and detecting cycles.
  * Time complexity: O(V + E).

**6.3 Shortest Path Algorithms**

* **Dijkstra's Algorithm:**
  * Finds the shortest path from a source vertex to all other vertices in a weighted graph with non-negative weights.
  * Uses a priority queue to select the next vertex with the smallest tentative distance.
  * Time complexity: O((V + E) log V) with a binary heap.
* **Bellman-Ford Algorithm:**
  * Finds the shortest path from a source vertex to all other vertices, accommodating graphs with negative weights.
  * Iteratively relaxes all edges.
  * Time complexity: O(VE).
  * Detects negative weight cycles.
* **Floyd-Warshall Algorithm:**
  * Computes shortest paths between all pairs of vertices.
  * Uses dynamic programming to update paths iteratively.
  * Time complexity: O(V^3).

**6.4 Minimum Spanning Tree (MST) Algorithms**

* **Kruskal's Algorithm:**
  * Finds the MST by sorting edges by weight and adding them to the MST if they don't form a cycle.
  * Uses a union-find data structure.
  * Time complexity: O(E log E).
* **Prim's Algorithm:**
  * Builds the MST by starting from an arbitrary vertex and repeatedly adding the smallest edge that connects the MST to a new vertex.
  * Uses a priority queue to manage edges.
  * Time complexity: O((V + E) log V).

**6.5 Other Graph Algorithms**

* **Topological Sorting:**
  * Orders vertices in a directed acyclic graph (DAG) such that for every directed edge `uv`, vertex `u` comes before `v`.
  * Uses DFS to determine the order.
  * Time complexity: O(V + E).
* **Strongly Connected Components (SCC):**
  * Identifies maximal subgraphs where every vertex is reachable from every other vertex.
  * Uses Kosaraju's or Tarjan's algorithm.
  * Time complexity: O(V + E).
* **Bipartite Graph Check:**
  * Determines if a graph can be colored with two colors such that no two adjacent vertices share the same color.
  * Uses BFS or DFS.
  * Time complexity: O(V + E).

**Practical Tips for Graph Problems**

1. **Understand the Problem Requirements:**
   * Carefully read the problem statement to identify the type of graph and required properties.
2. **Choose the Right Representation:**
   * Select the appropriate graph representation based on the graph's density and the operations needed.
3. **Optimize Data Structures:**
   * Use efficient data structures like priority queues and union-find to enhance algorithm performance.
4. **Practice Standard Algorithms:**
   * Regularly practice implementing and applying the standard graph algorithms to become proficient.

By mastering these graph concepts and algorithms, competitive programmers can efficiently tackle a wide range of problems involving networks, paths, and connectivity, leading to better performance in contests and real-world applications .



## <mark style="color:blue;">Chapter 7: (Computational) Geometry</mark>

**7.1 Overview and Motivation**

**Computational Geometry in Contests**

* Geometry problems are common in ICPC contests; they often involve either known solutions or require complex algorithms.
* IOI contests have varied in including geometry-specific problems; recent years have seen fewer pure geometry problems compared to earlier years.
* Contestants often avoid geometry problems early in contests due to lower acceptance rates compared to other problem types like Complete Search or Dynamic Programming.

**Challenges with Geometry Problems**

1. **Corner Cases**:
   * Problems often have tricky test cases (e.g., vertical lines, collinear points, concave polygons).
   * Testing with numerous corner cases is essential before submission.
2. **Floating Point Precision Errors**:
   * Even correct algorithms can yield wrong answers due to precision errors.
3. **Tedious Coding**:
   * Solutions usually involve extensive coding, making them less attractive during contests.

**Lack of Preparation**

* Contestants may forget basic formulas or struggle to derive complex ones.
* Inadequate pre-written library functions can lead to multiple bugs during contests.
* Top teams often bring comprehensive geometry formulas and library functions to contests.

**Goals of This Chapter**

* Increase the number of attempts and accepted solutions for geometry problems.
* Provide ideas and strategies for tackling computational geometry problems in ICPCs and IOIs.
* The chapter is divided into two main sections:
  1. **Basic Geometry Objects and Formulas**: Terminologies and formulas for 0D, 1D, 2D, and 3D objects.
  2. **Algorithms on Polygons**: Key algorithms like checking polygon convexity, point-in-polygon tests, cutting polygons, and finding convex hulls.

**7.2 Basic Geometry Objects with Libraries**

**Points (0D Objects)**

* Basic operations and properties involving points, such as distance calculations and transformations.

**Lines (1D Objects)**

* Formulas and algorithms for handling lines, including intersection tests and segment properties.

**Circles (2D Objects)**

* Handling circles, including tangents, intersections, and properties like circumference and area.

**Triangles (2D Objects)**

* Important triangle properties and formulas, such as Heron's formula for area and various circle-related properties (circumcircle, incircle).

**Quadrilaterals (2D Objects)**

* Properties of quadrilaterals, including area calculations and checks for specific types like parallelograms and rectangles.

**7.3 Algorithms on Polygon with Libraries**

**Polygon Representation**

* Methods for representing polygons and handling their vertices.

**Perimeter and Area Calculations**

* Algorithms for computing the perimeter and area of polygons.

**Convexity Checks**

* Algorithms to determine if a polygon is convex or concave.

**Point-in-Polygon Tests**

* Techniques for checking whether a point lies inside a polygon.

**Cutting Polygons**

* Algorithms for cutting a polygon with a straight line and handling the resulting pieces.

**Convex Hull Algorithms**

* Methods like Graham's Scan and others for finding the convex hull of a set of points.

**Implementation Techniques**

* Highlight potential special cases to reduce errors.
* Prefer integer operations to avoid precision issues with floating points.
* Use careful floating point comparisons to avoid equality test errors.

**Exercises and Practical Applications**

* The chapter includes practical exercises to test understanding and application of the concepts and algorithms discussed.

These detailed notes summarize the key points and structure of Chapter 7 from "Competitive Programming 3". For specific details and examples, refer to the full text of the chapter .





## <mark style="color:blue;">Chapter 8: More Advanced Topics</mark>

**Chapter Overview** Chapter 8 of "Competitive Programming 3" delves into advanced techniques and methods for solving complex competitive programming problems. It covers more sophisticated search techniques, dynamic programming (DP) methods, and problem decomposition strategies.

**8.1 Overview and Motivation**

This section introduces the chapter's focus on enhancing problem-solving skills through advanced techniques, providing the motivation for learning and applying these methods to tackle more challenging problems in competitive programming.

**8.2 More Advanced Search Techniques**

1. <mark style="color:red;">**Backtracking with Bitmask**</mark>
   * This technique combines backtracking with bitmasking to efficiently solve problems by representing states with bits.
   * Common use cases include problems where you need to keep track of subsets or combinations of elements.
   * Example Problems:
     * UVa 00131 - The Psychic Poker Player: Uses bitmask to decide which card to retain or exchange, leveraging factorial permutations.
     * UVa 00989 - Su Doku: Solvable with backtracking and bitmask to speed up digit checks.
2. <mark style="color:red;">**Backtracking with Heavy Pruning**</mark>
   * Enhances backtracking by aggressively pruning the search space to avoid unnecessary computations.
   * Example Problem:
     * UVa 00710 - The Game: Implements memoization and pruning to reduce the search space.
3. <mark style="color:red;">**State-Space Search with BFS or Dijkstra’s**</mark>
   * Uses BFS or Dijkstra’s algorithm for state-space search in problems involving paths, movements, or state transitions.
   * Example Problems:
     * UVa 00321 - The New Villa: State represented as a combination of position and a bitmask indicating visited rooms.
     * UVa 01057 - Routing: Uses Floyd-Warshall’s algorithm for all-pairs shortest path information and Dijkstra’s for single-source shortest path.
4. <mark style="color:red;">**Meet in the Middle (Bidirectional Search)**</mark>
   * A strategy that splits the problem into two halves and solves each half from opposite ends, meeting in the middle to combine results.
   * Example Problem:
     * UVa 00985 - Round and Round: Utilizes bidirectional search to find the shortest path with specific rotational constraints.
5. _<mark style="color:red;">Informed Search: A and IDA</mark>_<mark style="color:red;">\*\*</mark>
   * Uses heuristics to guide the search process efficiently, often leading to faster solutions compared to uninformed search methods.
   * Example Problems:
     * UVa 01251 - Repeated Substitution: Solves using BFS informed by problem-specific heuristics.
     * UVa 12135 - Switch Bulbs: BFS on an implicit unweighted graph.

**8.3 More Advanced DP Techniques**

1. <mark style="color:red;">**DP with Bitmask**</mark>
   * Involves using bitmasking to represent states in dynamic programming, allowing for efficient state transitions and memory usage.
   * Example Problem:
     * UVa 10891 - Game of Sum: Implements double DP with bitmasking for optimal game strategies.
2. <mark style="color:red;">**Compilation of Common (DP) Parameters**</mark>
   * Discusses common parameters and techniques used in dynamic programming to optimize state representation and transitions.
3. <mark style="color:red;">**Handling Negative Parameter Values with Offset Technique**</mark>
   * Introduces methods to handle negative values in DP states by offsetting parameters to ensure non-negative indices.
4. <mark style="color:red;">**MLE? Consider Using Balanced BST as Memo Table**</mark>
   * Suggests using balanced binary search trees for memoization to handle memory limitations.
5. <mark style="color:red;">**MLE/TLE? Use Better State Representation**</mark>
   * Encourages finding more efficient state representations to avoid memory and time limit exceed errors.
6. <mark style="color:red;">**MLE/TLE? Drop One Parameter, Recover It from Others**</mark>
   * Describes techniques to reduce the number of parameters in DP states, making the solution more efficient.

**8.4 Problem Decomposition**

1. **Two Components: Binary Search the Answer and Other**
   * Combines binary search with another algorithmic technique to find solutions efficiently.
   * Example Problems:
     * UVa 10917 - A Walk Through the Forest: Involves counting paths in a directed acyclic graph (DAG).
2. **Two Components: Involving 1D Static RSQ/RMQ**
   * Uses range sum queries (RSQ) and range minimum queries (RMQ) for efficient query processing on static arrays.
3. **Two Components: Graph Preprocessing and DP**
   * Combines graph preprocessing (e.g., finding strongly connected components) with dynamic programming for complex problem-solving.
   * Example Problems:
     * UVa 00976 - Bridge Building: Uses flood fill for preprocessing and DP for bridge installation cost computation.
     * UVa 10944 - Nuts for Nuts: BFS followed by TSP and DP.

These advanced topics provide powerful tools and techniques for competitive programmers to tackle harder problems effectively, enhancing their problem-solving skills and algorithmic knowledge





## <mark style="color:blue;">Chapter 9: Rare Topics</mark>

**Overview and Motivation**

* Chapter 9 covers rare and exotic topics in Computer Science that might occasionally appear in programming contests.
* These topics are not frequently encountered, making them less "cost-efficient" for preparation.
* However, knowing these topics can provide a competitive edge when they do appear.

**List of Rare Topics**

1. **2-SAT Problem**
2. **Art Gallery Problem**
3. **Bitonic Traveling Salesman Problem**
4. **Bracket Matching**
5. **Chinese Postman Problem**
6. **Closest Pair Problem**
7. **Dinic’s Algorithm**
8. **Formulas or Theorems**
9. **Gaussian Elimination Algorithm**
10. **Graph Matching**
11. **Great-Circle Distance**
12. **Hopcroft Karp’s Algorithm**
13. **Independent and Edge-Disjoint Paths**
14. **Inversion Index**
15. **Josephus Problem**
16. **Knight Moves**
17. **Kosaraju’s Algorithm**
18. **Lowest Common Ancestor**
19. **Magic Square Construction (Odd Size)**
20. **Matrix Chain Multiplication**
21. **Matrix Power**
22. **Max Weighted Independent Set**
23. **Min Cost (Max) Flow**
24. **Min Path Cover on DAG**
25. **Pancake Sorting**
26. **Pollard’s rho Integer Factoring Algorithm**
27. **Postfix Calculator and Conversion**
28. **Roman Numerals**
29. **Selection Problem**
30. **Shortest Path Faster Algorithm**
31. **Sliding Window**
32. **Sorting in Linear Time**
33. **Sparse Table Data Structure**
34. **Tower of Hanoi**

**Highlighted Topics**

1. **2-SAT Problem**
   * Useful in boolean logic simplification and circuit design.
   * It can be solved in polynomial time using graph theory techniques.
2. **Gaussian Elimination Algorithm**
   * A method for solving systems of linear equations.
   * Involves transforming the system into an upper triangular matrix and then performing back substitution.
   * **Sample Execution:**
     *   Given system:

         ```makefile
         makefileCopy codeX = 9 - Y - 2Z
         2X + 4Y = 1 + 3Z
         3X - 5Z = -6Y
         ```
     *   Transformed system:

         ```
         Copy code1X + 1Y + 2Z = 9
         2X + 4Y - 3Z = 1
         3X + 6Y - 5Z = 0
         ```
     * Matrix form: `A × x = b`
     * Forward elimination and back substitution steps are detailed to find the solution.
3. **Tower of Hanoi**
   * A classic problem involving recursive backtracking.
   * Minimum moves required for n discs is $$2𝑛−12n−1$$.

**Additional Notes**

* Chapter 9 contains 34 rare topics, with 10 rare algorithms highlighted in bold.
* The chapter aims to provide a comprehensive understanding of these rare topics, beneficial for deepening knowledge in Computer Science.
* The topics are diverse, covering areas from graph theory to number theory, from classical puzzles to advanced algorithms.

**Chapter Notes**

* The topics in Chapter 9 may not be part of a standard programming contest syllabus but are valuable for advanced problem solvers.
* The chapter closes with a list of other exotic data structures and algorithms that were not covered due to time constraints, such as Fibonacci heap, various hashing techniques, interval tree, k-d tree, and many more.

By studying these rare topics, competitive programmers can prepare themselves for a wider range of challenges and deepen their understanding of complex algorithms and data structures





