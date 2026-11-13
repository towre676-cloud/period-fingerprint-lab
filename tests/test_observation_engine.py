"""Regression tests for exact observation design, with independent receipt replay."""
import copy
import unittest
from fractions import Fraction

from periodlab.observation_engine import analyze
from verify_observation_engine import verify


class ObservationEngineTests(unittest.TestCase):
    def test_exact_linear_inverse(self):
        spec={"family":"rational_linear","universe":{"kind":"all_rational","dimension":3},
              "sensors":[{"name":"sum","coefficients":[1,1,1]},
                         {"name":"difference","coefficients":[1,-1,0]},
                         {"name":"z","coefficients":[0,0,1]}],"budget":3}
        receipt=analyze(spec)
        self.assertEqual(receipt["result"]["status"],"linear_reconstruction_theorem")
        self.assertTrue(verify(receipt)["verified"])
        broken=copy.deepcopy(receipt)
        broken["result"]["inverse_matrix"][0][0]="3"
        with self.assertRaises(ValueError):
            verify(broken)

    def test_rank_deficiency_and_optimal_extra_sensor(self):
        spec={"family":"rational_linear","universe":{"kind":"all_rational","dimension":3},
              "sensors":[{"name":"sum","coefficients":[1,1,1]},
                         {"name":"difference","coefficients":[1,-1,0]},
                         {"name":"z","coefficients":[0,0,1]}],"budget":2}
        receipt=analyze(spec)
        self.assertEqual(receipt["result"]["kernel_dimension"],1)
        self.assertEqual(receipt["result"]["pair_separator"]["sensor_position"],3)
        self.assertEqual(receipt["result"]["minimum_completion"]["sensors"],[3])
        self.assertTrue(verify(receipt)["verified"])
        receipt["result"]["witness"]["right"][0]="9"
        with self.assertRaises(ValueError):
            verify(receipt)

    def test_impossible_catalog(self):
        spec={"family":"rational_linear","universe":{"kind":"all_rational","dimension":3},
              "sensors":[{"name":"sum","coefficients":[1,1,1]}],"budget":1}
        receipt=analyze(spec)
        self.assertIsNone(receipt["result"]["pair_separator"])
        self.assertEqual(receipt["result"]["minimum_completion"]["status"],"impossible_in_catalog")
        self.assertTrue(verify(receipt)["verified"])

    def test_zero_observation_budget(self):
        spec={"family":"rational_linear","universe":{"kind":"all_rational","dimension":2},
              "sensors":[],"budget":0}
        self.assertTrue(verify(analyze(spec))["verified"])

    def test_finite_rational_minimum(self):
        spec={"family":"rational_linear","universe":{"kind":"explicit",
              "vectors":[[0,0],[1,0],[0,1],[1,1]]},
              "sensors":[{"name":"sum","coefficients":[1,1]},
                         {"name":"x","coefficients":[1,0]},
                         {"name":"y","coefficients":[0,1]}],"budget":1}
        receipt=analyze(spec)
        self.assertEqual(receipt["result"]["ambiguous_pair_count"],1)
        self.assertEqual(receipt["result"]["minimum_completion"]["sensors"],[2])
        self.assertTrue(verify(receipt)["verified"])
        spec["budget"]=2
        self.assertEqual(analyze(spec)["result"]["status"],"finite_reconstruction")

    def test_period_degree_117(self):
        spec={"family":"weighted_projective","universe":{"kind":"explicit",
              "weights":[[1,1,1,1,1,5,5,24],[2,2,2,2,3,3,25]]},
              "sensors":[1,2,3],"budget":2}
        receipt=analyze(spec)
        outcome=receipt["result"]
        self.assertEqual(outcome["pair_separator"]["sensor"]["degree"],117)
        self.assertEqual(outcome["minimum_completion"]["sensors"],[3])
        self.assertEqual(Fraction(int(outcome["pair_separator"]["left_value"]),
                                  int(outcome["pair_separator"]["right_value"])),
                         Fraction(1080400,1002001))
        self.assertTrue(verify(receipt)["verified"])
        damaged=copy.deepcopy(receipt)
        damaged["result"]["pair_separator"]["left_value"]="3"
        with self.assertRaises(ValueError):
            verify(damaged)

    def test_bounded_class_reconstruction(self):
        spec={"family":"weighted_projective",
              "universe":{"kind":"bounded","total_weight":7,"terminal_only":False},
              "sensors":[1,2,3],"budget":2}
        receipt=analyze(spec)
        self.assertEqual(receipt["result"]["model_count"],7)
        self.assertEqual(receipt["result"]["status"],"finite_reconstruction")
        self.assertTrue(verify(receipt)["verified"])
        receipt["result"]["table_sha256"]="0"*64
        with self.assertRaises(ValueError):
            verify(receipt)

    def test_known_weight_global_theorem_coverage(self):
        spec={"family":"weighted_projective","universe":{"kind":"explicit",
              "weights":[[1,1,1,1],[1,1,2]]},"sensors":[1,2,3],"budget":3}
        receipt=analyze(spec)
        self.assertTrue(receipt["result"]["known_weight_theorem"]["covered_by_budget"])
        self.assertTrue(verify(receipt)["verified"])

    def test_input_validation(self):
        spec={"family":"rational_linear","universe":{"kind":"all_rational","dimension":2},
              "sensors":[{"name":"x","coefficients":[0.1,1]}],"budget":1}
        with self.assertRaises(ValueError):
            analyze(spec)
        spec["sensors"][0]["coefficients"]=["1/2",1]
        spec["budget"]=2
        with self.assertRaises(ValueError):
            analyze(spec)


if __name__=="__main__":
    unittest.main()
