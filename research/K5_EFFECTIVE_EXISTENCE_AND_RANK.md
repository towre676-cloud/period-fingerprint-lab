# Effective K=5 terminal finite-prefix ambiguity: explicit bounds

*Research note, 2026-11-06. Priority and mathematical novelty have not been assessed.*

## Problem and conclusion

Let `M_5` denote the least integer M for which two **distinct**
well-formed terminal weighted projective spaces with the same total
weight and **all individual weights <=M** have identical first five
positive supported factorial-ratio quantum-period coefficients.

The present independently checkable bounds are

```
             25,809 <= M_5 <= 41,100,000,000.
```

The lower bound is a finite-field *no-relation* theorem.
The upper bound is a *nonconstructive existence theorem*
using a published explicit prime-counting inequality.
Neither result provides an explicit five-coefficient signed
integer witness, and neither asserts a dimension mismatch.

## Lower bound from two prime fields

The full factorial-valuation matrix V_5(M) has columns
indexed by weights 1,...,M, the total-weight row (a),
and one row `v_p((ma)!)` for each m=1,...,5 and
prime p<=5M.

- The original `scripts/verify_k5_modp.cpp` proves full
  column rank 25808 over F_65521, with first modular
  dependence at weight 25809.
- A separately written `scripts/verify_k5_second_modulus.cpp`
  gives the same result over F_65519.
- The original packed-bitset checker gives full rank
  through 25626 over F_2, with an earlier characteristic-two
  dependence at weight 25627.

Full rank modulo either odd prime implies full rational
rank of the same integer matrix. Thus no nontrivial
integer factorial relation can use only weights <=25808.
In particular, this excludes terminal collisions.
The modular dependence at 25809 in two different fields
does **not** prove existence of a rational relation.

Reproduce the independent odd-prime test:

```sh
g++ -O3 -std=c++20 -Wall -Wextra -o /tmp/k5_second \
  scripts/verify_k5_second_modulus.cpp
/tmp/k5_second 25810 5
```

## Upper bound from exact rational arithmetic and Dusart

We use Pierre Dusart, *Explicit estimates of some
functions over primes*, Corollary 5.3(d):

```
pi(x) <= x / (ln(x) - 1 - 1.2311/ln(x)),  x>5.6.
```

This is **external published mathematics**, not
reproved by our script.

Fix K=5 and M=41,100,000,000. The number of rows in
V_5(M) is at most `1+5*pi(5M)`. We prove that
this is **strictly smaller than M**, as follows.

Write `z=1/3` and `w=1/2`. The positive series

```
ln((1+z)/(1-z)) = 2 sum_{j>=0} z^(2j+1)/(2j+1)
```

proves rigorous *rational* lower bounds for ln2 and ln3
by taking only six terms. Also,

```
5M > 12*2^34*(299/300)
ln(299/300) > -1/299.
```

Consequently,

```
ln(5M) > 36 ln2 + ln3 - 1/299 > 26.048.
```

For the increasing function `f(t)=t-1-1.2311/t`,

```
ln(5M) - 1 - 1.2311/ln(5M)
    > 26.048 - 1 - 1.2311/26.048 > 25.
```

Dusart therefore yields `pi(5M) < 5M/25=M/5`.
The strict inequality is actually strong enough to
give `1+5*pi(5M)<M`; the last comparison is
verified *exactly* as a rational inequality in the
replay program.

Thus the M-column **integer matrix** V_5(M)
has fewer than M rows and a nonzero rational kernel.
Clearing denominators gives a nonzero integer vector.
Its positive and negative parts are distinct weight
multisets, have equal weight sum (first-row equation),
and have equal factorial-denominator products
for m=1,...,5 by prime valuations.

Adjoin 2M unit weights to *each* multiset.
The terminal-padding lemma ensures that both resulting
weighted projective spaces are well-formed and terminal;
their maximum individual weight remains at most M and
their five supported coefficients remain identical.
This proves the upper bound.

```sh
python scripts/verify_k5_effective_bound_411e8.py
```

This script checks **every new numerical inequality using
exact rational arithmetic**. Its only external axiom is
the clearly cited Dusart prime-counting theorem.

## Independent factorial identity checking

For any explicit signed relation, use

```sh
python scripts/verify_signed_relation_fast.py relation.json --K 5 --padding N
```

The verifier computes prime-exponent differences using
a smallest-prime-factor sieve and exact tail sums of
signed multiplicities; it does not use the original
discovery algorithm or construct astronomical factorials.

It has been tested against the independent known K3 and
K4 witnesses and detects deliberate perturbations.

## What remains open

1. Extract an **exact** integer kernel vector near
   individual weight 25809; the two modular dependencies
   are suggestive, not conclusive.
2. Construct a terminal K5 pair with a much smaller
   total weight and manageable dimensions.
3. Establish whether K5 finite ambiguity can
   **change dimensions**; neither the present
   existential argument nor the modular rank result
   guarantees that.
4. Cross-check any completed integer witness by an
   independently implemented exact factorial verifier.

No claim is made about arbitrary Fano varieties or
agreement of the complete infinite quantum period.
