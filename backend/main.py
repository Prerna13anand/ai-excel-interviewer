import os
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# Initialize the FastAPI app
app = FastAPI()

# --- MIDDLEWARE CONFIGURATION ---
origins = [
    "http://localhost:3000",
    "https://ai-excel-interviewer-brown.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------------------

# Configure the Gemini API client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- DEFINE THE AI'S PERSONA HERE ---
ATHENA_SYSTEM_PROMPT = """
You are Athena, a friendly AI assistant conducting a mock interview for Microsoft Excel skills. 
Your name is Athena. Do not mention that you are a language model.
Your goal is to create a welcoming environment and assess the user's skills.

Start the very first message of the conversation with this exact introduction:
"Hey there! 👋 I’m Athena, your AI assistant for this mock interview. I’m here to help you practice your Microsoft Excel skills by asking a few questions. Think of me as your friendly guide to prepare for your real interview.

Ready to start when you are!"
"""

# Define Pydantic models for request bodies
class ChatRequest(BaseModel):
    message: str
    history: list = []

class ReportRequest(BaseModel):
    history: list = []

@app.get("/")
def read_root():
    return {"message": "AI Interviewer API is running with Gemini!"}

@app.post("/chat")
def chat(request: ChatRequest):
    # Initialize the model with the Athena persona
    model = genai.GenerativeModel(
        'gemini-1.5-flash-latest',
        system_instruction=ATHENA_SYSTEM_PROMPT
    )
    
    chat_history = []
    for item in request.history:
        role = 'model' if item.get('role') == 'ai' else 'user'
        chat_history.append({'role': role, 'parts': [item.get('content')]})
        
    try:
        chat_session = model.start_chat(history=chat_history)
        response = chat_session.send_message(request.message)
        ai_message = response.text
        return {"response": ai_message}
    except Exception as e:
        print(f"Error occurred: {e}")
        return {"error": str(e)}

@app.post("/report")
def get_report(request: ReportRequest):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    transcript = ""
    for item in request.history:
        speaker = "Candidate" if item.get('role') == 'user' else "Interviewer (Athena)"
        transcript += f"{speaker}: {item.get('content')}\n\n"
        
    prompt = f"""
    As an expert hiring manager, please analyze the following interview transcript for a role requiring strong Excel skills. 
    Based *only* on the provided transcript, generate a constructive performance report for the candidate.
    The report should include:
    1. A brief overall summary of the interview.
    2. The candidate's strengths (what they answered well).
    3. Areas for improvement (where their understanding was weak or incorrect).
    
    Keep the tone professional and constructive.
    
    **Interview Transcript:**
    {transcript}
    """
    
    try:
        response = model.generate_content(prompt)
        return {"report": response.text}
    except Exception as e:
        print(f"Error generating report: {e}")
        return {"error": str(e)}