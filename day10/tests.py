import unittest
import script

test_file = "sample.txt"


class Tests(unittest.TestCase):

    def test_part_1_and_2(self):
        self.assertEqual(script.compute(test_file, 10), 3)


if __name__ == '__main__':
    unittest.main()
