import unittest
import script1
import script2

test_file = "sample5.txt"


class Tests(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(script1.compute(test_file), 18740)

    def test_part_2(self):
        self.assertEqual(script2.wrapper(test_file), 1140)

unittest.main()
