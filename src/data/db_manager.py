"""
Database Manager Module for EasyA Grade Analysis System

This module handles all database operations for the EasyA system. It provides a
centralized interface for:
- Managing MongoDB connections and collections
- Creating and maintaining database indexes for performance optimization
- Executing complex aggregation queries for grade statistics
- Supporting filtering by course, department, and instructor levels

The module uses MongoDB as its primary database and implements various aggregation pipelines
to efficiently process and analyze grade distribution data. It serves as the data access layer
for the entire application, providing clean interfaces for both the admin tools and the main
application to interact with the grade data.

Collections managed:
- courses: Stores course information (department, number, level)
- instructors: Stores instructor information (name, faculty status, departments)
- grade_distributions: Stores individual grade distribution records
"""

from pymongo import MongoClient
from typing import List, Dict, Any, Optional
from src.data.models import Course, Instructor, GradeDistribution

class DatabaseManager:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/"):
        """
        Initialize database connection and collections.
        Creates a new MongoDB client connection and sets up collection references.
        Also ensures all necessary indexes are created for optimal query performance.
        
        Args:
            connection_string: MongoDB connection URL, defaults to localhost
        """
        self.client = MongoClient(connection_string)
        self.db = self.client.easya_db
        
        # Collections
        self.courses = self.db.courses
        self.instructors = self.db.instructors
        self.grade_distributions = self.db.grade_distributions
        
        # Ensure indexes
        self._create_indexes()
    
    def _create_indexes(self):
        """
        Create MongoDB indexes for optimizing query performance.
        Sets up compound indexes on frequently queried fields to improve
        query execution time and efficiency. Includes:
        - Compound index on grade distributions for course and instructor lookups
        - Department and level index for course filtering
        - Name and department index for instructor lookups
        """
        self.grade_distributions.create_index([
            ("course_id", 1),
            ("instructor_name", 1),
            ("year", 1),
            ("term", 1)
        ])
        self.courses.create_index([
            ("department", 1),
            ("level", 1)
        ])
        self.instructors.create_index([
            ("name", 1),
            ("departments", 1)
        ])
    
    def get_course_stats(self, course_id: str) -> Dict[str, Any]:
        """
        Retrieve grade statistics for a specific course.
        Aggregates grade distribution data for all instructors who have taught
        the specified course, calculating average grade percentages and class counts.

        Args:
            course_id: Course identifier (e.g., "MATH111")
            
        Returns:
            List of dictionaries containing aggregated statistics per instructor:
            - instructor name
            - average percentage of As
            - average percentage of Ds and Fs
            - total number of classes taught
        """
        pipeline = [
            {"$match": {"course_id": course_id}},
            {"$group": {
                "_id": "$instructor_name",
                "avg_percent_a": {"$avg": "$percent_a"},
                "avg_percent_df": {"$avg": "$percent_df"},
                "class_count": {"$sum": 1}
            }}
        ]
        return list(self.grade_distributions.aggregate(pipeline))
    
    def get_department_stats(self, department: str, level: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve grade statistics for an entire department, optionally filtered by course level.
        Aggregates grade distributions across all courses in a department, with optional
        filtering by course level (e.g., 100-level, 200-level, etc.).

        Args:
            department: Department code (e.g., "MATH")
            level: Optional course level filter (e.g., 100, 200, etc.)
            
        Returns:
            List of dictionaries containing aggregated statistics per instructor:
            - instructor name
            - average percentage of As
            - average percentage of Ds and Fs
            - total number of classes taught
        """
        match_stage = {"department": department}
        if level:
            match_stage["level"] = level
            
        courses = self.courses.find(match_stage)
        course_ids = [course["course_id"] for course in courses]
        
        pipeline = [
            {"$match": {"course_id": {"$in": course_ids}}},
            {"$group": {
                "_id": "$instructor_name",
                "avg_percent_a": {"$avg": "$percent_a"},
                "avg_percent_df": {"$avg": "$percent_df"},
                "class_count": {"$sum": 1}
            }}
        ]
        return list(self.grade_distributions.aggregate(pipeline))
    
    def get_instructor_stats(self, instructor_name: str) -> Dict[str, Any]:
        """
        Retrieve grade statistics for a specific instructor across all their courses.
        Aggregates all grade distributions for the specified instructor, providing
        average grade percentages and class counts for each course they've taught.

        Args:
            instructor_name: Name of the instructor
            
        Returns:
            List of dictionaries containing aggregated statistics per course:
            - course ID
            - average percentage of As
            - average percentage of Ds and Fs
            - total number of times taught
        """
        pipeline = [
            {"$match": {"instructor_name": instructor_name}},
            {"$group": {
                "_id": "$course_id",
                "avg_percent_a": {"$avg": "$percent_a"},
                "avg_percent_df": {"$avg": "$percent_df"},
                "class_count": {"$sum": 1}
            }}
        ]
        return list(self.grade_distributions.aggregate(pipeline))