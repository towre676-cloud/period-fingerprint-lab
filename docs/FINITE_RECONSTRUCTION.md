# A constructive finite-weight reconstruction theorem

**Status: proved here by elementary polynomial interpolation and root
multiplicity inversion.** Whether this precise formulation or bound appears
already in the literature has not been determined. Do **not** claim novelty.

## Statement

Let `w=(a_1,...,a_N)` be a well-formed collection of positive integer
weights, `N>=2`, and suppose the **total weight L=sum_i a_i is known**.
Write `c_m=(Lm)!/prod_i (a_i m)!`, the nonzero-support coefficients of
the regularized quantum period. Then **the first L values
`c_0,c_1,...,c_(L-1)` uniquely determine the entire multiset of
weights** among such collections, hence determine dimension `N-1`.

The theorem presupposes the coefficient formula and the fixed total
weight; it is NOT a reconstruction theorem for arbitrary Fano varieties.
The coefficient notation here abbreviates support degree `Lm`.

## Proof (exact)

Define the consecutive coefficient ratio

`r(m)=c_(m+1)/c_m=P_L(m)/D_w(m)`,

with

`P_L(x)=prod_{j=1}^L (L*x+j)` and
`D_w(x)=prod_i prod_{j=1}^{a_i} (a_i*x+j)`.

Both polynomials have degree L. Every weight `a_i` contributes the
factor `a_i*(x+1)` (its `j=a_i` term), so `D_w(x)` is divisible
by `(x+1)^N`, in particular by `(x+1)^2`. Set
`Q_w(x)=D_w(x)/(x+1)^2`. This is a polynomial of degree at most
`L-2`. For integers `m=0,...,L-2`, the known coefficients determine

`Q_w(m)=P_L(m)*c_m/((m+1)^2*c_(m+1))`.

There are `L-1` samples. Unique polynomial interpolation determines
`Q_w` exactly; multiplication by `(x+1)^2` recovers `D_w`.

For each `a=1,...,L`, let `M(a)` be the multiplicity of root
`x=-1/a` in `D_w`. A factor `b*x+j` has this root precisely
when `j=b/a` is integral, i.e. when `a` divides `b`. If
`n_b` is the number of times weight `b` appears, then

`M(a)=sum_{b: a divides b} n_b`.

Descending inversion yields

`n_a=M(a)-sum_{b>a, a divides b}n_b`.

Thus all `n_a` are uniquely determined. End of proof.

## Algorithm and certificates

`periodlab.reconstruct.reconstruct_weights(L, coeffs)` interpolates
the quotient exactly with rational Newton differences, recovers rational
root multiplicities by synthetic division, performs descending inversion,
checks that weights are positive and well-formed, and recomputes *all*
supplied coefficients by an independent recurrence.

`python -m periodlab reconstruct --total-weight 3 --coefficients 1,6,90`

returns weights `[1,1,1]` and dimension 2.

For a certificate that can be checked *without* the original algorithm,
save the prefix, interpolated polynomial coefficients, the rational root
multiplicities and reconstructed weight list, then independently
evaluate `D_w` and the input series. The current code exports the original supported coefficients, the recovered
rational polynomial and the reconstructed weights in a JSON receipt. The
separate top-level `verify_receipt.py` checks the reconstructed polynomial,
all samples, terminality and uniqueness hypotheses without importing the
discovery engine.

## Limitations

- `L` must be supplied. An observed finite series with many initial
  zero coefficients does not necessarily determine the support step.
- The bound `L` is sufficient, not shown optimal.
- This is a theorem about weight multisets, not isomorphism classes of
  arbitrary toric varieties, singularity classifications, or smooth Fanos.
- The finite two-term collision at total weight 39 is compatible with
  this theorem, because 2 is less than 39.
- A function of a finite prefix with a deliberately restricted candidate
  class can achieve smaller bounds. A rigorous claim requires specifying
  that candidate class.
