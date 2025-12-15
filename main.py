from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from db import engine, AsyncSessionLocal, Base
from models import User
from users import UserManager
from auth import auth_backend
from schemas import UserRead, UserCreate, UserUpdate

app = FastAPI()


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

# Auth routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# Registration routes
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

# Protected route example
current_user = fastapi_users.current_user()

@app.get("/protected")
def protected_route(user=Depends(current_user)):
    return {"message": f"Hello {user.email}"}


# ---------- CREATE TABLES ----------
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
