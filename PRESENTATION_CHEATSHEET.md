# BIT3360 DATABASE SECURITY — QUICK PRESENTATION CHEAT SHEET
**Institution:** Zambia University College of Technology (ZUT)  
**Course:** BIT3360: Advanced Databases  

### Group Members & Assigned Presentation Roles:
1. **Comfort Penyengwe** — Student ID: **2410098**  
   👉 **Speaker 1: Foundations & Threats (Slides 1 to 3)**
2. **Gideon Namuya** — Student ID: **2410149**  
   👉 **Speaker 2: Defensive Controls & Query Protection (Slides 4 to 6)**
3. **Lubuto Matambo** — Student ID: **2410171**  
   👉 **Speaker 3: Architecture, Enterprise Tools & Law (Slides 7 to 9)**
4. **Lamla Mwanza** — Student ID: **2410205**  
   👉 **Speaker 4: Live Demonstration & Wrap-Up (Slides 10 to 12)**

---

## 1. The 60-Second Summary (What is our project about?)
We built a working prototype for the **ZUT Student Information System** (`zut_student_records`).
It stores student details, **NRC numbers**, courses, and exam marks.

**The Problem:**
If a university database is not secured:
1. A student or rogue insider can secretly change their marks from 45% to 90%.
2. A hacker can type a trick query into a search box and steal everyone's confidential NRC number (**SQL Injection**).

**Our Solution (The 3 Defenses we built):**
1. **Access Control (RBAC):** We created 3 separate roles:
   * **Admin:** Full DBA power.
   * **Lecturer:** Can enter and change marks, but CANNOT delete students or drop tables.
   * **Student:** Can only view their own marks; CANNOT change anything or see peer NRCs.
2. **Parameterized Queries (SQL Injection Defense):**
   * An attacker types `' OR '1'='1` in the NRC search bar to dump the whole database.
   * A vulnerable dynamic query falls for it.
   * Our **Parameterized Query** treats the attack as literal plain text, blocking it completely (0 records leaked).
3. **Audit Log Trigger:**
   * If a lecturer updates a grade, a database trigger automatically logs: *who changed it, the exact time, the old mark, and the new mark* for accountability (non-repudiation).

---

## 2. How to Run the Demo on Thursday (Takes 10 Seconds)

1. Open PowerShell or Command Prompt in this folder.
2. Type:
   ```bash
   python web_app.py
   ```
3. Your browser automatically opens to **`http://localhost:5000`**.
4. Everything Lamla needs to click during the demo is right on that screen!

---

## 3. Speaking Script for Each Member

### 👤 SPEAKER 1: Comfort Penyengwe (Student ID: 2410098)
**Section:** Part 1: Foundations & Threats (Slides 1 to 3)  
**Speaking Time:** ~2.5 minutes  

* **Slide 1 (Title Slide):**
  > *"Good morning Lecturer and colleagues. Today our group—Comfort Penyengwe, Gideon Namuya, Lubuto Matambo, and Lamla Mwanza—presents our project on Database Security under BIT3360: Advanced Databases. Databases represent an institution's most critical digital asset, holding confidential personal data and student examination results. In this presentation, we will explain how databases are attacked, how we defend them using industry-standard controls, and demonstrate a live working prototype built for the ZUT Student Information System."*

* **Slide 2 (The CIA Triad Explained):**
  > *"To understand database security, we look at the CIA Triad: Confidentiality, Integrity, and Availability. Confidentiality means sensitive student records—like their National Registration Card (NRC) numbers—are kept strictly private from unauthorized eyes. Integrity means nobody can secretly change their grade from 50% to 90%. And Availability ensures the system is always online when lecturers need to enter marks. True database security is not just an external firewall; it must be built directly into the database engine itself."*

* **Slide 3 (Common Threats: SQLi & Privilege Abuse):**
  > *"The most famous database attack is SQL Injection. When application code takes user input and concatenates it directly into an SQL query, an attacker can input quotes and SQL keywords to trick the database into dumping all records. The second major danger is giving regular users excessive privileges—if a student account has permission to update the grades table, the university's academic credibility is compromised.*  
  > ***I will now hand over to Gideon Namuya to explain how we defend against these threats.***"*

---

### 👤 SPEAKER 2: Gideon Namuya (Student ID: 2410149)
**Section:** Part 2: Defensive Controls (Slides 4 to 6)  
**Speaking Time:** ~2.5 minutes  

* **Slide 4 (Role-Based Access Control & Least Privilege):**
  > *"Thank you, Comfort. To defend against privilege abuse, we implement Role-Based Access Control under the Principle of Least Privilege. In simple terms: an Admin can do everything; a Lecturer can enter and update marks, but cannot drop tables; and a Student has strict read-only access to view their own grades. Even if a student tries to send an UPDATE query, the database engine checks their privileges and immediately blocks execution with Error 1142: Access Denied."*

* **Slide 5 (How Parameterized Queries Stop SQL Injection):**
  > *"Now look at why Parameterized Queries are the definitive defense against SQL Injection. In vulnerable code, strings are glued together, so the attacker's quotes become live SQL commands. But in a Parameterized Query—or Prepared Statement—the database engine pre-compiles the query template first. When the attack payload arrives, the database treats it strictly as plain text data. Code and data remain completely separated, neutralizing the attack completely."*

* **Slide 6 (Data Encryption & Audit Triggers):**
  > *"Our third layer of defense is Encryption and Auditing. Passwords are saved as one-way salted hashes so they cannot be stolen, and connections are encrypted. Furthermore, to prevent internal fraud, we created an automatic database trigger on the grades table. If a grade is modified, the database silently records who changed it, the previous score, and the new score for non-repudiation.*  
  > ***Now, Lubuto Matambo will explain the industry tools and our prototype architecture.***"*

---

### 👤 SPEAKER 3: Lubuto Matambo (Student ID: 2410171)
**Section:** Part 3: Architecture, Enterprise Tools & Law (Slides 7 to 9)  
**Speaking Time:** ~2.5 minutes  

* **Slide 7 (Enterprise Database Security Tools):**
  > *"Thank you, Gideon. In large corporations, database security is supported by specialized enterprise tools. MySQL Enterprise provides an automated Firewall that stops SQL injection, and Transparent Data Encryption to protect disks. PostgreSQL offers Row-Level Security so users only see their own rows. And centralized tools like HashiCorp Vault automatically rotate passwords so developers never write hardcoded credentials in source code."*

* **Slide 8 (Benefits, Trade-offs & The Zambia Data Protection Act):**
  > *"Database security provides indispensable protection. In Zambia, under the Data Protection Act of 2021, universities processing personal data like NRC numbers are legally required to enforce technical safeguards. But security also brings trade-offs: encrypting columns and firing audit triggers uses server CPU, and maintaining user permissions requires continuous administration. Furthermore, technology cannot fix human mistakes like sharing passwords."*

* **Slide 9 (Our Prototype Design: ZUT Student Records):**
  > *"For our practical assignment, we built the ZUT Student Records System (zut_student_records). Our database models students with their NRCs, courses, grades, and an automated audit log. We created 3 distinct user roles with exact GRANT permissions and built an interactive web portal to demonstrate the security controls in real time.*  
  > ***I will now hand over to Lamla Mwanza for the live demonstration.***"*

---

### 👤 SPEAKER 4: Lamla Mwanza (Student ID: 2410205)
**Section:** Part 4: Live Demonstration & Wrap-Up (Slides 10 to 12)  
**Speaking Time:** ~3 minutes  

* **Slide 10 (Live Demo Part 1: Access Control in Action):**
  > *"Thank you, Lubuto. Now let us look at our live demonstration. On screen in our web portal (`http://localhost:5000`), when logged in as a Lecturer and we update a student mark, it succeeds because lecturers have UPDATE permissions.*  
  > *(Lamla clicks Student role and clicks 'Alter Student Grade'):*  
  > *Notice that when a student attempts to update a mark or drop a table, the database engine returns **Error 1142: Access Denied** under the Principle of Least Privilege."*

* **Slide 11 (Live Demo Part 2: SQL Injection Defense & Audit Trail):**
  > *"Next, we demonstrate our additional security measures. In our NRC search box, we test the injection payload: single quote OR 1 equals 1.*  
  > *(Lamla clicks 'Execute Vulnerable Query'):*  
  > *In the vulnerable query, this dumps all student NRCs onto the screen!*  
  > *(Lamla clicks 'Execute Parameterized Query'):*  
  > *Now look at our Parameterized Query: the database treats the payload strictly as literal text, and zero records are leaked.*  
  > *(Lamla clicks Tab 3):*  
  > *Finally, looking at our audit log, the database trigger automatically recorded who made the grade update (`sec_lecturer`), the timestamp, the old score, and the new score for complete non-repudiation."*

* **Slide 12 (Conclusion & Wrap-Up):**
  > *"In conclusion, database security cannot be an afterthought. By combining Role-Based Access Control, Parameterized Queries, and automated triggers, we achieved confidentiality, integrity, and compliance with Zambian law.*  
  > *This concludes our presentation. Comfort, Gideon, Lubuto, and I are now ready to answer any questions from the panel. Thank you!"*

---

## 4. Likely Questions the Lecturer Will Ask (And Your Answers)

**Q1: What is the Principle of Least Privilege?**  
* **Answer:** Giving a user or program only the absolute minimum permissions needed to do their specific job, and nothing more. For example, a student only needs to read their own grades, not update them or view peer NRCs.

**Q2: Why does a Parameterized Query stop SQL Injection?**  
* **Answer:** Because it separates **Code from Data**. The database engine compiles the SQL syntax *before* the user input is inserted. When user input arrives, it is strictly treated as a literal text value, so it can never alter the query logic.

**Q3: What is non-repudiation in your audit log?**  
* **Answer:** Non-repudiation means a person cannot deny an action they took. Because our database trigger captures the user account and timestamp inside the transaction automatically, there is indisputable proof of who modified a grade.
