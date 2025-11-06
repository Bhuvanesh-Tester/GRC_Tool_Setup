from typing import List, Optional, Dict
from schemas.policy import PolicyCreate, PolicyUpdate, PolicyOut
from schemas.risk import RiskCreate, RiskUpdate, RiskOut
from schemas.compliance import FrameworkCreate, FrameworkUpdate, FrameworkOut
from schemas.workflow import WorkflowConfig, WorkflowRequest, WorkflowTransition, WorkflowStatus

class PoliciesStore:
    def __init__(self):
        self._items: Dict[int, PolicyOut] = {}
        self._seq = 1
        # seed
        self.create(PolicyCreate(title="Information Security Policy", description="Base IS policy", status="Approved"))

    def list(self, q: Optional[str] = None, skip: int = 0, limit: int = 20) -> List[PolicyOut]:
        items = list(self._items.values())
        if q:
            items = [i for i in items if q.lower() in i.title.lower()]
        return items[skip: skip + limit]

    def count(self) -> int:
        return len(self._items)

    def create(self, payload: PolicyCreate) -> PolicyOut:
        item = PolicyOut(id=self._seq, **payload.model_dump())
        self._items[self._seq] = item
        self._seq += 1
        return item

    def get(self, policy_id: int) -> Optional[PolicyOut]:
        return self._items.get(policy_id)

    def update(self, policy_id: int, payload: PolicyUpdate) -> Optional[PolicyOut]:
        existing = self._items.get(policy_id)
        if not existing:
            return None
        data = existing.model_dump()
        data.update({k: v for k, v in payload.model_dump(exclude_none=True).items()})
        updated = PolicyOut(**data)
        self._items[policy_id] = updated
        return updated

    def delete(self, policy_id: int) -> bool:
        return self._items.pop(policy_id, None) is not None

class RisksStore:
    def __init__(self):
        self._items: Dict[int, RiskOut] = {}
        self._seq = 1
        # seed
        self.create(RiskCreate(title="Data Breach", description="Unauthorized access", impact=5, likelihood=3))

    def list(self, q: Optional[str] = None, skip: int = 0, limit: int = 20) -> List[RiskOut]:
        items = list(self._items.values())
        if q:
            items = [i for i in items if q.lower() in i.title.lower()]
        return items[skip: skip + limit]

    def count(self) -> int:
        return len(self._items)

    def create(self, payload: RiskCreate) -> RiskOut:
        score = payload.impact * payload.likelihood
        item = RiskOut(id=self._seq, score=score, **payload.model_dump())
        self._items[self._seq] = item
        self._seq += 1
        return item

    def get(self, risk_id: int) -> Optional[RiskOut]:
        return self._items.get(risk_id)

    def update(self, risk_id: int, payload: RiskUpdate) -> Optional[RiskOut]:
        existing = self._items.get(risk_id)
        if not existing:
            return None
        data = existing.model_dump()
        data.update({k: v for k, v in payload.model_dump(exclude_none=True).items()})
        data["score"] = data["impact"] * data["likelihood"]
        updated = RiskOut(**data)
        self._items[risk_id] = updated
        return updated

    def delete(self, risk_id: int) -> bool:
        return self._items.pop(risk_id, None) is not None

class ComplianceStore:
    def __init__(self):
        self._items: Dict[int, FrameworkOut] = {}
        self._seq = 1
        self.create(FrameworkCreate(name="ISO 27001", description="Information Security Management", controls=["A.5.1", "A.8.2"]))

    def list(self, q: Optional[str] = None, skip: int = 0, limit: int = 20) -> List[FrameworkOut]:
        items = list(self._items.values())
        if q:
            items = [i for i in items if q.lower() in i.name.lower()]
        return items[skip: skip + limit]

    def count(self) -> int:
        return len(self._items)

    def create(self, payload: FrameworkCreate) -> FrameworkOut:
        item = FrameworkOut(id=self._seq, control_mappings={}, **payload.model_dump())
        self._items[self._seq] = item
        self._seq += 1
        return item

    def update(self, framework_id: int, payload: FrameworkUpdate) -> Optional[FrameworkOut]:
        existing = self._items.get(framework_id)
        if not existing:
            return None
        data = existing.model_dump()
        data.update({k: v for k, v in payload.model_dump(exclude_none=True).items()})
        updated = FrameworkOut(**data)
        self._items[framework_id] = updated
        return updated

    def map_controls(self, framework_id: int, mapping: Dict[str, List[int]]) -> bool:
        existing = self._items.get(framework_id)
        if not existing:
            return False
        existing.control_mappings.update(mapping)
        self._items[framework_id] = existing
        return True

class WorkflowsStore:
    def __init__(self):
        self._config = WorkflowConfig(role_order=["L1", "L2", "L3"])  # labels not tied to RBAC
        self._requests: Dict[str, WorkflowStatus] = {}

    def get_config(self) -> WorkflowConfig:
        return self._config

    def set_config(self, config: WorkflowConfig):
        self._config = config

    def create_request(self, req: WorkflowRequest) -> WorkflowStatus:
        status = WorkflowStatus(request_id=req.request_id, status="Pending", stage=self._config.role_order[req.current_stage_index])
        self._requests[req.request_id] = status
        return status

    def transition(self, tr: WorkflowTransition) -> Optional[WorkflowStatus]:
        status = self._requests.get(tr.request_id)
        if not status:
            return None
        if tr.action == "approve":
            # move to next stage or approve
            current_index = self._config.role_order.index(status.stage) if status.stage in self._config.role_order else 0
            if current_index + 1 < len(self._config.role_order):
                status.stage = self._config.role_order[current_index + 1]
                status.status = "Pending"
            else:
                status.status = "Approved"
                status.stage = None
            self._requests[tr.request_id] = status
            return status
        elif tr.action == "reject":
            current_index = self._config.role_order.index(status.stage) if status.stage in self._config.role_order else 0
            if current_index - 1 >= 0:
                status.stage = self._config.role_order[current_index - 1]
                status.status = "Pending"
            else:
                status.status = "Rejected"
                status.stage = None
            self._requests[tr.request_id] = status
            return status
        return None