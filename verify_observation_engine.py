"""Independent exact verification for observation-engine receipts.

This module imports no periodlab discovery code. It recomputes signatures
using factorial prime valuations or exact rational arithmetic.
"""
import argparse
import json
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import gcd


def check(ok, reason):
    if not ok:
        raise ValueError(reason)


def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(",", ":"))


def exact(value):
    """Parse receipt rationals without admitting floats or booleans."""
    check(type(value) in (str, int), "rational values must be integers or exact strings")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("invalid exact rational") from exc


def verify_spec(spec):
    """Validate the public contract independently of the discovery normalizer."""
    check(isinstance(spec, dict) and spec.get("schema")=="periodlab.observation.v1" and
          spec.get("family") in ("weighted_projective", "rational_linear") and
          type(spec.get("budget")) is int and isinstance(spec.get("sensors"), list) and
          0<=spec["budget"]<=len(spec["sensors"])<=64, "invalid specification")
    u=spec.get("universe")
    check(isinstance(u, dict), "invalid universe")
    sensors=spec["sensors"]
    if spec["family"]=="rational_linear":
        if u.get("kind")=="all_rational":
            n=u.get("dimension")
        else:
            check(u.get("kind")=="explicit", "unknown rational universe")
            models=u.get("vectors")
            check(isinstance(models, list) and 1<=len(models)<=100000 and
                  isinstance(models[0], list), "invalid finite rational universe")
            n=len(models[0])
            check(all(isinstance(row, list) and len(row)==n for row in models),
                  "inconsistent vector dimensions")
            for row in models:
                for value in row:
                    exact(value)
        check(type(n) is int and 1<=n<=32, "invalid model dimension")
        names=set()
        for sensor in sensors:
            check(isinstance(sensor, dict), "invalid sensor")
            name=sensor.get("name")
            check(isinstance(name, str) and 1<=len(name)<=100 and name not in names,
                  "empty or duplicate sensor name")
            names.add(name)
            row=sensor.get("coefficients")
            check(isinstance(row, list) and len(row)==n, "invalid sensor dimension")
            for value in row:
                exact(value)
    else:
        if u.get("kind")=="explicit":
            models=u.get("weights")
            check(isinstance(models, list) and 1<=len(models)<=100000 and
                  all(isinstance(w, list) and eligible(w) for w in models),
                  "invalid weight universe")
            L=sum(models[0])
            check(L<=4000 and all(sum(w)==L for w in models), "invalid weight support")
        else:
            check(u.get("kind")=="bounded", "unknown weighted-projective universe")
            L=u.get("total_weight")
            dim=u.get("max_dimension")
            check(type(L) is int and 2<=L<=45 and
                  (dim is None or type(dim) is int and 1<=dim<L) and
                  type(u.get("terminal_only")) is bool, "invalid bounded universe")
        indices=[]
        for sensor in sensors:
            check(isinstance(sensor, dict), "invalid sensor")
            m=sensor.get("supported_index")
            check(type(m) is int and m>=1 and L*m<=4000 and
                  type(sensor.get("degree")) is int and sensor["degree"]==L*m,
                  "invalid degree")
            indices.append(m)
        check(len(set(indices))==len(indices), "duplicate supported indices")


def rank(rows, n):
    rows = [[Fraction(x) for x in row] for row in rows]
    pos = 0
    for col in range(n):
        pivot = next((k for k in range(pos, len(rows)) if rows[k][col]), None)
        if pivot is None:
            continue
        rows[pos], rows[pivot] = rows[pivot], rows[pos]
        for k in range(pos+1, len(rows)):
            if rows[k][col]:
                m = rows[k][col] / rows[pos][col]
                rows[k] = [x-m*y for x,y in zip(rows[k],rows[pos])]
        pos += 1
        if pos == len(rows):
            break
    return pos


def verify_linear(spec, result):
    n = spec["universe"]["dimension"]
    budget = spec["budget"]
    rows = [[exact(v) for v in s["coefficients"]] for s in spec["sensors"]]
    check(1 <= n <= 32 and all(len(row)==n for row in rows), "invalid model dimension")
    r = rank(rows[:budget], n)
    check(result["rank"]==r and result["kernel_dimension"]==n-r and
          result["dimension"]==n, "incorrect rank")
    if r == n:
        check(result["status"]=="linear_reconstruction_theorem", "false theorem")
        idx = result["basis_sensor_positions"]
        inv = [[exact(v) for v in row] for row in result["inverse_matrix"]]
        check(len(idx)==len(set(idx))==n and all(1<=k<=budget for k in idx) and
              len(inv)==n and all(len(row)==n for row in inv), "invalid inverse shape")
        for i in range(n):
            for j in range(n):
                check(sum(inv[i][k]*rows[idx[k]-1][j] for k in range(n))==int(i==j),
                      "exact inverse failed")
        return
    check(result["status"]=="exact_collision", "missing rank-deficiency witness")
    w = result["witness"]
    left = [exact(x) for x in w["left"]]
    right = [exact(x) for x in w["right"]]
    check(len(left)==len(right)==n and left != right and
          w["shared_observations"]==["0"]*budget, "bad witness")
    for row in rows[:budget]:
        check(sum(a*b for a,b in zip(row,left))==0 and
              sum(a*b for a,b in zip(row,right))==0, "witness not in observed kernel")
    separator = result["pair_separator"]
    first = next((k for k in range(budget,len(rows))
                  if rank(rows[:budget]+[rows[k]],n)>r),None)
    if first is None:
        check(separator is None, "unexpected separator")
    else:
        check(separator is not None and separator["sensor_position"]==first+1 and
              separator["sensor"]==spec["sensors"][first] and
              exact(separator["left_value"])==sum(a*b for a,b in zip(rows[first],left)) and
              exact(separator["right_value"])==sum(a*b for a,b in zip(rows[first],right)) and
              exact(separator["left_value"])!=exact(separator["right_value"]), "false separator")
    completion = result["minimum_completion"]
    full = rank(rows,n)
    check(completion["full_catalog_rank"]==full and
          completion["extra_measurement_lower_bound"]==n-r and
          completion["optimal_within_catalog"] is True, "false rank bound")
    if full < n:
        check(completion["status"]=="impossible_in_catalog" and
              completion["sensors"] is None, "false catalog completion")
    else:
        idx = completion["sensors"]
        check(completion["status"]=="available" and
              len(idx)==len(set(idx))==n-r and
              all(budget < k <= len(rows) for k in idx) and
              rank(rows[:budget]+[rows[k-1] for k in idx],n)==n, "invalid completion")


def weight_partitions(total, minimum=1):
    if total == 0:
        yield ()
    else:
        for v in range(minimum,total+1):
            for suffix in weight_partitions(total-v,v):
                yield (v,)+suffix


def eligible(w):
    if len(w)<2 or any(type(a) is not int or a<1 for a in w) or tuple(sorted(w))!=tuple(w):
        return False
    for j in range(len(w)):
        g=0
        for i,v in enumerate(w):
            if i!=j:
                g=gcd(g,v)
        if g!=1:
            return False
    return True


def terminal(w):
    L,N=sum(w),len(w)
    if N<=3:
        return all(a==1 for a in w)
    for k in range(2,L-1):
        s=sum((k*a)%L for a in w)
        if s%L or not 2<=s//L<=N-2:
            return False
    return True


def primes(bound):
    marks=bytearray(b"\x01")*(bound+1)
    marks[0:2]=b"\x00\x00"
    for p in range(2,int(bound**0.5)+1):
        if marks[p]:
            for m in range(p*p,bound+1,p):
                marks[m]=0
    return [p for p in range(2,bound+1) if marks[p]]


def valuation(n,p):
    result=0
    while n:
        n//=p
        result+=n
    return result


def period(w,m):
    total=sum(w)*m
    answer=1
    for p in primes(total):
        e=valuation(total,p)-sum(valuation(a*m,p) for a in w)
        check(e>=0,"invalid multinomial valuation")
        answer*=p**e
    return answer


def verify_finite(spec,result):
    u=spec["universe"]
    family=spec["family"]
    if u["kind"]=="explicit":
        if family=="weighted_projective":
            models=[tuple(w) for w in u["weights"]]
            check(all(eligible(w) for w in models) and
                  len(set(map(sum,models)))==1,"invalid weight universe")
        else:
            models=[tuple(exact(v) for v in w) for w in u["vectors"]]
    else:
        check(family=="weighted_projective","invalid bounded universe")
        L=u["total_weight"]
        check(type(L) is int and 2<=L<=45,"unbounded candidate claim")
        models=[]
        for w in weight_partitions(L):
            if (eligible(w) and
                (u["max_dimension"] is None or len(w)-1<=u["max_dimension"]) and
                (not u["terminal_only"] or terminal(w))):
                models.append(w)
                check(len(models)<=100000, "bounded candidate count exceeds 100000")
    check(bool(models) and len(models)==len(set(models)) and models==sorted(models),
          "noncanonical or duplicate models")
    sensors=spec["sensors"]
    budget=spec["budget"]
    if family=="weighted_projective":
        L=sum(models[0])
        check(all(s["degree"]==L*s["supported_index"] and
                  type(s["supported_index"]) is int and s["supported_index"]>=1
                  for s in sensors),"invalid degree")
        readings=[[str(period(w,s["supported_index"])) for s in sensors] for w in models]
        check(result["known_weight_theorem"]=={
              "total_weight":L,
              "sufficient_positive_indices":list(range(1,L)),
              "covered_by_budget":set(range(1,L)).issubset(
                  {s["supported_index"] for s in sensors[:budget]}),
              "source":"docs/FINITE_RECONSTRUCTION.md"}, "wrong theorem scope")
    else:
        rows=[[exact(v) for v in s["coefficients"]] for s in sensors]
        readings=[[str(sum(a*b for a,b in zip(row,w))) for row in rows] for w in models]
    digest=sha256()
    for w,reading in zip(models,readings):
        record={"model":[str(v) if isinstance(v,Fraction) else v for v in w],
                "values":reading}
        digest.update((canonical(record)+"\n").encode())
    groups=defaultdict(list)
    for i,reading in enumerate(readings):
        groups[tuple(reading[:budget])].append(i)
    pair_count=sum(len(group)*(len(group)-1)//2 for group in groups.values())
    check(result["model_count"]==len(models) and
          result["fingerprint_count"]==len(groups) and
          result["ambiguous_pair_count"]==pair_count and
          result["table_sha256"]==digest.hexdigest(),"candidate census failed")
    if not pair_count:
        check(result["status"]=="finite_reconstruction","false collision status")
        return
    check(result["status"]=="exact_collision","false uniqueness")
    witness=result["witness"]
    a,b=witness["left"],witness["right"]
    if family=="rational_linear":
        a,b=tuple(map(exact,a)),tuple(map(exact,b))
    else:
        a,b=tuple(a),tuple(b)
    check(a!=b and a in models and b in models,"witness outside model class")
    i,j=models.index(a),models.index(b)
    check(readings[i][:budget]==readings[j][:budget]==witness["shared_observations"],
          "witness measurements differ")
    first=next((k for k in range(budget,len(sensors))
                if readings[i][k]!=readings[j][k]),None)
    sep=result["pair_separator"]
    expected=None if first is None else {
        "sensor_position":first+1,"sensor":sensors[first],
        "left_value":readings[i][first],"right_value":readings[j][first]}
    check(sep==expected,"wrong next separating observation")
    best=None
    for k in range(budget,len(sensors)):
        gain=0
        worst=0
        for group in groups.values():
            buckets=defaultdict(int)
            for idx in group:
                buckets[readings[idx][k]]+=1
            gain+=len(group)*(len(group)-1)//2-sum(v*(v-1)//2 for v in buckets.values())
            worst=max(worst,max(buckets.values()))
        if gain and (best is None or (-gain,worst,k)<best[0]):
            best=((-gain,worst,k),{"sensor_position":k+1,"sensor":sensors[k],
                  "ambiguous_pairs_separated":gain,
                  "worst_remaining_fingerprint_class":worst})
    check(result["best_next"]==(best[1] if best else None),"false sensor optimization")
    completion=result["minimum_completion"]
    if pair_count<=10000 and len(sensors)-budget<=12:
        pairs=[(i,j) for group in groups.values() for i,j in combinations(group,2)]
        found=None
        for size in range(1,len(sensors)-budget+1):
            for picks in combinations(range(budget,len(sensors)),size):
                if all(any(readings[i][k]!=readings[j][k] for k in picks)
                       for i,j in pairs):
                    found=[k+1 for k in picks]
                    break
            if found is not None:
                break
        check(completion=={
              "status":"available" if found is not None else "impossible_in_catalog",
              "sensors":found,"optimal_within_catalog":True},"invalid minimal completion")
    else:
        check(completion=={"status":"not_computed","sensors":None,
                          "optimal_within_catalog":False},"invalid uncomputed claim")


def verify(receipt):
    check(isinstance(receipt,dict) and set(receipt)=={"spec","result"},
          "invalid receipt")
    spec,result=receipt["spec"],receipt["result"]
    verify_spec(spec)
    check(isinstance(result, dict), "invalid result")
    if spec["family"]=="rational_linear" and spec["universe"]["kind"]=="all_rational":
        verify_linear(spec,result)
        scope="all rational vectors of the stated dimension"
    else:
        verify_finite(spec,result)
        scope="only the precisely specified finite candidate class"
    check(result.get("scope")==scope,"invalid proof scope")
    return {"verified":True,"status":result["status"],"scope":scope}


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("receipt")
    args=parser.parse_args()
    with open(args.receipt,encoding="utf-8") as f:
        print(json.dumps(verify(json.load(f)),indent=2,sort_keys=True))
