from app.upload.pdf_handler import extract_text_from_pdf
from app.upload.text_handler import extract_text_from_txt
from app.services.auth_service import get_current_user, get_db
from app.services.content_service import save_plaintext, save_summary, save_flashcard, save_quiz
from fastapi import Query
from app.models.schemas import QuizRequest, SummaryRequest, FlashCardGenerateRequest
from app.services.content_generator import generate_flashcard, generate_quiz, generate_summary


from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

import os
import uuid

router = APIRouter(prefix="/uploads", tags=["upload"])

UPLOAD_DIR = "uploaded_file"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...),
                     mode: str = Query("summary", enum=["summary", "flashcard", "quiz"]),
                     db = Depends(get_db),
                     user = Depends(get_current_user)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Wrong file format. PDF only.")
    
    filename = f"{uuid.uuid4()}_{file.filename}" # Create unique name
    path = os.path.join(UPLOAD_DIR, filename) # Place to save

    with open(path, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(path)
    save_plaintext(db, user.id, filename, content=text)

    if mode == "summary":
        result = generate_summary(SummaryRequest(text=text))
        save_summary(db, user.id, content=text)
        return {"type": "summary", "result": result}

    elif mode == "flashcard":
        cards = generate_flashcard(FlashCardGenerateRequest(text=text))
        for c in cards:
            save_flashcard(db, user.id, c.question, c.answer)
        return {"type": "flashcard", "result": cards}

    elif mode == "quiz":
        quiz = generate_quiz(QuizRequest(text=text))
        save_quiz(db, user.id, topic=filename)
        return {"type": "quiz", "result": quiz}


@router.post("/text")
async def upload_text(file: UploadFile = File(...),
                      mode : str = Query ("summary", enum=["summary", "flashcard", "quiz"]),
                      db = Depends(get_db),
                      user = Depends(get_current_user)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(400, "Wrong file format. Text files only.")
    
    filename = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(file, "wb") as f:
        f.write(await file.read())
    
    text = extract_text_from_txt(path)
    save_plaintext(db, user.id, filename, content=text)

    if mode == "summary":
        result = generate_summary(SummaryRequest(text=text))
        save_summary(db, user.id, content=text)
        return {"type": "summary", "result": result}

    elif mode == "flashcard":
        cards = generate_flashcard(FlashCardGenerateRequest(text=text))
        for c in cards:
            save_flashcard(db, user.id, c.question, c.answer)
        return {"type": "flashcard", "result": cards}

    elif mode == "quiz":
        quiz = generate_quiz(QuizRequest(text=text))
        save_quiz(db, user.id, topic=filename)
        return {"type": "quiz", "result": quiz}