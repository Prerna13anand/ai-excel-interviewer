Design Document: AI-Powered Excel Mock Interviewer
Author: Prerna Anand
Date: September 13, 2025
Role: Founding AI Product Engineer

1. The Business Context & Problem Statement
Our company is currently experiencing rapid growth in its Finance, Operations, and Data Analytics teams. A core requirement for all new hires in these divisions is advanced proficiency in Microsoft Excel.

The primary business problem is that our current screening process for Excel skills has become a significant bottleneck. The manual technical interviews are time-intensive for our senior analysts and suffer from inconsistent evaluation criteria. This inefficiency directly slows down our hiring pipeline and jeopardizes our ability to meet growth targets. The objective is to develop an AI-driven solution to automate and standardize this assessment process.

2. Proposed Solution: "Athena," an AI Interview Agent
I propose the development of "Athena," an automated, conversational AI agent designed to conduct structured technical interviews for Microsoft Excel. Athena will simulate a real interview experience, providing a consistent and scalable solution to our screening problem.

The agent's core mission is to design a system that automates the assessment of a candidate's Excel skills.

Key Features:

Structured Interview Flow: The agent will manage a coherent, multi-turn conversation. It will introduce itself, explain the interview process, ask a series of questions, and provide a concluding summary.

Intelligent Answer Evaluation: The system will go beyond simple keyword matching to evaluate the candidate's understanding of concepts and their ability to explain them clearly.

Agentic Behavior: The agent will function like a real interviewer, capable of asking follow-up questions or providing hints to guide the candidate, while managing the state of the interview from start to finish.

Constructive Feedback Report: Upon completion, the agent will generate a detailed performance summary, highlighting the candidate's strengths and areas for improvement.

3. System Architecture & Technology Stack
I have full autonomy in choosing the technology stack, and my choices are based on industry best practices for performance, scalability, and ease of development for this PoC.

Large Language Model (LLM):

Choice: Gemini 1.5 Flash (Google)

Justification: The project was developed using Google's Gemini 1.5 Flash model. This choice was driven by its generous free tier, which is ideal for building and testing a Proof-of-Concept without incurring costs. Additionally, Gemini 1.5 Flash is a fast and capable model with strong conversational and instruction-following abilities, making it perfectly suited for the core task of evaluating a candidate's responses in real-time.

Backend Framework:

Choice: Python with FastAPI

Justification: Python is the standard for AI development. FastAPI is a modern, high-performance framework ideal for building the API that will connect our frontend to the LLM. Its asynchronous capabilities ensure the application remains responsive.

Frontend Framework:

Choice: React.js

Justification: React is a leading JavaScript library for building dynamic user interfaces. Its component-based architecture is perfect for creating a clean, manageable chat application. My prior experience with React also accelerated development.

Deployment Platform:

Choice: Vercel (Frontend) & Render (Backend)

Justification: Both services offer robust free tiers, seamless integration with GitHub for continuous deployment, and are purpose-built for modern web applications, making them ideal for a Proof-of-Concept.

4. Solving the "Cold Start" Problem
The assignment notes that we have no pre-existing dataset of interview transcripts. My strategy addresses this in two phases.

Phase 1: Knowledge Base Bootstrapping:
I would use a more powerful model, such as Gemini 1.5 Pro, to act as a subject matter expert to generate a foundational knowledge base. This involves creating a structured set of Excel questions categorized by difficulty (Beginner, Intermediate, Advanced) and topic (e.g., VLOOKUP, Pivot Tables, Conditional Formatting). For each question, I would generate an ideal answer and a rubric for evaluating potential responses. This rubric would be fed into the agent's system prompt to guide its evaluations.

Phase 2: Continuous Improvement with Human-in-the-Loop:
After the initial deployment, all interview transcripts and the AI's evaluations will be stored. These will be periodically reviewed by our senior analysts. Their feedback and corrections will be used to create a high-quality, proprietary dataset. This dataset will be invaluable for future iterations, including potentially fine-tuning a smaller, more specialized model to improve accuracy and reduce API costs.