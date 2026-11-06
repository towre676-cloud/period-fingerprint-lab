import unittest
from periodlab.relations import valuation_matrix, nullspace, integer_basis, pair_from_relation, discover_relation
from periodlab.periods import coefficient
from periodlab.weights import WeightedProjective


class RelationTests(unittest.TestCase):
    def test_small_nullspace(self):
        self.assertEqual(nullspace([[1,1,1],[0,1,2]])[0], [1,-2,1])
        self.assertEqual(integer_basis([[1,1,1],[0,1,2]]),[[1,-2,1]])

    def test_rediscover_finite_collision(self):
        rows,_=valuation_matrix(25,2)
        known=[0]*25
        for w,c in {1:5,2:-4,3:-2,5:2,24:1,25:-1}.items():
            known[w-1]=c
        self.assertTrue(all(sum(a*b for a,b in zip(row,known))==0 for row in rows))
        a,b=pair_from_relation(known,2)
        self.assertEqual(a.total_weight,b.total_weight)
        self.assertNotEqual(a.weights,b.weights)
        for m in (1,2):
            self.assertEqual(coefficient(a,m),coefficient(b,m))

    def test_generated_basis(self):
        result=discover_relation(25,2)
        self.assertTrue(result["found"])
        self.assertGreaterEqual(result["nullity"],1)
        self.assertEqual(result["total_weight"],
                         sum(result["left"]))
        self.assertEqual(result["total_weight"],
                         sum(result["right"]))

    def test_bad_inputs(self):
        with self.assertRaises(ValueError):
            valuation_matrix(0,2)
        with self.assertRaises(ValueError):
            pair_from_relation([1,1],1)


if __name__=="__main__":
    unittest.main()
