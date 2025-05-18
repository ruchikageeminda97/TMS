from domain.models import Subject, UserRole
from infrastructure.database import db
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def add_subject(subject: Subject, username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Subject addition failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin]:
        logger.error(f"Subject addition failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    if await db.subjects.find_one({"subject_id": subject.subject_id}):
        logger.error(f"Subject addition failed: Subject ID {subject.subject_id} already exists")
        raise HTTPException(status_code=400, detail="Subject ID already exists")
    subject_doc = subject.dict()
    try:
        await db.subjects.insert_one(subject_doc)
    except Exception as e:
        logger.error(f"Failed to add subject {subject.subject_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Subject added: {subject.subject_id}")
    return subject

async def get_subject(subject_id: str, username: str):
    if not subject_id or not isinstance(subject_id, str):
        logger.error(f"Invalid subject_id: {subject_id}")
        raise HTTPException(status_code=400, detail="Invalid subject ID")
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Subject retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    subject = await db.subjects.find_one({"subject_id": subject_id})
    if not subject:
        logger.error(f"Subject retrieval failed: Subject {subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    logger.info(f"Subject retrieved: {subject_id}")
    return subject

async def update_subject(subject_id: str, subject: Subject, username: str):
    if not subject_id or not isinstance(subject_id, str):
        logger.error(f"Invalid subject_id: {subject_id}")
        raise HTTPException(status_code=400, detail="Invalid subject ID")
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Subject update failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin]:
        logger.error(f"Subject update failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    existing_subject = await db.subjects.find_one({"subject_id": subject_id})
    if not existing_subject:
        logger.error(f"Subject update failed: Subject {subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    subject_doc = subject.dict()
    try:
        await db.subjects.update_one({"subject_id": subject_id}, {"$set": subject_doc})
    except Exception as e:
        logger.error(f"Failed to update subject {subject_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Subject updated: {subject_id}")
    return subject

async def delete_subject(subject_id: str, username: str):
    if not subject_id or not isinstance(subject_id, str):
        logger.error(f"Invalid subject_id: {subject_id}")
        raise HTTPException(status_code=400, detail="Invalid subject ID")
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Subject deletion failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Subject deletion failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    existing_subject = await db.subjects.find_one({"subject_id": subject_id})
    if not existing_subject:
        logger.error(f"Subject deletion failed: Subject {subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    try:
        await db.subjects.delete_one({"subject_id": subject_id})
    except Exception as e:
        logger.error(f"Failed to delete subject {subject_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Subject deleted: {subject_id}")
    return {"message": f"Subject {subject_id} deleted successfully"}

async def list_subjects(username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Subjects retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    try:
        subjects = await db.subjects.find().to_list(length=None)
    except Exception as e:
        logger.error(f"Failed to retrieve subjects: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info("Subjects retrieved")
    return [Subject(**subject) for subject in subjects]