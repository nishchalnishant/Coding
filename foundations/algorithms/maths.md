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
- *Easy*: Count Primes, Power of Two, Roman to Integer, Excel Sheet Column Title.
- *Medium*: Pow(x,n), Factorial Trailing Zeroes, Rotate Image, Max Points on a Line.
- *Hard*: Basic Calculator, Max Points on a Line, Rectangle Area.

---

## Pattern Recognition

- **Primes** → Sieve (all primes ≤ N) or trial division up to √N for single number.
- **GCD/LCM** → Euclidean algorithm; LCM = (a×b)/gcd(a,b). **Modular** → (a±b) mod M, (a×b) mod M; use mod at each step to avoid overflow.
- **Combinatorics** → nCr = n!/(r!(n-r)!); permutations n!; pigeonhole for "at least one" arguments.
- **Geometry** → Distance, slope (avoid float when possible; use cross product for collinearity). Max points on a line: group by slope (handle vertical).

## Interview Strategy

- **Identify**: "Count primes" → Sieve. "GCD" / "divisible" → Euclidean. "Ways to choose" → combinations. "Same line" → slope or cross product.
- **Approach**: State formula or algorithm; handle overflow (mod, or use long). Edge cases: zero, negative, large N.
- **Common mistakes**: Integer overflow in (a×b) before mod; division by zero in slope; forgetting 0 and 1 for primes.

## Quick Revision

- **Sieve**: Mark multiples of primes; O(N log log N). **Primality**: Check 2..√N. **GCD**: gcd(a,b)=gcd(b,a%b); O(log min(a,b)).
- **LCM**: (a×b)/gcd(a,b). **Mod**: (a+b) mod M = ((a mod M)+(b mod M)) mod M; same for product.
- **Trailing zeroes in n!**: Count of 5 in 1..n (each 5 contributes at least one 0).

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness |
|----------|------------|------------|
| **Pow(x,n)** | Fast exponentiation binary expansion of n | Negative n; n = MIN_INT edge case |
| **Sqrt(x)** | BS on `[0,x]` or Newton | Integer sqrt floor; overflow in `mid*mid` |
| **GCD / LCM** | Euclidean `gcd(a,b)=gcd(b,a%b)` | LCM = `a*b/gcd` overflow → divide first |
| **Count Primes** | Sieve of Eratosthenes | `i*i <= n`; boolean array size n+1 |
| **Max Points on Line** | Slope map from point i; gcd normalize dy,dx | Duplicate points; vertical line (dx=0) |
| **Random Pick with Weight** | Prefix sum + BS on random value | Inclusive ranges; `rand` in `[0, total)` |

---

## See also

- [Bit manipulation](bit-manipulation.md) — powers of two, parity  
- [Greedy](greedy.md) — some math scheduling problems  
- [Miscellaneous](miscellaneous.md) — number-theory style mix problems
