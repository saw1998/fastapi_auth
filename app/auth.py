from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_db import AsyncSessionLocal
from app.models.user_model import User
from app.manager.user_manager import UserManager
from app.security.jwt import auth_backend
from app.schema.user_schema import UserRead, UserCreate, UserUpdate

# ---------- DB DEPENDENCIES ----------
async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

# ---------- FASTAPI USERS ----------
fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

# Get the users router separately to avoid circular imports
def get_users_router():
    return fastapi_users.get_users_router(
        user_schema=UserRead,
        user_update_schema=UserUpdate,
    )

# Get the auth router separately to avoid circular imports
def get_auth_router():
    return fastapi_users.get_auth_router(auth_backend)

# Get the register router separately to avoid circular imports
def get_register_router():
    return fastapi_users.get_register_router(
        user_schema=UserRead,
        user_create_schema=UserCreate,
    )