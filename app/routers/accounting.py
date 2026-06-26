from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Project, User
from ..auth import get_current_user, require_subscription
from angel.accounting_agent import build_accounting_ledger

router = APIRouter(prefix="/projects/{project_id}/accounting", tags=["accounting"])

@router.get("/")
def get_accounting(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project or not project.accounting_ledger_json:
        raise HTTPException(status_code=404, detail="Accounting ledger not found")
    return project.accounting_ledger_json

@router.post("/build")
async def build_accounting(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _=Depends(require_subscription("pro"))
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project or not project.finance_data_json:
        raise HTTPException(status_code=404, detail="Finance data not found")
    ledger = await build_accounting_ledger(project.finance_data_json)
    project.accounting_ledger_json = ledger.dict()
    db.commit()
    return ledger.dict()
