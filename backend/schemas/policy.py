from typing import Optional, List
from pydantic import BaseModel, Field

class PolicyBase(BaseModel):
    title: str = Field(..., min_length=3)
    description: Optional[str] = None
    status: str = "Draft"  # Draft, Under Review, Approved
    reviewers: Optional[List[str]] = None
    file_url: Optional[str] = None

class PolicyCreate(PolicyBase):
    pass

class PolicyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    reviewers: Optional[List[str]] = None
    file_url: Optional[str] = None

class PolicyOut(PolicyBase):
    id: int