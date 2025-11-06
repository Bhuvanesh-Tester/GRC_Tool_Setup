from typing import List, Optional
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from utils.auth import get_current_user
from utils.rbac import require_roles, Role
from utils.demo_store import PoliciesStore
from utils.db import get_repos, get_client
from schemas.policy import PolicyCreate, PolicyUpdate, PolicyOut
from schemas.common import PaginatedResponse

router = APIRouter(prefix="/policies", tags=["policies"])
store = PoliciesStore()
repos = get_repos()

@router.get("/")
def list_policies(q: Optional[str] = None, skip: int = 0, limit: int = 20, user=Depends(get_current_user)) -> PaginatedResponse[PolicyOut]:
    if repos:
        items = repos["policies"].list(q=q, skip=skip, limit=limit)
        total = repos["policies"].count()
        return PaginatedResponse(items=items, total=total)
    items = store.list(q=q, skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=store.count())

@router.post("/", dependencies=[Depends(require_roles([Role.ADMIN, Role.RISK_MANAGER, Role.COMPLIANCE_OFFICER]))])
def create_policy(payload: PolicyCreate, user=Depends(get_current_user)) -> PolicyOut:
    if repos:
        return repos["policies"].create(payload)
    return store.create(payload)

@router.get("/{policy_id}")
def get_policy(policy_id: int, user=Depends(get_current_user)) -> PolicyOut:
    item = repos["policies"].get(policy_id) if repos else store.get(policy_id)
    if not item:
        raise HTTPException(status_code=404, detail="Policy not found")
    return item

@router.put("/{policy_id}", dependencies=[Depends(require_roles([Role.ADMIN, Role.RISK_MANAGER, Role.COMPLIANCE_OFFICER]))])
def update_policy(policy_id: int, payload: PolicyUpdate, user=Depends(get_current_user)) -> PolicyOut:
    item = repos["policies"].update(policy_id, payload) if repos else store.update(policy_id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="Policy not found")
    return item

@router.delete("/{policy_id}", dependencies=[Depends(require_roles([Role.ADMIN]))])
def delete_policy(policy_id: int, user=Depends(get_current_user)):
    ok = repos["policies"].delete(policy_id) if repos else store.delete(policy_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Policy not found")
    return {"ok": True}

@router.post("/{policy_id}/upload")
def upload_policy_file(policy_id: int, file: UploadFile = File(...), user=Depends(get_current_user)) -> PolicyOut:
    item = (repos["policies"].get(policy_id) if repos else store.get(policy_id))
    if not item:
        raise HTTPException(status_code=404, detail="Policy not found")
    if repos:
        client = get_client()
        bucket = os.getenv("SUPABASE_STORAGE_BUCKET", "policy_files")
        path = f"policy_{policy_id}_{file.filename}"
        content = file.file.read()
        client.storage.from_(bucket).upload(path, content)
        public_url = client.storage.from_(bucket).get_public_url(path)
        updated = repos["policies"].update(policy_id, PolicyUpdate(file_url=public_url))
        return updated
    uploads_dir = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, f"policy_{policy_id}_{file.filename}")
    with open(file_path, 'wb') as f:
        f.write(file.file.read())
    updated = store.update(policy_id, PolicyUpdate(file_url=f"/uploads/{os.path.basename(file_path)}"))
    return updated