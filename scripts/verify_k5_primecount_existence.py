#!/usr/bin/env python3
"""Two independent exact prime enumerators prove a K=5 collision existence bound.

For each candidate weight a=1,...,M, include a total-weight row a
and the factorial prime-valuation rows indexed by (m,p), with
1<=m<=5 and p<=m*M. A common-total-weight collision is a nonzero
integral kernel vector. The total row and at most sum_m pi(m*M)
valuation rows are counted without assuming they are independent.

With M=2,867,000, exact prime counts imply the integer matrix has
at least 25 independent rational kernel directions. Adding a
count-of-weights row leaves at least 24, hence a same-dimensional
collision also exists. Adding 2M common unit weights produces
well-formed terminal weighted projective spaces.

This script proves a finite combinatorial count. It does NOT compute
a signed integer kernel witness or a dimension-changing example.
"""
from math import isqrt
import json

M=2_867_000
K=5
EXPECTED=(207927,395799,577502,755330,930416)

def full_sieve_counts():
    n=K*M
    flags=bytearray(b"\x01")*(n+1)
    flags[:2]=b"\x00\x00"
    for p in range(2,isqrt(n)+1):
        if flags[p]:
            flags[p*p::p]=b"\x00"*len(range(p*p,n+1,p))
    total=0
    last=0
    counts=[]
    for m in range(1,K+1):
        bound=m*M
        total+=sum(flags[last+1:bound+1])
        counts.append(total)
        last=bound
    return tuple(counts)

def odd_sieve_counts():
    n=K*M
    # bit i represents odd integer 2*i+1.
    flags=bytearray(b"\x01")*((n+1)//2)
    flags[0]=0
    for p in range(3,isqrt(n)+1,2):
        if flags[p//2]:
            j=(p*p)//2
            flags[j::p]=b"\x00"*len(range(j,len(flags),p))
    total=1  # The prime 2 lies below all requested thresholds.
    last=0
    counts=[]
    for m in range(1,K+1):
        bound=m*M
        end=(bound+1)//2
        total+=sum(flags[last:end])
        counts.append(total)
        last=end
    return tuple(counts)

def verify():
    a=full_sieve_counts()
    b=odd_sieve_counts()
    if a!=b or a!=EXPECTED:
        raise ArithmeticError(f"independent prime enumerators disagree: {a}, {b}")
    valuation_rows=sum(a)
    all_rows=valuation_rows+1
    assert valuation_rows==2_866_974
    assert all_rows==2_866_975
    assert all_rows<M
    # Adding one *independent or dependent* equality for count of
    # weights leaves more columns than rows, so a count-zero integer
    # relation is guaranteed too.
    assert all_rows+1<M
    return {
        "K":K,"max_individual_weight_upper_bound":M,
        "prime_counts":[*a],
        "valuation_constraint_rows_at_most":valuation_rows,
        "including_total_weight_row_at_most":all_rows,
        "matrix_columns":M,
        "rational_kernel_dimension_at_least":M-all_rows,
        "same_dimension_kernel_dimension_at_least":M-all_rows-1,
        "terminal_padding_each_side":2*M,
        "two_independent_exact_sieves_passed":True,
        "explicit_signed_integer_relation_produced":False,
        "different_dimensions_proved":False
    }

if __name__=="__main__":
    print(json.dumps(verify(),indent=2,sort_keys=True))
