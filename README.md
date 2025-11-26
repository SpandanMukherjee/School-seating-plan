# School Seating Arrangement Project
Intermediate-level Python project to generate seating plans for classes 6–12 based on exam fixtures.

INSTRUCTIONS FOR CORRECT USAGE:
1. Create a database named "School_seating_plan" using SQL Command Line or Workbench if running for the first     time.
1. Populate the data folder with the files classes.csv, exam_fixture.csv, rooms.csv
2. classes.csv must contain the columns: CLASS, SECTION, BOYS, GIRLS, TOTAL
3. exam_fixture.csv must contain: DATE, VI, VII, VIII, IX, X, XI, XII (under each class store the exams on that date and say NULL if no exams are to be held for that class on that day)
3. rooms.csv must contain: ROOM NO.
4. After loading these files, run the main.py file to run the package.
