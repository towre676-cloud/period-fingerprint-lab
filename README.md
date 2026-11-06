# Period Fingerprint Laboratory

[![Exact period laboratory](https://github.com/towre676-cloud/period-fingerprint-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/towre676-cloud/period-fingerprint-lab/actions/workflows/tests.yml)

**Research release candidate — finite reconstruction and terminal-collision certification**, Python 3.11+ (standard library). A computational laboratory investigating which geometric properties can be deduced rigorously from finite segments of regularized quantum periods.

## Exact mathematical core

- Weighted projective spaces: canonical weight multisets, well-formedness and exact terminal-singularity tests, supported factorial-ratio coefficients, rational recurrences.
- **Constructive reconstruction theorem:** Given the total weight `L=sum(weights)`, the first **L** supported period coefficients uniquely determine the full weight multiset, not just dimension. With the entire ordinary zero-inclusive period prefix through degree `L(L-1)`, the support step `L` can itself be recovered. See [proof](docs/FINITE_RECONSTRUCTION.md). This is an elementary derivation; its novelty has **not** been established.
- Bounded exhaustive collision census, explicit finite-prefix counterexamples, first distinguishing degrees. An independent census replayer confirms **425,291 terminal well-formed spaces and zero two-prefix collisions through total weight 45**; see [finite census](docs/TERMINAL_CENSUS.md).
- Exact prime-valuation integer-relation search through rational nullspace computations; conditional collision witnesses, not an all-K existence theorem.
- [External dataset adapter](docs/PUBLISHED_DATA.md) for the published 150,000 terminal WPS records (full external audit pending).
- JSON collision and unique-reconstruction receipts checked by an **independent standalone validator** (`verify_receipt.py`).
- A limited nonnegative-rank-two charge-model coefficient generator, benchmarked on `P¹ × P¹`.
- A local [browser explorer](web/index.html) using BigInt, no dependencies, plus a [loopback-only JSON HTTP API](docs/LOCAL_API.md) using the Python core.

## Quick start

```sh
python -m unittest discover -s tests -v
python -m periodlab analyze --weights 1,1,1,2 --count 6
python -m periodlab reconstruct --total-weight 3 --coefficients 1,6,90
python -m periodlab search --max-sum 40 --prefix 2 --different-dimensions
python -m periodlab search --max-sum 30 --prefix 2 --terminal-only
python verify_census.py --max-sum 45 --prefix 2 --expect-well-formed 513020 --expect-terminal 425291 --expect-collisions 0 > terminal-census.json
python -m periodlab.server --port 8765
```

Produce and replay a collision certificate:

```sh
python -m periodlab certificate --left 1,1,1,1,1,5,5,24 --right 2,2,2,2,3,3,25 --matching 2 > collision.json
python verify_receipt.py collision.json
```

Produce and replay a reconstruction receipt:

```sh
python -m periodlab reconstruction-certificate --total-weight 3 --coefficients 1,6,90 > reconstruction.json
python verify_receipt.py reconstruction.json
```

## New research results (November 2026)

We have now derived and independently computed three closely related
results; see the [research status](research/STATUS_2026-11-05.md):

1. **Sharp bounded terminal threshold (two supported coefficients):**
   Exhaustive exact enumeration through total weight 51 finds no terminal
   collision for smaller weights and exactly 77 two-space collision groups
   at weight 51. All 77 pairs differ in dimension, and are obtained by
   appending the same partition of 12 to a fixed base pair.
   [Proof and classification](research/terminal_collision_51.md).
2. **Explicit smallest terminal example:** the weight lists
   `(1,1,1,1,1,5,5,12,24)` (dimension 8) and
   `(2,2,2,2,3,3,12,25)` (dimension 7) agree in the first two
   supported coefficients at degrees 51 and 102, but differ at degree 153.
3. **Universal fixed-prefix ambiguity theorem:** for each finite K
   there are distinct terminal well-formed weighted projective
   spaces of a common total weight with the same first K positive
   supported period coefficients. The construction uses exact
   prime-valuation integer linear algebra, the prime number theorem,
   and unit-weight padding. The proof **does not** show distinct
   dimensions for every K.
   [Read the proof](research/universal_finite_prefix_ambiguity.md).
4. **Three-coefficient search:** no terminal three-supported-coefficient
   collisions through total weight 70 in an exact C++ enumeration;
   further independent replay and a larger frontier remain open.
   [Scope](research/three_prefix_frontier.md).

All novelty claims are deferred until relevant earlier mathematical
literature is compared. Numerical searches have explicitly bounded
domains and are not a general classification of Fano varieties.

## Exact finite-prefix collision

Exhaustive enumeration of 201,882 well-formed weight multisets with total weight ≤ 40 found a first two-coefficient collision at total weight 39:

| Space | Weights | Dimension |
|---|---|---|
| A | `1,1,1,1,1,5,5,24` | 7 |
| B | `2,2,2,2,3,3,25` | 6 |

Both have identical supported coefficients at degrees 39 and 78. At degree 117 the exact ratio A/B is **1080400/1002001**. Both spaces are **nonterminal**: this does not establish a counterexample inside the terminal weighted-projective subclass.

The census is finite and its exclusion scope is exactly the set defined in the search implementation. A pairwise collision receipt proves the reported equality and difference, **not** the exhaustiveness or uniqueness of the search.

## What has not been solved

This is not general reconstruction of Fano varieties; it does not prove or disprove the full-period uniqueness conjecture. It does not validate arbitrary rank-two charge matrices as projective fans, claim terminality for the example above, or identify quantum periods with other geometric periods. The local browser is a demonstration, not an independent scientific proof assistant. Sources and the evidence classification appear in [Evidence and Scope](docs/EVIDENCE_AND_SCOPE.md).

## Roadmap

See [the complete staged plan](docs/ROADMAP.md). Priorities are stronger independent exclusion certificates; datasets with integrity manifests and provenance; toric fan validation; additional period-generation methods; and effective uniqueness thresholds for restricted families.

## Mathematical literature

Coates, Kasprzyk and Veneziale, *Machine learning the dimension of a Fano variety*, Nature Communications **14** (2023), 5526. [DOI](https://doi.org/10.1038/s41467-023-41157-1).

Kasprzyk, *Classifying terminal weighted projective space*, exact terminality criterion, [source](https://kasprzyk.work/research/pdf/Terminal_Wps.pdf).

The project was inspired by 2023–2024 mathematical conversations recovered in a separate research excavation. No personal historical chat data are published in this repository.

MIT-licensed software.