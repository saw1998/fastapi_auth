from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_db import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    role: Mapped[str] = mapped_column(String, nullable=False, default="user")
