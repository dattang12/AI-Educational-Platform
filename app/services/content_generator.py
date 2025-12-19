from app.services.ai_service import ask_ai
from app.models.schemas import SummaryRequest, QuizRequest, QuizQuestion, FlashCardGenerateRequest, FlashCardGenerateResponse, FlashCard
import json

def generate_summary(summary: SummaryRequest) -> str:
    prompt = f"Summaize this text at a {summary.level} level:\n\n{summary.text}"
    return ask_ai(prompt)

def generate_quiz(quiz: QuizRequest):
    prompt = f"""
Generate a multiple-choice quiz based on the following text or topic:

\"\"\"{quiz.text}\"\"\"

Create exactly {quiz.num_question} questions.
Each question must include:
- A clear question
- Exactly {quiz.num_choices} answer choices
- Only 1 correct answer
- {quiz.num_choices - 1} incorrect but realistic answers
- A short explanation that describes **why** the correct answer is correct

Return ONLY valid JSON in the following format:
 
[
  {{
    "question": "string",
    "options": ["option A", "option B", "option C", "option D"],
    "answer": "option A",
    "explanation": "string explaining why the answer is correct"
  }}
]
    """

    raw_output = ask_ai(prompt)
    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError:
        fixed = ask_ai(f"Fix the JSON formatting in this text:\n{raw_output}")
        data = json.loads(fixed)
    
    converted = []
    for item in data:
        question_obj = QuizQuestion(
            question=item["question"],
            options=item["options"],
            answer=item["answer"],
            explanation=item["explanation"]
        )
        converted.append(question_obj)

    return converted


def generate_flashcard(card: FlashCardGenerateRequest) -> str: 
    prompt = f"""
You are an AI that generates clear, concise front/back study flashcards.

Create exactly {card.num_flashcards} flashcards based on the following content:

\"\"\"{card.text}\"\"\"

Each flashcard must include:
- "question": a short keyword, concept, or question for the front side
- "answer": a simple, correct explanation for the back side

Return ONLY valid JSON in the following format:

[
  {{
    "question": "string",
    "answer": "string"
  }}
]

Do NOT add any text outside the JSON. No markdown, no commentary.
"""
    raw_output = ask_ai(prompt)
    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError:
        fixed = ask_ai(f"Fix the JSON formatting in this text:\n{raw_output}")
        data = json.loads(fixed)
    
    converted = []

    for item in data:
        flashcard = FlashCard(
            question=item["question"],
            answer=item["answer"]
        )
        converted.append(flashcard)

    return converted
