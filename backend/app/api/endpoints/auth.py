from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any

# Use absolute imports when running as a module
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from app.core.database import users_collection
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.models.user import UserModel
from bson import ObjectId

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate) -> Any:
    """
    Register a new user
    """
    # Check if user with the same email exists
    if users_collection.find_one({"email": user_data.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    # Check if user with the same username exists
    if users_collection.find_one({"username": user_data.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )

    # Create new user
    user = UserModel(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
    )

    # Insert user into database
    result = users_collection.insert_one(user.model_dump(by_alias=True))

    # Get the created user
    created_user = users_collection.find_one({"_id": result.inserted_id})

    # Convert ObjectId to string
    created_user["id"] = str(created_user["_id"])

    return created_user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # Find user by username
    user = users_collection.find_one({"username": form_data.username})

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user["_id"]), expires_delta=access_token_expires
    )

    # Prepare user data for response
    user_data = {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "is_active": user.get("is_active", True),
        "created_at": user.get("created_at", datetime.now(timezone.utc))
    }

    # Return token and user data
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_data
    }
