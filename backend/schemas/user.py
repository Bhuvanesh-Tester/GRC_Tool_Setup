from pydantic import BaseModel
from utils.rbac import Role

class User(BaseModel):
    id: str
    email: str
    role: Role