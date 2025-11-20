# JAC Language Quick Reference Guide

## Basic Syntax

### Entry Point
```jac
with entry {
    // Your code here
}
```

### Variables and Types
```jac
// Basic types
name: str = "Alice"
age: int = 25
height: float = 5.6
is_student: bool = True

// Collections
numbers: list[int] = [1, 2, 3, 4, 5]
grades: dict[str, int] = {"Alice": 95, "Bob": 87}
unique_items: set[str] = {"apple", "banana", "cherry"}

// Global variables
glob app_name: str = "My JAC App"
```

### Functions
```jac
// Basic function
def greet(name: str) -> str {
    return f"Hello, {name}!";
}

// With default parameters
def calculate_area(width: float, height: float = 1.0) -> float {
    return width * height;
}

// Lambda function
square = lambda x: int : x * x;
```

### Control Flow
```jac
// If-else
if condition {
    // code
} elif other_condition {
    // code
} else {
    // code
}

// Loops
for i = 0 to i < 10 by i += 1 {
    print(i);
}

while condition {
    // code
}

// For-in loop
for item in collection {
    print(item);
}
```

### Object-Oriented Programming
```jac
// Object definition
obj Student {
    has name: str;
    has age: int;
    has grades: list[float] = [];
    
    def get_average() -> float {
        if len(self.grades) == 0 {
            return 0.0;
        }
        return sum(self.grades) / len(self.grades);
    }
}

// Implementation separation
impl Student.get_average {
    if len(self.grades) == 0 {
        return 0.0;
    }
    return sum(self.grades) / len(self.grades);
}
```

## Object-Spatial Programming

### Nodes and Edges
```jac
// Node definition
node Person {
    has name: str;
    has age: int;
}

// Edge definition
edge FriendsWith {
    has since: str;
    has closeness: int;
}

// Creating nodes and relationships
with entry {
    alice = root ++> Person(name="Alice", age=25);
    bob = root ++> Person(name="Bob", age=27);
    
    alice +>:FriendsWith(since="2020-01-01", closeness=8):+> bob;
}
```

### Walkers
```jac
walker GreetPerson {
    can greet with Person entry {
        print(f"Hello, {here.name}!");
        visit [-->]; // Continue to connected nodes
    }
}

// Running a walker
alice[0] spawn GreetPerson();
```

### Graph Queries
```jac
// Find connected nodes
friends = [alice[0] ->:FriendsWith:-> (`?Person)];

// Find with conditions
close_friends = [root --> ->:FriendsWith:closeness>=8:->];
```

## Advanced Features

### Pattern Matching
```jac
def process_input(input: any) -> str {
    match input {
        case int() if input > 0:
            return "Positive integer";
        case str() if len(input) > 5:
            return "Long string";
        case list():
            return f"List with {len(input)} items";
        case _:
            return "Unknown type";
    }
}
```

### Exception Handling
```jac
try {
    risky_operation();
} except ValueError as e {
    print(f"Error: {e}");
} finally {
    cleanup();
}
```

### AI Integration
```jac
import from byllm.llm {Model};

glob llm = Model(model_name="gpt-4o", verbose=False);

def smart_response(prompt: str) -> str byllm();

result = smart_response("Tell me a joke about programming");
```

### Pipe Expressions
```jac
// Function composition
result = data |> transform |> filter |> process;

// Reverse pipe
result = process <| filter <| transform <| data;
```

## Common Operators

### Arithmetic
```jac
+   // Addition
-   // Subtraction  
*   // Multiplication
/   // Division
%   // Modulo
**  // Exponent
```

### Comparison
```jac
==  // Equal
!=  // Not equal
>   // Greater than
<   // Less than
>=  // Greater or equal
<=  // Less or equal
```

### Logical
```jac
and // Logical AND
or  // Logical OR
not // Logical NOT
```

### Assignment
```jac
=   // Assignment
+=  // Add and assign
-=  // Subtract and assign
*=  // Multiply and assign
/=  // Divide and assign
:=  // Walrus operator
```

## Special Keywords

### Object-Spatial
```jac
root      // Root node of the graph
here      // Current node
visitor   // Current walker
spawn     // Start a walker
visit     // Move walker to node
disengage // Stop walker
++>       // Create and connect node
+>:+:     // Create edge with properties
-->       // Navigate edge
```

### Code Organization
```jac
with entry     // Entry point for execution
with root entry    // Root-specific entry
can         // Method declaration in walkers/objects
impl        // Implementation block
glob        // Global variable
def         // Function definition
obj         // Object definition
node        // Node archetype
edge        // Edge archetype
walker      // Walker archetype
```

### Control Flow
```jac
if, elif, else    // Conditional statements
for, while        // Loops
try, except, finally  // Exception handling
match, case       // Pattern matching
break, continue   // Loop control
return, raise     // Function control
```

### Comments
```jac
# Single line comment

#*
Multi-line comment
*#
```

## Running JAC Programs

```bash
# Run a JAC file
jac run program.jac

# Serve a JAC application
jac serve application.jac

# Run tests
jac test application.jac

# Check version
jac --version
```

## File Extensions

- `.jac` - Main JAC source files
- `.impl.jac` - Implementation files
- `.test.jac` - Test files

## Type Annotations

```jac
# Built-in types
str, int, float, bool, list, dict, set, tuple, any

# Collection types
list[int]           // List of integers
dict[str, int]      // Dictionary with string keys and integer values
set[str]            // Set of strings

# Function types
def func() -> str               // Returns string
def func(x: int, y: int) -> int // Takes two integers, returns integer

# Multiple return types
def risky_operation() -> int | str {
    // Returns either int or str
}
```

## Useful Built-in Functions

```jac
len(collection)          // Get length
sum(numbers)            // Sum of numbers
print(value)            // Print to console
input(prompt)           // Get user input
range(start, end, step) // Generate sequence
abs(number)             // Absolute value
max(values)             // Maximum value
min(values)             // Minimum value
```

## Best Practices

1. **Always use type annotations** for variables and functions
2. **End statements with semicolons**
3. **Use meaningful variable and function names**
4. **Keep functions small and focused**
5. **Use interface/implementation separation** for larger projects
6. **Comment complex logic**
7. **Handle edge cases** in your functions
8. **Test your code** with various inputs
9. **Follow the principle of least surprise**
10. **Document public APIs** clearly