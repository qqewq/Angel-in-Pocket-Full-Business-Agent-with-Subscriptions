from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Project, User
from ..auth import get_current_user, require_subscription
from angel.idea_intake import Vision, Constraints
from angel.preference_model import build_preferences
from angel.product_designer import design_product
from angel.business_designer import build_business_canvas
from angel.process_mapper import build_process_graph
from angel.strategy_planner import plan_strategy

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/{project_id}/launch")
async def launch_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _=Depends(require_subscription("pro"))  # launching requires Pro or higher
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    vision = Vision(**project.vision_json)
    constraints = Constraints(**project.constraints_json)
    preferences = build_preferences(vision, constraints)
    product_spec = design_product(vision, preferences)
    canvas = build_business_canvas(vision, product_spec, constraints)
    process_graph = build_process_graph(canvas)
    project.product_spec_json = product_spec.dict()
    project.canvas_json = canvas.dict()
    project.process_graph_json = process_graph.dict()
    db.commit()
    strategy = await plan_strategy(canvas, process_graph, constraints)
    return {"project_id": project_id, "product": product_spec.dict(), "canvas": canvas.dict(), "strategy": strategy}

@router.get("/{project_id}/status")
def get_status(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "vision": project.vision_json,
        "product": project.product_spec_json,
        "canvas": project.canvas_json,
        "process_graph": project.process_graph_json
    }

@router.get("/{project_id}/stability")
async def get_stability(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project or not project.canvas_json:
        raise HTTPException(status_code=404, detail="Project not fully designed")
    from gra_core.stability_engine import analyze_canvas
    from gra_core.models import BusinessCanvas
    canvas = BusinessCanvas(**project.canvas_json)
    report = await analyze_canvas(canvas)
    return report.dict()

@router.post("/{project_id}/nullify")
async def nullify_processes(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project or not project.process_graph_json:
        raise HTTPException(status_code=404)
    from gra_core.stability_engine import nullify_bad_processes
    from gra_core.models import ProcessGraph
    graph = ProcessGraph(**project.process_graph_json)
    cleaned = await nullify_bad_processes(graph)
    project.process_graph_json = cleaned.dict()
    db.commit()
    return cleaned.dict()
