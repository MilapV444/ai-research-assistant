# research_agent/memory.py

from langchain.memory import ConversationBufferMemory

# Conversation memory to store past Q&A
conversation_memory = ConversationBufferMemory(
    memory_key="chat_history",     # stored under this key
    return_messages=True           # return messages as objects, not just strings
)