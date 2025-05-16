from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import date
import logging
import uvicorn
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Tuition Class Management System (TCMS)",
    description="API for managing students, tutors, classes, subjects, enrollments, teacher assignments, payments, attendance, and grades in a tuition center.",
    version="1.0",
    openapi_tags=[
        {"name": "Auth", "description": "User authentication and registration."},
        {"name": "Students", "description": "Student management."},
        {"name": "Teachers", "description": "Teacher management."},
        {"name": "Subjects", "description": "Subject management."},
        {"name": "Classes", "description": "Class management."},
        {"name": "Enrollments", "description": "Enrollment management."},
        {"name": "TeacherAssignments", "description": "Teacher assignment management."},
        {"name": "Payments", "description": "Payment management."},
        {"name": "Attendance", "description": "Attendance management."},
        {"name": "Grades", "description": "Grade management."},
        {"name": "Health", "description": "Health check."},
    ]
)

# Add CORS middleware with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1", "http://localhost:3000", "http://127.0.0.1:3000", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)

# MongoDB configuration
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DATABASE = "tcms"

# Initialize MongoDB client
mongo_client = AsyncIOMotorClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}")
db = mongo_client[MONGO_DATABASE]

# Test connection on startup
@app.on_event("startup")
async def startup_event():
    try:
        await db.command("ping")
        logger.info("MongoDB connection successful")
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Enums for Status Fields
class UserRole(str, Enum):
    admin = "Admin"
    teacher = "Teacher"
    student = "Student"

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

# Pydantic Models
class User(BaseModel):
    username: str
    password: str
    role: UserRole
    email: str

class LoginRequest(BaseModel):
    username: str
    password: str

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
async def find_user(username: str) -> Optional[dict]:
    try:
        user = await db.users.find_one({"username": username})
        return user
    except Exception as e:
        logger.error(f"Error finding user {username}: {e}")
        raise HTTPException(status_code=500, detail="Database query error")

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Check server and database connectivity"""
    try:
        await db.command("ping")
        return {"status": "healthy", "timestamp": time.time()}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

# Root endpoint for testing
@app.get("/")
async def read_root():
    return {"message": "Tuition Class Management System API is running"}

# Authentication Endpoints
@app.post("/register/", tags=["Auth"])
async def register(user: User):
    """Register a new user"""
    logger.debug(f"Register attempt for username: {user.username}")
    
    # Check if username exists
    if await find_user(user.username):
        logger.error(f"Registration failed: Username {user.username} already exists")
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email exists
    if await db.users.find_one({"email": user.email}):
        logger.error(f"Registration failed: Email {user.email} already exists")
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Hash password
    try:
        hashed_password = pwd_context.hash(user.password)
    except Exception as e:
        logger.error(f"Password hashing error: {e}")
        raise HTTPException(status_code=500, detail="Password hashing error")
    
    # Create user document
    user_doc = {
        "username": user.username,
        "password": hashed_password,
        "role": user.role,
        "email": user.email
    }
    
    try:
        await db.users.insert_one(user_doc)
        logger.info(f"User registered successfully: {user.username}")
        return JSONResponse(
            status_code=201,
            content={"message": "Registration successful", "username": user.username}
        )
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/login/", tags=["Auth"])
async def login(request: LoginRequest):
    """Login a user"""
    logger.debug(f"Login attempt: {request.username}")
    user = await find_user(request.username)
    if not user or not pwd_context.verify(request.password, user["password"]):
        logger.error(f"Login failed: {request.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    logger.info(f"Login successful: {request.username}")
    return {"message": "Login successful"}

# Student Management
@app.post("/students/", tags=["Students"], response_model=Student)
async def enroll_student(student: Student, username: str):
    """Enroll a new student"""
    user = await find_user(username)
    if not user:
        logger.error(f"Student enrollment failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Student enrollment failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if student_id exists
    if await db.students.find_one({"student_id": student.student_id}):
        logger.error(f"Student enrollment failed: Student ID {student.student_id} already exists")
        raise HTTPException(status_code=400, detail="Student ID already exists")
    
    # Check if email exists
    if await db.students.find_one({"email": student.email}):
        logger.error(f"Student enrollment failed: Email {student.email} already exists")
        raise HTTPException(status_code=400, detail="Email already exists")
    
    student_doc = student.dict()
    # Convert dates to ISO strings
    student_doc["date_of_birth"] = student.date_of_birth.isoformat()
    student_doc["enrollment_date"] = student.enrollment_date.isoformat()
    
    try:
        await db.students.insert_one(student_doc)
        logger.info(f"Student enrolled: {student.student_id}")
        return student
    except Exception as e:
        logger.error(f"Student enrollment error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/students/{student_id}", tags=["Students"], response_model=Student)
async def get_student(student_id: str, username: str):
    """Get a student by ID"""
    if not await find_user(username):
        logger.error(f"Student retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    student = await db.students.find_one({"student_id": student_id})
    if not student:
        logger.error(f"Student retrieval failed: Student {student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    
    logger.info(f"Student retrieved: {student_id}")
    return student

@app.get("/students/", tags=["Students"], response_model=List[Student])
async def list_students(username: str):
    """List all students"""
    if not await find_user(username):
        logger.error(f"Students retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    try:
        students = await db.students.find().to_list(length=None)
        logger.info("Students retrieved")
        return students
    except Exception as e:
        logger.error(f"Students retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

# Teacher Management
@app.post("/teachers/", tags=["Teachers"], response_model=Teacher)
async def add_teacher(teacher: Teacher, username: str):
    """Add a new teacher"""
    user = await find_user(username)
    if not user:
        logger.error(f"Teacher addition failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Teacher addition failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if teacher_id exists
    if await db.teachers.find_one({"teacher_id": teacher.teacher_id}):
        logger.error(f"Teacher addition failed: Teacher ID {teacher.teacher_id} already exists")
        raise HTTPException(status_code=400, detail="Teacher ID already exists")
    
    # Check if email exists
    if await db.teachers.find_one({"email": teacher.email}):
        logger.error(f"Teacher addition failed: Email {teacher.email} already exists")
        raise HTTPException(status_code=400, detail="Email already exists")
    
    teacher_doc = teacher.dict()
    # Convert date to ISO string
    teacher_doc["hire_date"] = teacher.hire_date.isoformat()
    
    try:
        await db.teachers.insert_one(teacher_doc)
        logger.info(f"Teacher added: {teacher.teacher_id}")
        return teacher
    except Exception as e:
        logger.error(f"Teacher addition error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/teachers/{teacher_id}", tags=["Teachers"], response_model=Teacher)
async def get_teacher(teacher_id: str, username: str):
    """Get a teacher by ID"""
    if not await find_user(username):
        logger.error(f"Teacher retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    teacher = await db.teachers.find_one({"teacher_id": teacher_id})
    if not teacher:
        logger.error(f"Teacher retrieval failed: Teacher {teacher_id} not found")
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    logger.info(f"Teacher retrieved: {teacher_id}")
    return teacher

@app.get("/teachers/", tags=["Teachers"], response_model=List[Teacher])
async def list_teachers(username: str):
    """List all teachers"""
    if not await find_user(username):
        logger.error(f"Teachers retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    try:
        teachers = await db.teachers.find().to_list(length=None)
        logger.info("Teachers retrieved")
        return teachers
    except Exception as e:
        logger.error(f"Teachers retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

# Subject Management
@app.post("/subjects/", tags=["Subjects"], response_model=Subject)
async def add_subject(subject: Subject, username: str):
    """Add a new subject"""
    user = await find_user(username)
    if not user:
        logger.error(f"Subject addition failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Subject addition failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if subject_id exists
    if await db.subjects.find_one({"subject_id": subject.subject_id}):
        logger.error(f"Subject addition failed: Subject ID {subject.subject_id} already exists")
        raise HTTPException(status_code=400, detail="Subject ID already exists")
    
    subject_doc = subject.dict()
    try:
        await db.subjects.insert_one(subject_doc)
        logger.info(f"Subject added: {subject.subject_id}")
        return subject
    except Exception as e:
        logger.error(f"Subject addition error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/subjects/{subject_id}", tags=["Subjects"], response_model=Subject)
async def get_subject(subject_id: str, username: str):
    """Get a subject by ID"""
    if not await find_user(username):
        logger.error(f"Subject retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    subject = await db.subjects.find_one({"subject_id": subject_id})
    if not subject:
        logger.error(f"Subject retrieval failed: Subject {subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    
    logger.info(f"Subject retrieved: {subject_id}")
    return subject

@app.get("/subjects/", tags=["Subjects"], response_model=List[Subject])
async def list_subjects(username: str):
    """List all subjects"""
    if not await find_user(username):
        logger.error(f"Subjects retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    try:
        subjects = await db.subjects.find().to_list(length=None)
        logger.info("Subjects retrieved")
        return subjects
    except Exception as e:
        logger.error(f"Subjects retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

# Class Management
@app.post("/classes/", tags=["Classes"], response_model=Class)
async def create_class(class_: Class, username: str):
    """Create a new class"""
    user = await find_user(username)
    if not user:
        logger.error(f"Class creation failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Class creation failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if class_id exists
    if await db.classes.find_one({"class_id": class_.class_id}):
        logger.error(f"Class creation failed: Class ID {class_.class_id} already exists")
        raise HTTPException(status_code=400, detail="Class ID already exists")
    
    # Check if subject_id exists
    if not await db.subjects.find_one({"subject_id": class_.subject_id}):
        logger.error(f"Class creation failed: Subject {class_.subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    
    class_doc = class_.dict()
    # Convert dates to ISO strings
    class_doc["start_date"] = class_.start_date.isoformat()
    class_doc["end_date"] = class_.end_date.isoformat()
    
    try:
        await db.classes.insert_one(class_doc)
        logger.info(f"Class created: {class_.class_id}")
        return class_
    except Exception as e:
        logger.error(f"Class creation error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/classes/{class_id}", tags=["Classes"], response_model=Class)
async def get_class(class_id: str, username: str):
    """Get a class by ID"""
    if not await find_user(username):
        logger.error(f"Class retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    class_ = await db.classes.find_one({"class_id": class_id})
    if not class_:
        logger.error(f"Class retrieval failed: Class {class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    
    logger.info(f"Class retrieved: {class_id}")
    return class_

@app.get("/classes/", tags=["Classes"], response_model=List[Class])
async def list_classes(username: str):
    """List all classes"""
    if not await find_user(username):
        logger.error(f"Classes retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    try:
        classes = await db.classes.find().to_list(length=None)
        logger.info("Classes retrieved")
        return classes
    except Exception as e:
        logger.error(f"Classes retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

# Enrollment Management
@app.post("/enrollments/", tags=["Enrollments"], response_model=Enrollment)
async def enroll_student_in_class(enrollment: Enrollment, username: str):
    """Enroll a student in a class"""
    user = await find_user(username)
    if not user:
        logger.error(f"Enrollment failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Enrollment failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if enrollment_id exists
    if await db.enrollments.find_one({"enrollment_id": enrollment.enrollment_id}):
        logger.error(f"Enrollment failed: Enrollment ID {enrollment.enrollment_id} already exists")
        raise HTTPException(status_code=400, detail="Enrollment ID already exists")
    
    # Check if student_id exists
    if not await db.students.find_one({"student_id": enrollment.student_id}):
        logger.error(f"Enrollment failed: Student {enrollment.student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if class_id exists and capacity
    class_ = await db.classes.find_one({"class_id": enrollment.class_id})
    if not class_:
        logger.error(f"Enrollment failed: Class {enrollment.class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    
    enrolled_count = await db.enrollments.count_documents({"class_id": enrollment.class_id})
    if enrolled_count >= class_["capacity"]:
        logger.error(f"Enrollment failed: Class {enrollment.class_id} capacity reached")
        raise HTTPException(status_code=400, detail="Class capacity reached")
    
    enrollment_doc = enrollment.dict()
    # Convert date to ISO string
    enrollment_doc["enrollment_date"] = enrollment.enrollment_date.isoformat()
    
    try:
        await db.enrollments.insert_one(enrollment_doc)
        logger.info(f"Enrollment created: {enrollment.enrollment_id}")
        return enrollment
    except Exception as e:
        logger.error(f"Enrollment creation error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/enrollments/", tags=["Enrollments"], response_model=List[Enrollment])
async def list_enrollments(username: str):
    """List all enrollments"""
    if not await find_user(username):
        logger.error(f"Enrollments retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    try:
        enrollments = await db.enrollments.find().to_list(length=None)
        logger.info("Enrollments retrieved")
        return enrollments
    except Exception as e:
        logger.error(f"Enrollments retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

# Teacher Assignment Management
@app.post("/teacher-assignments/", tags=["TeacherAssignments"], response_model=TeacherAssignment)
async def assign_teacher_to_class(assignment: TeacherAssignment, username: str):
    """Assign a teacher to a class"""
    user = await find_user(username)
    if not user:
        logger.error(f"Teacher assignment failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Teacher assignment failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if assignment_id exists
    if await db.teacher_assignments.find_one({"assignment_id": assignment.assignment_id}):
        logger.error(f"Teacher assignment failed: Assignment ID {assignment.assignment_id} already exists")
        raise HTTPException(status_code=400, detail="Assignment ID already exists")
    
    # Check if teacher_id exists
    if not await db.teachers.find_one({"teacher_id": assignment.teacher_id}):
        logger.error(f"Teacher assignment failed: Teacher {assignment.teacher_id} not found")
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Check if class_id exists
    if not await db.classes.find_one({"class_id": assignment.class_id}):
        logger.error(f"Teacher assignment failed: Class {assignment.class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    
    assignment_doc = assignment.dict()
    # Convert date to ISO string
    assignment_doc["assignment_date"] = assignment.assignment_date.isoformat()
    
    try:
        await db.teacher_assignments.insert_one(assignment_doc)
        logger.info(f"Teacher assignment created: {assignment.assignment_id}")
        return assignment
    except Exception as e:
        logger.error(f"Teacher assignment creation error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/teacher-assignments/", tags=["TeacherAssignments"], response_model=List[TeacherAssignment])
async def list_teacher_assignments(username: str):
    """List all teacher assignments"""
    if not await find_user(username):
        logger.error(f"Teacher assignments retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    try:
        assignments = await db.teacher_assignments.find().to_list(length=None)
        logger.info("Teacher assignments retrieved")
        return assignments
    except Exception as e:
        logger.error(f"Teacher assignments retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

# Payment Management
@app.post("/payments/", tags=["Payments"], response_model=Payment)
async def process_payment(payment: Payment, username: str):
    """Process a payment"""
    user = await find_user(username)
    if not user:
        logger.error(f"Payment processing failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Payment processing failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if payment_id exists
    if await db.payments.find_one({"payment_id": payment.payment_id}):
        logger.error(f"Payment processing failed: Payment ID {payment.payment_id} already exists")
        raise HTTPException(status_code=400, detail="Payment ID already exists")
    
    # Check if enrollment_id exists
    enrollment = await db.enrollments.find_one({"enrollment_id": payment.enrollment_id})
    if not enrollment:
        logger.error(f"Payment processing failed: Enrollment {payment.enrollment_id} not found")
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    payment_doc = payment.dict()
    # Convert date to ISO string
    payment_doc["payment_date"] = payment.payment_date.isoformat()
    
    try:
        await db.payments.insert_one(payment_doc)
        # Update enrollment payment status
        await db.enrollments.update_one(
            {"enrollment_id": payment.enrollment_id},
            {"$set": {"payment_status": PaymentStatus.paid}}
        )
        logger.info(f"Payment processed: {payment.payment_id}")
        return payment
    except Exception as e:
        logger.error(f"Payment processing error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/payments/", tags=["Payments"], response_model=List[Payment])
async def get_all_payments(username: str):
    """Get all payments"""
    if not await find_user(username):
        logger.error(f"Payments retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    try:
        payments = await db.payments.find().to_list(length=None)
        logger.info("Payments retrieved")
        return payments
    except Exception as e:
        logger.error(f"Payments retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

# Attendance Management
@app.post("/attendance/", tags=["Attendance"], response_model=Attendance)
async def record_attendance(attendance: Attendance, username: str):
    """Record attendance"""
    user = await find_user(username)
    if not user:
        logger.error(f"Attendance recording failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Attendance recording failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if attendance_id exists
    if await db.attendance.find_one({"attendance_id": attendance.attendance_id}):
        logger.error(f"Attendance recording failed: Attendance ID {attendance.attendance_id} already exists")
        raise HTTPException(status_code=400, detail="Attendance ID already exists")
    
    # Check if student_id exists
    if not await db.students.find_one({"student_id": attendance.student_id}):
        logger.error(f"Attendance recording failed: Student {attendance.student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if class_id exists
    if not await db.classes.find_one({"class_id": attendance.class_id}):
        logger.error(f"Attendance recording failed: Class {attendance.class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    
    attendance_doc = attendance.dict()
    # Convert date to ISO string
    attendance_doc["date"] = attendance.date.isoformat()
    
    try:
        await db.attendance.insert_one(attendance_doc)
        logger.info(f"Attendance recorded: {attendance.attendance_id}")
        return attendance
    except Exception as e:
        logger.error(f"Attendance recording error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/attendance/", tags=["Attendance"], response_model=List[Attendance])
async def get_all_attendance(username: str):
    """Get all attendance records"""
    if not await find_user(username):
        logger.error(f"Attendance retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    try:
        attendance = await db.attendance.find().to_list(length=None)
        logger.info("Attendance retrieved")
        return attendance
    except Exception as e:
        logger.error(f"Attendance retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

# Grade Management
@app.post("/grades/", tags=["Grades"], response_model=Grade)
async def record_grade(grade: Grade, username: str):
    """Record a grade"""
    user = await find_user(username)
    if not user:
        logger.error(f"Grade recording failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Grade recording failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if grade_id exists
    if await db.grades.find_one({"grade_id": grade.grade_id}):
        logger.error(f"Grade recording failed: Grade ID {grade.grade_id} already exists")
        raise HTTPException(status_code=400, detail="Grade ID already exists")
    
    # Check if student_id exists
    if not await db.students.find_one({"student_id": grade.student_id}):
        logger.error(f"Grade recording failed: Student {grade.student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if class_id exists
    if not await db.classes.find_one({"class_id": grade.class_id}):
        logger.error(f"Grade recording failed: Class {grade.class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Check if subject_id exists
    if not await db.subjects.find_one({"subject_id": grade.subject_id}):
        logger.error(f"Grade recording failed: Subject {grade.subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    
    grade_doc = grade.dict()
    # Convert date to ISO string
    grade_doc["date"] = grade.date.isoformat()
    
    try:
        await db.grades.insert_one(grade_doc)
        logger.info(f"Grade recorded: {grade.grade_id}")
        return grade
    except Exception as e:
        logger.error(f"Grade recording error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/grades/", tags=["Grades"], response_model=List[Grade])
async def get_all_grades(username: str):
    """Get all grades"""
    if not await find_user(username):
        logger.error(f"Grades retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    try:
        grades = await db.grades.find().to_list(length=None)
        logger.info("Grades retrieved")
        return grades
    except Exception as e:
        logger.error(f"Grades retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

if __name__ == "__main__":
    try:
        uvicorn.run("index:app", host="127.0.0.1", port=8001, log_level="debug", workers=1)
    except Exception as e:
        logger.error(f"Uvicorn failed to start: {e}")
        raise