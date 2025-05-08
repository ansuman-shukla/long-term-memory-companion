from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

# Session creation schema
class SessionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

# Session update schema
class SessionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

# Session response schema
class SessionResponse(BaseModel):
    id: str
    user_id: str
    name: str
    created_at: datetime
    updated_at: datetime
    last_message_at: Optional[datetime] = None
