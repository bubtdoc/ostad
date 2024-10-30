import json

class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        print(f"Name: {self.name}\nAge: {self.age}\nAddress: {self.address}")

class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []

    def add_grade(self, subject, grade):
        if subject in self.courses:
            self.grades[subject] = grade
            print(f"Grade {grade} added for {self.name} in {subject}.")
        else:
            print(f"{self.name} is not enrolled in {subject}.")

    def enroll_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
            print(f"{self.name} (ID: {self.student_id}) enrolled in {course}.")
        else:
            print(f"{self.name} is already enrolled in {course}.")

    def display_student_info(self):
        self.display_person_info()
        print(f"Student ID: {self.student_id}")
        print(f"Enrolled Courses: {', '.join(self.courses) if self.courses else 'None'}")
        print(f"Grades: {self.grades if self.grades else 'No grades assigned'}")

class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)
            print(f"{student.name} (ID: {student.student_id}) added to {self.course_name}.")
        else:
            print(f"{student.name} is already in this course.")

    def display_course_info(self):
        print(f"Course Name: {self.course_name}\nCourse Code: {self.course_code}")
        print(f"Instructor: {self.instructor}")
        print("Enrolled Students:")
        for student in self.students:
            print(f"- {student.name}")

class StudentManagementSystem:
    def __init__(self):
        self.students = {}
        self.courses = {}

    def add_student(self):
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        address = input("Enter Address: ")
        student_id = input("Enter Student ID: ")
        if student_id not in self.students:
            student = Student(name, age, address, student_id)
            self.students[student_id] = student
            print(f"Student {name} (ID: {student_id}) added successfully.")
        else:
            print("Student ID already exists.")

    def add_course(self):
        course_name = input("Enter Course Name: ")
        course_code = input("Enter Course Code: ")
        instructor = input("Enter Instructor Name: ")
        if course_code not in self.courses:
            course = Course(course_name, course_code, instructor)
            self.courses[course_code] = course
            print(f"Course {course_name} (Code: {course_code}) created with instructor {instructor}.")
        else:
            print("Course Code already exists.")

    def enroll_student_in_course(self):
        student_id = input("Enter Student ID: ")
        course_code = input("Enter Course Code: ")
        student = self.students.get(student_id)
        course = self.courses.get(course_code)

        if student and course:
            student.enroll_course(course.course_name)
            course.add_student(student)
        else:
            print("Invalid Student ID or Course Code.")

    def add_grade_for_student(self):
        student_id = input("Enter Student ID: ")
        course_code = input("Enter Course Code: ")
        grade = input("Enter Grade: ")
        student = self.students.get(student_id)
        course = self.courses.get(course_code)

        if student and course and course.course_name in student.courses:
            student.add_grade(course.course_name, grade)
        else:
            print("Student is not enrolled in the course or invalid entries.")

    def display_student_details(self):
        student_id = input("Enter Student ID: ")
        student = self.students.get(student_id)
        if student:
            student.display_student_info()
        else:
            print("Student not found.")

    def display_course_details(self):
        course_code = input("Enter Course Code: ")
        course = self.courses.get(course_code)
        if course:
            course.display_course_info()
        else:
            print("Course not found.")

    def save_data(self):
        data = {
            "students": {
                sid: {
                    "name": student.name,
                    "age": student.age,
                    "address": student.address,
                    "student_id": student.student_id,
                    "grades": student.grades,
                    "courses": student.courses,
                }
                for sid, student in self.students.items()
            },
            "courses": {
                cid: {
                    "course_name": course.course_name,
                    "course_code": course.course_code,
                    "instructor": course.instructor,
                    "students": [student.student_id for student in course.students],
                }
                for cid, course in self.courses.items()
            }
        }
        with open("student_management_system.json", "w") as file:
            json.dump(data, file)
        print("All student and course data saved successfully.")

    def load_data(self):
        try:
            with open("student_management_system.json", "r") as file:
                data = json.load(file)
            self.students = {
                sid: Student(info["name"], info["age"], info["address"], info["student_id"])
                for sid, info in data["students"].items()
            }
            for sid, info in data["students"].items():
                self.students[sid].grades = info["grades"]
                self.students[sid].courses = info["courses"]

            self.courses = {
                cid: Course(info["course_name"], info["course_code"], info["instructor"])
                for cid, info in data["courses"].items()
            }
            for cid, info in data["courses"].items():
                for student_id in info["students"]:
                    student = self.students.get(student_id)
                    if student:
                        self.courses[cid].add_student(student)
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No saved data found.")

    def menu(self):
        while True:
            print("\n==== Student Management System ====")
            print("1. Add New Student")
            print("2. Add New Course")
            print("3. Enroll Student in Course")
            print("4. Add Grade for Student")
            print("5. Display Student Details")
            print("6. Display Course Details")
            print("7. Save Data to File")
            print("8. Load Data from File")
            print("0. Exit")
            choice = input("Select Option: ")

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.add_course()
            elif choice == "3":
                self.enroll_student_in_course()
            elif choice == "4":
                self.add_grade_for_student()
            elif choice == "5":
                self.display_student_details()
            elif choice == "6":
                self.display_course_details()
            elif choice == "7":
                self.save_data()
            elif choice == "8":
                self.load_data()
            elif choice == "0":
                print("Exiting Student Management System. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    system = StudentManagementSystem()
    system.menu()
