""" JAC Learning Examples - Object-Oriented Programming """

# Define a simple Student class
obj Student {
    has name: str;
    has age: int;
    has grades: list[float] = [];
    
    # Method to add a grade
    def add_grade(grade: float) -> None {
        self.grades.append(grade);
        print(f"Added grade {grade} for {self.name}");
    }
    
    # Method to calculate average
    def get_average() -> float {
        if len(self.grades) == 0 {
            return 0.0;
        }
        return sum(self.grades) / len(self.grades);
    }
    
    # Method to get letter grade
    def get_letter_grade() -> str {
        average = self.get_average();
        if average >= 90 {
            return "A";
        } elif average >= 80 {
            return "B";
        } elif average >= 70 {
            return "C";
        } elif average >= 60 {
            return "D";
        } else {
            return "F";
        }
    }
    
    # Method to display student info
    def display_info() -> str {
        avg = self.get_average();
        return f"{self.name} (age {self.age}): {avg:.1f} ({self.get_letter_grade()})";
    }
}

# Define a Calculator class
obj Calculator {
    has history: list[str] = [];
    has result: float = 0.0;
    
    def add(a: float, b: float) -> float {
        self.result = a + b;
        self.history.append(f"{a} + {b} = {self.result}");
        return self.result;
    }
    
    def subtract(a: float, b: float) -> float {
        self.result = a - b;
        self.history.append(f"{a} - {b} = {self.result}");
        return self.result;
    }
    
    def multiply(a: float, b: float) -> float {
        self.result = a * b;
        self.history.append(f"{a} * {b} = {self.result}");
        return self.result;
    }
    
    def divide(a: float, b: float) -> float | str {
        if b == 0 {
            self.history.append(f"ERROR: Division by zero ({a} / {b})");
            return "Error: Cannot divide by zero!";
        }
        self.result = a / b;
        self.history.append(f"{a} / {b} = {self.result}");
        return self.result;
    }
    
    def get_history() -> list[str] {
        return self.history;
    }
    
    def clear_history() -> None {
        self.history = [];
    }
}

# Define a BankAccount class
obj BankAccount {
    has account_holder: str;
    has account_number: str;
    has balance: float = 0.0;
    has transactions: list[str] = [];
    
    def deposit(amount: float) -> bool {
        if amount <= 0 {
            print("Error: Deposit amount must be positive");
            return False;
        }
        self.balance += amount;
        self.transactions.append(f"Deposit: +${amount:.2f}");
        print(f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}");
        return True;
    }
    
    def withdraw(amount: float) -> bool {
        if amount <= 0 {
            print("Error: Withdrawal amount must be positive");
            return False;
        }
        if amount > self.balance {
            print("Error: Insufficient funds");
            return False;
        }
        self.balance -= amount;
        self.transactions.append(f"Withdrawal: -${amount:.2f}");
        print(f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}");
        return True;
    }
    
    def get_balance() -> float {
        return self.balance;
    }
    
    def get_transactions() -> list[str] {
        return self.transactions;
    }
}

with entry {
    print("=== Object-Oriented Programming Examples ===");
    
    # Creating and using Student objects
    print("\n--- Student Class ---");
    alice = Student("Alice", 20);
    bob = Student("Bob", 19);
    
    # Adding grades
    alice.add_grade(95.0);
    alice.add_grade(87.0);
    alice.add_grade(92.0);
    
    bob.add_grade(78.0);
    bob.add_grade(85.0);
    bob.add_grade(90.0);
    
    # Displaying information
    print(alice.display_info());
    print(bob.display_info());
    
    # Creating a list of students
    students: list[Student] = [alice, bob];
    
    print("\nClass summary:");
    for student in students {
        print(f"  {student.display_info()}");
    }
}

with entry {
    print("\n--- Calculator Class ---");
    
    # Creating a calculator
    calc = Calculator();
    
    # Performing calculations
    result1 = calc.add(10.0, 5.0);
    result2 = calc.subtract(10.0, 3.0);
    result3 = calc.multiply(4.0, 6.0);
    result4 = calc.divide(15.0, 3.0);
    result5 = calc.divide(10.0, 0.0);  # This will cause an error
    
    print(f"Last result: {calc.result}");
    
    # Displaying history
    print("\nCalculation history:");
    for entry in calc.get_history() {
        print(f"  {entry}");
    }
    
    # Clearing history
    calc.clear_history();
    print("\nHistory cleared");
}

with entry {
    print("\n--- BankAccount Class ---");
    
    # Creating a bank account
    account = BankAccount("John Doe", "123456789");
    
    # Performing transactions
    account.deposit(1000.0);
    account.deposit(500.0);
    account.withdraw(200.0);
    account.withdraw(1500.0);  # This should fail (insufficient funds)
    account.withdraw(300.0);
    
    print(f"\nFinal balance: ${account.get_balance():.2f}");
    
    print("\nTransaction history:");
    for transaction in account.get_transactions() {
        print(f"  {transaction}");
    }
}

# Interface and Implementation Separation Example
# File: student_advanced.jac
obj GradeBook {
    has students: dict[str, Student] = {};
    
    def add_student(name: str, age: int) -> None;
    def get_student(name: str) -> Student;
    def get_class_average() -> float;
    def display_all_students() -> None;
}

# File: student_advanced.impl.jac
impl GradeBook.add_student(name: str, age: int) -> None {
    if name not in self.students {
        self.students[name] = Student(name, age);
        print(f"Added student: {name}");
    } else {
        print(f"Student {name} already exists");
    }
}

impl GradeBook.get_student(name: str) -> Student {
    if name in self.students {
        return self.students[name];
    } else {
        print(f"Student {name} not found");
        return Student("Unknown", 0);
    }
}

impl GradeBook.get_class_average() -> float {
    if len(self.students) == 0 {
        return 0.0;
    }
    
    total_average = 0.0;
    for student in self.students.values() {
        total_average += student.get_average();
    }
    return total_average / len(self.students);
}

impl GradeBook.display_all_students() -> None {
    if len(self.students) == 0 {
        print("No students in gradebook");
        return;
    }
    
    print("Gradebook contents:");
    for student in self.students.values() {
        print(f"  {student.display_info()}");
    }
    
    class_avg = self.get_class_average();
    print(f"Class average: {class_avg:.1f}");
}

with entry {
    print("\n--- GradeBook with Interface Separation ---");
    
    # Create a gradebook
    gradebook = GradeBook();
    
    # Add students
    gradebook.add_student("Alice", 20);
    gradebook.add_student("Bob", 19);
    gradebook.add_student("Charlie", 21);
    
    # Add some grades
    alice = gradebook.get_student("Alice");
    alice.add_grade(88.0);
    alice.add_grade(92.0);
    
    bob = gradebook.get_student("Bob");
    bob.add_grade(85.0);
    bob.add_grade(89.0);
    
    charlie = gradebook.get_student("Charlie");
    charlie.add_grade(94.0);
    charlie.add_grade(87.0);
    
    # Display all students
    gradebook.display_all_students();
}

# Practice exercise: Library system
with entry {
    print("\n=== Practice: Library System ===");
    
    obj Book {
        has title: str;
        has author: str;
        has isbn: str;
        is_checked_out: bool = False;
        due_date: str = "";
        
        def check_out(days: int) -> bool {
            if self.is_checked_out {
                print(f"Book '{self.title}' is already checked out");
                return False;
            }
            self.is_checked_out = True;
            self.due_date = f"Due in {days} days";
            print(f"Checked out '{self.title}' - {self.due_date}");
            return True;
        }
        
        def check_in() -> bool {
            if not self.is_checked_out {
                print(f"Book '{self.title}' is not checked out");
                return False;
            }
            self.is_checked_out = False;
            self.due_date = "";
            print(f"Returned '{self.title}'");
            return True;
        }
    }
    
    obj Library {
        has books: dict[str, Book] = {};
        has name: str;
        
        def add_book(title: str, author: str, isbn: str) -> None {
            if isbn in self.books {
                print(f"Book with ISBN {isbn} already exists");
                return;
            }
            self.books[isbn] = Book(title, author, isbn);
            print(f"Added '{title}' by {author}");
        }
        
        def check_out_book(isbn: str, days: int) -> bool {
            if isbn not in self.books {
                print(f"Book with ISBN {isbn} not found");
                return False;
            }
            return self.books[isbn].check_out(days);
        }
        
        def check_in_book(isbn: str) -> bool {
            if isbn not in self.books {
                print(f"Book with ISBN {isbn} not found");
                return False;
            }
            return self.books[isbn].check_in();
        }
        
        def list_books() -> None {
            print(f"\n{self.name} - Books:");
            for book in self.books.values() {
                status = "Available" if not book.is_checked_out else f"Checked out ({book.due_date})";
                print(f"  '{book.title}' by {book.author} - {status}");
            }
        }
    }
    
    # Create a library and add some books
    library = Library("City Library");
    
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "978-0-7432-7356-5");
    library.add_book("1984", "George Orwell", "978-0-452-28423-4");
    library.add_book("To Kill a Mockingbird", "Harper Lee", "978-0-06-112008-4");
    
    library.list_books();
    
    # Check out some books
    library.check_out_book("978-0-7432-7356-5", 14);
    library.check_out_book("978-0-452-28423-4", 21);
    
    library.list_books();
    
    # Check in a book
    library.check_in_book("978-0-7432-7356-5");
    
    library.list_books();
}