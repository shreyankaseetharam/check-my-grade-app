import os
import shutil
import unittest

from checkmygrade_app import CheckMyGradeApp, Student, Course, Professor

class TestCheckMyGradeApp(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_data"

        # remove old test folder if it exists
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

        self.app = CheckMyGradeApp(data_dir=self.test_dir)

        # add sample courses first, because students/professors need valid course_id
        self.app.add_new_course(Course("C101", "Python", 3, "Python programming"))
        self.app.add_new_course(Course("C102", "Data Science", 4, "Intro to data science"))

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_add_student(self):
        student = Student("S001", "John", "Doe", "john@example.com", "C101", "F", 85)
        result = self.app.add_new_student(student)
        self.assertTrue(result)
        self.assertEqual(len(self.app.students), 1)
        self.assertEqual(self.app.students[0].grade, "B")

    def test_update_student(self):
        student = Student("S001", "John", "Doe", "john@example.com", "C101", "F", 85)
        self.app.add_new_student(student)

        result = self.app.update_student_record("S001", marks=92)
        self.assertTrue(result)

        updated_student, _ = self.app.search_student_by_id("S001")
        self.assertIsNotNone(updated_student)
        self.assertEqual(updated_student.marks, 92.0)
        self.assertEqual(updated_student.grade, "A")

    def test_delete_student(self):
        student = Student("S001", "John", "Doe", "john@example.com", "C101", "F", 85)
        self.app.add_new_student(student)

        result = self.app.delete_new_student("S001")
        self.assertTrue(result)
        self.assertEqual(len(self.app.students), 0)

    def test_search_student_by_id_with_time(self):
        # add many records so timing screenshot looks meaningful
        for i in range(1000):
            sid = f"S{i:04d}"
            email = f"student{i}@example.com"
            student = Student(sid, f"First{i}", f"Last{i}", email, "C101", "F", 75)
            self.app.add_new_student(student)

        result, elapsed = self.app.search_student_by_id("S0999")
        self.assertIsNotNone(result)
        print(f"\n\nSearch by ID time: {elapsed:.8f} seconds")

    def test_search_student_by_name_with_time(self):
        for i in range(1000):
            sid = f"S{i:04d}"
            email = f"student{i}@example.com"
            student = Student(sid, f"First{i}", f"Last{i}", email, "C101", "F", 75)
            self.app.add_new_student(student)

        result, elapsed = self.app.search_student_by_name("First999", "Last999")
        self.assertIsNotNone(result)
        print(f"\nSearch by name time: {elapsed:.8f} seconds")

    def test_sort_students_by_marks_with_time(self):
        for i in range(1000):
            sid = f"S{i:04d}"
            email = f"student{i}@example.com"
            marks = (i * 7) % 101
            student = Student(sid, f"First{i}", f"Last{i}", email, "C101", "F", marks)
            self.app.add_new_student(student)

        elapsed = self.app.sort_students_by_marks(reverse=False)
        self.assertEqual(len(self.app.students), 1000)
        print(f"\nSort by marks time: {elapsed:.8f} seconds")

    def test_sort_students_by_email_with_time(self):
        for i in range(1000):
            sid = f"S{i:04d}"
            email = f"student{i}@example.com"
            student = Student(sid, f"First{i}", f"Last{i}", email, "C101", "F", 75)
            self.app.add_new_student(student)

        elapsed = self.app.sort_students_by_email(reverse=False)
        self.assertEqual(len(self.app.students), 1000)
        print(f"\nSort by email time: {elapsed:.8f} seconds")

    def test_add_course(self):
        result = self.app.add_new_course(Course("C103", "Statistics", 3, "Stats course"))
        self.assertTrue(result)
        self.assertIsNotNone(self.app.search_course_by_id("C103"))

    def test_modify_course(self):
        result = self.app.modify_course("C101", course_name="Advanced Python", credits=4)
        self.assertTrue(result)
        course = self.app.search_course_by_id("C101")
        self.assertEqual(course.course_name, "Advanced Python")
        self.assertEqual(course.credits, 4)

    def test_delete_course(self):
        result = self.app.delete_new_course("C102")
        self.assertTrue(result)
        self.assertIsNone(self.app.search_course_by_id("C102"))

    def test_add_professor(self):
        professor = Professor("P001", "Dr Smith", "smith@example.com", "Senior Professor", "C101")
        result = self.app.add_new_professor(professor)
        self.assertTrue(result)
        self.assertIsNotNone(self.app.search_professor_by_id("P001"))

    def test_modify_professor(self):
        professor = Professor("P001", "Dr Smith", "smith@example.com", "Senior Professor", "C101")
        self.app.add_new_professor(professor)

        result = self.app.modify_professor_details("P001", rank="Associate Professor")
        self.assertTrue(result)

        prof = self.app.search_professor_by_id("P001")
        self.assertEqual(prof.rank, "Associate Professor")

    def test_delete_professor(self):
        professor = Professor("P001", "Dr Smith", "smith@example.com", "Senior Professor", "C101")
        self.app.add_new_professor(professor)

        result = self.app.delete_professor("P001")
        self.assertTrue(result)
        self.assertIsNone(self.app.search_professor_by_id("P001"))


if __name__ == "__main__":
    unittest.main(verbosity=2)