# test_database.py

from src.data.db_manager import DatabaseManager
from src.data.models import Course, Instructor, GradeDistribution

def test_database():
    # Create database manager instance
    db = DatabaseManager()

    # Insert test data
    test_course = Course(
        course_id="MATH111",
        department="MATH",
        number=111,
        level=100
    )
    
    test_instructor = Instructor(
        name="John Smith",
        is_regular_faculty=True,
        departments=["MATH"]
    )
    
    test_grade = GradeDistribution(
        course_id="MATH111",
        instructor_name="John Smith",
        year=2015,
        term="Fall",
        percent_a=85.0,
        percent_df=5.0,
        total_students=30
    )

    # Insert into MongoDB
    db.courses.insert_one(test_course.to_dict())
    db.instructors.insert_one(test_instructor.to_dict())
    db.grade_distributions.insert_one(test_grade.to_dict())

    # Retrieve and print the data
    print("\nCourses in database:")
    for course in db.courses.find():
        print(course)

    print("\nInstructors in database:")
    for instructor in db.instructors.find():
        print(instructor)

    print("\nGrade distributions in database:")
    for grade in db.grade_distributions.find():
        print(grade)

    # Test some queries
    print("\nTesting course stats for MATH111:")
    stats = db.get_course_stats("MATH111")
    print(stats)

if __name__ == "__main__":
    test_database()