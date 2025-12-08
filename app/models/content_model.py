from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.core.database import Base

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
