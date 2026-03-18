# Overview
The Check My Grade App is a Python-based student management system that allows users to manage students, courses, professors, and grades through a menu-driven interface.

It is designed to demonstrate core programming concepts such as:
- Object-Oriented Programming (OOP)
- File handling (CSV)
- Searching and sorting algorithms
- Basic authentication system
- Unit testing and performance measurement

# Features
## Student Management
- Add, update, and delete student records
- Search students by ID and name
- Sort students by email and marks
- Generate reports (by course, professor, or student)

## Course Management
- Add, update, delete courses
- Search courses by ID
- Display all courses

## Professor Management
- Add, update, delete professors
- Assign professors to courses
- View professor’s course and students

## Grades & Statistics
- Display grading scale
- Calculate average marks for a course
- Calculate median marks for a course

## Login & Account System
- Register new users
- Login with authentication

# How to Run the Application
- Open terminal or command prompt
- Navigate to the project folder
- Run:
  **python checkmygrade_app.py**
- Follow the menu options on screen

# Running Unit Tests
To run tests:
   **python -m unittest -v test_checkmygrade_app.py**

This will:
- Run all test cases
- Display execution time for search and sort operations
- Change password (encrypted storage)
