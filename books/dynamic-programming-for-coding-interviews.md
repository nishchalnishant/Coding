---
description: Bottom-up approach to problem solving
---

# Dynamic programming for coding interviews

## Note to self

* Always start from the smallest example and keep increasing them unless you see a pattern.

## <mark style="color:blue;">Preface</mark>&#x20;

* Most DP problems don't need understanding of complex data structure r programming design, they just need right strategy and methodical approach.
* DP problems are not easy to visualize hence not easy to solve.
* Best way to visualize a DP problem is using recursion because DP problems demonstrates optimal substructure behavior.&#x20;
* Recursion gives the right solution but usually takes exponential time, as it solves subproblems multiple times.
* DP is bottom-up approach to problem solving where one subproblem is solved only once.
* In most cases this might seem counter intuitive as it may require a change in the way we approach a problem.

## Recursion&#x20;

In computer programming "When a function calls itself either directly or indirectly it is called a recursive function and the process is called recursion".

Here the solution of a larger problem is defined in terms of smaller instances of itself.

* Recursion always have a terminating condition, like in sum function if n=1 then stop recursion&#x20;
* Recursive function performs some part of the task and delegate rest of it to the recursive call
* Recursive code is a two step process&#x20;
  * Visualize the recursion by defining larger solution in terms of smaller solutions.
  * Add remaining conditions

> When there is a choice between simple and obfuscated code, go for the simpler one unless the other has a performance or memory advantage.

ex -- Tower of hanoi

*   This problem may seem hard but it can be solved in 3 steps&#x20;

    * move n-1 discs from S to E using D
    * Move the nth disc from S to D&#x20;
    * Move n-1 discs from E to D using S



Head recursion and Tail recursion&#x20;

A recursive function typically performs some task and call itself.

* if the call is made before the function performs its own task then it is called head recursion&#x20;
  * ex -- first traverse rest of the linked list then print the value of the current note
*   If the call is made at the end then it is called tail recursion.

    * ex -- print value of current node and move to next one till First traverse.



Most of the times recursion can be complex and may not be simple head or tail recursion.

* ex -- In order traversal -- LVR&#x20;

```python
def inorder(x):
    if(x==NULL):
        return 
    if(x.left!=NULL):
        inorder(x.left)
    print(x.val)
    if(x.right!=NULL):
        inorder(x.right)
```



How to solve problems using recursion&#x20;

* Our focus is to solve the problem with recursion, we can actually code without solving a problem, if we can somehow define the large problem in terms of smaller problems of the same type
* Our focus is on solving the problem for top case and leave the rest for recursive calls to do.
  * For ex -- one can implement bubble sort where can have two loops where we go from go over each pair using for loops and swap the numbers if second one is greater than other.
  * How can we solve using recursion --&#x20;
    * to make it recursive we first need to define the larger problem into smaller subproblems and
    * So here we are finding the greatest of the whole array and placing them in the last position .
    * WE HAVE TWO FUNCTIONS SWAP AND FIND THE GREATEST IN THE EXISTING ARRAY&#x20;





## <mark style="color:blue;">Chapter 2: How it looks in the memory</mark>&#x20;

How memory is divided internally and what part of the program goes in which section of memory

<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption><p>Life cycle of a C language program</p></figcaption></figure>

* When a process is executed first it is loaded into memory (RAM). Area of memory where process is loaded is called process adress space.
* The process adress space has following segments:
  * Code segments
    * Contains machine code of compiled program.
    * It is read only and don't be changed when executing.&#x20;
    * May be shareable so that only a single copy is in memory for different executing programs.
    * Size of code segment is fixed at load time.
  * Data segments
    * All global and static variables are allocated in this segments.
    * Memory is allocated in this area when the program is loading(before the main function is called). That is why global and static variables are also called load time variables&#x20;
    * All load time variables (global and static) are initialized at the load-time. If no initial value is given for a load time variable then it is initialized with zero of its type.
    * Internally this segment is divided in two areas, initialized and uninitialized. If initial value of a variable is given it goes in the initialized area or else it goes in the uninitialized area.
    * All uninitialized variables are initialized by 0 as it can be memset to zero in a single operation.
    * Size of data segment is fixed at load time and does not change when program is executing.
  * Stack segments
    * contains activation records of all the active functions.
    * An active function is a function that is currently under the call.
    * When main is called it is the only active function. The main calls fun1. At this point fun1 is executing but both main and fun1 are active.&#x20;
    * When fun1 calls fun2 then the execution is in fun2 but main, fun1 and fun2 are all active and has their activation record in stack
    * When function fun2 returns, then activation record of fun2 is poped from stack and execution is back in fun1. At this poing amin and fun1 are active and has their activation records in the stack.&#x20;
  * Heap segments&#x20;
    * When we allocate memory at run time using malloc, calloc in c thent hat memory is allocated on the heap.&#x20;
    * It is called dynamic memory or runtime memory
* Recursive vs non recursive inside memory&#x20;



## <mark style="color:blue;">Chapter 3 Optimal substructure</mark>

It means optimal solution to a problem of size n is based on an optimal solution to the same problem of smaller size.

We find optimal solutions of the less elements and combine the solutions to get the final result.

* Problem -- finding shortest path for travelling between two cities by car . B lies in between of those .&#x20;
  * thinking -- we will divide the whole problem into finding smallest distance between two subsequent cities .if we take shortest path for each subsequent cities we will reach A to C using shortest path.  &#x20;
  * So we can write recursive function to find shortest path between any two cities and use it subsequently to find shortest path between two cities.

use of optimal substructure in DP&#x20;

* DP is an important tool for recursive solutions.
* Writing recursive formula or defining the optimal substructure is the first step toward dynamic programming.
* If we can't write a recursive formula for the problem we may not be thinking about using dynamic programming.



## <mark style="color:blue;">Chapter 4 : Overlapping Subproblems</mark>&#x20;

All above problems were singular in nature, we were using recursion but each subproblem was solved only once.

But cases when recursive functions called with exactly same parameters more than once is called **Complex recursion.**

*   Problem: FInd nth term of Fibbonaci series&#x20;

    * Solution : To find 5th fibonacci numnber we need to add n-1 and n-2th fibbonaci number. But if we call the same function for n-2 th term we night call this again and agian which lead us to infinite time&#x20;
    * T(n)=T(n-1)+T(n-2) +O(1)
    * To solve this we memorize the nth fibbonaci number once calulated and use it again&#x20;



    <figure><img src="../.gitbook/assets/image (7).png" alt=""><figcaption><p>We are calculating it again and again </p></figcaption></figure>



OVERLAPPING SUBPROBLEMS -- USE MEMOIZATION

* Problem: there are N stations in a route starting from 0 to n-1.A train moves from first station(0) to last station(n-1) in only forward direction. the cost of ticket between any two stations is given. Find the minimum cost of travel from station 0 to station N-1.
  * Sol: Define data str, we can use 2-d array to store the prove values, or dict. so cost\[i]\[j] is cost of ticket from station i to station j&#x20;
  * So to find minimum cost from i to j we can have j-i choices to make . like
    * if we are going from 2 to 3 then we have 1 option ,&#x20;
      * mincost(2,3)
    * if we are going from 2 to 4 then we have&#x20;
      * min (mincost(2,4) , mincost(2,3)+mincost(3,4))
    * if we are going from 2 to 5 then&#x20;
      * min( mincost(2,5), min( mincost(2,3), min(mincost(3,5),min(mincost(3,4),mincost(4,5)))
      * if we notice we are calculating things again and again, so we need to store this to improve the performance.
      * ![](<../.gitbook/assets/image (8).png>)&#x20;

Note -- A recursive exponential time solution is usually acceptable answer in the interview as they understand that available time is limited.

In a coding competition the recursive solution may not be the way to go forward. In an online competition one may find some of the test cases falling because of the high execution time taken by recursive code (even the solution is right). Also, in the competition the code will be checked against the code of other contestents

P: Given a matrix of order N\*N. What are the toal number of ways in which we can move from top left cell (arr\[0]\[0]) to the bottom right cell (arr\[N-1]\[n-1], given that we can only move either downward or rightward?

sol :&#x20;

* lets say we have array of 1,1. when we are at \[0,0] we have two option to go down or right .
*   lets say we have arr of 2,2 when we are at \[0,0], we have two option to go down or right . so at each node we have option to go down or right unless we are already at the edge . so if we are at the bootom we can't go down , if we are at right most we can only go bottom.

    * optimizing : if we notice we will be at a point for multiple times so we can store the value for reaching from a particular index and we can use it later to optimize.



## <mark style="color:blue;">Chapter 5: Memoization: I wish we could choose which memories to remember.</mark>

In memoization we store the solution of subproblems in some sort of a cache when it is solved for the first time. When the same subproblem is encountered again, then the we use the results returned from the cache.&#x20;

So, Now we will have two types of call to the function, one that does actual computation and hence may call itself recursively and other that just do a look up in the array and return the already stored result. The former is non memorized call and the later one is memorized call.&#x20;

MEMOIZATION = RECURSION + CACHE - RECOMPUTATION



## <mark style="color:blue;">Chapter 6: Dynamic programming</mark>&#x20;

A method for solving a complex problem by breaking it down into a collection of simpler subproblems solving each of those subproblems just once, and storing their solutions ideally using a memory based data structure.

Some authors use Top-Down DP for memoization and Bottom-up DP to describe what we call DP.

In this book, we have used terms memoization and Dynamic programming to refer to top down and bottom up approaches of problem solving where a subproblem is solved only once.

Both Memoization and DP solved individual sub problems only once. Memoization uses recursion and works top-down, whereas Dynamic programming moves in opposite direction solving the problem bottom-up.

DP unroll the recursion and move in opposite direction to memoization.



{% code overflow="wrap" %}
```markup
Top-down approach

Starts with a large input size, reaches the base case, and stores subproblem solutions from the base case to the larger problem. This approach uses the memorization technique, which involves recursion and caching. The space complexity of the top-down approach is O(m * n * min(m * n)), but the time complexity is O(m * n).

Bottom-up approach

Starts with the base case, stores subproblem solutions in a particular order, and then solves larger subproblems using the solutions to the smaller problems. This approach uses the tabulation technique, which involves iteration instead of recursion. The bottom-up approach can sometimes optimize time and space complexity further than the top-down approach
```
{% endcode %}

P: There are N stations in a route starting from 0 to N-1. A train moves from first station(0) to last station(N-1) in only forwards direction. The cost of ticket between any two station is given, Find the minimum cost of travel from station 0 to station N-1.

S: We can solve this in 2 ways&#x20;

* Recursive and memozed version&#x20;
  * recursive version takes exponential time and memory&#x20;
  * Memoized version takes O(n3)
  *   Sol:

      * If minCost(s,d) is minimum cost of travelling from station s to station d. The minimum cost to reach from n-1 to 0 can be redursivly defined as&#x20;
      * mincost(0, n-1) = MIN(cost\[0]\[n-1], cost\[0]\[1] +mincost(1,n-1),mincost(0,2) +mincost(2,N-1),....................minCost(0,N-2) +cost\[N-2]\[n-1]}
      * To solve this using memoization we can store the results which are calulating again and agian to use it again.


* Bottoms up Dp approach&#x20;
  * takesO(n2) time and O(n) extra space
  * This approach is to firrst calculate min cost for station =0 then for station -1 then station -2 and so on. There costs are stored in an one dimensional array minCost\[N].
  * minimum cost to reach station-0 is zero, because we are already there minCost\[0]=0
  * Minimum cost to reach station-1 is cost\[0]\[1], because that is the only way to reach station-1 , minCost\[1]= cost\[0]\[1]
  * minimum cost to reach station 2 is minimum of below two values ( either go directly to station2 or take a break at station -1



```c
int CalculateMinCost(int cost[n][n]){
//minCost[i]=min cost from station -0 to station -i
int minCost[N];
minCost[0]=0;
minCost[1]=cost[0][1];
for (int i=2;i<N;i++)
    { minCost[i]=cost[0][i];
    for (int j=1:j<i;j++)
        if (minCost[i]> minCost[j]+cost[i][j])
            minCost[i]=minCost[j]+cost[i][j];
        }
        return minCost[N-1];
    }
```



P: Find the legnth of longest substring of a given string of digits such that sum of digits in the first half and second half of the substring is same.

Sol: we can think about this from small to large

Brute force sol can be to generate all even strings and calculate the sum of first half and second half  and find longest string which has same sum in forst hald and second half.

* Note:&#x20;
  * The most intutive solution may not always use recursion
  * The most inutive solution may not always take exponential time.
* DP solution
  * Here we build upon the existing solution , sum of digits from index i to j is alreaddy computed , while checking for one substring. Then for another substring(in next loop) we may be computing sum of digits from index i+1 to j. we are computing this sum all over again when we can reusing the sum of digits from i to j and just substract str\[i] from this sum rather than re-computing the sum from i+1 to j( linear time operation)
  * The above solution uses DP and taked O(n2) time and O(n2) extra memory. Clearly there is a scope of improvement in terms of extra memory taken as we are not using lot of space .
  * Try to solve in O(n2) time and O(1) time&#x20;
  * \\



## <mark style="color:blue;">Chapter 7 : Top down vs Bottom-up</mark>

Top down approach --&#x20;

* recursion, memoization
* While defining the solution top down , we define factorial(n) in terms of factorial(n-1) and then put a terminating condition at the bottom.
* more intuitive as we get a birds eye view of a broader understanding of the solution.
* for ex-- to frin the factorial(n) we first call fact(4) which calls fact(3) which calls fact(2) which calls fact(1)&#x20;
* In top Down we have understanding of the destination initally and we develop the means required to reach there.
* first i will take over the world . How will you do that you cay i will take over asia first . How will you take that ? I will take over india first. How will ypu take that? I will become chief minister of delhi.
* In this we have a backlog of computing all the factorials&#x20;
* Example of top down
  * Binary tree algorithms -- preoreder
    * this algorithm starts from the top and moves toward leaves. Most of the binary tree algorithms are like this only.
    * We start from the top, traverse the tree in some order and keep making descisions on the way.

Bottoms-up -- DP

* DP
* In bottoms up we have all the means available and we move toward the destination.
* ex-- one will say i will become CM of delhi. then will take over India then all other countries in asia and finally i will take over the whole world.
* Negatives of bottom up DP
  * In top down approach we don't need to solve all the subproblems. We solve only those problems that need to be solved to get the solution of the main problems
  * In Bottom up dynamic programming all the subproblems are solved before getting to the main problems&#x20;
  * So in some cases we may be solving more subproblems in top down DP than required. The DP solutions should be properly framed to remove this ill efect&#x20;
  * If DP can be ised, thn go for it . It will almost never dissapoint you.

But No matter the approach we will **calculate** the fact(1) first in both cases , in both cases we will begin from becoming the chief minister of Delhi first





## <mark style="color:blue;">Chapter 8 Strategy for DP question</mark>&#x20;



Best strategy

* Practive good practice hard
* More DP problems we solve the easier it gets to relate to a new problem to the one we have already solved and draw parallel between them.
* It is always good to write recursive solution first and tehm optimize it using either DP or memoization depending on the complexity of tthe problem and time available
* DP has two properties&#x20;
  * optimal substructure&#x20;
    * makes recursion an obvious choice to solve DP problem
  * Overlappind sub problems&#x20;

Exaplme

Given two diemsional square matrix cost\[]\[] pf prder m\*n where cost\[i]\[j] represents the cost of passing through cell(i,j). Total cost to reach a particular cell is the sum of costs of all the cells in that path (including the starting and final cell) we can only move either downward or rightward

Basic approach&#x20;

Memoized approach (recirsion\_remember)

Bottom-Up DP solution&#x20;



* Finding if DP is aplicable?
  * Strongest check for DP is to look for optimal substructure and overlapping subproblems
  * DP is used when a complex problem can be divided into subproblems of the same type and these subproblems overlap in some way&#x20;
  * Most of the times we may be trying to optimize something, maximize something, minimize something or finding the total number of ways of doing something and optimal solution for larger parameter depends on optimal solutions of some problems with smaller parameter.
  * Ask yourself
    * is it possible to divide the problems into subproblems of the same type
    * are the subproblems overlapping&#x20;
    * Are we trying to optimize something, maximizing or minimizing something or counting the total number of possible ways to do something.
* Ways to solve DP problems&#x20;
  * See if DP is applicable&#x20;
    * if problem can be defined in terms of smaller subproblems and subproblems overlap then chances are DP can be used
  * **Define recursion** Having subproblems of similar kinds means there is recursion&#x20;
    * **Define problem** in terms of subproblems Define it in a top down manner, Do not worry about time complexity at this point&#x20;
    * **Solve base case** (leave rest to recursion) the subproblems are solved by recursion, what is left is the base case
    * **Add a terminating** condition this step is relatively trivial. We need to stop somewhere . that will be the terminating condition
    * After this step we have a working solution using recursion&#x20;
  * **Try memoization (optional)** if a subproblem is solved multiple times then try to cache its solution and use the cache value when same subproblem is encounterd again
  * **Try Bottom-up** this is the step where we try to eliminate recursion and redefine our solution is forward direction starting from the most basic case. In this process we store only those result that will be required later &#x20;
  * Step 3 is usually for the beginners who are just starting with the concept. It is an improvement over step-2 without getting into the complexity of DP. In interviews, usually the recursive solution isacceptable but the best answer is DP . In the coding competition usually DP is the only accepted solution. With experience one can move to step 4 directly skipping the step3

Problem : Given an empty plot of size 2\*n. we want to place tiles such that the entire plot is covered. Each tile is of size 2\*1 and can be placed either horizontally or vertically. If n is 5 then one way to cover the plot is shown in fig

<figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

Solution&#x20;



Interview tip : It is a good idea in the interview if one can relate the unknown problem to a known problem. One can even tell this to the interviewer. This is a big quality and will in favour.

Problem: If size of the plot in example is changed to 3\*n then what changes do we need ot make in the solution? Picture 8.9 slows one of the possible arrangements on a plot of size 3\*n where n=12



Problem: Consider a game where a player can score 3,5,10 points in one move. Given a total score N find the toal numbe rof unique ways to reach a score of N.

Problem: Given an array of integers, write a function that returns the maximum sum of subarray such that elements are contigous.

Kadane algorithm



## <mark style="color:blue;">Chapter 9 Practice questions</mark>



Problem: EDIT DISTANCE the words computer and commuter are very similar and a update of just one letter p->M will change the first word into the second. Similarly word SPORT can be changed into SORT by deleting one character p or equivalently SORT can be changed into SPORT by inserting P.



* Recursive solution
* Dynamic solution

Problem: TOTAL PATH COUNT Given a two dimensional array find total number of paths possible from top left cell to bottom right cell if we are allowed to move only rightward and downward. For example if matrix is of order 2\*2 then inly two paths are possible



* Recursive&#x20;
* Dynamic

Problem : STRING INTERLEAVING String C is said to be interleaving of string A and B if it  contains all the characters of A and B and the relative order of character of both the strings is preserved in C . For example if values of A,B and C are as given below A=xyz B=abcd C- xabyczd.



* Recursive
* Dynamic

Problem: SUBSET SUM Given an array of non negative integers and a posetive number x determine if there exists a subset of the elements of array with the sum equal to X&#x20;



* recursive
* Dynamic

Problem: LONGEST COMMON SUBSEQUENCE A subsequence of a string S is a set of chrachters that appear in the string in left to tight order but not necessarily consecutively. For example if string is ACTTGG then ACT , ATTC , T are all subsequence but TTA is not a subsequence of the string . Given twi strings write a function that returns the total number of charachters in their longest common subsequence(LCS) in above example the function should return 13&#x20;

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

Recursive&#x20;

Dynamic



Problem: COIN CHANGE PrOBLEM given an infinite supply of N different denominations (values) (v1,v2,v3,..vn) find the minimum number of coins that sum upto a number S&#x20;

Greedy

Recursive

Dynamic

Problem :Cutting a rod Given an iron rod of a certain length and price of selling rods of different lengths in the market , how should we cut the rod so that the profit is maximized.

Recursive

Dynamic

problem 0-1 knapsach problem given n items in a shop where each item has a weight and a value. Achief breaks into the shop with a knapsack. The thief can carry a maximum weight C Items cacnnot be broken or taken partially Each ite has to either picked or left completly what is the maximum value that the thief can carry



Recursive

Dynamic



PROBLEM: Longest palindrome subsequence A subseqquence of a string is the subsequence of charachters in the samme relative order as they appear in the original string .&#x20;

Recursive

Dynamic

Problem: Dropping eggs puzzle We have two iddentical eggs and access to a 100 floor building. we don't know how string the eggs are eggs can be really strong and may not break even when dropped from 100th floor or they may be fragile and break if dropped from first floor . we want to find out the highest floor from where the eggs can be drroped but we have only&#x20;



