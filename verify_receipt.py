#!/usr/bin/env python3
"""Standalone, exact, standard-library validator for periodlab JSON receipts.

This file MUST NOT import periodlab or rely on its numerical algorithms.
Supports both collision/v1 and reconstruction/v1. It checks pairwise
certificates, NOT exhaustive census claims, geometric isomorphism or novelty.
"""
import json
import sys
from fractions import Fraction
from math import factorial, gcd
from functools import reduce


def fail(message):
    raise ValueError(message)


def validated_weights(value):
    if not isinstance(value, list) or len(value) < 2 or any(
        type(a) is not int or a < 1 for a in value
    ) or sorted(value) != value:
        fail("weights must be nondecreasing positive integer list")
    if any(reduce(gcd, value[:i]+value[i+1:]) != 1 for i in range(len(value))):
        fail("not a well-formed weighted projective space")
    return value


def coef(w, m):
    denominator = 1
    for a in w:
        denominator *= factorial(a*m)
    numerator = factorial(sum(w)*m)
    value, remainder = divmod(numerator, denominator)
    if remainder:
        fail("factorial ratio is not integer")
    return value


def is_terminal(w):
    L, N = sum(w), len(w)
    if N <= 3:
        return all(a == 1 for a in w)
    for k in range(2, L-1):
        v = sum((k*a) % L for a in w)
        if v % L:
            fail("nonintegral quotient age")
        if not 2 <= v//L <= N-2:
            return False
    return True


def expected_terminality(w):
    L, N = sum(w), len(w)
    if N <= 3:
        smooth = all(a == 1 for a in w)
        return {"terminal": smooth, "method": "dimension <= 2: smoothness",
                "failures": [] if smooth else [{"reason": "not all weights equal 1"}],
                "checks": 0}
    failures = []
    for k in range(2,L-1):
        n = sum((k*a)%L for a in w)
        if n%L:
            fail("unexpected nonintegral age")
        if not 2 <= n//L <= N-2:
            failures.append({"k":k,"age":n//L})
    return {"terminal": not failures, "method": "Reid-Tai/Kasprzyk age criterion",
            "failures": failures, "checks": max(0,L-3)}


def polynomial_product(w):
    poly = [Fraction(1)]
    for a in w:
        for j in range(1,a+1):
            next_poly = [Fraction(0)]*(len(poly)+1)
            for i,v in enumerate(poly):
                next_poly[i] += v*j
                next_poly[i+1] += v*a
            poly = next_poly
    return poly


def evaluate(poly,x):
    result = Fraction(0)
    for v in reversed(poly):
        result = result*x+v
    return result


def decode_fraction(s):
    if type(s) is not str:
        fail("polynomial coefficient not string")
    try:
        return Fraction(s)
    except Exception as e:
        fail("invalid rational polynomial: "+str(e))


def verify_collision(data):
    a = validated_weights(data["left_weights"])
    b = validated_weights(data["right_weights"])
    L = sum(a)
    if L != sum(b) or data["total_weight"] != L:
        fail("misaligned common support step")
    n = data["matching_nonzero"]
    if type(n) is not int or n < 1:
        fail("invalid matching prefix count")
    if data["matching_degrees"] != [L*m for m in range(1,n+1)]:
        fail("false matching degree list")
    if data["first_distinguishing_degree"] != L*(n+1):
        fail("false first distinguishing degree")
    if data["terminality"] != {"left":expected_terminality(a),
                                "right":expected_terminality(b)}:
        fail("terminality claim not independently verified")
    for m in range(1,n+1):
        if coef(a,m) != coef(b,m):
            fail("claimed matching coefficient differs")
    c = [coef(a,n+1),coef(b,n+1)]
    if c[0] == c[1] or data["first_distinguishing_coefficients"] != [str(v) for v in c]:
        fail("false first distinguishing coefficient")
    return {"valid": True, "type": "collision", "dimensions": [len(a)-1,len(b)-1],
            "matching_nonzero": n}


def verify_reconstruction(data):
    L = data["total_weight"]
    if type(L) is not int or L < 2:
        fail("invalid total weight")
    w = validated_weights(data["reconstructed_weights"])
    if sum(w) != L:
        fail("reconstructed weight sum differs")
    values = data["supported_coefficients"]
    if not isinstance(values,list) or len(values)<L:
        fail("insufficient first L coefficients for uniqueness")
    if any(type(v) is not str or not v.isdecimal() or int(v)<1 for v in values):
        fail("invalid integer coefficient string")
    if int(values[0]) != 1:
        fail("c0 must equal 1")
    if any(coef(w,m)!=int(values[m]) for m in range(len(values))):
        fail("coefficient sequence does not fit reported weights")
    poly = [decode_fraction(q) for q in data["denominator_polynomial_ascending"]]
    if poly != polynomial_product(w):
        fail("claimed polynomial does not equal weight-factor product")
    if len(poly) != L+1:
        fail("wrong degree for denominator polynomial")
    for m in range(L-1):
        P = factorial(L*(m+1))//factorial(L*m)
        left = evaluate(poly,Fraction(m))*int(values[m+1])
        right = P*int(values[m])
        if left != right:
            fail("interpolation sample does not match polynomial")
    if data["dimension"] != len(w)-1:
        fail("dimension mismatch")
    if data["terminal"] != is_terminal(w):
        fail("terminality mismatch")
    return {"valid": True, "type": "reconstruction", "dimension": len(w)-1,
            "uniqueness": "among well-formed weighted projective spaces with known L"}


def verify(data):
    if not isinstance(data,dict):
        fail("receipt must be a JSON object")
    schema = data.get("schema")
    if schema == "periodlab/collision/v1":
        return verify_collision(data)
    if schema == "periodlab/reconstruction/v1":
        return verify_reconstruction(data)
    fail("unknown schema")


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python verify_receipt.py receipt.json")
    try:
        with open(sys.argv[1],encoding="utf-8") as fh:
            receipt=json.load(fh)
        print(json.dumps(verify(receipt),sort_keys=True))
    except (ValueError,KeyError,TypeError,IndexError) as exc:
        print("INVALID:",str(exc),file=sys.stderr)
        raise SystemExit(2)


if __name__=="__main__":
    main()
