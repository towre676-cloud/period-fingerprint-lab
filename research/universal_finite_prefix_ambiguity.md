# Theorem: no universally sufficient fixed number of supported coefficients

**Status:** Mathematical proof, independent of the bounded census.
No assertion of originality is made. The class is terminal,
well-formed weighted projective spaces, not all Fano varieties.

## Statement

For every positive integer K there exist two *nonisomorphic* terminal,
well-formed weighted projective spaces with the same total weight L,
whose first K positive supported coefficients of the regularized
quantum period are identical.

This does **not** assert that their dimensions differ for every K.
Dimension mismatch is established explicitly for K=1 (weight 9)
and K=2 (weight 51). Nor does the theorem imply that the full
infinite periods agree: they cannot, by established asymptotic
dimension recovery or the finite weight-reconstruction theorem
where L is known.

## Proof

Fix K. Choose M sufficiently large so that

`1 + K * pi(K*M) < M`,

where pi(x) counts the primes at most x. Such M exists by the
prime number theorem: pi(K*M)=O_K(M/log M).

For each candidate weight a=1,...,M, form an integer column v(a)
consisting of the initial coordinate a and, for each
m=1,...,K and prime p<=K*M, the valuation

`v_p((m*a)!)`.

The resulting integer matrix has M columns and at most
`1+K*pi(K*M)` rows, hence it has a nonzero rational kernel
vector. Clearing denominators yields an integer vector u != 0
with `sum_a a*u_a=0` and

`sum_a u_a*v_p((m*a)!)=0`

for all the listed m,p. The first equation, together with all
a>0, forces u to contain both positive and negative entries.

Let U and V be the positive and negative multisets encoded by u.
They are distinct and have a common positive total weight H.
Unique prime factorization implies

`prod_(a in U) (m*a)! = prod_(a in V) (m*a)!`

for m=1,...,K.

Append `r=2H` unit weights to **both** U and V.
The new common total weight is `L=3H`, and the first K supported
regularized quantum-period coefficients agree exactly, since their
common numerator is (Lm)! and the added denominator factor (m!)^r
is the same on both sides. Both weight lists are well-formed,
because they contain at least two unit weights.

To verify terminality using the exact published fractional-age
criterion, take k=2,...,L-2. At k=2 every weight is less than L/2
(the old weights are each <=H=L/3), so the total fractional age
equals exactly 2. At k>=3, the r=2H added unit weights contribute
`r*k/L=2k/3 >= 2` to the age, while the other weights make a
nonnegative contribution. All ages are integers because the sum
of the weights equals L. The complementary identity

`age(k)+age(L-k)=N-z(k) <= N`,

where z(k) counts weights with k*a divisible by L, now gives
`age(k)<=N-2` as age(L-k)>=2. Thus all ages lie in [2,N-2],
so both weighted projective spaces have terminal quotient
singularities.

The two multisets remain distinct and, as well-formed weighted
projective spaces, define nonisomorphic varieties. QED.

## Interpretation

Every *fixed* K can be defeated by sufficiently high-dimensional
terminal examples, even when observing the first K **nonzero,
supported** coefficients and knowing the common support step L.
This is a genuine restriction on uniform finite-identifiability
theorems without a bound on L or dimension. It does not contradict
the fact that each fixed weighted projective space can be recovered
from sufficiently many coefficients.

The construction is existential, uses PNT, and offers no practical
small bound for L as a function of K. The 51-weight K=2 construction
is an explicit and substantially smaller witness.
