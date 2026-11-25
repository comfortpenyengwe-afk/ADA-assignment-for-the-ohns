# BIT3360: Advanced Databases - Group Assignment
## Topic: Database Security Prototype & Defense Architecture
**Institution:** Zambia University College of Technology (ZUT)  
**Submission Date:** 26/11/2026  

---

## Group Members

| Name | Student ID |
|---|---|
| Comfort Penyengwe | 2410098 |
| Gideon Namuya | 2410149 |
| Lubuto Matambo | 2410171 |
| Lamla Mwanza | 2410205 |

---

## 1. Project Overview & Deliverables
This repository contains the deliverables for the **BIT3360: Advanced Databases** group coursework on **Database Security**:

1. **`BIT3360_Database_Security_Presentation.pptx`**: Standalone Microsoft PowerPoint presentation deck (12 slides).
2. **`web_app.py`**: Zero-dependency interactive web portal (`http://localhost:5000`) built for the ZUT Student Records System (`zut_student_records`) to demonstrate Role-Based Access Control (RBAC), SQL Injection attacks vs. parameterized query defenses, and live audit triggers.
3. **`security_demo.py`**: Interactive terminal/CLI version of the security prototype.
4. **`database_security.sql`**: Full SQL DDL/DML script defining tables (`students` with `nrc`, `courses`, `grades`, `audit_log`), sample data, RBAC roles (`sec_admin`, `sec_lecturer`, `sec_student`), sanitized views (`vw_student_grades`), and automated audit triggers.
5. **`presentation.html`**: Browser-based version of the 12-slide presentation deck.

---

## 2. How to Run the Web Portal

Run:
```powershell
python web_app.py
```
* Your browser will open to `http://localhost:5000`.
* Available modules:
  * **1. Access Control (RBAC) & Query Inspector:** Switch between `sec_admin`, `sec_lecturer`, and `sec_student`. Students are restricted to viewing only their own grades and are blocked from viewing peer records or modifying marks (`Error 1142: Access Denied`).
  * **2. SQL Injection vs Parameterized Queries:** Test malicious payloads (e.g., `' OR '1'='1`) against vulnerable string concatenation versus pre-compiled parameterized queries.
  * **3. Tamper-Evident Audit Trail & Triggers:** Trigger grade updates and inspect the `audit_log` table populated automatically by `trg_audit_grade_update`.
  * **4. Full SQL Schema & Source Viewer:** Inspect the full `database_security.sql` schema and privilege definitions.
  * **5. Security Architecture:** Summary of the implemented defense layers and compliance with the **Zambia Data Protection Act No. 3 of 2021**.

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
