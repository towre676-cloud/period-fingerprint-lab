# Sharp maximal-weight thresholds for three coefficients

*Research note, 2026-11-06. Unrefereed. Novelty and priority are unassessed.*

## Definitions

For a finite signed integer relation `u=(u_a)` supported on
positive weights `a<=M`, define the two multisets by the positive
and negative parts of `u`. Let `K` be the number of supported
regularized quantum-period coefficients. Exact matching with a
**common total weight** is equivalent to

`sum_a a*u_a=0` and
`sum_a u_a*v_p((m*a)!)=0`

for all `1<=m<=K` and primes `p<=K*M`.

These are integer linear equations. Their coefficient matrix
`V_K(M)` has M columns indexed by candidate weights and rows
indexed by the total-weight equation and the factorial
prime-valuation equations. Thus **any** equal-support collision
produces a nonzero integral kernel vector; conversely, any such
vector gives two equal-support factorial-denominator multisets.

We distinguish two properties of the kernel: nonzero integer
vectors produce different weights, while vectors satisfying
`sum_a u_a!=0` produce different dimensions.

## Theorem A — first three-prefix relation at maximum weight 172

The matrix `V_3(171)` has rank **171 over F_1000003**.
Thus it has full column rank over the rationals, excluding
every nontrivial factorial collision among weights <=171,
with no assumptions about terminality or dimension.

The signed relation `K3-W172` in
[`k3_exact_relations.json`](k3_exact_relations.json)
uses only weights <=172. It has 15 positive weights and
15 negative weights, both totaling 659. The exact
prime-factorial conditions vanish for m=1,2,3.
Direct age checks for k=2,...,657 prove that both weight
multisets themselves give **well-formed terminal**
weighted projective spaces of dimension 14.

The fourth supported coefficients differ:
`c_A(4)/c_B(4)=65119987073340199/65119354660916775`.

Therefore 172 is the **minimum possible largest individual
weight** for any three-supported-coefficient collision with a
common support step, and this minimum is attained in the
terminal subclass. The total weight 659 is not claimed
minimal.

## Theorem B — dimension-changing relation first possible at 189

The weight-172 relation extends to a kernel vector of
`V_3(188)` with coefficient sum zero. Thus
`rank_Q V_3(188)<=187`.

Independent modular elimination proves
`rank_(F_1000003) V_3(188)=187`, so the exact rational
rank equals 187. Since there are 188 columns, the kernel
has dimension precisely **one**, spanned by the
weight-172 relation. Hence **every** relation with weights
<=188 has zero coefficient sum, and no two differently
dimensional spaces with a common total weight can share
their first three supported coefficients in this range.

The independently checked signed relation `K3-W189-dimension`
uses weights <=189 and satisfies every exact valuation equation
through m=3. Its positive and negative multiplicities total
**471,810** and **471,684** respectively, while both weight
sums are **27,847,032**. Thus the dimensions differ by 126.
The relation has nonzero fourth-coefficient valuation differences.

Adjoining **378 unit weights** to each multiset makes both
spaces well-formed and terminal. The new common total weight is
**27,847,410** and the dimensions are **472,187** and
**472,061**. The first three supported coefficients
remain exactly equal.

The 172 relation and 189 relation are independent. Consequently
the rational nullity of `V_3(189)` is at least two;
its modular rank is exactly 187, giving rational rank
at least 187, so the nullity is exactly two.

It follows that **189 is the smallest possible maximum
individual weight for an exact dimension-changing
three-supported-coefficient collision**, attained by
terminal weighted projective spaces. This is not a
minimality claim about total weight or dimension.

## Lemma — efficient terminal padding

Let `W=(a_1,...,a_N)` be a nonempty multiset of positive
integers with sum `H` and maximum `M`. Adjoin `r>=2M`
copies of the unit weight 1, obtaining `W'` of total
weight `L=H+r`. Then `W'` is well-formed and terminal
in the weighted-projective fractional-age criterion
(provided its resulting dimension is at least three).

**Proof.** The two unit weights alone ensure
well-formedness. For any integer `2<=k<=L-2`, if
`k<L/M` then `k*a_i<L` for every old weight.
All weights, including the new units, have no modular
wrap and the fractional-age sum equals `k>=2`.
If `k>=L/M`, the r added unit weights contribute
exactly `rk/L>=2M*k/L>=2`; all other contributions
are nonnegative. Therefore every relevant age is at
least two. Since for any k,

`age(k)+age(L-k)=N+r-z(k) <= N+r`,

where z(k) counts the entries divisible by L in the
corresponding residues, the lower bound for age(L-k)
implies `age(k)<=N+r-2`. The fractional-age criterion
proves terminality. QED.

This improves on the earlier padding of twice the
total weight, but does **not** by itself minimize
total weight or geometric dimension.

## Independent replay

```sh
python scripts/verify_k3_relations.py research/k3_exact_relations.json
```

The verifier does **not** import any periodlab discovery code.
It tests all three exact signed relations prime by prime, checks
all 657 age conditions of each 14-dimensional witness,
checks the efficient-padding lemma's hypotheses for the
dimension-changing witness, and independently recomputes
the ranks at maximal weights 171, 172, 188, 189 over
the prime field F_1000003.

Because the rank calculations are over a finite field,
a full modular rank proves a rational lower bound.
An explicit rational null vector proves the upper
rank bound. The matching bounds certify the exact rank;
no floating-point rank heuristic is involved.

## Four coefficients — stronger negative result

The separate `verify_k4_bound.py` constructs `V_4(1500)`
over F₂ and finds full rank **1500** by exact binary
elimination.

A further *correctly typed* C++ modular checker constructs
`V_4(1691)` over the prime field F₆₅₅₂₁ and finds
**rank 1691**. Therefore **no two different finite positive
weight multisets with common total weight and individual
weights at most 1691** can match their first four supported
factorial-ratio quantum-period coefficients. The same
conclusion holds *a fortiori* for terminal spaces.

The first modular dependence over F₆₅₅₂₁ appears on adding
weight 1692, but **this is not yet a rational or integer
factorial identity**. A prior exploratory large-prime scan
using 16-bit storage for much larger moduli was invalid;
its claimed threshold of 1929 was retracted. The corrected
checker uses wide integer intermediates and explicit
modular reductions.

```sh
python scripts/verify_k4_bound.py --max-weight 1500 --prefix 4
g++ -O3 -std=c++20 -Wall -Wextra -o /tmp/weight_rank scripts/verify_k4_rank.cpp
/tmp/weight_rank 1691 4
/tmp/weight_rank 1692 4
```

The next open task is to determine whether the modular
dependence at 1692 lifts to a genuine rational relation,
and to construct a fourth-prefix terminal collision.

The conditions and domain matter: none of these results
proves that four coefficients determine an arbitrary
Fano variety, or that the full quantum period fails
to determine geometry.

## Evidence grading

- Signed relations and age inequalities: direct exact computations.
- Sharp largest-weight thresholds: exact modular ranks plus explicit
  integer kernel witnesses; proof is conditional on correct
  verifier source and arithmetic, not formally checked in Lean.
- Prior originality: unknown; literature audit pending.
- Three-prefix minimal *total* weight: open.
- Smallest dimension-changing pair under geometric
  dimension/weight-sum constraints: open.

See `PAPER_DRAFT.md` and the primary quantum-period
and terminality literature linked there.


## Theorem C — three-coefficient ambiguity with dimension difference one

The signed identity `K3-W249-dimension-one` in the same
machine-readable certificate is a further exact relation with
largest individual weight **249**. Its positive and negative
multisets contain **117,549** and **117,548** weights, both
totalling **9,268,001**. For m=1,2,3 all factorial-prime
valuations cancel identically; they do not cancel at m=4.

Appending 498 (=2×249) unit weights to each side invokes the
terminal-padding lemma proved above. The resulting well-formed
terminal weighted projective spaces have common total weight

**9,268,499**

and dimensions

**118,046 and 118,045**.

Thus, unlike the first maximal-weight-189 witness with dimension
gap 126, there exists an explicit **dimension gap of just one**
for three matching supported coefficients.

This example is constructed as an integer linear combination
of separately computed rational-kernel basis vectors, followed
by lattice-basis reduction. The final signed relation is directly
rechecked prime-by-prime by `scripts/verify_k3_relations.py`,
independently of the search and reduction algorithms.

The weight 249 is **not** claimed minimal for a dimension gap
of one. The earlier weight 189 remains the sharp minimal
maximal-weight threshold for *any* dimension-changing relation;
whether a gap-one witness exists below weight 249 is open here.
