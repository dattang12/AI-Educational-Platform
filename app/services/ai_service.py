from openai import OpenAI
from app.core.config import settings
from app.models.schemas import SummaryRequest, SummaryResponse


client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url = settings.GROQ_BASE_URL,
)

def ask_ai(prompt: str) -> str:
    """Send a prompt to the AI model and return the response."""
    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
