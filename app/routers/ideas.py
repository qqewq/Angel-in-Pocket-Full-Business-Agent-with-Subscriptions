from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from ..database import get_db
from ..models import User, Project
from ..auth import get_current_user, require_subscription
from angel.idea_intake import capture_vision, capture_constraints

router = APIRouter(prefix="/ideas", tags=["ideas"])

class IdeaInput(BaseModel):
    idea: str
    product_type: Optional[str] = None
    audience: Optional[str] = None
    values: List[str] = []
    constraints: dict = {}

@router.post("/")
def submit_idea(
    input: IdeaInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Free users can only have 1 project
    if current_user.subscription_tier.value == "free":
        project_count = db.query(Project).filter(Project.user_id == current_user.id).count()
        if project_count >= 1:
            raise HTTPException(
                status_code=402,
                detail="Free tier allows only 1 project. Upgrade to Pro for unlimited projects."
            )
    vision = capture_vision(input.dict())
    constraints = capture_constraints(input.dict())
    project = Project(
        user_id=current_user.id,
        vision_json=vision.dict(),
        constraints_json=constraints.dict(),
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"project_id": project.id, "vision": vision.dict(), "constraints": constraints.dict()}
