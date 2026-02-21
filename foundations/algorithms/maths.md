# Mathematics

Maths concepts frequently appear in algorithm problems to optimize naive $O(N)$ loops down to $O(\sqrt{N})$ or $O(1)$. 

## Core Theory & Algorithms
- **Prime Numbers**:
  - *Sieve of Eratosthenes*: Find all primes up to $N$ in $O(N \log \log N)$ time.
  - *Primality Test*: Loop from $2$ to $\sqrt{N}$. If $N$ is divisible by any, it's not prime. Time: $O(\sqrt{N})$.
- **GCD & LCM**:
  - *Euclidean Algorithm*: `def gcd(a, b): return a if b == 0 else gcd(b, a % b)` in $O(\log(\min(a,b)))$ time.
  - *LCM*: `(a * b) // gcd(a, b)`
- **Modular Arithmetic**:
  - $(A + B) \mod M = ((A \mod M) + (B \mod M)) \mod M$
  - $(A \times B) \mod M = ((A \mod M) \times (B \mod M)) \mod M$

## Combinatorics & Probability
- **Permutations**: $N!$ ways to arrange $N$ distinct items.
- **Combinations**: $nCr = \frac{n!}{r!(n-r)!}$ ways to choose $r$ items from $n$.
- **Pigeonhole Principle**: If $N$ items are put into $M$ containers ($N > M$), at least one container must hold $> 1$ item.

## Geometry
- **Distance Formula**: $\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$

## Common SDE-3 Math Problems
- *Easy*: Count Primes, Power of Tree, Roman to Integer, Excel Sheet Column Title.
- *Medium*: Pow(x,n), Factorial Trailing Zeroes, Rotate Image, Max Points on a Line.
- *Hard*: Basic Calculator, Max Points on a Line, Rectangle Area.
