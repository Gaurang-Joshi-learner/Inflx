import streamlit as st
import requests
import uuid
import time

API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="Inflx ", page_icon="🎬", layout="wide")

# ---------- SESSION INIT ----------
if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "current_session" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.current_session = new_id
    st.session_state.sessions[new_id] = []

# ---------- CSS ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0E1117;
    color: white;
}

.chat-box {
    max-width: 800px;
    margin: auto;
}

.user-msg {
    background-color: #1F2937;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    text-align: right;
}

.bot-msg {
    background-color: #111827;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.session-btn {
    background-color: #111827;
    padding: 8px;
    border-radius: 8px;
    margin-bottom: 5px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 💬 Chats")

    # New chat button
    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.current_session = new_id
        st.session_state.sessions[new_id] = []

    # Show sessions
    for session_id, messages in st.session_state.sessions.items():
        if messages:
            title = messages[0]["content"][:25]
        else:
            title = "New Chat"

        if st.button(title, key=session_id):
            st.session_state.current_session = session_id

# ---------- HEADER ----------
st.markdown("## 🎬 Inflx ")
st.caption("AI-powered video automation assistant")

# ---------- CURRENT CHAT ----------
current_session = st.session_state.current_session
messages = st.session_state.sessions[current_session]

st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for msg in messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- INPUT ----------
user_input = st.chat_input("Type your message...")

if user_input:
    messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                API_URL,
                json={
                    "message": user_input,
                    "session_id": current_session
                }
            )

            data = response.json()
            bot_reply = data.get("response", "⚠️ Something went wrong.")

        except Exception as e:
            bot_reply = f"⚠️ Error: {e}"

    # Typing animation
    placeholder = st.empty()
    full_text = ""

    for char in bot_reply:
        full_text += char
        placeholder.markdown(
            f'<div class="bot-msg">{full_text}</div>',
            unsafe_allow_html=True
        )
        time.sleep(0.01)

    messages.append({"role": "assistant", "content": bot_reply})