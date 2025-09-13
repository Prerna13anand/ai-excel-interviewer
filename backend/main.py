import os
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <-- IMPORT THIS
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# Initialize the FastAPI app
app = FastAPI()

# --- ADD THIS MIDDLEWARE CONFIGURATION ---
origins = [
    "http://localhost:3000", # The origin of your React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)
# -----------------------------------------

# Configure the Gemini API client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the request body model using Pydantic
class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.get("/")
def read_root():
    return {"message": "AI Interviewer API is running with Gemini!"}

@app.post("/chat")
def chat(request: ChatRequest):
    # Set the model
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    # The conversation history from the frontend.
    chat_history = []
    for item in request.history:
        role = 'model' if item.get('role') == 'ai' else 'user'
        chat_history.append({'role': role, 'parts': [item.get('content')]})

    try:
        # Start a chat session with the existing history
        chat_session = model.start_chat(history=chat_history)
        
        # Send the new message
        response = chat_session.send_message(request.message)
        
        # Extract the AI's message
        ai_message = response.text
        return {"response": ai_message}

    except Exception as e:
        print(f"Error occurred: {e}")
        return {"error": str(e)}