#!/usr/bin/env python3
"""Independent bounded census replay; no imports from periodlab.

Enumerates every nondecreasing partition of totals 2..M using an
iterative stack. Checks the omit-one gcd, terminality by fractional
age, and the first K positive supported factorial-ratio coefficients.
This is independent of periodlab.search and its unit tests.

No finite census constitutes a theorem for arbitrarily large weight.
"""
import argparse
import hashlib
import json
from math import factorial, gcd
from functools import reduce


def integer_partitions(total):
    stack=[(total,1,())]
    while stack:
        remaining,smallest,prefix=stack.pop()
        if not remaining:
            yield prefix
            continue
        for n in range(remaining,smallest-1,-1):
            stack.append((remaining-n,n,prefix+(n,)))


def well_formed(w):
    if len(w)<2:
        return False
    for i in range(len(w)):
        if reduce(gcd,w[:i]+w[i+1:]) != 1:
            return False
    return True


def terminal(w):
    N=len(w)
    if N<=3:
        return all(a==1 for a in w)
    L=sum(w)
    for k in range(2,L-1):
        age_numerator=sum((k*a)%L for a in w)
        if age_numerator%L:
            raise ArithmeticError("non-integral expected age")
        age=age_numerator//L
        if age<2 or age>N-2:
            return False
    return True


def fingerprint(w,K):
    L=sum(w)
    result=[]
    for m in range(1,K+1):
        den=1
        for a in w:
            den*=factorial(a*m)
        q,r=divmod(factorial(L*m),den)
        if r:
            raise ArithmeticError("not a multinomial integer")
        result.append(q)
    return tuple(result)


def replay(max_sum,prefix,terminal_only=True):
    seen={}
    well_formed_count=terminal_count=pair_count=0
    by_total={}
    digest=hashlib.sha256()
    witnesses=[]
    for L in range(2,max_sum+1):
        row={"well_formed":0,"terminal":0,"collisions":0}
        for w in integer_partitions(L):
            if not well_formed(w):
                continue
            well_formed_count+=1
            row["well_formed"]+=1
            is_t=terminal(w)
            if is_t:
                terminal_count+=1
                row["terminal"]+=1
            if terminal_only and not is_t:
                continue
            # Encoding includes the exact support step L and the weights.
            digest.update(("%d:%s\n"%(L,",".join(map(str,w)))).encode())
            key=(L,fingerprint(w,prefix))
            if key in seen:
                pair_count+=1
                row["collisions"]+=1
                if len(witnesses)<10:
                    witnesses.append([list(seen[key]),list(w)])
            else:
                seen[key]=w
        by_total[str(L)]=row
    return {"schema":"periodlab/bounded-census/v1","max_sum":max_sum,
            "prefix":prefix,"terminal_only":terminal_only,
            "well_formed_count":well_formed_count,
            "terminal_count":terminal_count,
            "collision_count":pair_count,
            "first_witnesses":witnesses,
            "candidate_sha256":digest.hexdigest(),
            "per_total_weight":by_total,
            "scope":"Nondecreasing well-formed integer partitions; terminal only if flag set"}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-sum",type=int,default=40)
    parser.add_argument("--prefix",type=int,default=2)
    parser.add_argument("--all-well-formed",action="store_true")
    parser.add_argument("--expect-well-formed",type=int)
    parser.add_argument("--expect-terminal",type=int)
    parser.add_argument("--expect-collisions",type=int)
    args=parser.parse_args()
    if not 2<=args.max_sum<=45 or not 1<=args.prefix<=5:
        parser.error("bounds: 2<=max-sum<=45 and 1<=prefix<=5")
    report=replay(args.max_sum,args.prefix,not args.all_well_formed)
    for arg,key in (("expect_well_formed","well_formed_count"),
                    ("expect_terminal","terminal_count"),
                    ("expect_collisions","collision_count")):
        expected=getattr(args,arg)
        if expected is not None and report[key]!=expected:
            parser.error(f"{key}: expected {expected}, observed {report[key]}")
    print(json.dumps(report,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
