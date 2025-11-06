from enum import Enum
from typing import List
from fastapi import Depends, HTTPException, status

class Role(str, Enum):
    ADMIN = "admin"
    RISK_MANAGER = "risk_manager"
    COMPLIANCE_OFFICER = "compliance_officer"
    AUDITOR = "auditor"
    VIEWER = "viewer"

def require_roles(roles: List[Role]):
    # Import here to avoid circular import at module load time
    from utils.auth import get_current_user

    def dependency(user=Depends(get_current_user)):
        if user is None or getattr(user, "role", None) is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return True

    return dependency