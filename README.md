# School Seating Arrangement Project
Intermediate-level Python project to generate seating plans for classes 6–12 based on exam fixtures.

INSTRUCTIONS FOR CORRECT USAGE:
1. Populate the data folder with the files classes.csv, exam_fixture.csv, rooms.csv
2. classes.csv must contain the columns: CLASS, SECTION, BOYS, GIRLS, TOTAL
3. exam_fixture.csv must contain: DATE, VI, VII, VIII, IX, X, XI, XII (under each class store the exams on that date and say NULL if no exams are to be held for that class on that day)
3. rooms.csv must contain: ROOM NO.
4. After loading these files, run the csv_import.py file to send the data in these csv files to the MySQL database
5. Run the seating_algorithm.py for a specific date to create the alloted_classes table in the database
6. Run the pdf_gen.py to generate the pdf for the fixture in the alloted_classes table
