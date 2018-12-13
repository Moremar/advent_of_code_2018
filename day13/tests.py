import unittest
import script1
import script2

test_file1 = "sample.txt"
test_file2 = "sample2.txt"


class Tests(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(script1.compute(test_file1), (7,3))

    def test_part_2(self):
        self.assertEqual(script2.compute(test_file2), (6,4))

unittest.main()
