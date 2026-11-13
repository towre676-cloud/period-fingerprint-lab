#!/usr/bin/env python3
"""Standalone exact verifier for periodlab observation and holonomic receipts.

This deliberately imports neither periodlab nor its algorithms. It only
uses standard-library integers and fractions. The observation receipt claims
optimality WITHIN its listed finite candidate class, permitted coefficient
indices and exhaustive panel budget—not among all WPS/Fano varieties.
"""
import json
import sys
from fractions import Fraction
from itertools import combinations
from math import comb, factorial, gcd
from functools import reduce


def fail(message):
    raise ValueError(message)


def weights(value):
    if not isinstance(value,list) or len(value)<2 or any(type(a) is not int or a<1 for a in value):
        fail("invalid weight vector")
    if value!=sorted(value):
        fail("unsorted weight vector")
    if any(reduce(gcd,value[:i]+value[i+1:])!=1 for i in range(len(value))):
        fail("not well formed")
    return value


def coefficient(w,m):
    n=factorial(sum(w)*m)
    d=1
    for a in w:
        d*=factorial(a*m)
    q,r=divmod(n,d)
    if r:
        fail("noninteger coefficient")
    return q


def panels(orders,budget):
    for k in range(min(budget,len(orders))+1):
        yield from combinations(orders,k)


def partition(table,panel):
    classes={}
    for i,row in enumerate(table):
        key=tuple(row[m] for m in panel)
        classes.setdefault(key,[]).append(i)
    return classes


def separated(classes,n):
    return comb(n,2)-sum(comb(len(indices),2) for indices in classes.values())


def verify_observation(data):
    raw=data.get("model_weights")
    if not isinstance(raw,list) or not raw:
        fail("empty candidate class")
    ws=[weights(w) for w in raw]
    if len({tuple(w) for w in ws})!=len(ws):
        fail("duplicate candidate")
    L=sum(ws[0])
    if any(sum(w)!=L for w in ws) or data.get("known_total_weight")!=L:
        fail("support mismatch")
    allowed=data.get("allowed_supported_indices")
    if not isinstance(allowed,list) or not allowed or any(type(m) is not int or m<1 for m in allowed):
        fail("invalid supported indices")
    if allowed!=sorted(set(allowed)):
        fail("unordered/duplicate indices")
    if data.get("allowed_ordinary_degrees")!=[L*m for m in allowed]:
        fail("incorrect ordinary degrees")
    budget=data.get("observation_budget")
    cap=data.get("maximum_panel_trials")
    if type(budget) is not int or budget<0 or type(cap) is not int or cap<1:
        fail("invalid budget")
    ntrials=sum(comb(len(allowed),k) for k in range(min(budget,len(allowed))+1))
    if ntrials>cap:
        fail("unjustified claim over budget")
    table=[{m:coefficient(w,m) for m in allowed} for w in ws]
    best=None
    best_score=-1
    selected=None
    tested=0
    for panel in panels(allowed,budget):
        tested+=1
        score=separated(partition(table,panel),len(ws))
        if score>best_score:
            best_score,best=score,panel
        if score==comb(len(ws),2):
            selected=panel
            break
    if selected is None:
        selected=best
    cp=partition(table,selected)
    ap=partition(table,allowed)
    global_collision=next((v[:2] for v in ap.values() if len(v)>1),None)
    collision=next((v[:2] for v in cp.values() if len(v)>1),None)
    next_order=None
    if collision is not None:
        score=separated(cp,len(ws))
        for m in allowed:
            if m in selected:
                continue
            better=separated(partition(table,selected+(m,)),len(ws))
            if better>score:
                score,next_order=better,m
    status=("separating" if best_score==comb(len(ws),2)
            else "indistinguishable_within_allowed_indices" if global_collision is not None
            else "insufficient_observation_budget")
    want={
        "schema":"periodlab/exact-observation/v1",
        "selected_supported_indices":list(selected),
        "selected_signatures":[[str(table[i][m]) for m in selected] for i in range(len(ws))],
        "all_allowed_signatures":[[str(table[i][m]) for m in allowed] for i in range(len(ws))],
        "status":status,
        "panels_examined":tested,
        "total_candidate_pairs":comb(len(ws),2),
        "separated_candidate_pairs":best_score,
        "unresolved_pair":collision,
        "globally_ambiguous_pair_within_allowed":global_collision,
        "suggested_next_supported_index":next_order,
        "known_weight_reconstruction_theorem_applies":all(m in allowed for m in range(1,L)),
    }
    for key,value in want.items():
        if data.get(key)!=value:
            fail("invalid exact observation claim: "+key)
    return {"valid":True,"type":"exact_observation","models":len(ws),
            "selected_supported_indices":list(selected),"status":status}


def product_factors(w):
    p=[1]
    for a in w:
        for j in range(1,a+1):
            result=[0]*(len(p)+1)
            for k,v in enumerate(p):
                result[k]+=j*v
                result[k+1]+=a*v
            p=result
    return p


def shift(p,c):
    result=[0]
    for v in reversed(p):
        out=[0]*(len(result)+1)
        for i,t in enumerate(result):
            out[i]+=c*t
            out[i+1]+=t
        out[0]+=v
        result=out
    return result


def evaluate(p,x):
    v=0
    for a in reversed(p):
        v=v*x+a
    return v


def verify_holonomic(data):
    w=weights(data.get("weights"))
    L=sum(w)
    if data.get("support_step")!=L:
        fail("support mismatch")
    D=product_factors(w)
    P=[1]
    for j in range(1,L+1):
        r=[0]*(len(P)+1)
        for i,v in enumerate(P):
            r[i]+=j*v
            r[i+1]+=L*v
        P=r
    A=shift(D,-1)
    for name,poly in (("theta_polynomial_A_ascending",A),
                      ("theta_polynomial_B_ascending",P)):
        if data.get(name)!=[str(c) for c in poly]:
            fail("incorrect annihilator: "+name)
    n=data.get("checked_recurrence_steps")
    if type(n) is not int or n<1:
        fail("invalid recurrence steps")
    cs=[coefficient(w,m) for m in range(n+1)]
    if data.get("supported_coefficients")!=[str(c) for c in cs]:
        fail("incorrect coefficient list")
    if evaluate(A,0)!=0:
        fail("incorrect constant term")
    for m in range(n):
        if evaluate(D,m)*cs[m+1]!=evaluate(P,m)*cs[m]:
            fail("recurrence mismatch")
    return {"valid":True,"type":"holonomic","weight_sum":L,
            "annihilator_order_at_most":L}


def verify(data):
    if not isinstance(data,dict):
        fail("receipt must be object")
    if data.get("schema")=="periodlab/exact-observation/v1":
        return verify_observation(data)
    if data.get("schema")=="periodlab/holonomic/v1":
        return verify_holonomic(data)
    fail("unsupported bridge receipt")


def main():
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python verify_observation_bridge.py receipt.json")
    try:
        with open(sys.argv[1],encoding="utf-8") as file:
            receipt=json.load(file)
        print(json.dumps(verify(receipt),sort_keys=True))
    except (ValueError,TypeError,KeyError,IndexError) as e:
        print("INVALID:",str(e),file=sys.stderr)
        raise SystemExit(2)


if __name__=="__main__":
    main()
