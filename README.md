# ai-excel-interviewer
AI-Powered Excel Mock Interviewer
This project is a Proof-of-Concept for an AI-powered conversational agent, "Athena," designed to automate the initial technical screening of a candidate's Microsoft Excel skills. It provides a consistent, scalable, and efficient alternative to manual interviews, addressing a key bottleneck in the hiring pipeline for data-centric roles.

Live Demo
You can interact with the live application here: https://ai-excel-interviewer-brown.vercel.app/

Key Features
🤖 Conversational Interface: A real-time chat experience that simulates a technical interview.

🧠 Intelligent Evaluation: Utilizes Google's Gemini 1.5 Flash model to understand and evaluate candidate responses beyond simple keywords.

📈 Structured Interview Flow: The agent introduces itself, asks a series of questions, and can provide a summary at the end.

🔁 Full-Stack Architecture: Built with a modern tech stack, featuring a React frontend and a Python (FastAPI) backend.

Technology Stack
Large Language Model: Google Gemini 1.5 Flash

Frontend: React.js, Axios

Backend: Python, FastAPI

Deployment: Vercel (Frontend) & Render (Backend)

Local Setup & Installation
To run this project on your local machine, please follow these steps.

Prerequisites
Node.js and npm installed

Python 3.8+ and pip installed

A Google Gemini API Key

1. Clone the Repository
git clone [https://github.com/](https://github.com/)[YOUR_GITHUB_USERNAME]/ai-excel-interviewer.git
cd ai-excel-interviewer

2. Backend Setup
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file and add your API key
echo "GOOGLE_API_KEY='your_gemini_api_key_here'" > .env

# Run the backend server
uvicorn main:app --reload

The backend will be running at http://127.0.0.1:8000.

3. Frontend Setup
Open a new terminal for the frontend.

# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Run the frontend server
npm start

The frontend will open in your browser at http://localhost:3000.

Deployment
The application is deployed using a dual-platform approach for optimal performance and scalability:

Backend: The FastAPI application is hosted on Render as a web service, automatically redeploying on any push to the main branch.

Frontend: The React application is hosted on Vercel, which is connected to the same GitHub repository and also redeploys on push.