# from uuid import uuid4
import streamlit as st

from functions.gestion_etudiants import delete_student, load_students
from functions.gestion_notes import delete_student_notes


# checking if a name exists in a list of students
def name_exists(name: str, students: list):
    return any(s["name"].lower() == name.lower() for s in students)


# checking if the user input a valid name
def is_valid_name(name):
    cleaned = name.strip()
    return len(cleaned) >= 2 and cleaned.replace(" ", "").isalpha()


# get the next available ID
def get_next_id(students: list):
    if not students:
        return 1
    return max(student["id"] for student in students) + 1


# TODO: implement UUID generation
# def generate_student_id() -> str:
#     return str(uuid4())


# check if student ID exists in the list
def student_id_exists(student_id: int, students: list):
    return any(s["id"] == student_id for s in students)


def run_validations(rules: list[tuple[bool, str]]) -> bool:
    """Run a series of validation rules.
    Returns True if all rules pass, False otherwise.
    """
    for condition, error_message in rules:
        if not condition:
            st.error(error_message)
            return False
    return True


@st.dialog("Are you sure?", width="small")
def confirm_delete_student_by_id(student_id: int):
    st.write(f"Are you sure you want to delete student with ID {student_id}?")
    st.write("This action cannot be undone.")
    col1, col2, col3 = st.columns((2, 8, 2))
    with col1:
        if st.button("Yes"):
            # Call the delete function here
            delete_student(student_id)
            delete_student_notes(student_id)

            # Reload the list after deletion
            updated_students = load_students()

            if not updated_students:
                st.info("All students have been deleted from the database.")

            st.rerun()

    with col2:
        if st.button("No"):
            st.rerun()
