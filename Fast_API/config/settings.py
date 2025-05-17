import logging

# MongoDB configuration
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DATABASE = "tcms"

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
