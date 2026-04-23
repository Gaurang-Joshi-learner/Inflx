from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.graph import run_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str

# simple in-memory session
sessions = {}

@router.post("/chat")
async def chat(req: ChatRequest):
    session = sessions.get(req.session_id, {})

    result = run_agent(req.message, session)

    # 🔥 store updated state
    sessions[req.session_id] = result

    return {"response": result["response"]}