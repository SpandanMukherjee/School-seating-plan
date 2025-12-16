def csv_import(cursor, conn):
    import csv

    try:
       
        cursor.execute("""
                    
            CREATE TABLE IF NOT EXISTS classes(
                class VARCHAR(5) NOT NULL,
                section VARCHAR(5) NOT NULL,
                boys INT,
                girls INT,
                total INT NOT NULL,
                PRIMARY KEY (class, section)
            );
                    
        """)

        cursor.execute("""
                    
            CREATE TABLE IF NOT EXISTS exam_fixture(
                exam_date DATE PRIMARY KEY,
                VI VARCHAR(100),
                VII VARCHAR(100),
                VIII VARCHAR(100),
                IX VARCHAR(100),
                X VARCHAR(100),
                XI VARCHAR(100),
                XII VARCHAR(100)
            );
                    
        """)

        cursor.execute("""
                    
            CREATE TABLE IF NOT EXISTS rooms(
                room_no VARCHAR(20) PRIMARY KEY
            );
                    
        """)

        def import_csv_to_table(filename, table_name, columns):
            cursor.execute(f"TRUNCATE TABLE {table_name}")

            with open(filename, "r") as file:
                reader = csv.reader(file)
                next(reader)

                for row in reader:
                    placeholders = ', '.join(['%s'] * len(columns))
                    sql = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
                    cursor.execute(sql, row)

        import_csv_to_table("data/classes.csv", "classes", ["class", "section", "boys", "girls", "total"])
        import_csv_to_table("data/exam_fixture.csv", "exam_fixture", ["exam_date", "VI", "VII", "VIII", "IX", "X", "XI", "XII"])
        import_csv_to_table("data/rooms.csv", "rooms", ["room_no"])
        conn.commit()
        print("Data imported successfully")

    except Exception as e:
        print("Error while connecting to the database:", e)
