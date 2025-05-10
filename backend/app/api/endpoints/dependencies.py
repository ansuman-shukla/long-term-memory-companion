from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Optional
from bson import ObjectId

# Use absolute imports when running as a module
from app.core.config import settings
from app.core.database import users_collection
from app.schemas.token import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the current user from the JWT token

    Args:
        token: JWT token

    Returns:
        User document

    Raises:
        HTTPException: If the token is invalid or the user doesn't exist
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenPayload(sub=user_id)
    except JWTError:
        raise credentials_exception

    user = users_collection.find_one({"_id": ObjectId(token_data.sub)})
    if user is None:
        raise credentials_exception

    return user

async def get_current_active_user(current_user = Depends(get_current_user)):
    """
    Get the current active user

    Args:
        current_user: User document

    Returns:
        User document

    Raises:
        HTTPException: If the user is inactive
    """
    if not current_user.get("is_active", True):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
