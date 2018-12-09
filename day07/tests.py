import unittest
import script1
import script2

TEST_FILE = "sample.txt"


class Tests(unittest.TestCase):

    def test_1(self):
        self.assertEqual(script1.compute(TEST_FILE), 'CABDFE')

    def test_2(self):
        self.assertEqual(script2.compute(TEST_FILE, 2, 0), 15)


if __name__ == '__main__':
    unittest.main()
