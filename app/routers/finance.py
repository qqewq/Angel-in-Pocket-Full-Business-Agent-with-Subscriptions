from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Project, User
from ..auth import get_current_user, require_subscription
from angel.finance_agent import build_finance_model
from angel.strategy_planner import plan_strategy

router = APIRouter(prefix="/projects/{project_id}/finance", tags=["finance"])

@router.get("/")
def get_finance(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project or not project.finance_data_json:
        raise HTTPException(status_code=404, detail="Finance data not found")
    return project.finance_data_json

@router.post("/build")
async def build_finance(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _=Depends(require_subscription("pro"))
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project or not project.canvas_json:
        raise HTTPException(status_code=404, detail="Project canvas not found")
    finance_data = await build_finance_model(project.canvas_json)
    project.finance_data_json = finance_data.dict()
    db.commit()
    return finance_data.dict()
