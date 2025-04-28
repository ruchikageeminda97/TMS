-- tcms.sql
USE tcms;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(100) NOT NULL,
    role ENUM('Admin', 'Teacher', 'Student') NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

-- Students table
CREATE TABLE IF NOT EXISTS students (
    student_id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    address VARCHAR(200) NOT NULL,
    enrollment_date DATE NOT NULL,
    status ENUM('Active', 'Inactive') NOT NULL DEFAULT 'Active'
);

-- Teachers table
CREATE TABLE IF NOT EXISTS teachers (
    teacher_id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    address VARCHAR(200) NOT NULL,
    hire_date DATE NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    status ENUM('Active', 'Inactive') NOT NULL DEFAULT 'Active'
);

-- Subjects table
CREATE TABLE IF NOT EXISTS subjects (
    subject_id VARCHAR(10) PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    level ENUM('Beginner', 'Intermediate', 'Advanced') NOT NULL
);

-- Classes table
CREATE TABLE IF NOT EXISTS classes (
    class_id VARCHAR(10) PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    subject_id VARCHAR(10) NOT NULL,
    schedule VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    room_number VARCHAR(20),
    capacity INT NOT NULL,
    status ENUM('Ongoing', 'Completed', 'Cancelled') NOT NULL DEFAULT 'Ongoing',
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

-- Enrollments table
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id VARCHAR(10) PRIMARY KEY,
    student_id VARCHAR(10) NOT NULL,
    class_id VARCHAR(10) NOT NULL,
    enrollment_date DATE NOT NULL,
    payment_status ENUM('Paid', 'Pending') NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

-- Teacher Assignments table
CREATE TABLE IF NOT EXISTS teacher_assignments (
    assignment_id VARCHAR(10) PRIMARY KEY,
    teacher_id VARCHAR(10) NOT NULL,
    class_id VARCHAR(10) NOT NULL,
    assignment_date DATE NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

-- Payments table
CREATE TABLE IF NOT EXISTS payments (
    payment_id VARCHAR(10) PRIMARY KEY,
    enrollment_id VARCHAR(10) NOT NULL,
    amount FLOAT NOT NULL,
    payment_date DATE NOT NULL,
    status ENUM('Paid', 'Pending') NOT NULL DEFAULT 'Paid',
    FOREIGN KEY (enrollment_id) REFERENCES enrollments(enrollment_id)
);

-- Attendance table
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id VARCHAR(10) PRIMARY KEY,
    student_id VARCHAR(10) NOT NULL,
    class_id VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    status ENUM('Present', 'Absent') NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

-- Grades table
CREATE TABLE IF NOT EXISTS grades (
    grade_id VARCHAR(10) PRIMARY KEY,
    student_id VARCHAR(10) NOT NULL,
    class_id VARCHAR(10) NOT NULL,
    subject_id VARCHAR(10) NOT NULL,
    score FLOAT NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);