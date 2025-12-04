import os

def clear_screen():
    """Clears the console screen."""
    os.system("cls" if os.name == "nt" else "clear")


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Error: Cannot divide by zero!"
    return a / b


def calculate():
    """Reads user input, validates, and performs operation."""
    try:
        num1 = float(input("Enter first number: "))
        operator = input("Enter operator (+, -, *, /): ")
        num2 = float(input("Enter second number: "))

        if operator == "+":
            result = add(num1, num2)
        elif operator == "-":
            result = subtract(num1, num2)
        elif operator == "*":
            result = multiply(num1, num2)
        elif operator == "/":
            result = divide(num1, num2)
        else:
            print("Invalid operator. Please try again.")
            return

        print(f"\nResult: {result}\n")

    except ValueError:
        print("Invalid input! Please enter a valid number.")


def menu():
    """Simple menu for repeated calculations."""
    while True:
        print("\n====== SIMPLE CALCULATOR ======")
        print("1. Perform Calculation")
        print("2. Clear Screen")
        print("3. Exit")

        choice = input("Choose an option (1/2/3): ")

        if choice == "1":
            calculate()
        elif choice == "2":
            clear_screen()
        elif choice == "3":
            print("Exiting... Thank you!")
            break
        else:
            print("Invalid choice. Please try again.")


# Run the program
menu()
