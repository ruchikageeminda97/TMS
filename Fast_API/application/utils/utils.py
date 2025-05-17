from datetime import date
from bson import ObjectId

def get_today() -> str:
    """Return today's date in YYYY-MM-DD format."""
    return date.today().isoformat()

def serialize_object_ids(data):
    """Convert ObjectId fields to strings in a data structure."""
    if isinstance(data, list):
        return [serialize_object_ids(item) for item in data]
    if isinstance(data, dict):
        return {k: serialize_object_ids(v) if k != "_id" else str(v) for k, v in data.items()}
    if isinstance(data, ObjectId):
        return str(data)
    return data