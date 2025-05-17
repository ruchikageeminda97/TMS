from domain.models import Class, UserRole, ClassStatus
from infrastructure.database import db
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def create_class(class_: Class, username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Class creation failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Class creation failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    if not await db.subjects.find_one({"subject_id": class_.subject_id}):
        logger.error(f"Class creation failed: Subject {class_.subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    try:
        class_doc = class_.dict()
        class_doc["status"] = class_.status.value
        await db.classes.insert_one(class_doc)
        logger.info(f"Class created: {class_.class_id}")
        return class_
    except Exception as e:
        logger.error(f"Failed to create class {class_.class_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def get_class(class_id: str, username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Class retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    class_ = await db.classes.find_one({"class_id": class_id})
    if not class_:
        logger.error(f"Class retrieval failed: Class {class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    logger.info(f"Class retrieved: {class_id}")
    return Class(**class_)

async def update_class(class_id: str, class_: Class, username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Class update failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Class update failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    existing_class = await db.classes.find_one({"class_id": class_id})
    if not existing_class:
        logger.error(f"Class update failed: Class {class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    if not await db.subjects.find_one({"subject_id": class_.subject_id}):
        logger.error(f"Class update failed: Subject {class_.subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    class_doc = class_.dict()
    class_doc["status"] = class_.status.value
    try:
        await db.classes.update_one({"class_id": class_id}, {"$set": class_doc})
        logger.info(f"Class updated: {class_id}")
        return class_
    except Exception as e:
        logger.error(f"Failed to update class {class_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def delete_class(class_id: str, username: str):
    user = await db.users.find_one({"username": username})
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
        logger.error(f"Failed to delete class {class_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def list_classes(username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Classes retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    try:
        classes = await db.classes.find().to_list(length=None)
        logger.info("Classes retrieved")
        return [Class(**class_) for class_ in classes]
    except Exception as e:
        logger.error(f"Failed to retrieve classes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def get_class_students_and_teacher(class_id: str, username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Class details retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    class_ = await db.classes.find_one({"class_id": class_id})
    if not class_:
        logger.error(f"Class details retrieval failed: Class {class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    teacher_assignment = await db.teacher_assignments.find_one({"class_id": class_id})
    students = await db.students.find({"class_id": class_id}).to_list(length=None)
    logger.info(f"Class details retrieved: {class_id}")
    return {
        "class": Class(**class_),
        "teacher_assignment": TeacherAssignment(**teacher_assignment) if teacher_assignment else None,
        "students": [Student(**student) for student in students]
    }

async def clean_classes():
    """Clean up invalid or incomplete class documents in the classes collection."""
    classes = await db.classes.find().to_list(length=None)
    for class_ in classes:
        class_id = class_.get("class_id")
        if not class_id:
            logger.warning(f"Skipping class document with missing class_id: {class_}")
            continue
        updates = {}
        if "class_name" not in class_ or class_["class_name"] is None:
            updates["class_name"] = f"Class {class_id}"
        if "subject_id" not in class_ or class_["subject_id"] is None:
            updates["subject_id"] = "SUB000"  # Default or placeholder subject_id
        if "day" not in class_ or class_["day"] is None:
            updates["day"] = "Unknown"
        if "start_time" not in class_ or class_["start_time"] is None:
            updates["start_time"] = "00:00"
        if "end_time" not in class_ or class_["end_time"] is None:
            updates["end_time"] = "00:00"
        if "capacity" not in class_ or class_["capacity"] is None:
            updates["capacity"] = 0
        if "status" not in class_ or class_["status"] is None:
            updates["status"] = ClassStatus.ongoing.value
        
        if updates:
            await db.classes.update_one(
                {"_id": class_["_id"]},
                {"$set": updates}
            )
            logger.info(f"Updated class {class_id} with fields: {updates}")