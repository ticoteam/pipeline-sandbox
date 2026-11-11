import unittest

from calc import add, negate, subtract


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


class NegateTest(unittest.TestCase):
    def test_negate_positive(self):
        self.assertEqual(negate(5), -5)

    def test_negate_negative_float(self):
        self.assertEqual(negate(-2.5), 2.5)

    def test_negate_zero(self):
        self.assertEqual(negate(0), 0)

    def test_negate_float_zero(self):
        self.assertEqual(negate(0.0), 0.0)
        self.assertEqual(str(negate(0.0)), "-0.0")

    def test_negate_rejects_non_numbers(self):
        with self.assertRaises(TypeError):
            negate("a")
        with self.assertRaises(TypeError):
            negate(None)


if __name__ == "__main__":
    unittest.main()
