from pydantic import BaseModel
from typing import Optional, List, Dict

class EmailRequest(BaseModel):
    product_name: str
    product_description: str
    audience: str
    tone: Optional[str] = "friendly"   # friendly/professional/persuasive
    goal: Optional[str] = "drive signups"  # e.g., signup, demo, purchase
    iterations: Optional[int] = 1
    subject_line: str | None = None

class AgentStep(BaseModel):
    name: str
    output: str
    metadata: Optional[Dict] = None

class EmailResponse(BaseModel):
    subject: str
    body: str
    score: float
    steps: List[AgentStep]
