from domain.models import Teacher, UserRole
from infrastructure.database import db
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def add_teacher(teacher: Teacher, username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Teacher addition failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin]:
        logger.error(f"Teacher addition failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    if await db.teachers.find_one({"teacher_id": teacher.teacher_id}):
        logger.error(f"Teacher addition failed: Teacher ID {teacher.teacher_id} already exists")
        raise HTTPException(status_code=400, detail="Teacher ID already exists")
    if await db.teachers.find_one({"email": teacher.email}):
        logger.error(f"Teacher addition failed: Email {teacher.email} already exists")
        raise HTTPException(status_code=400, detail="Email already exists")
    teacher_doc = teacher.dict()
    teacher_doc["hire_date"] = teacher.hire_date.isoformat()
    try:
        await db.teachers.insert_one(teacher_doc)
    except Exception as e:
        logger.error(f"Failed to add teacher {teacher.teacher_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Teacher added: {teacher.teacher_id}")
    return teacher

async def get_teacher(teacher_id: str, username: str):
    if not teacher_id or not isinstance(teacher_id, str):
        logger.error(f"Invalid teacher_id: {teacher_id}")
        raise HTTPException(status_code=400, detail="Invalid teacher ID")
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Teacher retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    teacher = await db.teachers.find_one({"teacher_id": teacher_id})
    if not teacher:
        logger.error(f"Teacher retrieval failed: Teacher {teacher_id} not found")
        raise HTTPException(status_code=404, detail="Teacher not found")
    logger.info(f"Teacher retrieved: {teacher_id}")
    return teacher

async def update_teacher(teacher_id: str, teacher: Teacher, username: str):
    if not teacher_id or not isinstance(teacher_id, str):
        logger.error(f"Invalid teacher_id: {teacher_id}")
        raise HTTPException(status_code=400, detail="Invalid teacher ID")
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Teacher update failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin]:
        logger.error(f"Teacher update failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    existing_teacher = await db.teachers.find_one({"teacher_id": teacher_id})
    if not existing_teacher:
        logger.error(f"Teacher update failed: Teacher {teacher_id} not found")
        raise HTTPException(status_code=404, detail="Teacher not found")
    if teacher.email != existing_teacher["email"] and await db.teachers.find_one({"email": teacher.email, "teacher_id": {"$ne": teacher_id}}):
        logger.error(f"Teacher update failed: Email {teacher.email} already exists")
        raise HTTPException(status_code=400, detail="Email already exists")
    teacher_doc = teacher.dict()
    teacher_doc["hire_date"] = teacher.hire_date.isoformat()
    try:
        await db.teachers.update_one({"teacher_id": teacher_id}, {"$set": teacher_doc})
    except Exception as e:
        logger.error(f"Failed to update teacher {teacher_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Teacher updated: {teacher_id}")
    return teacher

async def delete_teacher(teacher_id: str, username: str):
    if not teacher_id or not isinstance(teacher_id, str):
        logger.error(f"Invalid teacher_id: {teacher_id}")
        raise HTTPException(status_code=400, detail="Invalid teacher ID")
    user = await db.users.find_one({"username": username})
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
    except Exception as e:
        logger.error(f"Failed to delete teacher {teacher_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Teacher deleted: {teacher_id}")
    return {"message": f"Teacher {teacher_id} deleted successfully"}

async def list_teachers(username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Teachers retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    try:
        teachers = await db.teachers.find().to_list(length=None)
    except Exception as e:
        logger.error(f"Failed to retrieve teachers: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info("Teachers retrieved")
    return [Teacher(**teacher) for teacher in teachers]