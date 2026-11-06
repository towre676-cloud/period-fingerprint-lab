"""Exact finite-fingerprint mathematics for well-formed weighted projective spaces.

The module intentionally has no machine-learning or network dependencies.
"""
from .weights import WeightedProjective, terminal_report, is_terminal
from .periods import coefficient, coefficient_at_degree, ratio, fingerprint
from .reconstruct import reconstruct_weights, reconstruct_from_prefix, reconstruct_dense_prefix
from .toric2 import rank_two_coefficient

__all__ = ["WeightedProjective", "terminal_report", "is_terminal",
           "coefficient", "coefficient_at_degree", "ratio", "fingerprint",
           "reconstruct_weights", "reconstruct_from_prefix", "rank_two_coefficient"]
