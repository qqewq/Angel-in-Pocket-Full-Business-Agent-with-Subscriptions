# Angel Idea Intake - stub (content omitted in source document)
from pydantic import BaseModel
from typing import Dict, Any

class Vision(BaseModel):
    idea: str = ""
    product_type: str = ""
    audience: str = ""
    values: list = []
    description: str = ""

class Constraints(BaseModel):
    budget: float = 0.0
    timeline: str = ""
    resources: list = []
    risks: list = []
    regulations: list = []

def capture_vision(data: Dict[str, Any]) -> Vision:
    return Vision(**data)

def capture_constraints(data: Dict[str, Any]) -> Constraints:
    return Constraints(**data)
