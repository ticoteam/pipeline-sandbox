import unittest

from calc import add, multiply, negate, power, subtract


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


class MultiplyTest(unittest.TestCase):
    def test_multiply_positive(self):
        self.assertEqual(multiply(3, 4), 12)

    def test_multiply_negative(self):
        self.assertEqual(multiply(-3, 4), -12)

    def test_multiply_floats(self):
        self.assertEqual(multiply(2.5, 2), 5.0)

    def test_multiply_zero(self):
        self.assertEqual(multiply(7, 0), 0)

    def test_multiply_rejects_non_number_first_argument(self):
        for bad, name in (("a", "str"), (None, "NoneType")):
            with self.assertRaises(TypeError) as ctx:
                multiply(bad, 3)
            self.assertIn("'a'", str(ctx.exception))
            self.assertIn(name, str(ctx.exception))

    def test_multiply_rejects_non_number_second_argument(self):
        with self.assertRaises(TypeError) as ctx:
            multiply(3, None)
        self.assertIn("'b'", str(ctx.exception))
        self.assertIn("NoneType", str(ctx.exception))

    def test_multiply_does_not_repeat_strings(self):
        with self.assertRaises(TypeError) as ctx:
            multiply("ab", 3)
        self.assertIn("'a'", str(ctx.exception))
        self.assertIn("str", str(ctx.exception))


class PowerTests(unittest.TestCase):
    def test_power_positive_whole_numbers(self):
        self.assertEqual(power(2, 3), 8)

    def test_power_zero_exponent(self):
        self.assertEqual(power(5, 0), 1)

    def test_power_zero_to_the_zero_is_one(self):
        self.assertEqual(power(0, 0), 1)

    def test_power_negative_exponent(self):
        self.assertEqual(power(2, -2), 0.25)

    def test_power_negative_base_whole_exponent(self):
        self.assertEqual(power(-2, 3), -8)

    def test_power_float_exponent(self):
        self.assertEqual(power(9, 0.5), 3.0)

    def test_power_zero_base_positive_exponent(self):
        self.assertEqual(power(0, 5), 0)

    def test_power_zero_base_negative_exponent_raises(self):
        with self.assertRaises(ZeroDivisionError) as ctx:
            power(0, -1)
        self.assertIn("'a'", str(ctx.exception))

    def test_power_negative_base_non_whole_exponent_raises(self):
        with self.assertRaises(ValueError) as ctx:
            power(-8, 0.5)
        self.assertTrue(str(ctx.exception))

    def test_power_rejects_non_number_first_argument(self):
        with self.assertRaises(TypeError) as ctx:
            power("a", 3)
        self.assertIn("'a'", str(ctx.exception))
        self.assertIn("str", str(ctx.exception))

    def test_power_rejects_non_number_second_argument(self):
        with self.assertRaises(TypeError) as ctx:
            power(3, None)
        self.assertIn("'b'", str(ctx.exception))
        self.assertIn("NoneType", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
