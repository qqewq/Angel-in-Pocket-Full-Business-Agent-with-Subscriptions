from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Project, User
from ..auth import get_current_user, require_subscription
from angel.process_mapper import build_process_graph
from angel.business_designer import build_business_canvas
from gra_core.stability_engine import nullify_bad_processes
from gra_core.models import ProcessGraph

router = APIRouter(prefix="/projects/{project_id}/processes", tags=["processes"])

@router.get("/")
def get_processes(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project or not project.process_graph_json:
        raise HTTPException(status_code=404, detail="Processes not found")
    return project.process_graph_json

@router.post("/build")
def build_processes(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project or not project.canvas_json:
        raise HTTPException(status_code=404, detail="Business canvas not found")
    canvas = build_business_canvas(**project.canvas_json)
    process_graph = build_process_graph(canvas)
    project.process_graph_json = process_graph.dict()
    db.commit()
    return process_graph.dict()

@router.post("/nullify")
async def nullify_processes(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _=Depends(require_subscription("pro"))
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project or not project.process_graph_json:
        raise HTTPException(status_code=404, detail="Process graph not found")
    graph = ProcessGraph(**project.process_graph_json)
    cleaned = await nullify_bad_processes(graph)
    project.process_graph_json = cleaned.dict()
    db.commit()
    return cleaned.dict()
