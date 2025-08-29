# app.py
import os
import sys
import time
import uuid
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

# ──────────────────────────────────────────────────────────────────────────────
# Imports / PYTHONPATH
# Make sure we can import your backend package (adjust the path if needed)
# Example project structure assumed:
#   project/
#     backend/
#       __init__.py
#       langgraph_tool_backend.py  (exports `chatbot`)
#     frontend/
#       app.py  (this file)
# ──────────────────────────────────────────────────────────────────────────────
FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(FRONTEND_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now import your chatbot
# Expecting: from backend.langgraph_tool_backend import chatbot
try:
    from backend.main import workflow
except ModuleNotFoundError as e:
    st.error(
        "Import error: Could not import `backend.langgraph_tool_backend`.\n\n"
        "Fix: Ensure your project structure matches the comment above, "
        "and that `backend/__init__.py` exists."
    )
    st.stop()


# ──────────────────────────────────────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────────────────────────────────────
def new_thread_id() -> str:
    return str(uuid.uuid4())

def add_thread(thread_id: str) -> None:
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def reset_chat() -> None:
    st.session_state["thread_id"] = new_thread_id()
    add_thread(st.session_state["thread_id"])
    st.session_state["message_history"] = []

def load_conversation(thread_id: str):
    """
    Pull messages from backend state.
    We tolerate two shapes:
      1) iterable of LangChain BaseMessage objects, or
      2) list[dict] like {"role": "...", "content": "..."}
    """
    state = workflow.get_state(config={"configurable": {"thread_id": thread_id}})
    messages = state.values.get("messages", []) if hasattr(state, "values") else []

    formatted = []
    for msg in messages:
        # LangChain message objects
        if hasattr(msg, "content"):
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            formatted.append({"role": role, "content": msg.content})
        # Dict fallback
        elif isinstance(msg, dict) and "role" in msg and "content" in msg:
            formatted.append({"role": msg["role"], "content": msg["content"]})
    return formatted


# ──────────────────────────────────────────────────────────────────────────────
# Session Initialization
# ──────────────────────────────────────────────────────────────────────────────
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = new_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

add_thread(st.session_state["thread_id"])


# ──────────────────────────────────────────────────────────────────────────────
# Sidebar (Thread controls)
# ──────────────────────────────────────────────────────────────────────────────
#st.sidebar.title("💬 LangGraph Chatbot")

if st.sidebar.button("➕ New Chat", use_container_width=True):
    reset_chat()
    st.rerun()

st.sidebar.subheader("📂 Previous Conversations")

# Show newest first
for tid in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(tid), key=f"thread_btn_{tid}", use_container_width=True):
        st.session_state["thread_id"] = tid
        st.session_state["message_history"] = load_conversation(tid)
        st.rerun()


# ──────────────────────────────────────────────────────────────────────────────
# Main Chat UI
# ──────────────────────────────────────────────────────────────────────────────
st.title("LangGraph Chat")

# Render existing messages
for m in st.session_state["message_history"]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Input
user_input = st.chat_input("Type here…")

if user_input:
    # 1) Show user message immediately
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    config = {"configurable": {"thread_id": st.session_state["thread_id"]}}

    # 2) Stream assistant message
    with st.chat_message("assistant"):
        start = time.time()

        captured_chunks = []

        def ai_stream():
            """
            Yields only assistant text chunks for Streamlit to render live.
            Also captures them so we can store the final answer.
            """
            # Expecting chatbot.stream(...) -> yields (message_chunk, metadata)
            for message_chunk, metadata in workflow.stream(
                {'user_input': user_input},
                config=config,
                stream_mode="messages",
            ):
                if isinstance(message_chunk, AIMessage):
                    text = message_chunk.content or ""
                    captured_chunks.append(text)
                    yield text

        try:
            # st.write_stream streams tokens and returns the final text (or None on older versions)
            final_text = st.write_stream(ai_stream())
            # Be robust across Streamlit versions
            ai_message = "".join(captured_chunks) if captured_chunks else (final_text or "")
        except Exception as e:
            st.exception(e)
            ai_message = f"⚠️ Error while streaming: {e}"

        elapsed = time.time() - start
        st.caption(f"⏱️ Response time: {elapsed:.2f} seconds")

    # 3) Save assistant reply in history
    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})
