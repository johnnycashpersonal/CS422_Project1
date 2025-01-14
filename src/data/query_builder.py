# query_builder.py

"""
Query Builder Module for EasyA Grade Analysis System

This module is responsible for constructing complex MongoDB aggregation pipelines
that power the visualization and analysis features of the EasyA system. As part of
the data management layer, it works in conjunction with DatabaseManager to provide
structured data access patterns that support all required view types specified in
the project requirements.

Key Features:
- Builds aggregation pipelines for different view types (course, department, level)
- Supports filtering between regular faculty and all instructors
- Handles metric switching between "Easy A" (percent As) and "Just Pass" (percent Ds/Fs)
- Provides sorted results for optimal visualization presentation
- Calculates class counts for each data point

This module is crucial for:
1. Supporting side-by-side comparisons of instructors within same courses
2. Enabling department-wide analysis across course levels
3. Facilitating comparison between regular faculty and all instructors
4. Supporting all graphing requirements specified in project documentation

Dependencies:
- DatabaseManager for executing the constructed queries
- MongoDB for query execution
"""

from typing import List, Dict, Any, Optional
from .db_manager import DatabaseManager

class QueryBuilder:
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize QueryBuilder with a database manager instance.
        
        Args:
            db_manager: DatabaseManager instance for executing queries
        """
        self.db = db_manager
    
    def build_comparison_query(
        self,
        department: str,
        course_number: Optional[int] = None,
        level: Optional[int] = None,
        instructors_only: bool = False,
        metric: str = "percent_a"  # or "percent_df"
    ) -> List[Dict[str, Any]]:
        """
        Build a query for comparing grade distributions across instructors.
        This is the primary query builder that supports the main visualization
        requirements, including:
        - Single class comparisons (e.g., all instructors teaching MATH 111)
        - Department-wide comparisons (e.g., all MATH instructors)
        - Level-specific comparisons (e.g., all 100-level MATH courses)
        
        Args:
            department: Department code (e.g., "MATH")
            course_number: Optional specific course number (e.g., 111)
            level: Optional course level for filtering (e.g., 100)
            instructors_only: If True, only include regular faculty
            metric: Which metric to compare ("percent_a" or "percent_df")
        
        Returns:
            List of dictionaries containing:
            - _id: instructor name
            - average: average percentage for specified metric
            - class_count: number of classes taught
            
        Note:
            Results are sorted by the specified metric in descending order to
            support the visualization requirement of ordering bars from highest
            to lowest.
        """
        # Base pipeline stages
        pipeline = []
        
        # Match stage for courses
        match_stage = {"department": department}
        if course_number:
            match_stage["number"] = course_number
        elif level:
            match_stage["level"] = level
        
        # Get relevant courses
        courses = self.db.courses.find(match_stage)
        course_ids = [course["course_id"] for course in courses]
        
        # Add course filter to pipeline
        pipeline.append({"$match": {"course_id": {"$in": course_ids}}})
        
        # Add instructor filter if needed
        if instructors_only:
            regular_faculty = self.db.instructors.find(
                {"is_regular_faculty": True},
                {"name": 1}
            )
            faculty_names = [f["name"] for f in regular_faculty]
            pipeline.append({"$match": {"instructor_name": {"$in": faculty_names}}})
        
        # Group by instructor and calculate statistics
        pipeline.append({
            "$group": {
                "_id": "$instructor_name",
                "average": {"$avg": f"${metric}"},
                "class_count": {"$sum": 1}
            }
        })
        
        # Sort by the metric
        pipeline.append({"$sort": {"average": -1}})
        
        return list(self.db.grade_distributions.aggregate(pipeline))

    def build_level_comparison_query(
        self,
        department: str,
        level: int,
        metric: str = "percent_a"
    ) -> List[Dict[str, Any]]:
        """
        Build a query for comparing different courses within the same level.
        This query supports the requirement to show grade distributions across
        different courses at the same level (e.g., all 400-level MATH courses),
        which helps students choose electives within a department.
        
        Args:
            department: Department code (e.g., "MATH")
            level: Course level to compare (e.g., 400 for 400-level courses)
            metric: Which metric to compare ("percent_a" or "percent_df")
        
        Returns:
            List of dictionaries containing:
            - _id: course ID
            - average: average percentage for specified metric
            - class_count: number of times course was taught
            
        Note:
            Results are sorted by average in descending order to support
            the visualization requirement of showing highest to lowest
            grade distributions.
        """
        pipeline = [
            # Match courses at the specified level
            {"$match": {
                "department": department,
                "level": level
            }},
            # Group by course
            {"$group": {
                "_id": "$course_id",
                "average": {"$avg": f"${metric}"},
                "class_count": {"$sum": 1}
            }},
            # Sort by average
            {"$sort": {"average": -1}}
        ]
        
        return list(self.db.grade_distributions.aggregate(pipeline))