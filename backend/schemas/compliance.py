from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class FrameworkBase(BaseModel):
    name: str = Field(..., min_length=2)
    description: Optional[str] = None
    controls: List[str] = []

class FrameworkCreate(FrameworkBase):
    pass

class FrameworkUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    controls: Optional[List[str]] = None

class FrameworkOut(FrameworkBase):
    id: int
    control_mappings: Dict[str, List[int]] = {}

class ControlMapRequest(BaseModel):
    framework_id: int
    control_to_policy: Dict[str, List[int]]