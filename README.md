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

## Latest exact results: compact K=4 witness and K=5 exclusion

A new exact **terminal** collision has been constructed with matching
first **four** supported period coefficients and **different dimensions**,
without artificial unit-weight padding:

| | Space A | Space B |
|---|---:|---:|
| Dimension | **12,621** | **12,622** |
| Weight sum | 6,448,232 | 6,448,232 |
| Number of weights | 12,622 | 12,623 |
| Terminal-age failures | 0 | 0 |

The 706 nonzero signed weight multiplicities are preserved as an exact
[compressed vector](research/k4_compact_vector.b85) and independently
checked by [verify_k4_compact.py](scripts/verify_k4_compact.py).
Prime valuations match for all m=1,2,3,4 and differ at **367 primes**
for m=5. All **6,448,229** relevant terminality ages per space are
checked with integer arithmetic. This improves the previous explicit
astronomical-size K=4 example by over 33 orders of magnitude in
common weight sum. It is not proved minimal in dimension or total sum.

[Mathematical scope and proof details](research/K4_COMPACT_TERMINAL_COLLISION.md).

**New K=5 algebraic obstruction:** the prime-field valuation matrix
has full rank for candidate individual weights through **25,808**.
This excludes any nontrivial *common-total-weight* match of the first
five supported coefficients where all individual weights are at most
25,808. The characteristic-65521 first modular dependency at 25,809
is **not** yet a genuine rational/integer collision.

[Exact K=5 proof and reproduction](research/K5_FINITE_RANK_BOUND.md).

## New: exact four-coefficient terminal collision

An exact integer relation supported on individual weights through **1692**
makes the first **four** positive supported quantum-period coefficients
identical for two different weighted-projective weight multisets. Their
fifth coefficients differ, and the original multisets have different
numbers of weights. Adding **3384 common unit weights** gives two
well-formed **terminal** weighted projective spaces of *different dimensions*.

This is **sharp in maximum individual weight**: an independently computed
full-column-rank certificate modulo the prime 65521 excludes any
nontrivial relation using only weights at most **1691**.
The total weights and geometric dimensions of the explicit pair are
very large and are **not** claimed minimal.

The full **587-entry signed integer witness** is reconstructed from
15 independent modular computations by Chinese remaindering and
rational reconstruction, then verified by exact prime valuations for
m=1,2,3,4,5. GitHub Actions publishes the resulting JSON as the
`certified-k4-collision` artifact after successful verification.

[Read the exact result and reproduction instructions](research/K4_EXACT_TERMINAL_COLLISION.md).

```sh
g++ -std=c++20 -O3 -Wall -Wextra -o /tmp/extract_k4_mod scripts/extract_k4_mod.cpp
# See the research note for the complete fifteen-prime loop.
python scripts/reconstruct_k4.py /tmp/k4
```

## New: terminal collisions through three coefficients and certified maximal-weight bounds

The exact three-prefix research now includes three independently replayable
signed factorial identities in
[`research/k3_exact_relations.json`](research/k3_exact_relations.json):

- **Maximum weight 172:** terminal dimensions 14 and 14, common total weight
  659, with the first 3 supported coefficients equal and the fourth unequal.
- **Maximum weight 189:** the **first possible maximum individual weight
  for a dimension-changing** three-prefix relation; terminal dimensions
  472,187 and 472,061 after common unit-weight padding.
- **Maximum weight 249:** a compressed terminal collision with a
  **dimension difference of exactly one**, dimensions 118,046 and 118,045.

The sharp thresholds 172 and 189 are certified by independent modular
rank computations and the explicit exact integer relations. These are
**not** minimality statements for total weight or dimension.

A separate exact finite-field proof shows that **four supported coefficients
cannot collide when all individual weights are at most 1,691** and the
total weights are equal. The first modular dependence at weight 1,692 is
not yet an integral factorial identity.

[Read the mathematical proofs and evidence limitations](research/K3_SHARP_WEIGHT_THRESHOLDS.md).
Run the independent checkers:

```sh
python scripts/verify_k3_relations.py research/k3_exact_relations.json
g++ -O3 -std=c++20 -Wall -Wextra -o /tmp/weight_rank scripts/verify_k4_rank.cpp
/tmp/weight_rank 1691 4
```

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