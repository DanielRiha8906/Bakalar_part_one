import math


class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def square(self, a):
        """Return a squared (a ** 2)."""
        return a ** 2

    def power(self, base, exp):
        """Return base raised to the power of exp."""
        return base ** exp

    def sqrt(self, a):
        """Return the square root of a.

        Raises ValueError if a is negative.
        """
        if a < 0:
            raise ValueError("Cannot take square root of a negative number")
        return math.sqrt(a)

    def nthroot(self, a, n):
        """Return the nth root of a (a ** (1/n)).

        Raises ValueError if n is zero, or if a is negative and n is even.
        """
        if n == 0:
            raise ValueError("Root degree cannot be zero")
        if a < 0 and n % 2 == 0:
            raise ValueError("Cannot take an even root of a negative number")
        if a < 0:
            return -((-a) ** (1 / n))
        return a ** (1 / n)

    def percentage(self, a, b):
        """Return a percent of b (b * a / 100)."""
        return b * a / 100

    def absolute(self, a):
        """Return the absolute value of a."""
        return abs(a)

    def factorial(self, n):
        """Return n! (n factorial).

        Raises ValueError if n is negative or not an integer.
        """
        if not isinstance(n, int):
            raise ValueError("Factorial is only defined for non-negative integers")
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        return math.factorial(n)


OPERATIONS = (
    "add", "subtract", "multiply", "divide",
    "square", "power", "sqrt", "nthroot",
    "percentage", "absolute", "factorial",
)


# Operations that take one numeric argument
_UNARY_OPERATIONS = ("square", "sqrt", "absolute", "factorial")
# Operations that take two numeric arguments
_BINARY_OPERATIONS = ("add", "subtract", "multiply", "divide", "power", "nthroot", "percentage")


def run_interactive() -> None:
    """Run the calculator in an interactive loop driven by user input.

    The user selects an operation and provides the required number of inputs.
    After each result the user is asked whether to continue or quit. The loop
    ends when the user types 'quit' or 'exit' at any prompt.
    """
    calc = Calculator()
    print("Simple Calculator")
    print(f"Available operations: {', '.join(OPERATIONS)}")
    print("Type 'quit' or 'exit' at any prompt to stop.\n")

    while True:
        operation = input("Operation: ").strip().lower()

        if operation in ("quit", "exit"):
            print("Goodbye!")
            break

        if operation not in OPERATIONS:
            print(f"Unknown operation '{operation}'. Choose from: {', '.join(OPERATIONS)}\n")
            continue

        try:
            a_raw = input("First number: ").strip()
            if a_raw.lower() in ("quit", "exit"):
                print("Goodbye!")
                break
            a = float(a_raw)

            if operation in _BINARY_OPERATIONS:
                b_raw = input("Second number: ").strip()
                if b_raw.lower() in ("quit", "exit"):
                    print("Goodbye!")
                    break
                b = float(b_raw)
        except ValueError:
            print("Invalid input — please enter numeric values.\n")
            continue

        try:
            if operation == "add":
                result = calc.add(a, b)
            elif operation == "subtract":
                result = calc.subtract(a, b)
            elif operation == "multiply":
                result = calc.multiply(a, b)
            elif operation == "divide":
                result = calc.divide(a, b)
            elif operation == "square":
                result = calc.square(a)
            elif operation == "power":
                result = calc.power(a, b)
            elif operation == "sqrt":
                result = calc.sqrt(a)
            elif operation == "nthroot":
                result = calc.nthroot(a, b)
            elif operation == "percentage":
                result = calc.percentage(a, b)
            elif operation == "absolute":
                result = calc.absolute(a)
            else:  # factorial
                result = calc.factorial(int(a))
            print(f"Result: {result}\n")
        except ValueError as exc:
            print(f"Error: {exc}\n")

        again = input("Another calculation? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("Goodbye!")
            break
        print()


if __name__ == "__main__":
    run_interactive()
