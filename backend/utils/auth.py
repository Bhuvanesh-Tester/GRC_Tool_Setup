import os
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from schemas.user import User
from utils.rbac import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_demo_token(role: str) -> str:
    return f"demo-{role}"

def parse_demo_token(token: str) -> Optional[User]:
    if not token.startswith("demo-"):
        return None
    role = token.replace("demo-", "")
    if role not in [r.value for r in Role]:
        return None
    return User(id="demo-user", email=f"demo@{role}.local", role=Role(role))

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    if demo_mode:
        user = parse_demo_token(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid demo token")
        return user

    secret = os.getenv("SUPABASE_JWT_SECRET")
    if not secret:
        raise HTTPException(status_code=500, detail="JWT secret not configured")
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        email = payload.get("email") or payload.get("sub")
        # Allow configuring a default role when Supabase JWT lacks a role claim
        default_role = os.getenv("DEFAULT_ROLE", Role.VIEWER.value)
        role = payload.get("role", default_role)
        if role not in [r.value for r in Role]:
            role = Role.VIEWER.value
        return User(id=str(payload.get("user_id", "unknown")), email=email or "unknown", role=Role(role))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")