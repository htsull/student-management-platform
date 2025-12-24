import json
from pathlib import Path

students_file = Path("data/etudiants.json")
notes_file = Path("data/notes.json")


def load_students():
    if not students_file.exists():
        return "No student data available."
    with open(students_file, "r") as file:
        students = json.load(file)
    return students


# load student list
students = load_students()


def add_student(student: dict):
    students = load_students()
    students.append(student)

    with open(students_file, "w") as file:
        json.dump(students, file, indent=4)

    return "Student added successfully."


def delete_student(student_id: int):
    students = load_students()

    # Check if the ID exists in the current student list
    if student_id not in [student["id"] for student in students]:
        return "Student ID not found."

    students = [student for student in students if student["id"] != student_id]

    with open(students_file, "w") as file:
        json.dump(students, file, indent=4)

    return "Student deleted successfully."


def update_student_infos(student_id: int, name: str, age: int):
    students = load_students()

    # Check if the ID exists in the current student list
    if student_id not in [student["id"] for student in students]:
        return "Student ID not found."
    else:
        # Update the student information
        for student in students:
            if student["id"] == student_id:
                if name:
                    student["name"] = name
                if age is not None and age > 0:
                    student["age"] = age
                break

        #  TODO : update only the fields that were changed

        # Save the updated list back to the file
        with open(students_file, "w") as file:
            json.dump(students, file, indent=4)

    return "Student information updated successfully."
