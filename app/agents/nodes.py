import re
from app.services.intent_classifier import classify_intent
from app.rag.retriever import get_answer
from app.tools.lead_capture import mock_lead_capture


# -------- INTENT NODE --------
def intent_node(state):
    message = state["messages"][-1]
    msg = message.lower()

    # 🔒 Never allow pricing to trigger lead
    if any(x in msg for x in ["price", "pricing", "cost", "how much"]):
        return {**state, "intent": "inquiry"}

    # 🔒 Lock once high intent
    if state.get("intent") == "high_intent":
        print("🔒 Staying in high_intent mode")
        return state

    intent = classify_intent(message)
    print("Detected Intent:", intent)

    return {**state, "intent": intent}


# -------- GREETING NODE --------
def greeting_node(state):
    return {
        **state,
        "response": "Hey! 👋 How can I help you with Inflx "
    }


# -------- RAG NODE --------
def rag_node(state):
    query = state["messages"][-1]

    answer = get_answer(query)

    return {
        **state,
        "response": answer
    }


# -------- LEAD NODE --------
def lead_node(state):
    message = state["messages"][-1].strip().lower()

    print("🔥 LEAD NODE STATE BEFORE:", state)

    # -------- EMAIL --------
    email_match = re.findall(r'\S+@\S+', message)
    if email_match:
        state["email"] = email_match[0]

    # -------- PLATFORM --------
    if "youtube" in message:
        state["platform"] = "YouTube"
    elif "instagram" in message:
        state["platform"] = "Instagram"

    # -------- NAME --------
    if not state.get("name"):
        if "my name is" in message:
            state["name"] = message.split("is")[-1].strip().title()
        elif "i am" in message:
            state["name"] = message.split("am")[-1].strip().title()
        elif len(message.split()) <= 2 and "@" not in message:
            state["name"] = message.title()

    print("🔥 LEAD NODE STATE AFTER:", state)

    # -------- QUESTIONS --------
    if not state.get("name"):
        return {**state, "response": "Great! Can I have your name?"}

    if not state.get("email"):
        return {
            **state,
            "response": f"Nice to meet you {state['name']}! Please share your email."
        }

    if not state.get("platform"):
        return {
            **state,
            "response": "Which platform do you create content on? (YouTube/Instagram)"
        }

    return state


# -------- TOOL NODE --------
def tool_node(state):
    print("🔥 TOOL NODE EXECUTED")

    result = mock_lead_capture(
        name=state["name"],
        email=state["email"],
        platform=state["platform"]
    )

    return {
        **state,
        "response": f"✅ {result['message']}\n\nOur team will contact you shortly 🚀"
    }


# -------- ROUTER --------
def route_intent(state):
    intent = state.get("intent")

    # 🔒 Stay in lead once triggered
    if intent == "high_intent":
        return "lead"

    if intent == "greeting":
        return "greeting"

    return "rag"


# -------- CHECK COMPLETION --------
def check_lead_completion(state):
    print("🔥 CHECKING LEAD:", state)

    if all([
        state.get("name"),
        state.get("email"),
        state.get("platform")
    ]):
        print("✅ COMPLETE")
        return "complete"

    print("❌ INCOMPLETE")
    return "incomplete"