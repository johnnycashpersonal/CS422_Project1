# Software Requirements Specification (SRS)

## 1. Problem Statement
Students face difficulty in selecting the best instructor for their courses based on past grading trends. Similarly, system administrators need an efficient way to update and manage grading data. This system provides a graphical interface that allows students to compare instructors' grading distributions while also enabling administrators to update the database seamlessly.

## 2. Description of Users

### **User Classes**
1. **Students**
   - Want to compare instructor grading distributions to make informed decisions.
   - Expect a simple and intuitive interface.
   - Have prior experience using academic platforms and graphical interfaces.
   - Regularly interact with online course selection tools.
   
2. **System Administrators**
   - Manage and update grading data within the system.
   - Require data import tools, scraping utilities, and discrepancy resolution features.
   - Have experience with database management and command-line utilities.

## 3. Scenarios / Use Cases

### **Scenario 1: Student Comparing Instructors**
A student wants to take Math 111 this semester and is choosing between multiple instructors. They use the system to view past grade distributions and find an instructor with a higher percentage of A grades.

### **Scenario 2: System Administrator Updating Data**
A system administrator receives new grading data for the semester. They use the admin tools to import data from a JSON file, scrape faculty names, and resolve discrepancies before making the updated data available to students.

### **Scenario 3: Comparing Different Course Levels**
A student is unsure whether to take a 300-level or 400-level Math course. They use the system to compare grade distributions across all Math 300-level and 400-level courses to make a decision.

## 4. Detailed Description of Requirements

### **Functional Requirements**
#### **Absolutely Required**
1. The system must allow students to compare instructors based on past grading data.
2. The system must provide an interactive graph visualization.
3. The system must allow filtering by course, department, or level.
4. The system must allow toggling between "Percentage of A grades" and "Percentage of D/F grades."
5. The system must allow toggling between all instructors or only regular faculty.
6. The system must allow sorting of grading distribution graphs.
7. The system must enable system administrators to import new grading data.
8. The system must allow system administrators to scrape faculty names.
9. The system must provide tools to resolve name discrepancies in faculty data.
10. The system must support data import from JSON or JS file formats.
11. The system must allow updating faculty records using the wayback machine.
12. The system must execute data updates in under 5 minutes.
13. The system must ensure data consistency in grading records.
14. The system must store instructor and course data in a structured MongoDB database.
15. The system must provide a user interface for administrative tasks.
16. The system must prevent redundant data entries.

#### **Not Absolutely Required**
17. The system should provide an export function to save comparison results.
18. The system should allow a detailed instructor profile view with grading trends over multiple years.
19. The system should support user authentication for personalized settings.
20. The system should include a mobile-responsive interface.

### **Non-Functional Requirements**
#### **Absolutely Required**
1. The system must load and display instructor comparison graphs within 2 seconds.
2. The system must handle at least 10,000 course records efficiently.
3. The system must be compatible with MacOS and Python 3+.
4. The system must use a secure and optimized MongoDB database for storage.
5. The system must have a user-friendly graphical interface using Tkinter.
6. The system must be installable using a single script (`install.sh`).

#### **Not Absolutely Required**
7. The system should be accessible via a web-based interface.
8. The system should support additional data visualization styles.
9. The system should allow students to leave instructor reviews.
10. The system should have multilingual support.

## 5. Reflection on Implementation

### **Changes from Initial Requirements**
- Initial requirements called for a faculty profile page, which was deferred due to time constraints.
- Originally planned web interface was replaced with a Tkinter-based GUI for faster development.
- Scraping faculty data from external sources was simplified to a single-click admin action.

### **Deferred Features and Rationale**
1. **Instructor Profile View** – Not implemented due to UI complexity; planned for future updates.
2. **User Authentication** – Deemed unnecessary for initial deployment.
3. **Web-Based Interface** – Chosen to focus on Tkinter implementation first.

## 6. Technical Specification

### **System Components and Interaction**

- **Frontend (Tkinter GUI)**
  - Displays visualizations of grade distributions.
  - Handles user input for filtering and sorting.
  
- **Backend (Database and Query Processing)**
  - Stores and retrieves grading data from MongoDB.
  - Uses Python scripts for query processing.

- **Admin Tools**
  - Scripts for importing and updating data.
  - Discrepancy resolution mechanisms.

### **Traceability Matrix**

| Requirement | Implemented Feature | Status |
|-------------|-------------------|--------|
| Compare Instructors | Graph Visualizations | ✅ Implemented |
| Filter by Course & Department | Filter Options | ✅ Implemented |
| Scrape Faculty Data | Admin Tool | ✅ Implemented |
| Instructor Profile View | Future Feature | ❌ Deferred |
| Web-Based Interface | Tkinter GUI | ❌ Deferred |

## 7. Conclusion
This document provides a comprehensive specification of the grading comparison system. It defines the user requirements, technical specifications, and outlines what has been built, deferred, or excluded. Future developers can use this document as a reference for system maintenance and expansion.
