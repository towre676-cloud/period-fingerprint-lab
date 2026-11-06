"""Fast, direct verification of the classified 77-pair construction."""
import unittest
from math import factorial, gcd
from fractions import Fraction
from periodlab.weights import WeightedProjective, is_terminal
from periodlab.periods import coefficient


A0=(1,1,1,1,1,5,5,24)
B0=(2,2,2,2,3,3,25)


def partitions(n, minimum=1):
    if n==0:
        yield ()
    else:
        for a in range(minimum,n+1):
            for rest in partitions(n-a,a):
                yield (a,)+rest


class TerminalCollisionTests(unittest.TestCase):
    def test_primitive_denominator_identity(self):
        for m in (1,2):
            lhs=1
            rhs=1
            for a in A0:
                lhs*=factorial(a*m)
            for b in B0:
                rhs*=factorial(b*m)
            self.assertEqual(lhs,rhs)
        self.assertNotEqual(len(A0),len(B0))

    def test_minimal_example_dimensions_8_and_7(self):
        A=WeightedProjective.from_weights(A0+(12,))
        B=WeightedProjective.from_weights(B0+(12,))
        self.assertEqual((A.dimension,B.dimension),(8,7))
        self.assertTrue(is_terminal(A))
        self.assertTrue(is_terminal(B))
        self.assertEqual(coefficient(A,1),coefficient(B,1))
        self.assertEqual(coefficient(A,2),coefficient(B,2))
        self.assertEqual(Fraction(coefficient(A,3),coefficient(B,3)),
                         Fraction(1080400,1002001))

    def test_77_partition_family(self):
        samples=list(partitions(12))
        self.assertEqual(len(samples),77)
        for pad in samples:
            A=WeightedProjective.from_weights(A0+pad)
            B=WeightedProjective.from_weights(B0+pad)
            self.assertEqual(A.total_weight,51)
            self.assertEqual(B.total_weight,51)
            self.assertTrue(is_terminal(A),A.weights)
            self.assertTrue(is_terminal(B),B.weights)
            self.assertEqual(coefficient(A,1),coefficient(B,1))
            self.assertEqual(coefficient(A,2),coefficient(B,2))
            self.assertEqual(A.dimension,B.dimension+1)


if __name__=="__main__":
    unittest.main()
