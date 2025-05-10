from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Use absolute imports when running as a module
from app.api.endpoints import auth, profile, session, memory, chat
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(profile.router, prefix="/api/profile", tags=["Profile"])
app.include_router(session.router, prefix="/api/sessions", tags=["Sessions"])
app.include_router(memory.router, prefix="/api/memory", tags=["Memory"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Personalized Chat Bot API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)