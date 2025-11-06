from typing import List, Optional
from pydantic import BaseModel

class WorkflowConfig(BaseModel):
    role_order: List[str] = ["L1", "L2", "L3"]

class WorkflowRequest(BaseModel):
    request_id: str
    title: str
    current_stage_index: int = 0

class WorkflowTransition(BaseModel):
    request_id: str
    action: str  # approve or reject

class WorkflowStatus(BaseModel):
    request_id: str
    status: str  # Pending, Approved, Rejected
    stage: Optional[str] = None