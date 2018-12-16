import unittest
import script1

TEST_FILE = "sample.txt"


class Tests(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(script1.compute(TEST_FILE), 1)

unittest.main()
