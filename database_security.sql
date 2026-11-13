-- =====================================================================
-- ZAMBIA UNIVERSITY COLLEGE OF TECHNOLOGY (ZUT)
-- BIT3360: ADVANCED DATABASES - GROUP ASSIGNMENT
-- TOPIC: DATABASE SECURITY PROTOTYPE
-- DATABASE: zut_student_records
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. DATABASE CREATION AND INITIALIZATION
-- ---------------------------------------------------------------------
DROP DATABASE IF EXISTS zut_student_records;
CREATE DATABASE zut_student_records
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE zut_student_records;

-- ---------------------------------------------------------------------
-- 2. SCHEMA DEFINITION
-- ---------------------------------------------------------------------

-- Table: students
-- Stores confidential student details including NRC
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_number VARCHAR(20) NOT NULL UNIQUE,
    nrc VARCHAR(20) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    program VARCHAR(100) NOT NULL,
    year_of_study INT NOT NULL CHECK (year_of_study BETWEEN 1 AND 5),
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Table: courses
CREATE TABLE courses (
    course_code VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    credits INT NOT NULL DEFAULT 15,
    lecturer_name VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- Table: grades
-- Sensitive academic data requiring strict access controls
CREATE TABLE grades (
    grade_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_code VARCHAR(10) NOT NULL,
    mark DECIMAL(5, 2) NOT NULL CHECK (mark BETWEEN 0 AND 100),
    grade_letter VARCHAR(2) NOT NULL,
    semester VARCHAR(20) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_code) REFERENCES courses(course_code) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Table: audit_log
-- Tamper-evident audit trail for accountability and non-repudiation
CREATE TABLE audit_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    action_type VARCHAR(20) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    record_id INT NOT NULL,
    changed_by VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- 3. AUDIT LOGGING TRIGGERS (ADDITIONAL SECURITY MEASURE)
-- ---------------------------------------------------------------------

-- Trigger: trg_grades_audit_update
-- Automatically tracks any changes made to grades (who, when, old mark, new mark)
DELIMITER $$
CREATE TRIGGER trg_grades_audit_update
AFTER UPDATE ON grades
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (
        action_type,
        table_name,
        record_id,
        changed_by,
        old_value,
        new_value
    ) VALUES (
        'UPDATE',
        'grades',
        NEW.grade_id,
        USER(),
        CONCAT('student_id=', OLD.student_id, ', course=', OLD.course_code, ', mark=', OLD.mark, ', grade=', OLD.grade_letter),
        CONCAT('student_id=', NEW.student_id, ', course=', NEW.course_code, ', mark=', NEW.mark, ', grade=', NEW.grade_letter)
    );
END$$

-- Trigger: trg_grades_audit_delete
-- Tracks any deletion of grade records
CREATE TRIGGER trg_grades_audit_delete
AFTER DELETE ON grades
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (
        action_type,
        table_name,
        record_id,
        changed_by,
        old_value,
        new_value
    ) VALUES (
        'DELETE',
        'grades',
        OLD.grade_id,
        USER(),
        CONCAT('student_id=', OLD.student_id, ', course=', OLD.course_code, ', mark=', OLD.mark),
        'RECORD DELETED'
    );
END$$
DELIMITER ;

-- ---------------------------------------------------------------------
-- 4. SAMPLE DATA POPULATION
-- ---------------------------------------------------------------------

INSERT INTO students (student_number, nrc, full_name, program, year_of_study, email) VALUES
('ZUT/2023/0142', '294812/10/1', 'Chileshe Mwape', 'BSc Information Technology', 3, 'cmwape@zut.ac.zm'),
('ZUT/2023/0188', '381940/11/1', 'Kondwani Banda', 'BSc Computer Science', 3, 'kbanda@zut.ac.zm'),
('ZUT/2023/0205', '412093/67/1', 'Thandiwe Phiri', 'BSc Information Systems', 3, 'tphiri@zut.ac.zm'),
('ZUT/2023/0277', '194820/82/1', 'Mutale Musonda', 'BSc Information Technology', 3, 'mmusonda@zut.ac.zm'),
('ZUT/2023/0310', '581932/10/1', 'Natasha Tembo', 'BSc Software Engineering', 3, 'ntembo@zut.ac.zm');

INSERT INTO courses (course_code, course_name, credits, lecturer_name) VALUES
('BIT3360', 'Advanced Databases', 15, 'Dr. C. Chanda'),
('BIT3320', 'Network & Database Security', 15, 'Mr. P. Mulenga'),
('BIT3310', 'Software Architecture & Design', 15, 'Mrs. F. Mumba');

INSERT INTO grades (student_id, course_code, mark, grade_letter, semester) VALUES
(1, 'BIT3360', 78.50, 'A', 'Semester 1 2026'),
(1, 'BIT3320', 82.00, 'A+', 'Semester 1 2026'),
(2, 'BIT3360', 64.00, 'B', 'Semester 1 2026'),
(2, 'BIT3320', 71.50, 'B+', 'Semester 1 2026'),
(3, 'BIT3360', 89.00, 'A+', 'Semester 1 2026'),
(4, 'BIT3360', 55.00, 'C+', 'Semester 1 2026'),
(5, 'BIT3360', 91.50, 'A+', 'Semester 1 2026');

-- ---------------------------------------------------------------------
-- 5. SECURE VIEW FOR STUDENTS (LEAST PRIVILEGE DATA FILTERING)
-- ---------------------------------------------------------------------
-- A view masking student NRC and only showing academic standing
CREATE OR REPLACE VIEW vw_student_grades AS
SELECT 
    s.student_number,
    s.full_name,
    c.course_code,
    c.course_name,
    g.mark,
    g.grade_letter,
    g.semester
FROM students s
JOIN grades g ON s.student_id = g.student_id
JOIN courses c ON g.course_code = c.course_code;

-- ---------------------------------------------------------------------
-- 6. ROLE-BASED ACCESS CONTROL (RBAC): USERS & PERMISSIONS
-- ---------------------------------------------------------------------

-- Remove existing demo users if they exist
DROP USER IF EXISTS 'sec_admin'@'localhost';
DROP USER IF EXISTS 'sec_lecturer'@'localhost';
DROP USER IF EXISTS 'sec_student'@'localhost';

-- User 1: Database Administrator (DBA)
-- Has complete administrative privileges over the database
CREATE USER 'sec_admin'@'localhost' IDENTIFIED BY 'Admin@Zut2026#Secure';
GRANT ALL PRIVILEGES ON zut_student_records.* TO 'sec_admin'@'localhost' WITH GRANT OPTION;

-- User 2: Lecturer
-- Needs to view student info and enter/modify grades, but CANNOT delete tables or drop DB
CREATE USER 'sec_lecturer'@'localhost' IDENTIFIED BY 'Lecturer@Zut2026#Pass';
GRANT SELECT ON zut_student_records.students TO 'sec_lecturer'@'localhost';
GRANT SELECT ON zut_student_records.courses TO 'sec_lecturer'@'localhost';
GRANT SELECT, INSERT, UPDATE ON zut_student_records.grades TO 'sec_lecturer'@'localhost';
GRANT SELECT ON zut_student_records.audit_log TO 'sec_lecturer'@'localhost';
-- Note: NO DELETE or DROP permissions granted to lecturer.

-- User 3: Student
-- Strictly restricted to viewing grade summaries; NO INSERT, UPDATE, DELETE permissions
CREATE USER 'sec_student'@'localhost' IDENTIFIED BY 'Student@Zut2026#Pass';
GRANT SELECT ON zut_student_records.vw_student_grades TO 'sec_student'@'localhost';
-- Note: Student has zero access to the base `students` table (cannot see NRCs) and zero write access to `grades`.

FLUSH PRIVILEGES;

-- =====================================================================
-- 7. SECURITY DEMONSTRATION & VERIFICATION INSTRUCTIONS
-- =====================================================================
/*
TEST CASE 1: Administrator (Full Access)
----------------------------------------
mysql -u sec_admin -pAdmin@Zut2026#Secure zut_student_records
SQL> SELECT * FROM students;                       --> [SUCCESS]
SQL> SELECT * FROM audit_log;                     --> [SUCCESS]

TEST CASE 2: Lecturer Permissions Verification
----------------------------------------------
mysql -u sec_lecturer -pLecturer@Zut2026#Pass zut_student_records
SQL> SELECT * FROM students;                       --> [SUCCESS] (Lecturer needs to see students)
SQL> UPDATE grades SET mark = 85.00 WHERE grade_id = 1; --> [SUCCESS] (Updates grade)
SQL> SELECT * FROM audit_log;                     --> [SUCCESS] (Trigger logged the update!)
SQL> DROP TABLE students;                         --> [ACCESS DENIED! ERROR 1142 (42000)]
SQL> DELETE FROM students WHERE student_id = 1;   --> [ACCESS DENIED! ERROR 1142 (42000)]

TEST CASE 3: Student Permissions Verification
---------------------------------------------
mysql -u sec_student -pStudent@Zut2026#Pass zut_student_records
SQL> SELECT * FROM vw_student_grades;             --> [SUCCESS] (Can view sanitized view)
SQL> SELECT nrc FROM students;                    --> [ACCESS DENIED! ERROR 1142 (42000)]
SQL> UPDATE grades SET mark = 100 WHERE grade_id = 1; --> [ACCESS DENIED! ERROR 1142 (42000)]
SQL> DROP TABLE grades;                           --> [ACCESS DENIED! ERROR 1142 (42000)]
*/
