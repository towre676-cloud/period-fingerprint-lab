#!/usr/bin/env python3
"""Independent exact verification of signed K=3 collision identities and sharp weight bounds.

No periodlab imports. Runs in the Python standard library:
python scripts/verify_k3_relations.py research/k3_exact_relations.json
"""
import json
import sys
from math import isqrt
from pathlib import Path


def primes_up_to(n):
    b = bytearray(b"\x01") * (n + 1)
    b[:2] = b"\0\0"
    for p in range(2, isqrt(n) + 1):
        if b[p]:
            b[p * p:n + 1:p] = b"\0" * len(range(p * p, n + 1, p))
    return [p for p in range(2, n + 1) if b[p]]


def valuation(n, p):
    s = 0
    while n:
        n //= p
        s += n
    return s


def valuation_matrix(M, K=3):
    primes = primes_up_to(K * M)
    rows = [list(range(1, M + 1))]
    for m in range(1, K + 1):
        for p in primes:
            if p > m * M:
                break
            rows.append([valuation(a * m, p) for a in range(1, M + 1)])
    return rows


def rank_mod(rows, p=1000003):
    # Finite-field rank is a certified lower bound on rational rank.
    a = [[x % p for x in row] for row in rows]
    n, nr, r = len(a[0]), len(a), 0
    for j in range(n):
        h = next((i for i in range(r, nr) if a[i][j]), None)
        if h is None:
            continue
        a[r], a[h] = a[h], a[r]
        pivot = a[r]
        inv = pow(pivot[j], -1, p)
        for k in range(j, n):
            pivot[k] = pivot[k] * inv % p
        for i in range(r + 1, nr):
            if a[i][j]:
                v, row = a[i][j], a[i]
                for k in range(j + 1, n):
                    row[k] = (row[k] - v * pivot[k]) % p
                row[j] = 0
        r += 1
        if r == nr:
            break
    return r


def verify_relation(record):
    rel = record["signed_multiplicities"]
    assert rel and all(type(x) is list and len(x) == 2
                       and type(x[0]) is int and type(x[1]) is int
                       and x[0] > 0 and x[1] != 0 for x in rel)
    assert all(rel[i][0] < rel[i + 1][0] for i in range(len(rel) - 1))
    max_weight = rel[-1][0]
    a_count = sum(max(0, c) for _, c in rel)
    b_count = sum(max(0, -c) for _, c in rel)
    H = sum(w * max(c, 0) for w, c in rel)
    assert H == sum(w * max(-c, 0) for w, c in rel)
    assert H == record["old_total_weight"]
    assert [a_count, b_count] == record["number_of_weights"]
    assert sum(w * c for w, c in rel) == 0
    for m in (1, 2, 3):
        for p in primes_up_to(m * max_weight):
            assert sum(c * valuation(m * w, p) for w, c in rel) == 0, (m, p)
    assert any(sum(c * valuation(4 * w, p) for w, c in rel) != 0
               for p in primes_up_to(4 * max_weight))
    padding = record.get("common_unit_padding", 0)
    if padding:
        # Padding lemma: r >= 2M common unit weights makes either WPS
        # terminal. For integer 2 <= k < L/M no weight wraps and
        # age(k)=k >=2; for k >= L/M units alone contribute rk/L>=2.
        # Then age(k)+age(L-k)<=N bounds age(k) from above.
        assert padding >= 2 * max_weight
        assert record["terminal_total_weight"] == H + padding
        assert record["terminal_dimensions"] == [a_count + padding - 1,
                                                 b_count + padding - 1]
        assert record["difference_in_dimension"] == a_count - b_count
    else:
        # Direct, exact age calculation for the compact example.
        assert record["terminal_without_padding"] is True
        for sign, count in ((1, a_count), (-1, b_count)):
            for k in range(2, H - 1):
                numerator = sum(max(0, sign * c) * ((k * w) % H)
                                for w, c in rel)
                assert numerator % H == 0
                assert 2 <= numerator // H <= count - 2
    return {"id": record["id"], "max_weight": max_weight,
            "total_weight": H, "weight_counts": [a_count, b_count],
            "padding": padding, "different_dimension": a_count != b_count}


def main(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    assert data["schema"] == "periodlab/k3-relations/v1"
    records = {x["id"]: x for x in data["relations"]}
    assert set(records) == {"K3-W172", "K3-W189-dimension", "K3-W249-dimension-one"}
    outcomes = [verify_relation(x) for x in data["relations"]]
    # Rational rank at 171 is exactly 171 by its F_p minor.
    # At 188 the W172 relation gives rank <=187, and modular rank
    # proves rank >=187. Thus its 1-dimensional kernel is count-zero.
    # At 189 two independent exact witnesses give rank <=187,
    # while modular rank proves >=187. The new witness has nonzero
    # count, proving max_weight 189 is the first possible.
    rank = {str(m): rank_mod(valuation_matrix(m))
            for m in (171, 172, 188, 189)}
    assert rank == {"171":171, "172":171, "188":187, "189":187}
    assert sum(c for _, c in records["K3-W172"]["signed_multiplicities"]) == 0
    assert sum(c for _, c in records["K3-W189-dimension"]["signed_multiplicities"]) == 126
    assert sum(c for _, c in records["K3-W249-dimension-one"]["signed_multiplicities"]) == 1
    print(json.dumps({"status":"PASS", "K":3,
        "smallest_max_weight_any_collision":172,
        "smallest_max_weight_different_dimension":189,
        "rank_mod_1000003":rank, "verified_relations":outcomes}, indent=2))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv)>1 else
         str(Path(__file__).resolve().parents[1]/"research/k3_exact_relations.json"))
