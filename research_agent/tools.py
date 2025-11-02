# research_agent/tools.py

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.chains import RetrievalQA
import os

# 🔍 Web Search Tool
search_tool = DuckDuckGoSearchRun()

# 📄 Create FAISS Index
def create_vectorstore(folder_path: str = "data"):
    """
    Create a FAISS vectorstore from local .txt or .pdf documents and save it.
    """
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    docs = []

    # Load all supported files in the folder
    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)
        if file.endswith(".txt"):
            docs.extend(TextLoader(path).load())
        elif file.endswith(".pdf"):
            docs.extend(PyPDFLoader(path).load())

    if not docs:
        raise ValueError(f"No supported documents found in {folder_path}")

    # Build FAISS and save
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(folder_path)
    print(f"✅ FAISS index created and saved in {folder_path}")

# 📄 Load FAISS Index
def load_vectorstore(folder_path: str = "data"):
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    index_file = os.path.join(folder_path, "index.faiss")
    if not os.path.exists(index_file):
        raise FileNotFoundError(f"No FAISS index found in {folder_path}. Run create_vectorstore() first.")
    return FAISS.load_local(folder_path, embeddings, allow_dangerous_deserialization=True)

# 📄 Retrieval Q&A
def get_doc_qa(folder_path: str = "data"):
    """
    Create a RetrievalQA chain to answer questions from local documents.
    Falls back if no FAISS index exists.
    """
    try:
        vectorstore = load_vectorstore(folder_path)
        retriever = vectorstore.as_retriever()
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

        return RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff"
        )
    except FileNotFoundError:
        print("⚠️ No FAISS index found. Run create_vectorstore() first or skip document Q&A.")
        return None



