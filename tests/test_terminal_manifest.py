"""Replay every listed classified weight-51 witness from the committed JSON."""
import json
from pathlib import Path
import unittest
from periodlab.weights import WeightedProjective, is_terminal
from periodlab.periods import coefficient


class TerminalManifestTests(unittest.TestCase):
    def test_all_classified_pairs(self):
        path=Path(__file__).resolve().parents[1]/"research"/"terminal_51_all_77.json"
        data=json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["schema"],"periodlab/terminal-2prefix-classification/v1")
        self.assertEqual(data["count"],77)
        self.assertEqual(len(data["pairs"]),77)
        seen=set()
        for rec in data["pairs"]:
            a=WeightedProjective.from_weights(rec["weights_A"])
            b=WeightedProjective.from_weights(rec["weights_B"])
            self.assertEqual(a.total_weight,b.total_weight)
            self.assertEqual(a.total_weight,51)
            self.assertTrue(is_terminal(a))
            self.assertTrue(is_terminal(b))
            self.assertEqual(coefficient(a,1),coefficient(b,1))
            self.assertEqual(coefficient(a,2),coefficient(b,2))
            self.assertNotEqual(coefficient(a,3),coefficient(b,3))
            self.assertEqual([a.dimension,b.dimension],rec["dimensions"])
            self.assertEqual(rec["id"],len(seen)+1)
            pair=(a.weights,b.weights)
            self.assertNotIn(pair,seen)
            seen.add(pair)


if __name__=="__main__":
    unittest.main()
