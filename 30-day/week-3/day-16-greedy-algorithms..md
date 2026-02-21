# Day 16: Greedy Algorithms.

Here are detailed notes for **Day 16: Greedy Algorithms**. This day focuses on understanding greedy techniques and applying them to classic problems like activity selection and coin change.

***

#### 1. **Greedy Algorithms Overview**

Greedy algorithms are an approach to problem-solving that builds up a solution piece by piece, always choosing the next piece that offers the most immediate benefit (local optimum). This method does not consider the global consequences of each choice.

**1.1 Key Characteristics**

* **Local Optimal Choice**: Always make the choice that looks the best at the moment.
* **Irrevocable**: Once a choice is made, it cannot be changed.
* **Efficiency**: Often faster and simpler than other algorithms, like dynamic programming.

#### 2. **Common Greedy Problems**

1. **Activity Selection Problem**
2. **Coin Change Problem**
3. **Huffman Coding**
4. **Minimum Spanning Tree (Kruskal’s and Prim’s algorithms)**
5. **Job Sequencing Problem**

#### 3. **Activity Selection Problem**

**3.1 Problem Statement**

Given a set of activities, each with a start and finish time, select the maximum number of activities that don’t overlap.

**3.2 Approach**

1. **Sort Activities**: Sort the activities by their finish times.
2. **Select Activities**: Start with the first activity and iteratively select the next activity that starts after the last selected activity finishes.

**3.3 Implementation**

```python
def activity_selection(activities):
    # Sort activities based on finish time
    activities.sort(key=lambda x: x[1])
    n = len(activities)

    # The first activity always gets selected
    selected_activities = [activities[0]]

    last_finish_time = activities[0][1]
    
    for i in range(1, n):
        if activities[i][0] >= last_finish_time:  # If start time is greater than or equal to last finish time
            selected_activities.append(activities[i])
            last_finish_time = activities[i][1]  # Update the finish time
    
    return selected_activities

# Example Usage
activities = [(1, 3), (2, 5), (4, 6), (6, 7), (5, 8)]
print(activity_selection(activities))  # Output: [(1, 3), (4, 6), (6, 7)]
```

**3.4 Time Complexity**

* **Time Complexity**: O(n log n) due to sorting the activities.
* **Space Complexity**: O(n) for storing the selected activities.

***

#### 4. **Coin Change Problem**

**4.1 Problem Statement**

Given an amount and a list of coin denominations, find the minimum number of coins needed to make that amount.

**4.2 Approach**

1. **Sort Coins**: Sort the coin denominations in descending order.
2. **Greedy Selection**: Start with the largest denomination and keep adding coins until the amount is reached.

**4.3 Implementation**

```python
def coin_change(coins, amount):
    coins.sort(reverse=True)  # Sort coins in descending order
    num_coins = 0
    
    for coin in coins:
        while amount >= coin:  # While the amount is greater than or equal to the coin value
            amount -= coin
            num_coins += 1
            
    return num_coins if amount == 0 else -1  # Return -1 if change cannot be made

# Example Usage
coins = [1, 5, 10, 25]
amount = 63
print(coin_change(coins, amount))  # Output: 6 (2*25 + 1*10 + 3*1)
```

**4.4 Time Complexity**

* **Time Complexity**: O(n), where n is the number of coins, since we potentially iterate through each coin multiple times.
* **Space Complexity**: O(1), as we are not using any additional space beyond a few variables.

***

#### 5. **Other Common Greedy Problems**

* **Huffman Coding**: Used for data compression.
* **Minimum Spanning Tree**: Algorithms like Prim's and Kruskal's find the least expensive way to connect all vertices in a graph.
* **Job Sequencing Problem**: Given jobs with deadlines and profits, find the maximum profit subset of jobs that can be completed by their deadlines.

#### 6. **Practice Problems**

1. **Fractional Knapsack**: Given weights and values of items, maximize the value in the knapsack of a given capacity by taking fractions of items.
2. **Task Scheduling**: Given tasks with start and finish times, find the maximum number of non-overlapping tasks.
3. **Minimum Number of Platforms**: Given arrival and departure times of trains, find the minimum number of platforms required.

***

#### 7. **Tips for Mastering Greedy Algorithms**

* **Understand the Problem**: Make sure the problem fits the greedy paradigm. If optimal substructure and greedy choice properties exist, a greedy solution may work.
* **Proof of Correctness**: Justify why a greedy approach yields an optimal solution.
* **Compare with Other Approaches**: Sometimes, problems can be solved by dynamic programming; understand the trade-offs.

By mastering greedy algorithms and applying them to these classic problems, you'll enhance your problem-solving skills and be better prepared for coding interviews.
