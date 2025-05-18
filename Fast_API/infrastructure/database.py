from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import MONGO_HOST, MONGO_PORT, MONGO_DATABASE
import logging

logger = logging.getLogger(__name__)

client = AsyncIOMotorClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}")
db = client[MONGO_DATABASE]

async def init_db():
    try:
        await client.server_info()
        logger.info("Connected to MongoDB")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise
