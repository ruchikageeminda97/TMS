-- Create Database
CREATE DATABASE IF NOT EXISTS tcms;
USE tcms;

-- Users Table
CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(100) NOT NULL,
    role ENUM('Admin', 'Teacher', 'Student') NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Students Table
CREATE TABLE students (
    student_id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    address VARCHAR(200) NOT NULL,
    enrollment_date DATE NOT NULL,
    status ENUM('Active', 'Inactive') DEFAULT 'Active' NOT NULL
);

-- Teachers Table
CREATE TABLE teachers (
    teacher_id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    address VARCHAR(200) NOT NULL,
    hire_date DATE NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    status ENUM('Active', 'Inactive') DEFAULT 'Active' NOT NULL
);

-- Subjects Table
CREATE TABLE subjects (
    subject_id VARCHAR(10) PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    level ENUM('Beginner', 'Intermediate', 'Advanced') NOT NULL
);

-- Classes Table
CREATE TABLE classes (
    class_id VARCHAR(10) PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    subject_id VARCHAR(10) NOT NULL,
    schedule VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    room_number VARCHAR(20),
    capacity INT NOT NULL,
    status ENUM('Ongoing', 'Completed', 'Cancelled') DEFAULT 'Ongoing' NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

-- Enrollments Table
CREATE TABLE enrollments (
    enrollment_id VARCHAR(10) PRIMARY KEY,
    student_id VARCHAR(10) NOT NULL,
    class_id VARCHAR(10) NOT NULL,
    enrollment_date DATE NOT NULL,
    payment_status ENUM('Paid', 'Pending') DEFAULT 'Pending' NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

-- Teacher Assignments Table
CREATE TABLE teacher_assignments (
    assignment_id VARCHAR(10) PRIMARY KEY,
    teacher_id VARCHAR(10) NOT NULL,
    class_id VARCHAR(10) NOT NULL,
    assignment_date DATE NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

-- Payments Table
CREATE TABLE payments (
    payment_id VARCHAR(10) PRIMARY KEY,
    enrollment_id VARCHAR(10) NOT NULL,
    amount FLOAT NOT NULL,
    payment_date DATE NOT NULL,
    status ENUM('Paid', 'Pending') DEFAULT 'Paid' NOT NULL,
    FOREIGN KEY (enrollment_id) REFERENCES enrollments(enrollment_id)
);

-- Attendance Table
CREATE TABLE attendance (
    attendance_id VARCHAR(10) PRIMARY KEY,
    student_id VARCHAR(10) NOT NULL,
    class_id VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    status ENUM('Present', 'Absent') NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

-- Grades Table
CREATE TABLE grades (
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