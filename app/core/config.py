import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL")
    GROQ_BASE_URL = os.getenv("GROQ_BASE_URL")

settings = Settings()
