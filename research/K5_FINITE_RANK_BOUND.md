# Five supported quantum-period coefficients: exact weight exclusion bound

**Status:** A finite algebraic rank theorem, not an explicit five-coefficient
collision. Computed with two independent finite-field elimination algorithms.

For a fixed positive integer K and maximum allowed weight M, define
the integer matrix V_K(M) with columns a=1,...,M, first row a,
and additional entries v_p((m*a)!) for every prime p<=K*M
and m=1,...,K. Equality of the first K supported factorial-ratio
quantum-period coefficients between two multisets with the **same**
total weight implies a nonzero integer vector in the kernel
of V_K(M), obtained by subtracting weight multiplicities.

## Verified bound for K=5

The full column rank calculation over **F_65521** gives

```
rank V_5(25808) mod 65521 = 25808
```

Therefore the integer matrix has full rational column rank, and
**no two distinct positive weight multisets with common total weight
and every individual weight <= 25808** can share all their first five
positive supported quantum-period coefficients.

No terminality hypothesis is needed for this exclusion. It is
stronger than a statement restricted to terminal spaces.

The first modular dependence over F_65521 occurs at M=25809,
but this alone is **not** an integer factorial identity.

## Independent cross-check

An independent bitset implementation over F_2 gives

```
rank V_5(25626) mod 2 = 25626
first modular dependence mod 2: M=25627
```

Thus the two modular characteristics differ in their earliest
dependency, as can happen even when the rational matrix is
full rank. It would be incorrect to infer a rational collision
from the characteristic-two kernel at 25627.

## Reproduction

```sh
g++ -std=c++20 -O3 -Wall -Wextra -o /tmp/k5_gf2 scripts/verify_k5_gf2.cpp
g++ -std=c++20 -O3 -Wall -Wextra -o /tmp/k5_modp scripts/verify_k5_modp.cpp
/tmp/k5_gf2 25627 5
/tmp/k5_modp 25809 5
```

The GitHub Actions job `five-prefix-rank-bound` executes
both from a clean checkout.

## Remaining scientific question

Does a genuine integer K=5 relation exist close to M=25809?
The present result proves only that no relation exists for
weights <=25808. To produce a terminal collision one must
construct a nonzero **integer** relation, check its factorial
valuations independently, and prove or impose terminality
via the exact fractional-age criterion.

There are no claims here of minimal total weight,
minimal dimension, or all-Fano uniqueness. Mathematical
priority and novelty remain unassessed.


## Update: exact effective existence upper bound (November 6, 2026)

The lower bound from modular rank now has a complement:
**a distinct terminal same-dimensional K5 collision exists using only
individual weights <=2,867,000**. This is an *existence* result,
not an explicit integer witness.

The new argument counts only the prime rows actually needed
for each m rather than using five copies of pi(5M).
Two independent Python sieve implementations and an independent
segmented C++ sieve establish the exact counts

```
pi(2,867,000)  = 207,927
pi(5,734,000)  = 395,799
pi(8,601,000)  = 577,502
pi(11,468,000) = 755,330
pi(14,335,000) = 930,416
```

Their sum is 2,866,974. Including the total-weight row
leaves at most 2,866,975 constraints on 2,867,000
unknown signed multiplicities, so the rational nullity
is at least 25. Even after imposing equality of the
number of weights by an additional all-ones row, nullity
remains at least 24. Nonzero rational relations clear to
integer relations. The common padding of 5,734,000
unit weights on each side makes the resulting weighted
projective spaces well-formed and terminal.

Thus for the minimum possible maximum individual weight
of a nontrivial terminal five-prefix collision, we now know:

```
                 25,809 <= M5 <= 2,867,000.
```

The independent prime-field calculations over F_65521
and F_65519 agree on the lower bound; their first modular
dependence is at 25,809. That dependence remains *only
modular* and must not be asserted to yield an integer witness.

Full proof and independent replay:
[research/K5_PRIMECOUNT_EXISTENCE_2867000.md](K5_PRIMECOUNT_EXISTENCE_2867000.md).

```sh
python scripts/verify_k5_primecount_existence.py
g++ -O3 -std=c++20 -Wall -Wextra -o /tmp/k5_primes scripts/verify_k5_primecount_segmented.cpp
/tmp/k5_primes
```

The earlier qualitative bound of 41.1 billion from Dusart
is superseded by the finite prime census. The new upper
bound requires no external analytic prime-counting estimate.
