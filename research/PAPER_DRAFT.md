# Finite quantum-period fingerprints of terminal weighted projective spaces

*Working research note, November 2026. Unrefereed, mathematical novelty not established.*

## Abstract

The regularized quantum period of a weighted projective space
\(\mathbb P(a_1,\ldots,a_N)\) has the factorial-ratio form
\[
\widehat G(t)=\sum_{m\ge0}\frac{(Lm)!}{\prod_{i=1}^N (m a_i)!}t^{Lm},
\qquad L=\sum_i a_i.
\]
The complete infinite series determines the dimension in this class,
by the asymptotic analysis of Coates–Kasprzyk–Veneziale. We consider
a complementary finite-data problem: how many *supported positive-degree*
coefficients are needed to exclude competing weighted-projective
dimensions? We construct an exact terminal pair of total weight 51
and dimensions 8 and 7 whose first two supported coefficients agree,
but whose third coefficients differ. Independent exhaustive searches
find that total weight 51 is minimal for a terminal two-coefficient
collision; at that weight there are exactly 77 pairs and all arise
from adjoining a common partition of 12 to a single factorial
identity. A separate constructive linear-algebra argument proves
that for **every fixed number K** of supported coefficients there
exist distinct terminal weighted projective spaces with the same
first K values, even when their common total weight is known.
Finally, we give an elementary finite reconstruction theorem:
with the total weight L known, L consecutive supported coefficients
uniquely recover the whole multiset of weights. The algebraic
statements have proofs; all minimality and classification bounds
are explicitly computer-assisted and require external replay before
they can be regarded as formal certificates.

## 1. Definitions and normalization

Let \(w=(a_1,\ldots,a_N)\) be a sorted list of positive integer
weights. It is *well-formed* if the gcd of every list obtained
by deleting one weight is 1. We write
\(X_w=\mathbb P(a_1,\ldots,a_N)\),
\(L=\sum_i a_i\), and \(d=N-1\).
Well-formed weighted projective spaces are classified up to
isomorphism by their weight multisets (in this normalization).

For the supported part of their regularized quantum period put
\[
C_w(m)=\frac{(Lm)!}{\prod_i (a_i m)!},\quad m=0,1,2,\ldots,
\]
and let \(F_K(w)=(L,C_w(1),\ldots,C_w(K))\).
Including L prevents two unrelated support patterns from being
identified because their supported subsequences happen to agree.

For dimension at least 3, the terminality criterion used here is
that for every \(k=2,\ldots,L-2\),
\[
 2\ \le\ \sum_i\left\{\frac{ka_i}{L}\right\}\ \le\ N-2,
\]
where \(\{x\}\) denotes fractional part. Since the sum of
weights is L, each displayed age is automatically an integer.
In dimensions at most 2, terminality means smoothness and is
checked separately. These criteria follow the published work;
they are not inventions of this note.

## 2. The first explicit two-coefficient terminal collision

Consider the denominator identity in weights summing to 39:
\[
 A_0=(1^5,5,5,24),\qquad B_0=(2^4,3^2,25).
\]
Here an exponent on a weight means its multiplicity. Direct
multiplication proves
\[
 (1!)^5(5!)^2(24!)=(2!)^4(3!)^2(25!)
\]
and
\[
 (2!)^5(10!)^2(48!)=(4!)^4(6!)^2(50!).
\]
Consequently \(C_{A_0}(1)=C_{B_0}(1)\) and
\(C_{A_0}(2)=C_{B_0}(2)\). Their dimensions differ by one.
The two spaces are not terminal.

**Theorem 2.1 (explicit terminal pair).** Put
\[
 A=(1^5,5,5,12,24),\qquad
 B=(2^4,3^2,12,25).
\]
Then A and B define terminal, well-formed weighted projective
spaces of dimensions 8 and 7 respectively. Their first two
positive supported quantum-period coefficients are equal at
degrees 51 and 102, but
\[
 \frac{C_A(3)}{C_B(3)}
 =\frac{1080400}{1002001}\neq1.
\]

**Proof.** Both total weights equal 51 and the common 12
contributes the same factorial denominator to both sides,
preserving the first two identities. Direct application of
the terminality age criterion for k=2,...,49 gives ages in
[2,7] for A and [2,6] for B. The integrality and inequalities
are exact; the checking script reproduces them without floating
point. The third coefficient ratio follows by cancelling the
common factorials and using exact integer arithmetic. QED.

The example is notable for demonstrating different dimensions,
not merely different weight lists. It is also far less
high-dimensional than the all-unit-padding construction:
the dimensions are 8 and 7, not 19 and 18.

## 3. A terminality-preserving splitting operation

**Lemma 3.1.** If a well-formed terminal weighted projective
space of dimension at least 3 has a weight a=b+c, with positive
integers b,c, then replacing a by b,c produces another
well-formed terminal weighted projective space.

**Proof.** Deleting one of the new weights leaves every unchanged
old weight, whose gcd is 1 by old well-formedness. Deleting an
unchanged weight leaves both b,c in place, and its gcd divides
the old omit-one gcd, because that old list contained their
sum a. Hence the new weights remain well-formed.

The total weight L is unchanged. At any relevant k the
new fractional-age sum differs from the old by
\[
 \left\{\frac{kb}{L}\right\}
 +\left\{\frac{kc}{L}\right\}
 -\left\{\frac{k(b+c)}{L}\right\}\in\{0,1\}.
\]
The old allowed range is [2,N-2], the new range is
[2,N-1], and therefore the terminality inequalities remain
valid. QED.

Taking any positive partition P of 12 and adjoining it to
both A0 and B0 is the same as repeatedly splitting the added
12 in Theorem 2.1. Thus all p(12)=77 partitions produce
distinct terminal two-prefix collision pairs with total
weight 51 and dimensions differing by one.

**Computational Theorem 3.2 (bounded minimum and complete list).**
Within *all* well-formed positive weight multisets of total
weight at most 51, no pair of terminal spaces shares F2
below weight 51. At L=51 there are precisely 77 unordered
collision pairs, each of size two, and every one is exactly
(A0+P,B0+P) for one partition P of 12.

**Evidence and limits.** This latter assertion is supported by
two separately written exhaustive enumerators: a C++ search
comparing prime valuations of factorial denominators, and an
independent Python program comparing the denominator integers.
Both enumerate nondecreasing integer partitions and independently
check all age conditions. At L=51 they agree on 239,943
integer partitions, 230,292 well-formed weight lists, 211,234
terminal weight lists, and 77 matching terminal pairs. The
Python classifier directly compares the complete 77-group
collection against the common-partition construction.
A complete exact C++ census through L=51 and a separate
Python L=51 replay are included in GitHub CI. This is strong
finite computational evidence but is **not** a formal proof
that the enumerators are complete.

For comparison, the smallest terminal one-supported-coefficient
collision occurs at L=9 between \((1^5,4)\) and
\((1,1,2,2,3)\), of dimensions 5 and 4, because
\(4!=(2!)^2(3!)\).

## 4. No fixed length suffices in general

**Theorem 4.1 (universal finite-prefix ambiguity).** For each
fixed positive integer K there are two nonisomorphic terminal,
well-formed weighted projective spaces with a common total
weight L and identical \(F_K\).

**Proof.** Fix K and take M so large that
\[
 M>1+K\pi(KM),
\]
where \(\pi(x)\) is the number of primes at most x. This is
possible by the prime number theorem, since K is fixed and
\(\pi(KM)=O_K(M/\log M)\).

Build an integer matrix with M columns indexed by a=1,...,M.
The first row is (1,2,...,M); the remaining rows are indexed
by m=1,...,K and primes p<=KM and have entries
\(v_p((ma)!)\). The row count is smaller than M; hence there
is a nonzero rational kernel vector. Multiplying by a common
denominator gives a nonzero integer vector u. The first row
forces \(\sum_a a u_a=0\), so u has positive and negative
entries. Separate the positive and negative components into
distinct multisets U and V, both with total weight H>0.
The other rows and unique prime factorization imply
\[
 \prod_{a\in U}(ma)!
 =\prod_{b\in V}(mb)!,\quad 1\le m\le K.
\]

Adjoin r=2H copies of weight 1 to **both** U and V. Each
resulting weight list sums to L=3H and contains at least
two 1s, so each is well-formed. Their first K supported
coefficients are equal because numerator (Lm)! and
denominator products are equal separately.

It remains to prove terminality. Every old weight is at
most H=L/3. At k=2, no old weight or added 1 wraps
modulo L, so the age is precisely 2. For every
3<=k<=L-2, the 2H added unit weights alone contribute
\(2Hk/L=2k/3\ge2\) to the age; the old weights contribute
nonnegative fractional parts. Therefore every relevant
age is at least 2. The identity
\[
 \operatorname{age}(k)+\operatorname{age}(L-k)
 =N-z(k)\le N
\]
(where z(k) counts weights divisible in the relevant
modular sense) now gives every age at most N-2.
Thus both spaces are terminal.

The two multisets remain distinct, so the resulting
well-formed weighted projective spaces are nonisomorphic.
QED.

**Important qualification:** Theorem 4.1 does not assert
different **dimensions** for every K. It proves failure
of *uniform identification of the whole space* from a
fixed number of initial supported coefficients. Separate
dimension-changing examples are explicit for K=1 and K=2.

## 5. A finite positive reconstruction result

There is a complementary constructive theorem, also fully
proved but with mathematical priority unassessed.

**Theorem 5.1.** If the total weight L is known, the
first L supported coefficients, numbered m=0,...,L-1,
determine the entire weight multiset.

**Proof sketch.** The consecutive ratio is a rational
function
\[
 \frac{C_w(m+1)}{C_w(m)}
 =\frac{\prod_{j=1}^{L}(Lm+j)}
 {D_w(m)},\qquad
 D_w(x)=\prod_i\prod_{j=1}^{a_i}(a_i x+j).
\]
The denominator polynomial has degree L and contains
\((x+1)^N\), hence at least \((x+1)^2\). The quotient
\(Q_w=D_w/(x+1)^2\) has degree at most L-2.
The L known coefficients determine its values at
m=0,...,L-2, enough for unique interpolation. The roots
x=-1/a have multiplicity
\[
 M(a)=\sum_{b:\ a\mid b}n_b,
\]
where n_b is the number of weights equal to b. Descending
divisor inversion recovers all n_b uniquely. QED.

The earlier thesis work of Sara Veneziale already includes a
factorial-factorization approach to weight candidates from
truncated periods, and must be carefully compared before any
originality claim. Our proof concerns an explicit **uniform
sufficient bound depending on L** and exact interpolation.

## 6. Computational frontier for three coefficients

A C++ integer-partition census using prime-valuation signatures
and the exact terminality criterion has found **no collisions
for the first three positive supported coefficients through
L=70**. The current repository's hosted CI runs this complete
bounded search. It is not a mathematical theorem outside the
declared finite universe, nor does it contradict Theorem 4.1.

The next computational goal is a concrete terminal K=3
collision, for which the general existence theorem only
provides a large implicit bound. A useful intermediate
problem is to construct a valuation-kernel vector u with
\(\sum_a u_a\neq0\), which would automatically produce
different-dimensional matching examples after common
unit padding.

## 7. Verification standard and open work

Exact calculations use integer factorials, integer
prime valuations and rational polynomial interpolation.
The C++ code uses a bounded one-byte encoding for each
valuation, with explicit overflow checking. Independent
Python and C++ checks agree for the weight-51 results.
GitHub Actions checks tests on Python 3.11 and 3.13 and
performs independent bounded search jobs.

An honest promotion from research note to article requires:
(1) independent mathematical review; (2) extensive novelty
comparison with prior factorial-product identities and
quantum-period inversion; (3) optional formal proof of the
padding and nullspace lemmas in Lean; (4) formally or
externally audited enumeration coverage; and (5) source
data provenance for any imported benchmarks. No result
here establishes the general conjecture that complete
quantum periods uniquely determine all Fano varieties.

## References

1. Coates, Kasprzyk, Veneziale, *Machine learning the
   dimension of a Fano variety*, Nature Communications
   14 (2023), 5526, DOI 10.1038/s41467-023-41157-1.
2. Kasprzyk, *Classifying terminal weighted projective
   space*, Proposition 2.3 (terminality criterion).
3. Veneziale, *Fano Varieties and Machine Learning*,
   PhD thesis, Imperial College London (2024), §6.2.


## Appendix A. Three-term collisions and sharp maximal-weight restrictions (November 6, 2026)

The first exact three-supported-coefficient collision obtained by the new
prime-valuation relation engine occurs with *largest individual weight*
172 (not to be confused with minimum total weight, which remains open).
The two weight multisets are

```
A = [3,3,3,3,5,8,8,12,22,32,34,85,107,162,172]
B = [2,4,4,4,4,6,9,11,21,33,35,86,108,161,171]
```

Both have sum 659, 15 entries, and terminal quotient singularities.
Their first 3 supported coefficients are exactly equal; the fourth
coefficient ratio A/B is

```
65119987073340199 / 65119354660916775
```

so their full periods differ. The original factorial relations are
stored as compressed signed-multiplicity lists, independently verified
prime-by-prime, not as decimal approximations.

**Exact maximal-weight obstruction.** The valuation matrix
`V_3(M)` has columns indexed by candidate weights `1,...,M`,
and rows recording total weight and the prime valuations
`v_p((ma)!)` for `m=1,2,3`. Exact elimination modulo the
prime 1000003 shows rank `171` at `M=171`; thus *no*
nontrivial common-total-weight relation can use exclusively
weights below 172. The explicit relation at 172 proves this
maximal-weight threshold sharp even for terminal spaces.

The W172 relation is a count-zero kernel vector in
`V_3(188)`. Exact modular rank is 187 at M=188, so
the rational kernel has dimension one and every such
relation has zero coefficient-count sum. The second signed
identity at maximum weight 189 has 471810 positive and
471684 negative entries, a common total weight 27847032,
and meets all 3 factorial identities. Adding 378 common
unit weights gives terminal examples of dimensions
472187 and 472061, differing by 126. Thus **189 is the
minimal possible maximum individual weight for a
dimension-changing three-coefficient collision**.

A further signed relation at maximum weight 249 has
117549 positive and 117548 negative entries, each with
sum 9268001. Adding 498 common unit weights gives
terminal examples of dimensions **118046 and 118045**,
with total weight **9268499**. This yields an explicit
three-coefficient terminal collision whose dimension
difference is exactly one. No minimality of weight 249
or of the overall total weight is claimed for this
gap-one construction.

All three integer relation lists and the standalone
verifier are available at
`research/k3_exact_relations.json` and
`scripts/verify_k3_relations.py`. The verifier independently
checks exact prime-valuation cancellations and modular
rank bounds, and it directly checks all age inequalities
for the two 14-dimensional examples.

### A sharper terminal-padding lemma

For any nonempty positive weight multiset with total weight H
and maximum entry M, adjoining **2M unit weights** produces
a terminal, well-formed weighted projective space. Put
L=H+2M. If 2<=k<L/M, then no original weight wraps
modulo L and the fractional age is precisely k. If
k>=L/M, the added unit weights alone contribute
2Mk/L>=2. Complementary ages give the upper bound
N-2. This proves the claim without running enormous
lists of quotient-age calculations and improves the
crude 2H-padding construction used in Section 4.

### Four-term obstruction and retracted exploratory claim

Independent exact GF(2) elimination certifies full column rank
for `V_4(1500)`. A correctly typed C++ finite-field
implementation further proves full rank at maximum weight
**1691 over F_65521**. Thus no distinct weight
multisets with the same total weight and all individual
weights <=1691 can agree on their first four supported
coefficients, even without imposing terminality.

The first modular dependence occurs at weight 1692
over the tested field, but **no integer relation has been
extracted or certified there**. An earlier exploratory
large-prime implementation used 16-bit storage, producing
an incorrect proposed threshold of 1929; that claim
is withdrawn. The corrected check is
`scripts/verify_k4_rank.cpp`. This distinction
between a modular dependence and an exact rational
factorial identity is indispensable.

The full detailed proofs, evidence labels and caveats
are in `research/K3_SHARP_WEIGHT_THRESHOLDS.md`.
