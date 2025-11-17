from app.services.ai_service import ask_ai
from app.models.schemas import SummaryRequest

def generate_summary(summary: SummaryRequest) -> str:
    prompt = f"Summaize this text at a {summary.level} level:\n\n{summary.text}"
    return ask_ai(prompt)