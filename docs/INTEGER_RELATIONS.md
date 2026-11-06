# Exact integer-relation discovery engine

The older bounded census searches through *spaces*. A complementary
method searches through *linear algebraic relations between weights*.

For each candidate weight a in 1,...,M define its column vector

`v(a) = (a; v_p((m*a)!) for every 1<=m<=K and prime p<=m*M)`.

A rational/integer kernel vector `u=(u_a)` satisfies
`sum_a u_a * v(a)=0`. Its positive entries define one weight
multiset and its negative entries another. The first row forces equal
weight totals L. The remaining rows force exact denominator
equality by unique prime factorization:

`prod_(u_a>0) (m*a)!^(u_a) = prod_(u_a<0) (m*a)!^(-u_a)`

for m=1,...,K. The common numerator `(L*m)!` makes their first K
supported period coefficients identical.

The positive and negative parts of a nonzero kernel vector must
both be nonempty because the first row has strictly positive entries.
Adding two weights of 1 to each space makes each well-formed,
preserves all equalities, and avoids the one-weight degenerate case.

This establishes, **for every finite K**, the existence of distinct
well-formed weighted projective spaces with matching first K
nonzero period coefficients: choose M large enough so the number
of columns M exceeds the number of (finite) valuation constraints.
However, this crude counting requires a careful bound on the number of
relevant prime rows as M grows, and that row count can also grow
with M. The code therefore **does not** claim this argument by itself
proves nullity for every K. A valid future theorem must construct
a kernel vector or prove a nontrivial rank bound.

The executable implementation `periodlab.relations` uses exact
Fraction RREF, integral LCM normalization, and independent
factorial-ratio checks. It can rediscover a nonzero relation in
a bounded candidate-weight interval; it does not guarantee that
the resulting spaces differ in dimension or have terminal singularities.

Example:

```python
from periodlab.relations import discover_relation
print(discover_relation(max_weight=25, prefix=2))
```

Potential research: kernel-vector size minimization, integer linear
programming with bounded multiplicities, choosing dimension mismatch,
terminality filters, and independence from the brute-force census.
