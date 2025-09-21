import mysql.connector
import getpass

try:
    password = getpass.getpass("Enter password: ")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="School_seating_plan"
    )

    cursor = conn.cursor()

    if conn.is_connected():
        print("Successfully connected to the database")

    cursor.execute("""
                
        CREATE TABLE IF NOT EXISTS extra_classes(
            class VARCHAR(5) NOT NULL,
            section VARCHAR(5) NOT NULL,
            boys INT,
            girls INT,
            total INT NOT NULL,
            PRIMARY KEY (class, section)
        );
                
    """)

    def pair_6_and_9(cursor):
        def get_strength(item):
            return item[4]

        cursor.execute("SELECT * FROM classes WHERE class = 'VI'")
        sections_6 = sorted(cursor.fetchall(), key=get_strength, reverse=True)

        cursor.execute("SELECT * FROM classes WHERE class = 'IX'")
        sections_9 = sorted(cursor.fetchall(), key=get_strength)

        len6, len9 = len(sections_6), len(sections_9)
        min_len = min(len6, len9)

        extra_sections = []
        if len6 > len9:
            extra_sections = sections_6[min_len:]
            sections_6 = sections_6[:min_len]
        elif len9 > len6:
            extra_sections = sections_9[min_len:]
            sections_9 = sections_9[:min_len]

        for row in extra_sections:
            cursor.execute("INSERT INTO extra_classes VALUES (%s, %s, %s, %s, %s)", row)

        pairs = []
        for s6, s9 in zip(sections_6, sections_9):
            _, sec6, _, _, total6 = s6
            _, sec9, _, _, total9 = s9
            pairs.append((sec6, total6, sec9, total9, total6 + total9))

        return pairs

    print(pair_6_and_9(cursor))

    conn.commit()
    cursor.close()
    conn.close()
    print("Successful completion of all required tasks")

except Exception as e:
    print("Error while connecting to database:", e)
