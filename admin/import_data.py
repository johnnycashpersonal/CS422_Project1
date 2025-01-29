"""
Data Import Module for EasyA Grade Analysis System
"""

import json
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

    def import_grade_data(self, json_file_path: str) -> None:
        """
        Import grade distribution data from the provided JSON file.
        """
        processed_courses = set()
        processed_grades = []
        skipped_entries = 0
        year_counts = {}
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                # load json from file
                data = json.loads(file.read().split("= ")[1].split(";")[0])
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise ValueError(f"Error reading JSON file: {e}")
        
        for course_id, course_entries in data.items():
            try:
                if not isinstance(course_entries, list) or not course_entries:
                    print(f"Warning: Invalid entries for course {course_id}")
                    skipped_entries += 1
                    continue
                
                for entry in course_entries:
                    # Extract term and year
                    term_desc = entry.get('TERM_DESC', '')
                    term_parts = term_desc.split()
                    # Check if format is correct TODO: are LAW terms supposed to be in here?? ask
                    if len(term_parts) != 2 and len(term_parts) != 3:
                        print(f"Warning: Invalid term format for {course_id}: {term_desc}")
                        skipped_entries += 1
                        continue
                    
                    term, year = term_parts
                    academic_year = int(year)
                    
                    # track year distribution DONT FORGET PLUS 1
                    year_counts[academic_year] = year_counts.get(academic_year, 0) + 1
                    
                    def safe_float(value: str, default: float = 0.0) -> float:
                        try:
                            return float(value) if value and value != 'NA' else default
                        except ValueError:
                            return default
                    
                    # get grade percentages
                    percent_a = safe_float(entry.get('aprec', '0.0'))
                    percent_b = safe_float(entry.get('bprec', '0.0'))
                    percent_c = safe_float(entry.get('cprec', '0.0'))
                    percent_d = safe_float(entry.get('dprec', '0.0'))
                    percent_f = safe_float(entry.get('fprec', '0.0'))
                    
                    # Validate percentages
                    if all(p == 0 for p in [percent_a, percent_b, percent_c, percent_d, percent_f]):
                        print(f"Warning: All percentages zero for {course_id}")
                        skipped_entries += 1
                        continue
                    
                    # Infer department and course number
                    department = ''.join(filter(str.isalpha, course_id))
                    try:
                        course_number = int(''.join(filter(str.isdigit, course_id)))
                    except ValueError:
                        print(f"Warning: Invalid course number for {course_id}")
                        skipped_entries += 1
                        continue
                    
                    # Add course if not already processed
                    if course_id not in processed_courses:
                        processed_courses.add(course_id)
                    
                    # Create grade distribution entry
                    grade_dist = {
                        'course_id': course_id,
                        'instructor_name': entry.get('instructor', '').strip(),
                        'year': academic_year,
                        'term': term,
                        'percent_a': percent_a,
                        'percent_b': percent_b,
                        'percent_c': percent_c,
                        'percent_df': percent_d + percent_f,
                        'crn': entry.get('crn', '')
                    }
                    
                    processed_grades.append(grade_dist)
            
            except Exception as e:
                print(f"Warning: Error processing {course_id}: {str(e)}")
                skipped_entries += 1
        
        print("\nImport Summary:")
        print(f"Total entries processed: {len(processed_grades)}")
        print(f"Entries skipped: {skipped_entries}")
        print(f"Unique courses: {len(processed_courses)}")
        print("\nYear Distribution:")
        for year in sorted(year_counts.keys()):
            print(f"Year {year}: {year_counts[year]} records")
        
        if processed_courses:
            self.db.courses.insert_many(
                [{'course_id': id, 'department': ''.join(filter(str.isalpha, id)), 
                  'number': int(''.join(filter(str.isdigit, id))), 
                  'level': (int(''.join(filter(str.isdigit, id))) // 100) * 100} 
                 for id in processed_courses]
            )
        if processed_grades:
            self.db.grade_distributions.insert_many(processed_grades)