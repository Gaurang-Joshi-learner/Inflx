#  Inflx – Social-to-Lead Agentic Workflow

## 📌 Overview
Inflx is an AI-powered conversational agent that converts user interactions into qualified leads. This project implements a **GenAI agent workflow** for a fictional SaaS product (AutoStream) that provides automated video editing tools.

The agent is capable of:
- Understanding user intent
- Answering product-related queries using RAG
- Detecting high-intent users
- Capturing leads via tool execution

---

## 🚀 Features

### ✅ Intent Detection
Classifies user messages into:
- Greeting
- Inquiry (pricing, features)
- High Intent (ready to subscribe)

---

###  RAG (Retrieval-Augmented Generation)
Answers are generated using a **local knowledge base** containing:
- Pricing details
- Product features
- Company policies

---

###  Lead Capture Tool
When high intent is detected:
1. Agent collects:
   - Name
   - Email
   - Platform (YouTube/Instagram)
2. Calls mock function:

```python
def mock_lead_capture(name, email, platform):
    print(f"Lead captured successfully: {name}, {email}, {platform}")

Architecture Explanation

This project uses LangGraph to build a structured agent workflow.

LangGraph was chosen because it provides:

Clear state management across multiple steps
Deterministic control over agent flow
Easy integration of tools and decision nodes

The system is divided into nodes:

Intent Node → Detects user intent
RAG Node → Retrieves answers from knowledge base
Lead Node → Collects user information
Tool Node → Executes lead capture

State is maintained using a shared dictionary (AgentState) that stores:

Messages
Intent
Name, Email, Platform

This ensures the agent remembers context across multiple turns (5–6 interactions), fulfilling the assignment requirement.

Conversation Flow
User asks pricing → RAG responds
User shows interest → intent switches to high_intent
Agent asks for:
Name
Email
Platform
Tool executes after all details are collected

 Tech Stack
Python 3.12
FastAPI (Backend)
Streamlit (Frontend)
LangGraph (Agent Workflow)
Gemini API (LLM)
Local JSON (RAG Knowledge Base)

 How to Run Locally
1. Clone the repo
git clone https://github.com/Gaurang-Joshi-learner/inflx-agent.git
cd inflx-agent
2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
3. Install dependencies
pip install -r requirements.txt
4. Add environment variable

Create .env file:

GOOGLE_API_KEY=your_api_key
5. Run Backend
uvicorn app.main:app --reload
6. Run Frontend
cd frontend
streamlit run app.py

WhatsApp Integration 

To integrate this agent with WhatsApp:

Use Twilio WhatsApp API
Configure a webhook endpoint (FastAPI /chat)
Incoming messages → sent to backend agent
Agent processes using LangGraph
Response → returned to Twilio → sent to user

Flow:

WhatsApp → Twilio → FastAPI Webhook → Agent → Response → Twilio → User

**Demo Video**
Watch Demo:
https://drive.google.com/file/d/1_3Vib6LyZaxjp3GBAN30PoloHeakplhW/view?usp=sharing
