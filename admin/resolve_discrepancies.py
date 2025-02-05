from src.data.db_manager import DatabaseManager

class NameStandardizer:
    def __init__(self, faculty_list_path: str):
        """
        Initialize the NameStandardizer with the faculty list.

        Args:
            faculty_list_path: Path to the faculty list file.
        """
        self.faculty_list = self._load_faculty_names(faculty_list_path)
        self.db = DatabaseManager()

    def _load_faculty_names(self, file_path):
        """Load faculty names from the provided text file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        faculty_names = []
        for line in lines:
            if line.strip() and ':' not in line:  # Exclude empty lines and department headers
                faculty_names.append(line.strip())

        return sorted(faculty_names)

    def standardize_faculty_name(self, faculty_name):
        """Standardizes faculty names from the faculty list into (first, middle_init, last)."""
        parts = faculty_name.split()

        if len(parts) == 1:  # Only last name
            return None, None, parts[0]
        elif len(parts) == 2:  # First and last name
            return parts[0], None, parts[1]
        else:  # First, middle, last
            return parts[0], " ".join(parts[1:-1]), parts[-1]

    def standardize_instructor_name(self, instructor_name):
        """Standardizes instructor names from the database into (first, middle_init, last)."""
        if "," not in instructor_name:
            return None, None, instructor_name.strip()

        last_name, rest = instructor_name.split(",", 1)
        last_name = last_name.strip()

        rest_of_names = rest.strip().split()
        first_name = rest_of_names[0]

        middle_init = None
        if len(rest_of_names) > 1 and '.' in rest_of_names[1]:  # Detect middle initial
            middle_init = rest_of_names[1]

        return first_name, middle_init, last_name

    def is_regular_faculty(self, instructor_name):
        """
        Check if an instructor is in the faculty list.

        Args:
            instructor_name: Name in "Last, First Middle" format from the database.

        Returns:
            Boolean - True if instructor is found in the faculty list, otherwise False.
        """
        standardized_instructor = self.format_name_tuple(self.standardize_instructor_name(instructor_name))

        for faculty in self.faculty_list:
            standardized_faculty = self.format_name_tuple(self.standardize_faculty_name(faculty))
            if self.compare_names(standardized_instructor, standardized_faculty):
                return True  # Found in faculty list

        return False  # Not in faculty list

    def format_name_tuple(self, name_tuple):
        """Convert name tuple into a standardized format."""
        if name_tuple == (None, None, None):
            return None  # Ignore names that couldn't be processed

        first, middle, last = name_tuple
        return (first or "", middle or "", last or "")  # Ensures comparison works

    def compare_names(self, name1, name2):
        """
        Compare names while handling middle initials intelligently.

        Returns:
            True if names match based on first, last, and middle initials (if both have one).
        """
        if not name1 or not name2:
            return False

        # If either name has no middle initial, ignore middle initials
        if not name1[1] or not name2[1]:
            return (name1[0], name1[2]) == (name2[0], name2[2])  # Compare first & last names only

        return name1 == name2  # Compare first, middle, and last names

    def update_db_instructors(self):
        """Standardize instructor names and update faculty status in the database."""

        db_names = self.db.grade_distributions.distinct("instructor_name")

        for old_name in db_names:
            standardized_tuple = self.standardize_instructor_name(old_name)  
            new_name = " ".join(filter(None, standardized_tuple))  # Convert tuple to string
            
            is_faculty = self.is_regular_faculty(old_name)  # Check faculty status

            # Rename instructor to match standardized format
            self.db.grade_distributions.update_many(
                {'instructor_name': old_name},
                {'$set': {'instructor_name': new_name}}
            )

            # Update faculty status after renaming
            self.db.grade_distributions.update_many(
                {'instructor_name': new_name},
                {'$set': {'is_regular_faculty': is_faculty}}
            )

            # print(f"Updated {old_name} to {new_name}: is_regular_faculty={is_faculty}")

        print("Database update complete.")

    
    def untuple(self,name_tuple):
        """Converts a tuple of names into a string."""
        return " ".join(filter(None, name_tuple))
    
def main():
    standardizer = NameStandardizer("faculty_list.txt")
    standardizer.update_db_instructors()
    
if __name__ == "__main__":
    main()
