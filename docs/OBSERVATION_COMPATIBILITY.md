# Observation planner and engine compatibility

This integration preserves three different mathematical contracts. Sharing
exact data does not turn a finite-model identification claim into an inverse
theorem on an unrestricted domain.

## API contracts

| Component | Inputs and budget meaning | Certified conclusion |
| --- | --- | --- |
| `observation_design.design_exact_observations` | Explicit validated WPS models of one known total weight; a finite sequence of allowed positive supported indices; maximum panel size | Minimum separating nonadaptive panel, if attainable within budget; otherwise maximum separated-pair count among budgeted panels and an exact unresolved pair |
| `observation_engine.analyze`, finite families | Explicit rational vectors, explicit WPS models, or a bounded WPS enumeration; ordered sensor catalog; budget selects the first entries | Identification or collision on precisely that finite class; a pair separator, best next sensor, and minimum additional completion when the search cap permits |
| `observation_engine.analyze`, `all_rational` | Rational linear sensors on all of Q^n; budget selects the first sensor rows | Full column rank gives an exact inverse using an observed row basis; deficient rank gives a nonzero kernel witness; full catalog rank determines whether completion is possible |
| `holonomic.holonomic_receipt` | One WPS weight multiset and a recurrence-check count | Exact factorial-ratio polynomial annihilator; no claim of minimal order, candidate identification, or unrestricted geometric equivalence |

The planner sorts allowed indices and retains model input order. The engine
retains sensor order and sorts models canonically. Map candidates by their
weight tuples and sensors by supported index, never by coincidental list
position. Engine completion entries are **1-based catalog positions**, not
supported indices.

The planner's upfront cap counts all panels of sizes zero through the allowed
budget, even if search could stop early. It raises instead of emitting a
partial optimality claim when that count exceeds `max_panels`. The finite
engine searches minimum additions only with at most 12 remaining sensors and
at most 10,000 ambiguous pairs; otherwise it explicitly reports `not_computed`.
The checker now counts pairs without allocating a quadratic list above that
boundary. These resource contracts remain distinct.

The planner's best-next tie rule uses the smallest supported index after
maximizing newly separated pairs. The engine further minimizes the worst
remaining class and then uses catalog order. Equal separation counts do not
guarantee identical tie choices in arbitrary examples.

## Reproducible weight-39 comparison

Let A=(1,1,1,1,1,5,5,24), B=(2,2,2,2,3,3,25). Both are well formed
and nonterminal. Their total weight is 39. For

    c_m(w) = (39m)! / product_i (w_i m)!,

c_1(A)=c_1(B), c_2(A)=c_2(B), and

    c_3(A) / c_3(B) = 1080400 / 1002001 != 1.

Thus the third supported coefficient has ordinary degree 117.

| Request | Planner | Engine |
| --- | --- | --- |
| Only indices 1 and 2 available | Cannot separate the pair; the optimal partial panel may be empty because neither index separates any pair | A prefix containing indices 1 and 2 has an exact collision and no available completion |
| Catalog [1,2,3], budget 1 | Chooses [3] and separates the two candidates | Measures index 1 and still has a collision |
| Catalog [1,2,3], prefix budget 2 | Not the planner's fixed-prefix contract | Reports index 3 / ordinary degree 117 as the next separator and minimum one-sensor completion |
| No observations yet, catalog [1,2,3] | Minimum separating panel [3] | Minimum completion is catalog position 3, which denotes supported index 3 |
| Planner's chosen panel placed first: [3,1,2], budget 1 | Panel [3] separates | Prefix [3] separates the same finite pair |

No new production optimizer or universal receipt adapter is introduced.
The cross-contract test maps data explicitly, keeps both native formats, and
checks mathematical facts using both independent implementations.

Run from a checkout containing both repaired contributions:

```sh
python -m unittest discover -s tests -p 'test_observation_compatibility.py' -v
python -m scripts.replay_observation_compatibility --out /tmp/observation-replay
python -m unittest discover -s tests -v
```

The replay script writes receipts and a summary, copies both standalone
checkers to a temporary directory without `periodlab`, and runs them with
`python -I`. It covers both weight-39 holonomic receipts, both observation
contracts, all four existing engine examples, and three rejected corruptions.
The regression also covers every well-formed WPS model at each total weight
4, 7, 9, and 12, candidate reordering, rational versus finite scope, and
tampered common coefficient evidence.

## Certificate reuse and independence

The reusable mathematical evidence consists of canonical weight multisets,
the known support step L, supported-index-to-degree mapping m -> Lm, exact
coefficient strings, collision pairs, and actual separating values. Preserve
the finite universe and observation provenance alongside these values.
The engine's table hash is a reproducibility check, not a substitute for
recomputing the coefficient table.

Both discovery components already reuse `periodlab.weights` and
`periodlab.periods`. Keep their standalone verifiers independent: the bridge
uses factorial division, and the engine uses prime valuations. They agree
on common data but do **not** accept each other's receipt formats. Neither
checker calls the other's discovery algorithm or verifier. A future format
adapter must not translate a bounded claim into a stronger one or discard
the original scope, ordering, or optimization objective.

One existing field needs careful interpretation:
`known_weight_reconstruction_theorem_applies` in the planner checks whether
the **allowed catalog** contains indices 1,...,L-1. It does not say the selected
panel observed them. The engine's `known_weight_theorem.covered_by_budget`
checks the **observed prefix** instead. A regression keeps this distinction
explicit rather than renaming or silently changing a v1 field.

The separate known-L theorem uses c_0,...,c_(L-1), including c_0=1, and is
restricted to the stated WPS factorial-ratio class. For L=39, its sufficient
positive-index set is 1,...,38; separation of two supplied candidates by c_3
does not prove general reconstruction from one or three coefficients.

For the holonomic bridge, factorial cancellation proves
D_w(m)c_(m+1)=P_L(m)c_m for every nonnegative m. With theta=z*d/dz, this yields
[D_w(theta-1)-z P_L(theta)]F=0; D_w(-1)=0 supplies the constant term.
The checker rebuilds the factor products as well as the finite sampled
recurrences. Finite samples alone are not a proof of an arbitrary sequence's
differential equation. No minimal Picard-Fuchs claim or equivalence among
Period Fingerprint, Singularity, and PerfectJet follows.

## Repairs and integration order

PR #1's repaired tampering test uses named subtests and verifies each expected
`ValueError`; signature corruption is covered as well. The public index API
accepts finite sequences including `range`, rejects floats/booleans/duplicates
and unsized iterators, and checks the combinatorial cap before any coefficient
evaluation.

Review also reproduced three checker defects in PR #2: accepting float
sensors, truncating dimension-mismatched finite linear sensors with `zip`,
and accepting numerically equal separator readings spelled `0` and `0/1`.
Its repair validates the contract independently and compares rational values
numerically. The discovery API and existing valid receipt formats are retained.

Recommended sequence, subject to the user's explicit approval: push the
isolated repairs to their respective PR branches and obtain green remote CI;
merge repaired PR #2 first; update PR #1 onto that main, add this compatibility
test/script/workflow change, and rerun remote CI before merging PR #1. The
prepared local combination merged without conflicts. Retain separate public
entry points and independent verifiers; do not create a third optimizer to
wrap their overlapping but different objectives.
