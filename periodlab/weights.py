"""Weighted projective geometry and exact terminality criterion.

Source: Coates--Kasprzyk--Veneziale (2023), Proposition 1, quoting
Kasprzyk's necessary and sufficient age criterion for dimension >= 3.
For dimensions 1 and 2, terminal weighted projective spaces are smooth.
"""
from dataclasses import dataclass
from math import gcd
from functools import reduce


def _gcd_all(values):
    return reduce(gcd, values, 0)


@dataclass(frozen=True)
class WeightedProjective:
    weights: tuple[int, ...]

    def __post_init__(self):
        w = self.weights
        if not isinstance(w, tuple) or len(w) < 2:
            raise ValueError("weights must be a tuple of at least two entries")
        if any(type(a) is not int or a <= 0 for a in w):
            raise ValueError("weights must be positive integers")
        if tuple(sorted(w)) != w:
            raise ValueError("weights must be canonical nondecreasing")
        if any(_gcd_all(w[:i] + w[i+1:]) != 1 for i in range(len(w))):
            raise ValueError("weights are not well-formed (omit-one gcd != 1)")

    @classmethod
    def from_weights(cls, weights):
        return cls(tuple(sorted(weights)))

    @property
    def total_weight(self):
        return sum(self.weights)

    @property
    def dimension(self):
        return len(self.weights) - 1


def necessary_terminal_filter(space):
    """Published necessary weight inequality; NOT sufficient for terminality."""
    w = space.weights
    L, n = space.total_weight, len(w)
    return all(w[j] * (n - j + 1) < L for j in range(2, n))


def terminal_report(space):
    """Exact terminal quotient-singularity verdict and failed age witnesses.

    For dim>=3 and k=2,...,L-2, age = sum_i (k*a_i mod L)/L
    must be an integer in [2,N-2], inclusive. No floating point.
    """
    w = space.weights
    L, N = space.total_weight, len(w)
    if N <= 3:
        result = all(a == 1 for a in w)
        return {"terminal": result, "method": "dimension <= 2: smoothness",
                "failures": [] if result else [{"reason": "not all weights equal 1"}],
                "checks": 0}
    failures = []
    for k in range(2, L - 1):
        residues = sum((k*a) % L for a in w)
        if residues % L:
            raise ArithmeticError("nonintegral age: implementation error")
        age = residues // L
        if not 2 <= age <= N-2:
            failures.append({"k": k, "age": age})
    return {"terminal": not failures, "method": "Reid-Tai/Kasprzyk age criterion",
            "failures": failures, "checks": max(0, L-3)}


def is_terminal(space):
    return terminal_report(space)["terminal"]
