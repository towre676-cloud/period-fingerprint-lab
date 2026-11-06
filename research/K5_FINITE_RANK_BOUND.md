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
