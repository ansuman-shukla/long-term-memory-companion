from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId
from .user import PyObjectId, utc_now

class MessageType:
    USER = "user"
    BOT = "bot"

class ChatMessageModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    session_id: str = Field(...)
    user_id: str = Field(...)
    content: str = Field(...)
    message_type: str = Field(...)  # "user" or "bot"
    timestamp: datetime = Field(default_factory=utc_now)
    model_used: Optional[str] = None  # Which model was used for bot responses
    reasoning: Optional[bool] = False  # Whether reasoning was used
    metadata: Optional[Dict[str, Any]] = None  # Additional metadata

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
