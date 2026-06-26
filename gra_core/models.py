# GRA Core Models - stub (content omitted in source document)
from pydantic import BaseModel
from typing import Dict, List, Any

class BusinessCanvas(BaseModel):
    segments: Dict[str, Any] = {}
    value_propositions: Dict[str, Any] = {}
    channels: Dict[str, Any] = {}
    customer_relationships: Dict[str, Any] = {}
    revenue_streams: Dict[str, Any] = {}
    key_resources: Dict[str, Any] = {}
    key_activities: Dict[str, Any] = {}
    key_partnerships: Dict[str, Any] = {}
    cost_structure: Dict[str, Any] = {}

class ProcessGraph(BaseModel):
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {}

class StabilityReport(BaseModel):
    score: float = 0.0
    issues: List[str] = []
    recommendations: List[str] = []
