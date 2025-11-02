from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
try:
    from langchain.chains import create_retrieval_chain
except ImportError:
    # Fallback for older LangChain versions
    from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
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

    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)
        if file.endswith(".txt"):
            docs.extend(TextLoader(path).load())
        elif file.endswith(".pdf"):
            docs.extend(PyPDFLoader(path).load())

    if not docs:
        raise ValueError(f"No supported documents found in {folder_path}")

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


# 🧠 Retrieval Q&A (new LangChain ≥ 0.3 syntax)
def get_doc_qa(folder_path: str = "data"):
    """
    Build a retrieval chain to answer questions using local documents.
    """
    try:
        vectorstore = load_vectorstore(folder_path)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

        prompt = ChatPromptTemplate.from_template(
            "You are a helpful research assistant. Use the context below to answer accurately.\n\n{context}\n\nQuestion: {input}"
        )

        combine_docs_chain = create_stuff_documents_chain(llm, prompt)
        retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

        return retrieval_chain
    except FileNotFoundError:
        print("⚠️ No FAISS index found. Run create_vectorstore() first or skip document Q&A.")
        return None

