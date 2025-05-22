from pathlib import Path
import json

notes_file = Path("data/notes.json")


def load_notes():
    if not notes_file.exists():
        return "No notes data available."
    with open(notes_file, "r") as file:
        notes = json.load(file)
    return notes

notes = load_notes()


# initializing the subjects list
subjects = ["Mathematics", "Physics", "Chemistry"]

# create the notes for each student
def init_student_notes(student_id: int):
    global notes
    next_id = max([note["id"] for note in notes], default=0) + 1
    for subject in subjects:
        notes.append({
            "id": next_id,
            "student_id": student_id,
            "subject": subject,
            "note": 0
        })
        next_id += 1
    with open(notes_file, "w") as file:
        json.dump(notes, file, indent=4)
    return "Notes initialized successfully."


#delete the notes of a student
# for a given student ID
def delete_student_notes(student_id: int):
    global notes
    # Check if the ID exists in the current notes list
    if student_id not in [note["student_id"] for note in notes]:
        return "Student ID not found."
    else:
        # Create a new list excluding the notes for the student with the given ID
        notes = [note for note in notes if note["student_id"] != student_id]

        # Save the updated list back to the file
        with open(notes_file, "w") as file:
            json.dump(notes, file, indent=4)

        return "Student notes deleted successfully."
    
    # update the notes for a given student ID
def update_student_notes(student_id: int, subject: str, note: float):
    global notes
    
    # Check if the ID exists in the current notes list
    if student_id not in [note["student_id"] for note in notes]:
        return "Student ID not found."
    else:
        
        # Update the note for the given student ID and subject
        for note_entry in notes:
            if note_entry["student_id"] == student_id and note_entry["subject"] == subject:
                note_entry["note"] = note
                
        # Save the updated list back to the file
        with open(notes_file, "w") as file:
            json.dump(notes, file, indent=4)
        return "Student notes updated successfully."
    
    