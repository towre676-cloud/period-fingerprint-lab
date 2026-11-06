"""Rank-two nonnegative-charge toric period coefficient model.

Given rows (a_i,b_i) of nonnegative integer GLSM charges, define
c_d = sum_{x,y>=0: sum_i(a_i*x+b_i*y)=d}
      d! / product_i (a_i*x+b_i*y)! .
This is the regularized I-function factorial-ratio coefficient for the
specified charge model, not a classifier for arbitrary rank-two Fanos.

The charge data must be validated geometrically before interpreting this
as a quantum period of a smooth/terminal toric Fano variety.
"""
from math import factorial


def rank_two_coefficient(charges, degree):
    if type(degree) is not int or degree < 0:
        raise ValueError("degree must be a nonnegative integer")
    if not charges or any(len(pair) != 2 or
                          any(type(v) is not int or v < 0 for v in pair) or
                          pair == (0, 0) for pair in charges):
        raise ValueError("charges must be nonzero nonnegative integer pairs")
    A = sum(pair[0] for pair in charges)
    B = sum(pair[1] for pair in charges)
    if A == 0 or B == 0:
        raise ValueError("both degree directions must be nonzero")
    ans = 0
    for x in range(degree//A + 1):
        remainder = degree - A*x
        if remainder % B:
            continue
        y = remainder//B
        den = 1
        for a, b in charges:
            den *= factorial(a*x + b*y)
        q, r = divmod(factorial(degree), den)
        if r:
            raise ArithmeticError("nonintegral multinomial coefficient")
        ans += q
    return ans


def product_p1_p1_coefficient(degree):
    """Exact P^1 x P^1 regularized period coefficient; odd entries vanish."""
    from math import comb
    return comb(degree, degree//2)**2 if degree % 2 == 0 else 0
