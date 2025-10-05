import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from research_agent.graph import build_graph

# --- Page Config ---
st.set_page_config(page_title="AI Research Assistant", page_icon="🤖", layout="wide")

# --- Custom CSS for chat bubbles ---
st.markdown("""
    <style>
    body {
        background-color: #1e1e2f;
        color: white;
    }
    .main {
        background-color: #1e1e2f;
    }
    .user-bubble {
        background-color: #2b313e;
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 0px 18px;
        margin: 8px 0px;
        text-align: right;
        max-width: 70%;
        float: right;
        clear: both;
    }
    .bot-bubble {
        background-color: #3e4a61;
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 0px;
        margin: 8px 0px;
        text-align: left;
        max-width: 70%;
        float: left;
        clear: both;
    }
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #444;
        background-color: #242432;
        margin-bottom: 20px;
    }
    .stTextInput>div>div>input {
        background-color: #2b313e;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Info ---
st.sidebar.title("📌 About this App")
st.sidebar.write("An **AI-powered Research Assistant** built with **LangChain + LangGraph + OpenAI**.")
st.sidebar.success("✅ Can surf through internet✅ Summarize research papers\n✅ Remembers Conversations")
st.sidebar.info("🚀 Imagine this deployed on your website to **reduce support workload by 50%**.")
st.sidebar.markdown("---")
st.sidebar.markdown("💡 Want this for your business?\n👉 [Contact Me](mailto:your@email.com)")

# --- Main Title ---
st.title("🤖 AI Research Assistant")
st.write("Ask me about **research papers, summarisation, write up.**")

# --- Session State ---
if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Chat Input ---
query = st.text_input("💬 Type your message:", "")

if st.button("Send", use_container_width=True) and query:
    result = st.session_state.graph.invoke({"query": query, "response": ""})
    st.session_state.chat_history.append(("User", query))
    st.session_state.chat_history.append(("Research Assistant", result["response"]))

# --- Display Chat History ---
st.subheader("💬 Conversation")
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for speaker, msg in st.session_state.chat_history:
    if speaker == "Customer":
        st.markdown(f'<div class="user-bubble">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{msg}</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

