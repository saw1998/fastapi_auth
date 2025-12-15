from typing import AsyncGenerator
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_db import engine, AsyncSessionLocal, Base
from app.models.user_model import User
from app.manager.user_manager import UserManager
from app.security.jwt import auth_backend
from app.schema.user_schema import UserRead, UserCreate, UserUpdate

app = FastAPI()


# ---------- DB DEPENDENCIES ----------
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
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


# ---------- ROUTERS ----------
# Auth
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# Registration
app.include_router(
    fastapi_users.get_register_router(
        user_schema=UserRead,
        user_create_schema=UserCreate,
    ),
    prefix="/auth",
    tags=["auth"],
)

# Users routes
app.include_router(
    fastapi_users.get_users_router(
        user_schema=UserRead,
        user_update_schema=UserUpdate,
    ),
    prefix="/users",
    tags=["users"],
)


# ---------- PROTECTED ROUTES ----------
@app.get("/protected")
def protected_route(user=Depends(current_user)):
    return {"message": f"Hello {user.email}", "role": user.role}


# Role-based route
def admin_required(user=Depends(current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return user

@app.get("/admin-only")
def admin_route(user=Depends(admin_required)):
    return {"msg": f"Hello admin {user.email}"}


# ---------- CREATE TABLES ----------
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)