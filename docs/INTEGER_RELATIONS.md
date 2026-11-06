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

This is a **conditional construction**: whenever the matrix has
nonzero integer kernel, it constructs an exact finite-prefix collision.
The existence of nonzero kernel for every arbitrary K does **not**
follow merely by increasing M, because the number of prime-valuation
constraints grows with M as well. A general existence theorem remains
open here; it requires an explicit construction or a rigorous rank
bound. The implemented examples are bounded, exactly checked witnesses.

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


## General existence theorem (proved separately, not by bounded experiments)

The exploratory warning above concerns what can be inferred from a
**particular finite matrix**. A separate asymptotic rank argument
actually does establish existence of collisions for *every* fixed K:
let M tend to infinity and use the prime number theorem to guarantee
M > 1+K*pi(K*M). This makes the full valuation matrix rectangular
with strictly fewer rows than columns, so a nonzero integral kernel
exists. Appending twice the old common total weight in unit weights
makes both resulting spaces well-formed and terminal, while preserving
the first K supported coefficients. This yields a genuine unconditional
existence theorem for each finite K, **not** a guarantee that any
particular small M works.

The complete proof, including terminality of the unit-weight padding,
is in [research/universal_finite_prefix_ambiguity.md](../research/universal_finite_prefix_ambiguity.md).
The argument guarantees distinct spaces, not differing dimension for
arbitrary K. This distinction is essential.
