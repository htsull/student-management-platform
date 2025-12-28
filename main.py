import streamlit as st
import pandas as pd
from data.database_management import add_grade_to_db, add_student_to_db, check_grade_already_exists, check_student_exists, create_tables, delete_student_from_db, drop_all_data, get_db_connection, join_students_and_grades, update_student_grade_in_db, update_student_infos_in_db
from functions.helpers import (
    is_valid_name,
    run_validations,
)

from functions.grade_analysis import pivot_data


def main():
    """
    Main entry point for the student management platform.

    This function initializes the Streamlit app, loads the student and note data, and displays the main interface.
    It also defines the logic for adding, updating, and deleting students, as well as updating their grades.
    """

    st.title("Student management platform")
    st.write("This platform allows you to manage student information and records.")

    #  init constants
    # students = pd.read_json("data/etudiants.json")
    # notes = pd.read_json("data/notes.json")
    create_tables()
    # def insert_student(name, age):
    #     add_student_to_db(name, age)
    # def insert_grade(student_id, subject, grade):
    #     add_grade_to_db(student_id, subject, grade)
    # insert_student("Alice", 20)
    # insert_student("Bob", 22)
    # insert_student("Charlie", 19)
    # insert_grade(1, "Subject 1", 18.5)
    # insert_grade(1, "Subject 2", 15.0)
    # insert_grade(2, "Subject 1", 12.0)
    # insert_grade(3, "Subject 3", 16.5)
    
    
    students = pd.read_sql("SELECT * FROM students", get_db_connection())
    grades = pd.read_sql("SELECT * FROM grades", get_db_connection())
    data = join_students_and_grades()

    options = [
        "Add Students",
        "Add Students Grades",
        "Update Student Infos",
        "Update Students Grades",
        "Delete Students",
    ]

    # Analyze and display student data
    # data = show_students_details_table(notes, students)

    if len(students) == 0:
        st.info("❌ No student data available. ➕ Try adding some for testing.")
    else:
        st.write(f"Number of students in the database : {len(students)}")
    data = join_students_and_grades()   
    pivoted = pivot_data(data)
    
    st.write(pivoted)



    with st.sidebar:
        st.sidebar.header("Configuration Panel")
        option = st.selectbox("Choose an option", options=options)
        with st.form("Options"):
            if option == "Add Students":
                st.subheader("Add a student informations")
                name = st.text_input(
                    "Name", placeholder="Enter student name...", key="name_input"
                )
                age = st.number_input(
                    "Age",
                    min_value=0,
                    max_value=100,
                    key="age_input",
                    placeholder="Enter student age...",
                )

                submitted = st.form_submit_button("Submit", type="primary")
                if submitted:

                    rules = [
                        (
                            is_valid_name(name),
                            "Invalid name. Please remove extra spaces or use a real name.",
                        ),
                        (age > 0, "Please enter an age greater than 0."),
                    ]

                    if run_validations(rules):
                        #  add the student
                        add_student_to_db(name, age)
                        
                        # rerun the app to refresh the data
                        st.success(f"Student {name} added successfully.")
                        st.rerun()
                        
            elif option == "Add Students Grades":
                st.subheader("Add a student grade for a subject")
                student_id = st.number_input("Student ID", min_value=1)
                subject = st.selectbox("Subject", subjects)
                grade = st.number_input(
                    "Updated Note", min_value=0.0, max_value=100.0, step=0.1
                )
                submitted = st.form_submit_button("Submit", type="primary")

                if submitted:
                    rules = [
                        (
                            check_student_exists(student_id),
                            "This ID does not exist in the database.",
                        ),
                        (
                            not check_grade_already_exists(student_id, subject, get_db_connection()),
                            "This student already has a grade for this subject.",
                        )
                    ]

                    if run_validations(rules=rules):
                        add_grade_to_db(student_id, subject, grade)
                        st.success("Student grade updated successfully.")
                        st.rerun()
                        
            elif option == "Delete Students":
                st.subheader("Delete a student")
                student_id = st.number_input(
                    "Student ID", min_value=1, placeholder="Enter student ID"
                )
                submitted = st.form_submit_button("Submit", type="primary")

                if submitted:
                    current_students = load_students()

                    rule = [
                        (
                           check_student_exists(student_id),
                            "This ID does not exist in the database.",
                        ),
                    ]

                    if run_validations(rule):
                        delete_student_from_db(student_id)
                        st.rerun()
   
            elif option == "Update Student Infos":
                st.subheader("Update a student's informations")

                student_id = st.number_input("Student ID", min_value=1)
                name = st.text_input("Updated Name", key="name", placeholder = "Leave blank to keep current name")
                age = st.number_input("Updated Age", min_value=0, max_value=100, key="age", placeholder = "Leave 0 to keep current age")
                submitted = st.form_submit_button("Submit", type="primary")

                if submitted:
                    rules = [
                        (
                            check_student_exists(student_id),
                            "This ID does not exist in the database.",
                        ),
                    ]

                    if run_validations(rules=rules):
                        update_student_infos_in_db(student_id, name, age)
                        st.rerun()

            elif option == "Update Students Grades":
                st.subheader("Update a student's grade")

                student_id = st.number_input("Student ID", min_value=1)
                subject = st.selectbox("Subject", subjects)
                grade = st.number_input(
                    "Updated Grade", min_value=0.0, max_value=100.0, step=0.1
                )
                submitted = st.form_submit_button("Submit", type="primary")

                if submitted:
                    rules = [
                        (
                            check_student_exists(student_id),
                            "This ID does not exist in the database.",
                        ),
                    ]

                    if run_validations(rules=rules):
                        update_student_grade_in_db(student_id, subject, grade)
                        st.rerun()

          
    drop_data = st.button("Drop all data from the database", type="primary")
    if drop_data:
        drop_all_data()
        st.rerun()

if __name__ == "__main__":
    main()
