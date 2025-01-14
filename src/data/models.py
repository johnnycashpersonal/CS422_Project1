# models.py

"""
Data models for the EasyA Grade Analysis System.
These models define the structure of our database documents and provide
type hints for the rest of the application.
"""

class Course:
    def __init__(self, course_id: str, department: str, number: int, level: int):
        """
        Initialize a Course object.
        
        Args:
            course_id: Unique identifier (e.g., 'MATH111')
            department: Department code (e.g., 'MATH')
            number: Course number (e.g., 111)
            level: Course level (e.g., 100)
        """
        self.course_id = course_id
        self.department = department
        self.number = number
        self.level = level

    def to_dict(self):
        """Convert Course object to dictionary for MongoDB storage"""
        return {
            'course_id': self.course_id,
            'department': self.department,
            'number': self.number,
            'level': self.level
        }

class Instructor:
    def __init__(self, name: str, is_regular_faculty: bool, departments: list):
        """
        Initialize an Instructor object.
        
        Args:
            name: Full name of instructor
            is_regular_faculty: Whether they are regular faculty
            departments: List of department codes they teach in
        """
        self.name = name
        self.is_regular_faculty = is_regular_faculty
        self.departments = departments

    def to_dict(self):
        """Convert Instructor object to dictionary for MongoDB storage"""
        return {
            'name': self.name,
            'is_regular_faculty': self.is_regular_faculty,
            'departments': self.departments
        }

class GradeDistribution:
    def __init__(self, course_id: str, instructor_name: str, year: int,
                 term: str, percent_a: float, percent_df: float, total_students: int):
        """
        Initialize a GradeDistribution object.
        
        Args:
            course_id: Course identifier (e.g., 'MATH111')
            instructor_name: Name of instructor
            year: Year course was taught
            term: Term course was taught
            percent_a: Percentage of A grades
            percent_df: Percentage of D and F grades
            total_students: Total number of students
        """
        self.course_id = course_id
        self.instructor_name = instructor_name
        self.year = year
        self.term = term
        self.percent_a = percent_a
        self.percent_df = percent_df
        self.total_students = total_students

    def to_dict(self):
        """Convert GradeDistribution object to dictionary for MongoDB storage"""
        return {
            'course_id': self.course_id,
            'instructor_name': self.instructor_name,
            'year': self.year,
            'term': self.term,
            'percent_a': self.percent_a,
            'percent_df': self.percent_df,
            'total_students': self.total_students
        }