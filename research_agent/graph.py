# research_agent/graph.py

from langgraph.graph import StateGraph, END
from research_agent.state import ResearchState
from research_agent.tools import search_tool, get_doc_qa
from langchain_openai import ChatOpenAI
import os

# LLM setup
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Tool for document QA
doc_qa = get_doc_qa("data")

# 🔹 Define nodes
def search_node(state: ResearchState) -> ResearchState:
    """Run web search."""
    query = state["query"]
    results = search_tool.run(query)
    state["search_results"] = results
    return state

def doc_node(state: ResearchState) -> ResearchState:
    """Run local document Q&A."""
    query = state["query"]
    results = doc_qa.run(query)
    state["doc_results"] = results
    return state

def synthesis_node(state: ResearchState) -> ResearchState:
    """Combine web + doc results into final answer."""
    query = state["query"]
    search = state.get("search_results", "")
    docs = state.get("doc_results", "")

    prompt = f"""
    You are a research assistant.
    Question: {query}

    Web Results: {search}
    Document Results: {docs}

    Provide a clear, well-structured final answer.
    """
    response = llm.invoke(prompt)
    state["final_answer"] = response.content
    state["history"].append(f"User: {query}")
    state["history"].append(f"Assistant: {response.content}")
    return state

# 🔹 Build the graph
def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("search", search_node)
    graph.add_node("doc", doc_node)
    graph.add_node("synthesis", synthesis_node)

    # flow: search -> doc -> synthesis
    graph.set_entry_point("search")
    graph.add_edge("search", "doc")
    graph.add_edge("doc", "synthesis")
    graph.add_edge("synthesis", END)

    return graph.compile()