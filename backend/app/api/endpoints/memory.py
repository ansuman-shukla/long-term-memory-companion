from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Any, List

# Use absolute imports when running as a module
from app.core.database import memories_collection
from app.schemas.memory import MemoryCreate, MemoryUpdate, MemoryResponse, MemoryType
from app.api.endpoints.dependencies import get_current_active_user
from app.models.memory import MemoryModel
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[MemoryResponse])
async def get_memories(
    memo_type: str = Query(None, description="Filter by memory type (core_memory or environment_memory)"),
    current_user: dict = Depends(get_current_active_user)
) -> Any:
    """
    Get all memories for the current user, optionally filtered by type
    """
    query = {"user_id": str(current_user["_id"])}

    # Add memo_type filter if provided
    if memo_type:
        if memo_type not in [MemoryType.CORE, MemoryType.ENVIRONMENT]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid memory type. Must be one of: {MemoryType.CORE}, {MemoryType.ENVIRONMENT}",
            )
        query["memo_type"] = memo_type

    memories = list(memories_collection.find(query).sort("created_at", -1))

    # Convert ObjectId to string
    for memory in memories:
        memory["id"] = str(memory["_id"])

    return memories

@router.post("/", response_model=MemoryResponse)
async def create_memory(
    memory_data: MemoryCreate, current_user: dict = Depends(get_current_active_user)
) -> Any:
    """
    Create a new memory
    """
    # Validate memory type
    if memory_data.memo_type not in [MemoryType.CORE, MemoryType.ENVIRONMENT]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid memory type. Must be one of: {MemoryType.CORE}, {MemoryType.ENVIRONMENT}",
        )

    memory = MemoryModel(
        user_id=str(current_user["_id"]),
        content=memory_data.content,
        memo_type=memory_data.memo_type,
    )

    # Insert memory into database
    result = memories_collection.insert_one(memory.model_dump(by_alias=True))

    # Get the created memory
    created_memory = memories_collection.find_one({"_id": result.inserted_id})

    # Convert ObjectId to string
    created_memory["id"] = str(created_memory["_id"])

    return created_memory

@router.get("/{memory_id}", response_model=MemoryResponse)
async def get_memory(
    memory_id: str, current_user: dict = Depends(get_current_active_user)
) -> Any:
    """
    Get a specific memory
    """
    try:
        memory = memories_collection.find_one({
            "_id": ObjectId(memory_id),
            "user_id": str(current_user["_id"])
        })
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    # Convert ObjectId to string
    memory["id"] = str(memory["_id"])

    return memory

@router.put("/{memory_id}", response_model=MemoryResponse)
async def update_memory(
    memory_id: str,
    memory_data: MemoryUpdate,
    current_user: dict = Depends(get_current_active_user)
) -> Any:
    """
    Update a memory
    """
    try:
        memory = memories_collection.find_one({
            "_id": ObjectId(memory_id),
            "user_id": str(current_user["_id"])
        })
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    update_data = memory_data.model_dump(exclude_unset=True)

    # Validate memory type if provided
    if "memo_type" in update_data and update_data["memo_type"] not in [MemoryType.CORE, MemoryType.ENVIRONMENT]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid memory type. Must be one of: {MemoryType.CORE}, {MemoryType.ENVIRONMENT}",
        )

    # Update memory in database
    if update_data:
        memories_collection.update_one(
            {"_id": ObjectId(memory_id)}, {"$set": update_data}
        )

    # Get updated memory
    updated_memory = memories_collection.find_one({"_id": ObjectId(memory_id)})

    # Convert ObjectId to string
    updated_memory["id"] = str(updated_memory["_id"])

    return updated_memory

@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory(
    memory_id: str, current_user: dict = Depends(get_current_active_user)
) -> None:
    """
    Delete a memory
    """
    try:
        memory = memories_collection.find_one({
            "_id": ObjectId(memory_id),
            "user_id": str(current_user["_id"])
        })
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    # Delete memory from database
    memories_collection.delete_one({"_id": ObjectId(memory_id)})
