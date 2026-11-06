#!/usr/bin/env python3
"""Independent exhaustive factorial-denominator scan for terminal WPS collisions.

No imports from periodlab. Each total weight is enumerated independently
as nondecreasing partitions. First two positive supported coefficients
are compared through their exact factorial denominators.
Usage: python scripts/first_terminal_collision.py --min-sum 39 --max-sum 51
"""
import argparse
import json
from math import factorial, gcd
from functools import reduce
from collections import Counter, defaultdict


def partitions(total, low=1):
    if total == 0:
        yield ()
    for a in range(low, total+1):
        for tail in partitions(total-a, a):
            yield (a,)+tail


def well_formed(w):
    return len(w)>=2 and all(reduce(gcd,w[:j]+w[j+1:])==1 for j in range(len(w)))


def terminal(w,total):
    n=len(w)
    if n<=3:
        return all(a==1 for a in w)
    counts=Counter(w)
    for k in range(2,total-1):
        age_numerator=sum(mult*((k*a)%total) for a,mult in counts.items())
        age,remainder=divmod(age_numerator,total)
        if remainder or age<2 or age>n-2:
            return False
    return True


def search(lo,hi,first_only=False):
    fact=[factorial(i) for i in range(2*hi+1)]
    report=[]
    for total in range(lo,hi+1):
        wf=t=0
        by_signature=defaultdict(list)
        for w in partitions(total):
            if not well_formed(w):
                continue
            wf+=1
            if not terminal(w,total):
                continue
            t+=1
            d1=d2=1
            for a in w:
                d1*=fact[a]
                d2*=fact[2*a]
            by_signature[(d1,d2)].append(w)
        colliding=[group for group in by_signature.values() if len(group)>1]
        # Number of pairs, not the number of groups.
        pair_count=sum(len(g)*(len(g)-1)//2 for g in colliding)
        row={"total_weight":total,"well_formed":wf,"terminal":t,
             "collision_groups":len(colliding),"collision_pairs":pair_count,
             "different_dimension_pairs":sum(
               1 for group in colliding
               for i in range(len(group)) for j in range(i+1,len(group))
               if len(group[i])!=len(group[j]))}
        if colliding:
            row["first_witness"]=[list(x) for x in colliding[0][:2]]
            if total==51:
                base_a=(1,)*5+(5,5,24)
                base_b=(2,)*4+(3,3,25)
                expected={frozenset((tuple(sorted(base_a+p)),
                                     tuple(sorted(base_b+p))))
                          for p in partitions(12)}
                actual={frozenset(group) for group in colliding}
                row["all_pairs_are_common_partition_of_12"]=actual==expected
                row["partition_count_12"]=len(expected)
        report.append(row)
        if first_only and colliding:
            break
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--min-sum",type=int,default=39)
    p.add_argument("--max-sum",type=int,default=51)
    p.add_argument("--first-only",action="store_true")
    p.add_argument("--assert-first",type=int,default=None)
    args=p.parse_args()
    if not 2<=args.min_sum<=args.max_sum<=55:
        p.error("require 2 <= min-sum <= max-sum <= 55")
    reports=search(args.min_sum,args.max_sum,args.first_only)
    actual=next((r["total_weight"] for r in reports if r["collision_pairs"]),None)
    if args.assert_first is not None and actual!=args.assert_first:
        p.error(f"expected first terminal collision {args.assert_first}; found {actual}")
    print(json.dumps({"schema":"periodlab/terminal-census-51/v1",
                      "rows":reports, "first_collision":actual},indent=2))


if __name__=="__main__":
    main()
