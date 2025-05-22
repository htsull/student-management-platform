import re


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


# check if student ID exists in the list
def student_id_exists(student_id: int, students: list):
    return any(s["id"] == student_id for s in students)


