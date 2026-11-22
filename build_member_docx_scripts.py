"""
Generates 4 personalized, professional Word documents (.docx)
for each group member:
1. SCRIPT_1_Comfort_Penyengwe.docx (Part 1: Slides 1 - 3)
2. SCRIPT_2_Gideon_Namuya.docx     (Part 2: Slides 4 - 6)
3. SCRIPT_3_Lubuto_Matambo.docx    (Part 3: Slides 7 - 9)
4. SCRIPT_4_Lamla_Mwanza.docx      (Part 4: Slides 10 - 12)
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_script_doc(filename, member_name, student_id, part_title, slide_range, overview_text, slides_data, handover_name, qna_list):
    doc = docx.Document()

    # Set page margins (1 inch)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    # 1. Header Box / Banner
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_inst = p_inst.add_run("ZAMBIA UNIVERSITY COLLEGE OF TECHNOLOGY (ZUT)\n")
    run_inst.font.name = "Calibri"
    run_inst.font.size = Pt(13)
    run_inst.font.bold = True
    run_inst.font.color.rgb = RGBColor(37, 99, 235) # Accent Blue

    run_sub = p_inst.add_run("BIT3360: ADVANCED DATABASES — GROUP PRESENTATION SCRIPT\n")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(11)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(100, 116, 139)

    # 2. Member Profile Table
    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    headers = [
        ("Presenter Name:", member_name),
        ("Student ID:", student_id),
        ("Assigned Section:", f"{part_title} ({slide_range})"),
        ("Speaking Time:", "~2.5 minutes")
    ]

    for i, (label, val) in enumerate(headers):
        row = table.rows[i]
        c0 = row.cells[0]
        c1 = row.cells[1]
        c0.width = Inches(2.0)
        c1.width = Inches(4.7)

        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "FFFFFF")

        p0 = c0.paragraphs[0]
        p0.add_run(label).font.bold = True
        p0.runs[0].font.name = "Calibri"
        p0.runs[0].font.size = Pt(10.5)

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.bold = (i == 0 or i == 1)
        r1.font.name = "Calibri"
        r1.font.size = Pt(10.5)
        if i == 0:
            r1.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph() # Spacer

    # 3. Overview Section
    h_ov = doc.add_heading(level=1)
    r_ov = h_ov.add_run("1. Your Section Overview (Plain English)")
    r_ov.font.name = "Calibri"
    r_ov.font.color.rgb = RGBColor(15, 23, 42)

    p_ov = doc.add_paragraph()
    r_ov_text = p_ov.add_run(overview_text)
    r_ov_text.font.name = "Calibri"
    r_ov_text.font.size = Pt(11)

    # 4. Slide-by-Slide Script
    h_sc = doc.add_heading(level=1)
    r_sc = h_sc.add_run("2. Slide-by-Slide Word-for-Word Script")
    r_sc.font.name = "Calibri"
    r_sc.font.color.rgb = RGBColor(15, 23, 42)

    for slide in slides_data:
        h_s = doc.add_heading(level=2)
        r_s = h_s.add_run(f"Slide {slide['num']}: {slide['title']}")
        r_s.font.name = "Calibri"
        r_s.font.color.rgb = RGBColor(37, 99, 235)

        p_pt = doc.add_paragraph()
        r_pt_title = p_pt.add_run("What is on screen:\n")
        r_pt_title.font.bold = True
        r_pt_title.font.name = "Calibri"
        r_pt_title.font.size = Pt(10)
        r_pt_title.font.color.rgb = RGBColor(100, 116, 139)

        for pt in slide['bullets']:
            p_b = doc.add_paragraph(style='List Bullet')
            rb = p_b.add_run(pt)
            rb.font.name = "Calibri"
            rb.font.size = Pt(10)

        # Word-for-Word Speaking Box
        box_table = doc.add_table(rows=1, cols=1)
        box_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        box_cell = box_table.rows[0].cells[0]
        box_cell.width = Inches(6.7)
        set_cell_background(box_cell, "F0F7FF") # Light blue tint

        p_box = box_cell.paragraphs[0]
        r_box_tag = p_box.add_run("🎙️ EXACT SCRIPT TO SAY OUT LOUD:\n")
        r_box_tag.font.bold = True
        r_box_tag.font.size = Pt(10.5)
        r_box_tag.font.color.rgb = RGBColor(29, 78, 216)

        r_box_speech = p_box.add_run(f'"{slide["script"]}"')
        r_box_speech.font.italic = True
        r_box_speech.font.size = Pt(11)
        r_box_speech.font.name = "Calibri"

        doc.add_paragraph() # Spacer

    # 5. Handover line
    if handover_name:
        p_hand = doc.add_paragraph()
        r_h_tag = p_hand.add_run("Handover to Next Speaker:\n")
        r_h_tag.font.bold = True
        r_h_tag.font.color.rgb = RGBColor(217, 119, 6)
        r_h_text = p_hand.add_run(f'At the end of your last slide, conclude with: "I will now hand over to {handover_name} for the next section."')
        r_h_text.font.italic = True

    # 6. Anticipated Questions for this Person
    h_q = doc.add_heading(level=1)
    r_q = h_q.add_run("3. Questions the Lecturer May Ask YOU & How to Answer")
    r_q.font.name = "Calibri"
    r_q.font.color.rgb = RGBColor(15, 23, 42)

    for q, a in qna_list:
        p_q = doc.add_paragraph()
        r_q_title = p_q.add_run(f"Q: {q}\n")
        r_q_title.font.bold = True
        r_q_title.font.name = "Calibri"
        r_q_title.font.color.rgb = RGBColor(185, 28, 28) # Red

        r_ans = p_q.add_run(f"Your Answer: {a}")
        r_ans.font.name = "Calibri"
        r_ans.font.size = Pt(10.5)

    doc.save(filename)
    print(f"[+] Successfully generated: {filename}")

# =====================================================================
# DATA FOR THE 4 MEMBERS
# =====================================================================

# 1. COMFORT PENYENGWE (Part 1: Slides 1 to 3)
comfort_slides = [
    {
        "num": 1,
        "title": "Title Slide & Group Introduction",
        "bullets": [
            "Project Title: Database Security & Practical Protection Prototype",
            "Course: BIT3360 Advanced Databases",
            "Group Members: Comfort Penyengwe, Gideon Namuya, Lubuto Matambo, Lamla Mwanza"
        ],
        "script": "Good morning Lecturer and colleagues. Today our group—Comfort Penyengwe, Gideon Namuya, Lubuto Matambo, and Lamla Mwanza—presents our project on Database Security under BIT3360: Advanced Databases. Databases represent an institution's most critical digital asset, holding confidential personal data and student examination results. In this presentation, we will explain how databases are attacked, how we defend them using industry-standard controls, and demonstrate a live working prototype built for the ZUT Student Information System."
    },
    {
        "num": 2,
        "title": "What is Database Security? (The CIA Triad Explained)",
        "bullets": [
            "Confidentiality: Protecting private data like student NRCs from unauthorized eyes.",
            "Integrity: Ensuring grades and academic records cannot be secretly faked or modified.",
            "Availability: Ensuring the database stays online and responsive during exams."
        ],
        "script": "To understand database security, we look at the CIA Triad: Confidentiality, Integrity, and Availability. Confidentiality means sensitive student records—like their National Registration Card (NRC) numbers—are kept strictly private from unauthorized eyes. Integrity means nobody can secretly change their grade from 50% to 90%. And Availability ensures the system is always online when lecturers need to enter marks. True database security is not just an external firewall; it must be built directly into the database engine itself."
    },
    {
        "num": 3,
        "title": "How Databases Get Hacked (Common Threats)",
        "bullets": [
            "SQL Injection (SQLi): Tricking the database into running user input as SQL commands.",
            "Attacker payload: ' OR '1'='1 in the NRC search box dumps the whole database.",
            "Privilege Abuse: Giving regular accounts too much power (e.g. DROP/DELETE privileges)."
        ],
        "script": "The most famous database attack is SQL Injection. When application code takes user input and concatenates it directly into an SQL query, an attacker can input quotes and SQL keywords to trick the database into dumping all records. The second major danger is giving regular users excessive privileges—if a student account has permission to update the grades table, the university's academic credibility is compromised. I will now hand over to Gideon Namuya to explain how we defend against these threats."
    }
]

comfort_qna = [
    ("What does the CIA triad mean in the context of this university database?",
     "Confidentiality means student NRCs and emails cannot be leaked. Integrity means grades cannot be tampered with. Availability means the database does not crash during exam registration."),
    ("Why is SQL Injection so dangerous?",
     "Because it bypasses application logic. If user input is not parameterized, the attacker's text becomes executable code, allowing them to dump tables or execute administrative commands.")
]

# 2. GIDEON NAMUYA (Part 2: Slides 4 to 6)
gideon_slides = [
    {
        "num": 4,
        "title": "Role-Based Access Control & Principle of Least Privilege",
        "bullets": [
            "Principle of Least Privilege: Users only get permissions required for their specific duties.",
            "sec_admin: Full DBA control (ALL PRIVILEGES).",
            "sec_lecturer: Can view students and update grades, but CANNOT drop tables or delete students.",
            "sec_student: Read-only access to view their own grades; CANNOT modify grades or view peer NRCs."
        ],
        "script": "Thank you, Comfort. To defend against privilege abuse, we implement Role-Based Access Control under the Principle of Least Privilege. In simple terms: an Admin can do everything; a Lecturer can enter and update marks, but cannot drop tables; and a Student has strict read-only access to view their own grades. Even if a student tries to send an UPDATE query, the database engine checks their privileges and immediately blocks execution with Error 1142: Access Denied."
    },
    {
        "num": 5,
        "title": "How Parameterized Queries Stop SQL Injection Completely",
        "bullets": [
            "Vulnerable Dynamic SQL: String concatenation turns input ' OR '1'='1 into executable logic.",
            "Parameterized Query (Prepared Statement): SQL structure is pre-compiled FIRST by DB engine.",
            "Input is bound as a literal data parameter (?). Payload fails; 0 records leaked!"
        ],
        "script": "Now look at why Parameterized Queries are the definitive defense against SQL Injection. In vulnerable code, strings are glued together, so the attacker's quotes become live SQL commands. But in a Parameterized Query—or Prepared Statement—the database engine pre-compiles the query template first. When the attack payload arrives, the database treats it strictly as plain text data. Code and data remain completely separated, neutralizing the attack completely."
    },
    {
        "num": 6,
        "title": "Data Encryption & Tamper-Evident Audit Logging",
        "bullets": [
            "Password Hashing: SHA-256 with salt ensures passwords cannot be reversed even if disk is stolen.",
            "Data in Transit: TLS/SSL encryption protects network packets from eavesdropping.",
            "Audit Logging Triggers: trg_grades_audit_update automatically captures who, when, old mark, and new mark."
        ],
        "script": "Our third layer of defense is Encryption and Auditing. Passwords are saved as one-way salted hashes so they cannot be stolen, and connections are encrypted. Furthermore, to prevent internal fraud, we created an automatic database trigger on the grades table. If a grade is modified, the database silently records who changed it, the previous score, and the new score for non-repudiation. Now, Lubuto Matambo will explain the industry tools and our prototype architecture."
    }
]

gideon_qna = [
    ("What is the Principle of Least Privilege?",
     "Giving a user or process only the minimum permissions necessary to perform their job and nothing more. For example, lecturers can update marks, but have no permission to drop tables."),
    ("Why is parameterization better than just filtering out quotes?",
     "Filtering or blacklisting quotes is fragile—attackers use alternate encodings or hex to bypass filters. Parameterization fundamentally separates code compilation from data evaluation at the database engine level.")
]

# 3. LUBUTO MATAMBO (Part 3: Slides 7 to 9)
lubuto_slides = [
    {
        "num": 7,
        "title": "Enterprise Database Security Systems & Tools",
        "bullets": [
            "MySQL Enterprise Security: Enterprise Firewall (real-time SQL inspection) & TDE (encryption at rest).",
            "PostgreSQL Security: Row-Level Security (RLS) and pg_audit for granular tracking.",
            "HashiCorp Vault: Dynamic database credential generation and automated password rotation."
        ],
        "script": "Thank you, Gideon. In large corporations, database security is supported by specialized enterprise tools. MySQL Enterprise provides an automated Firewall that stops SQL injection, and Transparent Data Encryption to protect disks. PostgreSQL offers Row-Level Security so users only see their own rows. And centralized tools like HashiCorp Vault automatically rotate passwords so developers never write hardcoded credentials in source code."
    },
    {
        "num": 8,
        "title": "Benefits, Real-World Trade-offs & The Zambia Data Protection Act",
        "bullets": [
            "Benefits: Guarantees academic integrity, prevents grade bribery, and isolates account compromises.",
            "Zambia Data Protection Act No. 3 of 2021: Legally mandates technical controls to protect citizen NRC numbers.",
            "Trade-offs: Audit triggers and column encryption consume CPU and disk I/O; permissions require administration."
        ],
        "script": "Database security provides indispensable protection. In Zambia, under the Data Protection Act of 2021, universities processing personal data like NRC numbers are legally required to enforce technical safeguards. But security also brings trade-offs: encrypting columns and firing audit triggers uses server CPU, and maintaining user permissions requires continuous administration. Furthermore, technology cannot fix human mistakes like sharing passwords."
    },
    {
        "num": 9,
        "title": "Our Prototype Design: ZUT Student Records System",
        "bullets": [
            "Database Schema: students (with nrc), courses (credits, lecturer), grades (marks), audit_log (trigger history).",
            "Roles: sec_admin (DBA), sec_lecturer (Grades only), sec_student (Sanitized view, NRC masked).",
            "Security Measures: RBAC user grants, Parameterized Query engine, and automated audit triggers."
        ],
        "script": "For our practical assignment, we built the ZUT Student Records System (zut_student_records). Our database models students with their NRCs, courses, grades, and an automated audit log. We created 3 distinct user roles with exact GRANT permissions and built an interactive web portal to demonstrate the security controls in real time. I will now hand over to Lamla Mwanza for the live demonstration."
    }
]

lubuto_qna = [
    ("How does this project comply with the Zambia Data Protection Act of 2021?",
     "The Act mandates that data controllers protect sensitive personal data (PII) against unauthorized access and leaks. We protect student NRCs using role masking and parameterized queries to prevent mass data exfiltration."),
    ("What is Transparent Data Encryption (TDE)?",
     "TDE is a database feature that encrypts database files on disk in real time. Even if someone physically steals the hard drive or backup file, the data cannot be read without the cryptographic key.")
]

# 4. LAMLA MWANZA (Part 4: Slides 10 to 12)
lamla_slides = [
    {
        "num": 10,
        "title": "Live Demonstration: Role-Based Access Control in Action",
        "bullets": [
            "Test 1 (Admin): View students & NRCs -> [SUCCESS]. Full DBA control.",
            "Test 2 (Lecturer): Update student mark -> [SUCCESS]. Attempt DROP TABLE students -> [ACCESS DENIED Error 1142]!",
            "Test 3 (Student): View sanitized grades -> [SUCCESS]. Alter mark -> [ACCESS DENIED Error 1142]!"
        ],
        "script": "Thank you, Lubuto. Now let us look at our live demonstration. On screen in our web portal, when logged in as a Lecturer and we update a student mark, it succeeds because lecturers have UPDATE permissions. But if the lecturer tries to DROP the table or delete records, the database engine returns Error 1142: Access Denied. Similarly, when logged in as a student, any attempt to change a grade or view peer NRC numbers is rejected immediately under the Principle of Least Privilege."
    },
    {
        "num": 11,
        "title": "Live Demonstration: SQL Injection Attack vs Defense & Audit Log",
        "bullets": [
            "SQL Injection Test: Search NRC with payload ' OR '1'='1.",
            "Vulnerable Query: Leaks all student records and confidential NRCs onto screen (Critical Breach!).",
            "Parameterized Query: Payload bound as literal text. 0 records leaked. Attack neutralized!",
            "Audit Log: Trigger captured grade modification from 78.50 to 95.00 with user, timestamp, old and new marks."
        ],
        "script": "Next, we demonstrate our additional security measures. In our search box, we test the injection payload: single quote OR 1 equals 1. In the vulnerable query, this dumps all student NRCs onto the screen. But in our Parameterized Query, the database treats it as literal text, and zero records are leaked. Finally, we look at the audit log: the database trigger captured the exact timestamp, the user ID, the old score, and the new score for complete non-repudiation."
    },
    {
        "num": 12,
        "title": "Challenges Encountered, Conclusion & References",
        "bullets": [
            "Challenge 1: Capturing true user identity in triggers -> Solved by passing session context.",
            "Challenge 2: Usability vs Least Privilege -> Solved by sanitized Views (vw_student_grades).",
            "Challenge 3: Portability -> Built zero-dependency web portal running locally on Python.",
            "Conclusion: Combining RBAC, Parameterized Queries, and Audit Logging ensures academic integrity."
        ],
        "script": "In conclusion, database security cannot be an afterthought. By combining Role-Based Access Control, Parameterized Queries, and automated triggers, we achieved confidentiality, integrity, and compliance with Zambian law. This concludes our presentation. Comfort, Gideon, Lubuto, and I are now ready to answer any questions from the panel. Thank you!"
    }
]

lamla_qna = [
    ("How does the database trigger ensure non-repudiation in the audit log?",
     "Non-repudiation means the actor cannot deny making the change. Because the trigger runs automatically inside the transactional engine, it captures the user and exact timestamp before committing the grade update."),
    ("During your live demo, why did the student get Error 1142?",
     "Error 1142 is MySQL's access denied code. In our SQL configuration, sec_student was only granted SELECT on the view. They possess zero UPDATE or DDL privileges, so the database engine blocked the command before touching the data.")
]

# Run generation
if __name__ == "__main__":
    create_script_doc(
        "SCRIPT_1_Comfort_Penyengwe.docx",
        "Comfort Penyengwe",
        "2410098",
        "Part 1: Foundations & Threats",
        "Slides 1 to 3",
        "You open the presentation! You introduce the group members, explain what Database Security is using the CIA Triad (Confidentiality, Integrity, Availability), and explain the two biggest threats databases face: SQL Injection and Privilege Abuse.",
        comfort_slides,
        "Gideon Namuya",
        comfort_qna
    )

    create_script_doc(
        "SCRIPT_2_Gideon_Namuya.docx",
        "Gideon Namuya",
        "2410149",
        "Part 2: Defensive Controls",
        "Slides 4 to 6",
        "You explain HOW databases are protected! You explain Role-Based Access Control (RBAC) and Least Privilege (Admin vs Lecturer vs Student), why Parameterized Queries completely neutralize SQL injection, and how password hashing and audit triggers protect data.",
        gideon_slides,
        "Lubuto Matambo",
        gideon_qna
    )

    create_script_doc(
        "SCRIPT_3_Lubuto_Matambo.docx",
        "Lubuto Matambo",
        "2410171",
        "Part 3: Industry Tools, Law & Architecture",
        "Slides 7 to 9",
        "You connect our project to real-world industry tools (MySQL Firewall, TDE, Vault), explain the legal requirements under the Zambia Data Protection Act No. 3 of 2021, and explain our prototype's database tables (students with NRC, courses, grades, audit log).",
        lubuto_slides,
        "Lamla Mwanza",
        lubuto_qna
    )

    create_script_doc(
        "SCRIPT_4_Lamla_Mwanza.docx",
        "Lamla Mwanza",
        "2410205",
        "Part 4: Live Demonstration & Conclusion",
        "Slides 10 to 12",
        "You lead the live prototype demonstration! You click the buttons on screen (http://localhost:5000) to prove that students get Access Denied, show SQL Injection getting blocked by Parameterized Queries, show the live audit trail, and give the final conclusion!",
        lamla_slides,
        None,
        lamla_qna
    )
