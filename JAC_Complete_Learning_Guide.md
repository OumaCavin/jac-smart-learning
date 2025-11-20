# The Complete JAC Programming Language Learning Guide
*From Beginner to Expert*

## Table of Contents
1. [Introduction to JAC](#introduction)
2. [Setting Up Your Development Environment](#setup)
3. [Key Learning Path Overview](#learning-path)
4. [Beginner Level (Foundation)](#beginner)
5. [Intermediate Level (Core Concepts)](#intermediate)
6. [Advanced Level (Object-Spatial Programming)](#advanced)
7. [Expert Level (AI Integration & Scale)](#expert)
8. [Real-World Projects](#projects)
9. [Resources & Next Steps](#resources)

---

## 1. Introduction to JAC {#introduction}

### What is JAC?

JAC (Java-like Architecture for Computation) is a revolutionary programming language that introduces **Object-Spatial Programming (OSP)** - a paradigm where computation moves to data, enabling scalable and distributed applications <citation>22</citation>.

### Why Learn JAC?

JAC offers a unique dual programming paradigm:
1. **Traditional Programming** - Like Python, JavaScript, Java
2. **Object-Spatial Programming (OSP)** - A revolutionary approach to handling interconnected data

Think of it this way:
- **Traditional Programming**: You call a restaurant and order food to be delivered to you
- **Object-Spatial Programming**: You send a robot to visit different restaurants and collect food

Both get you fed, but they work differently! <citation>21</citation>

### Key Advantages

- **Scale-Agnostic**: Code works for single user or millions without changes
- **Automatic Persistence**: No database management needed
- **Natural Relationship Modeling**: First-class citizens for graph-like data structures
- **Built-in Multi-User Isolation**: Automatic user separation
- **Python-like Syntax**: Familiar syntax for easy learning
- **Native AI Integration**: Seamless Large Language Model integration
- **Strong Typing**: Catches errors early, improves code maintainability

---

## 2. Setting Up Your Development Environment {#setup}

### Prerequisites

- **Python 3.12 or higher**
- **Basic command line knowledge**

### Installation Steps

#### Step 1: Install JAC
```bash
# Install using pip
python -m pip install -U jaclang
```

#### Step 2: Verify Installation
```bash
# Check JAC CLI version
jac --version

# Run a simple test
echo "with entry { print('Hello world'); }" > test.jac
jac run test.jac
rm test.jac
```

Expected output: `Hello world`

#### Step 3: Set Up Your IDE

**Visual Studio Code:**
1. Visit VS Code marketplace
2. Install [Jac Extension](https://marketplace.visualstudio.com/items?itemName=jaseci-labs.jaclang-extension)

**Cursor IDE:**
1. Go to [Jaseci release page](https://github.com/Jaseci-Labs/jaseci/releases/latest)
2. Download the latest `jaclang-extension-*.vsix` file
3. Open Cursor
4. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
5. Type `>install from vsix` and select the command
6. Select the downloaded VSIX file <citation>26</citation>

---

## 3. Key Learning Path Overview {#learning-path}

### **Phase 1: Foundation (Weeks 1-2)**
- Basic syntax and structure
- Variables and data types
- Control flow (if/else, loops)
- Functions
- Collections (lists, dictionaries, sets)

### **Phase 2: Object-Oriented Programming (Weeks 3-4)**
- Classes and objects
- Methods and attributes
- Type annotations
- Interface/implementation separation

### **Phase 3: Object-Spatial Programming (Weeks 5-7)**
- Nodes and edges
- Walkers and graph traversal
- Object-Spatial Programming paradigm
- Scale-agnostic programming

### **Phase 4: Advanced Features (Weeks 8-10)**
- AI integration with byLLM
- Concurrent programming
- Advanced graph operations
- Production deployment

### **Phase 5: Expert Level (Ongoing)**
- Complex system design
- Performance optimization
- Custom extensions
- Community contributions

---

## 4. Beginner Level (Foundation) {#beginner}

### 4.1 Your First JAC Program

Every JAC program needs a starting point. We use the special `with entry` block:

```jac
with entry {
    print("Hello, World!");
}
```

**What's happening?**
- `with entry` - This is where your program starts
- `print()` - Function that displays text on screen
- `"Hello, World!"` - Text (called a string)
- `;` - Every instruction ends with semicolon
- `{}` - Curly braces group instructions together <citation>21</citation>

### 4.2 Variables and Data Types

#### What is a Variable?
A variable is like a labeled box where you store information. You give it a name and can put different things in it.

```jac
with entry {
    name = "Alice";
    age = 25;
    height = 5.6;
    print(name);    # Shows: Alice
    print(age);     # Shows: 25
}
```

#### Data Types

**Text (Strings):**
```jac
with entry {
    greeting = "Hello";
    name = "Bob";
    message = "Welcome to Jac!";
    print(greeting);  # Shows: Hello
}
```
Strings go inside quotes: `"like this"` or `'like this'`

**Numbers (Integers):**
```jac
with entry {
    apples = 5;
    students = 30;
    year = 2024;
    print(apples);  # Shows: 5
}
```
Whole numbers with no decimal point.

**Numbers (Floats):**
```jac
with entry {
    temperature = 72.5;
    price = 19.99;
    pi = 3.14159;
    print(temperature);  # Shows: 72.5
}
```
Numbers with decimal points.

**True or False (Booleans):**
```jac
with entry {
    is_raining = True;
    is_sunny = False;
    print(is_raining);  # Shows: True
}
```
Only two values: `True` or `False` (notice the capital letters!) <citation>21</citation>

#### Type Annotations (Recommended!)

You can tell JAC what type of data a variable should hold:

```jac
with entry {
    name: str = "Alice";           # str means string (text)
    age: int = 25;                 # int means integer (whole number)
    height: float = 5.6;           # float means decimal number
    is_student: bool = True;       # bool means boolean (True/False)
    print(f"{name} is {age} years old");
}
```

**Pro tip:** The `f` before a string lets you insert variables using `{variable_name}` <citation>21</citation>

### 4.3 Mathematical Operations

You can calculate with numbers:

```jac
with entry {
    # Basic math
    sum = 5 + 3;           # Addition: 8
    difference = 10 - 4;   # Subtraction: 6
    product = 6 * 7;       # Multiplication: 42
    quotient = 20 / 4;     # Division: 5.0
    
    print(sum);      # Shows: 8
    print(product);  # Shows: 42
    
    # More operations
    remainder = 17 % 5;    # Modulo (remainder): 2
    power = 2 ** 3;        # Exponent: 8 (2³)
    
    # Combined operations
    total = (5 + 3) * 2;   # Use parentheses like in math: 16
    print(total);
}
```

**Common shortcuts:**
- `x += 5` means `x = x + 5` (add 5)
- `x -= 3` means `x = x - 3` (subtract 3)
- `x *= 2` means `x = x * 2` (multiply by 2)
- `x /= 4` means `x = x / 4` (divide by 4) <citation>21</citation>

### 4.4 Making Decisions: Control Flow

#### The If Statement

```jac
with entry {
    age = 18;
    if age >= 18 {
        print("You are an adult");
    }
}
```

**How it works:**
- `if age >= 18` - Check if age is greater than or equal to 18
- If the condition is `True`, run the code inside `{}`
- If the condition is `False`, skip the code inside `{}` <citation>21</citation>

#### Comparison Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `>` | Greater than | `x > 5` |
| `<` | Less than | `x < 10` |
| `>=` | Greater than or equal | `age >= 18` |
| `<=` | Less than or equal | `score <= 100` |
| `==` | Equal to | `name == "Alice"` |
| `!=` | Not equal to | `status != "done"` |

**Important:** Use `==` to compare (not `=`). Use `=` to assign values! <citation>21</citation>

#### If-Else

```jac
with entry {
    temperature = 72;
    if temperature > 75 {
        print("It's hot outside!");
    } else {
        print("It's nice outside!");
    }
}
```

#### If-Elif-Else (Multiple Conditions)

```jac
with entry {
    score = 85;
    if score >= 90 {
        print("Grade: A");
    } elif score >= 80 {
        print("Grade: B");
    } elif score >= 70 {
        print("Grade: C");
    } elif score >= 60 {
        print("Grade: D");
    } else {
        print("Grade: F");
    }
}
```

**How it works:**
1. Check first `if` - if `True`, run its code and skip the rest
2. If first is `False`, check first `elif`
3. Keep checking until one is `True`
4. If none are `True`, run `else` block <citation>21</citation>

#### Combining Conditions

```jac
with entry {
    age = 25;
    has_license = True;
    
    # AND - both must be true
    if age >= 16 and has_license {
        print("You can drive!");
    }
    
    # OR - at least one must be true
    if age < 18 or age > 65 {
        print("Discounted ticket price!");
    }
    
    # NOT - reverse the condition
    if not has_license {
        print("You need a license!");
    }
}
```

### 4.5 Repeating Actions: Loops

#### The While Loop

Repeat code while a condition is `True`:

```jac
with entry {
    count = 1;
    while count <= 5 {
        print(f"Count is {count}");
        count += 1;  # IMPORTANT: Change the variable or loop forever!
    }
    print("Done!");
}
```

**Warning:** Make sure your condition eventually becomes `False`, or your loop will run forever! <citation>21</citation>

#### The For Loop (Counting)

When you know exactly how many times to repeat:

```jac
with entry {
    # Count from 0 to 4
    for i = 0 to i < 5 by i += 1 {
        print(f"Number: {i}");
    }
}
```

**Breaking it down:**
- `i = 0` - Start at 0
- `to i < 5` - Continue while i is less than 5
- `by i += 1` - Add 1 to i each time <citation>21</citation>

#### The For-In Loop (Iterating)

Loop through items in a collection:

```jac
with entry {
    # We'll learn about lists soon!
    fruits = ["apple", "banana", "cherry"];
    for fruit in fruits {
        print(f"I like {fruit}");
    }
}
```

#### Breaking and Skipping

```jac
with entry {
    # Find first number divisible by 7
    for i = 1 to i <= 100 by i += 1 {
        if i % 7 == 0 {
            print(f"Found it: {i}");
            break;  # Exit the loop immediately
        }
    }
    
    # Print only odd numbers
    for i = 1 to i <= 10 by i += 1 {
        if i % 2 == 0 {
            continue;  # Skip even numbers
        }
        print(i);
    }
}
```

### 4.6 Organizing Code: Functions

Functions are reusable blocks of code that do specific tasks. Think of them as mini-programs within your program.

#### Creating Your First Function

```jac
# Define the function
def greet() {
    print("Hello, there!");
}

with entry {
    # Use (call) the function
    greet();
    greet();
    greet();
}
```

#### Functions with Parameters

Make functions more flexible by giving them inputs:

```jac
def greet(name: str) {
    print(f"Hello, {name}!");
}

with entry {
    greet("Alice");
    greet("Bob");
    greet("Charlie");
}
```

**Breaking it down:**
- `name: str` - This is a **parameter** (input)
- `: str` - Type annotation (optional but recommended)
- When you call `greet("Alice")`, `"Alice"` becomes the value of `name` <citation>21</citation>

#### Returning Values

Instead of just printing, functions can send values back:

```jac
def add(x: int, y: int) -> int {
    return x + y;
}

with entry {
    result = add(5, 3);
    print(result);  # Shows: 8
    
    # Use directly in calculations
    total = add(10, 20) + add(5, 5);
    print(total);  # Shows: 40
}
```

**Breaking it down:**
- `-> int` - This function returns an integer
- `return x + y;` - Send this value back to whoever called the function
- The returned value can be stored in a variable or used directly <citation>21</citation>

#### Default Parameters

Give parameters default values:

```jac
def greet(name: str = "friend", excited: bool = False) {
    if excited {
        print(f"HELLO, {name}!!!");
    } else {
        print(f"Hello, {name}.");
    }
}

with entry {
    greet();                    # Uses defaults
    greet("Alice");            # Uses name, default excited
    greet("Bob", True);        # Both specified
    greet(excited=True, name="Eve");  # Named parameters
}
```

#### Functions Example: Complete Calculator

Here's a simple calculator using functions:

```jac
def add(a: float, b: float) -> float {
    return a + b;
}

def subtract(a: float, b: float) -> float {
    return a - b;
}

def multiply(a: float, b: float) -> float {
    return a * b;
}

def divide(a: float, b: float) -> float {
    return a / b;
}

with entry {
    print("=== Simple Calculator ===");
    num1: float = 10.0;
    num2: float = 3.0;
    
    print(f"{num1} + {num2} = {add(num1, num2)}");
    print(f"{num1} - {num2} = {subtract(num1, num2)}");
    print(f"{num1} * {num2} = {multiply(num1, num2)}");
    print(f"{num1} / {num2} = {divide(num1, num2)}");
}
```

---

## 5. Intermediate Level (Core Concepts) {#intermediate}

### 5.1 Collections and Data Structures

JAC supports lists, dictionaries, sets, and tuples, but enforces type annotations for all collections.

#### Lists

Ordered, mutable collections of items, declared with `list` type:

```jac
with entry {
    # Create an empty list for storing integer grades
    alice_grades: list[int] = [];
    
    # Append grades to the list
    alice_grades.append(88);    # [88]
    alice_grades.append(92);    # [88, 92]
    alice_grades.append(85);    # [88, 92, 85]
    
    # Access grades by index
    first_grade: int = alice_grades[0];  # 88
    print(f"Alice's first grade: {first_grade}");
    
    # print the entire list of grades
    print(f"Alice's grades: {alice_grades}");
}
```

#### Dictionaries

Store data as key-value pairs, declared with `dict` type:

```jac
with entry {
    # Class gradebook
    math_grades: dict[str, int] = {
        "Alice": 92,
        "Bob": 85,
        "Charlie": 78
    };
    
    # Access grades by student name
    print(f"Alice's Math grade: {math_grades['Alice']}");
    print(f"Bob's Math grade: {math_grades['Bob']}");
    print(f"Charlie's Math grade: {math_grades['Charlie']}");
}
```

#### Sets

Unordered collections that do not allow duplicate items:

```jac
with entry {
    # Track unique courses
    alice_courses: set[str] = {"Math", "Science", "English"};
    bob_courses: set[str] = {"Math", "History", "Art"};
    
    # Find common courses
    common_courses = alice_courses.intersection(bob_courses);
    print(f"Common courses: {common_courses}");
    
    # All unique courses
    all_courses = alice_courses.union(bob_courses);
    print(f"All courses: {all_courses}");
}
```

### 5.2 Collection Comprehensions

JAC supports list and dictionary comprehensions, similar to Python:

#### Passing Grades Example

```jac
with entry {
    # Raw test scores
    test_scores: list[int] = [78, 85, 92, 69, 88, 95, 72];
    
    # Get passing grades (70 and above)
    passing_scores: list[int] = [score for score in test_scores if score >= 70];
    print(f"Passing scores: {passing_scores}");
}
```

#### Curved Scores Example

```jac
with entry {
    # Raw test scores
    test_scores: list[int] = [78, 85, 92, 69, 88, 95, 72];
    
    # Create a new list where each score is 5 points higher
    curved_scores: list[int] = [score + 5 for score in test_scores];
    print(f"Curved scores: {curved_scores}");
}
```

**Syntax:** `[expression for item in iterable if condition]` <citation>23</citation>

### 5.3 Object-Oriented Programming

JAC supports OOP concepts alongside its Object Spatial Language. Objects combine data and behavior.

#### Defining an Object

```jac
obj Student {
    has name: str;
    has age: int;
    has gpa: float;
    
    # Notice the 'self' parameter, which refers to the object itself.
    def get_info() -> str {
        return f"Name: {self.name}, Age: {self.age}, GPA: {self.gpa}";
    }
}

with entry {
    student: Student = Student("Alice", 20, 3.8);  # Create a new Student object
    print(student.get_info());
}
```

**Key concepts:**
- `obj` keyword defines a blueprint
- `has` defines attributes (data)
- `def` defines methods (behavior)
- JAC simplifies object initialization <citation>23</citation>

#### Enhanced Calculator with OOP

```jac
obj Calculator {
    has history: list[str] = [];
    
    def add(a: float, b: float) -> float {
        result: float = a + b;
        self.history.append(f"{a} + {b} = {result}");
        return result;
    }
    
    def subtract(a: float, b: float) -> float {
        result: float = a - b;
        self.history.append(f"{a} - {b} = {result}");
        return result;
    }
    
    def get_history() -> list[str] {
        return self.history;
    }
    
    def clear_history() {
        self.history = [];
    }
}

with entry {
    # Create an instance of our Calculator object
    calc = Calculator();
    
    # Perform calculations
    result1: float = calc.add(5.0, 3.0);
    result2: float = calc.subtract(10.0, 4.0);
    print(f"Results: {result1}, {result2}");
    
    # Show history
    print("\nCalculation History:");
    for entry in calc.get_history() {
        print(f" {entry}");
    }
}
```

### 5.4 Advanced Control Flow

#### Pattern Matching

Provides a cleaner alternative to long `if-elif-else` chains:

```jac
def process_grade_input(input: any) -> str {
    # The 'match' statement checks the input against several possible patterns
    match input {
        case int() if 90 <= input <= 100:
            return f"Excellent work! Score: {input}";
        case int() if 80 <= input < 90:
            return f"Good job! Score: {input}";
        case int() if 70 <= input < 80:
            return f"Satisfactory. Score: {input}";
        case int() if 0 <= input < 70:
            return f"Needs improvement. Score: {input}";
        case str() if input in ["A", "B", "C", "D", "F"]:
            return f"Letter grade received: {input}";
        case list() if len(input) > 0:
            avg = sum(input) / len(input);
            return f"Average of {len(input)} grades: {avg}";
        # The 'catch-all' case: If no other pattern matched
        case _:
            return "Invalid grade input";
    }
}

with entry {
    print(process_grade_input(95));        # Number grade
    print(process_grade_input("A"));       # Letter grade
    print(process_grade_input([88, 92, 85]));  # List of grades
}
```

#### Exception Handling

Manages unexpected errors to prevent program crashes:

```jac
def safe_calculate_gpa(grades: list[int]) -> float {
    try {
        if len(grades) == 0 {
            # If the list of grades is empty, we create our own error
            raise ValueError("No grades provided");
        }
        total = sum(grades);
        return total / len(grades);
    } except ValueError as e {
        # If a ValueError occurs, this block will run
        print(f"Error: {e}");
        return 0.0;
    }
}

def validate_grade(grade: int) -> None {
    if grade < 0 or grade > 100 {
        raise ValueError(f"Grade {grade} is out of valid range (0-100)");
    }
}

with entry {
    # Test 1: A valid calculation
    valid_grades: list[int] = [85, 90, 78];
    gpa: float = safe_calculate_gpa(valid_grades);
    print(f"The calculated GPA is: {gpa}");
    
    # Test 2: Handling a custom validation error
    try {
        validate_grade(150);
    } except ValueError as e {
        print(f"A validation error occurred: {e}");
    }
}
```

### 5.5 Interface and Implementation Separation

JAC encourages organizing code by separating interface (`.jac`) from implementation (`.impl.jac`):

#### Project Structure
```
my_project/
├── main.jac                 # Main program
├── models/
│   ├── user.jac            # User interface
│   ├── user.impl.jac       # User implementation
│   └── user.test.jac       # User tests
└── utils/
    ├── helpers.jac         # Helper functions
    └── constants.jac       # Application constants
```

#### Interface Declaration (user.jac)
```jac
obj User {
    # It has these attributes
    has name: str;
    has email: str;
    
    # And it must have these methods
    # We don't write the code for them here
    def validate() -> bool;
    def get_display_name() -> str;
}
```

#### Implementation (user.impl.jac)
```jac
# The implementation for the validate() method
impl User.validate {
    # It checks if the email contains an '@' and the name is not empty
    return "@" in self.email and len(self.name) > 0;
}

# The implementation for the get_display_name() method
impl User.get_display_name {
    return f"{self.name} <{self.email}>";
}
```

JAC automatically links these files. The `.jac` file defines an object's blueprint, while the `.impl.jac` file provides the actual code for the methods <citation>23</citation>

### 5.6 Complete Example: Grade Book System

Here's a comprehensive example integrating functions, collections, and control flow:

```jac
obj GradeBook {
    has students: dict[str, list[int]] = {};
    
    def add_student(name: str) -> None;
    def add_grade(student: str, grade: int) -> None;
    def get_average(student: str) -> float;
    def get_all_averages() -> dict[str, float];
}

impl GradeBook.add_student(name: str) -> None {
    if name not in self.students {
        self.students[name] = [];
        print(f"Added student: {name}");
    } else {
        print(f"Student {name} already exists");
    }
}

impl GradeBook.add_grade(student: str, grade: int) -> None {
    if grade < 0 or grade > 100 {
        print(f"Invalid grade: {grade}");
        return;
    }
    if student in self.students {
        self.students[student].append(grade);
        print(f"Added grade {grade} for {student}");
    } else {
        print(f"Student {student} not found");
    }
}

impl GradeBook.get_average(student: str) -> float {
    if student not in self.students or len(self.students[student]) == 0 {
        return 0.0;
    }
    grades = self.students[student];
    return sum(grades) / len(grades);
}

impl GradeBook.get_all_averages() -> dict[str, float] {
    averages: dict[str, float] = {};
    for (student, grades) in self.students.items() {
        if len(grades) > 0 {
            averages[student] = sum(grades) / len(grades);
        }
    }
    return averages;
}

with entry {
    # Create gradebook
    gradebook = GradeBook();
    
    # Add students
    gradebook.add_student("Alice");
    gradebook.add_student("Bob");
    
    # Add grades
    gradebook.add_grade("Alice", 88);
    gradebook.add_grade("Alice", 92);
    gradebook.add_grade("Bob", 85);
    gradebook.add_grade("Bob", 79);
    
    # Get results
    all_averages = gradebook.get_all_averages();
    for (student, avg) in all_averages.items() {
        letter = "A" if avg >= 90 else "B" if avg >= 80 else "C" if avg >= 70 else "F";
        print(f"{student}: {avg} ({letter})");
    }
}
```

---

## 6. Advanced Level (Object-Spatial Programming) {#advanced}

### 6.1 What is Object-Spatial Programming (OSP)?

Object-Spatial Programming is a paradigm where computation moves to data, enabling scalable and distributed applications. It's built on three fundamental concepts:

- **Nodes**: Stateful entities holding data
- **Edges**: Typed relationships between nodes  
- **Walkers**: Mobile computation that traverses the graph <citation>23</citation>

Think of it this way:
- **Traditional Programming**: You call a restaurant and order food to be delivered to you
- **Object-Spatial Programming**: You send a robot to visit different restaurants and collect food

### 6.2 Traditional vs Object-Spatial Approach

#### Traditional Approach (Python Example)

```python
class Person:
    def __init__(self, name):
        self.name = name
        self.friends = []

    def add_friend(self, friend):
        self.friends.append(friend)
        friend.friends.append(self)

# Create people and relationships
alice = Person("Alice")
bob = Person("Bob")
charlie = Person("Charlie")

# Establish relationships
alice.add_friend(bob) # bob.add_friend(alice) is redundant but necessary
bob.add_friend(charlie) # charlie.add_friend(bob) is redundant but necessary
```

#### Object-Spatial Approach (JAC Example)

```jac
node Person {
    has name: str;
}

edge FriendsWith;

with entry {
    # Create people
    alice = root ++> Person(name="Alice");
    bob = root ++> Person(name="Bob");
    charlie = root ++> Person(name="Charlie");
    
    # Create relationships naturally
    alice <+:FriendsWith:+> bob;
    bob <+:FriendsWith:+> charlie;
}
```

The syntax `alice <+:FriendsWith:+> bob;` creates a typed, two-way `FriendsWith` relationship <citation>23</citation>

### 6.3 Nodes: Data with Location

Nodes are objects with a location in a graph structure:

```jac
node User {
    has username: str;
    has email: str;
    has created_at: str;
}

node Post {
    has title: str;
    has content: str;
    has likes: int = 0;
}

with entry {
    # This is where your program starts
    # We will create the nodes in the graph here
    user = root ++> User(username="alice", email="alice@example.com", created_at="2024-01-01");
    post = user ++> Post(title="Hello Jac!", content="My first post in Jac");
    print(f"User {user[0].username} created post: {post[0].title}");
}
```

### 6.4 Edges: First-Class Relationships

Edges create typed connections between nodes; they can also have properties:

```jac
node Person {
    has name: str;
    has age: int;
}

edge FamilyRelation {
    # Edges can also have properties
    has relationship_type: str;
}

with entry {
    # First, let's create our family members as nodes
    parent = root ++> Person(name="John", age=45);
    child1 = root ++> Person(name="Alice", age=20);
    child2 = root ++> Person(name="Bob", age=18);
    
    # Now, let's create the relationships between them
    parent +>:FamilyRelation(relationship_type="parent"):+> child1;
    parent +>:FamilyRelation(relationship_type="parent"):+> child2;
    child1 +>:FamilyRelation(relationship_type="sibling"):+> child2;
    
    # You can now ask questions about these relationships
    children = [parent[0] ->:FamilyRelation:relationship_type=="parent":-> (`?Person)];
    print(f"{parent[0].name} has {len(children)} children:");
    for child in children {
        print(f" - {child.name} (age {child.age})");
    }
}
```

### 6.5 Walkers: Mobile Computation

Walkers are programs that traverse graphs of nodes and edges to perform tasks:

```jac
node Person {
    has name: str;
    has visited: bool = False;  # To keep track of who we've greeted
}

edge FriendsWith;

# This walker will greet every person it meets
walker GreetFriends {
    can greet_with Person entry {
        if not here.visited {
            here.visited = True;
            print(f"Hello, {here.name}!");
            # Now, tell the walker to go to all connected friends
            visit [->:FriendsWith:->];
        }
    }
}

with entry {
    # Create friend network
    alice = root ++> Person(name="Alice");
    bob = root ++> Person(name="Bob");
    charlie = root ++> Person(name="Charlie");
    
    # Connect friends
    alice +>:FriendsWith:+> bob +>:FriendsWith:+> charlie;
    alice +>:FriendsWith:+> charlie;  # Alice also friends with Charlie
    
    # Start the walker on the 'alice' node to greet everyone
    alice[0] spawn GreetFriends();
}
```

The `visit` statement directs the walker to travel across specified edges <citation>23</citation>

### 6.6 Complete Friend Network Example

Here's a comprehensive example demonstrating nodes, edges, and walkers working together:

```jac
node Person {
    has name: str;
    has age: int;
    has interests: list[str] = [];
}

edge FriendsWith {
    has since: str;
    has closeness: int;  # 1-10 scale
}

walker FindCommonInterests {
    # The walker needs to know who we're comparing against
    has target_person: Person;
    # It will store the results of its search here
    has common_interests: list[str] = [];
    
    # This ability runs automatically whenever the walker lands on a Person node
    can find_common with Person entry {
        # We don't want to compare the person with themselves
        if here == self.target_person {
            return;  # Skip self
        }
        
        # Find any interests this person shares with our target_person
        shared = [];
        for interest in here.interests {
            if interest in self.target_person.interests {
                shared.append(interest);
            }
        }
        
        # If we found any, print them and add them to our list
        if shared {
            self.common_interests.extend(shared);
            print(f"{here.name} and {self.target_person.name} both like: {', '.join(shared)}");
        }
    }
}

with entry {
    # Create friend network
    alice = root ++> Person(name="Alice", age=25, interests=["coding", "music", "hiking"]);
    bob = root ++> Person(name="Bob", age=27, interests=["music", "sports", "cooking"]);
    charlie = root ++> Person(name="Charlie", age=24, interests=["coding", "gaming", "music"]);
    
    # Create friendships with metadata
    alice +>:FriendsWith(since="2020-01-15", closeness=8):+> bob;
    alice +>:FriendsWith(since="2021-06-10", closeness=9):+> charlie;
    bob +>:FriendsWith(since="2020-12-03", closeness=7):+> charlie;
    
    print("=== Friend Network Analysis ===");
    
    # 1. Find all nodes connected to Alice by a FriendsWith edge
    alice_friends = [alice[0] ->:FriendsWith:-> (`?Person)];
    print(f"Alice's friends: {[f.name for f in alice_friends]}");
    
    # 2. Create an instance of our walker, telling it to compare against Alice
    finder = FindCommonInterests(target_person=alice[0]);
    
    # 3. Send the walker to visit each of Alice's friends
    for friend in alice_friends {
        friend spawn finder;
    }
    
    # Find close friendships (closeness >= 8)
    close_friendships = [root --> ->:FriendsWith:closeness>=8:->];
    print(f"Close friendships ({len(close_friendships)} found):");
}
```

### 6.7 Scale-Agnostic Programming

JAC allows code to work for a single user or millions, on a single machine or distributed system, without changes:

```jac
node UserProfile {
    has username: str;
    has bio: str = "";
}

walker GetProfile {
    can get_user_info with entry {
        # 'root' automatically points to the current user's graph
        profiles = [root --> (`?UserProfile)];
        if profiles {
            profile = profiles[0];
            print(f"Profile: {profile.username}");
            print(f"Bio: {profile.bio}");
        } else {
            print("No profile found");
        }
    }
}

walker CreateProfile {
    has username: str;
    has bio: str;
    
    can create with entry {
        # It looks for the profile connected to the current user's root
        profile = root ++> UserProfile(username=self.username, bio=self.bio);
        print(f"Created profile for {profile[0].username}");
    }
}

with entry {
    # This code works for any user automatically
    CreateProfile(username="alice", bio="Jac developer") spawn root;
    GetProfile() spawn root;
}
```

### 6.8 Automatic Persistence

JAC automatically saves data connected to the graph's root node, eliminating the need for manual database management:

```jac
node Counter {
    has count: int = 0;
    def increment() -> None;
}

impl Counter.increment {
    self.count += 1;
    print(f"Counter is now: {self.count}");
}

with entry {
    # Get or create counter
    counters = [root --> (`?Counter)];
    if not counters {
        counter = root ++> Counter();
        print("Created new counter");
    }
    # Increment and save automatically
    counter[0].increment();
}
```

To test persistence, save as "counter.jac" and run `jac serve counter.jac` <citation>23</citation>

### 6.9 Multi-User Isolation

JAC automatically provides each user with an isolated graph when running on a server. The `root` node always refers to the current user's graph.

---

## 7. Expert Level (AI Integration & Scale) {#expert}

### 7.1 AI Integration with byLLM

JAC provides native integration with Large Language Models through the `byLLM` feature.

#### Setting Up AI Integration

```jac
import random;
import from byllm.llm {Model};

# Global LLM to be used by byLLM annotated functions
glob llm = Model(model_name="gpt-4o", verbose=False);
# glob llm = Model(model_name="gemini/gemini-2.0-flash", verbose=False);

/** Provide a fun hint if guess is incorrect */
def give_hint(guess: int, correct_number: int) -> str byllm();
```

The `byLLM()` annotation indicates that the implementation of this function will be provided by the configured LLM based on its signature and context <citation>24</citation>

### 7.2 Complete AI-Enhanced Number Guessing Game

Here's the final version from the "JAC in a Flash" tutorial:

```jac
"""A Number Guessing Game"""
import random;
import from byllm.llm {Model};

# Glob llm to be used by byLLM annotated functions
glob llm = Model(model_name="gpt-4o", verbose=False);

"""Provide a fun hint if guess is incorrect"""
def give_hint(guess: int, correct_number: int) -> str byllm();

walker GuessGame {
    has guess: int;
    can start with `root entry;
    can process_guess with turn entry;
}

node turn {
    has correct_number: int = random.randint(1, 10);
}

# Will run when in CLI mode (not in cloud)
with entry: __main__ {
    root spawn GuessGame(3);
    root spawn GuessGame(4);
    root spawn GuessGame(5);
    root spawn GuessGame(6);
}
```

And the implementation:

```jac
impl GuessGame.start {
    if not [root --> (?turn)] {
        next = root ++> turn(random.randint(1, 10));
    } else {
        next = [root --> (?turn)];
    }
    visit next;
}

impl GuessGame.process_guess {
    if [-->] {
        visit [-->];
    } else {
        if self.guess == here.correct_number {
            print("Congratulations! You guessed correctly.");
            disengage;
        } elif self.guess < here.correct_number {
            print(give_hint(self.guess, here.correct_number));  # Use LLM generated hint
            here ++> turn(here.correct_number);
        } else {
            print(give_hint(self.guess, here.correct_number));  # Use LLM generated hint
            here ++> turn(here.correct_number);
        }
    }
}
```

### 7.3 Advanced Expressions

#### Ternary Conditional Expressions

Provide inline conditional value selection:

```jac
# Basic ternary
x = 1 if 5 / 2 == 1 else 2;  # x becomes 2

# More examples
status = "adult" if 20 >= 18 else "minor";  # status becomes "adult"
grade = "A" if 85 >= 90 else ("B" if 85 >= 80 else "C");  # grade becomes "B"

# Evaluation flow:
# 1. Evaluate condition
# 2. If true, return value_if_true
# 3. If false, return value_if_false
```

**Best practices:**
- Keep conditions simple and readable
- Avoid deep nesting (max 2 levels)
- Use for value selection, not side effects
- Parenthesize nested ternaries for clarity <citation>12</citation>

#### Lambda Expressions

Create anonymous functions – callable objects without formal function definitions:

```jac
# Basic lambda
square = lambda x: int : x ** 2;  # square(5) returns 25

# Multiple parameters
add = lambda a: int, b: int : a + b;  # add(3, 4) returns 7

# With explicit return type
multiply = lambda x: int, y: int -> int : x * y;

# No parameters
get_five = lambda : 5;  # get_five() returns 5

# Complex example combining lambda and ternary
abs_val = lambda n: int : (n if n >= 0 else -n);  # abs_val(-10) returns 10
```

**Syntax:** `lambda params : return_type : expression` <citation>12</citation>

**Components:**
- **Keyword**: `lambda` - Defines anonymous function
- **Parameters**: `x: int, y: int` - Function inputs with types
- **Return type**: `-> int` - Optional explicit return type
- **Expression**: `x + y` - Single expression to evaluate

### 7.4 Advanced Graph Operations

#### Graph Queries

```jac
# Find all nodes connected to Alice by a FriendsWith edge
alice_friends = [alice[0] ->:FriendsWith:-> (`?Person)];

# Find close friendships (closeness >= 8)
close_friendships = [root --> ->:FriendsWith:closeness>=8:->];

# Get all children of a parent
children = [parent[0] ->:FamilyRelation:relationship_type=="parent":-> (`?Person)];
```

#### Concurrent Operations

JAC supports concurrent expressions with `flow` and `wait`:

```jac
# Run multiple walkers concurrently
flow {
    walker1 spawn node1;
    walker2 spawn node2;
    walker3 spawn node3;
}

# Wait for all concurrent operations to complete
wait {
    # Operations that need to wait for flow to complete
}
```

### 7.5 Advanced Language Features

#### Pipe Expressions

```jac
# Pipe-style function calls
result = data |> transform |> filter |> process;

# Reverse pipe
result = process <| filter <| transform <| data;
```

#### Atomic Chain Operations

```jac
# Chain operations on objects
result = data.attr.method(arg)[index].field;
```

#### Special References

JAC provides special references for advanced operations:

- `init` - Initialization reference
- `post_init` - Post-initialization reference  
- `root` - Root node reference
- `super` - Superclass reference
- `self` - Current object reference
- `here` - Current node reference
- `visitor` - Current walker reference <citation>11</citation>

### 7.6 Production Deployment

#### Running JAC Applications

```bash
# Run a JAC file
jac run myapp.jac

# Serve a JAC application (enables persistence and web interface)
jac serve myapp.jac

# Run tests
jac test myapp.jac
```

#### Environment Configuration

```jac
# Global configuration
glob app_config = {
    "database_url": "postgresql://localhost/myapp",
    "redis_url": "redis://localhost:6379",
    "api_key": "your-api-key-here"
};

# Environment-specific configuration
glob debug_mode: bool = True;
glob max_connections: int = 100;
```

---

## 8. Real-World Projects {#projects}

### 8.1 Todo Application

Here's a complete full-stack Todo application using JAC:

```jac
node TodoItem {
    has title: str;
    has description: str = "";
    has completed: bool = False;
    has created_at: str;
    has priority: int = 1;  # 1=Low, 2=Medium, 3=High
}

edge HasTodo {
    has assigned_at: str;
}

walker CreateTodo {
    has title: str;
    has description: str = "";
    has priority: int = 1;
    
    can create with `root entry {
        todo = root ++> TodoItem(
            title=self.title,
            description=self.description,
            created_at="2024-01-01",
            priority=self.priority
        );
        root +>:HasTodo(assigned_at="2024-01-01"):+> todo;
        print(f"Created todo: {todo[0].title}");
    }
}

walker ListTodos {
    can list with `root entry {
        todos = [root --> ->:HasTodo:-> (`?TodoItem)];
        print(f"Found {len(todos)} todos:");
        for todo in todos {
            status = "✓" if todo.completed else "○";
            priority_text = ["", "Low", "Medium", "High"][todo.priority];
            print(f"  {status} {todo.title} [{priority_text}]");
            if todo.description {
                print(f"     {todo.description}");
            }
        }
    }
}

with entry {
    # Create some todos
    CreateTodo(
        title="Learn JAC programming",
        description="Complete the JAC tutorial and build projects",
        priority=3
    ) spawn root;
    
    CreateTodo(
        title="Build a web app",
        description="Create a real-world application using JAC",
        priority=2
    ) spawn root;
    
    # List all todos
    ListTodos() spawn root;
}
```

### 8.2 Social Network Graph

```jac
node User {
    has username: str;
    has email: str;
    has bio: str = "";
    has join_date: str;
}

edge FriendsWith {
    has since: str;
    has closeness: int;  # 1-10 scale
}

edge Follows {
    has since: str;
}

walker RecommendFriends {
    has target_user: User;
    has recommendations: list[User] = [];
    
    can recommend with User entry {
        if here == self.target_user {
            return;  # Skip self
        }
        
        # Check mutual friends
        mutual_friends = [self.target_user --> ->:FriendsWith:-> (`?User) 
                         --> ->:FriendsWith:-> here];
        
        if len(mutual_friends) > 0 and here not in self.recommendations {
            self.recommendations.append(here);
            print(f"Recommend: {here.username} (mutual friends: {len(mutual_friends)})");
        }
        
        # Continue to next user
        visit [--> ->:Follows:->];
    }
}

with entry {
    # Create users
    alice = root ++> User(username="alice", email="alice@email.com", join_date="2024-01-01");
    bob = root ++> User(username="bob", email="bob@email.com", join_date="2024-01-02");
    charlie = root ++> User(username="charlie", email="charlie@email.com", join_date="2024-01-03");
    
    # Create relationships
    alice +>:FriendsWith(since="2024-01-15", closeness=8):+> bob;
    bob +>:FriendsWith(since="2024-01-20", closeness=7):+> charlie;
    
    alice +>:Follows(since="2024-01-16"):+> charlie;
    
    # Get friend recommendations for Alice
    print("Friend recommendations for Alice:");
    RecommendFriends(target_user=alice[0]) spawn alice[0];
}
```

### 8.3 Knowledge Graph System

```jac
node Concept {
    has name: str;
    has description: str;
    has category: str;
}

edge RelatesTo {
    has relationship_type: str;  # "isa", "partof", "similar", "opposite"
    has strength: float;  # 0.0 to 1.0
}

edge DependsOn {
    has prerequisite_level: int;  # 1=basic, 2=intermediate, 3=advanced
}

walker LearnPath {
    has target_concept: Concept;
    has learning_path: list[Concept] = [];
    
    can find_prerequisites with Concept entry {
        if here == self.target_concept {
            return;
        }
        
        # Find direct dependencies
        prerequisites = [here --> ->:DependsOn:-> (`?Concept)];
        
        for prereq in prerequisites {
            if prereq not in self.learning_path {
                self.learning_path.append(prereq);
                print(f"Prerequisite: {prereq.name} ({prereq.category})");
            }
        }
        
        # Continue exploring dependencies
        visit [--> ->:DependsOn:->];
    }
}

walker ConceptExplorer {
    has search_term: str;
    has matches: list[Concept] = [];
    
    can explore with Concept entry {
        if self.search_term.lower() in here.name.lower() {
            self.matches.append(here);
            print(f"Found: {here.name} - {here.description}");
        }
        
        # Explore related concepts
        visit [--> ->:RelatesTo:->];
    }
}

with entry {
    # Create knowledge concepts
    programming = root ++> Concept(
        name="Programming",
        description="The art of creating computer programs",
        category="Computer Science"
    );
    
    python = root ++> Concept(
        name="Python",
        description="A high-level programming language",
        category="Programming Languages"
    );
    
    jac = root ++> Concept(
        name="JAC",
        description="Object-Spatial Programming Language",
        category="Programming Languages"
    );
    
    # Create relationships
    python +>:RelatesTo(relationship_type="isa", strength=0.9):+> programming;
    jac +>:RelatesTo(relationship_type="isa", strength=0.8):+> programming;
    
    jac +>:DependsOn(prerequisite_level=1):+> python;
    
    # Explore concepts
    print("Exploring programming concepts:");
    ConceptExplorer(search_term="programming") spawn programming[0];
    
    print("\nLearning path for JAC:");
    LearnPath(target_concept=jac[0]) spawn jac[0];
}
```

---

## 9. Common Mistakes and Solutions {#mistakes}

### 9.1 Common Beginner Mistakes

| Issue | Solution |
|-------|----------|
| Missing semicolons | Add `;` at the end of statements |
| Missing type annotations | Add types to all variables: `x: int = 5;` |
| No entry block | Add `with entry { ... }` for executable scripts |
| Python-style indentation | Use `{ }` braces instead of indentation |
| Using `=` instead of `==` for comparison | Use `==` for comparison, `=` for assignment |

### 9.2 Example of Fixes

**This won't work - missing types and semicolons:**
```jac
def greet(name) {
    return f"Hello, {name}"
}

# Missing entry block
print(greet("World"))
```

**This works - proper types and syntax:**
```jac
def greet(name: str) -> str {
    return f"Hello, {name}";
}

with entry {
    print(greet("World"));
}
```

---

## 10. Resources & Next Steps {#resources}

### 10.1 Official Documentation

- **JAC Language Reference**: https://jac-lang.org/learn/jac_ref/
- **Getting Started Guide**: https://jac-lang.org/learn/getting_started/
- **JAC in 5 Minutes**: https://www.jac-lang.org/learn/jac_in_a_flash/
- **Beginner's Guide**: https://docs.jaseci.org/learn/beginners_guide_to_jac/

### 10.2 Community Resources

- **GitHub Repository**: https://github.com/Jaseci-Labs/jaclang
- **Jaseci Documentation**: https://docs.jaseci.org/
- **JAC Playground**: https://jac-lang.org/playground/
- **VS Code Extension**: https://marketplace.visualstudio.com/items?itemName=jaseci-labs.jaclang-extension

### 10.3 Learning Path Summary

1. **Week 1-2**: Master basic syntax, variables, and control flow
2. **Week 3-4**: Learn functions, collections, and OOP concepts
3. **Week 5-7**: Dive deep into Object-Spatial Programming
4. **Week 8-10**: Explore AI integration and advanced features
5. **Ongoing**: Build real projects and contribute to the community

### 10.4 Practice Projects Ideas

1. **Beginner**: Calculator, To-do List, Grade Book System
2. **Intermediate**: Blog Platform, Contact Manager, Simple Game
3. **Advanced**: Social Network Graph, Recommendation System, Knowledge Graph
4. **Expert**: AI-Powered Chatbot, Distributed Computing System, Full-Stack Web Application

### 10.5 Tips for Success

- **Start with traditional programming concepts** before diving into OSP
- **Practice with small, focused examples** before building complex systems
- **Use the JAC playground** to experiment without installation
- **Join the community** for support and collaboration
- **Build real projects** to solidify your understanding
- **Don't fear the graph** - OSP becomes intuitive with practice

### 10.6 Advanced Topics to Explore

- **Concurrent Programming**: Using `flow` and `wait` expressions
- **Custom Archetypes**: Creating your own node and edge types
- **Performance Optimization**: Profiling and optimizing JAC applications
- **Deployment Strategies**: Scaling JAC applications in production
- **Plugin Development**: Extending JAC with custom functionality
- **Integration Patterns**: Connecting JAC with external systems and APIs

---

## Conclusion

JAC represents a revolutionary approach to programming that combines familiar traditional programming concepts with the powerful Object-Spatial Programming paradigm. Whether you're building simple scripts or complex distributed systems, JAC provides the tools and abstractions needed for modern software development.

The language's unique strength lies in its ability to handle interconnected, graph-like data structures naturally while maintaining the familiar syntax that makes it accessible to programmers from various backgrounds. From automatic persistence to built-in AI integration, JAC is designed for the challenges of modern software development.

Start with the basics, practice consistently, and gradually work your way up to more complex projects. The JAC community is welcoming and supportive, and the language's design makes it an excellent choice for both learning programming concepts and building production-ready applications.

**Happy Coding in JAC!** 🚀

---

*This guide was compiled from the official JAC documentation and learning resources. For the most up-to-date information, always refer to the official documentation at https://jac-lang.org/*