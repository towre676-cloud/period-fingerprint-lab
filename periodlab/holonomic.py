"""Exact recurrence-to-holonomic-operator bridge for WPS period series.

For weights a_i, L=sum(a_i), and supported coefficients
c_m=(L*m)! / product_i(a_i*m)!,

    D_w(m)*c_(m+1) = P_L(m)*c_m,

where D_w(X)=product_(i,j=1..a_i)(a_i*X+j) and
P_L(X)=product_(j=1..L)(L*X+j).

For F(z)=sum_m c_m*z^m and theta=z*d/dz this yields the
exact annihilator [D_w(theta-1) - z P_L(theta)] F=0.

This is an annihilator for the declared rank-one WPS factorial-ratio
class. It is NOT claimed minimal, nor automatically the geometric
Picard-Fuchs operator of an arbitrary toric/Fano variety.
"""
from fractions import Fraction

from .periods import coefficient
from .weights import WeightedProjective


def _multiply(poly, linear_constant, linear_slope):
    result = [0]*(len(poly)+1)
    for j, c in enumerate(poly):
        result[j] += c*linear_constant
        result[j+1] += c*linear_slope
    return result


def _poly_shift(poly, shift):
    """Exact Horner composition p(X+shift), ascending integer coefficients."""
    result = [0]
    for c in reversed(poly):
        expanded = _multiply(result, shift, 1)
        expanded[0] += c
        result = expanded
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def _evaluate(poly, value):
    out = 0
    for c in reversed(poly):
        out = out*value + c
    return out


def operator_polynomials(space):
    """Return A(theta), B(theta) for A(theta)-z*B(theta)."""
    if not isinstance(space, WeightedProjective):
        raise TypeError("expect a validated weighted projective space")
    L = space.total_weight
    numerator = [1]
    denominator = [1]
    for j in range(1,L+1):
        numerator = _multiply(numerator,j,L)
    for weight in space.weights:
        for j in range(1,weight+1):
            denominator = _multiply(denominator,j,weight)
    return _poly_shift(denominator,-1), numerator, denominator


def holonomic_receipt(space, checks=6):
    if type(checks) is not int or checks < 1:
        raise ValueError("checks must be a positive integer")
    A,B,D = operator_polynomials(space)
    L = space.total_weight
    coeffs = [coefficient(space,m) for m in range(checks+1)]
    if _evaluate(A,0) != 0:
        raise ArithmeticError("constant coefficient of differential equation failed")
    for m in range(checks):
        if _evaluate(D,m)*coeffs[m+1] != _evaluate(B,m)*coeffs[m]:
            raise ArithmeticError("exact WPS recurrence check failed")
    return {
        "schema": "periodlab/holonomic/v1",
        "class": "well-formed weighted-projective factorial-ratio series",
        "weights": list(space.weights),
        "support_step": L,
        "series_variable": "z=t^L (supported-index variable)",
        "theta": "z*d/dz",
        "theta_polynomial_A_ascending": [str(c) for c in A],
        "theta_polynomial_B_ascending": [str(c) for c in B],
        "differential_operator": "A(theta)-z*B(theta)",
        "checked_recurrence_steps": checks,
        "supported_coefficients": [str(c) for c in coeffs],
        "annihilator_proof": (
            "D_w(m)*c_(m+1)=P_L(m)*c_m follows by factorial cancellation; "
            "the coefficient of z^n in A(theta)F-zB(theta)F is zero "
            "for all n, including n=0 because A(0)=D_w(-1)=0."
        ),
        "scope": "Exact holonomic annihilator, not necessarily the minimal Picard-Fuchs operator; geometry beyond this WPS class is not inferred."
    }
