"""
Data Import Module for EasyA Grade Analysis System

This module handles the initial data population and subsequent data updates for the EasyA system.
It processes two main data sources:
1. Grade distribution data from the Daily Emerald (converted from gradedata.js to CSV)
2. Faculty information scraped from the 2014-2015 UO Course Catalog

Key responsibilities:
- Parsing and validating CSV input data files
- Converting raw data into appropriate MongoDB document format
- Managing bulk insertions into the database
- Maintaining data consistency across collections
- Supporting the administrator use case for data updates
"""

import csv
from typing import List, Dict, Any
from pymongo import MongoClient

class DataImporter:
    def __init__(self, db_manager):
        """
        Initialize the DataImporter with a database manager.
        
        Args:
            db_manager: Instance of DatabaseManager that provides access to MongoDB collections
        """
        self.db = db_manager

    def import_grade_data(self, csv_file_path: str) -> None:
        """
        Import grade distribution data from the provided CSV file.
        
        Maps CSV columns to database fields with robust error handling for:
        - Non-numeric values ('#VALUE!' entries)
        - Invalid course numbers
        - Missing or malformed data
        - Type conversion errors
        - UO quarter system academic year calculation
        """
        required_columns = {
            'TERM', 'TERM_DESC', 'SUBJ', 'NUMB', 'INSTRUCTOR',
            'aprec', 'dprec', 'fprec', 'TOT_NON_W'
        }
        
        processed_courses = set()
        processed_grades = []
        skipped_rows = 0
        year_counts = {}
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            if not reader.fieldnames:
                raise ValueError("CSV file is empty or improperly formatted")
            
            missing_columns = required_columns - set(reader.fieldnames)
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    # Extract and validate year from TERM
                    term = str(row['TERM']).strip()
                    if len(term) != 6:
                        print(f"Warning: Invalid TERM format in row {row_num}: {term}")
                        skipped_rows += 1
                        continue
                    
                    calendar_year = int(term[:4])
                    quarter = int(term[4:])
                    
                    # Adjust year based on UO's quarter system
                    # 01 = Fall (stays in same calendar year)
                    # 02, 03, 04 = Winter, Spring, Summer (belong to next calendar year)
                    academic_year = calendar_year + 1 if quarter in (2, 3, 4) else calendar_year
                    
                    if not (2013 <= academic_year <= 2016):
                        print(f"Warning: Academic year {academic_year} outside expected range in row {row_num}")
                    
                    # Track year distribution
                    year_counts[academic_year] = year_counts.get(academic_year, 0) + 1
                    
                    # Handle course number
                    try:
                        course_number = int(''.join(filter(str.isdigit, row['NUMB'])))
                        if course_number == 0:
                            print(f"Warning: Invalid course number in row {row_num}: {row['NUMB']}")
                            skipped_rows += 1
                            continue
                    except ValueError:
                        print(f"Warning: Non-numeric course number in row {row_num}: {row['NUMB']}")
                        skipped_rows += 1
                        continue
                    
                    # Create course entry
                    course = {
                        'course_id': f"{row['SUBJ']}{course_number}",
                        'department': row['SUBJ'].strip(),
                        'number': course_number,
                        'level': (course_number // 100) * 100
                    }
                    
                    # Handle percentage conversions
                    def safe_float(value: str, default: float = 0.0) -> float:
                        try:
                            if value in ('#VALUE!', '', 'NA', 'N/A'):
                                return default
                            return float(value)
                        except (ValueError, TypeError):
                            return default

                    percent_a = safe_float(row['aprec'])
                    percent_d = safe_float(row['dprec'])
                    percent_f = safe_float(row['fprec'])
                    
                    # Validate percentages
                    if percent_a == 0 and percent_d == 0 and percent_f == 0:
                        print(f"Warning: All percentages zero/invalid in row {row_num}")
                        skipped_rows += 1
                        continue
                    
                    # Add course if not already processed
                    if course['course_id'] not in processed_courses:
                        processed_courses.add(course['course_id'])
                    
                    # Create grade distribution entry
                    grade_dist = {
                        'course_id': course['course_id'],
                        'instructor_name': row['INSTRUCTOR'].strip(),
                        'year': academic_year,
                        'term': row['TERM_DESC'].strip(),
                        'percent_a': percent_a,
                        'percent_df': percent_d + percent_f,
                        'total_students': int(row['TOT_NON_W']) if row['TOT_NON_W'] else 0
                    }
                    
                    processed_grades.append(grade_dist)
                    
                except Exception as e:
                    print(f"Warning: Error in row {row_num}: {str(e)}")
                    skipped_rows += 1
                    continue
        
        # Print detailed import summary
        print("\nImport Summary:")
        print(f"Total rows processed: {len(processed_grades)}")
        print(f"Rows skipped: {skipped_rows}")
        print(f"Unique courses: {len(processed_courses)}")
        print("\nYear Distribution:")
        for year in sorted(year_counts.keys()):
            print(f"Year {year}: {year_counts[year]} records")
        
        # Insert processed data
        if processed_courses:
            self.db.courses.insert_many(
                [{'course_id': id, 'department': id[:-3], 'number': int(id[-3:]), 
                'level': (int(id[-3:]) // 100) * 100} for id in processed_courses]
            )
        if processed_grades:
            self.db.grade_distributions.insert_many(processed_grades)