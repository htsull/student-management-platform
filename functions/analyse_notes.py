import pandas as pd
from functions.gestion_notes import subjects


# def show_students_details_table(
#     notes: pd.DataFrame, students: pd.DataFrame
# ) -> pd.DataFrame:
#     if "student_id" not in notes.columns or notes.empty:
#         return pd.DataFrame()

#     else:
#         notes_pivot = notes.pivot(index="student_id", columns="subject", values="note")
#         merging = pd.merge(students, notes_pivot, left_on="id", right_on="student_id")
#         merging["Average"] = round(merging[subjects].mean(axis=1), 2)
#         merging = merging.sort_values(by="Average", ascending=False)
#         return merging


def show_students_details_table(
    notes: pd.DataFrame,
    students: pd.DataFrame,
) -> pd.DataFrame:
    if notes.empty or "student_id" not in notes.columns:
        return pd.DataFrame()

    # 1) Pivot notes: index = student_id
    notes_pivot = notes.pivot(
        index="student_id",
        columns="subject",
        values="note",
    )

    # 2) Merge students with pivot using the index on the right
    merging = students.merge(
        notes_pivot,
        left_on="id",
        right_index=True,
        how="left",
    )

    # 3) Compute average over subjects
    merging["Average"] = merging[subjects].mean(axis=1).round(2)

    # 4) Sort
    merging = merging.sort_values(by="Average", ascending=False)

    # merging = merging.drop(columns=["id"]).reset_index(drop=True)

    return merging
