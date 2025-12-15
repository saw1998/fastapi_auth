
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_db import Base
class Restaurent(Base):
    __tablename__ = "restaurent"
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    name : Mapped[str] = mapped_column(index=True)
    partner_id : Mapped[int] = mapped_column(ForeignKey("user.id"))

    # TODO: add condition check that user.role == "partner"
    partner : Mapped["User"] = relationship(back_populates="restaurents")