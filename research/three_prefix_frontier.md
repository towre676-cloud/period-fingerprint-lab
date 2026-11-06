# Three supported coefficients: exact terminal search through total weight 70

**Research status:** Bounded exact computation, pending complete
independent hosted replay on repository HEAD. Not a global theorem.

Given a well-formed terminal weighted projective space of total
weight L, compare the first three positive supported regularized
period coefficients, at degrees L, 2L and 3L. The exhaustive
integer-partition enumerator with prime-valuation factorial
signatures reports:

**No two distinct such spaces have an identical triple
(L, c_L, c_(2L), c_(3L)) for any L <= 70.**

Computations are reproducible with:

```sh
g++ -O3 -std=c++20 -Wall -Wextra \
  -o /tmp/terminal_scan scripts/terminal_collision_scan.cpp
/tmp/terminal_scan 2 70 3 > three-prefix-L70.log
grep '^TOTAL' three-prefix-L70.log
```

The scanner enumerates nondecreasing integer partitions, applies
the omit-one gcd definition of well-formedness, applies the exact
fractional-age condition for terminal quotient singularities,
and compares the prime-valuation vectors of the denominator
products `prod_i (m*a_i)!` for `m=1,2,3`.

It does not rely on decimal approximations, floating-point
hashes, or estimated dimensions. The signature uses a
one-byte-per-valuation encoding with an explicit overflow check;
for all L<=70 and m<=3, denominator factorial valuations are
bounded by those of `(210)!`, which fit within one byte.

A separate Python factorial-denominator implementation has
independently checked the smaller two-prefix L=51 threshold.
The third-prefix frontier is verified through L=70 with
C++ exact arithmetic and with no false match observed; **a
second independent Python full-L70 replay is outstanding**.

This finite result is compatible with the theorem that for each
fixed K there exist sufficiently large nonisomorphic terminal
weighted projective spaces with the same first K supported
coefficients. The search does not assert a unique dimension
from an arbitrary finite prefix.
