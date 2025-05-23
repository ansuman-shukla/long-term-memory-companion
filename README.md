# Personalized Chat Bot with Long-Term Memory

A full-stack application featuring a personalized chatbot with long-term memory capabilities, JWT authentication, and a pixel art-styled UI.

## Features

- **User Authentication**: Register, login, and profile management
- **Chat Sessions**: Create and manage multiple chat sessions
- **Memory Management**: Store and retrieve core and environment memories
- **AI Integration**: Uses Google's Gemini models for chat responses
- **Model Selection**: Choose between reasoning (Gemini 2.5 Pro) and faster (Gemini 2.0 Flash) models
- **Pixel Art UI**: Minimalist pixel art-styled interface

## Tech Stack

### Backend
- FastAPI
- MongoDB
- JWT Authentication
- LangChain
- Google Gemini AI

### Frontend
- React
- TypeScript
- Vite
- React Router
- Axios

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 14+
- MongoDB
- Google API Key (for Gemini)

### Environment Setup

1. Create a `.env` file in the root directory with the following variables:
```
GOOGLE_API_KEY=your_google_api_key
MONGO_DB_CONNECTION_STRING=your_mongodb_connection_string
```

### Backend Setup

1. Navigate to the backend directory:
```
cd backend
```

2. Create a virtual environment:
```
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Unix/MacOS: `source venv/bin/activate`

4. Install dependencies:
```
pip install -r requirements.txt
```

5. Start the backend server:
```
uvicorn app.main:app --reload
```

The backend will be available at http://localhost:8000.

### Frontend Setup

1. Navigate to the frontend directory:
```
cd frontend
```

2. Install dependencies:
```
npm install
```

3. Start the development server:
```
npm run dev
```

The frontend will be available at http://localhost:3000.

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   ├── core/
│   │   ├── models/
│   │   └── schemas/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── context/
│   │   ├── hooks/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
└── .env
```

## API Documentation

Once the backend is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
