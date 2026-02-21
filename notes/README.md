# Notes

Complete DSA can be divided into 2 parts,

* Data structures&#x20;
* Algorithms&#x20;

In hard/medium problems one needs to combine these two to reach to a solution.

Each part can be furtuer divided into many subparts which has its own problems sets.



#### **Data Structures**

1. **Arrays**
   * Types of Arrays: 1D, 2D, Multi-Dimensional Arrays
   * Operations: Insertion, Deletion, Searching, Traversal, Merging
   * Applications: Matrix operations, Sliding window, Prefix sums
   * Advanced Concepts: Sparse arrays, Dynamic arrays (like `ArrayList` in Java)
2. **Linked Lists**
   * Types: Singly, Doubly, Circular Linked Lists
   * Operations: Insertion, Deletion, Searching, Reversal, Merging
   * Applications: Implementation of stacks, queues, and graphs
   * Advanced: Skip Lists, XOR Linked List (space-efficient linked list)
3. **Stacks**
   * Implementation: Using arrays, linked lists
   * Operations: Push, Pop, Peek, Checking for balance (parentheses), Undo operations
   * Applications: Depth-first search, Expression evaluation (postfix, infix, prefix)
4. **Queues**
   * Types: Simple Queue, Circular Queue, Priority Queue, Double-ended Queue (Deque)
   * Operations: Enqueue, Dequeue, Peek
   * Applications: BFS (Breadth-First Search), Job scheduling, Cache implementations
5. **Trees**
   * Types: Binary Tree, Binary Search Tree (BST), AVL Tree, Red-Black Tree, B-trees, Segment Tree, Trie (Prefix Tree)
   * Operations: Insertion, Deletion, Traversal (Inorder, Preorder, Postorder, Level order)
   * Applications: Searching, Sorting (Heap Sort using Binary Heap), Expression trees, Huffman coding
6. **Heaps**
   * Types: Min Heap, Max Heap
   * Operations: Insertion, Deletion, Heapify, Build Heap
   * Applications: Priority Queues, Dijkstra's algorithm, Heap Sort
7. **Graphs**
   * Representation: Adjacency Matrix, Adjacency List, Edge List
   * Traversal: Depth-First Search (DFS), Breadth-First Search (BFS)
   * Types: Directed, Undirected, Weighted, Unweighted
   * Algorithms: Dijkstra, Bellman-Ford, Floyd-Warshall, A\*, Topological Sort, Kruskal’s and Prim’s algorithms (MST)
8. **Hashing**
   * Hash Functions: Simple, Division Method, Multiplication Method
   * Collision Handling: Chaining, Open Addressing (Linear Probing, Quadratic Probing, Double Hashing)
   * Applications: Hash Maps, Sets, Caches
9. **Advanced Data Structures**
   * **Disjoint Set (Union-Find)**: Union by Rank, Path Compression (used in Kruskal’s Algorithm, cycle detection)
   * **Segment Trees**: Used for range queries (sum, minimum, maximum) and updates
   * **Fenwick Tree (Binary Indexed Tree)**: Efficient updates and queries for cumulative sums

***

#### **Algorithms**

1. **Searching**
   * **Linear Search**: Simple search through each element
   * **Binary Search**: Requires sorted arrays, Divide and Conquer
     * Variations: First/Last occurrence of a number, Searching in a rotated sorted array
   * **Ternary Search**: Division into thirds (useful in unimodal functions)
2. **Sorting**
   * **Comparison-based Sorting**:
     * **Bubble Sort**, **Insertion Sort**, **Selection Sort** (O(n²))
     * **Merge Sort**, **Quick Sort**, **Heap Sort** (O(n log n))
   * **Non-comparison-based Sorting**:
     * **Counting Sort**, **Radix Sort**, **Bucket Sort** (O(n) for small ranges)
   * **Advanced Sorting**: TimSort (used in Python’s sort), External Sorting (for large data)
3. **Dynamic Programming (DP)**
   * Types: Top-down (Memoization), Bottom-up (Tabulation)
   * Famous Problems:
     * Fibonacci Sequence, Longest Common Subsequence (LCS), Longest Increasing Subsequence (LIS)
     * Knapsack Problem, Coin Change Problem
   * Optimization Techniques: Bitmask DP, DP with space optimization (reduce from 2D to 1D arrays)
4. **Greedy Algorithms**
   * Concept: Local optimum leads to global optimum
   * Famous Problems:
     * Activity Selection, Fractional Knapsack, Huffman Encoding
     * Job Sequencing, Dijkstra’s Algorithm (for shortest path in weighted graphs)
5. **Divide and Conquer**
   * Concept: Divide the problem into subproblems, conquer recursively, and combine
   * Famous Problems:
     * Merge Sort, Quick Sort, Binary Search
     * Closest Pair of Points, Karatsuba Algorithm (fast multiplication)
6. **Backtracking**
   * Concept: Explore all potential solutions, backtrack upon failure
   * Famous Problems:
     * N-Queens, Sudoku Solver, Hamiltonian Path, Rat in a Maze
     * Subset Sum Problem, Permutations, Combinations
7. **Recursion**
   * Basic and Advanced Recursion Problems: Towers of Hanoi, Subset generation, Permutations
   * Recursive Tree Problems: DFS-based tree traversal, Diameter of a tree, LCA (Lowest Common Ancestor)
8. **Graph Algorithms**
   * **Shortest Path Algorithms**: Dijkstra’s, Bellman-Ford, Floyd-Warshall
   * **Minimum Spanning Tree (MST)**: Kruskal’s, Prim’s
   * **Flow Algorithms**: Ford-Fulkerson, Edmonds-Karp (for max-flow problems)
   * **Cycle Detection**: DFS-based, Union-Find-based
9. **Bit Manipulation**
   * Operations: AND, OR, XOR, NOT, Shift Operations
   * Applications: Counting set bits, Checking if a number is a power of 2, Swapping numbers
   * Famous Problems: Single Number (finding unique number in an array using XOR), Subset generation using bitmask
10. **Mathematical Algorithms**
    * **Prime Factorization**, **GCD/LCM**, **Sieve of Eratosthenes**
    * Modular Arithmetic, Exponentiation by Squaring, Euclid’s Algorithm
    * **Combinatorics**: Pascal’s Triangle, Catalan Numbers, Binomial Coefficients
11. **String Algorithms**
    * **String Matching**: Naive, KMP (Knuth-Morris-Pratt), Rabin-Karp
    * **Pattern Searching**: Trie-based searching, Aho-Corasick algorithm
    * **Longest Prefix Suffix**: Z Algorithm, Suffix Arrays, Suffix Trees
12. **Miscellaneous Algorithms**
    * **Randomized Algorithms**: Randomized QuickSort, Monte Carlo simulations
    * **Number Theory Algorithms**: Fermat’s Little Theorem, Chinese Remainder Theorem
    * **Game Theory**: Minimax Algorithm, Alpha-Beta Pruning

***

This covers both basic and advanced topics, ensuring you have a well-rounded preparation for Data Structures and Algorithms. Let me know if you’d like to deep dive into any of these topics or need further assistance!
