import os
import shutil
import tempfile
import unittest

# CHANGE THIS:
# replace "checkmygrade" with your main python filename without .py
from checkmygrade import CheckMyGradeApp, Student, Course, Professor


class TestCheckMyGradeApp(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

        self.students_file = os.path.join(self.test_dir, "students.csv")
        self.courses_file = os.path.join(self.test_dir, "courses.csv")
        self.professors_file = os.path.join(self.test_dir, "professors.csv")
        self.login_file = os.path.join(self.test_dir, "login.csv")

        self.app = CheckMyGradeApp(
            students_file=self.students_file,
            courses_file=self.courses_file,
            professors_file=self.professors_file,
            login_file=self.login_file,
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    # -------------------------
    # Helper method
    # -------------------------
    def add_1000_students(self):
        for i in range(1000):
            student = Student(
                student_id=f"S{i:04d}",
                first_name=f"First{i}",
                last_name=f"Last{i}",
                email_address=f"student{i}@mycsu.edu",
                course_id="DATA200",
                grade="F",
                marks=i % 101,
            )
            self.app.add_new_student(student)

    # -------------------------
    # Student tests
    # -------------------------
    def test_add_student(self):
        student = Student("S1001", "Ana", "Lopez", "ana@mycsu.edu", "DATA200", "F", 84)
        result = self.app.add_new_student(student)

        self.assertTrue(result)
        self.assertEqual(len(self.app.students), 1)
        self.assertEqual(self.app.students[0].grade, "B")

    def test_delete_student(self):
        student = Student("S1001", "Ana", "Lopez", "ana@mycsu.edu", "DATA200", "F", 84)
        self.app.add_new_student(student)

        result = self.app.delete_new_student("S1001")

        self.assertTrue(result)
        self.assertEqual(len(self.app.students), 0)

    def test_modify_student(self):
        student = Student("S1001", "Ana", "Lopez", "ana@mycsu.edu", "DATA200", "F", 84)
        self.app.add_new_student(student)

        result = self.app.update_student_record("S1001", first_name="Ananya", marks=92)

        self.assertTrue(result)
        updated, _ = self.app.search_student_by_id("S1001")
        self.assertEqual(updated.first_name, "Ananya")
        self.assertEqual(updated.marks, 92.0)
        self.assertEqual(updated.grade, "A")

    def test_student_operations_with_1000_records(self):
        self.add_1000_students()

        self.assertEqual(len(self.app.students), 1000)

        found, elapsed = self.app.search_student_by_id("S0500")
        self.assertIsNotNone(found)
        self.assertEqual(found.email_address, "student500@mycsu.edu")

        print(f"\nSearch time for 1000 student records: {elapsed:.8f} seconds")

    def test_load_previous_run_and_search(self):
        self.add_1000_students()

        new_app = CheckMyGradeApp(
            students_file=self.students_file,
            courses_file=self.courses_file,
            professors_file=self.professors_file,
            login_file=self.login_file,
        )

        found, elapsed = new_app.search_student_by_id("S0999")

        self.assertIsNotNone(found)
        self.assertEqual(found.student_id, "S0999")

        print(f"\nReloaded CSV search time: {elapsed:.8f} seconds")

    def test_sort_students_by_email_ascending(self):
        self.app.add_new_student(Student("S001", "John", "Kim", "john@mycsu.edu", "CS101", "F", 92))
        self.app.add_new_student(Student("S002", "Ana", "Clooney", "ana@mycsu.edu", "DATA200", "F", 89))
        self.app.add_new_student(Student("S123", "Dave", "Clinton", "dave@mycsu.edu", "DATA500", "F", 78))

        elapsed = self.app.sort_students_by_email(reverse=False)

        emails = [student.email_address for student in self.app.students]
        self.assertEqual(emails, ["ana@mycsu.edu", "dave@mycsu.edu", "john@mycsu.edu"])

        print(f"\nSort by email ascending time: {elapsed:.8f} seconds")

    def test_sort_students_by_email_descending(self):
        self.app.add_new_student(Student("S001", "John", "Kim", "john@mycsu.edu", "CS101", "F", 92))
        self.app.add_new_student(Student("S002", "Ana", "Clooney", "ana@mycsu.edu", "DATA200", "F", 89))
        self.app.add_new_student(Student("S123", "Dave", "Clinton", "dave@mycsu.edu", "DATA500", "F", 78))

        elapsed = self.app.sort_students_by_email(reverse=True)

        emails = [student.email_address for student in self.app.students]
        self.assertEqual(emails, ["john@mycsu.edu", "dave@mycsu.edu", "ana@mycsu.edu"])

        print(f"\nSort by email descending time: {elapsed:.8f} seconds")

    def test_sort_students_by_marks_ascending(self):
        self.app.add_new_student(Student("S001", "John", "Kim", "john@mycsu.edu", "CS101", "F", 92))
        self.app.add_new_student(Student("S002", "Ana", "Clooney", "ana@mycsu.edu", "DATA200", "F", 89))
        self.app.add_new_student(Student("S123", "Dave", "Clinton", "dave@mycsu.edu", "DATA500", "F", 78))

        elapsed = self.app.sort_students_by_marks(reverse=False)

        marks = [student.marks for student in self.app.students]
        self.assertEqual(marks, [78.0, 89.0, 92.0])

        print(f"\nSort by marks ascending time: {elapsed:.8f} seconds")

    def test_sort_students_by_marks_descending(self):
        self.app.add_new_student(Student("S001", "John", "Kim", "john@mycsu.edu", "CS101", "F", 92))
        self.app.add_new_student(Student("S002", "Ana", "Clooney", "ana@mycsu.edu", "DATA200", "F", 89))
        self.app.add_new_student(Student("S123", "Dave", "Clinton", "dave@mycsu.edu", "DATA500", "F", 78))

        elapsed = self.app.sort_students_by_marks(reverse=True)

        marks = [student.marks for student in self.app.students]
        self.assertEqual(marks, [92.0, 89.0, 78.0])

        print(f"\nSort by marks descending time: {elapsed:.8f} seconds")

    # -------------------------
    # Course tests
    # -------------------------
    def test_add_course(self):
        course = Course("DATA200", "Data Science", 3, "Intro to DS")
        result = self.app.add_new_course(course)

        self.assertTrue(result)
        self.assertEqual(len(self.app.courses), 1)
        self.assertEqual(self.app.courses[0].course_id, "DATA200")

    def test_delete_course(self):
        self.app.add_new_course(Course("DATA200", "Data Science", 3, "Intro to DS"))

        result = self.app.delete_new_course("DATA200")

        self.assertTrue(result)
        self.assertEqual(len(self.app.courses), 0)

    def test_modify_course(self):
        self.app.add_new_course(Course("DATA200", "Data Science", 3, "Intro to DS"))

        result = self.app.modify_course("DATA200", course_name="Advanced Data Science", credits=4)

        self.assertTrue(result)
        self.assertEqual(self.app.courses[0].course_name, "Advanced Data Science")
        self.assertEqual(self.app.courses[0].credits, 4)

    # -------------------------
    # Professor tests
    # -------------------------
    def test_add_professor(self):
        professor = Professor("P001", "Michael John", "michael@mycsu.edu", "Senior Professor", "DATA200")
        result = self.app.add_new_professor(professor)

        self.assertTrue(result)
        self.assertEqual(len(self.app.professors), 1)
        self.assertEqual(self.app.professors[0].professor_id, "P001")

    def test_delete_professor(self):
        self.app.add_new_professor(
            Professor("P001", "Michael John", "michael@mycsu.edu", "Senior Professor", "DATA200")
        )

        result = self.app.delete_professor("P001")

        self.assertTrue(result)
        self.assertEqual(len(self.app.professors), 0)

    def test_modify_professor(self):
        self.app.add_new_professor(
            Professor("P001", "Michael John", "michael@mycsu.edu", "Senior Professor", "DATA200")
        )

        result = self.app.modify_professor_details("P001", name="Mike John", rank="Professor")

        self.assertTrue(result)
        self.assertEqual(self.app.professors[0].name, "Mike John")
        self.assertEqual(self.app.professors[0].rank, "Professor")


if __name__ == "__main__":
    unittest.main(verbosity=2)