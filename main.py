import streamlit as st
import pandas as pd
from functions.gestion_etudiants import delete_student, load_students, add_student, update_student_infos
from functions.gestion_notes import load_notes, init_student_notes, delete_student_notes, update_student_notes, subjects
from functions.helpers import name_exists, is_valid_name, get_next_id, student_id_exists

from functions.analyse_notes import show_students_details_table






def main():
    
    st.title("Student management platform")
    st.write("This platform allows you to manage student information and records.")
    students = pd.read_json("data/etudiants.json")
    notes = pd.read_json("data/notes.json")
    
    # st.write(students_list)
    # st.write(notes_list)
    
    data = show_students_details_table(notes, students)
    
    if data.empty:
        st.info("❌ No students found in the database. ➕ Try adding some for testing.")


    else:
        st.write(f"Number of students: {len(data)}")
        st.dataframe(data.style.format({'Average': '{:.2f}'}))
    
    with st.sidebar:
        st.sidebar.header("Configuration Panel")
        option = st.selectbox("Choose an option", ["Add Students", "Update Student","Update Students Notes", "Delete Students"])
        
        if option == "Add Students":
            name = st.text_input("Name", placeholder="Enter student name...", key="name_input")
            age = st.number_input("Age", min_value=0, max_value=100, key="age_input", placeholder="Enter student age...")
            
            if st.button("Add Student"):
                current_students = load_students()
                # Check if the name is valid and not already in the list
                if is_valid_name(name) and age > 0 and not name_exists(name, current_students): 
                    student = {
                        "id": get_next_id(current_students),
                        "name": name,
                        "age": age
                    }
                    add_student(student)
                    # Initialize notes for the new student
                    init_student_notes(student["id"])
                    st.success(f"Student {name} added successfully.")
                    
                    # rerun the app to refresh the data
                    st.rerun()
                else:
                    if not is_valid_name(name):
                        st.error("Invalid name. Please remove extra spaces or use a real name.")
                    elif name_exists(name, current_students):
                       st.error("This name already exists.")
                    elif age <= 0:
                        st.error("Please enter an age greater than 0.")
                    
                    
        elif option == "Delete Students":
            # st.subheader("Delete a student")
            student_id = st.number_input("Student ID", min_value=1, placeholder="Enter student ID")
            
            if st.button("Delete Student"):
                
                current_students = load_students()
                
                if student_id and student_id_exists(student_id, current_students):
                    
                    @st.dialog("Are you sure?", width="small")
                    def confirm():
                        
                        st.write(f"Are you sure you want to delete student with ID {student_id}?")
                        st.write("This action cannot be undone.")
                        col1, col2, col3 = st.columns((2,8,2))
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
                    confirm()
                else:
                    st.error("This ID does not exist in the database.")
                    
        elif option == "Update Students Notes":
            
            student_id = st.number_input("Student ID", min_value=1)
            subject = st.selectbox("Subject", subjects)
            note = st.number_input("Updated Note", min_value=0.0, max_value=100.0, step=0.1)
            
            if st.button("Update Note"):
                current_students = load_students()
                update_student_notes(student_id, subject, note)
                
                st.rerun()
                
                
        elif option == "Update Student":
            student_id = st.number_input("Student ID", min_value=1)
            name = st.text_input("Update Name")
            age = st.number_input("Update Age", min_value=0, max_value=100)
            
            if st.button("Update Student"):
                current_students = load_students()
                if not is_valid_name(name):
                    st.error("Name is invalid. Please remove extra spaces or use a real name.")
                elif age <= 0:
                    st.error("Please enter an age greater than 0.")
                elif name_exists(name, current_students):
                    st.error("This name already exists. Please use a different name.")
                else:
                    update_student_infos(student_id, name, age)
                    st.rerun()
                
                


if __name__ == "__main__":
    main()
