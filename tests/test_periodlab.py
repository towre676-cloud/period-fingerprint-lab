"""Exact regression tests for the expanded laboratory."""
import unittest
from fractions import Fraction
from math import comb

from periodlab.weights import WeightedProjective, is_terminal, terminal_report
from periodlab.periods import coefficient, coefficient_at_degree, fingerprint, ratio
from periodlab.reconstruct import reconstruct_weights, reconstruct_from_prefix
from periodlab.toric2 import rank_two_coefficient, product_p1_p1_coefficient
from periodlab.certificates import collision_receipt, verify_receipt
from periodlab.search import collision_scan, first_breaking_degree


A = WeightedProjective.from_weights((1,1,1,1,1,5,5,24))
B = WeightedProjective.from_weights((2,2,2,2,3,3,25))


class WeightsTests(unittest.TestCase):
    def test_geometry_and_failures(self):
        self.assertEqual(A.dimension, 7)
        self.assertEqual(B.dimension, 6)
        self.assertEqual(A.total_weight, 39)
        for weights in ((2,4), (2,2,3), (1,), (-1,1), (2,2,2,3)):
            with self.assertRaises(ValueError):
                WeightedProjective.from_weights(weights)

    def test_exact_terminality(self):
        self.assertTrue(is_terminal(WeightedProjective.from_weights((1,1,1))))
        self.assertFalse(is_terminal(WeightedProjective.from_weights((1,1,2))))
        self.assertTrue(is_terminal(WeightedProjective.from_weights((1,1,1,2))))
        self.assertFalse(is_terminal(A))
        self.assertFalse(is_terminal(B))
        self.assertTrue(terminal_report(A)["failures"])

    def test_periods(self):
        p2 = WeightedProjective.from_weights((1,1,1))
        self.assertEqual(fingerprint(p2, 5), [1, 6, 90, 1680, 34650])
        self.assertEqual(coefficient_at_degree(p2, 1), 0)
        self.assertEqual(coefficient_at_degree(p2, 6), 90)
        self.assertEqual(ratio(p2, 0), Fraction(6))


class ReconstructionTests(unittest.TestCase):
    def test_many_exact_reconstructions(self):
        for weights in ((1,1), (1,1,1,2), (1,2,3,5,7),
                        (1,1,1,1,1,5,5,24), (2,2,2,2,3,3,25)):
            space = WeightedProjective.from_weights(weights)
            result = reconstruct_weights(space.total_weight,
                                         fingerprint(space, space.total_weight))
            self.assertEqual(result, space)

    def test_malformed_prefix(self):
        p2 = WeightedProjective.from_weights((1,1,1))
        values = fingerprint(p2, 3)
        with self.assertRaises(ValueError):
            reconstruct_weights(3, [1, 6])
        with self.assertRaises(ValueError):
            reconstruct_weights(3, [1, 7, 90])
        with self.assertRaises(ValueError):
            reconstruct_weights(3, [0, 6, 90])


class RankTwoTests(unittest.TestCase):
    def test_product_p1_squared(self):
        rows = ((1,0), (1,0), (0,1), (0,1))
        for d in range(12):
            self.assertEqual(rank_two_coefficient(rows, d),
                             product_p1_p1_coefficient(d))
            self.assertEqual(rank_two_coefficient(rows, d),
                             comb(d, d//2)**2 if d % 2 == 0 else 0)


class CertificateTests(unittest.TestCase):
    def test_collision(self):
        self.assertEqual(first_breaking_degree(A, B, 4), 117)
        receipt = collision_receipt(A, B, 2)
        self.assertEqual(verify_receipt(receipt)["dimensions"], [7,6])
        receipt["first_distinguishing_degree"] = 156
        with self.assertRaises(ValueError):
            verify_receipt(receipt)

    def test_bounded_census(self):
        result = collision_scan(40, prefix=2, only_dim_mismatch=True)
        self.assertEqual(result["spaces_examined"], 201882)
        self.assertTrue(any(set((a.weights,b.weights)) == {A.weights,B.weights}
                            for a,b in result["collisions"]))


if __name__ == "__main__":
    unittest.main()
