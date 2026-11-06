# Compact terminal four-supported-coefficient collision

**Research status:** Independently checked exact computer-assisted witness.
Mathematical originality, optimality by total weight/dimension and independent
peer review are NOT established.

## Result

There are two **well-formed terminal weighted projective spaces**, with
no artificially added unit-weight padding, having:

| | Space A | Space B |
|---|---:|---:|
| Number of weights | 12,622 | 12,623 |
| Dimension | **12,621** | **12,622** |
| Total weight | 6,448,232 | 6,448,232 |
| Minimum relevant fractional age | 2 | 2 |
| Maximum relevant fractional age | 12,620 | 12,621 |
| Terminality violations | 0 | 0 |

Their first **four positive supported coefficients** agree exactly,
while their fifth supported coefficients differ, with nonzero valuation
differences at **367 primes**.

The signed multiplicities of all **706 nonzero weight types** are preserved
in [k4_compact_vector.b85](k4_compact_vector.b85), an exact lossless compressed
array of 2,000 signed 16-bit integers; positive multiplicities describe
Space A and negative multiplicities describe Space B. All zero entries are
included in the decompressed array for unambiguous alignment with weights
1,2,...,2000. Maximum individual weight used is 1,990.

The signed vector has SHA-256
`4b26a2d7e54e4e3e4b5bf4899b82df6e71c78663e9acc84e888ce968ec113783`
on the **decompressed little-endian signed-int16 byte sequence**.

## Verification

Run:

```sh
python scripts/verify_k4_compact.py
```

The checker uses only the Python standard library, independently of the
discovery algorithm. It performs all of:

1. Decompress and check the SHA-256 and 2,000-entry format.
2. Recompute common total weight and respective counts from exact integers.
3. Verify the full prime-valuation equality
   `sum_a u_a*v_p((ma)!)=0` for every m=1,2,3,4 and all relevant primes.
4. Confirm at least one unequal valuation for m=5; in fact **367** differ.
5. Verify well-formedness using exact gcd tests for every omitted entry
   (compressed appropriately for repeated weights).
6. Check **all 6,448,229 relevant quotient-age indices per space**
   using an exact event-sweep algorithm to compute
   `age(k)=k-sum_a n_a*floor(k*a/L)`.
7. Verify the required bounds `2 <= age(k) <= N-2`, without sampling.

The age event-sweep algorithm accumulates jumps at
`ceil(j*L/a)`, for `j=1,...,a-1`. Because this exact integer
identity underlies the algorithm, the test is not a floating-point
approximation. If the original weight multiset has no duplicates,
the omit-one gcd check is done explicitly for each unique entry;
duplicate entries are safely handled by the compressed multiplicity.

## How the witness was found

The earlier K4 exact relation at maximum weight 1692 produced terminal
spaces of astronomical dimension after padding. Extending the exact
prime-valuation kernel through maximum weight 2000 gave a
**21-dimensional rational kernel**. Reconstructing integer kernel
vectors by modular CRT, normalizing to an integral lattice using
Hermite normal form, and applying *exact Gram-matrix LLL* yielded a short
integer relation with:

- 706 nonzero signed weight types;
- signed coefficient-count difference **-1**;
- equal total weighted sum of **6,448,232**;
- no need for terminal-padding.

The integer relation and every age bound are independently verified.
This is a large empirical reduction in complexity, not a proof that the
relation minimizes total weight or dimension. The compressed witness
is the reproducibility anchor; LLL behavior may depend on basis ordering.

## Scientific interpretation

This is a dimension-changing terminal four-coefficient collision of
**dimensions about 12 thousand**, replacing the previous explicit
witness with dimensions about `10^37`. It retains the sharp earlier
**maximum individual weight obstruction** at 1692: no relation can
involve weights solely at or below 1691. The compact example does
*not* attain that sharp maximum-weight threshold—it uses weights
as high as 1990, trading larger individual weights for much smaller
multiplicities and total weight.

It does not contradict dimension recovery from the complete infinite
period. It is an exact computational observation and mathematical
construction within the weighted-projective factorial-ratio family,
not a general statement about all Fano varieties.
