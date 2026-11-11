import unittest

from calc import add, subtract


class AddTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)


class SubtractTest(unittest.TestCase):
    def test_subtract_positive(self):
        self.assertEqual(subtract(5, 3), 2)

    def test_subtract_negative_result(self):
        self.assertEqual(subtract(3, 5), -2)

    def test_subtract_floats(self):
        self.assertEqual(subtract(2.5, 0.5), 2.0)

    def test_subtract_zero(self):
        self.assertEqual(subtract(7, 0), 7)

    def test_subtract_rejects_non_numbers(self):
        with self.assertRaises(TypeError):
            subtract("a", 1)
        with self.assertRaises(TypeError):
            subtract(None, 1)


if __name__ == "__main__":
    unittest.main()
