# Full laboratory roadmap and completion gates

## v0.2 — exact weighted-projective foundation (implemented)

- Exact integer coefficients and support checking.
- Well-formedness and terminality predicates (Kasprzyk criterion).
- Finite-weight reconstruction with known sum.
- Pairwise collision JSON receipts and bounded search.
- Basic rank-two nonnegative-charge factorial sum.
- Local static browser preview.
- Python 3.11/3.13 standard-library CI.

**Gate:** all committed tests pass on current HEAD, and the CLI smoke
test passes on current HEAD. This is not a release of the general engine.

## v0.3 — certificate strengthening (next)

- Strengthen the existing independent standalone verifier with automatic
  proof-obligation coverage reports.
- Extend existing reconstruction JSON certificates with explicit root
  multiplicities and integer-nullspace signatures.
- Self-contained bounded census manifests and enumeration replay.
- Constraint-solving search by factorial-prime valuations and
  combinatorial linear algebra; retain an independent enumerator.
- Source-level mathematical review of terminality, exceptional cases.

**Gate:** verifier rejects deliberately corrupted receipts and verifies
all known good fixtures, including terminality witnesses.

## v0.4 — proven-family databases

- Obtain source datasets and cite original URLs, access dates and licenses.
- Validate types, normalizations, support degrees and duplicates.
- Published terminal WPS and rank-two example matching.
- Hold out entire geometry families during ML evaluation.
- Avoid treating prediction accuracy as reconstruction uniqueness.

**Gate:** machine-reproduced numerical reference tables with
content-addressed raw inputs and explicit mismatch ledger.

## v0.5 — broader geometry and effective bounds

- General toric fan and charge-matrix validation.
- Genuinely independent Laurent polynomial period engine.
- Rational recurrence and Picard–Fuchs differential-operator inference.
- Certified bounds for finite data and sharp restricted-family results.
- Optional SageMath interface, CPU profiling and parallel search.

**Gate:** independently computed coefficients agree on all comparable
benchmark families, and theorem hypotheses are machine-checkable.

## v1.0 — review-ready research tool

- Stable Python API and documented CLI.
- Browser UI with certificate upload and verification.
- Reproducible datasets, exact receipts, package/release hashes.
- Full security/validation audit, documented complexity and limits.
- Mathematical paper with proofs and precise novelty comparison.

**Gate:** clean install in an independent environment; reviewer replay
of all headline claims from the published release.

## Not implied by v1.0

A general solution to the Fano quantum-period uniqueness conjecture,
a complete classification of all terminal toric varieties, or a
proof that the quantum periods determine dimension for all Fano varieties.
