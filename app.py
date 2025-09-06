from __future__ import annotations

import datetime as dt
from typing import Dict, List

import streamlit as st

from agent import generate_reply
from logger import ChatLogger


# --- Page setup ---
st.set_page_config(page_title="pinkman", page_icon="💬", layout="centered")

# --- Constants ---
MAX_MESSAGES: int = 100  # Cap in-memory history length

# --- Session state init ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "logger" not in st.session_state:
    st.session_state["logger"] = ChatLogger()

# --- Header (banner) ---
st.title("pinkman")
st.divider()

# --- Chat feed ---
for msg in st.session_state["messages"]:
    role = msg.get("role", "assistant")
    content = msg.get("content", "")
    with st.chat_message(role):
        st.markdown(content)

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
            reply = generate_reply(st.session_state["messages"], context=None)
        except Exception as e:  # noqa: BLE001 - surface any agent error to the UI
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
