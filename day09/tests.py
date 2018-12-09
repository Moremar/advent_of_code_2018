import unittest
import script1
import script2

test_file = "sample.txt"


class Tests(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(script1.compute(test_file), 32)

    def test_part_2(self):
        self.assertEqual(script2.compute(test_file), 22563)


if __name__ == '__main__':
    unittest.main()
