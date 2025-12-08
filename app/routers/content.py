from fastapi import APIRouter
from app.models.schemas import SummaryRequest, SummaryResponse, QuizResponse, QuizRequest, FlashCardGenerateRequest, FlashCardGenerateResponse
from app.services.content_generator import generate_summary, generate_quiz, generate_flashcard
from app.services.auth_service import get_current_user
from app.services.auth_service import get_db
from fastapi import Depends
from app.services.content_service import save_summary, save_flashcard, save_quiz

router = APIRouter(prefix="/generate", tags=["content"])

@router.post("/summary", response_model=SummaryResponse)
def summary(req: SummaryRequest,
            db = Depends(get_db),
            user = Depends(get_current_user)):
    result = generate_summary(req)
    save_summary(db, user.id, result)
    return SummaryResponse(summary=result)

@router.post("/quiz-generate", response_model=QuizResponse)
def quiz(req: QuizRequest,
         db = Depends(get_db),
         user = Depends(get_current_user)):
    result = generate_quiz(req)
    save_quiz(db, user.id, topic = result.topic)
    return QuizResponse(questions=result)

@router.post("/flashcard-generate", response_model= FlashCardGenerateResponse)
def flashcard(req: FlashCardGenerateRequest,
              db =Depends(get_db),
              user = Depends(get_current_user)):
    result = generate_flashcard(req)
    
    for card in result:
        save_flashcard(db, user.id, card.question, card.answer)

    return FlashCardGenerateResponse(flashcards=result)
