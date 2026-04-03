import math
import pytest
from unittest.mock import patch, call
from src.calculator import Calculator, run_interactive


class TestCalculatorAdd:
    def setup_method(self):
        self.calc = Calculator()

    # Standard expected behavior
    def test_add_two_positive_integers(self):
        assert self.calc.add(2, 3) == 5

    def test_add_two_negative_integers(self):
        assert self.calc.add(-4, -6) == -10

    def test_add_positive_and_negative(self):
        assert self.calc.add(10, -3) == 7

    def test_add_floats(self):
        assert self.calc.add(1.5, 2.5) == 4.0

    # Edge cases
    def test_add_zeros(self):
        assert self.calc.add(0, 0) == 0

    def test_add_zero_and_number(self):
        assert self.calc.add(0, 42) == 42

    def test_add_positive_infinity(self):
        assert self.calc.add(float("inf"), 1) == float("inf")

    def test_add_opposite_infinities_is_nan(self):
        result = self.calc.add(float("inf"), float("-inf"))
        assert math.isnan(result)

    # Numeric precision
    def test_add_floating_point_precision(self):
        # 0.1 + 0.2 is a well-known floating-point precision case
        result = self.calc.add(0.1, 0.2)
        assert math.isclose(result, 0.3)

    def test_add_large_integers(self):
        assert self.calc.add(10**100, 10**100) == 2 * 10**100

    def test_add_large_floats(self):
        result = self.calc.add(1e308, 1e308)
        assert math.isinf(result)

    # Invalid input
    def test_add_string_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.add("a", 1)

    def test_add_none_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.add(None, 1)

    def test_add_list_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.add([1, 2], 3)


class TestCalculatorSubtract:
    def setup_method(self):
        self.calc = Calculator()

    # Standard expected behavior
    def test_subtract_two_positive_integers(self):
        assert self.calc.subtract(10, 3) == 7

    def test_subtract_two_negative_integers(self):
        assert self.calc.subtract(-5, -3) == -2

    def test_subtract_positive_minus_larger_positive(self):
        assert self.calc.subtract(3, 10) == -7

    def test_subtract_floats(self):
        assert self.calc.subtract(5.5, 2.5) == 3.0

    # Edge cases
    def test_subtract_same_number_gives_zero(self):
        assert self.calc.subtract(7, 7) == 0

    def test_subtract_zero(self):
        assert self.calc.subtract(5, 0) == 5

    def test_subtract_from_zero(self):
        assert self.calc.subtract(0, 5) == -5

    def test_subtract_infinity_from_infinity_is_nan(self):
        result = self.calc.subtract(float("inf"), float("inf"))
        assert math.isnan(result)

    # Numeric precision
    def test_subtract_floating_point_precision(self):
        result = self.calc.subtract(0.3, 0.1)
        assert math.isclose(result, 0.2)

    def test_subtract_large_integers(self):
        assert self.calc.subtract(10**100, 10**99) == 9 * 10**99

    # Invalid input
    def test_subtract_string_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.subtract("a", 1)

    def test_subtract_none_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.subtract(None, 5)

    def test_subtract_list_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.subtract([1], 1)


class TestCalculatorMultiply:
    def setup_method(self):
        self.calc = Calculator()

    # Standard expected behavior
    def test_multiply_two_positive_integers(self):
        assert self.calc.multiply(3, 4) == 12

    def test_multiply_two_negative_integers(self):
        assert self.calc.multiply(-3, -4) == 12

    def test_multiply_positive_and_negative(self):
        assert self.calc.multiply(-3, 4) == -12

    def test_multiply_floats(self):
        assert self.calc.multiply(2.5, 4.0) == 10.0

    # Edge cases
    def test_multiply_by_zero(self):
        assert self.calc.multiply(999, 0) == 0

    def test_multiply_by_one(self):
        assert self.calc.multiply(42, 1) == 42

    def test_multiply_by_negative_one(self):
        assert self.calc.multiply(42, -1) == -42

    def test_multiply_infinity_by_positive(self):
        assert self.calc.multiply(float("inf"), 2) == float("inf")

    def test_multiply_infinity_by_zero_is_nan(self):
        result = self.calc.multiply(float("inf"), 0)
        assert math.isnan(result)

    # Numeric precision / large values
    def test_multiply_large_integers(self):
        assert self.calc.multiply(10**50, 10**50) == 10**100

    def test_multiply_large_floats_overflow_to_infinity(self):
        result = self.calc.multiply(1e200, 1e200)
        assert math.isinf(result)

    # Invalid input
    def test_multiply_two_strings_raises_type_error(self):
        # Multiplying str by str is not defined in Python
        with pytest.raises(TypeError):
            self.calc.multiply("a", "b")

    def test_multiply_none_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.multiply(None, 3)

    def test_multiply_string_by_float_raises_type_error(self):
        # str * float is not valid in Python
        with pytest.raises(TypeError):
            self.calc.multiply("a", 1.5)


class TestCalculatorDivide:
    def setup_method(self):
        self.calc = Calculator()

    # Standard expected behavior
    def test_divide_exact_result(self):
        assert self.calc.divide(10, 2) == 5.0

    def test_divide_non_exact_result(self):
        assert self.calc.divide(7, 2) == 3.5

    def test_divide_two_negatives(self):
        assert self.calc.divide(-6, -3) == 2.0

    def test_divide_positive_by_negative(self):
        assert self.calc.divide(9, -3) == -3.0

    # Edge cases
    def test_divide_zero_numerator(self):
        assert self.calc.divide(0, 5) == 0.0

    def test_divide_by_one(self):
        assert self.calc.divide(42, 1) == 42.0

    def test_divide_number_by_itself(self):
        assert self.calc.divide(7, 7) == 1.0

    def test_divide_float_operands(self):
        assert math.isclose(self.calc.divide(1.0, 3.0), 1 / 3)

    # Expected exception — divide by zero
    def test_divide_by_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)

    def test_divide_negative_by_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(-5, 0)

    def test_divide_zero_by_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(0, 0)

    # Numeric precision / large values
    def test_divide_large_numerator(self):
        # Result is a float; use isclose due to floating-point representation
        assert math.isclose(self.calc.divide(10**100, 10**50), 10**50)

    def test_divide_very_small_result(self):
        result = self.calc.divide(1, 10**10)
        assert math.isclose(result, 1e-10)

    def test_divide_large_float_by_small_float(self):
        result = self.calc.divide(1e308, 1e-10)
        assert math.isinf(result)

    # Invalid input (type errors)
    def test_divide_string_numerator_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.divide("a", 2)

    def test_divide_none_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.divide(None, 2)

    def test_divide_list_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.divide([10], 2)


class TestRunInteractive:
    """Tests for the interactive user-input loop."""

    def _run(self, inputs: list[str], capsys) -> str:
        """Helper: patch input() with *inputs* and return captured stdout."""
        with patch("builtins.input", side_effect=inputs):
            run_interactive()
        return capsys.readouterr().out

    # --- quit / exit paths ---

    def test_quit_at_operation_prompt(self, capsys):
        out = self._run(["quit"], capsys)
        assert "Goodbye!" in out

    def test_exit_at_operation_prompt(self, capsys):
        out = self._run(["exit"], capsys)
        assert "Goodbye!" in out

    # --- successful calculations ---

    def test_add_then_quit(self, capsys):
        out = self._run(["add", "3", "4", "no"], capsys)
        assert "Result: 7.0" in out
        assert "Goodbye!" in out

    def test_subtract_then_quit(self, capsys):
        out = self._run(["subtract", "10", "3", "no"], capsys)
        assert "Result: 7.0" in out

    def test_multiply_then_quit(self, capsys):
        out = self._run(["multiply", "6", "7", "no"], capsys)
        assert "Result: 42.0" in out

    def test_divide_then_quit(self, capsys):
        out = self._run(["divide", "10", "2", "no"], capsys)
        assert "Result: 5.0" in out

    # --- continue loop ---

    def test_two_calculations_then_quit(self, capsys):
        inputs = ["add", "1", "2", "yes", "multiply", "3", "4", "no"]
        out = self._run(inputs, capsys)
        assert "Result: 3.0" in out
        assert "Result: 12.0" in out
        assert "Goodbye!" in out

    def test_yes_shorthand_continues_loop(self, capsys):
        inputs = ["add", "1", "1", "y", "quit"]
        out = self._run(inputs, capsys)
        assert "Result: 2.0" in out
        assert "Goodbye!" in out

    # --- error handling ---

    def test_unknown_operation_shows_error_then_continues(self, capsys):
        out = self._run(["unknown_op", "quit"], capsys)
        assert "Unknown operation" in out
        assert "Goodbye!" in out

    def test_invalid_number_shows_error_then_continues(self, capsys):
        out = self._run(["add", "abc", "quit"], capsys)
        assert "Invalid input" in out
        assert "Goodbye!" in out

    def test_divide_by_zero_shows_error(self, capsys):
        out = self._run(["divide", "5", "0", "no"], capsys)
        assert "Error: Cannot divide by zero" in out
        assert "Goodbye!" in out

    # --- new unary operations ---

    def test_sqrt_then_quit(self, capsys):
        out = self._run(["sqrt", "9", "no"], capsys)
        assert "Result: 3.0" in out
        assert "Goodbye!" in out

    def test_square_then_quit(self, capsys):
        out = self._run(["square", "5", "no"], capsys)
        assert "Result: 25" in out
        assert "Goodbye!" in out

    def test_absolute_then_quit(self, capsys):
        out = self._run(["absolute", "-7", "no"], capsys)
        assert "Result: 7" in out
        assert "Goodbye!" in out

    def test_factorial_then_quit(self, capsys):
        out = self._run(["factorial", "5", "no"], capsys)
        assert "Result: 120" in out
        assert "Goodbye!" in out

    # --- new binary operations ---

    def test_power_then_quit(self, capsys):
        out = self._run(["power", "2", "10", "no"], capsys)
        assert "Result: 1024" in out
        assert "Goodbye!" in out

    def test_nthroot_then_quit(self, capsys):
        out = self._run(["nthroot", "8", "3", "no"], capsys)
        assert "Result: 2.0" in out
        assert "Goodbye!" in out

    def test_percentage_then_quit(self, capsys):
        out = self._run(["percentage", "50", "200", "no"], capsys)
        assert "Result: 100.0" in out
        assert "Goodbye!" in out

    # --- error paths for new operations ---

    def test_sqrt_negative_shows_error(self, capsys):
        out = self._run(["sqrt", "-4", "no"], capsys)
        assert "Error:" in out
        assert "Goodbye!" in out


class TestCalculatorSquare:
    def setup_method(self):
        self.calc = Calculator()

    # Standard expected behavior
    def test_square_positive_integer(self):
        assert self.calc.square(5) == 25

    def test_square_negative_integer(self):
        assert self.calc.square(-4) == 16

    def test_square_zero(self):
        assert self.calc.square(0) == 0

    def test_square_float(self):
        assert math.isclose(self.calc.square(2.5), 6.25)

    def test_square_one(self):
        assert self.calc.square(1) == 1

    # Invalid input
    def test_square_string_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.square("a")

    def test_square_none_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.square(None)


class TestCalculatorPower:
    def setup_method(self):
        self.calc = Calculator()

    # Standard expected behavior
    def test_power_positive_base_and_exp(self):
        assert self.calc.power(2, 10) == 1024

    def test_power_negative_base_even_exp(self):
        assert self.calc.power(-3, 2) == 9

    def test_power_negative_base_odd_exp(self):
        assert self.calc.power(-2, 3) == -8

    def test_power_float_base(self):
        assert math.isclose(self.calc.power(2.0, 0.5), math.sqrt(2))

    # Edge cases
    def test_power_exp_zero_gives_one(self):
        assert self.calc.power(999, 0) == 1

    def test_power_base_zero(self):
        assert self.calc.power(0, 5) == 0

    def test_power_base_one(self):
        assert self.calc.power(1, 1000) == 1

    def test_power_negative_exp(self):
        assert math.isclose(self.calc.power(2, -1), 0.5)

    # Invalid input
    def test_power_string_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.power("a", 2)

    def test_power_none_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.power(None, 2)


class TestCalculatorSqrt:
    def setup_method(self):
        self.calc = Calculator()

    # Standard expected behavior
    def test_sqrt_perfect_square(self):
        assert self.calc.sqrt(9) == 3.0

    def test_sqrt_non_perfect_square(self):
        assert math.isclose(self.calc.sqrt(2), math.sqrt(2))

    def test_sqrt_zero(self):
        assert self.calc.sqrt(0) == 0.0

    def test_sqrt_one(self):
        assert self.calc.sqrt(1) == 1.0

    def test_sqrt_large_number(self):
        assert math.isclose(self.calc.sqrt(1e10), 1e5)

    # Expected exception
    def test_sqrt_negative_raises_value_error(self):
        with pytest.raises(ValueError, match="negative"):
            self.calc.sqrt(-1)

    def test_sqrt_negative_float_raises_value_error(self):
        with pytest.raises(ValueError):
            self.calc.sqrt(-0.001)

    # Invalid input
    def test_sqrt_string_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.sqrt("9")

    def test_sqrt_none_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.sqrt(None)


class TestCalculatorNthroot:
    def setup_method(self):
        self.calc = Calculator()

    # Standard expected behavior
    def test_nthroot_cube_root(self):
        assert math.isclose(self.calc.nthroot(8, 3), 2.0)

    def test_nthroot_square_root(self):
        assert math.isclose(self.calc.nthroot(9, 2), 3.0)

    def test_nthroot_fourth_root(self):
        assert math.isclose(self.calc.nthroot(16, 4), 2.0)

    def test_nthroot_zero_radicand(self):
        assert self.calc.nthroot(0, 3) == 0.0

    # Edge cases
    def test_nthroot_negative_radicand_odd_root(self):
        assert math.isclose(self.calc.nthroot(-8, 3), -2.0)

    def test_nthroot_one_as_degree(self):
        assert self.calc.nthroot(42, 1) == 42.0

    # Expected exceptions
    def test_nthroot_degree_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="zero"):
            self.calc.nthroot(8, 0)

    def test_nthroot_negative_radicand_even_root_raises_value_error(self):
        with pytest.raises(ValueError, match="even root"):
            self.calc.nthroot(-4, 2)

    # Invalid input
    def test_nthroot_string_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.nthroot("a", 2)


class TestCalculatorPercentage:
    def setup_method(self):
        self.calc = Calculator()

    # Standard expected behavior
    def test_percentage_50_of_200(self):
        assert self.calc.percentage(50, 200) == 100.0

    def test_percentage_10_of_50(self):
        assert self.calc.percentage(10, 50) == 5.0

    def test_percentage_100_of_any(self):
        assert self.calc.percentage(100, 75) == 75.0

    def test_percentage_zero_percent(self):
        assert self.calc.percentage(0, 500) == 0.0

    # Edge cases
    def test_percentage_over_100(self):
        assert self.calc.percentage(150, 200) == 300.0

    def test_percentage_of_zero(self):
        assert self.calc.percentage(50, 0) == 0.0

    def test_percentage_float_percent(self):
        assert math.isclose(self.calc.percentage(33.3, 300), 99.9)

    # Invalid input
    def test_percentage_string_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.percentage("a", 100)

    def test_percentage_none_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.percentage(None, 100)


class TestCalculatorAbsolute:
    def setup_method(self):
        self.calc = Calculator()

    # Standard expected behavior
    def test_absolute_negative_integer(self):
        assert self.calc.absolute(-7) == 7

    def test_absolute_positive_integer(self):
        assert self.calc.absolute(7) == 7

    def test_absolute_zero(self):
        assert self.calc.absolute(0) == 0

    def test_absolute_negative_float(self):
        assert self.calc.absolute(-3.14) == 3.14

    def test_absolute_negative_infinity(self):
        assert self.calc.absolute(float("-inf")) == float("inf")

    # Invalid input
    def test_absolute_string_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.absolute("a")

    def test_absolute_none_raises_type_error(self):
        with pytest.raises(TypeError):
            self.calc.absolute(None)


class TestCalculatorFactorial:
    def setup_method(self):
        self.calc = Calculator()

    # Standard expected behavior
    def test_factorial_zero(self):
        assert self.calc.factorial(0) == 1

    def test_factorial_one(self):
        assert self.calc.factorial(1) == 1

    def test_factorial_five(self):
        assert self.calc.factorial(5) == 120

    def test_factorial_ten(self):
        assert self.calc.factorial(10) == 3628800

    def test_factorial_large(self):
        assert self.calc.factorial(20) == 2432902008176640000

    # Expected exceptions
    def test_factorial_negative_raises_value_error(self):
        with pytest.raises(ValueError, match="negative"):
            self.calc.factorial(-1)

    def test_factorial_float_raises_value_error(self):
        with pytest.raises(ValueError, match="integer"):
            self.calc.factorial(3.5)

    # Invalid input
    def test_factorial_string_raises_value_error(self):
        with pytest.raises(ValueError):
            self.calc.factorial("5")

    def test_factorial_none_raises_value_error(self):
        with pytest.raises(ValueError):
            self.calc.factorial(None)
