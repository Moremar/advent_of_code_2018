import unittest
import script1

test_file1 = "sample1.txt"
test_file2 = "sample2.txt"


class Tests(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(script1.compute(test_file1), 23)
        self.assertEqual(script1.compute(test_file2), 31)

unittest.main()
