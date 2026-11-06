"""Portable JSON receipts for finite weighted-projective coefficient collisions.

Verification is separate from discovery. All arithmetic is exact; a receipt
for a *bounded* exhaustive census is NOT a proof that every omitted space
was considered unless its enumeration recipe is replayed.
"""
import json
from math import factorial
from .weights import WeightedProjective, terminal_report
from .periods import coefficient, factorial_valuation, primes_to


def _raw_coefficient(weights, m):
    top = factorial(sum(weights)*m)
    bottom = 1
    for a in weights:
        bottom *= factorial(a*m)
    q, r = divmod(top, bottom)
    if r:
        raise ArithmeticError("noninteger coefficient")
    return q


def collision_receipt(left, right, matching_nonzero=2):
    if not isinstance(left, WeightedProjective) or not isinstance(right, WeightedProjective):
        raise TypeError("must use validated geometric objects")
    if left.total_weight != right.total_weight:
        raise ValueError("same total weight required for aligned coefficient comparison")
    if type(matching_nonzero) is not int or matching_nonzero < 1:
        raise ValueError("matching_nonzero must be positive")
    L = left.total_weight
    for m in range(1, matching_nonzero+1):
        if coefficient(left, m) != coefficient(right, m):
            raise ValueError(f"prefix differs at m={m}")
    m = matching_nonzero + 1
    if coefficient(left, m) == coefficient(right, m):
        raise ValueError("next coefficient does not distinguish the pair")
    return {"schema": "periodlab/collision/v1",
            "left_weights": list(left.weights),
            "right_weights": list(right.weights),
            "total_weight": L,
            "matching_nonzero": matching_nonzero,
            "matching_degrees": [L*m for m in range(1, matching_nonzero+1)],
            "first_distinguishing_degree": L*m,
            "first_distinguishing_coefficients": [
                str(coefficient(left, m)), str(coefficient(right, m))],
            "terminality": {"left": terminal_report(left),
                            "right": terminal_report(right)},
            "limitations": "A pairwise exact witness, not an exhaustive or novelty certificate."}


def verify_receipt(receipt):
    """Independent integer evaluation of a receipt's public mathematical facts.

    The independent validator below does not invoke the production period
    coefficient generator, prime-valuation logic, or the discovery search.
    """
    if receipt.get("schema") != "periodlab/collision/v1":
        raise ValueError("unrecognized schema")
    a = WeightedProjective.from_weights(receipt["left_weights"])
    b = WeightedProjective.from_weights(receipt["right_weights"])
    L = a.total_weight
    if L != b.total_weight or receipt["total_weight"] != L:
        raise ValueError("total-weight mismatch")
    n = receipt["matching_nonzero"]
    if type(n) is not int or n < 1:
        raise ValueError("invalid prefix length")
    if receipt["matching_degrees"] != [L*m for m in range(1, n+1)]:
        raise ValueError("degree metadata mismatch")
    if receipt["first_distinguishing_degree"] != L*(n+1):
        raise ValueError("distinguishing degree mismatch")
    for m in range(1, n+1):
        if _raw_coefficient(a.weights, m) != _raw_coefficient(b.weights, m):
            raise ValueError("false collision")
    values = [_raw_coefficient(a.weights, n+1),
              _raw_coefficient(b.weights, n+1)]
    if values[0] == values[1]:
        raise ValueError("false distinguishing claim")
    if receipt["first_distinguishing_coefficients"] != [str(x) for x in values]:
        raise ValueError("incorrect distinguishing coefficients")
    if receipt["terminality"] != {"left": terminal_report(a), "right": terminal_report(b)}:
        raise ValueError("terminality report mismatch")
    return {"valid": True, "dimensions": [a.dimension, b.dimension],
            "common_support_step": L, "matching_nonzero": n}


def receipt_json(receipt):
    return json.dumps(receipt, indent=2, sort_keys=True) + "\n"
