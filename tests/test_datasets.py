import tempfile
import unittest
from pathlib import Path
from periodlab.datasets import read_zenodo_rank1, PUBLISHED_MD5


class DatasetImportTests(unittest.TestCase):
    def test_published_example(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/"rank_1_dim_4.txt"
            p.write_text("[1,2,5,14,21]\n", encoding="utf-8")
            result=read_zenodo_rank1(p,expected_dim=4,require_terminal=True)
            self.assertEqual(result["row_count"],1)
            self.assertEqual(result["rows"][0].weights,(1,2,5,14,21))
            self.assertEqual(result["source_doi"],"10.5281/zenodo.5790079")
            with self.assertRaises(ValueError):
                read_zenodo_rank1(p,expected_md5="00"*16)

    def test_reject_invalid_and_nonterminal(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/"rows.txt"
            p.write_text("[1,1,1,1]\n[1,1,1,1]\n",encoding="utf-8")
            with self.assertRaises(ValueError):
                read_zenodo_rank1(p)
            p.write_text("[1,1,2]\n",encoding="utf-8")
            with self.assertRaises(ValueError):
                read_zenodo_rank1(p)
            p.write_text("__import__('os').system('true')\n",encoding="utf-8")
            with self.assertRaises(ValueError):
                read_zenodo_rank1(p,require_terminal=False)

    def test_declared_md5_shape(self):
        self.assertEqual(len(PUBLISHED_MD5),10)
        self.assertTrue(all(len(v)==32 for v in PUBLISHED_MD5.values()))


if __name__=="__main__":
    unittest.main()
