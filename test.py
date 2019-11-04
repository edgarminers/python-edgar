import unittest
import edgar
import tempfile


def _get_qtr_of_year(year=2019, qtr=1):
    assert(1 <= qtr <= 4)
    # Direct use of internal function
    return edgar.main._quarterly_idx_list(year)[-4:4][-1 * qtr]


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

    def test_skip_files(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            print("created temporary directory", tmpdirname)
            data_qtr1_2019 = _get_qtr_of_year(year=2019, qtr=1)
            file_name = tmpdirname + '/' + data_qtr1_2019[1]
            # Now create a dummy file
            with open(file_name, "wb") as fp:
                fp.write(b"FAKE")
            # download it with skipping
            edgar.download(data_qtr1_2019, tmpdirname, skip_file=True)
            # -> Should have ignored it!
            with open(file_name, "r") as fp:
                self.assertEqual(fp.readline(), "FAKE")


if __name__ == "__main__":
    unittest.main()
