""" JAC Learning Examples - Loops and Collections """

with entry {
    print("=== Loop Examples ===");
    
    # While loop
    print("\n--- While Loop ---");
    count = 1;
    while count <= 5 {
        print(f"Count: {count}");
        count += 1;
    }
    
    # For-to-by loop
    print("\n--- For-to-by Loop ---");
    for i = 0 to i < 5 by i += 1 {
        print(f"i = {i}");
    }
    
    # For-to-by with different step
    print("\n--- Even Numbers (step 2) ---");
    for even = 0 to even <= 10 by even += 2 {
        print(f"Even: {even}");
    }
    
    # Countdown
    print("\n--- Countdown ---");
    for countdown = 10 to countdown >= 1 by countdown -= 1 {
        print(f"T-minus {countdown}");
    }
    print("Blast off!");
}

with entry {
    print("\n=== Collection Examples ===");
    
    # Lists
    print("\n--- Lists ---");
    fruits: list[str] = ["apple", "banana", "cherry", "date"];
    numbers: list[int] = [1, 2, 3, 4, 5];
    
    print(f"Fruits: {fruits}");
    print(f"Numbers: {numbers}");
    
    # Accessing list elements
    print(f"First fruit: {fruits[0]}");
    print(f"Last fruit: {fruits[len(fruits)-1]}");
    
    # Adding to lists
    fruits.append("elderberry");
    print(f"After adding elderberry: {fruits}");
    
    # For-in loop with lists
    print("\n--- Iterating through list ---");
    for fruit in fruits {
        print(f"I like {fruit}");
    }
    
    # List comprehensions
    print("\n--- List Comprehensions ---");
    squares = [n * n for n in numbers];
    print(f"Numbers: {numbers}");
    print(f"Squares: {squares}");
    
    # Filter with list comprehension
    even_squares = [n * n for n in numbers if n % 2 == 0];
    print(f"Even squares: {even_squares}");
}

with entry {
    print("\n=== Dictionaries ===");
    
    # Dictionary creation
    student_grades: dict[str, int] = {
        "Alice": 95,
        "Bob": 87,
        "Charlie": 92,
        "Diana": 88
    };
    
    print(f"Student grades: {student_grades}");
    
    # Accessing values
    print(f"Alice's grade: {student_grades["Alice"]}");
    
    # Adding new entries
    student_grades["Eve"] = 94;
    print(f"After adding Eve: {student_grades}");
    
    # Iterating through dictionary
    print("\n--- All students and grades ---");
    for (name, grade) in student_grades.items() {
        letter_grade = "A" if grade >= 90 else "B" if grade >= 80 else "C" if grade >= 70 else "D";
        print(f"{name}: {grade} ({letter_grade})");
    }
    
    # Dictionary methods
    print(f"\nClass average: {sum(student_grades.values()) / len(student_grades):.1f}");
    print(f"Highest grade: {max(student_grades.values())}");
    print(f"Student names: {list(student_grades.keys())}");
}

with entry {
    print("\n=== Sets ===");
    
    # Set creation
    alice_courses: set[str] = {"Math", "Science", "English", "History"};
    bob_courses: set[str] = {"Math", "Art", "Music", "Science"};
    
    print(f"Alice's courses: {alice_courses}");
    print(f"Bob's courses: {bob_courses}");
    
    # Set operations
    common_courses = alice_courses.intersection(bob_courses);
    print(f"Common courses: {common_courses}");
    
    all_courses = alice_courses.union(bob_courses);
    print(f"All unique courses: {all_courses}");
    
    only_alice = alice_courses.difference(bob_courses);
    print(f"Only Alice: {only_alice}");
    
    # Set membership
    print(f"\nIs Math in Alice's courses? { "Math" in alice_courses }");
    print(f"Is Art in Bob's courses? { "Art" in bob_courses }");
}

with entry {
    print("\n=== Nested Collections ===");
    
    # List of dictionaries
    students: list[dict[str, any]] = [
        {"name": "Alice", "age": 20, "grade": 95},
        {"name": "Bob", "age": 19, "grade": 87},
        {"name": "Charlie", "age": 21, "grade": 92}
    ];
    
    print("Student information:");
    for student in students {
        print(f"  {student["name"]}: age {student["age"]}, grade {student["grade"]}");
    }
    
    # Dictionary of lists
    class_schedule: dict[str, list[str]] = {
        "Monday": ["Math", "Science", "English"],
        "Tuesday": ["History", "Art", "Music"],
        "Wednesday": ["Math", "Science", "Physical Ed"]
    };
    
    print("\nClass schedule:");
    for (day, classes) in class_schedule.items() {
        print(f"  {day}: {', '.join(classes)}");
    }
    
    # Complex nested structure
    gradebook: dict[str, list[dict[str, int]]] = {
        "tests": [
            {"name": "Test 1", "score": 85},
            {"name": "Test 2", "score": 92}
        ],
        "quizzes": [
            {"name": "Quiz 1", "score": 88},
            {"name": "Quiz 2", "score": 94}
        ]
    };
    
    print("\nGradebook:");
    for (category, assessments) in gradebook.items() {
        print(f"  {category}:");
        for assessment in assessments {
            print(f"    {assessment["name"]}: {assessment["score"]}");
        }
    }
}

# Practice exercises
with entry {
    print("\n=== Practice Exercises ===");
    
    # Exercise 1: FizzBuzz
    print("\n--- FizzBuzz ---");
    for n = 1 to n <= 15 by n += 1 {
        if n % 15 == 0 {
            print("FizzBuzz");
        } elif n % 3 == 0 {
            print("Fizz");
        } elif n % 5 == 0 {
            print("Buzz");
        } else {
            print(n);
        }
    }
    
    # Exercise 2: Find prime numbers
    print("\n--- Prime Numbers (1-20) ---");
    primes: list[int] = [];
    for num = 2 to num <= 20 by num += 1 {
        is_prime = True;
        for divisor = 2 to divisor < num by divisor += 1 {
            if num % divisor == 0 {
                is_prime = False;
                break;
            }
        }
        if is_prime {
            primes.append(num);
        }
    }
    print(f"Primes: {primes}");
    
    # Exercise 3: Word frequency counter
    print("\n--- Word Frequency ---");
    text = "apple banana apple cherry banana apple date";
    words = text.split(" ");
    word_counts: dict[str, int] = {};
    
    for word in words {
        if word in word_counts {
            word_counts[word] += 1;
        } else {
            word_counts[word] = 1;
        }
    }
    
    print(f"Text: {text}");
    print("Word frequencies:");
    for (word, count) in word_counts.items() {
        print(f"  '{word}': {count}");
    }
}