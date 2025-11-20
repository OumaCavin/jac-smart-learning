""" JAC Learning Examples - Hello World and Basics """

with entry {
    print("Hello, World!");
    print("Welcome to JAC Programming!");
}

/*
 Try changing the text below and running this file:
   jac run examples/01_hello_world.jac
*/

# This is a comment - it won't be executed
# Variables store data for later use

with entry {
    # Basic variables
    name = "Alice"
    age = 25
    height = 5.6
    is_student = True
    
    print(f"Hello, {name}!")
    print(f"{name} is {age} years old")
    print(f"Height: {height} feet")
    print(f"Student: {is_student}")
    
    # Math operations
    years_until_30 = 30 - age
    print(f"Years until 30: {years_until_30}")
    
    # With type annotations (recommended)
    favorite_number: int = 42
    PI: float = 3.14159
    greeting: str = "Hello, JAC!"
    
    print(f"Favorite number: {favorite_number}")
    print(f"PI value: {PI}")
    print(greeting)
}