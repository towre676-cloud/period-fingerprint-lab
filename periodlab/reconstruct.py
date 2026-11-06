"""Finite exact reconstruction from a known common total weight L.

Given the first L nonzero coefficients c_0, c_L, ..., c_((L-1)L),
recover weights via polynomial interpolation, with NO estimated dimensions.
See docs/FINITE_RECONSTRUCTION.md for proof and assumptions.
"""
from fractions import Fraction
from math import factorial
from .periods import numerator_at, fingerprint
from .weights import WeightedProjective


def _mul_linear(poly, root):
    """Multiply ascending-coefficient polynomial by (x-root)."""
    result = [Fraction(0)] * (len(poly)+1)
    for j, c in enumerate(poly):
        result[j] -= c*root
        result[j+1] += c
    return result


def _newton_interpolate(evaluations):
    """Interpolate at x=0,1,...,d using exact forward differences."""
    data = list(map(Fraction, evaluations))
    polynomial = [Fraction(0)]
    basis = [Fraction(1)]
    for k in range(len(data)):
        scale = data[0]/factorial(k)
        if len(polynomial) < len(basis):
            polynomial.extend([Fraction(0)] * (len(basis)-len(polynomial)))
        for j, c in enumerate(basis):
            polynomial[j] += scale*c
        data = [data[j+1]-data[j] for j in range(len(data)-1)]
        basis = _mul_linear(basis, Fraction(k))
    return polynomial


def _divide_root(poly, root):
    """Synthetic divide by x-root; return quotient, remainder."""
    if len(poly) < 2:
        return [], poly[0] if poly else Fraction(0)
    q = [Fraction(0)]*(len(poly)-1)
    q[-1] = poly[-1]
    for j in range(len(q)-2, -1, -1):
        q[j] = poly[j+1] + root*q[j+1]
    return q, poly[0] + root*q[0]


def _multiplicity(poly, root):
    current = poly[:]
    multiplicity = 0
    while len(current) >= 2:
        candidate, rem = _divide_root(current, root)
        if rem:
            break
        multiplicity += 1
        current = candidate
    return multiplicity


def polynomial_from_prefix(total_weight, coeffs):
    """Recover D(x)=product_(i,j)(a_i*x+j) exactly, if valid.

    A candidate uses D(x)/(x+1)^2 of degree at most L-2.
    L-1 samples derived from L coefficients interpolate this quotient.
    """
    L = total_weight
    if type(L) is not int or L < 2:
        raise ValueError("total_weight must be integer >= 2")
    if len(coeffs) < L:
        raise ValueError(f"need at least {L} nonzero-support coefficients")
    values = []
    for m in range(L-1):
        a, b = coeffs[m], coeffs[m+1]
        if type(a) is not int or type(b) is not int or a <= 0 or b <= 0:
            raise ValueError("coefficients must be positive integers")
        # D(m) = N(m) * c_m / c_(m+1).
        denominator = Fraction(numerator_at(L, m)*a, b)
        values.append(denominator/Fraction((m+1)**2))
    quotient = _newton_interpolate(values)
    return _mul_linear(_mul_linear(quotient, -1), -1)


def reconstruct_weights(total_weight, coeffs):
    """Recover the unique weight multiset, or reject inconsistent data.

    For every positive integer a, multiplicity of the rational root -1/a
    in D is M(a)=sum_(a | b) multiplicity_of_weight(b).
    Descending Möbius inversion recovers each weight count.
    """
    L = total_weight
    poly = polynomial_from_prefix(L, coeffs)
    M = {a: _multiplicity(poly, Fraction(-1, a)) for a in range(1, L+1)}
    counts = {}
    for a in range(L, 0, -1):
        counts[a] = M[a] - sum(counts[b] for b in range(2*a, L+1, a))
        if counts[a] < 0:
            raise ValueError("interpolation does not describe factorial-ratio weights")
    recovered = tuple(a for a in range(1, L+1) for _ in range(counts[a]))
    if sum(recovered) != L or len(recovered) < 2:
        raise ValueError("data do not determine a valid weighted projective space")
    try:
        space = WeightedProjective(recovered)
    except ValueError as e:
        raise ValueError("recovered weights are not well-formed") from e
    if fingerprint(space, len(coeffs)) != list(coeffs):
        raise ValueError("data violate the predicted exact factorial ratio")
    return space


def reconstruct_from_prefix(total_weight, coeffs):
    space = reconstruct_weights(total_weight, coeffs)
    return {"total_weight": total_weight, "weights": list(space.weights),
            "dimension": space.dimension,
            "observed_coefficients": len(coeffs),
            "finite_uniqueness_within_class": len(coeffs) >= total_weight}
