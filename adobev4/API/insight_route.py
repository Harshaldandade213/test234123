from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

# Direct import since we're running from adobev4 directory
from Services.insight_service import generate_insights_gemini_flash

router = APIRouter()

class InsightRequest(BaseModel):
    query: str
    passages: list[dict]
    thinking_budget: int | None = None

@router.post("/insights")
def insights_endpoint(req: InsightRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Missing Gemini API key")

    insights = generate_insights_gemini_flash(
        query=req.query,
        passages=req.passages,
        api_key=api_key,
        thinking_budget=req.thinking_budget
    )
    return insights
