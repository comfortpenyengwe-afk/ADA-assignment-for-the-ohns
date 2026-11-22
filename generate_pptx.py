"""
=====================================================================
ZAMBIA UNIVERSITY COLLEGE OF TECHNOLOGY (ZUT)
BIT3360: ADVANCED DATABASES - PPTX GENERATOR (CYBERSECURITY DARK THEME)
Exact visual style from the Windows Security Presentation:
- Rich Deep Midnight Slate Background (#0F172A) across all slides
- Dark Slate Rounded Cards (#1E293B) with glowing accent borders
- Electric Cyan (#38BDF8), Mint (#34D399), Rose (#F87171), Amber (#FBBF24)
- High-contrast crisp White (#F8FAFC) & Silver (#CBD5E1) typography
- Group: Comfort Penyengwe, Gideon Namuya, Lubuto Matambo, Lamla Mwanza
=====================================================================
"""

import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette: Exact Windows Security Dark Cyber Aesthetic
    DARK_BG      = RGBColor(15, 23, 42)      # #0f172a (Deep Midnight Slate / Navy)
    CARD_BG      = RGBColor(30, 41, 59)      # #1e293b (Dark Charcoal Slate Card)
    BORDER_MUTED = RGBColor(51, 65, 85)      # #334155 (Subtle Slate Border)
    CYAN_GLOW    = RGBColor(56, 189, 248)    # #38bdf8 (Sky / Cyan Blue)
    MINT_GREEN   = RGBColor(52, 211, 153)    # #34d399 (Vibrant Emerald / Mint Green)
    ROSE_RED     = RGBColor(248, 113, 113)   # #f87171 (Rose / Coral Red)
    AMBER_GOLD   = RGBColor(251, 191, 36)    # #fbbf24 (Warm Amber / Gold)
    VIOLET_PURP  = RGBColor(167, 139, 250)   # #a78bfa (Electric Purple / Violet)
    ROYAL_BLUE   = RGBColor(96, 165, 250)    # #60a5fa (Bright Azure Blue)

    TEXT_WHITE   = RGBColor(248, 250, 252)   # #f8fafc (Pure White / Ghost White)
    TEXT_SILVER  = RGBColor(203, 213, 225)   # #cbd5e1 (Readable Light Slate Body)
    TEXT_MUTED   = RGBColor(148, 163, 184)   # #94a3b8 (Muted Slate / Subtitles)
    FOOTER_MUTED = RGBColor(100, 116, 139)   # #64748b

    blank_layout = prs.slide_layouts[6]

    def create_content_slide(slide_num, section_tag, slide_title, subtitle_text):
        slide = prs.slides.add_slide(blank_layout)

        # 1. Full Dark Background (#0F172A)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_BG
        bg.line.fill.background()

        # 2. Header Text Box (Clean, sleek cyber header)
        box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.15))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_tag = tf.paragraphs[0]
        p_tag.text = section_tag.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = CYAN_GLOW

        p_title = tf.add_paragraph()
        p_title.text = slide_title
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE
        p_title.space_before = Pt(3)

        p_sub = tf.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_before = Pt(3)

        # 3. Horizontal accent divider under header
        header_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.62), Inches(11.733), Inches(0.02))
        header_line.fill.solid()
        header_line.fill.fore_color.rgb = BORDER_MUTED
        header_line.line.fill.background()

        # 4. Bottom Footer Line & Metadata
        footer_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.92), Inches(11.733), Inches(0.02))
        footer_line.fill.solid()
        footer_line.fill.fore_color.rgb = BORDER_MUTED
        footer_line.line.fill.background()

        # Footer Left
        footer_box_left = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(8.5), Inches(0.4))
        f_tf_left = footer_box_left.text_frame
        f_tf_left.margin_left = f_tf_left.margin_top = f_tf_left.margin_right = f_tf_left.margin_bottom = 0
        p_foot = f_tf_left.paragraphs[0]
        p_foot.text = "ZAMBIA UNIVERSITY COLLEGE OF TECHNOLOGY (ZUT)  •  BIT3360: ADVANCED DATABASES"
        p_foot.font.size = Pt(9.5)
        p_foot.font.bold = True
        p_foot.font.color.rgb = FOOTER_MUTED

        # Footer Right (Slide Number)
        footer_box_right = slide.shapes.add_textbox(Inches(9.5), Inches(7.0), Inches(3.033), Inches(0.4))
        f_tf_right = footer_box_right.text_frame
        f_tf_right.margin_left = f_tf_right.margin_top = f_tf_right.margin_right = f_tf_right.margin_bottom = 0
        p_num = f_tf_right.paragraphs[0]
        p_num.text = f"Slide {slide_num} of 12"
        p_num.font.size = Pt(9.5)
        p_num.font.bold = True
        p_num.font.color.rgb = CYAN_GLOW
        p_num.alignment = PP_ALIGN.RIGHT

        return slide

    def add_card(slide, left, top, width, height, title, explanation, bullet_points, border_color=None, title_color=None):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = CARD_BG
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.color.rgb = BORDER_MUTED
            shape.line.width = Pt(1.0)

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
        p_title.font.color.rgb = title_color if title_color else (border_color if border_color else CYAN_GLOW)
        p_title.alignment = PP_ALIGN.LEFT

        # Simple Explanation
        if explanation:
            p_exp = tf.add_paragraph()
            r_bulb = p_exp.add_run()
            r_bulb.text = "💡 Concept: "
            r_bulb.font.size = Pt(11)
            r_bulb.font.bold = True
            r_bulb.font.color.rgb = CYAN_GLOW

            r_exp = p_exp.add_run()
            r_exp.text = explanation
            r_exp.font.size = Pt(11)
            r_exp.font.bold = True
            r_exp.font.color.rgb = TEXT_WHITE
            p_exp.space_before = Pt(4)

        # Bullets
        for b in bullet_points:
            p_b = tf.add_paragraph()
            p_b.space_before = Pt(5)

            if ":" in b:
                parts = b.split(":", 1)
                r_bullet = p_b.add_run()
                r_bullet.text = "• "
                r_bullet.font.size = Pt(11)
                r_bullet.font.bold = True
                r_bullet.font.color.rgb = border_color if border_color else CYAN_GLOW

                r_bold = p_b.add_run()
                r_bold.text = parts[0] + ":"
                r_bold.font.size = Pt(11)
                r_bold.font.bold = True
                r_bold.font.color.rgb = TEXT_WHITE

                r_text = p_b.add_run()
                r_text.text = parts[1]
                r_text.font.size = Pt(11)
                r_text.font.color.rgb = TEXT_SILVER
            else:
                r_bullet = p_b.add_run()
                r_bullet.text = "• "
                r_bullet.font.size = Pt(11)
                r_bullet.font.bold = True
                r_bullet.font.color.rgb = border_color if border_color else CYAN_GLOW

                r_text = p_b.add_run()
                r_text.text = b
                r_text.font.size = Pt(11)
                r_text.font.color.rgb = TEXT_SILVER

    def add_notes(slide, notes):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes

    # =========================================================
    # SLIDE 1: Title Slide (Group Members: Comfort, Gideon, Lubuto, Lamla)
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_BG
    bg1.line.fill.background()

    # Glowing decorative left border accent on title
    dec_line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.7), Inches(0.12), Inches(2.3))
    dec_line.fill.solid()
    dec_line.fill.fore_color.rgb = CYAN_GLOW
    dec_line.line.fill.background()

    tb_title = s1.shapes.add_textbox(Inches(1.1), Inches(0.6), Inches(11.4), Inches(2.3))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0

    p0 = tf_title.paragraphs[0]
    p0.text = "ZAMBIA UNIVERSITY COLLEGE OF TECHNOLOGY (ZUT)"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = CYAN_GLOW

    p1 = tf_title.add_paragraph()
    p1.text = "BIT3360: Advanced Databases — Group Assignment"
    p1.font.size = Pt(15)
    p1.font.color.rgb = TEXT_SILVER
    p1.space_before = Pt(4)

    p2 = tf_title.add_paragraph()
    p2.text = "Database Security & Practical Protection Prototype"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(8)

    p3 = tf_title.add_paragraph()
    p3.text = "Role-Based Access Control, SQL Injection Defense & Tamper-Evident Audit Logging"
    p3.font.size = Pt(15)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(6)

    # 4 Group Member Cards (Clean Names & IDs only - NO roles indicated on slide)
    members_data = [
        ("Comfort Penyengwe", "Student ID: 2410098", Inches(0.8), Inches(3.6), ROYAL_BLUE),
        ("Gideon Namuya", "Student ID: 2410149", Inches(6.8), Inches(3.6), MINT_GREEN),
        ("Lubuto Matambo", "Student ID: 2410171", Inches(0.8), Inches(5.2), AMBER_GOLD),
        ("Lamla Mwanza", "Student ID: 2410205", Inches(6.8), Inches(5.2), VIOLET_PURP)
    ]

    for name, sid, left, top, accent in members_data:
        m_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.7), Inches(1.3))
        m_card.fill.solid()
        m_card.fill.fore_color.rgb = CARD_BG
        m_card.line.color.rgb = accent
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
        p_name.font.color.rgb = TEXT_WHITE

        p_id = m_tf.add_paragraph()
        p_id.text = sid
        p_id.font.size = Pt(13)
        p_id.font.bold = True
        p_id.font.color.rgb = accent
        p_id.space_before = Pt(3)

    add_notes(s1, "Comfort Penyengwe (Intro): 'Good morning Lecturer and colleagues. Today our group—Comfort Penyengwe, Gideon Namuya, Lubuto Matambo, and Lamla Mwanza—presents our project on Database Security under BIT3360: Advanced Databases. Databases represent an institution's most critical digital asset, holding confidential personal data and student examination results. In this presentation, we will explain how databases are attacked, how we defend them using industry-standard controls, and demonstrate a live working prototype built for the ZUT Student Information System.'")

    # =========================================================
    # SLIDE 2: What is Database Security? (PART 1: COMFORT)
    # =========================================================
    s2 = create_content_slide(2, "Part 1: Foundations", "What is Database Security? (The CIA Triad Explained)", "Why database security is about protecting data from being seen, changed, or destroyed.")
    add_card(s2, Inches(0.8), Inches(1.85), Inches(3.6), Inches(4.8),
             "1. Confidentiality",
             "Only authorized eyes can see the data.",
             [
                 "Student Privacy: Protects sensitive personal identity like student NRC numbers and emails.",
                 "Access Restriction: Prevents confidential records leaking to unauthorized students or outside hackers.",
                 "Enforcement: Achieved through user privilege limits and masked database views."
             ], border_color=ROYAL_BLUE, title_color=ROYAL_BLUE)
    add_card(s2, Inches(4.8), Inches(1.85), Inches(3.6), Inches(4.8),
             "2. Integrity",
             "Data cannot be secretly changed or faked.",
             [
                 "Exam Authenticity: Ensures marks and transcripts remain 100% genuine and unaltered.",
                 "Fraud Prevention: Stops rogue users or unauthorized students from tampering with grades.",
                 "Enforcement: Implemented using database triggers, constraints, and audit logs."
             ], border_color=MINT_GREEN, title_color=MINT_GREEN)
    add_card(s2, Inches(8.8), Inches(1.85), Inches(3.6), Inches(4.8),
             "3. Availability",
             "The system is up and working when needed.",
             [
                 "Service Uptime: Ensures lecturers and students can access records during exams.",
                 "Resilience: Prevents malicious users from dropping tables or crashing the database engine.",
                 "Enforcement: Handled via automated backups, read replicas, and strict permission barriers."
             ], border_color=AMBER_GOLD, title_color=AMBER_GOLD)
    add_notes(s2, "Comfort Penyengwe: 'To understand database security, we look at the CIA Triad: Confidentiality, Integrity, and Availability. Confidentiality means student NRCs stay private. Integrity means nobody can secretly change their grade from 50% to 90%. Availability means the database is always online. Real security isn't just one firewall; it has to be built inside the database engine itself.'")

    # =========================================================
    # SLIDE 3: Common Threats (PART 1: COMFORT)
    # =========================================================
    s3 = create_content_slide(3, "Part 1: Threat Landscape", "How Databases Get Hacked (Common Threats)", "The two biggest dangers in database systems: SQL Injection and Privilege Abuse.")
    add_card(s3, Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.8),
             "1. SQL Injection (The #1 Web Attack)",
             "Trick the database into running the hacker's code.",
             [
                 "Vulnerability: Happens when an application glues user input directly into an SQL query.",
                 "Payload: In an NRC search box, typing: ' OR '1'='1",
                 "Execution: The database evaluates '1'='1' as TRUE for every single student record in the table.",
                 "Impact: The entire student registry, NRCs, and grades are leaked on screen in seconds!"
             ], border_color=ROSE_RED, title_color=ROSE_RED)
    add_card(s3, Inches(6.8), Inches(1.85), Inches(5.6), Inches(4.8),
             "2. Privilege Abuse & Insider Threats",
             "Giving regular users too much database power.",
             [
                 "Over-Privileged Accounts: If a lecturer or student account has DROP or DELETE rights, one rogue command destroys the entire institution database.",
                 "Missing Audit Trail: If someone alters a mark with no audit log, non-repudiation fails and nobody can prove who did it.",
                 "Weak Credentials: Default root passwords or credentials saved in plaintext source code."
             ], border_color=ROSE_RED, title_color=ROSE_RED)
    add_notes(s3, "Comfort Penyengwe: 'The most famous database vulnerability is SQL Injection. When application code takes user input and concatenates it directly into an SQL query, an attacker can input quotes and SQL keywords to trick the database into dumping all records. The second danger is giving regular users too much power—if a student can run an UPDATE command on the grades table, the integrity of the university is broken. Now, Gideon Namuya will explain how we defend against these threats.'")

    # =========================================================
    # SLIDE 4: Access Control & Least Privilege (PART 2: GIDEON)
    # =========================================================
    s4 = create_content_slide(4, "Part 2: Defensive Controls", "Role-Based Access Control & The Principle of Least Privilege", "Users should only be able to do what their specific job requires—nothing more.")
    add_card(s4, Inches(0.8), Inches(1.85), Inches(3.6), Inches(4.8),
             "Administrator (DBA)",
             "Full system control for maintenance.",
             [
                 "Account: sec_admin",
                 "Permissions: ALL PRIVILEGES.",
                 "Management: Can create tables, manage backups, and configure user accounts.",
                 "Assignment: Strictly restricted to authorized IT database administrators."
             ], border_color=ROYAL_BLUE, title_color=ROYAL_BLUE)
    add_card(s4, Inches(4.8), Inches(1.85), Inches(3.6), Inches(4.8),
             "Lecturer (Academic Staff)",
             "Can grade students, but cannot destroy data.",
             [
                 "Account: sec_lecturer",
                 "Permissions: SELECT, INSERT, UPDATE on grades.",
                 "Destruction Blocked: CANNOT drop tables (DROP privilege denied).",
                 "Identity Guard: CANNOT delete student accounts (DELETE privilege denied)."
             ], border_color=AMBER_GOLD, title_color=AMBER_GOLD)
    add_card(s4, Inches(8.8), Inches(1.85), Inches(3.6), Inches(4.8),
             "Student (Undergraduate)",
             "Strict read-only access to their own grades.",
             [
                 "Account: sec_student",
                 "Permissions: SELECT on masked View only.",
                 "Confidentiality: CANNOT view peer NRC numbers or student emails.",
                 "Tamper Prevention: CANNOT alter any grade (Error 1142 Access Denied)."
             ], border_color=ROSE_RED, title_color=ROSE_RED)
    add_notes(s4, "Gideon Namuya: 'Thank you, Comfort. To defend against privilege abuse, we use Role-Based Access Control under the Principle of Least Privilege. In simple terms: an Admin can do everything; a Lecturer can enter and update marks, but cannot drop tables; and a Student has strict read-only access to view their own grades. Even if a student tries to send an UPDATE query, the database engine checks their privileges and immediately blocks execution with Error 1142: Access Denied.'")

    # =========================================================
    # SLIDE 5: Parameterized Queries (PART 2: GIDEON)
    # =========================================================
    s5 = create_content_slide(5, "Part 2: Defensive Controls", "How Parameterized Queries Stop SQL Injection Completely", "The golden rule of database security: Treat user input as data, never as executable code.")
    add_card(s5, Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.8),
             "Vulnerable: String Concatenation",
             "The database gets tricked into running user text as commands.",
             [
                 "Vulnerable Code: SELECT * FROM students WHERE nrc = 'INPUT'",
                 "Attacker Types: ' OR '1'='1",
                 "Compiled Logic: WHERE nrc = '' OR '1'='1'",
                 "Why It Fails: The quotes terminate the string literal, and OR '1'='1 becomes live SQL logic.",
                 "Consequence: Every confidential student record and NRC is leaked!"
             ], border_color=ROSE_RED, title_color=ROSE_RED)
    add_card(s5, Inches(6.8), Inches(1.85), Inches(5.6), Inches(4.8),
             "Secure: Parameterized Prepared Statement",
             "The database engine compiles query structure FIRST.",
             [
                 "Prepared Code: cursor.execute('SELECT * FROM students WHERE nrc = ?', (input,))",
                 "Attacker Types: ' OR '1'='1",
                 "Safe Execution: Searches literally for a student whose NRC string equals \"' OR '1'='1\".",
                 "Why It Works: The ? is a placeholder. Input is strictly data, never parsed as code.",
                 "Defense Outcome: 0 records leaked. Attack 100% neutralized!"
             ], border_color=MINT_GREEN, title_color=MINT_GREEN)
    add_notes(s5, "Gideon Namuya: 'Now look at why Parameterized Queries are the ultimate defense against SQL Injection. In vulnerable code, strings are glued together, so the attacker's quotes become live SQL commands. But in a Parameterized Query—or Prepared Statement—the database engine pre-compiles the query template first. When the attack payload arrives, the database treats it purely as plain text data. Code and data remain completely separated, neutralizing the attack completely.'")

    # =========================================================
    # SLIDE 6: Encryption & Audit Logging (PART 2: GIDEON)
    # =========================================================
    s6 = create_content_slide(6, "Part 2: Defensive Controls", "Data Encryption & Tamper-Evident Audit Logging", "How we protect data on disk and catch anyone who tries to alter marks.")
    add_card(s6, Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.8),
             "1. Cryptographic Protection (Hashing & Encryption)",
             "If the database is stolen, the data cannot be read.",
             [
                 "Password Hashing: Passwords stored as one-way salted SHA-256 hashes. Even DBAs cannot reverse them.",
                 "In-Transit Security: Encrypted via TLS/SSL so network eavesdroppers cannot intercept traffic.",
                 "At-Rest Security: Sensitive personal identification columns like NRCs can be encrypted so raw files on hard drives are protected."
             ], border_color=ROYAL_BLUE, title_color=ROYAL_BLUE)
    add_card(s6, Inches(6.8), Inches(1.85), Inches(5.6), Inches(4.8),
             "2. Automated Database Triggers (Audit Log)",
             "A security camera recording every change in the database.",
             [
                 "Internal Threat: What if an insider alters a student's grade from 40 to 85?",
                 "Trigger Created: trg_grades_audit_update fires automatically on UPDATE.",
                 "Audit Record: The trigger silently logs: Changed By, Timestamp, Record ID, Old Score, and New Score.",
                 "Non-Repudiation: 100% accountability is guaranteed—no one can deny their actions."
             ], border_color=MINT_GREEN, title_color=MINT_GREEN)
    add_notes(s6, "Gideon Namuya: 'Our third layer of defense is Encryption and Auditing. Passwords are saved as one-way salted hashes so they cannot be stolen, and connections are encrypted. Furthermore, to prevent internal fraud, we created an automatic database trigger on the grades table. If a grade is modified, the database silently records who changed it, the previous score, and the new score for non-repudiation. Now, Lubuto Matambo will explain the industry tools and our prototype architecture.'")

    # =========================================================
    # SLIDE 7: Industry Tools & Systems (PART 3: LUBUTO)
    # =========================================================
    s7 = create_content_slide(7, "Part 3: Industry & Design", "Enterprise Database Security Systems & Tools", "How major enterprises and tech companies implement these controls in production.")
    add_card(s7, Inches(0.8), Inches(1.85), Inches(3.6), Inches(4.8),
             "MySQL Enterprise Security",
             "Commercial features built into MySQL.",
             [
                 "Enterprise Firewall: Blocks SQL injection in real time by learning normal query patterns.",
                 "Enterprise Audit: Government-grade compliance auditing and monitoring.",
                 "Transparent Encryption (TDE): Automatically encrypts database files on disk at rest."
             ], border_color=ROYAL_BLUE, title_color=ROYAL_BLUE)
    add_card(s7, Inches(4.8), Inches(1.85), Inches(3.6), Inches(4.8),
             "PostgreSQL Security Suite",
             "Advanced open-source security controls.",
             [
                 "Row-Level Security (RLS): Allows students to only see rows matching their own ID.",
                 "pg_audit Extension: Detailed logging of all DDL and DML commands for security audits.",
                 "SCRAM-SHA-256: State-of-the-art client-server password authentication."
             ], border_color=AMBER_GOLD, title_color=AMBER_GOLD)
    add_card(s7, Inches(8.8), Inches(1.85), Inches(3.6), Inches(4.8),
             "Vault & Activity Monitoring",
             "Protecting passwords and monitoring traffic.",
             [
                 "HashiCorp Vault: Generates temporary dynamic database passwords that expire automatically.",
                 "IBM Guardium / Imperva: Monitors all database traffic and raises alerts if suspicious queries occur.",
                 "Key Rotation: Automated cryptographic secret rotation prevents leaked credentials."
             ], border_color=MINT_GREEN, title_color=MINT_GREEN)
    add_notes(s7, "Lubuto Matambo: 'Thank you, Gideon. In large corporations, database security is powered by enterprise tools. MySQL Enterprise provides an automated Firewall that stops SQL injection, and Transparent Data Encryption to protect disks. PostgreSQL has Row-Level Security so users only see their own rows. And tools like HashiCorp Vault automatically rotate passwords so developers never have to write hardcoded credentials in source code.'")

    # =========================================================
    # SLIDE 8: Benefits & Real-World Challenges (PART 3: LUBUTO)
    # =========================================================
    s8 = create_content_slide(8, "Part 3: Industry & Design", "Benefits, Trade-offs & The Zambia Data Protection Act", "Balancing high security with system speed, usability, and legal requirements.")
    add_card(s8, Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.8),
             "Key Benefits & Legal Compliance",
             "Keeping the university reputable and compliant with law.",
             [
                 "Academic Integrity: Prevents unauthorized grade inflation, unauthorized alterations, or bribery.",
                 "Zambia Data Protection Act No. 3 of 2021: Legally requires universities handling citizen identity records (like NRCs) to enforce technical security.",
                 "Blast Radius Containment: If a student account is compromised, the attacker still cannot drop tables or access peer NRCs."
             ], border_color=MINT_GREEN, title_color=MINT_GREEN)
    add_card(s8, Inches(6.8), Inches(1.85), Inches(5.6), Inches(4.8),
             "Real-World Challenges & Trade-offs",
             "Security always has costs you have to manage.",
             [
                 "Performance Overhead: Executing triggers on every update and encrypting columns consumes server CPU and I/O cycles.",
                 "Administration Overhead: Managing granular user roles and privileges becomes complex as user bases expand.",
                 "The Human Factor: Technology cannot prevent staff from writing credentials on sticky notes or clicking phishing links."
             ], border_color=AMBER_GOLD, title_color=AMBER_GOLD)
    add_notes(s8, "Lubuto Matambo: 'Security delivers massive benefits. In Zambia, under the Data Protection Act of 2021, any institution holding citizen records like NRC numbers is legally mandated to protect them. But security comes with trade-offs: encrypting columns and running audit triggers uses more server CPU, and permissions must be managed carefully. Furthermore, technology cannot fix human mistakes like sharing passwords.'")

    # =========================================================
    # SLIDE 9: Our Prototype Architecture (PART 3: LUBUTO)
    # =========================================================
    s9 = create_content_slide(9, "Part 3: Industry & Design", "Our Prototype Design: ZUT Student Records System", "How our database tables, roles, and security measures fit together.")
    add_card(s9, Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.8),
             "Database Schema & Tables",
             "Models real academic university entities.",
             [
                 "students: student_id, student_number, nrc, full_name, program, year_of_study, email.",
                 "courses: course_code (e.g. BIT3360), course_name, credits, lecturer_name.",
                 "grades: grade_id, student_id, course_code, mark, grade_letter, semester.",
                 "audit_log: log_id, action_type, table_name, record_id, changed_by, old_value, new_value, timestamp."
             ], border_color=ROYAL_BLUE, title_color=ROYAL_BLUE)
    add_card(s9, Inches(6.8), Inches(1.85), Inches(5.6), Inches(4.8),
             "The 3 Implemented Defenses",
             "Proving the concepts through working code.",
             [
                 "1. RBAC Matrix: sec_admin (Full), sec_lecturer (Grades only), sec_student (Sanitized view, NRC masked).",
                 "2. Parameterized Query Engine: Protects the student search box against SQL injection attacks.",
                 "3. Automated Audit Trigger: Automatically records grade changes into audit_log for non-repudiation.",
                 "Demonstration Hand-Off: Now, Lamla Mwanza will walk you through the live demonstration of this system."
             ], border_color=MINT_GREEN, title_color=MINT_GREEN)
    add_notes(s9, "Lubuto Matambo: 'For our practical assignment, we built the ZUT Student Records System (zut_student_records). Our database models students with their NRCs, courses, grades, and an automated audit log. We created 3 distinct user roles with exact GRANT permissions and built an interactive web portal to demonstrate the security controls in real time. I will now hand over to Lamla Mwanza for the live demonstration.'")

    # =========================================================
    # SLIDE 10: Live Demo - Access Control (PART 4: LAMLA)
    # =========================================================
    s10 = create_content_slide(10, "Part 4: Live Demonstration", "Live Demonstration: Role-Based Access Control in Action", "Testing what each user can and cannot do live in our prototype.")
    add_card(s10, Inches(0.8), Inches(1.85), Inches(3.6), Inches(4.8),
             "Test 1: Administrator",
             "Has full DBA privileges.",
             [
                 "Action: View students & NRCs.",
                 "Result: [SUCCESS] Can view all records and manage tables.",
                 "Action: View audit trail.",
                 "Result: [SUCCESS] Complete inspection access."
             ], border_color=ROYAL_BLUE, title_color=ROYAL_BLUE)
    add_card(s10, Inches(4.8), Inches(1.85), Inches(3.6), Inches(4.8),
             "Test 2: Lecturer",
             "Allowed to grade, blocked from destruction.",
             [
                 "Action: Update grade mark.",
                 "Result: [SUCCESS] Grade updated; audit trigger fired.",
                 "Action: DROP TABLE students.",
                 "Result: [ACCESS DENIED Error 1142] Blocked by DB engine."
             ], border_color=AMBER_GOLD, title_color=AMBER_GOLD)
    add_card(s10, Inches(8.8), Inches(1.85), Inches(3.6), Inches(4.8),
             "Test 3: Student",
             "Least privilege enforced.",
             [
                 "Action: View grades view.",
                 "Result: [SUCCESS] Can see marks on masked view.",
                 "Action: Alter grade mark.",
                 "Result: [ACCESS DENIED Error 1142] Blocked immediately."
             ], border_color=ROSE_RED, title_color=ROSE_RED)
    add_notes(s10, "Lamla Mwanza: 'Thank you, Lubuto. Now let us look at our live demonstration. On screen in our web portal, when logged in as a Lecturer and we update a student mark, it succeeds because lecturers have UPDATE permissions. But if the lecturer tries to DROP the table or delete records, the database engine returns Error 1142: Access Denied. Similarly, when logged in as a student, any attempt to change a grade or view peer NRC numbers is rejected immediately under the Principle of Least Privilege.'")

    # =========================================================
    # SLIDE 11: Live Demo - SQLi & Audit (PART 4: LAMLA)
    # =========================================================
    s11 = create_content_slide(11, "Part 4: Live Demonstration", "Live Demonstration: SQL Injection Attack vs Defense & Audit Log", "Proving how prepared statements neutralize attacks and triggers record changes.")
    add_card(s11, Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.8),
             "SQL Injection Attack vs Defense",
             "Testing payload: ' OR '1'='1 in the NRC search box.",
             [
                 "Test A (Vulnerable Query): String concatenation causes the WHERE clause to evaluate as TRUE for every student. Critical Data Breach! All confidential NRCs and records are dumped.",
                 "Test B (Parameterized Query): The database engine compiles the query template first. The payload is treated strictly as plain literal text. 0 records leaked. Attack completely neutralized!"
             ], border_color=ROSE_RED, title_color=ROSE_RED)
    add_card(s11, Inches(6.8), Inches(1.85), Inches(5.6), Inches(4.8),
             "Tamper-Evident Audit Trail",
             "Inspecting the audit_log table live.",
             [
                 "Trigger Triggered: When the lecturer modified student 1's mark from 78.50 to 95.00, our database trigger automatically fired.",
                 "Query Result: Querying audit_log shows: Log ID #2 | UPDATE | Changed By: sec_lecturer | Old Mark: 78.50 | New Mark: 95.00 | Exact Timestamp.",
                 "Integrity Proof: Provides 100% accountability and non-repudiation."
             ], border_color=MINT_GREEN, title_color=MINT_GREEN)
    add_notes(s11, "Lamla Mwanza: 'Next, we test our additional security measures. In our search box, we test the injection payload: single quote OR 1 equals 1. In the vulnerable query, this dumps all student NRCs onto the screen. But in our Parameterized Query, the database treats it as literal text, and zero records are leaked. Finally, we look at the audit log: the database trigger captured the exact timestamp, the user ID, the old score, and the new score for complete non-repudiation.'")

    # =========================================================
    # SLIDE 12: Challenges, Conclusion & References (PART 4: LAMLA)
    # =========================================================
    s12 = create_content_slide(12, "Part 4: Conclusion", "Challenges Encountered, Conclusion & References", "What we learned building this prototype and the academic sources we consulted.")
    add_card(s12, Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.8),
             "Challenges & How We Solved Them",
             "Practical lessons learned during development.",
             [
                 "Challenge 1: Capturing User Identity in Triggers — Solved by passing session context so the audit log records the actual user rather than a generic pool account.",
                 "Challenge 2: Usability vs Least Privilege — Solved by creating sanitized Views (vw_student_grades) so students can view grades without exposing confidential NRC numbers.",
                 "Challenge 3: Portability — Built a zero-dependency web portal running locally on Python so it runs seamlessly on any machine."
             ], border_color=AMBER_GOLD, title_color=AMBER_GOLD)
    add_card(s12, Inches(6.8), Inches(1.85), Inches(5.6), Inches(4.8),
             "Conclusion & References",
             "Key takeaway for modern database systems.",
             [
                 "Core Takeaway: Proactive database security—combining RBAC, Parameterized Queries, and Audit Logging—is essential to protect institutional integrity and comply with the Zambia Data Protection Act.",
                 "References:",
                 "1. Silberschatz, Korth, Sudarshan (2020). Database System Concepts (7th ed.).",
                 "2. OWASP Top 10 (2021). A03: Injection Flaws.",
                 "3. Government of Zambia. The Data Protection Act, No. 3 of 2021.",
                 "4. Oracle. MySQL 8.0 Reference Manual: Security & Access Management."
             ], border_color=MINT_GREEN, title_color=MINT_GREEN)
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
