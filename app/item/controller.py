from typing import List
from fastapi import HTTPException
from app.item.schema import Item

class ItemController:
    def __init__(self):
        self.items = [Item(id=1, name="Foo", price=3.4)]

    def list_items(self) -> List[Item]:
        return self.items

    def create_item(self, item: Item) -> Item:
        if item.id is None:
            item.id = len(self.items) + 1
        else:
            for existing_item in self.items:
                if existing_item.id == item.id:
                    raise HTTPException(status_code=400, detail="Item already exists")
        self.items.append(item)
        return item

    def update_item(self, item_id: int, item: Item) -> Item:
        for existing_item in self.items:
            if existing_item.id == item_id:
                existing_item.name = item.name
                existing_item.price = item.price
                existing_item.is_offer = item.is_offer
                return existing_item
        raise HTTPException(status_code=404, detail="Item not found")

    def delete_item(self, item_id: int) -> None:
        for item in self.items:
            if item.id == item_id:
                self.items.remove(item)
                return
        raise HTTPException(status_code=404, detail="Item not found") 