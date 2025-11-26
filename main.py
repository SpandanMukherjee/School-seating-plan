from src import seating_algorithm, csv_import, pdf_gen
import mysql.connector
import getpass

password = getpass.getpass("Enter password: ")

def main(password):

    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = password,
            database = "School_seating_plan"
        )

        cursor = conn.cursor()

        if conn.is_connected():
            print("Successfully connected to the database")

        csv_import.csv_import(cursor, conn)
        seating_algorithm.seating_algorithm(cursor, conn)
        cursor.close()
        conn.close()
        pdf_gen.pdf_gen()

    except Exception as e:
        print("Error: ", e)

if __name__ == "__main__":
    main(password)