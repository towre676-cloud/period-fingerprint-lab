import unittest
from fractions import Fraction
from period_fingerprint_demo import (
    coefficient, exact_ratio, dimension_proxy, enumerate_collisions,
    prime_valuations_equal, validate, is_well_formed,
)


A = (1,1,1,1,1,5,5,24)
B = (2,2,2,2,3,3,25)


class PeriodFingerprintTests(unittest.TestCase):
    def test_exact_recurrence(self):
        validate()
        self.assertEqual(exact_ratio((1,1,1), 0), Fraction(6))
        self.assertEqual(coefficient((1,1,1), 2), 90)

    def test_dimensional_limits(self):
        for weights in ((1,1), (1,1,1,2), (1,2,3,5,7)):
            self.assertLess(abs(dimension_proxy(weights, 1000)
                                - (len(weights)-1)), 0.01)

    def test_two_term_collision(self):
        self.assertTrue(is_well_formed(A))
        self.assertTrue(is_well_formed(B))
        self.assertNotEqual(len(A), len(B))
        self.assertEqual(sum(A), sum(B))
        for m in (1, 2):
            self.assertEqual(coefficient(A, m), coefficient(B, m))
            self.assertTrue(prime_valuations_equal(A, B, m))
        self.assertEqual(Fraction(coefficient(A, 3), coefficient(B, 3)),
                         Fraction(1080400, 1002001))
        self.assertFalse(prime_valuations_equal(A, B, 3))

    def test_bounded_census(self):
        count, first, pairs = enumerate_collisions(40)
        self.assertEqual(count, 201882)
        self.assertEqual(first[0], 39)
        self.assertEqual({first[1], first[2]}, {A, B})
        self.assertEqual(pairs, 2)


if __name__ == "__main__":
    unittest.main()
