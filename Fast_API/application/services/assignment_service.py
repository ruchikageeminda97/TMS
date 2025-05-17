from domain.models import TeacherAssignment, UserRole
from infrastructure.database import db
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def assign_teacher_to_class(assignment: TeacherAssignment, username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Teacher assignment failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin]:
        logger.error(f"Teacher assignment failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    if await db.teacher_assignments.find_one({"assignment_id": assignment.assignment_id}):
        logger.error(f"Teacher assignment failed: Assignment ID {assignment.assignment_id} already exists")
        raise HTTPException(status_code=400, detail="Assignment ID already exists")
    if not await db.teachers.find_one({"teacher_id": assignment.teacher_id}):
        logger.error(f"Teacher assignment failed: Teacher {assignment.teacher_id} not found")
        raise HTTPException(status_code=404, detail="Teacher not found")
    if not await db.classes.find_one({"class_id": assignment.class_id}):
        logger.error(f"Teacher assignment failed: Class {assignment.class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    assignment_doc = assignment.dict()
    assignment_doc["assignment_date"] = assignment.assignment_date.isoformat()
    try:
        await db.teacher_assignments.insert_one(assignment_doc)
    except Exception as e:
        logger.error(f"Failed to assign teacher for assignment {assignment.assignment_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Teacher assignment created: {assignment.assignment_id}")
    return assignment

async def list_teacher_assignments(username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Teacher assignments retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    try:
        assignments = await db.teacher_assignments.find().to_list(length=None)
    except Exception as e:
        logger.error(f"Failed to retrieve teacher assignments: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info("Teacher assignments retrieved")
    return [TeacherAssignment(**assignment) for assignment in assignments]

async def update_teacher_assignment(assignment_id: str, assignment: TeacherAssignment, username: str):
    if not assignment_id or not isinstance(assignment_id, str):
        logger.error(f"Invalid assignment_id: {assignment_id}")
        raise HTTPException(status_code=400, detail="Invalid assignment ID")
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Teacher assignment update failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin]:
        logger.error(f"Teacher assignment update failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    existing_assignment = await db.teacher_assignments.find_one({"assignment_id": assignment_id})
    if not existing_assignment:
        logger.error(f"Teacher assignment update failed: Assignment {assignment_id} not found")
        raise HTTPException(status_code=404, detail="Assignment not found")
    if not await db.teachers.find_one({"teacher_id": assignment.teacher_id}):
        logger.error(f"Teacher assignment update failed: Teacher {assignment.teacher_id} not found")
        raise HTTPException(status_code=404, detail="Teacher not found")
    if not await db.classes.find_one({"class_id": assignment.class_id}):
        logger.error(f"Teacher assignment update failed: Class {assignment.class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    assignment_doc = assignment.dict()
    assignment_doc["assignment_date"] = assignment.assignment_date.isoformat()
    try:
        await db.teacher_assignments.update_one({"assignment_id": assignment_id}, {"$set": assignment_doc})
    except Exception as e:
        logger.error(f"Failed to update teacher assignment {assignment_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Teacher assignment updated: {assignment_id}")
    return assignment

async def delete_teacher_assignment(assignment_id: str, username: str):
    if not assignment_id or not isinstance(assignment_id, str):
        logger.error(f"Invalid assignment_id: {assignment_id}")
        raise HTTPException(status_code=400, detail="Invalid assignment ID")
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Teacher assignment deletion failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin]:
        logger.error(f"Teacher assignment deletion failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    existing_assignment = await db.teacher_assignments.find_one({"assignment_id": assignment_id})
    if not existing_assignment:
        logger.error(f"Teacher assignment deletion failed: Assignment {assignment_id} not found")
        raise HTTPException(status_code=404, detail="Assignment not found")
    try:
        await db.teacher_assignments.delete_one({"assignment_id": assignment_id})
    except Exception as e:
        logger.error(f"Failed to delete teacher assignment {assignment_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Teacher assignment deleted: {assignment_id}")
    return {"message": f"Teacher assignment {assignment_id} deleted successfully"}