from fastapi import APIRouter
from app.models.schemas import SummaryRequest, SummaryResponse
from app.services.content_generator import generate_summary

router = APIRouter(prefix="/generate", tags=["content"])

@router.post("/summary", response_model=SummaryResponse)
def summary(req: SummaryRequest):
    result = generate_summary(req)
    return SummaryResponse(summary=result)