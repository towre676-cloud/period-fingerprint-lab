#!/usr/bin/env python3
"""Prove a no-collision maximum-weight bound for K supported coefficients.

Construct the full matrix over F_2: its first row is the weight a mod 2;
remaining rows are parity of v_p((ma)!) for all 1<=m<=K and primes
p<=K*M. Exact bitset elimination on its columns gives the rank.
Full column rank modulo 2 implies full rank over Q, hence no
nontrivial integer factorial-denominator relation for max weight <=M.
"""
import argparse
import json
from math import isqrt


def primes_up_to(n):
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[:2] = b"\0\0"
    for p in range(2, isqrt(n) + 1):
        if sieve[p]:
            sieve[p*p:n+1:p] = b"\0" * len(range(p*p, n+1, p))
    return [p for p in range(2, n+1) if sieve[p]]


def valuation_parity(n, p):
    answer = 0
    while n:
        n //= p
        answer ^= n & 1
    return answer


def rank_via_bitsets(max_weight=1500, prefix=4):
    primes = primes_up_to(prefix*max_weight)
    pivots = {}
    for a in range(1, max_weight + 1):
        vector = a & 1
        for m in range(1, prefix + 1):
            offset = 1 + (m-1)*len(primes)
            for i,p in enumerate(primes):
                if p > m*a:
                    break
                if valuation_parity(m*a,p):
                    vector |= 1 << (offset+i)
        while vector:
            highest = vector.bit_length() - 1
            if highest not in pivots:
                pivots[highest] = vector
                break
            vector ^= pivots[highest]
        if len(pivots) != a:
            return {"rank":len(pivots),"nullity":a-len(pivots),
                    "first_dependent_column":a,"max_weight":max_weight,
                    "prefix":prefix}
    return {"rank":max_weight,"nullity":0,
            "first_dependent_column":None,
            "max_weight":max_weight,"prefix":prefix}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-weight",type=int,default=1500)
    parser.add_argument("--prefix",type=int,default=4)
    args = parser.parse_args()
    if not 2 <= args.max_weight <= 3000 or not 1 <= args.prefix <= 5:
        parser.error("supported bounds: 2<=max-weight<=3000, 1<=prefix<=5")
    result = rank_via_bitsets(args.max_weight,args.prefix)
    print(json.dumps(result,indent=2,sort_keys=True))
    if result["nullity"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
