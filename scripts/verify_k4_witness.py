#!/usr/bin/env python3
"""Check a compressed four-prefix factorial collision certificate INDEPENDENTLY.

No imports from periodlab or reconstruct_k4.py. Validates the complete
integer relation, fifth-coefficient discrepancy, exact dimensions, and
the terminal-padding lemma hypotheses.
Usage: python scripts/verify_k4_witness.py /path/to/k4_exact_relation.json
"""
import json
import math
import sys
from pathlib import Path


def primes_up_to(n):
    sieve=bytearray([1])*(n+1)
    sieve[:2]=b"\0\0"
    for p in range(2,math.isqrt(n)+1):
        if sieve[p]:
            sieve[p*p:n+1:p]=b"\0"*len(range(p*p,n+1,p))
    return [p for p in range(2,n+1) if sieve[p]]


def legendre(n,p):
    v=0
    while n:
        n//=p
        v+=n
    return v


def check(document):
    assert document.get("schema")=="periodlab/k4-exact-relation/v1"
    rel=document["relation"]
    assert type(rel) is list and len(rel)==587
    assert all(type(row) is list and len(row)==2 and
               all(type(x) is int for x in row) and
               row[0]>0 and row[1]!=0 for row in rel)
    assert all(rel[i][0]<rel[i+1][0] for i in range(len(rel)-1))
    M=rel[-1][0]
    assert M==1692==document["max_weight"]
    count_a=sum(max(v,0) for _,v in rel)
    count_b=sum(max(-v,0) for _,v in rel)
    H_a=sum(a*max(v,0) for a,v in rel)
    H_b=sum(a*max(-v,0) for a,v in rel)
    assert H_a==H_b==document["old_total_weight"]
    assert [count_a,count_b]==document["weight_counts"]
    assert count_a!=count_b
    r=document["common_unit_padding"]
    assert type(r) is int and r>=2*M
    L=H_a+r
    assert L==document["terminal_total_weight"]
    assert [count_a+r-1,count_b+r-1]==document["terminal_dimensions"]
    assert L==9161682624469356243039134091379944313467
    assert [count_a+r-1,count_b+r-1]==[
        27990950556264851229047371917314029891,
        27991392711556946301081239744549084077]
    primes=primes_up_to(5*M)
    wrong={}
    for m in range(1,6):
        bad=[p for p in primes if p<=m*M and
             sum(v*legendre(m*a,p) for a,v in rel if m*a>=p)!=0]
        wrong[m]=len(bad)
        assert (len(bad)==0)==(m<=4),(m,len(bad))
    assert wrong[5]==document["fifth_mismatch_prime_count"]==318
    assert document["verified_equal_m"]==[1,2,3,4]
    assert document["verified_different_m"]==5
    return {"valid":True,"supported_matching_terms":4,
            "first_distinguishing_term":5,
            "distinct_prime_valuation_failures_at_term_5":wrong[5],
            "max_original_weight":M,
            "terminal_padding_applied":r,
            "dimensions":document["terminal_dimensions"],
            "total_weight":L,
            "note":"Terminality uses the proved r>=2*M unit-padding lemma."}


def main():
    if len(sys.argv)!=2:
        raise SystemExit("usage: python scripts/verify_k4_witness.py witness.json")
    try:
        doc=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        print(json.dumps(check(doc),indent=2,sort_keys=True))
    except (ValueError,KeyError,TypeError,AssertionError) as exc:
        print("INVALID witness:",repr(exc),file=sys.stderr)
        raise SystemExit(2)


if __name__=="__main__":
    main()
