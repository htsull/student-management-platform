import pandas as pd
from functions.gestion_notes import subjects



def show_students_details_table(notes : pd.DataFrame, students : pd.DataFrame) -> pd.DataFrame:
   
    if 'student_id' not in notes.columns or notes.empty:
        pass
    else:
        notes_pivot = notes.pivot(index='student_id', columns='subject', values='note')
        merging = pd.merge(students, notes_pivot, left_on='id', right_on='student_id')
        merging['Average'] = round(merging[subjects].mean(axis=1), 2)
        merging = merging.sort_values(by='Average', ascending=False)
        return merging
    
    