# Advanced Graph Algorithms

For SDE 3 roles, problems often require knowledge of complex graph topologies, strongly connected components, or sophisticated shortest path algorithms.

## 1. Tarjan's Algorithm for Strongly Connected Components (SCC)
Used to find all strongly connected components in a directed graph.

```python
class Graph:
    def __init__(self, vertices):
        self.V = vertices 
        self.graph = collections.defaultdict(list) 
        self.Time = 0
  
    def addEdge(self, u, v):
        self.graph[u].append(v)
         
    def SCCUtil(self, u, low, disc, stackMember, st):
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
        stackMember[u] = True
        st.append(u)
  
        for v in self.graph[u]:
            if disc[v] == -1:
                self.SCCUtil(v, low, disc, stackMember, st)
                low[u] = min(low[u], low[v])
            elif stackMember[v]: 
                low[u] = min(low[u], disc[v])
  
        w = -1 # To store stack extracted vertices
        if low[u] == disc[u]:
            component = []
            while w != u:
                w = st.pop()
                component.append(w)
                stackMember[w] = False
            print("SCC:", component)

    def SCC(self):
        disc = [-1] * self.V
        low = [-1] * self.V
        stackMember = [False] * self.V
        st = []
        for i in range(self.V):
            if disc[i] == -1:
                self.SCCUtil(i, low, disc, stackMember, st)
```

## 2. Bridges and Articulation Points (Critical Edges/Nodes)
Very common in system design/LLD coding problems acting like "network robustess".

An Articulation Point is a vertex whose removal increases the number of connected components.
A Bridge is an edge whose removal increases the number of connected components.

```python
class BridgeGraph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = collections.defaultdict(list)
        self.Time = 0

    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def bridgeUtil(self, u, visited, parent, low, disc, bridges):
        visited[u]= True
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1

        for v in self.graph[u]:
            if not visited[v]:
                parent[v] = u
                self.bridgeUtil(v, visited, parent, low, disc, bridges)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]: 
                    bridges.append((u, v))
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])
                
    def findBridges(self):
        visited = [False] * (self.V)
        disc = [float("inf")] * (self.V)
        low = [float("inf")] * (self.V)
        parent = [-1] * (self.V)
        bridges = []
        for i in range(self.V):
            if not visited[i]:
                self.bridgeUtil(i, visited, parent, low, disc, bridges)
        return bridges
```

## 3. Disjoint Set Union (Union-Find) with Path Compression and Union by Rank
Essential for Kruskal's MST and solving connected components efficiently.

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # Path compression
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            # Union by rank
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1
            return True # Connected successfully
        return False # Already connected
```

## 4. Other Advanced Graph Concepts
- **A* Search**: Heuristic search for shortest paths (good for maze/grid problems in interviews where Euclidean distance matters).
- **Bellman-Ford / Floyd-Warshall**: For graphs with negative edge weights.
- **Hierholzer's Algorithm**: For finding Eulerian Paths or Circuits (visiting all edges exactly once, e.g., "Reconstruct Itinerary" on LeetCode).
