"""Finite, deterministic census of weighted-projective first-prefix collisions.

The search is exhaustive ONLY within a declared sum bound and its
well-formedness, dimension, and terminality filters. Each candidate is
enumerated exactly once as a nondecreasing integer partition.
"""
from collections import defaultdict
from .weights import WeightedProjective, is_terminal
from .periods import fingerprint
from .certificates import collision_receipt


def partitions(total, minimum=1):
    if total == 0:
        yield ()
        return
    for a in range(minimum, total+1):
        for suffix in partitions(total-a, a):
            yield (a,) + suffix


def enumerate_spaces(max_sum, terminal_only=False, max_dim=None):
    if type(max_sum) is not int or not 2 <= max_sum <= 45:
        raise ValueError("max_sum must be an integer from 2 to 45")
    if max_dim is not None and (type(max_dim) is not int or max_dim < 1):
        raise ValueError("max_dim must be a positive integer")
    for L in range(2, max_sum+1):
        for weights in partitions(L):
            if len(weights) < 2 or max_dim is not None and len(weights)-1 > max_dim:
                continue
            try:
                space = WeightedProjective(weights)
            except ValueError:
                continue
            if terminal_only and not is_terminal(space):
                continue
            yield space


def collision_scan(max_sum=40, prefix=2, terminal_only=False,
                   max_dim=None, only_dim_mismatch=False):
    if type(prefix) is not int or prefix < 1:
        raise ValueError("prefix must be positive")
    seen = defaultdict(list)
    counts = defaultdict(int)
    total = 0
    pairs = []
    for space in enumerate_spaces(max_sum, terminal_only, max_dim):
        total += 1
        L = space.total_weight
        counts[L] += 1
        sig = tuple(fingerprint(space, prefix+1)[1:])
        key = (L, sig)
        for previous in seen[key]:
            if only_dim_mismatch and previous.dimension == space.dimension:
                continue
            pairs.append((previous, space))
        seen[key].append(space)
    return {"spaces_examined": total, "spaces_per_total_weight": dict(counts),
            "collisions": pairs, "filters": {
                "max_sum": max_sum, "prefix": prefix,
                "terminal_only": terminal_only,
                "max_dim": max_dim,
                "only_dim_mismatch": only_dim_mismatch}}


def first_breaking_degree(a, b, max_m=20):
    if a.total_weight != b.total_weight:
        raise ValueError("requires a common total weight")
    for m in range(1, max_m+1):
        if fingerprint(a, m+1)[-1] != fingerprint(b, m+1)[-1]:
            return a.total_weight*m
    return None
