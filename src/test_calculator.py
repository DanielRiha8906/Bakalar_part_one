import pytest
from src.calculator import Calculator


class TestCalculatorDivide:
    def setup_method(self):
        self.calc = Calculator()

    def test_divide_by_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)
