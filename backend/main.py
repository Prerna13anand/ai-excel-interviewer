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
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
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

# --- NEW ENDPOINT FOR THE REPORT ---
@app.post("/report")
def get_report(request: ReportRequest):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    # Format the history into a simple transcript string
    transcript = ""
    for item in request.history:
        speaker = "Candidate" if item.get('role') == 'user' else "Interviewer"
        transcript += f"{speaker}: {item.get('content')}\n\n"
        
    # Create a specific prompt for the summarization task
    prompt = f"""
    As an expert hiring manager, please analyze the following interview transcript for a role requiring strong Excel skills. 
    Based *only* on the provided transcript, generate a constructive performance report for the candidate.
    The report should include:
    1.  A brief overall summary of the interview.
    2.  The candidate's strengths (what they answered well).
    3.  Areas for improvement (where their understanding was weak or incorrect).
    
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