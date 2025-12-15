from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_db import engine, AsyncSessionLocal, Base
from app.auth import current_user, get_auth_router, get_register_router, get_users_router
from app.router.partner_router import router as partner_router


# ---------- DB DEPENDENCIES ----------
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


@asynccontextmanager
async def lifespan(app : FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

# ---------- ROUTERS ----------
# Auth
app.include_router(
    get_auth_router(),
    prefix="/auth/jwt",
    tags=["auth"],
)

# Registration
app.include_router(
    get_register_router(),
    prefix="/auth",
    tags=["auth"],
)

# Users routes
app.include_router(
    get_users_router(),
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


app.include_router(partner_router)
