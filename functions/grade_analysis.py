import pandas as pd

subjects = [
    "Subject 1",
    "Subject 2",
    "Subject 3",
]
    
def pivot_data(df: pd.DataFrame) -> pd.DataFrame:
    pivoted = df.pivot(
        index=["student_id", "name"],
        columns="subject",
        values="grade",
    )

    pivoted = pivoted.reset_index()

    # specific subject ordering / subset:
    desired_cols = ["student_id", "name"] + subjects
    existing = [c for c in desired_cols if c in pivoted.columns]
    pivoted = pivoted.loc[:, existing]

    return pivoted