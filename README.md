# 🎓 Student Management Platform

A **Streamlit** web app for creating, updating, and reviewing student records and subject grades. Data is stored in a local **SQLite** database (created automatically on first run) and presented in a tidy, spreadsheet-like layout for quick review.

The app is optimized for classroom or small program management where instructors need to:

- Add new students and capture their basic details
- Record or adjust grades across predefined subjects
- Review grades in a pivoted table by student
- Remove records (students and their associated grades) when necessary

![Main Interface](screenshots/UI.png)

---

## ✨ Key Features

### Student records
- Add students with name and age validation (`functions/helpers.py`).
- Update a student’s name or age individually.
- Delete a student and cascade-delete their grades.

### Grade tracking
- Supported subjects are defined in `functions/grade_analysis.py` (`Subject 1`, `Subject 2`, `Subject 3`).
- Add a grade for a subject when no grade exists yet.
- Update an existing grade or insert a new one if missing.

### Data view
- Records are pivoted to a student-by-subject table using `pivot_data` in `functions/grade_analysis.py`.
- The UI refreshes after each action to keep the display in sync (`st.rerun()`).

---

## 🗂️ Project Structure

```
.
├── main.py                     # Streamlit app entry point and UI logic
├── data/
│   ├── database_management.py  # SQLite helpers (create tables, CRUD, joins)
│   ├── platform.db             # Auto-created SQLite database (generated at runtime)
│   ├── etudiants.json          # Legacy sample data (not used by the current app)
│   └── notes.json              # Legacy sample data (not used by the current app)
├── functions/
│   ├── grade_analysis.py       # Subject list and grade pivot helper
│   └── helpers.py              # UI validations and confirmation dialogs
├── .streamlit/config.toml      # Streamlit server config (runOnSave enabled)
├── requirements.txt            # Runtime dependencies (Streamlit, pandas, watchdog)
└── screenshots/UI.png          # UI preview
```

---

## 🚀 Quickstart

### Prerequisites
- Python 3.9 or later
- pip

### Installation & launch
```bash
git clone https://github.com/your-username/student-management-platform.git
cd student-management-platform

pip install -r requirements.txt
streamlit run main.py
```

The first launch creates `data/platform.db` and the required `students` and `grades` tables automatically.

---

## 🧭 Using the App

1. **Open the sidebar** and choose an action:
   - **Add Students** – create a record after passing name/age validation.
   - **Add Students Grades** – attach a grade for a subject when none exists yet.
   - **Update Student Infos** – change a student’s name and/or age.
   - **Update Students Grades** – modify an existing grade or insert if missing.
   - **Delete Students** – remove a student and their grades.
2. **Review the table** in the main view, which shows students pivoted by subject.
3. (Optional) Use the **“Drop all data from the database”** button to clear all tables.

> Tip: Subject choices come from the `subjects` list in `functions/grade_analysis.py`. Add or rename subjects there to change the dropdowns and pivoted view.

---

## 🛠️ Development Notes

- The database lives at `data/platform.db`; delete this file to start fresh.
- All database helpers are in `data/database_management.py` and return/accept `sqlite3` connections when needed.
- Validation helpers live in `functions/helpers.py` and are reused across sidebar forms.
- The app currently assumes a fixed subject list. If you add or remove subjects, also adjust any seed data or downstream reporting you introduce.

---

## 📄 License

This project is open source under the MIT license. Feel free to adapt it for your classroom, workshop, or internal tooling needs.
