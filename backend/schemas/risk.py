from typing import Optional
from pydantic import BaseModel, Field

class RiskBase(BaseModel):
    title: str = Field(..., min_length=3)
    description: Optional[str] = None
    impact: int = Field(..., ge=1, le=5)
    likelihood: int = Field(..., ge=1, le=5)
    mitigation: Optional[str] = None
    owner: Optional[str] = None

class RiskCreate(RiskBase):
    pass

class RiskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    impact: Optional[int] = None
    likelihood: Optional[int] = None
    mitigation: Optional[str] = None
    owner: Optional[str] = None

class RiskOut(RiskBase):
    id: int
    score: int