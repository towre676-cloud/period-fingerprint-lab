# First terminal two-supported-coefficient collision: exact construction and finite census

**Status (2026-11-05):** Explicit pairwise identities and terminality are proved
by elementary factorial equalities and Kasprzyk's criterion. The optimal
threshold at total weight 51 and completeness of the 77-pair classification
are **finite computer-assisted exhaustive claims**, independently replayed
by separate Python and C++ enumerators. Neither a proof assistant nor an
external referee has checked the result. Novelty has not been established.

## The primitive denominator identity

Put

`A0 = (1,1,1,1,1,5,5,24)`, `B0 = (2,2,2,2,3,3,25)`.

Both sum to 39 and have different numbers of weights (8 and 7).
For m = 1 and m = 2 the factorial denominators agree:

```
(1!)^5 (5!)^2 (24!) = (2!)^4 (3!)^2 (25!)
(2!)^5 (10!)^2 (48!) = (4!)^4 (6!)^2 (50!)
```

Thus adjoining an identical common weight multiset P with sum s
to each side produces two spaces of total weight L = 39+s with
identical supported period coefficients c_L and c_(2L). The first
difference is at m=3, with ratio A/B = 1080400/1002001,
independent of the common padding P.

## The first terminal pair, dimension 8 against dimension 7

Take P=(12). Then L=51, and the two spaces are

- A = P(1,1,1,1,1,5,5,12,24), dimension 8;
- B = P(2,2,2,2,3,3,12,25), dimension 7.

Both are well-formed. Their terminal quotient singularities pass the
Kasprzyk criterion: for k=2,...,49, the integral ages lie respectively
in [2,7] and [2,6]. At k=2, both ages equal 2. Independent local
cyclic quotient charts have minimum nontrivial age 9/8 for A and
26/25 for B (more chart data in the verification script).

### Splitting lemma (proof)

Suppose W is a well-formed terminal weighted projective space
with sum L, and replace one weight `a=b+c` by two positive weights
`b,c`. The new weights are still well-formed: for each omitted
entry, the gcd of all remaining entries divides the appropriate
old omit-one gcd, which was 1.

For any k, the new fractional-age sum minus the old one is

`{kb/L}+{kc/L}-{k(b+c)/L}`,

which equals 0 or 1. The new number of weights grows from N to
N+1, so old ages in [2,N-2] become ages in [2,N-1],
exactly the new terminality range. Therefore the split preserves
terminality. (The low-dimensional smooth cases are handled by
the directly observed new weights in this particular application.)

Iterating the lemma proves that **every partition P of 12**
adjoined to both A0 and B0 gives two terminal spaces. There are
p(12)=77 partitions, hence 77 distinct explicit terminal
two-prefix collisions of total weight 51.

## Exhaustive minimum and classification

An exhaustive search through **all** nondecreasing, well-formed
positive integer weight multisets with total weight at most 51 finds:

- No two-supported-coefficient collision in the unrestricted
  well-formed family at total weight below 39.
- At every L from 39 to 51, all well-formed two-prefix collisions
  are exactly (A0+P, B0+P), where P runs over the partitions of L-39.
- For L<=50, no collision pair has both spaces terminal.
  Indeed B0 has weight 25, so the second-age test at k=2
  fails whenever L<=50.
- At L=51 all 77 pair groups are terminal, each group has
  exactly 2 distinct spaces, and each pair has different dimension.
  There are 230292 well-formed candidates and 211234 terminal
  candidates at L=51.

The list of unrestricted pair counts for L=39,...,51 is exactly
1,1,2,3,5,7,11,15,22,30,42,56,77, the partition numbers
p(0),...,p(12). This finite classification and minimality
depend on exhaustive enumeration correctness, not an abstract
classification theorem for all weights.

## Reproduce

```sh
python scripts/first_terminal_collision.py --min-sum 39 --max-sum 51
python -m unittest tests.test_terminal_collision_51 -v
```

The first command is a separately authored Python exact-factorial
denominator search without the production `periodlab.search` code.
The independent C++ search implementation can run the same domain.
A successful complete enumeration is a bounded computational
certificate, not a Lean proof or claim of mathematical novelty.

## Primary sources and earlier work

- Coates–Kasprzyk–Veneziale (2023), period formula and terminal
  criterion, DOI: 10.1038/s41467-023-41157-1.
- Kasprzyk, *Classifying terminal weighted projective space*,
  Proposition 2.3, https://kasprzyk.work/research/pdf/Terminal_Wps.pdf.
- Sara Veneziale (2024), *Fano Varieties and Machine Learning*,
  Imperial College PhD thesis, Chapter 6.2.1: earlier period-to-weight
  recovery by factorial factorization. This pre-existing algorithm
  must be cited when discussing our separate polynomial-interpolation
  reconstruction method:
  https://kasprzyk.work/teaching/students/pdf/Veneziale.pdf.
