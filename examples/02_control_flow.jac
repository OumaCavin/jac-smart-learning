""" JAC Learning Examples - Control Flow """

with entry {
    print("=== Control Flow Examples ===");
    
    # If-else statements
    age = 18;
    if age >= 18 {
        print("You are an adult");
    } else {
        print("You are a minor");
    }
    
    # Multiple conditions
    temperature = 75;
    if temperature > 80 {
        print("It's hot!");
    } elif temperature > 60 {
        print("It's nice!");
    } else {
        print("It's cold!");
    }
    
    # Logical operators
    has_license = True;
    has_car = False;
    
    if has_license and has_car {
        print("You can drive anywhere!");
    } elif has_license {
        print("You have a license but no car");
    } else {
        print("You need a license");
    }
    
    # Comparison operators
    score = 85;
    if score >= 90 {
        grade = "A";
    } elif score >= 80 {
        grade = "B";
    } elif score >= 70 {
        grade = "C";
    } elif score >= 60 {
        grade = "D";
    } else {
        grade = "F";
    }
    
    print(f"Score: {score}, Grade: {grade}");
    
    # Ternary operator
    status = "pass" if score >= 60 else "fail";
    print(f"Status: {status}");
}

# Practice exercise: What's your grade?
with entry {
    print("\n=== Practice: Grade Calculator ===");
    
    test_score = 87;
    homework_score = 92;
    participation_score = 95;
    
    # Calculate weighted average (40% tests, 40% homework, 20% participation)
    average = (test_score * 0.4) + (homework_score * 0.4) + (participation_score * 0.2);
    
    if average >= 90 {
        letter_grade = "A";
    } elif average >= 80 {
        letter_grade = "B";
    } elif average >= 70 {
        letter_grade = "C";
    } elif average >= 60 {
        letter_grade = "D";
    } else {
        letter_grade = "F";
    }
    
    print(f"Test score: {test_score}");
    print(f"Homework score: {homework_score}");
    print(f"Participation score: {participation_score}");
    print(f"Average: {average:.1f}");
    print(f"Letter grade: {letter_grade}");
    
    # Extra credit: bonus points
    bonus_points = 5;
    final_average = min(average + bonus_points, 100);
    print(f"Final average with bonus: {final_average:.1f}");
}