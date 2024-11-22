def validate_score(func):
    """Decorator to validate score input: should be an integer between 1 and 100."""
    def wrapper(self, subject):  # Accept 'self' (instance) as the first argument
        while True:
            try:
                score = int(input(f"Enter the Score of {subject}: "))
                if 1 <= score <= 100:
                    return score
                else:
                    print("Invalid input. Score must be between 1 and 100.")
            except ValueError:
                print("Invalid input. Please enter an integer value for the score.")
    return wrapper

class Student:
    def __init__(self):
        self.students = {}  # Store students
        self.scores = {}    # Store scores

    def addStudent(self) -> dict:
        message = ""
        count = len(self.students)  # Initialize count based on current students
    
        while message != 'no':
            while True:  # Inner loop to ensure the user enters a valid name
                name = input("Enter student name: ").strip()  # .strip() removes leading/trailing spaces
                if name:  # If the name is not empty
                    break
                else:
                    print("Name cannot be empty. Please enter a valid name.")
        
            # Generate a new student ID based on the current count
            new_id = f's{count + 1}'
            print(f"{name} is assigned the student ID {new_id}")
        
            student = {'sid': new_id, 'sName': name}
            print(f"Student added: {student}")
        
            # Add the new student to the dictionary with the new ID
            self.students[new_id] = student
            print(f"Updated Students: {self.students}")
        
            message = input("Enter 'no' to stop adding students, or any other key to continue: ")
            count += 1  # Increment the student count
    
        return self.students

    @validate_score  # Apply the decorator to this method
    def get_score(self, subject: str) -> int:
        """This method is now decorated, so the validation happens inside the decorator."""
        return 0  # This return is redundant; it is handled by the decorator.

    def addScore(self):
        """Adds scores for all students and stops automatically after all scores are entered."""
        
        # Process all students' scores
        for student_id, student in self.students.items():
            print(f"Enter marks for {student['sName']} (ID: {student_id})")
            
            # Get individual subject scores with validation via the decorator
            math = self.get_score("Mathematics")
            science = self.get_score("Science")
            english = self.get_score("English")
            
            # Store the scores in the 'scores' dictionary
            self.scores[student_id] = {
                'math': math,
                'science': science,
                'english': english
            }
            
            print(f"Marks for {student['sName']} are: {self.scores[student_id]}")
        
        # Once all scores are entered, print the final scores and stop
        print("All student scores:", self.scores)

    def display_all_results(self):
        """Display the list of all students with their marks, total, and average."""
        print("\nDisplaying results for all students:")
        print("=" * 60)  # Separator for better readability
        
        total_class_marks = 0
        total_class_subjects = 0
        
        # Iterate through the students and their scores
        for student_id, student in self.students.items():
            student_scores = self.scores.get(student_id, {})
            if student_scores:
                total_marks = sum(student_scores.values())  # Sum all subject scores
                average_marks = total_marks / len(student_scores)  # Average marks
                
                print(f"Student ID: {student_id}")
                print(f"Name: {student['sName']}")
                print("Marks:")
                for subject, marks in student_scores.items():
                    print(f"  {subject.capitalize()}: {marks}")
                print(f"Total Marks: {total_marks}")
                print(f"Average Marks: {average_marks:.2f}")
                print("-" * 60)  # Separator for each student
                
                total_class_marks += total_marks  # Sum for class total
                total_class_subjects += len(student_scores)  # Total subjects across all students
            else:
                print(f"Scores for {student['sName']} (ID: {student_id}) are not available.")
                print("-" * 60)

        # Calculate the class average
        if total_class_subjects > 0:
            class_average = total_class_marks / total_class_subjects
            print(f"\nClass Average Marks: {class_average:.2f}")
        else:
            print("\nNo class data available for average calculation.")


class PerformanceTracker(Student):
    def __init__(self):
        super().__init__()  # Initialize the parent class (Student)
    
    def cal_total(self, student_id: str) -> int:
        """Calculate the total marks for a student."""
        student_scores = self.scores.get(student_id, None)
        if student_scores:
            total = sum(student_scores.values())  # Sum all subject scores
            return total
        else:
            print(f"No scores found for student with ID: {student_id}")
            return None  # Return None for invalid or missing data
    
    def cal_average(self, student_id: str) -> float:
        """Calculate the average marks for a student."""
        student_scores = self.scores.get(student_id, None)
        if student_scores:
            total = sum(student_scores.values())  # Sum all subject scores
            average = total / len(student_scores)  # Divide by the number of subjects
            return average
        else:
            print(f"No scores found for student with ID: {student_id}")
            return None  # Return None for invalid or missing data
    
    def is_pass(self, student_id: str) -> str:
        """Check if a student has passed based on their average score."""
        average = self.cal_average(student_id)
        if average is not None:
            if average >= 50:
                return "Pass"
            else:
                return "Fail"
        else:
            return "No data available"  # If no average can be calculated
    
    def cal_class_average(self) -> float:
        """Calculate the average marks for the entire class."""
        total_marks = 0
        total_subjects = 0
        
        # Iterate through all students' scores
        for student_scores in self.scores.values():
            total_marks += sum(student_scores.values())
            total_subjects += len(student_scores)
        
        # Calculate the class average (total marks / total subjects)
        if total_subjects > 0:
            return total_marks / total_subjects
        else:
            return 0.0  # Return 0.0 if no subjects/scores are available
    
    def cal_class_total(self) -> int:
        """Calculate the total marks for the entire class."""
        total_class_marks = 0
        
        for student_scores in self.scores.values():
            total_class_marks += sum(student_scores.values())
        
        return total_class_marks


# Welcome note
print("Welcome to Student Performance Tracker System,\n where you can enter marks of students, and it will calculate their total average marks.\n It will also calculate the average of the whole class.")

# Create an instance of PerformanceTracker
tracker = PerformanceTracker()

# Ask if the user wants to enter student records
enter_records = input("Do you want to enter student records? (yes/no): ").strip().lower()

if enter_records == "yes":
    students = tracker.addStudent()  # Add some students

    # Check if there are students added before proceeding
    if len(students) > 0:
        tracker.addScore()    # Add scores for the students

        # Display all student results (marks, total, and average)
        tracker.display_all_results()

        # Ask the user to select a student ID to view results
        while True:
            student_id = input("\nSelect the student ID whose result you want to view, or type 'done' to finish: ").strip()
            
            if student_id == 'done':
                break  # Exit the loop if the user is done viewing results
            
            if student_id in tracker.students:
                total_marks = tracker.cal_total(student_id)
                average_marks = tracker.cal_average(student_id)
                pass_status = tracker.is_pass(student_id)

                print(f"\nResults for {tracker.students[student_id]['sName']} (ID: {student_id}):")
        
                # Handle case where total or average might be None
                if total_marks is not None:
                    print(f"Total Marks: {total_marks}")
                else:
                    print("Total Marks: Data not available")
        
                if average_marks is not None:
                    print(f"Average Marks: {average_marks:.2f}")
                else:
                    print("Average Marks: Data not available")
        
                print(f"Pass Status: {pass_status}")
            else:
                print(f"Student ID {student_id} not found. Please enter a valid ID.")
    else:
        print("No students have been added.")
else:
    print("System will now exit.")
