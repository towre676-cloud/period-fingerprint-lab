#!/usr/bin/env python3
"""Independent exact factorial-valuation verifier in near-linear time.

For signed weight multiplicities u_a, the exponent of p in
product_a ((m*a)!)**u_a equals sum_{n=1}^{m*M} S_m(n)*v_p(n),
where S_m(n)=sum_{a: m*a>=n} u_a.
A reverse sweep updates S_m(n), factoring each n with a smallest
prime-factor sieve. No giant factorials or modular rank guesses.

Usage:
  python scripts/verify_signed_relation_fast.py witness.json --K 5 --padding N
Compatible with research/k4_compact_terminal_collision JSON format or
the K4/K5 'relation' array. The padding theorem is independent of
prime valuations; no-padding terminality requires separate age checks.
"""
import argparse
import hashlib
import json
from pathlib import Path

def prime_factor_sieve(n):
    spf=list(range(n+1))
    for p in range(2,int(n**0.5)+1):
        if spf[p]==p:
            for j in range(p*p,n+1,p):
                if spf[j]==j:
                    spf[j]=p
    return spf

def discrepancies(signed,m,spf):
    limit=m*signed[-1][0]
    end=[0]*(limit+1)
    for a,c in signed:
        end[m*a]+=c
    delta=[0]*(limit+1)
    active=0
    for n in range(limit,1,-1):
        active+=end[n]
        if not active:
            continue
        q=n
        while q>1:
            p=spf[q]
            e=0
            while q%p==0:
                q//=p
                e+=1
            delta[p]+=active*e
    return [(p,e) for p,e in enumerate(delta) if e]

def verify(signed,K,padding=0):
    if type(K) is not int or K<1 or type(padding) is not int or padding<0:
        raise ValueError("K positive; padding nonnegative integers required")
    if not isinstance(signed,list) or len(signed)<2:
        raise ValueError("signed relation required")
    if any(not isinstance(pair,list) or len(pair)!=2 or
           any(type(v) is not int for v in pair) or pair[0]<1 or pair[1]==0
           for pair in signed):
        raise ValueError("signed multiplicities must be nonzero exact integers")
    if any(signed[i][0]>=signed[i+1][0] for i in range(len(signed)-1)):
        raise ValueError("weights must be strictly increasing")
    M=signed[-1][0]
    if (K+1)*M>2_000_000:
        raise ValueError("requested prime-factor sieve exceeds safety limit")
    count_a=sum(max(c,0) for _,c in signed)
    count_b=sum(max(-c,0) for _,c in signed)
    H=sum(a*max(c,0) for a,c in signed)
    if H!=sum(a*max(-c,0) for a,c in signed) or not count_a or not count_b:
        raise ValueError("not a nontrivial equal-total-weight signed relation")
    spf=prime_factor_sieve((K+1)*M)
    mismatch_counts=[]
    for m in range(1,K+2):
        wrong=discrepancies(signed,m,spf)
        mismatch_counts.append(len(wrong))
        if m<=K and wrong:
            raise ValueError(f"false relation at m={m}: {wrong[:4]}")
    return {"valid_exact_factorial_identity":True,"matching_terms":K,
            "max_individual_weight":M,"signed_weight_types":len(signed),
            "common_original_weight_sum":H,
            "unpad_weight_counts":[count_a,count_b],
            "weight_count_difference":count_a-count_b,
            "discrepant_prime_counts":[*mismatch_counts],
            "next_term_differs":bool(mismatch_counts[-1]),
            "common_unit_padding":padding,
            "terminal_by_proved_unit_padding_lemma":padding>=2*M,
            "common_final_weight_sum":H+padding,
            "final_dimensions":[count_a+padding-1,count_b+padding-1]}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("witness",type=Path)
    parser.add_argument("--K",type=int)
    parser.add_argument("--padding",type=int,default=0)
    args=parser.parse_args()
    raw=args.witness.read_bytes()
    document=json.loads(raw)
    signed=document.get("signed_weight_multiplicities",
                        document.get("relation"))
    K=args.K or document.get("K") or document.get("common_supported_coefficient_count")
    if K is None:
        parser.error("K missing from file and arguments")
    result=verify(signed,K,args.padding)
    result["source_sha256"]=hashlib.sha256(raw).hexdigest()
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
