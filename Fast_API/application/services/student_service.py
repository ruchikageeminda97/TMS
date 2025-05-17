from domain.models import Student, UserRole
from infrastructure.database import db
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def enroll_student(student: Student, username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Student enrollment failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Student enrollment failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    if await db.students.find_one({"student_id": student.student_id}):
        logger.error(f"Student enrollment failed: Student ID {student.student_id} already exists")
        raise HTTPException(status_code=400, detail="Student ID already exists")
    if await db.students.find_one({"email": student.email}):
        logger.error(f"Student enrollment failed: Email {student.email} already exists")
        raise HTTPException(status_code=400, detail="Email already exists")
    student_doc = student.dict()
    student_doc["date_of_birth"] = student.date_of_birth.isoformat()
    student_doc["enrollment_date"] = student.enrollment_date.isoformat()
    try:
        await db.students.insert_one(student_doc)
    except Exception as e:
        logger.error(f"Failed to enroll student {student.student_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Student enrolled: {student.student_id}")
    return student

async def get_student(student_id: str, username: str):
    if not student_id or not isinstance(student_id, str):
        logger.error(f"Invalid student_id: {student_id}")
        raise HTTPException(status_code=400, detail="Invalid student ID")
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Student retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    student = await db.students.find_one({"student_id": student_id})
    if not student:
        logger.error(f"Student retrieval failed: Student {student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    logger.info(f"Student retrieved: {student_id}")
    return student

async def update_student(student_id: str, student: Student, username: str):
    if not student_id or not isinstance(student_id, str):
        logger.error(f"Invalid student_id: {student_id}")
        raise HTTPException(status_code=400, detail="Invalid student ID")
    user = await db.users.find_one({"username": username})
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
    if student.email != existing_student["email"] and await db.students.find_one({"email": student.email, "student_id": {"$ne": student_id}}):
        logger.error(f"Student update failed: Email {student.email} already exists")
        raise HTTPException(status_code=400, detail="Email already exists")
    student_doc = student.dict()
    student_doc["date_of_birth"] = student.date_of_birth.isoformat()
    student_doc["enrollment_date"] = student.enrollment_date.isoformat()
    try:
        await db.students.update_one({"student_id": student_id}, {"$set": student_doc})
    except Exception as e:
        logger.error(f"Failed to update student {student_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Student updated: {student_id}")
    return student

async def delete_student(student_id: str, username: str):
    if not student_id or not isinstance(student_id, str):
        logger.error(f"Invalid student_id: {student_id}")
        raise HTTPException(status_code=400, detail="Invalid student ID")
    user = await db.users.find_one({"username": username})
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
    except Exception as e:
        logger.error(f"Failed to delete student {student_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Student deleted: {student_id}")
    return {"message": f"Student {student_id} deleted successfully"}

async def list_students(username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Students retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    try:
        students = await db.students.find().to_list(length=None)
    except Exception as e:
        logger.error(f"Failed to retrieve students: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info("Students retrieved")
    return [Student(**student) for student in students]