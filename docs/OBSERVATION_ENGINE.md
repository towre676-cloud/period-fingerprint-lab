# Exact observation design engine

The engine accepts a model class, an ordered catalog of exact scalar observations, and an observation budget. It produces a **reconstruction certificate** or **exact indistinguishable candidates**, and ranks available follow-up measurements.

## Run

```sh
python -m periodlab.observation_engine examples/observation_period_collision.json --out collision.json
python verify_observation_engine.py collision.json
python -m periodlab.observation_engine examples/observation_rational_deficient.json --out deficient.json
python verify_observation_engine.py deficient.json
python -m periodlab.observation_engine examples/observation_rational_full_rank.json --out reconstruction.json
python verify_observation_engine.py reconstruction.json
python -m periodlab.observation_engine examples/observation_bounded_periods.json --out bounded.json
python verify_observation_engine.py bounded.json
python -m unittest discover -s tests -v
```

## Exact mathematical scope

* **Unrestricted `Q^n`:** for rational linear observations \(A:\mathbb Q^n\to\mathbb Q^k\), exact full column rank implies a reconstruction theorem for every rational vector. The certificate includes an invertible observed submatrix and its rational inverse. Rank deficiency implies indistinguishable vectors: the engine constructs a nonzero rational kernel witness. At least \(n-\mathrm{rank}(A)\) additional scalar sensors are necessary. A basis extension is a minimal-cardinality completion, **if** the supplied sensor catalog spans the entire dual space.
* **Finite rational model class:** enumerate the specified vectors and compute exact signatures. Injectivity is a reconstruction theorem **only on that finite class**, not for all vectors.
* **Finite weighted-projective model class:** enumerate explicit common-total-weight weight lists, or all admissible well-formed partitions of exactly one total weight \(L\le45\), optionally filtering dimension and terminality. Supported coefficients are factorial ratios at degrees \(Lm\). The **separate general theorem** `docs/FINITE_RECONSTRUCTION.md` states that, with known \(L\), coefficients \(c_0,\ldots,c_{L-1}\) reconstruct the entire weight multiset; the receipt records whether the budget includes indices \(1,\ldots,L-1\). A bounded collision-free enumeration does **not** prove general Fano reconstruction.

## Deciding which observation is missing

For a finite ambiguous class, `pair_separator` is the first available later sensor that separates the displayed witness pair, and `best_next` maximizes the number of currently indistinguishable **unordered candidate pairs** separated by one extra measurement. This is one-step optimal for that objective, not necessarily optimal over an adaptive policy. If at most 12 catalog sensors remain and at most 10,000 pairs are ambiguous, `minimum_completion` searches all subsets in increasing size and finds an exact smallest sensor set identifying the whole finite class. Otherwise it reports `not_computed`. Missing separators are explicitly null; a wholly nonseparating catalog is reported as insufficient.

For rational linear families the rank argument identifies a provably smallest independent sensor completion, and the pair-specific separator is a catalog sensor increasing the observed rank.

## Grounded examples

* Weights `(1,1,1,1,1,5,5,24)` and `(2,2,2,2,3,3,25)`, each with \(L=39\), agree at ordinary degrees 39 and 78. Degree **117** separates them with exact coefficient ratio **1080400/1002001**. They are **nonterminal**. This explicit two-model example does not prove bounded-search optimality.
* For a vector \(x,y,z\), observing \(x+y+z\) and \(x-y\) leaves a one-dimensional rational kernel. Measuring \(z\) gives a full-rank system. The engine constructs the null vector and the inverse.
* With \(L=7\), two supported coefficients separate all seven well-formed weight multisets in the declared enumerated class. This is **not** a universal two-coefficient theorem.

## Evidence limits

The independent `verify_observation_engine.py` does not import the discovery engine. It recomputes rational rank, verifies exact inverse matrix multiplication, checks nonzero null vectors, re-enumerates finite candidate classes, calculates factorial coefficients using prime valuations, checks signature hashes, and verifies reported separating measurements and minimum subsets. A green test verifies only the execution of the specified checks, not novelty, a Lean theorem, or arbitrary geometry. Inputs must use integer values or rational strings (e.g. `"1/7"`); floats are deliberately rejected.

Future integrations can supply new exact model families and sensor definitions while preserving proof scope, canonical candidates, and independent replay.

## Independent input validation

The standalone checker validates the model-family tag, rational dimensions,
sensor dimensions and names, exact scalar types, weight support, distinct
supported indices and catalog bounds without importing the engine normalizer.
A claimed linear separator must have numerically distinct rational values:
different spellings such as `0` and `0/1` do not establish separation.
Above 10,000 ambiguous pairs the verifier counts pairs without constructing
the quadratic pair list, and checks the `not_computed` completion claim.
