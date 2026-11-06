# Bounded terminality-constrained collision census

**Scope:** all canonical nondecreasing, well-formed weight multisets
with total weight `L <= 40`, at least two weights, and at worst
terminal singularities. The terminality check uses the exact
Kasprzyk age criterion in dimension >=3 and smoothness in
dimension <=2. The period fingerprint is the first two **positive**
nonzero supported coefficients, at degrees `L` and `2L`;
the support step `L` is part of each fingerprint.

## Computed result

- Well-formed spaces in unrestricted search: **201,882**.
- Spaces passing the terminality predicate: **158,816**.
- Pairs of distinct terminal spaces with the same `(L,c_L,c_(2L))`:
  **zero**.
- The unrestricted search has a nonterminal collision already
  at `L=39` between weights `(1,1,1,1,1,5,5,24)`
  and `(2,2,2,2,3,3,25)`.

The finite count and noncollision were independently calculated
using the legacy partition enumerator and a separate inline
terminal-age predicate, and are now included as deterministic
regression assertions against the production `collision_scan`.
GitHub Actions checks that the implemented search repeats them.

**This proves nothing about total weight 41 or higher**. No
statement of uniqueness among all terminal weighted projective
spaces follows from this finite enumeration.

## Reproduce

```sh
python -m unittest tests.test_periodlab -v
python -m periodlab search --max-sum 40 --prefix 2 --terminal-only
```

The result is a *computationally exhaustive statement about a
finite domain*, subject to correctness of the enumeration and
terminality implementation. The printed scan JSON gives counts
and collisions; a standalone independently replayable census
certificate is still future work. The independent `verify_receipt.py`
validates individual pair certificates and reconstructions but
does not certify global census exhaustiveness.
