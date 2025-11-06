from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from utils.auth import get_current_user
from utils.rbac import require_roles, Role
from utils.demo_store import ComplianceStore
from utils.db import get_repos
from schemas.compliance import FrameworkCreate, FrameworkUpdate, FrameworkOut, ControlMapRequest
from schemas.common import PaginatedResponse

router = APIRouter(prefix="/compliance", tags=["compliance"])
store = ComplianceStore()
repos = get_repos()

@router.get("/frameworks")
def list_frameworks(q: Optional[str] = None, skip: int = 0, limit: int = 20, user=Depends(get_current_user)) -> PaginatedResponse[FrameworkOut]:
    if repos:
        items = repos["compliance"].list_frameworks(q=q, skip=skip, limit=limit)
        total = repos["compliance"].count_frameworks()
        return PaginatedResponse(items=items, total=total)
    items = store.list(q=q, skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=store.count())

@router.post("/frameworks", dependencies=[Depends(require_roles([Role.ADMIN, Role.COMPLIANCE_OFFICER]))])
def create_framework(payload: FrameworkCreate, user=Depends(get_current_user)) -> FrameworkOut:
    if repos:
        return repos["compliance"].create_framework(payload)
    return store.create(payload)

@router.put("/frameworks/{framework_id}", dependencies=[Depends(require_roles([Role.ADMIN, Role.COMPLIANCE_OFFICER]))])
def update_framework(framework_id: int, payload: FrameworkUpdate, user=Depends(get_current_user)) -> FrameworkOut:
    item = repos["compliance"].update_framework(framework_id, payload) if repos else store.update(framework_id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="Framework not found")
    return item

@router.post("/map-controls", dependencies=[Depends(require_roles([Role.ADMIN, Role.COMPLIANCE_OFFICER]))])
def map_controls(payload: ControlMapRequest, user=Depends(get_current_user)):
    ok = repos["compliance"].map_controls(payload.framework_id, payload.control_to_policy) if repos else store.map_controls(payload.framework_id, payload.control_to_policy)
    if not ok:
        raise HTTPException(status_code=404, detail="Framework not found")
    return {"ok": True}