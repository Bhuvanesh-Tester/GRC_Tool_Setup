from typing import List
from fastapi import APIRouter, Depends, HTTPException
from utils.auth import get_current_user
from utils.rbac import require_roles, Role
from utils.demo_store import WorkflowsStore
from schemas.workflow import WorkflowConfig, WorkflowRequest, WorkflowTransition, WorkflowStatus

router = APIRouter(prefix="/workflows", tags=["workflows"])
store = WorkflowsStore()

@router.get("/config")
def get_config(user=Depends(get_current_user)) -> WorkflowConfig:
    return store.get_config()

@router.post("/config", dependencies=[Depends(require_roles([Role.ADMIN]))])
def set_config(config: WorkflowConfig, user=Depends(get_current_user)) -> WorkflowConfig:
    store.set_config(config)
    return store.get_config()

@router.post("/requests")
def create_request(req: WorkflowRequest, user=Depends(get_current_user)) -> WorkflowStatus:
    return store.create_request(req)

@router.post("/transition")
def transition(tr: WorkflowTransition, user=Depends(get_current_user)) -> WorkflowStatus:
    status = store.transition(tr)
    if not status:
        raise HTTPException(status_code=400, detail="Invalid transition")
    return status