# Reconciliation: Period Fingerprints × PerfectJet × Singularity

The shared mathematical object across these projects is an exact **observation
map**. However, the inverse problems are fundamentally different:

- Period Fingerprint: recover a *discrete* weight multiset from exact
  factorial-ratio coefficients; finite prefixes can collide.
- Singularity: recover a rational linear coefficient vector under a
  declared adversarial noise model. Rational sensor optimization uses a
  different operator norm / dual certificate.
- PerfectJet: exact polynomial operator algebra, kernels, rank strata, and
  proof-carrying rational computations. It is a natural provider of algebraic
  tools, not evidence that period sequences arise from Hamiltonian flows.
- Selmer: independently check arithmetic in rational quotient algebras;
  prime valuations and integer kernel witnesses can share certificate
  infrastructure, but no implication for Selmer groups follows.

## Reconciled capability 1: exact finite-class identification

Given a **declared finite list** of validated weighted-projective spaces
of common known total weight L, an allowed set of supported indices, and
an observation budget, `periodlab.observation_design` exhaustively
searches for a minimum-size **nonadaptive coefficient panel** separating all
models, if possible within budget. Otherwise it reports exact model
collisions, the strongest partial panel, and a suggested next index.

The complexity cap is enforced *before enumeration*; exceeding it raises an
error and does not issue an optimality certificate.

Example: the existing two-prefix collision

[
(1,1,1,1,1,5,5,24),qquad (2,2,2,2,3,3,25)
]

has total weight L=39, identical coefficients at supported indices m=1,2,
and distinct coefficients at m=3. An exact panel containing just m=3
separates these **two** supplied candidates, even though no panel using
only m=1,2 does.

This is a *finite-candidate-class* result. It does not contradict either
the universal fixed-K terminal collision constructions or the known-L
finite reconstruction theorem for all well-formed weighted projective
spaces. In that larger class, the first L supported coefficients are
sufficient for unique reconstruction, by polynomial interpolation and
root multiplicity inversion.

Every panel receipt is independently rechecked using
`verify_observation_bridge.py`, which does not import periodlab.

## Reconciled capability 2: exact differential operator from period ratio

For weights a_i and L=sum_i a_i, the supported quantum-period model is

[
c_m=rac{(Lm)!}{prod_i(a_i m)!}.
]

Define two polynomials

[
P_L(X)=prod_{j=1}^{L}(LX+j),qquad
D_w(X)=prod_iprod_{j=1}^{a_i}(a_i X+j).
]

The exact recurrence is

[
D_w(m)c_{m+1}=P_L(m)c_m.
]

For the supported-index series
(F(z)=sum_{mge0}c_mz^m) and
(	heta=zrac{d}{dz}), the exact annihilator is

[
oxed{(D_w(	heta-1)-zP_L(	heta)),F(z)=0.}
]

The constant-term equation holds since D_w(-1)=0. This is a
**holonomic annihilator**, not necessarily the minimal Picard–Fuchs
operator. A separate geometric comparison would be necessary before
identifying it as the canonical Picard–Fuchs operator of a given Fano.

`periodlab.holonomic` exports the rational/integer polynomial
coefficient lists and exact recurrence receipts. The standalone verifier
rebuilds the factor products and all specified coefficients independently.

This supplies an honest input bridge for PerfectJet's polynomial-operator
machinery and a future formal Lean proof: these are polynomial identities
in a derivation operator, not a claimed equivalence with Moyal dynamics.

## Open research and scope boundaries

1. Promote the discrete panel-search certificate into an adaptive
   decision-tree algorithm, measuring worst-case and expected number of
   coefficient queries separately.
2. Use valuation matrices to find compact **explicit K=5 integer relations**
   (the repository has bounds and existence results, not a compact witness).
3. Explore differential-operator order reduction and right-factor
   certificates, checking independently whether an operator is minimal.
4. Extend from rank-one weighted-projective factorial ratios to
   geometrically validated rank-two toric charge systems, with an
   independent Laurent-polynomial period generator.
5. Check theorems in Lean: exact factorial recurrence, interpolation and
   Möbius root-multiplicity reconstruction, and bounded observation
   panel certificate validity.
6. Treat all geometric claims as class-relative: the finite reconstruction
   theorem does not hold for arbitrary Fano periods, and a collision at
   finite K does not imply equal full infinite periods or identical geometry.

The exact measurement optimization theorem for Singularity's
(ell_1)-normalized rational sensors is not imported as a theorem about
these discrete observations. Its useful transferable lesson is instead
*specifying the sensor class and proving optimality within it*.
