from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, List

# Use relative imports when running from app directory
from core.database import sessions_collection, chat_messages_collection
from schemas.session import SessionCreate, SessionUpdate, SessionResponse
from api.endpoints.dependencies import get_current_active_user
from models.session import SessionModel
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter()

@router.get("/", response_model=List[SessionResponse])
async def get_sessions(current_user: dict = Depends(get_current_active_user)) -> Any:
    """
    Get all sessions for the current user
    """
    sessions = list(sessions_collection.find({"user_id": str(current_user["_id"])}).sort("updated_at", -1))

    # Convert ObjectId to string
    for session in sessions:
        session["id"] = str(session["_id"])

    return sessions

@router.post("/", response_model=SessionResponse)
async def create_session(
    session_data: SessionCreate, current_user: dict = Depends(get_current_active_user)
) -> Any:
    """
    Create a new session
    """
    session = SessionModel(
        user_id=str(current_user["_id"]),
        name=session_data.name,
    )

    # Insert session into database
    result = sessions_collection.insert_one(session.model_dump(by_alias=True))

    # Get the created session
    created_session = sessions_collection.find_one({"_id": result.inserted_id})

    # Convert ObjectId to string
    created_session["id"] = str(created_session["_id"])

    return created_session

@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str, current_user: dict = Depends(get_current_active_user)
) -> Any:
    """
    Get a specific session
    """
    try:
        session = sessions_collection.find_one({
            "_id": ObjectId(session_id),
            "user_id": str(current_user["_id"])
        })
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    # Convert ObjectId to string
    session["id"] = str(session["_id"])

    return session

@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: str,
    session_data: SessionUpdate,
    current_user: dict = Depends(get_current_active_user)
) -> Any:
    """
    Update a session
    """
    try:
        session = sessions_collection.find_one({
            "_id": ObjectId(session_id),
            "user_id": str(current_user["_id"])
        })
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    update_data = session_data.model_dump(exclude_unset=True)

    # Add updated_at timestamp
    update_data["updated_at"] = datetime.now(timezone.utc)

    # Update session in database
    if update_data:
        sessions_collection.update_one(
            {"_id": ObjectId(session_id)}, {"$set": update_data}
        )

    # Get updated session
    updated_session = sessions_collection.find_one({"_id": ObjectId(session_id)})

    # Convert ObjectId to string
    updated_session["id"] = str(updated_session["_id"])

    return updated_session

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: str, current_user: dict = Depends(get_current_active_user)
) -> None:
    """
    Delete a session
    """
    try:
        session = sessions_collection.find_one({
            "_id": ObjectId(session_id),
            "user_id": str(current_user["_id"])
        })
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    # Delete session from database
    sessions_collection.delete_one({"_id": ObjectId(session_id)})

    # Delete all chat messages for this session
    chat_messages_collection.delete_many({"session_id": session_id})
