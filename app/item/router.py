from typing import List
from fastapi import APIRouter
from app.item.controller import ItemController
from app.item.schema import Item

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

item_controller = ItemController()

@router.get("/", status_code=200, response_model=List[Item])
def list_items():
    return item_controller.list_items()

@router.post("/", status_code=201, response_model=Item)
def create_item(item: Item):
    return item_controller.create_item(item)

@router.put("/{item_id}", status_code=200, response_model=Item)
def update_item(item_id: int, item: Item):
    return item_controller.update_item(item_id, item)

@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int):
    item_controller.delete_item(item_id)
