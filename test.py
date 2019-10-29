import unittest
import edgar
import tempfile


class TestStringMethods(unittest.TestCase):
    def test_edgar(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            print("created temporary directory", tmpdirname)
            edgar.download_index(tmpdirname, 2019)
            file_name = tmpdirname + "/2019-QTR1.tsv"

            with open(file_name, "r", encoding="utf-8") as f:
                first_line = f.readline()
                self.assertEqual(
                    first_line,
                    "1000045|NICHOLAS FINANCIAL INC|10-Q|2019-02-14|edgar/data/1000045/0001193125-19-039489.txt|edgar/data/1000045/0001193125-19-039489-index.html\n",
                )


if __name__ == "__main__":
    unittest.main()
