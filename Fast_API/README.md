// Switch to the tcms database (creates it if it doesn't exist)
use tcms;

// Create the users collection
// MySQL: username (PK, String(50)), password (String(100)), role (Enum: Admin, Teacher, Student), email (String(100), unique)
db.users.createIndex({ username: 1 }, { unique: true }); // Primary key equivalent
db.users.createIndex({ email: 1 }, { unique: true }); // Unique constraint on email
// Note: Role is stored as a string (Admin, Teacher, Student) without explicit enum validation
// Sample document (optional, for testing):
db.users.insertOne({
    username: "testuser",
    password: "$2b$12$samplehashedpassword",
    role: "Admin",
    email: "testuser@example.com"
});
db.users.deleteOne({ username: "testuser" }); // Remove sample document

// Create the students collection
// MySQL: student_id (PK, String(10)), first_name (String(50)), last_name (String(50)), date_of_birth (Date), 
// gender (String(10)), contact_number (String(20)), email (String(100), unique), address (String(200)), 
// enrollment_date (Date), status (Enum: Active, Inactive)
db.students.createIndex({ student_id: 1 }, { unique: true }); // Primary key equivalent
db.students.createIndex({ email: 1 }, { unique: true }); // Unique constraint on email
// Note: status is stored as a string (Active, Inactive)
// Sample document (optional):
db.students.insertOne({
    student_id: "STU001",
    first_name: "John",
    last_name: "Doe",
    date_of_birth: ISODate("2000-01-01"),
    gender: "Male",
    contact_number: "1234567890",
    email: "john.doe@example.com",
    address: "123 Main St",
    enrollment_date: ISODate("2025-01-01"),
    status: "Active"
});
db.students.deleteOne({ student_id: "STU001" });

// Create the teachers collection
// MySQL: teacher_id (PK, String(10)), first_name (String(50)), last_name (String(50)), contact_number (String(20)), 
// email (String(100), unique), address (String(200)), hire_date (Date), specialization (String(100)), 
// status (Enum: Active, Inactive)
db.teachers.createIndex({ teacher_id: 1 }, { unique: true }); // Primary key equivalent
db.teachers.createIndex({ email: 1 }, { unique: true }); // Unique constraint on email
// Note: status is stored as a string (Active, Inactive)
// Sample document (optional):
db.teachers.insertOne({
    teacher_id: "TEA001",
    first_name: "Jane",
    last_name: "Smith",
    contact_number: "0987654321",
    email: "jane.smith@example.com",
    address: "456 Oak St",
    hire_date: ISODate("2024-01-01"),
    specialization: "Mathematics",
    status: "Active"
});
db.teachers.deleteOne({ teacher_id: "TEA001" });

// Create the subjects collection
// MySQL: subject_id (PK, String(10)), subject_name (String(100)), description (String(500)), 
// level (Enum: Beginner, Intermediate, Advanced)
db.subjects.createIndex({ subject_id: 1 }, { unique: true }); // Primary key equivalent
// Note: level is stored as a string (Beginner, Intermediate, Advanced)
// Sample document (optional):
db.subjects.insertOne({
    subject_id: "SUB001",
    subject_name: "Mathematics",
    description: "Basic algebra and geometry",
    level: "Beginner"
});
db.subjects.deleteOne({ subject_id: "SUB001" });

// Create the classes collection
// MySQL: class_id (PK, String(10)), class_name (String(100)), subject_id (FK to subjects, String(10)), 
// schedule (String(100)), start_date (Date), end_date (Date), room_number (String(20)), capacity (Integer), 
// status (Enum: Ongoing, Completed, Cancelled)
db.classes.createIndex({ class_id: 1 }, { unique: true }); // Primary key equivalent
// Note: subject_id is stored as a string reference to subjects.subject_id
// status is stored as a string (Ongoing, Completed, Cancelled)
// Sample document (optional):
db.classes.insertOne({
    class_id: "CLS001",
    class_name: "Math 101",
    subject_id: "SUB001",
    schedule: "Mon-Wed 10:00-11:30",
    start_date: ISODate("2025-01-01"),
    end_date: ISODate("2025-06-30"),
    room_number: "101",
    capacity: 30,
    status: "Ongoing"
});
db.classes.deleteOne({ class_id: "CLS001" });

// Create the enrollments collection
// MySQL: enrollment_id (PK, String(10)), student_id (FK to students, String(10)), 
// class_id (FK to classes, String(10)), enrollment_date (Date), 
// payment_status (Enum: Paid, Pending)
db.enrollments.createIndex({ enrollment_id: 1 }, { unique: true }); // Primary key equivalent
// Note: student_id and class_id are stored as string references
// payment_status is stored as a string (Paid, Pending)
// Sample document (optional):
db.enrollments.insertOne({
    enrollment_id: "ENR001",
    student_id: "STU001",
    class_id: "CLS001",
    enrollment_date: ISODate("2025-01-01"),
    payment_status: "Pending"
});
db.enrollments.deleteOne({ enrollment_id: "ENR001" });

// Create the teacher_assignments collection
// MySQL: assignment_id (PK, String(10)), teacher_id (FK to teachers, String(10)), 
// class_id (FK to classes, String(10)), assignment_date (Date)
db.teacher_assignments.createIndex({ assignment_id: 1 }, { unique: true }); // Primary key equivalent
// Note: teacher_id and class_id are stored as string references
// Sample document (optional):
db.teacher_assignments.insertOne({
    assignment_id: "ASN001",
    teacher_id: "TEA001",
    class_id: "CLS001",
    assignment_date: ISODate("2025-01-01")
});
db.teacher_assignments.deleteOne({ assignment_id: "ASN001" });

// Create the payments collection
// MySQL: payment_id (PK, String(10)), enrollment_id (FK to enrollments, String(10)), 
// amount (Float), payment_date (Date), status (Enum: Paid, Pending)
db.payments.createIndex({ payment_id: 1 }, { unique: true }); // Primary key equivalent
// Note: enrollment_id is stored as a string reference
// status is stored as a string (Paid, Pending)
// Sample document (optional):
db.payments.insertOne({
    payment_id: "PAY001",
    enrollment_id: "ENR001",
    amount: 500.0,
    payment_date: ISODate("2025-01-02"),
    status: "Paid"
});
db.payments.deleteOne({ payment_id: "PAY001" });

// Create the attendance collection
// MySQL: attendance_id (PK, String(10)), student_id (FK to students, String(10)), 
// class_id (FK to classes, String(10)), date (Date), status (Enum: Present, Absent)
db.attendance.createIndex({ attendance_id: 1 }, { unique: true }); // Primary key equivalent
// Note: student_id and class_id are stored as string references
// status is stored as a string (Present, Absent)
// Sample document (optional):
db.attendance.insertOne({
    attendance_id: "ATT001",
    student_id: "STU001",
    class_id: "CLS001",
    date: ISODate("2025-01-03"),
    status: "Present"
});
db.attendance.deleteOne({ attendance_id: "ATT001" });

// Create the grades collection
// MySQL: grade_id (PK, String(10)), student_id (FK to students, String(10)), 
// class_id (FK to classes, String(10)), subject_id (FK to subjects, String(10)), 
// score (Float), date (Date)
db.grades.createIndex({ grade_id: 1 }, { unique: true }); // Primary key equivalent
// Note: student_id, class_id, and subject_id are stored as string references
// Sample document (optional):
db.grades.insertOne({
    grade_id: "GRD001",
    student_id: "STU001",
    class_id: "CLS001",
    subject_id: "SUB001",
    score: 85.5,
    date: ISODate("2025-01-04")
});
db.grades.deleteOne({ grade_id: "GRD001" });

// Verify all collections
db.getCollectionNames();