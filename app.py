from __future__ import annotations
import datetime as dt
import html
from typing import Dict, List
import streamlit as st
from ai import AI
from logger import ChatLogger


# --- Page setup ---
st.set_page_config(
    page_title="pinkman",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Constants ---
MAX_MESSAGES: int = 100  # Cap in-memory history length

# --- Session state init ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "logger" not in st.session_state:
    st.session_state["logger"] = ChatLogger()

# --- Left sidebar (collapsible) ---
with st.sidebar:
    st.title("Pinkman")
    st.markdown(
        (
            "<div class=\"sidebar-desc\" style=\"color:#888;\">"
            "<p><strong>Jessy Pinkman</strong> is a no-frills Streamlit chat UI—fast, simple, and setup-free. It lets you plug directly into your AI backend with a clean single-page interface. Perfect for makers, hackers, and data scientists who want to prototype quickly without boilerplate: lighter than a CLI, richer than raw text, and built for fast demos, sharing, and iteration.</p>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

# --- Styles (align user right, assistant left; no avatars) ---
# Load external CSS if present
from pathlib import Path as _Path
_css_path = _Path(__file__).parent / "assets" / "styles.css"
if _css_path.exists():
    st.markdown(f"<style>{_css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

# --- Chat feed ---
_bubbles: list[str] = []
for msg in st.session_state["messages"]:
    role = msg.get("role", "assistant")
    content = msg.get("content", "")
    safe = html.escape(content)
    cls = "user" if role == "user" else "assistant"
    _bubbles.append(f'<div class="msg {cls}"><div class="content">{safe}</div></div>')

st.markdown(
    f'<div class="chat-feed">{"".join(_bubbles)}</div>',
    unsafe_allow_html=True,
)

# --- Input & send ---
prompt = st.chat_input("Type a message and press Enter")
if prompt is not None:
    text = prompt.strip()
    if text:
        # Append user message
        user_msg = {
            "role": "user",
            "content": text,
            # Timestamp is currently unused in UI but kept for future needs
            "ts": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        }
        st.session_state["messages"].append(user_msg)
        st.session_state["logger"].log(user_msg["role"], user_msg["content"])

        # Generate assistant reply
        try:
            ai = AI()
            reply = ai.generate_reply(st.session_state["messages"], context=None)
    except Exception as e:  # noqa: BLE001 - surface any AI error to the UI
            st.error(f"Couldn't get a reply: {e}")
        else:
            ai_msg = {
                "role": "assistant",
                "content": reply,
                "ts": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
            }
            st.session_state["messages"].append(ai_msg)
            st.session_state["logger"].log(ai_msg["role"], ai_msg["content"])

            # Enforce cap (keep most recent messages)
            if len(st.session_state["messages"]) > MAX_MESSAGES:
                st.session_state["messages"] = st.session_state["messages"][-MAX_MESSAGES:]

    # Re-render immediately so the new messages show up
    st.rerun()
