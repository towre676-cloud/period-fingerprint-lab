"""Exact factorial-ratio periods for weighted projective spaces."""
from fractions import Fraction
from math import factorial


def coefficient(space, m):
    """c_(L*m); no floating point, m >= 0."""
    if type(m) is not int or m < 0:
        raise ValueError("m must be a nonnegative integer")
    numerator = factorial(space.total_weight*m)
    denominator = 1
    for a in space.weights:
        denominator *= factorial(a*m)
    q, r = divmod(numerator, denominator)
    if r:
        raise ArithmeticError("multinomial integrality failure")
    return q


def coefficient_at_degree(space, degree):
    if type(degree) is not int or degree < 0:
        raise ValueError("degree must be nonnegative")
    L = space.total_weight
    return 0 if degree % L else coefficient(space, degree // L)


def numerator_at(L, m):
    if type(m) is not int or m < 0 or type(L) is not int or L < 1:
        raise ValueError("L positive, m nonnegative integers required")
    return factorial(L*(m+1)) // factorial(L*m)


def denominator_at(space, m):
    if type(m) is not int or m < 0:
        raise ValueError("m must be nonnegative")
    result = 1
    for a in space.weights:
        result *= factorial(a*(m+1)) // factorial(a*m)
    return result


def ratio(space, m):
    return Fraction(numerator_at(space.total_weight, m),
                    denominator_at(space, m))


def fingerprint(space, count):
    if type(count) is not int or count < 1:
        raise ValueError("count must be positive")
    out = [1]
    for m in range(count-1):
        n = Fraction(out[-1])*ratio(space, m)
        if n.denominator != 1:
            raise ArithmeticError("nonintegral recurrence")
        out.append(n.numerator)
    return out


def factorial_valuation(n, p):
    if type(n) is not int or n < 0 or type(p) is not int or p < 2:
        raise ValueError("invalid valuation inputs")
    count = 0
    while n:
        n //= p
        count += n
    return count


def primes_to(n):
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n+1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, int(n**0.5)+1):
        if sieve[p]:
            sieve[p*p:n+1:p] = b"\x00" * (len(range(p*p, n+1, p)))
    return [p for p in range(n+1) if sieve[p]]


def valuation_denominator(space, m, p):
    return sum(factorial_valuation(a*m, p) for a in space.weights)
