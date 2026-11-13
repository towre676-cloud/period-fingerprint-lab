"""Exact observation budgets: injectivity certificates or indistinguishable pairs.

Only a full-rank rational-linear result is an unrestricted reconstruction
statement. Weighted-projective and finite-vector results are exhaustive solely
for the stated, explicitly finite candidate universe.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import argparse
import json

from .weights import WeightedProjective, is_terminal
from .periods import coefficient
from .search import partitions

SCHEMA = "periodlab.observation.v1"
MAX_MODELS = 100_000


def rational(value):
    if type(value) not in (str, int):
        raise ValueError("rational values must be integers or exact strings")
    try:
        return Fraction(value)
    except (ZeroDivisionError, ValueError) as exc:
        raise ValueError("invalid exact rational") from exc


def rank_and_nullspace(rows, n):
    """RREF over Q; returns pivot columns, rational kernel basis."""
    a = [list(row) for row in rows]
    pivots = []
    r = 0
    for j in range(n):
        k = next((i for i in range(r, len(a)) if a[i][j]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        pivot = a[r][j]
        a[r] = [x / pivot for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][j]:
                multiple = a[i][j]
                a[i] = [x - multiple * y for x, y in zip(a[i], a[r])]
        pivots.append(j)
        r += 1
        if r == len(a):
            break
    free = [j for j in range(n) if j not in pivots]
    basis = []
    for j in free:
        v = [Fraction(0)] * n
        v[j] = Fraction(1)
        for i, p in enumerate(pivots):
            v[p] = -a[i][j]
        basis.append(v)
    return pivots, basis


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Fraction(0))


def inverse(matrix):
    n = len(matrix)
    a = [list(row) + [Fraction(int(i == j)) for j in range(n)]
         for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            raise ArithmeticError("pivot row selection was not independent")
        a[j], a[pivot] = a[pivot], a[j]
        d = a[j][j]
        a[j] = [v / d for v in a[j]]
        for i in range(n):
            if i != j:
                d = a[i][j]
                a[i] = [x-d*y for x, y in zip(a[i], a[j])]
    return [row[n:] for row in a]


def normalize(spec):
    if not isinstance(spec, dict) or type(spec.get("budget")) is not int:
        raise ValueError("provide a JSON specification with integer budget")
    family, budget = spec.get("family"), spec["budget"]
    source, given = spec.get("universe"), spec.get("sensors")
    if not isinstance(source, dict) or not isinstance(given, list):
        raise ValueError("universe must be an object and sensors an array")
    if not 0 <= budget <= len(given) <= 64:
        raise ValueError("budget must be between 0 and number of sensors (at most 64)")
    if family == "rational_linear":
        if source.get("kind") == "all_rational":
            n = source.get("dimension")
            if type(n) is not int or not 1 <= n <= 32:
                raise ValueError("rational dimension must be 1..32")
            uni = {"kind": "all_rational", "dimension": n}
        elif source.get("kind") == "explicit":
            raw = source.get("vectors")
            if not isinstance(raw, list) or not raw:
                raise ValueError("supply nonempty explicit vectors")
            n = len(raw[0]) if isinstance(raw[0], list) else 0
            if not 1 <= n <= 32 or len(raw) > MAX_MODELS:
                raise ValueError("invalid finite rational universe")
            vectors = []
            for row in raw:
                if not isinstance(row, list) or len(row) != n:
                    raise ValueError("inconsistent vector dimensions")
                vectors.append(tuple(str(rational(x)) for x in row))
            if len(vectors) != len(set(vectors)):
                raise ValueError("duplicate rational vectors")
            uni = {"kind": "explicit", "vectors": [list(v) for v in sorted(vectors)]}
        else:
            raise ValueError("unknown rational universe")
        names = set()
        sensors = []
        for sensor in given:
            if not isinstance(sensor, dict) or not isinstance(sensor.get("name"), str):
                raise ValueError("linear sensors need a name")
            name = sensor["name"]
            if not name or name in names or len(name) > 100:
                raise ValueError("empty or duplicate sensor name")
            names.add(name)
            row = sensor.get("coefficients")
            if not isinstance(row, list) or len(row) != n:
                raise ValueError("linear sensor must have exactly dimension entries")
            sensors.append({"name": name, "coefficients": [str(rational(v)) for v in row]})
    elif family == "weighted_projective":
        if source.get("kind") == "explicit":
            raw = source.get("weights")
            if not isinstance(raw, list) or not raw or len(raw) > MAX_MODELS:
                raise ValueError("supply nonempty explicit weights")
            ws = []
            for row in raw:
                if not isinstance(row, list):
                    raise ValueError("weight lists must be arrays")
                w = WeightedProjective.from_weights(row)
                ws.append(w.weights)
            if len(ws) != len(set(ws)):
                raise ValueError("duplicate weight multisets")
            totals = {sum(w) for w in ws}
            if len(totals) != 1:
                raise ValueError("supported coefficients require a common total weight L")
            uni = {"kind": "explicit", "weights": [list(w) for w in sorted(ws)]}
            L = totals.pop()
            if L > 4000:
                raise ValueError("explicit total weight exceeds 4000")
        elif source.get("kind") == "bounded":
            L = source.get("total_weight")
            max_dim = source.get("max_dimension")
            terminal = source.get("terminal_only", False)
            if type(L) is not int or not 2 <= L <= 45:
                raise ValueError("bounded total_weight must be 2..45")
            if max_dim is not None and (type(max_dim) is not int or not 1 <= max_dim < L):
                raise ValueError("max_dimension must be a positive integer < L")
            if type(terminal) is not bool:
                raise ValueError("terminal_only must be boolean")
            uni = {"kind": "bounded", "total_weight": L,
                   "max_dimension": max_dim, "terminal_only": terminal}
        else:
            raise ValueError("unknown weighted-projective universe")
        if any(type(k) is not int or k < 1 or L*k > 4000 for k in given):
            raise ValueError("supported indices must be positive integers with L*m <= 4000")
        if len(set(given)) != len(given):
            raise ValueError("supported coefficient sensors must be distinct")
        sensors = [{"supported_index": k, "degree": L*k} for k in given]
    else:
        raise ValueError("unsupported model family")
    return {"schema": SCHEMA, "family": family, "universe": uni,
            "sensors": sensors, "budget": budget}


def _serialize(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"))


def _all_models(spec):
    universe = spec["universe"]
    if universe["kind"] == "explicit":
        if spec["family"] == "weighted_projective":
            return [tuple(w) for w in universe["weights"]]
        return [tuple(rational(v) for v in row) for row in universe["vectors"]]
    L = universe["total_weight"]
    models = []
    for w in partitions(L):
        if len(w) < 2 or (universe["max_dimension"] is not None and
                         len(w)-1 > universe["max_dimension"]):
            continue
        try:
            model = WeightedProjective(w)
        except ValueError:
            continue
        if universe["terminal_only"] and not is_terminal(model):
            continue
        models.append(w)
        if len(models) > MAX_MODELS:
            raise ValueError("bounded candidate count exceeds 100000")
    return models


def _finite(spec):
    models = _all_models(spec)
    if not models:
        raise ValueError("the declared finite class has no admissible candidates")
    sensors = spec["sensors"]
    budget = spec["budget"]
    family = spec["family"]
    rows = [[rational(v) for v in s["coefficients"]] for s in sensors] if family == "rational_linear" else None
    @lru_cache(maxsize=4096)
    def period_at(weights, m):
        return coefficient(WeightedProjective(weights), m)
    values = [[str(dot(row, model)) for row in rows] if rows is not None else
              [str(period_at(model, s["supported_index"])) for s in sensors]
              for model in models]
    digest = sha256()
    for model, measured in zip(models, values):
        record = {"model": [str(x) if isinstance(x, Fraction) else x for x in model],
                  "values": measured}
        digest.update((_serialize(record) + "\n").encode("utf-8"))
    groups = defaultdict(list)
    for i, measurements in enumerate(values):
        groups[tuple(measurements[:budget])].append(i)
    ambiguous = [v for v in groups.values() if len(v) > 1]
    pairs_count = sum(len(group)*(len(group)-1)//2 for group in ambiguous)
    outcome = {"status": "finite_reconstruction" if not ambiguous else "exact_collision",
               "scope": "only the precisely specified finite candidate class",
               "model_count": len(models), "fingerprint_count": len(groups),
               "ambiguous_pair_count": pairs_count,
               "table_sha256": digest.hexdigest()}
    if family == "weighted_projective":
        L = sum(models[0]) if models else spec["universe"]["total_weight"]
        outcome["known_weight_theorem"] = {
            "total_weight": L, "sufficient_positive_indices": list(range(1, L)),
            "covered_by_budget": set(range(1, L)).issubset(
                {s["supported_index"] for s in sensors[:budget]}),
            "source": "docs/FINITE_RECONSTRUCTION.md"}
    if not ambiguous:
        outcome["statement"] = ("Every pair in the declared finite class is "
                                "separated by the budgeted observations.")
        return outcome
    ambiguous_pairs = [(i, j) for group in ambiguous
                       for i, j in combinations(group, 2)] if pairs_count <= 10000 else None
    def first_separator(i, j):
        return next((k for k in range(budget, len(sensors)) if values[i][k] != values[j][k]), None)
    first = (ambiguous[0][0], ambiguous[0][1])
    if ambiguous_pairs is not None:
        first = next((pair for pair in ambiguous_pairs if first_separator(*pair) is not None), first)
    i, j = first
    outcome["witness"] = {
        "left": [str(v) if isinstance(v, Fraction) else v for v in models[i]],
        "right": [str(v) if isinstance(v, Fraction) else v for v in models[j]],
        "shared_observations": values[i][:budget]}
    separating_index = first_separator(i, j)
    outcome["pair_separator"] = None if separating_index is None else {
        "sensor_position": separating_index+1, "sensor": sensors[separating_index],
        "left_value": values[i][separating_index], "right_value": values[j][separating_index]}
    best = None
    for k in range(budget, len(sensors)):
        separated = 0
        worst = 0
        for group in groups.values():
            bins = defaultdict(int)
            for index in group:
                bins[values[index][k]] += 1
            separated += len(group)*(len(group)-1)//2 - sum(n*(n-1)//2 for n in bins.values())
            worst = max(worst, max(bins.values()))
        if separated and (best is None or (-separated, worst, k) < best[0]):
            best = ((-separated, worst, k), {
                "sensor_position": k+1, "sensor": sensors[k],
                "ambiguous_pairs_separated": separated,
                "worst_remaining_fingerprint_class": worst})
    outcome["best_next"] = best[1] if best else None
    rem = list(range(budget, len(sensors)))
    completion = {"status": "not_computed", "sensors": None,
                  "optimal_within_catalog": False}
    if ambiguous_pairs is not None and len(rem) <= 12:
        found = None
        for size in range(1, len(rem)+1):
            for selection in combinations(rem, size):
                if all(any(values[i][k] != values[j][k] for k in selection)
                       for i, j in ambiguous_pairs):
                    found = list(selection)
                    break
            if found is not None:
                break
        completion = {"status": "available" if found is not None else "impossible_in_catalog",
                      "sensors": [i+1 for i in found] if found is not None else None,
                      "optimal_within_catalog": True}
    outcome["minimum_completion"] = completion
    outcome["statement"] = ("The two reported distinct candidates have identical "
                            "budgeted exact observations; no global injectivity follows.")
    return outcome


def _linear_all(spec):
    n = spec["universe"]["dimension"]
    sensors = spec["sensors"]
    budget = spec["budget"]
    rows = [[rational(v) for v in s["coefficients"]] for s in sensors]
    observed = rows[:budget]
    pivots, kernel = rank_and_nullspace(observed, n)
    rank = len(pivots)
    outcome = {"rank": rank, "dimension": n,
               "kernel_dimension": n-rank,
               "scope": "all rational vectors of the stated dimension"}
    if rank == n:
        selected = []
        for k in range(budget):
            if len(rank_and_nullspace([rows[i] for i in selected]+[rows[k]], n)[0]) > len(selected):
                selected.append(k)
                if len(selected) == n:
                    break
        outcome.update({"status": "linear_reconstruction_theorem",
                        "basis_sensor_positions": [k+1 for k in selected],
                        "inverse_matrix": [[str(v) for v in row]
                                           for row in inverse([rows[i] for i in selected])],
                        "statement": "Exact rational left inverse reconstructs every vector from the observed sensors."})
        return outcome
    chosen = None
    witness = kernel[0]
    for k in range(budget, len(rows)):
        if len(rank_and_nullspace(observed+[rows[k]], n)[0]) > rank:
            chosen = k
            witness = next(v for v in kernel if dot(rows[k], v))
            break
    outcome["status"] = "exact_collision"
    outcome["witness"] = {"left": ["0"]*n, "right": [str(v) for v in witness],
                          "shared_observations": ["0"]*budget}
    outcome["pair_separator"] = None if chosen is None else {
        "sensor_position": chosen+1, "sensor": sensors[chosen],
        "left_value": "0", "right_value": str(dot(rows[chosen], witness))}
    selected = []
    working = list(observed)
    for k in range(budget, len(rows)):
        if len(rank_and_nullspace(working+[rows[k]], n)[0]) > len(rank_and_nullspace(working, n)[0]):
            selected.append(k+1)
            working.append(rows[k])
            if len(selected) == n-rank:
                break
    can_reconstruct = len(rank_and_nullspace(working, n)[0]) == n
    outcome["minimum_completion"] = {
        "status": "available" if can_reconstruct else "impossible_in_catalog",
        "sensors": selected if can_reconstruct else None,
        "optimal_within_catalog": True,
        "extra_measurement_lower_bound": n-rank,
        "full_catalog_rank": len(rank_and_nullspace(rows, n)[0])}
    outcome["statement"] = ("A nonzero exact kernel vector produces "
                            "indistinguishable rational models under the budget.")
    return outcome


def analyze(spec):
    canonical = normalize(spec)
    result = (_linear_all(canonical) if canonical["family"] == "rational_linear" and
              canonical["universe"]["kind"] == "all_rational" else _finite(canonical))
    return {"spec": canonical, "result": result}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", help="exact JSON model class, sensors, and observation budget")
    parser.add_argument("--out", help="write a reproducible JSON receipt")
    args = parser.parse_args(argv)
    with open(args.spec, encoding="utf-8") as stream:
        receipt = analyze(json.load(stream))
    result = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as stream:
            stream.write(result)
    else:
        print(result, end="")
    return receipt


if __name__ == "__main__":
    main()
