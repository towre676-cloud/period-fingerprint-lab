#!/usr/bin/env python3
"""Independent exact rational certificate for an effective K=5 existence bound.

EXTERNAL INPUT: Dusart, 'Explicit estimates of some functions over
primes', Ramanujan J. (2018), Corollary 5.3 (d):
  pi(x) <= x/(ln(x) - 1 - 1.2311/ln(x)), for x>5.6.
Its proof is not reproduced here. Everything else is rational arithmetic.

If M > 1 + 5*pi(5M), the matrix of five factorial-valuation conditions
and the total-weight row has more columns than rows. Its integer kernel
is nonzero, producing two distinct equal-total-weight multisets with
identical first five supported coefficients. Adding 2M unit weights
to each side ensures terminality (see universal finite-prefix proof).
This does NOT provide an explicit kernel vector or distinct dimensions.
"""
from fractions import Fraction
import json

def log_lower(n, d, terms):
    """Partial atanh series: 2*sum_{j=0}^{terms-1} z^(2j+1)/(2j+1)
    strictly below ln((1+z)/(1-z)), z=n/d in (0,1).
    """
    z=Fraction(n,d)
    if not 0<z<1 or terms<1:
        raise ValueError("invalid series input")
    return 2*sum((z**(2*j+1))/Fraction(2*j+1)
                 for j in range(terms))

def verify():
    K=5
    M=41_100_000_000
    # 5M=205,500,000,000 exceeds 12*2^34*(299/300).
    assert Fraction(299,25)*2**34 < K*M
    # ln(5M)> 36 ln2 + ln3 + ln(299/300).
    # The positive atanh sums provide strict rational lower bounds.
    # ln(1-1/300)> -1/299 is the integral comparison
    # -ln(1-t)=integral_0^t 1/(1-u)du < t/(1-t).
    logarithm_lower=36*log_lower(1,3,6)+log_lower(1,2,6)-Fraction(1,299)
    threshold=Fraction(26048,1000)
    assert logarithm_lower>threshold
    dusart_c=Fraction(12311,10000)
    # f(t)=t-1-c/t increases strictly for t>0.
    denominator_lower=threshold-1-dusart_c/threshold
    assert denominator_lower>25
    # Cor 5.3 (d) plus the exact arithmetic gives the strict
    # row count inequality. A nonzero integer kernel follows.
    row_upper=1+Fraction(K*K*M)/denominator_lower
    assert row_upper<M
    return {
      "verified_conditional_on_published_prime_bound":True,
      "source":"Dusart, Explicit estimates of some functions over primes, Cor 5.3(d)",
      "K":K,"maximum_individual_weight_bound":M,
      "log_5M_strict_lower":"26048/1000",
      "denominator_strict_lower":str(denominator_lower),
      "valuation_matrix_column_count":M,
      "strict_row_count_upper":str(row_upper),
      "terminal_padding_per_space":2*M,
      "supports_an_explicit_signed_integer_witness":False,
      "guarantees_dimension_change":False}

if __name__=="__main__":
    print(json.dumps(verify(),indent=2,sort_keys=True))
