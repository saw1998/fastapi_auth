
from pydantic import BaseModel, Field


class DishCreate(BaseModel):
    name : str = Field(min_length=3)
    # this may throw error, id is in base 64 
    restaurent_id : int
