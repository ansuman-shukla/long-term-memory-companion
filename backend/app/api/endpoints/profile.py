from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any

# Use absolute imports when running as a module
from app.core.security import get_password_hash
from app.core.database import users_collection
from app.schemas.user import UserUpdate, UserResponse
from app.api.endpoints.dependencies import get_current_active_user
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: dict = Depends(get_current_active_user)) -> Any:
    """
    Get current user profile
    """
    # Convert ObjectId to string
    current_user["id"] = str(current_user["_id"])
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    user_data: UserUpdate, current_user: dict = Depends(get_current_active_user)
) -> Any:
    """
    Update current user profile
    """
    update_data = user_data.model_dump(exclude_unset=True)

    # If password is being updated, hash it
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    # Check if username is being updated and if it's already taken
    if "username" in update_data and update_data["username"] != current_user["username"]:
        if users_collection.find_one({"username": update_data["username"]}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

    # Check if email is being updated and if it's already taken
    if "email" in update_data and update_data["email"] != current_user["email"]:
        if users_collection.find_one({"email": update_data["email"]}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    # Add updated_at timestamp
    update_data["updated_at"] = datetime.now(timezone.utc)

    # Update user in database
    if update_data:
        users_collection.update_one(
            {"_id": current_user["_id"]}, {"$set": update_data}
        )

    # Get updated user
    updated_user = users_collection.find_one({"_id": current_user["_id"]})

    # Convert ObjectId to string
    updated_user["id"] = str(updated_user["_id"])

    return updated_user
