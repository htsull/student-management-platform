# from uuid import uuid4
import streamlit as st

from data.database_management import delete_student_from_db

# checking if the user input a valid name
def is_valid_name(name):
    cleaned = name.strip()
    return len(cleaned) >= 2 and cleaned.replace(" ", "").isalpha()

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
    """
    Displays a confirmation dialog box asking the user to confirm deletion of a student with the given ID.

    If the user clicks "Yes", the student is deleted and the list is reloaded. If the user clicks "No", the dialog is dismissed.

    :param student_id: The ID of the student to be deleted
    :return: None
    """
    st.write(f"Are you sure you want to delete student with ID {student_id}?")
    st.write("This action cannot be undone.")
    col1, col2, col3 = st.columns((2, 8, 2))
    with col1:
        if st.button("Yes"):
            # Call the delete function here
            delete_student_from_db(student_id)

            st.rerun()

    with col2:
        if st.button("No"):
            st.rerun()
            
            
# database connection helper
