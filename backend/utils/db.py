import os
from typing import Any, Dict, List, Optional
from supabase import create_client, Client
from schemas.policy import PolicyCreate, PolicyUpdate, PolicyOut
from schemas.risk import RiskCreate, RiskUpdate, RiskOut
from schemas.compliance import FrameworkCreate, FrameworkUpdate, FrameworkOut

def get_client() -> Optional[Client]:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        return None
    return create_client(url, key)

class PoliciesDB:
    def __init__(self, client: Client):
        self.client = client
        self.table = client.table("policies")

    def list(self, q: Optional[str], skip: int, limit: int) -> List[PolicyOut]:
        query = self.table.select("*")
        if q:
            query = query.ilike("title", f"%{q}%")
        query = query.range(skip, skip + limit - 1)
        data = query.execute().data or []
        return [PolicyOut(**row) for row in data]

    def count(self) -> int:
        res = self.table.select("id", count='exact').execute()
        return res.count or 0

    def create(self, payload: PolicyCreate) -> PolicyOut:
        row = payload.model_dump()
        data = self.table.insert(row).select("*").execute().data[0]
        return PolicyOut(**data)

    def get(self, policy_id: int) -> Optional[PolicyOut]:
        data = self.table.select("*").eq("id", policy_id).maybe_single().execute().data
        return PolicyOut(**data) if data else None

    def update(self, policy_id: int, payload: PolicyUpdate) -> Optional[PolicyOut]:
        row = payload.model_dump(exclude_none=True)
        data = self.table.update(row).eq("id", policy_id).select("*").maybe_single().execute().data
        return PolicyOut(**data) if data else None

    def delete(self, policy_id: int) -> bool:
        res = self.table.delete().eq("id", policy_id).execute()
        return (res.data is not None)

class RisksDB:
    def __init__(self, client: Client):
        self.client = client
        self.table = client.table("risks")

    def list(self, q: Optional[str], skip: int, limit: int) -> List[RiskOut]:
        query = self.table.select("*")
        if q:
            query = query.ilike("title", f"%{q}%")
        query = query.range(skip, skip + limit - 1)
        data = query.execute().data or []
        return [RiskOut(**row) for row in data]

    def count(self) -> int:
        res = self.table.select("id", count='exact').execute()
        return res.count or 0

    def create(self, payload: RiskCreate) -> RiskOut:
        row = payload.model_dump()
        row["score"] = row["impact"] * row["likelihood"]
        data = self.table.insert(row).select("*").execute().data[0]
        return RiskOut(**data)

    def get(self, risk_id: int) -> Optional[RiskOut]:
        data = self.table.select("*").eq("id", risk_id).maybe_single().execute().data
        return RiskOut(**data) if data else None

    def update(self, risk_id: int, payload: RiskUpdate) -> Optional[RiskOut]:
        row = payload.model_dump(exclude_none=True)
        if "impact" in row or "likelihood" in row:
            # fetch existing to recompute score
            existing = self.get(risk_id)
            if not existing:
                return None
            impact = int(row.get("impact", existing.impact))
            likelihood = int(row.get("likelihood", existing.likelihood))
            row["score"] = impact * likelihood
        data = self.table.update(row).eq("id", risk_id).select("*").maybe_single().execute().data
        return RiskOut(**data) if data else None

    def delete(self, risk_id: int) -> bool:
        res = self.table.delete().eq("id", risk_id).execute()
        return (res.data is not None)

class ComplianceDB:
    def __init__(self, client: Client):
        self.client = client
        self.frameworks = client.table("frameworks")
        self.mappings = client.table("control_mappings")

    def list_frameworks(self, q: Optional[str], skip: int, limit: int) -> List[FrameworkOut]:
        query = self.frameworks.select("*")
        if q:
            query = query.ilike("name", f"%{q}%")
        query = query.range(skip, skip + limit - 1)
        data = query.execute().data or []
        # we expect 'control_mappings' as json in frameworks; if not, default {}
        return [FrameworkOut(**{**row, "control_mappings": row.get("control_mappings") or {}}) for row in data]

    def count_frameworks(self) -> int:
        res = self.frameworks.select("id", count='exact').execute()
        return res.count or 0

    def create_framework(self, payload: FrameworkCreate) -> FrameworkOut:
        row = {**payload.model_dump(), "control_mappings": {}}
        data = self.frameworks.insert(row).select("*").execute().data[0]
        data["control_mappings"] = data.get("control_mappings") or {}
        return FrameworkOut(**data)

    def update_framework(self, framework_id: int, payload: FrameworkUpdate) -> Optional[FrameworkOut]:
        row = payload.model_dump(exclude_none=True)
        data = self.frameworks.update(row).eq("id", framework_id).select("*").maybe_single().execute().data
        if not data:
            return None
        data["control_mappings"] = data.get("control_mappings") or {}
        return FrameworkOut(**data)

    def map_controls(self, framework_id: int, mapping: Dict[str, List[int]]) -> bool:
        # store mapping json on frameworks table
        fw = self.frameworks.select("*").eq("id", framework_id).maybe_single().execute().data
        if not fw:
            return False
        control_mappings = fw.get("control_mappings") or {}
        control_mappings.update(mapping)
        self.frameworks.update({"control_mappings": control_mappings}).eq("id", framework_id).execute()
        return True

def get_repos():
    client = get_client()
    if not client:
        return None
    return {
        "policies": PoliciesDB(client),
        "risks": RisksDB(client),
        "compliance": ComplianceDB(client)
    }