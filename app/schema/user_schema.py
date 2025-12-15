from fastapi_users import schemas
from uuid import UUID

class UserRead(schemas.BaseUser[UUID]):
    role: str

class UserCreate(schemas.BaseUserCreate):
    role: str = "user"

class UserUpdate(schemas.BaseUserUpdate):
    role: str | None = None
