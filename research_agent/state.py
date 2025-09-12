# research_agent/state.py

from typing import TypedDict, List

class ResearchState(TypedDict):
    query: str               # user’s research question
    search_results: str      # web search output
    doc_results: str         # local doc QA output
    final_answer: str        # synthesized answer
    history: List[str]       # conversation history
