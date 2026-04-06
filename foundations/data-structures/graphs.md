# Graphs

#### **Striver**

**Graph traversal**

* breadth first search&#x20;
  * The graph itself is stored in the adjacency list ( we will be getting the adjacency list, no need to do it on our own)
  * to do bfs we need two other data structures
    * queue data structure — starting node should be here
    * visited data structure — array which stores the visited node
  * Next what ever is in the queue start taking it out and  get the neighbours of that node from the adjacency list and append them in the queue data structure and mark it as 1 in the visited data structure
  * Next time pop the first element and repeat the above exercise
  * &#x20; **questions** -
    * **Number of islands/ number of connected components**
      * grid of size n\*m where 0 is water and 1 is land, we have to find out the connected components&#x20;
      *

          <figure><img src="../../.gitbook/assets/image (11).png" alt="" width="375"><figcaption></figcaption></figure>


      *   It is clear from the above image that:

          * row can be row-1, row, row+1. Or deltaRow varies from -1 to 1.
          * col can be col-1, col, col+1. Or deltaCol varies from -1 to 1.


      *   Therefore, to effectively traverse all the neighbours, two loops can be used.

          #### Approach:

          1. Determine the dimensions of grid. Create a 2D visited array and initialize all values as false. Initialise a counter for the number of islands.
          2. Loop through each cell in the grid. If the cell is land and not yet visited, it signifies the start of a new island.
          3. Use BFS to explore all connected land cells starting from this cell and mark them visited.Increase the island count after completing the BFS for the current island.
    * **Flood fill algorithm**&#x20;
      * can be solved using bfs and dfs
      *

          <figure><img src="../../.gitbook/assets/image (12).png" alt="" width="375"><figcaption></figcaption></figure>


      * #### Approach:
        1. Initialise a new image to store the image after flood fill. (The given image can be used for the same but it is considered a good practice if the given input is not altered.)
        2. To navigate to the neighboring pixels, direction vectors are defined for moving up, right, down, and left. A helper function checks if a pixel is within the bounds of the image. This ensures that the traversal does not go out of the image boundary.
        3. Starting from the given pixel, a recursive DFS traversal is performed during which all the pixels having same initial color are marked with new color in the new image.
        4. Once the traversal terminates, the new image stores the flood filled image.
    *   **Rotten oranges**



        *   #### Intuition:



            * The idea is that for each rotten orange, the number of fresh oranges that are there its 4 directions can be found. With the passing of every minute, these fresh oranges will be rottened which will further rotten other fresh oranges in contact.
            * Consider each minute as level, where all the oranges will be rotten at once. Keeping this in mind, a level order traversal (BFS) can be performed making sure at each level, the fresh oranges in contact with the already rotten oranges gets rotten.
            * The number of levels for which the BFS is performed will denote the time taken by all oranges to rotten.
            * **How to identify if all the oranges are rotten or not?**
              * For this, a count can be maintained for the oranges that gets rotten after the traversal is complete. And a total count of oranges can be found by traversing the grid.
              *   If the total count matches with the count of rotten oranges, it can be concluded that all the oranges were rotten.


              * #### Approach:
                1. Determine the dimensions of grid. Variables are initialised to track time, total number of oranges, and the count of rotten oranges. A queue is taken for BFS traversal that will store the coordinates of the rotten oranges at that current level.
                   1. Traverse the grid and update the count of total oranges. If any cell containing rotten orange is found, add it to the queue.
                      1. Perform BFS to spread Rot. Continue until the queue is empty and for each level (each minute)
                         * Record the size of the queue, which represents the number of rotten oranges at that moment. And update the count of rotten oranges by adding the size of the queue.
                         * Process each rotten orange, by removing it from the queue, marking its four fresh oranges (if any) as rotten and adding them to the queue.
                         * If new oranges are marked rotten during this process, increment the time.
                      2. After processing, if the count of rotten oranges matches the total number of oranges, return the time taken. If not all oranges are rotten, return -1 to indicate it's not possible to rot all oranges.
    *   **Surrounded regions**



        *   #### Intuition:



            * An important thing to note is that the boundary elements in the matrix cannot be replaced with 'X' as they are not surrounded by 'X' from all 4 directions. This means if 'O' (or a set of 'O') is connected to a boundary 'O' then it can't be replaced with 'X'.<br>
            * Thus, to solve this problem efficiently, traversal can be started from the boundary 'O's. All the 'O's encountered during traversal will not be surrounded by 'X's in all 4 directions which can be marked as visited.<br>
            *   Once all the traversals are completed, the 'O's that are not marked as visited in the matrix will represent the 'O's that are completely surrounded by 'X's. For the particular problem, either of the traversal techniques can be used.


            * #### Approach:
              1. Initialise two lists to help navigate through the four possible directions (up, right, down, left). Define a function to check if a cell is within the matrix boundaries.
                 1. Implement a recursive function for DFS traversal of connected 'O' cells. Mark the current cell as visited. Explore the four possible neighbouring cells. If a neighbouring cell contains 'O' and is not visited, recursively apply the traversal function on it.
                 2. For the main driver function, traverse the boundaries to find unvisited 'O' cells and start the DFS traversal from those cells. Mark each cell as visited during the traversal.
                 3. After processing boundary cells, traverse the entire matrix and convert all unvisited 'O' cells to 'X' as they are surrounded by 'X'.
    * Number of distinct islands
    * Bipartite graphs
    * Topological sort or kahn's algorithm
    * Find evential safe states
  * DFS --
    * Uses stack
    * has visited list which has info of all the visited nodes.
  * Other graph questions&#x20;
    * course schedule 1 and 2 --
      * Form a graph and check if cycle is present if yes then we can't if no then we can \[ we can check cycle using a dfs]
      * OR we can do a topological sort of the pairs and we can do this.
      * we will use the fact a topological sort\[using bfs] is possible only if there isn't any cycle. so if we are able to do a topological sort then yes if w can't do a topological sort then no we can't
      *   **How this problem can be identified as a Graph problem?**



          * The problem suggests that some courses must be completed before other courses.&#x20;
          * This is analogous to Topological Sort Algorithm in graph which helps to find a ordering where a node must come come before other nodes in the ordering.\
            Hence, the courses can be represented as nodes of graphs and dependencies of courses can be shown as edges.<br>
          *   Now, For the graph formed, if the Topological sort can be found containing all the nodes (courses), all the courses can be completed in the order returned by topological sort. Else it is not possible to complete all the courses.


          *   **How to form the graph?**

              The pair `[a,b]` represents that the **Course b** must be completed before **Course a**.\
              Hence in the graph, two nodes representing **Course a** and **b** can be created with a directed edge from **Node b** to **Node a**. This way the topological sort will return **Node b** before **Node a**.

              #### Approach:

              1. Using the dependencies of courses, prepare a directed graph.
                 1. Get the topological ordering of the graph formed.
                 2. If the topological ordering contains all nodes, all the courses can be completed in that order.
                 3. Otherwise, it is not possible to completed all the courses.

              <br>
    * Alien dictionary \[ this can be solved using topological sort as we have an ask of something before something]
      *   #### Intuition:

          **How this problem can be identified as a Graph problem?**

          The problem suggests that there exists the ordering of different words based on the alien dictionary. Also, it is asked to find out the ordering of letters based on the dictionary. The concept of ordering of nodes can be solved using Topological sort which comes under the topic of Graphs.<br>

          **How to form the graph?**

          Here, the letters can be represented as nodes of the graph.\
          \
          To understand the edges, consider example 1 where\
          `N=5, K=4, dict = {"baa", "abcd", "abca", "cab", "cad"}`\
          \
          Considering the first two words "baa" and "abcd", it is clear that they are differentiated by the first letter i.e. 'b' and 'a'. Thus, a directed edge can be inserted in the graph from node 'b' to node 'a' representing that letter 'b' must appear before the letter 'a' in the ordering as shown in the figure:
      *

          <figure><img src="../../.gitbook/assets/image (13).png" alt=""><figcaption></figcaption></figure>


      *   By comparing pairs of words in the dictionary, edges can be added to the graph.

          **Note:**

          It is not required to check every pair of words possible to add the edges to the graph. Instead just checking the differentiating letter in consecutive pairs will work as well as shown in the image:
      *

          <figure><img src="../../.gitbook/assets/image (14).png" alt="" width="375"><figcaption></figcaption></figure>


      *   **Edge Case:**

          The problem arises when the value of K becomes 5 and there is no word in the dictionary containing the letter 'e'. In this case, a separate node with the value 'e' can be added in the graph and it will be considered a component of the directed graph like the following, and the same algorithm will work fine for multiple components.\
          ![](https://takeuforward.org/plus/dsa-concept-revision/graph-iii/alient-dictionary?tab=editorial)

          #### Approach:

          1. Initialise a graph with nodes equal to the number of required letters. The letters from 'a' to 'z' can be represented as numbers from 0 to 26 for easier understanding.
          2. Compare the consecutive pair of words, and find the differentiating letter. Compare the letters to add an edge to the graph.
          3. Once the graph is prepared, get the topological ordering of the graph formed.
          4. The ordering of letters obtained from the topological sorting, will be the ordering of letters based on the alien dictionary.









**Detailed Summary of Graphs (Data Structures)**

A **Graph** is a non-linear data structure that consists of a set of vertices (or nodes) connected by edges. Graphs are used to model relationships between pairs of objects, making them incredibly useful in various real-world applications such as social networks, navigation systems, recommendation systems, etc.

**Key Concepts:**

1. **Graph Terminology**:
   * **Vertex (Node)**: A fundamental unit of a graph.
   * **Edge**: A connection between two vertices. It can be **directed** (one-way) or **undirected** (two-way).
   * **Adjacency**: Two vertices are adjacent if they are connected by an edge.
   * **Degree**: The number of edges connected to a vertex. In directed graphs, the **in-degree** is the number of incoming edges, and the **out-degree** is the number of outgoing edges.
   * **Path**: A sequence of edges that connect a sequence of vertices.
   * **Cycle**: A path that starts and ends at the same vertex.
   * **Connected Graph**: A graph where there is a path between every pair of vertices.
   * **Disconnected Graph**: A graph that contains at least one pair of vertices with no path between them.
   * **Acyclic Graph**: A graph with no cycles. A **Directed Acyclic Graph (DAG)** is a directed graph with no cycles.
2. **Types of Graphs**:
   * **Directed Graph**: Edges have a direction, indicated by an arrow. The edge from vertex `A` to vertex `B` is not the same as an edge from `B` to `A`.
   * **Undirected Graph**: Edges do not have a direction; an edge from `A` to `B` is the same as an edge from `B` to `A`.
   * **Weighted Graph**: Each edge has a weight (or cost) associated with it, used in applications like finding the shortest path.
   * **Unweighted Graph**: Edges are uniform, without associated weights.
3. **Graph Representation**:
   * **Adjacency Matrix**: A 2D array where the element at index `(i, j)` is non-zero if there is an edge from vertex `i` to vertex `j`.
   * **Adjacency List**: An array of lists where the index represents the vertex, and the list at that index contains all adjacent vertices.
   * **Edge List**: A list of all edges, where each edge is represented as a pair of vertices (and optionally a weight).
4. **Graph Traversal Techniques**:
   * **Depth-First Search (DFS)**: Starts at a node and explores as far as possible along each branch before backtracking. It uses recursion or a stack.
   * **Breadth-First Search (BFS)**: Starts at a node and explores all neighbors before moving to the next level of neighbors. It uses a queue and is useful for finding the shortest path in unweighted graphs.
   * **Topological Sort**: An ordering of vertices in a directed acyclic graph (DAG) where for every directed edge `(u, v)`, vertex `u` appears before `v` in the ordering.
5. **Graph Algorithms**:
   * **Dijkstra's Algorithm**: Finds the shortest path from a source node to all other nodes in a weighted graph (works with non-negative weights).
   * **Bellman-Ford Algorithm**: Finds the shortest path from a source node to all other nodes, and handles graphs with negative weight edges.
   * **Floyd-Warshall Algorithm**: A dynamic programming approach for finding the shortest paths between all pairs of vertices.
   * **Prim’s and Kruskal’s Algorithms**: Used to find the Minimum Spanning Tree (MST), a subset of edges that connects all vertices without cycles and with the minimum possible total edge weight.
   * _A Search_\*: A pathfinding and graph traversal algorithm often used in gaming and AI. It uses heuristics to find the shortest path efficiently.
6. **Applications of Graphs**:
   * **Social Networks**: Representing people as nodes and relationships as edges.
   * **Maps and Navigation**: Cities are nodes, and roads are edges with weights representing distances.
   * **Recommendation Systems**: Items or users are nodes, and connections represent preferences or interactions.
   * **Network Flow**: Graphs are used to optimize the flow of goods, information, or data in networks.
   * **Dependency Management**: Directed acyclic graphs are used to represent dependencies in tasks, such as in build systems or project management (e.g., task scheduling).
   * **Web Page Ranking**: Search engines like Google use graphs to rank pages using algorithms like PageRank.

***

#### **List of Important Questions for Graphs**:

**Easy:**

1. **Implement DFS and BFS for a graph**.
2. **Find if there is a path between two vertices in a graph**.
3. **Check if a graph is connected**.
4. **Detect a cycle in a directed or undirected graph**.
5. **Find the number of connected components in an undirected graph**.
6. **Find the shortest path in an unweighted graph using BFS**.
7. **Check if a graph is bipartite**.

**Medium:**

1. **Topological sorting of a directed acyclic graph (DAG)**.
2. **Find the shortest path from a source to all vertices using Dijkstra’s algorithm**.
3. **Find the shortest path from a source in a graph with negative weights using Bellman-Ford**.
4. **Prim’s and Kruskal’s algorithms for finding the Minimum Spanning Tree**.
5. **Floyd-Warshall algorithm for finding all pairs shortest paths**.
6. **Clone a graph (deep copy)**.
7. **Find strongly connected components in a directed graph using Kosaraju’s algorithm**.
8. **Find the critical connections (bridges) in a graph**.

**Hard:**

1. **Solve the traveling salesman problem (TSP)** using dynamic programming or branch and bound.
2. **Find the maximum flow in a flow network using the Ford-Fulkerson algorithm**.
3. **Find articulation points (cut vertices) in a graph**.
4. **Solve the word ladder problem using BFS**.
5. **Implement a PageRank algorithm for ranking web pages**.
6. _A Search algorithm for finding the shortest path in weighted graphs_\*.
7. **Find Eulerian and Hamiltonian paths in a graph**.
8. **Optimize scheduling problems using graphs and topological sorting**.

***

These questions cover fundamental and advanced graph concepts, including traversal techniques, shortest path algorithms, minimum spanning trees, and real-world applications like network flow and dependency resolution. This set will help you understand and apply graph theory to a variety of problems. Let me know if you'd like explanations or solutions for specific questions!







Here are some useful tips and tricks for solving graph problems in software engineering interviews:

#### 1. **Understand Graph Representation**

* Know the two primary ways to represent a graph:
  * **Adjacency Matrix**:&#x20;
    * A 2D array where `matrix[i][j] = 1` means there’s an edge between node `i` and node `j`. Useful for dense graphs.
    * not good for larger arrays as it might create a sparse matrix.&#x20;
  * **Adjacency List**:&#x20;
    * An array of lists where each list contains the neighbors of a node. This is more space-efficient for sparse graphs.
* Make sure you’re familiar with both directed and undirected graphs, as well as weighted and unweighted graphs.

#### 2. **Graph Traversal Techniques**

* **Depth-First Search (DFS)**:
  * DFS explores as far as possible along each branch before backtracking.
  * It can be implemented recursively or iteratively using a stack.
  * Useful for pathfinding, detecting cycles, and exploring connected components.
* **Breadth-First Search (BFS)**:
  * BFS explores neighbors level by level, using a queue.
  * It’s commonly used for shortest path problems in unweighted graphs, finding the minimum number of steps, or solving problems like **connected components**.

#### 3. **Detecting Cycles**

* **In undirected graphs**, a cycle can be detected using DFS by checking if a node is revisited (ignoring the parent node).
* **In directed graphs**, cycle detection can be done using DFS and checking the back edges, or using **Kahn's Algorithm** for topological sorting.

#### 4. **Topological Sorting**

* **Topological sort** is used for ordering nodes in a directed acyclic graph (DAG). It’s often applied in scheduling problems, dependency resolution, or course prerequisites.
* You can implement topological sort using either DFS (by adding nodes to a stack in post-order) or BFS (Kahn’s Algorithm).

#### 5. **Dijkstra’s Algorithm**

* **Dijkstra’s Algorithm** finds the shortest path from a source to all other nodes in a graph with non-negative edge weights.
* It uses a **min-heap (priority queue)** to always expand the least-cost node first.
* Make sure you’re familiar with the implementation, especially the use of the priority queue to efficiently get the next node with the smallest distance.

#### 6. **Bellman-Ford Algorithm**

* The **Bellman-Ford Algorithm** handles graphs with negative weights. It’s slower than Dijkstra’s (O(VE)) but can detect negative cycles, which Dijkstra’s cannot.
* It’s useful for problems where negative weight edges are present.

#### 7. **Floyd-Warshall Algorithm**

* **Floyd-Warshall** is an all-pairs shortest path algorithm that works with negative weights but no negative cycles.
* It’s O(V³) in complexity, so it’s best for smaller graphs or for finding the shortest path between all pairs of nodes.

#### 8. **Union-Find (Disjoint Set Union - DSU)**

* **Union-Find** is useful for solving connectivity problems, such as detecting cycles in undirected graphs or finding connected components.
* Make sure you understand the concepts of **union by rank** and **path compression**, which optimize the data structure.
* Union-Find is also essential for **Kruskal’s Algorithm** for finding the minimum spanning tree (MST).

#### 9. **Minimum Spanning Tree (MST)**

* **Kruskal’s Algorithm**: A greedy algorithm that uses sorting and the Union-Find data structure to construct the MST by adding the smallest edges, ensuring no cycles are formed.
* **Prim’s Algorithm**: Another greedy algorithm that grows the MST by selecting the smallest edge that connects the current tree to a new vertex. It uses a priority queue (min-heap) to find the minimum edge efficiently.

#### 10. **Strongly Connected Components (SCCs)**

* For **directed graphs**, strongly connected components can be identified using **Kosaraju’s Algorithm** or **Tarjan’s Algorithm**.
* These algorithms are useful in problems where you need to identify maximal subgraphs where every node can reach every other node within the subgraph.

#### 11. **Bipartite Graph Check**

* A **bipartite graph** can be checked by using BFS or DFS to try and color the graph with two colors. If at any point, two adjacent nodes have the same color, the graph is not bipartite.
* This is commonly asked in problems related to scheduling or partitioning tasks into two groups.

#### 12. **Handling Weighted Graphs**

* For problems with **weighted edges**, Dijkstra’s or Bellman-Ford will typically be required to compute shortest paths.
* Make sure you understand how to handle negative weights and how to modify algorithms (like using a priority queue in Dijkstra’s).

#### 13. **Grid and Maze Problems**

* Many graph problems involve grids (e.g., shortest path in a maze).
* You can treat each cell in a grid as a node, and neighboring cells (up, down, left, right) as edges.
* Use BFS for shortest path problems on grids, and DFS for exploring or backtracking paths.

#### 14. **Graph Coloring and Path Problems**

* Problems involving **graph coloring** (like the **m-coloring problem**) are often solved using **backtracking**.
* For problems involving finding paths or cycles (like **Hamiltonian paths** or **Eulerian paths**), DFS is often combined with backtracking to explore all possible routes.

#### 15. **Key Practice Problems**

* **Shortest Path**: Use BFS for unweighted graphs, Dijkstra’s for non-negative weights, and Bellman-Ford for graphs with negative weights.
* **Topological Sort**: For dependency resolution problems or DAG scheduling.
* **Minimum Spanning Tree (MST)**: Prim’s and Kruskal’s algorithms.
* **Cycle Detection**: In both directed and undirected graphs.
* **Connected Components**: DFS or Union-Find for finding all connected components.
* **Bipartite Graph Check**: BFS or DFS to check for two-colorability.

#### 16. **Communicate Clearly During Interviews**

* Clearly explain your choice of traversal (BFS, DFS) or algorithm (Dijkstra, Union-Find, etc.).
* Mention edge cases such as disconnected components, self-loops, or parallel edges.
* Discuss time complexity (e.g., Dijkstra’s O((V + E) log V) or DFS O(V + E)) and space complexity.

By mastering these techniques and practicing a variety of graph problems, you'll be well-prepared for graph-related questions in interviews.

---

## Pattern Recognition (SDE-3)

- **Shortest path unweighted** → BFS (level = distance). Multi-source: enqueue all sources (e.g. Rotting Oranges).
- **Components / cycle / path** → DFS. Topological order → DFS post-order reverse or Kahn's (in-degree BFS).
- **Dependencies / "A before B"** → Build directed graph, then topological sort (Course Schedule, Alien Dictionary).
- **Shortest path weighted** → Non-negative: Dijkstra (min-heap). Negative: Bellman-Ford. All-pairs: Floyd-Warshall.
- **MST / connectivity** → Kruskal (sort edges + Union-Find) or Prim (heap). Union-Find for "are u and v connected?".

## Interview Strategy

- **Identify**: "Shortest path" → BFS (unweighted) or Dijkstra/Bellman-Ford (weighted). "Order" / "before" → topo sort. "Connected" → DFS or Union-Find.
- **Approach**: Choose representation (usually adjacency list). State time/space (e.g. BFS O(V+E)). Handle disconnected, self-loops, multiple edges.
- **Common mistakes**: Forgetting visited set; using Dijkstra with negative weights; assuming graph is connected; wrong direction of edges in dependency graph.

## Quick Revision

- **BFS**: Queue + visited; level = shortest distance in unweighted. **DFS**: Stack/recursion; for topo, push in post-order then reverse.
- **Dijkstra**: Min-heap (dist, node); relax neighbors; first extraction = final distance. **Kruskal**: Sort edges, add if Union-Find union succeeds.
- **Topo**: Kahn = in-degree 0 queue; or DFS post-order reverse. **Edge cases**: Disconnected, cycle (no topo), single node.

---

## See also

- [Graph algorithms](../algorithms/graph.md) — compact SDE-3 reference with pseudocode  
- [Union Find](../algorithms/union-find.md) — DSU for Kruskal and connectivity  
- [advanced-graphs.md](../../advanced-dsa/advanced-graphs.md) — Tarjan, bridges
