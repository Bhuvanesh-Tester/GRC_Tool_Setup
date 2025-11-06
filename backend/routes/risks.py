from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from utils.auth import get_current_user
from utils.rbac import require_roles, Role
from utils.demo_store import RisksStore
from utils.db import get_repos
from schemas.risk import RiskCreate, RiskUpdate, RiskOut
from schemas.common import PaginatedResponse

router = APIRouter(prefix="/risks", tags=["risks"])
store = RisksStore()
repos = get_repos()

@router.get("/")
def list_risks(q: Optional[str] = None, skip: int = 0, limit: int = 20, user=Depends(get_current_user)) -> PaginatedResponse[RiskOut]:
    if repos:
        items = repos["risks"].list(q=q, skip=skip, limit=limit)
        total = repos["risks"].count()
        return PaginatedResponse(items=items, total=total)
    items = store.list(q=q, skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=store.count())

@router.post("/", dependencies=[Depends(require_roles([Role.ADMIN, Role.RISK_MANAGER]))])
def create_risk(payload: RiskCreate, user=Depends(get_current_user)) -> RiskOut:
    if repos:
        return repos["risks"].create(payload)
    return store.create(payload)

@router.get("/{risk_id}")
def get_risk(risk_id: int, user=Depends(get_current_user)) -> RiskOut:
    item = repos["risks"].get(risk_id) if repos else store.get(risk_id)
    if not item:
        raise HTTPException(status_code=404, detail="Risk not found")
    return item

@router.put("/{risk_id}", dependencies=[Depends(require_roles([Role.ADMIN, Role.RISK_MANAGER]))])
def update_risk(risk_id: int, payload: RiskUpdate, user=Depends(get_current_user)) -> RiskOut:
    item = repos["risks"].update(risk_id, payload) if repos else store.update(risk_id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="Risk not found")
    return item

@router.delete("/{risk_id}", dependencies=[Depends(require_roles([Role.ADMIN]))])
def delete_risk(risk_id: int, user=Depends(get_current_user)):
    ok = repos["risks"].delete(risk_id) if repos else store.delete(risk_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Risk not found")
    return {"ok": True}