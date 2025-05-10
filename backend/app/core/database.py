from pymongo import MongoClient
from pymongo.server_api import ServerApi
import logging
from .config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default MongoDB connection string for local development

try:
    # Get MongoDB connection details
    mongo_uri = settings.MONGO_DB_CONNECTION_STRING
    db_name = settings.DATABASE_NAME or "chatbot_db"

    logger.info(f"Connecting to MongoDB at {mongo_uri}")

    # Create a MongoDB client
    client = MongoClient(mongo_uri, server_api=ServerApi('1'))

    # Test the connection
    client.admin.command('ping')
    logger.info("MongoDB connection successful!")

    # Get the database
    db = client[db_name]

    # Define collections
    users_collection = db["users"]
    sessions_collection = db["sessions"]
    memories_collection = db["memories"]
    chat_messages_collection = db["chat_messages"]

    # Create indexes
    users_collection.create_index("email", unique=True)
    users_collection.create_index("username", unique=True)
    sessions_collection.create_index("user_id")
    memories_collection.create_index("user_id")
    memories_collection.create_index([("user_id", 1), ("memo_type", 1)])
    chat_messages_collection.create_index([("session_id", 1), ("timestamp", 1)])

except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    # Create dummy collections for development/testing
    client = None
    db = None

    class DummyCollection:
        def __init__(self, name):
            self.name = name
            logger.warning(f"Using dummy collection for {name}")

        def find_one(self, *args, **kwargs):
            logger.warning(f"Dummy find_one called on {self.name}")
            return None

        def find(self, *args, **kwargs):
            logger.warning(f"Dummy find called on {self.name}")
            return []

        def insert_one(self, *args, **kwargs):
            logger.warning(f"Dummy insert_one called on {self.name}")
            return None

        def update_one(self, *args, **kwargs):
            logger.warning(f"Dummy update_one called on {self.name}")
            return None

        def delete_one(self, *args, **kwargs):
            logger.warning(f"Dummy delete_one called on {self.name}")
            return None

        def delete_many(self, *args, **kwargs):
            logger.warning(f"Dummy delete_many called on {self.name}")
            return None

        def create_index(self, *args, **kwargs):
            logger.warning(f"Dummy create_index called on {self.name}")
            return None

    users_collection = DummyCollection("users")
    sessions_collection = DummyCollection("sessions")
    memories_collection = DummyCollection("memories")
    chat_messages_collection = DummyCollection("chat_messages")
