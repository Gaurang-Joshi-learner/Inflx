from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes import (
    intent_node,
    greeting_node,
    rag_node,
    lead_node,
    tool_node,
    route_intent,
    check_lead_completion
)

builder = StateGraph(AgentState)

# -------- NODES --------
builder.add_node("intent", intent_node)
builder.add_node("greeting", greeting_node)
builder.add_node("rag", rag_node)
builder.add_node("lead", lead_node)
builder.add_node("tool", tool_node)

# -------- ENTRY --------
builder.set_entry_point("intent")

# -------- INTENT ROUTING --------
builder.add_conditional_edges(
    "intent",
    route_intent,
    {
        "greeting": "greeting",
        "rag": "rag",
        "lead": "lead"
    }
)

# -------- LEAD FLOW --------
builder.add_conditional_edges(
    "lead",
    check_lead_completion,
    {
        "complete": "tool",
        "incomplete": END
    }
)

# -------- END STATES --------
builder.add_edge("greeting", END)
builder.add_edge("rag", END)
builder.add_edge("tool", END)

graph = builder.compile()


def run_agent(message, session_state):
    state = {
        "messages": session_state.get("messages", []) + [message],
        "intent": session_state.get("intent"),
        "name": session_state.get("name"),
        "email": session_state.get("email"),
        "platform": session_state.get("platform"),
        "response": None
    }

    result = graph.invoke(state)

    # 🔥 safety fallback
    if not result.get("response"):
        result["response"] = "⚠️ Something went wrong in processing."

    return result