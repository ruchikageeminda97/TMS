from domain.models import Attendance, UserRole
from infrastructure.database import db
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def record_attendance(attendance: Attendance, username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Attendance recording failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Attendance recording failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    if await db.attendance.find_one({"attendance_id": attendance.attendance_id}):
        logger.error(f"Attendance recording failed: Attendance ID {attendance.attendance_id} already exists")
        raise HTTPException(status_code=400, detail="Attendance ID already exists")
    if not await db.students.find_one({"student_id": attendance.student_id}):
        logger.error(f"Attendance recording failed: Student {attendance.student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    if not await db.classes.find_one({"class_id": attendance.class_id}):
        logger.error(f"Attendance recording failed: Class {attendance.class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    attendance_doc = attendance.dict()
    attendance_doc["date"] = attendance.date.isoformat()
    try:
        await db.attendance.insert_one(attendance_doc)
    except Exception as e:
        logger.error(f"Failed to record attendance {attendance.attendance_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Attendance recorded: {attendance.attendance_id}")
    return attendance

async def get_all_attendance(username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Attendance retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    try:
        attendance = await db.attendance.find().to_list(length=None)
    except Exception as e:
        logger.error(f"Failed to retrieve attendance: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info("Attendance retrieved")
    return [Attendance(**record) for record in attendance]

async def update_attendance(attendance_id: str, attendance: Attendance, username: str):
    if not attendance_id or not isinstance(attendance_id, str):
        logger.error(f"Invalid attendance_id: {attendance_id}")
        raise HTTPException(status_code=400, detail="Invalid attendance ID")
    user = await db.users.find_one({"username": username})
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
    if not await db.students.find_one({"student_id": attendance.student_id}):
        logger.error(f"Attendance update failed: Student {attendance.student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    if not await db.classes.find_one({"class_id": attendance.class_id}):
        logger.error(f"Attendance update failed: Class {attendance.class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    attendance_doc = attendance.dict()
    attendance_doc["date"] = attendance.date.isoformat()
    try:
        await db.attendance.update_one({"attendance_id": attendance_id}, {"$set": attendance_doc})
    except Exception as e:
        logger.error(f"Failed to update attendance {attendance_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Attendance updated: {attendance_id}")
    return attendance

async def delete_attendance(attendance_id: str, username: str):
    if not attendance_id or not isinstance(attendance_id, str):
        logger.error(f"Invalid attendance_id: {attendance_id}")
        raise HTTPException(status_code=400, detail="Invalid attendance ID")
    user = await db.users.find_one({"username": username})
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
    except Exception as e:
        logger.error(f"Failed to delete attendance {attendance_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Attendance deleted: {attendance_id}")
    return {"message": f"Attendance {attendance_id} deleted successfully"}