from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# Chat message creation schema
class ChatMessageCreate(BaseModel):
    content: str = Field(..., min_length=1)
    reasoning: Optional[bool] = False

# Chat message response schema
class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    user_id: str
    content: str
    message_type: str
    timestamp: datetime
    model_used: Optional[str] = None
    reasoning: Optional[bool] = False
    metadata: Optional[Dict[str, Any]] = None

# Chat history response schema
class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessageResponse]
    session_id: str
