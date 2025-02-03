import sys
# sys.path.insert(0,'../')
from src.data.db_manager import DatabaseManager
from admin.import_data import DataImporter
from datetime import datetime
from collections import defaultdict

def test_database_functionality():
    """
    Test database operations and queries using the existing project CSV data.
    Validates data import, retrieval, and query functionality.
    """
    # Redirect output to both console and file
    original_stdout = sys.stdout
    with open('test_output.txt', 'w') as f:
        class MultiWriter:
            def write(self, text):
                original_stdout.write(text)
                f.write(text)
            def flush(self):
                original_stdout.flush()
                f.flush()
        
        sys.stdout = MultiWriter()

        # Record test start time
        print(f"Test Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        # Initialize database components
        db = DatabaseManager()
        importer = DataImporter(db)
        
        # Clean existing data for fresh test
        print("Cleaning existing database collections...")
        db.courses.delete_many({})
        db.instructors.delete_many({})
        db.grade_distributions.delete_many({})

        # Import project data
        print("Importing data from JSON...")
        try:
            importer.import_grade_data("src/data/gradedata.js")
        except Exception as e:
            print(f"Error during data import: {str(e)}")
            return

        # Analyze data by year
        print("\nData Distribution by Year:")
        pipeline = [
            {"$group": {
                "_id": "$year",
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ]
        year_stats = list(db.grade_distributions.aggregate(pipeline))
        for year_stat in year_stats:
            print(f"Year {year_stat['_id']}: {year_stat['count']} records")

        # Test data retrieval
        print("\nDetailed Data Analysis:")
        print("=" * 80)
        
        # Department Analysis
        departments = db.courses.distinct('department')
        print(f"\nAnalyzing {len(departments)} departments:")
        
        for dept in departments:
            print(f"\nDepartment: {dept}")
            print("-" * 40)
            
            # Get department statistics
            dept_stats = db.get_department_stats(dept)
            
            # Calculate department averages
            total_a = 0
            total_df = 0
            total_classes = 0
            instructors = defaultdict(int)
            
            for stat in dept_stats:
                total_a += stat['avg_percent_a'] * stat['class_count']
                total_df += stat['avg_percent_df'] * stat['class_count']
                total_classes += stat['class_count']
                instructors[stat['_id']] = stat['class_count']
            
            if total_classes > 0:
                dept_avg_a = total_a / total_classes
                dept_avg_df = total_df / total_classes
                print(f"Department Summary:")
                print(f"Total Classes: {total_classes}")
                print(f"Total Instructors: {len(instructors)}")
                print(f"Department Average A Rate: {dept_avg_a:.1f}%")
                print(f"Department Average D/F Rate: {dept_avg_df:.1f}%")
                
                # Show top 3 instructors by number of classes
                print("\nTop 3 Instructors by Classes Taught:")
                top_instructors = sorted(instructors.items(), key=lambda x: x[1], reverse=True)[:3]
                for instructor, count in top_instructors:
                    print(f"  {instructor}: {count} classes")

        # Sample Course Analysis
        print("\nDetailed Course Analysis:")
        print("=" * 80)
        
        sample_courses = list(db.courses.find().limit(3))
        for course in sample_courses:
            print(f"\nCourse: {course['course_id']}")
            print(f"Department: {course['department']}")
            print(f"Level: {course['level']}")
            
            # Test course statistics retrieval
            stats = db.get_course_stats(course['course_id'])
            print(f"\nStatistics for {course['course_id']}:")
            
            # Calculate year range for this course
            course_years = db.grade_distributions.distinct(
                'year', {'course_id': course['course_id']}
            )
            print(f"Years offered: {min(course_years)} - {max(course_years)}")
            
            for instructor_stat in stats:
                print(f"\n  Instructor: {instructor_stat['_id']}")
                print(f"  Average As: {instructor_stat['avg_percent_a']:.1f}%")
                print(f"  Average DFs: {instructor_stat['avg_percent_df']:.1f}%")
                print(f"  Classes taught: {instructor_stat['class_count']}")

        # Final Summary
        print("\nFinal Database Summary:")
        print("=" * 80)
        print(f"Total Courses: {db.courses.count_documents({})}")
        print(f"Total Grade Distributions: {db.grade_distributions.count_documents({})}")
        print(f"Total Departments: {len(departments)}")
        print(f"Date Range: {min(year_stats, key=lambda x: x['_id'])['_id']} - {max(year_stats, key=lambda x: x['_id'])['_id']}")

        # Restore original stdout
        sys.stdout = original_stdout

if __name__ == "__main__":
    test_database_functionality()