import pandas as pd



def show_students_details_table(notes : pd.DataFrame, students : pd.DataFrame) -> pd.DataFrame:
   notes_pivot = notes.pivot(index='student_id', columns='subject', values='note')
   merging = pd.merge(students, notes_pivot, left_on='id', right_on='student_id')
#    print(merging.columns)
   return merging