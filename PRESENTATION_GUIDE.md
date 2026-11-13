# BIT3360: ADVANCED DATABASES - GROUP ASSIGNMENT
## Topic: Database Security Prototype & Defense Architecture
**Institution:** Zambia University College of Technology (ZUT)  
**Submission Date:** 26/11/2026  
**Group Size:** 4 Members  

---

## 4-Member Speaking Breakdown & Script

```
+-----------------------------------------------------------------------------------------+
| SPEAKER 1 (Member 1): Foundations & Threat Landscape (Slides 1 - 3)                    |
|   • Slide 1: Title & Group Introduction                                                |
|   • Slide 2: What is Database Security? (The CIA Triad Explained in Simple Terms)       |
|   • Slide 3: How Databases Get Hacked (SQL Injection & Privilege Abuse)                 |
+-----------------------------------------------------------------------------------------+
| SPEAKER 2 (Member 2): Defensive Mechanisms & Query Protection (Slides 4 - 6)            |
|   • Slide 4: Role-Based Access Control (RBAC) & Least Privilege                        |
|   • Slide 5: The Magic of Parameterized Queries (Why SQL Injection Fails)               |
|   • Slide 6: Data Encryption & Tamper-Evident Audit Logging (Triggers)                 |
+-----------------------------------------------------------------------------------------+
| SPEAKER 3 (Member 3): Industry Systems & ZUT System Design (Slides 7 - 9)               |
|   • Slide 7: Enterprise Database Security Tools (MySQL Firewall, TDE, Vault)            |
|   • Slide 8: Benefits, Real-World Trade-offs & The Zambia Data Protection Act          |
|   • Slide 9: Our Prototype Architecture (Tables, NRC, and 3 User Roles)                 |
+-----------------------------------------------------------------------------------------+
| SPEAKER 4 (Member 4): Live Demonstration & Conclusion (Slides 10 - 12)                  |
|   • Slide 10: Live Demo Part 1: Testing User Permissions (Admin, Lecturer, Student)    |
|   • Slide 11: Live Demo Part 2: SQL Injection Attack vs Defense & Audit Trigger         |
|   • Slide 12: Challenges Solved, Conclusion & References                                |
+-----------------------------------------------------------------------------------------+
```

---

### Slide 1: Title Slide
* **Title:** Database Security & Practical Protection Prototype
* **Subtitle:** Role-Based Access Control, SQL Injection Defense & Tamper-Evident Audit Logging
* **Course:** BIT3360: Advanced Databases
* **Institution:** Zambia University College of Technology (ZUT)
* **Presented by (Group of 4):** [Insert Name 1, Name 2, Name 3, Name 4]
* **Date:** 26th November 2026

> **Speaker Notes (Member 1):**  
> *"Good morning/afternoon, Lecturer and colleagues. Today our group of 4 presents our project on Database Security under BIT3360: Advanced Databases. Databases represent an institution's most critical asset, holding confidential personal data and examination results. In this presentation, we will explain how databases get attacked, how we defend them using industry-standard controls, and demonstrate a live working prototype built for the ZUT Student Information System."*

---

### Slide 2: What is Database Security? (The CIA Triad Explained)
* **💡 In Simple Terms:** Protecting data from being seen by unauthorized people, secretly changed, or destroyed.
* **1. Confidentiality:**
  * Only authorized eyes can see the data.
  * Protects sensitive personal data like student **NRC numbers** and private contact details.
  * Enforced using role permissions and masked views (`vw_student_grades`).
* **2. Integrity:**
  * Data cannot be faked, modified, or tampered with.
  * Guarantees that exam marks and academic standings remain 100% genuine.
  * Enforced using constraints, triggers, and audit logging.
* **3. Availability:**
  * The database is up, fast, and accessible when needed.
  * Prevents accidental deletion of tables or malicious Denial-of-Service crashes.

> **Speaker Notes (Member 1):**  
> *"To understand database security, we look at the CIA Triad: Confidentiality, Integrity, and Availability. Confidentiality means that sensitive records—like a student's NRC number—are kept private from unauthorized users. Integrity means nobody can secretly change their grade from 50% to 90%. And Availability ensures the system is always online when lecturers need to enter marks. True database security is not just a firewall; it must be built into the database engine itself."*

---

### Slide 3: How Databases Get Hacked (Common Threats)
* **💡 In Simple Terms:** The two biggest dangers in database systems are SQL Injection and Privilege Abuse.
* **1. SQL Injection (SQLi) — The #1 Web Vulnerability:**
  * Happens when an application glues user text directly into an SQL query string.
  * Attacker types into an NRC search box: `' OR '1'='1`
  * The database evaluates `'1'='1'` as TRUE for every single row.
  * **Result:** The entire student registry, NRC list, and confidential emails are leaked onto the screen!
* **2. Privilege Abuse & Insider Threats:**
  * Giving regular accounts too much database power (violating Least Privilege).
  * If a student or lecturer has `DROP` or `DELETE` rights, one rogue action destroys the entire database.
  * **Missing Audit Logs:** If someone changes a grade and there is no audit log, nobody knows who did it.

> **Speaker Notes (Member 1):**  
> *"The most famous database attack is SQL Injection. When application code takes user input and concatenates it directly into an SQL query, an attacker can input quotes and SQL keywords to trick the database into dumping all records. The second danger is giving users excessive privileges—if a student account has permission to update the grades table, the university's academic credibility is compromised. I will now hand over to Member 2 to explain how we defend against these threats."*

---

### Slide 4: Role-Based Access Control & Least Privilege (MEMBER 2)
* **💡 In Simple Terms:** Users should only be allowed to do what their specific job requires—nothing more.
* **1. Administrator (`sec_admin`):**
  * Full DBA control: `GRANT ALL PRIVILEGES`.
  * Creates tables, manages backups, and handles user accounts.
  * Restricted strictly to authorized IT staff.
* **2. Lecturer (`sec_lecturer`):**
  * Academic staff permissions: `SELECT`, `INSERT`, `UPDATE` on grades.
  * Can view students and input marks, but **CANNOT** drop tables or delete student accounts.
* **3. Student (`sec_student`):**
  * Strict read-only access: `SELECT` on masked view `vw_student_grades`.
  * **CANNOT** view peer NRC numbers.
  * **CANNOT** update or alter any mark (`Error 1142: Access Denied`).

> **Speaker Notes (Member 2):**  
> *"Thank you, Member 1. To stop privilege abuse, we implement Role-Based Access Control under the Principle of Least Privilege. In simple terms: an Admin can do everything; a Lecturer can view students and update grades, but cannot drop tables; and a Student has strict read-only access to view their own grades. Even if a student tries to send an UPDATE query, the database engine checks their privileges and immediately blocks execution with Error 1142: Access Denied."*

---

### Slide 5: How Parameterized Queries Stop SQL Injection (MEMBER 2)
* **💡 In Simple Terms:** The golden rule of database security: Treat user input as plain data, never as executable SQL instructions.
* **Vulnerable Query (Dynamic String Concatenation):**
  * Code: `SELECT * FROM students WHERE nrc = '` + `user_input` + `'`
  * Attacker types: `' OR '1'='1`
  * Query becomes: `WHERE nrc = '' OR '1'='1'`
  * **Why it breaches:** The single quote breaks out of the data string, turning the attacker's text into live SQL logic that evaluates to TRUE for all rows!
* **Secure Query (Parameterized Prepared Statement):**
  * Code: `cursor.execute("SELECT * FROM students WHERE nrc = ?", (user_input,))`
  * Attacker types: `' OR '1'='1`
  * **Why it works:** The database compiles the SQL template *before* receiving the input. The placeholder `?` treats the payload strictly as literal plain text. It searches for an NRC containing quotes, finds nothing, and returns 0 records safely!

> **Speaker Notes (Member 2):**  
> *"Now look at why Parameterized Queries are the definitive defense against SQL Injection. In vulnerable code, strings are glued together, so the attacker's quotes become live SQL commands. But in a Parameterized Query—or Prepared Statement—the database engine pre-compiles the query template first. When the attack payload arrives, the database treats it strictly as plain text data. Code and data remain completely separated, neutralizing the attack completely."*

---

### Slide 6: Data Encryption & Tamper-Evident Audit Logging (MEMBER 2)
* **💡 In Simple Terms:** Protect data on disk with encryption, and use database triggers like security cameras to catch mark tampering.
* **1. Cryptographic Protection (Hashing & Encryption):**
  * **Password Hashing:** Passwords stored using SHA-256 with salt. Even if the database file is stolen, passwords cannot be reversed.
  * **Data in Transit:** TLS/SSL protects data travelling between the application and database.
  * **Data at Rest:** Transparent Data Encryption (TDE) protects raw database files on disk.
* **2. Automated Database Triggers (Audit Trail):**
  * What if a lecturer alters a student's mark from 45 to 85?
  * We built an automatic trigger: `trg_grades_audit_update`.
  * Every time a mark changes, the database silently logs: *who made the change, the exact timestamp, the old mark, and the new mark*.
  * **Guarantees Non-Repudiation:** Nobody can deny their actions.

> **Speaker Notes (Member 2):**  
> *"Our third layer of defense is Encryption and Auditing. Passwords are saved as one-way salted hashes so they cannot be stolen, and connections are encrypted. Furthermore, to prevent internal fraud, we created an automatic database trigger on the grades table. If a grade is modified, the database silently records who changed it, the previous score, and the new score. Now, Member 3 will explain the industry tools and our prototype architecture."*

---

### Slide 7: Enterprise Database Security Tools & Systems (MEMBER 3)
* **💡 In Simple Terms:** How major enterprise environments implement these security controls at scale.
* **1. MySQL Enterprise Security:**
  * **Enterprise Firewall:** Inspects incoming SQL traffic in real time and blocks injection attempts.
  * **Transparent Data Encryption (TDE):** Encrypts table data on hard drives automatically.
  * **Enterprise Audit:** Tamper-resistant compliance logging.
* **2. PostgreSQL Security Ecosystem:**
  * **Row-Level Security (RLS):** Automatically filters rows based on the logged-in user session.
  * **pg_audit:** Detailed logging of all administrative actions.
* **3. Vault & Activity Monitoring:**
  * **HashiCorp Vault:** Automatically rotates database credentials so hardcoded passwords never exist in source code.
  * **Imperva / IBM Guardium:** Database Activity Monitoring (DAM) detecting anomalous queries.

> **Speaker Notes (Member 3):**  
> *"Thank you, Member 2. In large enterprises, database security is supported by specialized tools. MySQL Enterprise provides an automated Firewall that stops SQL injection, and Transparent Data Encryption to protect disks. PostgreSQL offers Row-Level Security so users only see their own rows. And centralized tools like HashiCorp Vault automatically rotate passwords so developers never write hardcoded credentials in code."*

---

### Slide 8: Benefits, Real-World Trade-offs & The Law (MEMBER 3)
* **💡 In Simple Terms:** Balancing security with speed, and meeting Zambian legal requirements.
* **Key Benefits & Legal Compliance:**
  * **Preserves Academic Standing:** Prevents unauthorized grade inflation or bribery.
  * **Zambia Data Protection Act No. 3 of 2021:** Legally mandates that institutions handling personal records (such as **NRC numbers**) implement technical controls to prevent data breaches.
  * **Damage Containment:** Even if a student account is compromised, RBAC prevents privilege escalation.
* **Real-World Challenges & Costs:**
  * **Performance Overhead:** Running audit triggers on every update and encrypting columns consumes CPU and disk resources.
  * **Privilege Management:** Maintaining user roles across an expanding organization requires continuous administrative effort.
  * **The Human Factor:** Software cannot prevent users from sharing passwords or falling for social engineering.

> **Speaker Notes (Member 3):**  
> *"Database security provides indispensable protection. In Zambia, under the Data Protection Act of 2021, universities processing personal data like NRC numbers are legally required to enforce technical safeguards. But security also brings trade-offs: encrypting columns and firing audit triggers uses server CPU, and maintaining user permissions requires continuous administration. Furthermore, technology cannot fix human mistakes like sharing passwords."*

---

### Slide 9: Our Prototype Design: ZUT Student Records (MEMBER 3)
* **💡 In Simple Terms:** How our database tables, roles, and security measures work together.
* **Database Entities (`zut_student_records`):**
  * `students`: `student_id`, `student_number`, **`nrc`**, `full_name`, `program`, `email`.
  * `courses`: `course_code`, `course_name`, `credits`, `lecturer_name`.
  * `grades`: `grade_id`, `student_id`, `course_code`, `mark`, `grade_letter`, `semester`.
  * `audit_log`: `log_id`, `action_type`, `table_name`, `record_id`, `changed_by`, `old_value`, `new_value`, `timestamp`.
* **The 3 Implemented Defenses:**
  * **1. RBAC User Accounts:** `sec_admin` (DBA), `sec_lecturer` (Grades only), `sec_student` (Read-only view).
  * **2. Parameterized Query Engine:** Protects the student NRC search box against SQL injection.
  * **3. Automated Audit Trigger:** Automatically captures grade changes into `audit_log`.

> **Speaker Notes (Member 3):**  
> *"For our practical assignment, we built the ZUT Student Records System (zut_student_records). Our database models students with their NRCs, courses, grades, and an automated audit log. We created 3 distinct user roles with exact GRANT permissions and built an interactive web portal to demonstrate the security controls in real time. I will now hand over to Member 4 for the live demonstration."*

---

### Slide 10: Live Demo Part 1: User Permissions in Action (MEMBER 4)
* **💡 In Simple Terms:** Proving that the database engine enforces user boundaries.
* **Test 1: Administrator (`sec_admin`):**
  * Action: View confidential students & NRC list $\rightarrow$ **[ALLOWED]**
  * Action: View audit trail $\rightarrow$ **[ALLOWED]**
* **Test 2: Lecturer (`sec_lecturer`):**
  * Action: Update student mark $\rightarrow$ **[ALLOWED]** (Grade updated; audit trigger fired).
  * Action: Attempt `DROP TABLE students` $\rightarrow$ **[ACCESS DENIED Error 1142]** Blocked by DB engine!
* **Test 3: Student (`sec_student`):**
  * Action: View grades view $\rightarrow$ **[ALLOWED]** (Sanitized view).
  * Action: Alter student grade $\rightarrow$ **[ACCESS DENIED Error 1142]** Blocked immediately!

> **Speaker Notes (Member 4):**  
> *"Thank you, Member 3. Now let us look at our live demonstration. On screen in our web portal, when logged in as a Lecturer and we update a student mark, it succeeds because lecturers have UPDATE permissions. But if the lecturer tries to DROP the table or delete records, the database engine returns Error 1142: Access Denied. Similarly, when logged in as a student, any attempt to change a grade or view peer NRC numbers is rejected immediately under the Principle of Least Privilege."*

---

### Slide 11: Live Demo Part 2: SQL Injection Defense & Audit Trail (MEMBER 4)
* **💡 In Simple Terms:** Testing the attack live on screen, and inspecting the audit trail.
* **SQL Injection Test (Payload: `' OR '1'='1`):**
  * **Test A (Vulnerable Query):** String concatenation causes the WHERE condition to evaluate as TRUE for all rows. **Critical Data Breach!** All student NRCs, emails, and names are dumped.
  * **Test B (Parameterized Query):** Database compiles the query first. The input is treated strictly as plain literal text. **0 records leaked. Attack 100% neutralized!**
* **Audit Trail Verification (`audit_log` Table):**
  * Modify a grade from `78.50` to `95.00`.
  * The database trigger instantly logs: *Log ID #2 | UPDATE | User: sec_lecturer | Old Mark: 78.50 | New Mark: 95.00 | Exact Timestamp*.

> **Speaker Notes (Member 4):**  
> *"Next, we demonstrate our additional security measures. In our search box, we test the injection payload: single quote OR 1 equals 1. In the vulnerable query, this dumps all student NRCs onto the screen. But in our Parameterized Query, the database treats it as literal text, and zero records are leaked. Finally, we look at the audit log: the database trigger captured the exact timestamp, the user ID, the old score, and the new score for complete non-repudiation."*

---

### Slide 12: Challenges Encountered, Conclusion & References (MEMBER 4)
* **💡 In Simple Terms:** What we learned building this prototype, and closing remarks.
* **Challenges & Solutions:**
  * **Challenge 1:** Capturing true user identity in triggers $\rightarrow$ Solved by passing session context into the audit logging mechanism.
  * **Challenge 2:** Masking confidential NRC numbers $\rightarrow$ Solved by creating sanitized Views (`vw_student_grades`) separating presentation from base tables.
  * **Challenge 3:** Portability $\rightarrow$ Engineered a zero-dependency web portal that runs locally on Python on any machine.
* **Conclusion & References:**
  * **Key Takeaway:** Proactive database security—combining RBAC, Parameterized Queries, and Audit Logging—is essential to protect institutional integrity and comply with the Zambia Data Protection Act.
  * **References:** Silberschatz et al. (2020) *Database System Concepts*; OWASP Top 10 (2021); Government of Zambia *Data Protection Act No. 3 of 2021*; Oracle *MySQL 8.0 Reference Manual*.

> **Speaker Notes (Member 4):**  
> *"In conclusion, database security cannot be an afterthought. By combining Role-Based Access Control, Parameterized Queries, and automated triggers, we achieved confidentiality, integrity, and compliance with Zambian law. This concludes our presentation. Our group of 4 is now ready to answer any questions from the panel. Thank you!"*
