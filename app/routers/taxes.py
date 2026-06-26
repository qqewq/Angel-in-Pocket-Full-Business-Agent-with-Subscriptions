from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Project, User
from ..auth import get_current_user, require_subscription
from angel.tax_agent import build_tax_regime

router = APIRouter(prefix="/projects/{project_id}/taxes", tags=["taxes"])

@router.get("/")
def get_taxes(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project or not project.tax_regime_json:
        raise HTTPException(status_code=404, detail="Tax regime not found")
    return project.tax_regime_json

@router.post("/build")
async def build_taxes(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _=Depends(require_subscription("pro"))
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project or not project.accounting_ledger_json:
        raise HTTPException(status_code=404, detail="Accounting ledger not found")
    tax_regime = await build_tax_regime(project.accounting_ledger_json)
    project.tax_regime_json = tax_regime.dict()
    db.commit()
    return tax_regime.dict()
