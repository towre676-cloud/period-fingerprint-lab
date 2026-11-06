# Bounded terminality-constrained collision census

**Scope:** all canonical nondecreasing, well-formed weight multisets
with total weight `L <= 45`, at least two weights, and at worst
terminal singularities. Terminality uses the exact Kasprzyk fractional-age
criterion in dimension ≥3 and smoothness in dimensions ≤2.
The fingerprint comprises the first two **positive** supported
coefficients at degrees `L` and `2L`; the support step is included.

## Results

| Maximum total weight | Well-formed spaces | Terminal spaces | Terminal two-prefix collision pairs |
|---|---:|---:|---:|
| 40 | 201,882 | 158,816 | 0 |
| 45 | **513,020** | **425,291** | **0** |

The unrestricted well-formed search has a *nonterminal* pairwise collision
at `L=39`, with weights
`(1,1,1,1,1,5,5,24)` and `(2,2,2,2,3,3,25)`, dimensions 7
and 6; they first differ at degree 117.

The bound 45 was independently computed with the legacy partition
enumerator and a separate inline terminal-age predicate. The standalone
`verify_census.py` uses a second iterative partition generator and
an independently written coefficient and terminality evaluator;
GitHub Actions is configured to check the 45 bound. A successful
current-HEAD CI run is required before describing the GitHub
independent replay as completed.

## Reproduce

```sh
python verify_census.py --max-sum 45 --prefix 2 \
  --expect-well-formed 513020 --expect-terminal 425291 \
  --expect-collisions 0 > terminal-census-45.json

python -m periodlab search --max-sum 45 --prefix 2 --terminal-only
```

The production search has a conservative max_sum<=45 bound; the local
HTTP API limits searches to 40 for responsiveness.

**No global theorem follows from this finite result.** It makes no
claim about total weight 46 or higher, an unknown unrestricted class
of terminal spaces, or uniqueness from fewer or differently normalized
coefficients. Exhaustiveness is relative to the weight-domain
definition and correctness of the two enumeration implementations.
The separate receipt verifier checks individual mathematical
certificates, not global classification.
