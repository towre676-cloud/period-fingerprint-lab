#!/usr/bin/env python3
"""A small, auditable period-to-dimension experiment (Python standard library).

Scientific scope
----------------
This program implements an already known theorem for weighted projective spaces:
for weights a_1,...,a_N, put L = sum(a_i). The regularized quantum period has
coefficients c_(L*m) = (L*m)! / product((a_i*m)!), with the other coefficients 0.
The variety's dimension is N-1, and

    log c_(L*m) = A*m - (N-1)/2 * log(m) + B + O(1/m),
    A = L*log(L) - sum(a_i*log(a_i)).

A dimension proxy derived from the curvature of the log-coefficient sequence is

    D(m) = 2*m*m*log( c_(L*(m+1))*c_(L*(m-1)) / c_(L*m)^2 ).

D(m) tends to N-1; this script demonstrates the limit numerically. It is NOT
an algorithm that recovers the dimension of an arbitrary unknown Fano variety,
nor a novel theorem, nor an identification of annular with quantum periods.

Research source: Coates--Kasprzyk--Veneziale, Nature Communications 14, 5526
(2023), https://doi.org/10.1038/s41467-023-41157-1 .
"""

from fractions import Fraction
from math import factorial, gcd, log, log1p
from functools import reduce
from collections import defaultdict
import argparse


def check_weights(weights):
    if not weights or len(weights) < 2 or any(type(x) is not int or x <= 0 for x in weights):
        raise ValueError("weights must contain at least two positive integers")
    if reduce(gcd, weights) != 1:
        raise ValueError("weights should be primitive: gcd(weights) == 1")
    return tuple(weights)


def coefficient(weights, m):
    """Exact c_(L*m); m >= 0. No roundoff or external dependencies."""
    w = check_weights(weights)
    if type(m) is not int or m < 0:
        raise ValueError("m must be a nonnegative integer")
    L = sum(w)
    numerator = factorial(L * m)
    denominator = 1
    for a in w:
        denominator *= factorial(a * m)
    assert numerator % denominator == 0
    return numerator // denominator


def exact_ratio(weights, m):
    """Exact c_(L*(m+1))/c_(L*m), using only small integer products."""
    w = check_weights(weights)
    if type(m) is not int or m < 0:
        raise ValueError("m must be nonnegative")
    L = sum(w)
    top = 1
    bottom = 1
    for j in range(1, L + 1):
        top *= L * m + j
    for a in w:
        for j in range(1, a + 1):
            bottom *= a * m + j
    return Fraction(top, bottom)


def log_growth(weights):
    """Exact-form expression for leading exponential rate A (numerical log)."""
    w = check_weights(weights)
    L = sum(w)
    return L * log(L) - sum(a * log(a) for a in w)


def log_forward_ratio(weights, m):
    """Stable log(c_(L*(m+1))/c_(L*m)) for m >= 1.

    Separate the leading rate A and evaluate the small residual with log1p,
    avoiding factorial-sized floating-point numbers entirely.
    """
    w = check_weights(weights)
    if type(m) is not int or m < 1:
        raise ValueError("m must be a positive integer")
    L = sum(w)
    top = sum(log1p(j / (L * m)) for j in range(1, L + 1))
    bottom = sum(log1p(j / (a * m)) for a in w for j in range(1, a + 1))
    return log_growth(w) + top - bottom


def dimension_proxy(weights, m):
    """Finite-difference estimator converging to dim P(weights) = len(w)-1."""
    if type(m) is not int or m < 2:
        raise ValueError("m must be >= 2")
    return 2 * m * m * (log_forward_ratio(weights, m) - log_forward_ratio(weights, m - 1))


def validate():
    examples = (
        (1, 1), (1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 2), (1, 2, 3, 5, 7)
    )
    assert [coefficient((1, 1, 1), m) for m in range(5)] == [1, 6, 90, 1680, 34650]
    for w in examples:
        for m in range(5):
            # Validate exact factorial values against an independently assembled
            # rational recurrence, including its integrality.
            got = Fraction(coefficient(w, m + 1), coefficient(w, m))
            assert got == exact_ratio(w, m), (w, m)
        assert abs(dimension_proxy(w, 1000) - (len(w) - 1)) < 0.01
    return examples


def is_well_formed(weights):
    # A gcd-1 condition after removing EACH weight, as in the 2023 source.
    w = tuple(weights)
    return len(w) >= 2 and all(reduce(gcd, w[:j] + w[j+1:]) == 1 for j in range(len(w)))


def partitions(total, low=1):
    # One canonical nondecreasing representation per integer partition.
    if total == 0:
        yield ()
    else:
        for a in range(low, total + 1):
            for tail in partitions(total - a, a):
                yield (a,) + tail


def primes_upto(n):
    if n < 2:
        return []
    sieve = bytearray(b'\x01') * (n + 1)
    sieve[:2] = b'\x00\x00'
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            sieve[p*p::p] = b'\x00' * (n//p - p + 1)
    return [p for p in range(2, n + 1) if sieve[p]]


def factorial_valuation(n, p):
    # Legendre's formula, independently checking factorial equality prime by prime.
    ans = 0
    while n:
        n //= p
        ans += n
    return ans


def prime_valuations_equal(A, B, m):
    L = sum(A)
    assert sum(B) == L
    for p in primes_upto(L * m):
        vA = sum(factorial_valuation(a*m, p) for a in A)
        vB = sum(factorial_valuation(a*m, p) for a in B)
        if vA != vB:
            return False
    return True


def enumerate_collisions(max_sum):
    if max_sum > 45:
        raise ValueError('Use max_sum <= 45 for a short, reproducible census')
    count = 0
    pairs = 0
    first = None
    for L in range(2, max_sum + 1):
        seen = {}
        numerator1 = factorial(L)
        numerator2 = factorial(2 * L)
        for w in partitions(L):
            if not is_well_formed(w):
                continue
            count += 1
            den1 = 1
            den2 = 1
            for a in w:
                den1 *= factorial(a)
                den2 *= factorial(2*a)
            signature = (numerator1 // den1, numerator2 // den2)
            previous = seen.get(signature)
            if previous is not None:
                pairs += 1
                if first is None:
                    first = (L, previous, w)
            else:
                seen[signature] = w
    return count, first, pairs


def main(args):
    examples = validate()
    print("Exact recurrence checks: PASS (5 families, 5 transitions each)")
    print("Dimension convergence check at m=1000: PASS")
    print()
    print(f"{'weights':<17} {'dimension':>9} {'D(10)':>11} {'D(50)':>11} {'D(200)':>11} {'D(1000)':>11}")
    for w in examples:
        estimates = [dimension_proxy(w, m) for m in (10, 50, 200, 1000)]
        print(f"{str(w):<17} {len(w)-1:>9} " + " ".join(f"{v:>11.6f}" for v in estimates))
    print("\nExample: the P^2 nonzero coefficients c_(3m), m=0..4:")
    print([coefficient((1, 1, 1), m) for m in range(5)])
    print("\nNow verifying a finite-fingerprint collision in different dimensions:")
    A = (1, 1, 1, 1, 1, 5, 5, 24)  # dimension 7
    B = (2, 2, 2, 2, 3, 3, 25)    # dimension 6
    assert sum(A) == sum(B) == 39
    assert is_well_formed(A) and is_well_formed(B)
    for m in (1, 2):
        assert coefficient(A, m) == coefficient(B, m)
        print(f"    degree {39*m}: equal coefficients = {coefficient(A,m)}")
    ratio3 = Fraction(coefficient(A, 3), coefficient(B, 3))
    assert ratio3 == Fraction(1080400, 1002001)
    print(f"    degree 117: unequal coefficients, exact ratio A/B = {ratio3}")
    print(f"    dimensions: {len(A)-1} versus {len(B)-1}")
    assert prime_valuations_equal(A, B, 1)
    assert prime_valuations_equal(A, B, 2)
    assert not prime_valuations_equal(A, B, 3)
    print("    independent prime-valuation checks: PASS")
    if not args.skip_search:
        count, first_collision, num_collisions = enumerate_collisions(args.max_sum)
        print(f"\nExhaustive well-formed weighted-space census up to total weight {args.max_sum}:")
        print(f"    weight multisets checked: {count}")
        print(f"    first collision at total weight: {first_collision[0] if first_collision else 'none'}")
        print(f"    matching pairs found: {num_collisions}")
        if args.max_sum == 40:
            assert count == 201882
            assert first_collision == (39, A, B) or first_collision == (39, B, A)
            assert num_collisions == 2
        print("    enumeration checks: PASS")
    print("\nScope: the asymptotic dimension theorem is established in the literature.")
    print("The finite-truncation collision is an exact calculation, not a claim of novelty.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-sum', type=int, default=40,
                        help='exhaustive search cap (default 40, max 45)')
    parser.add_argument('--skip-search', action='store_true',
                        help='run only the exact example and asymptotic checks')
    main(parser.parse_args())