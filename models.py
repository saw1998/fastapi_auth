from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String
from db import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
