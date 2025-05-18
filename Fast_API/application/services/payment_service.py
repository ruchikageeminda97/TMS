from domain.models import Payment, UserRole, PaymentStatus
from infrastructure.database import db
from fastapi import HTTPException
import logging
import re

logger = logging.getLogger(__name__)

async def generate_payment_id():
    """Generate a unique payment_id in the format PAYXXX."""
    try:
        max_attempts = 10
        for _ in range(max_attempts):
            # Find the latest payment with a valid PAYXXX format
            latest_payment = await db.payments.find_one(
                {"payment_id": {"$regex": "^PAY\\d+$", "$exists": True, "$ne": None}},
                sort=[("payment_id", -1)]
            )
            
            if not latest_payment or not latest_payment.get("payment_id"):
                new_payment_id = "PAY001"
            else:
                latest_id = latest_payment["payment_id"]
                match = re.match(r"PAY(\d+)", latest_id)
                if not match:
                    logger.error(f"Unexpected invalid payment_id format: {latest_id}")
                    new_payment_id = "PAY001"
                else:
                    numeric_part = int(match.group(1)) + 1
                    new_payment_id = f"PAY{numeric_part:03d}"
            
            # Check if the generated payment_id already exists
            if not await db.payments.find_one({"payment_id": new_payment_id}):
                logger.debug(f"Generated unique payment_id: {new_payment_id}")
                return new_payment_id
            logger.warning(f"Generated payment_id {new_payment_id} already exists, retrying...")
        
        logger.error("Failed to generate unique payment_id after multiple attempts")
        raise HTTPException(status_code=500, detail="Unable to generate unique payment ID")
    
    except Exception as e:
        logger.error(f"Failed to generate payment_id: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate payment ID: {str(e)}")

async def process_payment(payment: Payment, username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Payment processing failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Payment processing failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if not await db.students.find_one({"student_id": payment.student_id}):
        logger.error(f"Payment processing failed: Student {payment.student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    if not await db.classes.find_one({"class_id": payment.class_id}):
        logger.error(f"Payment processing failed: Class {payment.class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    
    payment_id = None
    try:
        payment_id = await generate_payment_id()
        payment_doc = payment.dict()
        payment_doc["payment_id"] = payment_id
        payment_doc["payment_date"] = payment.payment_date.isoformat()
        
        await db.payments.insert_one(payment_doc)
        payment.payment_id = payment_id
        logger.info(f"Payment processed: {payment_id}")
        return payment
    
    except Exception as e:
        logger.error(f"Failed to process payment {payment_id or 'unknown'}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def get_all_payments(username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Payments retrieval failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    try:
        payments = await db.payments.find().to_list(length=None)
    except Exception as e:
        logger.error(f"Failed to retrieve payments: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info("Payments retrieved")
    return [Payment(**payment) for payment in payments]

async def update_payment(payment_id: str, payment: Payment, username: str):
    if not payment_id or not isinstance(payment_id, str):
        logger.error(f"Invalid payment_id: {payment_id}")
        raise HTTPException(status_code=400, detail="Invalid payment ID")
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Payment update failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] not in [UserRole.admin, UserRole.teacher]:
        logger.error(f"Payment update failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    existing_payment = await db.payments.find_one({"payment_id": payment_id})
    if not existing_payment:
        logger.error(f"Payment update failed: Payment {payment_id} not found")
        raise HTTPException(status_code=404, detail="Payment not found")
    if not await db.students.find_one({"student_id": payment.student_id}):
        logger.error(f"Payment update failed: Student {payment.student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    if not await db.classes.find_one({"class_id": payment.class_id}):
        logger.error(f"Payment update failed: Class {payment.class_id} not found")
        raise HTTPException(status_code=404, detail="Class not found")
    payment_doc = payment.dict()
    payment_doc["payment_date"] = payment.payment_date.isoformat()
    try:
        await db.payments.update_one({"payment_id": payment_id}, {"$set": payment_doc})
    except Exception as e:
        logger.error(f"Failed to update payment {payment_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Payment updated: {payment_id}")
    return payment

async def delete_payment(payment_id: str, username: str):
    if not payment_id or not isinstance(payment_id, str):
        logger.error(f"Invalid payment_id: {payment_id}")
        raise HTTPException(status_code=400, detail="Invalid payment ID")
    user = await db.users.find_one({"username": username})
    if not user:
        logger.error(f"Payment deletion failed: User {username} not found")
        raise HTTPException(status_code=401, detail="User not found")
    if user["role"] != UserRole.admin:
        logger.error(f"Payment deletion failed: User {username} not authorized")
        raise HTTPException(status_code=403, detail="Not authorized")
    existing_payment = await db.payments.find_one({"payment_id": payment_id})
    if not existing_payment:
        logger.error(f"Payment deletion failed: Payment {payment_id} not found")
        raise HTTPException(status_code=404, detail="Payment not found")
    try:
        await db.payments.delete_one({"payment_id": payment_id})
    except Exception as e:
        logger.error(f"Failed to delete payment {payment_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info(f"Payment deleted: {payment_id}")
    return {"message": f"Payment {payment_id} deleted successfully"}

async def clean_payments():
    """Clean up invalid payment_id values in the payments collection."""
    payments = await db.payments.find().to_list(length=None)
    seen_ids = set()
    for i, payment in enumerate(payments, 1):
        payment_id = payment.get("payment_id")
        if not payment_id or not isinstance(payment_id, str) or not re.match(r"PAY\d+", payment_id) or payment_id in seen_ids:
            new_id = f"PAY{i:03d}"
            while await db.payments.find_one({"payment_id": new_id}) or new_id in seen_ids:
                i += 1
                new_id = f"PAY{i:03d}"
            await db.payments.update_one(
                {"_id": payment["_id"]},
                {"$set": {"payment_id": new_id}}
            )
            logger.info(f"Updated payment_id to {new_id} for document {payment['_id']}")
        seen_ids.add(payment_id or new_id)