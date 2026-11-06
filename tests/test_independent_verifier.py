import copy
import unittest
from periodlab.weights import WeightedProjective
from periodlab.certificates import collision_receipt
from periodlab.reconstruction_receipt import receipt_for_weights, make_reconstruction_receipt
from verify_receipt import verify


A=WeightedProjective.from_weights((1,1,1,1,1,5,5,24))
B=WeightedProjective.from_weights((2,2,2,2,3,3,25))


class IndependentReceiptTests(unittest.TestCase):
    def test_collision_checker_independent(self):
        data=collision_receipt(A,B,2)
        self.assertTrue(verify(data)["valid"])
        for field,other in (
            ("first_distinguishing_degree",156),
            ("total_weight",38),
        ):
            bad=copy.deepcopy(data)
            bad[field]=other
            with self.assertRaises(ValueError):
                verify(bad)
        bad=copy.deepcopy(data)
        bad["terminality"]["left"]["terminal"]=True
        with self.assertRaises(ValueError):
            verify(bad)

    def test_finite_reconstruction_receipts(self):
        for w in ((1,1), (1,1,1), (1,1,1,2),
                  (1,2,3,5,7), (1,1,1,1,1,5,5,24)):
            data=receipt_for_weights(w)
            out=verify(data)
            self.assertTrue(out["valid"])
            self.assertEqual(out["dimension"],len(w)-1)
            bad=copy.deepcopy(data)
            bad["denominator_polynomial_ascending"][0]="0"
            with self.assertRaises(ValueError):
                verify(bad)

    def test_reconstruction_receipt_corruption(self):
        data=receipt_for_weights((1,1,1,2))
        bad=copy.deepcopy(data)
        bad["supported_coefficients"][2]="17"
        with self.assertRaises(ValueError):
            verify(bad)
        bad=copy.deepcopy(data)
        bad["reconstructed_weights"]=[1,1,1,1,1]
        with self.assertRaises(ValueError):
            verify(bad)


if __name__=="__main__":
    unittest.main()
