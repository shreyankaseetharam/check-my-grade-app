import csv
import os
import time
import statistics
import base64

from pathlib import Path

class Person:
    def __init__(self, email_address, first_name=None, last_name=None, name=None):
        self.email_address = email_address.strip()
        self.first_name = ""
        self.last_name = ""
        self.name = ""

        if first_name is not None and last_name is not None:
            self.first_name = first_name.strip()
            self.last_name = last_name.strip()
            self.name = f"{self.first_name} {self.last_name}"
        elif name is not None:
            self.name = name.strip()

    def get_email(self):
        return self.email_address

class Student(Person):
    def __init__(self, student_id, first_name, last_name, email_address, course_id, grade, marks):
        super().__init__(email_address=email_address, first_name=first_name, last_name=last_name)
        self.student_id= student_id.strip()
        self.course_id = course_id.strip()
        self.grade = grade.strip().upper()
        self.marks = float(marks)

    def display_records(self):
        return (
            f"Student ID: {self.student_id}, Name: {self.first_name} {self.last_name}, "
            f"Email: {self.email_address}, Course: {self.course_id}, Grade: {self.grade}, Marks: {self.marks}"
        )

    def update_student_record(
        self,
        first_name=None,
        last_name=None,
        email_address=None,
        course_id=None,
        grade=None,
        marks=None,
    ):
        if first_name is not None:
            self.first_name = first_name.strip()
        if last_name is not None:
            self.last_name = last_name.strip()
        if first_name is not None or last_name is not None:
            self.name = f"{self.first_name} {self.last_name}"
        if email_address is not None:
            self.email_address = email_address.strip()
        if course_id is not None:
            self.course_id = course_id.strip()
        if grade is not None:
            self.grade = grade.strip().upper()
        if marks is not None:
            self.marks = float(marks)

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_address": self.email_address,
            "course_id": self.course_id,
            "grade": self.grade,
            "marks": self.marks,
        }

class Course:
    def __init__(self, course_id, course_name, credits, description=""):
        self.course_id = course_id.strip()
        self.course_name = course_name.strip()
        self.credits = int(credits)
        self.description = description.strip()
    
    def display_courses(self):
        return (
            f"Course ID: {self.course_id}, Course Name: {self.course_name}, "
            f"Credits: {self.credits}, Description: {self.description}"
        )

    def update_course(self, course_name=None, credits=None, description=None):
        if course_name is not None:
            self.course_name = course_name.strip()
        if credits is not None:
            self.credits = int(credits)
        if description is not None:
            self.description = description.strip()
    
    def to_dict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "credits": self.credits,
            "description": self.description
        }


class Professor(Person):   # IS-A relationship: Professor is a Person
    def __init__(self, professor_id, name, email_address, rank, course_id):
        super().__init__(email_address=email_address, name=name)
        self.professor_id = professor_id.strip()
        self.name = name.strip()
        self.email_address = email_address.strip()
        self.rank = rank.strip()
        self.course_id = course_id.strip()

    def professor_details(self):
        return (
            f"Professor ID: {self.professor_id}, Name: {self.name}, "
            f"Email: {self.email_address}, Rank: {self.rank}, Course ID: {self.course_id}"
        )

    def modify_professor_details(self, name=None, email_address=None, rank=None, course_id=None):
        if name is not None:
            self.name = name.strip()
        if email_address is not None:
            self.email_address = email_address.strip()
        if rank is not None:
            self.rank = rank.strip()
        if course_id is not None:
            self.course_id = course_id.strip()

    def show_course_details_by_professor(self):
        return self.course_id

    def to_dict(self):
        return {
            "professor_id": self.professor_id,
            "name": self.name,
            "email_address": self.email_address,
            "rank": self.rank,
            "course_id": self.course_id,
        }

class Grade:
    def __init__(self, grade_id, grade, min_marks, max_marks):
        self.grade_id = grade_id.strip()
        self.grade = grade.strip().upper()
        self.min_marks = float(min_marks)
        self.max_marks = float(max_marks)

    def display_grade_report(self):
        return (
            f"Grade ID: {self.grade_id}, Grade: {self.grade}, "
            f"Range: {self.min_marks}-{self.max_marks}"
        )

class LoginUser:
    def __init__(self, email_id, password, role):
        self.email_id = email_id.strip()
        self.password = password
        self.role = role.strip().lower()

    @staticmethod
    def encrypt_password(password):
        return base64.b64encode(password.encode("utf-8")).decode("utf-8")

    @staticmethod
    def decrypt_password(encrypted_password):
        return base64.b64decode(encrypted_password.encode("utf-8")).decode("utf-8")

    def to_dict(self):
        return {
            "email_id": self.email_id,
            "password": self.password,
            "role": self.role,
        }

class CheckMyGradeApp:
    def __init__(self, data_dir: str = None):
        base = Path(data_dir) if data_dir else Path.cwd() / "data"
        base.mkdir(parents=True, exist_ok=True)
        self.students_file = str(base / "students.csv")
        self.courses_file = str(base / "courses.csv")
        self.professors_file = str(base / "professors.csv")
        self.login_file = str(base / "login.csv")

        self.students = []
        self.courses = []
        self.professors = []
        self.login_users = []

        self.load_all_data()

    @staticmethod
    def calculate_grade_from_marks(marks):
        marks = float(marks)
        if marks >= 90:
            return "A"
        if marks >= 80:
            return "B"
        if marks >= 70:
            return "C"
        if marks >= 60:
            return "D"
        return "F"

    @staticmethod
    def is_valid_marks(marks):
        try:
            marks = float(marks)
            return 0 <= marks <= 100
        except ValueError:
            return False

    def load_all_data(self):
        self.load_students()
        self.load_courses()
        self.load_professors()
        self.load_login_users()

    def ensure_csv_files_exist(self):
        if not os.path.exists(self.students_file):
            with open(self.students_file, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "student_id",
                        "first_name",
                        "last_name",
                        "email_address",
                        "course_id",
                        "grade",
                        "marks",
                    ],
                )
                writer.writeheader()

        if not os.path.exists(self.courses_file):
            with open(self.courses_file, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=["course_id", "course_name", "credits", "description"],
                )
                writer.writeheader()

        if not os.path.exists(self.professors_file):
            with open(self.professors_file, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                file,
                fieldnames=["professor_id", "name", "email_address", "rank", "course_id"],
                )
                writer.writeheader()

        if not os.path.exists(self.login_file):
            with open(self.login_file, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=["email_id", "password", "role"],
                    )
                writer.writeheader()
    
    def load_students(self):
        self.students = []
        self.ensure_csv_files_exist()
        with open(self.students_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                student = Student(
                    row["student_id"],
                    row["first_name"],
                    row["last_name"],
                    row["email_address"],
                    row["course_id"],
                    row["grade"],
                    row["marks"],
                )
                self.students.append(student)

    def save_students(self):
        with open(self.students_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "student_id",
                    "first_name",
                    "last_name",
                    "email_address",
                    "course_id",
                    "grade",
                    "marks",
                ],
            )
            writer.writeheader()
            for student in self.students:
                writer.writerow(student.to_dict())
        
    def student_id_exists(self, student_id):
        for s in self.students:
            if s.student_id == student_id.strip():
                return True
        return False
    
    def course_exists(self, course_id):
        for course in self.courses:
            if course.course_id == course_id.strip():
                return True
        return False

    def load_courses(self):
        self.courses = []
        self.ensure_csv_files_exist()
        with open(self.courses_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                course = Course(
                    row["course_id"],
                    row["course_name"],
                    row["credits"],
                    row.get("description", ""),
                )
                self.courses.append(course)

    def save_courses(self):
        with open(self.courses_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["course_id", "course_name", "credits", "description"],
            )
            writer.writeheader()
            for course in self.courses:
                writer.writerow(course.to_dict())

    def load_professors(self):
        self.professors = []
        self.ensure_csv_files_exist()
        with open(self.professors_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                professor = Professor(
                    row["professor_id"],
                    row["name"],
                    row["email_address"],
                    row["rank"],
                    row["course_id"],
                )
                self.professors.append(professor)
    
    def save_professors(self):
        with open(self.professors_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["professor_id", "name", "email_address", "rank", "course_id"],
            )
            writer.writeheader()
            for professor in self.professors:
                writer.writerow(professor.to_dict())

    def load_login_users(self):
        self.login_users = []
        self.ensure_csv_files_exist()
        with open(self.login_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = LoginUser(row["email_id"], row["password"], row["role"])
                self.login_users.append(user)


    def save_login_users(self):
        with open(self.login_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["email_id", "password", "role"],
            )
            writer.writeheader()
            for user in self.login_users:
                writer.writerow(user.to_dict())

    def add_new_student(self, student):
        if not student.student_id.strip():
            raise ValueError("student_id cannot be empty")

        if any(s.student_id == student.student_id for s in self.students):
            raise ValueError("student_id must be unique")

        if any(s.email_address == student.email_address for s in self.students):
            raise ValueError("student email must be unique")
        
        if not self.course_exists(student.course_id):
            raise ValueError("course_id does not exist")

        if not self.is_valid_marks(student.marks):
            raise ValueError("marks must be between 0 and 100")

        student.grade = self.calculate_grade_from_marks(student.marks)
        self.students.append(student)
        self.save_students()
        return True

    def delete_new_student(self, student_id):
        for i, student in enumerate(self.students):
            if student.student_id == student_id:
                del self.students[i]
                self.save_students()
                return True
        return False

    def update_student_record(self, student_id, **kwargs):
        for student in self.students:
            if student.student_id == student_id:
                if "email_address" in kwargs:
                    new_email = kwargs["email_address"]
                    for other in self.students:
                        if other.student_id != student_id and other.email_address == new_email:
                            raise ValueError("student email must be unique")

                if "marks" in kwargs:
                    if not self.is_valid_marks(kwargs["marks"]):
                        raise ValueError("marks must be between 0 and 100")
                    kwargs["grade"] = self.calculate_grade_from_marks(kwargs["marks"])

                if "course_id" in kwargs:
                    if not self.course_exists(kwargs["course_id"]):
                        raise ValueError("course_id does not exist")

                student.update_student_record(**kwargs)
                self.save_students()
                return True
        return False

    def search_student_by_id(self, student_id):
        start_time = time.perf_counter()
        result = None
        for student in self.students:
            if student.student_id == student_id:
                result = student
                break
        end_time = time.perf_counter()
        return result, end_time - start_time

    def search_student_by_name(self, first_name=None, last_name=None):
        start_time = time.perf_counter()
        results = []

        first_name = first_name.strip().lower() if first_name else ""
        last_name = last_name.strip().lower() if last_name else ""

        for student in self.students:
            first_matches = not first_name or student.first_name.lower() == first_name
            last_matches = not last_name or student.last_name.lower() == last_name

            if first_matches and last_matches:
                results.append(student)

        end_time = time.perf_counter()
        return results, end_time - start_time
    
    def search_course_by_id(self, course_id):
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None
    
    def search_professor_by_id(self, professor_id):
        for professor in self.professors:
            if professor.professor_id == professor_id:
                return professor
        return None

    def sort_students_by_marks(self, reverse=False):
        start_time = time.perf_counter()
        self.students.sort(key=lambda s: s.marks, reverse=reverse)
        end_time = time.perf_counter()
        self.save_students()
        return end_time - start_time

    def sort_students_by_email(self, reverse=False):
        start_time = time.perf_counter()
        self.students.sort(
            key=lambda s: s.email_address.lower(),
            reverse=reverse
        )
        end_time = time.perf_counter()
        self.save_students()
        return end_time - start_time

    def display_all_students(self):
        if not self.students:
            return ["No student records found."]
        return [student.display_records() for student in self.students]
    
    def add_new_course(self, course):
        if not course.course_id.strip():
            raise ValueError("course_id cannot be empty")
        if any(c.course_id == course.course_id for c in self.courses):
            raise ValueError("course_id must be unique")

        self.courses.append(course)
        self.save_courses()
        return True

    def delete_new_course(self, course_id):
        for i, course in enumerate(self.courses):
            if course.course_id == course_id:
                del self.courses[i]
                self.save_courses()
                return True
        return False

    def modify_course(self, course_id, **kwargs):
        for course in self.courses:
            if course.course_id == course_id:
                course.update_course(**kwargs)
                self.save_courses()
                return True
        return False

    def display_courses(self):
        if not self.courses:
            return ["No course records found."]
        return [course.display_courses() for course in self.courses]

    def add_new_professor(self, professor):
        if not professor.professor_id.strip():
            raise ValueError("professor_id cannot be empty")
        if any(p.professor_id == professor.professor_id for p in self.professors):
            raise ValueError("professor_id must be unique")
        if any(p.email_address == professor.email_address for p in self.professors):
            raise ValueError("professor email must be unique")
        if not self.course_exists(professor.course_id):
            raise ValueError("course_id does not exist")

        self.professors.append(professor)
        self.save_professors()
        return True

    def delete_professor(self, professor_id):
        for i, professor in enumerate(self.professors):
            if professor.professor_id == professor_id:
                del self.professors[i]
                self.save_professors()
                return True
        return False

    def modify_professor_details(self, professor_id, **kwargs):
        for professor in self.professors:
            if professor.professor_id == professor_id:
                if "email_address" in kwargs:
                    new_email = kwargs["email_address"]
                    for other in self.professors:
                        if other.professor_id != professor_id and other.email_address == new_email:
                            raise ValueError("professor email must be unique")
                
                if "course_id" in kwargs:
                    if not self.course_exists(kwargs["course_id"]):
                        raise ValueError("course_id does not exist")

                professor.modify_professor_details(**kwargs)
                self.save_professors()
                return True
        return False

    def display_professors(self):
        if not self.professors:
            return ["No professor records found."]
        return [professor.professor_details() for professor in self.professors] 

    def register_user(self, email_id, plain_password, role):
        if any(user.email_id == email_id for user in self.login_users):
            raise ValueError("email already exists")

        encrypted_password = LoginUser.encrypt_password(plain_password)
        user = LoginUser(email_id, encrypted_password, role)
        self.login_users.append(user)
        self.save_login_users()
        return True

    def login(self, email_id, plain_password):
        for user in self.login_users:
            if user.email_id == email_id:
                decrypted_password = LoginUser.decrypt_password(user.password)
                if decrypted_password == plain_password:
                    return True, user.role
                return False, None
        return False, None

    def change_password(self, email_id, old_password, new_password):
        for user in self.login_users:
            if user.email_id == email_id:
                current_password = LoginUser.decrypt_password(user.password)
                if current_password == old_password:
                    user.password = LoginUser.encrypt_password(new_password)
                    self.save_login_users()
                    return True
                return False
        return False

    def average_scores_for_course(self, course_id):
        marks_list = [student.marks for student in self.students if student.course_id == course_id]
        if not marks_list:
            return None
        return statistics.mean(marks_list)

    def median_scores_for_course(self, course_id):
        marks_list = [student.marks for student in self.students if student.course_id == course_id]
        if not marks_list:
            return None
        return statistics.median(marks_list)

    def report_by_course(self, course_id):
        course_students = [student for student in self.students if student.course_id == course_id]
        report = {
            "course_id": course_id,
            "students": [student.display_records() for student in course_students],
            "average_marks": self.average_scores_for_course(course_id),
            "median_marks": self.median_scores_for_course(course_id),
        }
        return report

    def report_by_student(self, student_id):
        student, _ = self.search_student_by_id(student_id)
        if student is None:
            return None
        return {
            "student_id": student.student_id,
            "name": f"{student.first_name} {student.last_name}",
            "email": student.email_address,
            "course_id": student.course_id,
            "grade": student.grade,
            "marks": student.marks,
        }

    def report_by_professor(self, professor_id):
        professor = None
        for prof in self.professors:
            if prof.professor_id == professor_id:
                professor = prof
                break

        if professor is None:
            return None

        course_report = self.report_by_course(professor.course_id)
        return {
            "professor_id": professor.professor_id,
            "professor_name": professor.name,
            "course_id": professor.course_id,
            "course_report": course_report,
        }

def print_lines(lines):
    for line in lines:
        print(line)


def show_empty_data_messages(app):
    if not app.courses:
        print("No course records found. Please add data.")

    if not app.professors:
        print("No professor records found. Please add data.")

    if not app.students:
        print("No student records found. Please add data.")

    if not app.login_users:
        print("No user data found. Please add data.")   


def student_menu(app):
    while True:
        print("""
            *** STUDENT RECORDS ***
            Press [1] to display all students
            Press [2] to add a student
            Press [3] to delete a student
            Press [4] to update a student
            Press [5] to search a student by ID
            Press [6] to search a student by name
            Press [7] to sort students by email
            Press [8] to sort students by marks
            Press [9] to see report by course
            Press [10] to see report by professor
            Press [11] to see report by student
            Press [0] to go back
            """)
        choice = input("Select an option: ").strip()

        if choice == '1':
            print_lines(app.display_all_students())

        elif choice == '2':
            try:
                # --- STUDENT ID (must be unique) ---
                while True:
                    student_id = input("Enter student ID: ").strip()

                    if not student_id:
                        print("Error: Student ID cannot be empty.")
                        continue

                    if app.student_id_exists(student_id):
                        print("Error: The student ID is already assigned to someone else. Enter a different student ID.")
                        continue

                    break

                # --- FIRST NAME (required) ---
                while True:
                    first = input("Enter first name: ").strip()
                    if not first:
                        print("Error: First name cannot be empty.")
                    else:
                        break

                # --- LAST NAME (required) ---
                while True:
                    last = input("Enter last name: ").strip()
                    if not last:
                        print("Error: Last name cannot be empty.")
                    else:
                        break

                # --- EMAIL (required) ---
                while True:
                    email = input("Enter email address: ").strip()
                    if not email:
                        print("Error: Email cannot be empty.")
                    else:
                        break

                # --- COURSE (must exist) ---
                while True:
                    course = input("Enter course ID: ").strip()
                    if not course:
                        print("Error: Course ID cannot be empty.")
                        continue

                    if not app.course_exists(course):
                        print("Error: Course does not exist. Enter a valid course ID.")
                        continue

                    break

                # --- MARKS (must be valid number 0–100) ---
                while True:
                    marks_input = input("Enter marks: ").strip()

                    if not marks_input:
                        print("Error: Marks cannot be empty.")
                        continue

                    try:
                        marks = float(marks_input)
                        if not app.is_valid_marks(marks):
                            print("Error: Marks must be between 0 and 100.")
                            continue
                        break
                    except ValueError:
                        print("Error: Please enter a valid number for marks.")

                # --- CREATE STUDENT ---
                student = Student(student_id, first, last, email, course, "F", marks)
                app.add_new_student(student)

                print("-------------------------------------------")
                print("Student record added successfully to the database.")

            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '3':
            while True:
                student_id = input("Enter Student ID that needs to be deleted: ").strip()

                if not student_id:
                    print("Error: Student ID cannot be empty.")
                    continue

                # check if student exists
                student, _ = app.search_student_by_id(student_id)
                if not student:
                    print(f"Error: Student with ID {student_id} does not exist. Please enter a valid ID.")
                    continue

                break

            # now safe to delete
            app.delete_new_student(student_id)
            print("Student record deleted successfully from the database")

        elif choice == '4':
            try:
                # keep asking until a valid existing student ID is entered
                while True:
                    student_id = input("Enter Student ID whose record needs to be updated: ").strip()

                    if not student_id:
                        print("Error: Student ID cannot be empty.")
                        continue

                    student, _ = app.search_student_by_id(student_id)
                    if not student:
                        print(f"Error: Student with ID {student_id} does not exist. Please enter a valid ID.")
                        continue

                    break

                first = input("Enter new first name or press enter to skip: ").strip()
                last = input("Enter new last name or press enter to skip: ").strip()
                email = input("Enter new email or press enter to skip: ").strip()
                course = input("Enter new course ID or press enter to skip: ").strip()
                marks = input("Enter new marks or press enter to skip: ").strip()

                update_data = {}

                if first:
                    update_data["first_name"] = first
                if last:
                    update_data["last_name"] = last
                if email:
                    update_data["email_address"] = email
                if course:
                    update_data["course_id"] = course
                if marks:
                    update_data["marks"] = float(marks)

                if not update_data:
                    print("No new updates were made to the record.")
                elif app.update_student_record(student_id, **update_data):
                    print("Student record updated successfully.")
                else:
                    print(f"Student with ID {student_id} not found.")

            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '5':
            while True:
                student_id = input("Search a record using student ID: ").strip()

                if not student_id:
                    print("Error: Student ID cannot be empty. Please try again.")
                    continue

                student, elapsed = app.search_student_by_id(student_id)

                if student:
                    print(student.display_records())
                    print(f"Search time: {elapsed:.8f} seconds")
                    break
                else:
                    print(f"Error: Student with ID '{student_id}' does not exist. Please try again.")

        elif choice == '6':
            while True:
                first_name = input("Enter student's first name: ").strip()
                last_name = input("Enter student's last name (press enter to skip): ").strip()

                if not first_name and not last_name:
                    print("Error: I can't search with both fields empty. Please enter at least the first name.")
                    continue

                if not first_name:
                    print("Error: First name is required. Please enter the student's first name.")
                    continue

                results, elapsed = app.search_student_by_name(first_name, last_name)

                if results:
                    print("\nMatching student record(s):")
                    for student in results:
                        print(student.display_records())
                    print(f"Search time: {elapsed:.8f} seconds")
                    break
                else:
                    print(f"Student with first name '{first_name}' does not exist.")
                    if last_name:
                        print(f"No record found for name: {first_name} {last_name}")
                    print("Please try again.")

        elif choice == '7':
            while True:
                sort_choice = input(
                    "Sort student records by email - Press [a] for ascending or [d] for descending: "
                ).strip().lower()

                if sort_choice == 'a':
                    asc = True
                    break
                elif sort_choice == 'd':
                    asc = False
                    break
                else:
                    print("Error: Invalid option. Please enter 'a' for ascending or 'd' for descending.")

            elapsed = app.sort_students_by_email(reverse=not asc)
            print_lines(app.display_all_students())
            print(f"Sort time: {elapsed:.8f} seconds")


        elif choice == '8':
            while True:
                sort_choice = input(
                    "Sort student records by marks - Press [a] for ascending or [d] for descending: "
                ).strip().lower()

                if sort_choice == 'a':
                    asc = True
                    break
                elif sort_choice == 'd':
                    asc = False
                    break
                else:
                    print("Error: Invalid option. Please enter 'a' or 'd'.")

            elapsed = app.sort_students_by_marks(reverse=not asc)
            print_lines(app.display_all_students())
            print(f"Sort time: {elapsed:.8f} seconds")

        elif choice == '9':
            while True:
                cid = input("Course ID: ").strip()

                if not cid:
                    print("Error: Course ID cannot be empty. Please enter a valid course ID.")
                    continue

                if not app.course_exists(cid):
                    print(f"Error: Course with ID '{cid}' does not exist. Please try again.")
                    continue

                report = app.report_by_course(cid)

                print("\n *** COURSE REPORT ***")
                print(f"Course ID     : {report['course_id']}")
                print(f"Average Marks : {report['average_marks']}")
                print(f"Median Marks  : {report['median_marks']}")
                print("Students:")

                if report["students"]:
                    for line in report["students"]:
                        print("\n" + line)
                else:
                    print("No student records found for this course.")

                break

        elif choice == '10':
            while True:
                pid = input("Professor ID: ").strip()

                if not pid:
                    print("Error: Professor ID cannot be empty. Please enter a valid professor ID.")
                    continue

                professor = app.search_professor_by_id(pid)
                if not professor:
                    print(f"Error: Professor with ID '{pid}' does not exist. Please try again.")
                    continue

                report = app.report_by_professor(pid)

                print("\n *** PROFESSOR REPORT ***")
                print(f"Professor ID   : {report['professor_id']}")
                print(f"Professor Name : {report['professor_name']}")
                print(f"Course ID      : {report['course_id']}")
                print("\nThis professor teaches the following students:")

                students = report["course_report"]["students"]
                if students:
                    for line in students:
                        print(line)
                else:
                    print("No student records found for this professor yet.")

                break

        elif choice == '11':
            while True:
                student_id = input("Student ID: ").strip()

                if not student_id:
                    print("Error: Student ID cannot be empty. Please enter a valid student ID.")
                    continue

                student, _ = app.search_student_by_id(student_id)
                if not student:
                    print(f"Error: Student with ID '{student_id}' does not exist. Please try again.")
                    continue

                report = app.report_by_student(student_id)

                print("\n *** STUDENT REPORT ***")
                print(f"Student ID : {report['student_id']}")
                print(f"Name       : {report['name']}")
                print(f"Email      : {report['email']}")

                if report['course_id']:
                    print(f"Course ID  : {report['course_id']}")
                else:
                    print("Course ID  : Not enrolled in any course")

                print(f"Grade      : {report['grade']}")
                print(f"Marks      : {report['marks']}")
                break

        elif choice == '0':
            break

        else:
            print("Invalid option.")

def course_menu(app):
    while True:
        print("""
              *** COURSE MENU ***
                Press [1] to display all courses
                Press [2] to add a course
                Press [3] to delete a course
                Press [4] to modify a course
                Press [5] to search a course
                Press [0] to go back
              """)
        choice = input("Select an option: ").strip()

        if choice == '1':
            print_lines(app.display_courses())

        elif choice == '2':
            try:
                while True:
                    cid = input("Course ID   : ").strip()
                    if not cid:
                        print("Error: Course ID cannot be empty. Please enter a valid Course ID.")
                        continue

                    if app.course_exists(cid):
                        print(f"Error: Course with ID '{cid}' already exists. Please enter a different Course ID.")
                        continue
                    break

                while True:
                    name = input("Name        : ").strip()
                    if not name:
                        print("Error: Course name cannot be empty. Please enter a valid course name.")
                        continue
                    break

                while True:
                    credits = input("Credits     : ").strip()
                    if not credits:
                        print("Error: Credits cannot be empty. Please enter valid credits.")
                        continue

                    try:
                        credits_value = int(credits)
                        if credits_value <= 0:
                            print("Error: Credits must be greater than 0.")
                            continue
                        break
                    except ValueError:
                        print("Error: Credits must be a whole number.")

                desc = input("Description : ").strip()

                course = Course(cid, name, credits_value, desc)
                app.add_new_course(course)
                print("\nCourse has been added successfully.")

            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '3':
            while True:
                cid = input("Enter the Course ID to delete: ").strip()

                # Empty check
                if not cid:
                    print("Error: Course ID cannot be empty. Please enter a valid Course ID.")
                    continue

                # Check existence
                if not app.course_exists(cid):
                    print(f"Error: Course with ID '{cid}' does not exist. Please try again.")
                    continue

                # Check if assigned
                assigned_to_students = any(student.course_id == cid for student in app.students)
                assigned_to_professors = any(professor.course_id == cid for professor in app.professors)

                if assigned_to_students or assigned_to_professors:
                    print(f"Error: Course with ID '{cid}' cannot be deleted because it is assigned to existing student or professor records.")
                    continue

                while True:
                    confirm = input(f"Are you sure you want to delete course {cid}? (y/n): ").strip().lower()

                    if confirm == 'y':
                        app.delete_new_course(cid)
                        print("Course has been deleted successfully.")
                        break

                    elif confirm == 'n':
                        print("Deletion cancelled.")
                        break

                    else:
                        print("Error: Please enter 'y' for yes or 'n' for no.")

                break

        elif choice == '4':
            try:
                while True:
                    cid = input("Course ID to modify: ").strip()

                    if not cid:
                        print("Error: Course ID cannot be empty. Please try again.")
                        continue

                    if not app.course_exists(cid):
                        print(f"Error: Course with ID '{cid}' does not exist. Please try again.")
                        continue

                    break

                # Get updates
                name = input("Enter new course name or press enter to skip: ").strip()
                credits_input = input("Enter new course credits or press enter to skip: ").strip()
                desc = input("Enter new course description or press enter to skip: ").strip()

                update_data = {}

                if name:
                    update_data["course_name"] = name

                if credits_input:
                    while True:
                        try:
                            credits_value = int(credits_input)
                            if credits_value <= 0:
                                print("Error: Credits must be greater than 0.")
                                credits_input = input("Enter valid credits or press enter to skip: ").strip()
                                if not credits_input:
                                    break
                                continue
                            update_data["credits"] = credits_value
                            break
                        except ValueError:
                            print("Error: Credits must be a number.")
                            credits_input = input("Enter valid credits or press enter to skip: ").strip()
                            if not credits_input:
                                break

                if desc:
                    update_data["description"] = desc

                if not update_data:
                    print("No updates were provided.")
                else:
                    app.modify_course(cid, **update_data)
                    print(f"Course with ID {cid} updated successfully.")

            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '5':
            while True:
                cid = input("Course ID to search: ").strip()

                if not cid:
                    print("Error: Course ID cannot be empty. Please enter a valid Course ID.")
                    continue

                course = app.search_course_by_id(cid)

                if not course:
                    print(f"Error: Course with ID '{cid}' does not exist. Please try again.")
                    continue

                print(course.display_courses())
                break

        elif choice == '0':
            break

        else:
            print("Invalid option.")

def professor_menu(app):
    while True:
        print("""
            *** PROFESSOR MENU ***
            Press [1] to see list of all professors
            Press [2] to add a professor's information to list
            Press [3] to delete a professor's information from list
            Press [4] to modify a professor's information
            Press [5] to see a professor's course
            Press [0] to go back
            """)
        choice = input("Select an option: ").strip()

        if choice == '1':
            print_lines(app.display_professors())

        elif choice == '2':
            try:
                while True:
                    pid = input("Professor ID : ").strip()
                    if not pid:
                        print("Error: Professor ID cannot be empty.")
                        continue
                    if any(p.professor_id == pid for p in app.professors):
                        print("Error: Professor ID must be unique.")
                        continue
                    break

                while True:
                    name = input("Name         : ").strip()
                    if not name:
                        print("Error: Name cannot be empty.")
                        continue
                    break

                while True:
                    email = input("Email        : ").strip()
                    if not email:
                        print("Error: Email cannot be empty.")
                        continue
                    if any(p.email_address == email for p in app.professors):
                        print("Error: Professor email must be unique.")
                        continue
                    break

                while True:
                    rank = input("Rank         : ").strip()
                    if not rank:
                        print("Error: Rank cannot be empty.")
                        continue
                    break

                while True:
                    course = input("Course ID    : ").strip()
                    if not course:
                        print("Error: Course ID cannot be empty.")
                        continue
                    if not app.course_exists(course):
                        print("Error: Course does not exist. Enter a valid course ID.")
                        continue
                    break

                professor = Professor(pid, name, email, rank, course)
                app.add_new_professor(professor)
                print(f"Professor with ID {pid} added successfully.")

            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '3':
            pid = input("Professor ID to delete: ").strip()
            if app.delete_professor(pid):
                print(f"Professor with ID {pid} deleted successfully.")
            else:
                print(f"Professor with ID {pid} not found.")

        elif choice == '4':
            try:
                pid = input("Professor ID to modify: ").strip()
                name = input("New name   (blank to skip): ").strip()
                email = input("New email  (blank to skip): ").strip()
                rank = input("New rank   (blank to skip): ").strip()
                course = input("New course (blank to skip): ").strip()

                update_data = {}
                if name:
                    update_data["name"] = name
                if email:
                    update_data["email_address"] = email
                if rank:
                    update_data["rank"] = rank
                if course:
                    update_data["course_id"] = course

                if app.modify_professor_details(pid, **update_data):
                    print("Professor updated successfully.")
                else:
                    print(f"Professor with ID {pid} not found.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '5':
            pid = input("Professor ID: ").strip()
            professor = app.search_professor_by_id(pid)
            if professor:
                print(f"Professor Name: {professor.name}")
                print(f"Course ID: {professor.course_id}")
            else:
                print(f"Professor with ID {pid} not found.")

        elif choice == '0':
            break

        else:
            print("Invalid option.")

def grades_menu(app):
    while True:
        print("""
            *** GRADES MENU ***
            Press [1] to display grade scale
            Press [2] to see average marks for a course
            Press [3] to see median marks for a course
            Press [0] to go back
            """)
        choice = input("Select an option: ").strip()

        if choice == '1':
            print("""
                Grade Scale
                A : 90 - 100
                B : 80 - 89
                C : 70 - 79
                D : 60 - 69
                F : Below 60
                """)

        elif choice == '2':
            while True:
                cid = input("Course ID: ").strip()

                if not cid:
                    print("Error: Course ID cannot be empty. Please enter a valid Course ID.")
                    continue

                if not app.course_exists(cid):
                    print(f"Error: Course with ID '{cid}' does not exist. Please try again.")
                    continue

                avg = app.average_scores_for_course(cid)
                if avg is None:
                    print("No student records found for this course.")
                else:
                    print(f"Average marks for {cid}: {avg:.2f}")
                break

        elif choice == '3':
            while True:
                cid = input("Course ID: ").strip()

                if not cid:
                    print("Error: Course ID cannot be empty. Please enter a valid Course ID.")
                    continue

                if not app.course_exists(cid):
                    print(f"Error: Course with ID '{cid}' does not exist. Please try again.")
                    continue

                med = app.median_scores_for_course(cid)
                if med is None:
                    print("No student records found for this course.")
                else:
                    print(f"Median marks for {cid}: {med:.2f}")
                break

        elif choice == '0':
            break

        else:
            print("Invalid option.")


def login_menu(app):
    while True:
        print("""
            *** LOGIN / ACCOUNT MENU ***
            Press [1] to register new user
            Press [2] to login
            Press [3] to change password
            Press [0] to go back
            """)
        choice = input("Select an option: ").strip()

        if choice == '1':
            try:
                email = input("Email   : ").strip()
                pwd = input("Password: ").strip()
                role = input("Role (student/professor/admin): ").strip()
                app.register_user(email, pwd, role)
                print("User registered successfully.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '2':
            email = input("Email   : ").strip()
            pwd = input("Password: ").strip()
            status, role = app.login(email, pwd)
            if status:
                print(f"Login successful. Role: {role}")
            else:
                print("Invalid login.")

        elif choice == '3':
            email = input("Email       : ").strip()
            old_pwd = input("Old password: ").strip()
            new_pwd = input("New password: ").strip()
            if app.change_password(email, old_pwd, new_pwd):
                print("Password changed successfully.")
            else:
                print("Password change failed.")

        elif choice == '0':
            break

        else:
            print("Invalid option.")

def main():
    app = CheckMyGradeApp(data_dir="data")
    show_empty_data_messages(app)

    while True:
        print("""
                CHECK MY GRADE APP (Student / Course/ Professor Manager)
                *** MAIN MENU ***
                Press [1] to see - Student Records
                Press [2] to see - Course Records
                Press [3] to see - Professor Records
                Press [4] to see - Grades & Statistics
                Press [5] to Login or View Account
                Press [0] to exit this program
            """)
        choice = input("Select an option: ").strip()

        if choice == '1':
            student_menu(app)
        elif choice == '2':
            course_menu(app)
        elif choice == '3':
            professor_menu(app)
        elif choice == '4':
            grades_menu(app)
        elif choice == '5':
            login_menu(app)
        elif choice == '0':
            print("\nExiting Program. Goodbye!\n")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()