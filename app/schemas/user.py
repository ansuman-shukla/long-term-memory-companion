from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# User creation schema
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1)

# User update schema
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)

# User response schema
class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    full_name: str
    created_at: datetime
    is_active: bool

# User in DB schema
class UserInDB(UserResponse):
    hashed_password: str
