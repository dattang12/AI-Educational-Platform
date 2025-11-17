from pydantic import BaseModel
from typing import List, Optional

class SummaryRequest(BaseModel):
    text: str
    level: str = "simple"

class SummaryResponse(BaseModel):
    summary: str
    