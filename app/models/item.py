from typing import Union
from pydantic import BaseModel, Field

class Item(BaseModel):
    id: Union[int, None] = None
    name: str
    price: float = Field(gt=3.0)
    is_offer: Union[bool, None] = None 