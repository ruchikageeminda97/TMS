from domain.models import Grade, UserRole
from infrastructure.database import db
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def record_grade(grade: Grade, username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Grade recording failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Grade recording failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    if await db.grades.find_one({"grade_id": grade.grade_id}):
        logger.error(f"Grade recording failed: Grade ID {grade.grade_id} already exists")
        raise HTTPException(status_code=400, detail="Grade ID already exists")
    if not await db.students.find_one({"student_id": grade.student_id}):
        logger.error(f"Grade recording failed: Student {grade.student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    if not await db.classes.find_one({"class_id": grade.class_id}):
        logger.error(f"Grade recording failed: Class {grade.class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    if not await db.subjects.find_one({"subject_id": grade.subject_id}):
        logger.error(f"Grade recording failed: Subject {grade.subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    grade_doc = grade.dict()
    grade_doc["date"] = grade.date.isoformat()
    try:
        await db.grades.insert_one(grade_doc)
    except Exception as e:
        logger.error(f"Failed to record grade {grade.grade_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Grade recorded: {grade.grade_id}")
    return grade

async def get_all_grades(username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Grades retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    try:
        grades = await db.grades.find().to_list(length=None)
    except Exception as e:
        logger.error(f"Failed to retrieve grades: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info("Grades retrieved")
    return [Grade(**grade) for grade in grades]

async def update_grade(grade_id: str, grade: Grade, username: str):
    if not grade_id or not isinstance(grade_id, str):
        logger.error(f"Invalid grade_id: {grade_id}")
        raise HTTPException(status_code=400, detail="Invalid grade ID")
    user = await db.users.find_one({"username": username})
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
    if not await db.students.find_one({"student_id": grade.student_id}):
        logger.error(f"Grade update failed: Student {grade.student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    if not await db.classes.find_one({"class_id": grade.class_id}):
        logger.error(f"Grade update failed: Class {grade.class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    if not await db.subjects.find_one({"subject_id": grade.subject_id}):
        logger.error(f"Grade update failed: Subject {grade.subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    grade_doc = grade.dict()
    grade_doc["date"] = grade.date.isoformat()
    try:
        await db.grades.update_one({"grade_id": grade_id}, {"$set": grade_doc})
    except Exception as e:
        logger.error(f"Failed to update grade {grade_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Grade updated: {grade_id}")
    return grade

async def delete_grade(grade_id: str, username: str):
    if not grade_id or not isinstance(grade_id, str):
        logger.error(f"Invalid grade_id: {grade_id}")
        raise HTTPException(status_code=400, detail="Invalid grade ID")
    user = await db.users.find_one({"username": username})
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
    except Exception as e:
        logger.error(f"Failed to delete grade {grade_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Grade deleted: {grade_id}")
    return {"message": f"Grade {grade_id} deleted successfully"}