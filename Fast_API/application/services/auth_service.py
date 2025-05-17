from domain.models import User, LoginRequest, UserRole
from infrastructure.database import db
from passlib.context import CryptContext
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def register_user(user: User):
    if await db.users.find_one({"username": user.username}):
        logger.error(f"Registration failed: Username {user.username} already exists")
        raise HTTPException(status_code=400, detail="Username already exists")
        logger.error(f"Registration failed: Email {user.email} already exists")
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_password = pwd_context.hash(user.password)
    user_doc = {
        "username": user.username,
        "password": hashed_password,
        "role": user.role,
        "email": user.email
    }
    await db.users.insert_one(user_doc)
    logger.info(f"User registered successfully: {user.username}")
    return {"message": "Registration successful", "username": user.username}

async def login_user(request: LoginRequest):
    user = await db.users.find_one({"username": request.username})
    if not user or not pwd_context.verify(request.password, user["password"]):
        logger.error(f"Login failed: {request.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    logger.info(f"Login successful: {request.username}")
    return {"message": "Login successful"}
