import sqlite3
import pandas as pd
  
# creating and connecting to the database
def get_db_connection():
    conn = sqlite3.connect("data/platform.db")
    conn.row_factory = sqlite3.Row
    return conn

#  create tables if they do not exist
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)

    # Create grades table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY,
            student_id INTEGER,
            subject TEXT NOT NULL,
            grade REAL NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    

def add_student_to_db(name: str, age: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

def add_grade_to_db(student_id: int, subject: str, grade: float):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)", (student_id, subject, grade))
    conn.commit()
    conn.close()
    
def check_student_exists(student_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM students WHERE id = ?", (student_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def check_grade_already_exists(student_id: int, subject: str, conn: sqlite3.Connection) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM grades WHERE student_id = ? AND subject = ?", (student_id, subject))
    exists = cursor.fetchone() is not None
    return exists

def delete_student_from_db(student_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete the student from the students table
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))

    # Delete the grades for the student from the grades table
    cursor.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))

    conn.commit()
    conn.close()
    
def update_student_infos_in_db(student_id: int, name: str = None, age: int = None):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Build the update query dynamically based on provided fields

    if name is not None and name != "":
        cursor.execute("UPDATE students SET name = ? WHERE id = ?", (name, student_id))
    if age is not None and age > 0:
        cursor.execute("UPDATE students SET age = ? WHERE id = ?", (age, student_id))

    conn.commit()
    conn.close()
    
def update_student_grade_in_db(student_id: int, subject: str, grade: float):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Only proceed if grade is valid
    if grade is None or grade == "":
        conn.close()
        return

    # Check if a row already exists
    cursor.execute(
        "SELECT 1 FROM grades WHERE student_id = ? AND subject = ?",
        (student_id, subject)
    )
    exists = cursor.fetchone() is not None

    if exists:
        # Update existing grade
        cursor.execute(
            "UPDATE grades SET grade = ? WHERE student_id = ? AND subject = ?",
            (grade, student_id, subject)
        )
    else:
        # Insert new grade row
        cursor.execute(
            "INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)",
            (student_id, subject, grade)
        )

    conn.commit()
    conn.close()

    


def join_students_and_grades() -> pd.DataFrame:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id AS student_id, s.name, s.age, g.subject, g.grade
        FROM students s
        LEFT JOIN grades g ON s.id = g.student_id
    """)
    results = cursor.fetchall()
    conn.close()

    # Turn the list of tuples into a DataFrame
    df = pd.DataFrame(results, columns=["student_id", "name", "age", "subject", "grade"])
    return df

    
    
def drop_all_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS grades")
    cursor.execute("DROP TABLE IF EXISTS students")
    conn.commit()
    conn.close()
    
    
    
# def insert_student(name: str, age: int):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
#     conn.commit()
#     conn.close()
    

# def insert_grade(student_id: int, subject: str, grade: float):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)", (student_id, subject, grade))
#     conn.commit()
#     conn.close()
    
# def fetch_all_students():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM students")
#     students = cursor.fetchall()
#     conn.close()
#     return students