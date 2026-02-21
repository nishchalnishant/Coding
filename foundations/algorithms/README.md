# Algorithms

Recursion and backtracking --

* Process of defining a function or calculating a number by repeated application of an algorithm.
* Recursion — make correct set of choices and you end up at the solution
* Backtrack —  extension of recursion where if you reach dead end or otherwise discover that you have made an incorrect choise you have to backtrack to previous descision point and try a different path.

Sorting algorithms  --

* arranges elements of a list in certain order
* sometimes sorting efficiently reduces the complexity of the problem, mostly in case of searching cases

Searchin algorithms --

* Find for a particular element usually from DB, simple data elements in arrays, texts in files etc.

Selection algorithms --

* Finding Kth smalest largest number in a list
* Multiple algorithms&#x20;

String algorithms --

* Algorithms based on strings

Greedy algorithms --

* Single minded algorithms.&#x20;
* Process that looks for simple, easy to implement solutions to complex multip step problems by deciding which next step will provide the most obvious benifit
* idea is to perform single procedure over and over again untill it can't be done any more and what kind of result it will produce

Divide and conquer --

* divide— breaks the problem into serveral subproblems that are similar to the original problem but smaller in size
* Conquer— solve the subproblem recursively
* Base case — if subproblem are small enout then solve them directly
* Combine — the solutions to create a solution for the original problem.
* Master algorithm for divide and conquer --
  * divide the problems in to subproblems each of which is part of the original problem and then perform some additional work to compute the final answer.
  * ex - For each of the following recurrence give an expression for the runtime T(n). IF the recurrence can be solved with the master theorm
  *

      <figure><img src="../../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>
  *   Problem -1 _1'(11)_ = 3T (11/2) I · 11 2

      Solution: _T(11)_ = _3T_ (n/2) + 11 2 = > _T_ (11) = 0(n2) (M aster Theore m Case 3 .a)

      Proble m-2 _T(n)_ = 4T (11/2) + 11 2

      Solution: _'f'(n)_ = 4T (n/2) + n2 => _T (n)_ = 0 (11210911) (Master Theorem Case 2 .a)

      Problem-3 _T(n)_ = _T(n/2)_ + 112

      Solution: '/'(11) = '/'(11/2) + 112 = > <9(112) (Master Theorem Case 3.a)

      Problem -4 _T(11)_ = 211 '/'(11/2) + 11 11

      Solution: '/'(11) = 2"T(n/2) + 11" => Docs not apply _(a_ is not constant)

      Problcm -5 '/'(11) = 167'(11/'1) + _n_

      Solution: _T(n )_ = 167' (n/4) + _n_ => _T(n)_ = 0(n2) (Master Theorem Case 1)

      Problem -6 _T(n )_ = 2'/'(11/2) + _11/0911_

      Solution: _T(n)_ = 2T(n/2) + _11/0911_ => _T(n)_ = _0(11/og'ln)_ (M aster Theorem Case 2.a)

      Problem-7 _T(n)_ = 2T(n/2) + _11//0911_

      Solut ion: 7'(11) = 27'(n/2) + _11/lo911_ = > 7'(11) = _S(nlo,qlogn)_ (Muster Theorem Case 2. b)

      Problem-8 _T(n)_ = 2T (11/4) + no si

      Solution: _T(n)_ = 2T(n/4) + n°·5 1 => _'l'_ (n) = 8(11°·

      51 ) (Master Theorem Case 3.b)

      Problem -9 _T(n)_ = O.ST(n/2) + 1/n

      Solution: '/'(11) = O.ST(n/2) + l/11 => Does not apply _(n_ < I)

      Problcm -10 _T_ (11) = _6T_ (11/3) 1 _11 l logn_

      Solution: _'f'(n) = 6T(n/3)_ 1- _112 10911_ => _T(11)_ = <9(112/o,q11) (Ma:>ter Theore m Case 3.a)

      Problem -11 _T (11 )_ = 64T(n/U) - _11 210911_
  *   Solution: _T(11)_ = 64T(n/8) - _11 210911_ = > Docs not apply (function is not positive)

      Problem-12 _T (n)_ = _7T(n/3)_ + 11 2

      Solut ion: _T(11)_ = _7T(n/3)_ + n2 => _T(n)_ = E> (n2) (M aster Theorem Case 3 .as)

      Problem -13 _T (11)_ = 47' (n/2) + _logn_

      Solut ion: 7'(11) = 47'(n/2) + _IO.CJ11_ - > 'f(11) = <9(112 ) (Mus ter Theorem Case I)

      Problem -14 7'(n) = 16'/'(n/4)+ 11!

      Solution: T(n) = 16T (n/4) + 11! - > T(n) = 0(11!) (Master Theorem Case 3.a)

      Problem -15 _T_ (11) = _.f2T_ (n/2) + _logn_

      Solut ion: '/'(11) = _..fi.T_ (n/2) + _logn_ => _T (n)_ = E>(..fii) (Master Theorem Case 1)

      Problem -16 _T (n)_ = 3'f' (11/2) + _11_

      Solution: _T(11 )_ = _3T_ (n/2) + 11 -> _T(n)_ = 0(111"0:1) (M aster Theorem Case 1)

      Problcm-17 T(n) = 3T (11 /3) + ..{ii.

      Solution: '/'(11) = _3T_ (n/3) + _Jn_ = > _T(11)_ = <9(11) (M aster Theorem Case 1)

      Problem-18 _T(n)_ = 4T (n/2) + _en_

      Solution: '/'(11 ) = 47' (n/2) + _en_ = > _T(n)_ = 0(n2) (Mas ter Theorem Case l)

      Problem-19 _T(n)_ = 3T (11/4) + _11/0911_

      Solution: _T(11)_ = 3T (n/4) + _11/0.qn_ => _T(11)_ = 0(11/og11) (Muster Theorem Case 3.a)

      Problem-20 _T_ (11) = _3T_ (n/3) + 11/2

      Solution: _T(11)_ = _3T_ (n/3) I- 11 /2 = > _T_ (11) = _8(11/o911)_ (M aster Theorem Cusc 2.a)

Dynamic programming --

* Technique to solve in cases when all above solutions have failed.
* DP is a simple technique but it can be difficult to master

Mislanious —&#x20;

* Bitwise tracking —&#x20;
*
