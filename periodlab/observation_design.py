"""Exact finite-class observation design for weighted-projective period fingerprints.

This is a *discrete identifiability* engine, not a continuous linear-sensor
optimizer. A proposed class is an explicit finite list of well-formed WPS
weight multisets of the same known total weight. An observation is one
positive supported coefficient c_m (the ordinary degree is L*m).

We exhaust all allowed nonadaptive panels of size <= budget, with an
explicit combinatorial-work cap. The returned receipt is independently
replayable by the repository's standalone verify_observation_bridge.py.
"""
from collections.abc import Sequence
from itertools import combinations
from math import comb

from .periods import coefficient
from .weights import WeightedProjective


def _validate(spaces, orders, budget, max_panels):
    if not isinstance(spaces, (list, tuple)) or not spaces:
        raise ValueError("provide a nonempty explicit finite model class")
    if not all(isinstance(s, WeightedProjective) for s in spaces):
        raise ValueError("every candidate must be a validated weighted projective space")
    weights = [s.weights for s in spaces]
    if len(set(weights)) != len(weights):
        raise ValueError("duplicate models are not distinct hypotheses")
    total_weight = spaces[0].total_weight
    if any(s.total_weight != total_weight for s in spaces):
        raise ValueError("supported coefficient indices require a common known total weight")
    if not isinstance(orders, Sequence) or isinstance(orders, (str, bytes, bytearray)) or not orders:
        raise ValueError("provide a nonempty finite sequence of allowed positive supported indices")
    if any(type(m) is not int or m < 1 for m in orders):
        raise ValueError("supported indices must be positive integers")
    if len(set(orders)) != len(orders):
        raise ValueError("duplicate observation indices")
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    if type(max_panels) is not int or max_panels < 1:
        raise ValueError("max_panels must be a positive integer")
    order = tuple(sorted(orders))
    upper = min(budget, len(order))
    trials = sum(comb(len(order), k) for k in range(upper + 1))
    if trials > max_panels:
        raise ValueError(
            f"{trials} candidate panels exceed exact budget cap {max_panels}; "
            "no partial optimality result"
        )
    return total_weight, order, upper


def _partition(table, panel):
    classes = {}
    for model_index, row in enumerate(table):
        key = tuple(row[m] for m in panel)
        classes.setdefault(key, []).append(model_index)
    return classes


def _separated_pairs(classes, total):
    return comb(total, 2) - sum(comb(len(indices), 2)
                                for indices in classes.values())


def design_exact_observations(spaces, orders, budget, *, max_panels=100000):
    """Find a minimum-cardinality separating nonadaptive panel if one fits.

    ``orders`` is a nonempty finite sequence (for example list, tuple, or
    range) of distinct positive Python integers. Input order is immaterial:
    indices are sorted for deterministic search. Strings, sets, mappings and
    one-shot iterators are not accepted. The full panel-count cap is checked
    before computing any coefficients, even if an early separator exists.

    If it does not fit, report the best partial panel (maximum number of
    separated candidate pairs), its exact collision, and the best additional
    allowed observation. Distinguish budget insufficiency from a pair that
    remains indistinguishable using *all* permitted observations.
    """
    L, allowed, upper = _validate(spaces, orders, budget, max_panels)
    table = [{m: coefficient(s, m) for m in allowed} for s in spaces]
    count = len(spaces)
    tested = 0
    best = None
    best_score = -1
    selected = None

    for size in range(upper + 1):
        for panel in combinations(allowed, size):
            tested += 1
            classes = _partition(table, panel)
            score = _separated_pairs(classes, count)
            if score > best_score:
                best_score, best = score, panel
            if score == comb(count, 2):
                selected = panel
                break
        if selected is not None:
            break

    if selected is None:
        selected = best
    chosen_classes = _partition(table, selected)
    complete_classes = _partition(table, allowed)
    fully_indistinguishable = next(
        (indices[:2] for indices in complete_classes.values()
         if len(indices) > 1), None
    )
    collision = next(
        (indices[:2] for indices in chosen_classes.values()
         if len(indices) > 1), None
    )
    extra = [m for m in allowed if m not in selected]
    next_order = None
    if collision is not None:
        next_rank = _separated_pairs(chosen_classes, count)
        for m in extra:
            trial = _separated_pairs(_partition(table, selected + (m,)), count)
            if trial > next_rank:
                next_rank, next_order = trial, m

    if best_score == comb(count, 2):
        status = "separating"
    elif fully_indistinguishable is not None:
        status = "indistinguishable_within_allowed_indices"
    else:
        status = "insufficient_observation_budget"

    return {
        "schema": "periodlab/exact-observation/v1",
        "candidate_class": "explicit finite well-formed weighted-projective spaces",
        "known_total_weight": L,
        "model_weights": [list(s.weights) for s in spaces],
        "allowed_supported_indices": list(allowed),
        "allowed_ordinary_degrees": [L*m for m in allowed],
        "observation_budget": budget,
        "panels_examined": tested,
        "maximum_panel_trials": max_panels,
        "status": status,
        "selected_supported_indices": list(selected),
        "selected_signatures": [
            [str(table[i][m]) for m in selected] for i in range(count)
        ],
        "all_allowed_signatures": [
            [str(table[i][m]) for m in allowed] for i in range(count)
        ],
        "separated_candidate_pairs": best_score,
        "total_candidate_pairs": comb(count, 2),
        "unresolved_pair": collision,
        "globally_ambiguous_pair_within_allowed": fully_indistinguishable,
        "suggested_next_supported_index": next_order,
        "known_weight_reconstruction_theorem_applies":
            all(m in allowed for m in range(1, L)),
        "scope": (
            "Exact optimal nonadaptive selection only within the explicitly "
            "supplied finite candidate class and allowed coefficient indices. "
            "Known-total-weight reconstruction from the first L supported "
            "coefficients is a separate theorem; collision here is not a "
            "global Fano or terminality classification. No stochastic or "
            "l1-normalized sensor optimality is claimed."
        )
    }
