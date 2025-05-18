from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from domain.models import (
    User, LoginRequest, Student, Teacher, Subject, Class, TeacherAssignment, Payment, Attendance, Grade,
    EntityCounts, TodayIncome, TodayClassesResponse
)
from application.services import (
    auth_service, student_service, teacher_service, subject_service, class_service,
    assignment_service, payment_service, attendance_service, grade_service, statistics_service
)
from infrastructure.database import init_db
from fastapi.security import OAuth2PasswordBearer
import uvicorn

app = FastAPI(title="Tuition Class Management System")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],             
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

# Authentication Endpoints
@app.post("/register", status_code=201, tags=["Auth"])
async def register(user: User):
    return await auth_service.register_user(user)

@app.post("/login", tags=["Auth"])
async def login(request: LoginRequest):
    return await auth_service.login_user(request)

# Student Endpoints
@app.post("/students", status_code=201, tags=["Students"])
async def enroll_student(student: Student, username: str):
    return await student_service.enroll_student(student, username)

@app.get("/students/{student_id}", tags=["Students"])
async def get_student(student_id: str, username: str):
    return await student_service.get_student(student_id, username)

@app.put("/students/{student_id}", tags=["Students"])
async def update_student(student_id: str, student: Student, username: str):
    return await student_service.update_student(student_id, student, username)

@app.delete("/students/{student_id}", tags=["Students"])
async def delete_student(student_id: str, username: str):
    return await student_service.delete_student(student_id, username)

@app.get("/students", tags=["Students"])
async def list_students(username: str):
    return await student_service.list_students(username)

# Teacher Endpoints
@app.post("/teachers", status_code=201, tags=["Teachers"])
async def add_teacher(teacher: Teacher, username: str):
    return await teacher_service.add_teacher(teacher, username)

@app.get("/teachers/{teacher_id}", tags=["Teachers"])
async def get_teacher(teacher_id: str, username: str):
    return await teacher_service.get_teacher(teacher_id, username)

@app.put("/teachers/{teacher_id}", tags=["Teachers"])
async def update_teacher(teacher_id: str, teacher: Teacher, username: str):
    return await teacher_service.update_teacher(teacher_id, teacher, username)

@app.delete("/teachers/{teacher_id}", tags=["Teachers"])
async def delete_teacher(teacher_id: str, username: str):
    return await teacher_service.delete_teacher(teacher_id, username)

@app.get("/teachers", tags=["Teachers"])
async def list_teachers(username: str):
    return await teacher_service.list_teachers(username)

# Subject Endpoints
@app.post("/subjects", status_code=201, tags=["Subjects"])
async def add_subject(subject: Subject, username: str):
    return await subject_service.add_subject(subject, username)

@app.get("/subjects/{subject_id}", tags=["Subjects"])
async def get_subject(subject_id: str, username: str):
    return await subject_service.get_subject(subject_id, username)

@app.put("/subjects/{subject_id}", tags=["Subjects"])
async def update_subject(subject_id: str, subject: Subject, username: str):
    return await subject_service.update_subject(subject_id, subject, username)

@app.delete("/subjects/{subject_id}", tags=["Subjects"])
async def delete_subject(subject_id: str, username: str):
    return await subject_service.delete_subject(subject_id, username)

@app.get("/subjects", tags=["Subjects"])
async def list_subjects(username: str):
    return await subject_service.list_subjects(username)

# Class Endpoints
@app.post("/classes", status_code=201, tags=["Classes"])
async def create_class(class_: Class, username: str):
    return await class_service.create_class(class_, username)

@app.get("/classes/{class_id}", tags=["Classes"])
async def get_class(class_id: str, username: str):
    return await class_service.get_class(class_id, username)

@app.put("/classes/{class_id}", tags=["Classes"])
async def update_class(class_id: str, class_: Class, username: str):
    return await class_service.update_class(class_id, class_, username)

@app.delete("/classes/{class_id}", tags=["Classes"])
async def delete_class(class_id: str, username: str):
    return await class_service.delete_class(class_id, username)

@app.get("/classes", tags=["Classes"])
async def list_classes(username: str):
    return await class_service.list_classes(username)

@app.get("/classes/{class_id}/details", tags=["Classes"])
async def get_class_details(class_id: str, username: str):
    return await class_service.get_class_students_and_teacher(class_id, username)

# Teacher Assignment Endpoints
@app.post("/assignments", status_code=201, tags=["Assignments"])
async def assign_teacher_to_class(assignment: TeacherAssignment, username: str):
    return await assignment_service.assign_teacher_to_class(assignment, username)

@app.get("/assignments", tags=["Assignments"])
async def list_teacher_assignments(username: str):
    return await assignment_service.list_teacher_assignments(username)

@app.put("/assignments/{assignment_id}", tags=["Assignments"])
async def update_teacher_assignment(assignment_id: str, assignment: TeacherAssignment, username: str):
    return await assignment_service.update_teacher_assignment(assignment_id, assignment, username)

@app.delete("/assignments/{assignment_id}", tags=["Assignments"])
async def delete_teacher_assignment(assignment_id: str, username: str):
    return await assignment_service.delete_teacher_assignment(assignment_id, username)

# Payment Endpoints
@app.post("/payments", status_code=201, tags=["Payments"])
async def process_payment(payment: Payment, username: str):
    return await payment_service.process_payment(payment, username)

@app.get("/payments", tags=["Payments"])
async def get_all_payments(username: str):
    return await payment_service.get_all_payments(username)

@app.put("/payments/{payment_id}", tags=["Payments"])
async def update_payment(payment_id: str, payment: Payment, username: str):
    return await payment_service.update_payment(payment_id, payment, username)

@app.delete("/payments/{payment_id}", tags=["Payments"])
async def delete_payment(payment_id: str, username: str):
    return await payment_service.delete_payment(payment_id, username)

# Attendance Endpoints
@app.post("/attendance", status_code=201, tags=["Attendance"])
async def record_attendance(attendance: Attendance, username: str):
    return await attendance_service.record_attendance(attendance, username)

@app.get("/attendance", tags=["Attendance"])
async def get_all_attendance(username: str):
    return await attendance_service.get_all_attendance(username)

@app.put("/attendance/{attendance_id}", tags=["Attendance"])
async def update_attendance(attendance_id: str, attendance: Attendance, username: str):
    return await attendance_service.update_attendance(attendance_id, attendance, username)

@app.delete("/attendance/{attendance_id}", tags=["Attendance"])
async def delete_attendance(attendance_id: str, username: str):
    return await attendance_service.delete_attendance(attendance_id, username)

# Grade Endpoints
@app.post("/grades", status_code=201, tags=["Grades"])
async def record_grade(grade: Grade, username: str):
    return await grade_service.record_grade(grade, username)

@app.get("/grades", tags=["Grades"])
async def get_all_grades(username: str):
    return await grade_service.get_all_grades(username)

@app.put("/grades/{grade_id}", tags=["Grades"])
async def update_grade(grade_id: str, grade: Grade, username: str):
    return await grade_service.update_grade(grade_id, grade, username)

@app.delete("/grades/{grade_id}", tags=["Grades"])
async def delete_grade(grade_id: str, username: str):
    return await grade_service.delete_grade(grade_id, username)

# Stats Endpoints
@app.get("/stats/counts", tags=["Stats"], response_model=EntityCounts)
async def get_entity_counts(username: str):
    """Get counts of all entities (students, teachers, subjects, classes, etc.)"""
    return await statistics_service.get_entity_counts(username)

@app.get("/stats/today-income", tags=["Stats"], response_model=TodayIncome)
async def get_today_income(username: str):
    """Get total income from payments made today"""
    return await statistics_service.get_today_income(username)

@app.get("/stats/today-classes", tags=["Stats"], response_model=TodayClassesResponse)
async def get_today_classes(day: str):
    """Get all classes scheduled for a specified day with their records"""
    return await statistics_service.get_today_classes(day)

# Maintenance Endpoints
@app.get("/clean-payments", tags=["Maintenance"])
async def clean_payments_endpoint():
    await payment_service.clean_payments()
    return {"message": "Payments collection cleaned"}

@app.get("/clean-classes", tags=["Maintenance"])
async def clean_classes_endpoint():
    await class_service.clean_classes()
    return {"message": "Classes collection cleaned"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)