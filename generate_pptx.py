"""
=====================================================================
ZAMBIA UNIVERSITY COLLEGE OF TECHNOLOGY (ZUT)
BIT3360: ADVANCED DATABASES - PPTX GENERATOR (SIMPLIFIED & EXPLANATORY)
Group: Comfort Penyengwe, Gideon Namuya, Lubuto Matambo, Lamla Mwanza
Generates: BIT3360_Database_Security_Presentation.pptx
=====================================================================
"""

import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette
    DARK_BLUE   = RGBColor(15, 23, 42)      # #0f172a
    ACCENT_BLUE = RGBColor(37, 99, 235)     # #2563eb
    TEXT_DARK   = RGBColor(30, 41, 59)      # #1e293b
    TEXT_MUTED  = RGBColor(100, 116, 139)   # #64748b
    BG_CARD     = RGBColor(248, 250, 252)   # #f8fafc
    WHITE       = RGBColor(255, 255, 255)
    RED         = RGBColor(220, 38, 38)
    GREEN       = RGBColor(22, 163, 74)
    AMBER       = RGBColor(217, 119, 6)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, section_tag, slide_title, subtitle_text):
        box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.3))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Section Tag
        p_tag = tf.paragraphs[0]
        p_tag.text = section_tag.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = ACCENT_BLUE

        # Title
        p_title = tf.add_paragraph()
        p_title.text = slide_title
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = DARK_BLUE
        p_title.space_before = Pt(3)

        # Subtitle
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_before = Pt(2)

    def add_card(slide, left, top, width, height, title, explanation, bullet_points, border_color=None, bg_color=BG_CARD):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(2)
        else:
            shape.line.color.rgb = RGBColor(226, 232, 240)
            shape.line.width = Pt(1)

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_top = Inches(0.2)
        tf.margin_right = Inches(0.25)

        # Title
        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(14)
        p_title.font.bold = True
        p_title.font.color.rgb = DARK_BLUE
        p_title.alignment = PP_ALIGN.LEFT

        # Simple Explanation
        if explanation:
            p_exp = tf.add_paragraph()
            p_exp.text = f"💡 In simple terms: {explanation}"
            p_exp.font.size = Pt(11)
            p_exp.font.bold = True
            p_exp.font.color.rgb = ACCENT_BLUE
            p_exp.space_before = Pt(4)

        # Bullets
        for b in bullet_points:
            p_b = tf.add_paragraph()
            p_b.text = f"• {b}"
            p_b.font.size = Pt(11.5)
            p_b.font.color.rgb = TEXT_DARK
            p_b.space_before = Pt(5)

    def add_notes(slide, notes):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes

    # =========================================================
    # SLIDE 1: Title Slide (Featuring the 4 Group Members)
    # Note: Clean list of names and student IDs only (no role labels on slide)
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = DARK_BLUE
    bg.line.fill.background()

    # Title & Header
    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(2.2))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0

    p0 = tf_title.paragraphs[0]
    p0.text = "ZAMBIA UNIVERSITY COLLEGE OF TECHNOLOGY (ZUT)"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(56, 189, 248)

    p1 = tf_title.add_paragraph()
    p1.text = "BIT3360: Advanced Databases — Group Assignment"
    p1.font.size = Pt(15)
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(4)

    p2 = tf_title.add_paragraph()
    p2.text = "Database Security & Practical Protection Prototype"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = WHITE
    p2.space_before = Pt(8)

    p3 = tf_title.add_paragraph()
    p3.text = "Demonstrating Role-Based Access Control, SQL Injection Defense & Audit Logging"
    p3.font.size = Pt(15)
    p3.font.color.rgb = RGBColor(203, 213, 225)
    p3.space_before = Pt(6)

    # 4 Group Member Cards (Names & IDs only, exactly as requested)
    members_data = [
        ("Comfort Penyengwe", "Student ID: 2410098", Inches(0.8), Inches(3.6)),
        ("Gideon Namuya", "Student ID: 2410149", Inches(6.8), Inches(3.6)),
        ("Lubuto Matambo", "Student ID: 2410171", Inches(0.8), Inches(5.2)),
        ("Lamla Mwanza", "Student ID: 2410205", Inches(6.8), Inches(5.2))
    ]

    for name, sid, left, top in members_data:
        m_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.7), Inches(1.3))
        m_card.fill.solid()
        m_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
        m_card.line.color.rgb = ACCENT_BLUE
        m_card.line.width = Pt(1.5)

        m_tf = m_card.text_frame
        m_tf.word_wrap = True
        m_tf.margin_left = Inches(0.25)
        m_tf.margin_top = Inches(0.2)
        m_tf.margin_right = Inches(0.25)

        p_name = m_tf.paragraphs[0]
        p_name.text = name
        p_name.font.size = Pt(17)
        p_name.font.bold = True
        p_name.font.color.rgb = WHITE

        p_id = m_tf.add_paragraph()
        p_id.text = sid
        p_id.font.size = Pt(13)
        p_id.font.bold = True
        p_id.font.color.rgb = RGBColor(56, 189, 248)
        p_id.space_before = Pt(3)

    add_notes(s1, "Comfort Penyengwe (Intro): 'Good morning Lecturer and colleagues. Today our group—Comfort Penyengwe, Gideon Namuya, Lubuto Matambo, and Lamla Mwanza—presents our project on Database Security under BIT3360. Databases hold an institution's most sensitive information. We will explain how databases are attacked, how we defend them, and show you a working prototype we built for the ZUT Student Information System.'")

    # =========================================================
    # SLIDE 2: What is Database Security? (PART 1: COMFORT)
    # =========================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Part 1: Foundations", "What is Database Security? (The CIA Triad Explained)", "Why database security is about protecting data from being seen, changed, or destroyed.")
    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.7),
             "1. Confidentiality",
             "Only authorized eyes can see the data.",
             [
                 "Protects sensitive identity info like student NRC numbers and emails.",
                 "Prevents data leaks to unauthorized students or outside hackers.",
                 "Enforced using user permissions and masked views."
             ], border_color=ACCENT_BLUE)
    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.7),
             "2. Integrity",
             "Data cannot be secretly changed or faked.",
             [
                 "Ensures exam marks and academic records remain 100% genuine.",
                 "Stops students or rogue actors from tampering with grades.",
                 "Enforced using triggers, constraints, and audit logs."
             ], border_color=ACCENT_BLUE)
    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.7),
             "3. Availability",
             "The system is up and working when needed.",
             [
                 "Ensures lecturers and students can access records during exams.",
                 "Prevents malicious users from dropping tables or crashing the server.",
                 "Enforced using backups, read replicas, and privilege limits."
             ], border_color=ACCENT_BLUE)
    add_notes(s2, "Comfort Penyengwe: 'To understand database security, we look at the CIA Triad: Confidentiality, Integrity, and Availability. Confidentiality means student NRCs stay private. Integrity means nobody can secretly change their grade from 50 to 90. Availability means the database is always online. Real security isn't just one firewall; it has to be built inside the database engine itself.'")

    # =========================================================
    # SLIDE 3: Common Threats (PART 1: COMFORT)
    # =========================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Part 1: Threat Landscape", "How Databases Get Hacked (Common Threats)", "The two biggest dangers in database systems: SQL Injection and Privilege Abuse.")
    add_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.7),
             "1. SQL Injection (The #1 Web Attack)",
             "Trick the database into running the hacker's code.",
             [
                 "Happens when an application glues user input directly into an SQL query.",
                 "Example: In an NRC search box, typing: ' OR '1'='1",
                 "The database evaluates '1'='1' as TRUE for every single row.",
                 "Result: The entire student registry, NRCs, and grades are leaked on screen!"
             ], border_color=RED)
    add_card(s3, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.7),
             "2. Privilege Abuse & Insider Threats",
             "Giving regular users too much database power.",
             [
                 "If a lecturer or student account has DROP or DELETE permissions, one mistake or rogue action destroys the entire university database.",
                 "Missing Audit Trail: If someone alters a grade, but there is no audit log, nobody knows who did it.",
                 "Weak Passwords: Default root passwords or passwords stored in plaintext."
             ], border_color=RED)
    add_notes(s3, "Comfort Penyengwe: 'The most famous database vulnerability is SQL Injection. If an application takes user text and glues it into a query, an attacker can input quotes and SQL keywords to trick the database into dumping all records. The second danger is giving regular users too much power—if a student can run an UPDATE command on the grades table, the integrity of the university is broken. Now, Gideon Namuya will explain how we defend against these threats.'")

    # =========================================================
    # SLIDE 4: Access Control & Least Privilege (PART 2: GIDEON)
    # =========================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Part 2: Defensive Controls", "Role-Based Access Control & The Principle of Least Privilege", "Users should only be able to do what their specific job requires—nothing more.")
    add_card(s4, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.7),
             "Administrator (DBA)",
             "Full system control for maintenance.",
             [
                 "Account: sec_admin",
                 "Permissions: ALL PRIVILEGES.",
                 "Can create tables, manage backups, and configure user accounts.",
                 "Only given to authorized IT database administrators."
             ], border_color=GREEN)
    add_card(s4, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.7),
             "Lecturer (Academic Staff)",
             "Can grade students, but cannot destroy data.",
             [
                 "Account: sec_lecturer",
                 "Permissions: SELECT, INSERT, UPDATE on grades.",
                 "CANNOT drop tables (DROP denied).",
                 "CANNOT delete student accounts (DELETE denied)."
             ], border_color=AMBER)
    add_card(s4, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.7),
             "Student (Undergraduate)",
             "Strict read-only access to their own grades.",
             [
                 "Account: sec_student",
                 "Permissions: SELECT on masked View only.",
                 "CANNOT view peer NRC numbers.",
                 "CANNOT update or alter any mark (Error 1142 Access Denied)."
             ], border_color=RED)
    add_notes(s4, "Gideon Namuya: 'Thank you, Comfort. To defend against privilege abuse, we use Role-Based Access Control under the Principle of Least Privilege. In simple terms: an Admin can do everything; a Lecturer can only enter and update marks; and a Student can only view their own grades on a masked view. Even if a student tries to hack the system and run an UPDATE command, the database engine blocks it immediately with an Access Denied error.'")

    # =========================================================
    # SLIDE 5: Parameterized Queries (PART 2: GIDEON)
    # =========================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Part 2: Defensive Controls", "How Parameterized Queries Stop SQL Injection Completely", "The golden rule of database security: Treat user input as data, never as executable code.")
    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.7),
             "Vulnerable: String Concatenation",
             "The database gets tricked into running user text as commands.",
             [
                 "Code: SELECT * FROM students WHERE nrc = 'INPUT'",
                 "User types: ' OR '1'='1",
                 "What runs: WHERE nrc = '' OR '1'='1'",
                 "Why it breaks: The quotes close the string, and OR '1'='1 becomes actual executable SQL logic.",
                 "Result: Every student record and NRC is leaked!"
             ], border_color=RED)
    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.7),
             "Secure: Parameterized Prepared Statement",
             "The database engine compiles the query FIRST, before input arrives.",
             [
                 "Code: cursor.execute('SELECT * FROM students WHERE nrc = ?', (input,))",
                 "User types: ' OR '1'='1",
                 "What runs: Searches literally for a student whose NRC text is \"' OR '1'='1\".",
                 "Why it works: The question mark ? is a placeholder. Input is strictly data literal.",
                 "Result: 0 records found. Attack 100% neutralized!"
             ], border_color=GREEN)
    add_notes(s5, "Gideon Namuya: 'Now look at why Parameterized Queries are the ultimate defense against SQL Injection. In vulnerable code, you glue strings together, so the attacker's quotes become SQL commands. But in a Parameterized Query—or Prepared Statement—the database engine compiles the SQL blueprint first. When the attack payload arrives, the database treats it purely as plain text. It searches for an NRC containing quotes, finds nothing, and the attack fails completely.'")

    # =========================================================
    # SLIDE 6: Encryption & Audit Logging (PART 2: GIDEON)
    # =========================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Part 2: Defensive Controls", "Data Encryption & Tamper-Evident Audit Logging", "How we protect data on disk and catch anyone who tries to alter marks.")
    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.7),
             "1. Cryptographic Protection (Hashing & Encryption)",
             "If the database is stolen, the data cannot be read.",
             [
                 "Password Hashing: Passwords are saved as one-way SHA-256 cryptographic hashes with salt. Even DBAs cannot reverse them.",
                 "Data in Transit: Encrypted with TLS/SSL so network eavesdroppers cannot see traffic.",
                 "Data at Rest: Sensitive personal identity columns like NRC numbers can be encrypted so raw files on hard drives are protected."
             ], border_color=ACCENT_BLUE)
    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.7),
             "2. Automated Database Triggers (Audit Log)",
             "A security camera recording every change in the database.",
             [
                 "What if a lecturer alters a student's grade from 40 to 85?",
                 "We created an automatic Trigger: trg_grades_audit_update.",
                 "Every time an UPDATE occurs, the trigger silently records: Who made the change, the exact timestamp, the old mark, and the new mark.",
                 "Guarantees Non-Repudiation: No one can deny what they did."
             ], border_color=GREEN)
    add_notes(s6, "Gideon Namuya: 'Our third layer of defense is Encryption and Auditing. We hash passwords so they cannot be reversed, and encrypt network connections. And to stop insider fraud, we created an automatic database trigger on the grades table. If a lecturer changes a grade, the database automatically logs who did it, the old score, and the new score. Now, Lubuto Matambo will explain the industry tools and our prototype architecture.'")

    # =========================================================
    # SLIDE 7: Industry Tools & Systems (PART 3: LUBUTO)
    # =========================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Part 3: Industry & Design", "Enterprise Database Security Systems & Tools", "How major enterprises and tech companies implement these controls in production.")
    add_card(s7, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.7),
             "MySQL Enterprise Security",
             "Commercial features built into MySQL.",
             [
                 "MySQL Enterprise Firewall: Blocks SQL injection in real time by learning normal query patterns.",
                 "MySQL Enterprise Audit: Government-grade compliance auditing.",
                 "Transparent Data Encryption (TDE): Automatically encrypts database files on disk."
             ])
    add_card(s7, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.7),
             "PostgreSQL Security Suite",
             "Advanced open-source security controls.",
             [
                 "Row-Level Security (RLS): Allows students to only see rows matching their own ID.",
                 "pg_audit: Detailed logging of all DDL and DML commands.",
                 "SCRAM-SHA-256: Modern client-server authentication."
             ])
    add_card(s7, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.7),
             "Vault & Activity Monitoring",
             "Protecting passwords and monitoring traffic.",
             [
                 "HashiCorp Vault: Generates temporary database passwords that expire automatically (no hardcoded passwords).",
                 "IBM Guardium / Imperva: Monitors all database traffic and raises alerts if unusual queries occur."
             ])
    add_notes(s7, "Lubuto Matambo: 'Thank you, Gideon. In large corporations, database security is powered by enterprise tools. MySQL Enterprise provides an automated Firewall that stops SQL injection, and Transparent Data Encryption to protect disks. PostgreSQL has Row-Level Security so users only see their own rows. And tools like HashiCorp Vault automatically rotate passwords so developers never have to write hardcoded credentials in code.'")

    # =========================================================
    # SLIDE 8: Benefits & Real-World Challenges (PART 3: LUBUTO)
    # =========================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Part 3: Industry & Design", "Benefits, Trade-offs & The Zambia Data Protection Act", "Balancing high security with system speed, usability, and legal requirements.")
    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.7),
             "Key Benefits & Legal Compliance",
             "Keeping the university reputable and compliant with law.",
             [
                 "Guarantees Academic Integrity: Prevents unauthorized grade inflation or bribery.",
                 "The Zambia Data Protection Act No. 3 of 2021: Legally requires universities handling personal records (like NRC numbers) to enforce technical security.",
                 "Containment: If a student account is compromised, the attacker still cannot drop tables or view peer NRCs."
             ], border_color=GREEN)
    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.7),
             "Real-World Challenges & Trade-offs",
             "Security always has costs you have to manage.",
             [
                 "Performance Overhead: Running triggers on every update and encrypting columns uses more CPU and disk I/O.",
                 "Management Complexity: Maintaining different user roles and permissions takes time as the university grows.",
                 "The Human Factor: Technology cannot stop people from writing passwords on sticky notes or falling for phishing."
             ], border_color=AMBER)
    add_notes(s8, "Lubuto Matambo: 'Security delivers massive benefits. In Zambia, under the Data Protection Act of 2021, any institution holding citizen records like NRC numbers is legally mandated to protect them. But security comes with trade-offs: encrypting columns and running audit triggers uses more server CPU, and permissions must be managed carefully. Plus, security software cannot fix human mistakes like sharing passwords.'")

    # =========================================================
    # SLIDE 9: Our Prototype Architecture (PART 3: LUBUTO)
    # =========================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Part 3: Industry & Design", "Our Prototype Design: ZUT Student Records System", "How our database tables, roles, and security measures fit together.")
    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.7),
             "Database Schema & Tables",
             "Models real academic university entities.",
             [
                 "students: student_id, student_number, nrc, full_name, program, year_of_study, email.",
                 "courses: course_code (e.g. BIT3360), course_name, credits, lecturer_name.",
                 "grades: grade_id, student_id, course_code, mark, grade_letter, semester.",
                 "audit_log: log_id, action_type, table_name, record_id, changed_by, old_value, new_value, timestamp."
             ], border_color=ACCENT_BLUE)
    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.7),
             "The 3 Implemented Defenses",
             "Proving the concepts through working code.",
             [
                 "1. RBAC Matrix: sec_admin (Full), sec_lecturer (Grades only), sec_student (Sanitized view, NRC masked).",
                 "2. Parameterized Query Engine: Protects the student search box against SQL injection attacks.",
                 "3. Automated Audit Trigger: Automatically records grade changes into audit_log for non-repudiation.",
                 "Now, Lamla Mwanza will walk you through the live demonstration of this system."
             ], border_color=GREEN)
    add_notes(s9, "Lubuto Matambo: 'For our practical assignment, we built the ZUT Student Records System (zut_student_records). Our database models students with their NRCs, courses, grades, and an automated audit log. We created 3 distinct user roles with exact GRANT permissions and built an interactive web portal to demonstrate the security controls in real time. I will now hand over to Lamla Mwanza for the live demonstration.'")

    # =========================================================
    # SLIDE 10: Live Demo - Access Control (PART 4: LAMLA)
    # =========================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Part 4: Live Demonstration", "Live Demonstration: Role-Based Access Control in Action", "Testing what each user can and cannot do live in our prototype.")
    add_card(s10, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.7),
             "Test 1: Administrator",
             "Has full DBA privileges.",
             [
                 "Action: View students & NRCs.",
                 "Result: [SUCCESS] Can view all records and manage tables.",
                 "Action: View audit trail.",
                 "Result: [SUCCESS] Complete inspection access."
             ], border_color=GREEN)
    add_card(s10, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.7),
             "Test 2: Lecturer",
             "Allowed to grade, blocked from destruction.",
             [
                 "Action: Update grade mark.",
                 "Result: [SUCCESS] Grade updated; audit trigger fired.",
                 "Action: DROP TABLE students.",
                 "Result: [ACCESS DENIED Error 1142] Blocked by DB engine."
             ], border_color=AMBER)
    add_card(s10, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.7),
             "Test 3: Student",
             "Least privilege enforced.",
             [
                 "Action: View grades view.",
                 "Result: [SUCCESS] Can see marks on masked view.",
                 "Action: Alter grade mark.",
                 "Result: [ACCESS DENIED Error 1142] Blocked immediately."
             ], border_color=RED)
    add_notes(s10, "Lamla Mwanza: 'Thank you, Lubuto. Now let us look at our live demonstration. On screen in our web portal, when logged in as a Lecturer and we update a student mark, it succeeds because lecturers have UPDATE permissions. But if the lecturer tries to DROP the table or delete records, the database engine returns Error 1142: Access Denied. Similarly, when logged in as a student, any attempt to change a grade or view peer NRC numbers is rejected immediately.'")

    # =========================================================
    # SLIDE 11: Live Demo - SQLi & Audit (PART 4: LAMLA)
    # =========================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Part 4: Live Demonstration", "Live Demonstration: SQL Injection Attack vs Defense & Audit Log", "Proving how prepared statements neutralize attacks and triggers record changes.")
    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.7),
             "SQL Injection Attack vs Defense",
             "Testing payload: ' OR '1'='1 in the NRC search box.",
             [
                 "Test A (Vulnerable Query): String concatenation causes the WHERE clause to evaluate as TRUE for every student. Critical Data Breach! All confidential NRCs and records are dumped.",
                 "Test B (Parameterized Query): The database engine compiles the query template first. The payload is treated strictly as plain literal text. 0 records leaked. Attack completely neutralized!"
             ], border_color=ACCENT_BLUE)
    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.7),
             "Tamper-Evident Audit Trail",
             "Inspecting the audit_log table live.",
             [
                 "When the lecturer modified student 1's mark from 78.50 to 95.00, our database trigger automatically fired.",
                 "Querying audit_log shows: Log ID #2 | UPDATE | Changed By: sec_lecturer | Old Mark: 78.50 | New Mark: 95.00 | Exact Timestamp.",
                 "Provides 100% accountability and non-repudiation."
             ], border_color=GREEN)
    add_notes(s11, "Lamla Mwanza: 'Next, we test our additional security measures. In our search box, we test the injection payload: single quote OR 1 equals 1. In the vulnerable query, this dumps all student NRCs. But in our Parameterized Query, the database treats it as literal text, and zero records are leaked. Finally, we look at the audit log: the database trigger captured the exact timestamp, the user ID, the old score, and the new score.'")

    # =========================================================
    # SLIDE 12: Challenges, Conclusion & References (PART 4: LAMLA)
    # =========================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Part 4: Conclusion", "Challenges Encountered, Conclusion & References", "What we learned building this prototype and the academic sources we consulted.")
    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.7),
             "Challenges & How We Solved Them",
             "Practical lessons learned during development.",
             [
                 "Challenge 1: Capturing User Identity in Triggers — Solved by passing session context so the audit log records the actual user rather than a generic pool account.",
                 "Challenge 2: Usability vs Least Privilege — Solved by creating sanitized Views (vw_student_grades) so students can view grades without exposing confidential NRC numbers.",
                 "Challenge 3: Portability — Built a zero-dependency web portal running locally on Python so it runs seamlessly on any machine."
             ], border_color=AMBER)
    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.7),
             "Conclusion & References",
             "Key takeaway for modern database systems.",
             [
                 "Takeaway: Proactive database security—combining RBAC, Parameterized Queries, and Audit Logging—is essential to protect institutional integrity and comply with the Zambia Data Protection Act.",
                 "References:",
                 "1. Silberschatz, Korth, Sudarshan (2020). Database System Concepts (7th ed.).",
                 "2. OWASP Top 10 (2021). A03: Injection Flaws.",
                 "3. Government of Zambia. The Data Protection Act, No. 3 of 2021.",
                 "4. Oracle. MySQL 8.0 Reference Manual: Security & Access Management."
             ], border_color=GREEN)
    add_notes(s12, "Lamla Mwanza: 'In conclusion, database security cannot be an afterthought. By combining Role-Based Access Control, Parameterized Queries, and automated triggers, we achieved confidentiality, integrity, and compliance with Zambian law. This concludes our presentation. Comfort, Gideon, Lubuto, and I are now ready to answer any questions from the panel. Thank you!'")

    output_filename = "BIT3360_Database_Security_Presentation.pptx"
    try:
        prs.save(output_filename)
        print(f"[+] Successfully generated official PPTX: {output_filename}")
    except PermissionError:
        alt_filename = "BIT3360_Database_Security_Presentation_Updated.pptx"
        prs.save(alt_filename)
        print(f"[!] '{output_filename}' is currently open in PowerPoint!")
        print(f"[+] Saved updated copy to: {alt_filename}")

if __name__ == "__main__":
    create_deck()
