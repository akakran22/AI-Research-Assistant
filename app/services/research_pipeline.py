from datetime import datetime
from app.core.config import get_settings
from app.services.agents import ResearchAgents
from app.services.retrieval import TavilyRetrievalSystem

def run_full_research(query: str) -> dict:
    settings = get_settings()

    agents = ResearchAgents(
        groq_api_key=settings.groq_api_key,
        tavily_api_key=settings.tavily_api_key
    )
    retrieval = TavilyRetrievalSystem(api_key=agents.tavily_api_key)

    # Research pipeline
    search_results = retrieval.advanced_search(query)
    research_data = agents.research_agent(query, search_results)
    summary = agents.summarizer_agent(research_data)
    critique = agents.critic_agent(summary)
    final_report = agents.writer_agent(research_data, summary, critique)

    return {
        "query": query,
        "research_data": research_data,
        "summary": summary,
        "critique": critique,
        "report": final_report,
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "ai_model": "llama-3.3-70b-versatile",
            "search_engine": "tavily_advanced"
        },
    }
