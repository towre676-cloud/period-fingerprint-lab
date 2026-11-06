"""Regression tests for two independent exact validation paths."""
import json
import unittest
from pathlib import Path

from scripts.verify_k5_effective_bound_411e8 import verify as effective_bound
from scripts.verify_k5_primecount_existence import verify as primecount_bound
from scripts.verify_signed_relation_fast import verify as verify_relation
from scripts.verify_k4_compact import read_vector

ROOT=Path(__file__).resolve().parents[1]


class FrontierValidationTests(unittest.TestCase):
    def test_effective_five_coefficient_existence(self):
        result=effective_bound()
        self.assertTrue(result["verified_conditional_on_published_prime_bound"])
        self.assertEqual(result["maximum_individual_weight_bound"],41_100_000_000)
        self.assertFalse(result["supports_an_explicit_signed_integer_witness"])
        self.assertFalse(result["guarantees_dimension_change"])

    def test_k5_dual_sieve_existence_bound(self):
        result=primecount_bound()
        self.assertTrue(result["two_independent_exact_sieves_passed"])
        self.assertEqual(result["max_individual_weight_upper_bound"],2_867_000)
        self.assertEqual(result["rational_kernel_dimension_at_least"],25)
        self.assertEqual(result["same_dimension_kernel_dimension_at_least"],24)
        self.assertFalse(result["explicit_signed_integer_relation_produced"])

    def test_independent_three_coefficient_witness(self):
        document=json.loads((ROOT/"research/k3_exact_relations.json").read_text())
        rec=next(x for x in document["relations"] if x["id"]=="K3-W172")
        result=verify_relation(rec["signed_multiplicities"],K=3)
        self.assertEqual(result["discrepant_prime_counts"][:3],[0,0,0])
        self.assertGreater(result["discrepant_prime_counts"][3],0)
        self.assertEqual(result["final_dimensions"],[14,14])

    def test_fast_four_coefficient_witness_and_corruption(self):
        vector=read_vector()  # Existing independent compressed-source checksum.
        signed=[[i+1,v] for i,v in enumerate(vector) if v]
        result=verify_relation(signed,K=4)
        self.assertEqual(result["discrepant_prime_counts"],[0,0,0,0,367])
        self.assertEqual(result["final_dimensions"],[12621,12622])
        bad=[pair[:] for pair in signed]
        bad[0][1]+=1
        with self.assertRaises(ValueError):
            verify_relation(bad,K=4)


if __name__=="__main__":
    unittest.main()
