from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Any, List, Optional
import datetime

# Use relative imports when running from app directory
from core.database import chat_messages_collection, sessions_collection, memories_collection
from schemas.chat import ChatMessageCreate, ChatMessageResponse, ChatHistoryResponse
from api.endpoints.dependencies import get_current_active_user
from models.chat import ChatMessageModel, MessageType
from core.config import settings
from bson import ObjectId

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

router = APIRouter()

def get_memory_from_mongo(user_id: str, memo_type: str) -> List[dict]:
    """
    Retrieve memories from MongoDB for a specific user and memory type
    """
    memories = list(memories_collection.find({
        "user_id": user_id,
        "memo_type": memo_type
    }).sort("created_at", -1))

    return memories

def format_core_memories(memories: List[dict]) -> str:
    """
    Format core memories into a string for the system prompt
    """
    if not memories:
        return ""

    formatted_memories = []
    for memory in memories:
        created_at = memory.get("created_at")
        if isinstance(created_at, datetime.datetime):
            created_at_str = created_at.isoformat()
        else:
            created_at_str = str(created_at)

        formatted_memories.append(f"- {memory.get('content', '')} (Recorded: {created_at_str})")

    return "Core Memories:\n" + "\n".join(formatted_memories)

def format_environment_memories(memories: List[dict]) -> str:
    """
    Format environment memories into a string for context
    """
    if not memories:
        return ""

    formatted_memories = []
    for memory in memories:
        created_at = memory.get("created_at")
        if isinstance(created_at, datetime.datetime):
            created_at_str = created_at.isoformat()
        else:
            created_at_str = str(created_at)

        formatted_memories.append(f"- {memory.get('content', '')} (Recorded: {created_at_str})")

    return "Environment/Event Memories:\n" + "\n".join(formatted_memories)

@router.get("/{session_id}/messages", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_id: str,
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0),
    current_user: dict = Depends(get_current_active_user)
) -> Any:
    """
    Get chat history for a specific session
    """
    # Check if session exists and belongs to the user
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

    # Get chat messages
    messages = list(
        chat_messages_collection.find({"session_id": session_id})
        .sort("timestamp", 1)
        .skip(skip)
        .limit(limit)
    )

    # Convert ObjectId to string
    for message in messages:
        message["id"] = str(message["_id"])

    return {"messages": messages, "session_id": session_id}

@router.post("/{session_id}/messages", response_model=ChatMessageResponse)
async def send_message(
    session_id: str,
    message_data: ChatMessageCreate,
    current_user: dict = Depends(get_current_active_user)
) -> Any:
    """
    Send a message in a chat session and get a response
    """
    # Check if session exists and belongs to the user
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

    # Create user message
    user_message = ChatMessageModel(
        session_id=session_id,
        user_id=str(current_user["_id"]),
        content=message_data.content,
        message_type=MessageType.USER,
    )

    # Insert user message into database
    user_message_result = chat_messages_collection.insert_one(user_message.model_dump(by_alias=True))

    # Update session's last_message_at
    now = datetime.datetime.now(datetime.timezone.utc)
    sessions_collection.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"last_message_at": now, "updated_at": now}}
    )

    # Get memories for context
    core_memories = get_memory_from_mongo(str(current_user["_id"]), "core_memory")
    environment_memories = get_memory_from_mongo(str(current_user["_id"]), "environment_memory")

    # Format memories
    core_memories_text = format_core_memories(core_memories)
    environment_memories_text = format_environment_memories(environment_memories)

    # Determine which model to use based on reasoning flag
    model_name = settings.REASONING_LLM_MODEL if message_data.reasoning else settings.NON_REASONING_LLM_MODEL

    # Initialize LLM
    try:
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.7,
            max_output_tokens=2048,
            top_k=40,
            top_p=0.95,
            google_api_key=settings.GEMINI_API_KEY or settings.GOOGLE_API_KEY
        )
    except Exception as e:
        # If there's an error initializing the LLM, return an error message
        bot_message = ChatMessageModel(
            session_id=session_id,
            user_id=str(current_user["_id"]),
            content=f"I'm sorry, I couldn't initialize the language model. Error: {str(e)}",
            message_type=MessageType.BOT,
            model_used="error",
            reasoning=message_data.reasoning,
        )

        # Insert bot message into database
        bot_message_result = chat_messages_collection.insert_one(bot_message.model_dump(by_alias=True))

        # Get the created bot message
        created_bot_message = chat_messages_collection.find_one({"_id": bot_message_result.inserted_id})

        # Convert ObjectId to string
        if created_bot_message:
            created_bot_message["id"] = str(created_bot_message["_id"])

        return created_bot_message

    # Create system prompt with core memories
    system_prompt = "You are a personalized AI assistant that remembers details about the user and provides helpful, accurate responses."
    if core_memories_text:
        system_prompt += f"\n\n{core_memories_text}"

    # Create human message with environment memories and user query
    human_message_content = message_data.content
    if environment_memories_text:
        human_message_content = f"{environment_memories_text}\n\nUser Query: {message_data.content}"

    # Create messages for LLM
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_message_content)
    ]

    # Generate response
    try:
        ai_response = llm.invoke(messages)
        bot_response_text = ai_response.content
    except Exception as e:
        bot_response_text = f"I'm sorry, I encountered an error while processing your request. Please try again later."

    # Create bot message
    bot_message = ChatMessageModel(
        session_id=session_id,
        user_id=str(current_user["_id"]),
        content=bot_response_text,
        message_type=MessageType.BOT,
        model_used=model_name,
        reasoning=message_data.reasoning,
    )

    # Insert bot message into database
    bot_message_result = chat_messages_collection.insert_one(bot_message.model_dump(by_alias=True))

    # Get the created bot message
    created_bot_message = chat_messages_collection.find_one({"_id": bot_message_result.inserted_id})

    # Convert ObjectId to string
    created_bot_message["id"] = str(created_bot_message["_id"])

    return created_bot_message
