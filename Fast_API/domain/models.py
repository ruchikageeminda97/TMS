from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import date

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

class TeacherAssignment(BaseModel):
    assignment_id: str
    teacher_id: str
    class_id: str
    assignment_date: date

class Payment(BaseModel):
    payment_id: Optional[str] = None
    student_id: str
    class_id: str
    amount: float
    payment_date: date
    month: str
    year: str
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

# Stats Models
class EntityCounts(BaseModel):
    students: int
    teachers: int
    subjects: int
    classes: int
    teacher_assignments: int
    payments: int
    attendance: int
    grades: int

class TodayIncome(BaseModel):
    today_income: float
    date: str

class TodayClass(BaseModel):
    class_id: str
    class_name: str
    subject_id: str
    day: str
    start_time: Optional[str] = None  # Made optional to handle missing fields
    end_time: Optional[str] = None
    room_number: Optional[str] = None
    capacity: Optional[int] = None
    status: ClassStatus
    attendance: List[Attendance] = []
    teacher_assignment: Optional[TeacherAssignment] = None

class TodayClassesResponse(BaseModel):
    today_classes: List[TodayClass]
    date: str