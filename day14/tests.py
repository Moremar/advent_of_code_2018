import unittest
import script1
import script2


class Tests(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(script1.compute(2018), '5941429882')

    def test_part_2(self):
        self.assertEqual(script2.compute('5941429882'), 2018)

unittest.main()
