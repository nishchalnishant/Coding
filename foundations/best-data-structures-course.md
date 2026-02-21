# Best data structures course

## S01E01 : Algorithms, Time complexity, Merge Sort

* What is an algorithm and how to measure its efficiency?
  * Formal way to solve a problem
  * in most cases it is input data -> algorithm -> output data (intended output)
  * To measure the efficiency of algorithm we use time complexity, which is time spent by the algorithm. We measure this not in seconds but in the number of operations. As different time is taken by different operations.
  * O(n) — here n is the number of operations
    * this means that for all n it would be less than C(g(n)) Upper bound
  * TIme complexity for recursive algorithms&#x20;

{% code fullWidth="false" %}
```python
def f(n):
    if n==0:
        return
    else:
        f(n-1)
```
{% endcode %}

*
