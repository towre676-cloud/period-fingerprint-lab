"""Tests for fully dense finite period reconstruction."""
import unittest
from periodlab.weights import WeightedProjective
from periodlab.periods import coefficient_at_degree
from periodlab.reconstruct import reconstruct_dense_prefix


class DenseReconstructionTests(unittest.TestCase):
    def test_known_weight_families(self):
        for w in ((1,1), (1,1,1), (1,1,1,2), (1,2,3,5,7)):
            space=WeightedProjective.from_weights(w)
            L=space.total_weight
            dense=[coefficient_at_degree(space,d) for d in range(L*(L-1)+1)]
            result=reconstruct_dense_prefix(dense)
            self.assertEqual(result["weights"],list(space.weights))
            self.assertEqual(result["dimension"],space.dimension)
            self.assertEqual(result["total_weight"],L)

    def test_insufficient_information_and_tampering(self):
        space=WeightedProjective.from_weights((1,1,1))
        dense=[coefficient_at_degree(space,d) for d in range(7)]
        with self.assertRaises(ValueError):
            reconstruct_dense_prefix(dense[:6])
        bad=dense[:]
        bad[4]=1
        with self.assertRaises(ValueError):
            reconstruct_dense_prefix(bad)
        with self.assertRaises(ValueError):
            reconstruct_dense_prefix([1,0,0,0,0,0,0])
        with self.assertRaises(ValueError):
            reconstruct_dense_prefix([1,1,2])


if __name__=="__main__":
    unittest.main()
