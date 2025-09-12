# research_agent/tools.py

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
import os

# 🔍 Web Search Tool
search_tool = DuckDuckGoSearchRun()

# 📄 Local Document Q&A
def load_vectorstore(folder_path: str = "data"):
    """
    Load documents into a FAISS vector database for semantic search.
    """
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    return FAISS.load_local(folder_path, embeddings, allow_dangerous_deserialization=True)

def get_doc_qa(folder_path: str = "data"):
    """
    Create a RetrievalQA chain to answer questions from local documents.
    """
    vectorstore = load_vectorstore(folder_path)
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )