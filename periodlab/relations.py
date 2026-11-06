"""Exact linear-algebra discovery of finite quantum-period collisions.

This builds an integer matrix whose columns are potential weights a and
whose rows encode total weight and prime valuations of (a*m)! for
m=1,...,K. A nonzero integer nullspace vector with mixed signs gives
two multisets with identical first K nonzero coefficients. Padding
each side by two unit weights enforces well-formedness. This method does
NOT ensure a particular dimension, terminality, or minimal total weight.
"""
from fractions import Fraction
from functools import reduce
from math import gcd, lcm
from .periods import primes_to, factorial_valuation, coefficient
from .weights import WeightedProjective


def valuation_matrix(max_weight, prefix):
    if type(max_weight) is not int or max_weight < 2:
        raise ValueError("max_weight must be an integer >= 2")
    if type(prefix) is not int or prefix < 1:
        raise ValueError("prefix must be a positive integer")
    if max_weight * prefix > 500:
        raise ValueError("limit max_weight * prefix <= 500")
    candidates = list(range(1, max_weight+1))
    primes = primes_to(max_weight*prefix)
    rows = [candidates]
    labels = [("total_weight", 0, 0)]
    for m in range(1,prefix+1):
        for p in primes:
            if p > m*max_weight:
                continue
            rows.append([factorial_valuation(a*m,p) for a in candidates])
            labels.append(("valuation", m, p))
    return rows, labels


def nullspace(rows):
    """Exact rational RREF nullspace basis as column lists."""
    if not rows or not rows[0] or any(len(row)!=len(rows[0]) for row in rows):
        raise ValueError("rectangular, nonempty matrix required")
    M=[list(map(Fraction,row)) for row in rows]
    m,n=len(M),len(M[0])
    pivots=[]
    i=0
    for j in range(n):
        pivot=next((k for k in range(i,m) if M[k][j]),None)
        if pivot is None:
            continue
        M[i],M[pivot]=M[pivot],M[i]
        c=M[i][j]
        M[i]=[x/c for x in M[i]]
        for k in range(m):
            if k!=i and M[k][j]:
                c=M[k][j]
                M[k]=[M[k][t]-c*M[i][t] for t in range(n)]
        pivots.append(j)
        i+=1
        if i==m:
            break
    free=[j for j in range(n) if j not in pivots]
    basis=[]
    for j in free:
        v=[Fraction(0)]*n
        v[j]=1
        for row,pivot in enumerate(pivots):
            v[pivot]=-M[row][j]
        basis.append(v)
    return basis


def integer_basis(rows):
    basis=[]
    for v in nullspace(rows):
        denominator=lcm(*(q.denominator for q in v))
        ints=[int(q*denominator) for q in v]
        divisor=reduce(gcd,(abs(x) for x in ints if x),0)
        ints=[x//divisor for x in ints]
        first=next(x for x in ints if x)
        if first<0:
            ints=[-x for x in ints]
        assert all(sum(a*b for a,b in zip(row,ints))==0 for row in rows)
        basis.append(ints)
    return basis


def pair_from_relation(vector, prefix):
    if not vector or any(type(x) is not int for x in vector):
        raise ValueError("integer vector required")
    a=[1,1]
    b=[1,1]
    for weight,count in enumerate(vector,1):
        if count>0:
            a.extend([weight]*count)
        elif count<0:
            b.extend([weight]*(-count))
    a=WeightedProjective.from_weights(a)
    b=WeightedProjective.from_weights(b)
    if a.total_weight != b.total_weight or a.weights==b.weights:
        raise ValueError("not a nontrivial equal-sum relation")
    if any(coefficient(a,m)!=coefficient(b,m) for m in range(1,prefix+1)):
        raise ValueError("prime valuation relation failed coefficient check")
    return a,b


def discover_relation(max_weight=25,prefix=2):
    matrix, labels=valuation_matrix(max_weight,prefix)
    basis=integer_basis(matrix)
    if not basis:
        return {"found":False,"nullity":0,"rows":len(matrix),
                "columns":max_weight}
    vector=basis[0]
    a,b=pair_from_relation(vector,prefix)
    return {"found":True,"nullity":len(basis),"rows":len(matrix),
            "columns":max_weight,"vector":vector,"left":list(a.weights),
            "right":list(b.weights),"dimensions":[a.dimension,b.dimension],
            "total_weight":a.total_weight,"matching_nonzero":prefix,
            "source":"exact prime-valuation integer nullspace",
            "limitations":"Witness only; no terminality, minimality or novelty implied"}
