# test_db.py (updated)
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, String, Date, Float, Integer, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database configuration
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "tcms"
DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Enums (unchanged, copied from your code)
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

# SQLAlchemy Base
Base = declarative_base()

# SQLAlchemy Models (unchanged, copied from your code)
class UserDB(Base):
    __tablename__ = "users"
    username = Column(String(50), primary_key=True)
    password = Column(String(100), nullable=False)
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

# Test database connection and table creation
try:
    logger.debug("Connecting to database")
    engine = create_engine(DATABASE_URL, echo=True)  # Enable SQLAlchemy logging
    logger.debug("Database connection successful")
    
    logger.debug("Attempting to create tables")
    Base.metadata.create_all(bind=engine, checkfirst=True)  # Check if tables exist
    logger.debug("Tables created successfully")
except SQLAlchemyError as e:
    logger.error(f"Database error: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
finally:
    logger.debug("Closing database connection")
    if 'engine' in locals():
        engine.dispose()