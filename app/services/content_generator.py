from app.services.ai_service import ask_ai
from app.models.schemas import SummaryRequest, QuizRequest, QuizQuestion
import json

def generate_summary(summary: SummaryRequest) -> str:
    prompt = f"Summaize this text at a {summary.level} level:\n\n{summary.text}"
    return ask_ai(prompt)

def generate_quiz(quiz: QuizRequest):
    prompt = f"""
Generate a multiple-choice quiz based on this topic:

\"\"\"{quiz.text}\"\"\"

Create exactly {quiz.num_question} questions.
Each question must have exactly {quiz.num_choices} answer choices.
- Only 1 answer is correct.
- {quiz.num_choices - 1} answers must be incorrect.
- Make sure the questions are clear and related to the text.

Return ONLY valid JSON in the following format:

[
  {{
    "question": "string",
    "options": ["option A", "option B", "option C", "option D"],
    "answer": "option A"
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
            answer=item["answer"]
        )
        converted.append(question_obj)

    return converted


