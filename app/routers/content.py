from fastapi import APIRouter
from app.models.schemas import SummaryRequest, SummaryResponse, QuizResponse, QuizRequest, FlashCardGenerateRequest, FlashCardGenerateResponse
from app.services.content_generator import generate_summary, generate_quiz, generate_flashcard

router = APIRouter(prefix="/generate", tags=["content"])

@router.post("/summary", response_model=SummaryResponse)
def summary(req: SummaryRequest):
    result = generate_summary(req)
    return SummaryResponse(summary=result)

@router.post("/quiz-generate", response_model=QuizResponse)
def quiz(req: QuizRequest):
    result = generate_quiz(req)
    return QuizResponse(questions=result)

@router.post("/flashcard-generate", response_model= FlashCardGenerateResponse)
def flashcard(req: FlashCardGenerateRequest):
    result = generate_flashcard(req)
    return FlashCardGenerateResponse(flashcards=result)
