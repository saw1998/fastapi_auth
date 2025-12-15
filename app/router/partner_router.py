from fastapi import APIRouter, Depends, HTTPException, status
from app.db.base_db import get_db
from app.main import current_user
from app.models.dish_model import Dish
from app.models.restaurent_model import Restaurent
from app.models.user_model import User
from app.schema.dish_schema import DishCreate
from app.schema.restaurent_schema import RestaurentCreate
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/partner", tags=["partner_previlidge"])

def partner_required(user=Depends(current_user)) -> User:
    if user.role != "partner":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you are not partner"
        )
    return user

@router.post("/restaurent")
async def create_restaurent(payload : RestaurentCreate, user = Depends(partner_required), db : AsyncSession = Depends(get_db)):
    new_restaurent = Restaurent(name=payload.name, partner_id=user.id)
    db.add(new_restaurent)
    await db.commit()
    await db.refresh(new_restaurent)
    return new_restaurent

@router.post("/dish")
async def add_dish(payload : DishCreate, user = Depends(partner_required), db : AsyncSession = Depends(get_db)):
    try:
        new_dish = Dish(name=payload.name, restaurent_id=payload.restaurent_id)
        db.add(new_dish)
        await db.commit()
        await db.refresh(new_dish)
        return new_dish
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Something went wrong: {str(e)}")
