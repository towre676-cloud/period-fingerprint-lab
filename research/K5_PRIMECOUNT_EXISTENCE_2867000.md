# Five-coefficient ambiguity with maximum individual weight at most 2,867,000

*Research note, November 6, 2026. An exact finite-combinatorial existence
proof. Neither a compact integer witness nor mathematical novelty is claimed.*

## Theorem (effective K=5 collision; even in the same dimension)

There exist **distinct, well-formed terminal weighted projective spaces**
with a common total weight, the **same geometric dimension**, and
identical first **five positive supported coefficients** of their
regularized quantum periods, such that *all individual weights are
at most 2,867,000*.

The proof is nonconstructive but finite and checkable. It uses two
independent standard-library exact prime sieves, then integer linear
algebra and the previously proved unit-weight terminal-padding lemma.

More precisely, if `M_5` denotes the smallest possible maximum
individual weight of a pair of **distinct terminal weighted projective
spaces** sharing five supported coefficients and total weight, our
current results give:

```
          25,809 <= M_5 <= 2,867,000.
```

The lower bound comes from full rank over F_65521 and F_65519
through individual weight 25,808. The upper bound is certified below.

## Proof

Let `M=2,867,000`. Build the integer matrix `V_5(M)`
with one column for each possible weight `a=1,...,M`.
Its first row is `a`, enforcing the same total weight.
For each integer `1<=m<=5` and each prime `p<=m*M`,
add a row whose column at weight a equals

```
        v_p((m*a)!).
```

The matrix therefore has **M columns** and **at most**

```
        1 + sum_{m=1}^5 pi(m*M)
```

rows, where pi(x) is the number of primes <= x.
The word *at most* allows duplicate or dependent valuation rows;
no rank assumptions are made.

Two independently implemented exact Eratosthenes sieves give:

| m | m*M | pi(m*M) |
|---|---:|---:|
| 1 | 2,867,000 | 207,927 |
| 2 | 5,734,000 | 395,799 |
| 3 | 8,601,000 | 577,502 |
| 4 | 11,468,000 | 755,330 |
| 5 | 14,335,000 | 930,416 |
| **Total** | | **2,866,974** |

Including the total-weight row yields at most **2,866,975**
rows, **25 fewer than the 2,867,000 columns**.
Thus the rational kernel has dimension at least 25.
Its nonzero vectors can be multiplied by a common
denominator to obtain nonzero integer kernel vectors.

A nonzero integer vector `u=(u_a)` has

```
sum_a a*u_a = 0
sum_a u_a * v_p((m*a)!) = 0
    for all m=1,...,5 and primes p<=m*M.
```

Because all a are positive, `u` must have both
positive and negative entries. These encode two
different positive weight multisets with equal
total weight `H`. Unique prime factorization
makes their factorial-denominator products
equal for m=1,...,5; their common factorial numerator
`((H*m)!)` is identical. Thus the first five
positive supported coefficients agree exactly.

To force **equal dimension**, append one more matrix
row consisting of ones. Even after adding this count
constraint the matrix has at most 2,866,976 rows,
still **24 fewer than its columns**. Choose any
nonzero integer kernel vector of this enlarged
matrix. It additionally satisfies `sum_a u_a=0`,
so its positive and negative sides contain the
same number of weights.

Finally, append `2M=5,734,000` common unit
weights to each multiset. Each resulting weight
list is well-formed and terminal by the proved
padding lemma: for `2<=k<L/M`, no weight wraps
and the age equals k; for larger k, the
common unit weights alone contribute at least
2 to the age, while complementary ages give
the upper bound. The common padding preserves
equality of the first five coefficients, equal
total weight, and equal numbers of weights.
The resulting maximum individual weight is
still <=M.

The two weight multisets remain distinct,
so their well-formed weighted projective spaces
are nonisomorphic. QED.

## Exact independent replay

```sh
python scripts/verify_k5_primecount_existence.py
```

The verifier constructs both a full boolean sieve
and a separate odd-only sieve with different
indexing, confirms all five exact prime counts,
and checks every dimension inequality as integers.
The calculation uses roughly 14.4 MB of sieve
storage and no external numerical dependencies.

The proof establishes existence of an integer
kernel, not its coefficients. It does NOT claim
the search bound is optimal, construct a
dimension-changing K5 example, or claim equal
**infinite** quantum periods. The first modular
dependency near 25,809 is still not a verified
rational identity.

## Comparison with previous bound

The earlier upper bound **41.1 billion** used
a published explicit prime-counting inequality
and the coarse estimate `5*pi(5M)` for all
five sets of valuation rows. Counting the rows
separately and using *actual finite prime counts*
replaces it with **2.867 million**, a more than
14,000-fold improvement. No external analytic
prime theorem is needed for the new certificate.

## Research frontier

Produce a fully explicit integer relation,
preferably near the 25,809 modular dependency;
then independently certify its first five
coefficient equalities, its sixth inequality,
and terminality. A dimension-changing example
or a compact low-dimensional example would
be stronger than the equal-dimension existence
result proved here.


## Sharpened exact row-count thresholds

An additional **complete scan of the row-count inequality**
for every integer M from 2 through 2,866,599 sharpens
the results:

- **M=2,866,589** is the first cap at which
  `1+sum_m pi(m*M)<M`, forcing a nonzero integer
  factorial relation. The exact prime counts are
  `207897,395749,577427,755224,930290`,
  summing to `2,866,587`. Including the total row
  gives `2,866,588` rows against `2,866,589` columns.
- **M=2,866,599** is the first cap at which
  `2+sum_m pi(m*M)<M`. The exact prime counts are
  `207897,395749,577429,755228,930293`,
  summing to `2,866,596`. Total-weight and
  weight-count rows give at most `2,866,598`
  rows against `2,866,599` columns, so a
  same-dimensional integer relation exists.

These are the first bounds that the **simple raw row-count
criterion** proves, not globally minimal weights for actual
collisions. Because the argument above already proves
terminality after common unit padding, the stronger
statements are

```
25,809 <= M5 <= 2,866,589                      (any collision)
25,809 <= M5_same_dimension <= 2,866,599       (same dimension)
```

The standalone C++ verifier computes all `pi(n)` through
`5*2,866,599` by an exact sieve, checks the integer
inequality **for every cap from 2 to 2,866,599**,
and records the first successful cap in each class.

```sh
g++ -O3 -std=c++20 -Wall -Wextra \
  -o /tmp/k5_threshold scripts/verify_k5_counting_threshold.cpp
/tmp/k5_threshold
```

The original 2,867,000 example remains useful:
its raw-count matrix has nullity at least **25**
(and at least **24** after the dimension constraint).
The sharper first-sufficiency bounds establish
existence but only guarantee one kernel direction
at the selected caps.

An *explicit signed integer relation at these caps*
has not been extracted.
