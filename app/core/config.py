import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # AI SETTING
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL")
    GROQ_BASE_URL = os.getenv("GROQ_BASE_URL")

    # AUTH SETTING
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    DATABASE_URL= os.getenv("DATABASE_URL")
    
settings = Settings()
