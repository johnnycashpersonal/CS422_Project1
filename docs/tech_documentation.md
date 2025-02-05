## Installation

*Prerequisites*
- MacOS
- Python 3+
- Homebrew

1. Make the install.sh script runnable using sudo chmod +x install.sh in the project folder
2. Make the run.sh script runnable using sudo chmod +x run.sh in the project folder
3. Run the install.sh script with ./install.sh
4. The user window and admin window will open, but can be opened again with ./run.sh
5. To update data in admin console
- In the admin view, click "Select Data" and choose a .js or .json file
6. To scrape faculty names
- In the admin view, click "Scrape for faculty" and then "Resolve Discrepancies" once it completes

## Requirements
The program uses the following python dependencies
- pymongo: 4.11
- matplotlib: 3.10.0
- beautifulsoup4: 4.13.3
- requests: 2.32.3

## Source Code Files

**/Admin**

*import_data.js*
- Creates class DataImporter with method import_grade_data that recieves a file path to a json file or js file containing a json object and logs it in the mongodb database using the db_manager.py module in /data

*main.py*
- Creates a window for the admininstrator view with tkinter and calls scrape_faculty.py, db_manager.py, import_data.py, and resolve_discrepancies.py
resolve_discrepancies.py
- Provides a NameStandardizer class
- Takes data created by scrape_faculty.py and resolves it to match the database
- Matches names with the database and marks them for use by the user window

*scrapefaculty.py*
- Provides the WebScraper class
- Scrapes the arts and sciences faculty webpage and provides a list of names in txt form

*update_db.py*
- Provides the DatabaseUpdater class that has helper functions for database management

**/src/data**

*db_manager.py*
- Provides the DatabaseManger class
- Creates an instance of a mongodb database and provides functions to other modules to read and write to it

*models.py*
- Contains classes Course, Instructor, GradeDistribution
- Defines classes to simplify importing data into a form readable to a database

*querybuilder.py*
- Provides the QueryBuilder class
- Helps with database queries for comparisons in the build_leve_comparion_query and build_comparion_query methods
**/src/gui**

*main_window.py*
- Uses tkinter to create a user window managing all aspects of the user view
- Uses the DatabaseManager class from db_manager.py to create queries specified by the user
- Uses return data from queries to construct matplotlib charts displaying it in easy to read views
