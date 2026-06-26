from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Project, User
from ..auth import get_current_user
from angel.product_designer import design_product
from angel.idea_intake import Vision, Constraints
from angel.preference_model import build_preferences

router = APIRouter(prefix="/projects/{project_id}/products", tags=["products"])

@router.get("/")
def get_product(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project or not project.product_spec_json:
        raise HTTPException(status_code=404, detail="Product not designed")
    return project.product_spec_json

@router.post("/redesign")
def redesign(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404)
    vision = Vision(**project.vision_json)
    constraints = Constraints(**project.constraints_json)
    prefs = build_preferences(vision, constraints)
    new_spec = design_product(vision, prefs)
    project.product_spec_json = new_spec.dict()
    db.commit()
    return new_spec.dict()
