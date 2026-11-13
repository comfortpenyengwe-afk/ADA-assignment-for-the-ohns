# BIT3360: Advanced Databases - Group Assignment
## Topic: Database Security Prototype & Defense Architecture
**Institution:** Zambia University College of Technology (ZUT)  
**Submission Date:** 26/11/2026  

---

## 1. Project Overview & Deliverables
This repository contains the complete deliverables for the **BIT3360: Advanced Databases** group coursework on **Database Security**:

1. **`BIT3360_Database_Security_Presentation.pptx`**: The official, standalone Microsoft PowerPoint presentation file (13 slides with embedded speaker notes).
2. **`web_app.py`**: **(Recommended Demo)** A zero-dependency visual web portal (`http://localhost:5000`) designed for ZUT to demonstrate Access Control, SQL Injection attacks vs defenses, and live audit triggers in a real browser.
3. **`security_demo.py`**: An interactive terminal/CLI version of the security prototype.
4. **`database_security.sql`**: Full MySQL DDL/DML script with tables (`students` with `nrc`, `courses`, `grades`, `audit_log`), sample data, RBAC user definitions, and automated audit triggers.
5. **`presentation.html`**: A web version of the 13-slide presentation deck (can be presented directly or printed to PDF).
6. **`PRESENTATION_GUIDE.md`**: Slide-by-slide word-for-word speaker notes divided among **5 group members**.

---

## 2. How to Run the Visual Web Portal (Recommended for Presentation)

Simply run:
```powershell
python web_app.py
```
* Your web browser will automatically open to `http://localhost:5000`.
* You can switch between 4 interactive tabs during your presentation:
  * **Tab 1: Access Control (RBAC):** Click **Student** and try to change a grade $\rightarrow$ triggers a red **`ACCESS DENIED (Error 1142)`** alert box. Then click **Lecturer** $\rightarrow$ shows green success box.
  * **Tab 2: SQL Injection Defense:** Click **`Payload: ' OR '1'='1`**. Test on the vulnerable query $\rightarrow$ leaks all student NRCs. Then test on the parameterized query $\rightarrow$ attack is completely neutralized.
  * **Tab 3: Tamper-Evident Audit Trail:** Trigger a grade change and watch the live `audit_log` record the timestamp, user, previous mark, and new mark.
  * **Tab 4: Viva Guide:** Quick reference for your group members during the presentation.

---

## 3. Database Schema Design (`zut_student_records`)

```
+-----------------------------------+        +-----------------------------------+
|             students              |        |              courses              |
+-----------------------------------+        +-----------------------------------+
| student_id      (PK, INT)         |        | course_code   (PK, VARCHAR)       |
| student_number  (UNIQUE, VARCHAR) |        | course_name   (VARCHAR)           |
| nrc             (UNIQUE, VARCHAR) |        | credits       (INT)               |
| full_name       (VARCHAR)         |        | lecturer_name (VARCHAR)           |
| program         (VARCHAR)         |        +-----------------+-----------------+
| year_of_study   (INT)             |                          |
| email           (UNIQUE, VARCHAR) |                          |
+-----------------+-----------------+                          |
                  |                                            |
                  | 1                                        1 |
                  |                                            |
                  | N                                        N |
                  +-----------------+--------------------------+
                                    |
                            +-------v---------------------------+
                            |              grades               |
                            +-----------------------------------+
                            | grade_id      (PK, INT)           |
                            | student_id    (FK -> students)    |
                            | course_code   (FK -> courses)     |
                            | mark          (DECIMAL 5,2)       |
                            | grade_letter  (VARCHAR)           |
                            | semester      (VARCHAR)           |
                            +-----------------+-----------------+
                                              |
                                              | (AFTER UPDATE / DELETE TRIGGER)
                                              v
                            +-----------------------------------+
                            |             audit_log             |
                            +-----------------------------------+
                            | log_id          (PK, INT)         |
                            | action_type     (VARCHAR)         |
                            | table_name      (VARCHAR)         |
                            | record_id       (INT)             |
                            | changed_by      (VARCHAR)         |
                            | old_value       (TEXT)            |
                            | new_value       (TEXT)            |
                            | timestamp       (DATETIME)        |
                            +-----------------------------------+
```

---

## 4. How to Present the Project (5-Minute Group Script)

1. **Member 1 (Intro & Threats):** Introduce the system and explain why database security is vital (protecting student NRCs from theft and marks from tampering).
2. **Member 2 (Defensive Theory):** Explain Role-Based Access Control (Principle of Least Privilege) and Parameterized Queries (separating SQL code from data).
3. **Member 3 (Architecture):** Explain the relational tables and the three database accounts (`sec_admin`, `sec_lecturer`, `sec_student`).
4. **Member 4 (Live Demo):** Share the screen on `http://localhost:5000` (run via `python web_app.py`) and click the buttons on Tab 1, 2, and 3.
5. **Member 5 (Compliance & Close):** Explain the audit logging mechanism, reference the **Zambia Data Protection Act No. 3 of 2021**, and conclude.
