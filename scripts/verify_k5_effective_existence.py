#!/usr/bin/env python3
"""Pure-rational audit of an explicit five-coefficient existence bound.

External input: Dusart's prime-counting theorem, pi(x) <= x/(ln(x)-1.112)
for x > exp(1.112). Its proof is NOT reproduced in this script.

The exact arithmetic below proves M > 1+5*pi(5M) for M=45,000,000,000.
Thus the factorial-valuation matrix has a nonzero INTEGER kernel, giving
distinct WPS with common total weight and matching K=5 supported terms.
Adding 2M unit weights to both makes them well-formed and terminal.
This is an existential bound, NOT an explicit integer relation.
"""
from fractions import Fraction
import json

def lower_log(numerator, denominator, terms):
    z=Fraction(numerator,denominator)
    assert 0<z<1
    return 2*sum((z**(2*j+1))/(2*j+1) for j in range(terms))

def verify():
    M=45_000_000_000
    K=5
    assert lower_log(1,3,3)>Fraction(693,1000)  # ln2 > 0.693
    assert lower_log(6,7,13)>Fraction(64,25)    # ln13 > 2.56
    assert 13*2**34 < 5*M                       # 223338299392 <225e9
    # ln(5M) > 34 ln2 + ln13 > 26.122.
    log_lower=34*Fraction(693,1000)+Fraction(64,25)
    assert log_lower==Fraction(13061,500)
    denominator=log_lower-Fraction(1112,1000)
    assert denominator==Fraction(2501,100)
    # By Dusart, pi(5M) <=5M/(ln(5M)-1.112) <5M/25.01.
    assert 1 + Fraction(K*K*M,1)/denominator < M
    return {"verified_conditional_on_Dusart_bound":True,"K":K,
            "original_max_weight_bound":M,
            "terminal_common_padding_per_space":2*M,
            "prime_counting_input":"pi(x) <= x/(ln(x)-1.112), x>exp(1.112)",
            "log_lower":"13061/500",
            "denominator_lower":"2501/100",
            "number_of_columns":M,
            "strict_row_upper_bound":str(1+Fraction(K*K*M)/denominator),
            "dimension_change_guaranteed":False,
            "explicit_integer_witness_available":False}

if __name__=="__main__":
    print(json.dumps(verify(),indent=2,sort_keys=True))
