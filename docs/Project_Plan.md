# Project Plan (10 Points)

## Project Planning and Execution
Our team followed a structured project plan with clear task assignments, regular progress tracking, and flexibility to handle challenges. Key components of our planning process included:
- Clearly defining roles and responsibilities  
- Holding **Scrum meetings twice weekly (Mondays & Wednesdays at 3:30 PM)**  
- Maintaining detailed records of completed work, pending tasks, and encountered issues  

## Team Organization

| **Team Member** | **Role & Responsibilities** |
|---------------|--------------------------|
| **John** | Backend Developer - Managed data processing, database architecture, and query optimization |
| **Manu** | Frontend Developer - Designed the GUI using Tkinter and integrated data visualizations |
| **Tim** | Admin Features - Developed backend tools for system administrators and advanced processing |
| **Myles** | Faculty Features - Created faculty-related features, filtering, and comparative data views |

## Decision-Making and Communication
- **Decisions** were made collaboratively during weekly meetings, with urgent matters handled in a shared group chat.  
- **Meetings**: Held twice weekly (Mondays & Wednesdays at 3:30 PM) to review progress and adjust plans.  
- **GitHub**: Used for version control, code reviews, and task tracking.  

## Task Assignments and Contributions

| **Team Member** | **Role & Responsibilities** | **Assigned Date** | **Completion Date** | **Time Spent** | **Files Worked On (Time Spent & Completion Date)** |
|---------------|--------------------------|----------------|----------------|---------------|----------------|
| **John** | Backend development - Database, queries, and data handling | Jan 13, 2025 | Feb 4, 2025 | **14.5 hours** | `update_db.py` (1.5 hrs, Finished Jan 22), `db_manager.py` (2 hrs, Finished Jan 22), `models.py` (2 hrs, Finished Jan 22), `query_builder.py` (3 hrs, Finished Jan 22), Filesystem setup (0.5 hrs, Finished Jan 22), `main_window.py` (4 hrs, Finished Feb 4) |
| **Tim** | Admin tools, resolving data discrepancies, and GUI fixes | Jan 13, 2025 | Feb 4, 2025 | **8.5 hours** | `scrape_faculty.py` (2 hrs, Finished Feb 4), `resolve_discrepancies.py` (4 hrs, Finished Feb 4), `update_db.py` (30 min, Finished Feb 4), `main_window.py` (2 hrs, Finished Feb 4) |
| **Manu** | Frontend development - GUI design, graphs, data formatting | Feb 13, 2025 | Feb 4, 2025 | **15.5 hours** | `main_window.py` (13 hrs, Finished Feb 4), `update_db.py` (1.5 hrs, Finished Jan 22), `db_manager.py` (0.5 hrs, Finished Jan 22), `models.py` (0.5 hrs, Finished Jan 22) |
| **Myles** | Data structuring, admin setup, and testing | Jan 20 | Feb 4, 2025 | **9.25 hours** | `import_data.py` (4 hrs, Finished Jan 30), `admin/main.py` (3 hrs, Finished Feb 3), `install.sh` (1 hr, Finished Feb 4), `requirements.txt` (15 min, Finished Feb 3), `admin/tests.py` (1 hr, Finished Feb 4) |

## Project Milestones and Adaptability

### 1. Initial Setup (Week 2: Jan 13 - Jan 20)
- **Database Design:** Schema defined (`models.py`)
- **Query System:** Initial implementation (`query_builder.py`)
- **Filesystem Setup:** Configured storage structure

### 2. Foundation Development (Week 3: Jan 21 - Jan 22)
- **Data Handling:** MongoDB import and structure (`import_data.py`)
- **Admin Tools:** Implemented data scraping system (`scrape_faculty.py`)
- **Query Optimization:** Improved database retrieval (`db_manager.py`, `update_db.py`)
- **Database & Query System Completed (Jan 22)**

### 3. Integration & Debugging (Week 4 - Week 5)
- **Connected Backend & Frontend:** Data integration across modules
- **Testing & Refinement:** Debugging and fixing inconsistencies
- **Faculty Features:** Data visualization and comparisons implemented

### 4. GUI & Admin Development (Week 5: Feb 2 - Feb 9)
- **Tkinter UI Designed:** Implemented layout and interactive elements (`main_window.py`)
- **Graph Formatting:** Ensured proper rendering and user experience
- **Admin Features Built:** Developed admin scripts (`admin/main.py`, `install.sh`, `requirements.txt`)

### 5. Testing & Optimization (Week 6: Feb 4 - Feb 9)
- **Admin Testing:** Verified admin scripts functionality (`admin/tests.py`)
- **Debugging & Code Review:** Final fixes and optimizations
- **Performance Improvements:** Optimized queries for efficiency
- **Final Deliverables Prepared:** Documentation and submission

## Risk Assessment and Mitigation

| **Risk** | **Mitigation Strategy** |
|---------|----------------------|
| **Data retrieval issues** | Refined query handling in `query_builder.py` |
| **Integration conflicts** | Ensured clear function documentation in `db_manager.py` |
| **Scraping inconsistencies** | Improved error handling in `scrape_faculty.py` |
| **Performance bottlenecks** | Optimized queries and indexing in MongoDB |

## Tracking Progress
- **GitHub**: Used for task tracking, pull requests, and version control  
- **Weekly Scrums**: Progress reports documented on Mondays & Wednesdays  
- **Documentation**: Each member recorded work in code comments and logs  

By maintaining detailed documentation and adapting our plan as needed, we successfully built a robust, well-organized system.
