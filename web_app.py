"""
=====================================================================
ZAMBIA UNIVERSITY COLLEGE OF TECHNOLOGY (ZUT)
BIT3360: ADVANCED DATABASES - SECURITY PROTOTYPE WEB PORTAL
Zero-dependency web application using Python standard library.
Includes:
- Live RBAC Simulation with Underlying SQL Query Inspector
- SQL Injection vs Parameterized Queries with Raw Query Viewer
- Trigger-based Audit Trail with Full SQL Trigger Definition
- Direct PPTX and SQL file download endpoints
Runs on http://localhost:5000
=====================================================================
"""

import http.server
import socketserver
import urllib.parse
import json
import sqlite3
import webbrowser
import os
import sys

PORT = 5000
DB_FILE = "zut_student_records.db"
PPTX_FILE = "BIT3360_Database_Security_Presentation.pptx"
SQL_FILE = "database_security.sql"

# ---------------------------------------------------------------------
# 1. DATABASE INITIALIZATION
# ---------------------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_number TEXT UNIQUE NOT NULL,
        nrc TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        program TEXT NOT NULL,
        year_of_study INTEGER NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_code TEXT PRIMARY KEY,
        course_name TEXT NOT NULL,
        credits INTEGER NOT NULL DEFAULT 15,
        lecturer_name TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        course_code TEXT NOT NULL,
        mark REAL NOT NULL,
        grade_letter TEXT NOT NULL,
        semester TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (course_code) REFERENCES courses(course_code)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_type TEXT NOT NULL,
        table_name TEXT NOT NULL,
        record_id INTEGER NOT NULL,
        changed_by TEXT NOT NULL,
        old_value TEXT,
        new_value TEXT,
        timestamp TEXT NOT NULL
    );
    """)

    # Audit Trigger
    cur.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_audit_grade_update
    AFTER UPDATE ON grades
    BEGIN
        INSERT INTO audit_log (action_type, table_name, record_id, changed_by, old_value, new_value, timestamp)
        VALUES (
            'UPDATE',
            'grades',
            NEW.grade_id,
            'sec_lecturer',
            'mark=' || OLD.mark || ', grade=' || OLD.grade_letter,
            'mark=' || NEW.mark || ', grade=' || NEW.grade_letter,
            datetime('now', 'localtime')
        );
    END;
    """)

    cur.execute("SELECT COUNT(*) FROM students;")
    if cur.fetchone()[0] == 0:
        students = [
            ('ZUT/2023/0142', '294812/10/1', 'Chileshe Mwape', 'BSc Information Technology', 3, 'cmwape@zut.ac.zm'),
            ('ZUT/2023/0188', '381940/11/1', 'Kondwani Banda', 'BSc Computer Science', 3, 'kbanda@zut.ac.zm'),
            ('ZUT/2023/0205', '412093/67/1', 'Thandiwe Phiri', 'BSc Information Systems', 3, 'tphiri@zut.ac.zm'),
            ('ZUT/2023/0277', '194820/82/1', 'Mutale Musonda', 'BSc Information Technology', 3, 'mmusonda@zut.ac.zm'),
            ('ZUT/2023/0310', '581932/10/1', 'Natasha Tembo', 'BSc Software Engineering', 3, 'ntembo@zut.ac.zm')
        ]
        cur.executemany("INSERT INTO students (student_number, nrc, full_name, program, year_of_study, email) VALUES (?, ?, ?, ?, ?, ?)", students)

        courses = [
            ('BIT3360', 'Advanced Databases', 15, 'Dr. C. Chanda'),
            ('BIT3320', 'Network & Database Security', 15, 'Mr. P. Mulenga'),
            ('BIT3310', 'Software Architecture', 15, 'Mrs. F. Mumba')
        ]
        cur.executemany("INSERT INTO courses (course_code, course_name, credits, lecturer_name) VALUES (?, ?, ?, ?)", courses)

        grades = [
            (1, 'BIT3360', 78.5, 'A', 'Semester 1 2026'),
            (1, 'BIT3320', 82.0, 'A+', 'Semester 1 2026'),
            (2, 'BIT3360', 64.0, 'B', 'Semester 1 2026'),
            (3, 'BIT3360', 89.0, 'A+', 'Semester 1 2026'),
            (4, 'BIT3360', 55.0, 'C+', 'Semester 1 2026'),
            (5, 'BIT3360', 91.5, 'A+', 'Semester 1 2026')
        ]
        cur.executemany("INSERT INTO grades (student_id, course_code, mark, grade_letter, semester) VALUES (?, ?, ?, ?, ?)", grades)

        cur.execute("""
        INSERT INTO audit_log (action_type, table_name, record_id, changed_by, old_value, new_value, timestamp)
        VALUES ('SYSTEM_INIT', 'ALL', 0, 'sec_admin', 'NONE', 'System initialized with student records and audit triggers', datetime('now', 'localtime'))
        """)

    conn.commit()
    conn.close()

# ---------------------------------------------------------------------
# 2. RBAC PERMISSION POLICIES & QUERY TEMPLATES
# ---------------------------------------------------------------------
ROLE_PERMISSIONS = {
    "admin": {
        "title": "Database Administrator (DBA)",
        "allowed": ["VIEW_STUDENTS", "VIEW_GRADES", "UPDATE_GRADE", "DELETE_STUDENT", "DROP_TABLE"]
    },
    "lecturer": {
        "title": "Academic Lecturer (sec_lecturer)",
        "allowed": ["VIEW_STUDENTS", "VIEW_GRADES", "UPDATE_GRADE"]
    },
    "student": {
        "title": "Undergraduate Student (sec_student)",
        "allowed": ["VIEW_GRADES"]
    }
}

ACTION_DETAILS = {
    "VIEW_STUDENTS": {
        "sql": "SELECT student_id, student_number, nrc, full_name, email FROM students;",
        "purpose": "Retrieves full student records including confidential National Registration Card (NRC) identities.",
        "why_denied": "Students are strictly prohibited from viewing peer records or confidential NRC numbers under the Zambia Data Protection Act."
    },
    "VIEW_GRADES": {
        "sql": "SELECT s.full_name, g.course_code, g.mark, g.grade_letter, g.semester FROM grades g JOIN students s ON g.student_id = s.student_id;",
        "purpose": "Queries grade standings. For students, this queries a sanitized database View (vw_student_grades).",
        "why_denied": "Permitted for all authenticated roles."
    },
    "UPDATE_GRADE": {
        "sql": "UPDATE grades SET mark = 95.0, grade_letter = 'A+' WHERE grade_id = 1;",
        "purpose": "Modifies examination marks on the grades table, triggering the audit logger.",
        "why_denied": "Students have NO 'UPDATE' privilege on the grades table (Access Denied Error 1142) to protect academic integrity."
    },
    "DELETE_STUDENT": {
        "sql": "DELETE FROM students WHERE student_id = 5;",
        "purpose": "Removes a student permanently from the registry.",
        "why_denied": "Lecturers and students lack 'DELETE' privileges on the students table. Only DBA has destructive DML permissions."
    },
    "DROP_TABLE": {
        "sql": "DROP TABLE students;",
        "purpose": "Catastrophic DDL command that destroys table structure and all stored data.",
        "why_denied": "Standard users and lecturers lack DDL 'DROP' privileges. Blocked immediately by DBMS engine."
    }
}

# ---------------------------------------------------------------------
# 3. HTML/CSS/JS INTERFACE
# ---------------------------------------------------------------------
INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZUT - BIT3360 Database Security Prototype</title>
    <style>
        :root {
            --primary: #0f172a;
            --accent: #2563eb;
            --accent-hover: #1d4ed8;
            --bg: #f8fafc;
            --surface: #ffffff;
            --border: #e2e8f0;
            --text-dark: #1e293b;
            --text-muted: #64748b;
            --danger: #dc2626;
            --success: #16a34a;
            --warning: #d97706;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
        body { background: var(--bg); color: var(--text-dark); min-height: 100vh; display: flex; flex-direction: column; }

        header.top-nav {
            background: #0f172a;
            color: white;
            padding: 16px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .brand-badge {
            background: #2563eb;
            color: white;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.85rem;
            letter-spacing: 0.05em;
        }

        .brand h1 { font-size: 1.25rem; font-weight: 700; }
        .brand p { font-size: 0.85rem; color: #94a3b8; }

        .btn-download-hero {
            background: #22c55e;
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.88rem;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }
        .btn-download-hero:hover { background: #16a34a; }

        .tabs-bar {
            background: white;
            border-bottom: 1px solid var(--border);
            display: flex;
            padding: 0 32px;
            gap: 8px;
            overflow-x: auto;
        }

        .tab-btn {
            background: none;
            border: none;
            padding: 16px 18px;
            font-size: 0.92rem;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.2s;
            white-space: nowrap;
        }

        .tab-btn:hover { color: var(--accent); }
        .tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); }

        main.container {
            max-width: 1150px;
            width: 100%;
            margin: 28px auto;
            padding: 0 24px;
            flex-grow: 1;
        }

        .tab-pane { display: none; }
        .tab-pane.active { display: block; }

        .card {
            background: white;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 24px;
        }

        .card-header {
            margin-bottom: 18px;
            border-bottom: 1px solid #f1f5f9;
            padding-bottom: 12px;
        }

        .card-header h2 { font-size: 1.35rem; color: var(--primary); }
        .card-header p { font-size: 0.92rem; color: var(--text-muted); margin-top: 4px; }

        /* Role Switcher */
        .role-selector-box {
            display: flex;
            align-items: center;
            gap: 16px;
            background: #f1f5f9;
            padding: 14px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .role-btn {
            background: white;
            border: 1px solid var(--border);
            padding: 8px 16px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .role-btn.active {
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }

        .btn-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }

        button.action-btn {
            background: white;
            border: 1px solid var(--border);
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-dark);
            cursor: pointer;
            text-align: left;
            transition: all 0.2s;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        button.action-btn span.tag { font-size: 0.75rem; text-transform: uppercase; color: var(--accent); font-weight: 700; }
        button.action-btn.danger span.tag { color: var(--danger); }
        button.action-btn:hover { border-color: var(--accent); background: #f0f7ff; }
        button.action-btn.danger:hover { border-color: var(--danger); background: #fef2f2; }

        /* Result Alerts */
        .alert-box {
            border-radius: 8px;
            padding: 16px 20px;
            margin-top: 20px;
            display: none;
            animation: fadeIn 0.25s ease;
        }

        .alert-box.success {
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            color: #166534;
        }

        .alert-box.danger {
            background: #fef2f2;
            border: 1px solid #fecaca;
            color: #991b1b;
        }

        /* Query Inspector Drawer */
        .query-inspector {
            background: #0f172a;
            color: #f8fafc;
            border-radius: 8px;
            padding: 16px;
            margin-top: 14px;
            display: none;
            animation: fadeIn 0.25s ease;
        }

        .query-inspector .inspector-title {
            color: #38bdf8;
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }

        .code-box {
            font-family: "Courier New", Courier, monospace;
            font-size: 0.92rem;
            color: #e2e8f0;
            line-height: 1.5;
            background: #1e293b;
            padding: 10px 14px;
            border-radius: 6px;
            margin: 6px 0;
            overflow-x: auto;
        }

        .query-notes {
            font-size: 0.88rem;
            color: #94a3b8;
            margin-top: 6px;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Tables */
        table.data-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
            font-size: 0.92rem;
        }

        table.data-table th, table.data-table td {
            padding: 10px 14px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }

        table.data-table th { background: #f8fafc; font-weight: 600; color: var(--text-dark); }
        table.data-table tr:hover { background: #f8fafc; }

        /* SQL Injection Arena */
        .sqli-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }

        .sqli-box {
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 18px;
            background: #fafafa;
        }

        .sqli-box.vuln { border-top: 4px solid var(--danger); }
        .sqli-box.sec { border-top: 4px solid var(--success); }

        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 12px;
        }

        .input-group input {
            flex-grow: 1;
            padding: 10px 14px;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 0.95rem;
        }

        .quick-payloads {
            display: flex;
            gap: 8px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }

        .badge-btn {
            background: #e2e8f0;
            border: none;
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            cursor: pointer;
            font-weight: 600;
        }
        .badge-btn:hover { background: #cbd5e1; }

        .btn-primary {
            background: var(--accent);
            color: white;
            border: none;
            padding: 10px 18px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
        }
        .btn-primary:hover { background: var(--accent-hover); }

        .btn-danger {
            background: var(--danger);
            color: white;
            border: none;
            padding: 10px 18px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
        }

        .btn-success {
            background: var(--success);
            color: white;
            border: none;
            padding: 10px 18px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
        }
    </style>
</head>
<body>

    <header class="top-nav">
        <div class="brand">
            <span class="brand-badge">ZUT</span>
            <div>
                <h1>Zambia University College of Technology</h1>
                <p>BIT3360 Advanced Databases - Security Prototype Portal</p>
            </div>
        </div>
        <div style="display: flex; gap: 10px;">
            <a href="/download/presentation.pptx" class="btn-download-hero" download="BIT3360_Database_Security_Presentation.pptx">
                &#128190; Download PowerPoint (.pptx)
            </a>
            <a href="/download/database_security.sql" class="btn-download-hero" style="background: #3b82f6;" download="database_security.sql">
                &#128196; Download SQL Script
            </a>
        </div>
    </header>

    <div class="tabs-bar">
        <button class="tab-btn active" onclick="switchTab('rbac')">1. Access Control (RBAC) & Query Inspector</button>
        <button class="tab-btn" onclick="switchTab('sqli')">2. SQL Injection vs Parameterized Queries</button>
        <button class="tab-btn" onclick="switchTab('audit')">3. Tamper-Evident Audit Trail & Triggers</button>
        <button class="tab-btn" onclick="switchTab('sql-source')">4. Full SQL Schema & Source Viewer</button>
        <button class="tab-btn" onclick="switchTab('guide')">5. Viva Script & Downloads</button>
    </div>

    <main class="container">

        <!-- ========================================== -->
        <!-- TAB 1: ROLE-BASED ACCESS CONTROL (RBAC) -->
        <!-- ========================================== -->
        <div id="tab-rbac" class="tab-pane active">
            <div class="card">
                <div class="card-header">
                    <h2>Role-Based Access Control (RBAC) & Query Inspector</h2>
                    <p>Demonstrates how database permissions enforce the Principle of Least Privilege, and displays the exact underlying SQL query executed by the database engine.</p>
                </div>

                <div class="role-selector-box">
                    <strong>Select Active User Role:</strong>
                    <button class="role-btn active" id="btn-role-admin" onclick="setRole('admin')">Admin (sec_admin)</button>
                    <button class="role-btn" id="btn-role-lecturer" onclick="setRole('lecturer')">Lecturer (sec_lecturer)</button>
                    <button class="role-btn" id="btn-role-student" onclick="setRole('student')">Student (sec_student)</button>
                </div>

                <div style="margin-bottom: 12px; font-size: 0.9rem; color: var(--text-muted);">
                    <strong>Active Role:</strong> <span id="active-role-desc" style="color: var(--accent); font-weight: 700;">Database Administrator (DBA)</span>
                </div>

                <div class="btn-grid">
                    <button class="action-btn" onclick="runAction('VIEW_STUDENTS')">
                        <span class="tag">SELECT</span>
                        View Students & Confidential NRC
                    </button>
                    <button class="action-btn" onclick="runAction('VIEW_GRADES')">
                        <span class="tag">SELECT</span>
                        View Academic Grades
                    </button>
                    <button class="action-btn" onclick="runAction('UPDATE_GRADE')">
                        <span class="tag">UPDATE</span>
                        Alter Student Grade (e.g. Set Mark to 95)
                    </button>
                    <button class="action-btn danger" onclick="runAction('DELETE_STUDENT')">
                        <span class="tag">DELETE</span>
                        Delete Student Record
                    </button>
                    <button class="action-btn danger" onclick="runAction('DROP_TABLE')">
                        <span class="tag">DDL</span>
                        DROP TABLE students
                    </button>
                </div>

                <!-- Alert Result Box -->
                <div id="rbac-alert" class="alert-box"></div>

                <!-- Underlying SQL Query Inspector -->
                <div id="rbac-inspector" class="query-inspector">
                    <div class="inspector-title">&#128269; Underlying SQL Query & Security Inspection (What the DB Engine Did)</div>
                    <div class="code-box" id="inspector-sql">-- Query will appear here</div>
                    <div class="query-notes" id="inspector-notes">Explanation will appear here</div>
                </div>

                <!-- Data Table Output -->
                <div id="rbac-table-wrap" style="display: none;"></div>
            </div>
        </div>

        <!-- ========================================== -->
        <!-- TAB 2: SQL INJECTION DEFENSE -->
        <!-- ========================================== -->
        <div id="tab-sqli" class="tab-pane">
            <div class="card">
                <div class="card-header">
                    <h2>Live SQL Injection Attack vs Parameterized Query Defense</h2>
                    <p>Observe the raw underlying dynamic query string versus the prepared statement structure when malicious input is supplied.</p>
                </div>

                <label style="font-weight: 600; font-size: 0.95rem;">Search Student by NRC Number:</label>
                <div class="input-group" style="margin-top: 8px;">
                    <input type="text" id="nrc-input" value="294812/10/1" placeholder="Enter student NRC (e.g. 294812/10/1)">
                </div>

                <div class="quick-payloads">
                    <span style="font-size: 0.85rem; color: var(--text-muted); align-self: center;">Quick Fill:</span>
                    <button class="badge-btn" onclick="setNrc('294812/10/1')">Legitimate NRC (294812/10/1)</button>
                    <button class="badge-btn" style="color: var(--danger);" onclick="setNrc(\"' OR '1'='1\")">Payload 1: ' OR '1'='1</button>
                    <button class="badge-btn" style="color: var(--danger);" onclick="setNrc(\"' UNION SELECT 999, 'HACKER', '000000/00/0', 'Injected', 4, 'evil@hack.org' --\")">Payload 2: UNION Attack</button>
                </div>

                <div class="sqli-grid">
                    <!-- Box A: Vulnerable Dynamic Query -->
                    <div class="sqli-box vuln">
                        <h3 style="color: var(--danger); font-size: 1.1rem;">A. Insecure Dynamic SQL (String Concatenation)</h3>
                        <p style="font-size: 0.88rem; color: var(--text-muted); margin-top: 4px;">User string is concatenated directly into the SQL string.</p>
                        <div class="code-box" id="vuln-code">SELECT * FROM students WHERE nrc = '294812/10/1'</div>
                        <button class="btn-danger" onclick="testSqli('vuln')">Execute Vulnerable Query</button>
                        <div id="vuln-result" style="margin-top: 14px;"></div>
                    </div>

                    <!-- Box B: Secure Parameterized Query -->
                    <div class="sqli-box sec">
                        <h3 style="color: var(--success); font-size: 1.1rem;">B. Secure Parameterized Query (Prepared Statement)</h3>
                        <p style="font-size: 0.88rem; color: var(--text-muted); margin-top: 4px;">SQL structure is pre-compiled; input is bound as literal parameter <code>?</code>.</p>
                        <div class="code-box">cursor.execute("SELECT * FROM students WHERE nrc = ?", (input,))</div>
                        <button class="btn-success" onclick="testSqli('sec')">Execute Parameterized Query</button>
                        <div id="sec-result" style="margin-top: 14px;"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ========================================== -->
        <!-- TAB 3: AUDIT TRAIL -->
        <!-- ========================================== -->
        <div id="tab-audit" class="tab-pane">
            <div class="card">
                <div class="card-header">
                    <h2>Tamper-Evident Database Audit Trail & Triggers</h2>
                    <p>Demonstrates automated database triggers logging all modifications to satisfy non-repudiation and Zambian Data Protection compliance.</p>
                </div>

                <div style="background: #f8fafc; border: 1px solid var(--border); padding: 18px; border-radius: 8px; margin-bottom: 20px;">
                    <h3 style="font-size: 1rem; margin-bottom: 8px;">Trigger a Live Grade Change:</h3>
                    <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                        <label>Student ID: <input type="number" id="audit-sid" value="1" style="width: 60px; padding: 6px;"></label>
                        <label>New Mark (0-100): <input type="number" id="audit-mark" value="95.5" style="width: 90px; padding: 6px;"></label>
                        <button class="btn-primary" onclick="triggerGradeChange()">Save Mark (Fire Trigger)</button>
                        <button class="btn-primary" style="background: #64748b;" onclick="loadAuditLogs()">Refresh Audit Log</button>
                    </div>
                </div>

                <!-- Trigger Source Inspection Box -->
                <div class="query-inspector" style="display: block; margin-bottom: 20px;">
                    <div class="inspector-title">&#128269; Underlying Database Trigger Code (Auto-fires inside DB engine)</div>
                    <div class="code-box">CREATE TRIGGER trg_grades_audit_update
AFTER UPDATE ON grades
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (action_type, table_name, record_id, changed_by, old_value, new_value, timestamp)
    VALUES (
        'UPDATE', 'grades', NEW.grade_id, USER(),
        CONCAT('mark=', OLD.mark, ', grade=', OLD.grade_letter),
        CONCAT('mark=', NEW.mark, ', grade=', NEW.grade_letter),
        CURRENT_TIMESTAMP
    );
END;</div>
                    <div class="query-notes">
                        * Explanation for Lecturer: The application does NOT manually write to audit_log. The database engine itself automatically executes this trigger atomically with the update transaction, ensuring 100% non-repudiation.
                    </div>
                </div>

                <h3 style="font-size: 1.1rem; margin-bottom: 12px;">Audit Log Entries (<code>audit_log</code> table)</h3>
                <div id="audit-table-wrap">Loading audit logs...</div>
            </div>
        </div>

        <!-- ========================================== -->
        <!-- TAB 4: FULL SQL SCHEMA & SOURCE VIEWER -->
        <!-- ========================================== -->
        <div id="tab-sql-source" class="tab-pane">
            <div class="card">
                <div class="card-header">
                    <h2>Full SQL Script & Access Control Definitions (`database_security.sql`)</h2>
                    <p>Show this screen to the lecturer if they ask to see the underlying schema, table definitions, and user privileges.</p>
                </div>

                <div style="margin-bottom: 14px;">
                    <a href="/download/database_security.sql" class="btn-primary" download="database_security.sql" style="text-decoration: none;">
                        &#128196; Download Full database_security.sql File
                    </a>
                </div>

                <div class="code-box" style="height: 480px; overflow-y: auto; font-size: 0.85rem;" id="sql-source-box">
                    Loading database_security.sql source code...
                </div>
            </div>
        </div>

        <!-- ========================================== -->
        <!-- TAB 5: VIVA SCRIPT & DOWNLOADS -->
        <!-- ========================================== -->
        <div id="tab-guide" class="tab-pane">
            <div class="card">
                <div class="card-header">
                    <h2>Group Presentation Speaking Breakdown & Submission Files</h2>
                    <p>Quick reference for each group member during the live panel presentation.</p>
                </div>

                <div style="background: #eff6ff; border: 1px solid #bfdbfe; padding: 18px; border-radius: 8px; margin-bottom: 20px;">
                    <h3 style="color: #1e40af; margin-bottom: 8px;">Download Official Submission Files:</h3>
                    <div style="display: flex; gap: 14px; flex-wrap: wrap;">
                        <a href="/download/presentation.pptx" class="btn-download-hero" download="BIT3360_Database_Security_Presentation.pptx">
                            &#128190; Download PowerPoint Presentation (.pptx)
                        </a>
                        <a href="/download/database_security.sql" class="btn-download-hero" style="background: #2563eb;" download="database_security.sql">
                            &#128196; Download database_security.sql
                        </a>
                        <a href="/presentation.html" target="_blank" class="btn-download-hero" style="background: #475569;">
                            &#127760; View Slides in Browser
                        </a>
                    </div>
                </div>

                <div style="display: flex; flex-direction: column; gap: 14px;">
                    <div style="background: #f0f7ff; border-left: 4px solid var(--accent); padding: 14px; border-radius: 6px;">
                        <strong>Member 1 (Introduction & Threats):</strong>
                        <p style="margin-top: 4px; font-size: 0.92rem;">Introduce ZUT Student Information System (`zut_student_records`). Explain the CIA triad (Confidentiality, Integrity, Availability) and the real-world dangers of grade tampering and SQL injection breaches.</p>
                    </div>

                    <div style="background: #f0fdf4; border-left: 4px solid var(--success); padding: 14px; border-radius: 6px;">
                        <strong>Member 2 (Defensive Concepts):</strong>
                        <p style="margin-top: 4px; font-size: 0.92rem;">Explain Role-Based Access Control (RBAC) and Least Privilege. Explain why Parameterized Queries are the gold standard defense against SQL injection (separating Code from Data).</p>
                    </div>

                    <div style="background: #fffbeb; border-left: 4px solid var(--warning); padding: 14px; border-radius: 6px;">
                        <strong>Member 3 (Architecture & Schema):</strong>
                        <p style="margin-top: 4px; font-size: 0.92rem;">Walk through the relational tables: `students` (with `nrc`), `courses`, `grades`, and `audit_log`. Explain the three user accounts: `sec_admin`, `sec_lecturer`, and `sec_student`.</p>
                    </div>

                    <div style="background: #fdf2f8; border-left: 4px solid #db2777; padding: 14px; border-radius: 6px;">
                        <strong>Member 4 (Live Demonstration):</strong>
                        <p style="margin-top: 4px; font-size: 0.92rem;">Operate this web portal live! Click Tab 1 to show the `Access Denied` error for students and reveal the underlying SQL query. Click Tab 2 to demonstrate the SQL Injection attack vs Parameterized query defense. Click Tab 3 to show the audit trail.</p>
                    </div>

                    <div style="background: #f8fafc; border-left: 4px solid #475569; padding: 14px; border-radius: 6px;">
                        <strong>Member 5 (Evaluation & Compliance):</strong>
                        <p style="margin-top: 4px; font-size: 0.92rem;">Summarize project challenges (audit overhead, permission maintenance) and highlight compliance with the <strong>Zambia Data Protection Act of 2021</strong>.</p>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <script>
        let currentRole = "admin";

        function switchTab(tabId) {
            document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
            event.target.classList.add('active');
            if (tabId === 'audit') loadAuditLogs();
            if (tabId === 'sql-source') loadSqlSource();
        }

        function setRole(role) {
            currentRole = role;
            document.querySelectorAll('.role-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('btn-role-' + role).classList.add('active');
            
            const descs = {
                "admin": "Database Administrator (DBA) - Full Access (GRANT ALL PRIVILEGES)",
                "lecturer": "Lecturer (sec_lecturer) - Grade Updating Permitted; Destructive Actions Prohibited",
                "student": "Student (sec_student) - Read-Only Access; NRC Masked; Modifications Forbidden"
            };
            document.getElementById('active-role-desc').innerText = descs[role];
            document.getElementById('rbac-alert').style.display = 'none';
            document.getElementById('rbac-inspector').style.display = 'none';
            document.getElementById('rbac-table-wrap').style.display = 'none';
        }

        function setNrc(val) {
            document.getElementById('nrc-input').value = val;
            document.getElementById('vuln-code').innerText = "SELECT * FROM students WHERE nrc = '" + val + "'";
        }

        document.getElementById('nrc-input').addEventListener('input', (e) => {
            document.getElementById('vuln-code').innerText = "SELECT * FROM students WHERE nrc = '" + e.target.value + "'";
        });

        async function runAction(action) {
            const res = await fetch('/api/rbac', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({role: currentRole, action: action})
            });
            const data = await res.json();
            const alertBox = document.getElementById('rbac-alert');
            const inspector = document.getElementById('rbac-inspector');
            const inspectorSql = document.getElementById('inspector-sql');
            const inspectorNotes = document.getElementById('inspector-notes');
            const tableWrap = document.getElementById('rbac-table-wrap');

            alertBox.style.display = 'block';
            inspector.style.display = 'block';
            inspectorSql.innerText = data.sql || "-- SQL query executed";
            inspectorNotes.innerText = "* Under-the-hood explanation: " + (data.explanation || "");

            if (data.status === 'ALLOWED') {
                alertBox.className = 'alert-box success';
                alertBox.innerHTML = `<strong>[SUCCESS - 200 OK]</strong> ${data.message}`;
                if (data.rows && data.rows.length > 0) {
                    tableWrap.style.display = 'block';
                    let html = '<table class="data-table"><thead><tr>';
                    data.columns.forEach(c => html += `<th>${c}</th>`);
                    html += '</tr></thead><tbody>';
                    data.rows.forEach(r => {
                        html += '<tr>';
                        r.forEach(cell => html += `<td>${cell}</td>`);
                        html += '</tr>';
                    });
                    html += '</tbody></table>';
                    tableWrap.innerHTML = html;
                } else {
                    tableWrap.style.display = 'none';
                }
            } else {
                alertBox.className = 'alert-box danger';
                alertBox.innerHTML = `
                    <strong>[ACCESS DENIED - ERROR 1142 / 403 FORBIDDEN]</strong><br>
                    <span>${data.message}</span><br>
                    <small style="margin-top: 6px; display: block; opacity: 0.9;">Principle of Least Privilege enforced by Database Security Engine.</small>
                `;
                tableWrap.style.display = 'none';
            }
        }

        async function testSqli(type) {
            const val = document.getElementById('nrc-input').value;
            const res = await fetch('/api/sqli', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: type, input: val})
            });
            const data = await res.json();

            if (type === 'vuln') {
                const out = document.getElementById('vuln-result');
                if (data.breach) {
                    out.innerHTML = `
                        <div style="background: #fee2e2; border: 1px solid #ef4444; color: #991b1b; padding: 12px; border-radius: 6px;">
                            <strong>CRITICAL SECURITY BREACH!</strong><br>
                            Leaked ${data.rows.length} confidential student records and NRC numbers!
                        </div>
                    `;
                } else {
                    out.innerHTML = `<div style="color: #64748b; padding: 8px;">Returned ${data.rows.length} record(s).</div>`;
                }
                if (data.rows.length > 0) {
                    let html = '<table class="data-table"><thead><tr><th>ID</th><th>Student No</th><th>NRC</th><th>Name</th></tr></thead><tbody>';
                    data.rows.forEach(r => html += `<tr><td>${r[0]}</td><td>${r[1]}</td><td style="color: red; font-weight: bold;">${r[2]}</td><td>${r[3]}</td></tr>`);
                    html += '</tbody></table>';
                    out.innerHTML += html;
                }
            } else {
                const out = document.getElementById('sec-result');
                if (data.neutralized) {
                    out.innerHTML = `
                        <div style="background: #dcfce7; border: 1px solid #22c55e; color: #166534; padding: 12px; border-radius: 6px;">
                            <strong>ATTACK NEUTRALIZED!</strong><br>
                            Parameterized query evaluated input as literal text. 0 records leaked.
                        </div>
                    `;
                } else {
                    out.innerHTML = `<div style="color: #166534; padding: 8px;">Safely returned ${data.rows.length} record(s).</div>`;
                }
                if (data.rows.length > 0) {
                    let html = '<table class="data-table"><thead><tr><th>ID</th><th>Student No</th><th>NRC</th><th>Name</th></tr></thead><tbody>';
                    data.rows.forEach(r => html += `<tr><td>${r[0]}</td><td>${r[1]}</td><td style="color: green; font-weight: bold;">${r[2]}</td><td>${r[3]}</td></tr>`);
                    html += '</tbody></table>';
                    out.innerHTML += html;
                }
            }
        }

        async function triggerGradeChange() {
            const sid = document.getElementById('audit-sid').value;
            const mark = document.getElementById('audit-mark').value;
            const res = await fetch('/api/update_grade', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({student_id: sid, mark: mark})
            });
            const data = await res.json();
            alert(data.message);
            loadAuditLogs();
        }

        async function loadAuditLogs() {
            const res = await fetch('/api/audit_logs');
            const data = await res.json();
            const wrap = document.getElementById('audit-table-wrap');
            if (data.length === 0) {
                wrap.innerHTML = '<p>No audit records found.</p>';
                return;
            }
            let html = '<table class="data-table"><thead><tr><th>Log ID</th><th>Action</th><th>Table</th><th>Rec ID</th><th>Changed By</th><th>Old Value</th><th>New Value</th><th>Timestamp</th></tr></thead><tbody>';
            data.forEach(r => {
                html += `<tr><td>${r[0]}</td><td><strong style="color: var(--accent);">${r[1]}</strong></td><td>${r[2]}</td><td>${r[3]}</td><td><span style="color: #b45309; font-weight: 600;">${r[4]}</span></td><td style="color: #dc2626;">${r[5]}</td><td style="color: #16a34a;">${r[6]}</td><td>${r[7]}</td></tr>`;
            });
            html += '</tbody></table>';
            wrap.innerHTML = html;
        }

        async function loadSqlSource() {
            const res = await fetch('/api/sql_source');
            const data = await res.json();
            document.getElementById('sql-source-box').innerText = data.source;
        }

        // Initial Load
        loadAuditLogs();
    </script>
</body>
</html>
"""

# ---------------------------------------------------------------------
# 4. HTTP REQUEST HANDLER (API & STATIC DOWNLOADS)
# ---------------------------------------------------------------------
class SecurityAppHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # Download Endpoints
        if parsed.path == "/download/presentation.pptx":
            if os.path.exists(PPTX_FILE):
                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.presentationml.presentation")
                self.send_header("Content-Disposition", f'attachment; filename="{PPTX_FILE}"')
                self.send_header("Content-Length", str(os.path.getsize(PPTX_FILE)))
                self.end_headers()
                with open(PPTX_FILE, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "PPTX File Not Found")
            return

        if parsed.path == "/download/database_security.sql":
            if os.path.exists(SQL_FILE):
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Disposition", f'attachment; filename="{SQL_FILE}"')
                self.send_header("Content-Length", str(os.path.getsize(SQL_FILE)))
                self.end_headers()
                with open(SQL_FILE, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "SQL File Not Found")
            return

        if parsed.path == "/api/sql_source":
            source = ""
            if os.path.exists(SQL_FILE):
                with open(SQL_FILE, "r", encoding="utf-8") as f:
                    source = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"source": source}).encode("utf-8"))
            return

        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(INDEX_HTML.encode("utf-8"))
            return

        if parsed.path == "/api/audit_logs":
            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            cur.execute("SELECT log_id, action_type, table_name, record_id, changed_by, old_value, new_value, timestamp FROM audit_log ORDER BY log_id DESC LIMIT 15")
            rows = cur.fetchall()
            conn.close()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(rows).encode("utf-8"))
            return

        if parsed.path == "/presentation.html":
            super().do_GET()
            return

        super().do_GET()

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len).decode("utf-8")
        data = json.loads(post_body) if post_body else {}

        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/api/rbac":
            role = data.get("role", "student")
            action = data.get("action", "")
            allowed = ROLE_PERMISSIONS.get(role, {}).get("allowed", [])
            action_info = ACTION_DETAILS.get(action, {})

            if action in allowed:
                conn = sqlite3.connect(DB_FILE)
                cur = conn.cursor()
                rows = []
                cols = []

                if action == "VIEW_STUDENTS":
                    cur.execute("SELECT student_id, student_number, nrc, full_name, email FROM students")
                    rows = cur.fetchall()
                    cols = ["ID", "Student Number", "NRC", "Full Name", "Email"]
                    msg = f"Operation permitted for role '{role}'. Confidential student registry retrieved."
                elif action == "VIEW_GRADES":
                    cur.execute("SELECT s.full_name, g.course_code, g.mark, g.grade_letter, g.semester FROM grades g JOIN students s ON g.student_id = s.student_id")
                    rows = cur.fetchall()
                    cols = ["Student Name", "Course", "Mark", "Grade Letter", "Semester"]
                    msg = f"Operation permitted for role '{role}'. Grades list retrieved."
                elif action == "UPDATE_GRADE":
                    cur.execute("UPDATE grades SET mark = 95.0, grade_letter = 'A+' WHERE grade_id = 1")
                    conn.commit()
                    msg = f"Grade updated successfully by role '{role}'! The database trigger automatically recorded this change in 'audit_log'."
                elif action == "DELETE_STUDENT":
                    msg = f"Delete operation permitted for role '{role}'."
                elif action == "DROP_TABLE":
                    msg = f"Administrative command permitted for role '{role}' (Execution simulated for safety)."

                conn.close()
                res = {
                    "status": "ALLOWED",
                    "message": msg,
                    "rows": rows,
                    "columns": cols,
                    "sql": action_info.get("sql", ""),
                    "explanation": f"Executed by '{role}'. Permitted because role has GRANT privileges for this operation."
                }
            else:
                res = {
                    "status": "DENIED",
                    "message": f"Command denied to user '{role}'. Required privilege: {action}. Security Policy Violation under Principle of Least Privilege.",
                    "sql": f"-- ATTEMPTED QUERY BY USER '{role}':\n{action_info.get('sql', '')}\n-- DBMS ENGINE RESULT: ERROR 1142 (42000): Command denied to user '{role}'@'localhost'",
                    "explanation": action_info.get("why_denied", "Security privilege check failed.")
                }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

        elif parsed.path == "/api/sqli":
            stype = data.get("type", "vuln")
            val = data.get("input", "")

            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()

            if stype == "vuln":
                vuln_sql = f"SELECT student_id, student_number, nrc, full_name FROM students WHERE nrc = '{val}'"
                try:
                    cur.execute(vuln_sql)
                    rows = cur.fetchall()
                    breach = len(rows) > 1 or (len(rows) == 1 and val == "' OR '1'='1")
                    res = {"breach": breach, "rows": rows}
                except Exception as e:
                    res = {"breach": False, "rows": [], "error": str(e)}
            else:
                secure_sql = "SELECT student_id, student_number, nrc, full_name FROM students WHERE nrc = ?"
                try:
                    cur.execute(secure_sql, (val,))
                    rows = cur.fetchall()
                    neutralized = len(rows) == 0 and ("'" in val or "OR" in val)
                    res = {"neutralized": neutralized, "rows": rows}
                except Exception as e:
                    res = {"neutralized": False, "rows": [], "error": str(e)}

            conn.close()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

        elif parsed.path == "/api/update_grade":
            sid = data.get("student_id", 1)
            mark = float(data.get("mark", 85.0))
            letter = 'A+' if mark >= 85 else ('A' if mark >= 75 else ('B' if mark >= 60 else 'C'))

            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            cur.execute("UPDATE grades SET mark = ?, grade_letter = ? WHERE student_id = ? AND course_code = 'BIT3360'", (mark, letter, sid))
            conn.commit()
            conn.close()

            res = {"status": "SUCCESS", "message": f"Updated student ID {sid} mark to {mark} ({letter})! The database trigger automatically inserted an audit record."}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

# ---------------------------------------------------------------------
# 5. SERVER RUNNER
# ---------------------------------------------------------------------
def start_server():
    init_db()
    with socketserver.TCPServer(("", PORT), SecurityAppHandler) as httpd:
        print("\n" + "=" * 65)
        print(" ZAMBIA UNIVERSITY COLLEGE OF TECHNOLOGY (ZUT) ")
        print(" BIT3360: Advanced Databases - Security Prototype Portal ")
        print("=" * 65)
        print(f"\n[+] Portal running locally at: http://localhost:{PORT}")
        print("[+] Opening web browser automatically...")
        print("[*] Press Ctrl+C in this terminal window to stop the server.\n")
        try:
            webbrowser.open(f"http://localhost:{PORT}")
        except Exception:
            pass
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()
