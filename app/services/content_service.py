from sqlalchemy.orm import Session
from app.models.content_model import Summary, Flashcard, Quiz

def save_summary(db: Session, user_id: int, content: str):
    summary = Summary(user_id=user_id, content=content)
    db.add(summary)
    db.commit()
    db.refresh(summary)
    return summary

def save_flashcard(db: Session, user_id: int, question: str, answer: str):
    flashcard = Flashcard(user_id=user_id, question=question, answer=answer)
    db.add(flashcard)
    db.commit()
    db.refresh(flashcard)
    return flashcard

def save_quiz(db: Session, user_id: int, topic: str):
    quiz = Quiz(user_id=user_id, topic=topic)
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz
    