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
