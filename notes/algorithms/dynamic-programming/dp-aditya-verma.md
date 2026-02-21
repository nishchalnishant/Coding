# DP Aditya verma

What it is

* Enhanced recursion
* Identify if question uses recursion
* Recursion happens when we have choices at each step
* So DP is Recursion + storage

DP happens when&#x20;

* If it calls two/multiple function and&#x20;
* has recursion with optimal scenarios (Like maximum or minimum, greatest largest as such)

How to approach

* Find the recursive function, which is to be used
* Then do memoization \[storing result] or top down \[stack]

Different types of DP Problem variation (parent question)

* O-1 knapsack (6 sub problem)
* Unbounded knapsack(5)
* Fibonacci (7)
* LSC (15)
* LIS (10)
* Kadane algorithm (6)
* Matrix chain multiplication (7)
* DP on trees (7)
* DP on Graphs(14)
* &#x20;Others (5)

***

## 0-1 knapsack problems

We have a sack which can store a limit of weight where we have items which has cost and weight associated with that, where we have to pick up the items so that profit is maximum.

* Three types&#x20;
  * Fractional knapsack (greedy)
    * we can have a fraction of an item in our bag, so that we can have a full bag always
    * This is of greedy approach where we can select the maximum one at a instance and get things one&#x20;
  * 0-1 knapsack (DP)
    * an object goes in or not, so we have to choose optimally all the time
  * unbounded knapsack
    * we can have multiple instance of the same object
* Initial steps
  * After reading the question we have to look for two things&#x20;
    * Choice at each step (choice to select or reject)
    * optimal (maximum, minimum etc)
  * After that we do
    * Find recursive solution --> memoization --> Top down
* Code
  * we have to find the recursive code first then do the memoization
  * recursive code&#x20;
    * then start with the base condition
      * to find base condition, think of smallest valid input&#x20;
      * in this case the size of weight, cost and weight is 0
      * then find the answer for that smallest input&#x20;
      * so here,
        * if (n==0) and (wt=0):
          * return 0
    * first start with choice digram&#x20;
      * here the choice digram would be for each object if the weight is more than the weight that can be part of the sack then we don't take that object, else&#x20;
      * we would have two options either to take the object or not based on certain condition such as max(val\[n-1]+knapsack(wt,val,w-wt\[n-1],n-1), knapsack(wt+val, w,n-1)
  * bottoms up approach
    * once we have recursive solution it is easy to create a bottoms up approach
    * for bottoms up we have to change 2 things, we need to store values which are not changing while calling the recursive function
    * and fill it with placeholder values
    * and before calling the recursive function we just need to check in the array if it is present of not, if yes we skip the recursive call if no we fill it with the value.
    * Note — if we look closely for different values of the n and w we get the values of the subproblems  therefore for each values of n and w
  * Topdown approach&#x20;
    * we plan to skip the recursive call all together , we just store the values and skip the recursive call
    * this is best efficient approach but in some question it might not work.
    * to derive the top down approach&#x20;
      * step 1: here also we create a matrix with values which are not change in the recursive calls
      * step 2: initialise the values in the array with random values but initialise the 0th row and 0th column with the case of the base condition
      * now instead of the recursive calls we just have to make it iterative so that we don't have the stack to worry about.
      * so we have to use previous result and run a loop to find out the result of that particular position using the past results
* identification of knapsack problem introduction
  * &#x20;subset sum problem&#x20;
    * is there a subset in an array where the summ is equal to a value
  * initial solution
    * we have a choice for each number so recursion can be used
