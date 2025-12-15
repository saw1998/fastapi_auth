from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_db import Base


class Dish(Base):
    __tablename__ = "dishes"
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    name : Mapped[str] = mapped_column(nullable=False)
    restaurent_id : Mapped[int] = mapped_column(ForeignKey("restaurent.id"))

    restaurent : Mapped["Restaurent"] = relationship(back_populates="dishes")