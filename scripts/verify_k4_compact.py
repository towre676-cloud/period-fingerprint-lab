#!/usr/bin/env python3
"""Independent exact verifier for the compact, unpadded terminal K=4 collision.

No periodlab imports; verifies:
- compressed 2,000-entry signed weight vector and SHA-256 identity
- equal weight totals, different weight counts
- all factorial-prime valuations for m=1..4, and m=5 discrepancy
- all relevant quotient ages on *both sides* by exact event sweep
- well-formedness via omit-one gcd for compressed weight types

Usage: python scripts/verify_k4_compact.py
"""
from array import array
from functools import reduce
import base64
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path
import struct
import sys
import zlib

ROOT=Path(__file__).resolve().parents[1]
VECTOR=ROOT/"research/k4_compact_vector.b85"
RAW_SHA256="4b26a2d7e54e4e3e4b5bf4899b82df6e71c78663e9acc84e888ce968ec113783"

def read_vector():
    compressed=base64.b85decode(VECTOR.read_text(encoding="ascii").strip())
    raw=zlib.decompress(compressed)
    if len(raw)!=4000 or hashlib.sha256(raw).hexdigest()!=RAW_SHA256:
        raise ValueError("compact collision signed-vector checksum mismatch")
    return list(struct.unpack("<2000h",raw))

def primes_upto(n):
    sieve=bytearray([1])*(n+1)
    sieve[:2]=b"\x00\x00"
    for p in range(2,isqrt(n)+1):
        if sieve[p]:
            sieve[p*p:n+1:p]=b"\x00"*len(range(p*p,n+1,p))
    return [p for p in range(2,n+1) if sieve[p]]

def valuation(n,p):
    result=0
    while n:
        n//=p
        result+=n
    return result

def term_valuation_differences(signed,m,primes):
    max_weight=signed[-1][0]
    differences=[]
    for p in primes:
        if p>m*max_weight: break
        value=sum(c*valuation(m*a,p) for a,c in signed if m*a>=p)
        if value:differences.append((p,value))
    return differences

def check_well_formed(space):
    weight_types=[a for a,c in space]
    if len(weight_types)<2:
        raise ValueError("too few weight types")
    overall_gcd=reduce(gcd,weight_types,0)
    if overall_gcd!=1:
        raise ValueError("weights are not primitive")
    for a,c in space:
        if c==1 and reduce(gcd,(b for b,count in space if b!=a),0)!=1:
            raise ValueError(f"omit-one gcd fails at weight {a}")

def terminal_ages(space,total):
    # age(k) = k - sum_{a} count(a)*floor(k*a/total).
    # floor(k*a/total) jumps at ceil(j*total/a) for j=1..a-1.
    events=array("i",[0])*(total+1)
    for a,count in space:
        for j in range(1,a):
            events[(j*total+a-1)//a]+=count
    N=sum(count for _,count in space)
    floor_sum=0;minimum=N+1;maximum=-1;failures=0
    for k in range(2,total-1):
        floor_sum+=events[k]
        age=k-floor_sum
        if age<minimum:minimum=age
        if age>maximum:maximum=age
        if not 2<=age<=N-2:failures+=1
    return {"minimum":minimum,"maximum":maximum,"failures":failures,
            "indices_checked":total-3}

def verify():
    vec=read_vector()
    relation=[(i+1,c) for i,c in enumerate(vec) if c]
    positive=[(a,c) for a,c in relation if c>0]
    negative=[(a,-c) for a,c in relation if c<0]
    assert len(relation)==706
    assert max(a for a,c in relation)==1990
    assert sum(c for a,c in relation)==-1
    assert sum(a*c for a,c in relation)==0
    A=sum(a*c for a,c in positive)
    B=sum(a*c for a,c in negative)
    assert A==B==6448232
    count_a=sum(c for a,c in positive)
    count_b=sum(c for a,c in negative)
    assert (count_a,count_b)==(12622,12623)
    check_well_formed(positive)
    check_well_formed(negative)

    primes=primes_upto(5*1990)
    mismatch_counts={}
    for m in range(1,6):
        mismatches=term_valuation_differences(relation,m,primes)
        mismatch_counts[str(m)]=len(mismatches)
        if (m<=4 and mismatches) or (m==5 and len(mismatches)!=367):
            raise ValueError(f"false factorial valuation identity at m={m}")
    ages_a=terminal_ages(positive,A)
    ages_b=terminal_ages(negative,B)
    assert (ages_a["minimum"],ages_a["maximum"],ages_a["failures"])==(2,12620,0)
    assert (ages_b["minimum"],ages_b["maximum"],ages_b["failures"])==(2,12621,0)
    return {"verified":True,"total_weight":A,
            "dimensions":[count_a-1,count_b-1],
            "signed_weight_types":len(relation),
            "matching_supported_terms":4,
            "fifth_valuation_mismatches":367,
            "mismatch_counts":mismatch_counts,
            "terminal_ages":{"A":ages_a,"B":ages_b},
            "no_padding_added":True}

if __name__=="__main__":
    try:print(json.dumps(verify(),indent=2,sort_keys=True))
    except Exception as error:
        print("INVALID compact witness:",repr(error),file=sys.stderr)
        raise SystemExit(2)
