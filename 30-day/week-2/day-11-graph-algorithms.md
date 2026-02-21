# Day 11: Graph Algorithms

Here are detailed notes for **Day 11: Graph Algorithms**. This day focuses on implementing two fundamental graph algorithms: Dijkstra’s algorithm and the Bellman-Ford algorithm, both of which are used for finding the shortest paths in graphs.

***

#### 1. **Dijkstra’s Algorithm**

Dijkstra’s algorithm is a greedy algorithm used to find the shortest path from a source vertex to all other vertices in a graph with non-negative edge weights.

**1.1 Algorithm Overview**

1. Initialize the distance to the source vertex as 0 and all other vertices as infinity.
2. Create a priority queue (min-heap) to store vertices based on their current shortest distance.
3. While the queue is not empty:
   * Extract the vertex with the minimum distance.
   * For each adjacent vertex, calculate the distance from the source. If it is less than the current known distance, update it and add the vertex to the priority queue.

**1.2 Implementation**

**Using a Min-Heap (Priority Queue)**:

```python
import heapq

def dijkstra(graph, start):
    # Initialize distances and priority queue
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    priority_queue = [(0, start)]  # (distance, vertex)

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # If the popped vertex distance is greater than recorded, skip
        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight

            # Only consider this new path if it's better
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

# Example Usage
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('C', 2), ('D', 5)],
    'C': [('A', 4), ('B', 2), ('D', 1)],
    'D': [('B', 5), ('C', 1)]
}
print(dijkstra(graph, 'A'))
```

**1.3 Time Complexity**

* **Time Complexity**: O((V + E) log V), where (V) is the number of vertices and (E) is the number of edges.
* This complexity arises from the use of a priority queue for selecting the vertex with the minimum distance.

***

#### 2. **Bellman-Ford Algorithm**

The Bellman-Ford algorithm is another algorithm for finding the shortest path from a single source vertex to all other vertices. It can handle graphs with negative edge weights but not negative cycles.

**2.1 Algorithm Overview**

1. Initialize the distance to the source vertex as 0 and all other vertices as infinity.
2. For each vertex, iterate through all edges and update the distance to each adjacent vertex if the new calculated distance is less than the current known distance.
3. Repeat the process for (V-1) iterations (where (V) is the number of vertices).
4. Perform one more iteration to check for negative-weight cycles.

**2.2 Implementation**

```python
def bellman_ford(graph, start):
    # Step 1: Initialize distances
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0

    # Step 2: Relax edges (V - 1 times)
    for _ in range(len(graph) - 1):
        for vertex in graph:
            for neighbor, weight in graph[vertex]:
                if distances[vertex] + weight < distances[neighbor]:
                    distances[neighbor] = distances[vertex] + weight

    # Step 3: Check for negative-weight cycles
    for vertex in graph:
        for neighbor, weight in graph[vertex]:
            if distances[vertex] + weight < distances[neighbor]:
                raise ValueError("Graph contains a negative-weight cycle")

    return distances

# Example Usage
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('C', -3), ('D', 2)],
    'C': [('D', 3)],
    'D': []
}
print(bellman_ford(graph, 'A'))
```

**2.3 Time Complexity**

* **Time Complexity**: O(V \* E), where (V) is the number of vertices and (E) is the number of edges.
* The algorithm requires (V-1) iterations through all edges, making it less efficient than Dijkstra’s algorithm for graphs without negative weights.

***

#### 3. **Comparison of Dijkstra’s and Bellman-Ford Algorithms**

* **Dijkstra’s Algorithm**:
  * Works only with non-negative weights.
  * More efficient for graphs with non-negative weights (O((V + E) log V)).
  * Uses a priority queue.
* **Bellman-Ford Algorithm**:
  * Can handle negative weights but not negative cycles.
  * Less efficient (O(V \* E)) compared to Dijkstra’s for graphs with non-negative weights.
  * Simpler to implement without a priority queue.

***

#### 4. **Applications of Shortest Path Algorithms**

* **Network Routing**: Finding the shortest path for data packets.
* **GPS Navigation**: Calculating the shortest route in maps.
* **Game Development**: Pathfinding for AI characters.
* **Robotics**: Navigation and movement planning.

***

#### 5. **Recommended Practice Problems**

1. **LeetCode**:
   * Number of Islands II (Union-Find approach, but can also use graph algorithms).
   * Cheapest Flights Within K Stops.
   * Shortest Path in Binary Matrix.
2. **HackerRank**:
   * Shortest Reach in a Graph.
   * Roads and Libraries.

***

#### 6. **Key Concepts to Remember**

* Understanding the differences between Dijkstra’s and Bellman-Ford algorithms is crucial for selecting the appropriate one based on edge weights.
* Both algorithms have practical applications in various fields, making them essential for problem-solving in coding interviews and real-world scenarios.
* Familiarity with graph representations and traversal techniques is fundamental when implementing these algorithms.

By mastering Dijkstra’s and Bellman-Ford algorithms, you’ll be well-prepared to tackle shortest path problems in coding interviews.
