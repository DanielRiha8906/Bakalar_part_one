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


OPERATIONS = ("add", "subtract", "multiply", "divide")


def run_interactive() -> None:
    """Run the calculator in an interactive loop driven by user input.

    The user selects an operation and provides two numbers. After each
    result the user is asked whether to continue or quit. The loop ends
    when the user types 'quit' or 'exit' at any prompt.
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
            a = float(input("First number: ").strip())
            b = float(input("Second number: ").strip())
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
            else:
                result = calc.divide(a, b)
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
