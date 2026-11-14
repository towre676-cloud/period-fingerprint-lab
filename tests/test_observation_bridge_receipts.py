"""Independent bridge receipt regression and tampering rejection."""
import copy
import unittest

import verify_observation_bridge as independent
from periodlab.holonomic import holonomic_receipt
from periodlab.observation_design import design_exact_observations
from periodlab.weights import WeightedProjective


class BridgeReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=WeightedProjective.from_weights((1,1,1,1,1,5,5,24))
        cls.b=WeightedProjective.from_weights((2,2,2,2,3,3,25))

    def test_observation_receipt(self):
        r=design_exact_observations([self.a,self.b], [1,2,3],budget=1)
        v=independent.verify(r)
        self.assertTrue(v["valid"])
        self.assertEqual(v["selected_supported_indices"],[3])

    def test_observation_tampering(self):
        r=design_exact_observations([self.a,self.b],[1,2],budget=2)
        self.assertTrue(independent.verify(r)["valid"])
        for key,val in (("status","separating"),
                        ("panels_examined",1),
                        ("separated_candidate_pairs",1),
                        ("suggested_next_supported_index",3)):
            with self.subTest(field=key):
                t=copy.deepcopy(r)
                t[key]=val
                with self.assertRaisesRegex(ValueError, "invalid exact observation claim: " + key):
                    independent.verify(t)

    def test_observation_signature_corruption(self):
        r=design_exact_observations([self.a,self.b],[1,2,3],budget=1)
        for field in ("selected_signatures", "all_allowed_signatures"):
            with self.subTest(field=field):
                t=copy.deepcopy(r)
                t[field][0][0]="0"
                with self.assertRaisesRegex(ValueError, field):
                    independent.verify(t)

    def test_holonomic_receipt_and_corruption(self):
        r=holonomic_receipt(WeightedProjective.from_weights((1,1,1)),5)
        self.assertTrue(independent.verify(r)["valid"])
        t=copy.deepcopy(r)
        t["theta_polynomial_A_ascending"][1]="1"
        with self.assertRaises(ValueError):
            independent.verify(t)
        t=copy.deepcopy(r)
        t["supported_coefficients"][2]="91"
        with self.assertRaises(ValueError):
            independent.verify(t)


if __name__=="__main__":
    unittest.main()
