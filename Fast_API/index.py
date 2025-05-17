from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import date, datetime
import logging
import uvicorn
import time
from bson import ObjectId

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
        {"name": "Stats", "description": "Statistical data and counts."},
    ]
)

# Add CORS middleware with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1", "http://localhost:3000", "http://127.0.0.1:3000", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS", "PUT", "DELETE"],
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
    day: str
    start_time: str
    end_time: str
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

# Helper function to get today's date
def get_today():
    return date.today().strftime("%Y-%m-%d")

# Helper function to convert ObjectId to string
def serialize_object_ids(doc):
    if isinstance(doc, dict):
        return {k: str(v) if k == "_id" or isinstance(v, ObjectId) else serialize_object_ids(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [serialize_object_ids(item) for item in doc]
    return doc

# Stats Endpoints
@app.get("/stats/counts", tags=["Stats"])
async def get_entity_counts(username: str):
    """Get counts of all entities (students, teachers, subjects, classes, etc.)"""
    user = await find_user(username)
    if not user:
        logger.error(f"Counts retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Counts retrieval failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")

    try:
        counts = {
            "students": await db.students.count_documents({}),
            "teachers": await db.teachers.count_documents({}),
            "subjects": await db.subjects.count_documents({}),
            "classes": await db.classes.count_documents({}),
            "enrollments": await db.enrollments.count_documents({}),
            "teacher_assignments": await db.teacher_assignments.count_documents({}),
            "payments": await db.payments.count_documents({}),
            "attendance": await db.attendance.count_documents({}),
            "grades": await db.grades.count_documents({})
        }
        logger.info("Entity counts retrieved")
        return counts
    except Exception as e:
        logger.error(f"Counts retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/stats/today-income", tags=["Stats"])
async def get_today_income(username: str):
    """Get total income from payments made today"""
    user = await find_user(username)
    if not user:
        logger.error(f"Today income retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Today income retrieval failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")

    today = get_today()
    try:
        payments = await db.payments.find({"payment_date": today, "status": PaymentStatus.paid}).to_list(length=None)
        total_income = sum(payment["amount"] for payment in payments)
        logger.info(f"Today\'s income retrieved: {total_income}")
        return {"today_income": total_income, "date": today}
    except Exception as e:
        logger.error(f"Today income retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/stats/today-classes", tags=["Stats"])
async def get_today_classes(day: str):
    """Get all classes scheduled for a specified day with their records"""
    try:
        classes = await db.classes.find({"day": day, "status": ClassStatus.ongoing}).to_list(length=None)
        for class_ in classes:
            # Fetch enrollments for each class
            class_["enrollments"] = await db.enrollments.find({"class_id": class_["class_id"]}).to_list(length=None)
            # Fetch attendance for each class (for today)
            class_["attendance"] = await db.attendance.find({"class_id": class_["class_id"], "date": get_today()}).to_list(length=None)
            # Fetch teacher assignment for each class
            class_["teacher_assignment"] = await db.teacher_assignments.find_one({"class_id": class_["class_id"]})
        # Serialize ObjectIds in the entire response
        serialized_classes = serialize_object_ids(classes)
        logger.info(f"Classes retrieved for day {day}: {len(classes)} classes")
        return {"today_classes": serialized_classes, "date": get_today()}
    except Exception as e:
        logger.error(f"Classes retrieval error for day {day}: {e}")
        raise HTTPException(status_code=500, detail="Server error")

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
    user = await find_user(username)
    if not user:
        logger.error(f"Student retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    student = await db.students.find_one({"student_id": student_id})
    if not student:
        logger.error(f"Student retrieval failed: Student {student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    
    logger.info(f"Student retrieved: {student_id}")
    return student

@app.put("/students/{student_id}", tags=["Students"], response_model=Student)
async def update_student(student_id: str, student: Student, username: str):
    """Update an existing student"""
    user = await find_user(username)
    if not user:
        logger.error(f"Student update failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Student update failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_student = await db.students.find_one({"student_id": student_id})
    if not existing_student:
        logger.error(f"Student update failed: Student {student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check for email conflict with other students
    if student.email != existing_student["email"] and await db.students.find_one({"email": student.email}):
        logger.error(f"Student update failed: Email {student.email} already exists")
        raise HTTPException(status_code=400, detail="Email already exists")
    
    student_doc = student.dict()
    # Convert dates to ISO strings
    student_doc["date_of_birth"] = student.date_of_birth.isoformat()
    student_doc["enrollment_date"] = student.enrollment_date.isoformat()
    
    try:
        await db.students.update_one({"student_id": student_id}, {"$set": student_doc})
        logger.info(f"Student updated: {student_id}")
        return student
    except Exception as e:
        logger.error(f"Student update error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.delete("/students/{student_id}", tags=["Students"])
async def delete_student(student_id: str, username: str):
    """Delete a student"""
    user = await find_user(username)
    if not user:
        logger.error(f"Student deletion failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Student deletion failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_student = await db.students.find_one({"student_id": student_id})
    if not existing_student:
        logger.error(f"Student deletion failed: Student {student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    
    try:
        await db.students.delete_one({"student_id": student_id})
        logger.info(f"Student deleted: {student_id}")
        return {"message": f"Student {student_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Student deletion error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/students/", tags=["Students"], response_model=List[Student])
async def list_students(username: str):
    """List all students"""
    user = await find_user(username)
    if not user:
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
    user = await find_user(username)
    if not user:
        logger.error(f"Teacher retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    teacher = await db.teachers.find_one({"teacher_id": teacher_id})
    if not teacher:
        logger.error(f"Teacher retrieval failed: Teacher {teacher_id} not found")
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    logger.info(f"Teacher retrieved: {teacher_id}")
    return teacher

@app.put("/teachers/{teacher_id}", tags=["Teachers"], response_model=Teacher)
async def update_teacher(teacher_id: str, teacher: Teacher, username: str):
    """Update an existing teacher"""
    user = await find_user(username)
    if not user:
        logger.error(f"Teacher update failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Teacher update failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_teacher = await db.teachers.find_one({"teacher_id": teacher_id})
    if not existing_teacher:
        logger.error(f"Teacher update failed: Teacher {teacher_id} not found")
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Check for email conflict with other teachers
    if teacher.email != existing_teacher["email"] and await db.teachers.find_one({"email": teacher.email}):
        logger.error(f"Teacher update failed: Email {teacher.email} already exists")
        raise HTTPException(status_code=400, detail="Email already exists")
    
    teacher_doc = teacher.dict()
    # Convert date to ISO string
    teacher_doc["hire_date"] = teacher.hire_date.isoformat()
    
    try:
        await db.teachers.update_one({"teacher_id": teacher_id}, {"$set": teacher_doc})
        logger.info(f"Teacher updated: {teacher_id}")
        return teacher
    except Exception as e:
        logger.error(f"Teacher update error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.delete("/teachers/{teacher_id}", tags=["Teachers"])
async def delete_teacher(teacher_id: str, username: str):
    """Delete a teacher"""
    user = await find_user(username)
    if not user:
        logger.error(f"Teacher deletion failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Teacher deletion failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_teacher = await db.teachers.find_one({"teacher_id": teacher_id})
    if not existing_teacher:
        logger.error(f"Teacher deletion failed: Teacher {teacher_id} not found")
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    try:
        await db.teachers.delete_one({"teacher_id": teacher_id})
        logger.info(f"Teacher deleted: {teacher_id}")
        return {"message": f"Teacher {teacher_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Teacher deletion error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/teachers/", tags=["Teachers"], response_model=List[Teacher])
async def list_teachers(username: str):
    """List all teachers"""
    user = await find_user(username)
    if not user:
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
    user = await find_user(username)
    if not user:
        logger.error(f"Subject retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    subject = await db.subjects.find_one({"subject_id": subject_id})
    if not subject:
        logger.error(f"Subject retrieval failed: Subject {subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    
    logger.info(f"Subject retrieved: {subject_id}")
    return subject

@app.put("/subjects/{subject_id}", tags=["Subjects"], response_model=Subject)
async def update_subject(subject_id: str, subject: Subject, username: str):
    """Update an existing subject"""
    user = await find_user(username)
    if not user:
        logger.error(f"Subject update failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Subject update failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_subject = await db.subjects.find_one({"subject_id": subject_id})
    if not existing_subject:
        logger.error(f"Subject update failed: Subject {subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    
    subject_doc = subject.dict()
    try:
        await db.subjects.update_one({"subject_id": subject_id}, {"$set": subject_doc})
        logger.info(f"Subject updated: {subject_id}")
        return subject
    except Exception as e:
        logger.error(f"Subject update error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.delete("/subjects/{subject_id}", tags=["Subjects"])
async def delete_subject(subject_id: str, username: str):
    """Delete a subject"""
    user = await find_user(username)
    if not user:
        logger.error(f"Subject deletion failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Subject deletion failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_subject = await db.subjects.find_one({"subject_id": subject_id})
    if not existing_subject:
        logger.error(f"Subject deletion failed: Subject {subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    
    try:
        await db.subjects.delete_one({"subject_id": subject_id})
        logger.info(f"Subject deleted: {subject_id}")
        return {"message": f"Subject {subject_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Subject deletion error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/subjects/", tags=["Subjects"], response_model=List[Subject])
async def list_subjects(username: str):
    """List all subjects"""
    user = await find_user(username)
    if not user:
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
    user = await find_user(username)
    if not user:
        logger.error(f"Class retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    class_ = await db.classes.find_one({"class_id": class_id})
    if not class_:
        logger.error(f"Class retrieval failed: Class {class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    
    logger.info(f"Class retrieved: {class_id}")
    return class_

@app.put("/classes/{class_id}", tags=["Classes"], response_model=Class)
async def update_class(class_id: str, class_: Class, username: str):
    """Update an existing class"""
    user = await find_user(username)
    if not user:
        logger.error(f"Class update failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Class update failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_class = await db.classes.find_one({"class_id": class_id})
    if not existing_class:
        logger.error(f"Class update failed: Class {class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Check if subject_id exists
    if class_.subject_id != existing_class["subject_id"] and not await db.subjects.find_one({"subject_id": class_.subject_id}):
        logger.error(f"Class update failed: Subject {class_.subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    
    class_doc = class_.dict()
    
    try:
        await db.classes.update_one({"class_id": class_id}, {"$set": class_doc})
        logger.info(f"Class updated: {class_id}")
        return class_
    except Exception as e:
        logger.error(f"Class update error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.delete("/classes/{class_id}", tags=["Classes"])
async def delete_class(class_id: str, username: str):
    """Delete a class"""
    user = await find_user(username)
    if not user:
        logger.error(f"Class deletion failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Class deletion failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_class = await db.classes.find_one({"class_id": class_id})
    if not existing_class:
        logger.error(f"Class deletion failed: Class {class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    
    try:
        await db.classes.delete_one({"class_id": class_id})
        logger.info(f"Class deleted: {class_id}")
        return {"message": f"Class {class_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Class deletion error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/classes/", tags=["Classes"], response_model=List[Class])
async def list_classes(username: str):
    """List all classes"""
    user = await find_user(username)
    if not user:
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
    user = await find_user(username)
    if not user:
        logger.error(f"Enrollments retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    try:
        enrollments = await db.enrollments.find().to_list(length=None)
        logger.info("Enrollments retrieved")
        return enrollments
    except Exception as e:
        logger.error(f"Enrollments retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.put("/enrollments/{enrollment_id}", tags=["Enrollments"], response_model=Enrollment)
async def update_enrollment(enrollment_id: str, enrollment: Enrollment, username: str):
    """Update an existing enrollment"""
    user = await find_user(username)
    if not user:
        logger.error(f"Enrollment update failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Enrollment update failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_enrollment = await db.enrollments.find_one({"enrollment_id": enrollment_id})
    if not existing_enrollment:
        logger.error(f"Enrollment update failed: Enrollment {enrollment_id} not found")
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    # Check if student_id exists
    if enrollment.student_id != existing_enrollment["student_id"] and not await db.students.find_one({"student_id": enrollment.student_id}):
        logger.error(f"Enrollment update failed: Student {enrollment.student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if class_id exists and capacity
    class_ = await db.classes.find_one({"class_id": enrollment.class_id})
    if not class_:
        logger.error(f"Enrollment update failed: Class {enrollment.class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    enrolled_count = await db.enrollments.count_documents({"class_id": enrollment.class_id})
    if enrollment.class_id != existing_enrollment["class_id"] and enrolled_count >= class_["capacity"]:
        logger.error(f"Enrollment update failed: Class {enrollment.class_id} capacity reached")
        raise HTTPException(status_code=400, detail="Class capacity reached")
    
    enrollment_doc = enrollment.dict()
    # Convert date to ISO string
    enrollment_doc["enrollment_date"] = enrollment.enrollment_date.isoformat()
    
    try:
        await db.enrollments.update_one({"enrollment_id": enrollment_id}, {"$set": enrollment_doc})
        logger.info(f"Enrollment updated: {enrollment_id}")
        return enrollment
    except Exception as e:
        logger.error(f"Enrollment update error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.delete("/enrollments/{enrollment_id}", tags=["Enrollments"])
async def delete_enrollment(enrollment_id: str, username: str):
    """Delete an enrollment"""
    user = await find_user(username)
    if not user:
        logger.error(f"Enrollment deletion failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Enrollment deletion failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_enrollment = await db.enrollments.find_one({"enrollment_id": enrollment_id})
    if not existing_enrollment:
        logger.error(f"Enrollment deletion failed: Enrollment {enrollment_id} not found")
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    try:
        await db.enrollments.delete_one({"enrollment_id": enrollment_id})
        logger.info(f"Enrollment deleted: {enrollment_id}")
        return {"message": f"Enrollment {enrollment_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Enrollment deletion error: {e}")
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
    user = await find_user(username)
    if not user:
        logger.error(f"Teacher assignments retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    try:
        assignments = await db.teacher_assignments.find().to_list(length=None)
        logger.info("Teacher assignments retrieved")
        return assignments
    except Exception as e:
        logger.error(f"Teacher assignments retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.put("/teacher-assignments/{assignment_id}", tags=["TeacherAssignments"], response_model=TeacherAssignment)
async def update_teacher_assignment(assignment_id: str, assignment: TeacherAssignment, username: str):
    """Update an existing teacher assignment"""
    user = await find_user(username)
    if not user:
        logger.error(f"Teacher assignment update failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Teacher assignment update failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_assignment = await db.teacher_assignments.find_one({"assignment_id": assignment_id})
    if not existing_assignment:
        logger.error(f"Teacher assignment update failed: Assignment {assignment_id} not found")
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Check if teacher_id exists
    if assignment.teacher_id != existing_assignment["teacher_id"] and not await db.teachers.find_one({"teacher_id": assignment.teacher_id}):
        logger.error(f"Teacher assignment update failed: Teacher {assignment.teacher_id} not found")
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Check if class_id exists
    if assignment.class_id != existing_assignment["class_id"] and not await db.classes.find_one({"class_id": assignment.class_id}):
        logger.error(f"Teacher assignment update failed: Class {assignment.class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    
    assignment_doc = assignment.dict()
    # Convert date to ISO string
    assignment_doc["assignment_date"] = assignment.assignment_date.isoformat()
    
    try:
        await db.teacher_assignments.update_one({"assignment_id": assignment_id}, {"$set": assignment_doc})
        logger.info(f"Teacher assignment updated: {assignment_id}")
        return assignment
    except Exception as e:
        logger.error(f"Teacher assignment update error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.delete("/teacher-assignments/{assignment_id}", tags=["TeacherAssignments"])
async def delete_teacher_assignment(assignment_id: str, username: str):
    """Delete a teacher assignment"""
    user = await find_user(username)
    if not user:
        logger.error(f"Teacher assignment deletion failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Teacher assignment deletion failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_assignment = await db.teacher_assignments.find_one({"assignment_id": assignment_id})
    if not existing_assignment:
        logger.error(f"Teacher assignment deletion failed: Assignment {assignment_id} not found")
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    try:
        await db.teacher_assignments.delete_one({"assignment_id": assignment_id})
        logger.info(f"Teacher assignment deleted: {assignment_id}")
        return {"message": f"Teacher assignment {assignment_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Teacher assignment deletion error: {e}")
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
    user = await find_user(username)
    if not user:
        logger.error(f"Payments retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    try:
        payments = await db.payments.find().to_list(length=None)
        logger.info("Payments retrieved")
        return payments
    except Exception as e:
        logger.error(f"Payments retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.put("/payments/{payment_id}", tags=["Payments"], response_model=Payment)
async def update_payment(payment_id: str, payment: Payment, username: str):
    """Update an existing payment"""
    user = await find_user(username)
    if not user:
        logger.error(f"Payment update failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Payment update failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_payment = await db.payments.find_one({"payment_id": payment_id})
    if not existing_payment:
        logger.error(f"Payment update failed: Payment {payment_id} not found")
        raise HTTPException(status_code=404, detail="Payment not found")
    
    # Check if enrollment_id exists
    if payment.enrollment_id != existing_payment["enrollment_id"] and not await db.enrollments.find_one({"enrollment_id": payment.enrollment_id}):
        logger.error(f"Payment update failed: Enrollment {payment.enrollment_id} not found")
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    payment_doc = payment.dict()
    # Convert date to ISO string
    payment_doc["payment_date"] = payment.payment_date.isoformat()
    
    try:
        await db.payments.update_one({"payment_id": payment_id}, {"$set": payment_doc})
        # Update enrollment payment status if changed
        if payment.status == PaymentStatus.paid and existing_payment["status"] != PaymentStatus.paid:
            await db.enrollments.update_one(
                {"enrollment_id": payment.enrollment_id},
                {"$set": {"payment_status": PaymentStatus.paid}}
            )
        logger.info(f"Payment updated: {payment_id}")
        return payment
    except Exception as e:
        logger.error(f"Payment update error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.delete("/payments/{payment_id}", tags=["Payments"])
async def delete_payment(payment_id: str, username: str):
    """Delete a payment"""
    user = await find_user(username)
    if not user:
        logger.error(f"Payment deletion failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Payment deletion failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_payment = await db.payments.find_one({"payment_id": payment_id})
    if not existing_payment:
        logger.error(f"Payment deletion failed: Payment {payment_id} not found")
        raise HTTPException(status_code=404, detail="Payment not found")
    
    try:
        await db.payments.delete_one({"payment_id": payment_id})
        logger.info(f"Payment deleted: {payment_id}")
        return {"message": f"Payment {payment_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Payment deletion error: {e}")
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
    user = await find_user(username)
    if not user:
        logger.error(f"Attendance retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    try:
        attendance = await db.attendance.find().to_list(length=None)
        logger.info("Attendance retrieved")
        return attendance
    except Exception as e:
        logger.error(f"Attendance retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.put("/attendance/{attendance_id}", tags=["Attendance"], response_model=Attendance)
async def update_attendance(attendance_id: str, attendance: Attendance, username: str):
    """Update an existing attendance record"""
    user = await find_user(username)
    if not user:
        logger.error(f"Attendance update failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Attendance update failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_attendance = await db.attendance.find_one({"attendance_id": attendance_id})
    if not existing_attendance:
        logger.error(f"Attendance update failed: Attendance {attendance_id} not found")
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    # Check if student_id exists
    if attendance.student_id != existing_attendance["student_id"] and not await db.students.find_one({"student_id": attendance.student_id}):
        logger.error(f"Attendance update failed: Student {attendance.student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if class_id exists
    if attendance.class_id != existing_attendance["class_id"] and not await db.classes.find_one({"class_id": attendance.class_id}):
        logger.error(f"Attendance update failed: Class {attendance.class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    
    attendance_doc = attendance.dict()
    # Convert date to ISO string
    attendance_doc["date"] = attendance.date.isoformat()
    
    try:
        await db.attendance.update_one({"attendance_id": attendance_id}, {"$set": attendance_doc})
        logger.info(f"Attendance updated: {attendance_id}")
        return attendance
    except Exception as e:
        logger.error(f"Attendance update error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.delete("/attendance/{attendance_id}", tags=["Attendance"])
async def delete_attendance(attendance_id: str, username: str):
    """Delete an attendance record"""
    user = await find_user(username)
    if not user:
        logger.error(f"Attendance deletion failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Attendance deletion failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_attendance = await db.attendance.find_one({"attendance_id": attendance_id})
    if not existing_attendance:
        logger.error(f"Attendance deletion failed: Attendance {attendance_id} not found")
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    try:
        await db.attendance.delete_one({"attendance_id": attendance_id})
        logger.info(f"Attendance deleted: {attendance_id}")
        return {"message": f"Attendance {attendance_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Attendance deletion error: {e}")
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
    user = await find_user(username)
    if not user:
        logger.error(f"Grades retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    
    try:
        grades = await db.grades.find().to_list(length=None)
        logger.info("Grades retrieved")
        return grades
    except Exception as e:
        logger.error(f"Grades retrieval error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.put("/grades/{grade_id}", tags=["Grades"], response_model=Grade)
async def update_grade(grade_id: str, grade: Grade, username: str):
    """Update an existing grade"""
    user = await find_user(username)
    if not user:
        logger.error(f"Grade update failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Grade update failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_grade = await db.grades.find_one({"grade_id": grade_id})
    if not existing_grade:
        logger.error(f"Grade update failed: Grade {grade_id} not found")
        raise HTTPException(status_code=404, detail="Grade not found")
    
    # Check if student_id exists
    if grade.student_id != existing_grade["student_id"] and not await db.students.find_one({"student_id": grade.student_id}):
        logger.error(f"Grade update failed: Student {grade.student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if class_id exists
    if grade.class_id != existing_grade["class_id"] and not await db.classes.find_one({"class_id": grade.class_id}):
        logger.error(f"Grade update failed: Class {grade.class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Check if subject_id exists
    if grade.subject_id != existing_grade["subject_id"] and not await db.subjects.find_one({"subject_id": grade.subject_id}):
        logger.error(f"Grade update failed: Subject {grade.subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    
    grade_doc = grade.dict()
    # Convert date to ISO string
    grade_doc["date"] = grade.date.isoformat()
    
    try:
        await db.grades.update_one({"grade_id": grade_id}, {"$set": grade_doc})
        logger.info(f"Grade updated: {grade_id}")
        return grade
    except Exception as e:
        logger.error(f"Grade update error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@app.delete("/grades/{grade_id}", tags=["Grades"])
async def delete_grade(grade_id: str, username: str):
    """Delete a grade"""
    user = await find_user(username)
    if not user:
        logger.error(f"Grade deletion failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Grade deletion failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    existing_grade = await db.grades.find_one({"grade_id": grade_id})
    if not existing_grade:
        logger.error(f"Grade deletion failed: Grade {grade_id} not found")
        raise HTTPException(status_code=404, detail="Grade not found")
    
    try:
        await db.grades.delete_one({"grade_id": grade_id})
        logger.info(f"Grade deleted: {grade_id}")
        return {"message": f"Grade {grade_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Grade deletion error: {e}")
        raise HTTPException(status_code=500, detail="Server error")

if __name__ == "__main__":
    try:
        uvicorn.run("index:app", host="127.0.0.1", port=8001, log_level="debug", workers=1)
    except Exception as e:
        logger.error(f"Uvicorn failed to start: {e}")
        raise