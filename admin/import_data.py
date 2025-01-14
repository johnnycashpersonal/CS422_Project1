# admin/import_data.py

"""
Data Import Module for EasyA Grade Analysis System

This module handles the initial data population and subsequent data updates for the EasyA system.
It processes two main data sources:
1. Grade distribution data from the Daily Emerald (gradedata.js)
2. Faculty information scraped from the 2014-2015 UO Course Catalog

Key responsibilities:
- Parsing and validating input data files
- Converting raw data into appropriate MongoDB document format
- Managing bulk insertions into the database
- Maintaining data consistency across collections
- Supporting the administrator use case for data updates

This module is essential for:
1. Initial system setup with historical grade data (2013-2016)
2. Administrator workflows for updating system data
3. Maintaining consistency between grade data and faculty information
4. Supporting the Natural Sciences department focus
"""

import json
from pymongo import MongoClient

class DataImporter:
    def __init__(self, db_manager):
        """
        Initialize the DataImporter with a database manager.
        
        Args:
            db_manager: Instance of DatabaseManager that provides access to MongoDB collections
        """
        self.db = db_manager

    def import_grade_data(self, json_file_path):
        """
        Import grade distribution data from the provided JSON file.
        
        This method processes the grade data file (gradedata.js) and populates two collections:
        1. courses: Unique course entries with department, number, and level information
        2. grade_distributions: Individual grade distribution records
        
        The method handles:
        - Course ID generation (e.g., "MATH111")
        - Course level calculation (e.g., 100-level from course number 111)
        - Data type conversions (strings to integers where needed)
        
        Args:
            json_file_path: Path to the grade data JSON file
                          (typically converted from gradedata.js)
        
        Note:
            This method uses bulk insert operations for better performance
            when handling large datasets.
        """
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            
        # Process and insert courses
        processed_courses = []
        for grade_entry in data:
            course = {
                'course_id': f"{grade_entry['department']}{grade_entry['number']}",
                'department': grade_entry['department'],
                'number': int(grade_entry['number']),
                'level': (int(grade_entry['number']) // 100) * 100
            }
            processed_courses.append(course)
        
        if processed_courses:
            self.db.courses.insert_many(processed_courses)

        # Process and insert grade distributions
        processed_grades = []
        for grade_entry in data:
            grade_dist = {
                'course_id': f"{grade_entry['department']}{grade_entry['number']}",
                'instructor_name': grade_entry['instructor'],
                'year': grade_entry['year'],
                'term': grade_entry['term'],
                'percent_a': grade_entry['percent_a'],
                'percent_df': grade_entry['percent_df'],
                'total_students': grade_entry['total_students']
            }
            processed_grades.append(grade_dist)
        
        if processed_grades:
            self.db.grade_distributions.insert_many(processed_grades)

    def import_faculty_data(self, json_file_path):
        """
        Import faculty information from the scraped course catalog data.
        
        This method processes the faculty data scraped from the 2014-2015 UO Course Catalog
        and populates the instructors collection. This data is crucial for:
        - Distinguishing between regular faculty and other instructors
        - Supporting the "All Instructors" vs "Regular Faculty" filtering requirement
        - Maintaining accurate department affiliations
        
        Args:
            json_file_path: Path to the JSON file containing scraped faculty data
        
        Note:
            - All imported faculty are marked as regular faculty (is_regular_faculty = True)
            - Faculty can be associated with multiple departments
            - This data is used in conjunction with grade data to support
              the instructor filtering feature
        """
        with open(json_file_path, 'r') as file:
            faculty_data = json.load(file)
            
        processed_faculty = []
        for faculty in faculty_data:
            instructor = {
                'name': faculty['name'],
                'is_regular_faculty': True,
                'departments': faculty['departments']
            }
            processed_faculty.append(instructor)
            
        if processed_faculty:
            self.db.instructors.insert_many(processed_faculty)