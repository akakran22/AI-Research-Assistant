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

