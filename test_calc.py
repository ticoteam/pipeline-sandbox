import math
import unittest

from calc import absolute_value, add, cube_of, floor_divide, modulo, multiply, negate, power, sqrt, subtract


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


class ModuloTest(unittest.TestCase):
    def test_modulo_positive(self):
        self.assertEqual(modulo(7, 3), 1)

    def test_modulo_even_division(self):
        self.assertEqual(modulo(6, 3), 0)

    def test_modulo_first_smaller(self):
        self.assertEqual(modulo(2, 5), 2)

    def test_modulo_negative_first_takes_sign_of_b(self):
        self.assertEqual(modulo(-7, 3), 2)

    def test_modulo_negative_second_takes_sign_of_b(self):
        self.assertEqual(modulo(7, -3), -2)

    def test_modulo_floats(self):
        self.assertEqual(modulo(5.5, 2), 1.5)

    def test_modulo_ints_give_int(self):
        self.assertIsInstance(modulo(7, 3), int)

    def test_modulo_zero_first(self):
        self.assertEqual(modulo(0, 5), 0)

    def test_modulo_zero_second_raises(self):
        with self.assertRaises(ZeroDivisionError) as ctx:
            modulo(5, 0)
        self.assertIn("'b'", str(ctx.exception))

    def test_modulo_rejects_non_number_first_argument(self):
        with self.assertRaises(TypeError) as ctx:
            modulo("a", 3)
        self.assertIn("'a'", str(ctx.exception))
        self.assertIn("str", str(ctx.exception))

    def test_modulo_rejects_non_number_second_argument(self):
        with self.assertRaises(TypeError) as ctx:
            modulo(3, None)
        self.assertIn("'b'", str(ctx.exception))
        self.assertIn("NoneType", str(ctx.exception))


class AbsoluteValueTest(unittest.TestCase):
    def test_absolute_value_negative_whole_number(self):
        self.assertEqual(absolute_value(-5), 5)

    def test_absolute_value_positive_whole_number(self):
        self.assertEqual(absolute_value(5), 5)

    def test_absolute_value_zero(self):
        self.assertEqual(absolute_value(0), 0)

    def test_absolute_value_negative_float(self):
        self.assertEqual(absolute_value(-2.5), 2.5)

    def test_absolute_value_negative_float_zero(self):
        result = absolute_value(-0.0)
        self.assertEqual(result, 0.0)
        self.assertEqual(math.copysign(1, result), 1.0)

    def test_absolute_value_keeps_int_and_float_types(self):
        self.assertIsInstance(absolute_value(-5), int)
        self.assertIsInstance(absolute_value(-2.5), float)

    def test_absolute_value_rejects_string(self):
        with self.assertRaises(TypeError) as ctx:
            absolute_value("a")
        self.assertIn("'a'", str(ctx.exception))
        self.assertIn("str", str(ctx.exception))

    def test_absolute_value_does_not_convert_numeric_string(self):
        with self.assertRaises(TypeError):
            absolute_value("-5")

    def test_absolute_value_accepts_bool_as_int(self):
        self.assertEqual(absolute_value(True), 1)
        self.assertIs(type(absolute_value(True)), int)
        self.assertEqual(absolute_value(False), 0)
        self.assertIs(type(absolute_value(False)), int)

    def test_absolute_value_rejects_none(self):
        with self.assertRaises(TypeError) as ctx:
            absolute_value(None)
        self.assertIn("'a'", str(ctx.exception))
        self.assertIn("NoneType", str(ctx.exception))


class SqrtTest(unittest.TestCase):
    def test_sqrt_perfect_square(self):
        result = sqrt(9)
        self.assertEqual(result, 3.0)
        self.assertIsInstance(result, float)

    def test_sqrt_non_square(self):
        self.assertEqual(sqrt(2), 1.4142135623730951)

    def test_sqrt_float(self):
        self.assertEqual(sqrt(0.25), 0.5)

    def test_sqrt_zero(self):
        result = sqrt(0)
        self.assertEqual(result, 0.0)
        self.assertIsInstance(result, float)

    def test_sqrt_negative_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            sqrt(-4)
        self.assertIn("'a'", str(ctx.exception))

    def test_sqrt_rejects_string(self):
        with self.assertRaises(TypeError) as ctx:
            sqrt("9")
        self.assertIn("'a'", str(ctx.exception))
        self.assertIn("str", str(ctx.exception))

    def test_sqrt_accepts_bool_as_int(self):
        self.assertEqual(sqrt(True), 1.0)
        self.assertEqual(sqrt(False), 0.0)

    def test_sqrt_rejects_none(self):
        with self.assertRaises(TypeError) as ctx:
            sqrt(None)
        self.assertIn("'a'", str(ctx.exception))
        self.assertIn("NoneType", str(ctx.exception))


class CubeOfTest(unittest.TestCase):
    def test_cube_of_positive_int(self):
        self.assertEqual(cube_of(3), 27)

    def test_cube_of_negative_keeps_sign(self):
        self.assertEqual(cube_of(-2), -8)

    def test_cube_of_zero(self):
        self.assertEqual(cube_of(0), 0)

    def test_cube_of_float(self):
        self.assertEqual(cube_of(1.5), 3.375)

    def test_cube_of_rejects_string(self):
        with self.assertRaises(TypeError) as ctx:
            cube_of("3")
        self.assertIn("'a'", str(ctx.exception))
        self.assertIn("str", str(ctx.exception))

    def test_cube_of_rejects_none(self):
        with self.assertRaises(TypeError) as ctx:
            cube_of(None)
        self.assertIn("'a'", str(ctx.exception))
        self.assertIn("NoneType", str(ctx.exception))

    def test_cube_of_accepts_bool_as_int(self):
        self.assertEqual(cube_of(True), 1)
        self.assertEqual(cube_of(False), 0)


class FloorDivideTest(unittest.TestCase):
    def test_floor_divide_even(self):
        self.assertEqual(floor_divide(6, 3), 2)

    def test_floor_divide_rounds_down(self):
        self.assertEqual(floor_divide(7, 2), 3)

    def test_floor_divide_negative_first_rounds_toward_negative_infinity(self):
        self.assertEqual(floor_divide(-7, 2), -4)

    def test_floor_divide_negative_second(self):
        self.assertEqual(floor_divide(7, -2), -4)

    def test_floor_divide_both_negative(self):
        self.assertEqual(floor_divide(-7, -2), 3)

    def test_floor_divide_smaller_first(self):
        self.assertEqual(floor_divide(2, 5), 0)

    def test_floor_divide_float_gives_whole_float(self):
        result = floor_divide(7.5, 2)
        self.assertEqual(result, 3.0)
        self.assertIsInstance(result, float)

    def test_floor_divide_ints_give_int(self):
        self.assertIsInstance(floor_divide(7, 2), int)

    def test_floor_divide_zero_first(self):
        self.assertEqual(floor_divide(0, 5), 0)

    def test_floor_divide_consistent_with_modulo(self):
        for a, b in ((7, 2), (-7, 2), (7, -2), (-7, -2)):
            self.assertEqual(floor_divide(a, b) * b + modulo(a, b), a)

    def test_floor_divide_zero_second_raises(self):
        with self.assertRaises(ZeroDivisionError) as ctx:
            floor_divide(5, 0)
        self.assertIn("'b'", str(ctx.exception))

    def test_floor_divide_rejects_string_first(self):
        with self.assertRaises(TypeError) as ctx:
            floor_divide("a", 3)
        self.assertIn("'a'", str(ctx.exception))
        self.assertIn("str", str(ctx.exception))

    def test_floor_divide_rejects_none_second(self):
        with self.assertRaises(TypeError) as ctx:
            floor_divide(3, None)
        self.assertIn("'b'", str(ctx.exception))
        self.assertIn("NoneType", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
