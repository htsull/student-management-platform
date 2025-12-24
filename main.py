import streamlit as st
import pandas as pd
from functions.gestion_etudiants import (
    load_students,
    add_student,
    update_student_infos,
)
from functions.gestion_notes import (
    init_student_notes,
    update_student_notes,
    subjects,
)
from functions.helpers import (
    confirm_delete_student_by_id,
    is_valid_name,
    get_next_id,
    student_id_exists,
    run_validations,
)

from functions.analyse_notes import show_students_details_table


def main():
    """
    Main entry point for the student management platform.

    This function initializes the Streamlit app, loads the student and note data, and displays the main interface.
    It also defines the logic for adding, updating, and deleting students, as well as updating their grades.
    """

    st.title("Student management platform")
    st.write("This platform allows you to manage student information and records.")

    #  init constants
    students = pd.read_json("data/etudiants.json")
    notes = pd.read_json("data/notes.json")

    options = [
        "Add Students",
        "Update Student",
        "Update Students Notes",
        "Delete Students",
    ]

    # Analyze and display student data
    data = show_students_details_table(notes, students)

    if data.empty:
        st.info("❌ No students found in the database. ➕ Try adding some for testing.")
    else:
        st.write(f"Number of students in the database : {len(data)}")
        st.dataframe(data.style.format({"Average": "{:.2f}"}), hide_index=True)

    with st.sidebar:
        st.sidebar.header("Configuration Panel")
        option = st.selectbox("Choose an option", options=options)
        with st.form("Options"):
            if option == "Add Students":
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
                    current_students = load_students()

                    rules = [
                        (
                            is_valid_name(name),
                            "Invalid name. Please remove extra spaces or use a real name.",
                        ),
                        (age > 0, "Please enter an age greater than 0."),
                    ]

                    if run_validations(rules):
                        student = {
                            "id": get_next_id(current_students),
                            "name": name,
                            "age": age,
                            # "UUID" : generate_student_id(),
                        }
                        add_student(student)
                        # Initialize notes for the new student
                        init_student_notes(student["id"])
                        st.success(f"Student {name} added successfully.")

                        # rerun the app to refresh the data
                        st.rerun()

            elif option == "Update Student":
                student_id = st.number_input("Student ID", min_value=1)
                name = st.text_input("Update Name")
                age = st.number_input("Update Age", min_value=0, max_value=100)
                submitted = st.form_submit_button("Submit", type="primary")

                if submitted:
                    current_students = load_students()
                    rules = [
                        (
                            is_valid_name(name),
                            "Invalid name. Please remove extra spaces or use a real name.",
                        ),
                        # (age > 0, "Please enter an age greater than 0."),
                        (
                            student_id_exists(student_id, current_students),
                            "This ID does not exist in the database.",
                        ),
                    ]

                    if run_validations(rules=rules):
                        update_student_infos(student_id, name, age)
                        st.rerun()

            elif option == "Delete Students":
                # st.subheader("Delete a student")
                student_id = st.number_input(
                    "Student ID", min_value=1, placeholder="Enter student ID"
                )
                submitted = st.form_submit_button("Submit", type="primary")

                if submitted:
                    current_students = load_students()

                    rule = [
                        (
                            student_id_exists(student_id, current_students),
                            "This ID does not exist in the database.",
                        ),
                    ]

                    if run_validations(rule):
                        confirm_delete_student_by_id(student_id)

            elif option == "Update Students Notes":
                student_id = st.number_input("Student ID", min_value=1)
                subject = st.selectbox("Subject", subjects)
                note = st.number_input(
                    "Updated Note", min_value=0.0, max_value=100.0, step=0.1
                )
                submitted = st.form_submit_button("Submit", type="primary")

                if submitted:
                    current_students = load_students()
                    rules = [
                        (
                            student_id_exists(student_id, current_students),
                            "This ID does not exist in the database.",
                        ),
                    ]

                    if run_validations(rules=rules):
                        update_student_notes(student_id, subject, note)
                        st.rerun()


if __name__ == "__main__":
    main()
