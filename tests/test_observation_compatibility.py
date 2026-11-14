"""Cross-contract checks: shared data, distinct search and theorem scopes."""
import copy
import unittest
from fractions import Fraction

from periodlab.holonomic import holonomic_receipt
from periodlab.observation_design import design_exact_observations
from periodlab.observation_engine import analyze
from periodlab.search import partitions
from periodlab.weights import WeightedProjective as W, is_terminal
import verify_observation_bridge as bridge
import verify_observation_engine as engine


WEIGHTS = [(1,1,1,1,1,5,5,24), (2,2,2,2,3,3,25)]


def specification(weights=WEIGHTS, sensors=(1,2,3), budget=2):
    return {"family":"weighted_projective",
            "universe":{"kind":"explicit", "weights":[list(w) for w in weights]},
            "sensors":list(sensors), "budget":budget}


class ObservationCompatibilityTests(unittest.TestCase):
    def test_weight39_exact_data_and_prefix_collision(self):
        planner=design_exact_observations([W(w) for w in WEIGHTS], [1,2], 2)
        receipt=analyze(specification())
        self.assertTrue(bridge.verify(planner)["valid"])
        self.assertTrue(engine.verify(receipt)["verified"])
        self.assertEqual(planner["status"], "indistinguishable_within_allowed_indices")
        self.assertEqual(receipt["result"]["status"], "exact_collision")
        for w, row in zip(WEIGHTS, planner["all_allowed_signatures"]):
            self.assertFalse(is_terminal(W(w)))
            self.assertEqual(row, receipt["result"]["witness"]["shared_observations"])
            for m in (1,2,3):
                self.assertEqual(bridge.coefficient(w,m), engine.period(w,m))
        sep=receipt["result"]["pair_separator"]
        self.assertEqual(sep["sensor"], {"supported_index":3, "degree":117})
        self.assertEqual(Fraction(int(sep["left_value"]), int(sep["right_value"])),
                         Fraction(1080400,1002001))

    def test_minimum_panel_equals_zero_prefix_completion(self):
        planner=design_exact_observations([W(w) for w in WEIGHTS], range(1,4), 1)
        receipt=analyze(specification(budget=0))
        self.assertTrue(bridge.verify(planner)["valid"])
        self.assertTrue(engine.verify(receipt)["verified"])
        positions=receipt["result"]["minimum_completion"]["sensors"]
        indices=[receipt["spec"]["sensors"][k-1]["supported_index"] for k in positions]
        self.assertEqual(planner["selected_supported_indices"], indices)
        self.assertEqual(indices, [3])

    def test_selected_panel_maps_to_ordered_catalog_prefix(self):
        planner=design_exact_observations([W(w) for w in WEIGHTS], [1,2,3], 1)
        selected=planner["selected_supported_indices"]
        receipt=analyze(specification(sensors=selected+[1,2], budget=len(selected)))
        self.assertTrue(engine.verify(receipt)["verified"])
        self.assertEqual(receipt["result"]["status"], "finite_reconstruction")
        # The same numeric budget on the original catalog measures coefficient 1.
        self.assertEqual(analyze(specification(budget=1))["result"]["status"], "exact_collision")

    def test_small_complete_classes_agree_on_minimum_and_signatures(self):
        for L in (4,7,9,12):
            models=[]
            for w in partitions(L):
                try:
                    models.append(W(w))
                except ValueError:
                    pass
            with self.subTest(total_weight=L):
                planner=design_exact_observations(models, [1,2,3], 3)
                receipt=analyze(specification([s.weights for s in models], budget=0))
                self.assertTrue(bridge.verify(planner)["valid"])
                self.assertTrue(engine.verify(receipt)["verified"])
                self.assertEqual(planner["status"], "separating")
                completion=receipt["result"]["minimum_completion"]
                self.assertEqual(completion["status"], "available")
                self.assertEqual(planner["selected_supported_indices"], completion["sensors"])
                for s,row in zip(models,planner["all_allowed_signatures"]):
                    self.assertEqual(row, [str(engine.period(s.weights,m)) for m in (1,2,3)])

    def test_candidate_identity_is_by_weights_not_position(self):
        planner=design_exact_observations([W(w) for w in reversed(WEIGHTS)], [1,2,3], 1)
        receipt=analyze(specification(list(reversed(WEIGHTS))))
        self.assertTrue(bridge.verify(planner)["valid"])
        self.assertTrue(engine.verify(receipt)["verified"])
        self.assertNotEqual(planner["model_weights"], receipt["spec"]["universe"]["weights"])
        rows=dict(zip(map(tuple,planner["model_weights"]),planner["all_allowed_signatures"]))
        for w in receipt["spec"]["universe"]["weights"]:
            self.assertEqual(rows[tuple(w)], [str(engine.period(w,m)) for m in (1,2,3)])

    def test_holonomic_coefficients_agree_without_reconstruction_claim(self):
        for w in WEIGHTS:
            with self.subTest(weights=w):
                receipt=holonomic_receipt(W(w), checks=3)
                self.assertTrue(bridge.verify(receipt)["valid"])
                self.assertEqual(receipt["supported_coefficients"],
                                 [str(engine.period(w,m)) for m in range(4)])
                bad=copy.deepcopy(receipt)
                # Use a guaranteed change, even if that coefficient was already zero.
                bad["theta_polynomial_A_ascending"][1]=str(
                    int(receipt["theta_polynomial_A_ascending"][1])+1)
                with self.assertRaises(ValueError):
                    bridge.verify(bad)

    def test_catalog_theorem_coverage_is_not_budget_coverage(self):
        ws=[(1,1,1,1),(1,1,2)]
        planner=design_exact_observations([W(w) for w in ws], [1,2,3], 0)
        receipt=analyze(specification(ws, budget=0))
        self.assertTrue(bridge.verify(planner)["valid"])
        self.assertTrue(engine.verify(receipt)["verified"])
        self.assertTrue(planner["known_weight_reconstruction_theorem_applies"])
        self.assertFalse(receipt["result"]["known_weight_theorem"]["covered_by_budget"])
        self.assertEqual(planner["selected_supported_indices"], [])

    def test_finite_identification_does_not_prove_unrestricted_linear_inverse(self):
        spec={"family":"rational_linear", "universe":{
            "kind":"explicit", "vectors":[[0,0],[1,0]]},
            "sensors":[{"name":"x", "coefficients":[1,0]}], "budget":1}
        finite=analyze(spec)
        spec["universe"]={"kind":"all_rational", "dimension":2}
        unrestricted=analyze(spec)
        self.assertTrue(engine.verify(finite)["verified"])
        self.assertTrue(engine.verify(unrestricted)["verified"])
        self.assertEqual(finite["result"]["status"], "finite_reconstruction")
        self.assertEqual(unrestricted["result"]["status"], "exact_collision")
        self.assertEqual(unrestricted["result"]["kernel_dimension"], 1)

    def test_both_verifiers_reject_corrupted_common_evidence(self):
        planner=design_exact_observations([W(w) for w in WEIGHTS], [1,2,3], 1)
        receipt=analyze(specification())
        planner["all_allowed_signatures"][0][2]="0"
        receipt["result"]["pair_separator"]["left_value"]="0"
        for checker, bad in ((bridge.verify,planner),(engine.verify,receipt)):
            with self.subTest(checker=checker.__module__):
                with self.assertRaises(ValueError):
                    checker(bad)


if __name__=="__main__":
    unittest.main()
