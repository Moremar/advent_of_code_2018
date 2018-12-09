import unittest
import script1
import script2

TEST_FILE_1 = "sample1.txt"
TEST_FILE_2 = "sample2.txt"


class Tests(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(script1.compute(TEST_FILE_1), 12)

    def test_part_2(self):
        self.assertEqual(script2.compute(TEST_FILE_2), 'fgij')


unittest.main()
