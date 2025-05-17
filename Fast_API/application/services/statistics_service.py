from domain.models import Attendance, TeacherAssignment, UserRole, PaymentStatus, ClassStatus, EntityCounts, TodayIncome, TodayClass, TodayClassesResponse
from infrastructure.database import db
from fastapi import HTTPException
import logging
from application.utils.utils import get_today, serialize_object_ids

logger = logging.getLogger(__name__)

async def get_entity_counts(username: str) -> EntityCounts:
    """Get counts of all entities (students, teachers, subjects, classes, etc.)"""
    user = await db.users.find_one({"username": username})
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
            "teacher_assignments": await db.teacher_assignments.count_documents({}),
            "payments": await db.payments.count_documents({}),
            "attendance": await db.attendance.count_documents({}),
            "grades": await db.grades.count_documents({})
        }
        logger.info("Entity counts retrieved")
        return EntityCounts(**counts)
    except Exception as e:
        logger.error(f"Counts retrieval error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

async def get_today_income(username: str) -> TodayIncome:
    """Get total income from payments made today"""
    user = await db.users.find_one({"username": username})
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
        logger.info(f"Today's income retrieved: {total_income}")
        return TodayIncome(today_income=total_income, date=today)
    except Exception as e:
        logger.error(f"Today income retrieval error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

async def get_today_classes(day: str) -> TodayClassesResponse:
    """Get all classes scheduled for a specified day with their records"""
    try:
        classes = await db.classes.find({"day": day, "status": ClassStatus.ongoing}).to_list(length=None)
        today_classes = []
        today_date = get_today()
        for class_ in classes:
            # Validate required fields
            required_fields = ["class_id", "class_name", "subject_id", "day", "status"]
            missing_fields = [field for field in required_fields if field not in class_ or class_[field] is None]
            if missing_fields:
                logger.warning(f"Skipping class document with missing fields: {missing_fields}, document: {class_}")
                continue
            
            # Fetch attendance for each class (for today)
            attendance = await db.attendance.find({"class_id": class_["class_id"], "date": today_date}).to_list(length=None)
            # Fetch teacher assignment for each class
            teacher_assignment = await db.teacher_assignments.find_one({"class_id": class_["class_id"]})
            # Create TodayClass instance with optional fields
            try:
                today_class = TodayClass(
                    class_id=class_["class_id"],
                    class_name=class_["class_name"],
                    subject_id=class_["subject_id"],
                    day=class_["day"],
                    start_time=class_.get("start_time"),
                    end_time=class_.get("end_time"),
                    room_number=class_.get("room_number"),
                    capacity=class_.get("capacity"),
                    status=ClassStatus(class_["status"]),
                    attendance=[Attendance(**att) for att in attendance],
                    teacher_assignment=TeacherAssignment(**teacher_assignment) if teacher_assignment else None
                )
                today_classes.append(today_class)
            except Exception as e:
                logger.error(f"Failed to create TodayClass for document {class_['_id']}: {str(e)}")
                continue
        
        # Serialize ObjectIds in the response
        serialized_classes = serialize_object_ids([class_.dict() for class_ in today_classes])
        logger.info(f"Classes retrieved for day {day}: {len(today_classes)} classes")
        return TodayClassesResponse(today_classes=serialized_classes, date=today_date)
    except Exception as e:
        logger.error(f"Classes retrieval error for day {day}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")