from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from enum import Enum
from sqlalchemy import create_engine, Column, String, Date, Float, Integer, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship
from sqlalchemy.exc import IntegrityError
import uuid

# At the top of index.py
import logging

import uvicorn
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Tuition Class Management System (TCMS)",
    description="API for managing students, tutors, classes, subjects, enrollments, teacher assignments, payments, attendance, and grades in a tuition center.",
    version="1.0",
    openapi_tags=[
        {"name": "Auth", "description": "User authentication and registration."},
        {"name": "Students", "description": "Operations related to student management."},
        {"name": "Teachers", "description": "APIs for teacher management."},
        {"name": "Subjects", "description": "APIs for subject management."},
        {"name": "Classes", "description": "APIs for class management."},
        {"name": "Enrollments", "description": "APIs for managing student enrollments in classes."},
        {"name": "TeacherAssignments", "description": "APIs for managing teacher assignments to classes."},
        {"name": "Payments", "description": "Handles payment processing."},
        {"name": "Attendance", "description": "Handles attendance tracking."},
        {"name": "Grades", "description": "Handles grades and progress tracking."},
    ]
)
print("FastAPI app initialized")

# Hardcoded database credentials
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "tcms"

# Create database URL
DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
print("Database URL:", DATABASE_URL)

# Test database connection
try:
    engine = create_engine(DATABASE_URL)
    print("Database connection successful")
except Exception as e:
    print(f"Database connection failed: {e}")
    raise

# Create SQLAlchemy base and session
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print("SQLAlchemy base and session initialized")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Enums for Status Fields
class StudentStatus(str, Enum):
    active = "Active"
    inactive = "Inactive"

class TeacherStatus(str, Enum):
    active = "Active"
    inactive = "Inactive"

class ClassStatus(str, Enum):
    ongoing = "Ongoing"
    completed = "Completed"
    cancelled = "Cancelled"

class PaymentStatus(str, Enum):
    paid = "Paid"
    pending = "Pending"

class AttendanceStatus(str, Enum):
    present = "Present"
    absent = "Absent"

class SubjectLevel(str, Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"

class UserRole(str, Enum):
    admin = "Admin"
    teacher = "Teacher"
    student = "Student"

# SQLAlchemy Models
class UserDB(Base):
    __tablename__ = "users"
    username = Column(String(50), primary_key=True)
    password = Column(String(100), nullable=False)  # In production, hash passwords
    role = Column(SQLAlchemyEnum(UserRole), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

class StudentDB(Base):
    __tablename__ = "students"
    student_id = Column(String(10), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    contact_number = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    address = Column(String(200), nullable=False)
    enrollment_date = Column(Date, nullable=False)
    status = Column(SQLAlchemyEnum(StudentStatus), default=StudentStatus.active, nullable=False)

class TeacherDB(Base):
    __tablename__ = "teachers"
    teacher_id = Column(String(10), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    contact_number = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    address = Column(String(200), nullable=False)
    hire_date = Column(Date, nullable=False)
    specialization = Column(String(100), nullable=False)
    status = Column(SQLAlchemyEnum(TeacherStatus), default=TeacherStatus.active, nullable=False)

class SubjectDB(Base):
    __tablename__ = "subjects"
    subject_id = Column(String(10), primary_key=True)
    subject_name = Column(String(100), nullable=False)
    description = Column(String(500))
    level = Column(SQLAlchemyEnum(SubjectLevel), nullable=False)

class ClassDB(Base):
    __tablename__ = "classes"
    class_id = Column(String(10), primary_key=True)
    class_name = Column(String(100), nullable=False)
    subject_id = Column(String(10), ForeignKey("subjects.subject_id"), nullable=False)
    schedule = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    room_number = Column(String(20))
    capacity = Column(Integer, nullable=False)
    status = Column(SQLAlchemyEnum(ClassStatus), default=ClassStatus.ongoing, nullable=False)
    subject = relationship("SubjectDB")

class EnrollmentDB(Base):
    __tablename__ = "enrollments"
    enrollment_id = Column(String(10), primary_key=True)
    student_id = Column(String(10), ForeignKey("students.student_id"), nullable=False)
    class_id = Column(String(10), ForeignKey("classes.class_id"), nullable=False)
    enrollment_date = Column(Date, nullable=False)
    payment_status = Column(SQLAlchemyEnum(PaymentStatus), default=PaymentStatus.pending, nullable=False)
    student = relationship("StudentDB")
    class_ = relationship("ClassDB")

class TeacherAssignmentDB(Base):
    __tablename__ = "teacher_assignments"
    assignment_id = Column(String(10), primary_key=True)
    teacher_id = Column(String(10), ForeignKey("teachers.teacher_id"), nullable=False)
    class_id = Column(String(10), ForeignKey("classes.class_id"), nullable=False)
    assignment_date = Column(Date, nullable=False)
    teacher = relationship("TeacherDB")
    class_ = relationship("ClassDB")

class PaymentDB(Base):
    __tablename__ = "payments"
    payment_id = Column(String(10), primary_key=True)
    enrollment_id = Column(String(10), ForeignKey("enrollments.enrollment_id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False)
    status = Column(SQLAlchemyEnum(PaymentStatus), default=PaymentStatus.paid, nullable=False)
    enrollment = relationship("EnrollmentDB")

class AttendanceDB(Base):
    __tablename__ = "attendance"
    attendance_id = Column(String(10), primary_key=True)
    student_id = Column(String(10), ForeignKey("students.student_id"), nullable=False)
    class_id = Column(String(10), ForeignKey("classes.class_id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(SQLAlchemyEnum(AttendanceStatus), nullable=False)
    student = relationship("StudentDB")
    class_ = relationship("ClassDB")

class GradeDB(Base):
    __tablename__ = "grades"
    grade_id = Column(String(10), primary_key=True)
    student_id = Column(String(10), ForeignKey("students.student_id"), nullable=False)
    class_id = Column(String(10), ForeignKey("classes.class_id"), nullable=False)
    subject_id = Column(String(10), ForeignKey("subjects.subject_id"), nullable=False)
    score = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    student = relationship("StudentDB")
    class_ = relationship("ClassDB")
    subject = relationship("SubjectDB")

# Pydantic Models
class User(BaseModel):
    username: str
    password: str
    role: UserRole
    email: str

class Student(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    contact_number: str
    email: str
    address: str
    enrollment_date: date
    status: StudentStatus = StudentStatus.active

class Teacher(BaseModel):
    teacher_id: str
    first_name: str
    last_name: str
    contact_number: str
    email: str
    address: str
    hire_date: date
    specialization: str
    status: TeacherStatus = TeacherStatus.active

class Subject(BaseModel):
    subject_id: str
    subject_name: str
    description: Optional[str] = None
    level: SubjectLevel

class Class(BaseModel):
    class_id: str
    class_name: str
    subject_id: str
    schedule: str
    start_date: date
    end_date: date
    room_number: Optional[str] = None
    capacity: int
    status: ClassStatus = ClassStatus.ongoing

class Enrollment(BaseModel):
    enrollment_id: str
    student_id: str
    class_id: str
    enrollment_date: date
    payment_status: PaymentStatus = PaymentStatus.pending

class TeacherAssignment(BaseModel):
    assignment_id: str
    teacher_id: str
    class_id: str
    assignment_date: date

class Payment(BaseModel):
    payment_id: str
    enrollment_id: str
    amount: float
    payment_date: date
    status: PaymentStatus = PaymentStatus.paid

class Attendance(BaseModel):
    attendance_id: str
    student_id: str
    class_id: str
    date: date
    status: AttendanceStatus

class Grade(BaseModel):
    grade_id: str
    student_id: str
    class_id: str
    subject_id: str
    score: float
    date: date

# Helper function to find user
def find_user(db: Session, username: str) -> Optional[UserDB]:
    return db.query(UserDB).filter(UserDB.username == username).first()

# # Create database tables
# try:
#     Base.metadata.create_all(bind=engine)
#     print("Database tables created successfully")
# except Exception as e:
#     print(f"Failed to create database tables: {e}")
#     raise
# print("Application startup completed")
print("Skipping table creation (handled manually)")
print("Application startup completed")

# Authentication Endpoints
@app.post("/register/", tags=["Auth"], response_model=User)
def register(user: User, db: Session = Depends(get_db)):
    """Register a new user"""
    if find_user(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    db_user = UserDB(**user.dict())
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    return user

@app.post("/login/", tags=["Auth"])
def login(username: str, password: str, db: Session = Depends(get_db)):
    """Login and verify user credentials"""
    user = find_user(db, username)
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": f"Login successful for {username} with role {user.role}"}

# Student Management
@app.post("/students/", tags=["Students"], response_model=Student)
def enroll_student(student: Student, username: str, db: Session = Depends(get_db)):
    """Enroll a new student (requires admin or teacher role)"""
    user = find_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if user.role not in [UserRole.admin, UserRole.teacher]:
        raise HTTPException(status_code=403, detail="Not authorized to enroll students")
    if db.query(StudentDB).filter(StudentDB.student_id == student.student_id).first():
        raise HTTPException(status_code=400, detail="Student ID already exists")
    db_student = StudentDB(**student.dict())
    try:
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    return student

@app.get("/students/{student_id}", tags=["Students"], response_model=Student)
def get_student(student_id: str, username: str, db: Session = Depends(get_db)):
    """Retrieve student details by ID (requires login)"""
    if not find_user(db, username):
        raise HTTPException(status_code=401, detail="User not found")
    student = db.query(StudentDB).filter(StudentDB.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.get("/students/", tags=["Students"], response_model=List[Student])
def list_students(username: str, db: Session = Depends(get_db)):
    """List all students (requires login)"""
    if not find_user(db, username):
        raise HTTPException(status_code=401, detail="User not found")
    return db.query(StudentDB).all()

# Teacher Management
@app.post("/teachers/", tags=["Teachers"], response_model=Teacher)
def add_teacher(teacher: Teacher, username: str, db: Session = Depends(get_db)):
    """Add a new teacher (requires admin role)"""
    user = find_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized to add teachers")
    if db.query(TeacherDB).filter(TeacherDB.teacher_id == teacher.teacher_id).first():
        raise HTTPException(status_code=400, detail="Teacher ID already exists")
    db_teacher = TeacherDB(**teacher.dict())
    try:
        db.add(db_teacher)
        db.commit()
        db.refresh(db_teacher)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    return teacher

@app.get("/teachers/{teacher_id}", tags=["Teachers"], response_model=Teacher)
def get_teacher(teacher_id: str, username: str, db: Session = Depends(get_db)):
    """Retrieve teacher details by ID (requires login)"""
    if not find_user(db, username):
        raise HTTPException(status_code=401, detail="User not found")
    teacher = db.query(TeacherDB).filter(TeacherDB.teacher_id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@app.get("/teachers/", tags=["Teachers"], response_model=List[Teacher])
def list_teachers(username: str, db: Session = Depends(get_db)):
    """List all teachers (requires login)"""
    if not find_user(db, username):
        raise HTTPException(status_code=401, detail="User not found")
    return db.query(TeacherDB).all()

# Subject Management
@app.post("/subjects/", tags=["Subjects"], response_model=Subject)
def add_subject(subject: Subject, username: str, db: Session = Depends(get_db)):
    """Add a new subject (requires admin role)"""
    user = find_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized to add subjects")
    if db.query(SubjectDB).filter(SubjectDB.subject_id == subject.subject_id).first():
        raise HTTPException(status_code=400, detail="Subject ID already exists")
    db_subject = SubjectDB(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return subject

@app.get("/subjects/{subject_id}", tags=["Subjects"], response_model=Subject)
def get_subject(subject_id: str, username: str, db: Session = Depends(get_db)):
    """Retrieve subject details by ID (requires login)"""
    if not find_user(db, username):
        raise HTTPException(status_code=401, detail="User not found")
    subject = db.query(SubjectDB).filter(SubjectDB.subject_id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@app.get("/subjects/", tags=["Subjects"], response_model=List[Subject])
def list_subjects(username: str, db: Session = Depends(get_db)):
    """List all subjects (requires login)"""
    if not find_user(db, username):
        raise HTTPException(status_code=401, detail="User not found")
    return db.query(SubjectDB).all()

# Class Management
@app.post("/classes/", tags=["Classes"], response_model=Class)
def create_class(class_: Class, username: str, db: Session = Depends(get_db)):
    """Create a new class (requires admin role)"""
    user = find_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized to create classes")
    if db.query(ClassDB).filter(ClassDB.class_id == class_.class_id).first():
        raise HTTPException(status_code=400, detail="Class ID already exists")
    if not db.query(SubjectDB).filter(SubjectDB.subject_id == class_.subject_id).first():
        raise HTTPException(status_code=404, detail="Subject not found")
    db_class = ClassDB(**class_.dict())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return class_

@app.get("/classes/{class_id}", tags=["Classes"], response_model=Class)
def get_class(class_id: str, username: str, db: Session = Depends(get_db)):
    """Retrieve class details by ID (requires login)"""
    if not find_user(db, username):
        raise HTTPException(status_code=401, detail="User not found")
    class_ = db.query(ClassDB).filter(ClassDB.class_id == class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_

@app.get("/classes/", tags=["Classes"], response_model=List[Class])
def list_classes(username: str, db: Session = Depends(get_db)):
    """List all classes (requires login)"""
    if not find_user(db, username):
        raise HTTPException(status_code=401, detail="User not found")
    return db.query(ClassDB).all()

# Enrollment Management
@app.post("/enrollments/", tags=["Enrollments"], response_model=Enrollment)
def enroll_student_in_class(enrollment: Enrollment, username: str, db: Session = Depends(get_db)):
    """Enroll a student in a class (requires admin or teacher role)"""
    user = find_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if user.role not in [UserRole.admin, UserRole.teacher]:
        raise HTTPException(status_code=403, detail="Not authorized to enroll students in classes")
    if db.query(EnrollmentDB).filter(EnrollmentDB.enrollment_id == enrollment.enrollment_id).first():
        raise HTTPException(status_code=400, detail="Enrollment ID already exists")
    if not db.query(StudentDB).filter(StudentDB.student_id == enrollment.student_id).first():
        raise HTTPException(status_code=404, detail="Student not found")
    class_ = db.query(ClassDB).filter(ClassDB.class_id == enrollment.class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    enrolled_count = db.query(EnrollmentDB).filter(EnrollmentDB.class_id == enrollment.class_id).count()
    if enrolled_count >= class_.capacity:
        raise HTTPException(status_code=400, detail="Class capacity reached")
    db_enrollment = EnrollmentDB(**enrollment.dict())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return enrollment

@app.get("/enrollments/", tags=["Enrollments"], response_model=List[Enrollment])
def list_enrollments(username: str, db: Session = Depends(get_db)):
    """List all enrollments (requires login)"""
    if not find_user(db, username):
        raise HTTPException(status_code=401, detail="User not found")
    return db.query(EnrollmentDB).all()

# Teacher Assignment Management
@app.post("/teacher-assignments/", tags=["TeacherAssignments"], response_model=TeacherAssignment)
def assign_teacher_to_class(assignment: TeacherAssignment, username: str, db: Session = Depends(get_db)):
    """Assign a teacher to a class (requires admin role)"""
    user = find_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized to assign teachers")
    if db.query(TeacherAssignmentDB).filter(TeacherAssignmentDB.assignment_id == assignment.assignment_id).first():
        raise HTTPException(status_code=400, detail="Assignment ID already exists")
    if not db.query(TeacherDB).filter(TeacherDB.teacher_id == assignment.teacher_id).first():
        raise HTTPException(status_code=404, detail="Teacher not found")
    if not db.query(ClassDB).filter(ClassDB.class_id == assignment.class_id).first():
        raise HTTPException(status_code=404, detail="Class not found")
    db_assignment = TeacherAssignmentDB(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return assignment

@app.get("/teacher-assignments/", tags=["TeacherAssignments"], response_model=List[TeacherAssignment])
def list_teacher_assignments(username: str, db: Session = Depends(get_db)):
    """List all teacher assignments (requires login)"""
    if not find_user(db, username):
        raise HTTPException(status_code=401, detail="User not found")
    return db.query(TeacherAssignmentDB).all()

# Payment Management
@app.post("/payments/", tags=["Payments"], response_model=Payment)
def process_payment(payment: Payment, username: str, db: Session = Depends(get_db)):
    """Process a payment for an enrollment (requires admin role)"""
    user = find_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized to process payments")
    if db.query(PaymentDB).filter(PaymentDB.payment_id == payment.payment_id).first():
        raise HTTPException(status_code=400, detail="Payment ID already exists")
    enrollment = db.query(EnrollmentDB).filter(EnrollmentDB.enrollment_id == payment.enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db_payment = PaymentDB(**payment.dict())
    enrollment.payment_status = PaymentStatus.paid
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return payment

@app.get("/payments/", tags=["Payments"], response_model=List[Payment])
def get_all_payments(username: str, db: Session = Depends(get_db)):
    """Retrieve all payments made (requires login)"""
    if not find_user(db, username):
        raise HTTPException(status_code=401, detail="User not found")
    return db.query(PaymentDB).all()

# Attendance Management
@app.post("/attendance/", tags=["Attendance"], response_model=Attendance)
def record_attendance(attendance: Attendance, username: str, db: Session = Depends(get_db)):
    """Record attendance for a student in a class (requires teacher role)"""
    user = find_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if user.role not in [UserRole.admin, UserRole.teacher]:
        raise HTTPException(status_code=403, detail="Not authorized to record attendance")
    if db.query(AttendanceDB).filter(AttendanceDB.attendance_id == attendance.attendance_id).first():
        raise HTTPException(status_code=400, detail="Attendance ID already exists")
    if not db.query(StudentDB).filter(StudentDB.student_id == attendance.student_id).first():
        raise HTTPException(status_code=404, detail="Student not found")
    if not db.query(ClassDB).filter(ClassDB.class_id == attendance.class_id).first():
        raise HTTPException(status_code=404, detail="Class not found")
    db_attendance = AttendanceDB(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return attendance

@app.get("/attendance/", tags=["Attendance"], response_model=List[Attendance])
def get_all_attendance(username: str, db: Session = Depends(get_db)):
    """Retrieve all attendance records (requires login)"""
    if not find_user(db, username):
        raise HTTPException(status_code=401, detail="User not found")
    return db.query(AttendanceDB).all()

# Grade Management
@app.post("/grades/", tags=["Grades"], response_model=Grade)
def record_grade(grade: Grade, username: str, db: Session = Depends(get_db)):
    """Record a grade for a student in a class (requires teacher role)"""
    user = find_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if user.role not in [UserRole.admin, UserRole.teacher]:
        raise HTTPException(status_code=403, detail="Not authorized to record grades")
    if db.query(GradeDB).filter(GradeDB.grade_id == grade.grade_id).first():
        raise HTTPException(status_code=400, detail="Grade ID already exists")
    if not db.query(StudentDB).filter(StudentDB.student_id == grade.student_id).first():
        raise HTTPException(status_code=404, detail="Student not found")
    if not db.query(ClassDB).filter(ClassDB.class_id == grade.class_id).first():
        raise HTTPException(status_code=404, detail="Class not found")
    if not db.query(SubjectDB).filter(SubjectDB.subject_id == grade.subject_id).first():
        raise HTTPException(status_code=404, detail="Subject not found")
    db_grade = GradeDB(**grade.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return grade

@app.get("/grades/", tags=["Grades"], response_model=List[Grade])
def get_all_grades(username: str, db: Session = Depends(get_db)):
    """Retrieve all grades (requires login)"""
    if not find_user(db, username):
        raise HTTPException(status_code=401, detail="User not found")
    return db.query(GradeDB).all()

# Root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "Tuition Class Management System API is running"}

# At the bottom of index.py
if __name__ == "__main__":
    try:
        uvicorn.run("index:app", host="127.0.0.1", port=8001, log_level="debug")
    except Exception as e:
        logger.error(f"Uvicorn failed to start: {e}")
        raise