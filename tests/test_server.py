import unittest
from periodlab.server import process


class ApiTests(unittest.TestCase):
    def test_analyze(self):
        obj=process("analyze",{"weights":[1,1,1,2],"count":3})
        self.assertEqual(obj["dimension"],3)
        self.assertEqual(obj["total_weight"],5)
        self.assertTrue(obj["terminality"]["terminal"])

    def test_reconstruct(self):
        out=process("reconstruct",{"total_weight":3,
               "coefficients":["1","6","90"]})
        self.assertEqual(out["weights"],[1,1,1])

    def test_dense(self):
        out=process("reconstruct-dense",{
            "coefficients":["1","0","0","6","0","0","90"]})
        self.assertEqual(out["dimension"],2)

    def test_certificate_and_standalone_verify(self):
        cert=process("certificate",{"left":[1,1,1,1,1,5,5,24],
              "right":[2,2,2,2,3,3,25],"matching":2})
        result=process("verify",{"certificate":cert})
        self.assertTrue(result["valid"])

    def test_bad_requests(self):
        for action,data in (("analyze",{"weights":[2,2,2],"count":5}),
                            ("analyze",{"weights":[1,1],"count":100}),
                            ("search",{"max_sum":100}),
                            ("certificate",{"left":[1,1],"right":[2,3]}),
                            ("unknown",{})):
            with self.assertRaises(ValueError):
                process(action,data)


if __name__=="__main__":
    unittest.main()
