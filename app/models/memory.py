from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from .user import PyObjectId, utc_now

class MemoryModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(..., description="The ID of the user who created the memory")
    content: str = Field(..., description="The content of the memory")
    created_at: datetime = Field(default_factory=utc_now, description="The creation date of the memory")
    memo_type: str = Field(..., description="The type of the memory (core or environment)")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
