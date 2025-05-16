from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
db = mongo_client["tcms"]

class TestStudent(BaseModel):
    student_id: str

@app.post("/test_student/")
async def test_student(student: TestStudent):
    try:
        await db.students.insert_one({"student_id": student.student_id, "test": "data"})
        logger.info(f"Test student inserted: {student.student_id}")
        return {"message": f"Inserted {student.student_id}"}
    except Exception as e:
        logger.error(f"Test insertion error: {str(e)}")
        raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)