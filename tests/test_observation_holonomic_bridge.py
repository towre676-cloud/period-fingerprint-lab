"""Exact independent checks for period observability and holonomic certificates."""
import unittest

from periodlab.observation_design import design_exact_observations
from periodlab.holonomic import holonomic_receipt, operator_polynomials
from periodlab.weights import WeightedProjective
from periodlab.periods import coefficient


class ObservationBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.left=WeightedProjective.from_weights((1,1,1,1,1,5,5,24))
        cls.right=WeightedProjective.from_weights((2,2,2,2,3,3,25))

    def test_known_collision_forces_third_observation(self):
        r=design_exact_observations([self.left,self.right], [1,2,3], budget=1)
        self.assertEqual(r["status"],"separating")
        self.assertEqual(r["selected_supported_indices"],[3])
        self.assertEqual(r["known_total_weight"],39)
        self.assertEqual(r["total_candidate_pairs"],1)

    def test_budget_insufficient_to_separate_prefix(self):
        r=design_exact_observations([self.left,self.right],[1,2],budget=2)
        self.assertEqual(r["status"],"indistinguishable_within_allowed_indices")
        self.assertEqual(r["globally_ambiguous_pair_within_allowed"],[0,1])

    def test_zero_budget_is_explicit(self):
        r=design_exact_observations([self.left,self.right],[1,2,3],budget=0)
        self.assertEqual(r["status"],"insufficient_observation_budget")
        self.assertEqual(r["selected_supported_indices"],[])
        self.assertEqual(r["suggested_next_supported_index"],3)

    def test_budget_cap_prevents_false_optimality(self):
        with self.assertRaisesRegex(ValueError,"no partial optimality result"):
            design_exact_observations([self.left,self.right],range(1,8),budget=4,max_panels=3)

    def test_common_support_required(self):
        other=WeightedProjective.from_weights((1,1,1))
        with self.assertRaises(ValueError):
            design_exact_observations([other,self.left],[1,2],budget=2)

    def test_holonomic_for_projective_plane(self):
        space=WeightedProjective.from_weights((1,1,1))
        A,B,D=operator_polynomials(space)
        self.assertEqual(A,[0,0,0,1])
        self.assertEqual(B,[6,33,54,27])
        self.assertEqual(D,[1,3,3,1])
        r=holonomic_receipt(space,checks=5)
        self.assertEqual(r["supported_coefficients"][:3],["1","6","90"])
        self.assertEqual(r["theta_polynomial_A_ascending"],["0","0","0","1"])

    def test_holonomic_for_collision_pair(self):
        for space in (self.left,self.right):
            r=holonomic_receipt(space,checks=3)
            self.assertEqual(r["support_step"],39)
            self.assertEqual(len(r["theta_polynomial_A_ascending"]),40)
            self.assertEqual(r["supported_coefficients"],
                             [str(coefficient(space,m)) for m in range(4)])


if __name__=="__main__":
    unittest.main()
