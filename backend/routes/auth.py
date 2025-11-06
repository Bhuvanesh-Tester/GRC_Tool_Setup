import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from utils.auth import get_current_user, create_demo_token
from utils.rbac import Role

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[Role] = None  # used for demo login

@router.post("/login")
def login(payload: LoginRequest):
    demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    if demo_mode:
        if not payload.role:
            raise HTTPException(status_code=400, detail="role required in demo mode")
        token = create_demo_token(payload.role.value)
        return {"access_token": token, "token_type": "bearer", "role": payload.role.value}

    raise HTTPException(status_code=501, detail="Non-demo login not implemented. Configure Supabase.")

@router.get("/me")
def me(user=Depends(get_current_user)):
    return user