from pydantic import BaseModel
from typing import List, Optional

class SummaryRequest(BaseModel):
    text: str
    level: str = "simple"

class SummaryResponse(BaseModel):
    summary: str

class QuizRequest(BaseModel):
    text: str
    num_question: int = 5
    num_choices: int = 4

class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    answer: str
    explanation: str

class QuizResponse(BaseModel):
    questions: list[QuizQuestion]

class FlashCardGenerateRequest(BaseModel):
    text: str
    num_flashcards: int = 10

class FlashCard(BaseModel):
    question: str
    answer: str

class FlashCardGenerateResponse(BaseModel):
    flashcards: list[FlashCard]


