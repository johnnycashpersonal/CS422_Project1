# Project 1 ReadMe

## Requirements

**User Classes** 

- (1) A student using the system to select a class or instructor.
- (2) A system administrator installing the system, or updating it with new data.

**Use Cases**

- (1) A student needs to take Math 111 this term, and there are many different faculty teaching the
class. The student wants to know which instructors are most likely to give As, and which are
most likely to give Ds and Fs. The student uses the system to compare the grading history of
the instructors teaching this term, side-by-side.

- (2) A system administrator acquires new data for the system, and updates the system with the
new data.

# Functional Requirements

## Data Views

1. **Single Graph Instructor Comparisons**
   - Single class (e.g., Math 111)
   - Single department (e.g., Math)
   - All classes of a level within department (e.g., Math 100-level)

2. **Class Level Comparisons**
   - Display all classes within a level (e.g., all Math 400-level courses)

3. **Instructor Type Toggle**
   - All instructors (default)
   - Regular Faculty only (from 2014-2015 UO Course Catalog)

4. **Grade Display Options**
   - Percent As (default)
   - Percent Ds or Fs

5. **Class Count Display**
   - Option to show number of classes taught per instructor

## Visualization Features

1. **Side-by-Side Viewing**
   - Compare graphs (e.g., Math 400-level vs CS 400-level)

2. **Graph Formatting**
   - Narrow, clearly visible bars
   - Easy-to-compare visualization
   - Ordered bars (highest to lowest or vice versa)

## System Administration

1. **Data Replacement**
   - Quick data update (< 5 minutes)
   - Support for gradedata.js or CSV format
   - Faculty name scraper for wayback machine
   - Name discrepancy resolution tools
   - Command-line admin tools
   - Complete data overwrite capability

## Initial System

- The system that is delivered should not require any administrator steps to convert or prepare data
for the system other than (optionally) setting up a database (if your system uses a database). 
- But, for example, there should not be any web scraping or data conversion required for the initial use
of the system.
