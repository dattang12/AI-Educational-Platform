from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from app.core.database import Base
from datetime import datetime

class Summary(Base):
    __tablename__ = "summaries"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))


class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True)
    topic = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))


class Flashcard(Base):
    __tablename__ = "flashcards"
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

class PlainText(Base):
    __tablename__ = "plaintext"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

