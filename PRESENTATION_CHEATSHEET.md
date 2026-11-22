# BIT3360 DATABASE SECURITY — QUICK PRESENTATION CHEAT SHEET
**Group Members:**
1. **Comfort Penyengwe** — Student ID: 2310385966 (Speaker 1)
2. **Lubuto Matambo** — Student ID: 2310385922 (Speaker 2)
3. **Lamla Mwanza** — Student ID: 2310385945 (Speaker 3)
4. **Gideon Namuya** — Student ID: 2310385918 (Speaker 4)

---

## 1. The 60-Second Summary (What is our project about?)
We built a prototype for the **ZUT Student Information System** (`zut_student_records`).
It stores student details, **NRC numbers**, courses, and exam marks.

**The Problem:**
If a university database is not secured:
1. A student or outsider can secretly change their marks from 45% to 90%.
2. A hacker can type a trick query into a search box and steal everyone's confidential NRC number (SQL Injection).

**Our Solution (The 3 Defenses we built):**
1. **Access Control (RBAC):** We created 3 separate roles:
   - **Admin:** Can do everything.
   - **Lecturer:** Can enter and change marks, but CANNOT delete students or drop tables.
   - **Student:** Can only view their own marks; CANNOT change anything or see peer NRCs.
2. **Parameterized Queries (SQL Injection Defense):**
   - An attacker types `' OR '1'='1` in the NRC search bar to dump the whole database.
   - A vulnerable query falls for it.
   - Our **Parameterized Query** treats the attack as plain text, blocking it completely (0 records leaked).
3. **Audit Log Trigger:**
   - If a lecturer updates a grade, a database trigger automatically logs: *who changed it, the exact time, the old mark, and the new mark* for accountability (non-repudiation).

---

## 2. How to Run the Demo on Thursday (Takes 10 Seconds)

1. Open PowerShell or Command Prompt in this folder.
2. Type:
   ```bash
   python web_app.py
   ```
3. Your browser automatically opens to `http://localhost:5000`.
4. Everything you need to click is right there on the screen!

---

## 3. Who Says What (Assigned for Comfort, Lubuto, Lamla, and Gideon)

### 👤 SPEAKER 1: Comfort Penyengwe — Foundations & Threats (Slides 1 to 3)
* **What you say:**
  > *"Good morning Lecturer. Today our group—Comfort Penyengwe, Lubuto Matambo, Lamla Mwanza, and Gideon Namuya—presents our project on Database Security under BIT3360. Databases hold an institution's most sensitive data—including student exam marks and confidential NRC numbers.*
  > 
  > *Database security is governed by the **CIA Triad**:*
  > * **Confidentiality:** *Keeping private data (like student NRCs) hidden from unauthorized people.*
  > * **Integrity:** *Making sure no one can secretly alter grades.*
  > * **Availability:** *Ensuring the database stays online during exams.*
  > 
  > *The two biggest threats databases face are:*
  > 1. **SQL Injection:** *When an attacker types SQL syntax into a web input to trick the database into dumping all records.*
  > 2. **Privilege Abuse:** *Giving regular users too much power—like a student having permission to edit marks.*
  > 
  > *Now Lubuto Matambo will explain our defenses."*

---

### 👤 SPEAKER 2: Lubuto Matambo — How We Defend Databases (Slides 4 to 6)
* **What you say:**
  > *"Thank you Comfort. To defend against these threats, we implement 3 core mechanisms:*
  > 
  > 1. **Role-Based Access Control & Least Privilege:** *Users only get the minimum permissions needed for their job. An Admin has full control; a Lecturer can only update marks; a Student has read-only access. If a student tries to change a mark, the database blocks it with an Error 1142 Access Denied.*
  > 2. **Parameterized Queries (Prepared Statements):** *This is the #1 defense against SQL Injection. The database compiles the SQL code FIRST. When user input arrives, it is treated strictly as plain text data, never as executable code.*
  > 3. **Data Encryption & Audit Triggers:** *Passwords are hashed using SHA-256 with salt so they cannot be reversed. And to stop insider fraud, we created an automatic database trigger that records every grade change in an audit log.*
  > 
  > *Now Lamla Mwanza will explain our system design."*

---

### 👤 SPEAKER 3: Lamla Mwanza — Tools, Law & Architecture (Slides 7 to 9)
* **What you say:**
  > *"Thank you Lubuto. In large corporations, database security is handled by enterprise tools like MySQL Enterprise Firewall (which blocks malicious queries in real time) and HashiCorp Vault (which rotates passwords automatically).*
  > 
  > *In Zambia, under the **Data Protection Act No. 3 of 2021**, institutions that handle personal records like NRC numbers are legally required to enforce technical safeguards.*
  > 
  > *For our prototype, we designed the **ZUT Student Records System** (`zut_student_records`). It contains:*
  > * `students` *(with `nrc`, student number, name)*
  > * `courses` *(course code, credits, lecturer)*
  > * `grades` *(marks, letter grades)*
  > * `audit_log` *(automated trail of all changes)*
  > 
  > *We created 3 database users: `sec_admin`, `sec_lecturer`, and `sec_student`. Now Gideon Namuya will show you our live demonstration."*

---

### 👤 SPEAKER 4: Gideon Namuya — The Live Demonstration & Wrap-up (Slides 10 to 12)
* **What you do and say on screen (`http://localhost:5000`):**

  1. **Click Tab 1 (Access Control):**
     * Click **Student** role $\rightarrow$ Click **"Alter Student Grade"**.
     * Point at the red box on screen:
       > *"Notice the database engine immediately blocked the student with **ACCESS DENIED (Error 1142)** under the Principle of Least Privilege."*
     * Now click **Lecturer** role $\rightarrow$ Click **"Alter Student Grade"**.
     * Point at the green box on screen:
       > *"Now it succeeds because lecturers possess UPDATE privileges on the grades table."*

  2. **Click Tab 2 (SQL Injection Defense):**
     * Click the quick-fill button: **`Payload: ' OR '1'='1`**.
     * Click **"Execute Vulnerable Query"**:
       > *"In dynamic SQL, string concatenation causes the condition to evaluate as TRUE for all rows. As you can see, all confidential student records and NRC numbers leak onto the screen!"*
     * Now click **"Execute Parameterized Query"**:
       > *"With our prepared statement, the database treats the payload as literal plain text. Zero records are leaked; the attack is completely neutralized!"*

  3. **Click Tab 3 (Audit Trail):**
     * Point at the table:
       > *"Here is our `audit_log` table. The database trigger automatically recorded who made the change (`sec_lecturer`), the timestamp, the previous mark, and the new mark for complete non-repudiation."*

  4. **Wrap-up (Slide 12):**
     > *"In conclusion, database security protects institutional integrity and ensures compliance with the Zambia Data Protection Act. Thank you, and Comfort, Lubuto, Lamla, and I are now ready to answer any questions!"*

---

## 4. Likely Questions the Lecturer Will Ask (And Your Answers)

**Q1: What is the Principle of Least Privilege?**
* **Answer:** Giving a user or program only the absolute minimum permissions needed to do their job, and nothing more. For example, a student only needs to read their own grades, not update them or view peer NRCs.

**Q2: Why does a Parameterized Query stop SQL Injection?**
* **Answer:** Because it separates **Code from Data**. The database engine compiles the SQL syntax *before* the user input is inserted. When user input arrives, it is strictly treated as a literal text value, so it can never alter the query logic.

**Q3: What is non-repudiation in your audit log?**
* **Answer:** Non-repudiation means a person cannot deny that they made a change. Because our database trigger captures the user account and timestamp inside the transaction automatically, there is indisputable proof of who modified a grade.
