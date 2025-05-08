from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class MemoryType:
    CORE = "core_memory"
    ENVIRONMENT = "environment_memory"

# Memory creation schema
class MemoryCreate(BaseModel):
    content: str = Field(..., min_length=1)
    memo_type: str = Field(..., description="Type of memory: core_memory or environment_memory")

# Memory update schema
class MemoryUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1)
    memo_type: Optional[str] = None

# Memory response schema
class MemoryResponse(BaseModel):
    id: str
    user_id: str
    content: str
    created_at: datetime
    memo_type: str
