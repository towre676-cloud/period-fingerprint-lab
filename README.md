# Period Fingerprint Laboratory

An exact, reproducible investigation of what a finite list of regularized
quantum-period coefficients can and cannot determine about the dimension
of a weighted projective space.

## Quick start

Python 3.11+; no third-party packages:

```sh
python period_fingerprint_demo.py
python period_fingerprint_demo.py --skip-search
python -m unittest discover -s tests -v
```

The default run enumerates **201,882** well-formed weight multisets with
total weight at most 40 (within the tested search convention), checking
their first two nonzero period coefficients exactly. Its first collision
occurs at total weight 39:

- A = (1,1,1,1,1,5,5,24), weighted-projective dimension 7
- B = (2,2,2,2,3,3,25), weighted-projective dimension 6

They share the coefficients at degrees 39 and 78, but **differ at degree 117**,
with exact coefficient ratio A/B = 1080400/1002001.

For weights `a = (a₁, ..., a_N)` and `L = sum(a)`, the source-dependent
weighted-projective period formula used is

`c_(L*m) = (L*m)! / product_i (a_i*m)!`, and all off-lattice coefficients
are zero. Consequently `dim = N-1`. The prototype also checks exact
successive-coefficient ratios and the limiting dimension estimator
based on second differences of logarithms.

## Scope, caveats, and evidence

This is a computational observation about finite truncations within the
specified class and search bound, **not** a demonstrated novel theorem.
The asymptotic dimension-recovery framework and broad period-fingerprint
research predate this project; see Coates–Kasprzyk–Veneziale,
*Machine learning the dimension of a Fano variety*,
Nature Communications 14 (2023), DOI
https://doi.org/10.1038/s41467-023-41157-1 .

This code does **not** reconstruct arbitrary Fano varieties, prove
birational/isomorphism classification, certify terminal singularities,
or identify these quantum periods with annular-period local systems.
The census is finite and the minimum-weight claim refers only to the
precise enumeration assumptions used in the script.

## Development direction

1. Export machine-readable collision certificates (weights, coefficients,
   prime-valuation equalities, first distinguishing degree).
2. Extend exact collision searches to longer coefficient prefixes and
   bounded weights, with reproducible checkpoints.
3. Prove finite-prefix obstruction theorems and investigate which additional
   geometric restrictions restore dimension identifiability.
4. Implement independent coefficient generation and exact rational
   recurrence certificates.
5. Compare against published Fano period datasets only after recording
   identity, provenance, and admissible singularity classes.

Historical inspiration: March and April 2024 research conversations recovered
in the excavation. Their prior assistant-produced equations are not accepted
as proofs.
