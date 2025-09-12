# app.py

import streamlit as st
from research_agent.graph import build_graph

# Build graph
app = build_graph()

# Streamlit UI
st.title("🧠 AI Research Assistant")
st.write("Ask research questions and get synthesized answers from web + local docs.")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Enter your question:")

if st.button("Ask") and query:
    state = {"query": query, "history": st.session_state.history}
    result = app.invoke(state)

    # Update conversation history
    st.session_state.history = result["history"]

    st.subheader("Answer")
    st.write(result["final_answer"])

    # Show chat history
    st.subheader("Conversation History")
    for msg in st.session_state.history:
        st.write(msg)