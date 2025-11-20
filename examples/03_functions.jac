""" JAC Learning Examples - Functions """

# Define some useful functions
def greet(name: str) -> str {
    return f"Hello, {name}!";
}

def add_numbers(a: int, b: int) -> int {
    return a + b;
}

def calculate_area(length: float, width: float) -> float {
    return length * width;
}

def is_even(number: int) -> bool {
    return number % 2 == 0;
}

def max_of_three(a: int, b: int, c: int) -> int {
    if a >= b and a >= c {
        return a;
    } elif b >= a and b >= c {
        return b;
    } else {
        return c;
    }
}

def convert_temperature(temp: float, from_scale: str, to_scale: str) -> float {
    if from_scale == "C" and to_scale == "F" {
        return (temp * 9/5) + 32;
    } elif from_scale == "F" and to_scale == "C" {
        return (temp - 32) * 5/9;
    } else {
        return temp;  # Same scale or invalid conversion
    }
}

with entry {
    print("=== Function Examples ===");
    
    # Basic function calls
    print(greet("Alice"));
    print(greet("Bob"));
    
    result = add_numbers(15, 25);
    print(f"15 + 25 = {result}");
    
    area = calculate_area(5.0, 3.0);
    print(f"Area of 5x3 rectangle: {area}");
    
    # Testing functions
    number = 42;
    if is_even(number) {
        print(f"{number} is even");
    } else {
        print(f"{number} is odd");
    }
    
    maximum = max_of_three(10, 25, 18);
    print(f"Maximum of 10, 25, 18: {maximum}");
    
    # Temperature conversion
    celsius = 25;
    fahrenheit = convert_temperature(celsius, "C", "F");
    print(f"{celsius}°C = {fahrenheit:.1f}°F");
    
    fahrenheit_back = convert_temperature(fahrenheit, "F", "C");
    print(f"{fahrenheit:.1f}°F = {fahrenheit_back:.1f}°C");
}

# Function with default parameters
def create_greeting(name: str, greeting: str = "Hello", punctuation: str = "!") -> str {
    return f"{greeting}, {name}{punctuation}";
}

with entry {
    print("\n=== Default Parameters ===");
    
    print(create_greeting("World"));
    print(create_greeting("Alice", "Hi"));
    print(create_greeting("Bob", "Hey", "..."));
    print(create_greeting(name="Charlie", punctuation="?"));
}

# Lambda functions
with entry {
    print("\n=== Lambda Functions ===");
    
    # Lambda for squaring
    square = lambda x: int : x * x;
    print(f"Square of 5: {square(5)}");
    
    # Lambda for addition
    add = lambda a: int, b: int : a + b;
    print(f"3 + 7 = {add(3, 7)}");
    
    # Lambda with explicit return type
    multiply = lambda x: float, y: float -> float : x * y;
    print(f"2.5 * 4.0 = {multiply(2.5, 4.0)}");
    
    # Using lambda in a list comprehension
    numbers = [1, 2, 3, 4, 5];
    squared_numbers = [square(n) for n in numbers];
    print(f"Numbers: {numbers}");
    print(f"Squared: {squared_numbers}");
}

# Practice exercise: Build a calculator
with entry {
    print("\n=== Practice: Simple Calculator ===");
    
    def calculator(a: float, b: float, operation: str) -> float {
        match operation {
            case "add":
                return a + b;
            case "subtract":
                return a - b;
            case "multiply":
                return a * b;
            case "divide":
                if b == 0 {
                    print("Error: Cannot divide by zero!");
                    return 0;
                }
                return a / b;
            case _:
                print(f"Unknown operation: {operation}");
                return 0;
        }
    }
    
    # Test the calculator
    num1 = 10.0;
    num2 = 3.0;
    
    print(f"Calculator Test:");
    print(f"{num1} + {num2} = {calculator(num1, num2, "add")}");
    print(f"{num1} - {num2} = {calculator(num1, num2, "subtract")}");
    print(f"{num1} * {num2} = {calculator(num1, num2, "multiply")}");
    print(f"{num1} / {num2} = {calculator(num1, num2, "divide")}");
    print(f"{num1} ^ {num2} = {calculator(num1, num2, "power")}");
}