from pydantic import BaseModel, EmailStr

# ---------- AI SCHEMAS ----------
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

# ---------- AUTH / USER SCHEMAS ----------

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# API responses: show user - info after login + after registration + profile
class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True

# response API sends when a user logs in.
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# to know who is logged in + which user is making the request
class TokenData(BaseModel):
    email: str | None = None