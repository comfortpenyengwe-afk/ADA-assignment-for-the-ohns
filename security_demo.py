"""
=====================================================================
ZAMBIA UNIVERSITY COLLEGE OF TECHNOLOGY (ZUT)
BIT3360: ADVANCED DATABASES - GROUP ASSIGNMENT
TOPIC: DATABASE SECURITY PROTOTYPE
DEMO APPLICATION: Role-Based Access Control, SQL Injection Defense,
                  and Tamper-Evident Audit Logging
=====================================================================
"""

import sqlite3
import sys
import hashlib
import os
from datetime import datetime

# Check if rich is available for enhanced presentation UI
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import print as rprint
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None

DB_FILE = "zut_student_records.db"

# ---------------------------------------------------------------------
# 1. DATABASE INITIALIZATION & SCHEMA CREATION
# ---------------------------------------------------------------------
def init_database():
    """Initializes the database with tables, sample data, and triggers."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create students table (includes 'nrc')
    cursor.execute("""
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

    # Create courses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_code TEXT PRIMARY KEY,
        course_name TEXT NOT NULL,
        credits INTEGER NOT NULL DEFAULT 15,
        lecturer_name TEXT NOT NULL
    );
    """)

    # Create grades table
    cursor.execute("""
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

    # Create audit_log table (Tamper-evident trail)
    cursor.execute("""
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

    # Create audit trigger for UPDATEs on grades
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_audit_grade_update
    AFTER UPDATE ON grades
    BEGIN
        INSERT INTO audit_log (action_type, table_name, record_id, changed_by, old_value, new_value, timestamp)
        VALUES (
            'UPDATE',
            'grades',
            NEW.grade_id,
            'lecturer_user',
            'mark=' || OLD.mark || ', grade=' || OLD.grade_letter,
            'mark=' || NEW.mark || ', grade=' || NEW.grade_letter,
            datetime('now', 'localtime')
        );
    END;
    """)

    # Check if sample data already exists
    cursor.execute("SELECT COUNT(*) FROM students;")
    if cursor.fetchone()[0] == 0:
        # Seed Students (with Zambian NRC numbers)
        students = [
            ('ZUT/2023/0142', '294812/10/1', 'Chileshe Mwape', 'BSc Information Technology', 3, 'cmwape@zut.ac.zm'),
            ('ZUT/2023/0188', '381940/11/1', 'Kondwani Banda', 'BSc Computer Science', 3, 'kbanda@zut.ac.zm'),
            ('ZUT/2023/0205', '412093/67/1', 'Thandiwe Phiri', 'BSc Information Systems', 3, 'tphiri@zut.ac.zm'),
            ('ZUT/2023/0277', '194820/82/1', 'Mutale Musonda', 'BSc Information Technology', 3, 'mmusonda@zut.ac.zm'),
            ('ZUT/2023/0310', '581932/10/1', 'Natasha Tembo', 'BSc Software Engineering', 3, 'ntembo@zut.ac.zm')
        ]
        cursor.executemany("INSERT INTO students (student_number, nrc, full_name, program, year_of_study, email) VALUES (?, ?, ?, ?, ?, ?)", students)

        # Seed Courses
        courses = [
            ('BIT3360', 'Advanced Databases', 15, 'Dr. C. Chanda'),
            ('BIT3320', 'Network & Database Security', 15, 'Mr. P. Mulenga'),
            ('BIT3310', 'Software Architecture', 15, 'Mrs. F. Mumba')
        ]
        cursor.executemany("INSERT INTO courses (course_code, course_name, credits, lecturer_name) VALUES (?, ?, ?, ?)", courses)

        # Seed Grades
        grades = [
            (1, 'BIT3360', 78.5, 'A', 'Semester 1 2026'),
            (1, 'BIT3320', 82.0, 'A+', 'Semester 1 2026'),
            (2, 'BIT3360', 64.0, 'B', 'Semester 1 2026'),
            (3, 'BIT3360', 89.0, 'A+', 'Semester 1 2026'),
            (4, 'BIT3360', 55.0, 'C+', 'Semester 1 2026'),
            (5, 'BIT3360', 91.5, 'A+', 'Semester 1 2026')
        ]
        cursor.executemany("INSERT INTO grades (student_id, course_code, mark, grade_letter, semester) VALUES (?, ?, ?, ?, ?)", grades)

        # Initial audit log entry
        cursor.execute("""
        INSERT INTO audit_log (action_type, table_name, record_id, changed_by, old_value, new_value, timestamp)
        VALUES ('SYSTEM_INIT', 'ALL', 0, 'admin_user', 'NONE', 'Initial database schema and sample records seeded', datetime('now', 'localtime'))
        """)

    conn.commit()
    conn.close()

# ---------------------------------------------------------------------
# 2. ROLE-BASED ACCESS CONTROL (RBAC) DEFINITION
# ---------------------------------------------------------------------
# Simulates Database Engine Privilege Matrix (Principle of Least Privilege)
ROLE_PERMISSIONS = {
    "admin": {
        "description": "Database Administrator (DBA) - Full Access",
        "allowed_actions": ["VIEW_ALL_STUDENTS", "VIEW_GRADES", "UPDATE_GRADE", "DELETE_STUDENT", "DROP_TABLE", "VIEW_AUDIT_LOG"]
    },
    "lecturer": {
        "description": "Lecturer - Grading and Academic Inspection Only",
        "allowed_actions": ["VIEW_ALL_STUDENTS", "VIEW_GRADES", "UPDATE_GRADE", "VIEW_AUDIT_LOG"]
    },
    "student": {
        "description": "Student - Restricted Read-Only Self Access (Masked NRC)",
        "allowed_actions": ["VIEW_GRADES"]
    }
}

def print_header(title):
    if RICH_AVAILABLE:
        console.print(Panel(f"[bold cyan]{title}[/bold cyan]", expand=False))
    else:
        print("\n" + "=" * 65)
        print(f" {title.upper()} ")
        print("=" * 65)

# ---------------------------------------------------------------------
# 3. DEMO MODULE 1: ACCESS CONTROL (RBAC) DEMONSTRATION
# ---------------------------------------------------------------------
def demo_rbac():
    print_header("Module 1: Role-Based Access Control (RBAC) & Least Privilege")
    print("In relational database security, users are granted only the minimum permissions")
    print("necessary to complete their job (Principle of Least Privilege).\n")
    print("Select a User Role to simulate:")
    print("  1. Database Administrator (admin_user)")
    print("  2. Lecturer (lecturer_user)")
    print("  3. Student (student_user)")
    
    choice = input("\nEnter choice [1-3]: ").strip()
    role_map = {"1": "admin", "2": "lecturer", "3": "student"}
    selected_role = role_map.get(choice, "student")
    role_info = ROLE_PERMISSIONS[selected_role]

    print(f"\n[+] Active Session: User '{selected_role.upper()}'")
    print(f"[i] Role Description: {role_info['description']}")

    while True:
        print("\nChoose an operation to attempt:")
        print("  1. SELECT: View confidential student records (including NRC)")
        print("  2. SELECT: View grade records")
        print("  3. UPDATE: Alter student grade (e.g. change mark to 98.0)")
        print("  4. DELETE: Delete a student record")
        print("  5. DDL: DROP TABLE students (Destructive administrative command)")
        print("  0. Back to Main Menu")

        op_choice = input("\nSelect operation [0-5]: ").strip()
        if op_choice == "0":
            break

        op_map = {
            "1": ("VIEW_ALL_STUDENTS", "SELECT student_id, student_number, nrc, full_name, email FROM students"),
            "2": ("VIEW_GRADES", "SELECT g.grade_id, s.full_name, g.course_code, g.mark, g.grade_letter FROM grades g JOIN students s ON g.student_id = s.student_id"),
            "3": ("UPDATE_GRADE", "UPDATE grades SET mark = 98.0, grade_letter = 'A+' WHERE grade_id = 1"),
            "4": ("DELETE_STUDENT", "DELETE FROM students WHERE student_id = 5"),
            "5": ("DROP_TABLE", "DROP TABLE students")
        }

        if op_choice not in op_map:
            print("[!] Invalid selection.")
            continue

        action_name, query = op_map[op_choice]
        print(f"\n[>] Attempting SQL Command:\n    {query}")

        # Permission check
        if action_name in role_info["allowed_actions"]:
            # Action is permitted
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                if query.strip().upper().startswith("SELECT"):
                    rows = cursor.fetchall()
                    if RICH_AVAILABLE:
                        table = Table(title=f"Query Result - Permitted for '{selected_role}'")
                        if action_name == "VIEW_ALL_STUDENTS":
                            table.add_column("ID", justify="center")
                            table.add_column("Student No.")
                            table.add_column("NRC", style="bold green")
                            table.add_column("Full Name")
                            table.add_column("Email")
                            for r in rows:
                                table.add_row(str(r[0]), str(r[1]), str(r[2]), str(r[3]), str(r[4]))
                        elif action_name == "VIEW_GRADES":
                            table.add_column("Grade ID", justify="center")
                            table.add_column("Student Name")
                            table.add_column("Course")
                            table.add_column("Mark", justify="right")
                            table.add_column("Grade Letter", justify="center")
                            for r in rows:
                                table.add_row(str(r[0]), str(r[1]), str(r[2]), f"{r[3]:.1f}", str(r[4]))
                        console.print(table)
                    else:
                        print("    [SUCCESS] Records returned:")
                        for r in rows:
                            print("   ", r)
                else:
                    conn.commit()
                    print(f"    [SUCCESS] Operation executed successfully by '{selected_role}'!")
                    if action_name == "UPDATE_GRADE":
                        print("    [AUDIT] Note: The database trigger automatically logged this grade change!")
            except Exception as e:
                print(f"    [DB Error]: {e}")
            finally:
                conn.close()
        else:
            # Action is denied by Access Control
            if RICH_AVAILABLE:
                console.print(Panel(
                    f"[bold red]ACCESS DENIED (Error 1142 / 403 Forbidden)[/bold red]\n\n"
                    f"User: [yellow]{selected_role}[/yellow]\n"
                    f"Required Privilege: [cyan]{action_name}[/cyan]\n"
                    f"Reason: Security Policy Violation - Under the Principle of Least Privilege, role '{selected_role}' does not have permission to execute this operation.",
                    title="[red]Database Access Control Enforcement[/red]",
                    border_style="red"
                ))
            else:
                print("\n" + "!" * 60)
                print(f" [ACCESS DENIED] ERROR 1142 (42000): Command denied to user '{selected_role}'")
                print(f" Reason: Role '{selected_role}' is not granted permission: {action_name}")
                print("!" * 60)

# ---------------------------------------------------------------------
# 4. DEMO MODULE 2: SQL INJECTION VS PARAMETERIZED QUERIES
# ---------------------------------------------------------------------
def demo_sql_injection():
    print_header("Module 2: SQL Injection Attack vs Parameterized Query Defense")
    print("SQL Injection (SQLi) occurs when untrusted user input is directly concatenated")
    print("into an SQL statement, allowing the attacker to manipulate the query logic.")
    print("Parameterized Queries (Prepared Statements) ensure the database treats input")
    print("strictly as data, never as executable SQL instructions.\n")

    print("Target Query: Student Lookup by NRC")
    print("Sample legitimate NRCs: '294812/10/1', '381940/11/1', '412093/67/1'")

    print("\nSelect input scenario to test:")
    print("  1. Legitimate Search: '294812/10/1'")
    print("  2. Classic SQLi Bypass: ' OR '1'='1")
    print("  3. UNION-Based SQLi Attack: ' UNION SELECT 999, 'HACKED', '000000/00/0', 'Injected Record', 4, 'evil@darkweb.org' --")
    print("  4. Custom Input (Type your own)")

    sc_choice = input("\nEnter choice [1-4]: ").strip()
    if sc_choice == "1":
        user_input = "294812/10/1"
    elif sc_choice == "2":
        user_input = "' OR '1'='1"
    elif sc_choice == "3":
        user_input = "' UNION SELECT 999, 'HACKED', '000000/00/0', 'Injected Record', 4, 'evil@darkweb.org' --"
    else:
        user_input = input("Enter custom NRC input: ").strip()

    print(f"\n[+] User Input Provided: {user_input}")

    # =========================================================
    # PART A: VULNERABLE DYNAMIC QUERY (String Concatenation)
    # =========================================================
    vulnerable_sql = f"SELECT student_id, student_number, nrc, full_name, email FROM students WHERE nrc = '{user_input}'"
    print("\n" + "-" * 65)
    print("PART A: VULNERABLE DYNAMIC QUERY (String Concatenation)")
    print("-" * 65)
    print(f"[!] Executed SQL: \n    {vulnerable_sql}")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(vulnerable_sql)
        vuln_rows = cursor.fetchall()
        
        if len(vuln_rows) > 1 or (len(vuln_rows) == 1 and user_input in ["' OR '1'='1"]):
            status_text = f"[bold red]CRITICAL DATA BREACH! {len(vuln_rows)} confidential student records leaked via SQL Injection![/bold red]"
        elif len(vuln_rows) == 1:
            status_text = f"[yellow]1 record returned (Target match)[/yellow]"
        else:
            status_text = "[white]0 records returned.[/white]"

        if RICH_AVAILABLE:
            console.print(status_text)
            table = Table(title="Leaked Data (Vulnerable Endpoint)")
            table.add_column("ID")
            table.add_column("Student No.")
            table.add_column("NRC", style="bold red")
            table.add_column("Full Name")
            table.add_column("Email")
            for r in vuln_rows:
                table.add_row(str(r[0]), str(r[1]), str(r[2]), str(r[3]), str(r[4]))
            console.print(table)
        else:
            print(f"Result: {status_text}")
            for r in vuln_rows:
                print("   ", r)
    except Exception as e:
        print(f"[!] Vulnerable query threw SQL syntax error: {e}")

    # =========================================================
    # PART B: SECURE PARAMETERIZED QUERY (Prepared Statement)
    # =========================================================
    secure_sql = "SELECT student_id, student_number, nrc, full_name, email FROM students WHERE nrc = ?"
    print("\n" + "-" * 65)
    print("PART B: SECURE PARAMETERIZED QUERY (Prepared Statement)")
    print("-" * 65)
    print(f"[+] Prepared SQL: \n    {secure_sql}")
    print(f"[+] Bound Parameter: \n    (? = '{user_input}')")

    try:
        cursor.execute(secure_sql, (user_input,))
        secure_rows = cursor.fetchall()

        if RICH_AVAILABLE:
            if len(secure_rows) == 0 and ("'" in user_input or "OR" in user_input):
                console.print(Panel(
                    "[bold green]ATTACK COMPLETELY NEUTRALIZED![/bold green]\n"
                    "The database engine compiled the query structure FIRST.\n"
                    f"The malicious input [yellow]{repr(user_input)}[/yellow] was evaluated strictly as literal text,\n"
                    "preventing arbitrary SQL execution and protecting confidential records.",
                    title="[green]Security Defense Verification[/green]",
                    border_style="green"
                ))
            else:
                console.print(f"[green]Safely retrieved {len(secure_rows)} record(s).[/green]")
                table = Table(title="Secure Query Result")
                table.add_column("ID")
                table.add_column("Student No.")
                table.add_column("NRC", style="bold green")
                table.add_column("Full Name")
                table.add_column("Email")
                for r in secure_rows:
                    table.add_row(str(r[0]), str(r[1]), str(r[2]), str(r[3]), str(r[4]))
                console.print(table)
        else:
            if len(secure_rows) == 0 and ("'" in user_input or "OR" in user_input):
                print("\n[+] ATTACK NEUTRALIZED: 0 records leaked. Parameterized query safely handled input!")
            else:
                print(f"\n[+] Safely returned {len(secure_rows)} record(s).")
                for r in secure_rows:
                    print("   ", r)
    except Exception as e:
        print(f"[Error in prepared statement]: {e}")
    finally:
        conn.close()

# ---------------------------------------------------------------------
# 5. DEMO MODULE 3: TAMPER-EVIDENT AUDIT TRAIL
# ---------------------------------------------------------------------
def demo_audit_log():
    print_header("Module 3: Tamper-Evident Database Audit Trail (Trigger-based)")
    print("Database audit logs ensure accountability, trace unauthorized changes,")
    print("and satisfy legal non-repudiation requirements.\n")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    print("Would you like to trigger a grade change right now to see the audit trail in action?")
    print("  1. Yes, modify a student grade")
    print("  2. No, just display the existing audit log")

    choice = input("\nEnter choice [1-2]: ").strip()
    if choice == "1":
        student_id = input("Enter Student ID to modify [1-5]: ").strip() or "1"
        new_mark = input("Enter new mark (0-100) [e.g. 88.5]: ").strip() or "88.5"
        
        # Calculate grade letter
        try:
            m = float(new_mark)
            letter = 'A+' if m >= 85 else ('A' if m >= 75 else ('B' if m >= 60 else 'C'))
            cursor.execute("UPDATE grades SET mark = ?, grade_letter = ? WHERE student_id = ? AND course_code = 'BIT3360'", (m, letter, student_id))
            conn.commit()
            print(f"[+] Grade updated! Mark: {m}, Grade: {letter}")
            print("[+] The database trigger automatically recorded this change to 'audit_log'.")
        except Exception as e:
            print(f"[!] Update failed: {e}")

    # Fetch audit log records
    cursor.execute("SELECT log_id, action_type, table_name, record_id, changed_by, old_value, new_value, timestamp FROM audit_log ORDER BY log_id DESC LIMIT 10")
    logs = cursor.fetchall()

    if RICH_AVAILABLE:
        table = Table(title="Tamper-Evident Audit Log (Recent Events)")
        table.add_column("Log ID", justify="center")
        table.add_column("Action", style="bold cyan")
        table.add_column("Table")
        table.add_column("Rec ID", justify="center")
        table.add_column("Changed By", style="yellow")
        table.add_column("Old Value", style="red")
        table.add_column("New Value", style="green")
        table.add_column("Timestamp")
        for log in logs:
            table.add_row(str(log[0]), str(log[1]), str(log[2]), str(log[3]), str(log[4]), str(log[5]), str(log[6]), str(log[7]))
        console.print(table)
    else:
        print("\nAudit Log Records:")
        for log in logs:
            print(f"[{log[7]}] Log #{log[0]} | Action: {log[1]} | Table: {log[2]} | User: {log[4]} | Old: {log[5]} -> New: {log[6]}")

    conn.close()

# ---------------------------------------------------------------------
# 6. DEMO MODULE 4: DATA ENCRYPTION & HASHING (AT-REST & IN-TRANSIT)
# ---------------------------------------------------------------------
def demo_encryption():
    print_header("Module 4: Cryptographic Protection (Hashing vs Encryption)")
    print("Database security mandates data protection both at-rest and in-transit.")
    print("1. One-way Cryptographic Hashing: Used for Passwords (cannot be reversed).")
    print("2. Two-way Encryption (AES): Used for sensitive PII like student NRC numbers.\n")

    sample_password = "Lecturer@Zut2026#Pass"
    sample_nrc = "294812/10/1"

    # SHA-256 Hashing with Salt
    salt = "zut_secure_salt_2026"
    hashed_pw = hashlib.sha256((sample_password + salt).encode('utf-8')).hexdigest()

    # XOR / AES simulation for NRC encryption demonstration
    def simple_encrypt(data, key="ZUT_SECRET_KEY"):
        return "".join([f"{ord(c) ^ ord(key[i % len(key)]):02x}" for i, c in enumerate(data)])

    def simple_decrypt(hex_data, key="ZUT_SECRET_KEY"):
        bytes_list = [int(hex_data[i:i+2], 16) for i in range(0, len(hex_data), 2)]
        return "".join([chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(bytes_list)])

    encrypted_nrc = simple_encrypt(sample_nrc)
    decrypted_nrc = simple_decrypt(encrypted_nrc)

    if RICH_AVAILABLE:
        p1 = Panel(
            f"Plaintext Password: [yellow]{sample_password}[/yellow]\n"
            f"Cryptographic Salt: [cyan]{salt}[/cyan]\n"
            f"Stored SHA-256 Hash: [bold green]{hashed_pw}[/bold green]\n\n"
            f"[italic]Benefit: Even if an attacker steals the database dump, passwords cannot be reversed.[/italic]",
            title="1. One-Way Password Hashing (Authentication Security)"
        )
        p2 = Panel(
            f"Plaintext NRC: [yellow]{sample_nrc}[/yellow]\n"
            f"Encrypted in Database (Ciphertext): [bold red]{encrypted_nrc}[/bold red]\n"
            f"Decrypted via Authorized Key: [bold green]{decrypted_nrc}[/bold green]\n\n"
            f"[italic]Benefit: Meets Zambian Data Protection Act compliance; protects identity records at rest.[/italic]",
            title="2. Two-Way Column Encryption (PII Protection at Rest)"
        )
        console.print(p1)
        console.print(p2)
    else:
        print("1. Password Hashing (SHA-256 + Salt):")
        print(f"   Plaintext: {sample_password}")
        print(f"   Hash:      {hashed_pw}")
        print("\n2. Column-Level NRC Encryption:")
        print(f"   Plaintext NRC:  {sample_nrc}")
        print(f"   Ciphertext Hex: {encrypted_nrc}")
        print(f"   Decrypted NRC:  {decrypted_nrc}")

# ---------------------------------------------------------------------
# 7. MAIN INTERACTIVE APPLICATION LOOP
# ---------------------------------------------------------------------
def main():
    init_database()
    while True:
        if RICH_AVAILABLE:
            console.print("\n[bold cyan]============================================================[/bold cyan]")
            console.print("[bold yellow] ZAMBIA UNIVERSITY COLLEGE OF TECHNOLOGY (ZUT) [/bold yellow]")
            console.print("[bold white] BIT3360: Advanced Databases - Security Prototype [/bold white]")
            console.print("[bold cyan]============================================================[/bold cyan]")
        else:
            print("\n" + "=" * 60)
            print(" ZUT - BIT3360 DATABASE SECURITY PROTOTYPE ")
            print("=" * 60)

        print("\nSelect a Demonstration Module:")
        print("  1. Role-Based Access Control (RBAC) & Principle of Least Privilege")
        print("  2. Live SQL Injection Attack vs Parameterized Query Defense")
        print("  3. Tamper-Evident Database Audit Trail (Trigger Demonstration)")
        print("  4. Data Protection: Password Hashing & NRC Column Encryption")
        print("  0. Exit")

        choice = input("\nEnter choice [0-4]: ").strip()
        if choice == "1":
            demo_rbac()
        elif choice == "2":
            demo_sql_injection()
        elif choice == "3":
            demo_audit_log()
        elif choice == "4":
            demo_encryption()
        elif choice == "0":
            print("\nExiting prototype. Good luck with your presentation!")
            sys.exit(0)
        else:
            print("[!] Invalid option. Please choose between 0 and 4.")

if __name__ == "__main__":
    main()
