# admin/update_db.py

"""
Database Update Module for EasyA Grade Analysis System

This module manages database maintenance and updates for the EasyA system,
specifically handling:
1. Database cleanup operations
2. Faculty status updates
3. Name matching between grade data and faculty records

Key responsibilities:
- Providing clean data reload capability
- Managing instructor status updates
- Resolving naming discrepancies between data sources
- Supporting administrator workflows for data maintenance

This module is crucial for:
1. Supporting the administrator use case for system data updates
2. Maintaining data consistency across different data sources
3. Ensuring accurate faculty status tracking
4. Facilitating clean data reloads when new data is available
"""

class DatabaseUpdater:
    def __init__(self, db_manager):
        """
        Initialize DatabaseUpdater with a database manager instance.
        
        Args:
            db_manager: Instance of DatabaseManager for collection access
        """
        self.db = db_manager

    def clean_collections(self):
        """
        Remove all existing data from the database.
        
        This method provides a clean slate for data reloads by removing
        all documents from all collections. This supports the requirement
        that new data should overwrite old data completely rather than
        being merged.
        
        It cleans:
        - courses collection
        - instructors collection
        - grade_distributions collection
        """
        self.db.courses.delete_many({})
        self.db.instructors.delete_many({})
        self.db.grade_distributions.delete_many({})

    def update_instructor_status(self, instructor_name, is_regular=True):
        """
        Update an instructor's regular faculty status.
        
        This method supports the "All Instructors" vs "Regular Faculty"
        filtering requirement by allowing status updates for individual
        instructors.
        
        Args:
            instructor_name: Name of the instructor to update
            is_regular: Boolean indicating if instructor is regular faculty
                      (defaults to True)
        """
        self.db.grade_distributions.update_many(
            {'instructor_name': instructor_name},   # Match existing instructor names
            {'$set': {'is_regular_faculty': is_regular}},   # Add/Update the field
            upsert=False   # Do NOT create new entries, just update existing ones
        )


    def match_instructor_names(self, grade_data_names, faculty_names):
        """
        Match instructor names between grade data and faculty data.
        
        This method handles the requirement to resolve discrepancies between
        names found in gradedata.js and the scraped faculty data. It implements
        a flexible matching system that can handle minor variations in name format.
        
        Args:
            grade_data_names: List of instructor names from grade data
            faculty_names: List of instructor names from faculty data
            
        Returns:
            Tuple containing:
            - matches: List of (grade_name, faculty_name) pairs that match
            - unmatched: List of grade_data_names that didn't find a match
            
        This supports the administrative requirement to ensure data consistency
        and provide statistics about name matching results.
        """
        matches = []
        unmatched = []
        
        for grade_name in grade_data_names:
            found = False
            for faculty_name in faculty_names:
                if self._names_match(grade_name, faculty_name):
                    matches.append((grade_name, faculty_name))
                    found = True
                    break
            if not found:
                unmatched.append(grade_name)
                
        return matches, unmatched

    def _names_match(self, name1, name2):
        """
        Helper function to determine if two name variants match.
        
        This internal method implements the name matching logic used to
        resolve discrepancies between different data sources. It uses
        a simple but flexible matching approach that can be enhanced
        for more sophisticated matching if needed.
        
        Args:
            name1: First name to compare
            name2: Second name to compare
            
        Returns:
            Boolean indicating whether names are considered a match
            
        Note:
            Current implementation uses case-insensitive substring matching,
            which can be enhanced with more sophisticated algorithms
            (e.g., Levenshtein distance) if needed.
        """
        name1 = name1.lower().strip()
        name2 = name2.lower().strip()
        return name1 == name2 or name1 in name2 or name2 in name1