# from fastapi import APIRouter
# from pydantic import BaseModel
# from datetime import datetime

# from app.core.config import get_settings
# from app.services.agents import ResearchAgents
# from app.services.retrieval import TavilyRetrievalSystem

# router = APIRouter(prefix="/api", tags=["api"])

# class ResearchRequest(BaseModel):
#     query: str

# @router.post("/research")
# def api_research(payload: ResearchRequest):
#     settings = get_settings()
#     agents = ResearchAgents(
#         groq_api_key=settings.groq_api_key, tavily_api_key=settings.tavily_api_key
#     )
#     retrieval = TavilyRetrievalSystem(api_key=agents.tavily_api_key)

#     search_results = retrieval.advanced_search(payload.query)
#     research_data = agents.research_agent(payload.query, search_results)
#     summary = agents.summarizer_agent(research_data)
#     critique = agents.critic_agent(summary)
#     final_report = agents.writer_agent(research_data, summary, critique)

#     return {
#         "query": payload.query,
#         "report": final_report,
#         "timestamp": datetime.now().isoformat(),
#         "metadata": {"ai_model": "llama-3.3-70b-versatile", "search_engine": "tavily_advanced"},
#     }



from fastapi import APIRouter
from pydantic import BaseModel
from app.services.research_pipeline import run_full_research

router = APIRouter(prefix="/api", tags=["api"])

class ResearchRequest(BaseModel):
    query: str

@router.post("/research")
def api_research(payload: ResearchRequest):
    result = run_full_research(payload.query)
    return {
        "query": result["query"],
        "report": result["report"],
        "timestamp": result["timestamp"],
        "metadata": result["metadata"],
    }
