import unittest
import script1
import script2

test_file = "sample.txt"


class Tests(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(script1.compute(test_file), 1147)

    def test_part_2(self):
        self.assertEqual(script2.compute(test_file), 0)

unittest.main()
